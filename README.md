# ARTIST HUB

## How to run ARTIST HUB

Follow these exact steps to run the backend from `artist-hub/backend`.

### 1. Open a terminal in the backend folder

```bash
cd /home/xian-flores/new-project/artist-hub/backend
```

### 2. Create and activate the Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

> A local virtual environment has already been created at `artist-hub/backend/.venv` and the required packages are installed there.
> When you open the project in VS Code, it will use that interpreter automatically.

### 4. Create or update the `.env` file

Create a file named `.env` in the same folder with these values:

```env
GOOGLE_APPLICATION_CREDENTIALS=/home/xian-flores/.config/gcloud/application_default_credentials.json
FIREBASE_STORAGE_BUCKET=your-bucket-name.appspot.com
```

Replace `your-bucket-name.appspot.com` with the actual Firebase storage bucket name.

> The project will also load `.env` from `CREDENTIALS/API/.env` if a local backend `.env` is not present.

### 5. Start the backend

```bash
cd /home/xian-flores/new-project/artist-hub/backend
python main.py
```

For automatic reload during development, use:

```bash
cd /home/xian-flores/new-project/artist-hub/backend
./run_dev.sh
```

### 6. Run the website from the terminal

If your frontend is static HTML in `front end/index.html`, serve it locally from the project root:

```bash
cd /home/xian-flores/new-project/front\ end
python3 -m http.server 8080
```

Then open your browser at:

- `http://127.0.0.1:8080/`

The backend should be available at:

- `http://127.0.0.1:8000/`

This setup lets you test the frontend and backend without killing and rerunning the backend server every time.

If you want to run with Uvicorn directly, use:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 6. Confirm the server is running

Open your browser or use curl to verify:

```bash
curl http://127.0.0.1:8000/
```

You should see a valid response from the FastAPI app.

### 7. If using Tailscale

The app automatically tries to bind to the `tailscale0` IP address when started with `python main.py`.

If you need the Tailscale address manually, run:

```bash
ip addr show tailscale0
```

Look for the `inet` line and use that IP with port `8000`.

### Notes

- `main.py` uses Firebase credentials from `.env`
- `requirements.txt` installs all Python dependencies
- The endpoint to upload art is `POST /upload-art`

## Secure API client script

A root-level script named `api_client.py` is included for securely calling an API.

### How to use it

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and set your real API values:
   ```env
   API_BASE_URL=https://api.example.com
   API_KEY=your_api_key_here
   ```
3. Run the client:
   ```bash
   python api_client.py
   ```

### Security details

- No API key or credential is hardcoded in the code.
- Sensitive values are loaded from environment variables.
- `.env` is ignored by `.gitignore`, so secrets are not pushed to GitHub.
