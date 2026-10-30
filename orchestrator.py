import json, os, time
from datetime import datetime
from agents.client_finder import run as find_clients
from agents.github_sourcer import search as find_candidates
from agents.email_sender import run_campaign

TRACKER = "tracker.csv"
LETTERS_DIR = "cover_letters"

def full_cycle():
    print(f"\n{'='*60}")
    print(f" ЦИКЛ: {datetime.now()}")
    print(f"{'='*60}")
    
    # Шаг 1: Найти клиентов
    print("\n[1/4] Поиск клиентов...")
    clients = find_clients()
    
    # Шаг 2: Для каждого клиента найти email и отправить
    print("\n[2/4] Рассылка...")
    total_sent = 0
    for c in clients[:5]:
        letter = os.path.join(LETTERS_DIR, "default.txt")
        if os.path.isfile(letter):
            sent = run_campaign(c.get("name", "Unknown"), c.get("domain", ""), letter)
            total_sent += sent
    
    # Шаг 3: Найти кандидатов (для будущих заказов)
    print("\n[3/4] Поиск кандидатов на GitHub...")
    find_candidates("python", "remote")
    
    print(f"\n[4/4] Цикл завершен. Отправлено: {total_sent}")
    print(f"{'='*60}\n")
    return total_sent

if __name__ == "__main__":
    print("🧠 TalentSourcing OS — Автономный оркестратор")
    print("Цикл каждые 12 часов. Ctrl+C для остановки.\n")
    full_cycle()
    while True:
        time.sleep(12 * 3600)
        full_cycle()
