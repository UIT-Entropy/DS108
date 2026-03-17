import time
from Search import SearchService
from appDetails import AppDetails
from Extractor import Extract
from tagParser import ParseTag
from ReviewParser import ParseReview
from SystemParser import ParseSysReq
from tqdm import tqdm 
from Saving import CheckAppid, AppendCSV
AppStore = "https://store.steampowered.com/app/{appid}/"
class SteamCrawler:
    def __init__(self, http, cfg, CSVpath: str):
        self.cfg = cfg
        self.http = http
        self.search = SearchService(http)
        self.appdetails = AppDetails(http, cfg)
        self.CSVpath = CSVpath
    def crawl(self):
        Allappids = self.search.FetchPage(self.cfg)
        CrawledID = CheckAppid(self.CSVpath)
        appids = [appid for appid in Allappids if appid not in CrawledID]
        results = []
        for rank, appid in enumerate(tqdm(appids, desc = "Đang cào"), start=1):
            data = self.appdetails.fetch(appid)
            if not data:
                continue
            row = Extract(appid, data)
            resp = self.http.get(
                AppStore.format(appid=appid),
                {"cc": self.cfg.cc, "l": self.cfg.lang},
            )
            html = resp.text
            row["Tags"] = ParseTag(html)
            score, posi, nega = ParseReview(self.http, appid)
            row["ReviewScore"] = score
            row["PositiveReview"] = posi
            row["NegativeReview"] = nega
            OsReq, MemReq, CpuReq = ParseSysReq(html)
            row["OsRequirement"] = OsReq
            row["MemoryRequirement"] = MemReq
            row["CpuRequirement"] = CpuReq
            row["Rank"] = rank
            #Lưu vào csv luôn
            AppendCSV(row, self.CSVpath)
            #trả về list để chút lưu bằng json 
            results.append(row)
            time.sleep(self.cfg.sleep_seconds)
        return results
    

    

 