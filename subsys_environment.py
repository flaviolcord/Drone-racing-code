from parameters import cv2

# output of subsystem


class environment:
    #--------------- Obstacle ----------------------

    # Index obstacle dimensions
    # Allocation index for lists obstacle_dimensions = []
    INDEX_DIMENSIONS_HEIGHT = 0
    INDEX_DIMENSIONS_WIDTH = 1
    INDEX_DIMENSIONS_ORIENTATION = 2
    INDEX_DIMENSIONS_OFFSET = 3

    # Obstacle dimensions
    obstacle_dimensions = []

    # ARCH - type 0
    ARCH_HEIGHT = 0.0
    ARCH_WIDTH = 0.0
    ARCH_ORIENTATION = 0
    ARCH_OFFSET = [-4, 0]

    ARCH_DIMENSIONS = [ARCH_HEIGHT, ARCH_WIDTH, ARCH_ORIENTATION, ARCH_OFFSET]

    # TV - type 1
    TV_HEIGHT = 0.0
    TV_WIDTH = 0.0
    TV_ORIENTATION = 0
    TV_OFFSET = [-4, 0]

    TV_DIMENSIONS = [TV_HEIGHT, TV_WIDTH, TV_ORIENTATION, TV_OFFSET]

    # TURN - type 3
    TURN_HEIGHT = 0.0
    TURN_WIDTH = 0.0
    TURN_ORIENTATION = 0
    TURN_OFFSET = [-4, 0]

    TURN_DIMENSIONS = [TURN_HEIGHT, TURN_WIDTH, TURN_ORIENTATION, TURN_OFFSET]
    
    # List - Obstacles dimensions

    obstacle_dimensions = [ARCH_DIMENSIONS, TV_DIMENSIONS, TURN_DIMENSIONS]

    # Circuit
    nb_obstacles = 0
    list_obstacles = [0, 1, 0] # Positions of the list = id marker, Value of each position = obstacle type {0, 1, 3}

    # Marker
    MARKER_HEIGHT = 0.0
    MARKER_WIDTH = 0.0

    @classmethod
    def setup(cls):
        pass

    @classmethod
    def run(cls, frame):
        pass

    @classmethod
    def stop(cls):
        pass

    @classmethod
    def _get_obstacle_dimensions(cls, id):
        _type_obstacle = environment.list_obstacles(id)
        _dimensions = environment.obstacle_dimensions(_type_obstacle)

        return _dimensions

    
