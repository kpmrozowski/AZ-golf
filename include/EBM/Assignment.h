#ifndef GOLF_ASSIGNMENT_H
#define GOLF_ASSIGNMENT_H
#include "../Util/IRandomGenerator.h"
#include "Constants.h"
#include "Graph.h"

namespace golf::ebm {

class Assignment {


public:
    Assignment(Graph &graph, util::IRandomGenerator &rand);

    void run();
    void reset();
};

} // namespace golf::ebm

#endif //GOLF_ASSIGNMENT_H