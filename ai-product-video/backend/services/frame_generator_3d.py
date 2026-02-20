from pathlib import Path
import numpy as np
from PIL import Image
import cv2
from config import FRAME_COUNT


def apply_perspective_transform(image: np.ndarray, progress: float) -> np.ndarray:
    """
    Apply 3D perspective transform to image.
    Creates a tilting/rotating effect in 3D space.
    
    Args:
        image: Input image as numpy array
        progress: Animation progress (0.0 to 1.0)
    
    Returns:
        Transformed image
    """
    h, w = image.shape[:2]
    
    # Calculate rotation angles based on progress
    angle_x = 15 * np.sin(progress * np.pi * 2)  # Tilt up/down
    angle_y = 20 * np.cos(progress * np.pi * 2)  # Rotate left/right
    angle_z = 10 * np.sin(progress * np.pi)       # Spin
    
    # Create rotation matrices
    alpha = np.radians(angle_x)
    beta = np.radians(angle_y)
    gamma = np.radians(angle_z)
    
    # Combined rotation matrix (XYZ Euler angles)
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha), np.cos(alpha)]
    ])
    
    Ry = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])
    
    Rz = np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
    ])
    
    # Combine rotations
    R = Rz @ Ry @ Rx
    
    # Apply perspective affine transformation
    pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    
    # Calculate perspective points
    offset_x = 20 * np.sin(progress * np.pi * 2)
    offset_y = 15 * np.cos(progress * np.pi * 2)
    
    pts2 = np.float32([
        [offset_x, offset_y],
        [w - offset_x * 0.5, offset_y + 5],
        [offset_x * 0.5, h - offset_y],
        [w - offset_x, h - offset_y + 5]
    ])
    
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image, matrix, (w, h))
    
    return result


def apply_camera_zoom(image: np.ndarray, progress: float, zoom_range: float = 0.2) -> np.ndarray:
    """
    Apply zoom/dolly effect - camera moving forward/backward.
    
    Args:
        image: Input image
        progress: Animation progress (0.0 to 1.0)
        zoom_range: Maximum zoom amount (0.2 = 20%)
    
    Returns:
        Zoomed image
    """
    h, w = image.shape[:2]
    
    # Smooth zoom oscillation
    zoom = 1.0 + zoom_range * np.sin(progress * np.pi * 3)
    
    # Calculate new dimensions
    new_w = int(w / zoom)
    new_h = int(h / zoom)
    
    # Calculate center crop
    x_offset = (w - new_w) // 2
    y_offset = (h - new_h) // 2
    
    # Crop center region
    cropped = image[y_offset:y_offset + new_h, x_offset:x_offset + new_w]
    
    # Resize back to original size
    result = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
    
    return result


def apply_camera_pan(image: np.ndarray, progress: float, pan_amount: int = 30) -> np.ndarray:
    """
    Apply panning effect - camera moving left/right/up/down.
    
    Args:
        image: Input image
        progress: Animation progress (0.0 to 1.0)
        pan_amount: Maximum pixel amount to pan
    
    Returns:
        Panned image
    """
    h, w = image.shape[:2]
    
    # Calculate pan offsets
    pan_x = int(pan_amount * np.sin(progress * np.pi * 2))
    pan_y = int(pan_amount * np.cos(progress * np.pi * 2))
    
    # Create translation matrix
    matrix = np.float32([
        [1, 0, pan_x],
        [0, 1, pan_y]
    ])
    
    result = cv2.warpAffine(image, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)
    
    return result


def apply_rotation_3d(image: np.ndarray, progress: float) -> np.ndarray:
    """
    Apply smooth 3D rotation around multiple axes.
    
    Args:
        image: Input image
        progress: Animation progress (0.0 to 1.0)
    
    Returns:
        Rotated image
    """
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Multi-axis rotation
    angle = 360 * progress  # Full rotation
    scale = 1.0 + 0.1 * np.sin(progress * np.pi * 2)
    
    # Get rotation matrix
    matrix = cv2.getRotationMatrix2D(center, angle, scale)
    
    result = cv2.warpAffine(image, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)
    
    return result


