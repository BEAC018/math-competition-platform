/**
 * ===== إصلاح جذري للنوافذ المنبثقة - منع الرعشة والاهتزاز =====
 * 
 * هذا الملف يحل مشاكل:
 * 1. الرعشة (flicker) في النوافذ المنبثقة
 * 2. الاهتزاز أو الحركة غير المرغوبة
 * 3. إعادة التحميل المستمر
 * 4. التضارب في الأحداث
 */

(function() {
    'use strict';
    
    // متغيرات للتحكم في حالة النوافذ
    let isModalOpen = false;
    let currentModal = null;
    let modalQueue = [];
    
    // منع تشغيل متعدد للنوافذ
    let modalInitialized = false;
    
    /**
     * تهيئة النوافذ المنبثقة بشكل مستقر
     */
    function initializeStableModals() {
        if (modalInitialized) return;
        modalInitialized = true;
        
        console.log('🔧 تهيئة النوافذ المنبثقة المستقرة...');
        
        // إزالة جميع event listeners القديمة
        document.removeEventListener('DOMContentLoaded', initializeStableModals);
        
        // تطبيق الإصلاحات على جميع النوافذ الموجودة
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            stabilizeModal(modal);
        });
        
        // مراقبة النوافذ الجديدة
        observeNewModals();
        
        // إصلاح أزرار فتح النوافذ
        fixModalTriggers();
        
        console.log('✅ تم تهيئة النوافذ المنبثقة بنجاح');
    }
    
    /**
     * تثبيت نافذة منبثقة واحدة
     */
    function stabilizeModal(modal) {
        if (!modal || modal.dataset.stabilized === 'true') return;
        
        // وضع علامة على أن النافذة تم تثبيتها
        modal.dataset.stabilized = 'true';
        
        // إزالة جميع الأحداث القديمة
        const newModal = modal.cloneNode(true);
        modal.parentNode.replaceChild(newModal, modal);
        
        // تطبيق الإعدادات المستقرة
        applyStableSettings(newModal);
        
        // إضافة أحداث مستقرة
        addStableEventListeners(newModal);
        
        console.log('🔧 تم تثبيت النافذة:', newModal.id);
    }
    
    /**
     * تطبيق الإعدادات المستقرة على النافذة
     */
    function applyStableSettings(modal) {
        // إعدادات CSS مستقرة
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.zIndex = '1055';
        modal.style.width = '100vw';
        modal.style.height = '100vh';
        modal.style.display = 'none';
        modal.style.transform = 'none';
        modal.style.transition = 'none';
        modal.style.animation = 'none';
        modal.style.willChange = 'auto';
        modal.style.backfaceVisibility = 'hidden';
        modal.style.webkitBackfaceVisibility = 'hidden';
        
        // إعدادات الحوار
        const dialog = modal.querySelector('.modal-dialog');
        if (dialog) {
            dialog.style.position = 'relative';
            dialog.style.top = '50%';
            dialog.style.transform = 'translateY(-50%)';
            dialog.style.transition = 'none';
            dialog.style.animation = 'none';
            dialog.style.willChange = 'auto';
            dialog.style.backfaceVisibility = 'hidden';
            dialog.style.webkitBackfaceVisibility = 'hidden';
        }
        
        // إعدادات المحتوى
        const content = modal.querySelector('.modal-content');
        if (content) {
            content.style.transform = 'none';
            content.style.transition = 'none';
            content.style.animation = 'none';
            content.style.willChange = 'auto';
            content.style.backfaceVisibility = 'hidden';
            content.style.webkitBackfaceVisibility = 'hidden';
        }
    }
    
    /**
     * إضافة أحداث مستقرة للنافذة
     */
    function addStableEventListeners(modal) {
        const modalId = modal.id;
        
        // حدث الفتح
        modal.addEventListener('show.bs.modal', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (isModalOpen && currentModal !== modal) {
                // إضافة إلى الطابور إذا كانت هناك نافذة مفتوحة
                modalQueue.push(modal);
                return false;
            }
            
            openModalStable(modal);
        });
        
        // حدث الإغلاق
        modal.addEventListener('hide.bs.modal', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            closeModalStable(modal);
        });
        
        // أحداث أزرار الإغلاق
        const closeButtons = modal.querySelectorAll('[data-bs-dismiss="modal"], .btn-close, .close');
        closeButtons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                closeModalStable(modal);
            });
        });
        
        // إغلاق بالنقر على الخلفية
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModalStable(modal);
            }
        });
        
        // إغلاق بمفتاح Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && currentModal === modal) {
                closeModalStable(modal);
            }
        });
    }
    
    /**
     * فتح النافذة بشكل مستقر
     */
    function openModalStable(modal) {
        if (isModalOpen || !modal) return;
        
        console.log('🔓 فتح النافذة:', modal.id);
        
        // تعيين الحالة
        isModalOpen = true;
        currentModal = modal;
        
        // منع التمرير في الخلفية
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed';
        document.body.style.width = '100%';
        document.body.classList.add('modal-open');
        
        // إظهار النافذة
        modal.style.display = 'block';
        modal.classList.add('show');
        modal.setAttribute('aria-hidden', 'false');
        
        // إضافة الخلفية
        addModalBackdrop(modal);
        
        // تركيز على النافذة
        setTimeout(() => {
            const firstInput = modal.querySelector('input, select, textarea, button');
            if (firstInput) {
                firstInput.focus();
            }
        }, 100);
        
        // إطلاق حدث الفتح
        modal.dispatchEvent(new CustomEvent('shown.bs.modal'));
    }
    
    /**
     * إغلاق النافذة بشكل مستقر
     */
    function closeModalStable(modal) {
        if (!isModalOpen || currentModal !== modal) return;
        
        console.log('🔒 إغلاق النافذة:', modal.id);
        
        // إخفاء النافذة
        modal.style.display = 'none';
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        
        // إزالة الخلفية
        removeModalBackdrop();
        
        // استعادة التمرير
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.width = '';
        document.body.classList.remove('modal-open');
        
        // تعيين الحالة
        isModalOpen = false;
        currentModal = null;
        
        // إطلاق حدث الإغلاق
        modal.dispatchEvent(new CustomEvent('hidden.bs.modal'));
        
        // فتح النافذة التالية في الطابور
        if (modalQueue.length > 0) {
            const nextModal = modalQueue.shift();
            setTimeout(() => openModalStable(nextModal), 100);
        }
    }
    
    /**
     * إضافة خلفية النافذة
     */
    function addModalBackdrop(modal) {
        // إزالة الخلفية القديمة
        removeModalBackdrop();
        
        const backdrop = document.createElement('div');
        backdrop.className = 'modal-backdrop show';
        backdrop.style.position = 'fixed';
        backdrop.style.top = '0';
        backdrop.style.left = '0';
        backdrop.style.zIndex = '1050';
        backdrop.style.width = '100vw';
        backdrop.style.height = '100vh';
        backdrop.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        backdrop.style.opacity = '1';
        
        // إضافة حدث الإغلاق
        backdrop.addEventListener('click', () => closeModalStable(modal));
        
        document.body.appendChild(backdrop);
    }
    
    /**
     * إزالة خلفية النافذة
     */
    function removeModalBackdrop() {
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(backdrop => backdrop.remove());
    }
    
    /**
     * إصلاح أزرار فتح النوافذ
     */
    function fixModalTriggers() {
        const triggers = document.querySelectorAll('[data-bs-toggle="modal"], [data-toggle="modal"]');
        
        triggers.forEach(trigger => {
            // إزالة الأحداث القديمة
            const newTrigger = trigger.cloneNode(true);
            trigger.parentNode.replaceChild(newTrigger, trigger);
            
            // إضافة حدث جديد مستقر
            newTrigger.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const targetId = this.getAttribute('data-bs-target') || this.getAttribute('data-target');
                const targetModal = document.querySelector(targetId);
                
                if (targetModal) {
                    openModalStable(targetModal);
                }
            });
        });
    }
    
    /**
     * مراقبة النوافذ الجديدة
     */
    function observeNewModals() {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        // البحث عن النوافذ الجديدة
                        const newModals = node.querySelectorAll ? node.querySelectorAll('.modal') : [];
                        newModals.forEach(modal => {
                            if (modal.dataset.stabilized !== 'true') {
                                stabilizeModal(modal);
                            }
                        });
                        
                        // البحث عن أزرار جديدة
                        const newTriggers = node.querySelectorAll ? node.querySelectorAll('[data-bs-toggle="modal"], [data-toggle="modal"]') : [];
                        if (newTriggers.length > 0) {
                            fixModalTriggers();
                        }
                    }
                });
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    /**
     * دالة عامة لفتح النافذة من الخارج
     */
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            openModalStable(modal);
        }
    };
    
    /**
     * دالة عامة لإغلاق النافذة من الخارج
     */
    window.closeModal = function(modalId) {
        const modal = modalId ? document.getElementById(modalId) : currentModal;
        if (modal) {
            closeModalStable(modal);
        }
    };
    
    // تهيئة عند تحميل الصفحة
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeStableModals);
    } else {
        initializeStableModals();
    }
    
    // تهيئة إضافية عند تحميل النافذة
    window.addEventListener('load', function() {
        setTimeout(initializeStableModals, 100);
    });
    
    console.log('📦 تم تحميل نظام النوافذ المنبثقة المستقرة');
    
})();
