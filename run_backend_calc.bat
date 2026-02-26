@echo off
call backend\calculations\cvenv\Scripts\activate.bat
cd backend\calculations\
python servercalc.py