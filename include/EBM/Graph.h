#ifndef GOLF_GRAPH_H
#define GOLF_GRAPH_H
#include "Constants.h"
#include "../Util/IRandomGenerator.h"
#include <fmt/core.h>
#include <cmath>

namespace golf::ebm {

struct Point {
    double x, y;
};

struct Edge {
    Point A, B;
    [[nodiscard]] constexpr double distance() const noexcept {
        return std::pow(std::pow(A.x - B.x, 2) + std::pow(A.y - B.y, 2), 0.5);
    }
};

class Graph {
    
    std::vector<Point> balls;
    std::vector<Point> holes;
    std::size_t pair_count;
    std::vector<std::pair<Point, Point>> pairs;

public:
    Graph(std::size_t pair_count);
    
    void print() const noexcept;
    void connect(std::size_t a, size_t b, Edge e);
};

} // namespace golf::ebm

#endif //GOLF_GRAPH_H