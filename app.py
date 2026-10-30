import streamlit as st
import requests
import sqlite3
import csv
import os
import time
from datetime import datetime

st.set_page_config(page_title="TalentSourcing OS", layout="wide", page_icon="🧠")

DB = "talent_sourcing.db"
CSV_JOBS = "jobs_found.csv"
LETTERS_DIR = "cover_letters"

st.markdown("""
<style>
    .stApp {background-color: #050505; color: #e0e0e0;}
    .grid-bg {position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-image: linear-gradient(rgba(0, 255, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px); background-size: 40px 40px; z-index: -1; animation: moveGrid 10s linear infinite;}
    @keyframes moveGrid {0% {background-position: 0 0;} 100% {background-position: 40px 40px;}}
    .neural-node {position: fixed; width: 6px; height: 6px; background: #00ffff; border-radius: 50%; box-shadow: 0 0 10px #00ffff; z-index: -1; animation: pulse 2s ease-in-out infinite;}
    @keyframes pulse {0%, 100% {opacity: 0.3; transform: scale(1);} 50% {opacity: 1; transform: scale(1.5);}}
    .signal {position: fixed; width: 3px; height: 3px; background: #00ffff; border-radius: 50%; box-shadow: 0 0 8px #00ffff; z-index: -1; animation: signalMove 4s linear infinite;}
    @keyframes signalMove {0% {transform: translate(0, 0); opacity: 0;} 10% {opacity: 1;} 90% {opacity: 1;} 100% {transform: translate(300px, 150px); opacity: 0;}}
    .neon-title {text-align: center; font-size: 3rem; color: #00ffff; text-shadow: 0 0 15px #00ffff; font-family: monospace; margin-bottom: 10px;}
    .neon-card {background: rgba(0, 255, 255, 0.05); border: 1px solid #00ffff; border-radius: 8px; padding: 20px; text-align: center; box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);}
    .neon-text {color: #00ffff; font-size: 2.5rem; font-weight: bold; margin: 0;}
    .neon-label {color: #888; text-transform: uppercase; letter-spacing: 2px; margin-top: 5px;}
    .agent-row {background: rgba(0, 255, 0, 0.05); border-left: 3px solid #00ff00; padding: 15px; margin: 10px 0; color: #fff; font-family: monospace;}
    .terminal {background: #000; border: 2px solid #00ff00; border-radius: 8px; padding: 20px; font-family: 'Courier New', monospace; color: #00ff00; min-height: 300px; max-height: 500px; overflow-y: auto; font-size: 0.9rem;}
</style>
<div class="grid-bg"></div>
<div class="neural-node" style="top: 15%; left: 20%;"></div>
<div class="neural-node" style="top: 80%; left: 80%; animation-delay: 1s;"></div>
<div class="signal" style="top: 20%; left: 25%;"></div>
<div class="signal" style="top: 50%; left: 70%; animation-delay: 2s;"></div>
""", unsafe_allow_html=True)

def db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, company TEXT, location TEXT, salary TEXT, url TEXT, description TEXT, score INTEGER, created_at TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY AUTOINCREMENT, job_id INTEGER, letter TEXT, status TEXT, created_at TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, agent TEXT, msg TEXT)")
    conn.commit()
    return conn

def log(agent, msg):
    conn = db()
    conn.execute("INSERT INTO logs (ts, agent, msg) VALUES (?,?,?)", (datetime.now().strftime("%H:%M:%S"), agent, msg))
    conn.commit()
    conn.close()

def get_logs():
    conn = db()
    rows = conn.execute("SELECT ts, agent, msg FROM logs ORDER BY id DESC LIMIT 100").fetchall()
    conn.close()
    return rows

