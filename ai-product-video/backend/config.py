from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

# Video settings
FPS = 24
FRAME_COUNT = 120  # Smooth transition frames (5 seconds at 24 FPS)
VIDEO_DURATION = FRAME_COUNT / FPS

# Image constraints
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}

# 3D Effects (configurable per request)
DEFAULT_3D_EFFECTS = {
    "zoom": True,              # Camera zoom/dolly
    "pan": True,               # Camera pan left/right/up/down
    "rotation": False,         # Full 3D rotation
    "perspective": True,       # 3D perspective tilt
    "depth_of_field": False,   # Focus blur effect
    "motion_blur": True,       # Cinematic motion blur
    "chromatic_aberration": False  # RGB channel separation
}