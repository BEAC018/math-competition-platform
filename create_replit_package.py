#!/usr/bin/env python3
"""
Script to create a deployment package for Replit
Creates a zip file with all necessary files for the math competition platform
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_replit_package():
    """Create a zip package for Replit deployment"""
    
    # Define the package name
    package_name = "math-competition-replit-package.zip"
    temp_dir = "replit_package_temp"
    
    # Create temporary directory
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    print("🚀 Creating Replit deployment package...")
    
    # List of directories to include
    directories_to_copy = [
        "alhassan",
        "accounts", 
        "competitions",
        "dashboard",
        "templates",
        "static"
    ]
    
    # List of files to include
    files_to_copy = [
        "manage.py",
        "requirements.txt",
        "db.sqlite3",
        ".replit",
        "REPLIT_DEPLOYMENT_GUIDE.md"
    ]
    
    # Copy directories
    for directory in directories_to_copy:
        if os.path.exists(directory):
            print(f"📁 Copying directory: {directory}")
            shutil.copytree(directory, os.path.join(temp_dir, directory))
        else:
            print(f"⚠️  Directory not found: {directory}")
    
    # Copy files
    for file in files_to_copy:
        if os.path.exists(file):
            print(f"📄 Copying file: {file}")
            shutil.copy2(file, temp_dir)
        else:
            print(f"⚠️  File not found: {file}")
    
    # Create additional files for Replit
    
    # Create main.py for Replit
    main_py_content = '''#!/usr/bin/env python3
"""
Main entry point for Replit deployment
"""

import os
import subprocess
import sys

def setup_django():
    """Setup Django application"""
    print("🔧 Setting up Django application...")
    
    # Install requirements
    print("📦 Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Run migrations
    print("🗄️  Running database migrations...")
    subprocess.run([sys.executable, "manage.py", "migrate"])
    
    # Collect static files
    print("📁 Collecting static files...")
    subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"])
    
    print("✅ Setup complete!")

def run_server():
    """Run the Django development server"""
    print("🚀 Starting Django server...")
    subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])

if __name__ == "__main__":
    setup_django()
    run_server()
'''
    
    with open(os.path.join(temp_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(main_py_content)
    
    # Create README for Replit
    readme_content = '''# 🎮 Math Competition Platform - Replit Deployment

## 🚀 Quick Start:

1. Upload all files to your Replit project
2. Click the "Run" button
3. Wait for setup to complete
4. Your app will be available at: https://your-repl-name.your-username.repl.co

## 🎯 Student Access:

**Direct Link:** https://your-repl-name.your-username.repl.co/student/login/
**Access Code:** ben25

## 👩‍🏫 Teacher Access:

**Analytics:** https://your-repl-name.your-username.repl.co/competitions/student-analytics/
**Admin:** https://your-repl-name.your-username.repl.co/admin/

## 📱 Share with Students:

```
🎯 منصة المسابقات الرياضية

🌐 الرابط: https://your-repl-name.your-username.repl.co/student/login/
🔑 رمز الدخول: ben25

📝 التعليمات:
1. انقر على الرابط
2. اكتب اسمك الكامل  
3. اكتب الرمز: ben25
4. اختر مستواك الدراسي
5. ابدأ المسابقة!

🎮 استمتعوا بالتعلم!
```

## 🔧 Manual Setup (if needed):

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
```

## 🎉 Features:

✅ 9 difficulty levels
✅ Student and teacher interfaces  
✅ Real-time analytics
✅ Excel/PDF exports
✅ Arabic language support
✅ Mobile-friendly design

Enjoy your math competition platform! 🚀
'''
    
    with open(os.path.join(temp_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Create the zip file
    print(f"📦 Creating zip package: {package_name}")
    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
                print(f"  ✅ Added: {arcname}")
    
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
    
    # Get file size
    file_size = os.path.getsize(package_name) / (1024 * 1024)  # MB
    
    print(f"\n🎉 Package created successfully!")
    print(f"📁 File: {package_name}")
    print(f"📏 Size: {file_size:.2f} MB")
    print(f"📍 Location: {os.path.abspath(package_name)}")
    
    print(f"\n🚀 Next steps:")
    print(f"1. Go to https://replit.com")
    print(f"2. Create new Python Repl: 'math-competition-platform'")
    print(f"3. Upload the zip file: {package_name}")
    print(f"4. Extract all files")
    print(f"5. Click 'Run' button")
    print(f"6. Share the link with your students!")

if __name__ == "__main__":
    create_replit_package()
