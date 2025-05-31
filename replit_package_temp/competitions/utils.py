"""
أدوات مساعدة للتطبيق
Utility functions for the application
"""

import logging
from django.core.cache import cache
from django.db.models import Count, Avg, Max, Min
from django.utils import timezone
from datetime import timedelta
from .models import Participant, Competition, CompetitionResult

logger = logging.getLogger('competitions')

class PerformanceAnalyzer:
    """محلل الأداء للمشاركين"""
    
    @staticmethod
    def get_participant_stats(participant):
        """الحصول على إحصائيات مشارك"""
        cache_key = f"participant_stats_{participant.id}"
        stats = cache.get(cache_key)
        
        if stats is None:
            competitions = participant.competitions.filter(is_completed=True)
            
            if competitions.exists():
                results = [comp.result for comp in competitions if hasattr(comp, 'result')]
                scores = [result.total_score for result in results]
                
                stats = {
                    'total_competitions': competitions.count(),
                    'average_score': sum(scores) / len(scores) if scores else 0,
                    'best_score': max(scores) if scores else 0,
                    'worst_score': min(scores) if scores else 0,
                    'improvement_trend': PerformanceAnalyzer._calculate_trend(scores),
                    'favorite_difficulty': PerformanceAnalyzer._get_favorite_difficulty(competitions),
                    'performance_level': PerformanceAnalyzer._get_performance_level(sum(scores) / len(scores) if scores else 0)
                }
            else:
                stats = {
                    'total_competitions': 0,
                    'average_score': 0,
                    'best_score': 0,
                    'worst_score': 0,
                    'improvement_trend': 'لا توجد بيانات كافية',
                    'favorite_difficulty': 'غير محدد',
                    'performance_level': 'جديد'
                }
            
            # تخزين في الكاش لمدة 10 دقائق
            cache.set(cache_key, stats, 600)
        
        return stats
    
    @staticmethod
    def _calculate_trend(scores):
        """حساب اتجاه التحسن"""
        if len(scores) < 2:
            return 'لا توجد بيانات كافية'
        
        recent_scores = scores[-3:] if len(scores) >= 3 else scores
        older_scores = scores[:-3] if len(scores) >= 3 else []
        
        if not older_scores:
            return 'جديد'
        
        recent_avg = sum(recent_scores) / len(recent_scores)
        older_avg = sum(older_scores) / len(older_scores)
        
        if recent_avg > older_avg + 2:
            return 'تحسن ممتاز 📈'
        elif recent_avg > older_avg:
            return 'تحسن جيد 📊'
        elif recent_avg == older_avg:
            return 'ثابت ➡️'
        else:
            return 'يحتاج تحسين 📉'
    
    @staticmethod
    def _get_favorite_difficulty(competitions):
        """الحصول على مستوى الصعوبة المفضل"""
        difficulty_counts = competitions.values('difficulty').annotate(
            count=Count('id')
        ).order_by('-count')
        
        if difficulty_counts:
            return f"مستوى {difficulty_counts[0]['difficulty']}"
        return 'غير محدد'
    
    @staticmethod
    def _get_performance_level(average_score):
        """تحديد مستوى الأداء"""
        percentage = (average_score / 45) * 100
        
        if percentage >= 90:
            return 'ممتاز 🌟'
        elif percentage >= 75:
            return 'جيد جداً 😊'
        elif percentage >= 60:
            return 'جيد 🙂'
        elif percentage >= 50:
            return 'مقبول 😐'
        else:
            return 'يحتاج تحسين 😞'

class DataValidator:
    """مدقق البيانات"""
    
    @staticmethod
    def validate_participant_data(name, grade, group):
        """التحقق من صحة بيانات المشارك"""
        errors = []
        
        # التحقق من الاسم
        if not name or len(name.strip()) < 2:
            errors.append('يجب أن يكون الاسم أطول من حرفين')
        
        if len(name) > 100:
            errors.append('الاسم طويل جداً (أقصى حد 100 حرف)')
        
        # التحقق من المستوى
        valid_grades = [choice[0] for choice in Participant.GRADE_CHOICES]
        if grade not in valid_grades:
            errors.append('المستوى الدراسي غير صالح')
        
        # التحقق من الفوج
        valid_groups = [choice[0] for choice in Participant.GROUP_CHOICES]
        if group not in valid_groups:
            errors.append('الفوج غير صالح')
        
        # التحقق من عدم التكرار
        if Participant.objects.filter(name=name, grade=grade, group=group).exists():
            errors.append('يوجد مشارك بنفس الاسم في نفس المستوى والفوج')
        
        return errors
    
    @staticmethod
    def validate_bulk_participants(participants_data):
        """التحقق من صحة بيانات مشاركين متعددين"""
        valid_participants = []
        invalid_participants = []
        
        for data in participants_data:
            name = data.get('name', '').strip()
            grade = data.get('grade')
            group = data.get('group', 1)
            
            errors = DataValidator.validate_participant_data(name, grade, group)
            
            if errors:
                invalid_participants.append({
                    'name': name,
                    'grade': grade,
                    'group': group,
                    'errors': errors
                })
            else:
                valid_participants.append({
                    'name': name,
                    'grade': grade,
                    'group': group
                })
        
        return valid_participants, invalid_participants

