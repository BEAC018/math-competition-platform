/**
 * Test script for the Alhassan Math Desktop Application
 * 
 * This script verifies that all necessary components for the desktop application are properly set up.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Set up colors for console output
const colors = {
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    reset: '\x1b[0m'
};

console.log(`${colors.blue}===== Alhassan Math Desktop Application Tester =====${colors.reset}\n`);

// Check for required files
const requiredFiles = [
    'package.json',
    'main.js',
    'preload.js',
    process.platform === 'win32' ? 'start_django.bat' : 'start_django.sh',
    'manage.py'
];

let allFilesExist = true;
console.log(`${colors.yellow}Checking required files:${colors.reset}`);

requiredFiles.forEach(file => {
    const exists = fs.existsSync(path.join(__dirname, file));
    console.log(`  ${file}: ${exists ? colors.green + '✓' : colors.red + '✗'} ${colors.reset}`);
    if (!exists) allFilesExist = false;
});

if (!allFilesExist) {
    console.log(`\n${colors.red}Error: Some required files are missing. Please check the setup.${colors.reset}`);
    process.exit(1);
}

// Check Node.js and npm versions
console.log(`\n${colors.yellow}Checking Node.js and npm:${colors.reset}`);
try {
    const nodeVersion = execSync('node --version').toString().trim();
    console.log(`  Node.js version: ${colors.green}${nodeVersion}${colors.reset}`);
    
    const npmVersion = execSync('npm --version').toString().trim();
    console.log(`  npm version: ${colors.green}${npmVersion}${colors.reset}`);
} catch (error) {
    console.log(`\n${colors.red}Error: Node.js or npm is not installed or not in PATH.${colors.reset}`);
    console.log(`Please install Node.js from https://nodejs.org/`);
    process.exit(1);
}

// Check Python and pip
console.log(`\n${colors.yellow}Checking Python and pip:${colors.reset}`);
try {
    const pythonCommand = process.platform === 'win32' ? 'python --version' : 'python3 --version';
    const pythonVersion = execSync(pythonCommand).toString().trim();
    console.log(`  Python version: ${colors.green}${pythonVersion}${colors.reset}`);
    
    const pipCommand = process.platform === 'win32' ? 'pip --version' : 'pip3 --version';
    const pipVersion = execSync(pipCommand).toString().trim();
    console.log(`  pip version: ${colors.green}${pipVersion}${colors.reset}`);
} catch (error) {
    console.log(`\n${colors.red}Error: Python or pip is not installed or not in PATH.${colors.reset}`);
    console.log(`Please install Python from https://www.python.org/downloads/`);
    process.exit(1);
}

// Check Django
console.log(`\n${colors.yellow}Checking Django:${colors.reset}`);
try {
    // Check if Django is installed by trying to import it in Python
    const djangoCheck = process.platform === 'win32' 
        ? 'python -c "import django; print(django.get_version())"'
        : 'python3 -c "import django; print(django.get_version())"';
    
    const djangoVersion = execSync(djangoCheck).toString().trim();
    console.log(`  Django version: ${colors.green}${djangoVersion}${colors.reset}`);
} catch (error) {
    console.log(`\n${colors.red}Error: Django is not installed.${colors.reset}`);
    console.log(`Please install Django using: pip install -r requirements.txt`);
    process.exit(1);
}

// Check npm dependencies
console.log(`\n${colors.yellow}Checking npm dependencies:${colors.reset}`);
if (!fs.existsSync(path.join(__dirname, 'node_modules'))) {
    console.log(`  node_modules: ${colors.red}✗${colors.reset}`);
    console.log(`\n${colors.yellow}Installing npm dependencies...${colors.reset}`);
    try {
        execSync('npm install', { stdio: 'inherit' });
        console.log(`  ${colors.green}Dependencies installed successfully.${colors.reset}`);
    } catch (error) {
        console.log(`\n${colors.red}Error installing dependencies. Please run 'npm install' manually.${colors.reset}`);
        process.exit(1);
    }
} else {
    console.log(`  node_modules: ${colors.green}✓${colors.reset}`);
}

// All checks passed
console.log(`\n${colors.green}All checks passed! The application is ready to run.${colors.reset}`);
console.log(`\nTo start the application, run: ${colors.blue}npm start${colors.reset}`);
console.log(`To build the application for distribution, run one of the following:`);
console.log(`  ${colors.blue}npm run package-win${colors.reset} (for Windows)`);
console.log(`  ${colors.blue}npm run package-mac${colors.reset} (for macOS)`);
console.log(`  ${colors.blue}npm run package-linux${colors.reset} (for Linux)`);