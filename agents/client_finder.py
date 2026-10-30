import requests, json, os
from datetime import datetime

def get_yc_companies():
    try:
        r = requests.get("https://api.ycombinator.com/companies", timeout=15)
        if r.status_code == 200:
            return [{"name": c.get("name"), "domain": c.get("domain"), "url": c.get("url"), "tags": ", ".join(c.get("tags", [])[:3]), "source": "YC"} for c in r.json().get("companies", [])[:50] if c.get("isHiring")]
    except: pass
    return []

def get_remoteok_jobs():
    try:
        r = requests.get("https://remoteok.com/api", headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if r.status_code == 200:
            out = []
            for j in r.json():
                pos = str(j.get("position", "")).lower()
                if any(k in pos for k in ["sourcer", "recruiter", "talent", "hr"]):
                    out.append({"name": j.get("company"), "domain": j.get("company", "").lower().replace(" ", "") + ".com", "url": "https://remoteok.com" + str(j.get("url", "")), "tags": pos, "source": "RemoteOK"})
            return out[:20]
    except: pass
    return []

def run():
    print("🔎 Поиск клиентов...")
    clients = get_yc_companies() + get_remoteok_jobs()
    print(f"✅ Найдено {len(clients)} компаний")
    with open("target_companies.json", "w", encoding="utf-8") as f:
        json.dump(clients, f, indent=2, ensure_ascii=False)
    return clients

if __name__ == "__main__":
    run()
