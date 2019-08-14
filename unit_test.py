# @Author: George Onoufriou <archer>
# @Date:   2019-08-14
# @Email:  george raven community at pm dot me
# @Filename: unit_test.py
# @Last modified by:   archer
# @Last modified time: 2019-08-14
# @License: Please see LICENSE in project root
import nemesyst


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


# test empty
test()
test_args = [
    "--db-user-name", "groot",
    # "--db-password", "iamgroot", # this is overriden manually
]
test(args=test_args)
