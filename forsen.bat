@echo off
mode con cols=100 lines=50
color a
python scripts/ascii_art.py -i examples/forsen.gif
PAUSE