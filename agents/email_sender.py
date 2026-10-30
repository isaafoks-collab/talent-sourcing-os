import requests, re, smtplib, json, os, csv, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

def find_emails(domain):
    urls = [f"https://{domain}", f"https://{domain}/contact", f"https://{domain}/about", f"https://{domain}/careers"]
    emails = set()
    for url in urls:
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8, verify=False)
            if r.status_code == 200:
                emails.update(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", r.text))
        except: pass
        time.sleep(0.8)
    return list(emails)

def send(to, subject, body):
    try:
        cfg = json.load(open("email_config.json", encoding="utf-8"))
        msg = MIMEMultipart(); msg["From"] = cfg["email"]; msg["To"] = to; msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        s = smtplib.SMTP_SSL("smtp.gmail.com", 465); s.login(cfg["email"], cfg["app_password"]); s.send_message(msg); s.quit()
        return True
    except Exception as e:
        print(f"Ошибка {to}: {e}")
        return False

def run_campaign(company, domain, letter_file):
    print(f"\n🔎 {company} ({domain})")
    emails = find_emails(domain)
    if not emails:
        emails = [f"hr@{domain}", f"talent@{domain}", f"careers@{domain}", f"contact@{domain}"]
    print(f"   Найдено: {len(emails)}")
    sent = 0
    if os.path.isfile(letter_file):
        with open(letter_file, encoding="utf-8") as f:
            content = f.read()
        subject = content.split("Subject:")[1].split("\n")[0].strip() if "Subject:" in content else f"Freelance Talent Sourcing — {company}"
        body = content.split("\n\n", 1)[1] if "\n\n" in content else content
        for e in emails[:3]:
            if send(e, subject, body):
                print(f"   ✓ Отправлено: {e}"); sent += 1
            time.sleep(1.5)
    print(f"   Итого: {sent}")
    return sent
