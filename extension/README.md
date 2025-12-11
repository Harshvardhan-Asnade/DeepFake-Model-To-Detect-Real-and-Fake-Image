# DeepGuard Browser Extension

A Chrome/Edge browser extension that integrates with the DeepGuard deepfake detection API to analyze images directly from your browser.

## Features

✨ **Right-Click Detection** - Right-click any image on the web to check for deepfakes  
📤 **Upload Images** - Drag-and-drop or select images from your computer  
📊 **Confidence Scores** - View detailed analysis with confidence percentages  
📜 **History Tracking** - Keep track of your recent image checks  
🎨 **Modern UI** - Premium glassmorphic design with smooth animations  

## Installation

### Prerequisites

Make sure the DeepGuard backend is running:

```bash
cd /Users/harshvardhan/Developer/Deepfake-Model-To-Detect-Real-and-Fake-Image
bash start_website.sh
```

The backend should be accessible at `http://localhost:5001`.

### Install Extension

1. **Open Chrome/Edge** and navigate to:
   - Chrome: `chrome://extensions/`
   - Edge: `edge://extensions/`

2. **Enable Developer Mode** (toggle in the top-right corner)

3. **Load Unpacked Extension**:
   - Click "Load unpacked"
   - Navigate to: `/Users/harshvardhan/Developer/Deepfake-Model-To-Detect-Real-and-Fake-Image/extension`
   - Click "Select"

4. **Pin the Extension** (optional):
   - Click the puzzle icon in the toolbar
   - Pin "DeepGuard - Deepfake Detector"

## Usage

### Method 1: Right-Click on Images

1. Browse any website with images
2. Right-click on any image
3. Select **"Check for Deepfake"**
4. View the result in the extension popup

### Method 2: Upload from Popup

1. Click the DeepGuard icon in your browser toolbar
2. Drag and drop an image, or click "Select Image"
3. Click "Analyze"
4. View detailed results with confidence scores

## Features Breakdown

### Popup Interface
- **Status Indicator**: Shows connection status to the backend API
- **Upload Zone**: Drag-and-drop or click to select images
- **Results Display**: 
  - Classification (Real/Fake)
  - Confidence percentage
  - Raw score from the model
  - Visual confidence meter
- **History**: View up to 20 recent image checks

### Context Menu Integration
- Right-click any image on any webpage
- Automatic analysis using the same AI model
- Results saved to history

## Configuration

### Change API URL (for Production)

If you deploy the backend to a production server:

1. Open `extension/popup.js`
2. Update line 6:
   ```javascript
   const API_URL = 'https://your-production-url.com/api/predict';
   ```

3. Open `extension/content.js`
4. Update line 6:
   ```javascript
   const API_URL = 'https://your-production-url.com/api/predict';
   ```

5. Reload the extension in Chrome

### Enable CORS (Already Done)

The backend has been updated to support CORS requests from the extension. If you need to modify CORS settings, edit `backend/app.py`:

```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

## File Structure

```
extension/
├── manifest.json       # Extension configuration (Manifest V3)
├── background.js       # Service worker for context menu
├── content.js          # Page interaction script
├── popup.html          # Extension popup interface
├── popup.css           # Modern styling with glassmorphism
├── popup.js            # Popup logic and API calls
└── icons/              # Extension icons
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

## Troubleshooting

### "Offline" Status

**Problem**: Extension shows "Offline" or "Model not loaded"

**Solutions**:
1. Ensure the backend is running: `bash start_website.sh`
2. Check that the API is accessible at `http://localhost:5001`
3. Verify the model file exists at `model/checkpoints/final_model_pro.keras`

### CORS Errors

**Problem**: Console shows CORS errors when analyzing images

**Solutions**:
1. Make sure `flask-cors` is installed: `pip install flask-cors`
2. Restart the backend server
3. Check that CORS is enabled in `backend/app.py`

### Context Menu Not Working

**Problem**: Right-click option doesn't appear

**Solutions**:
1. Reload the extension in `chrome://extensions/`
2. Refresh the webpage you're testing on
3. Check that the extension has required permissions

### Images Not Loading from Web

**Problem**: Right-click detection fails for some images

**Solutions**:
- Some websites block external access to images (CORS policy)
- Try downloading the image and uploading it via the popup instead
- This is a browser security limitation, not an extension issue

## Technology Stack

- **Manifest V3** - Latest Chrome extension standard
- **Service Workers** - Background task handling
- **Vanilla JavaScript** - No framework dependencies
- **Modern CSS** - Glassmorphic design with animations
- **Chrome Storage API** - History persistence

## Security & Privacy

- ✅ All analysis happens on your local backend
- ✅ Images are sent only to `localhost:5001` (your machine)
- ✅ No data is sent to external servers
- ✅ History is stored locally in browser storage
- ✅ Images are not permanently stored

## Development

### Making Changes

1. Edit files in the `extension/` directory
2. Go to `chrome://extensions/`
3. Click the refresh icon on the DeepGuard card
4. Test your changes

### Debugging

- **Background Script**: `chrome://extensions/` → DeepGuard → "Inspect views: service worker"
- **Popup**: Right-click the extension icon → "Inspect popup"
- **Content Script**: Regular page DevTools (F12)

## Future Enhancements

Potential features for future versions:

- [ ] Batch analysis of multiple images
- [ ] Configurable API endpoint in settings
- [ ] Desktop notifications for results
- [ ] Export history as CSV/JSON
- [ ] Video frame analysis
- [ ] Keyboard shortcuts
- [ ] Multiple backend profiles

## License

This extension is part of the DeepGuard project. See the main project README for license information.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the main project documentation
3. Ensure all dependencies are installed
4. Verify the backend is running correctly

---

**Built with ❤️ by the DeepGuard Team**
