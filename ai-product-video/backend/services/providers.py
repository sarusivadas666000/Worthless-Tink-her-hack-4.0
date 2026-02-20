"""Provider adapters for external image->video generation.

This module dispatches provider-specific calls. For now each adapter
uses a simple convention: look for an env var <PROVIDER>_API_URL and
optional <PROVIDER>_API_KEY. If present, POST multipart/form-data with
fields: prompt, initial_image, final_image. The endpoint is expected to
return binary MP4 bytes.

You can extend adapters here to implement provider-specific request
formats (OpenAI, Runway, Luma, Pika) when you have their exact API
specifications/SDKs.
"""
from pathlib import Path
import os
from fastapi import HTTPException

def _generic_post(url: str, api_key: str | None, prompt: str, img1_path: Path, img2_path: Path, output_path: Path) -> Path:
    try:
        import requests
    except Exception:
        raise RuntimeError("Missing dependency 'requests'. Install it with: pip install requests")

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
        for f in files.values():
            try:
                f.close()
            except Exception:
                pass

    if resp.status_code != 200:
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        raise HTTPException(status_code=502, detail=f"Provider error: {body}")

    content_type = resp.headers.get("Content-Type", "")
    if "video" in content_type or resp.content[:4] == b"\x00\x00\x00\x18":
        with open(output_path, "wb") as out_f:
            out_f.write(resp.content)
        return output_path
    else:
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        raise HTTPException(status_code=502, detail=f"Provider returned unexpected response: {body}")


def call_openai(prompt: str, img1_path: Path, img2_path: Path, output_path: Path) -> Path:
    # Default: use OPENAI_API_URL / OPENAI_API_KEY
    url = os.environ.get("OPENAI_API_URL")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not url:
        raise HTTPException(status_code=400, detail="OPENAI_API_URL not configured")
    return _generic_post(url, api_key, prompt, img1_path, img2_path, output_path)


def call_runway(prompt: str, img1_path: Path, img2_path: Path, output_path: Path) -> Path:
    url = os.environ.get("RUNWAY_API_URL")
    api_key = os.environ.get("RUNWAY_API_KEY")
    if not url:
        raise HTTPException(status_code=400, detail="RUNWAY_API_URL not configured")
    return _generic_post(url, api_key, prompt, img1_path, img2_path, output_path)


def _extract_id_or_url(resp_json: dict) -> str | None:
    # Helper to fetch common fields used by SDKs
    for key in ("id", "asset_id", "url", "upload_url", "location"):
        if key in resp_json:
            return resp_json[key]
    return None


def call_luma(prompt: str, img1_path: Path, img2_path: Path, output_path: Path) -> Path:
    """Luma adapter. Uses SDK-style flow when configured, otherwise falls
    back to a simple multipart POST to LUMA_API_URL.
    """
    url = os.environ.get("LUMA_API_URL")
    api_key = os.environ.get("LUMA_API_KEY")
    # SDK-style configuration detection
    sdk_mode = os.environ.get("LUMA_API_STYLE", "").strip().lower() == "sdk"
    upload_url = os.environ.get("LUMA_UPLOAD_URL")
    render_url = os.environ.get("LUMA_RENDER_URL")
    if sdk_mode or (upload_url and render_url):
        return call_luma_sdk(prompt, img1_path, img2_path, output_path)

    if not url:
        raise HTTPException(status_code=400, detail="LUMA_API_URL not configured")

    # Build optional options payload
    options = {}
    model = os.environ.get("LUMA_MODEL")
    params = os.environ.get("LUMA_PARAMS")
    if model:
        options["model"] = model
    if params:
        try:
            import json as _json
            options.update(_json.loads(params))
        except Exception:
            # If params isn't JSON, ignore but don't crash
            pass

    # Use generic POST but include 'options' as a JSON field if present
    try:
        import requests
    except Exception:
        raise RuntimeError("Missing dependency 'requests'. Install it with: pip install requests")

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    files = {
        "initial_image": open(img1_path, "rb"),
        "final_image": open(img2_path, "rb"),
    }

    data = {"prompt": prompt or ""}
    if options:
        try:
            import json as _json
            data["options"] = _json.dumps(options)
        except Exception:
            pass

    try:
        resp = requests.post(url, headers=headers, files=files, data=data, timeout=180)
    finally:
        for f in files.values():
            try:
                f.close()
            except Exception:
                pass

    if resp.status_code != 200:
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        raise HTTPException(status_code=502, detail=f"Luma API error: {body}")

    content_type = resp.headers.get("Content-Type", "")
    if "video" in content_type or resp.content[:4] == b"\x00\x00\x00\x18":
        with open(output_path, "wb") as out_f:
            out_f.write(resp.content)
        return output_path
    else:
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        raise HTTPException(status_code=502, detail=f"Luma returned unexpected response: {body}")


