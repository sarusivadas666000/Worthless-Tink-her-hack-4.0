from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

VIDEO_DURATION = 5  # seconds
FPS = 24
FRAME_COUNT = VIDEO_DURATION * FPS