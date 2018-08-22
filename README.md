# Nemesyst

###### (formerly: RavenRecSyst)

Please note: The examples in ./examples folder are still being written, in particular the movilense 20 million (ml_20m). This documentation is also in the process of being further updated with more examples and adding to testing and prediction sections. If you have any issues or see anything glaringly wrong please open an issue.

## Introduction

Experimental generalisable recommender system; Python, bash, and TensorFlow.

This experimental recommender system is part of an ongoing masters thesis, which purposely compares the use of
Generative Adversarial Neural Networks (GANs) with certain other traditional and prevalent machine learning (ML)
recommender system techniques. This recommender system is evaluated by the common method of rating prediction
via mean absolute error (MEA).

Along the way however I decided to make everything as configurable/ generalisable as possible. This system has become a framework for the application of machine learning into a wider environment, fascilitated by this configurability; Including config and pipeline files, custom cleaning script calls, and custom machine learning scripts all while the nuanced operations are completed automagically, such as transforming then loading the chosen data into mongoDB, allowing for interesting distributed applications to do with combining mongodb with machine learning. The use of mongodb also allows this program to act clay-like, keeping track of program state to be reloaded, reused, monitored etc, just as clay would keep the shape impressed upon it. It keeps track of each model trained, as a seperate document in the models collection, with the models binary also being saved so it can be directly replayed with simple calls.

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


You will first have to install/ verify a few key dependancies.

