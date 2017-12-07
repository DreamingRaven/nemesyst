cmake_minimum_required(VERSION 3.9)
project(OpenRecSyst)

set(CMAKE_CXX_STANDARD 11)

find_package(Armadillo REQUIRED)
include_directories(${ARMADILLO_INCLUDE_DIRS})
add_executable(OpenRecSyst main.cpp)
target_link_libraries(OpenRecSyst ${ARMADILLO_LIBRARIES})