#include <iostream>
#include <armadillo>
#include <mlpack/core.hpp> // please make sure path is set properly in CMakeLists.txt

int main(int argc, char** argv) {

    // process command line arguments

    // defining data object
    arma::mat data;
    // filling data object
    mlpack::data::Load("../DataSets/ml-20m/ratings.csv", data, true);

    // test output
    std::cout << "Hello, World!" << std::endl;
    return 0;
}