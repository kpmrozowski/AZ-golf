import argparse
import math
import numpy as np
import matplotlib.pyplot as plt

from .Point import Point
from .Line import Line
from .helpers import doIntersect

def parse_arguments():
    parser = argparse.ArgumentParser()
    # parser.add_argument("input_file", help="File path for a file to read")
    parser.add_argument("n", help="Balls/holes count")
    parser.add_argument("--silent", help="Don't print debug information", dest='silent_mode', action='store_true')
    args = parser.parse_args()

    np.set_printoptions(precision=2)

    return args

def generate_data(n):
    balls = np.random.rand(n, 2)
    holes = np.random.rand(n, 2)

    balls = np.array([ [i, np.random.random(), np.random.random()] for i in range(n) ])
    holes = np.array([ [n + i, np.random.random(), np.random.random()] for i in range(n) ])

    return [balls, holes]

def plot_data(balls, holes):
    n = balls.shape[0]
    plt.scatter(np.transpose(balls)[:][1], np.transpose(balls)[:][2])
    plt.scatter(np.transpose(holes)[:][1], np.transpose(holes)[:][2])

    for i in range(n):
        plt.annotate(str(i), (np.transpose(balls)[1][i]+.01, np.transpose(balls)[2][i]+.01), fontsize=12)
        plt.annotate(str(n + i), (np.transpose(holes)[1][i]+.01, np.transpose(holes)[2][i]+.01), fontsize=12)

    plt.show()

def plot_connections(balls, holes, connections):
    n = balls.shape[0]
    plt.scatter(np.transpose(balls)[:][1], np.transpose(balls)[:][2])
    plt.scatter(np.transpose(holes)[:][1], np.transpose(holes)[:][2])

    for i in range(n):
        plt.annotate(str(i), (np.transpose(balls)[1][i]+.01, np.transpose(balls)[2][i]+.01), fontsize=12)
        plt.annotate(str(n + i), (np.transpose(holes)[1][i]+.01, np.transpose(holes)[2][i]+.01), fontsize=12)

    for con in connections:
        plt.plot([con[0].x,con[1].x], [con[0].y,con[1].y])

    plt.show()

def get_mass_center_line_coefficients(balls, holes):
    balls_center = [np.mean(np.transpose(balls)[1][:]), np.mean(np.transpose(balls)[2][:])]
    print('balls_center = [{:.2f}, {:.2f}]'.format(balls_center[0], balls_center[1]))
    holes_center = [np.mean(np.transpose(holes)[1][:]), np.mean(np.transpose(holes)[2][:])]
    print('holes_center = [{:.2f}, {:.2f}]'.format(holes_center[0], holes_center[1]))

    # y = m*x + b
    m = (holes_center[1] - balls_center[1]) / (holes_center[0] - balls_center[0])
    b = holes_center[1] - m * holes_center[0] # y - m*x

    print('y = {:.2f} * x + {:.2f}'.format(m, b))

    return [m, b]

def uv_coordinates(point, R_abarot):
    return R_abarot.dot(point[1:])

def change_coordinate_system(points, m, b):
    # New coordinate system
    n = points.shape[0]
    u = np.array([1, m]) * (m ** 2 + 1) ** (-.5)
    v = np.array([-u[1], u[0]])
    print('u = [{:.2f}, {:.2f}]\tv = [{:.2f}, {:.2f}]'.format(u[0], u[1] , v[0], v[1]))
    R = np.array(np.transpose([u, v]))
    print('R = \n{}'.format(R))

    # inverse rotation matrix
    R_abarot = np.transpose(R)
    # R_abarot = np.linalg.inv(R)
    print('det(R^(-1)) = {}\n'.format(np.linalg.det(R)))

    new_coordinates = np.zeros((n,3))
    for i in range(n):
        uv_point = uv_coordinates(points[i], R_abarot)
        new_coordinates[i] = np.array([points[i][0], uv_point[0], uv_point[1]])
    return new_coordinates

