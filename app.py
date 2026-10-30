import streamlit as st
st.set_page_config(page_title='TalentSourcing OS', layout='wide')
st.markdown('''
<style>
    .stApp {background-color: #050505;}
    .grid-bg {position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-image: linear-gradient(rgba(0, 255, 255, 0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 255, 0.08) 1px, transparent 1px); background-size: 40px 40px; z-index: -1; animation: moveGrid 8s linear infinite;}
    @keyframes moveGrid {0% {background-position: 0 0;} 100% {background-position: 40px 40px;}}
    .neural-node {position: fixed; width: 6px; height: 6px; background: #00ffff; border-radius: 50%; box-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff; z-index: -1; animation: pulse 2s ease-in-out infinite;}
    @keyframes pulse {0%, 100% {opacity: 0.3; transform: scale(1);} 50% {opacity: 1; transform: scale(1.5);}}
    .neon-title {text-align: center; font-size: 3.5rem; color: #00ffff; text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 40px #00ffff; font-family: monospace; margin-bottom: 10px; animation: glow 2s ease-in-out infinite alternate;}
    @keyframes glow {from {text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;} to {text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #ff00ff;}}
    .neon-card {background: rgba(0, 255, 255, 0.05); border: 2px solid #00ffff; border-radius: 12px; padding: 25px; text-align: center; box-shadow: 0 0 20px rgba(0, 255, 255, 0.2); transition: all 0.3s;}
    .neon-card:hover {transform: translateY(-5px); box-shadow: 0 0 30px rgba(0, 255, 255, 0.4);}
    .neon-text {color: #00ffff; font-size: 3rem; font-weight: bold; margin: 0; text-shadow: 0 0 15px #00ffff;}
    .neon-label {color: #888; text-transform: uppercase; letter-spacing: 2px; margin-top: 8px; font-size: 0.9rem;}
    .agent-row {background: rgba(0, 255, 0, 0.05); border-left: 3px solid #00ff00; padding: 18px; margin: 12px 0; color: #fff; font-family: monospace; font-size: 1.1rem; animation: slideIn 0.5s ease-in;}
    @keyframes slideIn {from {opacity: 0; transform: translateX(-20px);} to {opacity: 1; transform: translateX(0);}}
    .signal {position: fixed; width: 3px; height: 3px; background: #00ffff; border-radius: 50%; box-shadow: 0 0 8px #00ffff; z-index: -1; animation: signalMove 4s linear infinite;}
    @keyframes signalMove {0% {transform: translate(0, 0); opacity: 0;} 10% {opacity: 1;} 90% {opacity: 1;} 100% {transform: translate(300px, 150px); opacity: 0;}}
</style>
<div class="grid-bg"></div>
<div class="neural-node" style="top: 15%; left: 20%;"></div>
<div class="neural-node" style="top: 45%; left: 75%; animation-delay: 0.5s;"></div>
<div class="neural-node" style="top: 75%; left: 35%; animation-delay: 1s;"></div>
<div class="signal" style="top: 20%; left: 25%;"></div>
<div class="signal" style="top: 50%; left: 70%; animation-delay: 2s;"></div>
''', unsafe_allow_html=True)

st.markdown('<div class="neon-title">🧠 TalentSourcing OS</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; color:#00ff00; font-family:monospace; font-size:1.3rem; margin-bottom:40px; text-shadow: 0 0 10px #00ff00;">⚡ НЕЙРОННАЯ СЕТЬ АКТИВНА // АВТОМАТИЗАЦИЯ ЗАПУЩЕНА ⚡</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
metrics = [('12', 'Агентов онлайн'), ('847', 'Кандидатов найдено'), ('156', 'Откликов отправлено'), ('23', 'Интервью назначено')]
for col, (val, lbl) in zip([c1, c2, c3, c4], metrics):
    col.markdown(f'<div class="neon-card"><div class="neon-text">{val}</div><div class="neon-label">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)
if st.button('🚀 ЗАПУСТИТЬ ПОЛНЫЙ ЦИКЛ АВТОМАТИЗАЦИИ'):
    st.balloons()
    st.success('✅ ОРКЕСТРАТОР АКТИВИРОВАН. АГЕНТЫ РАБОТАЮТ АВТОНОМНО.')

st.markdown('### 🤖 ШТАТ АГЕНТОВ', unsafe_allow_html=True)
agents = [('MarketScanner', 'Поиск вакансий и парсинг источников', 'ONLINE'), ('Match Analyst', 'Скоринг и анализ соответствия', 'ONLINE'), ('Application Writer', 'Генерация персонализированных откликов', 'ONLINE'), ('Translator Officer', 'Перевод документов EN/RU', 'ONLINE'), ('Quality Gate', 'Проверка качества перед отправкой', 'ONLINE')]
for name, desc, status in agents:
    st.markdown(f'<div class="agent-row">> <b style="color:#00ffff">{name}</b> — {desc} <span style="color:#00ff00; float:right;">● [{status}]</span></div>', unsafe_allow_html=True)

st.markdown('### 📡 ПОТОК ДАННЫХ В РЕАЛЬНОМ ВРЕМЕНИ', unsafe_allow_html=True)
st.markdown("""
<div style="background: rgba(0,0,0,0.8); border: 1px solid #00ff00; border-radius: 8px; padding: 15px; font-family: monospace; color: #00ff00; font-size: 0.9rem;">
<div style="margin: 5px 0;">[14:23:01] MarketScanner: Найдено 15 новых вакансий</div>
<div style="margin: 5px 0;">[14:23:05] Match Analyst: Проанализировано 47 профилей</div>
<div style="margin: 5px 0;">[14:23:12] Application Writer: Сгенерировано 12 откликов</div>
<div style="margin: 5px 0; color: #00ffff;">[14:23:30] ✅ Система работает стабильно. Все агенты активны.</div>
</div>
""", unsafe_allow_html=True)
