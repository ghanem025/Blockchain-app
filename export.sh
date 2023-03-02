#!/bin/bash
pip install -r requirements.txt
source .venv/bin/activate
export FLASK_APP="src"
export FLASK_DEBUG=1