def call_luma_sdk(prompt: str, img1_path: Path, img2_path: Path, output_path: Path) -> Path:
    """SDK-style Luma flow (upload -> render -> poll -> download).

    Required env vars:
      - LUMA_UPLOAD_URL: endpoint to upload assets (returns asset id/url)
      - LUMA_RENDER_URL: endpoint to create render jobs
      - LUMA_API_KEY: bearer token (optional but recommended)

    Optional env vars:
      - LUMA_MODEL: model name to request
      - LUMA_RENDER_STATUS_URL: template for status check, e.g. {render_url}/{job_id}
      - LUMA_API_POLL_TIMEOUT: total seconds to wait (default 300)
      - LUMA_API_POLL_INTERVAL: seconds between polls (default 2)

    Notes: Exact Luma public API may differ; set the above env vars according to
    your Luma account docs. This adapter tries to follow common provider patterns.
    """
    try:
        import time
        import json as _json
        import requests
    except Exception:
        raise RuntimeError("Missing dependency 'requests' or stdlib modules")

    upload_url = os.environ.get("LUMA_UPLOAD_URL")
    render_url = os.environ.get("LUMA_RENDER_URL")
    api_key = os.environ.get("LUMA_API_KEY")

    if not upload_url or not render_url:
        raise HTTPException(status_code=400, detail="LUMA_UPLOAD_URL and LUMA_RENDER_URL must be configured for SDK mode")

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Upload initial image
    files = {"file": open(img1_path, "rb")}
    try:
        r1 = requests.post(upload_url, headers=headers, files=files, timeout=120)
    finally:
        files["file"].close()

    if r1.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Luma upload failed: {r1.text}")

    try:
        j1 = r1.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"Luma upload returned non-json: {r1.text}")

    asset1 = _extract_id_or_url(j1)
    if not asset1:
        raise HTTPException(status_code=502, detail=f"Luma upload response missing asset id/url: {j1}")

    # Upload final image
    files = {"file": open(img2_path, "rb")}
    try:
        r2 = requests.post(upload_url, headers=headers, files=files, timeout=120)
    finally:
        files["file"].close()

    if r2.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Luma upload failed: {r2.text}")

    try:
        j2 = r2.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"Luma upload returned non-json: {r2.text}")

    asset2 = _extract_id_or_url(j2)
    if not asset2:
        raise HTTPException(status_code=502, detail=f"Luma upload response missing asset id/url: {j2}")

    # Create render job
    body = {
        "prompt": prompt or "",
        "assets": [asset1, asset2]
    }
    model = os.environ.get("LUMA_MODEL")
    if model:
        body["model"] = model

    try:
        rr = requests.post(render_url, headers={**headers, "Content-Type": "application/json"}, json=body, timeout=120)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Luma render request failed: {e}")

    if rr.status_code not in (200, 201):
        raise HTTPException(status_code=502, detail=f"Luma render error: {rr.status_code} {rr.text}")

    try:
        jr = rr.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"Luma render returned non-json: {rr.text}")

    # Extract job id and optional result URL
    job_id = _extract_id_or_url(jr) or jr.get("job_id") or jr.get("id")
    # Some providers return immediate output url
    possible_output = _extract_id_or_url(jr) or jr.get("output_url") or jr.get("result_url")

    if possible_output and (isinstance(possible_output, str) and possible_output.startswith("http")):
        # download directly
        d = requests.get(possible_output, headers=headers, timeout=120)
        if d.status_code == 200:
            with open(output_path, "wb") as out_f:
                out_f.write(d.content)
            return output_path
        else:
            raise HTTPException(status_code=502, detail=f"Failed to download Luma output: {d.status_code}")

    if not job_id:
        raise HTTPException(status_code=502, detail=f"Luma render response missing job id: {jr}")

    # Poll for job completion
    poll_timeout = int(os.environ.get("LUMA_API_POLL_TIMEOUT", "300"))
    poll_interval = float(os.environ.get("LUMA_API_POLL_INTERVAL", "2"))
    status_url_template = os.environ.get("LUMA_RENDER_STATUS_URL") or (render_url.rstrip("/") + "/{job_id}")

    deadline = time.time() + poll_timeout
    while time.time() < deadline:
        try:
            status_url = status_url_template.format(job_id=job_id)
            s = requests.get(status_url, headers=headers, timeout=60)
        except Exception as e:
            time.sleep(poll_interval)
            continue

        if s.status_code != 200:
            time.sleep(poll_interval)
            continue

        try:
            js = s.json()
        except Exception:
            time.sleep(poll_interval)
            continue

        status = js.get("status") or js.get("state")
        if status and status.lower() in ("succeeded", "completed", "done"):
            # get output URL
            out_url = _extract_id_or_url(js) or js.get("output_url") or js.get("result_url") or js.get("video_url")
            if out_url:
                d = requests.get(out_url, headers=headers, timeout=120)
                if d.status_code == 200:
                    with open(output_path, "wb") as out_f:
                        out_f.write(d.content)
                    return output_path
                else:
                    raise HTTPException(status_code=502, detail=f"Failed to download Luma output: {d.status_code}")
            # sometimes result is embedded
            if "result" in js and isinstance(js["result"], (str, bytes)):
                data = js["result"]
                if isinstance(data, str) and data.startswith("http"):
                    d = requests.get(data, headers=headers, timeout=120)
                    if d.status_code == 200:
                        with open(output_path, "wb") as out_f:
                            out_f.write(d.content)
                        return output_path
            raise HTTPException(status_code=502, detail=f"Luma job succeeded but no downloadable output found: {js}")

        if status and status.lower() in ("failed", "error"):
            raise HTTPException(status_code=502, detail=f"Luma job failed: {js}")

        time.sleep(poll_interval)

    raise HTTPException(status_code=504, detail=f"Luma render timed out after {poll_timeout} seconds")