def divide_into_subproblems(sorted_points, connections, nn, balls_uv, holes_uv):
    pivot_index = -1 # After which point there's a division to two subproblems
    n = sorted_points.shape[0] / 2

    subproblem_holes = sorted_points[sorted_points[:,0] >= nn]
    subproblem_balls = sorted_points[sorted_points[:,0] < nn]

    if n == 1: # One connection
        b1 = Point(subproblem_balls[0,1], subproblem_balls[0,2])
        h1 = Point(subproblem_holes[0,1], subproblem_holes[0,2])
        connections.append([b1, h1])

        plot_connections(balls_uv, holes_uv, connections)
    elif n == 2: # Two connections
        b1 = Point(subproblem_balls[0,1], subproblem_balls[0,2])
        b2 = Point(subproblem_balls[1,1], subproblem_balls[1,2])
        h1 = Point(subproblem_holes[0,1], subproblem_holes[0,2])
        h2 = Point(subproblem_holes[1,1], subproblem_holes[1,2])

        if not doIntersect(b1, h1, b2, h2):
            connections.append([b1, h1])
            connections.append([b2, h2])
        else:
            connections.append([b1, h2])
            connections.append([b2, h1]) # Reversed

        plot_connections(balls_uv, holes_uv, connections)
    elif n == 3:
        b1 = Point(subproblem_balls[0,1], subproblem_balls[0,2])
        b2 = Point(subproblem_balls[1,1], subproblem_balls[1,2])
        b3 = Point(subproblem_balls[2,1], subproblem_balls[2,2])

        h1 = Point(subproblem_holes[0,1], subproblem_holes[0,2])
        h2 = Point(subproblem_holes[1,1], subproblem_holes[1,2])
        h3 = Point(subproblem_holes[2,1], subproblem_holes[2,2])

        connections.append([b1, h1])
        connections.append([b2, h2])
        connections.append([b3, h3])

        plot_connections(balls_uv, holes_uv, connections)

        for con1 in connections:
            for con2 in connections:
                if con1 != con2:
                    print(doIntersect(con1[0], con1[1], con2[0], con2[1]))
    else:
        balls_left_count = 0
        holes_left_count = 0
        pivot_found = False

        for i in range(2 * int(n)):
            if sorted_points[i, 0] >= nn:
                holes_left_count = holes_left_count + 1
            else:
                balls_left_count = balls_left_count + 1

            if balls_left_count == holes_left_count:
                print('PIVOT FOUND by y')
                pivot_found = True
                pivot_index = i
                subproblem_left = sorted_points[0:i+1,:]
                subproblem_right = sorted_points[i+1:,:]

                divide_into_subproblems(subproblem_left, connections, nn, balls_uv, holes_uv)
                divide_into_subproblems(subproblem_right, connections, nn, balls_uv, holes_uv)

                break
        
        if not pivot_found:
            

def main():
    args = parse_arguments()

    n = int(args.n)
    silent_mode = True if args.silent_mode else False

    [balls, holes] = generate_data(n)

    if not silent_mode: 
        print('balls = {}'.format((np.transpose(balls))[:][0]))
        print('        {}'.format([round(x[1], 3) for x in balls]))
        print('        {}'.format([round(x[2], 3) for x in balls]))
        print('holes = {}'.format((np.transpose(holes))[:][0]))
        print('      = {}'.format([round(x[1], 3) for x in holes]))
        print('      = {}'.format([round(x[2], 3) for x in holes]))

        plot_data(balls, holes)

    [m, b] = get_mass_center_line_coefficients(balls, holes)

    balls_uv = change_coordinate_system(balls, m, b)
    holes_uv = change_coordinate_system(holes, m, b)
    
    print('balls_uv = \t\t\t\tholes_uv =')
    for i in range(n):
        print('{} \t {}'.format(balls_uv[i], holes_uv[i]))
    points_all = np.concatenate((balls_uv, holes_uv)) 
    points_all_byX = points_all[points_all[:,1].argsort(kind='mergesort')]
    points_all_byY = points_all[points_all[:,2].argsort(kind='mergesort')]

    print('\npoints_all_byX = \t\t\tpoints_all_byY =')

    for i in range(2*n):
        print('{} \t {}'.format(points_all_byX[i], points_all_byY[i]))

    plot_data(balls_uv, holes_uv)

    connections = []
    nn = points_all_byY.shape[0] / 2
    divide_into_subproblems(points_all_byY, connections, nn, balls_uv, holes_uv)
    
    plot_connections(balls_uv, holes_uv, connections)


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()