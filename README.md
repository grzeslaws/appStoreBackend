# AppStore backend

##### Introduction
* init virtual environment `virtualenv venv`
* activate virtual environment `source venv/bin/activate`
* install all dependencies via pip `pip install -r requirements.txt`
* export variables from .env file `source .env`
> app is served on gunicorn - a Python WSGI HTTP Server for UNIX
* run app `python run.py`
* stop app `ctrl + c`
* deactivate virtual environment `deactivate`

Sometimes you need install following:
* `pip install PyJWT`

> (The problem arises if you have JWT and PyJWT installed. When doing import jwt it is importing the library JWT as opposed to PyJWT. The one you want for encoding. I did pip uninstall JWT and pip uninstall PyJWT then finally pip install PyJWT. After that it imported the correct module and generated the token! :))

To setup python linter, eg. flake8:
* `pip install flake8`
* and activte it. (On VS Code: open the Command Palette (⇧⌘P), then enter and select Python: Run Linting)