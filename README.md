# CodeOverFlow-Hackathon
[Click here for installation guide](#installation-guide)
## Background
CodeOverflow is a 4 day hackathon, from 30 August 2022 to 2 September 2022.
## Problem Statment
How can we leverage technologies to combat climate change?

# Installation Guide
If you have not created a virutal environment after cloning the repository (repo), here are the steps to create a virutal environment

   1. Navigate to repo folder and open the terminal
   ```console
   C:\repo_folder_path>python -m venv virutal_environment_name
   C:\repo_folder_path>virutal_environment_name\Scripts\activate
   (virutal_environment_name)C:\repo_folder_path>
   ```
   
   2. After installing & opening/activating your virtual environment, you need to install all prerequisites python packages into your virtual environment by running the auto-installer.py
   ```console
   (virutal_environment_name)C:\repo_folder_path>python auto-installer.py
   ```

If you have already created your virtual environment, navigate to your repo and activate your virtual environment
   ```console
   C:\repo_folder_path>virutal_environment_name\Scripts\activate
   (virutal_environment_name)C:\repo_folder_path>
   ```

Everytime you clone repo, you are required to run the auto-installer.py in your virtual environment.
  ```console
  (virutal_environment_name)C:\repo_folder_path>python auto-installer.py
  ```
  
At the end of your session, you need to run auto-update.py
  ```console
  (virutal_environment_name)C:\repo_folder_path>python auto-update.py
  ```
