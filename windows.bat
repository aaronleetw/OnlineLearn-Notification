@echo Thanks for using this script! You might be prompted with your password.
@echo -----------------------------------------------------------------------------
@echo This script will only work on Windows 10. Please install Python3 first.
@echo What it will do:
@echo 1. Install venv
@echo 2. Create a venv environment called 'venv'
@echo 3. Activate the virtual environment
@echo 4. Install all the requirements for the project
@echo -----------------------------------------------------------------------------
@echo Press ENTER to continue or CTRL+C to cancel.
@pause
@echo -----------------------------------------------------------------------------
@echo (1) Installing venv...
py -3 -m pip install venv
@echo -----------------------------------------------------------------------------
@echo (2) Creating a virtual environment called 'venv'...
py -3 -m venv venv
@echo -----------------------------------------------------------------------------
@echo (3) Activating the virtual environment...
venv\Scripts\activate
@echo -----------------------------------------------------------------------------
@echo (4) Installing all the requirements for the project...
pip install -r requirements.txt
@echo -----------------------------------------------------------------------------
@echo (6) Done!
@echo You can now run the project by typing 'venv\Scripts\activate' and then 'flask run'
@echo You might want to switch to a Debian-based distro to serve the project to the rest of the world.
@echo If you have any questions, feel free to contact me!
@echo Thanks again!
@echo -----------------------------------------------------------------------------