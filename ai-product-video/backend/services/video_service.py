from pathlib import Path
from services.frame_generator_3d import generate_3d_transition_frames
from services.video_creator import create_video_from_frames
from config import DEFAULT_3D_EFFECTS


def process_images_to_video(
    img1_path: Path,
    img2_path: Path,
    temp_frame_dir: Path,
    output_video_path: Path,
    effects: dict = None
) -> Path:
    """
    Process two images and create a 3D transition video.
    
    Args:
        img1_path: Path to initial product image
        img2_path: Path to final product image
        temp_frame_dir: Directory for temporary frame files
        output_video_path: Path for output video file
        effects: Dictionary of effect settings (optional)
    
    Returns:
        Path to created video file
    """
    # Use default effects if not provided
    if effects is None:
        effects = DEFAULT_3D_EFFECTS
    
    # Generate transition frames with 3D effects
    frames = generate_3d_transition_frames(img1_path, img2_path, temp_frame_dir, effects)
    
    # Create video from frames
    video_path = create_video_from_frames(temp_frame_dir, output_video_path)
    
    return video_path

