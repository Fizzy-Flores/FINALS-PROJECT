import os
import re
import uuid
import subprocess
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile


def load_project_env() -> None:
    root_env = Path.cwd() / ".env"
    project_root = Path(__file__).resolve().parents[2]
    creds_env = project_root / "CREDENTIALS" / "API" / ".env"

    env_path = root_env if root_env.exists() else creds_env
    if env_path.exists():
        load_dotenv(dotenv_path=str(env_path))
    else:
        print(
            f"Warning: no .env found. Checked {root_env} and {creds_env}."
            " Create one in the project root or CREDENTIALS/API/.env."
        )


load_project_env()

SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
FIREBASE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")

# Initialize Firebase only if credentials are provided
cred = None
db = None
if SERVICE_ACCOUNT_PATH and FIREBASE_BUCKET:
    try:
        from firebase_admin import credentials, firestore, initialize_app, storage
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        initialize_app(cred, {"storageBucket": FIREBASE_BUCKET})
        db = firestore.client()
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")
        cred = None
        db = None
else:
    print("Firebase credentials not provided. Running without Firebase.")

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "ARTIST HUB API is running", "firebase_enabled": db is not None}


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
    if not db:
        raise HTTPException(status_code=503, detail="Firebase not configured. Cannot upload art.")

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
    uvicorn.run(
        "main:app",
        host=host,
        port=8000,
        reload=True,
        reload_dirs=[str(Path(__file__).resolve().parent)],
    )
