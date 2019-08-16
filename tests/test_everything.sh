# @Author: George Onoufriou <archer>
# @Date:   2019-08-16
# @Email:  george raven community at pm dot me
# @Filename: test_everything.sh
# @Last modified by:   archer
# @Last modified time: 2019-08-16
# @License: Please see LICENSE in project root

# ensuring we are in this files directory
script_path="${0%/*}"
# mkdir -p "${script_path}/../logs"

# testing setup.py and pkgbuild
cd "${script_path}/../.arch"
makepkg -f

# testing sphinx
cd "${script_path}/../docs"
make html

# testing nemesyst itself
cd "${script_path}/.."
python3 unit_test.py
