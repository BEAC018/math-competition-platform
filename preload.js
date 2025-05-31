// Preload script for Electron

// All Node.js APIs are available in preload process
// Expose protected methods that allow the renderer process to use the ipcRenderer without exposing all of electron
const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld(
  'api', {
    // Send a message to the main process
    send: (channel, data) => {
      // Allowed channels for send
      let validChannels = ['toggle-fullscreen', 'quit-app'];
      if (validChannels.includes(channel)) {
        ipcRenderer.send(channel, data);
      }
    },
    // Receive a message from the main process
    receive: (channel, func) => {
      // Allowed channels for receive
      let validChannels = ['fullscreen-status', 'app-status'];
      if (validChannels.includes(channel)) {
        // Deliberately strip event as it includes `sender` 
        ipcRenderer.on(channel, (event, ...args) => func(...args));
      }
    }
  }
);

// When the DOM is loaded, inject some additional CSS to ensure the app looks good in desktop mode
window.addEventListener('DOMContentLoaded', () => {
  // Add CSS to optimize for desktop display
  const style = document.createElement('style');
  style.textContent = `
    /* Desktop optimization styles */
    body {
      overflow: hidden; /* Prevent scrollbars in fullscreen */
    }
    
    /* Ensure content fills the screen */
    .main-content {
      min-height: calc(100vh - 150px) !important;
    }
    
    /* Make buttons more touchable */
    .btn {
      padding: 0.6rem 1.2rem;
    }
    
    /* Improve form controls for desktop */
    input, select, textarea {
      padding: 0.5rem;
    }
  `;
  document.head.appendChild(style);
  
  console.log('Preload script loaded successfully');
});