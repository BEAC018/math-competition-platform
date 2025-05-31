from django.contrib import admin
from .models import MathQuestion, Competition, UserResponse, CompetitionResult

class MathQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'get_operation_display', 'get_difficulty_display', 'answer', 'created_at')
    list_filter = ('operation', 'difficulty')
    search_fields = ('first_number', 'second_number', 'answer')
    ordering = ('-created_at',)

class UserResponseInline(admin.TabularInline):
    model = UserResponse
    extra = 0
    readonly_fields = ('question', 'user_answer', 'is_correct', 'response_time', 'created_at')
    can_delete = False
    max_num = 0
    
    def has_add_permission(self, request, obj=None):
        return False

class CompetitionResultInline(admin.StackedInline):
    model = CompetitionResult
    can_delete = False
    readonly_fields = ('total_score', 'addition_correct', 'subtraction_correct', 
                       'multiplication_correct', 'division_correct', 'addition_total', 
                       'subtraction_total', 'multiplication_total', 'division_total', 
                       'created_at')
    max_num = 0
    
    def has_add_permission(self, request, obj=None):
        return False

class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_difficulty_display', 'start_time', 'end_time', 'is_completed', 'get_score')
    list_filter = ('is_completed', 'difficulty', 'start_time')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    inlines = [CompetitionResultInline, UserResponseInline]
    readonly_fields = ('start_time', 'end_time')
    
    def get_score(self, obj):
        try:
            return obj.result.total_score
        except CompetitionResult.DoesNotExist:
            return '-'
    get_score.short_description = 'النتيجة'

class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('competition', 'question', 'user_answer', 'is_correct', 'response_time', 'created_at')
    list_filter = ('is_correct', 'created_at', 'question__operation', 'question__difficulty')
    search_fields = ('competition__user__username', 'competition__user__first_name', 'competition__user__last_name')
    readonly_fields = ('competition', 'question', 'created_at')

class CompetitionResultAdmin(admin.ModelAdmin):
    list_display = ('competition', 'total_score', 'addition_percentage', 'subtraction_percentage', 
                   'multiplication_percentage', 'division_percentage', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('competition__user__username', 'competition__user__first_name', 'competition__user__last_name')
    readonly_fields = ('competition', 'total_score', 'addition_correct', 'subtraction_correct', 
                      'multiplication_correct', 'division_correct', 'addition_total', 
                      'subtraction_total', 'multiplication_total', 'division_total', 
                      'created_at')

# Register the models
admin.site.register(MathQuestion, MathQuestionAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(UserResponse, UserResponseAdmin)
admin.site.register(CompetitionResult, CompetitionResultAdmin)
