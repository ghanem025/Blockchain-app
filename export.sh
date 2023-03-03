#!/bin/bash
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
export FLASK_APP="src"
export FLASK_DEBUG=1