class SystemOptimizer:
    """محسن النظام"""
    
    @staticmethod
    def cleanup_old_data():
        """تنظيف البيانات القديمة"""
        # حذف المسابقات غير المكتملة الأقدم من 24 ساعة
        cutoff_time = timezone.now() - timedelta(hours=24)
        old_competitions = Competition.objects.filter(
            is_completed=False,
            start_time__lt=cutoff_time
        )
        
        deleted_count = old_competitions.count()
        old_competitions.delete()
        
        logger.info(f"تم حذف {deleted_count} مسابقة غير مكتملة قديمة")
        
        return deleted_count
    
    @staticmethod
    def optimize_database():
        """تحسين قاعدة البيانات"""
        # مسح الكاش
        cache.clear()
        
        # تنظيف البيانات القديمة
        deleted_count = SystemOptimizer.cleanup_old_data()
        
        logger.info("تم تحسين قاعدة البيانات")
        
        return {
            'cache_cleared': True,
            'old_competitions_deleted': deleted_count
        }

class ReportGenerator:
    """مولد التقارير"""
    
    @staticmethod
    def generate_grade_report(grade):
        """إنشاء تقرير لمستوى دراسي"""
        participants = Participant.objects.filter(grade=grade)
        
        if not participants.exists():
            return None
        
        report = {
            'grade': grade,
            'grade_display': dict(Participant.GRADE_CHOICES)[grade],
            'total_participants': participants.count(),
            'participants_with_competitions': 0,
            'average_score': 0,
            'best_performer': None,
            'most_active': None,
            'performance_distribution': {
                'excellent': 0,
                'very_good': 0,
                'good': 0,
                'acceptable': 0,
                'needs_improvement': 0
            }
        }
        
        participants_with_stats = []
        
        for participant in participants:
            stats = PerformanceAnalyzer.get_participant_stats(participant)
            if stats['total_competitions'] > 0:
                report['participants_with_competitions'] += 1
                participants_with_stats.append({
                    'participant': participant,
                    'stats': stats
                })
                
                # تصنيف الأداء
                avg_percentage = (stats['average_score'] / 45) * 100
                if avg_percentage >= 90:
                    report['performance_distribution']['excellent'] += 1
                elif avg_percentage >= 75:
                    report['performance_distribution']['very_good'] += 1
                elif avg_percentage >= 60:
                    report['performance_distribution']['good'] += 1
                elif avg_percentage >= 50:
                    report['performance_distribution']['acceptable'] += 1
                else:
                    report['performance_distribution']['needs_improvement'] += 1
        
        if participants_with_stats:
            # حساب المتوسط العام
            total_avg = sum(p['stats']['average_score'] for p in participants_with_stats)
            report['average_score'] = total_avg / len(participants_with_stats)
            
            # أفضل أداء
            best = max(participants_with_stats, key=lambda x: x['stats']['average_score'])
            report['best_performer'] = {
                'name': best['participant'].name,
                'average_score': best['stats']['average_score']
            }
            
            # الأكثر نشاطاً
            most_active = max(participants_with_stats, key=lambda x: x['stats']['total_competitions'])
            report['most_active'] = {
                'name': most_active['participant'].name,
                'competitions_count': most_active['stats']['total_competitions']
            }
        
        return report
    
    @staticmethod
    def generate_system_summary():
        """إنشاء ملخص عام للنظام"""
        total_participants = Participant.objects.count()
        total_competitions = Competition.objects.filter(is_completed=True).count()
        
        # إحصائيات حسب المستوى
        grade_stats = {}
        for grade, name in Participant.GRADE_CHOICES:
            count = Participant.objects.filter(grade=grade).count()
            if count > 0:
                grade_stats[grade] = {
                    'name': name,
                    'count': count,
                    'percentage': (count / total_participants * 100) if total_participants > 0 else 0
                }
        
        # أحدث النشاطات
        recent_competitions = Competition.objects.filter(
            is_completed=True
        ).select_related('participant').order_by('-end_time')[:10]
        
        return {
            'total_participants': total_participants,
            'total_competitions': total_competitions,
            'active_grades': len(grade_stats),
            'grade_stats': grade_stats,
            'recent_competitions': recent_competitions,
            'system_health': 'ممتاز' if total_participants > 0 and total_competitions > 0 else 'جيد'
        }
