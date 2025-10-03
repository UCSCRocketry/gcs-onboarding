# Backend instructions
This is a simplified version of our main GCS backend to help you get familiar with our development environment and Flask application structure

## Project Structure

```
backend/
├── env/                    # Virtual environment (DON'T commit, this is your own)
├── .flaskenv              # Flask configuration
├── .python-version        # Specifies Python 3.12.8
├── base.py                # Main Flask application
├── README.pmd             # This :p
├── requirements.txt       # Python package dependencies
```


## Prerequisites

Make sure you have the following installed on your system:

- **Git** - for version control
- **Python 3.12** - specific version required for consistency
- **Code editor** - recommend VS Code but you can use whatever you want 

## 1. Install Python 3.12

Good resources:
* https://www.python.org/downloads/
* https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

Verify installation:
```bash
MacOS: python3.12 --version  # Should show Python 3.12.x
Windows/Linux: python --version
```

## 2. Project Setup

### 2.1 Clone the Repo and cd into backend
```bash
git clone git@github.com:UCSCRocketry/gcs-onboarding.git
cd gcs-onboarding/backend
```

### 2.2 Create Virtual Environment
**Important:** Use Python 3.12 to create venv

Interpreter names may not match up to the ones listed below (e.g. "python" instead of "py")
```bash
#For mac/unix users: 
python3.12 -m venv env

#For windows users: 
py -m venv env
```
Then activate the environment:
```bash 
#For mac/unix users: 
source env/bin/activate

#For windows users: 
.\env\Scripts\activate

#For bash on windows: 
source env/Scripts/activate
```

⚠️ **DON'T EXECUTE NOW!**  
But after you are done and you want to deactivate the environment, simply type into the terminal:
```
deactivate
```

*You'll see (env) at the beginning of your terminal prompt meaning its activated.*


### 2.3 Install Dependencies
Install all dependencies from requirements.txt file
```bash
# Make sure virtual environment is activated still
pip install -r requirements.txt
```

### 2.4 Verify Installation
```bash
# Make sure Flask is installed, check python version, and Werkzeug
flask --version 
# Flask should be 3.0.3
# Werkzeug should be 3.0.4 
# Python should be 3.12.x

```

## Doing and learning and doing and learning and ...
Go through and understand all the files, what they do, how they work. They're pretty well commented. You will need to write the parser and there are some questions (ok only one question) you should answer commented throughout the code


## Running the Application

### 1. Make sure the venv is activated and you are in the backend folder

### 2. Start the Flask development server
```bash
flask run --port 9999
```
Your terminal should say something like:
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 158-513-158
 wsgi starting up on http://127.0.0.1:9999

### 3. Test the endpoint /api/test 
Open a new terminal and run this command: 

```bash
curl http://127.0.0.1:9999/api/test
```

If you dont know, research this (and any other) commands you dont know:
* what is curl
* (optional) what does cli mean  