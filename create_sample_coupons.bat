
@echo off
echo Creating sample coupons...

cd /d "%~dp0"

python create_sample_coupons.py

echo.
echo Sample coupons created successfully!
pause
