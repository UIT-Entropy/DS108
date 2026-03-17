import csv
import json
from typing import List, Dict, Any
import os

def SaveCSV(rows: List[Dict[str, Any]], path: str):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
def SaveJSON(data: Any, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

#Đọc AppID đã có để tránh trùng lặp
def CheckAppid(path: str) -> set:
    if not os.path.exists(path) or os.path.getsize(path) == 0: 
        return set()
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {int(row["Appid"]) for row in reader if row.get("Appid")}
#chèn tiếp dữ liệu vào file csv
def AppendCSV(row: Dict[str, Any], path: str):
    ExistFile = os.path.isfile(path) and os.path.getsize(path) > 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not ExistFile:
            writer.writeheader()
        writer.writerow(row)