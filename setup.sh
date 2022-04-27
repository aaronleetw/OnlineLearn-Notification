#!/bin/bash
echo "-----------------------------------------------------------------------------"
echo "Thanks for using this script! You might be prompted with your SUDO password."
echo "-----------------------------------------------------------------------------"
echo "This script will only work on macOS or Debian based Linux distributions."
if [ "$(uname)" == "Darwin" ]; then
    echo "Currently dected OS: Mac OS X"
    echo "What it will do:"
    echo "1. Install and update Homebrew"
else
    echo "Currently dected OS: Linux"
    echo "Please double check that you are running this script on a Debian based Linux distribution."
    echo "What it will do:"
    echo "1. Install and update apt-get"
fi
echo "2. Install python3 python3-pip and python3-venv"
echo "3. Create and activate virtual environment in ./venv/ directory"
echo "4. Install requirements.txt"
echo "-----------------------------------------------------------------------------"
echo "Press ENTER to continue or CTRL+C to cancel."
read
echo "(1) Updating packages..."
if [ "$(uname)" == "Darwin" ]; then
    echo "(1-1) Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "(1-2) Updating Homebrew Packages..."
    brew update
else
    sudo apt-get update
    sudo apt-get upgrade -y
fi
echo "-----------------------------------------------------------------------------"
echo "(2) Installing packages..."
if [ "$(uname)" == "Darwin" ]; then
    brew install python3
    brew postinstall python3
else
    sudo apt install -y python3
    sudo apt install -y python3-pip
    sudo apt install -y python3-venv
fi
echo "-----------------------------------------------------------------------------"
echo "(3) Creating virtual environment..."
python3 -m venv venv
echo "-----------------------------------------------------------------------------"
echo "(4) Activating virtual environment..."
source venv/bin/activate
echo "-----------------------------------------------------------------------------"
echo "(5) Installing python packages..."
pip3 install -r requirements.txt
echo "-----------------------------------------------------------------------------"
echo "(6) Done!"
echo "You can now run the application by typing 'source venv/bin/activate' and then 'flask run'"
echo "Head to https://cutt.ly/zU975It to find out how to serve your app to the rest of the world using gunicorn and nginx!"
echo "If you have any questions, feel free to contact me!"
echo "Thanks again!"
echo "-----------------------------------------------------------------------------"
