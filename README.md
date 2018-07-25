# RavenRecSyst

Warning: this project has not yet reached it basic intended functionality, to be ready for normal usage will take time so some of the examples may not work currently. If you see anything glaringly wrong please do open an issue, thanks. GR

## Introduction

Experimental generalisable recommender system; Python, bash, and TensorFlow.

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
- [Bash](https://www.gnu.org/software/bash/) for simple system level operations

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

### All the options

This is a current list but **/ravenRecSyst.py --help will always be prefered.

| option       | alternate | default                  | isFlag | class  | description   |
|:------------:|:---------:|:------------------------:|:------:|:------:|:-------------:|
| \-\-coll     | \-C       | "testColl"               | 0      | mongo  | sets collection to operate on |
| \-\-cleaner  | \-c       | **/examples/cleaner.py   | 0      | import | specifies path to executable cleaner file  |
| \-\-dir      | \-D       | ~/db                     | 0      | mongo  | specifies path to mongoDb files  |
| \-\-newData  | \-d       | None                     | 0      | import | specifies path to .csv data folder  |
| \-\-ip       | \-I       | 127.0.0.1                | 0      | mongo | specifies ip of database  |
| \-\-toInitDb | \-i       | False                    | 1      | mongo | flags new user auth to create |
| \-\-toLogin  | \-l       | False                    | 1      | mongo | flags to log user into db for them |
| \-\-name     | \-N       | "RecSyst"                | 0      | mongo | specifies the name of the mongoDb DB  |
|------------|---------|------------------------|------|------|---still being filled in---|

### Config Files / Persistent Behavioral Changes

While RavenRecSyst supports a lengthy list of command line options: which dictate the flow and operation of the algorithm, it may be desireable to have a peristent set of options which one can use to reduce the need to repeatedley type out consistentley used commands.

For this RavenRecSyst supports .ini config files, the default / boilerplate of which can be found in [\*\*/RavenRecSyst/config/rrs_ml.ini](https://github.com/DreamingRaven/RavenRecSyst/blob/master/config/config.ini). This is implemented using [pythons configparser library](https://docs.python.org/3/library/configparser.html) and all keynames are shared with the command line interface although the config file only supports the long format e.g. 'user' instead of --user but not 'u' instead of -u. There is also an order of priority, cli > config > fallbacks; Explicitly, command line options will always take precedence to allow for quick customisation without having to persistentley change any underlying configuration file; Least priority is are the fallbacks which are only used if no cli or config file options exist.

Note however the config file above has sections called [options] and [DEFAULT], please refrain from changing the default section and instead overide the defaults by adding entries inside the options section which is the one specifically called by RavenRecSyst. This will mean you always have the original default options as a referance point for overiding.

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

Each file with the extension given by the --suffix option in the directory given by --newData option will become a mongoDB document as is. So please prepare, chunk and clean files in the manner in which you expect them to become documents.

#### Pipelines
After cleaning data or inserting clean data, it is neccessary to retrieve again the data from
the database. For this reason RavenRecSyst supports [aggregate pipelines](https://docs.mongodb.com/manual/core/aggregation-pipeline/), which not only
allow you to get existing data from the database but allows you to perform complex operations
on the data prior to getting it from the database in a non permanent manner; aggregate pipelines in this manner allow you to rapidly test small changes on the clean data set without having to reopen csv files or re-clean to calculate things like sums of a column etc, provided post cleaning the data has not been scrubbed of features you required to do tweaks, clearly you cant calculate sum of a column that no longer exists in the clean dataset. Any pipeline present in [pipeline.json](https://github.com/DreamingRaven/RavenRecSyst/blob/master/config/pipeline.json) will be used to create a cursor which in turn will iterate over your data set. This can of course be overidden, you can specify the pipeline file using the --pipeline option.

Pipelines can be confusing at first, but stick with it, they are incredibly powerfull tools that allow you to change things rapidly, efficientley, and with minimal fuss once you know what you are doing. I know firsthand how offputting they can be but im so glad I stuck with them myself: So muuch powweeerrrr.

The results of the pipeline are at a minimum an '_id' field, but RavenRecSyst requires two other fields, a "data" field and a "target" field; The "data" field should contain the exact data you would like to train on for a whole single example; The "target" field should contain a matching .. well target, so preciseley what you would like to backpropogate with. Clearly in the example case of predicting new data there is no "target" to include, but a pipeline which pushed something that doesnt exist into an array or single value will just be left empty anyway, which means you can use the same pipeline for training testing and predicting if you leave the "target" field in the aggregate pipeline, as it will be easily and intuitiveley dealt with.

Currentley RavenRecSyst does not support multivariate targets, specifically any "target" with more than one value, this is a future addition.

### Training
To train the data set you first require a pipeline (see pipelines section). This pipeline is what will create an interatable mongoDb cursor which can retrieve the data you want in the manner you want it retrieved.

The conditions that need to be met to allow for training:
- An initialised mongoDb database with username and password ( --toInitDb, --user, --pass )
- The desired collection name where the data should be stored or is stored to be known ( --coll )
- The database having data in the above collection ( --coll --newData, --cleaner | --coll --toJustImport )
- The afformetioned database to be currentley running ( --toStartDb )
- A working pipeline file in [default location](https://github.com/DreamingRaven/RavenRecSyst/blob/master/config/pipeline.json) or specified using options ( None | --pipeline )
- Specifying the manner in which you would like to train, E.G. rnn, or lstm etc ... ( --type, --timeSteps ... )

If all the above conditions are met at the point of training (they can all be done in one command and automatically run in the correct order), then you can specify the --toTrain flag.

(currentley completing documentation)

### Testing
(currentley completing documentation)

### Predicting
(not yet implemented)

---

## Closing examples
for user 'georgeraven' creating 'GeorgeRaven' user with 'password' password, in database 'mehDatabaseName', who desires to debug at log level '3' and to launch database:
````
/home/georgeraven/RavenRecSyst/ravenRecSyst.py -u GeorgeRaven -p password -N mehDatabaseName -v 3 -i -S
````

Please see help screen for more options there are many more but these are the main ones for localhost usage.
