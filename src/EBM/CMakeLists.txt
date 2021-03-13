project(golf_EBM)

add_library(golf_EBM Graph.cpp Assignment.cpp)
target_link_libraries(golf_EBM PUBLIC fmt spdlog)