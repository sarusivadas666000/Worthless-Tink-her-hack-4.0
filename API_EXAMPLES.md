# 📡 API Examples & Curl Commands

## Quick Reference

### Backend Running At
```
http://127.0.0.1:8000
```

### Frontend Running At
```
http://127.0.0.1:3000
```

---

## 🔍 Health Check

### Check Server Status
```bash
curl http://127.0.0.1:8000/health
```

### Response
```json
{
  "status": "ok",
  "service": "AI Product Video Generator 3D",
  "features": [
    "3D perspective",
    "camera zoom",
    "camera pan",
    "motion blur"
  ]
}
```

---

## 📋 Available Effects

### Get List of Effects
```bash
curl http://127.0.0.1:8000/effects
```

### Response
```json
{
  "available_effects": {
    "zoom": true,
    "pan": true,
    "rotation": false,
    "perspective": true,
    "depth_of_field": false,
    "motion_blur": true,
    "chromatic_aberration": false
  },
  "description": {
    "zoom": "Camera zoom/dolly effect - moves forward and backward",
    "pan": "Camera pan effect - moves left/right/up/down",
    "rotation": "Full 3D rotation - spins the image",
    "perspective": "3D perspective tilt - tilts in 3D space",
    "depth_of_field": "Depth of field - focus blur effect",
    "motion_blur": "Cinematic motion blur - smooths motion",
    "chromatic_aberration": "RGB channel separation - sci-fi effect"
  }
}
```

---

## 🎬 Generate Video

### Basic Usage (Default Effects)
```bash
curl -X POST http://127.0.0.1:8000/generate-video \
  -F "initial_image=@image1.jpg" \
  -F "final_image=@image2.jpg" \
  -o output.mp4
```

### With Custom Effects (All Disabled)
```bash
# Encode effects JSON
EFFECTS='{"zoom":false,"pan":false,"rotation":false,"perspective":false,"depth_of_field":false,"motion_blur":false,"chromatic_aberration":false}'

curl -X POST "http://127.0.0.1:8000/generate-video?effects=$(echo -n "$EFFECTS" | jq -sRr @uri)" \
  -F "initial_image=@image1.jpg" \
  -F "final_image=@image2.jpg" \
  -o output.mp4
```

### With Custom Effects (Action Mode)
```bash
EFFECTS='{"zoom":true,"pan":true,"rotation":true,"perspective":true,"motion_blur":true,"depth_of_field":false,"chromatic_aberration":false}'

curl -X POST "http://127.0.0.1:8000/generate-video?effects=$(python3 -c "import json, urllib.parse; print(urllib.parse.quote(json.dumps(json.loads('${EFFECTS}'))))" )" \
  -F "initial_image=@image1.jpg" \
  -F "final_image=@image2.jpg" \
  -o output_action.mp4
```

### PowerShell Examples

#### Default Effects
```powershell
$params = @{
    Uri = 'http://127.0.0.1:8000/generate-video'
    Method = 'POST'
    Form = @{
        initial_image = Get-Item -Path 'C:\path\to\image1.jpg'
        final_image = Get-Item -Path 'C:\path\to\image2.jpg'
    }
    OutFile = 'C:\path\to\output.mp4'
}

Invoke-WebRequest @params
```

#### Classic Mode (Zoom + Pan + Blur only)
```powershell
$effects = @{
    "zoom" = $true
    "pan" = $true
    "rotation" = $false
    "perspective" = $false
    "depth_of_field" = $false
    "motion_blur" = $true
    "chromatic_aberration" = $false
} | ConvertTo-Json

$effectsEncoded = [Uri]::EscapeDataString($effects)

$params = @{
    Uri = "http://127.0.0.1:8000/generate-video?effects=$effectsEncoded"
    Method = 'POST'
    Form = @{
        initial_image = Get-Item -Path 'image1.jpg'
        final_image = Get-Item -Path 'image2.jpg'
    }
    OutFile = 'video_classic.mp4'
}

Invoke-WebRequest @params
```

---

## 🎨 Effect Configurations

### Configuration 1: Premium Luxury
```json
{
  "zoom": true,
  "pan": true,
  "rotation": false,
  "perspective": true,
  "depth_of_field": true,
  "motion_blur": true,
  "chromatic_aberration": false
}
```

### Configuration 2: Tech Showcase
```json
{
  "zoom": true,
  "pan": true,
  "rotation": true,
  "perspective": true,
  "depth_of_field": false,
  "motion_blur": true,
  "chromatic_aberration": true
}
```

