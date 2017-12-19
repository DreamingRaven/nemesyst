cmake_minimum_required(VERSION 3.9)
project(OpenRecSyst)
set(CMAKE_CXX_STANDARD 11)

# setting version
set(PROJECT_VERSION_MAJOR 0)
set(PROJECT_VERSION_MINOR 0)
set(PROJECT_VERSION_PATCH 0)
set(PROJECT_VERSION ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH})

# find libraries/ packages for use
find_package(Armadillo REQUIRED)
#find_package(mlpack REQUIRED) # mlpack cannot be found normally with previous method
set(MLPACK_LIBRARIES /usr/lib/libmlpack.so) # libmlpack.so specifically found
set(MLPACK_INCLUDE_DIRS /usr/include/mlpack) # specifying mlpack src files directory
include_directories(${ARMADILLO_INCLUDE_DIRS})
include_directories(${MLPACK_INCLUDE_DIRS})

# display key information for debug purposes
message([STATUS] " components:\n\tName \t\t\tVersion \tPath \n\t${PROJECT_NAME} \t${PROJECT_VERSION} \t\tlib: ${CMAKE_BINARY_DIR} src: ${CMAKE_SOURCE_DIR} ")
message("\tCMake \t\t\t${CMAKE_VERSION} \t\t${CMAKE_ROOT} ")
message("\tArmadillo \t\t${ARMADILLO_VERSION_STRING} \tlib: ${ARMADILLO_LIBRARIES} src: ${ARMADILLO_INCLUDE_DIRS}")
message("\tmlPack \t\t\tunknown \tlib: ${MLPACK_LIBRARIES} src: ${MLPACK_INCLUDE_DIRS}") #TODO: find some way to display mlPack information
message("\n") # this message here just to improve expandability

# create executable and link to dynamic libraries
add_executable(${PROJECT_NAME} main.cpp) #TODO: complete wrapper
target_link_libraries(${PROJECT_NAME} ${ARMADILLO_LIBRARIES} ${MLPACK_LIBRARIES}) #TODO: link mlPack