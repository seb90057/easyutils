#/bin/bash
#
# Create build

python setup.py sdist bdist_wheel
python -m twine upload --verbose --repository testpypi dist/*
