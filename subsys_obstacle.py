from parameters import cv2

# output of subsystem


class obstacle:
    #default values
    id = -1
    height = 0.0
    width = 0.0
    orientation = 0 # orientation = {-1 , 0, 1}, -1 left, 0 unoriented, 1 right
    offset = [-4, 0] #ObS: estudar sinal

# subsystem
class obstacle:

    @classmethod
    def setup(cls):
        pass

    @classmethod
    def run(cls, frame):
        pass

    @classmethod
    def stop(cls):
        pass

    def _get_values(cls, id):
        


    @classmethod
    def _get_offset(cls):

        _offset = (int(obstacle.offset[0]*obstacle.width), int(obstacle.offset[1]*obstacle.height))

        return _offset
        pass


    
