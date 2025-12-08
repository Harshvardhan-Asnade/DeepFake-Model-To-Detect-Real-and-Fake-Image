// ==================== DOM Elements ====================
// Using safe selection to prevent errors if elements mockups don't match exactly
const safeGet = (id) => document.getElementById(id);

const uploadArea = safeGet('uploadArea');
const uploadPlaceholder = safeGet('uploadPlaceholder');
const fileInput = safeGet('fileInput');
const browseBtn = safeGet('browseBtn');
const previewContainer = safeGet('previewContainer');
const imagePreview = safeGet('imagePreview');
const removeBtn = safeGet('removeBtn');
const analyzeBtn = safeGet('analyzeBtn');
const resultsCard = safeGet('resultsCard');
const resultBadge = safeGet('resultsCard') ? safeGet('resultsCard').querySelector('.result') : null; // Adapted selector
const confidenceValue = safeGet('confidenceValue');
const confidenceFill = safeGet('confidenceFill');
const analyzeAnotherBtn = safeGet('analyzeAnotherBtn');
const loadingOverlay = safeGet('loadingOverlay');
const modelStatus = document.querySelector('.status-indicator'); // Class selector for status

// Missing elements in new design - keeping null reference or mocking
const detailClass = null;
const detailConfidence = null;
const detailRaw = null;
const closeResults = null;
const resultClass = null;

// ==================== State Management ====================
let currentFile = null;

// ==================== Check Model Status ====================
async function checkModelStatus() {
    if (!modelStatus) return;

    try {
        const response = await fetch('/api/model-status');
        const data = await response.json();

        const dot = modelStatus.querySelector('.status-dot');
        const text = modelStatus.querySelector('span:last-child'); // Target text span

        if (data.loaded) {
            if (dot) dot.style.background = 'var(--success-green, #10b981)';
            if (text) text.textContent = 'Model Ready';
        } else {
            if (dot) dot.style.background = 'var(--alert-red, #ef4444)';
            if (text) text.textContent = 'Model Not Loaded';
        }
    } catch (error) {
        console.error('Error checking model status:', error);
    }
}

// Check status on load
checkModelStatus();

// ==================== File Upload Handlers ====================
if (browseBtn && fileInput) {
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent bubbling to uploadArea
        fileInput.click();
    });
}

if (uploadArea && fileInput) {
    uploadArea.addEventListener('click', (e) => {
        if (e.target !== browseBtn && e.target !== removeBtn && e.target !== analyzeBtn && !e.target.closest('button')) {
            fileInput.click();
        }
    });

    // Drag and Drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--accent-purple)';
        uploadArea.style.background = 'rgba(127, 90, 240, 0.05)';
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '';
        uploadArea.style.background = '';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '';
        uploadArea.style.background = '';

        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFile(file);
        }
    });
}

if (fileInput) {
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });
}

// ==================== Handle File ====================
function handleFile(file) {
    currentFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        if (imagePreview) imagePreview.src = e.target.result;
        if (uploadPlaceholder) uploadPlaceholder.classList.add('hidden');
        if (previewContainer) previewContainer.classList.remove('hidden');
        // Simple display toggle for the new structure
        if (uploadPlaceholder) uploadPlaceholder.style.display = 'none';

        // Enable analyze
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.style.opacity = '1';
            analyzeBtn.style.cursor = 'pointer';
        }
    };
    reader.readAsDataURL(file);
}

// ==================== Remove Image ====================
if (removeBtn) {
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUpload();
    });
}

function resetUpload() {
    currentFile = null;
    if (imagePreview) imagePreview.src = '';
    if (fileInput) fileInput.value = '';

    if (uploadPlaceholder) {
        uploadPlaceholder.classList.remove('hidden');
        uploadPlaceholder.style.display = 'flex'; // Restore flex display
        uploadPlaceholder.style.flexDirection = 'column';
    }

    if (previewContainer) previewContainer.classList.add('hidden');
    if (resultsCard) resultsCard.classList.add('hidden');

    if (analyzeBtn) analyzeBtn.disabled = true;
}

// ==================== Analyze Image ====================
if (analyzeBtn) {
    analyzeBtn.addEventListener('click', async (e) => {
        e.stopPropagation();
        if (!currentFile) return;

        if (loadingOverlay) loadingOverlay.classList.remove('hidden');
        if (loadingOverlay) loadingOverlay.style.display = 'flex';

        const formData = new FormData();
        formData.append('image', currentFile);

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (loadingOverlay) {
                loadingOverlay.classList.add('hidden');
                loadingOverlay.style.display = 'none';
            }

            if (data.success) {
                // Store data for the results page
                sessionStorage.setItem('analysisResult', JSON.stringify(data.prediction));

                // Use the URL returned by server if available, else local reader result (less reliable for sharing but works for session)
                // Since I handle the file upload in app.py now, I should use the returned URL if possible.
                // But data.prediction might need update in app.py to return url. 
                // Let's rely on local preview for speed if needed, or better, use the server path.
                // Assuming app.py returns 'image_url' or similar now.

                if (data.prediction.image_url) {
                    sessionStorage.setItem('analysisImage', data.prediction.image_url);
                } else if (imagePreview && imagePreview.src) {
                    sessionStorage.setItem('analysisImage', imagePreview.src);
                }

                sessionStorage.setItem('analysisFilename', currentFile.name);

                // Redirect to results page
                window.location.href = '/results';
            } else {
                alert(data.error || 'An error occurred');
            }
        } catch (error) {
            if (loadingOverlay) {
                loadingOverlay.classList.add('hidden');
                loadingOverlay.style.display = 'none';
            }
            console.error('Error:', error);
            alert('Network error during analysis');
        }
    });
}

// ==================== Display Results ====================
function displayResults(prediction) {
    const { class: predClass, confidence } = prediction;

    if (resultBadge) {
        resultBadge.textContent = `${confidence}% ${predClass}`;
        resultBadge.className = 'result ' + (predClass === 'Real' ? 'genuine' : 'deepfake');
    }

    if (confidenceValue) confidenceValue.textContent = `${confidence}%`;

    if (confidenceFill) {
        confidenceFill.style.width = `${confidence}%`;
        confidenceFill.style.background = predClass === 'Real' ? 'var(--success-green)' : 'var(--alert-red)';
    }

    if (resultsCard) resultsCard.classList.remove('hidden');
}

// ==================== Analyze Another ====================
if (analyzeAnotherBtn) {
    analyzeAnotherBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUpload();
    });
}

console.log('Script initialized (New Design Compatible)');

