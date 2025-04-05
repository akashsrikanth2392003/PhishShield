console.log("PhishShield Content Script Loaded");

const scannedEmails = new Map(); // Track scanned emails with timestamps
const flaggedEmails = new Map(); // Store flagged email elements
const SCAN_EXPIRY = 60 * 1000; // 1-minute expiry
const SERVER_URL = "http://127.0.0.1:5001/predict";

// Listen for scan request from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.message === "scan_email") {
        scanEmails();
        const emailText = document.body.innerText;
        sendResponse({ emailText });
    }
});

// Flag suspicious emails
function flagEmail(emailElement) {
    if (flaggedEmails.has(emailElement)) return; // Avoid duplicate warnings

    emailElement.style.border = '3px solid red';
    emailElement.style.backgroundColor = 'rgba(255, 0, 0, 0.2)';

    const warning = document.createElement('div');
    warning.className = 'phishing-warning';
    warning.innerHTML = '🚨 <b>Suspicious Email Detected</b>';
    warning.style.color = 'white';
    warning.style.backgroundColor = 'red';
    warning.style.padding = '5px';
    warning.style.marginBottom = '5px';
    warning.style.fontWeight = 'bold';

    emailElement.prepend(warning);
    flaggedEmails.set(emailElement, warning);
}

// Remove warning when email is deleted/restored
function removeFlag(emailElement) {
    if (flaggedEmails.has(emailElement)) {
        console.log("Removing flagged email:", emailElement.innerText);
        
        const warning = flaggedEmails.get(emailElement);
        if (warning) {
            warning.remove(); // Remove the warning div
        }
        
        emailElement.style.border = '';
        emailElement.style.backgroundColor = '';
        
        flaggedEmails.delete(emailElement);  // Remove from flagged list
        scannedEmails.delete(emailElement);  // Remove from scanned list
    }
}


// Scan emails and send data via POST
async function scanEmails() {
    console.log("Scanning emails...");

    const emailElements = document.querySelectorAll('.zA');
    console.log("Email elements found:", emailElements.length, emailElements);

    if (emailElements.length === 0) {
        console.warn("No email elements found. Skipping scan.");
        return;
    }

    for (let emailElement of emailElements) {
        const subjectElement = emailElement.querySelector('.bog');
        const senderElement = emailElement.querySelector('.yX');

        if (!subjectElement || !senderElement) {
            console.warn('Missing email data, skipping...');
            continue;
        }

        const emailData = {
            email_text: `${subjectElement.innerText} ${senderElement.innerText}`
        };

        console.log("Sending email data for phishing detection:", emailData);

        try {
            const response = await fetch("http://127.0.0.1:5001/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(emailData)
            });

            console.log("Response status:", response.status);

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server error: ${response.status} - ${errorText}`);
            }

            const result = await response.json();
            console.log("Server response:", result);

            if (result.is_phishing) {
                flagEmail(emailElement);
            } else {
                removeFlag(emailElement);
            }

        } catch (error) {
            console.error('Error connecting to server:', error);
        }
    }
}


// Wait for emails and scan
function waitForEmailsAndScan(retries = 10) {
    console.log("Waiting for email elements...");

    let emailElements = document.querySelectorAll('.zA');

    if (emailElements.length === 0 && retries > 0) {
        console.warn(`No emails found. Retrying in 1s (${retries} left)...`);
        setTimeout(() => waitForEmailsAndScan(retries - 1), 1000);
    } else if (emailElements.length > 0) {
        console.log(`Found ${emailElements.length} emails. Starting scan.`);
        scanEmails();
    } else {
        console.error("No emails found after multiple retries.");
    }
}

// Detect email updates and rescan
const observer = new MutationObserver((mutationsList) => {
    console.log("Gmail updated, rescanning emails...");

    let emailAdded = false, emailRemoved = false;

    mutationsList.forEach(mutation => {
        mutation.removedNodes.forEach(node => {
            if (node.nodeType === 1 && node.matches('.zA')) {
                console.log("Email deleted, updating...");
                removeFlag(node);
                scannedEmails.delete(node);
                emailRemoved = true;
            }
        });

        mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1 && node.matches('.zA')) {
                console.log("New email detected, rescanning...");
                emailAdded = true;
            }
        });
    });

    if (emailAdded || emailRemoved) {
        scanEmails(); // Only rescan if emails were changed
    }
});


// Start scanning after Gmail loads
setTimeout(() => {
    console.log("Starting observer...");
    observer.observe(document.body, { childList: true, subtree: true });
    scanEmails();
}, 5000);
