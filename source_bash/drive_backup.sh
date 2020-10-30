#!/bin/bash
# Script to save ETF file on your google drive

cd ../source_python

# Used to activate the right env to run my python scripts. Don't use the following line if you already got the right env
source ../../.venv/clikraken/bin/activate

python ./drive_backup.py > "/home/pi/PythonW/ETF_PR-DMA/logs/drive_backup/$(date +%Y-%m-%d_%H:%M)_ETF_report.log"
deactivate
