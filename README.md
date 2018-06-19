# RavenRecSyst

Warning: this project has not yet reached it basic intended functionality, to be ready for normal usage will take time so some of the examples may not work currently. If you see anything glaringly wrong please do open an issue, thanks. GR
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
    * [Keras](https://github.com/keras-team/keras) although tensorflow has recentley bundled its own keras
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
**/ravenRecSyst.py --user *1* --pass *2* --name *3* --toInitDb --toStartDb
````
or
````
**/ravenRecSyst.py -u *1* --p *2* --N *3* -i -S
````
where:
* \*1\* is used in place of your *user* name if this is a new db then desired username.
* \*2\* is used in place of the users *pass* word, as above if new then desired password.
* \*3\* is the *name* of the database to be used or generated

And:
* --user / -u is an an argument which allows you to then set the username which will be used in any subsequent operations E.G --toInitDb + --user will attempt to add that user to the database.
* --pass / -p is a similar argument to --user except for the users password.
* --name / -N sets what the database name is which will effect all operations that referance this name.
* --toInitDb / -i is a flag with no subsequent argument, these kind of flags allow you to control what this sytem does, in this case initialising the database with a username password and a database name. --toInitDb only needs to be run once for each database you want to set up/ user.
* --toStartDb / -s is much like --toInitDb except this actually starts the database wheras --toInitDb just sets it up, with username password and allows for it to be authentacatable. Please note however, --toStartDb always starts the database with authentication requirements, to reduce accessability where not needed.

lastly as above, for debugging purposes there is a logger with log levels:
* -1 = Always shown + formatting
*  0 = [INFO] information on current operation
*  1 = [WARN] shows warnings of current operation
*  2 = [ERROR] shows all errors of current operation
*  3 = [DEBUG] a special mode that runs outside of main try catch and shows very verbose system operation

To use this logger simply add option -v OR --loglevel with the desired level. Anything less than that level will also be shown, so level 2 will show [ERROR], [WARN], [INFO] and formatting messages, but not [DEBUG] messages.
E.G to show all possible messages in most verbose state:
````
**/ravenRecSyst.py -u *1* --p *2* --N *3* --loglevel 9001
````
("over nine thousand!") will show all log levels < 9000
Note on log levels: loglevels > 3 will run outside of main try-catch statement for extra verbosity.

---

## Closing examples
for user 'georgeraven' creating 'GeorgeRaven' user with 'password' password, in database 'mehDatabaseName', who desires to debug at log level '3' and to launch database:
````
/home/georgeraven/RavenRecSyst/ravenRecSyst.py -u GeorgeRaven -p password -N mehDatabaseName -v 3 -i -S
````

Please see help screen for more options there are many more but these are the main ones for localhost usage.
