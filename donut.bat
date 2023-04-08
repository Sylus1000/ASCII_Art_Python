@echo off
mode con cols=120 lines=50
color a
python scripts/ascii_art.py -i examples/donut.gif -as small
PAUSE