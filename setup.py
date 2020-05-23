import setuptools

with open("requirements/common.txt", "r") as handler:
    install_requirements = handler.readlines()

conf = "sdeutils/file/field/cast/conf"

setuptools.setup(
    install_requires=install_requirements,
    name="sdeutils",
    version="0.2.1",
    author="SDE",
    description="various utils",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    python_requires=">=3.6",
    data_files=[(conf, ["{}/*".format(conf)])],
)
