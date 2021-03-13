#ifndef GOLF_GRAPH_H
#define GOLF_GRAPH_H
#include "Constants.h"
#include "../Util/IRandomGenerator.h"
#include <fmt/core.h>
#include <cmath>

namespace golf::ebm {

struct Edge {
    double x;
    double y;
    [[nodiscard]] constexpr double distance() const noexcept {
        return std::pow(std::pow(x, 2) + std::pow(y, 2), 0.5);
    }
};

class Graph {

    std::size_t pair_count;
    std::vector<std::pair<std::size_t, std::size_t>> pairs;

public:
    Graph(std::size_t pair_count);
    
    void print() const noexcept;
    void connect(std::size_t a, size_t b, Edge e);
};

} // namespace golf::ebm

#endif //GOLF_GRAPH_H