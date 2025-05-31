# 🔧 دليل تثبيت Git يدوياً وإكمال رفع المشروع

## 📥 **الخطوة 1: تحميل وتثبيت Git**

### **تحميل Git:**
1. **اذهب إلى:** https://git-scm.com/download/win
2. **انقر على:** "64-bit Git for Windows Setup"
3. **حفظ الملف** في مجلد Downloads

### **تثبيت Git:**
1. **شغل الملف المحمل** كـ Administrator
2. **اتبع خطوات التثبيت:**
   - **License:** انقر Next
   - **Installation Location:** اترك الافتراضي
   - **Select Components:** اترك الافتراضي
   - **Start Menu Folder:** اترك الافتراضي
   - **Default Editor:** اختر "Use Visual Studio Code" أو "Use Notepad++"
   - **Initial Branch:** اختر "Let Git decide"
   - **PATH Environment:** اختر "Git from the command line and also from 3rd-party software"
   - **SSH Executable:** اختر "Use bundled OpenSSH"
   - **HTTPS Transport:** اختر "Use the OpenSSL library"
   - **Line Ending:** اختر "Checkout Windows-style, commit Unix-style"
   - **Terminal Emulator:** اختر "Use Windows' default console window"
   - **Git Pull:** اختر "Default (fast-forward or merge)"
   - **Credential Helper:** اختر "Git Credential Manager"
   - **Extra Options:** اترك الافتراضي
   - **Experimental Features:** لا تختر شيء
3. **انقر Install** وانتظر الانتهاء
4. **انقر Finish**

### **التحقق من التثبيت:**
1. **افتح Command Prompt جديد**
2. **اكتب:** `git --version`
3. **يجب أن ترى:** `git version 2.49.0.windows.1`

---

## ⚙️ **الخطوة 2: إعداد Git**

### **افتح Command Prompt واكتب:**
```cmd
git config --global user.name "BEAC1"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

---

## 🚀 **الخطوة 3: رفع المشروع إلى GitHub**

### **1️⃣ انتقل إلى مجلد المشروع:**
```cmd
cd "C:\Users\aiitc\OneDrive\Bureau\math - Copy"
```

### **2️⃣ تهيئة Git:**
```cmd
git init
```

### **3️⃣ إضافة جميع الملفات:**
```cmd
git add .
```

### **4️⃣ إنشاء أول commit:**
```cmd
git commit -m "Initial commit: Math Competition Platform v2.0.0