def apply_depth_of_field(image: np.ndarray, progress: float) -> np.ndarray:
    """
    Apply depth of field effect with focal blur.
    
    Args:
        image: Input image
        progress: Animation progress (0.0 to 1.0)
    
    Returns:
        Image with DOF effect
    """
    h, w = image.shape[:2]
    
    # Create focus area mask
    mask = np.zeros((h, w), dtype=np.float32)
    center_x, center_y = w // 2, h // 2
    
    # Circular focus point that moves
    focus_x = int(center_x + 100 * np.sin(progress * np.pi * 2))
    focus_y = int(center_y + 100 * np.cos(progress * np.pi * 2))
    
    # Create gradient mask for smooth focus
    y, x = np.ogrid[:h, :w]
    dist = np.sqrt((x - focus_x)**2 + (y - focus_y)**2)
    mask = 1.0 - np.clip(dist / 200, 0, 1)
    
    # Apply selective blur
    blurred = cv2.GaussianBlur(image, (21, 21), 5)
    
    # Blend focused and blurred
    result = np.zeros_like(image, dtype=np.float32)
    for c in range(image.shape[2]):
        result[:, :, c] = image[:, :, c] * mask + blurred[:, :, c] * (1 - mask)
    
    return np.clip(result, 0, 255).astype(np.uint8)


def apply_motion_blur(image: np.ndarray, progress: float) -> np.ndarray:
    """
    Apply subtle motion blur for cinematic effect.
    
    Args:
        image: Input image
        progress: Animation progress (0.0 to 1.0)
    
    Returns:
        Image with motion blur
    """
    # Motion blur intensity varies with progress
    intensity = int(3 + 7 * abs(np.sin(progress * np.pi * 2)))
    
    if intensity > 1:
        # Create motion blur kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (intensity, intensity))
        result = cv2.filter2D(image, -1, kernel / kernel.sum())
    else:
        result = image
    
    return result


def apply_chromatic_aberration(image: np.ndarray, progress: float) -> np.ndarray:
    """
    Apply chromatic aberration (RGB channel separation) effect.
    
    Args:
        image: Input image
        progress: Animation progress (0.0 to 1.0)
    
    Returns:
        Image with chromatic aberration
    """
    h, w = image.shape[:2]
    
    # Shift amount increases and decreases
    shift = int(5 * abs(np.sin(progress * np.pi * 2)))
    
    if shift > 0:
        # Split channels
        r, g, b = cv2.split(image)
        
        # Shift red channel
        matrix_r = np.float32([[1, 0, shift], [0, 1, 0]])
        r = cv2.warpAffine(r, matrix_r, (w, h))
        
        # Shift blue channel
        matrix_b = np.float32([[1, 0, -shift], [0, 1, 0]])
        b = cv2.warpAffine(b, matrix_b, (w, h))
        
        result = cv2.merge([r, g, b])
    else:
        result = image
    
    return result


def generate_3d_transition_frames(
    image1_path: Path, 
    image2_path: Path, 
    output_dir: Path,
    effects: dict = None
) -> list[Path]:
    """
    Generate transition frames with 3D effects and camera movements.
    
    Args:
        image1_path: Path to initial image
        image2_path: Path to final image
        output_dir: Directory to save frames
        effects: Dictionary of effect settings
            {
                'zoom': bool,
                'pan': bool,
                'rotation': bool,
                'perspective': bool,
                'depth_of_field': bool,
                'motion_blur': bool,
                'chromatic_aberration': bool
            }
    
    Returns:
        List of paths to generated frames
    """
    # Default effects enabled
    if effects is None:
        effects = {
            'zoom': True,
            'pan': True,
            'rotation': False,
            'perspective': True,
            'depth_of_field': False,
            'motion_blur': True,
            'chromatic_aberration': False
        }
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load images
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)
    
    # Resize to same dimensions
    size = (1080, 1080)
    img1 = img1.resize(size, Image.Resampling.LANCZOS)
    img2 = img2.resize(size, Image.Resampling.LANCZOS)
    
    # Convert to OpenCV format (BGR)
    arr1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
    arr2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
    
    frame_paths = []
    
    for i in range(FRAME_COUNT):
        progress = i / (FRAME_COUNT - 1)
        
        # Start with blended base
        alpha = progress
        blended = cv2.addWeighted(arr1, 1 - alpha, arr2, alpha, 0).astype(np.uint8)
        
        # Apply 3D effects
        frame = blended.astype(np.uint8)
        
        if effects.get('perspective', True):
            frame = apply_perspective_transform(frame, progress)
        
        if effects.get('zoom', True):
            frame = apply_camera_zoom(frame, progress, zoom_range=0.15)
        
        if effects.get('pan', True):
            frame = apply_camera_pan(frame, progress, pan_amount=25)
        
        if effects.get('rotation', False):
            frame = apply_rotation_3d(frame, progress)
        
        if effects.get('motion_blur', True):
            frame = apply_motion_blur(frame, progress)
        
        if effects.get('depth_of_field', False):
            frame = apply_depth_of_field(frame, progress)
        
        if effects.get('chromatic_aberration', False):
            frame = apply_chromatic_aberration(frame, progress)
        
        # Convert back to RGB for PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        
        # Save frame
        frame_path = output_dir / f"frame_{i:04d}.png"
        frame_pil.save(frame_path)
        frame_paths.append(frame_path)
    
    return frame_paths
