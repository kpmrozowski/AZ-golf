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
        plt.annotate(str(i), (np.transpose(balls)[1][i]+.001, np.transpose(balls)[2][i]+.001), fontsize=8)
        plt.annotate(str(n + i), (np.transpose(holes)[1][i]+.001, np.transpose(holes)[2][i]+.001), fontsize=8)

    plt.show()

def to_point(custom_point):
    return Point(custom_point[1], custom_point[2])

def check_intersections(balls, holes, connections):
    n = balls.shape[0]
    for con1 in connections:
        for con2 in connections:
            if con1 != con2 and doIntersect(to_point(balls[con1[0]]), to_point(holes[con1[1]-n]),to_point(balls[con2[0]]), to_point(holes[con2[1]-n])):
                print("INTERSECTION FOUND!")

def plot_connections(balls, holes, connections):
    n = balls.shape[0]
    plt.scatter(np.transpose(balls)[:][1], np.transpose(balls)[:][2])
    plt.scatter(np.transpose(holes)[:][1], np.transpose(holes)[:][2])

    for i in range(n):
        plt.annotate(str(i), (np.transpose(balls)[1][i]+.001, np.transpose(balls)[2][i]+.001), fontsize=8)
        plt.annotate(str(n + i), (np.transpose(holes)[1][i]+.001, np.transpose(holes)[2][i]+.001), fontsize=8)

    for con in connections:
        i1 = int(con[0])
        i2 = int(con[1])-n

        ball = balls[i1,:]
        hole = holes[i2,:]

        plt.plot([ball[1],hole[1]], [ball[2],hole[2]], 'k--', linewidth=1.0)

    # check_intersections(balls, holes, connections)
    plt.show()

def get_mass_center_line_coefficients(balls, holes):
    balls_center = [np.mean(np.transpose(balls)[1][:]), np.mean(np.transpose(balls)[2][:])]
    if not silent_mode: print('balls_center = [{:.2f}, {:.2f}]'.format(balls_center[0], balls_center[1]))
    holes_center = [np.mean(np.transpose(holes)[1][:]), np.mean(np.transpose(holes)[2][:])]
    if not silent_mode: print('holes_center = [{:.2f}, {:.2f}]'.format(holes_center[0], holes_center[1]))

    # y = m*x + b
    m = (holes_center[1] - balls_center[1]) / (holes_center[0] - balls_center[0])
    b = holes_center[1] - m * holes_center[0] # y - m*x

    if not silent_mode: print('y = {:.2f} * x + {:.2f}'.format(m, b))

    return [m, b]

def uv_coordinates(point, R_abarot):
    return R_abarot.dot(point[1:])

def change_coordinate_system(points, m, b):
    # New coordinate system
    n = points.shape[0]
    u = np.array([1, m]) * (m ** 2 + 1) ** (-.5)
    v = np.array([-u[1], u[0]])
    if not silent_mode: 
        print('u = [{:.2f}, {:.2f}]\tv = [{:.2f}, {:.2f}]'.format(u[0], u[1] , v[0], v[1]))
    R = np.array(np.transpose([u, v]))
    if not silent_mode: 
        print('R = \n{}'.format(R))

    # inverse rotation matrix
    R_abarot = np.transpose(R)
    # R_abarot = np.linalg.inv(R)
    if not silent_mode: 
        print('det(R^(-1)) = {}\n'.format(np.linalg.det(R)))

    new_coordinates = np.zeros((n,3))
    for i in range(n):
        uv_point = uv_coordinates(points[i], R_abarot)
        new_coordinates[i] = np.array([points[i][0], uv_point[0], uv_point[1]])
    return new_coordinates

def add_new_connection(connections, ball_index, hole_index):
    if not silent_mode: print(f"  Connection: Ball {ball_index} -> Hole {hole_index}")
    connections.append([ball_index, hole_index])

