import requests, csv, os

def search(tech, location=""):
    q = f"language:{tech} location:{location}" if location else f"language:{tech}"
    r = requests.get("https://api.github.com/search/users", params={"q": q, "per_page": 30}, headers={"Accept": "application/vnd.github+json", "User-Agent": "TSOS"}, timeout=15)
    candidates = []
    if r.status_code == 200:
        for u in r.json().get("items", [])[:20]:
            d = requests.get(u.get("url"), headers={"Accept": "application/vnd.github+json"}, timeout=10)
            if d.status_code == 200:
                p = d.json()
                candidates.append({"login": p.get("login"), "name": p.get("name") or p.get("login"), "bio": p.get("bio") or "", "location": p.get("location") or "Remote", "repos": p.get("public_repos"), "url": p.get("html_url")})
    os.makedirs("candidates_db", exist_ok=True)
    with open(f"candidates_db/{tech}_candidates.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["login", "name", "bio", "location", "repos", "url"])
        w.writeheader(); w.writerows(candidates)
    print(f"✅ {len(candidates)} кандидатов ({tech}) сохранены")
    return candidates

if __name__ == "__main__":
    search("python", "remote")
