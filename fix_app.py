import io

# 1. Добавляем импорт и функцию
patch_code = """
import email_automation as ea

def run_auto():
    logs = ea.run_auto_campaign()
    return logs
"""

src = io.open("app.py", encoding="utf-8").read()

if "import email_automation" not in src:
    # Вставляем после импортов (после первой строки с import или в начало)
    idx = src.find("import ")
    if idx != -1:
        end_line = src.find("\n", idx)
        src = src[:end_line+1] + patch_code + src[end_line+1:]
    else:
        src = patch_code + src

# 2. Добавляем вкладку в конец файла
tab_code = """
st.markdown("---")
st.markdown("### 📧 Автоматическая рассылка откликов")
st.markdown("Система сама найдёт email компаний из tracker.csv, проверит валидность и отправит готовые письма.")
if st.button("🚀 ЗАПУСТИТЬ АВТО-РАССЫЛКУ", use_container_width=True, type="primary"):
    with st.spinner("Выполняю..."):
        logs = run_auto()
        st.markdown('<div class="terminal">' + '<br>'.join(logs) + '</div>', unsafe_allow_html=True)
"""

if "Автоматическая рассылка откликов" not in src:
    src = src + tab_code

io.open("app.py", "w", encoding="utf-8").write(src)
print("✅ Вкладка 'Авто-рассылка' успешно добавлена в app.py")
