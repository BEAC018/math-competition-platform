# 📥 دليل تثبيت Git وإعداده

## 🖥️ **تثبيت Git على Windows:**

### **الطريقة الأولى: التحميل المباشر (موصى بها)**

1. **اذهب إلى الموقع الرسمي:**
   - https://git-scm.com/download/win

2. **حمل الملف:**
   - سيتم تحميل ملف `.exe` تلقائياً
   - أو انقر "Click here to download manually"

3. **تثبيت Git:**
   - شغل الملف المحمل كـ Administrator
   - اتبع خطوات التثبيت:
     - **Select Components:** اترك الإعدادات الافتراضية
     - **Default Editor:** اختر VS Code أو Notepad++
     - **PATH Environment:** اختر "Git from the command line and also from 3rd-party software"
     - **HTTPS Transport:** اختر "Use the OpenSSL library"
     - **Line Ending:** اختر "Checkout Windows-style, commit Unix-style"
     - **Terminal Emulator:** اختر "Use Windows' default console window"
     - باقي الإعدادات: اترك الافتراضي

4. **التحقق من التثبيت:**
   ```cmd
   # افتح Command Prompt جديد
   git --version
   ```

### **الطريقة الثانية: باستخدام Chocolatey**
```powershell
# افتح PowerShell كـ Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# ثبت Git
choco install git
```

### **الطريقة الثالثة: باستخدام Winget**
```cmd
# افتح Command Prompt كـ Administrator
winget install --id Git.Git -e --source winget
```

---

## 🍎 **تثبيت Git على macOS:**

### **الطريقة الأولى: باستخدام Homebrew (موصى بها)**
```bash
# تثبيت Homebrew إذا لم يكن مثبتاً
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# تثبيت Git
brew install git
```

### **الطريقة الثانية: التحميل المباشر**
1. اذهب إلى: https://git-scm.com/download/mac
2. حمل الملف `.dmg`
3. شغل الملف واتبع التعليمات

### **الطريقة الثالثة: باستخدام MacPorts**
```bash
sudo port install git
```

---

## 🐧 **تثبيت Git على Linux:**

### **Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install git
```

### **CentOS/RHEL/Fedora:**
```bash
# CentOS/RHEL
sudo yum install git

# Fedora
sudo dnf install git
```

### **Arch Linux:**
```bash
sudo pacman -S git
```

### **openSUSE:**
```bash
sudo zypper install git
```

---

## ⚙️ **إعداد Git (مطلوب لأول مرة):**

### **1️⃣ إعداد الهوية:**
```bash
# إعداد الاسم (استبدل "Your Name" باسمك)
git config --global user.name "Ahmed Hassan"

# إعداد البريد الإلكتروني
git config --global user.email "ahmed@example.com"
```

### **2️⃣ إعداد المحرر الافتراضي:**
```bash
# VS Code
git config --global core.editor "code --wait"

# Notepad++ (Windows)
git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"

# Vim
git config --global core.editor "vim"

# Nano
git config --global core.editor "nano"
```

### **3️⃣ إعدادات إضافية مفيدة:**
```bash
# تحسين عرض الألوان
git config --global color.ui auto

# إعداد الفرع الافتراضي
git config --global init.defaultBranch main

# إعداد merge tool
git config --global merge.tool vimdiff

# إعداد push behavior
git config --global push.default simple

# إعداد pull behavior
git config --global pull.rebase false
```

### **4️⃣ التحقق من الإعدادات:**
```bash
# عرض جميع الإعدادات
git config --list

# عرض إعداد محدد
git config user.name
git config user.email
```

---

## 🔐 **إعداد المصادقة مع GitHub:**

### **الطريقة الأولى: Personal Access Token (موصى بها)**

1. **إنشاء Token:**
   - اذهب إلى GitHub.com
   - Settings > Developer settings > Personal access tokens > Tokens (classic)
   - انقر "Generate new token"
   - اختر الصلاحيات المطلوبة (repo, workflow, etc.)
   - انسخ الـ Token (لن تراه مرة أخرى!)

2. **استخدام Token:**
   ```bash
   # عند الـ push أول مرة، استخدم Token بدلاً من كلمة المرور
   git push origin main
   # Username: your-github-username
   # Password: your-personal-access-token
   ```

### **الطريقة الثانية: SSH Keys**

1. **إنشاء SSH Key:**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # اضغط Enter لحفظ في المكان الافتراضي
   # أدخل passphrase (اختياري)
   ```

2. **إضافة SSH Key لـ GitHub:**
   ```bash
   # نسخ المفتاح العام
   # Windows
   type %USERPROFILE%\.ssh\id_ed25519.pub
   
   # macOS/Linux
   cat ~/.ssh/id_ed25519.pub
   ```
   
3. **إضافة في GitHub:**
   - Settings > SSH and GPG keys > New SSH key
   - الصق المفتاح العام

4. **اختبار الاتصال:**
   ```bash
   ssh -T git@github.com
   ```

---

## 🧪 **اختبار Git:**

### **إنشاء مشروع تجريبي:**
```bash
# إنشاء مجلد جديد
mkdir test-git
cd test-git

# تهيئة Git repository
git init

# إنشاء ملف تجريبي
echo "# Test Project" > README.md

# إضافة الملف
git add README.md

# أول commit
git commit -m "Initial commit"

# عرض التاريخ
git log
```

---

## 🔧 **حل المشاكل الشائعة:**

### **مشكلة: Git command not found**
```bash
# Windows: أعد تشغيل Command Prompt
# أو أضف Git للـ PATH يدوياً

# macOS/Linux: تأكد من التثبيت
which git
```

### **مشكلة: Permission denied**
```bash
# تأكد من صلاحيات SSH أو استخدم HTTPS
git remote set-url origin https://github.com/username/repo.git
```

### **مشكلة: SSL certificate problem**
```bash
# حل مؤقت (غير آمن)
git config --global http.sslVerify false

# حل دائم: تحديث certificates
git config --global http.sslCAInfo /path/to/certificate.pem
```

### **مشكلة: Line ending warnings**
```bash
# Windows
git config --global core.autocrlf true

# macOS/Linux
git config --global core.autocrlf input
```

---

## 📚 **أوامر Git الأساسية:**

### **إعداد Repository:**
```bash
git init                    # تهيئة repository جديد
git clone <url>            # استنساخ repository موجود
git remote add origin <url> # ربط بـ remote repository
```

### **إدارة الملفات:**
```bash
git add <file>             # إضافة ملف للـ staging
git add .                  # إضافة جميع الملفات
git commit -m "message"    # حفظ التغييرات
git status                 # عرض حالة الملفات
```

### **التزامن مع Remote:**
```bash
git push                   # رفع التغييرات
git pull                   # سحب التحديثات
git fetch                  # سحب بدون دمج
```

### **إدارة الفروع:**
```bash
git branch                 # عرض الفروع
git checkout -b <branch>   # إنشاء فرع جديد
git merge <branch>         # دمج فرع
```

---

## 🎯 **الخطوة التالية:**

بعد تثبيت وإعداد Git، يمكنك الآن:

1. **رفع مشروع منصة المسابقات:**
   ```bash
   cd "C:\Users\aiitc\OneDrive\Bureau\math - Copy"
   git init
   git add .
   git commit -m "Initial commit: Math Competition Platform v2.0.0"
   ```

2. **ربط بـ GitHub:**
   ```bash
   git remote add origin https://github.com/USERNAME/math-competition-platform.git
   git push -u origin main
   ```

**🎉 مبروك! Git جاهز للاستخدام!**
