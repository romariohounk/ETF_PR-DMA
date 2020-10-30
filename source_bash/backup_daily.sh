#!/bin/bash
# Script to save automatically on daily basis ETF data

cd ../database
cp ./ETF_files/BMOM_DATA.csv backup_daily/
cp ./ETF_files/LN1L_DATA.csv backup_daily/
cp ./ETF_files/LSP5_DATA.csv backup_daily/
cp ./ETF_files/LYFB_DATA.csv backup_daily/

