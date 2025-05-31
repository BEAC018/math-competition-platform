const { app, BrowserWindow, Menu, globalShortcut, ipcMain } = require('electron');
const path = require('path');
const childProcess = require('child_process');
const { spawn } = require('child_process');

// Keep references to prevent garbage collection
let mainWindow;
let djangoProcess;

// Function to start Django server
function startDjangoServer() {
  // Use batch file for Windows to activate virtual environment and start Django
  const isWindows = process.platform === 'win32';
  
  if (isWindows) {
    // Create and run a batch file for Windows
    djangoProcess = childProcess.spawn('cmd.exe', ['/c', 'start_django.bat'], {
      detached: false
    });
  } else {
    // For macOS and Linux
    djangoProcess = spawn('python', ['manage.py', 'runserver', '8000']);
  }

  djangoProcess.stdout.on('data', (data) => {
    console.log(`Django stdout: ${data}`);
  });

  djangoProcess.stderr.on('data', (data) => {
    console.error(`Django stderr: ${data}`);
  });

  djangoProcess.on('close', (code) => {
    console.log(`Django server process exited with code ${code}`);
  });
}

// Function to create the main application window
function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false, // For security reasons
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    fullscreen: true, // Start in fullscreen mode
    icon: path.join(__dirname, 'assets/icon.png')
  });

  // Remove menu bar
  Menu.setApplicationMenu(null);

  // Load the Django app
  setTimeout(() => {
    mainWindow.loadURL('http://localhost:8000');
  }, 2000); // Wait a bit for Django to start

  // Open DevTools in development
  // mainWindow.webContents.openDevTools();

  // Keep window in fullscreen mode
  globalShortcut.register('Escape', () => {
    // Prevent Escape key from exiting fullscreen
    if (mainWindow.isFullScreen()) {
      mainWindow.setFullScreen(true);
    }
  });

  // Handle IPC messages from renderer
  ipcMain.on('toggle-fullscreen', () => {
    if (mainWindow) {
      const isFullScreen = mainWindow.isFullScreen();
      mainWindow.setFullScreen(!isFullScreen);
      mainWindow.webContents.send('fullscreen-status', !isFullScreen);
    }
  });

  ipcMain.on('quit-app', () => {
    app.quit();
  });

  // Handle window close
  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

// This method will be called when Electron has finished initialization
app.whenReady().then(() => {
  // Start Django server first
  startDjangoServer();
  
  // Create application window
  createWindow();

  app.on('activate', function () {
    // On macOS it's common to re-create a window when the dock icon is clicked
    if (mainWindow === null) createWindow();
  });
});

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', function () {
  // On macOS it is common for applications to stay open until explicitly quit
  if (process.platform !== 'darwin') {
    app.quit();
  }
  
  // Kill Django server process
  if (djangoProcess) {
    if (process.platform === 'win32') {
      // For Windows
      childProcess.exec('taskkill /pid ' + djangoProcess.pid + ' /T /F');
    } else {
      // For macOS and Linux
      djangoProcess.kill();
    }
  }
});

// When app is about to quit
app.on('will-quit', () => {
  // Unregister all shortcuts
  globalShortcut.unregisterAll();
  
  // Kill Django server process
  if (djangoProcess) {
    if (process.platform === 'win32') {
      // For Windows
      childProcess.exec('taskkill /pid ' + djangoProcess.pid + ' /T /F');
    } else {
      // For macOS and Linux
      djangoProcess.kill();
    }
  }
});