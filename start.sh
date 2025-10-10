#!/bin/bash

# MIMI STORE - Quick Start Script
echo "🚀 بدء تشغيل MIMI STORE..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 إنشاء البيئة الافتراضية..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 تفعيل البيئة الافتراضية..."
source venv/bin/activate

# Install backend dependencies
echo "📥 تثبيت متطلبات Backend..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ تشغيل migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 إنشاء مستخدم مشرف..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
from users.models import User
if not User.objects.filter(phone='admin').exists():
    User.objects.create_superuser(phone='admin', password='admin123', is_admin=True)
    print('تم إنشاء مستخدم مشرف: phone=admin, password=admin123')
else:
    print('مستخدم المشرف موجود بالفعل')
"

# Start backend server in background
echo "🖥️ تشغيل Backend server..."
python manage.py runserver &
BACKEND_PID=$!

# Install frontend dependencies and start
echo "🎨 إعداد Frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 تثبيت متطلبات Frontend..."
    npm install
fi

# Install Tailwind CSS dependencies
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
npm install -D @tailwindcss/forms @tailwindcss/aspect-ratio

# Start frontend server
echo "🌐 تشغيل Frontend server..."
npm start &
FRONTEND_PID=$!

# Wait for servers to start
sleep 5

echo "✅ تم تشغيل MIMI STORE بنجاح!"
echo ""
echo "🔗 الروابط:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000/api"
echo "   Admin Panel: http://localhost:3000/admin-panel"
echo ""
echo "👤 بيانات المشرف:"
echo "   الهاتف: admin"
echo "   كلمة المرور: admin123"
echo ""
echo "⏹️ لإيقاف الخوادم، اضغط Ctrl+C"

# Wait for user to stop
wait $BACKEND_PID $FRONTEND_PID