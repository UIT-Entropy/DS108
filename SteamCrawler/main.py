from Config import Config
from Client import Client
from Crawler import SteamCrawler
from Saving import SaveCSV, SaveJSON

def main():
    cfg = Config(pages=1, per_page=3)
    http = Client(cfg)
    crawler = SteamCrawler(http, cfg)
    rows = crawler.crawl()
    SaveCSV(rows, f"SteamGames.csv")
    SaveJSON({"Games": rows}, f"SteamGames.json")

if __name__ == "__main__":
    main()