# Blockchain-app
A prototype of a blockchain application, this application will have a front-end (HTML/CSS) and back-end (python, flask)

# Goal (will be updated)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We want to implement a blockchain for a PHR system (Personal health record). The blockchain will store a person’s name, date of birth, medical history, and their family doctor's name. The blockchain may also store any prescribed medication that a patient is currently on. We want to focus on a patient driven PHR system, as we believe that the exchange of medical information should be mediated by the patient. The patient should have access to there medical record at any time, they should also be able to update any information in their PHR. A doctor may also view a patients PHR, with the permission of the patient of course ( the patient’s family doctor for example). Also, if a prescription were to be given to a patient, pharmacist may verify this information (ideally we want the pharmacist to only be able to verify a prescription, no other information will be given). This is only a top-level discussion about what a PHR using a blockchain should function like. We may or may not implement all these features. *** more will be added in the next paragraphs, also edits to previous paragraphs may be done ***

# Setting up a virtual enviornment
To run the application we need a virtual enviornment. Here are the steps to setup a virtual enviornment.

```bash
$ cd Blockchain-app

$ python3 -m venv .venv

$ source .venv/bin/activate
```

# Import libraries
Once you have the virtual enviornment setup, you can now import all the neccesary python libraries using `requirements.txt`

```bash
$ pip install -r requirements.txt
```

# How to run the app
follow these steps to run the flask app. (make sure you are in the parent directory)
```bash
$ source export.sh
# if you already exported the env variable then you don't need to do this. (only need to run it once)

$ flask run
```
If the app is running, you have succesfully setup this flask application.
