import re
from bs4 import BeautifulSoup
from typing import Optional, Tuple
def ParseReview(http, appid:int) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    url = f"https://store.steampowered.com/appreviews/{appid}"
    params = {
        "json": 1,
        "filter": "summary",
        "language": "english"
    }
    try:
        resp = http.get(url, params=params)
        if not resp:
            return None, None, None
        data = resp.json()
        if not data.get("success"):
            return None, None, None
        summary_data = data.get("query_summary", {})
        ReviewScore = summary_data.get("review_score")
        Positive = summary_data.get("total_positive")
        Negative = summary_data.get("total_negative")
        return ReviewScore, Positive, Negative
    except Exception:
        return None, None, None

