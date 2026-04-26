const tabScan = document.getElementById('tab-scan');
const tabHist = document.getElementById('tab-hist');
const viewScan = document.getElementById('view-scan');
const viewHist = document.getElementById('view-hist');

// --- 1. Tab Switching Logic ---
tabScan.onclick = () => {
    viewScan.style.display = 'block'; 
    viewHist.style.display = 'none';
    tabScan.classList.add('active'); 
    tabHist.classList.remove('active');
};

tabHist.onclick = () => {
    viewScan.style.display = 'none'; 
    viewHist.style.display = 'block';
    tabScan.classList.remove('active'); 
    tabHist.classList.add('active');
    
    // Fetch History from Python DB
    fetch('http://127.0.0.1:8000/history')
        .then(r => r.json())
        .then(data => {
            document.getElementById('hist-list').innerHTML = data.map(h => 
                `<div class="hist-item"><b>${new URL(h.url).hostname}</b><br><small>${h.tech || 'No tech detected'}</small></div>`
            ).join('') || "No history found.";
        })
        .catch(() => {
            document.getElementById('hist-list').innerHTML = "<div class='hist-item' style='color:red'>Database Offline</div>";
        });
};

// --- 2. Live Scan Logic (Combined) ---
chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    const url = tabs[0].url;
    document.getElementById('url-text').innerText = url;
    
    // UI Feedback: Show user that analysis is happening
    document.getElementById('tech-tags').innerHTML = "<small style='color:#888'>Analyzing Infrastructure...</small>";

    fetch(`http://127.0.0.1:8000/analyze?url=${encodeURIComponent(url)}`)
        .then(r => r.json())
        .then(data => {
            if (data.tech && data.tech.length > 0) {
                // Map the array of tech strings into HTML tags
                document.getElementById('tech-tags').innerHTML = data.tech.map(t => `<span class="tag">${t}</span>`).join('');
            } else {
                document.getElementById('tech-tags').innerHTML = "<span class='tag'>Generic Tech</span>";
            }
        })
        .catch(err => {
            // Handle cases where Python backend isn't running
            document.getElementById('tech-tags').innerHTML = "<span style='color:#ff4757; font-size:10px;'>Backend Offline (Check VS Code)</span>";
        });
});