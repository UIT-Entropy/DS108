import time
import requests
from typing import Dict, Any, Optional
from Config import Config
#Gửi request và retry nếu bị chặn  

class Client:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.session = requests.Session()

    def get(self, url: str, params: Dict[str, Any]) -> requests.Response:
        headers = {

            "User-Agent": "Mozilla/5.0 (SteamDataCollector/2.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        SteamError: Optional[Exception] = None
        for attempt in range(1, self.cfg.max_retries + 1):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.cfg.timeout_seconds,
                )
                response.raise_for_status()
                return response
                if response.status_code in [402,503]:
                    backoff - self.cfg.sleep_seconds*(5**attempt)
                    print(f"retry lần thứ {attempt} do lỗi: {e}")
                    time.sleep(backoff)
            #nếu gặp lỗi thì chờ 
            except Exception as e:
                SteamError = e
                backoff = self.cfg.sleep_seconds * (2 ** (attempt - 1))
                print(f"Retry lần thứ {attempt} do lỗi: {e}")
                time.sleep(backoff)
        raise RuntimeError(SteamError)