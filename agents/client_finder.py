import requests, json, os, time
from datetime import datetime

def get_yc_companies():
    """Y Combinator — берем только те, что имеют job board"""
    try:
        r = requests.get("https://api.ycombinator.com/companies", timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            data = r.json()
            companies = []
            for c in data.get("companies", [])[:100]:
                # Берем компании с job board ИЛИ те, что в tech-секторе
                if c.get("isHiring") or c.get("tags") and any(t in str(c.get("tags")).lower() for t in ["saas", "ai", "b2b"]):
                    companies.append({
                        "name": c.get("name"),
                        "domain": c.get("domain") or c.get("name", "").lower().replace(" ", "") + ".com",
                        "url": c.get("url"),
                        "tags": ", ".join(c.get("tags", [])[:3]) if c.get("tags") else "tech",
                        "source": "YC"
                    })
            return companies[:20]
    except Exception as e:
        print(f"   YC Error: {e}")
    return []

def get_remoteok_jobs():
    """RemoteOK — ищем конкретно HR/Recruiter вакансии"""
    try:
        r = requests.get("https://remoteok.com/api", headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}, timeout=15)
        if r.status_code == 200:
            jobs = r.json()
            out = []
            for j in jobs:
                pos = str(j.get("position", "")).lower()
                company = j.get("company", "")
                # Ищем не только sourcer, но и компании которые нанимают много (значит им нужна помощь)
                if any(k in pos for k in ["sourcer", "recruiter", "talent", "hr", "hiring"]):
                    out.append({
                        "name": company,
                        "domain": company.lower().replace(" ", "").replace(",", "") + ".com",
                        "url": "https://remoteok.com" + str(j.get("url", "")),
                        "tags": pos,
                        "source": "RemoteOK"
                    })
                # Дополнительно: компании с пометкой "hiring multiple"
                elif "multiple" in str(j.get("tags", [])).lower():
                    out.append({
                        "name": company,
                        "domain": company.lower().replace(" ", "") + ".com",
                        "url": "https://remoteok.com" + str(j.get("url", "")),
                        "tags": "hiring_multiple",
                        "source": "RemoteOK"
                    })
            return out[:15]
    except Exception as e:
        print(f"   RemoteOK Error: {e}")
    return []

def get_wellfound_jobs():
    """Wellfound (AngelList) — стартапы"""
    try:
        # Используем публичный GraphQL endpoint или эмуляцию
        url = "https://wellfound.com/api/jobs"
        params = {"query": "talent sourcer OR recruiter OR hr manager", "page": 1}
        headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
        r = requests.get(url, params=params, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            jobs = []
            for j in data.get("jobs", [])[:20]:
                company = j.get("company_name", "Unknown")
                jobs.append({
                    "name": company,
                    "domain": company.lower().replace(" ", "") + ".com",
                    "url": f"https://wellfound.com{j.get('path', '')}",
                    "tags": j.get("title", ""),
                    "source": "Wellfound"
                })
            return jobs
    except Exception as e:
        print(f"   Wellfound Error: {e}")
    return []

def get_hardcoded_targets():
    """Резерв: проверенные компании которые всегда нанимают"""
    return [
        {"name": "Toptal", "domain": "toptal.com", "url": "https://toptal.com/careers", "tags": "freelance_platform", "source": "Hardcoded"},
        {"name": "Upwork", "domain": "upwork.com", "url": "https://upwork.com/careers", "tags": "freelance_platform", "source": "Hardcoded"},
        {"name": "GitLab", "domain": "gitlab.com", "url": "https://gitlab.com/groups/gitlab-org/-/jobs", "tags": "remote_first", "source": "Hardcoded"},
        {"name": "Automattic", "domain": "automattic.com", "url": "https://automattic.com/work-with-us", "tags": "wordpress", "source": "Hardcoded"},
        {"name": "Zapier", "domain": "zapier.com", "url": "https://zapier.com/jobs", "tags": "automation", "source": "Hardcoded"},
        {"name": "Buffer", "domain": "buffer.com", "url": "https://buffer.com/journey", "tags": "social_media", "source": "Hardcoded"},
        {"name": "InVision", "domain": "invisionapp.com", "url": "https://invisionapp.com/careers", "tags": "design", "source": "Hardcoded"},
        {"name": "Elastic", "domain": "elastic.co", "url": "https://elastic.co/about/hiring", "tags": "search", "source": "Hardcoded"},
    ]

def run():
    print(" Поиск клиентов (4 источника)...")
    
    # Источник 1: Y Combinator
    print("   [1/4] Y Combinator...")
    yc = get_yc_companies()
    print(f"       Найдено: {len(yc)}")
    time.sleep(1)
    
    # Источник 2: RemoteOK
    print("   [2/4] RemoteOK...")
    rok = get_remoteok_jobs()
    print(f"       Найдено: {len(rok)}")
    time.sleep(1)
    
    # Источник 3: Wellfound
    print("   [3/4] Wellfound...")
    wf = get_wellfound_jobs()
    print(f"       Найдено: {len(wf)}")
    time.sleep(1)
    
    # Источник 4: Hardcoded (всегда рабочие)
    print("   [4/4] Проверенные компании...")
    hc = get_hardcoded_targets()
    print(f"       Найдено: {len(hc)}")
    
    all_clients = yc + rok + wf + hc
    
    # Удаляем дубликаты по имени
    seen = set()
    unique_clients = []
    for c in all_clients:
        if c["name"] not in seen:
            seen.add(c["name"])
            unique_clients.append(c)
    
    print(f"\n✅ ВСЕГО найдено {len(unique_clients)} УНИКАЛЬНЫХ компаний")
    
    # Сохраняем
    with open("target_companies.json", "w", encoding="utf-8") as f:
        json.dump(unique_clients, f, indent=2, ensure_ascii=False)
    
    # Показываем первые 5
    print("\n📋 ТОП-5 для отправки:")
    for i, c in enumerate(unique_clients[:5], 1):
        print(f"   {i}. {c['name']} ({c['source']}) — {c['domain']}")
    
    return unique_clients

if __name__ == "__main__":
    run()
