from parameters import cv2
from subsys_environment import Environment

# output of subsystem

class Obstacles:
    list_obstacles = []

    def __init__(self, list_ids):

        for id in range(len(list_ids)):
            obs = Obstacle(id)
            self.list_obstacles.append(obs)

    def get_list_obstacles(self):
        return self.list_obstacles

    def get_obstacle(self, id):
        return self.list_obstacles[id]

# subsystem
class Obstacle:

    #default values
    id = -1
    obs_type = -1
    height = 0.0
    width = 0.0
    orientation = 0 
    offset = [-2, 0] 


    def __init__(self, id):
        self.id = id

        dimensions = Environment.get_obstacle_dimensions(id)
        
        self.obs_type = dimensions[Environment.INDEX_TYPE]
        self.height = dimensions[Environment.INDEX_HEIGHT]
        self.width = dimensions[Environment.INDEX_WIDTH]
        self.orientation = dimensions[Environment.INDEX_ORIENTATION]
        self.offset = dimensions[Environment.INDEX_OFFSET]

        # Correction target point for obstacles type 2
        signal = -1  if (self.obs_type == Environment.TURN_RIGHT_TYPE) else 1
        self.offset[0] *= signal

    # Gets
    def get_type(self): return self.obs_type

    def get_offset(self): return self.offset

    @classmethod
    def setup(cls):
        Environment.get_obstacles_ids()
        pass

    @classmethod
    def run(cls, frame):
        pass

    @classmethod
    def stop(cls):
        pass

    def _get_offset(self):
        pass


    
