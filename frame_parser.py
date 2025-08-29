import math

class Signal(object):
    x:float = 0
    y:float = 0
    activity:float = 0
    
    id:int
    angle:float

    def __init__(self):
        pass

    def readFrame(self,frame:dict):
        self.id = frame['id']
        self.x+=frame['x']
        self.y+=frame['y']
        self.activity+=frame['activity']

    def clear(self):
        self.x=0
        self.y=0
        self.activity=0

    def normalize(self, denominator:int):
        self.x = self.x/denominator
        self.y = self.y/denominator
        self.activity = self.activity/denominator
    
    def getAngle(self):
        self.angle = math.degrees(math.atan2(self.y,self.x))+120


