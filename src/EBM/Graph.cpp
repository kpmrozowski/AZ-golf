#include <EBM/Graph.h>

namespace golf::ebm {
    
    Graph::Graph(std::size_t _pair_count) : pair_count{_pair_count} {}

    void Graph::print() const noexcept {
        for (std::size_t i = 0; i < pair_count; ++i) {
            fmt::print("vertex connections {}\n", i);
            // for_each_connected(i, [](std::size_t id, const Edge &e) {
            // fmt::print(" {} (fer: {}, dist: {})\n", id, e.distance);
        }
    }

    void Graph::connect(std::size_t a, size_t b, Edge e) {}

} // namespace golf::ebm