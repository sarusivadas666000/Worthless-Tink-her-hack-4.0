from pathlib import Path
import os
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from config import FPS


def create_video_from_frames(frames_dir: Path, output_path: Path, fps: int = FPS) -> Path:
    """
    Create MP4 video from image sequence.
    
    Args:
        frames_dir: Directory containing ordered frame images
        output_path: Path for output MP4 file
        fps: Frames per second
    
    Returns:
        Path to created video file
    """
    # Get list of frame files in order
    frame_files = sorted([
        str(frames_dir / f) 
        for f in os.listdir(frames_dir) 
        if f.endswith(('.png', '.jpg', '.jpeg'))
    ])
    
    if not frame_files:
        raise FileNotFoundError(f"No image frames found in {frames_dir}")
    
    # Create video clip from image sequence
    clip = ImageSequenceClip(frame_files, fps=fps)
    
    # Write video file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clip.write_videofile(
        str(output_path),
        codec='libx264',
        audio=False,
        verbose=False,
        logger=None
    )
    
    clip.close()
    return output_path
