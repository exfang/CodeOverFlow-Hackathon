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
# Github Codes
How to manually add a branch from local
1. Create a Branch
   ```console
   C:\repo_folder_path>git branch [branch-name]
   ```
2. Pushing branch to github
   ```console
   C:\repo_folder_path>git push --set-upstream origin [branch-name]
   ```
3. Change Branch
   ```console
   C:\repo_folder_path>git checkout [branch-name]
   ```
4. Check Current Branch
   ```console
   C:\repo_folder_path>git branch
   ```
How to manually commit to github:
1. To add your manuiplated/updated files into git
   ```console
   (virutal_environment_name)C:\repo_folder_path>git add --all
   ```
   
2. Check which files will be uploaded
   ```console
   (virutal_environment_name)C:\repo_folder_path>git status
   ```
3. Commit file to GitHub with message
   ```console
   (virutal_environment_name)C:\repo_folder_path>git commit -m "message"
   ```
   
4. Push your updated files into GitHub
   ```console
   (virutal_environment_name)C:\repo_folder_path>git push
   ```
# Create SQL Table
How to manually create SQL table
1. To create table open Command Prompt
   ```command prompt
   (virutal_environment_name)C:\repo_folder_path>python
   ```
2. How to import db
   ```command prompt
   >>> from app import db
   ```
3. How to create Table
   ```command prompt
   >>> db.create_all()
   ```
4. How to exit the interface
   ```command prompt
   >>> exit()
   ```
