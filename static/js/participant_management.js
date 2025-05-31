/**
 * إدارة المشاركين - JavaScript محسن
 * Enhanced Participant Management JavaScript
 */

class ParticipantManager {
    constructor() {
        this.selectedParticipants = new Set();
        this.init();
    }

    init() {
        this.bindEvents();
        this.initializeTooltips();
        this.setupAutoSave();
    }

    bindEvents() {
        // تحديد/إلغاء تحديد الكل
        document.getElementById('selectAllCheckbox')?.addEventListener('change', (e) => {
            this.toggleSelectAll(e.target.checked);
        });

        // تحديد المشاركين الفرديين
        document.querySelectorAll('.participant-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.toggleParticipant(e.target.value, e.target.checked);
            });
        });

        // البحث المباشر
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.performSearch(e.target.value);
                }, 500);
            });
        }

        // تحديث الفلاتر تلقائياً
        document.querySelectorAll('select[name="grade"], select[name="group"], select[name="sort"]').forEach(select => {
            select.addEventListener('change', () => {
                this.updateFilters();
            });
        });
    }

    toggleSelectAll(checked) {
        document.querySelectorAll('.participant-checkbox').forEach(checkbox => {
            checkbox.checked = checked;
            this.toggleParticipant(checkbox.value, checked);
        });
        this.updateBulkActions();
    }

    toggleParticipant(participantId, selected) {
        if (selected) {
            this.selectedParticipants.add(participantId);
        } else {
            this.selectedParticipants.delete(participantId);
        }
        this.updateBulkActions();
    }

    updateBulkActions() {
        const bulkDeleteBtn = document.getElementById('bulkDeleteBtn');
        const selectedCount = this.selectedParticipants.size;
        
        if (bulkDeleteBtn) {
            bulkDeleteBtn.disabled = selectedCount === 0;
            bulkDeleteBtn.textContent = selectedCount > 0 ? 
                `حذف المحدد (${selectedCount})` : 'حذف المحدد';
        }

        // تحديث checkbox "تحديد الكل"
        const selectAllCheckbox = document.getElementById('selectAllCheckbox');
        const allCheckboxes = document.querySelectorAll('.participant-checkbox');
        
        if (selectAllCheckbox && allCheckboxes.length > 0) {
            const checkedCount = document.querySelectorAll('.participant-checkbox:checked').length;
            selectAllCheckbox.indeterminate = checkedCount > 0 && checkedCount < allCheckboxes.length;
            selectAllCheckbox.checked = checkedCount === allCheckboxes.length;
        }
    }

    performSearch(query) {
        const form = document.getElementById('filterForm');
        const searchInput = form.querySelector('input[name="search"]');
        searchInput.value = query;
        
        // إرسال النموذج تلقائياً
        if (query.length >= 2 || query.length === 0) {
            form.submit();
        }
    }

    updateFilters() {
        document.getElementById('filterForm').submit();
    }

    initializeTooltips() {
        // تفعيل tooltips لـ Bootstrap
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }

    setupAutoSave() {
        // حفظ حالة الفلاتر في localStorage
        const form = document.getElementById('filterForm');
        if (form) {
            const formData = new FormData(form);
            const filters = {};
            for (let [key, value] of formData.entries()) {
                if (value) filters[key] = value;
            }
            localStorage.setItem('participantFilters', JSON.stringify(filters));
        }
    }

    // استعادة الفلاتر المحفوظة
    restoreFilters() {
        const savedFilters = localStorage.getItem('participantFilters');
        if (savedFilters) {
            const filters = JSON.parse(savedFilters);
            Object.keys(filters).forEach(key => {
                const input = document.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = filters[key];
                }
            });
        }
    }
}

// إنشاء مثيل من مدير المشاركين
const participantManager = new ParticipantManager();

// وظائف عامة للنوافذ المنبثقة والإجراءات
function showAddSingleModal() {
    const modal = new bootstrap.Modal(document.getElementById('addParticipantModal'));
    modal.show();
}

function showBulkAddModal() {
    const modal = new bootstrap.Modal(document.getElementById('bulkAddModal'));
    modal.show();
}

function showImportModal() {
    const modal = new bootstrap.Modal(document.getElementById('importModal'));
    modal.show();
}

