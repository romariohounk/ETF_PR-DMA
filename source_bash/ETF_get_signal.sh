#!/bin/bash
# Script to get portfolio reporting

cd ../source_python

# Used to activate the right env to run my python scripts. Don't use the following line if you already got the right env
source ../../.venv/clikraken/bin/activate

python ETF_get_signal.py > "/home/pi/PythonW/ETF_PR-DMA/logs/ETF_report/$(date +%Y-%m-%d_%H:%M)_ETF_report.log"
deactivate
