import argparse

class Point():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="File path for a file to read")
args = parser.parse_args()

print(f"Input file: {args.input_file}")

f = open(args.input_file, 'r')
lines = [line.rstrip('\n') for line in f]
mode = "balls"

balls = []
holes = []

for line in lines:
    if line == 'Balls':
        continue
    elif line == 'Holes':
        mode = "holes"
        continue

    data = line.split()
    print(data)
    print(mode)

    if mode == "balls":
        balls.append(Point(data[0], data[1]))
    else:
        holes.append(Point(data[0], data[1]))
