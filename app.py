import streamlit as st
import time

st.set_page_config(page_title="TalentSourcing OS", page_icon="", layout="wide")

# Анимированная нейронная сеть на фоне
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: #000000;
        overflow: hidden;
    }
    
    .neural-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: radial-gradient(ellipse at center, #0a0e27 0%, #000000 100%);
    }
    
    .neural-bg::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridMove 20s linear infinite;
    }
    
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    .neural-node {
        position: absolute;
        width: 4px;
        height: 4px;
        background: #00ffff;
        border-radius: 50%;
        box-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.5); }
    }
    
    .signal {
        position: absolute;
        width: 2px;
        height: 2px;
        background: #00ffff;
        border-radius: 50%;
        box-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff;
        animation: signalMove 3s linear infinite;
    }
    
    @keyframes signalMove {
        0% { transform: translate(0, 0); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translate(200px, 100px); opacity: 0; }
    }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00ffff 0%, #ff00ff 50%, #00ffff 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease infinite;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
        margin: 2rem 0;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }
    
    .subtitle {
        text-align: center;
        color: #00ffff;
        font-size: 1.2rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 3rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff; }
        to { text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff; }
    }
    
    .agent-card {
        background: rgba(0, 255, 255, 0.05);
        border: 2px solid #00ffff;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .agent-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.1), transparent);
        animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
        0% { transform: translateX(-100%) translateY(-100%); }
        100% { transform: translateX(100%) translateY(100%); }
    }
    
    .agent-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.3);
        border-color: #ff00ff;
    }
    
    .agent-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #00ffff;
        margin-bottom: 10px;
    }
    
    .agent-status {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .status-online {
        background: rgba(0, 255, 0, 0.2);
        color: #00ff00;
        border: 1px solid #00ff00;
        animation: blink 1.5s ease-in-out infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .metric-box {
        background: rgba(0, 255, 255, 0.05);
        border: 2px solid #00ffff;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .metric-box::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        color: #00ffff;
        text-shadow: 0 0 20px #00ffff;
    }
    
    .metric-label {
        color: #888;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 10px;
    }
    
    .launch-button {
        background: linear-gradient(90deg, #00ffff 0%, #ff00ff 100%);
        color: #000;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.5rem;
        font-weight: 900;
        padding: 20px 60px;
        border: none;
        border-radius: 50px;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 3px;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
        transition: all 0.3s ease;
        animation: buttonPulse 2s ease-in-out infinite;
    }
    
    @keyframes buttonPulse {
        0%, 100% { box-shadow: 0 0 30px rgba(0, 255, 255, 0.5); }
        50% { box-shadow: 0 0 50px rgba(0, 255, 255, 0.8), 0 0 70px rgba(255, 0, 255, 0.5); }
    }
    
    .launch-button:hover {
        transform: scale(1.1);
        box-shadow: 0 0 50px rgba(0, 255, 255, 0.8);
    }
    
    .data-stream {
        font-family: 'Courier New', monospace;
        color: #00ff00;
        font-size: 0.9rem;
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid #00ff00;
        border-radius: 10px;
        padding: 15px;
        margin: 20px 0;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .stream-line {
        margin: 5px 0;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
</style>

<div class="neural-bg">
    <div class="neural-node" style="top: 10%; left: 20%;"></div>
    <div class="neural-node" style="top: 30%; left: 70%;"></div>
    <div class="neural-node" style="top: 60%; left: 40%;"></div>
    <div class="neural-node" style="top: 80%; left: 80%;"></div>
    <div class="signal" style="top: 10%; left: 20%;"></div>
    <div class="signal" style="top: 30%; left: 70%;"></div>
</div>
""", unsafe_allow_html=True)

# Заголовок
st.markdown('<div class="main-title">🧠 TalentSourcing OS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Multi-Agent Neural Orchestrator v2.0</div>', unsafe_allow_html=True)

# Метрики
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-box"><div class="metric-value">12</div><div class="metric-label">Агентов онлайн</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-box"><div class="metric-value">847</div><div class="metric-label">Кандидатов найдено</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-box"><div class="metric-value">156</div><div class="metric-label">Откликов отправлено</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-box"><div class="metric-value">23</div><div class="metric-label">Интервью назначено</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Кнопка запуска
st.markdown('<div style="text-align: center; margin: 3rem 0;">', unsafe_allow_html=True)
if st.button(" ЗАПУСТИТЬ ОРКЕСТРАТОР", key="launch"):
    st.markdown('<div style="text-align: center; color: #00ffff; font-size: 1.5rem; animation: glow 1s ease-in-out infinite;">🚀 ОРКЕСТРАТОР АКТИВИРОВАН</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Штат агентов
st.markdown("### 🤖 ШТАТ АГЕНТОВ", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

agents = [
    ("MarketScanner", "scanner", "Поиск вакансий"),
    ("Match Analyst", "analyst", "Анализ соответствия"),
    ("Translator Officer", "translator", "Перевод документов"),
    ("Application Writer", "writer", "Генерация откликов")
]

for i, (name, role, desc) in enumerate(agents):
    with [col1, col2, col3, col4][i]:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-name">{name}</div>
            <div style="color: #888; margin-bottom: 10px;">{desc}</div>
            <span class="agent-status status-online">● ONLINE</span>
        </div>
        """, unsafe_allow_html=True)

# Поток данных
st.markdown("### 📡 ПОТОК ДАННЫХ В РЕАЛЬНОМ ВРЕМЕНИ", unsafe_allow_html=True)
st.markdown("""
<div class="data-stream">
    <div class="stream-line">[14:23:01] MarketScanner: Найдено 15 новых вакансий на LinkedIn</div>
    <div class="stream-line">[14:23:05] Match Analyst: Проанализировано 47 профилей кандидатов</div>
    <div class="stream-line">[14:23:12] Application Writer: Сгенерировано 12 персонализированных откликов</div>
    <div class="stream-line">[14:23:18] Quality Gate: Проверено 8 откликов, 3 отправлены на доработку</div>
    <div class="stream-line">[14:23:25] Translator Officer: Переведено 5 документов EN→RU</div>
    <div class="stream-line" style="color: #00ffff;">[14:23:30] Система работает стабильно. Все агенты активны.</div>
</div>
""", unsafe_allow_html=True)

# Футер
st.markdown("---")
st.markdown('<div style="text-align: center; color: #00ffff; font-family: Orbitron;">Powered by Neural Network Technology | hello@techspendaudit.com</div>', unsafe_allow_html=True)
