from pathlib import Path
from services.frame_generator import generate_transition_frames
from services.video_creator import create_video_from_frames


def process_images_to_video(
    img1_path: Path,
    img2_path: Path,
    temp_frame_dir: Path,
    output_video_path: Path
) -> Path:
    """
    Process two images and create a transition video.
    
    Args:
        img1_path: Path to initial product image
        img2_path: Path to final product image
        temp_frame_dir: Directory for temporary frame files
        output_video_path: Path for output video file
    
    Returns:
        Path to created video file
    """
    # Generate transition frames
    frames = generate_transition_frames(img1_path, img2_path, temp_frame_dir)
    
    # Create video from frames
    video_path = create_video_from_frames(temp_frame_dir, output_video_path)
    
    return video_path
