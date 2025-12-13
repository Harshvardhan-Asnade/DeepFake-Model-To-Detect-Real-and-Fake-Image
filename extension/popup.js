/**
 * DeepGuard Browser Extension - Compact Popup Logic
 */

const API_URL = 'http://localhost:5001/api/predict';
const API_STATUS_URL = 'http://localhost:5001/api/model-status';

// DOM Elements
const uploadZone = document.getElementById('uploadZone');
const uploadSection = document.getElementById('uploadSection');
const fileInput = document.getElementById('fileInput');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const resultImage = document.getElementById('resultImage');
const resultBadge = document.getElementById('resultBadge');
const resultLabel = document.getElementById('resultLabel');
const resultConfidence = document.getElementById('resultConfidence');
const statusValue = document.getElementById('statusValue');
const confidenceDetail = document.getElementById('confidenceDetail');
const newCheckBtn = document.getElementById('newCheckBtn');
const historyGrid = document.getElementById('historyGrid');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const apiStatus = document.getElementById('apiStatus');

// State
let selectedFile = null;
let selectedImageUrl = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkAPIStatus();
    loadHistory();
    setupEventListeners();
    checkForContextMenuResult();
});

// Check if there's a result from context menu to display
function checkForContextMenuResult() {
    chrome.storage.local.get(['showLastResult', 'lastResult', 'lastError'], (data) => {
        if (data.showLastResult && data.lastResult) {
            // Get the image URL from history
            chrome.storage.local.get(['history'], (historyData) => {
                const history = historyData.history || [];
                if (history.length > 0 && history[0].imageUrl) {
                    displayResults(data.lastResult, history[0].imageUrl);
                } else {
                    displayResults(data.lastResult, null);
                }
            });
            chrome.storage.local.set({ showLastResult: false });
        } else if (data.lastError) {
            showError(data.lastError);
            chrome.storage.local.remove('lastError');
        }
    });
}

// Setup Event Listeners
function setupEventListeners() {
    uploadZone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);

    // Global Drag & Drop
    document.body.addEventListener('dragover', handleGlobalDragOver);
    document.body.addEventListener('dragleave', handleGlobalDragLeave);
    document.body.addEventListener('drop', handleGlobalDrop);

    newCheckBtn.addEventListener('click', resetToUpload);
    clearHistoryBtn.addEventListener('click', clearHistory);
}

// Check API Status
async function checkAPIStatus() {
    try {
        const response = await fetch(API_STATUS_URL);
        const data = await response.json();

        if (data.loaded && data.exists) {
            apiStatus.classList.add('online');
        } else {
            apiStatus.classList.add('offline');
        }
    } catch (error) {
        apiStatus.classList.add('offline');
    }
}

// File Selection Handlers
// Global Drag & Drop Handlers
function handleGlobalDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.body.classList.add('dragging');
}

function handleGlobalDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    // Only remove if leaving the window (not just entering a child element)
    if (e.clientX <= 0 || e.clientY <= 0 || e.clientX >= window.innerWidth || e.clientY >= window.innerHeight) {
        document.body.classList.remove('dragging');
    }
}

function handleGlobalDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    document.body.classList.remove('dragging');

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        selectedFile = file;
        selectedImageUrl = URL.createObjectURL(file);
        analyzeImage();
    }
}

// Analyze Image
async function analyzeImage() {
    if (!selectedFile) return;

    // Show loading state
    uploadSection.style.display = 'none';
    loadingState.style.display = 'block';
    resultsSection.style.display = 'none';

    try {
        const formData = new FormData();
        formData.append('image', selectedFile);

        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data.prediction, selectedImageUrl);
            saveToHistory(data.prediction, selectedImageUrl);
        } else {
            showError(data.error || 'Analysis failed');
        }
    } catch (error) {
        showError('Unable to connect to API. Make sure backend is running on localhost:5001');
    }
}

