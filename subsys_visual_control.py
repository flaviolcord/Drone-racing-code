from parameters import DEG2RAD, RAD2DEG
import numpy as np
from DJITelloPy.djitellopy.tello import Tello
from subsys_select_target_marker import marker_status
from parameters import run_status, RUN, MODE, pygame,cv2
from subsys_tello_sensors import TelloSensors
import time
from subsys_environment import Environment
from subsys_read_keyboard import mode_status

# output of subsystem

# Compteur values
COMPTEUR_VALUE_MIN = 20 # Etudier ces valeurs
COMPTEUR_VALUE_MAX = 50

COMPTEUR_LOST_MARKER = 20 # 10 pour le reel
COMPTEUR_LAND = 70

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
    def run(cls, target_marker, drone_status, compteur, obstacles):# partie à modifier
        
        
        for i in range (1, Environment.get_nb_obstacles()):
            if (compteur[i] < COMPTEUR_VALUE_MIN) and (compteur[i-1] > COMPTEUR_VALUE_MAX):
                idd = i #permet de récupérer le numéro de la prochaine port à passer
                break
            else:
                idd = 0
    
        if idd != 0 :
            porte_actuelle = idd-1
        else:
            porte_actuelle = 0

        # Foward
        if target_marker.id == -1:
            # Drone is going to the last obstacle
            if obstacles.get_last_obs_id() == (Environment.get_nb_obstacles() - 1) :
                if (compteur[Environment.get_nb_obstacles()] > COMPTEUR_LAND):
                    #Land
                    print("Land condition activated")
                    mode_status.value = MODE.LAND
                    TelloSensors.run(mode_status)

                    return rc_status
                else:
                    rc_status.a=0 
                    rc_status.b=30 # Check velocity !
                    rc_status.c=0
                    rc_status.d=0

                    return rc_status
                    
            # Drone lost is in the middle of the circuit
            else:
                if (compteur[Environment.get_nb_obstacles()] > COMPTEUR_LOST_MARKER):

                    rc_status.b = 0 
                    rc_status.c = 0 #pas de descente ni de montée
                    
                    # Tourner pour trouver le marker 
                    #print("la prochaine porte à passer est:",idd,"\n")
                    if rc_status.d >= 0 and drone_status.hauteur > 0 : #à changer en fonction de la porte suivant
                        rc_status.d = -50
                    if rc_status.d <= 0 and drone_status.hauteur > 0 : #à changer en réel
                        rc_status.d = 50 #int(0.99*rc_status.d)    # yaw_velocity
                    rc_status.a = int(0.99*rc_status.a)    # left_right_velocity
                    # wait for the drone to pass the last Gate

                    return rc_status

                else:
                    rc_status.a=0 
                    rc_status.b=30 # Check velocity !
                    rc_status.c=0
                    rc_status.d=0

                    return rc_status
        
        # Get the angle and the distance between the marker and the drone
        phi = int(target_marker.m_angle * RAD2DEG) #angle entre le marker et la trajectoire du drone en degré
        distance = marker_status.m_distance #distance au markeur
        
        # Reduire les zig-zags
        if compteur[porte_actuelle] > 20 : #ce compteur évite de tourner trop tôt
        # Yaw velocity control
            rc_status.d = int(cls.KP_YAW_CTRL * phi)
        # Left/Right velocity control
            DX = distance * np.sin(phi*DEG2RAD)
            rc_status.a = int(cls.KP_LR_CTRL * DX)

        # Forward/Backward velocity control
        rb_threshold = Environment.Pourcentage_vitesse# pourcentage de vitesse fixé dans l'environnement
        if rc_status.d < 15 :
            rc_status.b = rb_threshold
        else:
            rc_status.b = rb_threshold - int(rb_threshold * abs(phi)/70) #angle est de 0 quand on se trouve dans la trajectoire de la porte
        print("le drone est au niveau de la porte n°",porte_actuelle, "\n")
        
        # Get obstacle values : height and type
        obst = obstacles.get_obstacle(porte_actuelle)
        hauteur_obs = obst.get_height()
        type = obst.get_type()

        print("hauteur de la porte:", hauteur_obs)

        # Regler l'hauteur drone
        if type == Environment.TV_TYPE and drone_status.hauteur < hauteur_obs:
                print("MONTER", drone_status.hauteur)
                rc_status.c=17 #pourcentage vitesse de montée 
        if type != Environment.TV_TYPE and drone_status.hauteur > hauteur_obs:
            print("MONTER", drone_status.hauteur)
            rc_status.c=-15

        return rc_status

        
    @classmethod
    def stop(cls):
        pass
