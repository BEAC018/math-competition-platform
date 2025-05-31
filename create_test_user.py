import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')
django.setup()

# Import Django models
from django.contrib.auth.models import User
from accounts.models import Profile

# Check if test user already exists
username = 'testuser'
if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists.")
else:
    # Create a test user
    user = User.objects.create_user(
        username=username,
        password='testpassword123',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    
    # Update profile information
    profile = user.profile
    profile.user_type = 'student'
    profile.grade = '3'
    profile.save()
    
    print(f"User '{username}' created successfully with password 'testpassword123'.")
    print("You can now log in using these credentials.")