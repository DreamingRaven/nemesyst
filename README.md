# RavenRecSyst
Experimental recommender system; C++, Python, bash, CMake; TensorFlow, MLpack toolchain.

This experimental recommender system is part of an ongoing masters thesis, which purposely compares the use of 
Generative Adversarial Neural Networks (GANs) with certain other traditional and prevalent machine learning (ML) 
recommender system techniques. This recommender system is evaluated by rating prediction via mean absolute
error (MEA).

Quick references
* [Keystone Paper](https://arxiv.org/pdf/1707.07435.pdf) 
Deep Learning based Recommender System: A Survey and New Perspectives

Quick Definitions (Wiki)
* [ML](https://en.wikipedia.org/wiki/Machine_learning) Machine Learning
* [GAN](https://en.wikipedia.org/wiki/Generative_adversarial_network) Generative Adversarial Networks
* [MEA](https://en.wikipedia.org/wiki/Mean_absolute_error) Mean Absolute Error

## Introduction


---Remove Me---

Incredibly important note:
    In (your chosen installed directory)/OpenRecSyst/CMakeLists.txt:Line(14):set(MLPACK_LIBRARIES x)
    this 'x' needs to be replaced with the compiled binary object location. E.G on linux
    x = /usr/lib/libmlpack.so
