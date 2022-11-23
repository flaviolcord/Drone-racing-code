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
from subsys_environment import Environment
from subsys_obstacles import Obstacles, Obstacle


def setup():
    ENV.status = ENV.SIMULATION
    TelloSensors.setup()
    TelloActuators.setup(TelloSensors.TELLO)
    # ReadCAM.setup()
    Display.setup()
    VisualControl.setup()
    ReadKeyboard.setup()
    MarkersDetected.setup()
    SelectTargetMarker.setup()

def run(obstacles):

    # run keyboard subsystem
    rc_status_1, key_status, mode_status = ReadKeyboard.run(rc_threshold=70)
    # get keyboard subsystem
    frame, drone_status = TelloSensors.run(mode_status)
    markers_status, frame = MarkersDetected.run(frame)
    marker_status = SelectTargetMarker.run(
        frame, markers_status, DRONE_POS, obstacles)
    rc_status_2 = VisualControl.run(marker_status, drone_status)

    if key_status.is_pressed:
        rc_status = rc_status_1
    else:
        rc_status = rc_status_2

    TelloActuators.run(rc_status)

    Display.run(frame,
                Battery=drone_status.battery,
                Roll=drone_status.roll,
                Pitch=drone_status.pitch,
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


def stop():
    Display.stop()
    TelloSensors.stop()
    TelloActuators.stop()
    ReadKeyboard.stop()
    MarkersDetected.stop()
    SelectTargetMarker.stop()


if __name__ == "__main__":

    # Object obstacles
    obstacles = Obstacles(Environment.get_obstacles_ids())

    setup()

    while run_status.value:
        run(obstacles)

    stop()
