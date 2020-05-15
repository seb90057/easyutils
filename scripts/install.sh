#/bin/bash
#
# Install development environment

echo "Creating Python virtual environment..."
python -m venv venv/

source venv/Scripts/activate

echo "Upgrading pip..."
python -m pip install -q --upgrade pip

echo "Installing Python requirements..."
if ! pip install --ignore-installed -qr requirements/common.txt; then
    echo
    echo -e "Failed to install Python requirements"
    exit 1
fi

echo "Installing Git pre-commit hook..."
pre-commit install