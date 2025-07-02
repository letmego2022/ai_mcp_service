import requests

def fetch_html_from_url(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return f"ERROR: {e}"
