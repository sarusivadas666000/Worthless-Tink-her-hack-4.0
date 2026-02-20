from pathlib import Path
import shutil
from fastapi import UploadFile


def create_directories(*dirs: Path) -> None:
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    with destination.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)


def cleanup_files(*paths: Path) -> None:
    for path in paths:
        if path.exists():
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path)