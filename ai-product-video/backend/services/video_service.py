from pathlib import Path
import os
from services.frame_generator_3d import generate_3d_transition_frames
from services.video_creator import create_video_from_frames
from config import DEFAULT_3D_EFFECTS
from fastapi import HTTPException
from services import providers


def _call_external_provider_api(provider: str, prompt: str, img1_path: Path, img2_path: Path, output_path: Path) -> Path:
    """Generic caller for external provider APIs.

    Requires two environment variables to be set for the provider:
      - {PROVIDER_UPPER}_API_URL  (endpoint URL)
      - {PROVIDER_UPPER}_API_KEY  (bearer API key)  (optional)

    The function posts multipart form-data with fields:
      - prompt (string)
      - initial_image (file)
      - final_image (file)

    The provider is expected to stream or return binary video/mp4 bytes.
    """
    try:
        import requests
    except Exception:
        raise RuntimeError("Missing dependency 'requests'. Install it with: pip install requests")

    prov = provider.upper()
    url = os.environ.get(f"{prov}_API_URL")
    api_key = os.environ.get(f"{prov}_API_KEY")

    if not url:
        raise HTTPException(status_code=400, detail=f"API URL for provider '{provider}' not configured. Set env {prov}_API_URL")

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    files = {
        "initial_image": open(img1_path, "rb"),
        "final_image": open(img2_path, "rb"),
    }

    data = {"prompt": prompt or ""}

    try:
        resp = requests.post(url, headers=headers, files=files, data=data, timeout=120)
    finally:
        # close files
        for f in files.values():
            try:
                f.close()
            except Exception:
                pass

    if resp.status_code != 200:
        # try to provide helpful message
        try:
            msg = resp.json()
        except Exception:
            msg = resp.text
        raise HTTPException(status_code=502, detail=f"Provider {provider} error: {msg}")

    content_type = resp.headers.get("Content-Type", "")
    if "video" in content_type or resp.content[:4] == b"\x00\x00\x00\x18":
        # write bytes to output
        with open(output_path, "wb") as out_f:
            out_f.write(resp.content)
        return output_path
    else:
        # provider returned JSON or something unexpected
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        raise HTTPException(status_code=502, detail=f"Provider {provider} returned unexpected response: {body}")


def process_images_to_video(
    img1_path: Path,
    img2_path: Path,
    temp_frame_dir: Path,
    output_video_path: Path,
    effects: dict = None,
    provider: str = None,
    prompt: str = None
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

    # If a provider is specified, delegate to external API
    if provider:
        # Provider may produce final mp4 directly
        return providers.call_provider(provider, prompt, img1_path, img2_path, output_video_path)

    # Generate transition frames with 3D effects
    frames = generate_3d_transition_frames(img1_path, img2_path, temp_frame_dir, effects)

    # Create video from frames
    video_path = create_video_from_frames(temp_frame_dir, output_video_path)

    return video_path

