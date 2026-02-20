from typing import List
from pathlib import Path
from moviepy.editor import ImageSequenceClip
from backend.config import FPS


def create_video(
    frame_paths: List[Path],
    output_video_path: Path
) -> Path:
    clip = ImageSequenceClip(
        [str(p) for p in frame_paths],
        fps=FPS
    )
    clip.write_videofile(
        str(output_video_path),
        codec="libx264",
        audio=False
    )
    return output_video_path