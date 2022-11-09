from parameters import DEG2RAD, RAD2DEG
import numpy as np
from DJITelloPy.djitellopy.tello import Tello
from subsys_select_target_marker import marker_status
from parameters import run_status, RUN, MODE, pygame

# output of subsystem

nb_gate=2
id=0
class rc_status:#au debut tout à l'arret
    a = 0
    b = 0
    c = 0
    d = 0
    

# subsystem
class VisualControl:
    KP_LR_CTRL = 0.2
    KP_YAW_CTRL = 0.5
    cmp = 0
    @classmethod
    def setup(cls):
        pass
    @classmethod
    def run(cls, target_marker, drone_status,id):# partie à modifier
        
        if target_marker.id >0:
            id=target_marker.id
            print(id)
        if target_marker.id == -1:
            rc_status.c = 0#pas de descente ni de montée
            
            
            if rc_status.d>0:
                rc_status.b = -10
            else:
                rc_status.b = 10#int(0.99*rc_status.d)    # yaw_velocity
            rc_status.a = int(0.99*rc_status.a)    # left_right_velocity
            # wait for the drone to pass the last Gate
            if cls.cmp > 10:
                rc_status.b = int(0.99*rc_status.b)  # for_back_velocity

            cls.cmp = cls.cmp + 1
            return rc_status
        cls.cmp = 0
        if target_marker.id==-1 and id >= nb_gate:#arreter le drone à la fin du circuit
            print(1)
            #MODE.LAND
        # Get the angle and the distance between the marker and the drone
        phi = int(target_marker.m_angle * RAD2DEG)#angle entre le marker et la trajectoire du drone en degré
        distance = target_marker.m_distance#distance au markeur
        
        # Yaw velocity control
        rc_status.d = int(cls.KP_YAW_CTRL * phi)

        # Left/Right velocity control
        DX = distance * np.sin(phi*DEG2RAD)
        rc_status.a = int(cls.KP_LR_CTRL * DX)
        # Forward/Backward velocity control
        rb_threshold = 20# vitesse du drone fixe?
        #rc_status.b = rb_threshold - int(rb_threshold * abs(phi)/70)#angle est de 0 quand on se trouve dans la trajectoire de la porte
        rc_status.b=rb_threshold
        print("phi   ",phi)
        print("statut ",rc_status.b)
        # Up/Down velocity control
        if target_marker.id ==2:
            if drone_status.hauteur<4 and distance<260:
                print(drone_status.hauteur)
                rc_status.c = 20
        else:
            if drone_status.hauteur>2:
                rc_status.c = -20
        

        return rc_status
    @classmethod
    def stop(cls):
        pass
