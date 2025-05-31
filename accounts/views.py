from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile

# Form imports will be defined when we create forms.py
# from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm

def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('competitions:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'competitions:home')
            return redirect(next_url)
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')

    return render(request, 'accounts/login.html')

def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('competitions:home')

def register(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('competitions:home')

    # This is a placeholder for the actual implementation
    # The full implementation will use forms for validation
    if request.method == 'POST':
        # We'll implement the form handling here
        # UserRegistrationForm will be defined in forms.py
        messages.info(request, 'نظام التسجيل قيد التطوير')
        return redirect('accounts:login')

    return render(request, 'accounts/register.html')

@login_required
def profile(request):
    """View user profile"""
    user = request.user

    # Get competition statistics if user is a student
    context = {'user': user}

    if user.profile.is_student:
        # Import here to avoid circular imports
        from competitions.models import Competition, UserResponse

        # Count participated competitions
        participated_count = Competition.objects.filter(user=user).count()
        context['participated_count'] = participated_count

        # Count correct answers
        correct_answers = UserResponse.objects.filter(
            competition__user=user,
            is_correct=True
        ).count()
        context['correct_answers'] = correct_answers

        # Calculate total points
        total_points = correct_answers * 3  # Each correct answer is worth 3 points
        context['total_points'] = total_points

    return render(request, 'accounts/profile.html', context)



@login_required
def edit_profile(request):
    """Edit user profile"""
    user = request.user
    profile = user.profile
    grade_choices = profile._meta.get_field('grade').choices

    if request.method == 'POST':
        # Update user info
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')

        # Update profile info
        if request.POST.get('date_of_birth'):
            profile.date_of_birth = request.POST.get('date_of_birth')

        if profile.is_student and request.POST.get('grade'):
            profile.grade = request.POST.get('grade')

        # Handle profile image
        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES.get('profile_image')

        # Save changes
        user.save()
        profile.save()

        messages.success(request, 'تم تحديث الملف الشخصي بنجاح')
        return redirect('accounts:profile')

    return render(request, 'accounts/edit_profile.html', {
        'user': user,
        'grade_choices': grade_choices,
    })

@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # This updates the session to prevent logging out
            update_session_auth_hash(request, user)
            messages.success(request, 'تم تغيير كلمة المرور بنجاح')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})
