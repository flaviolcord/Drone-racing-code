from parameters import DEG2RAD, RAD2DEG
import numpy as np
from DJITelloPy.djitellopy.tello import Tello
from subsys_select_target_marker import marker_status
from parameters import run_status, RUN, MODE, pygame,cv2
import subsys_tello_sensors
import time
import subsys_environment

# output of subsystem

nb_gate=2
id=0
class rc_status:#au debut tout à l'arret
    a = 0
    b = 0
    c = 0
    d = 0
   
class VisualControl:
    KP_LR_CTRL = 0.3
    KP_YAW_CTRL = 0.7
    cmp = 0
    
    @classmethod
    def setup(cls):
        
        pass
    @classmethod
    def run(cls, target_marker, drone_status,compteur, obstacles):# partie à modifier
        
        
        for i in range (1,len(compteur)):
                if compteur[i]<20 and compteur[i-1]>50:
                    idd=i#permet de récupérer le numéro de la prochaine port à passer
                    break
                else:
                    idd=0
        porte_actuelle=idd-1
        if target_marker.id==-1 and compteur[10]<10:
            print("moins de 10 fois perdu")
            rc_status.a=0
            rc_status.b=30
            rc_status.c=0
            rc_status.d=0
            return rc_status
        if target_marker.id == -1:
            rc_status.b=0
            rc_status.c = 0#pas de descente ni de montée
            
            print("la prochaine porte à passer est:",idd,"\n")
            if rc_status.d>=0 and drone_status.hauteur>0:#à changer en fonction de la porte suivant
                rc_status.d = -50
            if rc_status.d<=0 and drone_status.hauteur>0:#à changer en réel
                rc_status.d = 50#int(0.99*rc_status.d)    # yaw_velocity
            rc_status.a = int(0.99*rc_status.a)    # left_right_velocity
            # wait for the drone to pass the last Gate
            
            return rc_status
        
        
          
        # Get the angle and the distance between the marker and the drone
        phi = int(target_marker.m_angle * RAD2DEG)#angle entre le marker et la trajectoire du drone en degré
        distance = marker_status.m_distance#distance au markeur
        
        if compteur[porte_actuelle]>20:
        # Yaw velocity control
            rc_status.d = int(cls.KP_YAW_CTRL * phi)

        # Left/Right velocity control
            DX = distance * np.sin(phi*DEG2RAD)
            rc_status.a = int(cls.KP_LR_CTRL * DX)
        # Forward/Backward velocity control
        rb_threshold = 80# vitesse du drone fixe?
        rc_status.b = rb_threshold - int(rb_threshold * abs(phi)/70)#angle est de 0 quand on se trouve dans la trajectoire de la porte
        print("le drone est au niveau de la porte n°",porte_actuelle, "\n")
        
        hauteur_sup= obstacles(porte_actuelle).height
        
        hauteur_inf=1
        if porte_actuelle==2:
            type_porte=2
        else:
            type_porte=1
        if type_porte==2:
            if drone_status.hauteur<hauteur_sup:
                print(drone_status.hauteur)
                rc_status.c = 20
        else:
            if drone_status.hauteur>hauteur_inf:
                print(drone_status.hauteur)
                rc_status.c=-20

        #rc_status.b=rb_threshold
        # Up/Down velocity control
       # if target_marker.id ==2:
           #if drone_status.hauteur<140:
                #print(drone_status.hauteur)
               # rc_status.c = 20
        #else:
            #if drone_status.hauteur>140:
                #rc_status.c = -20
            #if drone_status.hauteur<100:
              # rc_statusc=30
        

        return rc_status
    @classmethod
    def stop(cls):
        pass
