from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class StatisticsCache(models.Model):
    """
    Cache model for storing pre-calculated statistics to improve dashboard performance.
    """
    CACHE_TYPES = [
        ('daily_stats', 'إحصائيات يومية'),
        ('weekly_stats', 'إحصائيات أسبوعية'),
        ('monthly_stats', 'إحصائيات شهرية'),
        ('grade_stats', 'إحصائيات حسب الصف'),
        ('operation_stats', 'إحصائيات حسب العمليات'),
        ('difficulty_stats', 'إحصائيات حسب الصعوبة'),
    ]
    
    cache_type = models.CharField(max_length=20, choices=CACHE_TYPES)
    cache_key = models.CharField(max_length=255, help_text="Unique identifier for this cache entry")
    data = models.JSONField(help_text="Cached JSON data")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        unique_together = ['cache_type', 'cache_key']
        indexes = [
            models.Index(fields=['cache_type', 'cache_key']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"{self.get_cache_type_display()} - {self.cache_key}"
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @classmethod
    def get_cache(cls, cache_type, cache_key):
        """
        Get a cache entry if it exists and is not expired.
        Returns None if no valid cache is found.
        """
        try:
            cache = cls.objects.get(cache_type=cache_type, cache_key=cache_key)
            if cache.is_expired:
                cache.delete()
                return None
            return cache.data
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def set_cache(cls, cache_type, cache_key, data, expiry_hours=24):
        """
        Create or update a cache entry with the given data.
        """
        expires_at = timezone.now() + timezone.timedelta(hours=expiry_hours)
        cache, created = cls.objects.update_or_create(
            cache_type=cache_type,
            cache_key=cache_key,
            defaults={
                'data': data,
                'expires_at': expires_at
            }
        )
        return cache
