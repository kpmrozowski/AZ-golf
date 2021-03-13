project(golf_EBM)

FetchContent_Declare(
        fmt
        GIT_REPOSITORY https://github.com/fmtlib/fmt
        GIT_TAG 7.1.3
)
FetchContent_MakeAvailable(fmt)

add_library(golf_EBM Graph.cpp Assignment.cpp)
target_link_libraries(golf_EBM PUBLIC fmt spdlog)