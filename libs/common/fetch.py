import httpx
from tenacity import retry, wait_exponential, stop_after_attempt

HEADERS = {"User-Agent": "QSR-RegIntel/1.0 (+https://example.com/bot-policy)"}

@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(5))
def fetch_url(url: str) -> bytes:
    with httpx.Client(timeout=30, headers=HEADERS, follow_redirects=True) as c:
        r = c.get(url)
        if r.status_code == 404:
            # Return empty to allow pipeline to continue; discover may include alternates
            return b""
        r.raise_for_status()
        return r.content