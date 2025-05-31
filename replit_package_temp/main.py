#!/usr/bin/env python3
"""
Main entry point for Replit deployment
"""

import os
import subprocess
import sys

def setup_django():
    """Setup Django application"""
    print("🔧 Setting up Django application...")
    
    # Install requirements
    print("📦 Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Run migrations
    print("🗄️  Running database migrations...")
    subprocess.run([sys.executable, "manage.py", "migrate"])
    
    # Collect static files
    print("📁 Collecting static files...")
    subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"])
    
    print("✅ Setup complete!")

def run_server():
    """Run the Django development server"""
    print("🚀 Starting Django server...")
    subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])

if __name__ == "__main__":
    setup_django()
    run_server()