def call_pika(prompt: str, img1_path: Path, img2_path: Path, output_path: Path) -> Path:
    url = os.environ.get("PIKA_API_URL")
    api_key = os.environ.get("PIKA_API_KEY")
    if not url:
        raise HTTPException(status_code=400, detail="PIKA_API_URL not configured")
    return _generic_post(url, api_key, prompt, img1_path, img2_path, output_path)


def call_external(prompt: str, img1_path: Path, img2_path: Path, output_path: Path) -> Path:
    # Use EXTERNAL_API_URL / EXTERNAL_API_KEY for custom endpoints
    url = os.environ.get("EXTERNAL_API_URL")
    api_key = os.environ.get("EXTERNAL_API_KEY")
    if not url:
        raise HTTPException(status_code=400, detail="EXTERNAL_API_URL not configured")
    return _generic_post(url, api_key, prompt, img1_path, img2_path, output_path)


def call_provider(provider: str, prompt: str, img1_path: Path, img2_path: Path, output_path: Path) -> Path:
    p = (provider or "").strip().lower()
    if p == "openai":
        return call_openai(prompt, img1_path, img2_path, output_path)
    if p == "runway":
        return call_runway(prompt, img1_path, img2_path, output_path)
    if p == "luma":
        return call_luma(prompt, img1_path, img2_path, output_path)
    if p == "pika":
        return call_pika(prompt, img1_path, img2_path, output_path)
    if p in ("google", "gcp", "ai_studio", "ai-studio", "googleai"):
        return call_google(prompt, img1_path, img2_path, output_path)
    # fallback to generic external
    return call_external(prompt, img1_path, img2_path, output_path)


