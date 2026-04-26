const API_BASE_URL = "https://weblens-f2br.onrender.com";

// --- Tab Switching Logic ---
const tabScan = document.getElementById('tab-scan');
const tabHist = document.getElementById('tab-hist');
const viewScan = document.getElementById('view-scan');
const viewHist = document.getElementById('view-hist');

tabScan.addEventListener('click', () => {
    tabScan.classList.add('active');
    tabHist.classList.remove('active');
    viewScan.style.display = 'block';
    viewHist.style.display = 'none';
});

tabHist.addEventListener('click', async () => {
    tabHist.classList.add('active');
    tabScan.classList.remove('active');
    viewScan.style.display = 'none';
    viewHist.style.display = 'block';
    
    // Auto-fetch history when clicking the tab
    loadHistory();
});

// --- History Logic ---
async function loadHistory() {
    const histList = document.getElementById('hist-list');
    histList.innerHTML = "<p style='font-size:10px; color:#888'>Loading history...</p>";

    try {
        const response = await fetch(`${API_BASE_URL}/history`);
        const data = await response.json();

        histList.innerHTML = ""; // Clear loader
        if (data.length > 0) {
            data.forEach(item => {
                const div = document.createElement('div');
                div.className = "hist-item";
                div.innerHTML = `
                    <div style="color:#f15a24; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${item.url}</div>
                    <div style="color:#888; font-size:9px;">${item.tech}</div>
                `;
                histList.appendChild(div);
            });
        } else {
            histList.innerHTML = "<p style='font-size:10px;'>No scans yet.</p>";
        }
    } catch (error) {
        histList.innerHTML = "<p style='font-size:10px; color:red;'>Server unreachable.</p>";
    }
}

// --- Automated Scan on Load ---
async function runAutoScan() {
    const urlText = document.getElementById('url-text');
    const techTags = document.getElementById('tech-tags');
    
    try {
        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        urlText.innerText = tab.url;
        techTags.innerHTML = "<span style='font-size:10px;'>Analyzing...</span>";

        const response = await fetch(`${API_BASE_URL}/analyze?url=${encodeURIComponent(tab.url)}`);
        const data = await response.json();

        if (data.status === "success") {
            techTags.innerHTML = ""; // Clear loader
            data.tech.forEach(t => {
                const span = document.createElement('span');
                span.className = "tag";
                span.innerText = t;
                techTags.appendChild(span);
            });
        }
    } catch (e) {
        techTags.innerText = "Check connection...";
    }
}

// Run scan as soon as popup opens
runAutoScan();