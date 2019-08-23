# @Author: George Onoufriou <archer>
# @Date:   2019-08-16
# @Email:  george raven community at pm dot me
# @Filename: test_everything.sh
# @Last modified by:   archer
# @Last modified time: 2019-08-16T15:44:28+01:00
# @License: Please see LICENSE in project root

# get absolute path to current running script parent dir
script_path="${0%/*}"
script_path="`( cd \"$script_path\" && pwd )`"
echo "${script_path}"
# mkdir -p "${script_path}/../logs"

# testing setup.py and pkgbuild
pkgbuild_dir_path="${script_path}/../.arch"
echo "cd ${pkgbuild_dir_path}"
cd "${pkgbuild_dir_path}"
makepkg -f

# testing sphinx
sphinx_dir_path="${script_path}/../docs"
echo "cd ${sphinx_dir_path}"
cd "${sphinx_dir_path}"
make html
make man # and update our man pages while we are at it

# testing nemesyst itself
nemesyst_dir_path="${script_path}/../"
echo "cd ${nemesyst_dir_paths}"
cd "${nemesyst_dir_path}."
python3 unit_test.py

# testing documentation examples
documentation_dir_path="${script_path}"
echo "cd ${documentation_dir_path}"
cd ${documentation_dir_path}
echo "cleaning.sh"
bash cleaning.sh
echo "serving.sh"
bash serving.sh
echo "learning.sh"
bash learning.sh
echo "predicting.sh"
bash predicting.sh
