from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

# Video settings
FPS = 24
FRAME_COUNT = 60  # Smooth transition frames
VIDEO_DURATION = FRAME_COUNT / FPS

# Image constraints
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}