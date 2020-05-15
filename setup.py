import setuptools

with open("requirements/common.txt", "r") as handler:
    install_requirements = handler.readlines()

setuptools.setup(
    install_requires=install_requirements,
    name="easyutils",
    version="0.0.3",
    author="SDE",
    description="various utils",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    python_requires='>=3.6',
)
