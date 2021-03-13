# Advanced Algorithms WUT - Euclidean Bipartite Matching
The Euclidean Bipartitle Matching algorithm for a golfer-hole problem in c++ cpp.

# Euclidean Bipartite Matching

This repository holds a solution to a problem, which can be reconstructed as a euclidean bipartite matching problem, which me and my friend were tasked to solve. Two versions of the code are provided - one with comments, and one without. The remainer of this README is an explanation of the Problem. The paper regarding the problem, algorithm, results, complexities and proofs is also provided as [paper.pdf](paper.pdf).


## Problem
We were tasked to find the best assignment for balls and holes in the following problem:

>(golf) There are n balls and n ball holes on a golf course. Golfers want to put their ball in one of the holes at the same time. For this purpose, they determine among themselves who is targeting which hole, but in such a way that the tracks of their balls do not cross, which guarantees no ball collisions.
>
>Let us assume that the balls and holes are points on the plane and that no three of these points are collinear and that the paths of the balls are straight line segments. 
>
>Present an O (n ^ 2 * log n) time algorithm for assigning balls to holes so that no two ball paths cross each other.

## Input
Input to the program is given via **stdin**, in the following format:
```
Balls
0.0 0.0
5.0 8.0
4.0 7.0
Holes
0.0 1.0
6.0 7.0
3.0 8.0
```

The Balls columns contains coordinates of balls, which are real numbers. Analogously for Holes.

## Output
The program should output a map of connected points and full length of those connections.


### License
This project is licensed under the MIT License - see the LICENSE.md file for details.
