import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

if not API_BASE_URL or not API_KEY:
    raise RuntimeError(
        "Missing required environment variables. "
        "Create a .env file with API_BASE_URL and API_KEY."
    )


def build_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def build_url(path: str) -> str:
    return f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def call_api(endpoint: str, payload: dict | None = None) -> dict:
    url = build_url(endpoint)
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    method = "POST" if payload is not None else "GET"

    request = Request(url, data=body, headers=build_headers(), method=method)

    try:
        with urlopen(request, timeout=15) as response:
            response_text = response.read().decode("utf-8")
            return json.loads(response_text) if response_text else {}
    except HTTPError as exc:
        raise RuntimeError(
            f"API request failed: {exc.code} {exc.reason} - {exc.read().decode('utf-8', errors='ignore')}"
        )
    except URLError as exc:
        raise RuntimeError(f"Unable to reach API: {exc.reason}")


def main() -> None:
    example_payload = {"message": "hello from api_client"}
    result = call_api("status", example_payload)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