### Configuration 3: Simple Fade
```json
{
  "zoom": false,
  "pan": false,
  "rotation": false,
  "perspective": false,
  "depth_of_field": false,
  "motion_blur": true,
  "chromatic_aberration": false
}
```

### Configuration 4: Action Pack
```json
{
  "zoom": true,
  "pan": true,
  "rotation": true,
  "perspective": true,
  "depth_of_field": false,
  "motion_blur": true,
  "chromatic_aberration": false
}
```

### Configuration 5: Subtle Pro
```json
{
  "zoom": false,
  "pan": false,
  "rotation": false,
  "perspective": true,
  "depth_of_field": false,
  "motion_blur": true,
  "chromatic_aberration": false
}
```

---

## 🖥️ Frontend Usage

### JavaScript Example - Default Effects
```javascript
const formData = new FormData();
formData.append('initial_image', imageFile1);
formData.append('final_image', imageFile2);

fetch('http://127.0.0.1:8000/generate-video', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const videoUrl = URL.createObjectURL(blob);
    document.getElementById('video').src = videoUrl;
});
```

### JavaScript Example - Custom Effects
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

const effectsJson = JSON.stringify(effects);
const url = `http://127.0.0.1:8000/generate-video?effects=${encodeURIComponent(effectsJson)}`;

const formData = new FormData();
formData.append('initial_image', imageFile1);
formData.append('final_image', imageFile2);

fetch(url, {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const videoUrl = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = videoUrl;
    link.download = 'product_video_3d.mp4';
    link.click();
});
```

### Fetch with Error Handling
```javascript
async function generateVideoWithEffects(image1, image2, effects) {
    try {
        const effectsJson = JSON.stringify(effects);
        const url = `http://127.0.0.1:8000/generate-video?effects=${encodeURIComponent(effectsJson)}`;
        
        const formData = new FormData();
        formData.append('initial_image', image1);
        formData.append('final_image', image2);
        
        console.log('Sending video generation request with effects:', effects);
        
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Video generation failed');
        }
        
        const blob = await response.blob();
        console.log('Video generated successfully, size:', blob.size);
        
        return blob;
    } catch (error) {
        console.error('Error generating video:', error);
        throw error;
    }
}

// Usage
try {
    const videoBlob = await generateVideoWithEffects(
        imageFile1,
        imageFile2,
        {
            "zoom": true,
            "pan": true,
            "rotation": false,
            "perspective": true,
            "motion_blur": true,
            "depth_of_field": false,
            "chromatic_aberration": false
        }
    );
    
    // Save or play video
    const url = URL.createObjectURL(videoBlob);
    document.getElementById('videoPlayer').src = url;
} catch (error) {
    console.error('Failed to generate video:', error);
}
```

---

## 🐍 Python Examples

### Using Requests Library
```python
import requests
import json

# Prepare files
files = {
    'initial_image': open('image1.jpg', 'rb'),
    'final_image': open('image2.jpg', 'rb')
}

# Prepare effects
effects = {
    "zoom": True,
    "pan": True,
    "rotation": False,
    "perspective": True,
    "motion_blur": True,
    "depth_of_field": False,
    "chromatic_aberration": False
}

# Generate video
effects_json = json.dumps(effects)
url = f'http://127.0.0.1:8000/generate-video?effects={requests.utils.quote(effects_json)}'

response = requests.post(url, files=files)

if response.status_code == 200:
    with open('output_video.mp4', 'wb') as f:
        f.write(response.content)
    print('Video saved successfully!')
else:
    print(f'Error: {response.status_code}')
    print(response.json())
```

### Using urllib
```python
import urllib.request
import urllib.parse
import json

