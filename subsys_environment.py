from parameters import cv2

# output of subsystem


class Environment:
    #--------------- Obstacle ----------------------

    # Index obstacle dimensions
    # Allocation index for lists obstacle_dimensions = []
    INDEX_TYPE = 0
    INDEX_HEIGHT = 1
    INDEX_WIDTH = 2
    INDEX_ORIENTATION = 3
    INDEX_OFFSET = 4

    # Obstacle dimensions
    obstacle_dimensions = []

    # ARCH - type 0
    ARCH_TYPE = 0
    ARCH_HEIGHT = 0.0
    ARCH_WIDTH = 0.0
    ARCH_ORIENTATION = 0
    ARCH_OFFSET = [-4, 0]

    ARCH_DIMENSIONS = [ARCH_TYPE, ARCH_HEIGHT, ARCH_WIDTH, ARCH_ORIENTATION, ARCH_OFFSET]

    # TV - type 1
    TV__TYPE = 1
    TV_HEIGHT = 0.0
    TV_WIDTH = 0.0
    TV_ORIENTATION = 0
    TV_OFFSET = [-4, 0]

    TV_DIMENSIONS = [TV__TYPE, TV_HEIGHT, TV_WIDTH, TV_ORIENTATION, TV_OFFSET]

    # TURN - type 2
    TURN_LEFT_TYPE = 2
    TURN_LEFT_HEIGHT = 0.0
    TURN_LEFT_WIDTH = 0.0
    TURN_LEFT_ORIENTATION = 0
    TURN_LEFT_OFFSET = [-4, 0]

    TURN_LEFT_DIMENSIONS = [TURN_LEFT_TYPE, TURN_LEFT_HEIGHT, TURN_LEFT_WIDTH, TURN_LEFT_ORIENTATION, TURN_LEFT_OFFSET]

    # TURN - type 3
    TURN_RIGHT_TYPE = 3
    TURN_RIGHT_HEIGHT = 0.0
    TURN_RIGHT_WIDTH = 0.0
    TURN_RIGHT_ORIENTATION = 0
    TURN_RIGHT_OFFSET = [-4, 0]

    TURN_RIGHT_DIMENSIONS = [TURN_RIGHT_TYPE, TURN_RIGHT_HEIGHT, TURN_RIGHT_WIDTH, TURN_RIGHT_ORIENTATION, TURN_RIGHT_OFFSET]
    
    # List - Obstacles dimensions

    obstacle_dimensions = [ARCH_DIMENSIONS, TV_DIMENSIONS, TURN_LEFT_DIMENSIONS, TURN_RIGHT_DIMENSIONS]

    # Circuit
    list_obstacles = [2, 3, 0, 0] # Positions of the list = id marker, Value of each position = obstacle type {0, 1, 3}

    # Marker
    MARKER_HEIGHT = 0.0
    MARKER_WIDTH = 0.0

    def get_obstacle_dimensions(id):
        _type_obstacle = Environment.list_obstacles[id]
        _dimensions = Environment.obstacle_dimensions[_type_obstacle]

        return _dimensions

    def get_obstacles_ids(): return Environment.list_obstacles

    def get_nb_obstacles(): return len(Environment.list_obstacles)

    
