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

    nemesyst.main(
        nemesyst.argument_handler(
            args=args,
            config_files=config_files,
            description=description
        )
    )


# test empty
test()
