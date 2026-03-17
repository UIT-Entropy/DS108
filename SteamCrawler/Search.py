import re
from typing import List
from bs4 import BeautifulSoup
from tqdm import tqdm
#Lấy AppID 
Search = "https://store.steampowered.com/search/results/"
class SearchService:
    def __init__(self, http):
        self.http = http
    def ParseAppid(self, html: str, limit: int) -> List[int]:
        soup = BeautifulSoup(html, "html.parser")
        seen = set()
        appids = []
        for a in soup.find_all("a", href=True):
            m = re.search(r"/app/(\d+)/", a["href"])
            if not m:
                continue
            appid = int(m.group(1))
            if appid in seen:
                continue
            seen.add(appid)
            appids.append(appid)
            if len(appids) >= limit:
                break
        return appids
    
    def FetchPage(self, cfg) -> List[int]:
        appids = []
        for idx in tqdm(range(cfg.pages), desc = "Đang Search"):
            start = idx * cfg.per_page
            params = {
                "supportedlang": cfg.lang,
                "ndl": 1,
                "infinite": 1,
                "start": start,
                "count": cfg.per_page,
                "cc": cfg.cc,
                "l": cfg.lang,
            }
            resp = self.http.get(Search, params)
            payload = resp.json()
            html = payload.get("results_html", "")
            Newids = self.ParseAppid(html, cfg.per_page)
            if not Newids:
                break
            appids.extend(Newids)
        return appids