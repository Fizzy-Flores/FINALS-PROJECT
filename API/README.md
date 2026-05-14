# API

A simple FastAPI application.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the API

Run the server with:
```
uvicorn app:app --reload
```

For Tailscale access, run with:
```
uvicorn app:app --host 0.0.0.0 --port 8000
```

The API will be available at http://127.0.0.1:8000 locally, and via Tailscale at http://100.75.71.126:8000

## Endpoints

- GET / : Returns {"Hello": "World"}
- GET /items/{item_id} : Returns item details

## Troubleshooting

- Ensure Python 3.8+ is installed.
- If port 8000 is in use, change it with --port option.