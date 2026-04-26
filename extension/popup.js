// Change this to your live Render URL
const API_BASE_URL = "https://weblens-f2br.onrender.com";

document.getElementById('scan-btn').addEventListener('click', async () => {
    const statusDiv = document.getElementById('status');
    const resultsDiv = document.getElementById('results');
    
    statusDiv.innerText = "🔍 Scanning & Syncing...";
    resultsDiv.innerHTML = "";

    try {
        // 1. Get the current active tab
        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        
        // 2. Tell the Backend to analyze this URL
        // This is the part that saves it to your history!
        const response = await fetch(`${API_BASE_URL}/analyze?url=${encodeURIComponent(tab.url)}`);
        const data = await response.json();

        if (data.status === "success") {
            statusDiv.innerText = "✅ Scan Complete & Saved";
            
            // 3. Display the results in the popup
            data.tech.forEach(tech => {
                const span = document.createElement('span');
                span.className = "tag";
                span.innerText = tech;
                resultsDiv.appendChild(span);
            });
        } else {
            statusDiv.innerText = "❌ Error: " + (data.message || "Unknown error");
        }
    } catch (error) {
        console.error("Connection Error:", error);
        statusDiv.innerText = "❌ Server Offline (Waking up Render...)";
    }
});