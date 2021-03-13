#ifndef GOLF_GRAPH_H
#define GOLF_GRAPH_H
#include "Constants.h"
#include "../Util/IRandomGenerator.h"
#include <fmt/core.h>
#include <spdlog/spdlog.h>
#include <cmath>

namespace golf::ebm {

struct Point {
    double x, y;
    std::size_t nr;
};

struct Edge {
    Point A, B;
    double dist;
    [[nodiscard]] constexpr double distance() const noexcept {
        return std::pow(std::pow(A.x - B.x, 2) + std::pow(A.y - B.y, 2), 0.5);
    }
};

class Graph {
    
    std::vector<Point> balls;
    std::vector<Point> holes;
    int pair_count;
    std::vector<Edge> edges;

public:
    Graph(int pair_count);
    
    void print() const noexcept;
    // void connect(std::size_t a, size_t b, Edge e);
};

} // namespace golf::ebm

#endif //GOLF_GRAPH_H