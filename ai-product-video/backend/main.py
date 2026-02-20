from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
import logging

from config import UPLOAD_DIR, OUTPUT_DIR, ALLOWED_IMAGE_TYPES
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
    title="AI Product Video Generator",
    description="Generate smooth transition videos between product images",
    version="1.0.0"
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
    return {"status": "ok", "service": "AI Product Video Generator"}


@app.post("/generate-video")
async def generate_video(
    initial_image: UploadFile = File(...),
    final_image: UploadFile = File(...)
):
    """
    Generate a transition video between two product images.
    
    Args:
        initial_image: Initial product image (jpg/png)
        final_image: Final product image (jpg/png)
    
    Returns:
        MP4 video file with smooth transition
    """
    job_id = uuid.uuid4().hex
    logger.info(f"Processing video generation job: {job_id}")
    
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
        
        # Generate video
        logger.info(f"Generating video for job {job_id}")
        video_path = process_images_to_video(
            img1_path, img2_path, temp_frames, output_video
        )
        
        logger.info(f"Video generation completed for job {job_id}")
        
        # Return video file
        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename="product_video.mp4"
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
