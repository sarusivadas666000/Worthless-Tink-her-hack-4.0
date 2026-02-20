# 🚀 Quick Start Guide

## Installation (One-Time Setup)

### 1. Virtual Environment
```powershell
cd "c:\Users\dolus\OneDrive\Desktop\tink"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
cd "ai-product-video\backend"
pip install -r requirements.txt
```

## Running the Application

### Terminal 1 - Backend API Server
```powershell
cd "c:\Users\dolus\OneDrive\Desktop\tink\Worthless-Tink-her-hack-4.0\ai-product-video\backend"
.\..\..\.venv\Scripts\python.exe -m uvicorn main:app --reload
```
**Runs at**: http://127.0.0.1:8000

### Terminal 2 - Frontend Server
```powershell
cd "c:\Users\dolus\OneDrive\Desktop\tink\Worthless-Tink-her-hack-4.0\ai-product-video\frontend"
.\..\..\.venv\Scripts\python.exe -m http.server 3000
```
**Runs at**: http://127.0.0.1:3000

## Usage

1. Open browser to http://127.0.0.1:3000
2. Upload initial product image
3. Upload final product image
4. Select 3D camera effects:
   - ✓ Zoom/Dolly
   - ✓ Pan
   - ✓ 3D Perspective
   - ✓ Motion Blur
   - □ Full Rotation (optional)
   - □ Depth of Field (optional)
5. Click "Generate 3D Video"
6. Wait 2-3 minutes for processing
7. Download generated MP4

## API Testing

### Health Check
```bash
curl http://127.0.0.1:8000/health
```

### Available Effects
```bash
curl http://127.0.0.1:8000/effects
```

### Generate Video (CLI)
```bash
curl -X POST "http://127.0.0.1:8000/generate-video?effects=%7B%22zoom%22%3Atrue%2C%22pan%22%3Atrue%7D" \
  -F "initial_image=@image1.jpg" \
  -F "final_image=@image2.jpg" \
  -o output.mp4
```

## Output

- **File**: product_video_3d.mp4
- **Duration**: ~2.5 seconds
- **Resolution**: 1080x1080
- **FPS**: 24

## Troubleshooting

### OpenCV Import Error
```powershell
pip install --upgrade opencv-python
```

### Port Already in Use
- Backend (8000): `netstat -ano | findstr :8000`
- Frontend (3000): `netstat -ano | findstr :3000`

### Video Generation Slow
This is normal! Processing pipeline:
1. Frame generation: ~1 min (60 frames with 3D effects)
2. Video encoding: ~1-2 min (MP4 compression)
3. Total: 2-3 minutes expected

## 3D Effects Explanation

| Effect | What It Does |
|--------|-------------|
| 🔍 Zoom | Camera moves forward/backward |
| ↔️ Pan | Camera moves left/right/up/down |
| 🎲 Perspective | Image tilts in 3D space |
| 💨 Motion Blur | Smooth cinematic motion effect |
| 🔄 Rotation | Full 360° spin |
| 👁️ DOF | Focus blur effect |
| 🌈 Chroma | RGB separation effect |

## File Locations

```
ai-product-video/
├── backend/
│   ├── main.py                  ← FastAPI app
│   ├── config.py                ← Settings
│   ├── requirements.txt          ← Dependencies
│   ├── uploads/                 ← Temp images
│   ├── outputs/                 ← Generated videos
│   ├── utils/file_manager.py    ← File ops
│   └── services/frame_generator_3d.py  ← 3D effects
├── frontend/
│   ├── index.html               ← UI
│   ├── style.css                ← Styling
│   └── script.js                ← Effects control
└── README_3D.md                 ← Full documentation
```

## Made With ❤️

- **Python**: FastAPI, OpenCV, MoviePy, Pillow
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **OS**: Windows 10/11

---

**Ready to create cinematic product videos! 🎬✨**
