# ========================================
#    🔍 سكريبت تشخيص المشاكل
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🔍 تشخيص المشاكل" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# قائمة المشاكل
$problems = @(
    @{
        Number = 1
        Name = "الخصم لا يظهر في بطاقة المنتج"
        File = "frontend/src/pages/Home.jsx"
        Check = "discount_percentage"
    },
    @{
        Number = 2
        Name = "يمكن إضافة أكثر من المخزون المتوفر"
        File = "frontend/src/pages/Home.jsx"
        Check = "product.stock"
    },
    @{
        Number = 3
        Name = "خطأ 405 عند إرسال الطلب"
        File = "frontend/src/api.js"
        Check = "params:"
    },
    @{
        Number = 4
        Name = "خطأ تسجيل الدخول يوجه إلى 404"
        File = "frontend/src/pages/Login.jsx"
        Check = "error.response?.status"
    },
    @{
        Number = 5
        Name = "الصور تختفي من ImgBB"
        File = "backend/products/models.py"
        Check = "main_image"
    }
)

Write-Host "اختر المشكلة التي تريد تشخيصها:" -ForegroundColor Yellow
Write-Host ""

foreach ($problem in $problems) {
    Write-Host "  $($problem.Number). $($problem.Name)" -ForegroundColor White
}

Write-Host ""
Write-Host "  0. تشخيص جميع المشاكل" -ForegroundColor Cyan
Write-Host ""

$choice = Read-Host "أدخل رقم المشكلة"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Test-Problem {
    param (
        [hashtable]$Problem
    )
    
    Write-Host "🔍 تشخيص: $($Problem.Name)" -ForegroundColor Yellow
    Write-Host ""
    
    if (Test-Path $Problem.File) {
        Write-Host "  ✅ الملف موجود: $($Problem.File)" -ForegroundColor Green
        
        $content = Get-Content $Problem.File -Raw
        if ($content -match [regex]::Escape($Problem.Check)) {
            Write-Host "  ✅ التحديث موجود في الملف" -ForegroundColor Green
            Write-Host ""
            Write-Host "  📝 السطر المطابق:" -ForegroundColor Cyan
            $lines = Get-Content $Problem.File | Select-String $Problem.Check -Context 2
            foreach ($line in $lines) {
                Write-Host "    $($line.Line)" -ForegroundColor White
            }
        } else {
            Write-Host "  ❌ التحديث غير موجود في الملف!" -ForegroundColor Red
            Write-Host ""
            Write-Host "  💡 الحل:" -ForegroundColor Yellow
            Write-Host "    - تأكد من رفع التحديثات من GitHub" -ForegroundColor White
            Write-Host "    - أو أعد تطبيق التحديثات" -ForegroundColor White
        }
    } else {
        Write-Host "  ❌ الملف غير موجود: $($Problem.File)" -ForegroundColor Red
        Write-Host ""
        Write-Host "  💡 الحل:" -ForegroundColor Yellow
        Write-Host "    - تأكد من أنك في المجلد الصحيح" -ForegroundColor White
        Write-Host "    - المجلد الصحيح: C:\Users\a\Desktop\ecom_setup\ecom_project\ecom_project" -ForegroundColor White
    }
    
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host ""
}

