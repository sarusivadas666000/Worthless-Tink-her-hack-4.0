from PIL import Image
from typing import List
from pathlib import Path
from backend.config import FRAME_COUNT


def generate_frames(
    img1_path: Path,
    img2_path: Path,
    output_dir: Path
) -> List[Path]:
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB").resize(img1.size)

    frame_paths = []

    for i in range(FRAME_COUNT):
        alpha = i / (FRAME_COUNT - 1)
        blended = Image.blend(img1, img2, alpha)

        frame_path = output_dir / f"frame_{i:03d}.jpg"
        blended.save(frame_path)
        frame_paths.append(frame_path)

    return frame_paths