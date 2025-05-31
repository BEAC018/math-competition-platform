/**
 * نظام الإشعارات المحسن للتطبيق
 * Enhanced Notification System
 */

class NotificationManager {
    constructor() {
        this.container = null;
        this.notifications = [];
        this.init();
    }

    init() {
        // إنشاء حاوية الإشعارات
        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.className = 'notification-container';
        this.container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
            pointer-events: none;
        `;
        document.body.appendChild(this.container);
    }

    show(message, type = 'info', duration = 5000, options = {}) {
        const notification = this.createNotification(message, type, options);
        this.container.appendChild(notification);
        this.notifications.push(notification);

        // تأثير الظهور
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // إزالة تلقائية
        if (duration > 0) {
            setTimeout(() => {
                this.remove(notification);
            }, duration);
        }

        return notification;
    }

    createNotification(message, type, options) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            background: white;
            border-radius: 15px;
            padding: 16px 20px;
            margin-bottom: 10px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
            border-left: 4px solid ${this.getTypeColor(type)};
            transform: translateX(100%);
            transition: all 0.3s ease;
            pointer-events: auto;
            font-family: 'Cairo', sans-serif;
            direction: rtl;
            opacity: 0;
        `;

        const icon = this.getTypeIcon(type);
        const closeBtn = options.closable !== false ? 
            '<button class="notification-close" style="float: left; background: none; border: none; font-size: 18px; cursor: pointer; color: #999;">&times;</button>' : '';

        notification.innerHTML = `
            <div style="display: flex; align-items: center;">
                <span style="font-size: 20px; margin-left: 10px;">${icon}</span>
                <div style="flex: 1;">
                    ${options.title ? `<div style="font-weight: 600; margin-bottom: 4px; color: #333;">${options.title}</div>` : ''}
                    <div style="color: #666; font-size: 14px;">${message}</div>
                </div>
                ${closeBtn}
            </div>
        `;

        // إضافة مستمع للإغلاق
        const closeButton = notification.querySelector('.notification-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                this.remove(notification);
            });
        }

        // إضافة تأثير التمرير للإغلاق
        let startX = 0;
        let currentX = 0;
        let isDragging = false;

        notification.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            isDragging = true;
        });

        notification.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            currentX = e.touches[0].clientX - startX;
            if (currentX > 0) {
                notification.style.transform = `translateX(${currentX}px)`;
                notification.style.opacity = Math.max(0.3, 1 - currentX / 200);
            }
        });

        notification.addEventListener('touchend', () => {
            if (currentX > 100) {
                this.remove(notification);
            } else {
                notification.style.transform = 'translateX(0)';
                notification.style.opacity = '1';
            }
            isDragging = false;
            currentX = 0;
        });

        return notification;
    }

    remove(notification) {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
            const index = this.notifications.indexOf(notification);
            if (index > -1) {
                this.notifications.splice(index, 1);
            }
        }, 300);
    }

    getTypeColor(type) {
        const colors = {
            success: '#4CAF50',
            error: '#F44336',
            warning: '#FF9800',
            info: '#2196F3',
            primary: '#2D8CFF'
        };
        return colors[type] || colors.info;
    }

    getTypeIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️',
            primary: '🔔'
        };
        return icons[type] || icons.info;
    }

    // طرق مختصرة
    success(message, options = {}) {
        return this.show(message, 'success', 4000, { title: 'نجح!', ...options });
    }

    error(message, options = {}) {
        return this.show(message, 'error', 6000, { title: 'خطأ!', ...options });
    }

    warning(message, options = {}) {
        return this.show(message, 'warning', 5000, { title: 'تحذير!', ...options });
    }

    info(message, options = {}) {
        return this.show(message, 'info', 4000, { title: 'معلومة', ...options });
    }

    // إزالة جميع الإشعارات
    clear() {
        this.notifications.forEach(notification => {
            this.remove(notification);
        });
    }
}

// إنشاء مثيل عام
window.notifications = new NotificationManager();

// إضافة CSS للإشعارات
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification.show {
        transform: translateX(0) !important;
        opacity: 1 !important;
    }

    .notification:hover {
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }

    @media (max-width: 768px) {
        #notification-container {
            right: 10px;
            left: 10px;
            max-width: none;
        }
    }
`;
document.head.appendChild(notificationStyles);

// تحسين رسائل Django
document.addEventListener('DOMContentLoaded', function() {
    // تحويل رسائل Django إلى إشعارات محسنة
    const djangoMessages = document.querySelectorAll('.alert');
    djangoMessages.forEach(alert => {
        const message = alert.textContent.trim();
        let type = 'info';
        
        if (alert.classList.contains('alert-success')) type = 'success';
        else if (alert.classList.contains('alert-danger')) type = 'error';
        else if (alert.classList.contains('alert-warning')) type = 'warning';
        else if (alert.classList.contains('alert-info')) type = 'info';
        
        if (message) {
            notifications.show(message, type);
            alert.style.display = 'none';
        }
    });
});
