from pathlib import Path
import shutil
from fastapi import UploadFile


def create_directories(*dirs: Path) -> None:
    """Create directories if they don't exist."""
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)


async def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """Save uploaded file to destination."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as buffer:
        content = await upload_file.read()
        buffer.write(content)


def cleanup_files(*paths: Path) -> None:
    """Delete files and directories."""
    for path in paths:
        if path.exists():
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path)


def file_exists(file_path: Path) -> bool:
    """Check if file exists."""
    return Path(file_path).exists()