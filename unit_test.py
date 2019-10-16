# @Author: George Onoufriou <archer>
# @Date:   2019-08-14
# @Email:  george raven community at pm dot me
# @Filename: unit_test.py
# @Last modified by:   archer
# @Last modified time: 2019-08-16
# @License: Please see LICENSE in project root
import nemesyst
import shutil  # deleting directories
import os


def test(args=None, config_files=None, description=None):
    args = args if args is not None else []
    config_files = config_files if config_files is not None else \
        nemesyst.default_config_files()
    description = description if description is not None else \
        "Nemesyst; Unit tests."
    args = nemesyst.argument_handler(
        args=args,
        config_files=config_files,
        description=description
    )
    args["db_password"] = "iamgroot"
    nemesyst.main(args)


# set the directory to use for tests
test_dir = "test_dir"  # testing ability to recover from relative path
# test empty
test()

# ensure db is closed before attempting
test(args=["--db-stop", "--db-path", test_dir])
test_args = [
    "--db-init",
    "--db-start",
    "--db-path", test_dir,
    "--db-log-path", os.path.join(os.path.abspath(test_dir), "logs"),
    "--db-user-name", "groot",
    "--db-port", "22229",
    "--db-stop",
    "--data-cleaner", "examples/cleaners/debug_cleaner.py",
    "examples/cleaners/debug_cleaner.py", "examples/cleaners/debug_cleaner.py",
    "--data-cleaner-entry-point", "main", "main", "main",
    "--data-collection", "debug_data", "debug_data", "debug_data",
    "--dl-learner", "examples/learners/debug_learner.py",
    "examples/learners/debug_learner.py",
    "--dl-learner-entry-point", "main", "main", "main",
    "--dl-data-collection", "debug_data", "debug_data", "debug_data",
    "--dl-input-model-collection", "debug_models", "debug_models",
    "--dl-output-model-collection", "debug_models", "debug_models",
    "--i-predictor", "examples/predictors/debug_predictor.py",
    "--i-predictor-entry-point", "main",
    "--i-output-prediction-collection", "debug_predictions",
    "debug_models",
    "--data-clean",
    "--dl-learn",
    "--i-predict"
    # "--db-login"
    # "--db-password", "iamgroot", # this is overriden manually
]
test(args=test_args)
# clean up after ourselves
shutil.rmtree(os.path.abspath(test_dir))
