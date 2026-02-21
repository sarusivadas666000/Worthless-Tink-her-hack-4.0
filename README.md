# Worthless-Tink-her-hack-4.0<p align="center">

  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# 🎬 AI 3D Product Video Generator 🎯

## Basic Details

### Team Name: Worthless

### Team Members

- Member 1: Saru S - ICCS College of Engineering and Management, Mupliyam, Thrissur
- Member 2: STINY N S - ICCS College of Engineering and Management, Mupliyam, Thrissur

### Hosted Project Link

[mention your project hosted link here]

### Project Description

AI 3D Product Video Generator is a professional web application that creates cinematic 3D transition videos between two product images. It applies advanced camera movements, depth effects, motion blur, and perspective transformations to generate smooth, high-quality MP4 videos.

### The Problem statement

Creating engaging product promo videos requires advanced video editing skills, expensive software, and significant time. Small businesses and creators struggle to produce cinematic product transitions quickly and affordably.
### The Solution

How are you solving it?
Our application automates product video creation using AI-powered 3D transformations. Users upload two images, select cinematic effects, and the system generates a smooth 3D transition video with professional camera movements and visual effects.


---

## Technical Details

### Technologies/Components Used

**For Software:**

- Languages used: Python, JavaScript, HTML, CSS
-Frameworks used: FastAPI
-Libraries used: OpenCV, MoviePy, Pillow, NumPy
-Tools used: Uvicorn, VS Code, Virtual Environment (venv), Python HTTP Server

**For Hardware:**

- Main components: Not applicable (Software-only project)
- Specifications:Runs on Python 3.11+ system
- Tools required: System with moderate processing capability (GPU recommended)

---

## Features

List the key features of your project:

-3D Camera Effects: Zoom, Pan, Full Rotation, Perspective tilt

-Cinematic Enhancements: Motion Blur, Depth of Field, Chromatic Aberration

-Smooth Alpha Blending between product images

-60-frame transition at 24 FPS with H.264 MP4 output

-Drag & Drop image upload with live preview

-One-click video generation and download

---

## Implementation

### For Software:

#### Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
cd backend
pip install -r requirements.txt
```

#### Run

```bash
# Start Backend
cd backend
python -m uvicorn main:app --reload

# Start Frontend
cd frontend
python -m http.server 3000
```
Backend runs at: http://127.0.0.1:8000

Frontend runs at: http://127.0.0.1:3000


### For Hardware:

#### Components Required

Not applicable (Software-based system)

#### Circuit Setup

Not applicable

---

## Project Documentation

### For Software:

#### Screenshots (Add at least 3)

1.
<img width="1743" height="969" alt="Screenshot 2026-02-21 061802" src="https://github.com/user-attachments/assets/5eb53b2f-7d2d-4787-8533-48849de96279" />
Web Interface


2.
<img width="1232" height="919" alt="Screenshot 2026-02-21 061911" src="https://github.com/user-attachments/assets/30c8f2e5-b5d6-4c4c-9ffa-688cba6929ef" />
Uploading of photo


4.
_<img width="1284" height="969" alt="Screenshot 2026-02-21 062138" src="https://github.com/user-attachments/assets/c6b0de49-2ce9-4660-b041-33628ee48eef" />
Generating video


5.
<img width="1300" height="895" alt="Screenshot 2026-02-21 062214" src="https://github.com/user-attachments/assets/28cbfa6e-6c6d-4b5c-9358-07551924503c" />
Generated Video with Download option

#### Diagrams


**System Architecture:**

<img width="2816" height="1536" alt="systemarch" src="https://github.com/user-attachments/assets/6f6b2ec1-11f8-49ad-ac15-7bbdaef7109f" />
The AI 3D Product Video Generator follows a client–server architecture with a clearly separated frontend, backend processing pipeline, and local storage layer.

The system follows a client–server architecture where the frontend (HTML, CSS, and Vanilla JavaScript) handles user interaction and sends image data to the FastAPI backend via REST APIs. The backend orchestrates the processing pipeline by validating inputs, generating 60 transition frames using OpenCV, NumPy, and Pillow, and compiling them into an MP4 video using MoviePy (H.264 encoding). Temporary files are managed through a file manager module with automatic cleanup. The final 1080x1080 cinematic video is then returned to the user for preview and download.


**Application Workflow:**

<img width="2816" height="1536" alt="workdia" src="https://github.com/user-attachments/assets/4f9b186a-26bc-4ec4-948f-995b27eaf0f8" />

The workflow begins with the user uploading product images via the frontend interface. The client sends a multipart request to the FastAPI backend, which validates the inputs, generates 60 3D transition frames, and compiles them into an MP4 video. Finally, the server cleans up the temporary files and returns the downloadable video file to the user.

---

### For Hardware:

Not applicable

#### Schematic & Circuit

Not applicable

#### Build Photos

Not applicable

---

## Additional Documentation

### For Web Projects with Backend:

#### API Documentation

**Base URL:** `(http://127.0.0.1:8000)`

##### Endpoints

**GET /health**

- **Description:** Checks if backend service is running
- **Response:**

```json
{
  "status": "ok",
  "service": "AI Product Video Generator 3D",
  "features": ["3D perspective", "camera zoom", "camera pan", "motion blur"]
}
```

**GET /effects**

- **Description:** Returns available 3D effects with descriptions

 **POST /generate-video**
- **Description:** Generates cinematic 3D transition video
- **Content-Type:** multipart/form-data
- **Parameters:**
  - `initial_image` (File - JPG/PNG)
  - `final_image` (File - JPG/PNG)
  -  `effects` (JSON string - optional): [Description]
  -  
```json
{
  "zoom": true,
  "pan": true,
  "rotation": false,
  "perspective": true,
  "motion_blur": true
}
```

- **Response:** MP4 Video File

```json
{
  "status": "success",
  "message": "Operation completed"
}
```

---

### For Mobile Apps: 
Not applicable

---


## Project Demo

### Video


https://drive.google.com/file/d/1hnpqt7kXdEI8Amgvyg1oVIH7zGGI9FHf/view?usp=sharing

The demo showcases uploading two product images, selecting 3D cinematic effects, generating a transition video, and downloading the final MP4 output.

### Additional Demos

-Local deployment demo
-Backend API testing via browser/Postman

---

## AI Tools Used (Optional - For Transparency Bonus)

If you used AI tools during development, document them here for transparency:

**Tool Used:** ChatGPT

**Purpose:**

-Assistance in FastAPI structure setup

-Debugging OpenCV transformations

-Improving motion blur and depth of field logic

-Documentation formatting



**Key Prompts Used:**

-Create a FastAPI endpoint for video generation

-Implement 3D perspective transform using OpenCV

-Optimize MoviePy encoding performance"

**Percentage of AI-generated code:** 30–40%

**Human Contributions:**

-Core architecture design

-3D transformation logic implementation

-Frame generation pipeline

-Frontend UI and user interaction logic

-Performance optimization and testing


---

## Team Contributions

- Saru S: Backend development, 3D frame generation, video encoding integration
- STINY N S: Frontend development, UI design, API integration, testing & documentation

---

## License

This project is licensed under the MIT License – see the LICENSE file for details..

**Common License Options:**

- MIT License (Permissive, widely used)
- Apache 2.0 (Permissive with patent grant)
- GPL v3 (Copyleft, requires derivative works to be open source)

---

Made with ❤️ at TinkerHub
hi
