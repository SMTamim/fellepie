echo off
CALL pip install -r requirements.txt
CALL playwright install
CALL python test.py