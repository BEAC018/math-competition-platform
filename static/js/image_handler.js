/**
 * 🖼️ معالج الصور المتقدم
 * Advanced Image Handler
 */

class ImageHandler {
    constructor() {
        this.init();
    }

    init() {
        this.setupImageErrorHandling();
        this.setupLazyLoading();
        this.setupImagePreview();
        this.setupProfileImageFallbacks();
    }

    /**
     * إعداد معالجة أخطاء الصور
     */
    setupImageErrorHandling() {
        // معالجة الصور المكسورة
        document.addEventListener('error', (e) => {
            if (e.target.tagName === 'IMG') {
                this.handleBrokenImage(e.target);
            }
        }, true);

        // فحص الصور الموجودة
        document.querySelectorAll('img').forEach(img => {
            if (!img.complete || img.naturalHeight === 0) {
                this.handleBrokenImage(img);
            }
        });
    }

    /**
     * معالجة الصورة المكسورة
     */
    handleBrokenImage(img) {
        const isProfileImage = img.classList.contains('profile-image') || 
                              img.closest('.profile-image-container');
        
        if (isProfileImage) {
            this.createProfileFallback(img);
        } else {
            this.createGenericFallback(img);
        }
    }

    /**
     * إنشاء صورة بديلة للملف الشخصي
     */
    createProfileFallback(img) {
        const container = img.parentElement;
        const size = Math.min(img.offsetWidth || 150, img.offsetHeight || 150);
        
        // إخفاء الصورة المكسورة
        img.style.display = 'none';
        
        // إنشاء عنصر بديل
        const fallback = document.createElement('div');
        fallback.className = 'profile-image-placeholder rounded-circle avatar-style-1';
        fallback.style.cssText = `
            width: ${size}px;
            height: ${size}px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
        `;
        
        // إضافة أيقونة المستخدم
        const icon = document.createElement('i');
        icon.className = 'fas fa-user';
        icon.style.cssText = `
            font-size: ${size * 0.4}px;
            color: white;
            opacity: 0.9;
        `;
        
        fallback.appendChild(icon);
        
        // إدراج العنصر البديل
        if (container) {
            container.appendChild(fallback);
        } else {
            img.parentNode.insertBefore(fallback, img.nextSibling);
        }
    }

    /**
     * إنشاء صورة بديلة عامة
     */
    createGenericFallback(img) {
        const fallback = document.createElement('div');
        fallback.className = 'image-fallback';
        fallback.style.cssText = `
            width: ${img.offsetWidth || 200}px;
            height: ${img.offsetHeight || 150}px;
            background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            color: #9CA3AF;
            font-size: 2rem;
            border: 2px dashed #D1D5DB;
        `;
        
        fallback.innerHTML = '🖼️';
        
        // إخفاء الصورة المكسورة
        img.style.display = 'none';
        
        // إدراج العنصر البديل
        img.parentNode.insertBefore(fallback, img.nextSibling);
    }

    /**
     * إعداد التحميل الكسول للصور
     */
    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        this.loadImage(img);
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    /**
     * تحميل الصورة
     */
    loadImage(img) {
        img.classList.add('image-loading');
        
        const tempImg = new Image();
        tempImg.onload = () => {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
            img.classList.remove('image-loading');
            img.classList.add('image-loaded');
        };
        
        tempImg.onerror = () => {
            img.classList.remove('image-loading');
            this.handleBrokenImage(img);
        };
        
        tempImg.src = img.dataset.src;
    }

    /**
     * إعداد معاينة الصور
     */
    setupImagePreview() {
        document.querySelectorAll('input[type="file"][accept*="image"]').forEach(input => {
            input.addEventListener('change', (e) => {
                this.previewImage(e.target);
            });
        });
    }

