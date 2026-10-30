import json, imaplib
cfg = json.load(open("email_config.json", encoding="utf-8"))
try:
    m = imaplib.IMAP4_SSL(cfg["imap"])
    m.login(cfg["email"], cfg["app_password"])
    print("ПОЧТА ПОДКЛЮЧЕНА: логин успешен")
    m.logout()
except Exception as e:
    print("ОШИБКА ВХОДА: " + str(e))
