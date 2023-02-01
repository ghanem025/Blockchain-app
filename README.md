# Blockchain-app
A prototype of a blockchain application, this application will have a front-end (HTML/CSS) and back-end (python, flask)

# Setting up a virtual enviornment
To run the application we need a virtual enviornment. Here are the steps to setup a virtual enviornment.

```bash
$ cd Blockchain-app

$ python3 -m venv venv

$ source venv/bin/activate
```

# Installing Flask
Installing flask is simple, just run this command.

```bash
$ pip install Flask
```

# Import libraries
Once you have the virtual enviornment setup, you can now import all the neccesary python libraries using `requirements.txt`

```bash
$ pip install -r requirements.txt
```



# How to run the app
First you need to go into the source directory and run the `flask --app main.py run` command
```bash
$ cd src

$ flask --app main.py run
```
If the app is running, you have succesfully setup this flask application.