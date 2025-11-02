# Code-Analyser-Python

# Inital Description
- This is a program written in python which analyses a certain file written in python and tells the user where the mistakes are made and what feature doesnt fit with UTF-8

# Features
- The program lets user enter a file name using argparse with command line arguments
- It lets the user add what type of checks (line-checks, ast-checks or both) he or she wishes to do on the file
- There are three main files besides the main.py: one which contains line base checks, one with ast checks and another with more advanced ast checks
- There is also another file with decorators from which the three check files import from
- The decorators are applied to all functions
- The main file imports the functions from the three checks file

  # Requirements
- All modules needed are already imported
