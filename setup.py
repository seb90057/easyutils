import setuptools
from os import listdir
from os.path import isfile, join


with open("requirements/common.txt", "r") as handler:
    install_requirements = handler.readlines()

conf = "src/sdeutils/file/field/cast/conf"
conf_list = [f for f in listdir(conf) if isfile(join(conf, f))]


setuptools.setup(
    install_requires=install_requirements,
    name="sdeutils",
    version="0.2.3",
    author="SDE",
    description="various utils",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    python_requires=">=3.6",
    data_files=[(conf, ["{}/{}".format(conf, c) for c in conf_list])],
)
