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



def setup():
    ENV.status = ENV.SIMULATION # met 2 éléments de la classe ENV à égalité
    TelloSensors.setup()
    TelloActuators.setup(TelloSensors.TELLO)
    ReadCAM.setup()
    Display.setup()
    VisualControl.setup()
    ReadKeyboard.setup()
    MarkersDetected.setup()
    SelectTargetMarker.setup()


def run(compteur):
    # run keyboard subsystem
    rc_status_1, key_status, mode_status = ReadKeyboard.run(rc_threshold=20)
    # get keyboard subsystem
    frame, drone_status = TelloSensors.run(mode_status)
    markers_status, frame = MarkersDetected.run(frame)
    marker_status = SelectTargetMarker.run(frame, markers_status, DRONE_POS, offset=(-6.5, 0))#offset à définir le jour J
    rc_status_2 = VisualControl.run(marker_status, drone_status,compteur)

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
                haut_angle=marker_status.haut_angle,
                offset=marker_status.offset_longueur
                )

    time.sleep(1 / FPS)
    return marker_status.id

def stop():
    Display.stop()
    TelloSensors.stop()
    TelloActuators.stop()
    ReadKeyboard.stop()
    MarkersDetected.stop()
    SelectTargetMarker.stop()
compteur=[0,0,0,0,0,0,0,0,0,0,0]
if __name__ == "__main__":
    setup()

    while run_status.value:
       
        print("compteur",compteur,"\n")
        id_percu=run(compteur)
        if id_percu==-1:
            id_percu=10
        if id_percu>=0 and id_percu<=10:
            compteur[id_percu]=compteur[id_percu]+1
            for j in range(len(compteur)):
                if j!=id_percu and compteur[j]>0:
                    compteur[j]=compteur[j]-1
            print("iddd",compteur,"\n")
        if id_percu==-1 and compteur[2]>100 and compteur[1]>100:
            Tello.move_forward(1000)#distance à modifier le jour J
            time.sleep(2)
            stop()
    
    stop()

