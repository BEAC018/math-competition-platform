import os
import django
from django.contrib.auth import get_user_model

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')
django.setup()

# Get the User model
User = get_user_model()

# Create the superuser if it doesn't exist
username = 'BEAC25'
email = 'admin@example.com'
password = '2025'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")