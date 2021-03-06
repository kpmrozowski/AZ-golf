cmake_minimum_required(VERSION 3.16)
project(golf)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
set(CMAKE_CXX_FLAGS "-Wall -Wextra -Wpedantic")

include(FetchContent)

FetchContent_Declare(
        spdlog
        GIT_REPOSITORY https://github.com/gabime/spdlog
        GIT_TAG v1.8.2
)
FetchContent_MakeAvailable(spdlog)

FetchContent_Declare(
        fmt
        GIT_REPOSITORY https://github.com/fmtlib/fmt
        GIT_TAG 7.1.3
)
FetchContent_MakeAvailable(fmt)

FetchContent_Declare(
        gtest
        GIT_REPOSITORY https://github.com/google/googletest
        GIT_TAG release-1.10.0
)
FetchContent_MakeAvailable(gtest)

include_directories(./include)

add_subdirectory(src/EBM)
add_subdirectory(src/Test)
add_subdirectory(QtGui)
add_executable(${PROJECT_NAME} 
        Main.cpp
        # QtGui/main.cpp
        src/EBM/Graph.cpp
        src/EBM/Assignment.cpp)
target_link_libraries(golf PUBLIC fmt spdlog)
