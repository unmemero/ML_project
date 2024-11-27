#!/bin/bash

# Check if Homebrew is installed
if ! command -v brew &> /dev/null
then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is installed."
fi

# Install dependencies
# Check if git is installed
comms = ("git" "python3" "pip3" "upx")

for comm in $comms
do
    if ! command -v $comm &> /dev/null
    then
        brew install $comm
    else
        echo "$comm is installed."
    fi
done

# Install pip libs
requirements=("scikit-learn" "pandas" "numpy" "matplotlib" "pyqt5" "pyqt5-tools" "pyinstaller" "jupyter" "seaborn" "pandoc")

for req in $requirements
do
    if ! pip3 show $req &> /dev/null
    then
        pip3 install $req
    else
        echo "$req is installed."
    fi
done

# All dependencies are installed
echo "All dependencies are installed."