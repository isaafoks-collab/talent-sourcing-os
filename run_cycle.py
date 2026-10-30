import os
import sys

print("🧠 TalentSourcing OS — Запуск полного автономного цикла...")
print("="*60)

try:
    import orchestrator
    orchestrator.full_cycle()
    print("\n✅ ЦИКЛ ЗАВЕРШЕН УСПЕШНО.")
    print("📂 Проверь папку 'candidates_db' (кандидаты) и 'target_companies.json' (клиенты).")
except Exception as e:
    print(f"\n❌ ОШИБКА ВЫПОЛНЕНИЯ: {e}")
    print("💡 Совет: выполни 'pip install requests beautifulsoup4 dnspython scikit-learn pandas'")
