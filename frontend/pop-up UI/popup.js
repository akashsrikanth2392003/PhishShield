document.getElementById("start-button").addEventListener("click", () => {
  // Query the active tab in the current window and initiate the scan
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { message: "scan_email" }, (response) => {
      document.getElementById("result").textContent = response && response.emailText
        ? "Scan completed. Suspicious emails detected!"
        : "No suspicious emails detected.";
    });
  });
  // Start scanning animation and enable the stop button
  document.getElementById("scan-progress").style.animationPlayState = "running";
  document.getElementById("stop-button").disabled = false;
});

document.getElementById("stop-button").addEventListener("click", () => {
  document.getElementById("scan-progress").style.animationPlayState = "paused";
  document.getElementById("stop-button").disabled = true;
});