* [MongoDb](https://www.mongodb.com/)
* Python modules:
    * [Pymongo](https://api.mongodb.com/python/current/) for MongoDb
    * [TensorFlow | TensorFlow-gpu](https://www.tensorflow.org/install/) for that juicy machine-learning
    * [Keras](https://github.com/keras-team/keras) although tensorflow has recentley bundled its own keras
- [Bash](https://www.gnu.org/software/bash/) for simple system level operations

If any have been left out please create an issue and post any log messages.

Then simply: *
````
git clone https://github.com/DreamingRaven/Nemesyst
````
````
./Nemesyst/nemesyst.py --toUpdate
````

Other than those that should be all you need, as dependanices have been kept to as few as needed to make a good extensible result.


\* Note: This system is being developed on linux (Arch Linux) and since the focus is not cross platform there has been no checking for windows support, meaning it may need tinkering if you would like to run it on windows, although I have made every attempt to make this as straight forward as possible, with minimal dependencies and sanitising paths for cross platform use.

---

## Usage

The entry point file is [nemesyst.py](https://github.com/DreamingRaven/Nemesyst/blob/master/nemesyst.py)

This recommender system should flag any issues with arguments automagically. For a list of what arguments are availiable:
````
**/nemesyst.py -h
````

** is used in place of whatever the path is to the Nemesyst root directory location, since it will vary between systems. e.g the full bash command on my system would be:
````
 ~/Nemesyst/nemesyst.py -h
````
where '~' is expanded by bash to /home/whateverYourUserNameIs

standard usage for a localhost server with authentication (auth non optional forced):
````
**/nemesyst.py --user *1* --pass *2* --name *3* --toInitDb --toStartDb
````
or
````
**/nemesyst.py -u *1* --p *2* --N *3* -i -S
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
**/nemesyst.py -u *1* --p *2* --N *3* --loglevel 9001
````
("over nine thousand!") 9001 will show all log levels < 9001

### All the options

This is a current list but **/nemesyst.py --help will always be prefered and this is not going to be as up to date or verbose, just a basic overview. For any in depth queries see the argparse [parser.add_arguments](https://github.com/DreamingRaven/Nemesyst/blob/master/src/arg.py)

| option       | alternate | default                  | isFlag | class  | description   |
|:------------:|:---------:|:------------------------:|:------:|:------:|:-------------:|
| \-\-coll     | \-C       | "testColl"               | 0      | mongo  | sets collection to operate on |
| \-\-cleaner  | \-c       | **/examples/cleaner.py   | 0      | import | specifies path to executable cleaner file  |
| \-\-dir      | \-D       | ~/db                     | 0      | mongo  | specifies path to mongoDb files  |
| \-\-newData  | \-d       | None                     | 0      | import | specifies path to .csv data folder  |
| \-\-ip       | \-I (eye) | 127.0.0.1                | 0      | mongo  | specifies ip of database  |
| \-\-toInitDb | \-i       | False                    | 1      | mongo  | flags new user auth to create |
| \-\-toLogin  | \-l (ell) | False                    | 1      | mongo  | flags to log user into db for them |
| \-\-name     | \-N       | "RecSyst"                | 0      | mongo  | specifies the name of the mongoDb DB  |
| \-\-port     | \-P       | 27017                    | 0      | mongo  | specifies the mongoDb port |
| \-\-pass     | \-p       | iamgroot                 | 0      | auth   | specifies the password for mongoDb auth  |
| \-\-toStartDb| \-S       | False                    | 1      | mongo  | flags to start mongoDb (with auth) |
| \-\-toStopDb | \-s       | False                    | 1      | mongo  | flags to stop db in -D path |
| \-\-toTrain  | \-T       | False                    | 1      | ann    | flags to train |
| \-\-toTest   | \-t       | False                    | 1      | ann    | flags to test  |
| \-\-url      | \-U       |mongodb://localhost:27017/| 0      | mongo  | specifies mongoDb url  |
| \-\-user     | \-u       | groot                    | 0      | auth   | specifies the mongoDb usernam for auth  |
| \-\-loglevel | \-v       | 2                        | 0      | debug  | specifies the min loglevel to log  |
| \-\-batchSize|           | 1                        | 0      | mongo ann | specifies the size of batches to use |
| \-\-target   |           | target                   | 0      | mongo ann | specifies the name of target feature |
| \-\-type     |           | lstm                     | 0      | ann       | specifies the type of neural network to create |
| \-\-timeSteps|           | 25                       | 0      | ann       | specifies if sequential type, num cells of rnn |
| \-\-testSize |           | 0.2                      | 0      | validation| specifies the % size of test set |
| \-\-activation|          | tanh                     | 0      | ann    | specifies keras activation alg |
| \-\-dimensionality|      |                          | 0      | ann    | specifies num of features in data during learning and predicting |
| \-\-layers   |           | 1                        | 0      | ann    | specifies num of layers in things like lstm |
| \-\-lossMetic|           | mae                      | 0      | ann    | specifies keras loss metric |
| \-\-optimizer|           | sgd                      | 0      | ann    | specifies keras optimiser |
| \-\-randomSeed|          | 42                       | 0      | ann    | specifies random seed (unused) |
| \-\-epochs   |           | 1                        | 0      | ann    | specifies num of keras epochs |
| \-\-suffix   |           | .data                    | 0      | rrs    | specifies extension of all temporary data files |
| \-\-chunkSize|           | 10000000                 | 0      | rrs    | specifies the maximum number of rows to be processed in imported csv file at a time |
| \-\-toJustImport|        | False                    | 1      | rrs    | flags using residual temporary files without cleaning to import to db |
| \-\-pipeline |           | **/config/pipeline.json  | 0      | config | specifies file path to pipeline.json file |
| \-\-config   |           | **/config/config.ini     | 0      | config | specifies file path to config.ini file |
| \-\-mongoCursorTimeout   |           | 600     | 0      | mongo | specifies the time in milliseconds to allow a cursor to remain inacive before it is deleted |
| \-\-kerLogMax|           | 0                        | 0      | ann    | specifies the maximum log level of keras log/ print statements |
| \-\-toUpdate |           | False                    | 1      | rrs    | flag to update / install nemesyst and RavenPythonLib |
| \-\-modelColl|           | modelStates              | 0      | mongo  | specifies the collection to store model states and history in |
| \-\-identifier|          | getpass.getuser()        | 0      | mongo  | specifies an identifier so you can differentiate between model sources easily |
| \-\-tfLogMin |           | 1                        | 0      | tf     | specifies how verbose you want tensorflow to be i.e TF_CPP_MIN_LOG_LEVEL |

### Config Files / Persistent Behavioral Changes

While Nemesyst supports a lengthy list of command line options: which dictate the flow and operation of the algorithm, it may be desireable to have a peristent set of options which one can use to reduce the need to repeatedley type out consistentley used commands.

For this Nemesyst supports .ini config files, the default / boilerplate of which can be found in [\*\*/Nemesyst/config/config.ini](https://github.com/DreamingRaven/Nemesyst/blob/master/config/config.ini). This is implemented using [pythons configparser library](https://docs.python.org/3/library/configparser.html) and all keynames are shared with the command line interface although the config file only supports the long format e.g. 'user' instead of --user but not 'u' instead of -u. There is also an order of priority, cli > config > fallbacks; Explicitly, command line options will always take precedence to allow for quick customisation without having to persistentley change any underlying configuration file; Least priority is are the fallbacks which are only used if no cli or config file options exist.

Note however the config file above has sections called [options] and [DEFAULT], please refrain from changing the default section and instead overide the defaults by adding entries inside the options section which is the one specifically called by Nemesyst. This will mean you always have the original default options as a referance point for overiding.

---

## Application Specific Customisation

Nemesyst includes customisable modules that should be used to get the
functionality you need. These modules should be executable and will be called
by Nemesyst to do data/ application specific operations.

There will be 4 such modules; these were included since there is no way to
create things such as a universal dataset cleaner, as each data set has its own
nuances.

### Cleaning
Nemesyst supports arbitray cleaning code execution.* To tell Nemesyst
which file is you're cleaning file simply use the -c / --cleaner argument
followed by the file inclusive path to the (executable) cleaner file.

An example using the default cleaner:
```
**/nemesyst.py *yourOtherArguments* --cleaner **/examples/cleaner --newData *1*
```
Where:
* \*\* is the inclusive path to wherever you have Nemesyst/ directory, read
usage section.
* \*1\* is the inclusive file path or folder of files which are to be cleaned

Both arguments provided to --cleaner and --newData will be used as arguments to
you're cleaner file. See \*\*/examples/cleaner.py for a boiler plate template.

Notice --newData is also specified, as the cleaner will not be used if there is
nothing to clean.

Once cleaning is complete, Nemesyst will use the same files/ folder of files
provided to --newData and put them into mongoDb for you. You may want to verify
that this has been done correctly using a tool such as MongoDb compass or
using the RavenRecSysts -l flag to log you in so you can inspect mongoDb
manually.

\* please note: this is a potential security concern if this file is edited to
include malicious code, please make sure that all files in this project have
minimum write premissions on you're system so that they can not be used as such.
Pleae also ensure that you do not execute Nemesyst with administrator
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
the database. For this reason Nemesyst supports [aggregate pipelines](https://docs.mongodb.com/manual/core/aggregation-pipeline/), which not only
allow you to get existing data from the database but allows you to perform complex operations
on the data prior to getting it from the database in a non permanent manner; aggregate pipelines in this manner allow you to rapidly test small changes on the clean data set without having to reopen csv files or re-clean to calculate things like sums of a column etc, provided post cleaning the data has not been scrubbed of features you required to do tweaks, clearly you cant calculate sum of a column that no longer exists in the clean dataset. Any pipeline present in [pipeline.json](https://github.com/DreamingRaven/Nemesyst/blob/master/config/pipeline.json) will be used to create a cursor which in turn will iterate over your data set. This can of course be overidden, you can specify the pipeline file using the --pipeline option.

Pipelines can be confusing at first, but stick with it, they are incredibly powerfull tools that allow you to change things rapidly, efficientley, and with minimal fuss once you know what you are doing. I know firsthand how offputting they can be but im so glad I stuck with them myself: So muuch powweeerrrr.

The results of the pipeline are at a minimum an '_id' field, but Nemesyst requires two other fields, a "data" field and a "target" field; The "data" field should contain the exact data you would like to train on for a whole single example; The "target" field should contain a matching .. well target, so preciseley what you would like to backpropogate with. Clearly in the example case of predicting new data there is no "target" to include, but a pipeline which pushed something that doesnt exist into an array or single value will just be left empty anyway, which means you can use the same pipeline for training testing and predicting if you leave the "target" field in the aggregate pipeline, as it will be easily and intuitiveley dealt with.

Pipeline:
```
[
  {"$unwind": "$data"},
  {"$group":
    {
    "_id": "$_id",
    "data":
      { "$push": {
          "whatNameToGiveIt":    "$data.feature1",
          "anotherName":         "$data.feature2"
      }},
    "target": {"$first": "$someKey"}
    }
  }
]
```
You will need to inspect the database to see how your data is structured to
be able to write your pipeline file.

Given a single normal mongoDb document generated by nemesyst.py->importer.py:
```
{
  {"id": someIdNumber},
  {"data":
    [
      { {"index": 0}, {"feature1": 22}, {"feature2": "tomato"} },
      { {"index": 1}, {"feature1": 66}, {"feature2": "apples"} },
      { {"index": 2}, {"feature1": 13}, {"feature2": "cucumb"} },
      { {"index": 3}, {"feature1": 11}, {"feature2": "cherry"} },
      { {"index": 4}, {"feature1": 77}, {"feature2": "pillow"} }
    ]
  },
  {"someKey":}
}
```
As you may notice the area in between the [] square brackets is almost exactly
how a CSV file would be laid out. It may be usefull to think of these embedded
arrays like that, and I have lain them out to suit the analogy. The main difference
is that instead of column names you have keys like "feature1" and to access a
specific row you can use their index or whatever identifier you have to
[$match](https://docs.mongodb.com/manual/reference/operator/aggregation/match/) or
select them in whatever way you desire. I would however recommend [$push](https://docs.mongodb.com/manual/reference/operator/aggregation/push/) if you would
like to get a a whole collumn, lets say all of "feature1". A good visualisation can
be found on the
[$push](https://docs.mongodb.com/manual/reference/operator/aggregation/push/)
documentation page. Also a quick note the dot notation as in '$data.X' means sub key X in data, I.E call a key that is nested within another key. The $ symbol is used to mean variables, so '$data.X' = the value associated with that key e.g 22, 'data.X' = the string "data.X".

Results in:

| key           | value 0 | value 1 | value 2 |...| value timeSteps-1   |
|:-------------:|:-------:|:-------:|:-------:|:-:|:-------------------:|
| id            | someIdNumber |    |         |...|                     |
| whatNameToGiveIt| 22   | 66       | 13      |...| 17                  |
| anotherName   | tomato | apples   | cucumb  |...| pillow              |

Currentley Nemesyst does not support multivariate targets, specifically any "target" with more than one value, this is a future addition.

### Training
To train the data set you first require a pipeline (see pipelines section). This pipeline is what will create an interatable mongoDb cursor which can retrieve the data you want in the manner you want it retrieved, please see previous section "Pipelines".

The conditions that need to be met to allow for training:
- RavenPythonLib to have been installed using automatic updater ( --toUpdate )
- An initialised mongoDb database with username and password ( --toInitDb, --user, --pass )
- The afformetioned database to be currentley running ( --toStartDb )
- The desired collection name where the data should be stored or is stored to be known ( --coll )
- The database having data in the above collection ( --coll --newData, --cleaner | --coll --toJustImport )
- A working pipeline file in [default location](https://github.com/DreamingRaven/Nemesyst/blob/master/config/pipeline.json) or specified using options ( None | --pipeline )
- Specifying the manner in which you would like to train, E.G. rnn, or lstm etc ... ( --type, --timeSteps ... )

If all the above conditions are met at the point of training (they can all be done in one command and automatically run in the correct order), then you can specify the --toTrain flag.

````
**/Nemesyst/nemesyst.py --toTrain
````

### Testing

Similar to above it needs all of those training requirements but it also
requires that a model have been trained and exists in the "states" collection.

If not parameter is given (currentley you cant specify) then it will pull the most
recent model. This will test on the data set pointed to by --coll. As such you
will need to re-run nemesyst.py to swap from training to testing if you want
to train on one set and test on another.

````
**Nemesyst/nemesyst.py --toTest
````

### Predicting
(documentation still being written)

---

## Closing examples
for user 'georgeraven' creating 'GeorgeRaven' user with 'password' password, in database 'mehDatabaseName', who desires to debug at log level '3' and to launch database:
````
/home/georgeraven/Nemesyst/nemesyst.py -u GeorgeRaven -p password -N mehDatabaseName -v 3 -i -S
````

Please see help screen for more options there are many more but these are the main ones for localhost usage.

### Asside

For all those fellow Arch(Linux)-ers out there, we are "Arch Nemesysts" :D
