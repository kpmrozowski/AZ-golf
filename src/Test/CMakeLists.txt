project(golf_Test)

add_library(golf_Test EBMtest.cpp)
# add_executable(golf_Test EBMtest.cpp)
target_link_libraries(golf_Test PUBLIC fmt)