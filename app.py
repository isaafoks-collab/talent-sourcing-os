import streamlit as st
import os

st.set_page_config(page_title="TalentSourcing OS", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0e1117 0%, #161b22 100%); }
    h1, h2, h3 { color: #ffffff !important; font-family: "Inter", sans-serif; }
    .gradient-text {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .card:hover { transform: translateY(-2px); border-color: rgba(0, 201, 255, 0.3); }
    .metric-value { font-size: 2.2rem; font-weight: 700; color: #00C9FF; margin: 0; }
    .metric-label { font-size: 0.85rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 8px; }
    .stButton>button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #0e1117;
        font-weight: 800;
        border: none;
        border-radius: 10px;
        padding: 14px 28px;
        font-size: 1.1rem;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3);
    }
    .stButton>button:hover { opacity: 0.9; transform: scale(1.02); }
    section[data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #21262d; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🚀 TalentSourcing")
    st.markdown("---")
    st.page_link("app.py", label="📊 Dashboard", icon="📊")
    st.page_link("app.py", label="🤖 AI Agents", icon="🤖")
    st.page_link("app.py", label="📈 Pipeline", icon="📈")
    st.markdown("---")
    st.caption("v2.0 Premium Edition")

st.markdown('<div class="gradient-text">TalentSourcing Orchestrator</div>', unsafe_allow_html=True)
st.markdown("Автономная система алгоритмического поиска, скоринга и аутрича талантов.")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="card"><p class="metric-value">1,240</p><p class="metric-label">Candidates Sourced</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card"><p class="metric-value">84</p><p class="metric-label">Interviews Set</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card"><p class="metric-value">32%</p><p class="metric-label">Response Rate</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="card"><p class="metric-value">12</p><p class="metric-label">Active Agents</p></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("### ⚡ Управление оркестратором")
colA, colB = st.columns([2, 1])
with colA:
    st.markdown('<div class="card">Запуск полного цикла: <b>MarketScanner</b> → <b>Match Analyst</b> → <b>Application Writer</b>. Система работает асинхронно, соблюдая лимиты и протоколы безопасности.</div>', unsafe_allow_html=True)
with colB:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("▶️ ЗАПУСТИТЬ ОРКЕСТРАТОР"):
        st.success("Оркестратор активирован. Агенты начали работу в фоновом режиме.")

st.markdown("---")
st.caption("Powered by TalentSourcing OS | hello@techspendaudit.com")
