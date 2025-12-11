/**
 * DeepGuard Browser Extension - Background Service Worker
 * Handles context menu creation and message passing
 */

// Create context menu on installation
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: 'checkDeepfake',
        title: 'Check for Deepfake',
        contexts: ['image']
    });

    console.log('DeepGuard extension installed successfully!');
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'checkDeepfake' && info.srcUrl) {
        // Send message to content script to fetch the image
        chrome.tabs.sendMessage(
            tab.id,
            {
                action: 'analyzeImage',
                imageUrl: info.srcUrl
            },
            (response) => {
                if (chrome.runtime.lastError) {
                    console.error('Error sending message:', chrome.runtime.lastError);
                    return;
                }

                if (response && response.success) {
                    // Store result for popup to display
                    chrome.storage.local.get(['history'], (data) => {
                        const history = data.history || [];
                        history.unshift({
                            timestamp: Date.now(),
                            imageUrl: info.srcUrl,
                            result: response.result,
                            source: 'context-menu'
                        });

                        // Keep only last 20 results
                        if (history.length > 20) {
                            history.pop();
                        }

                        chrome.storage.local.set({
                            history,
                            lastResult: response.result,
                            showLastResult: true  // Flag to show result in popup
                        }, () => {
                            // Open the popup to show the result
                            chrome.action.openPopup();
                        });
                    });
                } else if (response && !response.success) {
                    // Store error state and open popup
                    chrome.storage.local.set({
                        lastError: response.error || 'Analysis failed',
                        showLastResult: false
                    }, () => {
                        chrome.action.openPopup();
                    });
                }
            }
        );
    }
});

// Show notification with result
function showNotification(result) {
    const isReal = result.class === 'Real';
    const title = isReal ? '✓ Image appears Real' : '⚠ Deepfake Detected';
    const message = `Confidence: ${result.confidence}%`;

    // You can add chrome.notifications here if you want desktop notifications
    console.log(`${title} - ${message}`);
}

// Handle messages from content script or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getLastResult') {
        chrome.storage.local.get(['lastResult'], (data) => {
            sendResponse({ result: data.lastResult });
        });
        return true; // Keep channel open for async response
    }

    if (request.action === 'clearHistory') {
        chrome.storage.local.set({ history: [] }, () => {
            sendResponse({ success: true });
        });
        return true;
    }
});
