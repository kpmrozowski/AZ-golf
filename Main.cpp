#include <EBM/Graph.h>

int main() {
    golf::ebm::Graph g(21);
    g.print();
    spdlog::info("hello from spdlog!");
    fmt::print("hello from fmt!\n");

    return 0;
} 