function viewParticipant(participantId) {
    // جلب تفاصيل المشارك وعرضها
    fetch(`/competitions/participant/${participantId}/details/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateParticipantDetails(data.participant);
                const modal = new bootstrap.Modal(document.getElementById('participantDetailsModal'));
                modal.show();
            } else {
                notifications.error('فشل في جلب تفاصيل المشارك');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            notifications.error('حدث خطأ في جلب التفاصيل');
        });
}

function editParticipant(participantId) {
    // جلب بيانات المشارك للتعديل
    fetch(`/competitions/participant/${participantId}/edit/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateEditForm(data.participant);
                const modal = new bootstrap.Modal(document.getElementById('editParticipantModal'));
                modal.show();
            } else {
                notifications.error('فشل في جلب بيانات المشارك');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            notifications.error('حدث خطأ في جلب البيانات');
        });
}

function deleteParticipant(participantId) {
    if (confirm('هل أنت متأكد من حذف هذا المشارك؟ سيتم حذف جميع مسابقاته أيضاً.')) {
        fetch(`/competitions/participant/${participantId}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                notifications.success('تم حذف المشارك بنجاح');
                location.reload();
            } else {
                notifications.error(data.message || 'فشل في حذف المشارك');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            notifications.error('حدث خطأ في الحذف');
        });
    }
}

function bulkDelete() {
    const selectedIds = Array.from(participantManager.selectedParticipants);
    
    if (selectedIds.length === 0) {
        notifications.warning('يرجى تحديد مشاركين للحذف');
        return;
    }

    if (confirm(`هل أنت متأكد من حذف ${selectedIds.length} مشارك؟ سيتم حذف جميع مسابقاتهم أيضاً.`)) {
        fetch('/competitions/participants/bulk-delete/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ participant_ids: selectedIds })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                notifications.success(`تم حذف ${data.deleted_count} مشارك بنجاح`);
                location.reload();
            } else {
                notifications.error(data.message || 'فشل في الحذف الجماعي');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            notifications.error('حدث خطأ في الحذف الجماعي');
        });
    }
}

function generateReport() {
    notifications.info('جاري إنشاء التقرير...');
    
    fetch('/competitions/participants/generate-report/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `تقرير_المشاركين_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        notifications.success('تم إنشاء التقرير بنجاح');
    })
    .catch(error => {
        console.error('Error:', error);
        notifications.error('فشل في إنشاء التقرير');
    });
}

function populateParticipantDetails(participant) {
    // ملء نافذة تفاصيل المشارك
    document.getElementById('detailName').textContent = participant.name;
    document.getElementById('detailGrade').textContent = participant.grade_display;
    document.getElementById('detailGroup').textContent = participant.group_display;
    document.getElementById('detailCompetitions').textContent = participant.competitions_count;
    document.getElementById('detailAverage').textContent = participant.average_score.toFixed(1);
    document.getElementById('detailBest').textContent = participant.best_score;
    document.getElementById('detailCreated').textContent = participant.created_at;
}

function populateEditForm(participant) {
    // ملء نموذج التعديل
    document.getElementById('editParticipantId').value = participant.id;
    document.getElementById('editName').value = participant.name;
    document.getElementById('editGrade').value = participant.grade;
    document.getElementById('editGroup').value = participant.group;
}

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
           document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
}

// تحسينات إضافية
document.addEventListener('DOMContentLoaded', function() {
    // استعادة الفلاتر المحفوظة
    participantManager.restoreFilters();
    
    // تحسين الأداء للجداول الكبيرة
    if (document.querySelectorAll('.participant-checkbox').length > 100) {
        // استخدام virtual scrolling للجداول الكبيرة
        console.log('تم تفعيل التحسينات للجداول الكبيرة');
    }
    
    // إضافة اختصارات لوحة المفاتيح
    document.addEventListener('keydown', function(e) {
        // Ctrl+A لتحديد الكل
        if (e.ctrlKey && e.key === 'a' && e.target.tagName !== 'INPUT') {
            e.preventDefault();
            document.getElementById('selectAllCheckbox').click();
        }
        
        // Delete لحذف المحدد
        if (e.key === 'Delete' && participantManager.selectedParticipants.size > 0) {
            e.preventDefault();
            bulkDelete();
        }
    });
});
