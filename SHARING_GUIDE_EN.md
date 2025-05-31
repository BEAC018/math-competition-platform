# Alhassan Math Platform - Sharing Guide

This guide explains different ways to share the Alhassan Math Platform application with others.

## Option 1: Share as a Desktop Application

You can create a distributable package of the application and share it with others:

### 1. Create a Distributable Package:

We've added a convenient script to package the application with a single command:

```bash
# Install the required archiver package first
npm install archiver

# Then run the packaging script
npm run share
```

This will:
- Package the application for your current operating system
- Create an installation guide
- Generate a ZIP file containing everything needed to run the application

### 2. Share the Generated Package:

After running the command, you'll find a ZIP file named `alhassan-math-[platform]-[timestamp].zip` in your project directory. You can:

- Copy this file to a USB drive
- Upload it to a file sharing service like Google Drive or Dropbox
- Send it via email (if the size is manageable)

### 3. Instructions for Recipients:

Recipients simply need to:
1. Extract the ZIP file
2. Follow the instructions in the included INSTALLATION_GUIDE.md file

## Option 2: Share via ngrok (Temporary Demo)

If you want to share the application temporarily for demo or testing purposes:

### 1. Ensure pyngrok is installed:

```bash
pip install pyngrok
```

### 2. Start the Django server:

```bash
python manage.py runserver
```

### 3. In a separate terminal, run ngrok:

```bash
# If you have ngrok installed directly
ngrok http 8000

# Or using Python with pyngrok
python share_app.py
```

### 4. Share the generated link:

You'll get a link like `https://xxxx-xxxx-xxxx.ngrok-free.app` that you can share with others.
This link will remain active as long as the server and tunnel are running on your computer.

**Note**: This method only shares the web interface, not the complete desktop application.

## Option 3: Share via Code Repository

If you want to share the source code for others to develop:

### 1. Create a Git Repository:

```bash
# Initialize a Git repository
git init

# Add files (excluding those in .gitignore)
git add .

# Create the first commit
git commit -m "Initial version of Alhassan Math Platform"
```

### 2. Upload to GitHub or other hosting platform:

```bash
# Add a remote repository
git remote add origin https://github.com/username/math-platform.git

# Push the code
git push -u origin main
```

### 3. Share the repository link:

Share the repository link with others so they can:
- View the code
- Clone the project
- Run it on their own machines

**Requirements for those downloading the repository:**
- Install Node.js
- Install Python and required packages
- Follow the setup and run instructions in README.md

## Additional Sharing Options

### Host as a Web Application:

1. Deploy the Django app on a hosting platform like:
   - PythonAnywhere (offers free hosting)
   - Heroku
   - DigitalOcean

2. Configure production settings:
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`
   - Configure a production database

3. Share the website URL with users

**Note**: This will provide access to the web interface only, not the Electron desktop application.