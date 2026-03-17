AppDetail = "https://store.steampowered.com/api/appdetails"

class AppDetails:
    def __init__(self, http, cfg):
        self.http = http
        self.cfg = cfg
    def fetch(self, appid: int) -> dict:
        params = {
            "appids": appid,
            "cc": self.cfg.cc,
            "l": self.cfg.lang,
        }
        resp = self.http.get(AppDetail, params)
        data = resp.json()
        entry = data.get(str(appid), {})
        if not entry.get("success"):
            return {"appid": appid, "success": False}
        return entry.get("data", {})