#include <spdlog/spdlog.h>
#include <EBM/Graph.h>

int main() {
    spdlog::info("hello world!\n");
    golf::ebm::Graph g(21);
    g.print();

    return 0;
} 