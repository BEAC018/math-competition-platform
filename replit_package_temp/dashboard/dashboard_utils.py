import json
import os
import subprocess
import platform
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

# Check if user is an admin
def is_admin(user):
    if not user.is_authenticated:
        return False
    try:
        return user.profile.is_admin
    except:
        return False

# Admin-only decorator
def admin_required(view_func):
    decorated_view = user_passes_test(is_admin, login_url='accounts:login')(view_func)
    return login_required(decorated_view)

@admin_required
def execute_start_script(request):
    """Execute the start_django script to start the application automatically"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'طريقة غير مسموح بها'}, status=405)
    
    try:
        # Check if the request is AJAX
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.loads(request.body)
            if data.get('action') != 'start':
                return JsonResponse({'success': False, 'error': 'إجراء غير صالح'}, status=400)
        
        # Determine which script to run based on the OS
        is_windows = platform.system() == 'Windows'
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                  'start_django.bat' if is_windows else 'start_django.sh')
        
        # Make sure the script exists
        if not os.path.exists(script_path):
            return JsonResponse({'success': False, 'error': 'ملف بدء التشغيل غير موجود'}, status=404)
        
        # Make the script executable on Unix-like systems
        if not is_windows:
            try:
                os.chmod(script_path, 0o755)  # rwx for owner, rx for group and others
            except Exception as e:
                return JsonResponse({'success': False, 'error': f'فشل تعيين صلاحيات التنفيذ: {str(e)}'}, status=500)
        
        # Execute the script
        if is_windows:
            # On Windows, start the script in a new console window
            subprocess.Popen(['start', 'cmd', '/k', script_path], shell=True)
        else:
            # On Unix-like systems, run the script in the background
            subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                            shell=True, start_new_session=True)
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)