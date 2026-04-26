const tabScan = document.getElementById('tab-scan');
const tabHist = document.getElementById('tab-hist');
const viewScan = document.getElementById('view-scan');
const viewHist = document.getElementById('view-hist');

// Replace this variable with your actual Render URL!
const API_BASE_URL = "https://your-web-service.onrender.com";

tabScan.onclick = () => {
    viewScan.style.display = 'block'; viewHist.style.display = 'none';
    tabScan.classList.add('active'); tabHist.classList.remove('active');
};

tabHist.onclick = () => {
    viewScan.style.display = 'none'; viewHist.style.display = 'block';
    tabScan.classList.remove('active'); tabHist.classList.add('active');
    
    fetch(`${API_BASE_URL}/history`)
        .then(r => r.json())
        .then(data => {
            document.getElementById('hist-list').innerHTML = data.map(h => 
                `<div class="hist-item"><b>${new URL(h.url).hostname}</b><br><small>${h.tech || 'No tech detected'}</small></div>`
            ).join('') || "No history found.";
        })
        .catch(() => {
            document.getElementById('hist-list').innerHTML = "<div class='hist-item' style='color:red'>Cloud DB Unreachable</div>";
        });
};

chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    const url = tabs[0].url;
    if (!url.startsWith('http')) return; // Don't scan system pages

    document.getElementById('url-text').innerText = url;
    document.getElementById('tech-tags').innerHTML = "<small style='color:#888'>Cloud Analysis in Progress...</small>";

    fetch(`${API_BASE_URL}/analyze?url=${encodeURIComponent(url)}`)
        .then(r => r.json())
        .then(data => {
            if (data.tech && data.tech.length > 0) {
                document.getElementById('tech-tags').innerHTML = data.tech.map(t => `<span class="tag">${t}</span>`).join('');
            } else {
                document.getElementById('tech-tags').innerHTML = "<span class='tag'>Generic Tech</span>";
            }
        })
        .catch(err => {
            document.getElementById('tech-tags').innerHTML = "<span style='color:#ff4757; font-size:10px;'>Backend Sleeping or Offline</span>";
        });
});