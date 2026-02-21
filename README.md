# Worthless-Tink-her-hack-4.0<p align="center">

  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# 🎬 AI 3D Product Video Generator 🎯

## Basic Details

### Team Name: [Worthless]

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

![Screenshot1](Add screenshot 1 here with proper name)
_Add caption explaining what this shows_

![Screenshot2](Add screenshot 2 here with proper name)
_Add caption explaining what this shows_

![Screenshot3](Add screenshot 3 here with proper name)
_Add caption explaining what this shows_

#### Diagrams

**System Architecture:**

![Architecture Diagram](docs/architecture.png)
_Explain your system architecture - components, data flow, tech stack interaction_

**Application Workflow:**

![Workflow](docs/workflow.png)
_Add caption explaining your workflow_

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

[Add more endpoints as needed...]

---

### For Mobile Apps: 
Not applicable

---


## Project Demo

### Video

[Add your demo video link here - YouTube, Google Drive, etc.]

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

- "Create a FastAPI endpoint for video generation"
-"Implement 3D perspective transform using OpenCV"
--"Optimize MoviePy encoding performance"

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