def generate_product_video(image1_path, image2_path, effects=None):
    """Generate product video with specified effects"""
    
    if effects is None:
        effects = {
            "zoom": True,
            "pan": True,
            "rotation": False,
            "perspective": True,
            "motion_blur": True,
            "depth_of_field": False,
            "chromatic_aberration": False
        }
    
    # Encode effects
    effects_json = json.dumps(effects)
    effects_encoded = urllib.parse.quote(effects_json)
    
    # Prepare form data
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = []
    
    # Add initial image
    with open(image1_path, 'rb') as f:
        body.append(f'--{boundary}\r\n'.encode())
        body.append(b'Content-Disposition: form-data; name="initial_image"; filename="image1.jpg"\r\n')
        body.append(b'Content-Type: image/jpeg\r\n\r\n')
        body.append(f.read())
        body.append(b'\r\n')
    
    # Add final image
    with open(image2_path, 'rb') as f:
        body.append(f'--{boundary}\r\n'.encode())
        body.append(b'Content-Disposition: form-data; name="final_image"; filename="image2.jpg"\r\n')
        body.append(b'Content-Type: image/jpeg\r\n\r\n')
        body.append(f.read())
        body.append(b'\r\n')
    
    body.append(f'--{boundary}--\r\n'.encode())
    
    # Make request
    url = f'http://127.0.0.1:8000/generate-video?effects={effects_encoded}'
    req = urllib.request.Request(url, data=b''.join(body))
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    
    try:
        with urllib.request.urlopen(req) as response:
            video_data = response.read()
            with open('output_video.mp4', 'wb') as f:
                f.write(video_data)
            print('Video generated successfully!')
    except Exception as e:
        print(f'Error: {e}')

# Usage
generate_product_video('image1.jpg', 'image2.jpg')
```

---

## 📊 Response Examples

### Success Response (200 OK)
```
Content-Type: video/mp4
Content-Length: 20500000

[Binary MP4 video data... 20.5 MB]
```

### Error Response (400 Bad Request)
```json
{
  "detail": "Invalid initial image type. Allowed: {'image/jpeg', 'image/png'}"
}
```

### Error Response (500 Internal Server Error)
```json
{
  "detail": "Video generation failed: [specific error message]"
}
```

---

## 🚀 Tips for Integration

### Batch Processing
```python
videos = []
for product in products:
    img1_path = f"./images/{product.name}_before.jpg"
    img2_path = f"./images/{product.name}_after.jpg"
    
    effects = get_effects_for_product_type(product.type)
    video_blob = await generate_video(img1_path, img2_path, effects)
    
    videos.append({
        'product_id': product.id,
        'video': video_blob,
        'effects': effects
    })

save_all_videos(videos)
```

### Error Handling & Retry
```python
import time
from typing import Optional

def generate_with_retry(
    image1_path: str,
    image2_path: str,
    effects: dict = None,
    max_retries: int = 3
) -> Optional[bytes]:
    """Generate video with automatic retry"""
    
    for attempt in range(max_retries):
        try:
            result = generate_product_video(image1_path, image2_path, effects)
            return result
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return None

# Usage
video = generate_with_retry('img1.jpg', 'img2.jpg')
```

---

## 📱 Integration Examples

### WordPress Plugin (Pseudo-code)
```javascript
// Add video generation to product pages
addEventListener('generate_product_video', async (event) => {
    const beforeImg = document.querySelector('.product-before-image');
    const afterImg = document.querySelector('.product-after-image');
    
    const effects = wp.localStorage.getItem('product_video_effects');
    const video = await fetch_generate_video(beforeImg, afterImg, effects);
    
    display_video_in_modal(video);
});
```

### Shopify App (Pseudo-code)
```javascript
// Shopify webhook handler
app.post('/webhooks/product-updated', async (req, res) => {
    const product = req.body;
    
    const images = product.images.slice(0, 2);
    if (images.length < 2) return;
    
    const video = await generateProductVideo(
        images[0].src,
        images[1].src,
        SHOPIFY_EFFECTS_CONFIG
    );
    
    product.media.push({
        type: 'video/mp4',
        url: await uploadToS3(video)
    });
});
```

---

## 🔐 Security Notes

### Image Validation
```python
# Always validate on backend
ALLOWED_TYPES = {'image/jpeg', 'image/png'}
MAX_SIZE = 10 * 1024 * 1024  # 10MB

if file.content_type not in ALLOWED_TYPES:
    raise HTTPException(400, "Invalid file type")

if len(await file.read()) > MAX_SIZE:
    raise HTTPException(400, "File too large")
```

### Effects Validation
```python
# Validate effects JSON
ALLOWED_EFFECTS = {
    'zoom', 'pan', 'rotation', 'perspective',
    'depth_of_field', 'motion_blur', 'chromatic_aberration'
}

def validate_effects(effects_dict):
    for key, value in effects_dict.items():
        if key not in ALLOWED_EFFECTS:
            raise ValueError(f"Invalid effect: {key}")
        if not isinstance(value, bool):
            raise ValueError(f"Effect value must be boolean")
    return effects_dict
```

---

**API Documentation Complete! Happy Integrating! 🚀**
