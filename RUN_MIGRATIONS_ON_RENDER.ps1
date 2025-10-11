# Script to run migrations on Render PostgreSQL database
# Run this from PowerShell: .\RUN_MIGRATIONS_ON_RENDER.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running Migrations on Render Database" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set database URL
$env:DATABASE_URL = "postgresql://ecom_postgres_db_za4r_user:elNITLRgmSTvJ2mZG3MG3YcDkqD1q51E@dpg-d3khj849c44c73agblb0-a/ecom_postgres_db_za4r"

# Change to backend directory
Set-Location "backend"

Write-Host "📦 Installing psycopg2 if needed..." -ForegroundColor Yellow
pip install psycopg2-binary

Write-Host ""
Write-Host "🗄️ Running migrations..." -ForegroundColor Yellow
python manage.py migrate --noinput

Write-Host ""
Write-Host "👤 Creating superuser..." -ForegroundColor Yellow
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(phone='01234567890', password='admin123', first_name='Admin', last_name='User') if not User.objects.filter(phone='01234567890').exists() else print('Superuser already exists')"

Write-Host ""
Write-Host "🎫 Creating coupons..." -ForegroundColor Yellow
python create_coupons.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Done! Database is ready." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "You can now access:" -ForegroundColor White
Write-Host "  Backend: https://ecom-parent-project.onrender.com/admin/" -ForegroundColor Cyan
Write-Host "  Login: 01234567890 / admin123" -ForegroundColor Cyan
Write-Host ""

# Return to original directory
Set-Location ".."

Read-Host "Press Enter to exit"