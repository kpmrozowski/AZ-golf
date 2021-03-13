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
lines{std::vector<Line>(_pair_count)} {
    srand(115);
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
        lines[i].A = holes[i];
        lines[i].B = balls[i];
        lines[i].dist = lines[i].distance();
    }
}

void Graph::print() const noexcept {
    fmt::print("Connections:\n");
    for (std::size_t i = 0; i < pair_count; ++i) {
        fmt::print("connection {}:\t{}-{}\t [A,B] = [({:.2f}, {:.2f}), ({:.2f}, {:.2f})]\t dist: {:.2f}\n", i, lines[i].A.nr, lines[i].B.nr, lines[i].A.x, lines[i].A.y, lines[i].B.x, lines[i].B.y, lines[i].dist);
    }
}

void Graph::intersects(Line l1, Line l2) {}
// void Graph::connect(std::size_t a, size_t b, Line e) {}

} // namespace golf::ebm