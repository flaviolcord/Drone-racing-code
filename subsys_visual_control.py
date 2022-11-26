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
COMPTEUR_VALUE_MIN = 250 #* int(2 - Environment.Pourcentage_vitesse/100) # Etudier ces valeurs

COMPTEUR_LOST_MARKER = 20
COMPTEUR_LAND = 250
conteur_montee_descente=30
# Constants Velocity
VITESSE_B = 50
VITESSE_MONTER = 30
VITESSE_DESCENDRE = 60
VITESSE_ROTATION_PERDU = 60


VITESSE_FOWARD_LAST_OBS = Environment.Pourcentage_vitesse # Id = -1 (last obstacle, else case)

class rc_status:#au debut tout à l'arret
    a = 0
    b = 0
    c = 0
    d = 0
   
class VisualControl:
    KP_LR_CTRL = 0.25 #a modifier le jour J
    KP_YAW_CTRL = 0.5
    cmp = 0
    
    @classmethod
    def setup(cls):
        
        pass
    @classmethod
    def run(cls, target_marker, drone_status, compteur, obstacles):# partie à modifier
  
        # ------------------- Define current porte --------------------------
        """ for i in range (Environment.get_nb_obstacles()-1,1,-1):

            if i == 0:
                continue

            if (compteur[i]> COMPTEUR_VALUE_MIN and compteur[i-1] < COMPTEUR_VALUE_MAX):
                print("\n TEst \n")
                porte_actuelle = i #permet de récupérer le numéro de la prochaine port à passer
                break   
            else:
                #print("oookokok\n")
                porte_actuelle = obstacles.get_last_obs_id() """

        if obstacles.get_last_obs_id() == 0 :
            porte_actuelle = 0
        elif compteur[obstacles.get_last_obs_id()] > COMPTEUR_VALUE_MIN :
            porte_actuelle = obstacles.get_last_obs_id()
        else :
            porte_actuelle = obstacles.get_last_obs_id() - 1

        # Get obstacle values : height and type
        obst = obstacles.get_obstacle(porte_actuelle)
        hauteur_obs = obst.get_height()
        type = obst.get_type()

        #------------- Regler l'HAUTEUR drone ---------------
        if drone_status.hauteur>20 and compteur[porte_actuelle]>conteur_montee_descente:
            if drone_status.hauteur < hauteur_obs:
                rc_status.c = VITESSE_MONTER #pourcentage vitesse de montée 
            if drone_status.hauteur > hauteur_obs:
                rc_status.c = -VITESSE_DESCENDRE
        #-----------------------------------------------------------------
        
        # Checks last obstacle
        if porte_actuelle == (Environment.get_nb_obstacles() - 1) : final_obs_arrived = True
        else: final_obs_arrived = False
        
        #------------- Land condition for circule of the obstacles
        if final_obs_arrived and compteur[0] > int(COMPTEUR_LAND/4) :
                    #Land
                    print("\n Final obstacle arrived \n")
                    mode_status.value = MODE.LAND
                    TelloSensors.run(mode_status)

                    return rc_status
        #-------------------------------------------------------------------

        #------------------ Target marker lost ----------------------------------
        if target_marker.id == -1:
            print(compteur)
            # Drone is going to the last obstacle
            #if obstacles.get_last_obs_id() == (Environment.get_nb_obstacles() - 1) :
            if porte_actuelle == (Environment.get_nb_obstacles() - 1) :
                if (compteur[Environment.get_nb_obstacles()] > COMPTEUR_LAND):
                    #Land
                    print("\n Land command activated \n")
                    mode_status.value = MODE.LAND
                    TelloSensors.run(mode_status)

                    return rc_status
                else:
                    rc_status.a=0 
                    rc_status.b = VITESSE_FOWARD_LAST_OBS # Check velocity !
                    #rc_status.c=0
                    rc_status.d=0

                    return rc_status
                    
            # Drone lost is in the middle of the circuit
            else:

                if (compteur[Environment.get_nb_obstacles()] > COMPTEUR_LOST_MARKER):

                    # Get obstacle values : height and type
                    obst = obstacles.get_obstacle(obstacles.get_last_obs_id())
                    hauteur_obs = obst.get_height()
                    type = obst.get_type()

                    #Regler hauteur
                    if drone_status.hauteur < hauteur_obs:
                        rc_status.c = VITESSE_MONTER #pourcentage vitesse de montée 
                    if drone_status.hauteur > hauteur_obs:
                        rc_status.c = -VITESSE_DESCENDRE

                    rc_status.b = 0 
                    #rc_status.c = 0 #pas de descente ni de montée
                    
                    # Tourner pour trouver le marker 
                    if Environment.get_next_direction(porte_actuelle) >= 0 and drone_status.hauteur > 0 : #à changer en fonction de la porte suivant
                        rc_status.d = VITESSE_ROTATION_PERDU
                    if Environment.get_next_direction(porte_actuelle) < 0 and drone_status.hauteur > 0 : #à changer en réel
                        rc_status.d = - VITESSE_ROTATION_PERDU #int(0.99*rc_status.d)    # yaw_velocity

                    #rc_status.a = int(0.99*rc_status.a)    # left_right_velocity
                    # wait for the drone to pass the last Gate

                    # if drone_status.hauteur<100:
                    #     rc_status.c=20
                    # if drone_status.hauteur>150:
                    #     rc_status.c=-20
                    # return rc_status

                else:
                    rc_status.a=0 
                    rc_status.b = VITESSE_B # Check velocity !
                    #rc_status.c=0
                    rc_status.d=0

                    return rc_status
        # -------------------------------------------------------------------
        
        # Get the angle and the distance between the marker and the drone
        phi = int(target_marker.m_angle * RAD2DEG) #angle entre le marker et la trajectoire du drone en degré
        distance = marker_status.m_distance #distance au markeur
        
        #-------- ------------- Reduire les zig-zags
        print("porte_actuelle : ", porte_actuelle, "Valeur compteur : ", compteur[porte_actuelle])
        rc_status.d = int(cls.KP_YAW_CTRL * phi)
        #Left/Right velocity control
        DX = distance * np.sin(phi*DEG2RAD)
        rc_status.a = int(cls.KP_LR_CTRL * DX)

        #---------- Forward/Backward velocity control -----------------------------
        rb_threshold = Environment.Pourcentage_vitesse # pourcentage de vitesse fixé dans l'environnement
        #rc_status.b = rb_threshold
        if rc_status.d < 15 :
            rc_status.b = rb_threshold
        else:
            rc_status.b = rb_threshold - int(rb_threshold * abs(phi)/70) #angle est de 0 quand on se trouve dans la trajectoire de la porte

        return rc_status

        
    @classmethod
    def stop(cls):
        pass
