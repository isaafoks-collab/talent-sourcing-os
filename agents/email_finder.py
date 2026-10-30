import smtplib, dns.resolver, sys

PATTERNS = ["{f}@{d}", "{f}.{l}@{d}", "{f}{l}@{d}", "{f[0]}{l}@{d}", "{f}_{l}@{d}", "{f}-{l}@{d}", "hr@{d}", "talent@{d}", "recruiting@{d}", "careers@{d}", "jobs@{d}", "hiring@{d}", "contact@{d}", "info@{d}", "hello@{d}"]

def generate(first, last, domain):
    f, l = (first or "").lower(), (last or "").lower()
    return [p.format(f=f, l=l, d=domain) for p in PATTERNS]

def verify(email):
    try:
        domain = email.split("@")[1]
        mx = [str(r.exchange) for r in dns.resolver.resolve(domain, "MX")]
        if not mx: return False
        s = smtplib.SMTP(mx[0], timeout=5); s.helo("v"); s.mail("t@v.com"); code, _ = s.rcpt(email); s.quit()
        return code == 250
    except: return False

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        emails = generate(sys.argv[1], sys.argv[2], sys.argv[3])
        print(f"Сгенерировано {len(emails)} паттернов")
        for e in emails[:15]:
            print(f"  {'✓' if verify(e) else '✗'} {e}")
