// package_for_sharing.js
// Script to automate packaging the application for sharing

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const archiver = require('archiver');

// Determine current platform
const platform = process.platform;
let packageCommand = '';
let platformName = '';

// Set the appropriate package command and platform name
if (platform === 'win32') {
  packageCommand = 'npm run package-win';
  platformName = 'windows';
} else if (platform === 'darwin') {
  packageCommand = 'npm run package-mac';
  platformName = 'mac';
} else if (platform === 'linux') {
  packageCommand = 'npm run package-linux';
  platformName = 'linux';
} else {
  console.error('Unsupported platform for packaging');
  process.exit(1);
}

// Create a timestamp for the package
const timestamp = new Date().toISOString().replace(/[:.]/g, '-');

console.log(`\n===== Packaging Alhassan Math Application for ${platformName} =====\n`);

try {
  // Install archiver if not already installed
  try {
    require.resolve('archiver');
    console.log('✓ Archiver is installed');
  } catch (e) {
    console.log('Installing archiver package...');
    execSync('npm install archiver --no-save', { stdio: 'inherit' });
  }

  // Step 1: Package the application
  console.log('\n1. Building the application package...');
  execSync(packageCommand, { stdio: 'inherit' });
  console.log('✓ Application packaged successfully');

  // Step 2: Create a README file for the package
  console.log('\n2. Creating installation guide...');
  const readmePath = path.join('release-builds', 'INSTALLATION_GUIDE.md');
  const readmeContent = `# Alhassan Math Platform - Installation Guide

Thank you for downloading the Alhassan Math Platform!

## Installation Instructions

### Requirements
- Windows: Windows 10 or newer
- Mac: macOS 10.13 or newer
- Linux: Ubuntu 18.04 or equivalent

### Steps to Install and Run

1. Extract all files from this package to a location on your computer
2. Run the application:
   - Windows: Double-click on the "alhassan-math.exe" file
   - Mac: Double-click on the "alhassan-math" application
   - Linux: Run the "alhassan-math" executable

### First Run

On first run, the application will:
1. Start a Django server in the background
2. Open the math platform in fullscreen mode

### Notes

- The application requires internet connection for the first run to set up
- All your data will be stored locally on your computer
- Press Alt+F4 (Windows/Linux) or Cmd+Q (Mac) to exit the application

## Support

If you encounter any issues, please contact the Alhassan Math Platform support team.

Packaged on: ${new Date().toLocaleDateString()}
  `;
  
  fs.writeFileSync(readmePath, readmeContent);
  console.log('✓ Installation guide created');

  // Step 3: Create a ZIP archive of the release
  console.log('\n3. Creating ZIP archive...');
  const zipFileName = `alhassan-math-${platformName}-${timestamp}.zip`;
  const output = fs.createWriteStream(zipFileName);
  const archive = archiver('zip', {
    zlib: { level: 9 } // Maximum compression
  });

  output.on('close', function() {
    console.log(`✓ Archive created: ${zipFileName} (${(archive.pointer() / 1024 / 1024).toFixed(2)} MB)`);
    console.log('\n===== Packaging Complete =====');
    console.log(`\nYour application is ready to share!`);
    console.log(`\nShare the file: ${zipFileName}`);
  });

  archive.on('error', function(err) {
    throw err;
  });

  archive.pipe(output);
  
  // Add the release-builds directory to the ZIP file
  archive.directory('release-builds/', 'alhassan-math');
  
  archive.finalize();
  
} catch (error) {
  console.error('Error during packaging:', error);
  process.exit(1);
}