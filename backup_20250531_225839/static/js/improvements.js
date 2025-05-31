/**
 * تحسينات JavaScript لمنصة المسابقات الرياضية
 * JavaScript improvements for Math Competition Platform
 */

// إعدادات عامة
const CONFIG = {
    loadingTimeout: 30000, // 30 ثانية
    animationDuration: 300,
    debounceDelay: 500
};

// معالج رسائل التحميل
class LoadingManager {
    constructor() {
        this.loadingElement = null;
        this.isLoading = false;
    }

    show(message = 'جاري التحميل...') {
        if (this.isLoading) return;
        
        this.isLoading = true;
        
        // إنشاء عنصر التحميل
        this.loadingElement = document.createElement('div');
        this.loadingElement.id = 'loading-overlay';
        this.loadingElement.className = 'loading-overlay';
        this.loadingElement.innerHTML = `
            <div class="loading-content">
                <div class="spinner-border text-primary" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
                <p class="mt-3 text-center">${message}</p>
            </div>
        `;
        
        // إضافة الأنماط
        this.loadingElement.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            backdrop-filter: blur(3px);
        `;
        
        document.body.appendChild(this.loadingElement);
        
        // إخفاء تلقائي بعد مهلة زمنية
        setTimeout(() => {
            if (this.isLoading) {
                this.hide();
                console.warn('Loading timeout reached');
            }
        }, CONFIG.loadingTimeout);
    }

    hide() {
        if (!this.isLoading || !this.loadingElement) return;
        
        this.isLoading = false;
        
        // إضافة تأثير الاختفاء
        this.loadingElement.style.opacity = '0';
        this.loadingElement.style.transition = `opacity ${CONFIG.animationDuration}ms ease-out`;
        
        setTimeout(() => {
            if (this.loadingElement && this.loadingElement.parentNode) {
                this.loadingElement.parentNode.removeChild(this.loadingElement);
            }
            this.loadingElement = null;
        }, CONFIG.animationDuration);
    }

    updateMessage(message) {
        if (this.loadingElement) {
            const messageElement = this.loadingElement.querySelector('p');
            if (messageElement) {
                messageElement.textContent = message;
            }
        }
    }
}

// إنشاء مثيل عام لمعالج التحميل
const loadingManager = new LoadingManager();

// معالج الأخطاء المحسن
class ErrorHandler {
    static show(message, type = 'error') {
        const alertClass = type === 'error' ? 'alert-danger' : 
                          type === 'warning' ? 'alert-warning' : 
                          type === 'success' ? 'alert-success' : 'alert-info';
        
        const alertElement = document.createElement('div');
        alertElement.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
        alertElement.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 10000;
            min-width: 300px;
            max-width: 500px;
        `;
        
        alertElement.innerHTML = `
            <strong>${type === 'error' ? 'خطأ!' : type === 'warning' ? 'تحذير!' : type === 'success' ? 'نجح!' : 'معلومة!'}</strong>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertElement);
        
        // إزالة تلقائية بعد 5 ثوان
        setTimeout(() => {
            if (alertElement.parentNode) {
                alertElement.remove();
            }
        }, 5000);
    }
}

// تحسين النماذج
class FormEnhancer {
    static enhance() {
        // إضافة التحقق من صحة البيانات
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', function(e) {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>جاري الإرسال...';
                    
                    // إعادة تفعيل الزر بعد 10 ثوان كحد أقصى
                    setTimeout(() => {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || 'إرسال';
                    }, 10000);
                }
            });
        });
        
        // حفظ النص الأصلي للأزرار
        document.querySelectorAll('button[type="submit"]').forEach(btn => {
            btn.setAttribute('data-original-text', btn.innerHTML);
        });
    }
}

// تحسين الجداول
class TableEnhancer {
    static enhance() {
        // إضافة فلترة للجداول
        document.querySelectorAll('table').forEach(table => {
            if (table.rows.length > 10) {
                this.addTableFilter(table);
            }
        });
    }
    
    static addTableFilter(table) {
        const filterContainer = document.createElement('div');
        filterContainer.className = 'mb-3';
        filterContainer.innerHTML = `
            <div class="input-group">
                <span class="input-group-text">🔍</span>
                <input type="text" class="form-control" placeholder="البحث في الجدول...">
            </div>
        `;
        
        table.parentNode.insertBefore(filterContainer, table);
        
        const filterInput = filterContainer.querySelector('input');
        filterInput.addEventListener('input', this.debounce((e) => {
            this.filterTable(table, e.target.value);
        }, CONFIG.debounceDelay));
    }
    
    static filterTable(table, searchTerm) {
        const rows = table.querySelectorAll('tbody tr');
        const term = searchTerm.toLowerCase();
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(term) ? '' : 'none';
        });
    }
    
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// تحسين الاستجابة للشاشات الصغيرة
class ResponsiveEnhancer {
    static enhance() {
        // تحسين الجداول للشاشات الصغيرة
        this.enhanceTablesForMobile();
        
        // تحسين النماذج للشاشات الصغيرة
        this.enhanceFormsForMobile();
        
        // إضافة زر العودة للأعلى
        this.addBackToTopButton();
    }
    
    static enhanceTablesForMobile() {
        if (window.innerWidth <= 768) {
            document.querySelectorAll('table').forEach(table => {
                if (!table.classList.contains('table-responsive')) {
                    const wrapper = document.createElement('div');
                    wrapper.className = 'table-responsive';
                    table.parentNode.insertBefore(wrapper, table);
                    wrapper.appendChild(table);
                }
            });
        }
    }
    
    static enhanceFormsForMobile() {
        if (window.innerWidth <= 768) {
            document.querySelectorAll('.btn-group').forEach(group => {
                group.classList.add('btn-group-vertical');
            });
        }
    }
    
    static addBackToTopButton() {
        const button = document.createElement('button');
        button.innerHTML = '⬆️';
        button.className = 'btn btn-primary position-fixed';
        button.style.cssText = `
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: none;
        `;
        
        button.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        
        document.body.appendChild(button);
        
        window.addEventListener('scroll', () => {
            button.style.display = window.scrollY > 300 ? 'block' : 'none';
        });
    }
}

// تحسين الأداء
class PerformanceEnhancer {
    static enhance() {
        // تحميل الصور بشكل كسول
        this.lazyLoadImages();
        
        // ضغط الطلبات
        this.optimizeRequests();
    }
    
    static lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    static optimizeRequests() {
        // إضافة معالجة للطلبات المتكررة
        const requestCache = new Map();
        
        window.cachedFetch = function(url, options = {}) {
            const key = url + JSON.stringify(options);
            
            if (requestCache.has(key)) {
                return Promise.resolve(requestCache.get(key));
            }
            
            return fetch(url, options)
                .then(response => response.clone())
                .then(response => {
                    requestCache.set(key, response);
                    // إزالة من التخزين المؤقت بعد 5 دقائق
                    setTimeout(() => requestCache.delete(key), 300000);
                    return response;
                });
        };
    }
}

// تحسين إمكانية الوصول
class AccessibilityEnhancer {
    static enhance() {
        // إضافة دعم لوحة المفاتيح
        this.enhanceKeyboardNavigation();
        
        // تحسين قارئات الشاشة
        this.enhanceScreenReaders();
    }
    
    static enhanceKeyboardNavigation() {
        // إضافة تنقل بالمفاتيح للعناصر التفاعلية
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                // إغلاق النوافذ المنبثقة
                const modals = document.querySelectorAll('.modal.show');
                modals.forEach(modal => {
                    const closeBtn = modal.querySelector('.btn-close');
                    if (closeBtn) closeBtn.click();
                });
                
                // إخفاء رسائل التحميل
                loadingManager.hide();
            }
        });
    }
    
    static enhanceScreenReaders() {
        // إضافة تسميات للعناصر التفاعلية
        document.querySelectorAll('button:not([aria-label])').forEach(btn => {
            if (!btn.textContent.trim()) {
                btn.setAttribute('aria-label', 'زر');
            }
        });
        
        // إضافة وصف للجداول
        document.querySelectorAll('table:not([aria-label])').forEach(table => {
            table.setAttribute('aria-label', 'جدول بيانات');
        });
    }
}

// تهيئة التحسينات عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 تطبيق تحسينات منصة المسابقات الرياضية...');
    
    try {
        FormEnhancer.enhance();
        TableEnhancer.enhance();
        ResponsiveEnhancer.enhance();
        PerformanceEnhancer.enhance();
        AccessibilityEnhancer.enhance();
        
        console.log('✅ تم تطبيق جميع التحسينات بنجاح');
    } catch (error) {
        console.error('❌ خطأ في تطبيق التحسينات:', error);
        ErrorHandler.show('حدث خطأ في تحميل بعض التحسينات', 'warning');
    }
});

// تصدير الوظائف للاستخدام العام
window.MathPlatformEnhancements = {
    loadingManager,
    ErrorHandler,
    FormEnhancer,
    TableEnhancer,
    ResponsiveEnhancer,
    PerformanceEnhancer,
    AccessibilityEnhancer
};
