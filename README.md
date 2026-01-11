# LITRevu
## Version
1.0.0
## Overview
LITRevu is an innovative startup focused on developing a platform that 
empowers a community of users to:
- Publish reviews of books and literary articles.
- Browse or request on-demand book reviews.

The application web create a dynamic space where literature enthusiasts can 
share insights, discover new perspectives, and engage with thoughtful critiques.
## Installation
1. Clone the project with the command:`git clone https://github.
com/GitDrinou/DA_Python_P09_LITRevu.git`
2. Create a virtual environment by running the following lines in your terminal:
   a - first, go the application's root directory
   b - check if you have access to `venv`: `python -m venv --help`
   c - create the environment with : `python -m venv env`
   d - activate the environment with:
      - for MacOS: `source env/bin/activate`
      - for Windows: `env\Scripts\activate`
3. Install the required packages with : `pip install -r requirements.txt`
## Launch application
On your terminal:
1. go to the application directory: `cd litrevu/`
2. run the server with: `python manage.py runserver`

To disconnect the server: `CTRL` + `C`
To deactivate the virtual environment, go to the directory application's 
root and copy/paste or write the following command: `deactivate`

If you already install the application, you don't have to create a new 
virtual environment, just activate it (see the points 2c of the installation 
chapter), and run the server (see the 2 steps on the launch application chapter)

## Code style and linting
This project follows the PEP8 coding style and uses flake8 as a linting tool 
to maintain code quality.

To launch and check the flake8 report:
1. open your terminal and go the application's root directory
2. execute the following command: 'flake8'

If the code is not valid, you will see a list of errors.
