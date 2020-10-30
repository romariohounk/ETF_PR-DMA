#!/bin/bash
# Script to update files with daily data

cd ../source_python

# Used to activate the right env to run my python scripts. Don't use the following line if you already got the right env
source ../../.venv/clikraken/bin/activate

python ETF_write_files.py > "/home/pi/PythonW/ETF_PR-DMA/logs/ETF_files_writing/$(date +%Y-%m-%d_%H:%M)_ETF_report.log"
deactivate
