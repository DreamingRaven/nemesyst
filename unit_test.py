# @Author: George Onoufriou <archer>
# @Date:   2019-08-14
# @Email:  george raven community at pm dot me
# @Filename: unit_test.py
# @Last modified by:   archer
# @Last modified time: 2019-08-14
# @License: Please see LICENSE in project root
import nemesyst

nemesyst.main(
    nemesyst.argument_handler(
        args=[],
        config_files=nemesyst.default_config_files(),
        description="Nemesyst; Unit tests."
    )
)
