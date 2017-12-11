# OpenRecSyst
Open source C++ recommender system focusing on neural-net; GAN techniques.

# Introduction

# Set up

Incredibly important note:
    In (your chosen installed directory)/OpenRecSyst/CMakeLists.txt:Line(14):set(MLPACK_LIBRARIES x)
    this 'x' needs to be replaced with the compiled binary object location. E.G on linux
    x = /usr/lib/libmlpack.so
