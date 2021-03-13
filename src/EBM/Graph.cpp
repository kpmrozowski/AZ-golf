#include <EBM/Graph.h>
#include <spdlog/spdlog.h>

namespace golf::ebm {
    
class Random : public golf::util::IRandomGenerator {
    public:
    double next_double(double max) noexcept override {
        return static_cast<double>(std::rand() % 10000) * max / 10000.0;
    }
    int next_int(int max) noexcept override {
        return std::rand() % max;
    }
};

Graph::Graph(std::size_t _pair_count) : 
pair_count{_pair_count}, 
pairs {std::vector<std::pair<Point, Point>>(_pair_count)} {
    srand(800);
    Random r;
    for (std::size_t i = 0; i < _pair_count; i++) {
        holes[i].x = r.next_double(10);
        holes[i].y = r.next_double(10);
        balls[i].x = r.next_double(10);
        balls[i].y = r.next_double(10);
    }
    
    // random matching
    for(std::size_t i = 0; i < _pair_count; i++) {
        pairs[i].first = holes[i];
        pairs[i].second = balls[i];
    }
}

void Graph::print() const noexcept {
    for (std::size_t i = 0; i < pair_count; ++i) {
    }
}

void Graph::connect(std::size_t a, size_t b, Edge e) {}

} // namespace golf::ebm