import time
from parameters import ENV, run_status, FPS, DRONE_POS, RAD2DEG
from subsys_display_view import Display
from subsys_read_cam import ReadCAM
from subsys_read_keyboard import ReadKeyboard
from subsys_markers_detected import MarkersDetected
from subsys_select_target_marker import SelectTargetMarker
from subsys_tello_sensors import TelloSensors, drone_status
from subsys_tello_actuators import TelloActuators
from subsys_visual_control import VisualControl
from parameters import MODE, pygame
from DJITelloPy.djitellopy.tello import Tello
from subsys_environment import Environment
from subsys_obstacles import Obstacles

NB_ITERATION = 1000
DISTANCE_LAST_MARKER = 1000 # 1 m

def setup():
    ENV.status = ENV.REAL # met 2 éléments de la classe ENV à égalité
    TelloSensors.setup()
    TelloActuators.setup(TelloSensors.TELLO)
    ReadCAM.setup()
    Display.setup()
    VisualControl.setup()
    ReadKeyboard.setup()
    MarkersDetected.setup()
    SelectTargetMarker.setup()

def run(compteur, obstacles):
    # run keyboard subsystem
    rc_status_1, key_status, mode_status = ReadKeyboard.run(rc_threshold=20)

    # get keyboard subsystem
    frame, drone_status = TelloSensors.run(mode_status)
    markers_status, frame = MarkersDetected.run(frame)
    marker_status = SelectTargetMarker.run(frame, markers_status, DRONE_POS, obstacles)#offset à définir le jour J
    rc_status_2 = VisualControl.run(marker_status, drone_status,compteur, obstacles)

    if key_status.is_pressed:
        rc_status = rc_status_1
    else:
        rc_status = rc_status_2

    TelloActuators.run(rc_status)

    Display.run(frame,
                Battery=drone_status.battery,
                Roll=drone_status.roll,
                Pitch=drone_status.pitch,
                hauteur=drone_status.hauteur,
                Yaw=drone_status.yaw,
                Mode=mode_status.value,
                LeftRight=rc_status.a,
                ForBack=rc_status.b,
                UpDown=rc_status.c,
                YawRC=rc_status.d,
                id=marker_status.id,
                H_angle=int(marker_status.h_angle * RAD2DEG),
                v_angle=int(marker_status.v_angle * RAD2DEG),
                m_angle=int(marker_status.m_angle * RAD2DEG),
                m_distance=marker_status.m_distance,
                m_height=marker_status.height,
                m_width=marker_status.width,
            
                )

    time.sleep(1 / FPS)
    return marker_status.id, mode_status

def stop():
    Display.stop()
    TelloSensors.stop()
    #TelloActuators.stop()
    #ReadKeyboard.stop()
    MarkersDetected.stop()
    SelectTargetMarker.stop()

#-------------------------- MAIN ----------------------------------------------------

if __name__ == "__main__":
    setup()
    compteur=[]
    # Get zeros vector with size of the number the markers
    for i in range(Environment.get_nb_obstacles()):
        compteur.append(0)

    # Last element for id = -1
    compteur.append(0)
    
     # Object obstacles
    obstacles = Obstacles(Environment.get_obstacles_ids())

    while run_status.value:

        #Run
        id_percu, _mode_status = run(compteur, obstacles)

        # Condition always false
        if(_mode_status.value == MODE.FLIGHT):

            # if id_percu==-1 and compteur[Environment.get_nb_obstacles()] > NB_ITERATION:
            #     Tello.move_forward(DISTANCE_LAST_MARKER)#distance à modifier le jour J
            #     time.sleep(2)
            #     stop()
            #Si le circuit est serré
            
            # Ajouter ou retirer du compteur
            
            if id_percu>0 and id_percu < Environment.get_nb_obstacles():
                print(id_percu)
                if compteur[id_percu]==0 and compteur[id_percu-1]==0:
                    id_percu=-1
            if id_percu == -1:
                id_percu = Environment.get_nb_obstacles()
            if id_percu >= 0 and id_percu <= Environment.get_nb_obstacles():
                compteur[id_percu] = compteur[id_percu]+1
                for j in range(Environment.get_nb_obstacles()):
                    if j != id_percu and compteur[j] > 0 :
                        compteur[j] = compteur[j]-1
            print(compteur)
    
    stop()

