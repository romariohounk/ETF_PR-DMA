#!/bin/bash
# Script to delete automatically log files older than 30 days

cd ../logs/drive_backup
find ./ -mtime +30 -type f -delete
cd /home/pi/PythonW/ETF_PR-DMA/logs/ETF_files_writing
find ./ -mtime +30 -type f -delete
cd /home/pi/PythonW/ETF_PR-DMA/logs/ETF_report
find ./ -mtime +30 -type f -delete
