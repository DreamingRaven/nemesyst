# RavenRecSyst

## Introduction

Experimental recommender system; C++, Python, bash, CMake; TensorFlow, MLpack toolchain.*

This experimental recommender system is part of an ongoing masters thesis, which purposely compares the use of 
Generative Adversarial Neural Networks (GANs) with certain other traditional and prevalent machine learning (ML) 
recommender system techniques. This recommender system is evaluated by the common method of rating prediction 
via mean absolute error (MEA).

This recommender system currentley predicts using the [MovieLense 20M](https://grouplens.org/datasets/movielens/20m/),
 and [Netflix (2007)](https://www.kaggle.com/netflix-inc/netflix-prize-data) datasets. In future this recommender system
  (minus certain data specific steps) will have functionality with databases, specifically mongoDB.

Quick references
* [Keystone Paper](https://arxiv.org/pdf/1707.07435.pdf) - 
Deep Learning based Recommender System: A Survey and New Perspectives [sic]

Quick Definitions (Wiki)
* [ML](https://en.wikipedia.org/wiki/Machine_learning) - Machine Learning
* [GAN](https://en.wikipedia.org/wiki/Generative_adversarial_network) - Generative Adversarial Networks
* [MEA](https://en.wikipedia.org/wiki/Mean_absolute_error) - Mean Absolute Error

*please note, the majority of single run scripts (such as data pre-processing) are done synchronously and in a single 
threaded manner. The TensorFlow and certain C++ implementations for the model building which may need to be repeated
 will however not be single threaded and may not be calculated synchronously.

---Rework Me---

Incredibly important note:
    In (your chosen installed directory)/OpenRecSyst/CMakeLists.txt:Line(14):set(MLPACK_LIBRARIES x)
    this 'x' needs to be replaced with the compiled binary object location. E.G on linux
    x = /usr/lib/libmlpack.so
