
<p align="center">
  <img src="./Icon_cropped.png" alt="Phiserman Logo" width="100" align="left" style="margin-right: 20px;" />
  <h1>PhishShield - Phishing Email Detector</h1>
</p>

Phisherman is a Chrome Extension that detects potential phishing emails in Gmail and Outlook. It scans emails, highlights suspicious content, and provides an easy-to-use interface to start and stop scans.

---

## ✨ Features
- **🛡️ Real-time Email Scanning**: Detects suspicious emails in Gmail and Outlook.
- **✅ User-Friendly Interface**: Popup controls for scanning with dynamic progress feedback.
- **⚠️ Visual Alerts**: Highlights flagged emails with a red border and warning message.

## 💻 Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/username/phiserman.git
   cd PhishShield
   ```
2. **Load the Extension in Chrome**:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable **Developer Mode**
   - Click **Load unpacked** and select the Phiserman project directory.

## 🔧 Usage
1. Open Gmail or Outlook in your browser.
2. Click the Phiserman extension icon to open the popup.
3. Click **Start Scanning** to detect and highlight any suspicious emails in your inbox. The extension will automatically highlight suspicious emails with a warning icon and red border.

## 📂 Files Overview

### Core Components
- **`manifest.json`**: Specifies metadata, permissions, and settings for running the extension on Gmail and Outlook.
- **`background.js`**: Activates a background listener that logs a message when Phiserman is installed.
   ```javascript
   chrome.runtime.onInstalled.addListener(() => {
       console.log("Phiserman installed!");
   });
   ```

### Content Script
- **`content.js`**:
  - Scans Gmail and Outlook emails for phishing content.
  - Receives messages from `popup.js` to initiate the scan.
  - Flags suspicious emails by adding a red border and warning text.

Example function for flagging emails:
  ```javascript
  function flagEmail(emailElement) {
      emailElement.style.border = '2px solid red';
      const warning = document.createElement('div');
      warning.innerText = '⚠️ Suspicious Email Detected';
      warning.style.color = 'red';
      emailElement.prepend(warning);
  }
  ```

### User Interface Components
- **`popup.html`**: Provides the popup interface with controls to start and stop scanning. Displays a progress bar and scan results for user feedback.
- **`popup.js`**: Connects with `content.js` to initiate scanning in the current tab. Controls the progress animation and displays scan results in the popup.
  ```javascript
  document.getElementById("start-button").addEventListener("click", () => {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          chrome.tabs.sendMessage(tabs[0].id, { message: "scan_email" });
      });
  });
  ```
- **`style.css`**: Styles the popup interface, including the progress bar, buttons, and dialog layout, for a clean and professional look.

## 🔍 How It Works

1. **Initialization**: Phiserman initializes upon installation and provides a popup interface for users to interact with.
2. **Scanning Process**: When the **Start Scanning** button is clicked, `popup.js` sends a command to `content.js`. `content.js` scans the emails in Gmail or Outlook, sending each email’s data to a local server (`server.py`) for phishing detection.
3. **Detection and Highlighting**: Emails identified as suspicious are flagged by adding a warning message and red border around the email in the interface.

## 🔧 Backend (Server)
- **`main.py`** and **`server.py`**: These files set up a Flask server that receives email data from `content.js` and analyzes it to predict phishing emails. `server.py` defines API routes to handle email data, while `main.py` runs the server.

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.