def scan_remoteok():
    try:
        r = requests.get("https://remoteok.com/api", headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        out = []
        if r.status_code == 200:
            for j in r.json():
                pos = str(j.get("position", "")).lower()
                if any(k in pos for k in ["sourcer", "recruiter", "talent", "hr", "hiring", "headhunter"]):
                    out.append({"title": j.get("position", "N/A"), "company": j.get("company", "N/A"), "location": j.get("location", "Remote"), "salary": str(j.get("salary", "N/A")), "url": "https://remoteok.com" + str(j.get("url", "")), "description": str(j.get("description", ""))[:300]})
        return out
    except Exception as e:
        log("MarketScanner", "RemoteOK ошибка: " + str(e))
        return []

def scan_remotive():
    try:
        r = requests.get("https://remotive.com/api/remote-jobs", params={"search": "recruiter sourcer hr"}, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        out = []
        if r.status_code == 200:
            for j in r.json().get("jobs", [])[:30]:
                out.append({"title": j.get("title", "N/A"), "company": j.get("company_name", "N/A"), "location": j.get("candidate_required_location", "Remote"), "salary": str(j.get("salary", "N/A")), "url": str(j.get("url", "")), "description": str(j.get("description", ""))[:300]})
        return out
    except Exception as e:
        log("MarketScanner", "Remotive ошибка: " + str(e))
        return []

def score(job):
    s = 50
    t = (str(job["title"]) + " " + str(job["description"])).lower()
    if "remote" in t: s += 15
    if any(k in t for k in ["freelance", "contract"]): s += 15
    if any(k in t for k in ["sourcer", "sourcing", "recruit"]): s += 10
    if job["salary"] not in ("", "N/A", "None"): s += 10
    return min(s, 100)

LETTER = """Subject: Freelance Talent Sourcing — {title} at {company}

Dear {company} Hiring Team,

I'm reaching out regarding the {title} opportunity. I'm a freelance talent sourcing researcher specializing in hard-to-find tech candidates through advanced Boolean and X-Ray search.

What I deliver:
- 15-20 validated candidate profiles per week
- Deep sourcing across LinkedIn, GitHub, Stack Overflow, niche communities
- Async workflow, UTC+3, flexible overlap with EU/US hours
- Clear deliverables, weekly reporting, no fluff

I propose a 20-hour paid pilot so you can evaluate quality risk-free. During the pilot I'll deliver a shortlist of pre-screened candidates matching your exact requirements.

Available to start immediately. Happy to jump on a quick call or continue async — whatever works for your team.

Best regards,
Andrey
Freelance Talent Sourcing Researcher
Email: hello@techspendaudit.com
Portfolio: techspendaudit.com"""

def gate(letter):
    problems = []
    words = len(letter.split())
    if words < 150 or words > 400:
        problems.append("длина " + str(words) + " слов")
    if "[" in letter and "]" in letter:
        problems.append("шаблонные скобки")
    return (len(problems) == 0), problems

def save_jobs(jobs):
    conn = db()
    seen = set(x[0] for x in conn.execute("SELECT url FROM jobs").fetchall())
    added = 0
    for j in jobs:
        if j["url"] not in seen:
            conn.execute("INSERT INTO jobs (title, company, location, salary, url, description, score, created_at) VALUES (?,?,?,?,?,?,?,?)", (j["title"], j["company"], j["location"], j["salary"], j["url"], j["description"], score(j), datetime.now().isoformat()))
            added += 1
    conn.commit()
    conn.close()
    return added

def top_jobs(n=10):
    conn = db()
    rows = conn.execute("SELECT id, title, company, location, salary, url, score FROM jobs ORDER BY score DESC LIMIT ?", (n,)).fetchall()
    conn.close()
    return rows

def run_cycle():
    log("ОРКЕСТРАТОР", "Запуск автономного цикла")
    jobs = scan_remoteok() + scan_remotive()
    log("MarketScanner", "Найдено вакансий: " + str(len(jobs)))
    added = save_jobs(jobs)
    log("MarketScanner", "Новых в базе: " + str(added))
    tops = top_jobs(10)
    log("Match Analyst", "Топ-10 отобран, лучший скоринг: " + (str(tops[0][6]) if tops else "0"))
    ok = 0
    os.makedirs(LETTERS_DIR, exist_ok=True)
    conn = db()
    for row in tops:
        letter = LETTER.format(title=row[1], company=row[2])
        passed, problems = gate(letter)
        status = "Ready" if passed else "Rejected"
        if passed:
            ok += 1
            safe = (str(row[2]) + "_" + str(row[1])[:30]).replace(" ", "_").replace("/", "_")
            with open(os.path.join(LETTERS_DIR, safe + ".txt"), "w", encoding="utf-8") as f:
                f.write(letter)
        conn.execute("INSERT INTO applications (job_id, letter, status, created_at) VALUES (?,?,?,?)", (row[0], letter, status, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    log("Quality Gate", "Пройдено валидацию: " + str(ok) + "/10")
    conn = db()
    rows = conn.execute("SELECT title, company, location, salary, url, score FROM jobs").fetchall()
    conn.close()
    with open(CSV_JOBS, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["title", "company", "location", "salary", "url", "score"])
        w.writerows(rows)
    log("ОРКЕСТРАТОР", "Цикл завершен. Экспорт в " + CSV_JOBS + " и " + LETTERS_DIR)

db()

st.markdown('<div class="neon-title">🧠 TalentSourcing OS</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; color:#00ff00; font-family:monospace; margin-bottom:30px;">⚡ АВТОНОМНЫЙ ОРКЕСТРАТОР АКТИВЕН ⚡</div>', unsafe_allow_html=True)

if st.button("🚀 АКТИВИРОВАТЬ ОРКЕСТРАТОР", use_container_width=True):
    run_cycle()
    st.rerun()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🤖 Агенты", "💬 Терминал", "📨 Отклики", "📡 Логи"])

with tab1:
    conn = db()
    nj = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    na = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    nr = conn.execute("SELECT COUNT(*) FROM applications WHERE status='Ready'").fetchone()[0]
    conn.close()
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown('<div class="neon-card"><div class="neon-text">' + str(nj) + '</div><div class="neon-label">Вакансий в базе</div></div>', unsafe_allow_html=True)
    c2.markdown('<div class="neon-card"><div class="neon-text">' + str(na) + '</div><div class="neon-label">Откликов</div></div>', unsafe_allow_html=True)
    c3.markdown('<div class="neon-card"><div class="neon-text">' + str(nr) + '</div><div class="neon-label">Готово к отправке</div></div>', unsafe_allow_html=True)
    c4.markdown('<div class="neon-card"><div class="neon-text">5</div><div class="neon-label">Агентов</div></div>', unsafe_allow_html=True)
    st.markdown("### Топ вакансий по скорингу")
    for row in top_jobs(20):
        st.markdown('<div class="agent-row"><b style="color:#00ffff">' + str(row[6]) + '/100</b> | ' + str(row[1]) + ' @ ' + str(row[2]) + ' | ' + str(row[3]) + ' | <a href="' + str(row[5]) + '" target="_blank" style="color:#00ffff;">открыть</a></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="agent-row">> <b style="color:#00ffff">MarketScanner</b> — парсинг RemoteOK, Remotive <span style="color:#00ff00; float:right;">[ONLINE]</span></div>', unsafe_allow_html=True)
    if st.button("🔍 Запустить MarketScanner"):
        jobs = scan_remoteok() + scan_remotive()
        log("MarketScanner", "Найдено: " + str(len(jobs)) + ", новых: " + str(save_jobs(jobs)))
        st.rerun()
    st.markdown('<div class="agent-row">> <b style="color:#00ffff">Match Analyst</b> — скоринг 0-100 <span style="color:#00ff00; float:right;">[ONLINE]</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-row">> <b style="color:#00ffff">Application Writer</b> — генерация откликов <span style="color:#00ff00; float:right;">[ONLINE]</span></div>', unsafe_allow_html=True)
    if st.button("✍️ Сгенерировать отклики для топ-10"):
        run_cycle()
        st.rerun()
    st.markdown('<div class="agent-row">> <b style="color:#00ffff">Quality Gate</b> — валидация 150-400 слов <span style="color:#00ff00; float:right;">[ONLINE]</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-row">> <b style="color:#00ffff">Translator Officer</b> — локализация RU <span style="color:#00ff00; float:right;">[ONLINE]</span></div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### Терминал управления")
    cmd = st.text_input("Команда:", placeholder="scan / analyze / apply / status / export / help / clear / reset")
    if st.button("Выполнить") and cmd:
        c = cmd.strip().lower()
        if c == "scan":
            jobs = scan_remoteok() + scan_remotive()
            log("MarketScanner", "Найдено: " + str(len(jobs)) + ", новых: " + str(save_jobs(jobs)))
            st.markdown('<div class="terminal">✅ Сканирование завершено. Найдено: ' + str(len(jobs)) + '</div>', unsafe_allow_html=True)
        elif c == "analyze":
            tops = top_jobs(10)
            st.markdown('<div class="terminal">📊 Топ-10:<br>' + '<br>'.join([str(r[6]) + '/100 ' + str(r[1]) + ' @ ' + str(r[2]) for r in tops]) + '</div>', unsafe_allow_html=True)
        elif c == "apply":
            run_cycle()
            st.markdown('<div class="terminal">✅ Отклики сгенерированы и провалидированы</div>', unsafe_allow_html=True)
        elif c == "status":
            conn = db()
            nj = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
            na = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
            conn.close()
            st.markdown('<div class="terminal">🟢 Все 5 агентов ONLINE<br>Вакансий: ' + str(nj) + '<br>Откликов: ' + str(na) + '</div>', unsafe_allow_html=True)
        elif c == "export":
            conn = db()
            rows = conn.execute("SELECT title, company, location, salary, url, score FROM jobs").fetchall()
            conn.close()
            data = "title,company,location,salary,url,score\n" + "\n".join([",".join([str(x) for x in r]) for r in rows])
            st.download_button("📥 Скачать jobs_found.csv", data, file_name="jobs_found.csv")
        elif c == "help":
            st.markdown('<div class="terminal">scan — парсинг<br>analyze — скоринг<br>apply — отклики<br>status — статус<br>export — CSV<br>clear — очистить логи<br>reset — сброс БД</div>', unsafe_allow_html=True)
        elif c == "clear":
            conn = db()
            conn.execute("DELETE FROM logs")
            conn.commit()
            conn.close()
            st.markdown('<div class="terminal">✅ Логи очищены</div>', unsafe_allow_html=True)
        elif c == "reset":
            conn = db()
            conn.execute("DELETE FROM jobs")
            conn.execute("DELETE FROM applications")
            conn.commit()
            conn.close()
            st.markdown('<div class="terminal">✅ База сброшена</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="terminal">❌ Неизвестная команда. Введите help</div>', unsafe_allow_html=True)

with tab4:
    conn = db()
    apps = conn.execute("SELECT id, job_id, letter, status FROM applications ORDER BY id DESC LIMIT 20").fetchall()
    conn.close()
    for a in apps:
        st.markdown("### Отклик #" + str(a[0]) + " — статус: " + str(a[3]))
        st.text_area("Текст:", a[2], height=250, key="app_" + str(a[0]))
        st.markdown("---")

with tab5:
    logs = get_logs()
    st.markdown('<div class="terminal">' + '<br>'.join(['[' + str(l[0]) + '] [' + str(l[1]) + '] ' + str(l[2]) for l in logs]) + '</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align: center; color: #555; font-family: monospace; font-size: 0.8rem;">TalentSourcing OS v3.0 | Autonomous Orchestrator | STRICT-EXECUTION</div>', unsafe_allow_html=True)
