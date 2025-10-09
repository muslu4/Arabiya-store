@echo off
echo Fixing database issues...
cd backend
python ../fix_database.py
echo Database issues fixed successfully!
pause
