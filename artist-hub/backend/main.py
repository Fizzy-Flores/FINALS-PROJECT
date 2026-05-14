import os
import re
import uuid
import subprocess
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from firebase_admin import credentials, firestore, initialize_app, storage

load_dotenv()

SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
FIREBASE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")

if not SERVICE_ACCOUNT_PATH or not FIREBASE_BUCKET:
    raise RuntimeError(
        "Missing required environment variables. Set GOOGLE_APPLICATION_CREDENTIALS and FIREBASE_STORAGE_BUCKET."
    )

cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
initialize_app(cred, {"storageBucket": FIREBASE_BUCKET})

db = firestore.client()
app = FastAPI()


def get_tailscale_ip() -> str | None:
    """Return the IPv4 address assigned to tailscale0."""
    try:
        result = subprocess.check_output(["ip", "addr", "show", "tailscale0"], text=True)
        match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)/", result)
        return match.group(1) if match else None
    except subprocess.CalledProcessError:
        return None


@app.post("/upload-art")
async def upload_art(
    file: UploadFile = File(...),
    title: str = Form(...),
    price: float = Form(...),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File must have a filename.")

    bucket = storage.bucket()
    blob_name = f"artworks/{uuid.uuid4().hex}-{file.filename}"
    blob = bucket.blob(blob_name)

    blob.upload_from_file(file.file, content_type=file.content_type)
    blob.make_public()

    art_record = {
        "title": title,
        "price": price,
        "image_url": blob.public_url,
        "filename": file.filename,
        "uploaded_at": datetime.utcnow().isoformat() + "Z",
    }
    db.collection("artworks").add(art_record)

    return art_record


if __name__ == "__main__":
    import uvicorn

    host = get_tailscale_ip() or "0.0.0.0"
    uvicorn.run(app, host=host, port=8000)
