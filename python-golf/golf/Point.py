class Point():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def distance(self, point):
        return math.sqrt(math.pow((self.x - point.x), 2) + math.pow((self.y - point.y), 2))

    def __str__(self):
        return "Point{{{0},{1}}}".format(self.x, self.y)