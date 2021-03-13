import argparse
import math
import numpy as np
import matplotlib.pyplot as plt

class Point():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def distance(self, point):
        return math.sqrt(math.pow((self.x - point.x), 2) + math.pow((self.y - point.y), 2))

    def __str__(self):
        return "Point{{{0},{1}}}".format(self.x, self.y)

class Line():
    def __init__(self, p1 = Point, p2 = Point):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return "Line{{{0},{1}}}".format(self.p1, self.p2)

    def getA(self):
        return (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)

    def getB(self):
        return self.p1.y - self.getA() * self.p1.x

    def intersects(self, line):
        # I1, I2 - x- and y-areas - boundaries on x and y axis
        I1 = [min(self.p1.x, self.p2.x), max(self.p1.x, self.p2.x)] # Our line
        I2 = [min(line.p1.x, line.p2.x), max(line.p1.x, line.p2.x)] # Line we compare to

        #print(f"I1 = {I1}, I2 = {I2}")

        Ia = [max(min(self.p1.x, self.p2.x), min(line.p1.x, line.p2.x)), 
                min(max(self.p1.x, self.p2.x), max(line.p1.x, line.p2.x))]

        #print(f"Ia = {Ia}")

        A1 = self.getA()
        A2 = line.getA()
        b1 = self.getB()
        b2 = line.getB()

        #print(f"A1 = {A1}, A2 = {A2}, b1 = {b1}, b2 = {b2}")

        if(A1 == A2):
            return False # Parallel segments, the same coefficient

        Xa = (b2 - b1) / (A1 - A2)
        #print(f"Xa = {Xa}")

        if ((Xa < max(min(self.p1.x,self.p2.x), min(line.p1.x, line.p2.x))) or 
            (Xa > min(max(self.p1.x, self.p2.x), max(line.p1.x, line.p2.x)))):
            return False  # intersection is out of bounds
        else:
            return True

parser = argparse.ArgumentParser()
# parser.add_argument("input_file", help="File path for a file to read")
parser.add_argument("n", help="Points count")
parser.add_argument("rmin", help="Range min (for data generation)")
parser.add_argument("rmax", help="Range max (for data generation)")

args = parser.parse_args()

np.set_printoptions(precision=2)

n = int(args.n)
range_min = int(args.rmin)
range_size = int(args.rmax) - int(args.rmin)

balls = np.random.rand(n, 2) * range_size + range_min
print("Balls:")
print(balls)
print("Holes:")
holes = np.random.rand(n, 2) * range_size + range_min
print(holes)

connections = []

for x in range((len(balls))):
    p1 = Point(balls[x][0], balls[x][1])
    p2 = Point(holes[x][0], holes[x][1])
    connections.append(Line(p1, p2))
    print(f"Connection {x}: {x}-{x+n} [P1,P2]=[{balls[x]}, {holes[x]}]")

for x in range((len(connections))):
    for y in range((len(connections))):
        if(x != y):
            c1 = connections[x]
            c2 = connections[y]
            if(c1.intersects(c2)):
                print(f"{x} {y}")
                print(f"{c1} # {c2}")

# print(f"Input file: {args.input_file}")

# f = open(args.input_file, 'r')
# lines = [line.rstrip('\n') for line in f]
# mode = "balls"

# balls = []
# holes = []

# for line in lines:
#     if line == 'Balls':
#         continue
#     elif line == 'Holes':
#         mode = "holes"
#         continue

#     data = line.split()

#     if mode == "balls":
#         balls.append(Point(data[0], data[1]))
#     else:
#         holes.append(Point(data[0], data[1]))

# print("Balls:")
# for x in range(len(balls)):
#     print(str(balls[x]))
# print("Holes:")
# for x in range(len(holes)):
#     print(str(holes[x]))