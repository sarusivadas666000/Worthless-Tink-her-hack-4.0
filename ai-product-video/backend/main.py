from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import uuid

from backend.config import UPLOAD_DIR, OUTPUT_DIR
from backend.utils.file_manager import (
    create_directories,
    save_upload_file,
    cleanup_files,
)
from backend.services.video_service import process_images_to_video

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

create_directories(UPLOAD_DIR, OUTPUT_DIR)


@app.post("/generate-video")
async def generate_video(
    initial_image: UploadFile = File(...),
    final_image: UploadFile = File(...)
):
    if initial_image.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid image type")

    job_id = uuid.uuid4().hex

    img1_path = UPLOAD_DIR / f"{job_id}_start.jpg"
    img2_path = UPLOAD_DIR / f"{job_id}_end.jpg"

    temp_frames = OUTPUT_DIR / f"{job_id}_frames"
    output_video = OUTPUT_DIR / f"{job_id}.mp4"

    create_directories(temp_frames)

    try:
        save_upload_file(initial_image, img1_path)
        save_upload_file(final_image, img2_path)

        video_path = process_images_to_video(
            img1_path, img2_path, temp_frames, output_video
        )

        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename="product_video.mp4"
        )

    finally:
        cleanup_files(img1_path, img2_path, temp_frames)