    /**
     * معاينة الصورة المختارة
     */
    previewImage(input) {
        if (input.files && input.files[0]) {
            const file = input.files[0];
            
            // التحقق من نوع الملف
            if (!file.type.startsWith('image/')) {
                this.showError('يرجى اختيار ملف صورة صحيح');
                return;
            }
            
            // التحقق من حجم الملف (5MB)
            if (file.size > 5 * 1024 * 1024) {
                this.showError('حجم الصورة كبير جداً. يرجى اختيار صورة أصغر من 5 ميجابايت');
                return;
            }
            
            const reader = new FileReader();
            reader.onload = (e) => {
                this.updateImagePreview(input, e.target.result);
            };
            reader.readAsDataURL(file);
        }
    }

    /**
     * تحديث معاينة الصورة
     */
    updateImagePreview(input, imageSrc) {
        const previewId = input.getAttribute('data-preview') || 'profile-preview';
        const preview = document.getElementById(previewId);
        const placeholder = document.getElementById('profile-preview-placeholder') || 
                           document.querySelector('.profile-image-placeholder');
        const icon = document.getElementById('profile-icon');
        
        if (preview) {
            preview.src = imageSrc;
            preview.style.display = 'block';
            preview.classList.remove('d-none');
        }
        
        if (placeholder) {
            placeholder.style.display = 'none';
        }
        
        if (icon) {
            icon.style.display = 'none';
        }
    }

    /**
     * إعداد الصور الشخصية البديلة
     */
    setupProfileImageFallbacks() {
        // إنشاء صور شخصية بديلة بناءً على الأحرف الأولى
        document.querySelectorAll('.profile-image-placeholder:not([data-processed])').forEach(placeholder => {
            const userName = placeholder.getAttribute('title') || 
                           placeholder.getAttribute('data-name') || 
                           'مستخدم';
            
            this.createInitialsAvatar(placeholder, userName);
            placeholder.setAttribute('data-processed', 'true');
        });
    }

    /**
     * إنشاء صورة شخصية من الأحرف الأولى
     */
    createInitialsAvatar(placeholder, name) {
        const initials = this.getInitials(name);
        const colors = [
            'avatar-style-1', 'avatar-style-2', 'avatar-style-3', 
            'avatar-style-4', 'avatar-style-5'
        ];
        
        // اختيار لون بناءً على الاسم
        const colorIndex = name.length % colors.length;
        placeholder.classList.add(colors[colorIndex]);
        
        // إضافة الأحرف الأولى
        const initialsElement = document.createElement('span');
        initialsElement.textContent = initials;
        initialsElement.style.cssText = `
            font-size: ${placeholder.offsetWidth * 0.3}px;
            font-weight: 700;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        `;
        
        // إزالة المحتوى السابق وإضافة الأحرف
        placeholder.innerHTML = '';
        placeholder.appendChild(initialsElement);
    }

    /**
     * استخراج الأحرف الأولى من الاسم
     */
    getInitials(name) {
        const words = name.trim().split(' ');
        if (words.length >= 2) {
            return (words[0][0] + words[1][0]).toUpperCase();
        } else if (words.length === 1) {
            return words[0].substring(0, 2).toUpperCase();
        }
        return 'مج'; // مستخدم جديد
    }

    /**
     * عرض رسالة خطأ
     */
    showError(message) {
        // يمكن تخصيص هذه الدالة لعرض الأخطاء بطريقة أفضل
        alert(message);
    }

    /**
     * تحديث جميع الصور
     */
    refreshImages() {
        this.setupImageErrorHandling();
        this.setupProfileImageFallbacks();
    }
}

// تهيئة معالج الصور عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    window.imageHandler = new ImageHandler();
});

// إعادة تهيئة معالج الصور عند إضافة محتوى جديد
document.addEventListener('DOMNodeInserted', () => {
    if (window.imageHandler) {
        setTimeout(() => {
            window.imageHandler.refreshImages();
        }, 100);
});

// دالة عامة لمعاينة الصور (للاستخدام في النماذج)
function previewImage(input) {
    if (window.imageHandler) {
        window.imageHandler.previewImage(input);
    }
}
