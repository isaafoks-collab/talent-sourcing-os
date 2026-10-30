import os

PROFILE_FILE = "profile.txt"
REPORT = "profile_report.md"

HEADLINE_KEYWORDS = ["sourcer", "sourcing", "recruiter", "recruiting", "talent", "boolean", "x-ray", "freelance", "remote", "contract"]
ABOUT_MIN_WORDS = 120
SKILLS_MIN = 15

def analyze(text):
    low = text.lower()
    gaps = []
    hits = [k for k in HEADLINE_KEYWORDS if k in low]
    if len(hits) < 4:
        gaps.append("HEADLINE: мало ключевых слов (" + str(len(hits)) + "/4). Заменить на готовый блок из LINKEDIN_PROFILE.md")
    words = len(text.split())
    if words < ABOUT_MIN_WORDS:
        gaps.append("ABOUT: " + str(words) + " слов, минимум " + str(ABOUT_MIN_WORDS) + ". Заменить на готовый блок")
    if "pilot" not in low and "hour" not in low and "$" not in low:
        gaps.append("ABOUT: нет коммерческого оффера (пилот, ставка). Добавить из готового блока")
    if text.count("|") < 2 and text.count("•") < 3:
        gaps.append("ФОРМАТ: нет структуры (разделители |, маркеры •). Применить готовый шаблон")
    return hits, gaps

def main():
    out = []
    out.append("# ОТЧЁТ АГЕНТА-ОПТИМИЗАТОРА LINKEDIN")
    out.append("")
    if os.path.isfile(PROFILE_FILE):
        with open(PROFILE_FILE, encoding="utf-8") as f:
            text = f.read()
        hits, gaps = analyze(text)
        out.append("## НАЙДЕНО КЛЮЧЕВЫХ СЛОВ: " + ", ".join(hits))
        out.append("")
        out.append("## ВЫЯВЛЕННЫЕ ПРОБЕЛЫ:")
        if gaps:
            for g in gaps:
                out.append("- " + g)
        else:
            out.append("- Критических пробелов не найдено")
        out.append("")
        out.append("## ДЕЙСТВИЕ: замени блоки профиля на готовые из LINKEDIN_PROFILE.md, затем пришли мне в чат текущий текст — верну финальную редактуру.")
    else:
        out.append("profile.txt не найден.")
        out.append("")
        out.append("## ДЕЙСТВИЕ (2 варианта):")
        out.append("1. Быстрый: скопируй готовые блоки из LINKEDIN_PROFILE.md в свой профиль LinkedIn как есть.")
        out.append("2. Точный: сохрани текущий текст профиля в profile.txt, запусти python linkedin_optimizer.py снова, затем пришли отчет мне в чат.")
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("\n".join(out))

main()
