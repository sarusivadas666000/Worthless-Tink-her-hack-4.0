from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
import logging
import json

from config import UPLOAD_DIR, OUTPUT_DIR, ALLOWED_IMAGE_TYPES, DEFAULT_3D_EFFECTS
from utils.file_manager import (
    create_directories,
    save_upload_file,
    cleanup_files,
)
from services.video_service import process_images_to_video

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Product Video Generator 3D",
    description="Generate cinematic 3D transition videos between product images with camera effects",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create required directories
create_directories(UPLOAD_DIR, OUTPUT_DIR)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "AI Product Video Generator 3D",
        "features": ["3D perspective", "camera zoom", "camera pan", "motion blur"]
    }


@app.get("/effects")
async def get_available_effects():
    """Get available 3D effects."""
    return {
        "available_effects": DEFAULT_3D_EFFECTS,
        "description": {
            "zoom": "Camera zoom/dolly effect - moves forward and backward",
            "pan": "Camera pan effect - moves left/right/up/down",
            "rotation": "Full 3D rotation - spins the image",
            "perspective": "3D perspective tilt - tilts in 3D space",
            "depth_of_field": "Depth of field - focus blur effect",
            "motion_blur": "Cinematic motion blur - smooths motion",
            "chromatic_aberration": "RGB channel separation - sci-fi effect"
        }
    }


@app.post("/generate-video")
async def generate_video(
    initial_image: UploadFile = File(...),
    final_image: UploadFile = File(...),
    effects: str = Query(None, description="JSON string with effect settings"),
    provider: str = Query(None, description="Optional external provider: openai, runway, luma, pika, or external"),
    prompt: str = Query(None, description="Optional text prompt to guide external image->video generation")
):
    """
    Generate a cinematic 3D transition video between two product images.
    
    Args:
        initial_image: Initial product image (jpg/png)
        final_image: Final product image (jpg/png)
        effects: Optional JSON string with effect settings
                Example: {"zoom": true, "pan": true, "rotation": false}
    
    Returns:
        MP4 video file with 3D effects and camera movements
    """
    job_id = uuid.uuid4().hex
    logger.info(f"Processing 3D video generation job: {job_id}")
    
    try:
        # Validate image types
        if initial_image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid initial image type. Allowed: {ALLOWED_IMAGE_TYPES}"
            )
        
        if final_image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid final image type. Allowed: {ALLOWED_IMAGE_TYPES}"
            )
        
        # Parse effects from query parameter
        video_effects = DEFAULT_3D_EFFECTS.copy()
        if effects:
            try:
                custom_effects = json.loads(effects)
                video_effects.update(custom_effects)
                logger.info(f"Applied custom effects: {custom_effects}")
            except json.JSONDecodeError:
                logger.warning(f"Invalid effects JSON, using defaults")
        
        # Define paths
        img1_path = UPLOAD_DIR / f"{job_id}_start.jpg"
        img2_path = UPLOAD_DIR / f"{job_id}_end.jpg"
        temp_frames = OUTPUT_DIR / f"{job_id}_frames"
        output_video = OUTPUT_DIR / f"{job_id}.mp4"
        
        # Create frame directory
        create_directories(temp_frames)
        
        # Save uploaded files
        logger.info(f"Saving uploaded images for job {job_id}")
        await save_upload_file(initial_image, img1_path)
        await save_upload_file(final_image, img2_path)
        
        # If an external provider is requested, delegate generation
        if provider:
            logger.info(f"Generating video using external provider={provider} prompt={'present' if prompt else 'none'} for job {job_id}")
            video_path = process_images_to_video(
                img1_path, img2_path, temp_frames, output_video, effects=video_effects, provider=provider, prompt=prompt
            )
        else:
            # Generate video locally with 3D effects
            logger.info(f"Generating 3D video with effects: {list(video_effects.keys())} for job {job_id}")
            video_path = process_images_to_video(
                img1_path, img2_path, temp_frames, output_video, effects=video_effects
            )
        
        logger.info(f"3D Video generation completed for job {job_id}")
        
        # Return video file
        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename="product_video_3d.mp4"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")
    
    finally:
        # Cleanup temporary files
        logger.info(f"Cleaning up temporary files for job {job_id}")
        try:
            cleanup_files(img1_path, img2_path, temp_frames)
        except Exception as e:
            logger.warning(f"Error during cleanup for job {job_id}: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
