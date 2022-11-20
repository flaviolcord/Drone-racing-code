from parameters import cv2
from subsys_environment import environment

# output of subsystem

class obstacles:
    list_obstacles = []

    def __init__(cls, list_ids):
        
        for id in list_ids:
            obs = obstacle.__init__(id)
            cls.list_obstacles.append(obs)

    @classmethod
    def _get_obstacle(cls, id):
        return cls.list_obstacles[id]

# subsystem
class obstacle:
    #default values
    id = -1
    height = 0.0
    width = 0.0
    orientation = 0 # orientation = {-1 , 0, 1}, -1 left, 0 unoriented, 1 right
    offset = [-4, 0] #ObS: estudar sinal

    @classmethod
    def __init__(cls, id):
        cls.id = id
        cls._get_dimension_values()

    @classmethod
    def setup(cls):
        pass

    @classmethod
    def run(cls, frame):
        pass

    @classmethod
    def stop(cls):
        pass

    def _get_dimension_values(cls):

        dimensions = environment._get_obstacle_dimensions(cls.id)
        
        cls.height = dimensions(environment.INDEX_DIMENSIONS_HEIGHT)
        cls.width = dimensions(environment.INDEX_DIMENSIONS_WIDTH)
        cls.orientation = dimensions(environment.INDEX_DIMENSIONS_ORIENTATION)
        cls.offset = dimensions(environment.INDEX_DIMENSIONS_OFFSET)


    @classmethod
    def _get_offset(cls):

        # Incorrect !
        _offset = (int(obstacle.offset[0]*obstacle.width), int(obstacle.offset[1]*obstacle.height))

        return _offset
        pass


    
