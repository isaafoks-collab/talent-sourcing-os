import io

EFFECTS = '''st.markdown("""
<style>
    .grid-bg {position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-image: linear-gradient(rgba(0, 255, 255, 0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 255, 0.06) 1px, transparent 1px); background-size: 40px 40px; z-index: 0; pointer-events: none; animation: moveGrid 8s linear infinite;}
    @keyframes moveGrid {0% {background-position: 0 0;} 100% {background-position: 40px 40px;}}
    .neural-node {position: fixed; width: 7px; height: 7px; background: #00ffff; border-radius: 50%; box-shadow: 0 0 12px #00ffff, 0 0 24px #00ffff; z-index: 0; pointer-events: none; animation: pulseNode 2s ease-in-out infinite;}
    @keyframes pulseNode {0%, 100% {opacity: 0.25; transform: scale(1);} 50% {opacity: 1; transform: scale(1.6);}}
    .signal {position: fixed; width: 4px; height: 4px; background: #00ffff; border-radius: 50%; box-shadow: 0 0 10px #00ffff; z-index: 0; pointer-events: none; animation: signalMove 5s linear infinite;}
    @keyframes signalMove {0% {transform: translate(0, 0); opacity: 0;} 8% {opacity: 1;} 92% {opacity: 1;} 100% {transform: translate(45vw, 35vh); opacity: 0;}}
    .signal-red {background: #ff00ff; box-shadow: 0 0 10px #ff00ff; animation-duration: 7s; animation-delay: 2s;}
    .scanline {position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: repeating-linear-gradient(0deg, rgba(0, 0, 0, 0.15) 0px, rgba(0, 0, 0, 0.15) 1px, transparent 1px, transparent 3px); z-index: 1; pointer-events: none; opacity: 0.35;}
    .stApp {background-color: #050505;}
</style>
<div class="grid-bg"></div>
<div class="scanline"></div>
<div class="neural-node" style="top: 12%; left: 18%;"></div>
<div class="neural-node" style="top: 30%; left: 78%; animation-delay: 0.6s;"></div>
<div class="neural-node" style="top: 68%; left: 30%; animation-delay: 1.2s;"></div>
<div class="neural-node" style="top: 82%; left: 70%; animation-delay: 1.8s;"></div>
<div class="signal" style="top: 15%; left: 10%;"></div>
<div class="signal" style="top: 45%; left: 55%; animation-delay: 1.5s;"></div>
<div class="signal signal-red" style="top: 70%; left: 20%;"></div>
""", unsafe_allow_html=True)
'''

src = io.open("app.py", encoding="utf-8").read()
if "grid-bg" in src:
    print("PATCH: эффекты уже в app.py")
else:
    idx = src.find("set_page_config")
    if idx == -1:
        src = EFFECTS + src
    else:
        end = src.find("\n", idx)
        src = src[: end + 1] + "\n" + EFFECTS + "\n" + src[end + 1 :]
    io.open("app.py", "w", encoding="utf-8").write(src)
    print("PATCH: эффекты внедрены в рабочую базу")
