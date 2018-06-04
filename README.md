# RavenRecSyst

## Introduction

Experimental recommender system; C++, Python, bash, CMake, and TensorFlow.

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

Baseline algorithms:
* [kNN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)
[(why)](http://ieeexplore.ieee.org/document/5286031/?reload=true);
 K-nearest neighbors; traditional computer science technique -> comparable
* [SVD](https://en.wikipedia.org/wiki/Singular-value_decomposition);
[(why)](http://ieeexplore.ieee.org/document/5286031/?reload=true);
Singular-value decomposition; hidden latent factors through eigen vectors; Derivative -> 3rd place Netflix prize
* [MF](https://en.wikipedia.org/wiki/Matrix_decomposition)
[(why)](https://link.springer.com/content/pdf/10.1007%2Fs10115-018-1157-2.pdf);
Matrix factorisation; prevalent -> comparable
* [RNN](https://en.wikipedia.org/wiki/Recurrent_neural_network)
[(why)](https://arxiv.org/abs/1707.07435);
traditional neural network technique -> comparable

Compared-to algorithms:
* [LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory); providing a control to directly compare the effect of GANs.
* [LSTM + GAN](https://arxiv.org/abs/1611.09904)

Quick Definitions (Wiki)
* [ML](https://en.wikipedia.org/wiki/Machine_learning) - Machine Learning
* [GAN](https://en.wikipedia.org/wiki/Generative_adversarial_network) - Generative Adversarial Networks
* [MEA](https://en.wikipedia.org/wiki/Mean_absolute_error) - Mean Absolute Error

---

## Installation

Simply: *
````
git clone https://github.com/DreamingRaven/RavenRecSyst
````
You will also have to install/ verify a few key dependancies.

* [MongoDb](https://www.mongodb.com/)
* Python modules:
    * [Pymongo](https://api.mongodb.com/python/current/) for MongoDb
    * [TensorFlow | TensorFlow-gpu](https://www.tensorflow.org/install/) for that juicy machine-learning
    * [Bash](https://www.gnu.org/software/bash/) for simple system level operations
* [GCC](https://gcc.gnu.org/) for compilation of c++ (not currentley needed but soon)
* [CMake](https://cmake.org/) (not currently needed but soon)
* C++ libraries:
    * currentley none but will likeley use C++ soon.

If any have been left out please create an issue and post any log messages.

Other than those that should be all you need, as dependanices have been kept to as few as needed to make a good extensible result.


\* Note: This system is being developed on linux (Arch Linux) and since the focus is not cross platform there has been no checking for windows support, meaning it may need tinkering if you would like to run it on windows, although I have made every attempt to make this as straight forward as possible, with minimal dependencies.

---

## Usage

entry point is ./ravenRecSyst.py

this recommender system should flag any issues with arguments automagically. For a list of what arguments are availiable:
````
**/ravenRecSyst.py -h
````

** is used in place of whatever the path is to the ravenRecSyst file location, since it will vary between systems. e.g the full bash command on my system would be:
````
 ~/RavenRecSyst/ravenRecSyst.py -h
````

standard usage for a localhost server with authentication (auth non optional forced):
````
**/ravenRecSyst.py --user *1* --pass *2* --name *3*
````
or
````
**/ravenRecSyst.py -u *1* --p *2* --N *3*
````
where:
* \*1\* is used in place of your *user* name if this is a new db then desired username.
* \*2\* is used in place of the users *pass* word, as above if new then desired password.
* \*3\* is the *name* of the database to be used or generated

Please see help screen for more options.
