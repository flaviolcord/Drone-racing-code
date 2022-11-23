from parameters import cv2

# output of subsystem


class Environment:
    #--------------- Obstacle ----------------------
    #Maëlle
    liste_ofset=[-4,-4,-4,-4,-4,-3,-4,-4,-4,-4,-3]
    Pourcentage_vitesse=80
    # Index obstacle dimensions
    # Allocation index for lists obstacle_dimensions = []
    INDEX_DIMENSIONS_HEIGHT = 0
    INDEX_DIMENSIONS_WIDTH = 1
    INDEX_DIMENSIONS_ORIENTATION = 2
    INDEX_DIMENSIONS_OFFSET = 3

    # Obstacle dimensions
    obstacle_dimensions = []

    # ARCH - type 0
    ARCH_HEIGHT = 1.0
    ARCH_WIDTH = 0.0
    ARCH_ORIENTATION = 0
    ARCH_OFFSET = [-4, 0]

    ARCH_DIMENSIONS = [ARCH_HEIGHT, ARCH_WIDTH, ARCH_ORIENTATION, ARCH_OFFSET]

    # TV - type 1
    TV_HEIGHT = 3.0
    TV_WIDTH = 0.0
    TV_ORIENTATION = 0
    TV_OFFSET = [-4, 0]

    TV_DIMENSIONS = [TV_HEIGHT, TV_WIDTH, TV_ORIENTATION, TV_OFFSET]

    # TURN - type 2 (Left, orientation = -1)
    TURN_L_HEIGHT = 1.0
    TURN_L_WIDTH = 0.0
    TURN_L_ORIENTATION = -1
    TURN_L_OFFSET = [-4, 0]

    TURN_L_DIMENSIONS = [TURN_L_HEIGHT, TURN_L_WIDTH, TURN_L_ORIENTATION, TURN_L_OFFSET]

    # TURN - type 3 (Right, orientation = 1)
    TURN_R_HEIGHT = 1.0
    TURN_R_WIDTH = 0.0
    TURN_R_ORIENTATION = 1
    TURN_R_OFFSET = [-4, 0]

    TURN_R_DIMENSIONS = [TURN_R_HEIGHT, TURN_R_WIDTH, TURN_R_ORIENTATION, TURN_R_OFFSET]
    
    # List - Obstacles dimensions

    obstacle_dimensions = [ARCH_DIMENSIONS, TV_DIMENSIONS, TURN_L_DIMENSIONS, TURN_R_DIMENSIONS]

    # Circuit
    nb_obstacles = 0
    list_obstacles = [0, 0, 0, 0] # Positions of the list = id marker, Value of each position = obstacle type {0, 1, 2, 3}

    # Marker
    MARKER_HEIGHT = 0.0
    MARKER_WIDTH = 0.0

    # List offsets

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
        _type_obstacle = Environment.list_obstacles(id)
        _dimensions = Environment.obstacle_dimensions(_type_obstacle)

        return _dimensions

    @classmethod
    def _get_list_obstacle_id(cls):

        return Environment.list_obstacles

    
