# @Author: George Onoufriou <archer>
# @Date:   2019-08-16
# @Email:  george raven community at pm dot me
# @Filename: test_everything.sh
# @Last modified by:   archer
# @Last modified time: 2019-08-16
# @License: Please see LICENSE in project root

# ensuring we are in this files directory
cd "${0%/*}"

# testing setup.py and pkgbuild
cd ../.arch
makepkg

# testing sphinx
cd ../docs
make html

# testing nemesyst itself
cd ..
python3 unit_test.py
