#include <EBM/Graph.h>

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

Graph::Graph(int _pair_count) : 
pair_count{_pair_count}, 
balls{std::vector<Point>(_pair_count)},
holes{std::vector<Point>(_pair_count)},
edges{std::vector<Edge>(_pair_count)} {
    srand(111);
    Random r;
    for (std::size_t i = 0; i < _pair_count; i++) {
        balls[i].x = r.next_double(10);
        balls[i].y = r.next_double(10);
        balls[i].nr = i;
        holes[i].x = r.next_double(10);
        holes[i].y = r.next_double(10);
        holes[i].nr = _pair_count + i;
    }
    
    // random matching
    for(std::size_t i = 0; i < _pair_count; i++) {
        edges[i].A = holes[i];
        edges[i].B = balls[i];
        edges[i].dist = edges[i].distance();
    }
}

void Graph::print() const noexcept {
    fmt::print("Connections:\n");
    for (std::size_t i = 0; i < pair_count; ++i) {
        fmt::print("connection {}:\t{}-{}\t [A,B] = [({:.2f}, {:.2f}), ({:.2f}, {:.2f})]\t dist: {:.2f}\n", i, edges[i].A.nr, edges[i].B.nr, edges[i].A.x, edges[i].A.y, edges[i].B.x, edges[i].B.y, edges[i].dist);
    }
}

// void Graph::connect(std::size_t a, size_t b, Edge e) {}

} // namespace golf::ebm