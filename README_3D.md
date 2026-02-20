# 🎬 AI 3D Product Video Generator

A professional web application that creates cinematic 3D transition videos between product images with advanced camera movements and visual effects.

## ✨ Features

### 3D Camera Effects
- **🔍 Zoom/Dolly**: Camera moves forward and backward for depth effect
- **↔️ Pan**: Camera moves smoothly left, right, up, and down
- **🎲 3D Perspective**: Images tilt and rotate in 3D space
- **🔄 Full Rotation**: Complete 360° spin on multiple axes
- **💨 Motion Blur**: Cinematic motion blur for smooth transitions
- **👁️ Depth of Field**: Focus blur effect with moving focal points
- **🌈 Chromatic Aberration**: RGB channel separation for sci-fi effect

### Technical Features
- Smooth alpha blending between images
- OpenCV-based image transformations
- MoviePy video encoding (H.264/libx264)
- 60-frame smooth transitions at 24 FPS
- CORS enabled for cross-origin requests
- Real-time effect preview controls

## 🚀 Project Structure

```
ai-product-video/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration and default settings
│   ├── requirements.txt        # Python dependencies
│   ├── utils/
│   │   ├── __init__.py
│   │   └── file_manager.py    # File operations
│   └── services/
│       ├── __init__.py
│       ├── frame_generator_3d.py    # 3D frame generation
│       ├── video_creator.py         # MP4 creation
│       └── video_service.py         # Orchestration
│
└── frontend/
    ├── index.html             # Modern UI
    ├── style.css              # Responsive styling
    └── script.js              # Effect controls & API calls
```

## 📦 Requirements

### Backend Dependencies
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pillow==10.1.0
moviepy==1.0.3
numpy==1.24.3
opencv-python==4.8.1.78
```

### Python Version
- Python 3.11+ (Windows compatible)

## 🔧 Installation

### 1. Setup Virtual Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate environment
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
cd backend
pip install -r requirements.txt
```

## 🎯 Usage

### Start Backend Server
```powershell
cd backend
python -m uvicorn main:app --reload
```
Backend runs at: `http://127.0.0.1:8000`

### Start Frontend Server
```powershell
cd frontend
python -m http.server 3000
```
Frontend runs at: `http://127.0.0.1:3000`

## 📡 API Endpoints

### Health Check
```
GET /health
```
Response:
```json
{
  "status": "ok",
  "service": "AI Product Video Generator 3D",
  "features": ["3D perspective", "camera zoom", "camera pan", "motion blur"]
}
```

### Available Effects
```
GET /effects
```
Returns all available 3D effects with descriptions.

### Generate Video
```
POST /generate-video
Content-Type: multipart/form-data

Parameters:
- initial_image: File (JPG/PNG)
- final_image: File (JPG/PNG)
- effects: JSON string (optional)

Example effects parameter:
{"zoom": true, "pan": true, "rotation": false, "perspective": true, "motion_blur": true}
```

Response: MP4 video file

## 🎨 Frontend Features

- **Drag & Drop Upload**: Easy image upload
- **Live Previews**: See uploaded images before processing
- **Effect Controls**: Toggle 3D effects on/off
- **Progress Indicator**: Loading animation during processing
- **Video Player**: Built-in video preview
- **One-Click Download**: Download generated video

## 🔄 3D Effects Implementation

### Perspective Transform
Uses multi-axis 3D rotation matrices (Euler angles) to create tilting effects that simulate camera movement in 3D space.

### Camera Zoom
Implements dolly effect by cropping center region and scaling back, creating smooth zoom in/out motion.

### Camera Pan
Applies translation matrix for horizontal and vertical camera movement across the image.

### Motion Blur
Applies Gaussian blur with intensity that varies with animation progress for cinematic smoothness.

### Depth of Field
Creates circular focus point that moves throughout the animation with gradient mask for selective blur.

### Chromatic Aberration
Separates and shifts RGB channels for sci-fi visual effect.

## 📊 Video Output Specs

- **Resolution**: 1080x1080 pixels
- **Duration**: ~2.5 seconds (60 frames at 24 FPS)
- **Codec**: H.264 (libx264)
- **Format**: MP4
- **Audio**: None

## 🚨 Error Handling

- Image type validation (JPG/PNG only)
- Size validation (10MB max)
- Async file operations
- Automatic cleanup of temporary files
- Detailed error logging
- User-friendly error messages

## 💡 Usage Examples

### Basic Usage
1. Upload initial product image
2. Upload final product image
3. Select desired 3D effects
4. Click "Generate 3D Video"
5. Download when complete

### Customization

#### Enable Specific Effects Only
```javascript
const effects = {
  "zoom": true,
  "pan": true,
  "rotation": false,
  "perspective": true,
  "motion_blur": true,
  "depth_of_field": false,
  "chromatic_aberration": false
};
```

#### Disable All Effects (Basic Fade)
```javascript
const effects = {
  "zoom": false,
  "pan": false,
  "rotation": false,
  "perspective": false,
  "motion_blur": false,
  "depth_of_field": false,
  "chromatic_aberration": false
};
```

## ⚡ Performance Notes

- Frame generation: ~30-60 seconds (60 frames)
- Video encoding: ~1-2 minutes
- Total processing time: ~2-3 minutes per video
- Requires moderate GPU acceleration for optimal performance

## 🛠️ Configuration

Edit `backend/config.py` to customize:

```python
FRAME_COUNT = 60              # Number of transition frames
FPS = 24                      # Playback frame rate
MAX_IMAGE_SIZE = 10485760     # Maximum upload size
DEFAULT_3D_EFFECTS = {...}    # Default effect settings
```

## 📝 File Formats

**Supported Input Formats**:
- JPEG (.jpg, .jpeg)
- PNG (.png)

**Output Format**:
- MP4 (H.264 video codec)

## 🔐 Security Features

- CORS enabled for cross-origin requests
- File type validation
- File size limits
- Automatic temporary file cleanup
- Input sanitization

## 🎓 Technical Details

### Technologies Used
- **Backend**: FastAPI (async Python framework)
- **Video**: MoviePy (video processing)
- **Image**: Pillow + OpenCV (image manipulation)
- **Frontend**: Vanilla JavaScript (no dependencies)
- **Server**: Uvicorn (ASGI server)

### Architecture
- RESTful API endpoints
- Async/await file operations
- Multi-step processing pipeline
- Temporary file cleanup
- Logging and error handling

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 📞 Support

For issues or questions, check the console logs for detailed error messages and API responses.

---

**Happy video generating! 🎬✨**
