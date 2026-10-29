import streamlit as st, plotly.graph_objects as go, networkx as nx, json, os
from datetime import datetime

st.set_page_config(page_title="TalentSourcing OS", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600;700&display=swap');
*{font-family:'Rajdhani',sans-serif} h1,h2,h3{font-family:'Orbitron',sans-serif;color:#00ffff;text-shadow:0 0 10px #00ffff}
.cyber{background:linear-gradient(135deg,#0a0e27,#1a1f3a);border:2px solid #00ffff;border-radius:15px;padding:20px;margin:10px 0;box-shadow:0 0 20px rgba(0,255,255,.3)}
.agent{background:linear-gradient(135deg,#001f3f,#003366);border:2px solid #00ff88;border-radius:10px;padding:15px;margin:8px 0;color:#00ffff}
.cmd{background:#000;border:2px solid #00ffff;color:#00ff00;padding:12px;border-radius:10px;font-family:'Courier New',monospace}
.stButton>button{background:linear-gradient(135deg,#00ffff,#0088ff);color:#000;border-radius:10px;padding:10px 20px;border:none;font-weight:700;font-family:'Orbitron',sans-serif}
</style><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0a0e27">""",unsafe_allow_html=True)

if 'projects' not in st.session_state: 
    st.session_state.projects = {"TalentSourcing OS": {"agents": [
        {"name":"MarketScanner","role":"scanner","goal":"Мониторинг западных вакансий (hourly/contract)","status":"active"},
        {"name":"Match Analyst","role":"analyst","goal":"Проверка на red flags и оценку ставок","status":"active"},
        {"name":"Translator Officer","role":"translator","goal":"Двуязычный контур EN/RU + Критичные условия","status":"active"},
        {"name":"Application Writer","role":"writer","goal":"Генерация откликов без указания ставки","status":"active"},
        {"name":"CaseBuilder","role":"builder","goal":"Создание кейсов из открытых источников (X-Ray)","status":"active"},
        {"name":"Outreach Composer","role":"composer","goal":"Шаблоны аутрича и LinkedIn приглашений","status":"active"},
        {"name":"Data Steward","role":"steward","goal":"Ведение /pipeline, /memory, снапшоты, P-SCORE","status":"active"},
        {"name":"Ops & Compliance","role":"compliance","goal":"Инвойсы, лимит 2.4млн, чеки Мой налог","status":"active"},
        {"name":"Quality Gate","role":"gate","goal":"Финальная проверка перед отправкой (Уровень C)","status":"active"},
        {"name":"Scheduler","role":"scheduler","goal":"Follow-up через 48ч, еженедельные отчёты","status":"active"},
        {"name":"Market Intel","role":"intel","goal":"Анализ рыночных ставок сорсеров","status":"active"},
        {"name":"Risk Guard","role":"security","goal":"Блокировка скама, ToS-нарушений, VPN-схем","status":"active"}
    ], "tasks": [], "running": False, "created": datetime.now().isoformat(), "pscore": 0}}
if 'active' not in st.session_state: st.session_state.active = "TalentSourcing OS"
if 'logs' not in st.session_state: st.session_state.logs = [f"[{datetime.now():%H:%M:%S}] 🟢 Система инициализирована. Домен: techspendaudit.com (Reg.ru). Фокус: Прямые западные клиенты."]

def gp(n): return st.session_state.projects[n]

st.markdown('<div class="cyber" style="text-align:center;padding:30px"><h1 style="font-size:2.5em;margin:0">🎯 TalentSourcing OS</h1><p style="color:#888">MULTI-AGENT ORCHESTRATOR v1.0 | P-SCORE: ' + str(st.session_state.projects["TalentSourcing OS"]["pscore"]) + '</p></div>',unsafe_allow_html=True)

c1,c2=st.columns([1,3])
with c1:
    st.markdown('<div class="cyber"><h3>📁 ПРОЕКТЫ</h3></div>',unsafe_allow_html=True)
    for pn in st.session_state.projects:
        p=gp(pn); ia=st.session_state.active==pn
        if st.button(f"{'🟢' if p['running'] else '⚪'} {pn} ({len(p['agents'])} агентов)",key=f"p_{pn}",use_container_width=True,type="primary" if ia else "secondary"):
            st.session_state.active=pn; st.rerun()

with c2:
    pr=gp(st.session_state.active)
    st.markdown(f'<div class="cyber"><h3>🎯 {st.session_state.active}</h3></div>',unsafe_allow_html=True)
    cc1,cc2,cc3=st.columns(3)
    with cc1:
        if pr['running']:
            if st.button("⏹ СТОП",use_container_width=True):
                pr['running']=False; st.session_state.logs.append(f"[{datetime.now():%H:%M:%S}] 🔴 Оркестратор остановлен")
                st.rerun()
        else:
            if st.button("▶️ ЗАПУСТИТЬ ОРКЕСТРАТОР",type="primary",use_container_width=True):
                pr['running']=True; st.session_state.logs.append(f"[{datetime.now():%H:%M:%S}] 🟢 Оркестратор запущен. MarketScanner активирован.")
                st.rerun()
    with cc2: st.metric("Агентов онлайн", len(pr['agents']))
    with cc3: st.metric("Задач в работе", len(pr['tasks']))
    st.divider()
    t1,t2=st.tabs(["🤖 ШТАТ АГЕНТОВ", "📜 ЖУРНАЛ ОПЕРАЦИЙ"])
    with t1:
        cols = st.columns(3)
        for idx, ag in enumerate(pr['agents']):
            with cols[idx % 3]:
                st.markdown(f'<div class="agent"><b>{ag["name"]}</b><br><small>{ag["role"]}</small><br><i>{ag["goal"]}</i></div>',unsafe_allow_html=True)
    with t2:
        for l in reversed(st.session_state.logs[-50:]): 
            st.markdown(f'<div class="cmd">{l}</div>',unsafe_allow_html=True)
