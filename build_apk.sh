#!/bin/bash
# سكريبت بناء APK للتطبيق

echo "📱 بناء تطبيق المسابقات الرياضية APK"
echo "========================================"

# التحقق من وجود buildozer
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer غير مثبت. يرجى تثبيته أولاً:"
    echo "pip3 install buildozer"
    exit 1
fi

# التحقق من وجود الملفات المطلوبة
if [ ! -f "main.py" ]; then
    echo "❌ ملف main.py غير موجود"
    exit 1
fi

if [ ! -f "buildozer.spec" ]; then
    echo "❌ ملف buildozer.spec غير موجود"
    exit 1
fi

echo "✅ جميع الملفات المطلوبة موجودة"

# تنظيف البناء السابق
echo "🧹 تنظيف البناء السابق..."
buildozer android clean

# بناء APK
echo "🏗️ بناء APK..."
buildozer android debug

# التحقق من نجاح البناء
if [ -f "bin/*.apk" ]; then
    echo "✅ تم بناء APK بنجاح!"
    echo "📁 الملف: $(ls bin/*.apk)"
    echo "📏 الحجم: $(du -h bin/*.apk | cut -f1)"
    
    # نسخ APK إلى اسم واضح
    cp bin/*.apk math-competition-app.apk
    echo "📱 تم نسخ APK إلى: math-competition-app.apk"
    
else
    echo "❌ فشل في بناء APK"
    exit 1
fi

echo "🎉 اكتمل البناء بنجاح!"