- منصة تعليمية تفاعلية لمسابقات الحساب
- دعم 9 مستويات صعوبة متدرجة  
- واجهة عربية جميلة ومتجاوبة
- نظام إدارة شامل للمعلمين
- إحصائيات وتقارير مفصلة
- تحسينات الأداء والأمان"
```

### **5️⃣ ربط بـ GitHub:**
```cmd
git remote add origin https://github.com/BEAC1/math-competition-platform.git
```

### **6️⃣ تعيين الفرع الرئيسي:**
```cmd
git branch -M main
```

### **7️⃣ رفع الملفات:**
```cmd
git push -u origin main
```

---

## 🔐 **الخطوة 4: المصادقة مع GitHub**

### **إذا طُلب منك تسجيل الدخول:**

#### **Username:** `BEAC1`

#### **Password:** استخدم Personal Access Token

### **إنشاء Personal Access Token:**
1. **اذهب إلى GitHub.com**
2. **انقر على صورتك الشخصية** (أعلى اليمين)
3. **Settings**
4. **Developer settings** (أسفل القائمة الجانبية)
5. **Personal access tokens**
6. **Tokens (classic)**
7. **Generate new token**
8. **Note:** اكتب "Math Competition Platform"
9. **Expiration:** اختر "No expiration" أو "90 days"
10. **Select scopes:** اختر:
    - ✅ **repo** (Full control of private repositories)
    - ✅ **workflow** (Update GitHub Action workflows)
11. **Generate token**
12. **انسخ الـ Token** (لن تراه مرة أخرى!)

### **استخدام Token:**
عند طلب كلمة المرور، الصق الـ Token بدلاً من كلمة المرور.

---

## 📋 **الخطوة 5: تحسين Repository**

### **بعد الرفع الناجح:**

#### **1️⃣ تحديث وصف Repository:**
- اذهب إلى صفحة GitHub Repository
- انقر على ⚙️ **Settings**
- في **Repository name:** تأكد أنه `math-competition-platform`
- في **Description:** أضف:
  ```
  منصة تعليمية تفاعلية لمسابقات الحساب للطلاب من الصف الأول إلى التاسع - Interactive Math Competition Platform for students grades 1-9
  ```
- في **Website:** أضف (اختياري):
  ```
  https://beac1.github.io/math-competition-platform
  ```

#### **2️⃣ إضافة Topics:**
- في صفحة Repository الرئيسية
- انقر على ⚙️ **بجانب About**
- أضف Topics:
  ```
  django python education math arabic competition platform interactive learning
  ```

#### **3️⃣ تفعيل GitHub Pages (اختياري):**
- **Settings** > **Pages**
- **Source:** Deploy from a branch
- **Branch:** main
- **Folder:** / (root)
- **Save**

---

## ✅ **التحقق من النجاح**

### **يجب أن ترى في GitHub:**
- ✅ جميع ملفات المشروع (150+ ملف)
- ✅ README.md يظهر بشكل جميل مع badges
- ✅ ملفات التوثيق (CHANGELOG, CONTRIBUTING, etc.)
- ✅ ملفات الكود (Django, HTML, CSS, JS)
- ✅ تاريخ الـ commits

### **في صفحة Repository:**
- ✅ الوصف واضح ومفيد
- ✅ Topics مضافة
- ✅ README يظهر المحتوى بشكل صحيح
- ✅ عدد الملفات والمجلدات صحيح

---

## 🎯 **خطوات إضافية (اختيارية)**

### **1️⃣ إضافة Collaborators:**
- **Settings** > **Manage access**
- **Invite a collaborator**

### **2️⃣ إعداد Branch Protection:**
- **Settings** > **Branches**
- **Add rule** للفرع main

### **3️⃣ إضافة Issues Templates:**
- **Settings** > **Features**
- **Set up templates** للـ Issues

---

## 🆘 **حل المشاكل الشائعة**

### **مشكلة: Git command not found**
```cmd
# أعد تشغيل Command Prompt بعد تثبيت Git
# أو أعد تشغيل الكمبيوتر
```

### **مشكلة: Authentication failed**
```cmd
# تأكد من استخدام Personal Access Token
# وليس كلمة المرور العادية
```

### **مشكلة: Repository already exists**
```cmd
# إذا كان Repository موجود، استخدم:
git remote set-url origin https://github.com/BEAC1/math-competition-platform.git
git push -u origin main
```

### **مشكلة: Large files**
```cmd
# إذا كانت هناك ملفات كبيرة، أضفها للـ .gitignore:
echo "*.exe" >> .gitignore
echo "*.zip" >> .gitignore
git add .gitignore
git commit -m "Update gitignore"
```

---

## 🎉 **النتيجة النهائية**

بعد إكمال هذه الخطوات، ستحصل على:

✅ **Git مثبت ومُعد بشكل صحيح**  
✅ **Repository منظم على GitHub**  
✅ **جميع ملفات المشروع مرفوعة**  
✅ **توثيق شامل ومفصل**  
✅ **Repository جاهز للمشاركة والتطوير**  

---

## 📞 **الدعم**

إذا واجهت أي مشاكل:
1. تأكد من تثبيت Git بشكل صحيح
2. تأكد من إعداد Personal Access Token
3. تأكد من صحة رابط Repository
4. جرب إعادة تشغيل Command Prompt

**🚀 مبروك! مشروعك الآن على GitHub!**
