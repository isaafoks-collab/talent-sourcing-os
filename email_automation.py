import requests
import re
import smtplib
import json
import os
import csv
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def _get_bs4():
    from bs4 import BeautifulSoup
    return BeautifulSoup

EMAIL_CONFIG = "email_config.json"
EMAIL_PATTERNS = [
    "{first}@{domain}", "{first}.{last}@{domain}", "{first}{last}@{domain}",
    "f{last}@{domain}", "{first}_{last}@{domain}", "{first}-{last}@{domain}",
    "{first}{last_initial}@{domain}", "{first_initial}{last}@{domain}",
    "hr@{domain}", "careers@{domain}", "jobs@{domain}", "talent@{domain}",
    "recruiting@{domain}", "hiring@{domain}", "contact@{domain}", "info@{domain}",
]

def load_config():
    with open(EMAIL_CONFIG, encoding="utf-8") as f:
        return json.load(f)

def find_emails_on_website(domain):
    urls = [f"https://{domain}", f"https://{domain}/contact", f"https://{domain}/about",
            f"https://{domain}/careers", f"https://{domain}/team", f"https://www.{domain}/contact"]
    emails = set()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=8, verify=False)
            if r.status_code == 200:
                soup = _get_bs4()(r.text, "html.parser")
                found = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.get_text())
                emails.update(found)
        except:
            pass
        time.sleep(0.8)
    return list(emails)

def generate_possible_emails(first_name, last_name, domain):
    out = []
    first = (first_name or "").lower()
    last = (last_name or "").lower()
    for p in EMAIL_PATTERNS:
        out.append(p.format(first=first, last=last,
            first_initial=first[0] if first else "", last_initial=last[0] if last else "", domain=domain))
    return out

def verify_email(email):
    try:
        import dns.resolver
        domain = email.split("@")[1]
        mx = [str(r.exchange) for r in dns.resolver.resolve(domain, "MX")]
        if not mx:
            return False
        s = smtplib.SMTP(mx[0], timeout=8)
        s.helo("verify")
        s.mail("test@verify.com")
        code, _ = s.rcpt(email)
        s.quit()
        return code == 250
    except:
        return False

def send_email(to_email, subject, body):
    try:
        cfg = load_config()
        msg = MIMEMultipart()
        msg["From"] = cfg["email"]
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        s = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        s.login(cfg["email"], cfg["app_password"])
        s.send_message(msg)
        s.quit()
        return True, ""
    except Exception as e:
        return False, str(e)

def extract_domain(url):
    url = url.replace("https://", "").replace("http://", "").replace("www.", "")
    return url.split("/")[0].split("?")[0]

def auto_send_company(company, url, letter_file):
    domain = extract_domain(url)
    log = []
    log.append(f"🔎 {company} ({domain})")
    
    emails = find_emails_on_website(domain)
    log.append(f"   Найдено на сайте: {len(emails)}")
    
    if not emails:
        emails = generate_possible_emails("", "", domain)
        log.append(f"   Сгенерировано по паттернам: {len(emails)}")
    
    emails = list(set(emails))
    valid = []
    for e in emails[:15]:
        if verify_email(e):
            valid.append(e)
            log.append(f"   ✓ {e}")
        time.sleep(0.3)
    log.append(f"   Валидных: {len(valid)}")
    
    sent = 0
    if valid and os.path.isfile(letter_file):
        with open(letter_file, encoding="utf-8") as f:
            content = f.read()
        if "Subject:" in content:
            subject = content.split("Subject:")[1].split("\n")[0].strip()
            body = content.split("\n\n", 1)[1] if "\n\n" in content else content
        else:
            subject = f"Freelance Talent Sourcing — {company}"
            body = content
        for e in valid[:3]:
            ok, err = send_email(e, subject, body)
            if ok:
                sent += 1
                log.append(f"    Отправлено: {e}")
            else:
                log.append(f"   ✗ Ошибка {e}: {err[:60]}")
            time.sleep(1.5)
    log.append(f"   Итого отправлено: {sent}")
    return log, sent

def run_auto_campaign(progress_callback=None):
    tracker = "tracker.csv"
    if not os.path.isfile(tracker):
        return ["❌ tracker.csv не найден. Сначала запусти оркестратор."]
    
    rows = []
    with open(tracker, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    
    outbox = [r for r in rows if r.get("status", "").lower() in ("outbox", "")]
    if not outbox:
        return ["✅ Все отклики уже отправлены. Outbox пуст."]
    
    logs = [f"🚀 Запуск авто-рассылки. В очереди: {len(outbox)} компаний"]
    total_sent = 0
    
    for i, row in enumerate(outbox[:10], 1):
        company = row.get("company", "")
        url = row.get("url", "")
        letter = row.get("letter_file", "")
        letter_path = os.path.join("cover_letters", letter) if letter else ""
        
        logs.append(f"\n[{i}/10] Обработка: {company}")
        try:
            step_logs, sent = auto_send_company(company, url, letter_path)
            logs.extend(step_logs)
            total_sent += sent
            row["status"] = "Sent" if sent > 0 else "Failed"
            if progress_callback:
                progress_callback(i, 10, company, sent)
        except Exception as e:
            logs.append(f"   ✗ Ошибка: {str(e)[:100]}")
            row["status"] = "Error"
    
    with open(tracker, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else ["date","company","title","url","letter_file","status"])
        if rows:
            w.writeheader()
            w.writerows(rows)
    
    logs.append(f"\n✅ АВТО-РАССЫЛКА ЗАВЕРШЕНА. Отправлено: {total_sent}")
    return logs
