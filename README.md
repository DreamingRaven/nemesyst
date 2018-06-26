# RavenRecSyst

Warning: this project has not yet reached it basic intended functionality, to be ready for normal usage will take time so some of the examples may not work currently. If you see anything glaringly wrong please do open an issue, thanks. GR

## Introduction

Experimental generalisable recommender system; C++, Python, bash, CMake, and TensorFlow.

This experimental recommender system is part of an ongoing masters thesis, which purposely compares the use of
Generative Adversarial Neural Networks (GANs) with certain other traditional and prevalent machine learning (ML)
recommender system techniques. This recommender system is evaluated by the common method of rating prediction
via mean absolute error (MEA).

Along the way however I decided to make everything as configurable/ generalisable as possible. This recommender system allows for custom cleaning script calls, and custom machine learning scripts all while the nuanced operations are completed automagically, such as transforming then loading the chosen data into mongoDB, allowing for interesting distributed applications to do with combining mongodb with machine learning. The use of mongodb also allows this program to act clay-like, keeping track of program state to be reloaded, reused, monitored etc, just as clay would keep the shape impressed upon it. It keeps track of each model trained, as a seperate document in the models collection, with the models binary also being saved so it can be directly replayed with simple calls.

This recommender system used to predict exclusiveley using [MovieLense 20M](https://grouplens.org/datasets/movielens/20m/),
 and [Netflix (2007)](https://www.kaggle.com/netflix-inc/netflix-prize-data) datasets. Now however it can predict using any data set, given an appropriate cleaning script path to the -c / --cleaner argument.

If you are interested in the masters itself the plan was to explicitly compare recommender system algorithms with newer neural network approaches, although this program can use any supplied algorithm. Find below some specifics...

Quick references
* [Keystone Paper](https://arxiv.org/pdf/1707.07435.pdf) -
Deep Learning based Recommender System: A Survey and New Perspectives [sic]

Baseline algorithms (most will be removed as they are just masters specific functions, except RNN):
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

If any have been left out please create an issue and post any log messages.

Other than those that should be all you need, as dependanices have been kept to as few as needed to make a good extensible result.


\* Note: This system is being developed on linux (Arch Linux) and since the focus is not cross platform there has been no checking for windows support, meaning it may need tinkering if you would like to run it on windows, although I have made every attempt to make this as straight forward as possible, with minimal dependencies and sanitising paths for cross platform use.

---

## Usage

entry point is ./ravenRecSyst.py

this recommender system should flag any issues with arguments automagically. For a list of what arguments are availiable:
````
**/ravenRecSyst.py -h
````

** is used in place of whatever the path is to the RavenRecSyst root directory location, since it will vary between systems. e.g the full bash command on my system would be:
````
 ~/RavenRecSyst/ravenRecSyst.py -h
````
where '~' is expanded by bash to /home/whateverYourUserNameIs

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
*  3 = [DEBUG] main debugging level, displays all availiable debug prints and statements
*  4 = [noTry] a special log level, that runs recSyst outside of main try catch for full, verbose information on any errors

To use this logger simply add option -v OR --loglevel with the desired level. Anything less than that level will also be shown, so level 2 will show [ERROR], [WARN], [INFO] and formatting messages, but not [DEBUG] messages.
E.G to show all possible messages in most verbose state:
````
**/ravenRecSyst.py -u *1* --p *2* --N *3* --loglevel 9001
````
("over nine thousand!") 9001 will show all log levels < 9001

---

## Application Specific Customisation

RavenRecSyst includes customisable modules that should be used to get the
functionality you need. These modules should be executable and will be called
by RavenRecSyst to do data/ application specific operations.

There will be 4 such modules; these were included since there is no way to
create things such as a universal dataset cleaner, as each data set has its own
nuances.

### Cleaning
RavenRecSyst supports arbitray cleaning code execution.* To tell RavenRecSyst
which file is you're cleaning file simply use the -c / --cleaner argument
followed by the file inclusive path to the (executable) cleaner file.

An example using the default cleaner:
```
**/ravenRecSyst.py *yourOtherArguments* --cleaner **/examples/cleaner --newData *1*
```
Where:
* \*\* is the inclusive path to wherever you have RavenRecSyst/ directory, read
usage section.
* \*1\* is the inclusive file path or folder of files which are to be cleaned

Both arguments provided to --cleaner and --newData will be used as arguments to
you're cleaner file. See \*\*/examples/cleaner.py for a boiler plate template.

Notice --newData is also specified, as the cleaner will not be used if there is
nothing to clean.

Once cleaning is complete, RavenRecSyst will use the same files/ folder of files
provided to --newData and put them into mongoDb for you. You may want to verify
that this has been done correctly using a tool such as MongoDb compass or
using the RavenRecSysts -l flag to log you in so you can inspect mongoDb
manually.

\* please note: this is a potential security concern if this file is edited to
include malicious code, please make sure that all files in this project have
minimum write premissions on you're system so that they can not be used as such.
Pleae also ensure that you do not execute RavenRecSyst with administrator
permissions as it is uneccessary and potentially harmfull if these files have
been maliciously tampered as with any code base.

#### Formatting

For cleaning operations, please ensure that the data files passed in to
--newData are in csv or end up in csv after you're cleaning file completes

It is also neccessary that each individual file is a single csv table,
with a header row which is the names you would like to use in the database for
those columns.

As an example:

| name        | age | legs | has Furr |...| class   |
|:-----------:|:---:|:----:|:--------:|:-:|:-------:|
| Jimmy       | 9   | 4    | 1        |...| dog     |
| Dumbledore  | 115 | 2    | 1        |...| wizard  |
| Margret     | 152 | 4    | 0        |   | turtle  |

Resulting in database attribute names ["name", "age", "legs", "has Furr", ...,
 "class"]

The spaces and casing of the words will be enshrined, which means if they are
inconsistent between tables they will be completeley different things. Please
ensure there are no special characters specifically any not in this list:
* alphanumeric
* hyphen
* underscore

As those characters will have to be stripped or they will result in headaches.

### Training
(not yet implemented)

### Testing
(not yet implemented)

### Predicting
(not yet implemented)

---

## Closing examples
for user 'georgeraven' creating 'GeorgeRaven' user with 'password' password, in database 'mehDatabaseName', who desires to debug at log level '3' and to launch database:
````
/home/georgeraven/RavenRecSyst/ravenRecSyst.py -u GeorgeRaven -p password -N mehDatabaseName -v 3 -i -S
````

Please see help screen for more options there are many more but these are the main ones for localhost usage.