// Display Results
function displayResults(prediction, imageUrl) {
    loadingState.style.display = 'none';
    uploadSection.style.display = 'none';
    resultsSection.style.display = 'flex';

    const isReal = prediction.class === 'Real';

    // Set image
    if (imageUrl) {
        resultImage.src = imageUrl;
    }

    const imageContainer = document.querySelector('.result-image-container');

    // Visual Feedback
    if (isReal) {
        launchConfetti();
        imageContainer.classList.remove('fake-warning');
        // Green glow for real
        imageContainer.style.boxShadow = '0 4px 20px rgba(0, 212, 170, 0.3)';
        imageContainer.style.border = '2px solid var(--success)';
    } else {
        imageContainer.classList.add('fake-warning');
        imageContainer.style.boxShadow = 'none'; // Class handles it
        imageContainer.style.border = 'none'; // Class handles it
    }

    // Update badge
    resultLabel.textContent = isReal ? 'REAL' : 'FAKE';
    resultLabel.className = 'result-label ' + (isReal ? 'real' : 'fake');
    resultConfidence.textContent = prediction.confidence + '%';

    // Update details
    statusValue.textContent = isReal ? 'Real Image ✓' : 'Deepfake Detected ⚠';
    statusValue.style.color = isReal ? 'var(--success)' : 'var(--warning)';
    confidenceDetail.textContent = prediction.confidence + '%';
}

// Show Error
function showError(message) {
    loadingState.style.display = 'none';
    uploadSection.style.display = 'flex';
    resultsSection.style.display = 'none';
    alert(message);
}

// Reset to Upload
function resetToUpload() {
    selectedFile = null;
    selectedImageUrl = null;
    fileInput.value = '';
    uploadSection.style.display = 'flex';
    loadingState.style.display = 'none';
    resultsSection.style.display = 'none';
}

// History Management
function saveToHistory(result, imageUrl) {
    chrome.storage.local.get(['history'], (data) => {
        const history = data.history || [];

        history.unshift({
            timestamp: Date.now(),
            imageUrl: imageUrl,
            result: result,
            source: 'popup'
        });

        if (history.length > 12) {
            history.pop();
        }

        chrome.storage.local.set({ history }, () => {
            loadHistory();
        });
    });
}

function loadHistory() {
    chrome.storage.local.get(['history'], (data) => {
        const history = data.history || [];

        if (history.length === 0) {
            historyGrid.innerHTML = '<div class="empty-history">No recent checks</div>';
            return;
        }

        historyGrid.innerHTML = history.slice(0, 8).map(item => {
            const isReal = item.result.class === 'Real';
            return `
        <div class="history-item" data-timestamp="${item.timestamp}" title="${new Date(item.timestamp).toLocaleString()}">
          <img src="${item.imageUrl}" alt="History">
          <div class="history-item-badge ${isReal ? 'real' : 'fake'}"></div>
        </div>
      `;
        }).join('');

        // Add click handlers
        document.querySelectorAll('.history-item').forEach(item => {
            item.addEventListener('click', () => {
                const timestamp = parseInt(item.dataset.timestamp);
                const historyItem = history.find(h => h.timestamp === timestamp);
                if (historyItem) {
                    displayResults(historyItem.result, historyItem.imageUrl);
                }
            });
        });
    });
}

function clearHistory() {
    if (confirm('Clear all history?')) {
        chrome.storage.local.set({ history: [] }, () => {
            loadHistory();
        });
    }
}

// Simple Confetti
function launchConfetti() {
    const colors = ['#667eea', '#00d4aa', '#ff6b6b', '#ffd166', '#ffffff'];

    for (let i = 0; i < 40; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';

        // Random properties
        const left = Math.random() * 100;
        const color = colors[Math.floor(Math.random() * colors.length)];
        const duration = Math.random() * 1.5 + 1.5; // 1.5-3s
        const delay = Math.random() * 0.5;

        confetti.style.left = left + '%';
        confetti.style.backgroundColor = color;
        confetti.style.animation = `fall ${duration}s ease-out ${delay}s forwards`;

        document.body.appendChild(confetti);

        // Cleanup
        setTimeout(() => {
            confetti.remove();
        }, (duration + delay) * 1000);
    }
}
