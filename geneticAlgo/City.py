import numpy
class City:
    def __init__(self, x, y) :
        self.x = x;
        self.y = y;

    def calc_distance(self, city) :
        distancex = abs(self.x - city.x)
        distancey = abs(self.y - city.y)
        return numpy.sqrt((distancex ** 2) + (distancey **2))