if ($choice -eq "0") {
    # تشخيص جميع المشاكل
    foreach ($problem in $problems) {
        Test-Problem -Problem $problem
    }
} elseif ($choice -ge 1 -and $choice -le $problems.Count) {
    # تشخيص مشكلة محددة
    $selectedProblem = $problems[$choice - 1]
    Test-Problem -Problem $selectedProblem
    
    # عرض معلومات إضافية حسب المشكلة
    Write-Host "📚 معلومات إضافية:" -ForegroundColor Cyan
    Write-Host ""
    
    switch ($choice) {
        "1" {
            Write-Host "  المشكلة: الخصم لا يظهر في بطاقة المنتج" -ForegroundColor White
            Write-Host ""
            Write-Host "  الحل المطبق:" -ForegroundColor Yellow
            Write-Host "    - تم إضافة حقول الخصم في Serializer" -ForegroundColor White
            Write-Host "    - تم تحديث عرض السعر في Home.jsx" -ForegroundColor White
            Write-Host "    - الآن يظهر السعر الأصلي مع خط" -ForegroundColor White
            Write-Host ""
            Write-Host "  التحقق:" -ForegroundColor Yellow
            Write-Host "    1. افتح الموقع" -ForegroundColor White
            Write-Host "    2. ابحث عن منتج عليه خصم" -ForegroundColor White
            Write-Host "    3. يجب أن ترى السعر الأصلي مع خط" -ForegroundColor White
            Write-Host "    4. والسعر الجديد بلون مميز" -ForegroundColor White
        }
        "2" {
            Write-Host "  المشكلة: يمكن إضافة أكثر من المخزون المتوفر" -ForegroundColor White
            Write-Host ""
            Write-Host "  الحل المطبق:" -ForegroundColor Yellow
            Write-Host "    - تم إضافة التحقق من المخزون في addToCart" -ForegroundColor White
            Write-Host "    - رسالة خطأ عند تجاوز المخزون" -ForegroundColor White
            Write-Host "    - زر معطل عند نفاد المخزون" -ForegroundColor White
            Write-Host ""
            Write-Host "  التحقق:" -ForegroundColor Yellow
            Write-Host "    1. افتح الموقع" -ForegroundColor White
            Write-Host "    2. جرب إضافة منتج للسلة" -ForegroundColor White
            Write-Host "    3. جرب إضافة أكثر من المتوفر" -ForegroundColor White
            Write-Host "    4. يجب أن تظهر رسالة خطأ" -ForegroundColor White
        }
        "3" {
            Write-Host "  المشكلة: خطأ 405 عند إرسال الطلب" -ForegroundColor White
            Write-Host ""
            Write-Host "  الحل المطبق:" -ForegroundColor Yellow
            Write-Host "    - تم إزالة timestamp parameter من api.js" -ForegroundColor White
            Write-Host "    - تم إصلاح URLs في Backend" -ForegroundColor White
            Write-Host "    - الآن الطلبات تُرسل بنجاح" -ForegroundColor White
            Write-Host ""
            Write-Host "  التحقق:" -ForegroundColor Yellow
            Write-Host "    1. افتح الموقع" -ForegroundColor White
            Write-Host "    2. أضف منتجات للسلة" -ForegroundColor White
            Write-Host "    3. اذهب للدفع" -ForegroundColor White
            Write-Host "    4. أكمل الطلب" -ForegroundColor White
            Write-Host "    5. يجب أن يُرسل بنجاح" -ForegroundColor White
        }
        "4" {
            Write-Host "  المشكلة: خطأ تسجيل الدخول يوجه إلى 404" -ForegroundColor White
            Write-Host ""
            Write-Host "  الحل المطبق:" -ForegroundColor Yellow
            Write-Host "    - تم تحسين معالجة الأخطاء في Login.jsx" -ForegroundColor White
            Write-Host "    - رسائل خطأ واضحة بالعربية" -ForegroundColor White
            Write-Host "    - عدم التوجيه عند الخطأ" -ForegroundColor White
            Write-Host ""
            Write-Host "  التحقق:" -ForegroundColor Yellow
            Write-Host "    1. افتح صفحة تسجيل الدخول" -ForegroundColor White
            Write-Host "    2. أدخل رقم هاتف خاطئ" -ForegroundColor White
            Write-Host "    3. يجب أن تظهر رسالة خطأ" -ForegroundColor White
            Write-Host "    4. يجب أن تبقى في نفس الصفحة" -ForegroundColor White
        }
        "5" {
            Write-Host "  المشكلة: الصور تختفي من ImgBB" -ForegroundColor White
            Write-Host ""
            Write-Host "  السبب:" -ForegroundColor Yellow
            Write-Host "    - ImgBB قد يحذف الصور بعد فترة" -ForegroundColor White
            Write-Host "    - خاصة إذا تم استخدام expiration parameter" -ForegroundColor White
            Write-Host ""
            Write-Host "  الحلول المقترحة:" -ForegroundColor Yellow
            Write-Host "    1. استخدام Cloudinary (موصى به)" -ForegroundColor White
            Write-Host "    2. استخدام Render.com Disk + WhiteNoise" -ForegroundColor White
            Write-Host "    3. التأكد من عدم استخدام expiration" -ForegroundColor White
            Write-Host ""
            Write-Host "  📄 راجع ملف: 📋_حل_مشكلة_الصور_ImgBB.txt" -ForegroundColor Cyan
        }
    }
} else {
    Write-Host "❌ اختيار غير صحيح!" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# انتظار ضغطة مفتاح
Write-Host "اضغط أي مفتاح للخروج..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")