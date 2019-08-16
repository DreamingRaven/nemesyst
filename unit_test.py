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
    "--data-cleaner", "scripts/cleaners/debug_cleaner.py",
    "scripts/cleaners/debug_cleaner.py", "scripts/cleaners/debug_cleaner.py",
    "--dl-learner", "scripts/learners/debug_learner.py",
    "scripts/learners/debug_learner.py",
    "--data-clean",
    "--dl-learn",
    # "--db-password", "iamgroot", # this is overriden manually
]
test(args=test_args)
# clean up after ourselves
shutil.rmtree(os.path.abspath(test_dir))
