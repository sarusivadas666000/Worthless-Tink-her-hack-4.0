from pathlib import Path
from backend.ai.frame_interpolator import generate_frames
from backend.ai.video_generator import create_video


def process_images_to_video(
    img1_path: Path,
    img2_path: Path,
    temp_frame_dir: Path,
    output_video_path: Path
) -> Path:
    frames = generate_frames(img1_path, img2_path, temp_frame_dir)
    video_path = create_video(frames, output_video_path)
    return video_path