def divide_into_subproblems(sorted_points, connections, nn, balls_uv, holes_uv):
    pivot_index = -1 # After which point there's a division to two subproblems
    n = int(sorted_points.shape[0] / 2) # current subproblem size

    subproblem_holes = sorted_points[sorted_points[:,0] >= nn]
    subproblem_balls = sorted_points[sorted_points[:,0] < nn]

    if not silent_mode: print(f"Subproblem: pairs={n}, points={2*n}")

    if n == 1: # One connection
        b1_index = int(subproblem_balls[0,0])
        h1_index = int(subproblem_holes[0,0])
        add_new_connection(connections, b1_index, h1_index)
    elif n == 2: # Two connections
        b1 = Point(subproblem_balls[0,1], subproblem_balls[0,2])
        b2 = Point(subproblem_balls[1,1], subproblem_balls[1,2])
        h1 = Point(subproblem_holes[0,1], subproblem_holes[0,2])
        h2 = Point(subproblem_holes[1,1], subproblem_holes[1,2])

        b1_index = int(subproblem_balls[0,0])
        b2_index = int(subproblem_balls[1,0])
        h1_index = int(subproblem_holes[0,0])
        h2_index = int(subproblem_holes[1,0])

        if not doIntersect(b1, h1, b2, h2):
            add_new_connection(connections, b1_index, h1_index)
            add_new_connection(connections, b2_index, h2_index)
        else:
            add_new_connection(connections, b1_index, h2_index)
            add_new_connection(connections, b2_index, h1_index)
    # elif n == 3:
    #     b1 = Point(subproblem_balls[0,1], subproblem_balls[0,2])
    #     b2 = Point(subproblem_balls[1,1], subproblem_balls[1,2])
    #     b3 = Point(subproblem_balls[2,1], subproblem_balls[2,2])

    #     h1 = Point(subproblem_holes[0,1], subproblem_holes[0,2])
    #     h2 = Point(subproblem_holes[1,1], subproblem_holes[1,2])
    #     h3 = Point(subproblem_holes[2,1], subproblem_holes[2,2])

    #     connections.append([b1, h1])
    #     connections.append([b2, h2])
    #     connections.append([b3, h3])

    #     plot_connections(balls_uv, holes_uv, connections)

    #     for con1 in connections:
    #         for con2 in connections:
    #             if con1 != con2:
    #                 print(doIntersect(con1[0], con1[1], con2[0], con2[1]))
    else:
        [m, b] = get_mass_center_line_coefficients(subproblem_balls, subproblem_holes)

        balls_uv = change_coordinate_system(subproblem_balls, m, b)
        holes_uv = change_coordinate_system(subproblem_holes, m, b)

        subproblem_balls = balls_uv
        subproblem_holes = holes_uv

        points_all = np.concatenate((balls_uv, holes_uv)) 
        points_all_byX = points_all[points_all[:,1].argsort(kind='mergesort')]
        points_all_byY = points_all[points_all[:,2].argsort(kind='mergesort')]

        if not silent_mode: 
            print('balls_uv = \t\t\t\tholes_uv =')
            for i in range(n):
                print('{} \t {}'.format(balls_uv[i], holes_uv[i])) 
            print('\npoints_all_byX = \t\t\tpoints_all_byY =')
            for i in range(2*n):
                print('{} \t {}'.format(points_all_byX[i], points_all_byY[i]))

        balls_left_count = 0
        holes_left_count = 0
        pivot_found = False

        sorted_points = points_all_byX

        for i in range(2 * int(n)):
            if sorted_points[i, 0] >= nn:
                holes_left_count = holes_left_count + 1
            else:
                balls_left_count = balls_left_count + 1

            if balls_left_count == holes_left_count:
                pivot_found = True
                pivot_index = i
                subproblem_left = sorted_points[0:i+1,:]
                subproblem_right = sorted_points[i+1:,:]
                if not silent_mode:
                    print(f"  Pivot found by X: Left={len(subproblem_left)},Right={len(subproblem_right)}")
                break
            
        if len(subproblem_left) == 0 or len(subproblem_right) == 0:
            if not silent_mode:
                print(f"  Empty subproblem found. Attempting to find connections by Y.")
            pivot_found = False

        if not pivot_found:
            balls_left_count = 0
            holes_left_count = 0
            pivot_found = False

            sorted_points_by_y = sorted_points[sorted_points[:,2].argsort(kind='mergesort')]
        
            for i in range(2 * int(n)):
                if sorted_points_by_y[i, 0] >= nn:
                    holes_left_count = holes_left_count + 1
                else:
                    balls_left_count = balls_left_count + 1

                if balls_left_count == holes_left_count:
                    if not silent_mode:
                        print(f"  Pivot found by Y: Left={len(subproblem_left)},Right={len(subproblem_right)}")
                    pivot_found = True
                    pivot_index = i
                    subproblem_left = sorted_points_by_y[0:i+1,:]
                    subproblem_right = sorted_points_by_y[i+1:,:]
                    break

        divide_into_subproblems(subproblem_left, connections, nn, balls_uv, holes_uv)
        divide_into_subproblems(subproblem_right, connections, nn, balls_uv, holes_uv)

def main():
    args = parse_arguments()

    np.random.seed(5)

    global n
    global silent_mode

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

    # [m, b] = get_mass_center_line_coefficients(balls, holes)

    # balls_uv = change_coordinate_system(balls, m, b)
    # holes_uv = change_coordinate_system(holes, m, b)
    
    # if not silent_mode:
    #     print('balls_uv = \t\t\t\tholes_uv =')
    #     for i in range(n):
    #         print('{} \t {}'.format(balls_uv[i], holes_uv[i]))
    
    # points_all = np.concatenate((balls_uv, holes_uv)) 
    # points_all_byX = points_all[points_all[:,1].argsort(kind='mergesort')]
    # points_all_byY = points_all[points_all[:,2].argsort(kind='mergesort')]

    points_all = np.concatenate((balls, holes)) 
    points_all_byX = points_all[points_all[:,1].argsort(kind='mergesort')]
    points_all_byY = points_all[points_all[:,2].argsort(kind='mergesort')]

    if not silent_mode:
        print('\npoints_all_byX = \t\t\tpoints_all_byY =')
        for i in range(2*n):
            print('{} \t {}'.format(points_all_byX[i], points_all_byY[i]))

        # plot_data(balls_uv, holes_uv)

    connections = []
    nn = int(points_all_byX.shape[0] / 2)
    points = np.concatenate((balls, holes))
    divide_into_subproblems(points_all_byX, connections, nn, balls, holes)
    
    if not silent_mode:               
        plot_connections(balls, holes, connections)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()