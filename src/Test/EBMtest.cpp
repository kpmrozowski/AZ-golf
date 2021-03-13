#include <EBM/Assignment.h>
#include <Util/IRandomGenerator.h>
#include <gtest/gtest.h>

/* Random coordinates generator */
class Random : public golf::util::IRandomGenerator {
 public:
   double next_double(double max) noexcept override {
      return static_cast<double>(std::rand() % 10000) * max / 10000.0;
   }

   int next_int(int max) noexcept override {
      return std::rand() % max;
   }
};

/* Euclidean Bipartite Matching algorithm test */
TEST(EBM, BasicGraph) {
   Random r;

   golf::ebm::Graph graph(7);

   golf::ebm::Assignment Assignment(graph, r);
   for (std::size_t i = 0; i < 10; ++i) {
      Assignment.run();
      Assignment.reset();
   }
}

static std::size_t find_overall_length(golf::ebm::Graph &graph, std::size_t starting_pair) {
   std::size_t current_pair = starting_pair;
   std::size_t path_length = 0;
   while (current_pair != 0 && false) {
      ++path_length;
   }
   return path_length;
}

TEST(EBM, RandomGraph) {
   srand(800);
   Random r;

   golf::ebm::Graph graph(50);
   //graph.connect(r.next_int(50), r.next_int(50), {1.0, r.next_double(10.0)});

   srand(111);
   golf::ebm::Assignment Assignment(graph, r);
   for (std::size_t i = 0; i < 100; ++i) {
      Assignment.run();
      Assignment.reset();
   }

   graph.print();

   ASSERT_EQ(find_overall_length(graph, 49), 2);
   ASSERT_EQ(find_overall_length(graph, 30), 5);
   ASSERT_EQ(find_overall_length(graph, 2), 5);
}
