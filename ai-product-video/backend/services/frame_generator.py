from pathlib import Path
from PIL import Image
import numpy as np
from config import FRAME_COUNT


def generate_transition_frames(
    image1_path: Path, image2_path: Path, output_dir: Path
) -> list[Path]:
    """
    Generate smooth transition frames between two images.
    
    Args:
        image1_path: Path to initial image
        image2_path: Path to final image
        output_dir: Directory to save frames
    
    Returns:
        List of paths to generated frames
    """
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load images
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)
    
    # Resize to same dimensions
    size = (1080, 1080)  # Standard square for product videos
    img1 = img1.resize(size, Image.Resampling.LANCZOS)
    img2 = img2.resize(size, Image.Resampling.LANCZOS)
    
    # Convert to numpy arrays for blending
    arr1 = np.array(img1, dtype=np.float32)
    arr2 = np.array(img2, dtype=np.float32)
    
    # Generate frames
    frame_paths = []
    for i in range(FRAME_COUNT):
        # Calculate alpha blend value (0.0 to 1.0)
        alpha = i / (FRAME_COUNT - 1)
        
        # Blend frames
        blended = (1 - alpha) * arr1 + alpha * arr2
        blended = np.clip(blended, 0, 255).astype(np.uint8)
        
        # Convert back to PIL Image
        frame = Image.fromarray(blended)
        
        # Save frame
        frame_path = output_dir / f"frame_{i:04d}.png"
        frame.save(frame_path)
        frame_paths.append(frame_path)
    
    return frame_paths