def call_google(prompt: str, img1_path: Path, img2_path: Path, output_path: Path) -> Path:
    """Adapter for Google AI Studio / Generative APIs.

    Preferred configuration:
      - Set `GOOGLE_AI_API_URL` to the model endpoint that accepts a JSON
        payload containing `prompt` and image data (base64).
      - Authentication via `GOOGLE_API_KEY` (simple) or
        `GOOGLE_APPLICATION_CREDENTIALS` service account JSON (recommended).

    This adapter will base64-encode the two images and POST a JSON body:
      {"prompt": ..., "images": [{"mime":..., "b64":...}, ...], "duration": seconds}

    The exact API path for Google AI Studio may vary; if your account uses
    a different contract, set `GOOGLE_AI_API_URL` to a proxy that translates
    our payload into the provider-specific shape.
    """
    try:
        import base64
        import json
        import requests
    except Exception:
        raise RuntimeError("Missing dependency 'requests' or stdlib modules")

    url = os.environ.get("GOOGLE_AI_API_URL")
    api_key = os.environ.get("GOOGLE_API_KEY")
    sa_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    project = os.environ.get("GOOGLE_AI_PROJECT")  # e.g. projects/191101875509
    model = os.environ.get("GOOGLE_AI_STUDIO_MODEL") or os.environ.get("GOOGLE_AI_MODEL")

    if not url:
        # try to construct a sensible default if project+model provided
        if project and model:
            url = f"https://generativelanguage.googleapis.com/v1beta2/{project}/models/{model}:generateVideo"
        else:
            raise HTTPException(status_code=400, detail="GOOGLE_AI_API_URL not configured and no project/model available")

    # Read and base64-encode images
    def _b64(path: Path):
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("ascii")

    img1_b64 = _b64(img1_path)
    img2_b64 = _b64(img2_path)

    payload = {
        "prompt": prompt or "",
        "images": [
            {"mime": "image/jpeg", "b64": img1_b64},
            {"mime": "image/jpeg", "b64": img2_b64},
        ],
        "duration": float(os.environ.get("GOOGLE_AI_VIDEO_DURATION", "5"))
    }

    headers = {"Content-Type": "application/json"}

    # Authentication: API key or service account
    if api_key:
        url = f"{url}?key={api_key}"
    else:
        # Use service account to obtain bearer token
        if not sa_path:
            raise HTTPException(status_code=400, detail="No GOOGLE_API_KEY or GOOGLE_APPLICATION_CREDENTIALS configured for Google provider")
        try:
            from google.oauth2 import service_account
            from google.auth.transport.requests import Request as GoogleRequest
            creds = service_account.Credentials.from_service_account_file(sa_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])
            creds.refresh(GoogleRequest())
            headers["Authorization"] = f"Bearer {creds.token}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to obtain Google credentials: {e}")

    # Post and expect binary video bytes in response
    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=300)
    if resp.status_code not in (200, 201):
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        raise HTTPException(status_code=502, detail=f"Google AI Studio error: {body}")

    # If the response is JSON and contains an output URL, download it
    content_type = resp.headers.get("Content-Type", "")
    if "application/json" in content_type:
        try:
            j = resp.json()
        except Exception:
            raise HTTPException(status_code=502, detail="Google returned invalid JSON")
        # try to find an output URL
        out = j.get("output_url") or j.get("result_url") or j.get("video_url")
        if out and isinstance(out, str) and out.startswith("http"):
            d = requests.get(out, timeout=120)
            if d.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(d.content)
                return output_path
            else:
                raise HTTPException(status_code=502, detail=f"Failed to download Google output: {d.status_code}")
        raise HTTPException(status_code=502, detail=f"Google returned JSON but no output URL: {j}")

    # Otherwise assume binary MP4 bytes
    with open(output_path, "wb") as out_f:
        out_f.write(resp.content)
    return output_path
