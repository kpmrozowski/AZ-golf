import Point

def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2

    def __str__(self):
        return "Line{{{0},{1}}}".format(self.p1, self.p2)

    def getA(self):
        return (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)

    def getB(self):
        return self.p1.y - self.getA() * self.p1.x