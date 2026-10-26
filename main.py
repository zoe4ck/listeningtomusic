import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import urllib.request
import json
import re
from html import escape


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="record hotel",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Noto+Serif+KR:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 55% 35%, #3b281d 0%, #24160f 42%, #120b08 78%, #0b0705 100%)
        !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

.main .block-container {
    padding-top: 0 !important;
    max-width: 1400px !important;
}

/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #170d09 0%, #120906 55%, #0d0705 100%) !important;
    border-right: 1px solid rgba(190,145,92,0.22);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 35px;
}

.sidebar-title {
    color: #d9a96f;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 24px;
    letter-spacing: 4px;
    text-align: center;
}

.sidebar-subtitle {
    color: #805c3d;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 12px;
    letter-spacing: 3px;
    text-align: center;
    margin-top: 7px;
    margin-bottom: 45px;
}

.sidebar-rule {
    width: 67px;
    height: 1px;
    background: #65452f;
    margin: 0 auto 18px auto;
}

[data-testid="stSidebar"] .stButton {
    margin: 0 !important;
}

[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    color: #9b704c !important;
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: 15px !important;
    letter-spacing: 4px !important;
    text-align: left !important;
    padding: 14px 12px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    color: #e1b67c !important;
    background: rgba(190,137,82,0.08) !important;
}

/* =========================================================
   COMMON BUTTON
   ========================================================= */

div[data-testid="stButton"] > button {
    min-height: 44px !important;
    width: 100% !important;
    padding: 0.55rem 1rem !important;
    line-height: 1.25 !important;
    white-space: normal !important;
    background: transparent !important;
    color: #d8ad79 !important;
    border: 1px solid rgba(190,145,92,0.5) !important;
    border-radius: 2px !important;
    font-family: "Cormorant Garamond", Georgia, serif !important;
    letter-spacing: 3px !important;
    transition: 0.25s ease !important;
}

div[data-testid="stButton"] > button:hover {
    background: rgba(197,145,88,0.08) !important;
    border-color: #d5a66c !important;
    color: #efd7b0 !important;
}

/* =========================================================
   MAIN
   ========================================================= */

.welcome-area {
    min-height: 82vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.welcome-small {
    color: #a6784c;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 14px;
    letter-spacing: 5px;
    margin-bottom: 18px;
}

.welcome-title {
    color: #dcae73;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: clamp(58px, 7vw, 100px);
    font-weight: 400;
    letter-spacing: 8px;
    line-height: 1;
}

.welcome-line {
    width: 110px;
    height: 1px;
    background: #9c7047;
    margin: 28px auto;
}

.welcome-description {
    color: #bda087;
    font-family: "Noto Serif KR", serif;
    font-size: 15px;
    line-height: 2;
    letter-spacing: 1px;
}

/* =========================================================
   LETTER
   ========================================================= */

.letter-wrap {
    min-height: 86vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 35px 20px;
}

.letter-paper {
    width: min(1080px, 90vw);
    min-height: 650px;
    box-sizing: border-box;
    padding: 72px 90px;
    background: radial-gradient(ellipse at center, #f7eedb 0%, #eee0c4 62%, #e2cfac 100%);
    border: 1px solid rgba(117,80,42,0.18);
    box-shadow: 0 20px 45px rgba(0,0,0,0.45);
    position: relative;
    color: #49382c;
}

.letter-paper:before {
    content: "";
    position: absolute;
    inset: 15px;
    border: 1px solid rgba(117,80,42,0.18);
    pointer-events: none;
}

.letter-date {
    color: #856344;
    text-align: right;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 14px;
    margin-bottom: 48px;
}

.letter-title {
    color: #49301f;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 34px;
    letter-spacing: 3px;
    margin-bottom: 38px;
}

.letter-body {
    color: #49382c;
    font-family: "Noto Serif KR", serif;
    font-size: 17px;
    line-height: 2.25;
    letter-spacing: 0.2px;
}

.letter-sign {
    color: #604531;
    text-align: right;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 17px;
    line-height: 1.9;
    margin-top: 45px;
}

/* =========================================================
   CHOICE
   ========================================================= */

.section-area {
    min-height: auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding-top: clamp(38px, 7vh, 76px);
    margin-bottom: 22px;
}

.section-title {
    color: #d5a56d;
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: 15px !important;
    letter-spacing: 2.2px !important;
    border-radius: 2px !important;
    box-shadow: none !important;
    transition: background .18s ease, border-color .18s ease, color .18s ease !important;
    margin-bottom: 12px;
}

.section-subtitle {
    color: #96765d;
    font-family: "Noto Serif KR", serif;
    font-size: 14px;
    letter-spacing: 2px;
    margin-bottom: 0;
    line-height: 1.15;
}

.choice-paper-button button {
    min-height: 95px !important;
    background: radial-gradient(ellipse at center, #fbf3e3 0%, #ead9b9 100%) !important;
    color: #4c3424 !important;
    border: 1px solid rgba(111,75,42,0.45) !important;
    border-radius: 2px !important;
    font-family: "Noto Serif KR", serif !important;
    font-size: 18px !important;
    letter-spacing: 3px !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.25) !important;
}

/* =========================================================
   ROOM SERVICE
   ========================================================= */

.room-service-container {
    width: min(1100px, 90vw);
    margin: 0 auto;
    padding-top: 45px;
}

.room-service-title {
    color: #d5a56d;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 48px;
    letter-spacing: 6px;
    text-align: center;
}

.room-service-subtitle {
    color: #96765d;
    font-family: "Noto Serif KR", serif;
    font-size: 14px;
    text-align: center;
    margin-top: 8px;
}

/* =========================================================
   RECORD PLAYER
   ========================================================= */

.record-stage {
    min-height: 470px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

.record-player {
    width: 370px;
    height: 370px;
    border-radius: 50%;
    background:
        repeating-radial-gradient(
            circle,
            #17110e 0px,
            #17110e 3px,
            #211813 4px,
            #211813 6px
        );
    box-shadow:
        0 0 0 10px rgba(47,31,22,0.75),
        0 25px 55px rgba(0,0,0,0.6);
    position: relative;
}

.record-player:before {
    content: "";
    position: absolute;
    inset: 28px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.06);
}

.record-label {
    width: 125px;
    height: 125px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background:
        radial-gradient(
            circle,
            #b98555 0%,
            #8f5e3b 48%,
            #6c412a 100%
        );
    box-shadow: 0 0 15px rgba(0,0,0,0.45);
}

.record-hole {
    width: 12px;
    height: 12px;
    background: #17110e;
    border-radius: 50%;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}

.record-ring {
    position: absolute;
    width: 92px;
    height: 92px;
    border-radius: 50%;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    border: 1px solid rgba(240,204,160,0.3);
}

.record-label-text {
    position: absolute;
    width: 100%;
    text-align: center;
    top: 31px;
    color: #ead1af;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 12px;
    letter-spacing: 2px;
}

.record-caption {
    text-align: center;
    color: #b99676;
    font-family: "Noto Serif KR", serif;
    margin-top: 15px;
}

/* =========================================================
   FIREPLACE
   ========================================================= */

.fireplace-container {
    width: min(1100px, 90vw);
    margin: 0 auto;
    padding-top: 40px;
}

.fireplace-title {
    color: #d5a56d;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 48px;
    letter-spacing: 6px;
    text-align: center;
}

.fireplace-subtitle {
    color: #96765d;
    font-family: "Noto Serif KR", serif;
    text-align: center;
    font-size: 14px;
    margin-top: 8px;
}

.fireplace {
    width: min(720px, 80vw);
    height: 350px;
    margin: 55px auto 25px auto;
    background:
        radial-gradient(
            ellipse at 50% 100%,
            #8a4424 0%,
            #542617 28%,
            #27130d 58%,
            #110a07 100%
        );
    border: 16px solid #3b261a;
    box-shadow:
        inset 0 0 40px rgba(0,0,0,0.7),
        0 25px 60px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}

.fire {
    position: absolute;
    bottom: 30px;
    left: 50%;
    width: 130px;
    height: 190px;
    transform: translateX(-50%);
    background:
        radial-gradient(
            ellipse at center bottom,
            #f2a34d 0%,
            #d8642f 35%,
            #7b2f1b 62%,
            transparent 72%
        );
    border-radius: 50% 50% 35% 35%;
    filter: blur(1px);
    animation: flame 1.4s infinite alternate ease-in-out;
}

.fire-small {
    position: absolute;
    bottom: 35px;
    left: 50%;
    width: 65px;
    height: 110px;
    transform: translateX(-50%);
    background:
        radial-gradient(
            ellipse at center bottom,
            #ffe0a3 0%,
            #f19a43 40%,
            #bd4825 70%,
            transparent 75%
        );
    border-radius: 50% 50% 35% 35%;
    animation: flameSmall 0.9s infinite alternate ease-in-out;
}

.wood {
    position: absolute;
    bottom: 27px;
    left: 50%;
    width: 210px;
    height: 22px;
    background: #24140e;
    transform: translateX(-50%) rotate(4deg);
    border-radius: 8px;
}

.wood.two {
    transform: translateX(-50%) rotate(-7deg);
}

@keyframes flame {
    from {
        transform: translateX(-50%) scaleY(0.95) rotate(-2deg);
    }
    to {
        transform: translateX(-50%) scaleY(1.08) rotate(2deg);
    }
}

@keyframes flameSmall {
    from {
        transform: translateX(-50%) scaleY(0.9);
    }
    to {
        transform: translateX(-50%) scaleY(1.1);
    }
}

.fireplace-note {
    text-align: center;
    color: #a17f63;
    font-family: "Noto Serif KR", serif;
    line-height: 2;
}

/* =========================================================
   SEARCH
   ========================================================= */

.listen-search {
    width: min(1000px, 90vw);
    margin: 30px auto 0 auto;
}

.result-title {
    color: #dca072;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 28px;
    letter-spacing: 3px;
    margin: 35px 0 15px 0;
}

.result-card {
    display: flex;
    gap: 20px;
    align-items: center;
    background: rgba(247,238,219,0.06);
    border: 1px solid rgba(199,157,109,0.25);
    padding: 18px;
    margin: 12px 0;
    border-radius: 4px;
}

.result-card img {
    width: 90px;
    height: 90px;
    object-fit: cover;
}

.result-name {
    color: #e0bd91;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 23px;
}

.result-meta {
    color: #a98a70;
    font-family: "Noto Serif KR", serif;
    font-size: 13px;
    line-height: 1.8;
}

.no-result {
    color: #9b7960;
    text-align: center;
    margin-top: 35px;
    font-family: "Noto Serif KR", serif;
    font-size: 15px;
    line-height: 2;
}

[data-testid="stTextInput"] input {
    background: #f3ead9 !important;
    color: #49382c !important;
    border: 1px solid #8d6746 !important;
    border-radius: 2px !important;
    font-family: "Noto Serif KR", serif !important;
}

[data-testid="stRadio"] label {
    color: #a98a70 !important;
}

/* =========================================================
   BACK BUTTON
   ========================================================= */

.back-button {
    margin-top: 20px;
}


/* =========================================================
   RECORD HOTEL POLISH PASS — layout + luxury cocktail styling
   Kept inside this single Python file; no separate HTML/CSS files.
   ========================================================= */
.main .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2.4rem !important;
}

/* Bring ROOM SERVICE buttons up, closer to the title and subtitle. */
.section-area {
    min-height: 0 !important;
    padding-top: clamp(30px, 5vh, 58px) !important;
    margin-bottom: 20px !important;
}
.section-title {
    font-size: clamp(36px, 4vw, 48px) !important;
    letter-spacing: 5px !important;
    line-height: 1.15 !important;
    margin: 0 0 10px !important;
}
.section-subtitle {
    margin: 0 !important;
    line-height: 1.8 !important;
    letter-spacing: 1px !important;
}
.section-area + div[data-testid="stHorizontalBlock"] {
    gap: 22px !important;
    max-width: 1060px;
    margin: 0 auto !important;
}
.section-area + div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
    min-height: 54px !important;
    font-size: 15px !important;
    letter-spacing: 3px !important;
    background: linear-gradient(135deg, rgba(111,72,43,.20), rgba(45,27,19,.55)) !important;
    border: 1px solid rgba(207,157,99,.48) !important;
    box-shadow: 0 8px 22px rgba(0,0,0,.13), inset 0 1px rgba(255,255,255,.025) !important;
}
.section-area + div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, rgba(156,99,57,.30), rgba(64,37,25,.72)) !important;
    transform: translateY(-1px);
}

/* MY ROOM check-in gate: centered, compact, and visually grouped. */
.auth-box {
    margin: 16px auto 8px !important;
    padding: 25px 30px !important;
    max-width: 520px !important;
    background: linear-gradient(145deg, rgba(247,238,219,.075), rgba(247,238,219,.025)) !important;
    border-color: rgba(199,157,109,.32) !important;
    box-shadow: 0 16px 38px rgba(0,0,0,.22) !important;
}
.auth-subtitle { margin: 5px 0 8px !important; }

/* Cocktail menu cards: editorial hotel-bar styling. */
.cocktail-header {
    padding: 18px 0 24px !important;
}
.cocktail-kicker {
    color: #a17b59 !important;
    font-size: 11px !important;
    letter-spacing: 4.5px !important;
}
.cocktail-title {
    font-size: clamp(40px, 5vw, 58px) !important;
    letter-spacing: 6px !important;
    text-shadow: 0 4px 24px rgba(219,151,91,.08);
}
.cocktail-subtitle {
    margin-top: 10px !important;
    color: #b79a80 !important;
    letter-spacing: .5px !important;
}
.order-slip {
    min-height: 355px !important;
    padding: 22px 15px 20px !important;
    border: 1px solid rgba(211,170,121,.34) !important;
    border-radius: 3px !important;
    background: linear-gradient(155deg, rgba(255,240,220,.075), rgba(54,34,24,.22) 54%, rgba(14,9,7,.28)) !important;
    box-shadow: 0 18px 42px rgba(0,0,0,.22), inset 0 1px rgba(255,255,255,.035) !important;
    transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
}
.order-slip:hover {
    transform: translateY(-3px);
    border-color: rgba(224,177,123,.65) !important;
    box-shadow: 0 23px 48px rgba(0,0,0,.3), 0 0 25px rgba(210,155,97,.055) !important;
}
.order-slip:before { inset: 8px !important; border-color: rgba(211,170,121,.14) !important; }
.slip-no { color: #997453 !important; letter-spacing: 2.5px !important; }
.slip-label { color: #f0d5b3 !important; font-size: 15px !important; margin-top: 12px !important; }
.slip-drink { color: #dfb17c !important; font-size: 14px !important; letter-spacing: 1.8px !important; }
.slip-desc { color: #b2957c !important; font-size: 11px !important; }
.order-slip div[data-testid="stButton"] > button { margin-top: 10px !important; }

/* Miniature glass composition. All decorative parts stay clipped inside the glass. */
.mini-drink { transform: scale(1.05); margin-top: 16px !important; margin-bottom: 8px !important; filter: drop-shadow(0 12px 12px rgba(0,0,0,.26)) !important; }
.mini-glass { backdrop-filter: blur(2px); box-shadow: inset 7px 0 13px rgba(255,255,255,.08), inset -7px 0 12px rgba(0,0,0,.08), 0 8px 18px rgba(0,0,0,.18) !important; }
.mini-rim { border-color: rgba(255,244,229,.82) !important; box-shadow: 0 0 8px rgba(255,255,255,.07) !important; }
.mini-pink .mini-glass {
    height: 58px !important; bottom: 37px !important; width: 88px !important; left: 12px !important;
    border-radius: 0 0 46px 46px !important;
    background: linear-gradient(90deg, rgba(255,255,255,.24), rgba(255,255,255,.025) 42%, rgba(255,255,255,.15)) !important;
}
.mini-pink .mini-liquid { background: linear-gradient(180deg,#ffdce6 0%,#f29db8 42%,#bd557d 100%) !important; box-shadow: inset 0 3px 8px rgba(255,255,255,.22); }
.mini-green .mini-liquid { background: linear-gradient(180deg,#d8ffc9 0%,#8fe4a0 35%,#3a9b65 100%) !important; }
.mini-orange .mini-liquid { background: linear-gradient(180deg,#ffe9ad 0%,#ffb84e 45%,#e96b20 100%) !important; }
.mini-navy .mini-liquid { background: linear-gradient(180deg,#91b4ec 0%,#4c669f 45%,#171e42 100%) !important; }
.mini-cocktail-olive { background: radial-gradient(circle at 30% 25%, #fff0bd, #c8a76a 52%, #78603b) !important; border: 1px solid rgba(255,255,255,.55); box-shadow: 0 0 0 3px rgba(255,255,255,.07), inset 2px 2px 4px rgba(255,255,255,.45) !important; }
.mini-pick { background: linear-gradient(#fff0c8,#c59b62) !important; }

/* Large cocktail scene: more glass-like reflections, restrained luxury colors. */
.drink-stage { min-height: 410px !important; padding: 0 0 8px !important; }
.drink-visual {
    height: 365px !important;
    filter: drop-shadow(0 20px 24px rgba(0,0,0,.24));
}
.glass {
    border-color: rgba(255,238,220,.7) !important;
    background: linear-gradient(90deg, rgba(255,255,255,.19), rgba(255,255,255,.025) 24%, rgba(255,255,255,.015) 70%, rgba(255,255,255,.14)) !important;
    box-shadow: 0 24px 50px rgba(0,0,0,.25), inset 9px 0 15px rgba(255,255,255,.08), inset -9px 0 15px rgba(0,0,0,.07) !important;
}
.glass .liquid { opacity: .96 !important; }
.glass-rim { border-color: rgba(255,245,231,.82) !important; box-shadow: 0 0 10px rgba(255,255,255,.1) !important; }
.glass-shine { background: linear-gradient(180deg, rgba(255,255,255,.34), rgba(255,255,255,.025)) !important; width: 10px !important; left: 20px !important; filter: blur(1.5px) !important; }
.drink-scene.pink .glass {
    width: 238px !important; height: 160px !important; margin-top: 35px !important;
    border-radius: 0 0 119px 119px !important;
    background: linear-gradient(90deg, rgba(255,255,255,.22), rgba(255,255,255,.02) 40%, rgba(255,255,255,.12)) !important;
}
.drink-scene.pink .liquid { background: linear-gradient(180deg,#ffdce6 0%,#f19ab6 35%,#c95c84 72%,#963b62 100%) !important; }
.drink-scene.green .glass { width: 170px !important; height: 255px !important; border-radius: 8px 8px 36px 36px !important; }
.drink-scene.green .liquid { background: linear-gradient(180deg,#d9ffc8 0%,#9ce7a3 28%,#57bf7c 68%,#2d8154 100%) !important; }
.drink-scene.orange .glass { width: 210px !important; height: 205px !important; border-radius: 12px 12px 54px 54px !important; }
.drink-scene.orange .liquid { background: linear-gradient(180deg,#fff0b9 0%,#ffd077 24%,#ff9e34 65%,#d9581b 100%) !important; }
.drink-scene.navy .glass { width: 218px !important; height: 200px !important; border-radius: 12px 12px 44px 44px !important; }
.drink-scene.navy .liquid { background: linear-gradient(180deg,#9ab8ef 0%,#526fae 28%,#2d3e75 62%,#11172f 100%) !important; }
/* Keep garnishes inside the glass boundary, including at full fill. */
.melon-ice-cream { top: 15px !important; width: 64px !important; height: 34px !important; }
.drink-straw { top: 18px !important; height: 62px !important; }
.drink-cherry { top: 24px !important; width: 15px !important; height: 15px !important; }
.orange-half.one { top: 18px !important; right: 8px !important; width: 54px !important; height: 32px !important; }
.orange-half.two { top: 56px !important; bottom: auto !important; left: 17px !important; width: 44px !important; height: 25px !important; }
.pink-olive { top: 18px !important; width: 20px !important; height: 20px !important; }
.pink-pick { top: 8px !important; height: 37px !important; }
.navy-garnish { top: 22px !important; left: 15px !important; width: 52px !important; }
.drink-name { margin-top: 34px !important; font-size: 17px !important; letter-spacing: 3.5px !important; }
.drink-state { color: #a98768 !important; letter-spacing: 2.5px !important; }
.concierge-card {
    border-radius: 3px !important;
    padding: 22px 24px !important;
    background: linear-gradient(145deg, rgba(255,240,220,.075), rgba(54,34,24,.18)) !important;
    border-color: rgba(211,170,121,.3) !important;
}
.concierge-title { font-size: 20px !important; line-height: 1.65 !important; }
.recommendation-title { font-size: 24px !important; letter-spacing: 3.5px !important; }

@media (max-width: 900px) {
    .section-area { padding-top: 28px !important; margin-bottom: 16px !important; }
    .section-area + div[data-testid="stHorizontalBlock"] { gap: 12px !important; }
    .cocktail-header { padding: 14px 0 18px !important; }
    .order-slip { min-height: 320px !important; }
    .drink-visual { transform: scale(.9); transform-origin: center top; margin-bottom: -18px; }
}
@media (max-width: 700px) {
    .section-title { font-size: 34px !important; letter-spacing: 3px !important; }
    .section-subtitle { padding: 0 14px; font-size: 12px !important; }
    .order-slip { min-height: 270px !important; }
    .drink-visual { transform: scale(.78); transform-origin: center top; margin-bottom: -48px; }
    .drink-name { margin-top: 10px !important; }
}

</style>

<style>
.record-selected-note {
    text-align: center;
    color: #b99676;
    font-family: "Noto Serif KR", serif;
    margin: 8px 0 20px 0;
    line-height: 1.8;
}
.room-record-card {
    background: rgba(247,238,219,0.055);
    border: 1px solid rgba(199,157,109,0.24);
    padding: 16px;
    margin: 12px 0;
    border-radius: 4px;
}
.room-record-card img {
    width: 86px;
    height: 86px;
    object-fit: cover;
    border: 1px solid rgba(199,157,109,0.25);
}
.room-record-title {
    color: #e0bd91;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 21px;
    letter-spacing: 2px;
}
.room-record-meta {
    color: #a98a70;
    font-family: "Noto Serif KR", serif;
    font-size: 13px;
    line-height: 1.8;
}
.auth-box {
    width: min(520px, 90vw);
    margin: 18px auto 0 auto;
    padding: 28px 34px;
    background: rgba(247,238,219,0.055);
    border: 1px solid rgba(199,157,109,0.28);
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
}
.auth-title {
    color: #d5a56d;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 42px;
    letter-spacing: 5px;
    text-align: center;
}
.auth-subtitle {
    color: #96765d;
    font-family: "Noto Serif KR", serif;
    text-align: center;
    margin: 8px 0 18px 0;
    line-height: 1.8;
}
.room-tabs {
    color: #c49a70;
    font-family: "Cormorant Garamond", Georgia, serif;
    letter-spacing: 3px;
    text-align: center;

    margin: 20px 0;
}

/* =========================================================
   COCKTAIL BAR
   ========================================================= */
.cocktail-header {
    width: min(1120px, 92vw);
    margin: 0 auto;
    padding: 34px 0 24px;
    text-align: center;
}
.cocktail-kicker {
    color:#806047;
    font-family:"Cormorant Garamond",Georgia,serif;
    letter-spacing:4px;
    font-size:12px;
    line-height:1.4;
}
.cocktail-title {
    color:#d5a56d;
    font-family:"Cormorant Garamond",Georgia,serif;
    font-size:56px;
    letter-spacing:7px;
    line-height:1.12;
    margin-top:12px;
    margin-bottom:0;
}
.cocktail-subtitle {
    color:#96765d;
    font-family:"Noto Serif KR",serif;
    font-size:14px;
    line-height:1.85;
    margin:16px auto 0;
    max-width:650px;
}
.order-slip {
    min-height:330px;
    padding:22px 18px 18px;
    border:1px solid rgba(199,157,109,.3);
    background:linear-gradient(180deg, rgba(247,238,219,.065), rgba(247,238,219,.025));
    position:relative;
    text-align:center;
    box-shadow:0 15px 35px rgba(0,0,0,.18);
    overflow:hidden;
}
.order-slip:before {
    content:"";
    position:absolute;
    inset:8px;
    border:1px dashed rgba(199,157,109,.16);
    pointer-events:none;
}
.slip-no {
    color:#806047;
    font-family:Georgia,serif;
    font-size:10px;
    letter-spacing:2px;
}
.slip-label {
    color:#e0bd91;
    font-family:"Noto Serif KR",serif;
    font-size:16px;
    line-height:1.5;
    margin-top:16px;
}
.slip-drink {
    color:#c49a70;
    font-family:"Cormorant Garamond",Georgia,serif;
    font-size:15px;
    letter-spacing:2px;
    margin-top:7px;
}
.slip-desc {
    color:#92735d;
    font-family:"Noto Serif KR",serif;
    font-size:11px;
    line-height:1.8;
    margin:8px auto 0;
    max-width:190px;
}
.mini-drink {
    position:relative;
    width:88px;
    height:112px;
    margin:18px auto 2px;
}
.mini-glass {
    position:absolute;
    left:12px;
    bottom:3px;
    width:64px;
    height:84px;
    border:1.5px solid rgba(240,228,211,.58);
    border-top:0;
    border-radius:5px 5px 19px 19px;
    overflow:hidden;
    background:linear-gradient(90deg, rgba(255,255,255,.10), rgba(255,255,255,.02), rgba(255,255,255,.08));
    box-shadow:0 10px 18px rgba(0,0,0,.22), inset 0 0 8px rgba(255,255,255,.06);
}
.mini-liquid {
    position:absolute;
    inset:auto 0 0 0;
    height:66%;
    opacity:.88;
}
.mini-pink .mini-liquid { background:linear-gradient(180deg,#da93aa,#a94f70); }
.mini-green .mini-liquid { background:linear-gradient(180deg,#84d38a,#49a968); }
.mini-orange .mini-liquid { background:linear-gradient(180deg,#ffc06a,#ef761b); }
.mini-navy .mini-liquid { background:linear-gradient(180deg,#4969a0,#1d274f); }
.mini-ice {
    position:absolute;
    width:19px;
    height:19px;
    border:1px solid rgba(255,255,255,.28);
    background:rgba(255,255,255,.13);
    transform:rotate(12deg);
}
.mini-ice.a { top:34px; left:12px; }
.mini-ice.b { top:42px; right:10px; transform:rotate(-14deg); }
.mini-scoop {
    position:absolute;
    z-index:4;
    left:24px;
    top:2px;
    width:42px;
    height:35px;
    border-radius:50%;
    background:radial-gradient(circle at 35% 28%, #fffdf2 0%, #fff3d3 55%, #e5d2aa 100%);
    box-shadow:0 5px 10px rgba(0,0,0,.2);
}
.mini-straw {
    position:absolute;
    z-index:5;
    right:20px;
    top:0;
    width:3px;
    height:58px;
    background:#e9a0a8;
    transform:rotate(16deg);
    transform-origin:bottom center;
    border-radius:3px;
}
.mini-cherry {
    position:absolute;
    z-index:6;
    left:18px;
    top:3px;
    width:10px;
    height:10px;
    border-radius:50%;
    background:#b63f4e;
    box-shadow:0 0 0 2px rgba(255,255,255,.12);
}
.mini-citrus {
    position:absolute;
    z-index:6;
    right:6px;
    top:8px;
    width:24px;
    height:24px;
    border-radius:50%;
    background:radial-gradient(circle, #ffe2a0 0 33%, #f5a33f 35% 72%, #fff0c9 74% 82%, #df7d20 84%);
}
.mini-moon {
    position:absolute;
    z-index:6;
    left:23px;
    top:20px;
    width:32px;
    height:32px;
    border-radius:50%;
    box-shadow:0 0 18px rgba(121,153,225,.55);
    background:radial-gradient(circle at 36% 30%, #96aedd, #334b83 58%, #1a2448 100%);
}
/* refined cocktail glass details */
.mini-drink { width:112px; height:138px; margin:14px auto 0; position:relative; filter:drop-shadow(0 10px 12px rgba(0,0,0,.22)); }
.mini-glass { position:absolute; left:18px; bottom:18px; width:76px; height:84px; border:1.5px solid rgba(245,232,213,.65); border-top:0; border-radius:7px 7px 24px 24px; overflow:hidden; background:linear-gradient(90deg,rgba(255,255,255,.16),rgba(255,255,255,.025),rgba(255,255,255,.12)); box-shadow:inset 8px 0 15px rgba(255,255,255,.06),inset -8px 0 12px rgba(0,0,0,.08); }
.mini-rim { position:absolute; z-index:10; left:18px; top:34px; width:76px; height:13px; border:1.5px solid rgba(245,232,213,.68); border-radius:50%; background:rgba(255,255,255,.035); }
.mini-liquid { position:absolute; left:0; right:0; bottom:0; opacity:.92; border-radius:0 0 20px 20px; }
.mini-stem { position:absolute; left:50%; bottom:7px; width:3px; height:22px; transform:translateX(-50%); background:rgba(235,218,192,.65); }
.mini-base { position:absolute; left:50%; bottom:1px; width:48px; height:7px; transform:translateX(-50%); border:1.5px solid rgba(235,218,192,.65); border-radius:50%; }
.mini-pink .mini-glass { height:62px; bottom:36px; width:84px; left:14px; border-radius:0 0 42px 42px; }
.mini-pink .mini-rim { width:84px; left:14px; top:32px; }
.mini-pink .mini-liquid { background:linear-gradient(180deg,#ffd0dc,#df779a 55%,#a8446b); }
.mini-green .mini-glass { height:92px; width:68px; left:22px; border-radius:5px 5px 22px 22px; }
.mini-green .mini-rim { width:68px; left:22px; top:25px; }
.mini-green .mini-liquid { background:linear-gradient(180deg,#b8f2a9,#62c976 55%,#2f9958); }
.mini-orange .mini-glass { height:72px; width:82px; left:15px; border-radius:7px 7px 28px 28px; }
.mini-orange .mini-rim { width:82px; left:15px; top:43px; }
.mini-orange .mini-liquid { background:linear-gradient(180deg,#ffd995,#ffac3b 48%,#ec7018); }
.mini-navy .mini-glass { height:70px; width:82px; left:15px; border-radius:8px 8px 25px 25px; }
.mini-navy .mini-rim { width:82px; left:15px; top:44px; }
.mini-navy .mini-liquid { background:linear-gradient(180deg,#6f91d2,#354d91 52%,#171f4d); }
.mini-scoop { position:absolute; z-index:20; left:29px; top:-9px; width:55px; height:39px; border-radius:50%; background:radial-gradient(circle at 34% 25%,#fffef7,#fff0cc 62%,#d9c394); box-shadow:0 5px 10px rgba(0,0,0,.24); }
.mini-cherry { position:absolute; z-index:22; left:24px; top:-11px; width:11px; height:11px; border-radius:50%; background:radial-gradient(circle at 30% 25%,#f08089,#a52d43 65%,#671a2b); }
.mini-straw { position:absolute; z-index:21; right:18px; top:-17px; width:3px; height:68px; border-radius:3px; background:linear-gradient(#ef9a9f,#db5d76); transform:rotate(13deg); transform-origin:bottom; }
.mini-bubbles { position:absolute; inset:0; z-index:12; }
.mini-bubbles i { position:absolute; width:4px; height:4px; border-radius:50%; background:rgba(255,255,255,.45); }
.mini-bubbles i:nth-child(1){left:25px;bottom:35px}.mini-bubbles i:nth-child(2){left:44px;bottom:52px}.mini-bubbles i:nth-child(3){right:20px;bottom:25px}
.mini-orange-half { position:absolute; z-index:20; width:38px; height:22px; border-radius:38px 38px 0 0; background:radial-gradient(circle at 50% 100%,#ffe7a2 0 32%,#ffb447 34% 68%,#e86d18 70% 100%); box-shadow:0 4px 8px rgba(0,0,0,.2); }
.mini-orange-half:after { content:""; position:absolute; left:18px; top:3px; width:1px; height:17px; background:rgba(255,239,188,.65); transform:rotate(28deg); }
.mini-orange-half { right:4px; top:20px; transform:rotate(13deg); }
.mini-orange-half.second { left:5px; right:auto; top:62px; width:28px; height:17px; transform:rotate(-18deg); }
.mini-leaf { position:absolute; z-index:21; right:23px; top:12px; width:20px; height:10px; border-radius:100% 0 100% 0; background:linear-gradient(135deg,#83a85c,#456b40); transform:rotate(-20deg); }
.mini-cocktail-olive { position:absolute; z-index:20; left:36px; top:30px; width:13px; height:13px; border-radius:50%; background:#b5b86d; box-shadow:inset 3px 2px 4px rgba(255,255,255,.28); }
.mini-pick { position:absolute; z-index:19; left:43px; top:9px; width:2px; height:47px; background:#e9c78d; transform:rotate(-10deg); }
.mini-blue-glow { position:absolute; z-index:15; left:31px; top:47px; width:45px; height:30px; border-radius:50%; background:radial-gradient(circle,#91b8ff,rgba(60,89,155,.2) 70%,transparent); filter:blur(4px); }
.mini-lemon-twist { position:absolute; z-index:21; right:11px; top:30px; width:30px; height:10px; border:3px solid #f5c75d; border-left-color:transparent; border-bottom-color:transparent; border-radius:50%; transform:rotate(18deg); }
.mini-star { position:absolute; z-index:22; left:33px; top:49px; color:#dbe6ff; font-size:12px; text-shadow:0 0 9px #89aaff; }

.selected-order {
    width:min(900px,92vw);
    margin:0 auto 14px;
    text-align:center;
}
.selected-order-small {
    color:#805c3d;
    font-family:Georgia,serif;
    font-size:10px;
    letter-spacing:3px;
    line-height:1.4;
}
.selected-order-title {
    color:#dcae73;
    font-family:"Noto Serif KR",serif;
    font-size:28px;
    line-height:1.45;
    margin-top:5px;
}
.selected-order-sub {
    color:#96765d;
    font-family:"Noto Serif KR",serif;
    font-size:13px;
    line-height:1.8;
    margin-top:2px;
}
.drink-stage {
    min-height:540px;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:8px 0 14px;
}
.drink-visual {
    position:relative;
    width:300px;
    height:430px;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
}
.glass {
    position:relative;
    width:190px;
    height:270px;
    margin-top:22px;
    border:2px solid rgba(226,208,178,.57);
    border-top:0;
    border-radius:10px 10px 52px 52px;
    overflow:visible;
    background:linear-gradient(90deg,rgba(255,255,255,.11),rgba(255,255,255,.025),rgba(255,255,255,.09));
    box-shadow:0 28px 55px rgba(0,0,0,.35), inset 0 0 20px rgba(255,255,255,.05);
}
.glass .liquid {
    position:absolute;
    left:0;
    right:0;
    bottom:0;
    border-radius:0 0 48px 48px;
    transition:height .4s ease;
    opacity:.9;
    overflow:hidden;
}
.glass .liquid:after {
    content:"";
    position:absolute;
    inset:0;
    background:radial-gradient(circle at 20% 28%, rgba(255,255,255,.28) 0 1px, transparent 2px), radial-gradient(circle at 68% 45%, rgba(255,255,255,.18) 0 1px, transparent 2px), radial-gradient(circle at 48% 70%, rgba(255,255,255,.16) 0 1px, transparent 2px);
    background-size:40px 45px, 52px 55px, 64px 62px;
    opacity:.6;
}
.drink-scene.green .liquid { background:linear-gradient(180deg,#a4ec9d 0%,#68ca79 46%,#3ca45f 100%); }
.drink-scene.orange .liquid { background:linear-gradient(180deg,#ffd98f 0%,#ffad3c 42%,#f17b19 100%); }
.drink-scene.pink .liquid { background:linear-gradient(180deg,#f4b1c0 0%,#dc7f9b 42%,#b24e76 100%); }
.drink-scene.navy .liquid { background:linear-gradient(180deg,#708dc4 0%,#40598f 40%,#202c59 100%); }
.glass-shine {
    position:absolute;
    z-index:9;
    top:25px;
    left:28px;
    width:18px;
    height:205px;
    border-radius:50%;
    background:rgba(255,255,255,.14);
    filter:blur(2px);
    pointer-events:none;
}
.glass-rim {
    position:absolute;
    z-index:10;
    left:-1px;
    right:-1px;
    top:-1px;
    height:17px;
    border:2px solid rgba(236,226,214,.58);
    border-radius:50%;
    background:rgba(255,255,255,.03);
    box-shadow:0 2px 7px rgba(0,0,0,.16);
}
.glass-foot {
    position:absolute;
    left:50%;
    bottom:-35px;
    width:3px;
    height:38px;
    transform:translateX(-50%);
    background:rgba(226,208,178,.55);
}
.glass-base {
    position:absolute;
    left:50%;
    bottom:-43px;
    width:112px;
    height:10px;
    transform:translateX(-50%);
    border:2px solid rgba(226,208,178,.55);
    border-radius:50%;
}
.drink-scene.green .glass {
    width:174px;
    height:285px;
    border-radius:5px 5px 38px 38px;
}
.drink-scene.green .glass-foot,
.drink-scene.green .glass-base { display:block; }
.drink-scene.orange .glass {
    width:220px;
    height:220px;
    margin-top:45px;
    border-radius:11px 11px 56px 56px;
}
.drink-scene.orange .glass-foot,
.drink-scene.orange .glass-base { display:none; }
.drink-scene.pink .glass {
    width:225px;
    height:170px;
    margin-top:58px;
    border-radius:0 0 110px 110px;
    transform:perspective(200px) rotateX(-3deg);
}
.drink-scene.pink .glass-foot,
.drink-scene.pink .glass-base { display:block; }
.pink-olive {
    position:absolute;
    z-index:14;
    left:50%;
    top:22px;
    width:24px;
    height:24px;
    transform:translateX(-50%);
    border-radius:50%;
    background:radial-gradient(circle at 32% 25%,#d7d99b 0%,#a8ad63 48%,#68703d 100%);
    box-shadow:inset 3px 2px 4px rgba(255,255,255,.28), 0 4px 8px rgba(0,0,0,.22);
}
.pink-olive:after {
    content:"";
    position:absolute;
    left:8px;
    top:8px;
    width:7px;
    height:7px;
    border-radius:50%;
    background:rgba(90,60,35,.45);
}
.pink-pick {
    position:absolute;
    z-index:13;
    left:50%;
    top:8px;
    width:2px;
    height:46px;
    transform:translateX(-50%) rotate(-9deg);
    transform-origin:bottom center;
    background:#e5c98e;
    border-radius:2px;
}
/* 실제 음료에서는 잔 안쪽에서만 보이도록 합니다. */
.glass { overflow:hidden !important; isolation:isolate; }
.glass .liquid { left:2px !important; right:2px !important; bottom:2px !important; max-height:calc(100% - 18px); }
.glass .glass-rim { z-index:20; pointer-events:none; }
.glass-foot, .glass-base { overflow:visible !important; }
/* 가니시는 잔 위로 튀어나오지 않고 잔 안쪽에서 보이도록 */
.melon-ice-cream { top:18px !important; width:72px; height:42px; z-index:12; }
.melon-ice-cream:after { bottom:0; width:54px; }
.drink-straw { top:18px !important; height:72px !important; left:66%; }
.drink-cherry { top:24px !important; left:35%; }
.drink-cherry:after { display:none; }
.orange-half.one { top:18px !important; right:8px; width:64px; height:36px; }
.orange-half.two { top:58px !important; bottom:auto; left:20px; width:52px; height:29px; }
.orange-leaf { display:none; }
.navy-garnish { top:24px !important; left:18px; width:60px; height:13px; }

.drink-scene.navy .glass {
    width:230px;
    height:205px;
    margin-top:44px;
    border-radius:12px 12px 46px 46px;
}
.drink-scene.navy .glass-foot,
.drink-scene.navy .glass-base { display:none; }
.melon-ice-cream {
    position:absolute;
    z-index:12;
    top:-35px;
    left:50%;
    width:98px;
    height:72px;
    transform:translateX(-50%);
    border-radius:54% 54% 45% 45%;
    background:radial-gradient(circle at 34% 24%, #fffef7 0%, #fff2d0 55%, #dfcca2 100%);
    box-shadow:0 8px 16px rgba(0,0,0,.24);
}
.melon-ice-cream:after {
    content:"";
    position:absolute;
    left:50%;
    bottom:-4px;
    width:65px;
    height:12px;
    transform:translateX(-50%);
    border-radius:50%;
    background:rgba(218,194,150,.55);
}
.drink-straw {
    position:absolute;
    z-index:13;
    top:-56px;
    left:63%;
    width:4px;
    height:112px;
    border-radius:4px;
    background:linear-gradient(180deg,#ec8f9c,#dd5f76);
    transform:rotate(12deg);
    transform-origin:bottom center;
}
.drink-cherry {
    position:absolute;
    z-index:14;
    top:-45px;
    left:38%;
    width:18px;
    height:18px;
    border-radius:50%;
    background:radial-gradient(circle at 30% 25%, #e77c83, #ae3147 62%, #762033 100%);
    box-shadow:0 4px 8px rgba(0,0,0,.2);
}
.drink-cherry:after {
    content:"";
    position:absolute;
    width:30px;
    height:22px;
    top:-16px;
    left:9px;
    border-top:2px solid #6b8156;
    border-radius:50%;
    transform:rotate(28deg);
}
.orange-half {
    position:absolute;
    z-index:14;
    width:88px;
    height:48px;
    border-radius:88px 88px 0 0;
    background:radial-gradient(circle at 50% 100%, #ffe8a6 0 34%, #ffb84c 36% 69%, #f47b20 71% 88%, #fff1c6 90% 94%, #df6b17 95%);
    box-shadow:0 8px 16px rgba(0,0,0,.22);
}
.orange-half:after {
    content:""; position:absolute; left:50%; bottom:4px; width:2px; height:39px;
    background:rgba(255,240,190,.7); transform:translateX(-50%) rotate(25deg);
    box-shadow:-15px 8px 0 -0.5px rgba(255,240,190,.5), 15px 8px 0 -0.5px rgba(255,240,190,.5);
}
.orange-half.one { right:8px; top:-20px; transform:rotate(15deg); }
.orange-half.two { left:20px; bottom:12px; width:60px; height:34px; opacity:.95; transform:rotate(-18deg); }
.orange-leaf {
    position:absolute;
    z-index:14;
    left:37px;
    top:-22px;
    width:42px;
    height:22px;
    border-radius:100% 0 100% 0;
    background:linear-gradient(135deg,#7eac58,#406b40);
    transform:rotate(-20deg);
}
.melon-straw-line {
    position:absolute;
    z-index:15;
    left:50%;
    top:-52px;
    width:4px;
    height:150px;
    border-radius:4px;
    background:linear-gradient(180deg,#f3c67a,#db8b41);
    transform:translateX(-50%) rotate(-13deg);
    transform-origin:bottom center;
}
.bubbles {
    position:absolute;
    z-index:11;
    inset:0;
    pointer-events:none;
}
.bubbles span { position:absolute; border-radius:50%; background:rgba(255,255,255,.35); box-shadow:0 0 7px rgba(255,255,255,.24); }
.bubbles .b1 { width:7px; height:7px; left:28%; top:33%; }
.bubbles .b2 { width:4px; height:4px; left:42%; top:26%; }
.bubbles .b3 { width:6px; height:6px; left:63%; top:43%; }
.bubbles .b4 { width:3px; height:3px; left:73%; top:30%; }
.navy-garnish {
    position:absolute;
    z-index:14;
    left:16px;
    top:8px;
    width:75px;
    height:17px;
    border-radius:70% 30% 70% 30%;
    background:linear-gradient(90deg,#f8e3a2,#f3b54e);
    transform:rotate(-17deg);
    box-shadow:0 6px 13px rgba(0,0,0,.2);
}
.navy-garnish:after {
    content:"";
    position:absolute;
    width:28px;
    height:7px;
    left:11px;
    top:5px;
    border-radius:50%;
    background:#fff1bd;
}
.stars { position:absolute; inset:0; z-index:13; pointer-events:none; }
.stars span { position:absolute; color:rgba(220,229,255,.75); font-size:16px; text-shadow:0 0 12px rgba(160,187,255,.8); }
.stars .s1 { top:35px; left:34px; }
.stars .s2 { top:75px; right:44px; font-size:12px; }
.stars .s3 { bottom:43px; left:62px; font-size:11px; }
.drink-name {
    color:#dcae73;
    font-family:"Cormorant Garamond",Georgia,serif;
    letter-spacing:3px;
    font-size:18px;
    line-height:1.3;
    margin-top:66px;
    text-align:center;
}
.drink-state {
    color:#896951;
    font-family:Georgia,serif;
    font-size:10px;
    letter-spacing:3px;
    margin-top:6px;
    text-align:center;
}
.concierge-card {
    padding:25px 26px 23px;
    border:1px solid rgba(199,157,109,.25);
    background:linear-gradient(180deg, rgba(247,238,219,.065), rgba(247,238,219,.025));
    box-shadow:0 20px 45px rgba(0,0,0,.22);
    margin-bottom:18px;
}
.concierge-label {
    color:#805c3d;
    font-family:Georgia,serif;
    font-size:11px;
    letter-spacing:3px;
    line-height:1.4;
}
.concierge-title {
    color:#dcae73;
    font-family:"Noto Serif KR",serif;
    font-size:21px;
    line-height:1.75;
    margin-top:10px;
}
.concierge-copy {
    color:#96765d;
    font-family:"Noto Serif KR",serif;
    font-size:12px;
    line-height:1.9;
    margin-top:12px;
}
.compact-recommendations {
    max-height:510px;
    overflow-y:auto;
    padding-right:5px;
}
.compact-recommendation {
    border-top:1px solid rgba(199,157,109,.16);
    padding:13px 0 14px;
}
.compact-recommendation:first-child { border-top:0; }
.compact-rec-title {
    color:#e0bd91;
    font-family:"Cormorant Garamond",Georgia,serif;
    font-size:18px;
    line-height:1.4;
}
.compact-rec-meta {
    color:#9c7b63;
    font-family:"Noto Serif KR",serif;
    font-size:11px;
    line-height:1.7;
    margin-top:2px;
}
.recommendation-title {
    color:#dca072;
    font-family:"Cormorant Garamond",Georgia,serif;
    font-size:25px;
    letter-spacing:4px;
    margin:2px 0 7px;
}
.ai-note {
    color:#76563e;
    font-family:Georgia,serif;
    font-size:9px;
    letter-spacing:2px;
    margin-bottom:5px;
}
.drink-controls {
    width:min(340px, 90vw);
    margin:0 auto;
}

@media (max-width: 1050px) {
    .cocktail-title { font-size:48px; }
    .drink-stage { min-height:520px; }
}

@media (max-width: 900px) {
    .cocktail-title { font-size:42px; }
    .cocktail-header { padding-top:26px; padding-bottom:18px; }
    .drink-stage { min-height:430px; }
    .drink-visual { transform:scale(.9); transform-origin:center; margin-bottom:-18px; }
}

@media (max-width: 700px) {
    .room-service-container, .listen-search, .fireplace-container { width:92vw; }
    .room-service-title, .fireplace-title { font-size:38px; }
    .section-title { font-size:38px; }
    .cocktail-title { font-size:34px; letter-spacing:4px; }
    .cocktail-subtitle { padding:0 20px; }
    .order-slip { min-height:285px; margin-bottom:10px; }
    .slip-label { margin-top:15px; font-size:15px; }
    .letter-paper { padding:50px 35px; min-height:auto; }
    .letter-body { font-size:15px; }
    .drink-visual { transform:scale(.82); margin-bottom:-35px; }
    .drink-stage { min-height:380px; padding-bottom:0; }
}
/* Final visual spacing and cocktail refinement */
.order-slip {
    min-height: 372px !important;
    padding: 27px 18px 24px !important;
    margin-bottom: 18px !important;
    background: linear-gradient(145deg, rgba(255,244,229,.095), rgba(69,42,30,.34) 48%, rgba(16,10,8,.34)) !important;
    border-color: rgba(220,177,128,.42) !important;
}
.order-slip div[data-testid="stButton"] { margin-top: 18px !important; }
.order-slip div[data-testid="stButton"] > button {
    min-height: 48px !important;
    margin-top: 0 !important;
    letter-spacing: 3px !important;
    background: linear-gradient(135deg, rgba(105,68,43,.26), rgba(28,17,13,.66)) !important;
}
.cocktail-header { padding: 26px 0 34px !important; }
.cocktail-subtitle { margin-top: 15px !important; line-height: 2 !important; }
.mini-drink { margin-top: 25px !important; margin-bottom: 15px !important; transform: scale(1.12); }
.slip-drink { margin-top: 15px !important; }
.slip-desc { margin-top: 12px !important; line-height: 2 !important; }
.drink-visual { filter: drop-shadow(0 24px 28px rgba(0,0,0,.32)) !important; }
.glass {
    backdrop-filter: blur(3px) !important;
    border-color: rgba(255,245,232,.82) !important;
    box-shadow: 0 28px 54px rgba(0,0,0,.28), inset 10px 0 17px rgba(255,255,255,.13), inset -10px 0 18px rgba(0,0,0,.11), inset 0 0 0 1px rgba(255,255,255,.08) !important;
}
.glass .liquid { transition: height .28s ease, background .28s ease; }
.glass .bubble-dot { position:absolute; z-index:5; width:5px; height:5px; border-radius:50%; background:radial-gradient(circle at 30% 25%,rgba(255,255,255,.95),rgba(255,255,255,.18) 72%); box-shadow:0 0 7px rgba(255,255,255,.2); pointer-events:none; }
.bubbles { position:absolute; inset:0; overflow:hidden; border-radius:inherit; pointer-events:none; }
.drink-straw { z-index:18 !important; filter:drop-shadow(1px 1px 1px rgba(0,0,0,.16)); }
.melon-ice-cream { box-shadow: inset 5px 3px 8px rgba(255,255,255,.65), inset -4px -4px 8px rgba(194,165,120,.2), 0 7px 13px rgba(0,0,0,.18) !important; }
.melon-ice-cream.half-gone { opacity:.55 !important; transform:translateY(12px) scale(.82) !important; transition:all .2s ease; }
.orange-half { box-shadow: inset 0 0 0 2px rgba(255,243,203,.72), 0 5px 12px rgba(0,0,0,.2) !important; }
.pink-olive { box-shadow: inset 4px 3px 5px rgba(255,255,255,.7), inset -3px -3px 5px rgba(120,39,70,.2), 0 4px 8px rgba(0,0,0,.2) !important; }
.drink-name { margin-top: 26px !important; }
.drink-state { margin-top: 8px !important; }
@media (max-width: 900px) {
    .order-slip { min-height: 340px !important; margin-bottom: 18px !important; }
    .cocktail-header { padding-bottom: 26px !important; }
}
@media (max-width: 700px) {
    .order-slip { min-height: 300px !important; margin-bottom: 16px !important; }
    .mini-drink { margin-top: 18px !important; transform: scale(1.02); }
}

<style>
/* COCKTAIL BAR final art direction: more breathing room and clear, connected glassware. */
.cocktail-header {
    width: min(1180px, 94vw) !important;
    margin: 0 auto !important;
    padding: 34px 0 48px !important;
}
.cocktail-kicker { font-size: 11px !important; letter-spacing: 4.5px !important; color: #a98563 !important; }
.cocktail-title {
    margin-top: 15px !important;
    font-size: clamp(42px, 5vw, 60px) !important;
    letter-spacing: 6.5px !important;
    line-height: 1.16 !important;
}
.cocktail-subtitle {
    margin: 18px auto 0 !important;
    max-width: 720px !important;
    font-size: 14px !important;
    line-height: 2 !important;
    letter-spacing: .6px !important;
    color: #c2a287 !important;
}
/* Explicitly create a gap between the menu card and its Streamlit button element. */
[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:has(.order-slip) {
    margin-bottom: 23px !important;
}
[data-testid="stColumn"] [data-testid="stVerticalBlock"] { row-gap: 13px !important; }
.order-slip {
    box-sizing: border-box !important;
    min-height: 425px !important;
    height: 425px !important;
    padding: 25px 18px 24px !important;
    margin: 0 !important;
    overflow: hidden !important;
    border-radius: 5px !important;
    border: 1px solid rgba(218,177,133,.40) !important;
    background: linear-gradient(155deg, rgba(255,242,224,.09), rgba(63,39,28,.25) 52%, rgba(16,10,8,.36)) !important;
    box-shadow: 0 18px 40px rgba(0,0,0,.24), inset 0 1px rgba(255,255,255,.045) !important;
}
.order-slip:before { inset: 9px !important; border-color: rgba(218,177,133,.16) !important; }
.slip-no { font-size: 10px !important; color: #a17f60 !important; letter-spacing: 3px !important; }
.slip-label {
    min-height: 48px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 14px auto 0 !important;
    max-width: 250px !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
    letter-spacing: .3px !important;
    color: #f3debf !important;
}
.slip-drink { margin-top: 8px !important; font-size: 13px !important; line-height: 1.5 !important; letter-spacing: 2px !important; }
.slip-desc {
    min-height: 44px !important;
    margin: 9px auto 0 !important;
    max-width: 245px !important;
    font-size: 11px !important;
    line-height: 1.9 !important;
    color: #b69a81 !important;
}
[data-testid="stColumn"] div[data-testid="stButton"] { margin-top: 0 !important; }
[data-testid="stColumn"] div[data-testid="stButton"] > button {
    min-height: 52px !important;
    letter-spacing: 3px !important;
    background: linear-gradient(135deg, rgba(92,58,39,.42), rgba(24,15,11,.82)) !important;
    border-color: rgba(213,167,117,.55) !important;
    box-shadow: 0 8px 22px rgba(0,0,0,.16) !important;
}
[data-testid="stColumn"] div[data-testid="stButton"] > button:hover { transform: translateY(-1px); border-color: #eac18e !important; }
.mini-drink {
    width: 100% !important;
    height: 190px !important;
    margin: 2px auto 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    filter: drop-shadow(0 12px 15px rgba(0,0,0,.22)) !important;
    transform: none !important;
    position: relative !important;
    z-index: 1 !important;
}
.cocktail-svg { display: block; overflow: visible; }
.cocktail-svg.mini { width: 146px !important; height: 190px !important; max-width: 100% !important; }
.cocktail-svg.hero { width: min(300px, 100%) !important; height: auto !important; max-height: 390px !important; margin: 0 auto !important; }
.drink-visual {
    width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    margin: 0 auto !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    filter: drop-shadow(0 20px 24px rgba(0,0,0,.28)) !important;
    transform: none !important;
}
.drink-name { margin-top: 7px !important; font-size: 16px !important; letter-spacing: 3.2px !important; line-height: 1.8 !important; }
.drink-state { margin-top: 3px !important; font-size: 10px !important; letter-spacing: 2.5px !important; }
.selected-order { margin: 7px auto 25px !important; }
.selected-order-title { margin-top: 9px !important; font-size: clamp(22px, 2vw, 28px) !important; line-height: 1.6 !important; }
.selected-order-sub { margin-top: 7px !important; line-height: 1.9 !important; }
.concierge-card { padding: 27px 28px !important; margin-bottom: 24px !important; }
.recommendation-title { margin-top: 20px !important; }
@media (max-width: 1150px) {
    .order-slip { min-height: 405px !important; height: 405px !important; padding-left: 12px !important; padding-right: 12px !important; }
    .mini-drink { height: 172px !important; }
    .cocktail-svg.mini { height: 172px !important; }
}
@media (max-width: 700px) {
    .cocktail-header { padding: 23px 0 30px !important; }
    .cocktail-title { font-size: 36px !important; letter-spacing: 4px !important; }
    .cocktail-subtitle { padding: 0 16px !important; margin-top: 14px !important; }
    .order-slip { min-height: 390px !important; height: 390px !important; }
    .mini-drink { height: 170px !important; }
    .cocktail-svg.mini { height: 170px !important; }
    .cocktail-svg.hero { width: min(265px, 100%) !important; }
}
</style>
</style>
"""

try:
    st.html(CSS)
except Exception:
    st.markdown(CSS, unsafe_allow_html=True)

# Final responsive visual corrections. Kept separate so these overrides reliably win.
POLISH_CSS = r"""
<style>
/* Consistent, legible section heading and more breathing room before actions. */
.section-area { min-height: 0 !important; padding-top: clamp(34px, 5vh, 58px) !important; margin: 0 auto 0 !important; text-align: center !important; }
.section-area .section-title, .cocktail-header .cocktail-title { color: #d9ad75 !important; font-family: "Cormorant Garamond", Georgia, serif !important; font-weight: 400 !important; letter-spacing: 5px !important; line-height: 1.2 !important; }
.section-area .section-subtitle { color: #aa8667 !important; line-height: 1.9 !important; margin-top: 12px !important; }
.room-service-buttons-spacer { height: 34px !important; width: 100%; line-height: 0 !important; }

/* Mood menu: compact cards, centered type and clearly separated order buttons. */
.cocktail-header { width: min(1180px, 94vw) !important; padding: 25px 0 35px !important; margin: 0 auto !important; text-align: center !important; }
.cocktail-kicker { color: #a98563 !important; font-size: 10px !important; letter-spacing: 4px !important; }
.cocktail-title { color: #dcb47c !important; font-family: "Cormorant Garamond", Georgia, serif !important; font-size: clamp(38px, 4.3vw, 52px) !important; font-weight: 400 !important; letter-spacing: 5px !important; line-height: 1.15 !important; text-align: center !important; }
.cocktail-subtitle { color: #c0a087 !important; font-size: 13px !important; margin: 15px auto 0 !important; max-width: 680px !important; line-height: 1.9 !important; text-align: center !important; }
.order-slip { height: 360px !important; min-height: 360px !important; box-sizing: border-box !important; padding: 18px 14px 16px !important; margin: 0 !important; overflow: hidden !important; border: 1px solid rgba(211,170,121,.34) !important; border-radius: 4px !important; background: linear-gradient(155deg, rgba(255,240,220,.065), rgba(54,34,24,.20) 54%, rgba(14,9,7,.28)) !important; box-shadow: 0 12px 28px rgba(0,0,0,.19), inset 0 1px rgba(255,255,255,.03) !important; }
.order-slip:before { inset: 7px !important; border-color: rgba(211,170,121,.12) !important; }
.slip-no { color: #957353 !important; text-align: center !important; font-size: 9px !important; letter-spacing: 2.4px !important; }
.slip-label { display: block !important; min-height: 0 !important; margin: 10px auto 0 !important; max-width: 240px !important; color: #f0d7b8 !important; text-align: center !important; font-size: 14px !important; line-height: 1.6 !important; letter-spacing: 0 !important; }
.mini-drink { display: flex !important; width: 100% !important; height: 198px !important; align-items: center !important; justify-content: center !important; margin: 7px auto 0 !important; transform: none !important; filter: drop-shadow(0 7px 9px rgba(0,0,0,.20)) !important; overflow: visible !important; }
.cocktail-svg.mini { display: block !important; width: 158px !important; height: 198px !important; max-width: 100% !important; margin: 0 auto !important; overflow: visible !important; }
.slip-drink { color: #d9b182 !important; text-align: center !important; margin: 6px auto 0 !important; font-size: 12px !important; line-height: 1.5 !important; letter-spacing: 1.5px !important; }
.slip-desc { min-height: 0 !important; max-width: 245px !important; margin: 5px auto 0 !important; color: #aa8b71 !important; font-size: 10px !important; line-height: 1.6 !important; text-align: center !important; }
.cocktail-order-button-gap { height: 10px !important; min-height: 10px !important; width: 100%; line-height: 0 !important; }
[data-testid="stColumn"] div[data-testid="stButton"] > button { min-height: 46px !important; letter-spacing: 2.5px !important; border-color: rgba(213,167,117,.48) !important; background: linear-gradient(135deg, rgba(92,58,39,.34), rgba(24,15,11,.80)) !important; }

/* Selected drink: smaller overall glass, connected stem/base retained in the SVG. */
.selected-order { margin: 4px auto 16px !important; }
.selected-order-title { color: #dcb47c !important; font-size: clamp(20px, 2vw, 25px) !important; line-height: 1.45 !important; }
.drink-stage { min-height: 0 !important; padding: 0 !important; }
.drink-visual { width: 100% !important; height: auto !important; min-height: 0 !important; margin: 0 auto !important; filter: drop-shadow(0 12px 18px rgba(0,0,0,.24)) !important; }
.cocktail-svg.hero { display: block !important; width: min(225px, 100%) !important; height: auto !important; max-height: 300px !important; margin: 0 auto !important; }
.drink-name { color: #dcb47c !important; margin-top: 8px !important; font-size: 14px !important; letter-spacing: 1.5px !important; line-height: 1.6 !important; text-align: center !important; }
.drink-state { margin-top: 2px !important; color: #a98768 !important; font-size: 9px !important; letter-spacing: 2px !important; text-align: center !important; }
.concierge-card { padding: 21px 22px !important; }

@media (max-width: 1050px) {
  .order-slip { height: 348px !important; min-height: 348px !important; padding-left: 10px !important; padding-right: 10px !important; }
  .mini-drink { height: 184px !important; }
  .cocktail-svg.mini { width: 148px !important; height: 185px !important; }
}
@media (max-width: 700px) {
  .room-service-buttons-spacer { height: 26px !important; }
  .cocktail-header { padding: 20px 0 25px !important; }
  .cocktail-title { font-size: 34px !important; letter-spacing: 3px !important; }
  .order-slip { height: 334px !important; min-height: 334px !important; padding: 16px 9px 14px !important; }
  .mini-drink { height: 172px !important; }
  .cocktail-svg.mini { width: 138px !important; height: 172px !important; }
  .slip-label { font-size: 12px !important; }
  .slip-desc { font-size: 9px !important; }
  .cocktail-svg.hero { width: min(210px, 100%) !important; }
}
</style>
"""
st.markdown(POLISH_CSS, unsafe_allow_html=True)

# Final targeted fixes requested after live-screen review.
# These rules intentionally come last to override conflicting earlier style layers.
FINAL_VISUAL_FIXES = r"""
<style>
/* MY ROOM check-in gate: readable contrast and truly centered supporting text. */
.main .block-container .auth-box {
    width: min(520px, 90vw) !important;
    max-width: 520px !important;
    margin: 16px auto 10px !important;
    padding: 25px 30px !important;
    box-sizing: border-box !important;
    background: linear-gradient(145deg, rgba(247,238,219,.095), rgba(247,238,219,.045)) !important;
    border: 1px solid rgba(213,167,117,.42) !important;
    box-shadow: 0 12px 28px rgba(0,0,0,.18) !important;
}
.main .block-container .auth-box .auth-subtitle {
    display: block !important;
    width: 100% !important;
    color: #e6c7a3 !important;
    font-family: "Noto Serif KR", serif !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    text-align: center !important;
    line-height: 2 !important;
    letter-spacing: .1px !important;
    margin: 4px auto 8px !important;
    opacity: 1 !important;
    text-shadow: none !important;
}
.main .block-container .auth-box .auth-title {
    color: #e1b276 !important;
    text-align: center !important;
}

/* ROOM SERVICE landing: a clearly visible pause between subtitle and both action buttons. */
.room-service-buttons-spacer {
    display: block !important;
    width: 100% !important;
    height: 64px !important;
    min-height: 64px !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 0 !important;
}
@media (max-width: 700px) {
    .room-service-buttons-spacer {
        height: 48px !important;
        min-height: 48px !important;
    }
}

/* Warm, restrained room interior: legible and responsive. */
.room-interior-heading { text-align:center; padding: 14px 0 24px; }
.room-interior-kicker { color:#9f7956; font-size:10px; letter-spacing:4px; margin-bottom:9px; }
.room-interior-title { color:#d9ad76; font-family:"Cormorant Garamond", Georgia, serif; font-size:clamp(34px,4vw,46px); letter-spacing:5px; line-height:1.1; }
.room-interior-subtitle { color:#b3977d; font-family:"Noto Serif KR", serif; font-size:13px; margin-top:12px; letter-spacing:.4px; }
.room-scene-wrap { width:100%; max-width:1120px; margin:0 auto; border:1px solid rgba(190,145,92,.32); background:#1a100c; box-shadow:0 16px 36px rgba(0,0,0,.18); overflow:hidden; }
.room-scene { display:block; width:100%; height:auto; }
.room-scene-caption { text-align:center; color:#9e7b59; font-family:Georgia,serif; font-size:10px; letter-spacing:3px; margin:12px 0 8px; }
.room-scene-caption span { color:#d3a56d; padding:0 8px; }
.st-key-room_service_actions { margin-top: 76px !important; max-width:1100px !important; margin-left:auto !important; margin-right:auto !important; }
.st-key-room_service_actions div[data-testid="stButton"] > button { min-height:54px !important; background:rgba(42,27,19,.42) !important; border:1px solid rgba(191,145,95,.48) !important; color:#dfb27b !important; font-size:15px !important; letter-spacing:3px !important; }
.st-key-room_service_actions div[data-testid="stButton"] > button:hover { background:rgba(112,75,45,.24) !important; border-color:rgba(220,174,119,.7) !important; color:#f0d3a9 !important; transform:translateY(-1px); }
.st-key-room_furniture_actions { margin-top:-350px !important; position:relative !important; z-index:10 !important; }
.st-key-room_furniture_actions div[data-testid="stButton"] > button { min-height:250px !important; height:250px !important; padding:12px 8px !important; background:rgba(18,10,7,.035) !important; border:1px solid rgba(190,145,92,.12) !important; color:#f0d0a0 !important; font-size:13px !important; letter-spacing:1.2px !important; white-space:normal !important; text-shadow:0 1px 4px rgba(0,0,0,.9) !important; }
.st-key-room_furniture_actions div[data-testid="stButton"] > button:hover { background:rgba(122,83,51,.18) !important; border-color:rgba(221,176,119,.55) !important; color:#ffe2b6 !important; }
.main .block-container div[data-testid="stButton"] > button { font-size:15px !important; letter-spacing:2px !important; line-height:1.35 !important; min-height:44px !important; border-radius:2px !important; box-shadow:none !important; }

/* Final check-in typography and controls: override older conflicting style layers. */
.main .block-container .section-area:has(+ div .auth-box),
.main .block-container .section-area:has(+ div .auth-box) .section-title {
    text-align: center !important;
}
.main .block-container .section-area:has(+ div .auth-box) {
    padding-top: clamp(42px, 8vh, 86px) !important;
    margin-bottom: 24px !important;
}
.main .block-container .section-area:has(+ div .auth-box) .section-title {
    color: #e4bd86 !important;
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: clamp(38px, 4.5vw, 52px) !important;
    font-weight: 400 !important;
    letter-spacing: 7px !important;
    line-height: 1.1 !important;
}
.main .block-container .auth-box {
    width: min(560px, calc(100vw - 36px)) !important;
    max-width: 560px !important;
    margin: 0 auto 18px !important;
    padding: 25px 32px !important;
    box-sizing: border-box !important;
    background: rgba(31, 19, 13, .72) !important;
    border: 1px solid rgba(204, 163, 111, .36) !important;
    border-radius: 4px !important;
    box-shadow: 0 12px 34px rgba(0, 0, 0, .16) !important;
}
.main .block-container .auth-box .auth-subtitle {
    display: block !important;
    color: #e7d3b8 !important;
    font-family: "Noto Serif KR", serif !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    text-align: center !important;
    line-height: 2 !important;
    letter-spacing: .15px !important;
    margin: 0 auto !important;
    opacity: 1 !important;
    text-shadow: none !important;
    overflow-wrap: keep-all !important;
}
.main .block-container .auth-box .auth-title {
    color: #e4bd86 !important;
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: 32px !important;
    font-weight: 400 !important;
    letter-spacing: 5px !important;
    text-align: center !important;
    line-height: 1.25 !important;
    margin-bottom: 8px !important;
}
.st-key-checkin_gate_action { max-width: 250px !important; margin: 0 auto 18px !important; }
.st-key-checkin_gate_action div[data-testid="stButton"] > button {
    min-height: 48px !important;
    background: #d4ad7b !important;
    color: #21150e !important;
    border: 1px solid #d4ad7b !important;
    border-radius: 3px !important;
    box-shadow: none !important;
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 3px !important;
}
.st-key-checkin_gate_action div[data-testid="stButton"] > button:hover {
    background: #e6c79e !important;
    border-color: #e6c79e !important;
    color: #21150e !important;
    transform: translateY(-1px) !important;
}
.st-key-checkin_gate_back { max-width: 560px !important; margin: 0 auto !important; }
.st-key-checkin_gate_back div[data-testid="stButton"] > button {
    min-height: 40px !important;
    background: transparent !important;
    color: #bda184 !important;
    border: 1px solid rgba(204,163,111,.25) !important;
    border-radius: 3px !important;
    box-shadow: none !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
}
.st-key-checkin_gate_back div[data-testid="stButton"] > button:hover {
    background: rgba(204,163,111,.08) !important;
    color: #f0d7b5 !important;
    border-color: rgba(204,163,111,.55) !important;
}

/* Room hotspots stay quiet until the pointer reaches the actual object target. */
.st-key-room_fullscreen .st-key-room_hotspot_fireplace div[data-testid="stButton"] > button,
.st-key-room_fullscreen .st-key-room_hotspot_lp div[data-testid="stButton"] > button,
.st-key-room_fullscreen .st-key-room_hotspot_bookshelf div[data-testid="stButton"] > button {
    background: rgba(18,10,6,.12) !important;
    color: rgba(244,214,168,.0) !important;
    border-color: rgba(218,177,116,.0) !important;
    box-shadow: none !important;
}
.st-key-room_fullscreen .st-key-room_hotspot_fireplace div[data-testid="stButton"] > button:hover,
.st-key-room_fullscreen .st-key-room_hotspot_lp div[data-testid="stButton"] > button:hover,
.st-key-room_fullscreen .st-key-room_hotspot_bookshelf div[data-testid="stButton"] > button:hover {
    background: rgba(18,10,6,.76) !important;
    color: #fff0d3 !important;
    border-color: rgba(218,177,116,.72) !important;
}

/* Reduce the glass gloss while preserving a clear rim and stem/base connection. */
.mini-drink {
    filter: drop-shadow(0 4px 7px rgba(0,0,0,.14)) !important;
}
.drink-visual {
    filter: drop-shadow(0 9px 14px rgba(0,0,0,.17)) !important;
}
.cocktail-svg .glass-highlight,
.cocktail-svg .glass-shine {
    opacity: .42 !important;
}
</style>
"""
st.markdown(FINAL_VISUAL_FIXES, unsafe_allow_html=True)


# =========================================================
# SUPABASE
# =========================================================

try:
    from supabase import create_client
except Exception:
    create_client = None

SUPABASE_CONFIG_ERROR = ""
SUPABASE_URL_VALUE = ""

@st.cache_resource
def get_supabase():
    global SUPABASE_CONFIG_ERROR, SUPABASE_URL_VALUE

    SUPABASE_CONFIG_ERROR = ""
    SUPABASE_URL_VALUE = ""

    if create_client is None:
        SUPABASE_CONFIG_ERROR = "supabase 패키지가 설치되어 있지 않습니다. requirements.txt에 supabase를 추가해 주세요."
        return None

    try:
        url = str(st.secrets["SUPABASE_URL"]).strip()
        key = str(st.secrets["SUPABASE_KEY"]).strip()
        SUPABASE_URL_VALUE = url
    except Exception:
        SUPABASE_CONFIG_ERROR = "Streamlit Secrets에 SUPABASE_URL과 SUPABASE_KEY가 없습니다."
        return None

    # Project URL이 아닌 Supabase 대시보드 주소를 넣는 실수를 방지합니다.
    if (
        not url.startswith("https://")
        or "supabase.com/dashboard" in url
        or "/dashboard/" in url
        or ".supabase.co" not in url
    ):
        SUPABASE_CONFIG_ERROR = (
            "SUPABASE_URL이 올바른 Project URL이 아닙니다. "
            "Supabase → Project Settings → API → Project URL의 "
            "https://프로젝트주소.supabase.co 형태를 넣어 주세요."
        )
        return None

    if not key:
        SUPABASE_CONFIG_ERROR = "SUPABASE_KEY가 비어 있습니다."
        return None

    try:
        return create_client(url, key)
    except Exception as e:
        SUPABASE_CONFIG_ERROR = f"Supabase 연결 오류: {e}"
        return None

supabase = get_supabase()

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "page": "main",
    "main_entered": False,
    "choice_mode": None,
    "room_service_step": "search",
    "search_text": "",
    "search_results": [],
    "logged_in": False,
    "current_user": None,
    "auth_mode": "login",
    "my_room_checkin_open": False,
    "current_record": None,
    "room_records": [],
    "room_books": [],
    "my_room_view": "room",
    "room_lobby_migration_v1": False,
    "cocktail_mood": None,
    "cocktail_sips": 0,
    "cocktail_recommendations": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# One-time migration for guests who were already signed in when the room lobby was added.
if not st.session_state.room_lobby_migration_v1:
    if st.session_state.logged_in and st.session_state.my_room_view == "fireplace":
        st.session_state.my_room_view = "room"
    st.session_state.room_lobby_migration_v1 = True

# =========================================================
# NAVIGATION
# =========================================================

def go(page):
    st.session_state.page = page
    if page != "main":
        st.session_state.main_entered = False
    if page != "choice":
        st.session_state.choice_mode = None
    if page != "my_room":
        st.session_state.my_room_checkin_open = False
    if page != "choice":
        st.session_state.cocktail_mood = None
        st.session_state.cocktail_sips = 0
        st.session_state.cocktail_recommendations = []
    st.rerun()

def go_room_service():
    st.session_state.page = "choice"
    st.session_state.choice_mode = None
    st.session_state.room_service_step = "search"
    st.session_state.cocktail_mood = None
    st.session_state.cocktail_sips = 0
    st.session_state.cocktail_recommendations = []
    st.rerun()

def go_my_room():
    st.session_state.page = "my_room"
    st.rerun()

# =========================================================
# AUTH
# =========================================================

def _auth_error_message(message, action="회원가입"):
    """Supabase의 오류를 사용자가 알아보기 쉽게 변환합니다."""
    text = str(message).strip()
    lower = text.lower()

    if "already registered" in lower or "user already registered" in lower:
        return "이미 가입된 이메일입니다."

    if "email signups are disabled" in lower:
        return "Supabase에서 이메일 회원가입이 비활성화되어 있습니다. Authentication → Providers → Email에서 활성화해 주세요."

    if "invalid api key" in lower or ("apikey" in lower and "invalid" in lower):
        return "Supabase API KEY가 올바르지 않습니다. Streamlit Secrets의 SUPABASE_KEY를 확인해 주세요."

    if "rate limit" in lower or "email rate limit" in lower:
        return "이메일 발송 제한에 걸렸습니다. 잠시 후 다시 시도해 주세요."

    # Supabase URL이 잘못되어 HTML 페이지가 JSON 대신 반환되는 경우
    # 현재 화면에서 보였던 pydantic 'Invalid JSON' 오류를 사람이 이해할 수 있게 바꿉니다.
    if "invalid json" in lower and "doctype html" in lower:
        return (
            "SUPABASE_URL이 잘못되었습니다. 지금 Supabase API가 JSON 대신 HTML 페이지를 반환했습니다. "
            "Streamlit Secrets의 SUPABASE_URL에는 Supabase Dashboard 주소가 아니라 "
            "Project Settings → API → Project URL(https://프로젝트주소.supabase.co)을 넣어 주세요."
        )

    if "fetch failed" in lower or "connection" in lower or "connect" in lower:
        return f"Supabase 연결에 실패했습니다. SUPABASE_URL과 SUPABASE_KEY를 확인해 주세요.\n\n상세 오류: {text}"

    return f"{action} 오류: {text}"


def login_user(email, password):
    if supabase is None:
        return False, SUPABASE_CONFIG_ERROR or "Supabase 연결을 확인해 주세요."
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        user = getattr(response, "user", None)
        if user is None:
            return False, "로그인 정보를 확인해 주세요."
        st.session_state.logged_in = True
        st.session_state.current_user = user
        return True, "CHECK-IN 완료"
    except Exception as e:
        message = str(e).strip()
        lower_message = message.lower()
        if "invalid login credentials" in lower_message:
            return False, "이메일 또는 비밀번호가 올바르지 않습니다."
        if "email not confirmed" in lower_message:
            return False, "이메일 인증이 아직 완료되지 않았습니다. 가입한 이메일의 인증 메일을 확인해 주세요."
        return False, _auth_error_message(message, "로그인")


def signup_user(email, password):
    if supabase is None:
        return False, SUPABASE_CONFIG_ERROR or "Supabase 연결을 확인해 주세요."
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        user = getattr(response, "user", None)
        if user is None:
            return False, "회원가입에 실패했습니다. Supabase 응답에 사용자 정보가 없습니다."

        session = getattr(response, "session", None)
        if session is not None:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            return True, "CHECK-IN 완료"

        return True, "회원가입이 완료되었습니다. 이메일 인증 후 CHECK-IN 해주세요."
    except Exception as e:
        return False, _auth_error_message(str(e), "회원가입")


def logout_user():
    if supabase is not None:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_record = None
    st.session_state.room_records = []
    st.rerun()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">RECORD HOTEL</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sidebar-subtitle">A QUIET PLACE FOR MUSIC</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sidebar-rule"></div>',
        unsafe_allow_html=True
    )

    if st.button("MAIN", key="nav_main"):
        go("main")

    if st.button("ROOM SERVICE", key="nav_choice"):
        go("choice")

    if st.button("MY ROOM", key="nav_my_room"):
        go("my_room")

# =========================================================
# APPLE API
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def apple_search(params):
    url = "https://itunes.apple.com/search?" + urllib.parse.urlencode(params)
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "record-room/1.0"}
        )
        with urllib.request.urlopen(request, timeout=12) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return {"resultCount": 0, "results": []}

@st.cache_data(ttl=600, show_spinner=False)
def apple_lookup(params):
    url = "https://itunes.apple.com/lookup?" + urllib.parse.urlencode(params)
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "record-room/1.0"}
        )
        with urllib.request.urlopen(request, timeout=12) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return {"resultCount": 0, "results": []}

# =========================================================
# KOREA POPULAR CHART
# =========================================================

@st.cache_data(ttl=900, show_spinner=False)
def korea_top_chart():
    """Apple Music 대한민국 Top 100을 받아 검색 결과의 인기순 정렬에 사용합니다."""
    urls = [
        "https://rss.applemarketingtools.com/api/v2/kr/music/most-played/100/songs.json",
        "https://itunes.apple.com/kr/rss/topsongs/limit=100/json",
    ]

    for url in urls:
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "record-room/1.0"}
            )
            with urllib.request.urlopen(request, timeout=12) as response:
                data = json.loads(response.read().decode("utf-8"))

            results = data.get("feed", {}).get("results", [])
            if not results:
                results = data.get("results", [])

            if results:
                return results[:100]
        except Exception:
            continue

    return []


def artist_names_equivalent(name_a, name_b):
    na = normalize(name_a)
    nb = normalize(name_b)
    if not na or not nb:
        return False
    if na == nb:
        return True

    for key, aliases in ARTIST_ALIASES.items():
        group = {normalize(key)}
        group.update(normalize(alias) for alias in aliases)
        if na in group and nb in group:
            return True

    return False


def korea_chart_rank(track):
    title = normalize(track.get("trackName") or track.get("name") or "")
    artist = track.get("artistName", "")
    if not title:
        return 9999

    for rank, item in enumerate(korea_top_chart(), start=1):
        chart_title = normalize(item.get("name") or item.get("trackName") or "")
        chart_artist = item.get("artistName", "")
        if chart_title == title and artist_names_equivalent(artist, chart_artist):
            return rank

    return 9999


def popularity_sort_key(track):
    chart_rank = korea_chart_rank(track)
    release_date = track.get("releaseDate", "") or ""
    release_score = 0
    if release_date:
        try:
            release_score = -int(release_date[:10].replace("-", ""))
        except Exception:
            release_score = 0
    return (0 if chart_rank < 9999 else 1, chart_rank, release_score)


def rank_by_korea_popularity(results, limit=None):
    ranked = sorted(results, key=popularity_sort_key)
    return ranked[:limit] if limit else ranked

def normalize(text):
    if not text:
        return ""
    return re.sub(r"[^0-9a-z가-힣]", "", text.lower())

# =========================================================
# SEARCH ALIASES
# =========================================================

ARTIST_ALIASES = {
    "아이유": ["IU"],
    "iu": ["아이유"],
    "지코": ["ZICO", "Zico"],
    "zico": ["지코"],
    "뉴진스": ["NewJeans"],
    "newjeans": ["뉴진스"],
    "방탄소년단": ["BTS"],
    "bts": ["방탄소년단"],
    "블랙핑크": ["BLACKPINK"],
    "blackpink": ["블랙핑크"],
    "에스파": ["aespa"],
    "aespa": ["에스파"],
    "아이브": ["IVE"],
    "ive": ["아이브"],
    "세븐틴": ["SEVENTEEN"],
    "seventeen": ["세븐틴"],
    "르세라핌": ["LE SSERAFIM", "LE SSERAFIM"],
    "le sserafim": ["르세라핌"],
    "보이넥스트도어": ["BOYNEXTDOOR", "BOY NEXT DOOR"],
    "boynextdoor": ["보이넥스트도어", "BOYNEXTDOOR"],
    "boy next door": ["보이넥스트도어", "BOYNEXTDOOR"],
    "투모로우바이투게더": ["TOMORROW X TOGETHER", "TXT"],
    "txt": ["TOMORROW X TOGETHER", "투모로우바이투게더"],
    "스트레이키즈": ["Stray Kids"],
    "straykids": ["스트레이키즈", "Stray Kids"],
    "엔하이픈": ["ENHYPEN"],
    "enhypen": ["엔하이픈"],
    "르세라핌": ["LE SSERAFIM"],
    "아이들": ["(G)I-DLE", "G I-DLE", "여자아이들"],
    "여자아이들": ["(G)I-DLE", "아이들"],
    "gidle": ["(G)I-DLE", "여자아이들"],
    "빅뱅": ["BIGBANG"],
    "bigbang": ["빅뱅"],
    "악뮤": ["AKMU", "악동뮤지션"],
    "akmu": ["악뮤", "AKMU"],
}

# Apple Music/iTunes의 동명이인 아티스트를 피하기 위한 대표 아티스트 ID입니다.
# 특히 IU는 같은 이름을 쓰는 다른 아티스트가 검색되는 경우가 있어 ID로 고정합니다.
KNOWN_ARTIST_IDS = {
    "아이유": 409076743,
    "iu": 409076743,
}

PREFERRED_ARTIST_NAMES = {
    "아이유": ["아이유", "IU"],
    "iu": ["아이유", "IU"],
    "지코": ["ZICO", "지코"],
    "zico": ["ZICO", "지코"],
    "뉴진스": ["NewJeans", "뉴진스"],
    "newjeans": ["NewJeans", "뉴진스"],
    "보이넥스트도어": ["BOYNEXTDOOR", "보이넥스트도어"],
    "boynextdoor": ["BOYNEXTDOOR", "보이넥스트도어"],
    "방탄소년단": ["BTS", "방탄소년단"],
    "bts": ["BTS", "방탄소년단"],
    "블랙핑크": ["BLACKPINK", "블랙핑크"],
    "blackpink": ["BLACKPINK", "블랙핑크"],
    "에스파": ["aespa", "에스파"],
    "aespa": ["aespa", "에스파"],
}


SONG_ALIASES = {
    "러브 윈즈 올": ["Love wins all"],
    "love wins all": ["러브 윈즈 올"],
    "러브윈즈올": ["Love wins all"],
}


def expand_search_terms(query, alias_map):
    query = query.strip()
    terms = [query]
    lower = query.lower()
    normalized = normalize(query)

    for key, aliases in alias_map.items():
        if lower == key.lower() or normalized == normalize(key):
            for alias in aliases:
                if alias not in terms:
                    terms.append(alias)
            break

    return terms


# =========================================================
# ARTIST SEARCH
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def find_artist_tracks(query):
    query = query.strip()
    if not query:
        return []

    search_terms = expand_search_terms(query, ARTIST_ALIASES)
    nq = normalize(query)
    candidates = []

    for search_term in search_terms:
        for country in ["KR", "US"]:
            data = apple_search({
                "term": search_term,
                "country": country,
                "media": "music",
                "entity": "musicArtist",
                "attribute": "artistTerm",
                "limit": 50
            })

            for artist in data.get("results", []):
                artist_id = artist.get("artistId")
                artist_name = artist.get("artistName", "")
                if not artist_id or not artist_name:
                    continue
                if not any(x.get("artistId") == artist_id for x in candidates):
                    candidates.append(artist)

    # musicArtist 검색이 한글 검색에서 비어 있는 경우 곡 검색으로 아티스트를 역추적합니다.
    if not candidates:
        for search_term in search_terms:
            for country in ["KR", "US"]:
                data = apple_search({
                    "term": search_term,
                    "country": country,
                    "media": "music",
                    "entity": "song",
                    "attribute": "artistTerm",
                    "limit": 100
                })
                for song in data.get("results", []):
                    artist_id = song.get("artistId")
                    artist_name = song.get("artistName", "")
                    if not artist_id or not artist_name:
                        continue
                    if not any(x.get("artistId") == artist_id for x in candidates):
                        candidates.append({
                            "artistId": artist_id,
                            "artistName": artist_name
                        })

    if not candidates:
        return []

    # -----------------------------------------------------
    # 0. 대표 아티스트 ID가 있으면 이름 검색 결과보다 ID를 우선합니다.
    # -----------------------------------------------------
    known_id = None
    for key, artist_id in KNOWN_ARTIST_IDS.items():
        if normalize(key) == normalize(query):
            known_id = artist_id
            break

    if known_id is not None:
        canonical = [
            artist for artist in candidates
            if artist.get("artistId") == known_id
        ]
        if canonical:
            selected = canonical[0]
        else:
            # 검색 결과에 ID가 빠져도 직접 lookup하면 정확한 아티스트를 확보할 수 있습니다.
            lookup_data = apple_lookup({
                "id": known_id,
                "entity": "song",
                "country": "KR",
                "limit": 100
            })
            canonical_tracks = [
                item for item in lookup_data.get("results", [])
                if item.get("wrapperType") == "track"
                and item.get("kind") == "song"
            ]
            if canonical_tracks:
                return rank_by_korea_popularity(canonical_tracks, limit=30)
            selected = None
    else:
        selected = None

    # 원래 검색어 → 공식/대표 표기 → 별칭 → 부분 일치 순서로 정확도를 높입니다.
    preferred_names = PREFERRED_ARTIST_NAMES.get(lower := query.lower(), [])
    preferred_normalized = [normalize(name) for name in preferred_names]

    if selected is None and preferred_normalized:
        preferred = [
            artist for artist in candidates
            if normalize(artist.get("artistName", "")) in preferred_normalized
        ]
        if preferred:
            selected = preferred[0]

    if selected is None:
        exact = [
            artist for artist in candidates
            if normalize(artist.get("artistName", "")) == nq
        ]
        if exact:
            selected = exact[0]

    if selected is None:
        for alias in search_terms[1:]:
            alias_normalized = normalize(alias)
            exact_alias = [
                artist for artist in candidates
                if normalize(artist.get("artistName", "")) == alias_normalized
            ]
            if exact_alias:
                selected = exact_alias[0]
                break

    if selected is None:
        for term in search_terms:
            nt = normalize(term)
            contains = [
                artist for artist in candidates
                if nt and nt in normalize(artist.get("artistName", ""))
            ]
            if contains:
                selected = contains[0]
                break

    if selected is None:
        return []

    artist_id = selected.get("artistId")
    if not artist_id:
        return []

    all_tracks = []
    for country in ["KR", "US"]:
        data = apple_lookup({
            "id": artist_id,
            "entity": "song",
            "country": country,
            "limit": 100
        })
        for item in data.get("results", []):
            if item.get("wrapperType") == "track" and item.get("kind") == "song":
                track_id = item.get("trackId")
                if track_id and any(x.get("trackId") == track_id for x in all_tracks):
                    continue
                all_tracks.append(item)

    # 대한민국에서 현재 많이 듣는 곡을 먼저 보여주고,
    # 그 뒤에 최신 발매곡을 보완합니다. 그래서 "아이유"처럼
    # 동명이인의 듣보 아티스트가 검색 상단을 차지하는 문제를 줄입니다.
    return rank_by_korea_popularity(all_tracks, limit=30)


# =========================================================
# SONG SEARCH
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def find_song(query):
    query = query.strip()
    if not query:
        return []

    search_terms = expand_search_terms(query, SONG_ALIASES)
    all_results = []

    for search_term in search_terms:
        for country in ["KR", "US"]:
            data = apple_search({
                "term": search_term,
                "country": country,
                "media": "music",
                "entity": "song",
                "attribute": "songTerm",
                "limit": 100
            })
            for result in data.get("results", []):
                track_name = result.get("trackName", "")
                if not track_name:
                    continue
                track_id = result.get("trackId")
                if track_id and any(x.get("trackId") == track_id for x in all_results):
                    continue
                all_results.append(result)

    if not all_results:
        return []

    # 원문 정확 일치
    for term in search_terms:
        nt = normalize(term)
        exact = [
            result for result in all_results
            if normalize(result.get("trackName", "")) == nt
        ]
        if exact:
            return rank_by_korea_popularity(exact, limit=30)

    # 제목에 검색어가 포함되는 결과
    partial = []
    for term in search_terms:
        nt = normalize(term)
        if not nt:
            continue
        partial.extend([
            result for result in all_results
            if nt in normalize(result.get("trackName", ""))
        ])

    unique = []
    seen = set()
    for result in partial:
        track_id = result.get("trackId")
        if track_id in seen:
            continue
        seen.add(track_id)
        unique.append(result)

    return rank_by_korea_popularity(unique, limit=30)


# =========================================================
# GENERAL SEARCH
# =========================================================

def search_music(query, mode):
    query = query.strip()
    if not query:
        return []

    if mode == "artist":
        return find_artist_tracks(query)
    if mode == "song":
        return find_song(query)

    artist_results = find_artist_tracks(query)
    if artist_results:
        return artist_results
    return find_song(query)


# =========================================================
# AI COCKTAIL RECOMMENDATION
# =========================================================

MOOD_CONFIG = {
    "sad": {
        "label": "조금 위로가 필요해요",
        "drink": "핑크 칵테일",
        "color": "pink",
        "description": "마음을 가라앉히고 천천히 쉬어 가는 음악",
        "fallback": ["Korean sad ballad", "Korean emotional R&B", "IU ballad", "Korean indie melancholy"],
    },
    "refresh": {
        "label": "산뜻하게 기분 전환",
        "drink": "멜론 소다",
        "color": "green",
        "description": "가볍고 청량한 분위기로 전환하는 음악",
        "fallback": ["K-pop refreshing", "Korean upbeat pop", "Korean pop summer", "K-pop bright"],
    },
    "excited": {
        "label": "신나는 노래가 필요해요",
        "drink": "오렌지 주스",
        "color": "orange",
        "description": "리듬을 타면서 기분을 끌어올리는 음악",
        "fallback": ["K-pop dance", "Korean hip hop", "K-pop party", "Korean upbeat R&B"],
    },
    "quiet": {
        "label": "조용히 쉬고 싶어요",
        "drink": "네이비 칵테일",
        "color": "navy",
        "description": "차분하게 집중하고 편하게 쉴 수 있는 음악",
        "fallback": ["Korean indie acoustic", "Korean chill R&B", "Korean lo-fi", "Korean soft pop"],
    },
}


def cocktail_visual_html(color, fill=100, mini=False):
    """Inline SVG cocktail illustration with connected bowl, stem and base.

    Liquid, bubbles and in-glass details are clipped to the bowl. Garnishes are
    progressively removed after each sip; the melon soda's long straw remains.
    """
    color = color if color in {"pink", "green", "orange", "navy"} else "pink"
    height = 100 if mini else max(0, min(100, int(fill)))
    sips = 0 if mini else max(0, min(6, round((100 - height) / 17)))
    uid = f"rh-{color}-{'mini' if mini else 'hero'}"

    # Bowl geometry, stem and base are a single visual assembly. Each liquid is clipped
    # to its own glass silhouette so none can spill outside the vessel.
    specs = {
        "pink": {
            "body": "M 30 80 C 40 126 74 164 120 174 C 166 164 200 126 210 80 Q 120 60 30 80 Z",
            "rim_y": 80, "rim_rx": 90, "rim_ry": 11,
            "floor": 171, "usable": 88, "left": 30, "width": 180,
            "stem": "M 116 170 L 117 251 Q 120 256 123 251 L 124 170 Z",
            "base_y": 260, "base_rx": 39, "base_ry": 6,
            "shine": "M 48 91 C 58 124 79 150 98 159",
        },
        "green": {
            "body": "M 70 68 Q 120 57 170 68 L 158 201 Q 156 215 140 220 L 100 220 Q 84 215 82 201 Z",
            "rim_y": 68, "rim_rx": 51, "rim_ry": 10,
            "floor": 214, "usable": 137, "left": 70, "width": 100,
            "stem": "M 116 217 L 117 267 Q 120 270 123 267 L 124 217 Z",
            "base_y": 278, "base_rx": 45, "base_ry": 6,
            "shine": "M 82 82 L 91 193 Q 92 205 101 209",
        },
        "orange": {
            "body": "M 48 116 Q 120 98 192 116 C 188 158 176 198 153 214 Q 120 229 87 214 C 64 198 52 158 48 116 Z",
            "rim_y": 116, "rim_rx": 72, "rim_ry": 12,
            "floor": 219, "usable": 94, "left": 49, "width": 142,
            "stem": "M 116 217 L 117 269 Q 120 272 123 269 L 124 217 Z",
            "base_y": 280, "base_rx": 46, "base_ry": 6,
            "shine": "M 62 128 C 68 166 77 191 94 204",
        },
        "navy": {
            "body": "M 34 80 Q 120 52 206 80 L 128 155 Q 120 163 112 155 Z",
            "rim_y": 80, "rim_rx": 86, "rim_ry": 12,
            "floor": 156, "usable": 67, "left": 36, "width": 168,
            "stem": "M 117 157 L 118 238 Q 120 241 122 238 L 123 157 Z",
            "base_y": 250, "base_rx": 48, "base_ry": 6,
            "shine": "M 49 82 Q 87 72 113 82 L 118 105",
        },
    }
    s = specs[color]
    liquid_h = s["usable"] * height / 100.0
    liquid_top = s["floor"] - liquid_h
    top_width = s["rim_rx"] * 2 * (0.88 if color == "navy" else 0.96)
    bottom_width = {"pink": 22, "green": 56, "orange": 58, "navy": 16}[color]
    frac = min(1.0, max(0.0, (liquid_top - (s["floor"] - s["usable"])) / s["usable"])) if s["usable"] else 0
    surface_w = bottom_width + (top_width - bottom_width) * frac
    surface_left = 120 - surface_w / 2

    liquid_colors = {
        "pink": ("#ffe5ed", "#ee94b2", "#b94070"),
        "green": ("#e0ffd5", "#83dfa0", "#26965d"),
        "orange": ("#fff0bb", "#ffb33e", "#e75f19"),
        "navy": ("#b6d0ff", "#536fb2", "#151c43"),
    }
    c1, c2, c3 = liquid_colors[color]
    bubble_positions = [(0.24, .20), (.69, .34), (.43, .52), (.78, .66), (.29, .76), (.57, .26), (.61, .86), (.18, .48)]
    # Small, fine carbonation bubbles; fewer as the drink is sipped.
    bubble_count = 0 if height <= 0 else min(5, max(1, round(height / 21)))
    bubbles_svg = []
    if liquid_h > 6:
        interior_left = s["left"] + 6
        interior_w = s["width"] - 12
        for i, (xp, yp) in enumerate(bubble_positions[:bubble_count]):
            bx = interior_left + interior_w * xp
            by = s["floor"] - max(4, liquid_h * yp)
            radius = (1.05, 1.25, 0.95, 1.15, 1.0, 0.9, 1.2, 0.85)[i]
            bubbles_svg.append(
                f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{radius}" '
                'fill="#fff9f1" fill-opacity=".30" stroke="#ffffff" stroke-opacity=".08" stroke-width=".35"/>'
            )
    bubbles = ''.join(bubbles_svg)

    liquid_block = ""
    if height > 0 and liquid_h > 0:
        liquid_block = (
            f'<rect x="0" y="{liquid_top:.2f}" width="240" height="{liquid_h + 7:.2f}" '
            f'fill="url(#{uid}-liquid)" opacity=".92"/>'
            f'<path d="M {surface_left:.1f} {liquid_top:.1f} Q 120 {liquid_top + 3:.1f} '
            f'{surface_left + surface_w:.1f} {liquid_top:.1f}" fill="none" stroke="#fff9ee" '
            'stroke-opacity=".27" stroke-width="1.2"/>'
            + bubbles
        )

    # Decorations are layered intentionally and have discrete stages tied to each sip.
    garnish = ""
    sparkles = ""
    if color == "pink":
        if sips < 1:
            garnish += (
                '<path d="M 111 52 L 136 112" stroke="#edcf91" stroke-width="3.2" stroke-linecap="round"/>'
                '<path d="M 112 54 L 136 112" stroke="#fff0c8" stroke-width=".9" stroke-linecap="round"/>'
            )
        if sips < 2:
            garnish += (
                '<circle cx="135" cy="105" r="9.5" fill="url(#' + uid + '-pearl)" stroke="#fff0da" stroke-width="1.2"/>'
                '<circle cx="132" cy="102" r="2.6" fill="#fff8f4" fill-opacity=".78"/>'
            )
    elif color == "green":
        # This long straw is intentionally retained for every sip state.
        garnish += (
            '<path d="M 157 13 L 132 109" stroke="#e87f95" stroke-width="8" stroke-linecap="round"/>'
            '<path d="M 156 14 L 133 105" stroke="#ffe2df" stroke-width="2" stroke-linecap="round"/>'
        )
        if sips < 1:
            # Full scoop and cherry overlap slightly so they read as one garnish on the rim.
            garnish += (
                '<path d="M 73 72 C 70 53 86 37 107 37 C 130 37 144 53 142 73 '
                'Q 109 88 73 72 Z" fill="url(#' + uid + '-cream)" stroke="#fff9e9" stroke-width="1.5"/>'
                '<path d="M 80 65 Q 108 76 136 66" fill="none" stroke="#e9d9b8" stroke-width="1.6" stroke-opacity=".68"/>'
                '<circle cx="135" cy="66" r="9.5" fill="url(#' + uid + '-cherry)" stroke="#f5b8af" stroke-width="1.1"/>'
                '<path d="M 134 57 Q 142 49 150 54" fill="none" stroke="#7a9659" stroke-width="2.1" stroke-linecap="round"/>'
            )
        elif sips < 2:
            garnish += (
                '<path d="M 89 73 Q 100 62 115 69 L 130 74 Q 108 82 89 73 Z" '
                'fill="url(#' + uid + '-cream)" stroke="#fff9e9" stroke-width="1.1" opacity=".70"/>'
            )
    elif color == "orange":
        if sips < 2:
            # One modest citrus wheel sits directly on the bowl's rim; no detached garnish.
            garnish += (
                '<g transform="translate(171 113) rotate(10)">'
                '<circle r="19" fill="#e9671b" stroke="#ffcd74" stroke-width="2.0"/>'
                '<circle r="15.8" fill="#fff0b9"/>'
                '<circle r="13.7" fill="url(#' + uid + '-liquid)" stroke="#f28b2d" stroke-width="1.15"/>'
                '<path d="M 0 0 L 0 -13 M 0 0 L 11.8 6.5 M 0 0 L -11.8 6.5 M 0 0 L 0 13" stroke="#fff2c5" stroke-width="1.15" stroke-linecap="round"/>'
                '<circle r="2.0" fill="#fff3cf"/>'
                '</g>'
            )
    else:  # navy
        if sips < 2:
            # A single fine lemon twist sits across the rim; no loose pick or floating dot.
            garnish += (
                '<path d="M 151 80 C 157 66 176 65 185 78 C 177 84 163 84 155 78" '
                'fill="#ffd46e" stroke="#fff0b2" stroke-width="1.25" stroke-linejoin="round"/>'
                '<path d="M 158 78 Q 170 72 179 78" fill="none" stroke="#fff6d3" stroke-width="1.4" stroke-linecap="round"/>'
            )
        # Fine, sparse glints fade with the liquid level.
        star_specs = [(91, .30, 1.45), (145, .49, 1.2), (111, .68, 1.05)]
        count = 0 if height < 8 else (1 if height < 34 else (2 if height < 62 else 3))
        for sx, yf, rr in star_specs[:count]:
            sy = s["floor"] - max(5, liquid_h * yf)
            sparkles += (
                f'<path d="M {sx} {sy-rr*2:.1f} L {sx+rr*.55:.1f} {sy-rr*.55:.1f} '
                f'L {sx+rr*2:.1f} {sy:.1f} L {sx+rr*.55:.1f} {sy+rr*.55:.1f} '
                f'L {sx} {sy+rr*2:.1f} L {sx-rr*.55:.1f} {sy+rr*.55:.1f} '
                f'L {sx-rr*2:.1f} {sy:.1f} L {sx-rr*.55:.1f} {sy-rr*.55:.1f} Z" '
                'fill="#e3eaff" fill-opacity=".84"/>'
            )

    bubble_gradient = {
        "pink": ("#fff2f6", "#e7a0b7", "#b73e70"),
        "green": ("#f2ffdf", "#a3efb5", "#2a9a62"),
        "orange": ("#fff4c9", "#ffc15c", "#eb6b1e"),
        "navy": ("#e0eaff", "#8ca9e7", "#283d80"),
    }[color]
    g1, g2, g3 = bubble_gradient
    rim_y = s["rim_y"]
    rim_rx, rim_ry = s["rim_rx"], s["rim_ry"]
    base_y, base_rx, base_ry = s["base_y"], s["base_rx"], s["base_ry"]
    top_y = rim_y
    glass_shape = s["body"]
    stem = s["stem"]

    # Draw base and stem first so the bowl visibly joins them rather than floating above them.
    svg = (
        f'<svg class="cocktail-svg {"mini" if mini else "hero"}" viewBox="0 0 240 300" width="{158 if mini else 240}" height="{198 if mini else 300}" '
        'role="img" aria-label="' + {"pink":"Pink cocktail", "green":"Melon soda", "orange":"Orange juice", "navy":"Navy cocktail"}[color] + '">' 
        '<defs>'
        f'<linearGradient id="{uid}-liquid" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{c1}"/><stop offset=".45" stop-color="{c2}"/><stop offset="1" stop-color="{c3}"/></linearGradient>'
        f'<linearGradient id="{uid}-glass" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#ffffff" stop-opacity=".17"/><stop offset=".22" stop-color="#ffffff" stop-opacity=".02"/>'
        '<stop offset=".76" stop-color="#ffffff" stop-opacity=".015"/><stop offset="1" stop-color="#ffffff" stop-opacity=".11"/></linearGradient>'
        f'<linearGradient id="{uid}-stem" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#cbbba5" stop-opacity=".68"/><stop offset=".45" stop-color="#fff2dc" stop-opacity=".9"/>'
        '<stop offset="1" stop-color="#a18d77" stop-opacity=".74"/></linearGradient>'
        f'<radialGradient id="{uid}-pearl" cx="30%" cy="25%">'
        '<stop offset="0" stop-color="#fffef8"/><stop offset=".55" stop-color="#f7dfc5"/><stop offset="1" stop-color="#c68b91"/></radialGradient>'
        f'<radialGradient id="{uid}-cream" cx="32%" cy="20%">'
        '<stop offset="0" stop-color="#fffef3"/><stop offset=".62" stop-color="#fff0c8"/><stop offset="1" stop-color="#dbc59a"/></radialGradient>'
        f'<radialGradient id="{uid}-cherry" cx="25%" cy="20%">'
        '<stop offset="0" stop-color="#ff9aa0"/><stop offset=".55" stop-color="#d9364f"/><stop offset="1" stop-color="#781c35"/></radialGradient>'
        f'<clipPath id="{uid}-clip"><path d="{glass_shape}"/></clipPath>'
        '</defs>'
        f'<ellipse cx="120" cy="{base_y + 4}" rx="{base_rx + 6}" ry="4" fill="#000000" fill-opacity=".20"/>'
        f'<path d="{stem}" fill="url(#{uid}-stem)" stroke="#f2dfc7" stroke-opacity=".58" stroke-width=".8"/>'
        f'<ellipse cx="120" cy="{base_y}" rx="{base_rx}" ry="{base_ry}" fill="#281911" fill-opacity=".56" stroke="#e8d7c0" stroke-opacity=".62" stroke-width="1.5"/>'
        f'<ellipse cx="120" cy="{base_y-1}" rx="{base_rx-7}" ry="{max(2,base_ry-2)}" fill="none" stroke="#fff1da" stroke-opacity=".15" stroke-width=".8"/>'
        f'<g clip-path="url(#{uid}-clip)">'
        + liquid_block + sparkles +
        '</g>'
        f'<path d="{glass_shape}" fill="url(#{uid}-glass)" fill-opacity=".24" stroke="#f5e7d5" stroke-opacity=".70" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<path d="{s["shine"]}" fill="none" stroke="#fffdf6" stroke-opacity=".28" stroke-width="2.0" stroke-linecap="round"/>'
        f'<ellipse cx="120" cy="{top_y}" rx="{rim_rx}" ry="{rim_ry}" fill="#ffffff" fill-opacity=".025" stroke="#fff6e9" stroke-opacity=".68" stroke-width="1.6"/>'
        f'<ellipse cx="120" cy="{top_y+1}" rx="{rim_rx-4}" ry="{max(2,rim_ry-3)}" fill="none" stroke="#ffffff" stroke-opacity=".13" stroke-width=".8"/>'
        + garnish +
        '</svg>'
    )
    if mini:
        return f'<div class="mini-drink mini-{color}">{svg}</div>'
    return f'<div class="drink-visual drink-scene {color}" data-sips="{sips}">{svg}</div>'


def get_openai_key():
    try:
        key = str(st.secrets["OPENAI_API_KEY"]).strip()
        return key
    except Exception:
        return ""


def extract_response_text(data):
    pieces = []
    for item in data.get("output", []) if isinstance(data, dict) else []:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []) or []:
            if isinstance(content, dict) and content.get("type") in ("output_text", "text"):
                text_value = content.get("text", "")
                if text_value:
                    pieces.append(str(text_value))
    return "\n".join(pieces).strip()


@st.cache_data(ttl=1800, show_spinner=False)
def ai_search_terms(mood_key):
    config = MOOD_CONFIG[mood_key]
    api_key = get_openai_key()

    if not api_key:
        return config["fallback"], False

    system_prompt = (
        "You are the music concierge of a Korean mystery hotel. "
        "The user has selected a mood. Generate exactly 5 concise search phrases "
        "that can be sent to the Apple iTunes music search API. "
        "Prefer real Korean/English genres, artists, or music styles rather than abstract adjectives. "
        "Do not invent song titles. Return only 5 lines, one search phrase per line, with no numbering."
    )
    user_prompt = (
        f"Mood: {config['label']}\n"
        f"Description: {config['description']}\n"
        "Create five useful search phrases for finding songs that fit this mood."
    )

    body = json.dumps({
        "model": "gpt-5.6-luna",
        "input": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_output_tokens": 180,
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8"))
        text = extract_response_text(data)
        terms = []
        for line in text.splitlines():
            line = re.sub(r"^[\s\-•\d\.\)]+", "", line).strip()
            if line and line not in terms:
                terms.append(line)
        if len(terms) >= 2:
            return terms[:5], True
    except Exception:
        pass

    curated_fallbacks = {
        "sad": ["IU Through the Night", "AKMU How can I love the heartbreak", "BOL4 To My Youth", "Taeyeon Fine", "Paul Kim Me After You"],
        "refresh": ["NewJeans Super Shy", "IVE After LIKE", "DAY6 Time of Our Life", "ZICO Any Song", "LE SSERAFIM Perfect Night"],
        "excited": ["aespa Supernova", "BLACKPINK Shut Down", "ZICO SPOT", "BTS Dynamite", "SEVENTEEN Super"],
        "quiet": ["wave to earth seasons", "DEAN instagram", "Colde Your Dog Loves You", "BIBI Restless", "IU 밤편지"],
    }
    return curated_fallbacks.get(mood_key, config["fallback"]), False


@st.cache_data(ttl=1800, show_spinner=False)
def get_ai_recommendations(mood_key):
    terms, used_ai = ai_search_terms(mood_key)
    results = []

    for term in terms:
        data = apple_search({
            "term": term,
            "country": "KR",
            "media": "music",
            "entity": "song",
            "limit": 25,
        })
        for item in data.get("results", []):
            if not item.get("trackName") or not item.get("artistName"):
                continue
            if not item.get("previewUrl"):
                continue
            track_id = item.get("trackId")
            if track_id and any(x.get("trackId") == track_id for x in results):
                continue
            results.append(item)
            if len(results) >= 35:
                break
        if len(results) >= 35:
            break

    if results:
        return rank_by_korea_popularity(results, limit=8), used_ai

    # KR 검색이 부족하면 US 검색도 보완합니다.
    for term in terms:
        data = apple_search({
            "term": term,
            "country": "US",
            "media": "music",
            "entity": "song",
            "limit": 25,
        })
        for item in data.get("results", []):
            if not item.get("trackName") or not item.get("artistName") or not item.get("previewUrl"):
                continue
            track_id = item.get("trackId")
            if track_id and any(x.get("trackId") == track_id for x in results):
                continue
            results.append(item)
            if len(results) >= 35:
                break
        if len(results) >= 35:
            break

    return rank_by_korea_popularity(results, limit=8), used_ai

# =========================================================
# RECORD HELPERS
# =========================================================

def record_data(result):
    return {
        "track_id": result.get("trackId"),
        "track": result.get("trackName", "제목 없음"),
        "artist": result.get("artistName", "아티스트 없음"),
        "album": result.get("collectionName", "앨범 정보 없음"),
        "artwork": result.get("artworkUrl600")
                    or result.get("artworkUrl100", ""),
        "preview": result.get("previewUrl", ""),
        "apple_url": result.get("trackViewUrl", ""),
    }

def add_to_room(result):
    record = record_data(result)

    if not record["preview"]:
        st.warning(
            "이 곡은 Apple Music 미리듣기를 제공하지 않아 LP에서 재생할 수 없습니다."
        )
        return

    existing_ids = [
        x.get("track_id")
        for x in st.session_state.room_records
    ]

    if record["track_id"] not in existing_ids:
        st.session_state.room_records.append(record)

    st.session_state.current_record = record

def remove_from_room(track_id):
    st.session_state.room_records = [
        x for x in st.session_state.room_records
        if x.get("track_id") != track_id
    ]

    if (
        st.session_state.current_record
        and st.session_state.current_record.get("track_id") == track_id
    ):
        st.session_state.current_record = (
            st.session_state.room_records[-1]
            if st.session_state.room_records
            else None
        )

# =========================================================
# RESULT DISPLAY
# =========================================================

def display_results(results):
    if not results:
        st.markdown(
            '<div class="no-result">'
            '검색 결과를 찾지 못했습니다.<br>'
            '가수 이름이나 정확한 곡 제목을 다시 입력해 주세요.'
            '</div>',
            unsafe_allow_html=True
        )
        return

    st.markdown(
        '<div class="result-title">SEARCH RESULT</div>',
        unsafe_allow_html=True
    )

    for index, result in enumerate(results[:30]):

        artwork = result.get("artworkUrl100", "")
        track = escape(result.get("trackName", "제목 없음"))
        artist = escape(result.get("artistName", "아티스트 없음"))
        album = escape(result.get("collectionName", "앨범 정보 없음"))
        date = escape((result.get("releaseDate", "") or "")[:10])
        apple_url = result.get("trackViewUrl", "")
        preview_url = result.get("previewUrl", "")

        col_img, col_info, col_action = st.columns(
            [1, 4, 1.5],
            vertical_alignment="center"
        )

        with col_img:
            if artwork:
                st.image(artwork, width=90)

        with col_info:
            st.markdown(
                '<div class="result-name">' + track + '</div>',
                unsafe_allow_html=True
            )

            link_html = ""
            if apple_url:
                link_html = (
                    '<a href="' + escape(apple_url)
                    + '" target="_blank" '
                    'style="color:#c89b6b;text-decoration:none;">'
                    'Apple Music ↗</a>'
                )

            st.markdown(
                '<div class="result-meta">'
                + artist + '<br>'
                + album + ' · ' + date + '<br>'
                + link_html + '</div>',
                unsafe_allow_html=True
            )

        with col_action:
            if preview_url:
                if st.button(
                    "TAKE TO MY ROOM",
                    key=f"take_record_{index}_{result.get('trackId')}",
                    use_container_width=True
                ):
                    add_to_room(result)
                    st.session_state.page = "my_room"
                    st.rerun()
            else:
                st.caption("LP 재생 불가")

        # 검색 결과의 미리듣기는 유지하되,
        # 실제 LP 재생은 MY ROOM에서 한다.
        if preview_url:
            st.audio(preview_url)

        st.markdown(
            '<div style="height:1px;background:rgba(199,157,109,0.10);'
            'margin:14px 0 20px 0;"></div>',
            unsafe_allow_html=True
        )

# =========================================================
# LP PLAYER
# =========================================================

def render_lp_player(record):

    if not record:
        st.markdown(
            '<div class="record-stage">'
            '<div class="record-player">'
            '<div class="record-label">'
            '<div class="record-label-text">EMPTY<br>RECORD</div>'
            '<div class="record-ring"></div>'
            '<div class="record-hole"></div>'
            '</div></div></div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="record-caption">'
            'ROOM SERVICE에서 음악을 가져오면 이곳에서 재생할 수 있습니다.'
            '</div>',
            unsafe_allow_html=True
        )
        return

    title = escape(record.get("track", "RECORD"))
    artist = escape(record.get("artist", ""))
    artwork = escape(record.get("artwork", ""), quote=True)
    preview = escape(record.get("preview", ""), quote=True)

    player_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; background:transparent; }}
body {{ color:#d8ad79; font-family:Georgia, serif; overflow:hidden; }}
.wrap {{ min-height:500px; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.hint {{ color:#a98a70; font-size:13px; letter-spacing:1.5px; margin-bottom:22px; text-align:center; }}
.record {{ width:min(360px, 70vw); height:min(360px, 70vw); border-radius:50%; position:relative; cursor:pointer; user-select:none; touch-action:manipulation;
    background:repeating-radial-gradient(circle,#17110e 0px,#17110e 3px,#211813 4px,#211813 6px);
    box-shadow:0 0 0 10px rgba(47,31,22,.75),0 25px 55px rgba(0,0,0,.6); }}
.record.playing {{ animation:spin 2.6s linear infinite; }}
.record:before {{ content:""; position:absolute; inset:28px; border-radius:50%; border:1px solid rgba(255,255,255,.06); }}
.label {{ position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:132px; height:132px; border-radius:50%; overflow:hidden;
    background:radial-gradient(circle,#b98555 0%,#8f5e3b 48%,#6c412a 100%); box-shadow:0 0 15px rgba(0,0,0,.45); }}
.label img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.hole {{ position:absolute; width:12px; height:12px; background:#17110e; border-radius:50%; left:50%; top:50%; transform:translate(-50%,-50%); }}
.info {{ margin-top:20px; text-align:center; max-width:80vw; }}
.title {{ color:#e0bd91; font-size:23px; letter-spacing:2px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.artist {{ color:#a98a70; font-size:14px; margin-top:6px; }}
.state {{ color:#c49a70; font-size:12px; letter-spacing:2px; margin-top:12px; }}
audio {{ display:none; }}
@keyframes spin {{ from {{ transform:rotate(0deg); }} to {{ transform:rotate(360deg); }} }}
</style>
</head>
<body>
<div class="wrap">
<div class="hint">CLICK ONCE · PLAY / PAUSE &nbsp;&nbsp; DOUBLE CLICK · STOP</div>
<div class="record" id="record">
    <div class="label">
        <img src="{artwork}" onerror="this.style.display='none'">
        <div class="hole"></div>
    </div>
</div>
<div class="info">
    <div class="title">{title}</div>
    <div class="artist">{artist}</div>
    <div class="state" id="state">STOPPED</div>
</div>
<audio id="audio" preload="auto" playsinline></audio>
</div>
<script>
const record = document.getElementById("record");
const audio = document.getElementById("audio");
const state = document.getElementById("state");
let clickTimer = null;

// Apple의 preview는 AAC/M4A인 경우가 많아서 audio/mp4로 직접 연결합니다.
audio.src = {json.dumps(record.get("preview", ""))};
audio.load();

function playRecord() {{
    if (!audio.src) {{ state.textContent = "NO PREVIEW"; return; }}
    const promise = audio.play();
    if (promise !== undefined) {{
        promise.then(() => {{
            record.classList.add("playing");
            state.textContent = "PLAYING";
        }}).catch(() => {{
            state.textContent = "PRESS AGAIN TO PLAY";
            record.classList.remove("playing");
        }});
    }}
}}

function pauseRecord() {{
    audio.pause();
    record.classList.remove("playing");
    state.textContent = "PAUSED";
}}

function stopRecord() {{
    audio.pause();
    try {{ audio.currentTime = 0; }} catch(e) {{}}
    record.classList.remove("playing");
    state.textContent = "STOPPED";
}}

record.addEventListener("click", () => {{
    if (clickTimer) clearTimeout(clickTimer);
    clickTimer = setTimeout(() => {{
        if (audio.paused) playRecord();
        else pauseRecord();
        clickTimer = null;
    }}, 230);
}});

record.addEventListener("dblclick", (event) => {{
    event.preventDefault();
    if (clickTimer) {{ clearTimeout(clickTimer); clickTimer = null; }}
    stopRecord();
}});

audio.addEventListener("ended", () => {{
    record.classList.remove("playing");
    state.textContent = "FINISHED";
}});

audio.addEventListener("error", () => {{
    record.classList.remove("playing");
    state.textContent = "PREVIEW UNAVAILABLE";
}});
</script>
</body>
</html>
"""

    components.html(player_html, height=540, scrolling=False)

# =========================================================
# FIREPLACE
# =========================================================

ROOM_BACKGROUND_JPEG_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBAUEBAYFBQUGBgYHCQ4JCQgICRINDQoOFRIWFhUSFBQXGiEcFxgfGRQUHScdHyIjJSUlFhwpLCgkKyEkJST/2wBDAQYGBgkICREJCREkGBQYJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCT/wgARCAQABgADASIAAhEBAxEB/8QAGwAAAwEBAQEBAAAAAAAAAAAAAAECAwQFBgf/xAAZAQEBAQEBAQAAAAAAAAAAAAAAAQIDBAX/2gAMAwEAAhADEAAAAfy+8zO+rXz0em/N1l7Tm0XUllCYo0DGdyXnvWRXlMdRx0vSsqlpNCGEq0kDKlUiRiJUhDBMCVaIKLIYBUuLrImtzBy6vFrusyLUlOQRJliGAAAAAAAAAAAMEMAbiWxUNksAABoRiVUkwGyVq4xNwxeyXN2QmCgA0AIAEDSVUkFEBamE1MIs6TkmzsnkLOlc5ZrMFyhlIAAAqahkSupkGhmyiAtwjQzDQzEskWkAAJRTms3Vmb0cuRqGboJYADEqSobgGCYwKc1kdXTnXmH0Hp8uvxMxXs8RN0ZGqMi1CuA6dOEX068q19E4tY6DO5QBSKDOdQwrWYKhGxzuXZRStURmaIzLVSqSJgIYSMJGCVhJVA7edZZ7TZiazYqQUglABDBDBDZJQSWElMkpAIKJVlqQoTENkrRmbsiXTVNkAwQ0MQrEAIGkDEiiUUZTZuc02dS41Z1xzlm05OypC5QAAUAAAAAAAACaABCpqVRUqA7JAQAAYDHKmNU3US6FlsG05VpnoogEqZK1IydhLBUUoRTlmqcr3y6MdNJ6vV5dvJ7PofU5a+Y7faw57/MMr1+98Tjx9epfEr1cc3he2WdBk5blUStGZFoltRppzC9t+eR6K4tGukx0loRDQLKtEOgLzUu6wJd1ncNU1zWgZrRWZloQxHrO+dqj08b8jLoz1nBWtYkpkO2uZoS5ulYmlZRAlJA0FgmCbQmANBQiGSjQxVdBypOs41Z2LkVnVXGHoHn6S9iwmXpOUOs41Z2Txh0xiWaTBYKixDBDQDQDQAADEMVDEQ0AFCYCYIAASAAUnNTNwDBJAsYAAFNVNKnUsPVzWL6CXAoQoSrTNmrfTjpyLdGC3SZPt9ePnF9x14v54focx8R7HreSet3/AAnGfo6/OHL995vzeK+t5mC6Z0hGs84Hp8xpm06NOM1O+vOLO7LCqeetS8s9iy5TeZqGRLahytOjN2RmWg0yF6NONS95w3L1nPcuqTmmgEqZmaMi5Uur5yOhY2rG5ZuZTauYN4hWUSrNCGNMJVszLRJSAYqHIyJudTCbOk40nXPMWbzkWaShEMpMYhgAAAAMlNCpMGMGCgMSYIYIaAAAAABMAABghghoAEEwQFAAhoEwQCFTU0ouBgEgXLDSXN1K7XhWd6mblsWsuB7nr5fGX9n40vlLpq65TrqL+pz5vP6PYPzvHr5/0hfm7ufu/J+aWp38mZpZfTNcM9vNrOZ1kle35Hdx79H13yOXDt5GenP7PJSa1nEH6POhkIZQDEUWSMByFvINXiWazLlmdWc72Wbm6mWiFLalqi3LmaIztI1vnUvbXBUvccmmdbkXNAEszoGK3dnO9pSdM2aPO5WEy2ZxW5zRc9ZwzZ3Rxlz0zgWazBYJliGAAAAwABDEDEFCBiAGCGhgyZqRtMbVAwlAATBDBAUAAACYIYJpgAA0AAgAABMRDQAUJoEwVxcsxpAAyUy5dv1ufbydfeXPb9P5/kj6+/jBftI+MmPovJ4vUa86+vPWTPCLLmK1j6h8N+X2eFntXr8WVVKZ9GAes5jl34erk6tOHfDffC9I78dCNM+fTq8f2PGV8/Rh146RU2SB6fM0ykMJGQDVJUokaAAAIAYmFDQMQUkAmRE6pc3ZKnKl0mFm2Kll6kuLtFXgS9ennqX0ThrOu0xrO7UKylCuXzuenNyy5AAAAAAAEDEDEwAAATGIGJgAAxAxAxAADaZKaBpjqaGBKDBDBAAmqGAgAAAATAAYACGgAEAACAAJggKQAVNSqLiVidJNXOnqeT7HD0Px/X8tSt3rGF1mbVzdU0u3z+/G9+fPKa5pqevAErNNcVHR6UcGN9fl+142sFTes+kM49/N35d9zk6ebp3yLjuzrTHfo5dl4/u+At8u+HXhpNRcw0ejg2gYgYigYiGhDBDQAAwAQAAAAAAwQAAySgm0pVFTjbWz3jKrnOmZznWsZ0EatNFoufXObjWRzNlSncgAKgkoJKCWwTAAATAAAAAABiGCGCGCGCGCAGAJNA0x0nK2mAAJoBoAAAAAEykNAAMABNRMRDQJghoAEABAUhoKm5pZ6Zw6myJqbL9Ty/Q5d+HTDffK9uasdE8K1jrzzJrTv830sbxm8prCKjpyQnrFo0l9by+/gxv3vnfa8iXC8tO3D2VZ5/X4u+G3Tlzb4dG+Z6fl+lz6V2cfZx7nge94OsvDXHtw2zqEa0fq8+RpMsFyIagGWIAAAABMAAQwEwQwQMQ0AwTAAAmpzUmsb1GdcDQMQZSGSmpl62Vx75Z65ayJlzIFg5oQwAYhgAAAAAhghghgAAAAAAAAAAACAGDJTQVLKaqUYAMVAAAiAAAAFBghpAAAFAAGgTLEAAAJoAEQ0AAqm5pZ6QO50msZuNYvs4+nn15unk11jV5uaKxdhUWj9nxPd5duHn3yXGLjpylp3LDaPQ8/0+LHTbi7/O1nNp75+6KvN6/D2y6OvLk2w9PWOP1vM7+fTTp8x8+np+D0cus6cux05uLFkT9flABKkiAEqCVaJGQgAAAAAAAAAAAAAAAAACLjNSDG9yTrhicJMMgeapqTr0y2498Md8NZY1cyDsmpoYAAxDQAAAoAACACgAAAAgAACgAAIAKgEbQJNDaY6mpW05QAABDVCYAMQwQwQAmAmAAAAIAAEQFCYIAExEAFTU0ouFvTPTOss9M989NsdMdOfTPXfO1m5VU7mNTrE+54fucu/BnpjWcXG+ctVchesvsZ8scuvoeJ01qcxtGsdk8c53TxNY1WQaKGULSIfodWdeNfrXm+S/Wqb+dcv3eKiXYxAxAxOxFNInRELSVkZCAAAABDBAAANMEADQPLTPNSazvYDeGIAAyYZqmpOvXLXj3xx2x1mpqbJadzNKgAVgAmkBAxAxIoTUGQhsk0qXA6qmuR7hibo5mnvAAAAgEYNVNSFTSVU1NMHCGKhghpAAAYJioYIYIaAATBENUJoAATVgAIaAAQ0hU1NKala0i87yz0jfPSorOs9VZjr0LOsbqR68yOmuPM7s+Tayo0zE1SWa9ed8MfQ45vgHurWPEPYqPJ79uBfSnxhPaPFD2l4rX2Y8lx0YJ7jEwOms3iA9PnAKaAGhKG9FUylvINFAWSxCBDIQwQAhghghgACGCz1yzUBneoG8AwQwyAzVNSdlxfLvjjtnc1GmdiYXM1NqhgAQ2XLDu5rFdTl53rJI0OspOh8snYuN2dU4M0FKbkaZ3xNPpyaYIYSNVQEEXIVNU6TzWwUGQhggKQwAAAUAACACkNIAAAICxDQACGrAAEwSYKpuWZqFu86ms5a1zuakAEGmoMEqCSwnox3zq40zx1ildz7/0vxn0/j9mn59+jfFb5+adm3p8/mv2Nc68N+1lHmXntvORX0WN/OvsE467HLxnWHJXQz0QWd+FOz9vi510o5jcsweiJdKwaolaFmS1gzNFEGhWZcwhqgThMBDBNskaoaYYb4ZqAxvcZ0whghoyVTikXB2aRXLvhLLmstcrAFYriwBwmA9sd5vJQ7gVKxDQxhIwQ3KjUlmxzSm6lG1NcbT6cWAqGEgIwYppKqTSqmpptOABQAECAAAUCAABpygAJqgAAEE0gmqAAAEAgBSACpqWY0zWqipc01vnc0ppA0dxrLJe+dcq9AmvPPQyOTfOdY6o2nl3y0V2d3u/Oetw7+l8h9J80adGHT05VOmUsYbcms5NHTmfReJ38e/K8nefZOWebs8sNZ61CX1tMNs78Y5K93i6VhoUqRBoqgtXMq0SMJVqySlCVCwtFZmWEKgkpQ2nSKCZpCYBhtliyBjfSg7cwCUAMlUYpNTHa0c++IncvLXJGmtRVNwAKDA6MOnOuOk98wHLJYSW1zt1LnbUtPMloxqyoedmu/PvnfI09cwYIAkCxgAqmVUnZVTU1QEACgAlrpLzPoZzLtcvC+5rwHeHAujj1jUBRMRAUAIACTBDLENAAIYJMsVTc1OekDqLlzmp1i0yV+j5vo43x1l0W83T0+pi+BP03krgvexzrxsva83WBImzTPaU9DzunOu3x+3hN+vk67L5teaJwvLeMs9MenLs1jr49eHSuW87nB9MbVz6zWxlWb6/TydeO3zLR7fG3IUSJoZs3rneps8GaqKCdEQXIkIYIZINykpIGgExiGyC5FjvjmyMxvcR1wwIExYz0jKVUy9ya59cKm0WWuVjTViuLUacDTV9GG+dcTR05VrjtnadXLnWzzvKbRk7LIh53JUu5vOoL6ebqx04xm8AwSYQDuRhKJoVTVOlUrAlAAANtsJmtoxjWds4m5qZqkqSdvH28eOmoCoaQAAAEyxJiIABoE1YAAmhXNSzFxRpFy5JrWLQSr1fL9PG+DbC7ero8X0slzdeZMerwy8ZrHTn0NHLu9MdYdxK789wm3Vy7zUY643OUNbxlpnrrnrllWVGeyPHbAN8d1xkdel6Xm+lx7/Ng/b5EAAACaUBY2nTEDmmFZKLcUOUCbKJbJKEgpADJKQhoMdsc1AY6boOnNgKJhOeuWSmlL2Jrn1x0iyctM7mppVNzYDJQAfVzdWd8JZvnNrTOgyR3GZz6sTpRSTndrfOC8rALR9OHRjrxVN6wmAhiZg9QBwTUqqTsqprNYCgMQBtLJqIo1INCzBaQjb1mteHu4c3cBQAQxEmWIAQKxgIACABMRAUqmpZi4p3N51imt86BS17Hj+zz6+ReN7w/W8r0ufTOZ549Pz9pXmip68eok59nrltLWd5Bph0pptp046efl6OKeZPVHTHHpk98AWSb5awKhDtVNXm6zrt9TyNefXzBns8qGqQxEmDGXIDEDBqgbZEaoyNpMy0SVIADQDEDEDQWGWuWdSxY3uJ9MA0AELLXKEmS9aa59cdM9Cctcrm00TpGipslSoU6uXqzri0xOnLfXj3zvFrTWNCo59ukjfG+adc7lCNZwcrfO5cGnVx9uN8dTWsg3EjVZsLlgKTSFU0lNVNDHCGLIytZpTWGkO53Q2sp0hIpCd3m+l5ud7jBDQhgkyxJliTSAFgAIaQAENIqTaiamyqmprJOdc7TUte14vsc+vjXOu+Z6PndfPrWMyej5+U2VDrfPQFjo9ufaa0kEnq5xfTnzIl9COAuexcas7ubNs4je+eufo78d+Ysuncd7ejy6eX29vXy7cOvt6c+/wCcjPq/MSpCVKxKhA0VkDAaaBTVAgTAqQ0IEpJVUoBCgaABAAGWuUqAxvVh0wwBDQstM81AR1oOfXHTPQjPXK5saWdc95qW6zYLFjpw6JrzGn2841UTplRqpcuunNWd65qLKJVkrdEVO8YdXP0Z3z0VcyADAyA1lscqmptVJpVKpRhKDBTSN085vHTLXWdN8OvHTljfFMGG8eh5fqeZjfQDJKQhlkqkiGqlNXIAAFiGkAAAE01iamyqmprJp6xUBFXiGz6vT59fDPd0xr56fpeCvHz1z7cFs1LtNRjpF5VrO9+h2+f08Wn0Pk8u3mJrv5d9s9oVGc1l5fueVrnym965xpw6ItNOa31efmjOvW9DzvoOHf0a8/Xz+r4UT+x8oaVE20yNCydEkQ6IW0mT1iyC4SkkCGAMRQSNkttZLZmtBM3YsYdPNmpqsb2NH155GiiFoqxzuM1AZvUJ464a5bJnF52aMcs7ZdGdqqrO83qpcto6JfFoPR5UwJHZFoKJ1zqc+iDObjWb35Xm7WVjeWksh5PWKgmtBAkFU04SaVVNWVU1msbUGSyqVmuW+U1zdPPrZ0aYLPTbDTCM8rnrx9fy/W8rl26GxUrRCtJKqdSRlkJlwhoAEEykDENIAlmaVl6Z6Y6c7T3y6L5NcdXPNW+Xsvyjl1+jnnnh6e3wdeXt51NT15Rc3c7zrPLvgw3jt9Xw/V8/q9PGcMo8zbl9Plv1/F9vOji35s6wx2W+WEb1Y+jn157rXLXGtOXq8+31unOuXTr10w59vlmP6fz5VqoblGkrLcTc1KEYAJliAAAABgA01BBSQMQOpBuQrl6ebNVxeN9hL6YQ0IqTmi4yEyXopPHXDXLZMs9Is1pXjc75756PStufXJdU51xdmfUfOq16vFmXNkg7Jd6SroT59p59sdYzoesVoY41r0cesdGNa4154T35PWKlKTlzbKBoJpCaaVc1NNjlBipUk1y2ymuWh7xSrXO8Z1ZzT0Z6z63k+p5vPp1GhnpBQZq1ZnOkXCVTqQqVwJupGkQwQxEmUgCE5s0vO87xY9YVypct8dtc46OffO/QqL8/p5+D0vP68kmt84ubs7ctcePpxYdON+l5fbz7ehz6xi8vL08/fhr6fk+vjefP082bz1nvcUXtz1xVd1brnzrr8+O+z0+rj5+Hf1PO0x1rDT6ieff5l/U6S/G5fZRrPxGP2nnduPzc2fQ+bmaymboqFo0yNEZukSwAYIAAAAAAAAYQc/Rzyq5059NqK6ZmNoSZ0mzmlrIAl6XNY68++HQmWemdm+sa8+p0ZdfPr099e/5vT8vHUprg9HD3mfz1d3H7PHzuZ68QS1nXTnJd5zF2zFBLWsiBNXk5e2+Ls5deMN945zTG5sVLKaqmnKJoVJl1NStjlGnKKka474TXORXTnVZ1K89AgpWepwel5/Hv2vSsdcF0Sc09EazhG8axirnWIVFzIykqSJUWSNAmkQ0RNTqXcVnUAXLi8qWuOlxPRz6y+poaeX2cXB2cXbg2ttTmvN6x3ZXny9ECN8n1cvRnfoqnz3wc3Ty9/Pft+H7WNrj7uHHTDXn01z7DF8+j6eToN+Xeca4PQx3uN9ufv59uXi1nV+2rZ/N+nOmrzOPHvyt4OX0+fV+D4/p/mPt/CEHfzjloNFMTBADHBRa5mqMzSDMaB0EFhI6I5uzkg2x25dd3T6ZynabM1rNzxJrIAl6Li+fXn3w3syi4Tq0y059tN+bbHX1fX+f9bzd9N13Y343t/N9bPz3J9B5vq4+XPfHbhxHXFxzvUqGyE1SobE6JQFLl01pHBpFay8rmyC1ZEsuWxqlUqNUlXFy005oacoNG+O2edcVI6c3LFpDhKg9Xh9Hi5d/Sq9OPbnXTK8mfXjrPLHRlvGEbRvniWtYgpWJMRJlkjSJUqSaSJpajuKzqQVzWXQ15NOjWOHbRHqV5K5dteYOvE6+L0ZrzCp6cuzO45eiE1rm+nm6M69G89ufTzebp5u/nfteL7mN153peVjeIjpz2rB4u2nJpL1acW2d7b5GN9fqeXty6eT6Pmez0fYXk/mfS6qx2mYx24GtcHFvJ8N9z837/AB+IrX1fjwUJLoJuGWSDqGW8xdCWDAJrGNVrjTAJaCuLs44NMr579AzrYSVyJK54wMgHLtrlfPrhtlrZlLVnReVc+mu3Neenb3eSufT3vK186X0duLjr0+Dmjpx2yDeJVRrBI7lMQO8wBi3V56cvVlae94freLz6rR4dOW84WWpEchZTTUTUqqasuprOqacracrTDbPbLO+JUdOSaFYMVBL7PF3c3H0eputOPaM94Xmx6sdY5cujHeMctc+nPObz1hDLlKlUjElVNiTViTDOaWsuouWJtXNDylus6Jeu81VTPPpjnrHTnn28vTLxO51jpyvPHWU53zrp5ejOu3Th059Fn0LWef1PPlPT4ciVkGpIUzNhFTprnWV7POn28ffy6+PfUdJ9ttyL5f1u44NE1jDC3swwy1NPP6ebrj5merk+x8JoesIoJKCSwh2EGjJKSjQLn6edOnNgikIAfL1c0sNGNdtB0zFSwVynEmsUYG9TWOuOkWmIK51uOvHTDfpjn15c+rj3ju5unjzqcbx7cO3iJsLz0ubcdWd0aKVSI6ODaIyWisNMGr059TTO9s7jm1w1h6Z3c0DzpJqmDBVMqpOy6m86bHNDCVjcb65dvPt59daOZ9AYvVSzdazU8Ho8qepthrz61nUGWemOs44b5b54565dMZxpOsSqViVJEBZKZZM0rEmiJqbHeeik1MVFKzMpXPpejy9Pk9uhz6zXlc22Xp8u/r+V28e3DydnL143G+S5JrfLbTPp59vU9PLu8H0vE4u3zvR5XXM+vn6K5nLu+dR05ZmpctJcDlXRyo3hWq5+rns+215Y+f8AV6lyKzpjGbNYjOrxWO8Y+T6/mezwZjXq8bAEwBgMRDci0IGJhBjHscCeoNEqGBy9XLEDWNd4V0zzXnqtyxOFMxRIkvfmqbtyAkq19DyzOvW8/El7cudWdnLKs6edKxiLKcEaGYaGYarNrd4hu+cl6K5iXrrkc12VwEehp5bPQvjc0sJN86UK52IuVgTSqaSqm5qmnNNpytpyk2SxVUQ6cqp9mdc+ns78fR4nR73Vz385X1noufwM/b/NV5OO3X0eRn3ce84ZaZdOUy51hqehMDp5KaVaxKaFNK5lNVE1Nhvh0SxncFZ643JplvYtsds614fQ88rSWvZz9HJjadLWOjDbLHbCLnrw29Hy9+fX6q+Dp+f9Tn879C+a1z+c29Pj9Pkz5ejk3z7fP9HhOZXPbh6CJ8/p35ahOiAQWlLgqdfez808T6Dz+Gc9Pps/n51z+gz+eivoM/n89Z93wufi64Kzrvw1YWAwAAGKhsljExk5dHPLuurluWNyyxi5O7imom4xfQCOmcNNKzpw51niQYTScFRS6VLm8lc3KKQpqLExgAAAhgAAArAACGJqAAMEqCkt5c3o5rN3giQrlOasdJzWiHnU0mVc3NUCzavDWWnnpNNjUG5U2w5+jM4ZzXbhuZ1NU05UnNkzSuZVLWZVKxKki9Lzt876MNY59I2w33hJksqlczNKs5ubHvlpnWKFrOuG+CLp5umxk6Z1ryd3FLpjpFvo+f6Xm41vFTrOmWmOdxLXTlW2NzXsdHmdXk9sGGm+XP2+b3deMF5Z108nRymeW2HXj6EO+Pong7sbjfp5dMbnowIWdLcBL0+e9cXy6TKO3IAsYGsGF4wdfEzomZs3I0AaGADVCGgaRMqc66SSrciVeTX6v5/o4PJ7eTn2y6+bpUTvGk5arTnWzhTUgDiehqaiZqwaJdAtqMOjC5GOkUyCgkoJGySyWSgQwSoJKCSgkoRa53NPSNJqMtsUlNWRc1ZTKzplGdxWlyS/o/J5deKPrfLzvyl7Xn1z79P0nPp8tPt+RbDb3zkpDaDx8+zj9Plvbn2zrWp259sp2zsyjSNc4VLeJVKxKkiuGdcueXfLo5unfMVKWVU2KLlImp1NaSzvKXe+d8/VlnWHVntZnrGkbcPVyy7Za5L3+f2cZ0VlsThvzzUprpydw5enfj05du/i7/Mh9vB6OsGOuWd68vZyWZYXHXh3aY9HD1ZxjNx0acvRLr0X6PHt4K9by95eCr2+NxrjjY3p05Y0orbKlcY565k6Zh6nmen51ze2OyjijTBEtXi1bVCKmMqm86nfPpXNaZDLs9ny/W8rx/R5OLt4u/i6prDpyZOmWtcypXk0s1zsMLymm9HLiFVTbmpx6edBlWDZLJSqRgmMEEMQrQWNAAAAANDrPWUel51jl1ctSnNyqm7LpPG+qnfH0cvq8lyej6fhdfn7fRb/ADXlS/d3+e/YXPo9/wCcO6+q+bl1zrqW5yvoE560VnP5H0Hg9eMbYV15dOnO+fbSJVlEtlTSsmaWspNWJgm5FY6ZdnH3WJaRjcTS1mI1zshNWb564zWd5G+WwsprUx2Qp6TWC7OYrHXI6+Xp5k035t5Tn3wbgDfJtOWryvN9byPS8zO79TzPTIy0xl6uLu4TDLbLrw6+zh9jz+vxN5rWK7uH3eXXs96PvfH3/KvI+1+b1r57nd/Z+QYVzZvbnlvrOe3M7NteXTWM+f0PPG0S9PP3+fvHR3+XpnVeh51azbwM66ubaJa1x7Th7M8Mbh9OuN+d6PHge/4j0Xr08paz9R4nd5fn9eeGuPTy3CnWL0y2rHPfKzO40KfPUTpnVuwjO8xlyxtZnTIekayitzWS0lJnRWZlqyRpAYoANyGlYkvQYEvQc7OjTkuXoOepdea8rJGtYmk61qax06tua+PehaM79Xlb899fThzY3n9L8/1Nc+k1qaXNZ35HPjHr8PXv5+k32+z8z7vHtv4Xrch4Yj2eHR5vOrcC2SS0SwE7EurmJQtZvTDXNn0fM9PO64jC50MXrHueX1cfL0TLOnLp5urjmoA6cdctJms9DZM9nOOm2M0GG816HD0mdcmmHRrCw3wmpB75sKlm2pe3zumJT0fO7c2s3lNdnDvyWTlrHTl0el5nTx9GY9JcvV45xr9D+p/MfV8Hr9/4L0/leuOXXG/s/Jnl6ubLelrqRDkoFrERrlK2me34Wkbw9sNc6snpmuR5tOm+Ss67OfNqxFg7ebEev50uWmnIbZnUbc3XxY7Z4aReXSydQDumuDn6sLnAqWQTFcaK7axvMRrNtVNGO+KXtl056ZIyNnzuzZZI2WJZpMCWRQxMG6lh6XNYPaSE5uS4qy6ms7fPvgkprWU5qzVjx01rN8+jqBFesHRqTy7bYma9WnPrNbuHnXzlzPs8FFEq9Xz+3n2o5983xX6XN388erXTz64z4/VNzrOW+Oj48rO/my6LIt89jhFjoFn0fP8ARxvjy35d86kNZ7ufbHl3mpvWNMt9OfXzRrv59QMbzOvU6OvXDy+zPy+/j68Nd+bWb0zKk461y6YnDfHWZudLmujT3PP6svN++8Hy+n5E3y93ht9W+N+aexpm+Gvfcvz0/RyfNr6R2fNv6EPAfvZS+RW/PvDMVrIM9fkOTfnjo1yKGqubqXrOME5tzIvqd3z73z9LhynO+vWfa59Pmncazv18046HZ52++fq9fz/f05e/83E532+Lrjz6dV4md6VqRPPvzrjltlc9nUuaazzWbG1YaVzlqyVUpbHNUBmy07EMUi8613w6OfXFXNImbjSZLARYAAAA3LLulyN5lzelRiwsLikq4qbfP0YJKa1mamrNqmufShE0qhp09HmPO/SXN0Y6Xht051hcM2rFzXg0vS9Pj8097LO/IXrI8q/SDy2s+nLqrHKXpnm3NteXDOu/PlnU664tU9ZOOHp83Go9PlHLua7fP6c6zx1jWE2q68dM+fZXF2dO3Npx7+eqXo8u3r+R6nn9Xn1z+j044YdCmsNculHpPscu/hZe5xXOXLry9Oe2O+Vkaxqej63i9vk93vc/zBJ63mfReRrHPfH1dOXTfXx8u1rm1ufS9Pk7+HT08/U34a+R+b+v+O9EDlfo85zrbeOVerjZ594aevy54a4p3b8etuZIympG/R93fP5Gve8CWDr24+nz30RnUe34zjI36FxjVERpzpppzzqdJmY30PnvOtrNcbjj7fP6c9s9cu3niLjOuwXrZ6ePzfSeOc/VvynHGkdOAO828dspophzaQbx05KsbU3Nl75bY6zGkS5RcdOSelLibqMDWbINGZmrmsTXU5jqUc7DWWBKXFjpOaeG+ApqdZmk7ndqufVDmWnirKiizeubXO/oePgfDv3+fWus3rjOdcL1z7cd8lgnb1+VEvqLyVqdefOb571zCdevATXrx5Zm+i/LnU9efJ2j0ubnwstRXTm3NC2yvNI0ysuB10QnjorjWXOsdrMgLnTp5Jz017PMtNa56sr0fO7ufWvY8L0ePbTyq5unJ8/Vy9efVlrlnS1y0Ono4t+Xfk7cPoLjT634zo8nox8T0vG9PDr34dK9Xs+d1x0+ijzeDL9B4/Lnz93z8mfq83lxq/R5Du4OnOvV58Xz7eLsj3eI4+rjTp0iSbzuiujlTt9nzfSzjh8nq5nXX0/I38vu9vwfrPnOPbiCPT5L7PPcvV1cNZ6ehWWPPrvp5z1jt04+dPWz8vrN64ue57vO6ct4ROvbhgmZvV7Xz/bN1wVlc0ppmBVcymo6OTq52tFVxxjN4YC0lUumuW3PsRpnLnGs7w7V50Kybxz6MtYKblT0JvF3NznNq4hp6wA1VTaVUvOnjtjUzU6ymquehj5domosvHXKzM9PKXhWnXvn59fQvl2+dr7/AF56/PF9/wA9nw59v4m8+GvX5N54m53y1QpsSVzTyLNTMl1MQ6HzOXpfPU1q8Q3OcOk5g63xuXqxyqytMtJVFxYb5uanXDWXnarfPo5Ovjml0c2muem2F52urk6M7XqeP2Y3yHXlrOfNvhvHVlpnnavK7NbyMbXseH60mnZwejw7+djGXbltXNdT08nRZ2Zazz17/kdPHy7cvR5nod/P56a3x2rG5enSXnp6/i8C9Hnxx2y1jo3weemL6IuSVpYbaYZ0+Tr5OffTfn3l9/Pk9Pye35rLfH1+GQN4Kz0PSri38/pMJOnLEHvmXMm+chaqInbJ6yripfT9zi8/PacOjn1z04KLzg6M4htGvNvlVRpkBOiZpmhcaSnRz9PPq898c7zNJ1nRmvPpBo5vnz6effO7nbOk9XjtzOs9c5yuN88Sp6cRp2KotKcvOqy0zpRpFzNTdnS2cu2MaZ6woqN57spXPph28m+sd/X5lcPR9dt8bPPX3FfFXnX3HyXG9Tfh35+vPz4qPT5dkE1E1OsdvZGnn9ETpzG08vfqY4ejnm+VUV25AACBiCnLlJasNM7lEBYTLG/PtWLHcb8vThN5ax0655MJa0gz0fp+V7fPeHL6HBLz4a49uPTnrlnc1FazYlm19X8d7XPpj6Pi+9jfz9xPfz7vHTPXLs4eo125+zLu8/t4+fQrXOzzMOqOvmjqz9Ca6OH1PP59vovN8eNReXWXp8vs35DmvevwdMdM31Z75YaaepZ5eO64+rk35ejfLp+l+Z97y+3yOD1vJ68IQuvBVK1nToxrHR3SzvLKlvkyXcibEkFAKa565vTye/4WpgtK3zxbzTYKxo0nTn0XN04bzeWudYsLlgBpGk1PVzdeOmnN2ceOmk6OWtNL5dpNFnpy8/bz9eOnQt+fXqrv87zezhz007+bgx7ubrx84qPT4hFWTedpVTU0Z64hNTcqpuzsHXD0cue2PTnEtb506JuWBTkzbcSamQaxKppFyhljE5YVlzs8HnXR08Dmu98RnXXXnK5h6PecjZGRqGT0DMuBJq5nTOwrPRay1xlnTLXWJELc1kW8xNCaXWazzqvR43jfVz5JXjot89stMs7hp750mTWXped72NeT7vj+5z6/OxV9/M9c+nn24+nl7bJ9LzvQ566/O7uHHTVcz1nPLp6rOT2ez9B4dfyrl9HxeuOLPr4/b4jDSE1NMrL2nTHR7ej7/l9fxnXy+n14cGeHPZ03wVqdPZ5vscu/Pw/YZY38lPr59ePlT6WOsc20tWPOVzJrnpIxKkOpZUhLv9R8Rtz6/Z8Hg+pw9W3Ni94hUbxmpWubeRc6YdATlqrnlez1nAasNsds6ns4+3HTo4e7i59ul2Z10bLu8/qwz9Bc+3l83r8PXhfqL2eHe/N+x+U4dPJe2/Z4nB699uHyL2y+h8mFHbqcdzrcqoqWsryHFxrK1y2Tubfn9fLh0c/TjmmunPRNZ2CdjBRUVIwYgBAWMBYzudc9L1vHTlXQzknpx1jM6cbINvQzryq6c7Mjq5hNsKMzfXgUvpcMsTl6y9cdpqsN+YVS9YaEaZtCDRI01WdqN8ZrB9C3yxNJFeVL051PPrLl6zWmEHZr5zl7uryrzrtXKS9S5mb7cjl6u3yVL7PFyM9Hn5g36OXDO/sPQ+BOfT7PwPPS78Pr+V7fn4YehzWd/D7VS+L6vrHHv9l6f49p4vV6fm7+535/Gc/TzeryZ+l5vry93tY9Hl93GeT06z1nkcFnocD5e3m1nJbx0R0eny7eEe1x2ck65b5JyrKuJLI0OfWVZu8njpprzE11acLl764bzrbPGN4lbc2+W8XmT3cHq5cCa0Nstc6XZydOOnRxdnHjr6OnNvy6d3oed3+b27Y55Y6aR39Uel0+pc4bfOe55/J43rY+vO3w8a3vt8Ry+jyfY+Fx+n53ZvHHvjrcy5YZ65ITU6ya5aS+g5rh6cOfp5t88k568dBObEwAIJpU3LgBUAIwFiLnXP0TRcPRhl04aznGk7578/VhN5+n53pZvJltNzrx+jwqujm6afP1YRjca6yc/VypLRvL35+jOlz7Y2DC5JqUYCrXKzZOcb3x2wzujTDfLaICSo1NoqMdJE9YcXJL9DXOuGPo+Hn18g6tunLgPZ8+XnKnWNe7j359fR18l8+vdHOld5TZ6Xb4XVx7vDI6c98Pq/l/R5erm4cl+p6viiPqn8q1+n1+TeL9avk0vucvlVvn2Ph2s6JjbO9evg6MdeLDKu3mUzesKqiavq5nL6OPnXndyGsSQaxZDHUtamqllus7zKVgArcuHNSa8vTzWb53CT7Hjevm+cqLHr0Rjrl0Pqx058HJrXMq9fo8Tp49/V87kD7PyPH7Mb+n4cuzl0z+0+T+v4dPP1/PI649H0fkfp51+SyrP6Xys9ufTXOLSuWwWsdckSa1k0z0O6s78/qz59+ffLJB15UxTTSBtAAgpUqTQCaMEqmnceg8dePdYbY2Zzcbx28fZy53l7Xk+rLy8vXknRwel55n0ZdFl8ndwmW2eus1x9nHcyBvB0c3RncY65XNlJZm4uWwFUWak1nemG3PL0RM6xq8gqBJrFTNwBrNJkaet5/u8PR51Z9Wd+d0TWp3ebTk5+7i4enP1eblq56XyUdTx2ztiJRAMlHsno8eOvhef3cPq8XfmFcwKKQoGqXu6uDuzvg6+Tt59efq4OoinyWcrmu3mjp5+marLScdejm1wMrzvrwq46OfTGtqz053vrLyP0OrG/L6e/jzvrfDzzXXzc8dOO0Zm8WoVzakpZ6VczG2KT6nmd+dcjC56J6MOfZ9nNpNc6RrEE1vD6Oesb1x0Jq93pz7ec/oLzr53o9HC5nA5NTWss94Th74zpjpZSpZoai55dHNcia1kubjqvOuXonDXHXPNM6YuamaExBoUTSU5aiaAAYEQOdY798duPo50yzHHWd8+vl7Mc7fVx+lnXDn08usd/nen5ctdPJ01tx65QtM6rXz/S83WJBdORvhvnWUj1nRTpnecbOzJbJMdKQ6ipbw1yLWudylVVknCbyGekAaxQlL3ex43o+b1Ya9M51wXlp0xrPRwxPB18vbglsazibUnOulLzvaUzdId5JfevzJ83u9bxtb1z5TSfR5eaaSNNDqal09byPV5d+Dt4uzO+D0fP7rnk4+zi6cVSrfOd8dc9LQ8dKw3xs56R18+mj6uXfKoiXacwozLAFZUgIBAFTQINA0I6OXoylz6+XprMojrv0+rzev5p9M9ePFd1c8ls1G+31ePb52f0b5rG/nTXL0edklm3Z5rzr0J4fSx0w57x1kjXPfN6ZaSq3pNIrKU5+jDfOULXOnNL0Xz3z6PGstZoWlSU5rMtJInY0IbQrQA0wVEZjNY9Dfn34ejlQaY51PTj6HF18eOm3q+T6+N8nF28Wsel53p+bLn0c/RuE688ka4a10+Z6nlswB15VpFZ1jU6azbZz64TS6cmVUuaqbKorOpo6ZrmXTMuK6EYLWNZSckjLlqka+1x+z5vXlxekufX5z0PQW8Lj6vKhcmdevxVJVkG1S4PaSLZLCtJNTFd84HPvpkK5qbjXPEDWaTJRiNfT8n2OXfg7OXfO1l1Zy8vFpl6PJoKkblzdtGd64b4RgB28/RpjXPuqhM6KAolWUpCnDpkiUIAQMQMA3vHTn0w6+b17ORfUVy7fO7+xxS8fHa3ha4ynVga53r99+e+55/R+m/nleHx6cGfXw+7yETe+ecdVnN3Y546dl8EL0c5lvnss3Zbm4zjTPWHNRZKa1i7zvOmMms4qdYTRqVWblsza71zLOuk5g6DBmpmxl1NQNENq49DTg6eXaYJ1MqNNY24+zkzuvT830c6jh6uXWfW8zs48XLp5evc15evjjHfDbWery/U8ogDrx1VTneeme1yhTNSC1jQklrXn1mtZqM6gefTlrMe3jfk6ejlz65ZdPPXOrz6ch16svm9HpnHvWuU8u2+/LtjdaZaS9Pger5O8eOyff82iBNjFLtObS0gc1NMlluHjpZNTW2XXypzgb50JysEr+h+c9bl2y6OZ51o83L5ue2Pp8m8XnK3GhTmsdNubp5pcRrtw2vO+fWELWAAABAWMlFkCWpCqblTGDKlRTllrOzXbko9Hp8ozu4zyud5xqy7xR19PC+fXv5sNpr0MuWM77seN3On13yH2HDv8AY/G/pXhfP9H5Zx/R+F9TyZJR38+1YOOmdLx15cuyNY5p2WsYG1WY1qSwaTNYRqt88nash2CEyhKUip1loCkyErKhsEwlp5i7VzEvWuVr0Rk037PNeddeEUelzcxnd78tXPq8WazuNczWO7yu/gIA68d8tsM7np5+hM5qalNaxacym+G81ca4Y28ts+nKfa8j0sdNcyufXCLjfLnio1EC1hgFa87Xt38qsa9rq+bMdPref5kl+gz8R6nrc/N0GefdaeYerqeJPsc9nnLvz1njOmbnF9WE1N50d3D2cUsDW+bacoMWfT8z1cbnDt4cdN514Tnlrv5erLfHHTLTO94ty8dNcNsVmLW+UU4uaSBoABiYAIGKiTXSWNVGdalZy00wQiqjRZN1LzruqPLWy3jN2LDojVT6fPt59/TfO8+tLnesbVi16PoPmfU49/1f5/zPA8XY8nPn+j5bwI7+V3t152MfLuN1Lnn1yeTHqz05eY/TDzX3Z2ck9MaziaK5zLVmNaCZrUMVsrMzQIKQhqwTAEDQAAgAIZUlIQxENrNSx1BLpfMHVlmKBVztz7881W+Osuc1NzILWdJqZTo5+rO65ujCXTDfn3zfr+R6+NvPTPHXEa3z5oqNZQFywBNMHNCAAAoBZpMkaQaYJodQGzxUvrOax1eWily4fUVnkndza55tVSBQvW8r0s76fM7/ADs9Orh35N8kF75dHPrnneV53rFXlpneuO2ed5q53zmaq5zNrXmOpy8tdEmZTJY4szRsYhvzaRZJJZbhGihlCZTgl6dOJS+hHGzecgsgNNuUl9jzciapI1kaEolrSRKxMzarWfoYS8X0Lw16zg26ya5Y6kcdazYqKlzz6Is589o1jGdFrOaqdZlUXMKwznVazmaJILVQrEhWrJVpJVqySglUWSrRI1YJoLiyXLGIJTVy2qlKVTRnWdl7ZEu8ZaTWa6ROeeqTDom1rDXE1598N8z3/A9/n0xw2587E1rPLFRrADsABMBUqECAAoCWamrJABqhACaYDR6D5DOux8Qd551y9r4WvRy6bRwHZyai359435eyMdOfC468TTTTOoz6uEzuNenOzZcuyioJrF759ueRjdJLWaJBoEGmCaBDsTZCVzWaZYJgADaYwJZmpsbTBgACjRDEDFayaXm4NLUolFpAXFHqzc+b1zTzq7x1je8Zx06jlR2vlc10Z5Z2aRoJznRNmU9GRlOi1nKdlc4mqszWisgsM1askaRKys1oJmtVZmWiVZZmWklWVDbTIoslWkgsqHQFTUsRU6xsnOduKmyWi5pzUr2x6M7nHSK159sbg97wfbx0zx1vHTmSN8+WKneU1SAAACqaBMECLAWamkkAKmhJoGmAB6GndfPrxadLmuO+xy8+us50LWpeLH0XXiL34Tw69fkl+d17uTt59gwz0jnZ185omtErNpJWSx2UhSskqnAWTUCujJ9Fy8t7Ih3mPLXNMgNRAAAAANBp28PXjoBed5XsS5WKVUtFW+e+Na7ceuOlZdEy/OTU+354BYxCvTPSX278+/N6u7Hks0TlalTZpJrLmqg1vlhehc93O84hrpnc0xuV56uXkjtLnhXTVnEdEamQK5AkaHYlQIaQTVIbJVpJTViFVkDZLYSrVklAhyZJm+W0XGeghXMjLl1NzRtned5yGsWmSzrmjSsQ3WIKWrBqgAAAGmAAgRYOWGqskaCpoSqQAGCPojB8+wqSKjSWXrtLhp0VNctdBNY3UxOkIrKwxz6Vc8k9hZ5nL7rs8LP3s5fAj3+bWPJ0vLeLx3o5zrE5a0CLLM62cuO0ayyyDbPKLKx1zswaesoAABAAwOjs4NefQSKpwS28hNq50vYuMO6eSpd656OWWuvEAGJhrlrNeislw767cRXacJHUc+prUazWC6WclXhc7qUrWLs6JkmjLRWRqtDRROdNw7LOcOycLl0zmycdtLORdonCusrkek2S2Ik2SWiCpsSbIVlkFhLaFnees5XG2udqpx1FSEqLJKBgRhU3vFASiaGhiVIlNWDQDATTE0xggTRTVSxU1STSFTQJyAA00fd+T6HqeH6Hz+30nkWczxw68uxcUWdWWJZoRZJrcc51M5a6Red9CMdaUoSD0glohyxzdrPIXsKzx+f2OO54J9E1nhV46x0HNR0TGko9EZaRqkcndwWc4PpzSaAEAAxMvfn1zq3Ey6TmWbGAu5zh0LENTITWJRBT1nM0CCwjbLaa6Gly66ZjMjZWRetSwUSybzKmkEUrCpzNnz2bZqlozRQayyillzCdGWZUjdy50mUc6jaU1q+eY2WRZrKFlXVmM9MmC0Vma0SQrLILRNTFnNq3vnQLOxAiKKl0hy5TPXLTWbQ8bB0QtEua0mzMtXKm4sGIAaAmNNKgEqpqaipqialCpoJqQAGmH2/0vJt8f7V+L6WNnzGnvc/r8vkvpx6ck4mtZjQg3cc1dVnM+ol5tNZJTSynilnPVlnOJ0PnhepcrOnI7Y8zD0+SubXYOSOsTgfZVnnL02z58+nzVzc2saxyHTW8ci9PWXx19Bcvzh9Kl+cf0BHg16+Z5k9qs5XeVjEwSdjEikEqHSQa6rzPsma5jq6M3zr7iXi3i11rFZ30ZadEvnz6MWcWnRzlXgFOwSESq2TCllW2mGsumYRnj0zrPOt6uec6IqVpcuOmzzvnCrLWLleWjsxbNQeeqKo0lla3NZhYmZy656QLLqo4TqVzy59Ss5DTPeLrNy0gWFSuUNkzrFmW2N6xoZvOrFSyNDSQyRHFTYAXIAABU1Kg0luamoqapJpCooE0JpjAPrayfD1aa4VL39Plb8e3pRzPn0WOmO+eWemXXmRnlvn17cbNo5EnXnzo315tlDPQ06Iebz8/cWcR1zZjbhdN+dy9z4Lzd5z1EuiF54c3JDZgaq5nLR0dXFmenhxI3zmkyouw155OxcEHq15ZL60eXod786j0DhcvVHOy+bbWzy17UHnZdnNcloXRzjNdBw63O0VC52izSTSV1E503nGsbVjUusRQm5pLRGb3mBVcuOkZWaRtovMatM611l5arRcs9KTl0vLWTVVK3hkda59Fed0RactZVFDU2OCkzrTpXnVuWniS6vHM7OfIuUD1mY30l412lcS6FZiqm5modzqRU0xuINEuaubJGIs9ctZALkAE06qWpWgSmiaTl2AIKlgmgaCkB9VOJy76mFlEqLFRWk9XPqu/S/N6ebw+/k78Vjrn24YV6PRHl9PXK82jqXOOlRlVTSVkKp56635uSetPjZWe9HhTZ7uPjFnqR5bufQfn0dmXKk3nnVmiRZU6ksdEaK8yoESEt0S2ZzrKJatc7txm3suD67l5N9spddOKZe+vOZ2cuVjz11l49XmOYdmrwhdVGhSkGRnZos9LJ0WRrOeiC0mFpq5vHLWbmXNWFQo0edGt4zNPSGnTy7RN5VbuUZ2Rtcy63wweg+LqztrWJcbS1lc282ZKyyEp1GEpo82AqFcMuGSxSdiEjeBS6ynKstXZzLbbWeV74iLzBCsZAVjpnrABcpp0gCk1KAJQDUtNEADTBNAAjAX3303y78t9NRzVulyNZMLiTpvjmX0cc9+fTk6Dl1n0583PWPVXj4WfQYeErPYz8aLn1o8+bOvPlVnSuSrN5ytLWdib0lyfRqvEd2kvAdlRy10wsUsjpmHKXIWnmb3zTL1vDRbC4znZGc9LXme8mOfVacT7JMbzyrXPTZOPP0iXzY9Qs8qvQyON9uh529ZGkLomuOPVmXzJ7+fWOe73OWOwlwnqyMLvOzTTmZTmlixpnGpZNCi0t5rLTSs6xdoznqgwXRqcd7QVd5TWiwsZGhlosbNJxnWds1mdBhqTFanM9NbOOt2Z1WC2qRazCiaSZ6EuFbqMqCwmCy03CozGBQNLMaJMlqWZZdPNvABcJpiaY05VgJQDUtNEAAMQAAIAL9e4y5d+o83M9VeNKe1n4qs9bLz0m9cxZs+YOzPBm2edBBVkc/W05F3WvmnqI86u2TkrpRjYy9MXm9CxlbgLEtNY5Tpa8x1Bk3scmtwut82su748j1MuATszzArMsbzhOquO13WIaEyFTnZreJFVMGmmTXauZHeefcvfPHcvVzmhlXC7n0OjzdM77ny3ne0q5eWNsNZyuZ1jo5enkNBUI2gnpz3zrWcaztxvRyz1ycd9GlnFl6eZy5+jgc3ZMjyvM0yl2ZtxqVfOrnqOS5d4z0W4upeNdGms8l3CaPANQqalWkp0Z1z6zVirF2b5ygbzRuFWkIVgIDalS4ctkK5pAJPN1cu+YBrEtOgCKmpAAoTVNMQCDTVAICYAL2KVGkSwAEVscz7NprirrJcnYQ1JThLttwKOqYaVCKbhjSYUItxMuswG6yDoygGUzlrWrMp2gcWowpPUaz0gZBUUhXEVqYWa6YEdJzWut8qOqcyNYzuqaUukKzDHui55NTKzXLTSXG1FbPO5dM1rLx6681z1a+d1TW2nLWdd+M3nXO9OSzqxjrObTp5DSX1S5a87l104mdz8xL6XPz7G65oOpYaLFS7GJSu+armV0zYrwzN8ltXOdeJiqesZ1vEues3KLPVc1vSYGkoGeolqlycqzaMyW1DqhOEmWJAANExq2nLTlDkKQNJ5Ozj3hga5y06GnDlyMAbTVAAAiaYACaYAL6d5xnWpkG98kHUYyaznmmtczrZZ3E5dGtcr7al5TrqXkfUS5a2SpzBqufKztPPZ2vz9DsjGgzqbJMZud755Op8lrvWZLcao5nqrMiWhNFJaVGZu5cF12vC+9Rxr0KPOvsF4zoac8dgvDfZmmSFV0KHK2Xn01qMa2lcY6kca7BOSuiV5cO2LnC8XZ0md53tfLU1MdOFmnb5ZHq48nTnYjNRKNZpsJhu5blF3zUGuW0stwbQiWKk1na8FnWizdl1iHTE1LthIJaxciSrRYNNa5xXebs0IJqiXANUySGhWAFAA2nAMVtOGmLCqbEDRcnXyb5sDWJadAENNUADAlBME0g0wAEBTAl3bog30lxOu5eHosJBSkVRlTRrXJmdhzo6p5ZOvPnuxuGE1SQWLkt6OdbJMr1Szo84udBcForJZJW2Cjs18wX078vSXtrimX0X5Cs9i/ED2l5BHrZ+fR1xhVaXzydi4tDsONy7maNnlmdE5o1Mkm9Z5r0Pno3eLltAamOZ0QARu5eLj9fG58zRTvG+ee81FTBZk7Lcpd+vzNMa6J3M9OetaKhE1zxvW+eD3zImqTN60uGmuMO1IZs1ib0csK7lwd510ZZqVyLWWSFJAAWCYIGJpFEBZAWSFEtaRUIYKgVuSNJQICgAXH28W+bA1zlp0AQ5pCAqgJU00EANME0JoqgJfX2wjG9zkZ1Tzo2jMspIGKzFkoNoq8IOg51Wr56TU5w6DJGyxDZYKtlkJsYs6JwC1AW8w0M2W8wt5hdTJpWLNnjctzNCbRLpColdLyUbCJXUi0UiNYRoVrLzKpTPRTZqZtaM0m8wLoZRG5KHrlB6VeXtnW3B6mS+dSW+eqnea58erGyHBrFvNrvty7c+tjzVipHoVneWe83OVUrkq3LmbOXK5FuomacpFSTZagspS0SasaYSrRJU2MljEADJKQhoStWSwKcuWnDlsllEuWkUsKkibLFxdvFvDEa5pp0AQAAgptOVNNBADAQKgBKAl7XzqXpXPJ1TzutViJtGaLeYaViGihFkCMkq1IMQNVrLg+vaa4L7Zl59qUpy1ncytVrOauQEWMTAaAGAmNy5aUho8ma1z2u1ZVm2nA9Itc1pKJgG+BL0xnaxvnKd+Ma53zHbjZzGhZkXKSOBArFrEmidS5XBW3XwbY13+T31nfnCXTlrNOb41vhvkOXZW3PU12Snz6KnZnPS5efa1NFQ86cW5qRoZJVSJCHNiTWsiCxAICLGIGSFEisQgMVDSDkKctWiogtElKwVAmErEDExikt5tb4ezj1zAN8006c1IwIQ1TacJoGmgYCTVACUglHJZTkGhDQhiEYimIhiYi7XE67l49Ot51htES9q41LtGa1KUiUGhzx142Z3v1Lx336515EevzHE5nWNZlrEbTc5hNlOAtSFEsokKqHLoTJo80b6c8y9eeWqtZ2jvMl1lM1qCa69OLozpY9MpxvbOyFpFmKqNZCCzTXn6c6xjXKzTTOprffz9s624+uIi8dVXN2TXCVHTiwZffw6c+vYsdOfa2PO3WSNHlRUiBzNlKHctCGSrKUuxK0SqVkqlYgSNCsGACCnDloQNCGADBW5CySKE1FRElAlSJKViGBydnHrCB75oAaENNU0A2nCaBpoGgE1QAjAlQi5aKWS7MToo5TqJeV9AZa25rTTK86Kki4yzrXJ62c67oON9HUnFv3XN8Gm5LnosTrnluXZTRFNEWpH5/pKzxD0OPfKHDsuUzN3FiGIhqgHCaFbVCAAQVeRLteFrvOdQyLJ0mTprn0zrp25OnOpz6ZXlz6MbnLPfLWcp0z1l6ZUu2dxm50jWavOpejfi2xvKuznXRKs6w5PS5N45xrpzvo5dsb3FXPsrTl0rBTW8zcSVFlJAkyzMubkAHIAmWDhFynYipATBMEmWA5GncZupWiQoTGBKMYJijTihErQqaYSNi4+7h3zlp75S06E0NNAAjacqaBpoAATVACMCXa+vPOlrhS9BhMb4ZTXQY2OOipeU6Nzza9OE5NatYNnLOilXjcpOvG7PQrh1muic3Dx1zqKdJlRnWtctHXGVyjUppnpUvm8/scm8cQLXMuRUtc7BDJGkaGqqWMHLJU2JoKqGUIl1maNZhyus0dO3Fcvo6+frjdzuLxZ9XPrGEaZ6wmitKjTOs5oslisqoqXrePRz643lSaIia543jpzxYtY6NeLfHTWpeOtvKpdCLlS1SwQ7lqkJNAmrEybEOUoRQmkQ0Nyi0mMAQwkpDigVJghgwVuXKwcDGqbISpKhiIoVcPocO+ebDpylhYJkCaoBJTRKAACGACaoARgS9DWko99JrljrDhfdqcnTtM1Eacp0b+foehljpm8z1z1FLlGoRvrz9EvNGsWFKgqA1rLWWorBXBNyJodZhsZ0K8pOyee5eXm9Li3zzvO9ZpKpcjSLEJiaBpgOWaSay4LSLE0DcsdS5SoYUgq8rja8bmupqsbXJqrMsOvm1nMDWb1xuVTrAppWAgvp5Nc70rTlzrfDfEnPfm1jXM0rPXJnRXN08+qYTQxFXk5dslRldZ2amDLTBJqwQIppWKkgFVicg0wTQaGZLoRQ5YSWhNANMpxUrZUqbJWS5RUCaYDcq4PR4N4yTXbgAIAAnNNAlAKAQJqmBAmrATGJr64jG6vK5cc9+eytMGdVc1y64aIxsVmpnnHUc2i7KKXnnTO5135rlrK5E1NgSyrxs3zdzWU65pKJubSFdSyotRFQ61xtnAtct86chaqZYNMrGmhiYmhHrlU1rlYZKpsGgbTGDlTkSqhreuDl6uzzujGxbZy5Y2bxzrWNZTTNoozqJqbJAsq8rl3iNc6z059rDHfIzaNZ2U3nZpnpLoOefVqgHFrmVOst5iaShZdTZVZJNZmpUrmxAhodiTQAADEOiaSiyGtE0AwSbJbJSppXebzdTO5Qdy5vVzWJvRhwewWeCvT4e/nyA1zE1TmpABKByoAQFjQKAImgYC+qQY3o8rKy2iMVcWPTGjoMNJSXFXDZmyU00w0V5aZDvOxEhcjJGkmkq215dc3XHbJcwdyS0MQW5pc51zQvNi5urn1IaLm6z0lmbRmBcgFAEUJrWmOk1M65pKasAB1LBUgacNoXTTOZe18/VjeEqNZedKyBKzfTm6s6ynozMZuNZAB74aTQtcY0J3muM7eS5mlVg0S9T5urn1hsmxJoJzQIuUBYikCAQywqAtS5QYSqVgNiBCGAANAJjgci6mdRYmowlBuVMBtOau8tM601z0xvaszO9MCLPM4vR832eBiN86SAAKaJQAQFgAoAgAAC9zl506gNzPSXONM0QpsemNGkOFrTCzSKmFUlVIirzuJGACHUWszcJNZFnWo1zrEpVKauSoa3Wbl1hqM50mxZaxZgnOsXUOXROVUa5WAFgAFRcoxS7wtprmWkXKVKwuKGgiWnTEQ7il3159sanLo56iWtZQJK0xpddMdM6WPZzEoNZKhnRk7zqd+Psl68brl289+hz7xzLoLnl1arofPtz6i1lcVRcpJWMRY0BIFlCkoljAEAlEMsmpQaVKhJVKgAGOAQrBibUOs2u1Y1LYqzpMY6V53Wmd51aSlSWOs4cG/P6fGAbwAIAUNENyKxMAFBpAAAF//EADMQAAIBAwIFAwQBBAMBAQEBAAABAgMREgQQEyAhMTIiMEEFFDNAIxUkQlAGNEMWYEQl/9oACAEBAAEFAsmhVBVYiaftYowLPbNnEMl+vYtz3Mua5cuXL/6uzMTAxRb9O+9zNHERxTiSMpe3cuXLl+e5fmtvYtyWLFv1lKSFVkKshVIv2sUYmLOxkziGa/eucQy/01+SxiYmJZfr3MkcRHEM2Xfvv9T42sYlkdC/v4swYqDZHSojpaaIUYpWLFubsKpJCriqxZdP2bIxMdsmZmS/WsWLcmJYuzL/AENjExMSy/XyRmjiGbMmX/Vf6FixbZbfPs257CiiJYwEiERUyEbF2ZGRfaxYtzZyQqzFWQpxfs2MS22TMzJcti3vWLFi3Jb3rc1y/PYsW/XuZo4iOIZsu/3H+su+9ixbnsW5EIpxlUKf0vWVCn9A1MiP0WjRHL6PpyX176XQHRiPTjozQ4tbZGRfaxYtzXaFUkcYVSLL+zYttdmZkuWxb2kixYaH7NixYsW5Ll/07ozRxBVEX3uXL8mSOIjiHEZnIu/9E/0sZFtrEUWLLmsWLFt6enq1Sl9C+oVSn/xbUyP/AJvS0Tgf8f05/VvpGnJ/8pkT/wCRa2RV+qaysSm5FxsVdCqwZ32cIsdCI6DHSkjttkZF9rFi3NnJHFOIi9/ZsWLF2ZmSOnJYtypCRjK81pMFGRJW5LFi29y5cuX/AEbmaOIjinEZky/MplzJGZmZsu/9S/cxkYGCLQOhlIbFv2LshG442LFjHano9RWKf/H/AKjUKf8AxXUs/wDntBQMP+Oac/rf0nTlX/llZlT/AJH9QmVPqOrrGVy4upwKrKkJ0p326mLfIpyQq0jjnEiy42OMWcNHDZi9rmRfaxYtzZNHEZxUZJ+zYsWLtGZmuW2+RxWcY4g5X3uXMjIv+hczRxEcQ4jMnvb/AHT9pbekyiZnEkXbLFiJYsWMTT0pyl/QtbUcf+MzR/TPpGnPuP8AjunP/pNHQKv/ACvVSKn1/wCo1Cpq69YvtZsfTk0v5smiLvL6n9Pp6ulVozoz6rZ+zdmbMzJb4owMDF7XLl9rFi3L2M5HEM17NjEsXaM2ZouvbsWLFvZujOJxEcU4jMn/APhHz4jVt7Fi20KU6hS+jfUKxD/jGuP6HpKRrqOjoyURwPSjiwifT9ZKrU+q6rVaerOtOoXLly5fdO7h0nKpen0FRUlwJFGm41KkrRpGq+qamrUblN/5D965kZF1vZGJiy22RkXLIsW5spI4jOIhNP2LGJizqi7LiLFixb2LozicRHEOIzORd/8A4p89xlOhVqlH6B9RrC/4xXif0n6VRL/8fon9Y0NEl/yfWFX6zrqxUrTqFyJnaMqg5nc0Dxf1H+QeyhJjpyiZFOtg+HTRK0YLuQ7pdf8A0lxFO382pby0/jLrOx/lYl+ncuX5LGJba7MjI6MsWLcqbRxGcRCkn7FkYGLRdoyMltdGcTio4xxmcSRd/wD5F81OzqKnSJaz7Al/yD6hJS+o6uqZXMjIyLl+sKNK9XSq9ahPSl94mn1EKctdXcZuTE3tfoMm7Rl+KBJoj3Xl/wD0VqmDl0ranzo+D80j/If71ixbbIyL7WLcvY4kjjCqRfsdNnJI+f8A8s+aHlR8tb13uWkzhzFTMImFO17PJZ6ytxXutqksynR4jp0qGVemoNsRO9qq/ja/gpeVbvDv/kvz15fy96+q/Lp/B/k9J8kv9HYsWLly50MUYlny5yRxWKfTIuXLlyXf/wDLvkey70e+pnGysZIzkZs7jFdqfepKzqP1VneXKmUlhpqMlnrR9ia6VPxy/BT8qvePR39UfzVHab/LX7QfofmfI/8ATNdGtsWdUZszMkdGYmO6/H8PorsyLj//ADD5Hsu8GN+q1iEciUeqHYqdIqTJedbyreVfz5accpVkqlCCZJdW+hLtNfxT/BAqd4915Q/NW/JL81XtHwfmfKJf6ZsfLiYlmXZkZHRi8H4vsfP/AOZey2ey7pn+VsSJfoRJCfWfnW71vyVekny0pYjqNaf4p6hk7OKH2f46n4Yd5949/mH5qvWcvyz6i6Rl5HyMt/r+m6/HLxfYfff5/wDyr2W0tl3O8pXahbGMokX0lJtMXd+VRNmo/JLvyxuJZaQ1Fo1f8SXZ/jn+GBPvHv8AMPzSpycppqtNpCalB+Tisfn4kr8li3+u/wAJeL7D77/P+lf+wey2lt8ny+1LuuguR92V/OfflpNIv/bT6Q1Ef4/hEuzaVOX4afV1VaUfJOEIppV5V6bqTr5VJarI+5nb/bM/xl4/BLuLb5/0r/2D2W0t2fPxBXS736fG3yyt+STu2Pkgmz7Oo6H2MYjhHCzIKaHCUjP0ureOKW9uS/v2LFv9Quz7LaWy2+f9K/8AYPZbS3ey8duhxJ2IxufLZV61Jd3yY3IRwfFkllJnUuZxOIjiI4hmy75owlIh9O1lQ/pGrR/ToxPttDEv9LgfdfTo/wCm+fbYu3xDaXZd9vn9exZliyPn2X/sHstpbsXf02QlI4U2OlNionDiYxOr3fJnY4hnIcpPljCUyH03W1D+j6yJ/Tkj7XRRLfTInG0ET76lE/qleJL6rrpkq9We9y/6Fi363z7bF2IbS7Lvt8+9ZmLLbWMTAw2sYIwQ0kn5ey/9g9ltLkshGVjiI4qOKjiHFkcSRfaA+RUJzKX0vU1XV+lPTv7XQxMfpcTjfTYH31GLX1avEl9X18ieorVPd+3qH2tT3Lly5cv+t8+2xbU9peK77fPNhI4bMUWgWRYtIxZwzhxMInQvtcyRlEzRmRldy8X5ey/9g9ls97l/bp9h70qto6Cd5f8AIYcYtYvy2FG46biWLGJiYmJiYmIo+p9P9P8APtsW1Mfd+C77fPKhRusUWRba6MomaOIcRmbMpc1tod5+EvL2X/sHsvZsWLc1M+XtYiaOWJrXnGdKLfAgKjSFToH8aMrFeSlSROXpybK1KE44oxMTExLFhLrIRiW9uxYt+u+/tsW1Pu+78F3+T55o+ObMpF37i5IL1S8Jefsv/XslsuRci9mmLv8AIin3pOyryH5isXHJkpFSV6UUVO6Kk/TPvSfW4m7OaQnsu8vBduSxYsWLFvYsW/Tff23vDvLyfgu/yfPKiHb3FEceWPlLwl5ey/8AXslsuRci77RpZEdPkvtzhJP0FS14kB92Ig+sJ9KkrkvIRbaZL8MSZFrFu7U8im25fCtlN4vOVxd5P0w7Fvet+s+/tveHeXk/Bd/k+ean29lK5YxOxcuXLmRDzfjLz9l/p2Zbb4v+wx7LkWy7TUY0SfRJmVhzdk5DpV5H21UemkODgQ7PuRI90+kpD8iKKn4ETJxa00bEu6vg5XScotvFfcVLcSUmqjITZldneMS5cyYpFzp+xf2H39t7w7y8n4Lu+588qKfbktviWLc72p+f+MvP2X7iSZwjgs4LOCcI4UThwLQRlBFXxj+wx7LkW3xUd9OmVHeOlpQnGlSo5TqypxXF41NPGPpVWXWu03AfkREXJM/yLuKqr+3jK5Mk/wCGI+8OsacY4yrQtJPZXYnZ5XIro53ISTFyXL7ZGbFIuXX7fz7b2+Id5+T8F3fc+eVEOxcXflW9h9C+0R7Q834z8/ZfuUvOVbGX3DPuJHHmOrMzkX3qeEf2H2ey5F3PirH+0xsq/QpV+FH7qbJaio1xJF/TxbDn1i7kez7kRdrkmfN+s5+mpWk0yTJ+CIRynUbg25WSzlK7dSPSKR0viMXQpi9y5kX/AGPn23s+0e8/J+C7vufPKiHjstkWEkSlfa28t094eT7VPyey/cpec/yexU8I/sPs+wj42Xc+JX+2J2OpQ03EFSjjGnHKMYqjCxklJO5Hs9kR7DYu78ySYxk/xiXWdRzcfWXxdJk6iaTLE+i2pv3bFjHdFy/Pb3H3934j3n5PxXd9z55oePLF3FvfZ9uaC9b7T/JzPd+5S85/lHtbksT/ABx/YY+wuZFX/q/Muz7UIcRWtCHnf+KmNdYC7MREh2YyPd+ZJjJdqn40JpSqd4WUW2W5H1l0EiKbF29u5cuZFy/Jcv8AoPv7L5PiPep3fiu77nzyop+JYW0hdHlvbZvZo7LeHSb7T/JzPd+5S85/k5ltPwj+y+wuRbIrf9T5l2KdaVMcna/rj4UifRxF2YiJAe0TgNy+3HRim4xKqWNdrgJndzttF2UmW6JMSu3CxboiMmZz/Rts/wBN9/dfjHvU7vxXd7fPNDxLkH1bHs+0Nmt7DVjsM7FyHn8T8+Z7v3KXnV/KIsNbfJ8SX8cf2GPZci2Xat/1B9vinjaXdP1x/HT86vnDkREcWzhsVjj9XXZxWObG77OxJ8jRewrSIR6zh1VEjpYi0tI+3pfq2LFtre78+38j8Y96g/Fd/Zh47qQ+8USIikm7jkOYn0lLo3tbaHl8T8+Z7v3KXnV/ILl7C7S/HH9j4ey5Fsu1W/2vzOzZCqoxc+t+uTM7NvNxVtntAU4xONE4qZxDjHGkcWRnIykXYtmRIaqpGnVipRZGhO9DT1HX1Oj4JV0tOgtLSpVaa02nODpV79uW/JbaxYt7Xz7fyPxXeoPxXf2afhyxY3cQn12l3HvFjRHyuP1S5LbPd+5S86v5GLZK6ZLtLqR7f+cf2H2ey5MrC2vyXLl9ntB9R7U2YNv7eTKP06pUT0NKI9NpkRo6Nio6Q4emMKR6SrTyOE5EU+K4WlVkmRzlRxdvTnCkvs6VWKdWb1ctGqlKV/aSLe7cyMi5f2/n213H4rvUH4rvv8b2Pin4b/Ah7XFIuN7pRk6i6ru10/zLeofsP3KXlWf8t+i7JERol2In+Ef2GPZcjLFtqOj1FYX0XXM/ouqF9Fqn9IRq9HDTUxoljET6j2iUpfxxeRSeMdWupSWy7HFSlOWJLUerjKRnlFlPJvVRjGqo3StizSfwTUIU2qhnyWLci3sW5Lly5cv7Nuew++1i3sLuPwXeoPxXfZC7bWLD7Ufx736cmLMZGD5FLrHKYorJy6+m9yQxscud9/bpeeo/L2I9kKVtpl7K4vCH7DHtHZ9zJWJYoTjd6yVNx+p1kfdVK0fuK0T+owca1adaezIdx7IhOxSkTmxNyerqvDNlzT/9eD61/wAsn1ZY6oiozjGM6Q8lToxpZVYxUb0MqlJyqUZwnSipY9uaxYxLcvQ6HQuvZt7j7+2vIfgu9Qfiu+yF2LFiw/Ggv4t7CLnXa5F3GZDlvewpqRJPKmvVLbLq37D9yl56j83wn6Uxzs3IkxdR914Q/Ze0dn5bS7Fhs7lBfw3yhDx+NmR7/HwLal2vcoybnqfyvah/1qPWWo/NLu+9rkqbRCNhSJzzp0l6KkHwlC5UqcM0lPKLrV6Sryq58tzIyLmQ5Fy/7L7875F5D8F3n2fiu+yF2sJFhokvTpV/Bz3E7iGX2sKN3w+qp5O1RT81UidC4upex89Llr7v3KXnqfzfCfRMkNl0R7s/wh+y9o7fO0tkui7yi4n/APJH/r0747sh3Xb4FtTfSm7x0/5NR+aXe13RX9tSj69T+aW1hopqzcClGLgo4ybuYNzjQjXWjdClqdZq6jq1L8X/AEr77X5XyLyH4LvPxfiu62iLskKJiWJdI6NX01tnvYsKIrIuPqW3VVRWbQqljLJS86kfT8WuLoOWQuh0MrO/v0vPUL+bExIw6SUUp439NvSSVh/jp97Fv13tHb52e0X0XRyl176OH/XpO0XuyHddtkMi+lDxofk1H5p+UmUf+tRXr1P5pCErSn26XcbxjHBP0VuuVCMI1Vr2lp53qVJT1M6qxqL6fWYvptVn9Oq3l9OqH9OrD0NdD0tdEqcor919/bXkPwXefi/Fd47QIx6UaTm9RpJaariYko3h9PpZaBLo1yXMua/IsYmfSnZQlKw+76Fy9xLoW/Qpeep/NcuRlZZNkhby/FT72LFixb9R7IXI9k+nzPrKK/soL+Cn22+GR7j3ZHtpvGj+TU/ml5M03/Xo99T+aRHuNjldJbVmY9aNDiwjCktNTpS0VaUrtREhQ6Rg28bjiOFxxuaulnS5rb2Lfpvut7FtrDXIvIfgu8vF+K7x2h2h4/TZ/wB19en/AHiGuij6PpMP/wDMUf4pD57l/Yg/VOm4z7ysrzS2TL39pc9Lz1P5t7FjFFtpfipd0ixYsNFv03stnyx7FvTT/wCn/wDzxdobSVqTI8iGLtpvGl5an8z7s03/AF6RqPzMTLlz5L9H1LmnlhU1H8so6lQp1Ki4sP5JOPTF3jH0qI0m7Dh1qxNTT4VX3bGJiYmJb2n3Xf5Lj3+N15EvBd5eD8V3jtAj20c8NT9RbmaWg609bpZaWrSXo+ktL6XGX8UoyZw5nDmcOZwpnCkcJnBOCcE4SOEjhROFE4UThwOHExWepg41KvpafRli279hc9H8mq/OZMy5LbS/FSXVIsWLFhoa2t7/AMPZbPvyR7D7U/8Aqf8Ah/5ruVelNiPjZbLx03hS89T+UfbTf9emaj8z2W9zLpf0uzjBotYdKFXRmlj0QukVG0OhIt1kiSPqVG9P3bl9rlxlixYsWLbWLD7rvzPtuvMl4LvPwfiu8exARQf8usn/AB/Sp/3f1bVU6td1caegr46CrJkmNlzJGSMkZIyiXRdGZmZMTbOqfqPWUKLq19TVqceq3Ukuz5Xu+Vc9H8mr/OXLly5feX46PdIsWLDQ0Mts/fey3XUxOGjhxLRSxiNF5JXlvc1KsmukT42W3xpvGl5an8o+2mX9vTNT+dpj6CZfa5cTumr01Eq5yhp6klG5p2+GPu7MsSuSG9qsMlUpulPnRYxLFvY+eeXdd/nZ9tn23XmS/Gu8vF+Me62gJ9Kc4wnWrQqw0VS2pjNuV0feaakLV0qs+PFycxzMmZMyZlIykZyLsykdTrtU6xsUEuLoouh9T1Es6pB9G1yvd8q56P5NX+fa5dl+R+FBepIsWGhjGhjH775U2jKRxJmczrb1HUhTpYOFHGSij4RqKiq7JD7ctGajGFWCdb11LMxZRrRhRjUpxK38lTAcTttcuN2Mm0qricednq6rKNW1CU5NrUVYrKyizoy43dOV1fpfrUZr4dee5kZGRkZGRcvvcy9VSKjLml32uXGy+z7bx8yXiu8vF+MRbRFIUutJ+nTP+enL136SrDqM4nXiIvzWYqc3yJtQlFYWKbtOGu/v5u7hG76Fy5cv7S56P5NX+f2P8KHluxjGMf6D9i5cisjgs4LOGTVn8RV5cIlHF8vzdCWRwKgqchrEyRkjJGaM0Z7YtnCmKNRnArC09cWjrt/aV8vsdSUdLVivstQz7DUHk8urmOQ5DmOXpcybK0c4P9J9ipCVOfM+/JJenZ9t4+ZLxXefi/GO+MrVNPXoizTg2U7qcPKrJ5XKnSDe0dsbmU2ZTQqtY/lMq4+j6HQv0v0uR7ol0dOWPO/fo+eo09SpV+zqn2VU+xqH2FQ+wkfYMWgPsCtDCGn7rdjGSHu/efJ8bNFtqFNNKnA4cDgwNSrVfjTK9VpFVdeVQTShE0enpynXhwyVZonqZI+8mfe1T76uf1DVH3+qPvtWPValH3WpHqNRJcSpE4tRjqVLqdQVb0VJSk6eaqVdPOjtnYv0y6ZlSdzMy9UmOXSRqI4z9qxYtyvsONud9+RzcGuw+28fP5l2Xefi+0dqdHKNeceGtQ1D0splKajUg/VVXUy3W1NTi8qzL1m7TQ5SMpIuy+8umyImpUVUSulzP2Fz02on3cT7xH3p94fen3h92LUi1ESdSFRUaMkLkYxjH+g9/j45F3okqkYH3EBVVJVnlUZpvJ1EVH17lum6IxuaZWKrvGaKiMSxiYlt7Fiwo3cvK26taVWco2Mus5l+im7zkXHIyGPoV/XD3Lly/JKeT1cfVzPvyT7x7D7b9nky94LvLqrdEmWKVZQpfcxLtilZT84Txn1ve5gYGBgYli21trFi+1zodGYoSLIbu8oHFgcSmcSmVXFz9pexijFGKMUYoxQooSLCQhcjGMY/0HyS3uXIid2m2PxUpR2l3oLpqOkyI+28SlYg7DfSSKuygiSjGFOWcuGV+jSP8qXUy6ZKJKV6kVdNWPgsW2uSl0UiT6ZFxsuNjJxxl+hLsJ9OZ9+SXUWz7cqYupK6MmXZdl2XZdl5F5F2dS7LsuzqdTqdeWxbe5dl2ZyMpF2X2VhSpjlS/apaepVI6PpHRIjo6YtNQRClokRl9MgVNT9NNTqY8Spq6jlPWaYlqqDJV6Q61M4tM4kDOBnEWnq1V9u4FRpCd/Ye/wAy77oh2h5LvP8AGi3WXeg1hV8rCHyxKc/Tfrp9TShpazycsUNems/4qMWqmV56letH+Wn8rDLq76nS0erqSymfP9A15/8AP60n/wAf1ijpvpWtrVn/AMf1p/8APa0/+f1w/wDj+vH9A+on9A+pkvov1KJrNPX07v1y99nTK0cOZ92Lvtk3GnPHZ8i3iVH0faxYsWHtYsW/V6M6HQvEvElbdi9hclnb2aspRHUmZyMuZ+zSqtU5ScifjD2HtHv8i77w7UZYyXeUbQgQ8jTdIVPMQ+WJTkT6xlVeMekas3IqP0VfxQ6OP5NV+RM/z0/SoNWL2m+9bqRk4tfzSksZM/q+vP6xrxfV9cxfVdXF/wBa+oD+s68/q2uP6prWffapj1NZjk5Eu/6DjHhkqilpuZ9322k7KrV48/uJKNx9t1siJM/xRizExH3/AGrFixLvuvYW1zI4iMvZqxyh+jT2n4w9h9iHl8MXfemU7Xj3n4QlZR2oWtV80IlyopyJTxhL8OXpl41PCr+Gn5J/y6r8kZF/XQ/NZXyySnYXqSdo2OtuSPlOyLt8/wDmKFLgHz7j6tKc3ShOceRH0/6RDWw1ejjp6k4qxmiUkU20pyzZbk+B9FfEcmz4iO512ff9l+MYXOEJWJeQ9lzpXihljExFEjAcbexJYyELew0W9mPcn2h3532Kfd+JHkplPvDvJ+iJHxKRPyRAnzQY36KitpOyfhP8dZ/ww8v/AF1Pmmf50fyS6Sh404Kbi0nt/wCHJHyqv180nYvv6i7Iv3JdyjWnRLly5cuQj0qImrK5a5Y6oV5z63fbf4jDEk+nfb4ifO0vL9l9ojd9peQ9lvYsQjGU6tJ0qlOhCtQ0+nqV6/1P6dDRvTaOVaVfT8F4lKlk9N9N4sakIxg+/NqI+oQhFtn7fxPxj353tAqdIkYljhnDIqxBWI2JSWKP8CmyfdECffliX61f+pcfjLwq/ih5f+uq8z/Ol51ekrtIXR3uU9PdPSUcJaJtWMP4yHlP8m1y6ZOKiyW9OWFRayrT2Um5bOUpHSbuXM3e/IxK7Rblpr+Op3rLoWHsvS4YYSsko5mOLdMxSdS58Hw+0dr7Py/Z+F22l5breK6Yji0Q/mpyr1KMtHUo0a9eeg1VTTx+m6d1NP8AS6z/AKDo1TjoPpkHTegouvQ0DeohShLmrRyp7IuXGy+1i3sRfpl2j3XO9o+FUuZmZmjNGaMjIbPh+BAn3IFTvyoj5VF/b/L8f8a34oeVv5NT5n+cOk669XzTjk2rGmpXKWndVy0DdOpQlSdeDcxyuRn1k71LOzlUQ/Vt8EzoParQ08ZRjk4brrz/AC+wk7FvTOUpsdslEpXdOr0nW8Erl+ltsJNLqy5F9WX6zvtBdZnxFckvIsW57/oIzOISlkPuPZbx8fiNVotEo2qOsnVKkqVOL2VSt/Q2xGJgYGBwzhmBiWJrGQtr+7EkR7rne3xU8hciZFkJWc55RJ7QJ9xOxU78qF5Sl/H8vx/xrfih5/8ApqfNdv8AOPlOGU5xs6bxal0oTtpfp9W74UeDrZuMtTL+2qSi4ESn6q9ScXNyTnKV3KfFq3Vs4MqK2zVtquG2mlFajKlCoihTUqMYubVS0qtpbLDB0rKKvKpQ4RYsX6/e/wAlDVwjKzK841KnHoYwrShTqzvOq7rIZkZCbRJ9W98zKzEQ7zPhbWe0u92eo9R6j1HqG5HU6l2XZdl2ZMyZkzNmZxEcSJnTM4HEicUVZo+5mfcyPuJjrSZN3e63i/T/AIyjCZFypEE6kc5Xco1p152WJ97VWnELaerqyk9RVFqKotTVa+4qFixrIY1Nrl/di7SYvJFapBR4jOIzMitO4ytls+8/IXJcTRCw7YlTv80JPKt3+I9SfflQurmmqV/VK+H+NVfxRg4zbXE1Pmrn+a718rt3UYtkoYx0FSMzSQjTa1CS1eNQ+pVoxOiL2kps/wAyM1TnvCWE9TVVWO9aNeoyKW6e6tjZFNKVRR49SnTyfrozlra8q1bVznV6Yl/TUqTmppZEZemp5z8X26WxMGRGujeSJckSPeZ8ROh0Og+/7NrljFswY++63XY6NqsJWV2iOpWNRetDl/CLe9i2yfS/V1DiGqjnT9yGmrVIyWL5PmJU83un0ffb/J7LkWzL7T6tJEEiUYW+YIn35LFjEtcdKN8TidJ1MoRl1dT1VfW+pi7nFOLMU5mNSpH7eqU9RKiLWvCrrHVXCntTqKm1L+NeW0neKsX2lyVqdZVLi77syKOolQqOq5y4k6blNylkzuW2s3v2U3FyEybu5durMcdpEV6qjWMdnyLsrjH2jyPyRbptYxMTEwMDEsWLFixYsYmLMWYsxZ22ycVxKhxKhlKRLy3W62+ehayzciKsr+psv0FyKyG7iPm5xIolXhZig2QpSnKH0qpI/pUspfTJRMadOpxNIcTTGenMqJKUUSqN1auPFsuVeNTztfdD2j5EojELvj6dqEFhwaZVp04011lJdYUYODpxQ4jpoXQl32Rhcjp5SKX0SvUhqNHU072wZwps4FQ4NQ4FQ4UzhTMJFnvbkyZmziS2xZk1Tj0n3eKzyvEt0sSfo3djF3RcyIVsae3ztbddHJ3nCMtPWpYMrVLqx1IOGPptUtlLsM+PnT4T1FWCylBDa5UiBMfZcj8kLwn2sWLFtup1Opdl2ZSMpGcjiSONI47PuGfcDrnFJdx+PwIl5brlb6Xu508KdON1yXFvliQhKbdGaUYM4bGiWQpJFTUNN6icjRz0pq/qvGg5FHUqKqxWFCEKtSaxeQmOCSm42bSeRcs77R7VmnUvyPaPeCu6sR90fJHT1JxjpJtx0tWJKrGJVrRnCHmxVoqPFiy5LaW6KauaeFiFW0Nb6nKNi3VC5LmRcuX26FkOMSUUNcrbUF5DUZR2i+jg2TVi9jq0001rK0qn3Nf7mu5cJxeNKSgoVLb5JknRjUquLq0NNUq09BRdaPAnBcKpnKLnqHGrDWJu1KPFquEpL/FL09WT6Sl22c/7aacZOfSL6ZJrkSu33iSPjkfkheM/1Zbf47y8h7Lmj3qNzgqien5r7MifO9y5mxVZH3VVH3lQeqmfczZx5irSQ6tzIyOI2dKo6cSp0lvcjLpU8uR7RKXer1cu6I+TjFHWo9Ink/VUx6FLzY9HVHp6iHTnFZ9MnJvdFDtCQqnSdOdUqaHUIlp60X1QmJlzIyNDRjqdTOjoadWn9J0tSEvo2nRW0FGmVHhVzHIkPfvtLxXlstoOIqs4w5r7afgEtNoZuaSkVaOCrShKT7wq1IRp1akHqq38q1VYZUq1K1WxSxzb61FHhxrIUibvJ9iUlJTqznGUZR3jZJ8kVcas4sbvzPyQvGptJtSykZMykZSMmZMyLly6LxLwL0j+A/jP4x8OxLb/AB2RLyHshczfRSISuzsKj/b73LFCjCq19OV39OR9gf08/p8h6KaV7PoQq8OU5ZuwrNyVuWPam7QlMbu+SPaXctyMXjHoJ3c/KJ/lU7QliaNJ1f8A0TXCKESS63eMpGof8f8Aiu/wIRTZGXXUT9atGMtQ50ZpvalKkjT/AG0yWop3ynOXBrn0qNSGr1NR/daKX8VSp01M2VYT43Fpo41OzrJuhCNeq9JFOenjAjJpqpJOXaPk0rzoONO6sp2adm3dbWJWG7lrmDMWWsUq+kUGutjivhvq5NNlyU3UZYxLJnSInSJulKCuIY+xJtk5eqrVqVUrkY9atJRi94xu0sYyErktoux33fdEe1Tap5WbVmWft2LbLaW3+C2RLyHsuXFlmSjZkOi4lilS09Sr97jHUYUanG63ETi6bjW4cvuqsl95Mjq6hxq6PuKx91UHKmXon8J/AfwEODCTq0Zn9uY0Dh0ThUjh0zsVZdOWBLuPkZ8OTUsne1y20q+ShJRIatxMvVGpaFyh+PuXUac+1Z5Ul4rv/jvEuVFKpVjoNXJaNKM9JS0OqPrEadPUu6I1FGS1lch9Rr05/wBUqGl1UZaqvUtqtPWwoarWVKi+6rmp1FV0ZofjSqKmaarnqX+TUdNoQnOU+3yuhlKbsRi5tiKK0v2uP0a9KX077fucHA4eQ42Ll9kTo3OA7cGom6VRD6F77XvtkRybdGrMWjiNRptuzcXEbHsuroaBVNTrqE1SpwEpVIQrOgSllv2LXJd4E91u+6IFXap5c/XkuKaOJAzgPvtLb/HZEvIe65JdN8mZMVSSFqqiPu6h95M+9Z96x6xj1DZxjjSSXQze1jExMDA4bOHI4cjhTOFM4c0We1ulTFPbqW3iOLtcuJXMtns+sowyb6C6lpIuy51OrEpMsLpQiVb/AG9Sv/De9CNsF3/we8WXKf8A2aeTo0639z9P1MqWv+rzy1GLvU8FHpPpUcjRS/va8VGtpU6enVTOF556h/xO1qmOKjc0nTU1a0lWr9jJlSNo/Ku3KWMrj6qxl0puP28KsZieGip+l5XNJUcamv08cmt7lKp6L2aaZdo40jjKRHhzlKlCIpRjHjonVbOIKpGaqE/JdppqWyn1esrThU1MpLNnFnfLIxLbSH0LtmLt3HyvuiBW2q+ey7c9rnQ6c0tv8fgXeXkPdbPZo+LFufqZMuy7LsuXL73LmRkZmZkZGZxGcWRxpHEZmziM4hmjOJnTM6Y502ngdDoh23+Sn3l3gPuIyuRKb9LfW/ob6zqKVHEf4ov0rv8A4vdFyM8atDUvi5cWtpY21uqlev1VSaj9vdYTdqn+Gl6ayr6q0H/b07ypQUs9V+LHOMu0LGm6aqupfcVzEasVbHzaVOU5ynLatGmtqMIPS1KNKtRWKh02jKxTlxdPVjZ7p2bd1Cdh1EyV2n0IyxOM2Zu/EbMsibur2OJcqESrLOe0VeUozpwfYSFhYQ10+MR94dRsfKxFPvW2q+ZYS6bW2sJGJYttbf4Jbf4/Au78h7IWz2b2XaY2afxpUJ1njY0X0X73Ty+g2qr/AI/UnW/+eqTnU/45Xow+0g3LSxjKvRVMt7y3sWLFixYtyvZd9qY+8B99kRI7MfdSIlTx/wAV3fZ7LdRyqfb1Ch+TTv8Aua8/5Yu9Sp+JP01PyO7NNL+8rwxq072pWdDplXX8CXSfaDNN/wBrUpcapLKL+q6JR1teGoqS7fJBwS2+BSaFNuMlemxMiuv06cjV0nGUuTIZSR/hN5SqFz4IuxKZe4+h8R6OpjmfNOnHLj6D+ozkqrxxctPeEo4uMblj/H4kNERuxclG3JIRS719q/mjES9PTZi26F0SsLEcY3xiWH32lt/iuwj/ACHsj4HsxEWTfUo+EJKbhjI0mrjpqP3+jqSWp0rlpatDTGq+oxenjWnCdeVWrW1d+egljhBko0IltMcPTs4FI+2gVKCgl+gh9iAyJ87WsRELb/Lhk42K3ivFd32ey3p/loySIz/uKKaqVvy/5VPwk/PLpQf93Uh/KulPS9YKCdTUdKN3aZB2NP8A9irC8tRtLoS7Lv22drFhVJQWp1X3JdxUeoyIkyg5KrrJqZJcq7RqCq+lSJdVtYbd79Ou/wAs+V3UqFFqUpahSpcNzp8PNpRfW6t8vtb0yveXeJLuxS9O8+yKPlqNtT+QfZL04jRbbESFC7lTMRosWGj4J7PstkPyHst5dx7RYyzKcpI4mE/vLH3zsq1IVekKvTHXhfjRk4Yp6p8r2VGJCFyrp8iNPUUhQqVKi0bQ48KNWnJ01+gifYjKw0JWPmzMWSjZLshdz5JRyK6tBeMe78Xst1LGdPVQjGk8qtHrGt+WHep+NE/M0/8A2p/m/wANL4rpLUv+JQnJSo1CNGoR0Wq09VmoRoNDToS+q6f+41dHhEZWlpK0oamrrJVZcd146LhU43O+yiQ6SrRxnF9SMusafGoVqeLfIiN8nLpw5GJL2l3K79SlKLe/yJ9Wh9U/GXeBPu+Wfiih56rbVfliNdIR9LgxoaEhWYoFOliTi4LG5KI6dlYl5RcU7ktvjZD8h7LeXce1t+pnI4kjiyOKcRGUD+M9BaI0m8UYljGRjIsz7iZ9zMWrkR+ozifen3h91CRLUU+D+h8TLlntfa50Lly5Hb5vTMqZWaxv6V3/AMXy/K00+BTVqlKahCt0qwfWX4ifkUf+0/ytejTu0bkqmBU1FSoXuRTtU++dGs3Ec8iM6mNfV1a6k7ra4rsptKbnTzqyi5wwlONGNRfOo6nZoiaJqS1XST5b9fUxXim92X2TvvYQj51NGD01jG5w2StEXVkFc7D7PtIgT7vln4I03nqz41a/kj426RXpsYjIkY2OHYenjhqaRix5WcpRi59bq/wVFi+V+Q9kLaQxiFz/ADtbmvY4rOKziGRmZmRmi8R4noLQMYmEThmBw2cOZw5mEl7Mu5cYtrly5dbLt8jkZMy3+OX5Woa0dNrNaegpVeleD6S/GopxqefCbKP/AGpSSqZqUKMVKNsZOvUilTqzFpa5p9FqzUTqV/p+rp14uVXrkX61ZRlyRm4uFnFRbJwaFH0xxVLOBKosVUpokrpOzo3RWld8seq4ki8mZMvs9nyJE/TLS1KcKsKmgqE6WnkSoRylQUDhRZOnTI07p0WKm0ODLO7ys0yBU7vlqeCNL56zbWr1w8GvTBenGNpRHEpxIx66elxJaSjKVLUxQqVx0ipB2w2t6fiWz3RLzHtHeQxi/RZ88PoqXpdPF4XMGWMWW36l5GTM2Zs4hxDioVZH3B9wmPml3+Ri5LFhLp8Pe5kzITPjZHyrl2capbiO61LG4M/iGqTXoHTTfDkU4ThWc/XKqlGjVUTiRZVsKViFeSKH1jUUz/6DUFf63WqlTUznLGjwR7OEkidTiEFd6Onef1uh/IaKMYUank9m+qZptPVqKH07TxK32NMlPSswoyctIyWnqxEmpWReW1uS+/wSd0hEbX4NKVNQlI4NVLGRnIdRnEbMmZSI1bP7mVuMx1rnEgJKb+NqngjS+etPjX+VP8dukI9JRGiUOlKJOhwp/TqalXrR+3o1qeRwitp3A4b4lia/ml4mq/IT5P8ALeAtpDGL9Fi7/wDlF/xVV1g1aXdFTyYu0ks13Xi4RxJKyjTyI0czDrYx6YNfoKKvLo0SI05STg03FottE+NkS3yZnI4jOKziGaMol4npOh1MpIzkZyM2xwko9bttHFZkZEdPKVBk1ZFetKpSLH0+nGtW02j0tM1sdPqV9Wp0dPKnWUqLHtaEilp9PipXKtVznPSwqJqjSi6sIup9RaHq6sh6ibOKXuuS4y4u522asxMyMmcWVuPNC1HXNMxiycFFVMdupe49tD11S8dqngabz1h8a/ypL0Tdo2aO45InlalErUlU0/0yjL7nUUc9O6LcZ0sJ6+jeFrVZx6yjeu/A1uORU77/ADvAW0h7L9Fi7pfwRS+3rd6ZLoIrd5rq+1/5I+UPF+K/HPtTKT9VutvT/wCFblR8ezfr3a7TEi7UpykZSshd/jZD3ScnwZji1zwp8Qho0xaGBwVE4koj1TR90m+NTZThQqFT6bRJwpDpQZGVX7C7jLURnNqlIjpVOl9iinqIRNRq1VpLUV0S1Na2hqQ4qlpNVTrRdOpK1k7OjFVVRoaeRW+laqhSpStSnU9DqolPjTqwoU1kdWKJShTZHRqZP6ZWgnpZolFw5bi2kLnuZjkMpxTaFez2+mK+uXjtU8DT+erPjXP10Zeio705T9WXSM7Vpq8a+nUNQ6GP03QKFNVPqdKT0qdWMqOVf6jHDSQam8Uhq2oqfhNW71yp1a2+P8t4C2Yxi/RYvKP/AF4x/t669cO0xL01x9Yf4yX8kfKn4tH/AJT7QKMVOR8f+FftyfEvH2VvMUHjJOM3shci3oWJq2oizWEKDqFLTXqfZxKkVCe1Msix6kcSqjjVTiNl4H8Avs7OlSZ9vAxfCjUVKU9VSqRzpFOvRxU6ciWjpsjoa5H6NXZL6VNFPQUacqtPQ3ktES+zMtOhV6aPumVNXqJwiVH6a0ikyTvLa5kylWhGctddSr8WF+r6O/LcyLW9plMRDu9vpX/fXiYySqJ4WIRlSq6l7avrKnL0Ofp4hldSqyVet9Seiov6lqa1TUfW6lSj/U9S3HUStxvsdDR+q0alb6rrZfa6XWKdRu7qy/nnLKDtjXkpVWSd9/j53iLZkhi52fPsPtHzj/1ov+31P5Kfap2/x1K9Mep8SX8sF1p+Ez/yq9CBS6M/x/8ADU8vxPtu/ZmJxtdObdy4hd+VkDBF3xtWrmLRpvOF86q/uKkPXDT3jWp8EzM0ZF+axYpwVT6Q6FSdNq3LbbptfexTpTqS4TvwoqFN3lVk4qTuRdoiVzAsRpSk5QwZHab9XJZlmWZZljBmLLMs+aAiHd7fS/8AvJdCUlwKr/hoNOeqSjrK4itK8lLpxWOo8PuXdV43qVYVShHT2eloOlotLQUnpnS1NRfc6OOmqznUqTaoyxrKcYqt11FnJFTyY+T53iLZkhi/Rfak0qif9uvwanziT7f46jwh3sSa4lMpr+Nr1/8AjW6kO1LyR8f+Gp5fifI+dbS2+d49+VrpTp3jVhipW+41jKj6aXy08HxtQv7ionGYjqXEzKmX05aiYI4cjCqY1ENyFXg6dCuoabUP0E4xtjFLmo2w203nLrKXXS0Iq1a9mfBEYiM5UyXVkdnC5gYlizLFmRIQUnHTodGmiVKmOEUNcnTaxYjv9OdtatrtRm2yHfUdNVV2m+q2jUspUzEhp6kyvpalBuE0IuyGpqwP6jqUfe1TjtuWpnJXbkpNRuT7nxv/AJbrdjGL9FkPOK/t4x/h1PlFdJenbUL00+8usp/kpeqvCXpk/V/5Veij2035Uhr0/wD8+q7csu4/YS6LaW3zvDvyy7UJMq1byk/59Y8lWglDTR/kpQtqK7/uq7wqWMTEszqdS5fe5xJHHqH9NpWq6GrGnqIyihdn25UUpY7NdaPoptif8FKeNGpUzW6JdojHstro6FiwqbZwURVCBLU0LS1EGfdztKu2Oo2ZFy5fluOOMdtH01PwUkmTd2p5KpU4lab6nyXZcyifxiqdOJNlLWayJHiOpaEa6emygtO6qjFtKNnbb4H1b7GMTEcbHzuhbMey9j59hkPOH/Wj+DUea8anbtCt1pq0TvKskqtPpXj4S6zl+Oq+kGUOtZEu/wD5ajxfJ8vuXZmzIygegtExiWO27IztG/Vs6CFzMoySKvWXBjKr9QtEnVvT0jbqdb13/cah3qCaOhFXMTAxZiYmJiWLH3Mj7yY9VxI1qSgLs+3Kim7Nsl5U7/bu7IK1Caxp8iH2iMey2UWxRS2zHMyMi/vS/Htpn/NtGPp1FF0Z0ouTqRwrvlsWLclyNerAX1DVoeurM+6uOrAcoMVrtFiaSZ6DCJwzFkl15Fsx7Lt+gyn+SH/Uiv7bU/kh41O3+M+tMj+Sqv5Yfnh42/mmv4qnjA0qfGR8f+GoVoPdd9o9yyu+b4W/QsjBGBhIxtzMi7Ksd5a8t00sHGTKjpKdeUKhgzCZaW1y5kZszLl9rq2yJTTV0iUrrmj5MqeS6aazI1cI6jpMW3xEYiXZ7xsYPBsv+m+scXtQ/Lt9Mox1L+t1aVTWaalOpUr3nqOFJmDLW20tONSVLQub1n0qrDS/bJSn0ly2IfTtVUKlCrSaiPv8pku8MUKFIlShbhmNREk78lzIbLiLIsjAwkYy2v7NtmU/yR/6if8Aa6nzj2qeP+L60PhfkrfkX54C/wC0/wAM/GPfSddR8/H/AIanxe8e72hu++1t7W2+c6bHwy1MwRwzFjTXMzS6bix1NGyj0KkI1TGxZljVr1FmdRSkjjVDjM4kS9ItRMKRwzhSMJnVF9nta6asual0quaKj9UvwOl6VeUtQ86guzIkBiH47ocrouX/AEls+9GnccLFinTcpV6To6ii50p363FJEpwZ6GUMYn0zQUKum1FLT1aP1OENLrJULy4A6LOFIwktkz72sQ1krvWScZWxvEvEk43XYe75Lbve5cyMjI4sjiXLxZ6DGJgYSMJnYyRfaXal1qRt9p1+3rxcqkWrT8IEP+t/jHrUrP8AlX/aiS6ahfin4WNH/wBj5P8Aw1Hi94Eto9my497ibM5RO4xisYo6GQpO6jJlRW5EKnOQtJIpJUouqKqhVEcRMVOUj7Y+pQwmZGXROyujodC3SxiWe12ZMuX3U8FKWXPHzwiVlaWouk+kISxJ9yPZkO67vb4XI/1YuxkWuaGtTpClpah9tSm39MKmgqRPUYmKOgmZmfTS6yVPTvXSNXX4lRqRKc085C4jMJD6npGoihs/HqdbyRHsPd8i3fflYixbbqXZkZF0Ko0cVsuj0jSYlZpvCNSWFWTvTnYbWNNq8H/D3UFepVX8k5Yansambxh4y8TTP+f/ACH+Gt47x7S2Xi+ZEuxLu9+FCUHSo0iVWSF6ozikPaGOUZ6SL41Jl0zhs4MhUThpFoilicWZrHOQ4GJYszrtcuXLmXsQgpFRWlzLv0NT5aqV3UqRsvUpdyHZkPL/AC2+Pn9G5c6lubsXLdVxIkdbWgR+q1xzm3nIzOh0MrHEbIStF1CUrt8Nl4ZcZIeoHWufSaF6Mfo+kr09d9D4DdJwbH2UmjJ72Y93tblfflfZdt37Fy5kZF0ZGRcuXVrIj0brNlSTlNvrVrRahNXm1Kd7xoQUZyXX/F/grdt49pdz4fPK2z7/AAtssaWofonbh0/x1O3NdirVIi1tdC+o1hfUCP1GgL6ho2V62nqPhRkPSXHo5D080OlIxZYsYmJiWLPmod6rvPnzKnqnXf8ALUvIbsVPIS9Iu8vIQz53fPcuXL8vb2GrlmdTOSPuJkZwJtXZcyLs6lJWkperLrA4bRJMxMDhs+jPGnpZenXs1PepHryWLNDGtmiyMUY25GixYsW2Yi+79uxbkuzJmRkZIui5ky50PSJq9mcOaHNqE66kfG777Pn6XWy8Yd2VfwV/xzu1HrRqePv3aFWqxI62vE/qNUWvgfc6Vl9BIdLTMdCJwGcKRgyz5dP5S6+xHxs3OTvNxTlXf8j2teDR8z2Q+zH3e2Rcv7qZa41bnsW2scMcS3L8KBw7C6GR05PpvRaeaVPXVSu7uY94Jt9Gena1zhE6Y4zXJflsWLD/AHrmRkXMkcSRxJD5V3HzpbrwQydnQ1P4qngv+vU8P2LmcjizONIenY6clvRdh+xT607EbcSn66kug9vhnzIW3wx9x292zOHI4I6dto1ZwM2KUS8TpvDv0MSFHJ16DpSaLFixYsRKEcnqNHhTmrMuZGRmjTa2lRF/yLSwp6j6xxSWqnIc291QFFR5LGLGjqtsYs4UB0InBHSZw2YMxZYt/qI99o9x867fAvHaf/Wr/hm/TH8FTt+502cbj08WcGSJJp89D8Ul6VZOMpKnJ3HtfoMfaPY+GPv7GLMGcNmB0Ll97jMmXLl+W7M5Cr1IktXVm/uDjI4hmZGRkyGoqU3V+q6ytF1JSL+2iVOJh1dGY7oRYsNyMmdDFGI0W26c1ixYsW5LFi36XwvZiPttZM4TY6coli26F2fgLtsutDU/iqfjp/hq9vZXM/dsYlpHqLyHIdOEh05R5tN+Oc8S5N+naPdvo9viO9rjGdzBnDOGjGJ6TIuX57mQ/cuXLly/6S7qrFHGiKUGRnEtE9B6TgzY6coltrbOw1tYxLP27exYty2Lcvx7K7PsJXVtlUlE402Zo9BaBjtLxFvH8Gp/HU/FS/FU7P8AcuXLnFaOMcSB6GWJU1InBw5Kfj8JO8312Q4sl02irnDaLbfLId7ja96xYfb2n+rfaPfJjyLtGVjM4kiNU4yvxzPJ5RbsNbNIxOvJZGJiW9qxYsWLFv1fiWy6Rvy3Llxdp7dLbQ60dT4VPw0vxVe37mRkZGRcVzrsqkkKrcdOLJKzKKbMGYWH3FTZaxO7JvaPe5fZjZH37suzJj7e0/dUZM4ckcJ+xHu7xVmzqOJgYNCpnRmKQowR0HOJkZWHUbLo9DLIwkP2Lfr2LFuW28tvj2Z9133g06Ff8dWnFUYdKVTx/cWnOBAVKkj+NHEFObPWxRZimOkOiiVCMl9miGmnTPnoPo4zjE4lxSRObb2Rcvs9l7dy5cV2WZgxRRL24eX8Z6GYxMEcJIdJI4KOBZKg2uE4NXIzhIcacjCiPTwH35oeWNI9LPRa0DKI8dnkz1DTFBNOnYgrFlEeAsS6Lstd3sPI6HCHTkNNct+WxbmtzWLFvbff2n3l5cmXRu430jJxjOV1+5wThxOHE4US0EXiOpY4pxTMc0jOLOg1FmBPTQkS0uJwrvoibQywo865r7WkzhyZwhU4mCR22622l7ce6Yp2OIcS5dva8kK7LNHqPURlKD4sxVmyUh9+aHfiTu5zHJsUGcNs4Vx08S+JmKRK42y7HkZO7TR1ZixJMV0ky8jqjiHFHMyg3w4nC6unJFua/JblsWZ19ixblXf2F3H3X+l4kTiRHWZeTPUWkWOglc4bMJGEmcJmIqe2JKhCR9rSHoqJ9hSHoIktDI+yrIdKxwkOmy3WSKcMyUEizMGYlto9C+/cw6OBijhDpmJP26XWcoQtbptcujJF0ZmbOIziSMqibnUbymPvzQ78aZkZdeLIUmNyRmziM4jZ1ZjLbrezZgOI29szKI22mKEmRpiikOUbZRMoj6idiU7ixHGmzhI4MhxLFuS/s2LFi3K9499uhZFixYsLvsv9LikW29RjUZ9vNn2wqEThxW3QujNHEOIzMzZkZGRki5cyMzCMz7WDKmmq2lTkYNEUXZ6h2GkdCwoCpDhJHiZo4qQ6pltcn7cfLFmLMWYljEtYyZeR1Ls6mTMmZD780O/QsWOqMmZWMmzLoncRfaVXEz68RjqSMmKZdmNzBjgJMvIvK7pHDsS6beLtIszEtbZSsZnoZjFnBY4NFuS29uW5fewx9iHsreJYt+y/a1H07EenkmqAqaRY6GaHVHWY5mRkZFy+3XaxZmFzhCihqBYsYGDJKTJUYM4FRFieDjjGRwjGxmcRsVRMlULzkYSQqcmcPpw2cNGBVXtx73Mi5cvEui6M0XR0Oh2MjIv7EN2PkW1mz1xMpWykzFsfQsKET0I9KPSOzOqE0XRZsXQdhMshROpKRcTLSLsRZswLCuOR6GYwOGODidCxYttYsW5bJlWhhAi7F/ZfYj25rFi36T9qNedQp6fIlQVqqwHMyMjLaxgzhSOCzhIxgWiXSMziHFZnIyZc6GO92XLsvYcsiVOLbh1WmkyVGMF/Gl02UZMUWKpKIq0mN2FNp8ZjqSKjb9uPexYsW5bl/ZsWMSxDe53MSxjHb1PZXL2MhtF2ZO7qGZlJmMjFmMjFscBQMUk0jsM+LROluu1zoxQMTqPMcpnUTZ0LITnA47YnGRiYS3sW5n2shRMTH2H2EXL/ALL9rR6dkfSpzVtR1OHNv7eRwEcKBaKMkjMuzrtba+ySZiixicNGKOh0Lly5kXR0Y1I9RKFx0mjhSFDEcDgjpCps63UrGbY5MWBW7+3cuXLl+exb2YjuRuY9eEjhpDytwWzBp2F0O+3RDV32Lxa9BeN7oUi6MkKxkxyyOti99uorjLl1s7CSReRJsuzJnVl2i6MjI4qOpk0cTo7sznfuYIcDhSY01tblT5LFuSWy7W3uXL/orkftQsXG4DlAbJXZKLGnvYxMDExRZFjodC6MkZGQ+o+go9H0Ey5mXvtGdhWZOkPptYxL4iqnFSLuQ8iyZKNk43JJM4aFSuLTSForn2ED7OkjgUEOFAxpDhSODSZLT0zgHBmSg0WLP2OooyZhIVNnBJ0sSnFMwRimOF1YwQ+gpsjUO6yFYm7GQ00RckZdMkx2MbnZuY5l0RfXrEyci8TJHpMUWidBiiWRlC7wHjfJDkr5I8jFMwMGWMXbFsxselF7j7pnpYmjMysXhIuzBjgjE4UmSi17SdiXUsW/XXI/aVWSOLIzkKpIjWFO5ZDhFjoodEcWjIyMxSMiVUU2OZmZFxzMiI+0t8WzBmBwxWRGSHGDOHYxZ1Rk9uHE4CY6BjUQqbY6UDCmixGI7IdRIdVs9TLSYqbZGi2cJHCiONO7jTRemhygy1I/jLQYqdM4VJn29E4FIdBDpTQ1NEZO7mmOwnYvJifT0vZ3OjGWYuhmcXEVQyiXV/QSURYmSQ5RuZSOJIybO5YxGsTNGRISZYvYxMJHDkYNDVh+ocRWHG4o2HJo8iyHFswttxBScy8oHFM4yM0XQ2dzFiizhiUojR6i6L9JTyP4zCJhLnZcW9i3Nb3V+kpCqpC1ET7iI9Qh6gdW41ccWtokpWLlzI7i2syNNiVhs9J0MWYyHFmMjrvdnEYqjOIScTOJmz1mLGi6Q3EVamh6lH3I6/TiXOKcbpncuZnEHXOJc4jM2ZszMrvJo4hmcQzMxTMiUYSJUTgyRgxXOxKYpCkol7jaGzCTFTFTsZNGSY0izMbGJjFipmFjuYpluvDOGr4WLDgWaIyja8WObQpMjGZiOnd4tCfW6My/XscaRKbZcSZacT1sxmYlpGM4meRZDXTGw0hCHc6suxDLtGZcudCyFkjJMcIHDOFPmuX5LfoL3sjIzMi5lui1yNK5CgVaStJdYk5bdWRoyYqNjhosO56hFixZ7XL7WRaJjAcoIc4HGih6g41xVrCrsdZjrM4lxyMhS2uLqLps4in0yGJDUR7ZFy9y9jMyL7oURIxMUYWJU0x6cVAlCKIxpmNMvEzjaM0ZHFFNmUjudi8TJo6Pdxe9xItEl6S+90Kw7FmRdy9ldkJM9TTjJFy+1jHrFQiZxRnFiuSyYoyHFxG6l/IlGA4oUWXsWbOwzNoyuOXTK4zExLDuzqIbsZX3zZ0Y6UThDhKPtP8AavvflSuQiRcUVKt1KrNOUk2xUWyNGKFGKLj2uXOhiWLnEijjQHqoj1R9yx15HFbOKziHGOJ04jFUOIX2sM6mDMWYmIlYud93Fs4ZiYMwZgcMwFAsYDSFGIktrodQ4jOIxTd5TZxZC1BxziqQ8iUmhRizCJii0U1IzOKKoxyd3spWMkNbKVhTR0E6ZemjKDPQfJYsy4roV5brEtBmdn3HGxixQmSi7KFyeQ8j1WhIyuPqP0kWmOEW7QRZIdVl2XMi533syw0KR1L2Olrly6Op1L7XbLtCqSJOArMcWv0l7/UsYsxMdrmQpM4jFVPIlRMXEhtJ7ZWOJAdSA66HqB6iTHWkcRjmcRGaMzJ79d7FiwjEVMwMBQOGxwMToPE9AnAygXRkX2ui6HY6GCMLGA6J9uOg0RptFmiSkcNmLRZss0NSYoyOGzhswkjJoU0zhJjpTRLIsi23Ys91FEoWLCR0Og73VjFmBKO/pFJW9ZlcxOt2dRuxmzvtkxyxVJ5JsySOJCRdMySfRjcGdEOVzu7WVyUjJjz27bXRZsxltGTHJIzTLwOha5jctY7F0dT5sXEmx3LRL23sYlveXvWLFuVocRIb2iziIdWBKsj7hjrsdeQ6jMmOVjIzZxDMb57lpHDkcJnBOEjhwPQnlE4iMzJnEYqw55CaLI9JZGJjIWRaR12djoWTLRLockKaLnEMiUzisVS5mZIbiKxYxsOViL2kOwroVQ6MdOLHRHSmhUZsVNoUUYdeGiTafclFoUmXMmXkZyHlJYM4bHCSMZHDkKEtrWM6TSVEVOmx04JqihUYjoxQoRu1GBnFHHicWLV4F+lkySPSZITLsuRqDd2rtWYmzs/SOKH0eQ5IyOo4iUSzPUXZZli9lkj1CszIcnIt7L7e2v07l0OaOKiVY4jbzZmy5dFzIb3Y+Wxizhs4bFTMIkcC8S6HOxmxzZny9RJjpipsVAVE4YoIxidEOqjjkqjOIzMyZxBVDimRe5YzkZMzE9uxkzNimXFMyZmiy2Y+hdPaMrGVy++MSUIjkcSRxGxyMzIyMi4m0RrzQ53SY3FlojpMdOSI023wZE1JRj1F0GRZ6iSudEcQk2zFiVi6vmWZYvZJlx2LX2xLMzFNMcomSHItKQojpiaRmXuWuWY+hxD1sselF37z7fs8WI66Q9UfdH3LOOzjM4pcuXMi/NYszBios4JwUcOKLRQ5RMzMuzFipXOGYDTOpjJnCkcI4Zij0l0XRkZGQ6jFUZxTiHEZxGXuKxfaxZmLLPfsZF+S5kXLFtrmTFK5lYzFVJWmpJwaqCmZCmZWMzuSRZDgRg5HCiiyvgcM4djBncjAlchAfRpK0nYUkfyXvUJcQWd5Tg1lHa+RiSR1EZWcmW2uKx2M7mVxzZjd4xOi2YltYySMoinEcoi2zSFxJrhNH8aM+a/Jb2H+1mzLkvtbZXO4oGJgYmJZF4ilEyiMux3PVtYsi8TJGZc6ltlJIzRxSVUybGxyuLdDLi2tyouZGQqhltczO40joW2SMSyHTHkdTJoUiSL2Mi99lIyyJ0i9hTFIb2U2ZEo3LtF0zocORhUMZItIxYqXQzuXSFUg3/GOEZnCUXkZsczpb0xMjNnVmVjjk4zvHJCZjFjosdJo6liw9rbRRiWG7HQts1cxHij1MwkYwM7GR0925fmfb9q27uzBnDkKkxUDBIdkXRkZoczNHQstsrGZmZmZ1ZjIwMEWR0MjJnViiOIkWMSxjcwMd7j6jRcuIaE+aJYsZNGe12J7ZGS2uXuKVi9yUBxOxFjhcwHFoiY7RkSipDjYTIzOwpFyLJxHcjOxGqSm2N1CEaiG8R1erqKQ4QZ0ROVxS6Ju95mURzSFVuWjtlIzmOTHIhIdxXGolmi8kZSMlZqJ0EWHbboxx69TNnUeydzGKMoolNy9i/vX3f7UaJwxwRZCxLoyOKcQzMzIyLkntcVzFnDFAxIwMDExMDFHQ9J6Tptew6g5GZxDMyMmZGR3MR3L73HIuXLl9+21zuYlixiWLDjvc77JljEcRFixiWLckoFxS2RexGY+pIuRlYjURKqjisybOp1MtsmjKRm2KLMBQHAs0ZSOIyM2OxJIUzIi7jnicU4hmWuYK1kiSyHAwMdk0O5dGau6spKyLmRdFuS29/8AV8U4hmZXGZF77YmLMWWZixU2YCpHDRjtiYCijKKOKjiHFHUZmzIuXLimXGiw1tcuzIUi62THs4nUszGRw5HCkcJipM4LFRZwTgo4RwjAwMDFmBwzhnCOEODRZrax1Ey6LFjsdyxiYGBgWsSp3LWEy4hqxGoO0hx2yMhS6OoZNjyMJGMkYvZFjqfNy4pMvYui7gZykPqW39J0OpZnTZmR65Eujdmryty3L8ly9/fv/pEYkYMwLHQuhnUV2JF0XMjIzMxyLly/sdTqddrXOEcMxMEYCgWQkj0mMT0npLwQqlM4lMVSBnAziZoyGy5kziM4pxBTMtrs4ljiHEM0zoOyL3EWRihIsYpmFjsKzHExZ1Ra5jYlG442FsmSiXLlyy2uRl1XbqjIc7kWXgzCI0dTrt2L7YtlrCizIUyUUzhmKLW2ukerb+JJ1Ha7t7ty+12X/wBZYwFTOGKCR0Ll2WLHQyRkjMczIvtflttYxLFiyHY6CaMkX2UrHFMi5cuXMi5czZmZDHtkZMzZkziHEMzLkvtmKYxDFuuhltkZGZczMk9smjinELrbElC5KOL2T6NCGXL7xqWFVVsYSHQQ6UUWiTaFdHFscVjncui6E4o6SPTbFov0vshQkx0rH8aFNjbb9+3+yVMx2uMujJGZky+2O9jEW90XMjMyL7ZFzIyMi5fbIczIuXLmRcvtcuXLlzIv7NxS5L7sUrClfbsNlxuxGXJcuMyMi+12RqCqF0ypG41bdEonc7b32iyxk0Xey2sNNDYmdzFbX2xkcNH8SOKxymyy3uX2t/v+IObLl3tYtyKRmORcuOZkXLl+S4pGRcvzXL/oX3W9i29tky/PEaHEsNb3L732vte21xSExSTU4XJRttcTuNElyXLi6jcTiHcWO3VGRcvslJnDP4onEY1KRgtrexcv/v7ly5kORkZGQ2X2uXL733v7GLMGKmKkSgki3vIeye9y5fbEaEW3uMUhPZl7EZnRkltYZbl7Hc6ovc7b3LkJFSmpprFiYx9VyIiORa5itrlxXYqbLU0KQ3NmK9rt/pr/ALuRcyLmRcuXLl+S+9/YxbFSYqIoI6IyMjMnIW1i36N9kXMjMvyYluS5kPaLO5gNW3aL7Pk7Cd9nshMjNlSOSa2SLE48qYncvtw5M4cEXij1s4ZgdUZf6a3+8xYqYqYooWKHNDmZFy+8tr7JXOGzCxYsWMTAa91b3Mi4p+xcTMiMrjVzEs97bMuXLiYx7IRcjIqQvsmN7SXKugpQS4kmYtmKRcyL7XLRY0kXXNcv/obe2+/+nsYnDFTMCyRcbLmRflxZw2OkzhsjRI0hRSOg0mTpDTRcyMi5Yt+hcuJ7oaLlxbroZjkXMS275Yvo1spGRcjIyJ7IsWuNW5LC6FxSLncsdS5fa5imWsXfPfa3v3OhZl/1n/pLGIoCpnDMC2zY2X5VBsVE4QqZihWOhijEtyJkqeROlbkvs1+kmXMi+7LikZFyPUx2Y92uRD5os8lKNnF23qRvyItyXMy5be+19ntfnyOhb38joW57b39p9/28WYM4bOEcI4ZgYlt1IzMzMci5ZsVM4Q6YqRGkKKXI9sjIzMt3spD6kqZKFuS/6t90NbLZdCMhjiWGtny3HypkZWLKSwE9rlSFnbdNly+1i21zIsW5re1fa3u22uy6/Sff9jhigKCFBGCLIbRkX5L72YomBwjhCpnbZikKYpF+R8lzIuX5XG5OmduW36l+VMyFIjIbGdxjXLEfNcpyJOzcr7YkuqtvexGQ9rl9rbWaMv0rl/8AQy7/ALF0MuKZxDMci5cV2KBwzhEaJwRwtsmXMjIci5LdMuZF9mLd7XLl909nEnTH0/YWyYy+6EKR0YkTQx8i9iLO6sLoMUiT6vkjLluX2cblrCl+nf27/qS8v2MjLbEwMDFmDI0hQttkKQpmRIaFtcuXFs1z2LD5rl9rikZDJx/0FxCudh9UMe62fPBkujXUZckJncYtlzXMjuOJ2FMuv07nT27/AKE/L9jAUBRLF9ugkt2SLiYmXHvbdbS5bly5cbL+1cuNXJLZcj9tr3VtEgyRcsSQ+RMfPE7x7PumfBc7jQmZdfYvtidUXL7W/SvzW9m299rctTz/AGLbLaRcuKRkXGx7LbIy3Y9ltLe5fe5cZb3ZrkT9xMfvoXe1042OxcfuIhIqEZD2e6ZYxI81ua21y5f9GxZF9rctvZsW5UVfP9yQ+Z8ty5fZ7Iv7K2fsvkZJcz9pDXu3ExSFUsZZDGWHyL2X1RF7S5L7RY+W4/ZuXL/qX2t7Ny/JYxMTBMdBSKmlsODX7jXLf2nyX57lxMftPknyJj2fsrZ+8hMiyW19nvEa50RZJbtctxEOpba/v3L/AKt/fQtrkopmogo/rXL8j5b73L8t/eT2fstcr5F7iH+gmd0977oTvs+ZD6raPUlSLW5Yuzvtba/6F/1b+2hC2uXLmp7fsX2fMmX9pe2mIftPklyIez9tr9Bdn7CZ3GuW5Fj7kNpQuONixbdSsKzMeS/Lfe/s3/Uv719tR2/ZXOuRfosuRez91879pbP3kxMkh+wmdyXKiaEyMkXMkO0iUbbYmJiJiZdMcf1bl/1Lly/tSlYqSv8Arf/EADURAAIBAwMDBAEDAgUEAwAAAAABEQIQEgMhMSAwQRMyQFEiBEJhUHEUUqHB8CMzgdFDYrH/2gAIAQMBAT8BJJJ6578kkokn4sEEEdmTJGZmZMl9CtJNpJJ6YII7EC06mU/pm+qTInqkm0EEdcEEEd2eiO3JkjMyMn20PvQRaCCCkgVVKPWS8EszMyeqTInqlmRJBBBFkrNWggi0oyJ7EmSMjIyMiTIyMjJk/BQ+qGYmJF1QYmJFoNjJGQ20Zk3hGJBLMjInqyMieiDcyJV82ZGRkzcgggi0oyRmZGTJ+ch3SIJtuQYQYmJEUSh6hmZGTFTI0Ys03CMkl+RVHZgi0mRJPTkzMyV4MTFn9za0ozR6h6hmyX/RUO+nRkVUUp7sUGxkJuodLXI6rZJaZtZNq1HAiDwV8IqH8CTIyJtBBkz1D1ESSSN/0tDvocmv7iDYRSVVbReRQoNTk8Wp9pSLciUyvhFY/hq0mZmSiCBk/wBMQxD5NEQmSN7lPkq4fRXyam96faIp4KfJqeCofw10RfwP+moYh8lAhMna2l5KvI71FfN17SlSUR5FWkV1SPf4i60P+mq1I+RCJF/IjR8j8jtB+P0VbkIzJ6IYl8RdaGPntQQYswMTH5qtSPmyQqUiKROlGaMpHbGoaINjYlEmRkybQ/hrrQ+B9KRBjbYypMzMzZLFx81DF2KOb6TNejeUYM9Nnpigo08uDAwMTH4i60eB9NJL6sSCDx81DF0IVMnpM9MWzIEjTZqk2bPBpOB1bkjqsufhrseB9NN4IErSZDZRwee3izFmDMDEez7iGK9HDOUUUMqpgw+yqlI8CKStiHyPyPgRMEskkXw12PA7K9NkQYkEDYuRlHB57cwh1Ml3q57iGK+n5F7WUVVPZDpqHS1bwK6GeLN3VqfhrseB2V6SBIkmzIGQUcHnt+BiVkpK+e4hivp8MT2NPncbOWjyeBHgpMWOka2fWvhrrQuB2V6eSSmrwLk8i3HBsSMoPPb8WV6/HcQxX0+GeChwNjrPNqSROD1DMyHVaJEKnYopUwQvr4a60LgdqSCClb3VlUN2gRR3PAilW8lfjuKytuSKhs9Or6HpVJSMShjE9ynRTK9ClU7DoQkiCtIhCe49nBkUKdyfhoXUhcDtSiCClfl0pJjSGKo/sIkntP2lJMFQyvx3qbKozPXrnZmdT8mpqVVc2XJFtKore5W9zT5G9hkCFyV/2P3fFXUhDEUiRiUL8iLqkSgqINhNHNl2n7SGRsQNbFfggjuK9Ihf7FfCGLkdtN7jKvJp8j9toIOEj3EqVAz/AAmmf4XTP8HQan6NJSvgU2fQhD5EUIpggo95VTF8jIm8lL2EpH2n7SRSRapboggga7SsxCKV/wDhW+LLkdqeT6KuTS5KvaIkpGUpSJKTm03/AFOnhXHfo4s+hCGIpKX+Ihe8rpHQjBGKIpIRCIR/4I/E8jI7L9tpu+UQQMY12VbFi02YweoSLhnkdqT6KuTS5K+LSJiYhGnu7q363Tyoy+u/TxZ9CFZMTFX4HXwPUxHrN8jdpJZvZcFK3NSI2ODInsv29LXQx9lWl2VDZD+hopTjYgYykWXhD03yU/iNybEWgSqKcp3MarySVbqCunFx1RdnPU+hCtSpMUPkcFT3KqpFeTm0iY+BsXUuhJNQzGgx0zGgVNBUt9rsY+yh3pSSJpY+WaTikr5GrUoo01gaigmr7Py+yX9m5vbiz/gyMjIyHUfql+7tLbtJ2kprgeo2OsdQ3PXJKMkZGZJJPZggppngWgz0Y8lcUiYsX5Gl9jj7NiJ4Go56qR8jEIrEV+yzGadUCq2K6JKqYG3JqcWo4KrRb1P5Ka1HJ6n8nq/yesV6sqO0up9CPA++iOyul8Ek9em4ZVwU8dNPB5KikQ+TwV+xWYxFNf4k7k8nkr9oyjg1BdFL/EbnuLoqoUcFVp6OCbvqjrQourQQem9j0XI9OCjSnc1NPHoqUMpEND6XwU9P7TyNMppYkVcjK3+JSVWQqtiplJ5K/baj2jqEymhjpasvb1U/x0LogZBqe1FfN56Ervuo2HZWgRS3yV1OeRTUKqpcMcvkxMSDVXkTFUN9U7FHTV7RMliqYhoqKuCkqujUKDyanFtJSmUrfcoSdRXWqIkrp2tO1psrUcWqUrox8kUiqdPA2nyOo1atkVPqR46F2JZkzNmbMmZVDb82VkzzJTUTsUbTd1sprZp1/Zq/lTaSSbuyexplVTkllb2tXZipIi1SGm6YFyVXgrl8FI4krexBpuEbNiTpcpDxq5NaraKexSosl92lmT4J6IkrvSpKubroZSh7EmxKNjY2PxIo+yKfsceLvpkxcwRBIrqZKEZMaRR6a5M9L/L/AKnnYygmbTbTKubVC5MZR5sqGQktyuG9iV5NmNQVCNPRVRX+moVOw0YI9JHoo9FHo/yeiekcGXTG93popUCsqvJXuOlyaaat4s3tZbD7NA+SSemP5MTH+Txd8dS1N5JkibSU0yx6FR6VR6dRLM39iqqfkzaHqMVRt5Halj5sxcie0Hk0uGUb1IiSlbipT5KtNIqYylGnVCH+o8FaT3EzwSUrYVG5q7I9REzwYO6jzd1QJyU6DZ6KFppHoSejHgdEckIhGxD8I1VZFKdXBXpuSEubsjboo5KuR8ipMDExMTExX3bwKz4H0SbCqQ9anwOul+TKj7Hj4Y6qvs9Rnq1GT+iX9GT/AMpnV/lM/wD6ma+irU8E2Q7oTbtk0U1tcCqNLmSmraSuudirwMRSzT01U22KIg1Pc0hN8C1GPUcEyh1bEFDconp4MZZRQ0zTqhmtT+5WprhlNcDf0Z/Y60uD1JHqQV7jQjTqaKq2ze9XTTyVe4a/IVmhIxIIt4FZ8Duxj0hUy4FoC/Tv7Hov7PRqHQ0b2kyZkzJnqMyZkzJmTM2ZNiGIp5FyViZSygpq5MSrwMRJpOrwUbwVVblNW5TyzwNyJ/izwLwfY7IxtR7ivgpFvRBVZCrQ3NpgbsynghUjHDIVn0Io5RX7hr8mJbkFSEYuLMZ4uxisxjqlFHIq0uT1l4Z6v8jrkq9t2UrwOU+Bb+B0fwLqVvBS9zyVFKsjT8lZV4GIk/T1pcmi5J3KXuUPdi4Hyh8MacFKZUh6lERBVVL2PVaUC1mQeSpfiUM0WavN04ISH00Faad0IZ4uuGafuRqe8j83/wA8lNO5BUtymkdMUkSVUoZ4FZjFao8kWlkslk2g28n4mX8irf2ZP7M6iCGQyHdCKuBWZlenYdUjHfSpTmTRpfg/cULcp5ZRwPkyPTqZg0V7D2ObU8wU6P4yU0zXBVUU1mm5ZVptmP8AI9NiJJ6dHXdKgVefge/gxXlEUGxFP2bGP1ZcM0/cjV97P/kf/PJRTuYlVH5FKxUs06lUnHBBVpZDUHNLPFnwMp5tUeeyxUoxUjRiKiSByfkTULUqHU3zakqFZkCpGtjE3E75QeqLVg9RGSE0KqODOTIzdJ6/2h6riCpGJ6dTNPTxqyk9al7/APojKrNFRpCcCc8j1EuCquqd2ZVFOm6h6Nf0PoWwmKtnqVGf2VVfQ0M0/crLhlHuRq+9i/7j/wCeSnkbMfyK9X/p1R/Y0HXRR+RXqRXQcla/5/5F7GeLMZTzartPk/8AQ1+R5H5KbNbi9xG1qubUlXQrVcWmzsz0/JVpJKT02PTa5tQl9CqX0Zirf2U10vlIqqnwNfR6rPVPUX0epT/l/wBT1l4pPUnwJvwRUyl7GU1ScshiyW56tTGTeCOhlXgfBp+5WxhFNP7ip/kOr82ynWKtdPyerlXKF/Bqb0r6Nvc0fptR1U/kVPdnh3dqbVdS6HyL/Yq9x5H7iggq5P3D4EuSvm1JVzZ2Vq3sSTZ30qdjwx7OBuUOpUvgdZmJ23t/h9WnwVc9CNMp5KXyNpU2o5HyVvaBFKT5MEKgWkRSvJ6lCHWvoyJJszS96s1+InsTvalwPFipogWgvD/0MGvI66/DMqo5JE9hkFVkIq7T5Kf9h+5j5Kl+V6xe48H2anNqbSQQQIr69N/iNPFyNrLYq2Rqe4gggi0s9ao1Ks1+RF0aRRyUfyanNqDyV2ppJMiexUafuVsFhJH4iVqNJ1bo9DyhkiraKatR8Dqq4YxcCQ1/BVZCY2Igh9b5Kf8AYfuY+SopGVC5FwU+TU5shckWiyQkYHpmPRp0PGSqnKmCnRg1dlI6snNtrbm9shlUdGlMC2kaUlb3tTaq02kknrVSKOTAhj3N0TJpPxJUlRTsyqEbMwFlTwz1KyqrclwIY7KztLMmZszMkTSbWjcpZO4luVcC4GVcwI/aLyanNvBTyTdPa1T3KFlwKmOWVRFqaZ8i0qRTwhZC/k12sNrz1IrXRpVQZbMncq5HwK1dl0yST1SZv7MmSSU1wZZDqf0epUfpZ9TcppzraqNbTx4JMiJHSQYmJBBBF307mTM2ZmSFXBMme82bF/JqR4tVwUDvTwMfJpbSfZ4HeRalX2L9RWh/qanyeqvKMtP6I0/s9NeGPSZ6bMSGIr46NPkZW9rO9Q+xD6oMNpIItQsivSwMyUaNdKqli1tOltyamsquBsp035tA6EPSPSZ6dRiyCCCCCCO3uSZszm1RT0UDKjS8j82fdyd2kyL6XuK2VvxZiFwMdsWYmJCItI+rJmRJIqmuB1t8u8k3mkhMxI+iHZjIvBBBBBBBBHSulDESjGkxKVBUM0fJWeOldqTIzZkbMaKeR0j5FSVbFJCGydzL4uLtJIrbiklmVRkZErogggi8EEEEEEEEEEECHZ2kpKuRmiVLk8d9UGJFtiEYK2LQ3A3IiexHZoNjFEIhCX0Kr7IpfQuTJGRLJ+yUzYygyMhW2III7sdD6F0ST35tBDItsbEmxFJgjFHpnkgi8W2J66XtaSWZGbMzLop5JZkZk2glIyRmZDEifo3MibQQYkdUEWqKebwRZfD9JV+0ejiPYyJtDI7GKHSenePshGxVHUrSSZEkk9FN4ItF5RNpdpJHV0yTbYjpYkb9DKbwQQPu0UqlFW49FDpjogjpkkmztBCMR0jIMGemz0z0zBmL61SYsVJiI2ITMCIJ6JFZogg3vkcm5uLIi+xCMSLT0NCJ6X3cmKplOoZ0jxGvoZJJPTF5JXVKMibbGSMzIyJRKNjEaduDK+5JJJLtuYkEtEGwqTG3AoMjI/sSxs3sqZIJJHVNoMTHpi7+DSpKaUjVadoI6ZMkZo9Q9QzMjJk3XVF4tJkZI2tuSySUZdMD6Js/5IslBmKq7tJPVJJJCI6au9HQq2SnyNJGRkZmZmZEk3xMSCEbG156ItCIRtbExMTG+I6WKlmA0QZW2IspItizFkM4ZleSRO0EXk3IItNo6IKu7JkjMzMiSSSbQYmJBCvJuQyCLbGxkZE2kknqkyJtkKomzZLKpNyGKSSDFGKHTuNCUWk2MmZE2xIMnfYRkb9qv4EGJHRJPYm0dqSemOrgVRNnsbM4EiUSzM2ZkTIrZEbkkJmNsRdHJBBJPar7u1pJJJtBiYkXkyJJtJJPVuQyDFmJBBBHRBBBBA0J2y+xoVUGU9G9pQrSbkksmza6JtPdr70EEdEkkk9EdjIyRJmZmZkSSSSSSSSSTebQOm3JwTamv7I+jF2i8EEmxDII7Mk9qvvST1SSSSSSTefkTaRVDU3aJJKWN3d4MSLz8SvuySSSTaeqDExIQyPiR2ExqbtRZMk/sQxUGJC+TJX8WDExtkTdoSMR0227U9SfUrqoYhq9Owv5P7Ek3m8/Fr+BBiQQbWm0EEEWnoaka+CiOwmRFq15tSxWyNuxPw9TuxeSbQR0yT0yTd0/Akmz61dq1NVptH0T8nU78GJFp+BI18N2XRSx7DGciKXeSZtl2p7upx330yT/AEBPsI8CY7rpkm0/DgxKtNtFVDXzF2H2EPuIi6GIdMXpfy0SNmr7v6O+6h9CHfwU2dJBwJkfFnoVmzUcvpnq/8QAMhEAAgEDAwMEAQMCBgMAAAAAAAERAhASICExAzBBEyJAUTIEUGEUcTNCgbHB8CNSof/aAAgBAgEBPwG0ao+DBBBHxpJJJ7WJiYmKI1R257MjrSKv1CWuO3PYknvxokntQYmJiQu2/hSSSMygqqMaqiKWememzF64I1QReSbt2TvN4II7EGJiYmJiQYmJiYkfBeuSSdDqMiR1I9Wk9T6R/wCR+DCv7PS+2LpUCoS0ZMzJIRgYsjVBBGqCL4mJBCNiSSbwYsxMSPnsWvYfUSF1E9kZGRLdcHpP7PRXk9Kn6FSNwIyR1FLHRU6vaLsyTaEYkPVBiReSSbb2hmLMDAxRH7KxXrrgVdb4R7zF/Z6aGlSKpMi2LzvCdquR28lPLF8GDEgi02hGBgyCCBL9rYr9U6X4k2ZUU07zeDdyUcXf5DGTDKOWU/EdsTAxI0R+2MQ7dQYyCNirwU6KeDp7XfIyrkq8HTEIggj4D0ToX7axDEVDGRbqeCnRSU8XfJU4Kp8DpZRTAtviPWxftrsxDHZ26ngV5PcLYlmOl10/Zmif4+G9b7k2yMjIn5rsxWbMj3EMxMbuqnyKtGf8E1fR7iKvsx/k9NHp0/V5XYntvWzyLTJJNtyGYGBiQjz81iH2KuL9VbHQr2gyR6hnaqvEyMjIn4lXY8i0shaptJ5+axaWNmaMzlXrR0rpHk6m5G1kps/h1djyLS9Ek2gggq57kmRkZGQu4xaKuTyV1oVUmYqmzzaopQxcCFyVOBb8mKGiB/Dq7HkWl2ZJNpFerk8duNxUohXp7jEO9fg8lVNK3YmhVJ3d2KzMYQ/sUwOz+HV2PIrO7syNE3q7nkQ7SU9x2d6+VbqcbEC2TPFmeRkoTExi4FabP4b7HkVndkDVvAxToqPHb86ae8718q1aEhUHizIGjAxMSLZtPccIqqhjrfJm/hvW7Kzu9LQlaRvcqJ7a5tVenz8GB10ryerR9i6tDcIRM2Y+o0U9Wp1EsdqW/BLMdhbqTH7Opt7TH4b1sYrMkkqe2ncmzpPO9oEu0uRkCEU+e87NGJ6NHlGNP0UdOmniz4v1EUrYoWx1OBc2kqHwU8D/ABOfhsepjEMqGzIqft0SMVtypM4s+0vytJJJT57zuxj/AOSnmz4FatWpK+BcjJJOR+0xcblKg/qqz+qrF+rrKP1Tbh99j1MYhlTKm5JOpV7BOXeCNEFS33JgXaX5aaeCSSSe07IYxv8A3KbeBWdqeDqcC5GiBiKm4G2Im0iZ+n6mdE95lXNloY7MZWveh8ldLdBTUZMyZLJZLNyXZvc8C7S/LSuCSRCF2XaR1mR6dnyrKzGU8HU4KebQQNWa8ley0/o64qjvvUx3aHR5FRuxdPIXSSIvtd8j4KJnc5I7S/LsIQu66oP9RFTUkisxx5FX4HuJQb22JRlSVuiNjKggxFSKkoUFLlT3Xrd2ZM8CKeBId4vA0eRLttudjKsyrJrHVUJ7b3Qu09FTbZDRTwdT8ikVqmV1vMogxp+jGj6MafoSX0bGw0meIKZ8mJiYkCR+nf8Al7Tu9btA6ZFQkYGIlGuCCGYmJBBHbdUcj61I+uhdSRVT4PcvAp+hSbkxyJzxqYhDGU2p/KytWhrco6m5TVIlsUc2fJSrTb0q/wCB0dSfB6Vf8Ho1/wAHoV/wUdKqly33X8h9p6VyQRrrUoQ9LsioYuLU/k7KzKqdyBrg8FP5CKuSkY71U+4S7jFeXPIiXZa13Wb6ZJF1U5F1k1Iq5K+rBRXlopcoYxC0rkq0+bJjYykRTyMV3TuUjPBTzarkxGiqtCqTs/y1VdiSSSnkpJIELUu67LRJVuVJfiUUKIK6cYgq6SfJSoJMiTpPwNEEavJVpp5IIIshC5GK7KCo8FHNuo4Y+CttI91bceDp1uzW9oIHavm1Ow7yTURIlBiU079jzofYgxRijFGKIQktDVqqBLcr3i6pQ6UV0nT2do0zZorKaSCi1NkN3QtmMWinYqFwUre1a3OBtNQ2OipH6fpw5qt51VObNkkELTIr1OND0IqYr7m5ubm5NRNQrrTBKiTkjRsVMgTZU6/BFf2eJZjJEaKyniytMO+aJl7FExub+DcTEM6nVdJR+ordW5I6z1Weqz1WeseqeqTJFneb5jcjaXNmikTUFbt50NiXZqFwQRpkknQtTo2IgmLQVVQhdak9Sk9SkhGC+jGleDFMVA6TfwK1SFZDGt5PB1PBXsmSVcDqa4Ka2UoQzqIXQ8lNTGjzBBW/dA+pUdFt8mDIjkyWqBoq6qR6jHVJ6sHqiqklks3Ml5Z03eqEU1bEzxabedFQuBcGRkSSSSZPStMWdIuk/IqWvBjV9G/lCpX0YHpoxRC+yF9mC+zD+TD+SmjyRZiuxxbGR0J8kHU4Kl4KaI3EIY0dSt0wkV0t7nSXsUjSH0qX4PSWQqIqFTuSVQRqdUGUorplHSq8WqpkdJH2YfRg3yenBhJTsSMrSEkroROioXAuB2TJJ1oWhC6g6oUnrD/VUn9RQetSKtPRBBiYmKIRijFGKIGIY+DwUjGVFVPBIhDIOoqfJXwU07ED8H+YSga3R5Ps+hKzJtVuikY9qxXdLEovFkMe4iCbLTVwU8E+1EkiYyVZaldCI3KuB0N8H9P9o9D+CnpYlP5CvU/Iv7j28ir351u7PBSN2ZWUiFfrUN8HV2PB4Kh8i4Z5ExtCYunXlMiW256amR9PaCRvYT3KkdU6fF2SLTUUuVd2R50V8FH4k+1Dq2JEyqoVWVRIm9KFdaIRCIIvubmK+h0J+DBfRgiSSSVd2Q7xd7ipEK/UbUQdV/Z4Gx8FfIuCDOlFXURRuK9S2kq63ugqcUyKkdJXsimtcGQq0PX1eiqnJhj5F/clnuIZ7jcmz5RXwzp/ij/Iv++CqrYyKatiuv6E3MsyF1IJPN0Idqe0h1My2ExMdcEig2PaYIVKXFmU6JJETZq8Hpj6ZizEhjpkwMTFM/p14KeikUskypR1K8lB/TVfZOFOLKSsbkiOBUSU00+EYodapF1aRaYMTBGIlZHV/B2fKK+GdP8AFD/w1/3wVcCpM9hUe9JnUifaUy0yYKX/AN/0H+SPNlZ2p7SsvxPBSVWpY+DyMp4synQ7U82jTn4Keo24M0KtPi1UkP7MTFFVNXhsSjyJzJgj0zB/Y+nV/wC3/wAPSflmEeRpeT2oa3I2tKHD2PTSF2keTrf4btMjfgpXtMfakPpC6TR6Spp3Hitz2yLpbwmdfp41bC4R5urO1Pa8DF+J4KfxK7U8D4FyMo4tULVSQRp6lW55R4EoZjKMTEa0et02IjRUVcD8ENu1QimzMjIfUJb8GFQqWQRdHV/B2XI+TxZqRSZVSPrPz/uZJ+BUUfRjTokVnZdrwMX4oRTwO1A+Dzbp8WeiSbU6617hNZKDfEp3ZRwSSSTaEemilY8E6OoVcFRRxaq1NnUQQR2KSv8AF2zecE+4m1XUVPIuuvIrOil8odNCEqfAjyNiFeBIdp1+Cr/kX4oXBSVciKR8HkZ0+LMepsyMydHUqWUFNUOR9STpqXAlG1t9MWWjqH0SylbWdqdEdloq4MzK8QdaltbHTVTq3KZZuZDirlGFIkRvZXdlaCDFGJDNze3gaFweBFXJSU8SM8jOnxbyPQ1ZFTxJnhFPNqqoH1KjbyOD+x0U87xrpejqUyRxZWdqdcEa4MF9EEEDpMYMf5MEfqv8PYo61VMQdKubQSKokyJJJJJutUIxMSB0yJQYbQQJH9ijbmyKtDEI6ngXjTA+nT9D6FDF+npXBg/sismv6M39HqGSJJtTortTzZXp7M6pM94JvU8SjqZmJB1qG6YRR+m6n0UdJoSHWvF8j1D1EZoyRJJJJJPexMbUlWioQjqeBd+FdMm9fBSUqysxCtkjIkl6FqxRBBA6UxUUrha4ZLRkT9k9iSSSey9LEM3JZkNiEdUpPPfggxIN0SPgTEOopGSxEEfFla3BCMUQY3m0kkk6JJ7E3WliEdQR57+RJNtyWZO2SYlIlA+zPZqNyWSyWMdP0S9DMWYmxFtyCCL7kkk/FeiCPgySTbe0G5LMmSzM8Ek3m2/Ya3vBBiYkaGQQYkWm0MxIsyPs2MSLSySSeyh/J9R0fkU9bIRF5J7EsTM7Rbc3FqdoIIIIItNneSbTeGRaNEaYItuTqb0ofw+pU6mUbC6rMtEk6oIsrSyWZCqESZI9RGZmZIla5MjIyGbktGRMkaIHZE3m0X2HGjckkm0aEx6l3cUNIq6ZjULIT+7QQR2I1wyL7kMxMTEghm5kKLxfYgi0K2xJJCJtkTfcxItsJXbtBBjFpMiewvg1MqqqZ001adeLMTAwMTEgjuTaDEhm9tiCCCNMi0RZE2kxGrruSydK+E6UQ1wJsgxMTExII0SSSTbe8aJtJLvJkSTfITG0ZE2i822JtJkiUckXggi0k3i0k9iSnvQYmJiQQRokyJJ1STbc3IMSLwRqggi0DpIsjYpg2JQ4IJJZkzITObRaCCLZEkX3GR26fgyTojsx3II0zq5GiLLc3RyNkMgwIgxIvBJBuTaR2nTHbp78EEXkkkm8EEEWggjXJJJJJJJOibSSSSRaBDpkxjVDHaLQQiLJXgi0d2nvSSTogggjuQQQYmJiYkEEEWjRGpO3Fos6T+5KtN5JvN4+HT3o1wQQQRaLx8iLukTunaBoi60Toj4lHegggjsSZGRLF8Wew0JxdOzV5HUST8qn4smRlaCLySST3I1Rqd2hDE71Xgj5dPwJJJJvFpJJvGhMT+C+y0TNqX4s7x8yjuzeLyTpgjTGhP4EEWWt3Ts6bR8yj4E3j4ECfw1Z6GIQrtXgi0fH6fP7q12mK77EfDkkprSKa0/2RfFehisqpu18t2R0+P3Ri0MWiq2RNmvmJFC27f8A/8QASxAAAQIDBAcEBggFAgUDBQEAAQACESExAxASQSAiMlFxgZEwQFBhBBMzQnKhI1JggpKxweEFNGJw0RSTJENzovAVRPE1U4CDkKP/2gAIAQEABj8CVLq9vT7Y1updXx2t0wq/bat1Lq+N1CmStlSaOyqpjuFO8V+wlbqfZWqpdX7QVupdX7DQa0u4BS9Hf96S1n2TOcVG29K+UFr24d96P5L6OyLuDP8AKzCkVRTHbVumFX7EVv3dlW6l1fFady+jsnv4NX8sW/EYLXtbJnzUfSPTfyata19YfiJ/JfQ+h4vuD9VCy9FY0eZWq5jPhatf0m1PNTMeN82qqldNoWYUiqdvVU77WS1R6WHebmkLWh4XPSr4rRVC2vksypMCyCr2n0dhav4NXsMHxuAX0lvYs4RK/wCI/iH5NU3etPElf8P6DE/AAvovR7No8zFStWs+Fq+k9JtXfeU7pTXs3Ise0tcMj2G0VkVRVvpfTtq317xTvlPsVVVWa2QshwCmT2DRgdPyXscI/qKjbek2bOAivp/T8XkHBSszbHgSv+G/h4HQLUsrJnUr+YLfhAC+ktrR/F19DoiIB4qUuFwytAJOWB7SD2le8U8IrdT7K6jXO4BavolrzEFG0NjZD+p6/wCI/ilgPJk00eh2zrUQ1iUL6RTW4WhoCLbL0i0ZZH3Q6i13udxPYhMBAcZ1Wz80cMYjJZIGS3KKeBauayMmhRcSfB6ql1e91updX7KfR2T3/C1S9FcPikvp/SfRrHi5fT/xXF5WbVKy9J9I4mC/4f8AhViPN81CzbY2Q/patb0q05GC13udxN40BoUUSJKgUxiEIQWyOajhb0uF4ClRM4pzYy4Kadx8MrdRV7hW6l1fsw2NIqkV6uz9HsDmHOZEqDbbAP6GgLX9JtnfeU9LXxu4SQ9W6RydkgHkHFu0QDFYRCBEVkq3FUF/LRCaPJWfFPXJO4+ISumFX7UC4HQkCVSHFe0YqHqozBjkuKYHGDZpn9IhHfpN4XYY4nKgw3ZKaauSapQF2XVDiuCs5QmnI8E7xWqoo/aQXALNbDVu4Kbj10APNNTewe6mKiESR5hQvE01Hggv3vHFNVnxROa5J3HxCn2tKrdEFvAG6UUNrqoJvFNTdPyTsNGwVJJxzhLQajw0W8UxWfG7kjx8ZP2kKFJ6IQQTUxT0iU4ipkbsBRheEeCGg3imqz43ckf7PDZlKSO8KOGmUaqgUJDyvHFBN7B90WyiIhHQKGg3igrMHepowRVfFh9qIb5LzUdAIJvYWnmVhl0Vkf6UbxFckEQLi0gE70DliQfmPJB8KLYaoCAHDxgXcvtMVGgujeLmacqrCXBs1rW3yWHE4jzuzugoQ+wIu5faU3UVFuF0zC9qMNKMVCKrdUKqzVFTsNVrncAtX0W2/AtdtnZ/HaNC+k9O9DbwcXfktb+IF3wWJ/Vf+8tPwtUv4e93x2x/TxMXcvAKhV+wjpmOSpFSaqKbgpuVbs1++lCCpdXR1Wl3ALV9Etj9xa9myz+O0aFr+m+ht/8A2R/Ja/8AEI/BYkra9MtOAa1S9DtX/Hbf4C1PQPRh8UXfqvoxY2fwWTVP0q25Ogta0e7i7xgXcu60vqs1QqgWS/ZV+xGSqs1QqgWSredGQWoxAekek+j2DoRwuJj+S1v4jH4LElTtPTLTg1rVL0K2f8dt/gL6P+H+jD4sTv1X0bPR7P4bFq/m7UfCYLXtrR3Fx7XYgqDr4mLz2lFVvVbYVXdFslbAWQW0q3U0KhVuoVRUFx+xp0W8LmOzaOwqFTsh4qLz2Z4aVQqrNUVBdXsBcfsadEX+0aOqnaHk1VtD8l7Jx4vUrCz5xP6qTLMfcC2WxjkIXNVUHQnAeOi89mUFkqlV7gLj9jT2DuN1FsqguCihcBcbjGEtE+KC89meCHcx42O2rdkOam9gVUIURggjebzpVuChdMUThJuaxNdVTK89EeJjtjwQ7mLj3+o70OyBwt0aqhXs4KcBzVQpoaB43m8PkI3FNO8qYukVCHzRwqbQCUYmLdxUyqlTNEcvGB2h4IdzFx7tn0VHqnzWSqOi2lmqLJVHeh2TaXBEuEZrYb0T/VtEM5IalJwWuITRi4VOaGupIaB46MQmfWJibioXwTjHnuWFlnTNYnmd2FRRUYwUvFih2h4IdzFx7sOaIwrZWSqtoraPg7DmgUJQUA3qVKA5I66jiKiX8rjpHjoBQCDYLPnobJdwUBBQyqjhkgK8VwU15KYvj4qe1PBDuYuPHuwTvDGxj5aEyFzRCcICtzjnpHjoC6gvF0TIKNxAU6KWd9Y+MHtSm9zFx7sOad4ZZ3hGcEE5OudpHjeNIXRc2IuP1tHyXkq3S8VPalN7aui2492bzTvDLO8IgOI4KZRTpXHsQoqqhMqnzuyrdO871SV8IquhtHxQ9s3joUj2cNAXHuzead2PLwOz0DK5yeEOKPYZKqoqKl/7afFQzuhmhEqZKz6rZ+fih7ZvHSooKOhTTHeG807seXgbY3HCJIJwOdxKr2EzdRUWysrqqqz0fUspGfmsNiwvOcG0uLcJjCKNniY0ipc6XVN+lsn4hVjpIB/pVniwxhByxOtyHZt9XGCnaWx4MH+VT0g82+JC49sO5SQuPdm807seXgddGnZRVESC0Q3rW9MZHcLNyn6TaH4bH917T0l33AP1Xs/SXcXtH6KXorudt+yl6LZc3OP6qVh6OPufuvcaB9RkFEf/ACsMaKBqvMe9ROFkHwh9JOqBhAUioRi3fBW1rugB1X0uIthKGSa6IL3auFEERnAzp4se1KHby6KgEsrsrzdLujead2PLwT6OwtHcAv5cjiQFP1TeNq1Tt/Rh99a3pdjyDj+iDhb4yTCGAi+gVANFovjcbo3YSpr2dPNTYOqdBkxS7C3PJFrKBOMaLONzLQ5oFsetfFBce1KHYUVCqaXyVeq3rzuj3ZvNOuGnyQ7/AE0B6uEIZhazbN3JBwOAbgvauQjZPJzmiSThjIbuxFwgVMprdziq3NRumdA704s6oxAmeaIMTuTyGgDJCb4LUpBOsnxkZOaqGSnn4kLj2pQ0qqt81TSNGqFWjcmxFTW6Xdm807QGgVy/RDwMcLgsSoh2IvcCaI3tTo3DQPRaxiQhHaCxjaW0Y53QAjJPc3LJeqs4teSgLdwLw3LwY9oLj2pXPsaaMVBYZrCI4lCPrJKMYTWtLSn3FvNHSnfy/RDwIyu3IGN0Mu0cjxuFEAgFzXJDRjFfmq8lhWETTcL5NEDETTmua543isVFtWyDi2BKDXkxDZnz8SFx7V3Bcz2lbqKkzVHzRlGKECoCiiTivjG7ep9xbzRvjFM3qiohcEO+nRd53VihNclnojTdxR43CaqgjOhuENAbkFCKiaFYozTSXjAJxRGAQPmjXE5CcxmjrB3mvc6ras1DExS9WOqlg6qjT95ezKiRDwoXHT63QCNm+ovtPhKj5ns66UxE8VAtCJhnU5IxHzU1NT7o3mjob9FqHgRlcYXctIabuKOg1HjpUByvhC60Iq0RhvVq7aJgAaYSg6sDD5I+a8iuCEc7qXG7zFPCh2PM3WYDY61FTLrfbf8AScnfE5R7mGmBxATC5qndWo6Vb2oeBG/khwRN7fPsXcUeOg1HsBc4ptpXCU57W4RGMFZudYzBk6NUXN2YpoU7uKndwvIyqO+nuvM3WbtxVgd7T+aDRmiwzgvSP+i9O+NyA4qh6LZPRbJWyqXVC2mrbC2/ktr5KpVSs1n1VPmqKSo0U2UANw7s1HRpoM5IeBG8cEOCN9nw7F3FHjoNR7IwrmtWQWU0SSSWHCHbvK7FdFCF5vx5t76e68zc1ej/AAn81ZgugFis34g4dFa+dmQsO9xVdCqqqqujRUWyqKlzLNs3vdBRfJ7ZdEXEz7s3ijy7Gz5IeAZrPqoQ+apdDEYLaPXQao9g7ijoNR7GeSjLzUkJs1WxhmscSzBF0bhRSQU5blXK4KNxBzRYcu+HuvW4FxgrLC4GAKbzTkQ6MCISUB6M9BrbF0076OMSvZrZWyFQLK+EVVbRVSqm5sa743NjvVh6yLNYO/VPfGMTHu7eKPLsbLiEPAKqq2jFZ3AutoO3YV7Qk/CpXyjz7ExMFkotov3uDDVUKxC6uhRU0Bs/hT3u2o6pgoyUA6F0SvNQyVV56AtOR7pGCgHYvPTPdet1Oq4Ic05RKoogEKnYyY7poQyJTDGseSqgrO3tJhteneGcUeXY2PEJvHwTJVC2goXALa7CqktlUU7/AN1l1WV9D0UcDuiEGOPJewtPwFCFja/gK9haj7hRYLG0LsxhXsLTooPs3tjXgvZHqFsf9w/ypXQv+egW91LHVGme0HZfSMLeIUjBVkgcRTtYqETcwas5yOlslbJUgVslU+am1UughIXC8ny7sz4v0Rc0S4rLqvd6qrVtNW21bY6L2nyXtPkrMbim+BzVFRbIRA7TWbFatnYkebV7H0f8C9j6P/tr2fo/+0Fs2H+01f8AK/2m/wCF7Qfgb/he2PQL271/MWn4l/MWv4lB1takebioC0eIU1l7S0/EjC0ePvFHXd+JVdj3xWKkUMMyZcVrAXVgoled/ktwuhdHf3s6ILa6YuGkXShlNWLWhoLWwdDMosDjA1C1qXNJ3oqOnqhQksll1VVHELqKmlq7gnThAd2BiJFe71Xu9V7q935r3fmsui/ZV/7VV/4V/wAzfQIR8DCmVVSMU7jcT5KEe8HQO/JQJjozovO6Krfw7lMwG9E4WiO5MtMRPrGB0xDy0z2w0sJbGeaP0Vn0WSrNEsgAgf0ioxCmqqqqq31Krdno0WwptXs/zXs/ktn5KLgDxCo3oqWf4Qvc/Cvd6LVh9gKrhdqmF7u3zRMD1QbvVVC+e5ZKgRRnS7z0SVHQlow7mNM9xpp1VVVVVVVVVVW6qqqqqqqqqqqqpVStp3VbR6qpVT1VfndsnqvZnr3rVaYb1D1R4r2am1vVT9V1WsfR+oU/9L8lI+i/JfRP/h4Z5qVv6E0eQ/ZStWL2oXtAttbS2lVVUWsOHetZzQhh7nROQMbyndkEFaMfAxpKhVWKeBSRTSoIcLxfWt1TFBE3/wAz6N0K/mrD8JRd/qbAw/pKNn6yzbDMr+bsPwr+asOhX8x6P817X0Zf+3P3l7OyP31P0dv+4EPXWZYeIPcZqMJbk0gmM4jdpnRhlGKIwgx+XhOazWaoqKncI9lEOK2iqnuEI91MgY705AooXPur2MlVAqJK5opi5IKgubobk3cJR3qIRfhEDuyRF381ar+atFP0o/eTnMt2An6q/mn/ACX809fzVr1X83bfiU/Sbb8ZU7a0P3ipknuROODoybCt1myM2Eyw056Z0cWFrfJognMkA6EQG7vCsuiy6dz2cvCjp0TrnDeuVzuHZkppnUoLncU1ckOCpczjcUYrzRBVVHz0atHxCIWrbeju4M/ZTh0053OcbWFoDJmGo49vJEiJzKeWtc4NETAU0o/6uya76uaeBb2b4EiS2o6DoOAjCRzRc46x8LqtrtXGIllv7gR349i64p1zuHZlN+IoXlNuF7OITuKoiSZIwnfT3qx0Qj2dD07gcJk6Thv0gQjpAMEyZDTnfDw0BzsI3wiix2SsHOAg0FrgK+SbYQg4mE01rTGSg0KBvdSLRFf1A9hHvxQ0NoKoVbnX87jw7MBM+I6BTLhe3iE/iVDQi52GK9q6Pwr6O0Fod0IG71kWwjCEZ3DSk4OG8aLXAwgYx3LU9IJk8U31uneMRjCShJghnfizOlAabeCco6Tol+KIwwpzR3Gl0DdDw8XAwWJ1pOybCGHJYbRuEObqiOz5p1vaveH4jAYS49V9L6Y5vmLNRZ/EiPuKLv4khan0m19X9eUFEfxJf/UGnkif/Um/7ZQ9Vb+t+6R4MLqKhVFRUVNAXHQPYNnmdApvG4Xt4p3G7yuNoRIKKhc1++twkBAZZoeQgio7kY/NFx0THkpXNFn6TiBEyWQgVCQ46B0xn5X+V0fkokkyhcYUuEISCeDeRvWampROahmuOjXl4JsM6L2dn0VGjh2AUYItcYshHCaIljsTYUzCwOYS/wCsrL1bpjVKAAiI71G7ASagw/o7QjSqq92HYuuCHbDQKbxuF44rDSJULnhWc5TKhAQUfmnarQnzhMSWFsZONxQEI+Si1mFv1YxUcIhuVILFaF06nNCS9nlCRz3oaAwUhczGzG2M2xhFG0bZh9nigGvN1s44ZDN8P/lYRVMdhZq+VeKDgWxNQBCFzokh0oea1otfKDSFhTmOm6UC0y0MX+nsIfVwyT7YjC4tczCxkhEKOSc95cLRzokQkgPUCOF0SSTE5LC0wDgIp5XkpDQlJRUr4Fb9Oqqq3VW0qqqr22yeq2XfiWw/8X7Kj+q99e8v8gL3fwhUZ+ELZZ+ALYb+EKYA0wjPkvqmERNFhxN8lNxE1tQhuTcT5QqW5ptiXN9W36v63R1YwHujRJiB5ALbK9oVtLavjv7iNBjWM1gNYnNZXzs3x+JGFNA6ZRRAvCrl2gM7o3FMjvUEFS4KLVDCYqjuiJ1ui9TaHzbc2z3glQzQsGGMJuQg7ioznOqJ31vDmim/foB0AYZGiaY60TFobADQbisSCG5MhLfdWd5vPyuaHGDYzO5P+kJhExOYCIiYw1YCpWbXBPtcUDabUFakWj8NpIxlEIxJ8roIRdGSOGJGUbgnQkNINRlHzQ8vCKqqqq9nAgQ4IujEZTQcSJe6gLMYZkmK4+cbocPz0YqulHd2uJtmS3eoGo0z3WYVOzqoF8BwUnx+7dRYUPJRgojRz6qh6qGE9V7MoNFi89VH1Fri5ot9VaDqth/S4xY18QRPLzTxoCQEPmp6bQ701josOt6z5dgHNDTAxg4RCccLdfy/JYZAtMZjNF2/sGmU9xRwghuQN5N+83iKzioaUVLsY3ZrNZ6dVVVvy0aKd0ll0WXRT7QwU91wxfK7n2dVCfS6h6LDIfFJe1sR96Kw+ts6bWS9tYn7yItNYD6pqv5e1/3P2XsHf7v7L2Lv9z9l7H//AEXs/msTQLP4MkcLi8fWOemdMaUYz3X6withqcQwRQF0TGPFZrPsJQWLFZjitbDy0KLYK2HLYd0Ww7oth3RbJ6KmnVbR6rad1uhBObkULi31jZUORQGEcd+gGwFYxz0BCPmoQnoWjfVtdiFTldLTm1RDYRyCfZ2otLB7WuMtqlFruLR5CK9U0xs2mLThAJvmw4oSIcpzRhTz0mC0IwFwxGOSMN9wh2/PTrfVVVVVfssuioz8K2LL8C9lY/gXsrH8K9lZdFsNQ7eF2LFWUFGUAq3/AHtGVVq/monD+ILLqsuqqpMPGKEbK089WK1GwHmxaxKLrY2Zh7rnOEfkvVWbbKxsx7rM1UIscA4HzgvWBzCN2OaawuwxMI4lDE08DdVa5IiIiSjBhLpy91V53wgbwpdtiEIeZgq2f4wiINlXWC228ioAoXARVe80CoFshU0nDfe58Wgx2b3CAp0UULsU4CUVNNONjThwRwiiifS7IHUOKEpUQabZj2i0dJv5rFki6OsCC0QiDxRMdoEGV8TJBzfWhnERinYI4fNF7bF724oEj8lbNb6IfSHQkQdhWMf4aI+tgC6Ov5Jg/wDSGGOKABM5/ojhsYa8PVjLyVq1no+F2B4NnGOGU0U1jSJ75J9oXNkZzndHCZZ3HQwiyZqnbhNa1VCSM+480O6juAWI71ZsnERiq3n4tM6WfVVPVbbuq23dVVVU3mC2ll0Co3oFRv4VRv4VF1kyPkvZtWWkdM3m4cbjc8neo6FB1VFEhUbpc7qrUaXcF7C0/Cp2T+iodIWb44YEyXqj6/H8X7LFithzC27bqFLH+JOaKA9idJ2LdLinAPIxapG8di712Omrh3qxbZ+lFmJuuXjZKIBj53AttG2ghVsZLUZhG6Mbi1r3AVgCtR7mxrAwX0TrRtnGLQXxgh9LaS/qRtGxk6qdaPcS91Tc3EIiM1GEAck17ZThDFFH1jccgKwgvJEi+B1cIlKZQGTaBDE0iMxEXuxAxy8tHy7PmhcZqqqq35KioqKioVRy99VtegUnO6KcSjBro8bh3Yvg0xi6PA6UA4gwzCOK0zpBe1/7SvajoV7VnQr2jPmi7G3egd1wdAGG8KNOF0ghG6ndjcOOg/inUuefK6NVS49g5NcHV+SsATH6IIqaOJjzD+qCOKzeDCWuoNsB+IoBtn0BXsbX8JQLrN7dU1CACdxveS1wEYxwr/mfJbL+qk09UGElsc17R3RbZ6IQiCKQRIcQTcFKa9ZliwrNRF0NCIEL6X2AtLCOHFjw+9uR3XOs8TsJyUb6LEYRWSy6LJZKBDeioz8KwgsH3IKGiIx3LfCSbje5waINjle3A4PjuroT7UXFS7gbh29CqaFQrNj3Ng9mIkPoVgFnZwhDNYWlpEAaxWV8D8liaESG0879n5rZKmCvZrZWaq5VcsWIqZisll1WXVfupQ63Q7eCjobKOqDHehKSJ3pzd9z/ADlcCTAQUUCN6M7hpYW1KhhjDLEsFtZtcW2Yk7JFvqLIubtQTRZWTbMQyzRiCEyJIEZkL29p1UfWudL3jEKDrOyPVNb6lrSQdYOKGvUq0O5AsLmSoCvbWn4kY2rz96+dnZv+IJmqxvwhAIXBoFaaBjFxNwDRErzutPWY/XxGCFIIztQMTYTyzXpHrWWnrZ+qIN2vXcidJpZ7yk5p5rZK2HdNCN+q0nkhINhvK1rSPBarGc53TENACMExhxGzLjrgbQCsXGwLItOt9dYpENqI1Vp6tgEiTE+6nMqd40d/aC48ezyVG9F7KzPJews/n/leyH4jcbh3DaC2h1W181tLaW0PwhUsvwBezsfwL2Nj0XsmfNbAWyqIgREaqUVtOVSqqqqqhVCy6rLqv3WyVsO6LZPRUN0YhahiOwL8qXy0SoR06KigpJsoIzyTWipE0OKMrhpDirZgfB/CCcTXCEWtOq8zTOC/dNQgCghNM4FYY5q2EdU0uhEdLxCt1nxUIZyTY1ugCcO6KExO6AqjqkeV0Y3QVprgOybhjHnkvX2npGG2Zhwt9TIiCtgy0drSeICFeqjc3XDQa5xWKypoubzVZZLVinHFyWZRiB+ELYswOC2GE7phTsWA7gFKA+S2igSswVv87yDXQFpZNNm2zb6uLKJsYlooCUZCfyWFpM5SzUDw4Kt7fO+IKn2IuPFC6ioqaFFRU+ap81Q6BuGke6VVe4VK2itt3VbZVVVe7+ELZZ+FezYvZt+a9iPxFezP4lDA78SkHdVRUCoNI6OXK5/K4IcU5u64cexisUMpjFVWriIRyQoOaypCanJMfimTRUCCxRzomcEXGU6JydOCIjzullcYpnFN1q/JC+DTEb7s2uCLnuJJmSc72+rJMp3P/wCILSf+XCqx/wCvDn6owuZCATg8+bQAq3kQGnAqRUUcoqaAxQKjkgZc1KSlNZzUzBRUEXb74JzMUsVAZHzULo0R36DVPsReLjxQ7gbh3QoBjYxMERAIW3rGNrItQs8diSfJPsmixiwRqVha2ycYRk9OtHWbcLRE66gGmPFFpDgRkU2s9/fxoHTdeOKgqdlBH1YkE6O5EyML2KCF1nwRT0+KO5DkpXtTU0lOaP4XYRMqlYmWNnZeTCdB+NmKLdWdDeZ3wOSju0MGKEZIx0or/wAkicl5NlM56EFVRpduULnYI4co3zVm7/RwssMHMxRi5Ns22QEHGEKlQgVEWjCY7AM1BTuM03RnReWg24oXO+JNuE1nfRUVCveVT0VfktsLbaqjQHdKLCpFywu/1UpxY4QXrPX+mA/dRP8ArLee+z/dHD6c5vCxKtGt9MNpEQw4CE19m6DgYjinOfD1hOsrMGEhlpmIWy1azYKoUiq/NSis+6nTN44qKl2QTuCtFjjIp3NNTeNwUEy5yfxVBotTXIaYleWgyNRvTfoLGyhL6MQisBhJEbxfJatawUsQ34uwM6T4odhCOiEXtt8bmQwxZtIeoxFwOrATThaWjsbdiDfzUMJxb4ogEwKKO+4oaUDoNuPBC53xFM59iOxHcsrsMFsR81sqGvDdiVCs+iOvVbQUS5vJR9Zw8k2cdPZUIHqtUEnitUPbGSgYxOcFN0eSm/5ImI391qsr6IVKCKFw49pFOcG5Jx3oJ3G4cbhcxBOT+N8WtK2StgqztLSwe1pzIuamutrJtubSLWNjmrOFi2yxCEA6qOyIOhAOigVFnq4mI16I6tm2my3cn2traWZtAdlwrEI29rAtGoWx1jEaIKIvBdOElEYnQ08ImsLZrWUxdu7OsVEEg+WmQh2TLj8JQuf8as+dwuyvrdMTjWOStBDaVFRDzuKi4RG66Xdc1Uqqoz8IWxZ9F7JnzXs/+5UPVZqNNCiobqKiopSVLtZoKcwdyHY1u5X7Ll7wUnE9lioIoqZTrhxuFzEEU/ipAlA4QTucFrOukrPGbX1YpFBQKL/W085pvrHl2GmlFwxAZb0D/p2Q+rEqIs2tG4RQjqDMhW/qgHhoxYnSIFzXbxfBQmPMFGelFQUJKOjx0JaHr/WRtMcCDcU2MsQjNHfoFDsmXO+EoXP+NWX3rhpCKstUSaowhFVPVbRQjNTa1O1Yxp5Xw8Gqqr3VssWy1bHzWyeq95Vctr5LbC2mr3eqp81sFbLunc5I6Fbqdjgwuic8kcQXtAfvJ2GgKghxW0FCKk5pVmop0E8eazBRbGu9R1CthqaR6LGCh6iNp9Ra/oxCmwg3RM1qsw89CIkURDW3qV7jB5cK5tgtpoP/AE0PpGyy9UtZgf8AdgsYDWjdiuJAiB5zVY6UFXR8tPimutW4m7ltubxUGWzSoNg8+S1jZt+ZWOQGW9RmtUGF1VK6ioewZc74HJtz/wDqforD71zTJbQWfRUvw1iM0LJ1AcWJCPJFeSMqXi4eBxWKKh21FRZracpnTPeoRlwWy1QNm1Ts/mqOW07ovaL2jVItKY6FCo4HI6rk6MVMhRjdtFarlmtZFGdp62Mh7sNCMJb7hqsEPqiCMJISWL1Qs4gaoRXpFo+EgAAidEP2G7zmvpC93EwATg2xa7zRjZNG6BKwiytQeK1TXfJTs3clAy4qPacLxGixNeQfqrVdyzK8lvjpazYrZCo3op2dn0XsW8orC1pDshoWdzvgchc//q/ovR/v3N4XlTWH5ocDBYogZKN0HNmhVTirTiU27ldyHgLuN/3VRNR4o3mNxOhJQuj3ETUL5AlQhNU7OqrdRUvqqi6pW0VVZLYigYKhuqq3PtpYWEDQsgTGDYUvwEgSqUIWrPwqNpaNl/SmGwtA6J+rBFmGBmY79BuoGwq4ZoPBjPZK1TkhYWYa5zZucaBFz34+cAtRlmD1WK0jMV3oizg1TeVNxPFU6Lf3GESqqYCoqKq1fnpM5/loWfC53wOQuf8A9U/kF6P99UKwwEvNVCw5oyQmrK1bAnYcgchVYTlrJphKEFAptqB/SfJSyu9Jhli/NNua0VaJ3ch+XgNpxXnNc0fhNzUfivb5wTuK5p3AqKC5BDgVyXNc+4imjWamSq9lALZKpp7TRxU7ZvJVcea9mvY/JbJC1gswta1WOztdXzVQeC1XQ4pzcX0RfTzQIqFjmYzubkVN56KVj6I7jYLC2y9EsnCjrNuErbU7T5pzrdrrUYZQTxZejndHGIosOSrPgoqNrbYPJoQh6U1sBCBajbMfZ2ohEFpWH6xmUFOKhRAtc57jk4QgqgclW6bw1ajsXCCJLXBozLFVp5qcOR7pPcbmjzvs+f5aFnwud8DvyQuf/wBT9AvR/voom6G8KWac1ggAaISnGKi503yA4LCNg5q1nIUHmmn/AO5NYoyzTiI3ek8HKx4H87jG7kPy8BtfiQPFQ8/0R+Eqe9BH4k3yuZyTuK5hP4H8rguQTQ7zR4LmufcRoAwUCIG89iONzVqkR3JzHygtootrBUvpdJx6r2hVQeSmxh5KdkORU2PHNf8AOClanm1e3aoqJZiUNYLaQHrGqT2dVKXBy1LSPGBXtGDihi9KspcFG19KYR8QXtG8nraJ5qWJSYVKy+a1WNCwG1dg+rGSE6yugidJpfYsdD5qDbNrOEUA6ouI7mfhNw432XP8rwSIA081Z8LnNeC04TI8ELnfGVY+WJG4qRTGWeHG6c54VF9s6as7JmJoZU4tpe2f1QDvNWdu2zjjOtNA4hKgIgmHA02bgYtM16vAGx3I+StuJVmNw/VDeiRTwIK1+JNHFEef6I/AVzTUT/Wobxcz7qeuYVp5A/lcFyTT5OTuC5rn3UVWcEIuKiSOiPY2b/ekmgEJijBHgiE7igFrOs670IGPDtLWIs2wdEOJmYZIua0kNr5dtha2JUFiiYoQrGKByhcdGDRFQJmNA9rTSd8J0bLn+V7WwEYKyGYirMOhhjNPgYjD+iFx+JN53CAiVRRLZoHE7FnEKLvSMLvhki5np1i4/VogbW3sjPZxKFnB7QYicUbDGRAbqqABRgXYQmkCM0aBWkJzKEBGvggirTim81Hz/RfcK5oIz99MXJM4tR3RQ4j81a/CfyQQK6Jg8nJw8ijxXPSCHeqpnJSETu3qziMMqbltST/gQaQU/igDdVVWSm0FezPIr/mhStiOLVK3YpOYea2Yr2blNpTiGtYIQg381bM+uAOCE7mwhTJHOWnQXud9VpWpNCVDVPi6BhJTEN0dOI7KioqFQqtiHFUh2Zvszx/K6qChuTck4RjKHyvPG+CxYrhhY6dPNEQJAqQpscOV+raPHBy9s9GbZ/0qJaz8KgYEbkTExUPBArT4k3gVz/RH4CuaCJ/qQ8ppx5JvEIsNIqHmFbN3NJXJD/zJdEBmMSdwTj/Uvvdxj3ADJNCEIRVkc4L30RPYzRkYCidH6yMh2m0VtlENtHCKwswuFdxUHNIPndXsDK+0fGFAjvU8kYiUeqnXuM3BRxEqHq4rZ6/5UIxur2QP1r2XgQjEb1GBTRCiJO7S2VQqrkP+JeIUkv5izPFStLN/3017vQA+cXQniVo619BtPVuo2eqmY7G0a33pp4tHPFn7sKqZICj8t6kjeL9v5Lbaqg99CtfiTeDkR5r7pXNNmnfEg3dM3Nh/SnnzXRW3AnihwX/m66RhIrkUY/WXNHiOwqsui2WrY+azVT0W0FXRgoqg7KYTNUiQTIjirMDJQwhO+FBO49jRU0aqqw2gDm7lFk2fl2VUUfiueXRb+qbwj4Ezne29sEWGUlDmnN3drq2toODl/MWnMxU/Vu42YU7Gx6QXsocHKh0BBTktpScqrLvreKtfiTeDkeK+65c0E/4ruq/CrTiU7gE/zDvyQ4If+ZKHkh8Kh5FH4lzTuXdc1tKoun2DCNwus7okShdifUoYHBZdVRbJ0a9jsABQ7NuKNTBHqmtPvV4KGY7XHl3VvO9t7WYoGPJOdZQIhBBrICOZKtHASJWXVUvdiyEVq+pVi71XozZTgEA+zYY/ViiPPTlYu5yUHsc3ioz0AomMVtkfdURasUnN6rNT7L3ltfJbTFkea2HdO2an/Em8HI8V90rmmp587/wq04lO5I8D+S5IL7oQ+FO4FHiuady0T2c78lkqqqr2IdigEIGIuGIUUmgXjQkStpTa08lOyYvZkcCvfClanmFK0asjzWyqHRj2AVbrOWW9RjCGSiU50Y8dA6I0AIDuovxCMrqITwp0LVroGpbVB7XMLhEwIvnFSiOKpHknwENVWVs+2eHOnBMY61dBm5WLbK1eWOmYonFmtv5LaCyVDftKLsJP9QiEWBoa0mMG0RMPkqLZVD3XbKnhPJezbyWy7qtpw5LbavdPNbBUwRotVpxCbCEIH80QBGaMfqlc1Z8VaXBfhT/iKdy/NWZ+IJ43D9UOK+6FyR4Fc1zT+WgezrobUOS2hoSadKTStYgLCDoSuqm6dFHSro5c1PTCpdZt3NUKRqsRVdEjwBwtM1tQUnN5qQHJV6rbPJVN+SqimNjRVTTuWq5pUCIG73lMHmVOzBWzBVR1h4FJ5UyDxC2GrZ+azUQ5FuKuSDZFGU4xR4Fc0zinmSJiEzkieCcTQPR4qzfnEp/woL7iHwp3Nc1zT+XbjSEskCbPEI5lalmxi15nipXjHHD5LVxcwpWgUnN63Z30UrgD3OagNMXDgpikqo1pABCPvSvj4HVf4XviC9oqx5qiqFtKpVCtlYckLgvZjkow63VujaN2jELWsxHyR9U+I3FQIvqqqpUvBKqqoFRQmqoTVQU4wzijHMpkAQRGqMdy3Cal9UKzIzaiYjOSJj71FzTuA0BeOwbC4o3t4IcU1ufY1Unu6r2hU8B5LWsG8ip2Luq98clFj+qk5p53UN1FTtSj2LOKdvJWHJNqjojwLNQOF3ELWs+hWrTS1wcOcFCMAqrOKk4qZupc5v8AVdXsKHTr4LW6gVCs+iGtRScDzVCsJCMt3btvdcUxBMuHcKqVo7qvaR4qbbM8lrejt5FTsXjmtq0byWrbhStGnsTw7EJnxXEU3LyErwod5mpKY73z7GbR0WzDgtp/VbQ5tWzZngSFKzP4oqbT4fJ56rI8u3HC83s5IJshc3vVSqrJSIKpe74T2LeF0SvnFbzeJ93pdVVu1XFZKbTyKqeiqNOHYgw0aqq1ieQUBZWzj0WrYw4lZBVvmVLsJqjVRZqvjZ0WckE2dw79VTAKlJGhkpiHYBFHgnEGEZaHDuNL81Tt6qqk5ReQ7iF7Gx6L2Vn8/wDK2Gqg0NV0EGvtyQPIKbj2u18lJ7TzVI8JqY0KqYF1fFdsKUDwKmD00zos4XNuHfq6Ewpaq8tOAnG5o7hUKt1B4fII6vzW5ar/AJr3VsHkVWHEKUDwKmCPEzpScRzUzHiFOzbykqOHNbXUKRb1u56LeFzbh4DNoVFVSIX1Sp6BCmdKl8PG6xWSqFkqgcFUrZWsCpPUT/lbI6rcpPb+SpdXxgIaLeFzbh4FQ6OrIqBuMCq81GMYaMvE5AqYgqt7ALa0MlVRxnktpyrdnBVC/e7b/VTAVD+ar1kt/DxblotGIRhczWuHfqqc1KzCkAOSrdrFV+So0r2Y5KBa5Sf1CJ1XKD2/onT8lC7V3QUxTvFFRTVe0EV7MFbAWwtlTC2Pmtkx4rZUmtXs/kvYt6LZIUfmtoKLSeXYDislACMFmttQislIrbW0qrWcVtLagoxVFtwVfkq/NVmpH5qbR0UC0x8ltdQt/BTB8VhC6AKh36Z0MllfRUVFVVVRduRMI8FuUIRUu5Uu2gsythSEO4C6ioslVbSrdCCoQv8ACMvmo4SqFQwhHsIxUyVME81QL3VULa6KBj0UIFU6hf4Waqo1W5b1mtyopR6KbR+SyUZdVOH5qUBwMFMR4hQw9CveHFSc0qh8LPhlVVVUjdRVUzFVK33TCoeqoeq95StCtV7Vsx4FTZBbS33lbWjQKujT5qnzWx0K/wArWc1q8t/aNVQFtR0p3SVSpKMStZV7KjVJrFAy4KGOIvqFkpKboLfdlfUrZF1CtmAuzukqc1tKoW1d5dVst/Je8PmpPH5Lfw+xlLsr5lbSzVLq3UVOyrdNgUjDipa3BUVdCZVRfQqhVJea91ZrZVCqDthBV7Ct2d1e5/sqqEVthQ+cFQLJVu3qh5L/ACL6qoW0t/FVgqqbgpOF0nXfuv8AK/dazR0VIc1tQ4hSwu4FTBH2G1DdNU0KdpRUuqqqoVVVSctZgcpRYpTCMqf0qcVXqpXbMV+6mVqhUHVe7zKkFsuiswVMr3e1roUuoqaVO5ZXzUIfNUN81+6zVSqKRWsfktpZwWar8rqj8l+6qqxVIc1ko0VVu53f4KotqHNTgeS2ehW1DipFp5qYPazMFjba2bx5GfTxOqiVTsKKl1bqLZVO0rdMKMAVBtmYr91rvbFTjyvoVGQW8eS9ph5LbxKP6rJbQUzHta3V71VSUgSthSatxVCoYStped+aoVMFfvdIxU5LbKqpFV0aragtoLfdJblUFRiFSKotkLViOCg4A8Qtjoq9QpT4Knjk9CQU76KnYU0qqqrpVvjEqIJKhEKQEeCmZea25ea2gtpVJvhFbQ5+BUVFkpxWaqoY5cFKamqqqp81Ni2AFINWy1Tks1vX7KEFQr91FSa5SCzUlN126797qraX7qRHNb+CrDitoLJVCmVvVAqfNTas76qvzWtDmqHkVtdVKB4FTEPF5KqqqKQ8CpyCgQeinFbJ6qIBuyJUx81ESC2lmVJpWwFOCmbqKiotm6qkbpjs6XTVQol12zfAkxUzdT5L9rqy3RVIqEB0VYKqkspKB/NVKmoiBXu9Fsr91RUCzKoty95V0Jr3lmphUks1l0voYqvVSU1QqYgqlUW7yWyqHmqLaW0Cv8FTIWqXQ4qcOio4cJra6qQjwUwR2WXMKgHDweqrfPvlVVTN0gqaFFU9VtDmqqt2ypN7Cqm5V0JhUVFsqbVsql2qRfMr/CiHELaioSPJQhDgtpSupFS/NTKqpzUhBa2JSYVrRVT0UipraW9asQqlVKqb6FZqd02lZqd1FRUU8QUdZUunHqpA8ytia1mLY+a2oLaVVQclMuC3rZhdOakFIKaldMKRW0sj5qhuqVSPEKcRwUn9Vv4fYmnZzF8hdMqqqpnvdFqm7K6SqswpFSWV1IKoUoKBUP10Jqb1KirdJzVtKpKqqEqE1IxumpOIUIhZKpW4qbvktUqa1SFDAqFRWV+zFZhSKnh6LMKsVQrWDbqhUBWyqwUiFktsLJbS2itpUvzukXKbWfkqOHzUnDmqR4Kfic+717Gqr2s7pdwrdI3ayoeikxezithbMFQqhC2Vrfkt62bpKY6XZX1u2ltqToqqroblRSXms1K6ZurfOSqtuHJVW0eYUjBTgpE8FQBaxapfmtsc1/i6Mb6qgVLqG7es1IqctCt1TzWyD8l7zVJzSpjw+SndJTup2VbpKl1VVV8Jqq6GqVrQW1BQiVmLpQCrdSC2joTEdCipdWK3Kt1b87v2VLpiF0lmVRbJWyqKbSVDDBbHyWYU8R5KhCk5pUyAqBRyUnKIGlW6gXkpR0aKCpdQrIKqoqx5LdwXl5hbHRV8Qno10aqqr3qioqKncKdjrLVN04qcdGl21fkqBbIUlndv0JrMKMTdT5qkFvWyLpKl5kowUolTit12d0C4lRAKm5ZlUC2gtm6hWzfKV8wq3TvyuhC6i/yv8XTK1QpkBe85SACmT4bW6WhXt6d0p3ySnpbTVtBTJWYUDNbKmFCSpfVVN1Ct6pdL81MhbLVNizCgHr2iqqlVW0FmpMcpgqRWysgqqhVVSKlAaNZqqqFQLILddW7epRWQU1IBfsqwvqpLctY9FqgDiq9PEa9tTx+i2oLaU4LJVKrowkqwW9bUFtraitpZqc1Nean+S3Kq1VrEBVaVJTJVFMqc1CS2lkqBVVRoxBW9bIVFJqlBTVQomKpduX7XTN1IKb+i2Y8VKA+wVFT7BblNwVb6rJSAVFDCtYKGqFkVUXSIVApQKmGhb1sL3VUlTgFtC7aVI6M1W+YCmByUnKRF+arBZlZhTUjBb1RTKotUFa74LZJPmpABT8el2VPCpdnNS7CIumqKQWapdRRxQukVNTAW5VC2uioqhTJKjBRDlvUoLetlQgo1F0xFblJb1uurp71srdduW9blNSbFazg1Ti4rVAaq/wBhp6MtCSgFVUithbJUjBbRN2akFkFtKQUypmKlhVVCCgRdkpBQcFnG+l2YuoqwW9bltFVW0t6yukoUU3uPBarBzUz/AGImpdrs6FdCF1VOSqo3TuooxVVW7eqKir0X+VVUvzumbqLaipN6qEen2ooqKniNFmqaNVXRqt6nJSMVksr6qqlo1uk1QceikJqEftfTxCakVrXzVb6LZVL5aFFW6t1FM3SCm5ULlAQCqf7STVVJVuldTS2lBSN2SrdsrWdBZuUmtCn/AGwpdS+SrdRaz1QuWq0BTd/a+l8lXR2VN0FvWq0Bazv7ZU0qKZgqxWq3+1ke1kFuWs5arIrcq/26k2alAKZ7Gv8A/DCHazUv/wAtT9u4/YU/3AP9wD/cGX9waKX9wB/cAf3W/8QAKhAAAgEDBAEEAgMBAQEAAAAAAAERECExQVFhcYEgkaGxMMHR4fDxQFD/2gAIAQEAAT8hWqGrIY3XZhEf4Wk8oZNtGNWhdYEvWexbvYJ+pJJJCIIIII/M0ouifSnQtxM4M4II5LehzJeiCP8AyRSPwySSS6wcRPchucZBYS/8Mk0SSOGWQ6B8xw+Q3bLwN2X/AAaUlbkKe9SSaSSiVUkkkmisISHMl2SFYJ0wILVj1wXIIII9EGEcSykzVCMAhJPrakYPax7BfgJes9i3ITNSfTH/AIIIIfpmCeUZanYn/wA8EEEEEEemUSTRLrLYkS3Em5xELb/xSSSSNVqhmewxtoJ9Uhuy35tPwpJJJJpekehUNYEVypWaUS6T+CCKpujJdBNLQOZXQ6Vr7uWAekNDuTIj0QJvBtG5Oz+hNWjsWI0/wt2g+Y2Ia3Qk6yLeEzUzj0QQR+aC7g5hIJRtRpPI0JrBALdYTn/wQQQQQQRSUSSSTWCWxI7EDg/FNJJrJJJJNJGnQPnY9gfEPfGz1f8A5NPyIIpBHrCLPwQRRBBFYENoIk7JF6FcW1Y4iSHFFAIwIMaWxGmW3qWM4jlGM5TRgFJ/BB6UTIa4INZOSEzgs8EEEUSI/JAgqLEUaIbCUL8MEEEURWSVUl+iCHRAgRWSfXJPpkkkkkaLLQ1h6SbJ6B8aG/Lf+vT8xU8lvwkNk6UhCp5rDetSCCKGSLo7mZeV1vZ+SE96N8CSx6T7iVpuufwGgXwhvHgY3R8o3R0zIi7JaEx0IlmQO5MiPRAsBkJ7MX9A2B2JHi5PraTI0QRaibVIn4LPDrCokQQQR6UqCLpE9UEEeoEUlb1Jfpgggj8UWg5SCwmNZENGiVuStyBAgTSRp0D5RroHsJDYGzLZH5o/8Wn4yZPrk1exNZEtJouPs7EB4Ipcv6wfx2UxBKS3V9yK65S/wQ7PeP2M2NFNaJi1i+Qp5Q/1BP8Ah39yYBNlH6GEubdpHSaoXTNgdoTWZPplz+mQ/j7BbAzUvgaeViWtSVEHqQmQpl6IFbDFuHYm19gn7oS4NP8ADClsJGom1UidwJthkFyKkEVczlJF88ZG3tW1yeyNU8B3JbkEEejQYIbkTqSJeiCCPxSNVloj1O44KlNqyRLPNZh2tQRzJyEeSeiOWCfLf/I0/HQk3hMX9wT6p8kOfaINPNAn+yljV+lJEuZjSNXMCbkSalhTOqtgd++bEU2gIdpNcEy/En90kG+r/OIQ8VRh/acssnKv6QSaQ8a+zEFs3gck3Pd0u3hG3AsPyKDICxENUSdGSoSl7ejDe4J59gS6uuhbZ2QeGmIfJoHwPQbQ0YaY0aiIJLU6ESUyB3JkNeiBYTCXlJiZlNCxk/DCmYtYxPqkxMzKE08NVhUQJtCdCRoif/Q32GiSSG5EfAkNnrWCCPxtFloadR7DOA6Rv1LvUiiF+F0X/wA3T8OBIW1kS1lPc5e1EGj/AAQ08zk2fADyh5qLmhi8noJo6ULcYZN5aEEH1k+0DesstA+pY8Dn+cwj5BNfWmWfuv5RI01Hp+sPnG2MTInoTG9IJM0001lMkkkjhBOySsES74PoaqdxiW/qp8Dek/kSlalDMPwpWo6GJNUSamcDQ9ghoxtwNGjLokdSJZ7ETuS29ECbwbQlayLeE/WOxOcX/BE7EzcNEWYYnZTQmYdXFII9EE68CPwNGWhoD22PYHwDfqyWyCCP/A80X/zdPwZ7pVCn0CBhDTZzIS0esX5IXL38A2e1RL7JpuR4vpFiZciGCIJJ7QW5uREyXSUp5LoPpYcz9cJuNuMRM8m+qiXSm1yGeC6YfzQpneemQZSeRnnqWeBj3PYjClOGW8gMxCO0mbkbw0LD2/NJaktkQOQsOHoPage10JIlrUkdCLJDuTGnt6V/MC1kYn5lGET8DV6D5j7BveR5qb3ajsRIbfgaMtDRoHyse0PjGzUNmWyCCP8AxST6HRf/AFKyKGaX8dkMXJod3X3L2p72Jqw6zK/kWSXU/RsWwyX0ReAMPufAH9QYSx5mOA0pjgVoPYxsyJvwh3fsxCNhBKYQJ+eujOCPA5zmGZsXItndmyUS2piBeHbCIGDGFKe3cotKPZCyTU+HASgoaBnOWkowW4WWE6FJZLKwQQR65JJ9EqYE0aT0InYmRBAdCB0ETuS9EGEYScwxazIwyEEEUgggbtBpoyRY1wuItwkastIatA+Vj2/Meikht1DZlv3/APHJJNL0ggj1PNF/87Gio6KhyImTIYNaFNKBPkiB2gPacbwOebnzVYZTtFu4ErnaX8xRs74wvyVmSkSSpyOwdMjZAXQsy8khi/0GrSG9xwQtS0W7mLaYiRyWoGbdsaBKLfNJLE2lfU0OSPlM7hmmW3S9im8L2ltx2OVlGJBBFYI/8Mkk1hbDWluS0Spi9SE9CBMiPQm8jQk6p9i/omxOxNPDTpPomhpFhkcSaRPBH55JJpcuQQRW9bfgeaL/AOdjRUdGjvQko+Txyom6F8FEWpcG9gnXwNnKdhoR0okSt8jRKc3QSIlw2KUV06oWRobE3I9mb2jnJOIuyekgxLEqECZNpQhnt2aEVGkThpHvP6PmRJU1KbQiTNFJxCdxE7vuBRdANLGJobUh3PuDFnNJhI3FyLpl0qIyyEWkkkn/AN8Ia0yRIkIpvszsQ33ItB+hfyAtZBDyIg8P0hd+RJNLkEEf+N1eaL/52NF6HzjASI7uS9hvIl49uR6TXRBjbMaBuUvJYPYIknrWDMa71PnDYPA6TDJETEpuSZbE6WO20WRlKopCE66fgi9TB8yXTzE6CqMW9w+AU0u/Fh25XIdDtMTyOaKiXapDvRR0Mf8AwR/4oIIp9UUlRl3ISeRbxP8A2RtDTRjYae1F+A18S4vpSyuhK9TP8UEEf+jQdXmiov8A5mIxCpRi7IIGPsZGFjnbQZwW7cCvkogjq7cKSRr5CKrSSpSc0i0RtJliOBHyn2DKPNHmiwOixqZORpPlwQr2XkT0Wa4L0Tm9h1CGn0I9oT3BkhUor0JukxCLRXOWvRVozTCHLhf/ABzIyNb0NJ5Q1G+jGrQg1E4l1k5EWQ4Lex8Q0H9xY8CpqQR/8F1eaL/5uxgOhV4CAfzDaRuxNmQauJlyGxvsawi4GM5uUW39S5QrasjJ01FSDK1DHJtQt4JvjgvWzCtydGT8iU/rnzg1DxioV4uyLzJBqYNyPl1zYxogj/4b1H63gsQGlTF0YDPT7RY8Cqf/AMJ1eaL/AObsYVIyfdMBJDalqydO1Rna5aJiYsNOVoULXFOokNAnKQYwDpwYDCMUqww8sdFRGVpibwZRh6+CysJK2i3LoXwmtG5fAk9TMqD95NIs2Gu9RTkPQTraEPhphHzxCX0EgraJ6GVOpBH/AL9xmvqeH6HkXxUPpp9xp4FU8/8AwnXKi/8Am7GHkZqEZvuiwGx5mpJdN/0FSrfM8DxyQ3qMR8hUrzzjyP0LXL1IOK0GfA0aa5bWXkb4kXwCNuybMpKyMDqd9QiTbgW8Si/3DBEuoCE4y8CwSwLTNDzDHS1t7nw6BuX6If4X/wC1601JJJJJ9OQviMhmh9xt0YVa/wDwnXKi/wDm7GFNYjV2I1XoEpSmEImktDN8GFEYLoYmP5KHgJlmXpSq8BE5yes2HG09EJxMPZgVyzJGEpPTEvdjWLrQ6qgWCmZIolbkrclHQmqLEeuCPQII/wDTq/yM+GZei8LB+5qujCrX/wCDoOuVFVf/ACnpQzWI1diNUNk1GsN9CdhNK7RvklG4WHvoYMQ6JDwKkBwlScqcmGGuTM4kgtIZDohbxZDSKMxUzgeYxPIis+Rj2lI975Y2eEG3b2JtWS9/Rbcbx3gzIXyS+SBKD/bc+ErT4Hx8f+yIGv4P2fNv9JSSfw3III/8+r8mR8EeVBYMxg6FVr/5ZomejOI5oP8AFDsy9Wg65UX/AM15VWsRq7YjYwETVOykhf1JHNJKu+xK0ds/sYJ/hRDq9xz2SHvBrleUHebrwZDrFbhN4RHMl4Mg45eW6RR5DrkZ75Ul9jvkG/7k+L8n+DEtkbfNODW9RPls+fkX0H0rfeF8d1+jSFt+gOffhltkJ1J/IkNEUMR/5dX5XxUPFLcyGDo1dTyvyTTmHSvJZqiEIcvAm/mE+x5FDX2jT0aXSInvOw4CcRqZvW65UVV/8p6VaxZNXbFg2LC2RksIhqTyPYEOvgh7l5G+hdDwNusbPLbpiMmOiMwuSDz9uB4YXAh4DSsPt9lBrA4z5bPmTGF4/wAVyPgTn2mZBDb9EezJ74fuSSSSXLkMgggSlwLG27WE/wBCkkkn0SdSBClzENUgj/wvL8rDohmXgf2o4OjV91PK9KTdkmzn+TcR2I8+JScwNhvk4I7Fpe0T5EHlzsZAITCSokjseR7Me8/agL/qxy04TW6/BnXKiFRf/KelLZrph5FSRLf8E1RhEsQii17Y/Rey3dB4GwkSXIexDE71EtEHbHinK6i8nUX4A+LsQ2QnMv8ABerRf0oms/8AheX5WPQ0Zl4PkUsHRq6aB6emxRCEN6kWgtpC4ERmw0/zjV/FD05eBro/l0Bv2Xg5hLer9yCKQLWQYR+j8CdcxiF/8x6ejdEL0yqQR6MAqDQhpcIcY5PYaPEhv0f5b8snqfahD/J8IhXuxIfBv2F4oVYa7PBmQovN4vY1bDCLqFZ4GpwnNePoSIdl6mRLSPaN1oQQQR6E6R6HA/8AxwQZKLP430Gj6MHVd4Oh5U0D09Kx0pOt4JibMt7kVgj8CB3cEOqXyPW65UQv/maPUIy9GVIIIIIIMZMAkoNBq4pFtwLyDXI/uBIbcOPuZsgYthjT1aPARFwqFAtiyNkK7xrlcjgm8xoPZC6E7nOyWYt7YJ5JrO0m4iwlvXoiSI19IR6HFIqQi34oIGvTlos/gdS+g8PoxdUGUx9DypoHp+UJDfoSJdSFmkCIo5XjKL07j0rlRf8AzcOhh6mXowEEGlSYbuNkTWkXyNt4tw4y2ZmRwevozh9h4yQJM+RSSwpB3EGZZSxffdbtMmohByypkjDu+kZ2xYQdpewxCnQY0xS9xCFArhLWJRexM6ROjGYE9zNa5kbmMoslLY7BxuSvbEJ60QRR1gVIIIIoisEEUggj0QRRv05aLP4HVp0Hh9GMzmUx9DypoHlelYBDXoZBFIN1A4ieJbgXIhVZckO32l5SEc+rQelcqKq/JJGyZwMlx7kf9BqGciR/+Z0wGPqZUVZIXCZpXgi6ski1x4Yycie9OCy6cIaahzeLZIRTh4LbaIWrQir4ZHEQPkGceKkjQvov7Br7L1yxJ0N/gMErWL9jpaxqPbGB1vlOYQ9DK+QynhYvcdvtPcSlIdbR/ouUaSMNsRIl0YEZAXaY1rCwkhMT3EjU3SBLakEEEfgtWKyqwQYoksNEejJRZ/A6tEPD6qvLTyU0DyvSgfLFisHKkFzhU2Ub5Jo2K5hT5I/0Pmet1y9CF67LMnopC5HhI/6wip9gR1bwbjbyf9BsFH/6ozAY1OuVE4F0aFguKxcjnQlrrEIYHuJFbWsYEsmnUYQvaPhfQVqIXlZgS7JpaShKknYa3YzVZtyMUTwauWZfksZLHJ+WDgyMGQZ6qB0k7xYxE9ssjiCpJROyDyw3g7l9jGpPXI2ki1Qi/AiyRZiGzBgLCQggekk1JJ70EvJCMk2tZGTS9JJq0QR6HWfS8qLP4H6D+KqMlPJTQPT1D5YmMOJbIIErlxHA+zIhYLpgZdfRDWdyDR7n6BI7vW65ehC9fwRGMo5HsPceyg2aF4GSbc+6SeW3X6//AEsBjU8UXonSm+hdDzsJrJKYYuHvVh+t5Coev3G9ym7E7ybwzkSNDSZIFwYKjGbzMUYBP5igrSRr0TIJVFk9RlNgkTMPdECugLh3iIHlfVYhjDRmc4JJbSciWUXQSUyFroRWjqNFpcPYZtKZhLQjFvwQR6ZKxlqNMaZFIHJckn1wWG1SB5U1/A/Q+EY6GSnkpoHp6cS+aRRBWQwhrcmJB4HwISoyeXR8EUjcXmnyz9J8sL1PSuXoX4Psnzh3Q6NVgaPp/wDTweiMP0C+xhsLXbEJxcmUqF0RAiOFGZG55clkfeUpciIah24OqSwGpcEt2iFQe4nczPkBuksp2JYHkW0eUieolmO/IIsmw85JjdyStN4yWZb5J5moasYcHmMUp4YppOYveSEaSzKZBqRQmpQsWwvwzSCVMhp0kOinI0NEMVUEVn15KLP4HRmo/jMZiMpjqaDb0r6C+4QQIU6iGs0YYMjsK8bkjlXsiOqRBaeaPzfXoFTP0L8LL7hqIQMNCM0fQafxv8uCPsqY80VMT41WgM9hJCbsMlJ0QV1J8k7D2zZlkjh7mRdc124cc+YYV2KCVjGQb3FREVFCTZBu0M/y1uEhmMN6EuuyFGSySgUvPYiyMLLoc1D0WsTPaBYpJMTF7fikkmTJkjqOVEiYqJk0klFvwRTJRfiPIx/GYzCZTHU0er6D5BFFsWMZGc30HeQUlZkkSYzRC0M2gQsB7thuyEjQ9wofN9egVMvQvwpb3EqRiQ1YaIFkhQfSZr/0PCPspro8sVWPkSGbqhg8BbNOZZIBYBSBpRBjqUm73JpzljzNRmWGrulsW4u6UY6FubRE5FtAVeEl0QyicIsrIsi1tjBAnBOmnsLmgNlLME2Yjssqx5OqZB5OReRHDj/wwlQkN659M+vJTX8DpquzU+DQwGWnlTQaL0rD6pEiTUihwOStAXNsWcMsnLRLBbRDGNNDUm3cTC1sMbuZT2LZWHc+KHnvp+V69FcvzIGXoRWnkaIihORIxzX/AKMEYeaazUeRVZuz4xrS0dDJMmBolD9h6dq40Q2kvDu6J801CGxO4+TF9jayLv8AIRIu9jI17mMaPcbtA1lownD8Fnogyf8AC66K6GnGGRxLdxw3c6CIr+TwaAyLtv4JsKdhJxJQhvECy9354EhUsQiFSPzHl+J5po7Hk+DQyRnpvNNUaVimj6pk0Q9KNBpD27Sa5IRJwMlcyIXILgWsXEZE6TlF0kSTyS2bplDWYPl0PL91wu7GK6K5UX40QmPcTGMe41qoZDmvVHpf5XgYU1mqHliqzdkM9PEQohChXzE3HlBaU7miHUAtJK0JwW7gns29xNPtcvD1EtbWpDTIoavTgelJoGP9yN1hPcbtBJt7E45Byh3fPZOXMixeRW3wKcKZpK7kKbn1DFjh2gbsJKpiw9KbKdKg5rXJeQmNi606o6dlMCHh5De5Iv8ADL7H8Rnpj8KouTRkiRSyKIIEWxmBoggj0vL8TzRfIanwaWSr7zRZErEEEEEWfR8miJNKjk5GgUtjG5GtzAhOMDTNJIJurrbIpvlqW9xYtuScJzLstyIMK4nNoxS5SM0Vy9KF6lvUbWJGoiYjYQSA1C1d/uDNemPU/wAxhTWaoeTQksDTRWfyLbnkkhyRQc9BZMiYHu4ZgNkA44siAh8icriqENbCPg/2odoYt5bGpf6L2EvI7/0hD/m3Qj9mP7EeYkHY/wChJuJaJMJoyJtAzdhZbtUJH9EYDhL9Wxesl8A2rWZxxbwMSLND3fwIpDMpL9CXMIo7wsCxqYNzftCQlP8ABBKOFZJF6YpPJbUdKSSaT6nl+J0wdmtXaK+80SuIQQRRHsHy/RFzra2aKwgHfcuEwMSHLu8+SJYQaOBj0GQ1TKYmsNzky3NjQmnF1IxOGPuR5Y9BUypqKq9bR/60HJhLOhjNpqC5EmpDy/3Bmqx+B/lwq1kDy6IK0kQxMmheG2BT/lm7LsJ/oaiP7j9IhwjC4VoPkMSuXhGQneRTSOgPA1MiGAsHsjCEroJq6YhPuYEbuCbeo39nZiVnDsTdCcHoJzMSWIiNTRKYEuhuKhqMVbUk766l5EpKUZL1zI8aQIM4pE03qluQrlDUXKVBFIagUDSloijQTJFWIpJIlQ3/AAoogikEEUZKLNSKujp8r0G0V7Ug/ZiBIiokdQnvUXNHgpBfYScZD0vYOYbsEKMjUayS3m8DUllG0DW083dDyKwZSahrBCPDmVnoWZElw3uMlES9xayStbiJGx4Qn6DUVF+AE+L6Ig5PiDQSMSMklBca3JS2hJ8v0JeqPwP8uFWoSuZezUcRQsQmpZYS8i9zt0Lm2W4NbJ4CddFlyxyYd25FECq5LcuoY3vAQ3UaCWpmMg0oSUelGgyNjIGcO4WYhHOG7m7Elren7M1Se5MfZdcy2HJMud5HJELmX8jxm+Nwi5RKyIkpetEAiLknqXKSV00YOUF9EXuNxf6wtkrJxgvFo1CVOq9KJE6sMhiY7EtqQpJ4Bx+FFIrBBCLVz9iFkj0tWGOnyDWosFXtafsxPmJCosL7JO7lkEUu1EjYkJCLEtzCSSCcrwHwRITRM0pwJlcEWbu2y7W9cmBEETzMIaL73k3ughucbCO9jWdavI8IVMqa1QvRrT5H0LOpfQ3cNgSKR0TDyRykNaEx3YwLZ3GdUEEUikUf5XirULJk7q+NMLMQ7NEQkIHzCSNW3EUrnzI2uTU0NRDAJBqjITuGvFd4J1MoQ3tGSuO0jpqe37GuEw4Ri6JLFBbJKEXVyYC6GIyalqwhs7ATJQ7upcmca4Wg/dYSujEMl8ljeMp0N0xTK9zCH11H2P5hjbJBA0RRMhiROhpKRs//AAWHBJPpZ84QsoggaIpgxjp8j0KxVxEC/bFC9AvspYvkQNDq85miZE5J+RAj0Rc9jyKSewgUyyMWubidBMwmx4FA7EIWGkNq3OsGMcpnDFhwhr2IpPcaTbIL9GtRcstONiVN0SxiuVNaIQvSz530Pgr6NRg8j7jy1xRVy7iBoVmUixDMQQRWPQx/leKtQsmur2pIyyORZDCNSnMlp0HoK3Lh3nI8yPBtqmhrTgoOpsQm5d/0JLJ/xFmCxqO1+sOepX2sSzNBTZvKt9hIQJCR7jSlJq6Eu49J2wSVu2xENpLQiSvyIGYzMLsKVyyhbj4UamR4YRsIy2yuLuIuzNeM3W46PZRZt1ZJ9MUgggj/AMk1kziFlUS2TuTTBmg6fIHVS2d+mCfbFsriDKz4m8hWGElxh4IodvInUgQNFwPJ3gihC3G1ItG46NbCUReWw5UdhGTdx2abw/4GUn3Wu5NRTTzlQTD2UznYTt+xE36MiZNKIGVydyuJ6DHIsoYlWgmpcqeqOmtEL1/K+hN1r6JXUluWhDkVbFhlZL5LPdyKLppOgkmG8mBOlx46f0JUIIIH6GP8rxVqFmgiB5o2KPcODHgsJ0SJfdyULhKrw1UZMqLUxqh4HQxbjzc/xELjwzXNh7x28qEMbm4vXwOk6Pgezo2GpfNlO49GHyzRWjnscJB4JJbmbzGR2yXQOAZ52GhFx0FDaxtYNEZUrCEA3VhXXIXNVmu5swSWl2NX7Esk8SvDue9yXJvL+CQ9ohmfHDE66OL5FgcUir/8+YWRZF6XhmlfnDPrUsHo5Ak+4sGJapbsL0uiLidIcOZHH6yecbiFS0w7EtUXawyW9RzyNp7iug5bJeiJOsL+QlvG7baV2QjPQC1MEWiaFwLCEcrAkiJOMQNFiIe6HtmsLJD2Y2yMVHRVVVR0+V9D4a+iYxKL2LSboGcOV/QzRIxfYX0KCqGGGhoij/M8GFNdD17q1FQIIQsERoIz2f2RXoQfgNyxiWdLhMIwoqcJd/tgXoln0GAwPhMtt5H1CKVeEbAnksCIVyGgyI4o1xgnInvatyWmqNBJW1nquHdRq7ZHdadkHKn/ABkmbjgxCaUtMkhU4X+Sa1f+MQG8ZZCUw4Fp36EWlFjOa0GOWbgUQQtyEPNIIEJEJjQf/gKuYyEriVSHRYZpX51M/dLHXk+yBbdwazt/oYpxadriJYpo0w6atST8LBTtf6RbyzP2LAw70ikkveiRO/qghysPqlCbuRKNh5ZJUeyGo8DVwNrmMegqPNF+A6fLf0fHX1RK6LRApK9oINCgYcVMkC+yvoT0IOkYaGhof5nirWLPrjUsuWSS8onbwOjGI1JDyfzS8MbsPUdTGf7OKd9BgMBvZMuxm6MkQOlzSkykb3J1khyakGkbSxJwohlvmkjSeRkopEOhDqmIxLLhj92vLoR8KLtyibCwItyKTN6rFltMGEyiMTq0NkSPtEs2Nz3sUkkkkkn1RRIkSJbDiMi2axRenSVhDRIZwXJY05GlcfZqfb6a7GmKBrPJ3AE4uf2gwa7QNnUmVqSTf6SP9gYGqI305HH7wyz/AKo5h/izhXuJ+j5J6++yH9LEmwLfj/nH+FH+LFshBrH+bMJIQ5puw0Y4FW/LzBIjocm9EOCu8CTGaKIeR/jJ7r+hfZX1TkexlriDwQ5vogh7MbLKp/o4Pe6p0nWDQw1+Z5GFNQs1FVHwaiyO8nbQeUciHdkTFQVJca7+huMyHSf/AA2JoWXoeTIfYFv2PrMibjyToK7X7LcYEjZZ7E0G4hESZwvJjCusQJFzJYiSUNbXglaGw9Y1IW1u3gglMpzdibh6diEUmEWZUiXt0yNxcksr7EtSix8t7aEfkkQQmojZMlImolRAg6diNVSBoavTJ16MRqfb6Yb7CR8BiiBnJKPkYJplcXJtZBproWCwnQtX9DjyGTlnKNd0PYe49gcI4xJr8Hf7HGxJszsJNYySTNsd5qWBtx0Q3+Ai7JNm0glqtAlM3zoY6JHg0P4NFcvyPnvo+H9KSWCZKU9iQnJby6L730F9/wBBuuEGGhCCCPxvBh6GtNcj/JikwCepa8ja+bJLQKNp2SNyhwDGotWahyD0SQxhqHh0qMyGLE/2cCLLga8u9GZD5v7IY7jR4EROMitoah0GEr5lE9yenkYhtbARAUtWo5XY02Wi39iNOQOgpCEL1ZJeE47JNWF/rjcQI2svoERXUbDJS/0Okwnv2KwpLyZjXgga9KIbER7DrRHrf1JJrImNnyqCdlZygdMnXoxGpg79Nhj5JGt5Fp2xAlJ1EzGxrVXJqn/iYgm8EqfnG1jtoX+5EfUtWhsFhjQtu0PIz/ukf804PYdHsN+X8Is3Y2J9RPn3Cf7hP9oU7v3JLXJPIi3JJcEjGQjVeq6UQY14zPZvLuIRm9aC1Xr0aKIyqqlRej576Ph/SshbxL0LKd/pPcaasrUELwgkUYH62P0PBhRDwbvgxguP2P8AREjyJd206FuZ59xHP3GFCK8zgSbE4EZeRcJfyMJVELuxEzB0hjFmiwI2c3KGJym/Is17cJe4cDVvck9grwXZZZyJLgjUluhj0DW4m5BRbzJa4yIkwnvAmFlCFUbkFjSScxAtZueiSWROyywRw9o2Gt7nfBMmm0IcB84ImspDOeRzmLWFtRr0ntgtSeTUGNrUirsNE0xp8EyWv9FJrK2HBIoEiRJiYYlSkdbFI+IjAzpraxNackkkjgQ6JZE7kxBUXVhiTJ16MBqYe/RZkMSPYQaCoODhhCTGSTHuHb6OgxTMSSEN2f3EVqJTJazsW0jfuiDG0MkVyDYT9jLgTVoRq4fj/ooqrayXYg7QUbk2lCmqgJcogS0TDciILxrCmCUkhJHRP2OvwS5JfI7xRDzRC/CX3n0fH+lIIIW5rYVf8/AkkSEQJStLUPI/yvUwojQ0ZFUm5EkQvkTdfeQf3k/+pDSTtNqNGJZPZ7EjeRO43ZV1EwtkNwyQXnHZw/kdoD3F7j3vkj1oxkhsJt6MWE/yHA7NazJRPYadySzAjClrafwCZMjf+AT1wKy0pGp8sipna8W3ZpI+f5DgrszdjBY7FHpZDnczai61HpzdovOHaPcaLVyr4ZIrO5hd1JPVpJJw8qkEVikEP0QaVyJcNkTNqYc6T6V6MsqiHScWkggydemPJg79EGQqWCSV+R8rvjC/JAXXQ7h1pEWPbQjcCurSJXBRqxSf9jtxKGsjvm1CS7chC0030f0AazSWmodhL4Qm38xwcQEkTJR3LwRvF0U5GqW4lPY7noPeMp4FCc14YTtRVY1XTUVEKi9C3OQWQbJfA4y5i/77F/2T/mM3SbiGI3JmBT4H90YVbegMefwGP07mFEaGKNS5RBbDIsW+lELCSSSoWuVKSbIGEKbjNFRiySBsQ3FJwOyXZHO/sVW/37Jax4iXgnbV/rY63QrEJHSBdw9I/RJ9cjyFDwP+7GhlZTSYoSVgTKCW0mPl/wCRCAtl/ILSl7axdWJWVhKfwcWHYJpjvcQDiPVOS2yNiwa5uKKS7hRa1a+RCJscbNXLcWBPgLrSw7maeBp6JnRf+GCPQoZFc40SY6IIIGL0ZZVWRQmGYqZPTmPneiHIQ560g7oSxuajEvJlvURgR3bOBtL8osS9TAgqFsOBMDkTSxUYGhvGRzIyWb4HIWPtGbPtGTFE7UcjZezJBvkTcRtDTT5RljQywgDNrWUXi5OoXHfFEifotdXVfhSshyw3GhFr/nocll7n8HT3P+B/7/oT29g/1Iu/7N1vH9zXeJf5EVObThuEjgopTGx+gJUx/keakRYPCmtHQdJq2kRFqT/VMmCk4JUMV0WmKuymIeREhwToayPIrMexIRbsjuqU9C9EwkOhWv4G03uWAWAuINFbA6T2gLO7mhTXVLJYjccM7DAFRKQSJSsvcuXZsOHRwP7oZ2JyhZd7l6Z9EkkkkiVMklm0pJ3hMHTwJCXQ6zKhyv8AIz6HX71FlVYPKUzdehWGslhXuOU1kzDYCTiJO6ExDo8nZgcCTSmr4cjY0eREMZJp7caEZDYXYmbiE5m842EkbK4GiQ3wP/CP9Qf4gSL+h2I7slINN5Y8iFuIckNn7isSjHJPAkMO5/Yi5L3JDo9gjZ7iC8UVOdHlgko8Jzdn4/4Fvx6/wTpoRooPKJG5/CVF6In01XEcBsBOwq6lJGxluR3oahof4H6Xkwoh2S6LGKqQs3H32GDlt4KRcycl3QS8tyzItoReui0RFnYS59SHqPJqQi7FZq6IiRbrgkMvI+CLLXuFJmQspG4d8fURLz1EsSwFUkjd0X1gewGorzgxgTZ1CY3HtDTUbkJ4PlJBlQs7IduQiXwM07CWjuW45LE2ikn1mR2tOzN5jXJAJtTDj/xcnrvtDFlUQ0pha4UIjdLC1iKZPTjsZgSQmyzgHGjjRxo6TpOY4lFPoklJSE/9Dt8l/wDov/0XEcDoOkilJa/c/wC+f98WrBRL/unIEzqEDu7diOXBJWHMt2LDgQnHo1qhfgXoSLo3wWGpWe90yan3MWw+/wCxii9r/JhB3/ML727ZXmKZR6YS3fsiWrrw+4bf7RiPlP8ArhnT7Mex9mP/AIj/AFVMqN2utD8jS8SnJfRu93uJw9Lo8mBoIdw0sLI6uQXYY6WhclYGnoLLFKA3uExaTawIna5RFp3LX4Ht4Q8MeTUQ5MN6Ca+S9pIIkT1s0iVjnFkO0J5IJcwWBRIldd7VIwbuaV8MUlLHGt/YjBrK0IavqS7rQWErSyzaUvQkUNFI5LqK+ZZREgh+pqlF39gjx/m4HvP+cGhd5f8AAzh9H9BoXwgpuOv5SZVYlB+zJ3Ck8fnhF0IbbFlr02EhxPcK2y+vqgX5zAwUbhDvlxsciEY1am5npTF9VZkMSjXwZlgJKM8TxPE8BYgijwPAjojojogj0+x5R5PJ5PJ5PJ5PJ5FoUHUcj3OT7jQUQm+SfSKuvoKvU+iPQhDlIU9mf3MTM+8SepNZoikapBFIpAozQnga3wfeZeljGYeaJKrk1sdB5ohBojosx0X9g2cyOtbTjQu7pGd1C+xgkobCXMfCJyPJrRi0h3uEMWrl2jHkuy7dyRYcNJcIjXoXDLK/yHvHwB6WTtGgsT1Zewy607GTqmXIEgyhoiosIlXUk2GuK1MSi04elH/SR/kX8GjLZFD+BqF5bgm/g/4H8Bn+n+BvI8oDyT/jc+ZL+Y+aRyZTUWaLtfggj0OuqlLuzecCzAhTuRgSlHlWBoSEj74oWV3S4DnX9JWTGRwlb1KdHRF3TGu6o6NEjyJaTMxQwkn+pJ/5kqkEVgisEEEdEEdEdEdEdEdEEU9iBWc29hKY/QWf0Ef8kO7+kZaOmHp1rhRosnBFmFfZM6yJdhNPBFYqiQ4uMkQpIIY0/wAbZRAgz9LGM+6nxXMMqnmqWfRczLa+CPlGsydDjNvZqRT/ACIqzBruroW/ijceTWjmI3QNQlcuJH1F7fsY+0bATKQPYMBK1RrfI7I7ktial2Q2Z5JiYxZJajXWwmVXhqNBSmxQvcdyKhwsbjUquCV94jxDLCS2ifyH+oovRJJJCekpNRhkSqdzPQqJXv8AKrTqiRIzEmzjcnxgZIbukUauIYJSZOw1jAkQtRtkYZBqMpa3FnZCDdvpA2cWX/kV7RA4J3NKqz9iu4QkCJti5kYose40oTI3oh6tGcVbkMhkQR6YEiCGXpBDIZDL1wEGfaNv+DdSZKYUw9OtFQE4RqGJJ4E7ZNUSHANu0II9CImxMGjo9C6PA6Fhr8DQtMfrmPWovsGvuxmXoa3ga4aO8mzYl3EucJfNOQP8h7NuZF+ixs3Hk1oqU6DCOaHx4JypsTv5HlPBI7o+eJZcGuvYhTUO6g0jw7/UngGI3OE3kgnoIKaTZsyyBxBN5VnRsNCUuknyB77qZ9LYQOTmktinhlAxu4om+B2dqItOsUV8EKM3LEkj0NFel3LheRUJGdLeOpXzinlCSwZuyhdLWFlvQTR9UnDZmgdUm0Sy2Tm2Tf0Ici7Dsg7V02Fky1ggj0wQR+R1WaholzJJkphTASphRMD8zQ8GXR86NbjYRYkO59w8rTqENE4fcy94x7Y5Q7hkCQyI0sDHhRquUJDR6VSJN9Mqi3DgbkYx+tZFeZ9g5VIo6PLMKWoNBIkatie6Jf8AWjRmhJcv2IHJ5wW6blk9kw/KfRNyJ43H2mDMvBno8+hxz8gZ9n6RSUbGQWV8Fq+j5QvofCEaTK/1Jav8STCOzEndz4PeD1XJFI7TUsSWwzzj9jQ1Te8E5JTA31hzjrYemLnyhXISpBC1EEAjE/oJHxRj59rSE5ZGc4oPFP8AYkkTS4it9MEJ0RMVnJabpfujHQvZZJfZdV4Y09j1QS7XcGSoah3lVSuXwf4diC1GkiJ6jSxMjQZs9Mk6VNAWTcTCGpLmpgZhaEYFlF2E+zMsKSRWwYh5G2sZGmklRVzehOay/DP5XR0EiMlHTAQiVwy4kQ8OMiwLthLj2d3fgjiQwXsnKbn+S7eIsE1ZwLTKJTzTHVu5h+ifCekv0NKh9at7keHmB8anKAkV7ST6EohXlqL7+mBIlN1emowgl1o3EtjbaiCOPVgGgYxLkDGOjyYUs7D3TYUXgXNQcz3Ob7nM9yO4jszgIsLUctlpUSjK7Q+80MvFU6Oj3LjuDQ2xTmNHR9KnP4D4gsGjsedMWfZ7kGhuiTLjBiRgakg6F2LmqS2Eaj/E2I25x3pFjbH7HyMc6WAeRFxC2XBndaNJjwM3hOImXEmp0RA8tOZYrZGnGCyyE5NckDJDVu4GnMjUyk1aEJdMSlwaiwsdlNqwyHMQI6FC9yMhAwzizPApXQ5YVeArw1Em8JaDiVsSMV3WTJJcpcbiSCwy4FdoNNz7n2DmsW2DD2CFDg2cPLFcklFh8k5nRNxLuJlyM8JQiCg8saGCF2Kosu6LjkulAjVyIezE2zOjI4ZA6eGXJEsklkkk+mSSeievYkZWw+GbRpUg2+Ltgz0wpgIR8cackaFlxgyLOW5PjZ8jRdJoawO1skd4jXggLoXA+bNk8ElFzlKInRSTvBxPikxYlP8AGJGEmXEKHWNkTG7UM4FZIwnydh31ov6D9T5Q9jD2KMaHRjzUrLM/CVMh4oi0ZiaKMoU3AsDBeBu6JS7PB9xNj3yMlVXIeAxyu17D+4twmGBhP6HxaGmD4InpSyDX7HBhHBcz2j3IsmTNy0bmBNkdMCfE1MTITHIhDIJJPZlyJzcZO2/YlKfGgqubwhdcXqiR32E1jyMESUxdo2JNpF2RhKhgcIG7AazDsxMpNVvK7CNPLmb8kUCGR3NSdxsZiMwZPJEUwbQGkwZJvDE6SXDkLpBZTLYUjUmLZrENmphYW4c8u3/BwKz0Gylbd0OdCYkLKazPt7jVySbcXeBUxmSER3wW4TsWzhW0LkiwiDS+ROFNKRWXnciU04ajCNIeCizTkSIYqEKzJLSB/dhHeMEsOW5+zK2TUTNRYLJurakOzrI0mTbpjUiQmtjxGaG0CgvkRF0JBuW3uOmqD6DMmskOgXCPVNhbgT3DMwbQdhnLRJn8NfVUy0fuf4f8C1fGn8C/qY4/x/g2F7kQi31Hlp8gg08v4yVz/j6P8L+jIjPnYcKKN0wFT2gTb0avdEmyO1BN7PYft3Lyi5IIKC2FLShWU+JJQng4keBM2khWvvkZEzJ4F96NthoS1CyLem24TSRKxULxDbApVOrZDRMaFp4UYmKlJJJJIyfUpp4m45g7phiMTndOnEQPaHQJ05aT4ER71Fv0Yu1JwmPAxLFshpfyMyNKrHBIE17FyjkwaOyX0T7wq8OhdN7kpaZsX7mTx9VVchLg1W/OPBcnYkkLbjnXGMIvEzYggujkQuXgf2BXVmjcWHYvuIdr5pNzGg2VyoMp4xqge8RYoimVvV5RfChkq/1H/RZ4N7kMJA8q30RqxzeyIL55uSN5GTRDyJkZZI/z1hu8skmSOJaYZbtER03q8aIikt5bFmBTWlq4TP8Aalg9TEaEUsYYG6Ky7zb+Q+TkZVcigmG41JQerftRoRsmaEl7HBYO+StGXlcrFnH/AAcrItE3Ml0KSFoViWXzRai7d0RLWFC0SshCZJuSG0JinLdQpRG2cjhNzBp8lkVpkiR3b04EzIM2LmhpXyxSQ1ldXWNYWQfQ0xaBiavPimQ4zHWTwq0heh/+KKSSQm2EyEhxDPR1Kj2CWrcInYpLOo3KxiNC/kkVJoTJvcjw14eqBBgZyOU5I2vuCwWQ8UKkmhoJIbd2nIlB8wxd0djLSy01QvRPpYVopfAa/mL+hujCRyZzCFm9e9/YxKWkSlPk3MdSxTEhcewyWEvYUjLElZvxn/SHmcP3HoEJ22M1UqJd2JTLT4FYe3VMuj+0Bu1Zr2I2MJYih9jU9xDTYW7gdpRgVn9iu4+RN7DaW1PuSMv83+xtEbPD+RJQxhySvkXa1HCW0YSWndXoeT5o87DpjEWs18kLWtaX3X9iE5xSlfsXnB4tG5oWxMmmqtccSMtaSiX57CD0QRksVD5xmAfKH+lbCtUv2DnisEm3IfB3aXFhbjG3k5JZgvIrBJvoi/BMIhMGyui4r67D3cncS0iG8DElfQnR3cjvWXFcjJOJNMEFkCtg8iEU1xs7NCpt23WZgyM3HozaMEzCxlKazUhEJUFufPgst6P8QXf0J8+xPn2JDbcfM70Og6Dsjsie/uJce51e5xr3OP5pmntUSB5EizdwEtR9ZtPhGajqVHsiSRZfUbMyaWXtJgsklCwhcOdRq99mECG7DvrivkboQ2SPkmNoJTY9jR2O4TV1+xl7shL6+xgnhJWV6tD3YmlrcfqI0snK6zjcWtuB0E9TRnOm0U7DibUl7RidNxJphYt5ieg/u/guqRX1djE9aKSQR9xliW4whEGEvYyYhY8X0ZHtkbn9sY1jJ9jL+0VyAyowkIw3Ru7GhTuX5DPcep7AtpRWZ3RoTIQlSTgYD5CcSEHaRJZpOiCe5QNwivjM5+iGScsQ0TeIFor5Nx96D/zqEj/mH/YDRlPkPeexBHRDgULYtwKxFhl5or/rKX7rbUxA0Y8MoeRCfDIWxPwR+UkMVWm3v7UTNnohwcMnwNrN3HRBgwK2U49xBccCScwWiQU6iymvfoSRLW7QhjA25u5EzlpOFngiiuaRbOxPIK1sS4JFTRHwtw5yIxqGWf8AKLXnrHNnH1JZBdEzayEWWGQl5y1/wULLRq0OIZqe9xqgYTLQ0SkSJUXMQhY8SsFJ3GENZND3EFKtBrGYvJmipArjXGqUrkKCL0s2P/rgxLn0bsxprVk7hO5k7mco51J/ojnXsP8AVTkPAS9TtD/kCZZNDp/5HL+EuZvRAsaZGTujqVESN0IHdPUfuz9pg8i6m40kk7p+Bkjdn0+xhhMklfCWuwxKDavdF9n2Yz9pIf8AAXQdLhGt0xdffgfg+LR9l0N82haf2xlf+6FH/wAdYMMRp6XHbcTMhuInkXkuzra0Pg2aaELm5JWXWQfIa2FSR1NJOJcJo04PbFxoSl9hoQFrBtBxinwhwhFkvMUTNFgyfYzW2TLSQGehYEEaVlEp+wvpOYT/ACLwvksbb5Bxnts9mx2NTiJvEg8MQeTLwOiEbyKuZbB13Exis9ijoUGhehjuIdhtHL2Bt/jP6aTHYIH6FJdlSfvJgppEss44MkCkwycn8kSCJtbjb2vImuTgafaUHBsiIZQRiDCkuVhN0SVYS0RpNyzLjpO09Xp0doRPJJlbB3Fw+3LFLzxoMVhttDbSBA0SIeC+h0ZFtYqOEdWwGZwsqm+9skaRdGVzehTC/eX2vQn93Bc3beOZyDeLeeYyW1i0sekDeE3hJM2Qo0k3sti0b3l22G2rq+mHgsq9l8CwdnTVmiFcY7Sgesd4b8D8oPhD+hjwFM4Lo1thPUcC8kQ4IpqWj3HkS0Uib5FOxrkjwS8Fyb1H3j7jQjujH+eDIsbKwLURk79Iqycmq3J3PhoLg0ZFCi/I9MpRNH9H2MTEJMxb2c2Go7jAiRBbkQ4STyExLASd9nYa1+yExE78IspcA8F+XwRMvNg0YSj/ABhqXjSjAlaeRiUiYtgXWHwRakkjZEkkiCYIfzUajIybGTGYsNnTJ7wtxPbCWYRL9cwhl2liBs8cyTxxMZIi/Jf0TFoFp33RbSXZJbRbDcJx4QlqIU/w8C0xCSUS5Y7mP2yKLpndixnDO8jv0v36jv5mJw7IT1yRZIG9G04ib9GuH+NiUk/f9DaIFIhINmjekNrJtsiXgaAwUirV13tCzUiQxyeyHel8Tbas0SWp8+HpM6CVQ1vWtkQ5VNpJrzSfWI2i69HKE529c6L3LpJQth1PubKTa1HKDtlyJWd73O+/ZJ3SLrTknDNkpO83a+h6dG9V0qjtBJiV2X6ZRZQQISNnuJSz1cc1NBzZFsXGk4zakUuQm7LalrckspDzcLaHDdqFKEhnZbASt0ZIlDTShenEp13tJdcizGLN8F28cBNhEDOIWau4RLf9CV/QZn3BLdhCoTJScmqHIvY6/Y4BLYdZH/s5vuf9oWr76Fqx6gn/ACvsf8x/cUfpWGfFGtGdLKwjViSZ+6YeseaYcj0okddeEZY3qcD8gEXTCPG4+BMTod0jvfgEgl0I90SHiHjlLQjad/nA4zYTycllXgcnBfC6JkyRipaJCRAXCJdlknaMkSYTUL/BF12RZ2fBpCESW5ehMPf03IZxInljNB5ozdjQIGdxvfY1xP2g946XYnYs5Q4utZaSMRQaa0yO5M9j96FQ8jL70rZnzETIPeZUYhoGJRyOzZMqbSrDTWbNNRAdygm/kmDwROvwILJWS/iLdKDTXGmCbUdsGwWW8ONkASywrrVoW5Q+LkkuiCEGW7P2H5nVxEDXumE8l5U/gxQchT0lhOhGPg/yLpl/zkfzXBs5JsgJtPM5M5DNFxhJqWw7yyQahyQqsryMjOpeBsi6GpbCxSJpuLRbTN9xrS22+RNgmzlHEJtHyPBvmoc906D5lqsLkWRYZ0WwOrCFZW6JYk0StiKYZ5LZhQRqmb3cIO93gSGE8EMaJ+Qkr/J/ZKHTMzb3kuOF1e2xqFhuklLQySRpZacC5p4IxYRF4VmGyIFGjckl9lq9icanr9yEazrTZQm5NmK9yBMs+wpi0dIkuA7OCTGJk+9n3Gh8okGmMuhwEPYhl62pBBFPde5Eaow6CMqWMEas1GXseTCpeiW9ro5nsO8EiTTwzM1Y2e3RsSCJgFp2uRtqaWUPOpdEFXPJDaC3CMW7lsz5aSfgyoiROiayjAmGGkk7j13wg9b4RxNQXwjVfAbtS9zqvkX/AEEN/N/QyiPa3FkKTk6mf+w5/cHur3G4DUp1NUVxvkklVYziybZXdXQsURoJaI7ocjbyxQFEpxgfA0XkQq9y0DOxBy0lEjWfNzZrfbpgwlDwzcg2msxKQRc2Mk0oUZJQSgt6Ca03M4ieRZFoPbybxjRLLIiBUusEaCe8FqoxYspJ5g25ske1FqoH5zEEhvCFpERUkrEmhIrh/wA1F3djhNmWejyJPGTh5MC16lwj/pxMInZptikkeBIXTccfI1BLttYdGLcakWEwXR2s4JSTEvmM2tYbg9wbbl9jaXdDiztEQjXKZEl5jsbw24XapsS22Tdu2eNBRDbLCVtJsV2xLdB/ATfQVoHOTORAjTlENa1sbMnlxaDjizpGdjTXZBOUTDsONYPDJZZqfDmEquAidIQ1a0WPlkUYW6Nvk4CC1vmph7Mmu5nkwFkWcgbiXpyM+vBYQ0Q9HsN23lM8QiSXTNNkISZiEpEpafyJrDNbEq8PkY2iSwtiDVdkwhvexcluHxSW7Mx4FgaGWc6GqFtNZ+4luxoqJtRKyIIGhSTuYmyXx7E8eymJ57TfyNr+hqG3S6B5klC2mRY6CqsrCNTMy9jqRhR0yM0mDhyJkYSXr96Jwr+2fo5vs53Lb4i/jHX7J/0MQ/3DS6e5J/3EwCLYPJB5gY35Bts7tfsf5g6iRS/sJcMP9VONew5SiHkL8iP+Acrci4LGmpkWBe9IdEtiHsQyS0MeXar+1Rk4TCka81Rp0I3uSIlJM7k9aHrEdQn4Oq9xaAStp2lmNBQhrPU7htsZQnA+WLdW4KCL6AEWnmSIaylmTPQyNROyMnZpIysO8zbp4oe5I1hpZ3hDhqYjvCbLMf8ArMhtOZxIRWNxkzCJItNdj1BdhP8AvwyA2asbZJA8Vudyc0i3wPK2oem7Ql1t431LNGy8EVwf4Oxa/KhdkfuL3FlSrajZYZWeUCGpHoTuuyY8yAQ21klqIScezbKYmmZuI0Mm0ai2lmOJnFxFrlEmzAVXMhq9QfyJQFxudo/4GsndIbZmhQbIdkbkMpaEbGTYQmcePhhkHpWsoHbtTrN2OERTSlNxuTl8DckhGb8BYnuETAb6SPsbLthTJ8s2bHhJJy0QwpzZliu07WsyATgZwNE44M+ULHa48r8ikWkymMWRGOiFXPNJCVq92R4sLJoiS/4NBWwQt0NiDJE2g2w4NqAsmNwp2LlvT9liFsTdEJL42RtpcpEFis3MVOXuYdjRCe4IuHBCH7FtPkY0D8CFnBK/6Lf9C0MRD6hH9whckDVzToIypYWI8i4Hyh1Iw9CZtPb9GUGJEMYqqSU1ZyjmHMchMmTNC5KnoLidCGxHYiKOPcP+iJePcEuW9sbCtp7Im3h/ihvN8Nfs/on/ACJ8+AocK/3gsgXmyfwPDO5T+BL/AKCSNwT+gMiX5oWTP0fIMjFTIVuyQosiTFkKf8uSO+WKKdlQyCKYQOUueBIRyGzxCMg8ak8GqiAhMcizTOGC0cqyJZLL5ysPsOxvcGocLHHKgvicR7RXt2x7BwJNvDKhYJ5/6EgrdSuEww1Z5GT3HadrDrsYvFjx5ITyMtTllqJE8FlNZ2GfZfTM43zIWV3JbDHhqBlbYU7MonwfuRWQTW6GaHkJbbiJWgjuWUnhjU8F8fNNLFSlNvskKFfAIURPHAzbptQCG3zoKL/gJmYtLmkNrJO2GTR9oanFlB3Z/BiJJokMkrcCW3ZcpIScYlqBogHifdkbLZBR3ttRCXBn4JtFmV9hQSyV7aCzFg0p7kMfOXdTUauxS4uXcbDwj5djuEnCwh2vEkOrlJBNL02sSayZ3tA73R2XSfGa+I1GTMJyhrmTSmosOlc3kW3YeEfPiV/MYtCLjW4wkKh4D0mDGqnk+gRlS9IhqZDP2PPoMKZUveP0J4Q8p0NDdJtVK5boSWFLxLdkOZkylOwlc02jxYZD6NOagYtIM4E5EkeF2zEwKtJQtAlT1nCSuZaxY7DRZWGRAg0q/XJJcQRwQ2IbENiB5HZkt2Q93RMm1XzJNG+CTJnzKMNFmu9l4pZanMwecwWvcuRfkxZ3M3oWAndjdiK3ikZGik74GhatOEonfTFzqIc2k7vPYtDXIl0guZiS+DgkzKxdCHFuXwxmAm3uMr3qt+BtLT+iF7kGIugzF3f9DKEKN7kUxmP2fIf0SqViWN1Q7W0HUKEjxckYw1dgn7loX2ExTsaJlC9nkauYi4obIJrTeiVpOJsyZFsDsmPDGJBEL2didJN0pFc2pY2TcbuclnWpkk1JdE7S21I2MI5hvIpFnlLIEeLRiZtJKMqMl0zc9CbUzHyyn5JsoCRtJdti9lovJLu60HLF70aCyJWCaaHq2WA1hYNwWGrEzPDfA0eyGrOWaVuuf4l72azO5IuiFZbk/I4vXWtuKHwDQrZZI0INYjKSpjRudxpXHrR9oS3Y0QkdwX4sdmwi54wf4gfTE4+SH/Qmoj7i3+Eu49iGeZaxJrXkLspo1h3LD/YP/uFg6PqmfWjqGux59jzVgJUZsZgNctIkYdxEpXXZnm92Il425JPNFIdNDRsl1cv4GuTqVz4EslLbD3LoHjzPLIyDNWmgn/tOSi5YuDF7hjNCB0dgHfYWQ7wMYUz2kbYsXvd4H/MibANjubpkzy5LPxMdFgeKa+jJ3Vn2Mx06koSmpWtOZua7G8j+ERbg4NcsNC3m5kM/oGJqxseHRI4aJcBkrz/Y/QQ+T2T+xdsaStoy26LQnA8kmzOOx1lx/wAZPNblq7Ghf5YaMcbCyJYUCsEjTcgPMvnB8l/TEuotJOe4lm0iuEqJufeJ8hPQJw5H0F5ncW8Ki9Q09CGCXFhX9luONklOFPuaTODuhZQ89QttG/IL4jowRczXGhqrZziwhaSmhmIp2NZGJDbu32RkenyOc2l3mSy6nslpE/ZkItoOWS9pF0lXOxDWquh2ehBMzhTccaYhsyzO0EDJJkGtYH069tJpbzKbDbZrH4QQz4m1ysF0d29WaJdqZjOSETUkE1TfMipDbJYhdQ0i1Ak0pB8Oj5hiQu5ohIOScc0FnBEyPiiMYSFAuF5bmstW5LcEA7Bht3Zq2o3crdiGTcdquFMmZB5qwErUyUYhj1a3lk3/AGHtiVQw3qnYc5pGxCTm+4nX0jGhA0mmuRHL47CD8hcjCTDGlpJWab4E3DGEkJbgueB00o1Ikr2MTJkNZugYiDJBSGUaizBbdgkaujGtEK2cltGtj9Tsm9lCJFV4osDpgxoTuiIErdhOz7iVdKHtClyMxkUuVhkFgWTIfuEk+2EluIEdeb0MvoDE5GyIu8DWM2TJKOiRZuYPlvum0iuR9Cn2vpizA2YvNyJ/psXF7CG/aJwq3SIuYfdmjgXWtMC2vk+YY2yiSXeSVa5CykycTwKih7L4X+3GJMpyKTsoVZ7yWwcK4VOhigUSsHA3taEI1HTQsG3jajgiJLTulB0xyQ9oyJkJkqRyS6ZfJeF5ga25NUwPI6mHhiWCTwKs4Tnd7ivaFohopak9FIjfEL2HMy/4EqbQnuREw07EynDyJZSyTm74Hm7GTKoLIyXuREiCusNoaJyxKNSYejJhIJgiR8yNUzVpEjYx9C2eiOk0NCKfHf3T/qbCQu5ofMfSEldfvTMnh4NQo7LV37hG4pZYqkoim4le5iXUkBWZx2xeSSWZMl2DmXjAzE90U25ro4nycEkQnKORDCpqoPJnTDyIgyDpUvUTbouQ9vklN/ciw18n/bOx2kTeWBLl/t+mSZ8DT9kts6Ya0L/3guF31NErHIQ3JOyoH/VEWj9iHR7EQT/sKoknBer/AAGrX9DbVoxKdiyuWnebi/G8UWB4NBBwm4Oj3JjQUtDwyBIhuTCZzcmpezGr4FMLai1EGhPkYz4AxLZCM5o6MKKjIkXJGVLwRydCwBJuxYOaG8SwfWo/zfTEkkI7w/yCbbtmxhiXuETrY+MJeC0awka6yi5Apuck158ohuLdWd7oXz5WpPCH3BZLyJjAUt7IQM9N3HQaVT1L8zJyR6h8siq3clwt4GVZemqeYnLNhY2/3wTCywvmWUOV4/8ABFuuGmjo2NbDltQSlrLWyVi9OUTqWrEo0X0PW/L5HDm8sSMihaZQ8TNhgaj4dhReRS4bDZW5kLDsupc0NjRjE8yUXuRNWWQwSkkJMo4UYFLcSxFidP0Rg1t9GIebaVukZpX4ro/w9hPnRF3/AKQsPWq+w5z6FuxNjHBg7pcbiCS0IaYXRfgypInLcmMt3GJqxm0lsJNhTJdfIim1OGk0MbOBwoHi2qbuGoSNRKxCSm24h4FRa0XmrHzQ0Jd1cfWR+lIWxAgjlkcsh7kPcneq5J5kjuxB0C/0kSfwG84u4+GICWgk8on0vCOT5/uQ/lTO97/wbLbxNqXSG23pDyleQ5Wj9iVuPFE7V0PjE7iuM2Zk+gLVJQYLXEoYlZsbdQ2eYZKCSmyJLoqNMSawH5567ZIVZLbeBptbRgRy1jqXDJXcyJq2lYmDU9nJaqI7q6EziFOYI+R46Ygs4S3RfyYsOJs+iDUhRtvKUTZblzoiZvIm4Q0j5LgLbYxiCHYWRITdblyyOQqSTZgw0NPGq7QYKGpnvksnzECoTnfCkaNDapW2f9jq2zYSxIf5nZiFNC0bvZ3LpsPHNxKgiPuwYxmRyS4BKogo2OByaFuIY0SUOeyfI2Yj9iN9TB7l8ySnZ+CYj9ETs75QrsKISh7BeUNTL2EVw4v2rmFl5LjM6R8BoGvNXcwMOSk+RMUI5n+y40MCpaSUw051MrMfwI1zoly/apQ6TQ0r8N0f52wkeRoRd/6C+x9yKXKFXmC1GqxjEYUuhBLu7IEXCMnk1LZYTMkzJmGrr4G1NFou5NA6ucD3cEYk5xMFiv8AJF2nlDdX7Ofsz0F+FNPSETcbJCUYkeatPYkP0DEVHRV18enT0YiUhSeWBL+IRDQJ5RFr5GpS1bcb+40OGoJKkvcneyLWn0nEJthLqOUJFR0PLNQvsw9LzA09whrRlWJJEyAfsaiGXE+7ORktx7JDNaJ3Gw37kP8AaIrZ7Ggkyn8DKk+mXti6QjY/7sgEYSTDLuRFaYSfCR/IwsrlrDH+uFgpnwYWS7WP30PJKkOxDsxqmkNciXQWVIlS1EZI6tTui5Paxe5mRq4tqPU0XGyjnlgrMuyaIrMI2tkSo2WtDGRppI73WRnjLcVzMnkHIxI+KLCElaRbadakI0Or/khCg5b3BDmupT4G2Wef6MRi4sIhvHYSV8EDGzWiBSSUlxx7QNObQnR8cGlrmZevYpWb/oah92kSXfRMfAmYUyazIe40GvbrxmBZjq7QnoU3CW4HNXgpnYiWG30IM3jTQkjS/g5SLUXaVgbIQeDXXnVmoHtGzPlJ+xrYGpKNVfhOj/O2L33EEjtfUWej7ofzL7IXT0GNxyQtWFc0Mx6Bka6s+QnHKeBvAhqMOWe72FXMwNJTgUNhQTS71EhCbZtI2Thpdni/sGavZT+xlyXWGFGgkJDX+LCNRaj+xqOmjsuHk1VsRZHVV1/DjQSucP0ebf7HXcr6GGUYbzcdNrnfHgzbkW8XxPpJVJK8aEIkwyLlliiCcpN/QkmpasJU92zcRZMYyTXc54HDBRJ2LDylA8ehaE3mizRiqiGl2OSNDzYRNQSV7iwmITWcIaXdbIuZxl4J7MgsbFQ6MqS1qznCAuP2OAf4k4GLmE3+lJwa8Msx4Gf3kk/kRbvArNp4EwKnTYtA+1RoyG7y1h65wZZIS7tvYW9h17fGtEtUtEii/Ge2JFhGduV2F7Ewkq+f7FyWSEy2BslKxAw6Nmnw/sWlXZEWbYw2/AlsiyaL2GTkSWj2NfTBsJLCMuA+loLkBe2zdk6d0z/QipI9Lv3Hk5M5JbrWlCRq69iOgmyHw1ydpQaZQl82LIsrfJcpXlFyc6m9Ybh7cFh8jCToJoyLJN9xvRnJYTeBMWDLmhQpWBqWhHJNot7DIlfhKd2thsT2sne1GlkZZJEgPX9h+iv+TkRb/usP8yRedK18Y9ol3tfYm02hE32I2Q87m+Al06UZZHcIzgrCiGsfBC6stiRU5zc3E5k13kXqb0LUFkmZkkWDyTJJOIve5eS0gzYiz83yaEC1p1Pu5n6JgW1TP8YVNPI/vR0w80amqlmJr69fw4iyp/s8CqOb8PIuWyL4Es4O0bTi/wCjD/NRYYhetYalGHocLmX0Lv8ADUX4hbH+7CA89zEuEen/AAlzMf4dEQFi9h49GgeXVFR+hE2QpyprDyxHCPrIXGJI2luGFDV9RqhjsLkzUN+oWVS3gt/rMuyIME+iV8nFCBJSUl7I+7jbuq6Gd8Id7GuzQe4OYX0MqGk3p/Qm7uchC0mQRwld+3JNKGSmJVzecaj2Ul2y6u68iT9AIoQr/coZ79GPSa5+B1YHPAftoUjZyLpXDwXpCNWm0XLD2hEJpuW6TxJYhVDE+1cTaVkGle8ENC802hAttJRh7v8Ao1z/ADQbor+EZOafsg3eOlAcF5iNZHr93LbPe9v2XKUSIXlF0XtgmdzpcexZa3Q1YTiRR/cijO41y99jFDicMkkkkTEJbjGx29Wxj0JnxQ1wbUrew16R3/bz9Vf8HIsDDLn3IHukof8AfKPASbUDdNFiY2jY6NJwLewFsGqWQv8AQxrKW4xkQnsNN/PwXaNZYsxDyw0XvFG3yIsGlxuLBAd0/JZe4fIeBslovo0Hh6PhQzV2MMdGsu6tdZ7fg18C/BiYuzK/zBJxfue1/pS7YaSlh4Pcaa/bGn7junRLHv8AUW1yMfP3F5DRb5+z5f6FZY4oK56xvFf5Bp/zIn0H6F9DJRYo/QqQmatrDpwN9jMjD1HtxFoYztLZMijNiwMdDGhpKWvIhRREDCkPhwzLHkhkQWyGyC8LkHbQXeiL05VJHSUJ4GNAO73AxQk/SBKXsQwJb4GVkCZj2ByIWmBRWTvAlsmzN0XsPZid9xqxJDHSjGXnwIaTTE2f9hm0un8kcQSQoicWYSv2Ju0opzfvJtG8seUfIh+wQfTSWVrCQ9g7aVwUf5svJWXa+mCzCzXOSJvvaCUbJVE27INfdF8hE7bNUTao96fsfCnIlaLbvdiSF7YcGQJxaVqO6SSaSJFm5wRN7qzrrWSfQs/0xVmVLf8AXMdSWtoIG+1GWdg0+0T15E7SxfkSFM6IYl8xYH/zsIgRu/UtE6Mcmnwvotzw0NybEQILgJ3c5EvRtdq30MySNJu5jVu4pSeiSWktOx7DsQoau9WtAyGa1zLiRZdEtW5aLoPBtljmLrCZI+ZHyOhFDl8mWBKLpc5LybYomTOi+hKiy7GWOmnsYn0TGkjfoawoy2E/Q6Kus9o7Im8ucJlr9DAH/LoXyfs8iFrkCw6FKO1/oTMW/wDIn+G5oAKYbJP7Egm38Ga6FvZBOV2mrr9CX+OSyEPHo0mBc0St6iNDEUbyNgSsTm99Byrd7OpNwr2L4mk8COb6MhoMYqmurxYcbcn0MJD30LwsNDVk0YxYd+f+iR/CUk8DVtQ7BmYHRzODAtoKv2EUcxF6iXckktSEQGkCPYsvLROC6Lrd3W4ZmmiaIs9CGyIWyI2IwMSK5LYQ3m4WBXaF5IlnNdKIQqVlLA8Lb1OSQZhdjzTdzMR2Gbga2MyHF17kj3HkmdvsSSSXejOAW0JWg3LQTvY6BhxHMIezpJI5MAYDx5GVP8HMsCCAGajV1dl8JWLtyY4ThpqXw619hpfYax5qY5LnH8DQE3WBEcG/Ul72xwmYKScsg3mmybQ8mnGL3P3G0WCgllqyHtoSo1yQxJJTjOJHRFDvNoEbrpTpyXfKsUxJK0glrd1Yvusa2yGSjKiyshDA2NRYGXWyO1Q/RMSKqrNfAl69B5LjW0ntEexw49yWt+hBJ3yaSqV/6C/x2Ot9KwvyItTWwaZOEfBm+Gh5h0adX+wJamV+xLTX+BLN4EWBa0CJr/HY/wB+RbrwP0PANhxR+ohCdjJUzFih0WpmoxipmD1NKraiU05hhFSCYLzysgUmeTC3HT5G+yJvI5IQQDDG7nYiVMtfgLQiflAz7vaZIES5naaGn4U7XgY872BJWfgz+VzamNzyxyUneJ0OSy3JOSRZyPKt8hwxKVjejpNGyWK5fSxzqkaRgbuK4DSTTn2GaYOCnaBHdL1jwOvgYJuKs3XQmhKhB5EsixOhzNceCjQxkiZp6onQkFuBE7XOEQap7Tcw27C1OToxE1PZrjQlaodiSVsiNg1s4JQ7zYsyhLdB2pJT1+wwVyGLReUXjqZLbTk26LLewaWhOESdw0TyQ9EyAZYFXTJTDyxTm6UXHStPaDoKqhWTegy94cdjUz5BxEtuad3JvDVKDZMW+C+hOeioWhExyJbcjgkYa96LllyPA6NRDy79GnsXpWK/Br49L9GJ88mv4QkdMRZ3uZv9wL3gbCu1u8Cw0RzuZPtgknrVInGwpl7Eu76RckdnAz5LyOt9S8EW3x+4uX/oF/8AjQi51iRaaVmZJhV8Ef65Eu4gePQ9OqKVxkbDNTWiyWjNxmRR3UrWROww6LUhKTVjohjWIUuOWR03KTV/I9x7zS93kY6hs0xiZIHCPnQjui2IJlArHEiNUoWEQvNoRep2Jb0oUnY6kkk1htCTj3SH+Ue/PKzJNLN2XS6lsJFLl+A14/TkQkg29XoOdmy47JpnazG5Fc7i4UMoUTJLJL75aIbqNTeR3Y5wOnIZGJp9FQw3cUsNUT2piVdDyIE3QsXInJ/yWn2tMdZGT7mZI1ITrSJJJJFoiwzQUceGTR5Pf0xUK2MzNkCbQXciksLrzkbClKSliygkQTsS5F2Wo0EuqMsRAnyJ6k+JLYlrEbQvkvGnHDtamMHPn/lxEVEyLEhKPyxpPFkWvBOmnNmi9wEuS0+Bp2JaSEjDVpT5CSYeYXRKUf2Imw6CUwm4E3Z2w10Z8EHUbMefobHYxIw4zH8H6fhxPnmRwMr/AFI+BjPwi96ea1C+Nh+mWslvJew3O93+jkEFURh/2WNxL5II3TnPpgS7/lywlTp8DS1t9E4pDuGssHCErwPF6fyETncf2GHpNeyRKwxuJ+0I6/MixknwbtvyOiKaoLlImSXjVJHlF7tF+Cf9AlC1+RJTuqFgdEOiJu+RnqCXebiekRL7E5SFJJCNKarJeBt/yFBSbnJe+H6FMdIFzUIa7gaJxORNEyMG2oaCBA7k9zmCTrJh0ahxM2b54MlEyD9OQ23qK4HyBkasbFrBIbalt5ZLhOkL2FkrLNcb1Fd0eK5KM1W9ziKBKQmVpGbk9yQ5E0b5RPJ7ng9jyeWWpJI7jf8As1gfy/oWCB0+Vyalkj+JHOcWfsREWLPgyErCVxVPjRFJJrDa6PklEKYmW37BhPdf0bi6f6MeWHY/Y2w+zEZ22421YiVkgLZm1uSm0mhvBDuzeRN3PA22ezItfcMTzRtUWV2MSMMafhtfFX6sKAl7iXP/AFJ8R9DCus/yB4+SPSDbvOW2ZF/liVOAjaVufZfI9j3MLZH2CJm3/Q+g/gsLLZosnYg125s+mTb/AJkSopy932YVSURq6IIU4NoWN1kkmjAtzMjjYiGH7ibqhJj3Ilo7ybC9mJ8EUdENUORCLbyLk7jwJZW5Kx8knDI7upnVyHsO85sYCN7G23HNfRF/CS1lNHcXMlvQJy+iUJDpq+jIZcaHLUkM0RxqRbMcmlQPPpReiFEhxZSQbYsTLGrKUi2ifg/kNI+KOnRbSbkSGsYV18UQi98i7DE8l3J2RM/8J4Z4+TTQ8/B5ZC2ETSfwTXWlFBaz/YNMEwN9donyLSSTT2UEjDY4yS1FucMURDqHIxMRy2hXcTKzBlp3P7M6MlefbL2ii5GKk2EyXvWCGQxMxU9PO57jk2LYNakoCS7WB4Kg8h9Qoagaz3f4MSkXDTT+jmelNJ7XJJ3TyRRCEYbihi7Iocp7M6vZUsO7bRNhdCkeQNw727IbjZrSfRBNogxPnElsxIf91xp630b+F94lz4fRE8jGXdvo3j9Zkf8AxyY0tf3GKf5csQ9WItKv/Ll3e/pCWP8AxBKRoyFciXBpF/BG7/HR8K/GWKhLsauamYQh3saI2JQSeGJWLJDWL2kmngxMmPkTKwbbB8ZmPQs1NYeMbVaEtC7dYwPXa9JG3qEM2xF0kHEWbmEXkg1Ps/eSk2V1KJwKarv2mSYAtdX8Gy+oNWoazI8DmNplmWNzqN1S4IqunobyTYPcU5JzYn2t/LQ4TW1CuoXgSodG7alwMUe4uScGFS9jShZQw9hYUYJ4owJJG7Ikmk/jeYbSOxk7GWrvO0mpXumhO8J7iBk05RJQWvqGh97MBXI5vOdxX3a8C70OBtejZkxtmHQXBnJ2hHUJKlCuKWENJuk2fIAZjoJdnjkgCGG+6NmXkYqXgcmoNz4ki5PCEkemuy6HexXHBFjOMV5GkMtpBe6wKwghjXHSW7JiD3ISK6bQv5FksHcprvMaL9Hr+ps9yRw80o2H0Kc70pHPyBHILmTQmkomSwTN8i3Sybhp5v4l5LC0+D6IQSz3ftDNq3f7L8Ye6vsWEDvy/wAe5eQfJfSE3+thMuYjVdPp9D/12Xf65MHXUMHTUGCizJiEO5m++CNonaxuexp6pRldG2FmZiVxInWJ9xi5+DIjwPhJiuRnYOfyhJQ0WIm1A1oNiMi/2FqiQJOVGSYJJmkLYneRuT1HfbEDV3Aj+gU0nJ2pYIMNnOryQmMspr6B0XDxRGlNKJMuJRFgWXgd/tC1cabY/CS0TKcvmDKrh0EyNgW8gYVGyiyhDUkkmk+mfwwx2R1LzcN9CW8she5cFJ2OGn7IOd/IQM5mlvJii3Y0F2Wjv5tyJX2WSF6EQtYoGrhc2j5FjsSBpBzd3T9jl+GdmOa6MprBPqvYXDLpEbl5bQG7StMuxEPoY1rXgUkyZbogmnUO7QlsEoCKCfpMx1b8EqElEiRDJTV0pbENhK3Rhj5Y/hGMbst6UfQ02pdBFFvyQzCa1gQWtZdoEpqrrGLjbnuAnFDg9zQE3fD6E3zDTeC8JQ1KeHccRRrCXIqE8/sMcGyU/guimEzV5gQZZQne1HyH9HM6CYL+ArDXE/27Pj/ceHW1+XWttToqmnFg0o4M0JsxT9VZdW0IGmQchZlbxCv7jPNmc3l/snSr3Iaj5kF+wrCG0+Gn0byYbrYWsN1BeRjdiRwxKyMW5LcnQ6F9qO1EyVdCSaRsIcrCnYFRUeDSjQ7ka3IbHrD5ENSm1UlwGsz/AAtkkVSdmMK1hWmTeBljyusDSYDD3kYhj9x5YsiGNk1n0weS25KIHAS6UQQQJEEvU10xu7OXYpQSTfIeSHrNYMD7rCbj/DsYGoS5uyD+YbPPsHLWLdTtkNDyJV2cEQoZuOMy7++Q1wzcZuHgQh3/AEbwnlNUvaBiVszYyZMBdYzihLaEkeS6FnMO+CQ9omtGN0zM0QJEEc0n6EZKzpkLFYIILkt2T3JkdVSSBMY6tITp6ZcWUzkewzeS2ZIZjWYvA1qXwIbZXlkc7xlY1gkbKLbrgZYiSG2BwctgYU23tkOyO5CSseHJiNt/uRXH/iR49SMK4qdFRC5Lwp7Mnzj6TkNZHPzEppOgtt0Hn1voVx7Zi7GP0pWGXkwyGvndzQO0L1PYhLE6kZBdoTkekgjSE0C9mLY9gaYEA1ZY6ESBA7E96EPak0RcgmPNFTQWKp2hrngSTYGuEOyU3WFssRTmJyxpdrN6QK9aNEzMJosQy8uiY0f2NyQ9iOi25bklbEOPRJZcggSwJqkQRTcHMQgkGpSckyUIijwlucwEnBrQnkZcnVEmN25DCrohkv4J1le8tYRJssdxE88d7Cwx5GG5G6EzHETppu4L3SxnsLmwQyQ8VUzJPSH00zUI8ECyNcCbWOETNR7Sk8fI5e3gukNiBCiIMGNCommQsfggipBDpyM5CfB1OAW8f7kbNZFEJ1eBkaWnYTYlTSJuidtsHxIWdTOJGSIpm4liylJkeVVZLozUeKnmioiGgbFuhvJl8Cp5NGY3mi+j56InMt/AmjLTce4kWR+hVdF6YNAy8mMIZZdEknzpYzfAfXCRHyOT9tlB+xA9FpjRoNejGrSkkiPYSGlO9FTQVGXdBmMOBN3lzkYxJdS0YhInKR3fNCPcsDE9xMKaH8Gg0MeToM1CcEtye9EkusEVkmv9oSZJJcMXZHokTFLFEIixoQMgQtqoTTeMklxvcYy8cmQKkc8NyMj0FNtSIYJcVQW3G9hD4+Ccx8CNPkNEtYV7vslq+v8AQ2OjYsekGEHgvrIiWqJG6QiG52RI1loI7I7Iew0JEEemfwwQQQRW+4m3JHQjsJGHAl/tiTL7EZg6QPI7tmD0XmiojJkJ54TonyCzuWSi80ny6ESixYSMo3nU37JvPk1Ax1XpXpWB/hTLDYkY94Re94EDMm9Eye7aVYqaCoxZAcL4i5FgRc6DUu7/AEOr/JtQh3ssCxrmnEaVRjRShNqcCJz+VOwwmaJdsTaqaCVEUJraZXsNjuvZBowEul2Htd7lt170YNsQZBpakyDPUDIhlBvCRYCYYqUNglaSKldhsCHCfY93B5JP26kZNhjH59oURBU8CjlCTRoTtCMb3iZw90f1Im/saBoOGPiaJpjXoQ6Mg0J7EkNOCKQQOkIgggj/AMUWEiPVJJco9XT6Bu1TzRUQ/nBr8UyiNBcM4+g3wjnPqVht+r+zfjx6EP0IfoWBiNfx+YuCj5kjUHlJFi5WViAM7URrV0dO7uSQNYH1aYWJFd9WSU23L1oQ5onojsfJkPb6DhQY/Wm6jfheT/KLMoJKEqwqZ2FOhLcXXkg1OpEh6Je7OYJGsfJtTXBJD8I5q7PP+Ru/WgavT6n+R8MlwS4ErBLJXSMNSlB+htLA2erJ9Ekk1be5kIKZrv8AixK4exPs0Hm/oK2GLtFwlFBypXk03uNw9SKWjQmaPNMI+Q1wMNTqQ0X2Q1wNL0B+ghVZEOsEEEfjX4hLzshrhCtq0JD7pRrvSMxz7Yb8Elp6CwxZyQqZaPAvhTAPGP8AZd7vugfoX4ixVr+OG4gaME6jzDWoW0a0b4L61O5GtXS6EpQ2JsLENihKxuQTMLG1GL7BiZJ5yqHkmaywXIEuYkPBMTdI7E+qDdfwR7sswEiY2YmSTyOkkiRj5/G3Cp6+gSSST+bEN5evEE9zSHEvDj+CE1Yek19kyn6/wNo4aet/Y1uTxa+jZ7iH3vSoSW8FupdZudgjRjVhoxzwhq3LkulqQQQQRRBekkltiEdqIdYqQyKoIkkn0wW+xSkZIS2IPiuZDwDrMnf3Al/0jG7H+PBFO6/zcm2mdBrKMHTQf241vgyzAuz534iH6FgZqa/l5p5NwQ1A2ZdeSdau0KN3umNsciwYZbfQVXlBxchqFwSe2dSZhkCwrEXdqWOdaSdAmtGNllNCY3AYYtdxgb5JJJ/DDeEyexLZ/kMP/JI6MHZE9zUaTeQn94SrqLnMngLRiGtZNrWYHCulfKYlvb4ujME34QwUfDIhrKe4lTK7n7EN4Z9X+hizHHEBwy0X2Rcd9mPYGu7HyXoXrHH4SyLolngsQQyGRxVYErEeiKeSRDRR6CWOkktyVCQWC9sWwrm8iUsdj2uJ9T4ZYnk+UOmtEP0Ifo0Gamo/xpk6E8kv8A1sZeDUBSQ14My4nhjIiHSNoXbLTm3Y5RDRrnZjy1xJtwrkeybYtBXwSVB4cokdLVpb8InoeFNBr1mk0n8EGrORjZlv8BPow/LlV0jVPawnKYvI7OCfUk9wkBQnkVkmn5LE1CQ97LwxSUW8wzZUtyFQcGpE/INSLPIwso5Ukxv7xKf7jHErgKSz+L+6EcSS2b/Y3TvEouOEdMOSEvuGwvJIjWaQQNEEEUR+COiHt6III9EkrZCjYhTPb0RRBoZek/QmSPRcDWIYBa3ILwJ6iC0mNTMQaQ3EzpYa7E3eBpfiWP8ACh+jQeKa/jRu/oSsjBGJTHmokviBqwXMIfwGkTyP6MPZJHE2ew250DJSt2Ic0U9BEFTJxK82L59DAz2QVQd5Lj7iwr8+BrcsbliLHapJgMzpJJPpkn0BMDGh8jQZJiDuj8n7/ikhZSpuiV/nD0r/AHYabZdiZZO57F/MCBuc4gNqhK5BvM5ckgZ8/wBinnd5DRlvjoZh3WFIvkG66c/KGlldyaRmXri5sQJMLxkSVITgRgSecEKeHkUll8tl23kkJF1gt8hpTmWEifEWuRqwr2g2/nGdy5eBINpuEDdfMSSknaK1xpo4E0rL2/sTxI9v0JNYOSfg7F2iLhJd0mMXaOi9ZbkkrYsQt6kUmkKiHsRSCOaGZEEUl0sQRyQMzGppVjFSCKGcWaSW2FagEJsSqzbSTCBDKMcjovWh+jQeDUeR0X4EBLJBaq+TTBK1CEtAr8SJWIPR7jS7+BakuxNsSog5YcrYfTDfjBEgJwIQW1QJKsJi4g2tw0iZlhkwySSaPT1JolixH9hMRZdsyhycEmG3bIe2djhbDcGXr4G11Ibl5kfCZh5/H8gTqSNSEsynXMiXJdpGrMnwZVkTJDSadYLiOsjbk3tJfE/CFHHs37Gbc2HEmSuLlhmE4I8wfO9bNK1mRKzWMDQQo0wI2DuWRnl4gTI3ChCTK9glZyFpItaslhK5Iy3LW6MwrF3I0bqArqJblwhpumQjDeSPK9wiiTa2EgWdmjGKyPQvTetmN/pIDgom7gKWDd3Di7238q5dEe1fY2YfSn6GzZeQj7M7SQxqs0Sti25HKG1JJLDTeg0mjpoSSTwWIqQRR3bMQ8DJpArVSwyx5dyZUggguXHRkfgQ/RoaGox/i3hq5GLJQjmEPoxFblTtE6pNdLFwoWcnckOlClYkLlE1aG34EE9Rk3deWrEqgrZJ9U8iOJ2iDcfA3ptA1Yd2Q9JEJ4sE6uTXZBD3FXNEYZeibCka1LUHJ/Al2Z0vwSk0iO1iY1XsN7OfAk9UilJ+Y1YvuBNrfwGcpeAvPAIlOQSNfxIRJOM6k1Le6TGmCQ4E114LPMEIymi1dewuEmViXKEmjSXkzO/wOGWjxYwp03zYdub7JU0+cCY1LQZO/W8K9mLBCc7oc9DwTf0Rr7UMOxyMYOGvceXJuI7E5kzsHumRNpy7zkurKRbc2vAtEy3wJ8ly1nxYjw+pibxJyiCTTVuhqWYjCbsJZmH2XmGW8FzNhimz8iDOHwI9fTUid/A0MmgKeZ9rDUvfoZVf3GxyRs0HrFchxSkk5JjFmxMkQ6XRIngseUQXLkkLYjydydEEUkwY/R22RGyhE71FCzRrk/8AhQ/RpTUY/wALFiS7OqEowG9LQtaxAFvYRzIWB7yGuCEyO4goOQnU9SHNK+izAbYmR/KysPI22KDwB2FY0XEp4ZCm0vgu2aXkl9o4QzOFSIP90i5/ApOXJIwa3oljaAlqbcIWp4QNy3nJyHbj6L5j3GaXgnFnPY7d3E/iQ7uIe4yRYackL2JaXJqZJf5ibiQYsakiUyWbhN7CW/2N5x0JtF8jXfgm20jyNYs2eP0T4B61xSTLXRuJ7E9j/kbi8CDbjyHPR5aOIFwhULnGprjds85aWpaQb4iXV+GM/shRaQ2U/AOSLfyRXleRDHtP+Wxs2X8DHrLlBcX3Cape475HaE7Abl/saMD4ZyieiaZh8B5vD4Q0qS6sGj/bfoc1n6S+zTzbRDa4fomfKgqYIIqjiiHWaliEdhYVRc0j1QajRuiTJA7EMvtS25FH+FD9Wv4zFsMedNhAokpljSIWEOoNetLMtybpuxIKSTFvBM2ZLoSd0EsIK60PRDaX/wBRrxFmUiWJnVhvWpGqZY2aPU1gOimtxFiK1ZF+Q2i3ybsCbVGWqHfNwIpstpDYhTJfgga3IguYgihrXCG+p+Arijm4ExwqUtjXHukid48fjeFcwXZahWfwx7tDeEqsmo4FkaQaEVySbk6/kjehtYENpIbB7UkPJHqzI2uJPcuvaxlaxfs7ZM6iPKj2LxcNiLshVpLrT2JCwz/AhFhf3Ri7fIy8F5EtLyJds4kh3M/ECMV8LdjckC6Y4JqlKwyk+hSSeG0ILqXYksPlNm2LuUupD3PHSIrC7rIgkxJ9imu90jhEm4b8BqoaE2VDQJdWb5GR5pshedjzf8DSsk/8ZLVmbZP4JzEteymI3g7D5UuBD3OlSCKQSEom6UmZPj+cvRSXIkokkkkmidjLRBBHoaRA7DYjgt60PHoVNfxmODvExcCYIjIzEaPUlPUuJcMJoWo0JGS1ci0DoEI7ET0Rykg9ZEXlEMcCH2S+UczJ7ugndCIkToZnc5HJuQTZCptqORYcbRKS8TO9GsfZjq/JK5gwKhOUbVq3AzcxqNLiT9mSFZZ9lrBOmkle8DiunpEy5E5/Idmdg+RLQYFKdiSaJEsnk9nWCCC4idiewjTwy+8jtkzJ2E4mLCXdIUFvcKdatyXG9wEmsIuxtMnwXW37AkVlcG5STsjtltA7xxuJ0pc8CeG0SIUhObyED8KEa79huB0/RGpx2E65OMll+glC+vKJxdi1jv5Jr3XyNIyUeZEuLE1rDwTicRuTCp06GFm47IbBOOS7b5GC/CQ9xfDIb+Jj4B7gSzg9yF8ixq4h5r7I70D0C7hynDZdkTQxFLEcjVh5g0n4JNIETmmSMaE8EosQQzSviT3oTRbcgggf43j0I09RYH6WWTLKA1AdK4HeAtaBajIBYymkQe0btTsQyQpQhKGiCRoR0IvLHukYhQ2oiRrPWRsRNE0yzIh7JjhMmti9cLMtiMduF2+EG21AP0FmQ3cl0xwg+DgY0xD6Ghlp7oeyNbtXFhLk7EHY01uvw+KKx5ql3CHsLf5kDXKMalmskVIIIZFcajnYZtwpMh2djNb4CVwg7FpP2SNBTF9CPrB2DoxwEp5Q1W4WWQnK7yE5sl7NMn7ncX9SHK3QiyXONS3+w0SSacjhw09lIv3b8wRvB5N2WI3o8yRO4erGo5Z7G10d7SXlyfhDa9jZlXdyWtYXNJGjLXgN07/DJuHKE5s7OxMLMNJR6HIk6EHLoI5g5MtfEkaL1Yn4eIFmtIhhIJq6uCZb2clz+FiXifgT7kPC4uNBIhMN3NPFd+xJoeb4ZDiHWBJN+KGVuyITOxA0R6RodCGXGzBUSyiDBCiW5I3V4/A/WfoIdVVkVyIRdTWSNFMboo2jNmJaDkgkJhCG4hWyJNkSmiJDWREGOglyGuTGbUJj0EqGNBBhjFdEwnaxqypEyTiYTkiS2CXhLGBsLVCwaW7QljtBfNLtCZse2Qx4PJJlPiRXb6D+WjByblhYEgNVQkMKKXEdWBtxPEBusJxT0aIl5xDTrCIL6Ck6moOxaKZqCQlyWEEhlF2RvKNzUexeErrA2b6AKT7ZI3pqeBfR3cPmIb6gNpER22J7qzYkiRtJU1shKJWraxoc5SYJbtfZySE5XKEz/pSO3ICbadlJqI7axAtYCVYls4EjjLse010EP9hKHAK0K5kSKGg1/MiW4gUS0KEpQ1uybw1BrfAS3LXtNdFrRoZtbtJDJrbJOuvcuC+g1oU+Rb0vYxV0GNHta2DgcJ8im9HwYS+0npdqBTQn9ISzYeRZk4cCTslGqcF6y+IMaQ7lGwg812WZWIvN15B3iHiBYEG2kNjtaOk+wnnaSF7hJ4waY7kxjDjlUkkj1Ma2WwxbYEkSIZcTLEIjkj8a/KOqqihMco5hYfoFaCTQ0wcdkKWDQRwO4zOKCIrIQV2S6jsySkRgEbmJFgsjcEtoWkEkTboXEIgyQxSTIYJA8SNKPA90d8wyRylT4JUiiVmvgNBpo3oxtLz3uQIaQ3MGLQpeBqV2kRslxLkkxtTdxTLCaZg0CJQItkkTCQwIoSJWD1jSwNCDsmNgOYzkPBNRhibV9iOAuSzNN8yQz+6huJNXAD1I3JCzeMblnMnbka2cdkyJpybFaURQb7yeSa2jwOF025E2SJpaX7IsZm5I2DgWlR7MIPAh0WS5MSKXkYujqWV/cETlybyOYtYHT5FPdCZYbOqYprx7FoJILT2Y1/mCeEkidajRyZam+R4p+5Jlp7FZ9wwiZ7tyJDW9xi0aIVZ4ida+Utmk5SYQfRayw7zdoZhlfuhvJfK5F4Ui3ElkObmCS96IGHUbNzMNCdcfqWUvkyJ02X2QMSmhlIn4uxaUm+5xUx4seRs4fssyy7h6kmc29jWSumIZyktYvkusjt2lE2PwgiVkl5yOVlNdliOSPSNJBBdRBYhEIhUNW/Bp+A/wsggQnAlUjUDPQEmnopx2GHIdrjd0S8CaY3sNzwbEm3Yp6i3Jsh8CbEUOXQSTLJJRBghplOwR8QXrDZYm3dIgyIAZuOBQnMIchLFjBZaBpYJsbFqyW2RbmkmCRkbroU1xPqboeNgTPUbrUnOSLEyeTkFvSZkoMnkU7dSiPLCI7uVsLWkSXmn4wXJ8qNUFuJ2lpfQg8chE2T6kzPcE6ydES1uYGpb6diDJKAhNnxDIHqpJJkuV0GsHGghu58mPlItY2JT5CI7CHr8BE8JJ8o0uwjG3s2bR8CX+0JJe2Y7DkZud0PqEyw4cHEDgsrciTA7fBaF18SIl+pHuMqWhQuR+RoBNWmp2aHvdIG8z4G70GIkMxIlNDSSVJy7ie3InI3bHNjNg6uNvsVctTEdE0ESfMSG1jTZvwiCUEZ3ErGzY1e8A7135mBnGMD7BmBs/7kP+osdo8CXATbfsVMpLZ3RKae5hh9Wc4cCL+FYNeHTyHKsnuPqiE6EJLEUNEUePyYeh+h+poONEhuSJe4hmhaYwWQraRxLESuKJYEaKJW7L4o4Rsk6mQ1I6DagpJHNFmPXOZEGgtkiiHgFy2B5oNgaIaeaI2BsZJsgsSOkkhnKNWSCCJDbO5I7jRFglxcTDgLcEaDkXq5Owk3oJuNH7iTUmZsBbcjuLHrPkfNfQw51uFBlW8DXhQ8a7YjRNt0OKzPljmnPSuaJJ3JlY1HYeuG3UFlvcN2U0Jx3pbMbwq5CibQ+xQ7pJ5EP6ZD5L7Btgg0Lo/wAUQS7wRNYyLa/AmMTA0f0NzZMx2PkkRl3A0YrrcmX7vyJUND7G21MPeR43C9xQV7iWMUKHon0NXhEQSUZ5lFlCcEFNSnynA8siWgNYUMV+yY4baDauMuRW3PDRfN0uhlLwCC4Sa5DddZ5sRQvbPwTmzT6sSokvIpLs7ESSRdEEiHPAnYJ31wzKVPkQV4Vn6RJhjDceck7LfYpbr5JetnuOU7R4cMhz0pJPxpXGb7ylDf8AcwZBF6ZJqln+RY/OzRB0hiToIndi8stprgiVD2gOJcSXFmA9KEkuhCJcNCzUgss1SDjyIjaDe7DwlB7omxviC+5C2hhdoQG9qEaIcsSTMUNRzdO4oTZUqxC2MIKI20QmC1mM7iEXEkE4ghmwk9BzUTdkWnA48CVobRvmpUaBB2GK4hQ0KjlJY2aRDZOEkTk57JDhz3GUlrdkv2RZJ+SJ4iVyYCBiVw4XNN+DY3JGJmwpWRWSTEHjHUjbOUFFEQ+RoOQdp8S5OX4sdrCnGJPS/QuZEnaQ15J2GVdi6d/BkqHpwXAO8skuyFw4Enewy3AvW9wk7OxdLmOGQuLw4Nx2wmqTOtkJjJ5gK0rbViOXSMl8iljlzJ0T9HDA86XGR3B7mBlRZeJE+YjwS3g7nH5N0EROH8jSxI95OB9GRX7BCxHZoLQbyuX4crtDeKXJFWJeRZCzj2IR2h5J/sF+FfaG4v7kNCYA/wCQESHD2SEBtouWJEK5l/atuvTI3b8mH5oYkE4iRsMaDVGRuiAY9SVmSYGKPYyQqBKFJHNjerhbDEcEOBpahOe5XuIkbA23JCLZIe4wpIJaEtSCETJtjNhXYE+xO7mwbjGieRLeLvFAkEVkEvSQeArriVsRaEmg0bm1IkIhyGTkTDSzNSJxsht0pjcwaRGiEq6G7BPTyi3oO/gNQLikE6ZCGjflEWLtYSFLTL7GPoeXLgY+bbibRydrtii4a/MkvCTUtcDI2S4EZOzC0E0t2JW5T9wlPbiZIaykJTqSisbYlBNnBZchG6170CjkQlFkwlDIuyVn2E2VJonC5ilYz2bzTY5rVkRBYY37R2G7LqXuW3bIVmz9oHBdwuxBBNkNOhI3cDUagXFy0ScWrEjJQ+WSi3UkI2Ce7T4EZwyTizf2Jk5FD1T+CBZMaVZ6GpY9jn4RpNPHgUb+DWF7FyZ9kN3ZgvYEmh44ubx5FDXXhF7HpDaaqNkOyT4H+N5HoaILrjgRFe1yPVfRYTJHg5Zm7HbITIjEqPH5MPzIoowNUsIoMRCJ3IdSJXoSLCUTRzUZyEzUgZG+Rs1JJE2SMdNBWZkwxM9CR5ifpApbihqbjElaCWiGsaVYSMacDWPWRFxEE5yyYQKUcsCzQK9mEh4FuEJASo1o2RLI2QyQwNW8jpsxyZNwIrWoLpB7DbRIzQSjckE7oR9DUB+BZwYCxtskEi6Ca6PI1Y3tDg2FzGGDkyssmhgjYvYKKuvYsMt8D4kLUc1QWyQoYhl3AbgFvESaCSugRNnuITIo5YOAYnwxjWTkcTYI8kfgl5xuhnAOP3H87gyyRPRGVaDcmiQsEbNDY5u+Bo0lK9xTolwlAzRHZMZaTtc2oOUNhtOgetIkzgTpd8D5rofQg0ufcNWTmNzSyc3GrXHkJMryE1F2hvGLWxBsmnwyzT3Cb4+RJn3hD+DILx98ik7KeBPaHAsxM+CKyn5Y00i4NpIpvEObGqXGgcXZFjJj67rSLCzEF/wZPwvNcPzR6JIbj3xHUaxKxUByZE+osERhrMDuNCsSbIcDVEpE+1MnsiE6sSNRFd4I3ZCdohyWJLs3g3Y29xsSZDEpYorQ0OeWKTyJRd3gc+g47CGhwQ3dFy5JqxvMluPRsJaM3hsrocEDS5JwN1GpRcwExpMcLpjnqLuGzKE9WLrDLldDJ7icsyKJIhAu9S+CdRDXQhqfLZEoXRkW4FqhclqZDloEsxfgjGPJZZQ+TqOclhSF6uJ67yLR27hz6hT9SCQnI2t3bLkWinwhMIbDNLGGjRoPT2Dgk2hmS43kUl1OEN1rR9OB6i+TMh6RfXDaSLkkwpBqGJWG8ohm9PlEG8L6Im5md0NGcshLJdfCIsjobwpaGUYJuW64NKXwMjALBYEr/obgQ22kMqeoFMFJM34HgGWp7ZBO1ukQubW7HdMvQU1vNNwjZIi9/mkkkiZJCehHpyfhearH5mkxwlDkOitzyKeWby9lpE4ktlzCG2y6Q3YtpkwwzlS10UyWAlDd4RMsEugxLlooakG1OwNwW4hBHkUNqLUJm7ISRccXaglGAw5bHKLUEGQ4ZwG6gkMU6lyWNo7h3REOxMkzkOWDEXIcrUbaCVl1UmWpcvRLEGUEZCVwkZCwN9F8dpceQ47Md7E4HMi0WpSxM9Uhqt2fQ9RQRChgC1dpIruHkKWq+yEBdiEmbk4LHXIMJpsbT2AupNXJ/NiDy5MgD9g0au2yVFoLocFmNsCRrK5GTZi4RCz9s2P2Ds5djwcSXXmRp5mwu/glyfuWezscF4fYssJQfsFiT5wMqYhpgpc2flE9Wi9IcvIdEC/jJM7m+xDB4G2YlexUXKSVjYiL1J4JyJItvzEl8eh3yb79E0SWIVEOr9GD9GvpearFV+N7gneRtMaJguLUNtYopPIaxQtA2JiXVjTmgsxsDubG2WclxDnJyGMAtsSBO8IkJtWNQ8mUHtiRaDngWuGJZGCTLocssQzJDOkhKM0bgyWPI4iQloMVmQE5Vh2EMEqhSGkTTcp3jWCIN7xAlGZQmCKKYIcMS2CC4TPDLgpsahPVMWZFq4tKE00jkWw3XbAkWgIV7J/1C7snBhbxqPSxaQMCYRE5XsEENy3NBMOzVGrsJ6xFgJppljlimsOCLcw+TIFgXQ3cl/AaankU1h6Q01wJgaS5JfpCsYkawuz+GEI8Dlk3MJF4gXDJmcwiRasgswhbE0MCCOUh8JW6Er5Y5HZkFsEZdJMs6bkqhYJK+UMXLakpls2TsLbl+/xSySORKYx1yfhdViq/HEokXRdiYEJulCGXriMlKihkgk1LqDhCJTRCmWipclC1CMlNCzCoTrDGxpujo2DiIlgxiUQQMaJUs2RqSEmaNDljTGL2Wakilub0twhaCg4dCS0TDUDRhDuiVDkT2ZAlEhjYuzREGizBDnLhKoDbaUxbINXILTYlUhEGOSWbLfGCU/cII/vY1bBZbRfGOKyDRqBlkj9mFm7QbjPg/ZRgwdC2hyXUxZCUosE52GRMAerJ+5Fi/kWdjtGeYtzQsndXEjqkJ8WNDdBqODJJvdboe8qwg7tB3oWzhwJL1hqwxuJ6Zic4aXgTLCTwZXv5G1pfRJk1PUTkKeAsfPe9j2fAsDf4Hj8celg/wvNdPzQEKCAcQ4HfgbEnqMpWzgMqdSUEgmEyHUgIZZoS0RJ0RZY0tMIItIaC5A0miRJsTxk5iZkSlGyETUbTcdxQqWRRaXicmRDQl0wE0kxFzE6GrIS4lJFGRDRBZj1jmQ4HcDbVCVocSQ2LkMUMQXDaSPJlyhtGSeiqSRIFAbka5IRwpMrVvJFv9EOpSbITKSIKzCaiyZoENlxswRhWg3pGSO5DXU0J6BOrogwGsXQzq7JkOwQJqRN3bEuGpW4m1WDd5WCEG79ENz5G0+CTeXkQiSccHX4YkWrdCnhLyNQogRspGVYLsty34ISGwiYES4QJAmWCeqTJOCDw0NNZVInSiyJJE/gRHrePRr+BY/M3G9KQcBOsiQNSxsMIiHQnEBTYkgIIS4JD5CWRBYMOhN2o3Mciea2AhjtHJiZBDJMbgmGHYlLSzIFMENoznD3gmBM0OE2dUcqEUxCwYdpEyQjNjsG2lETBlDZXExbuXCGUXEoQkFFF1LgMyeBSyhu9xidi4abMyCCzIBdsS0JhOhbjciUDRBRgFgCVlMaad5gVLEBoIEuyCWGmicQJ2gOZqw2T5IV5FehskEbXUuBWRIlG42kroQ1xdpYt6sNTyvIrNZ4I1hIdvLCSMORPRuWO8pD3j2Y7tZwR5IrNS1E2sMmspMf5SC6olD9Dx6NaP1L8ypArDSORIJFuSEGHBE7BAh1ICMjXBaPmS3HbikMNiWTSCWJksSlQjO9NmwjQgQCpNLCwlPQahoQtNsB7RshOsI6BtwPYMJ7jKIQuVGLGNQnF9LC2WwCRBL3GLeiFVFvgJvKhgw6DTB66GS1wOeiWIdmQOUJ0OwSvNDAmWBLCTYWnZCviJH2YFzdI7ANv8mWLk7zQnoYbeoskyXO48jcEsUzJhMisqhWz2LtLkxlqLckUlqBvbib7PJ1LhCeRuWOwE8CXCZd1mCePRHrR2JOQ5Itv+CSRMsNDXoePyL85MxglNILDgNhJ6kdSwQugeJpLi6uN2OSWKYIbExBAaEBVhIRHINIsZYgwGrIPUYZRY7k9xbwjeNIjJZKtIpielTHcZLkQbYnQhjJiKDIgNSNWvSgyWhBRFMtFuoHbBIyKy5HUlRlDkhCXGBLE2agnUoa8MsciqMcxbryVaBNlpRdRe4ElDjp0JYibgbmLaRKJJJA9S2SNDk0LNktkIeWGl2uN5TDMJRY4FL6gmzMiNCR/hkkkRAj0yTSSfxSSTR4/IqP8kIlSG0nQy3pMnRTMjYhyMk6FgbRKGDWSBZTJksbblvozOAsltBs/R5EiZJZRZUTCEogaIJIJE2WUZMjQgriEegwIDWwm6kxiVFmN2FckhG26YnjNR3wRDFkRBAmjc5InItyNyiIQO4kTq0mQzgdomyZXYperEaeTIprDMYG6IbqPYJOWy2glqLTZNia9HYk4l0J64IFBuR+keSskQZE6jZDr4H6J9MVj0yIn8Eelj/GqP8l9FOlLY2pijaEIgS0WiaW9LlSRuiAZRYkmsslRPqmkkkiUjsSJ0K5LGGiJJ+mTad6DmITuZHJBEMcS0OomQlBLLTiSyVR0STE5VDIw+YY1MiAlRriJJkK5E5XqiG84EluNMBPdAyO9xPqNlbrU3QPcWbtcW2FuPgLYbluOQZ+gBJ0khbQNhiG4JJJpJajouTWPTPrgj1yTWawRRjz+NUf5JgiQI1ExsdqiRCAzmqSaJJpNJLsTBE0TSTQ/xkSO9CQaUJMUooxJKg0DkqWQriVZsxBM1BQ8kA5YoCORbiIZdkFyWw2EwghIe9EU6ZPkkKyPgGQsaL0Dz6GGuIiDHRBBqY0GxyFbYbCDSuzCUvnF93C4JHLlvkiNF6mxwNCYfHqmK4JralqSTS1IXRHn0RWSfTNEqjHn/wBLqmUHWOhJJPpJJJJJpDYtINZNwSGUK7WxiJobDTIZekepUmrqeqrBzYkqRI3LBOSBMURSyImQOQnK40yqyJISwlNkiU8nQrjusKsZCVix0YiFGJiZIHDIJEKL4NZemBikIbil5GLOjsJ3L0YXYZ0LwXK7sgsKDzISdEp7McF6SSNlyCC/pc0mskk0mkUgisk1g7ENE0hEeifQiR5/GvzT6H6p9M+iGJg0gFxECmBg3HSkmiaE2xmgk0G+ggiBEiMQ0kkn1TSaG4JkkhBPQbTGyRie5A5RJkVYhDiRDbkUMd4xLltW4JCkeSWTJCiSirkQ0xCLFhbMjfpeQhuQQ7BeTsWiLBBq8o6YnWUPUm8iFHTGRSaYE0sR6orPo8l0TJJFJJZNZLVhUR6IrFcn41R/iX/ghkxOKVFKhAiquZeTWGJgmkQvHAIVG60KTA5plRcOY3Xpn0TROBuSYJJFYOhiUOZEYxCZFw0EoiR2wo5EtFyHId47DZcNjqlwdaIdGITTwJF4JTEkZcEE70JGO7KGISshBxLKUZTNmR8BjgEUkk1kQszgXHFYo7lxDtr6JaOaLtYIMHJFqySTSSaQ6wR6Irk/xr/wyST6YpRQKIIgKJgRRYkkkUvFcOolCQQl+gzYY1o3DoKDg00TUmnRaikfgXommKpC4bExBOqKQixEMDDEhiyjJBAOriWGrUTonFFRAMJ7Dc3JuNSUOuZISIJYnQtxB6jkNRkuvQtSI4LoVE0iktUSw6JpFXSeDxWC6E2tyX0g4OS60JpBBCJUmiUW3rHogyfjX/gh0EwRJhU7aiRMEFZ0LZiA9iKyRiUaBR0QbgkJhCDqhihFbi2M9M1I1H/hTEKBKY0NKoqiw7oETLAxGxqBh1QpKh1dUOTHsIlDHGRTFwHQhYU6LUMIToi7INNQ2JgdJHcYTHakk0apLRfkhPDHD1RSBMhMaRFEMSiTSCNmXQmQXJLUisk1imeuv4FR/iVJ+hSgIBYd4pDGvQcioaPQRQhJBsdohoyUMwOiK2UI3DomNUkBDE0TgyOH/hTGJwXImGK6GiaKokEiHgiAt67qwg6IkwIaBciSK6N0moGGiBAnUTVUQRs6ITyO8RzJTIGvVJZjcEkliCKSIao6frgujI1AiHSCCWSnoRyXRJBH4YMtdfwLH5mDE0NVDMlVKgyJdBqhAmKlVBSEsMToqsmhJGh2GJEFQYnFRDppITGhWHdDRPrVENeqaNcZAMISSO5GaHEIECkNah+m8kEVQhDg1dA0iUWNBkATVDq1WZZiRJIipCYgNqCZI/BikUmkVkSuvTFIJOqL1ismSPRYggj1zX8C/Iq0Fcvpb0k4cIDsW1S4uL1DfpFqUXqKkkipUBxjIpIgpDLKKDpqlgTohoa/CmTI1+BOk2qmKhpQ8CW1JqIJRDUX0yJkArgDIzSHcLKkerDSCRRYxrFbBCUNocjcEwaWhBPpgliY6zSKyJbggkkggiiZkuqJIILkiZYgaZJNI9Wf4F+RUlX7CBKYlQbIboyFUNwlGpHAbJHJtUqTQiqV4Ykn0JkjJFQiEboxN6MT8KZEog9aZJPoYVywSY0qbkg9FUEI9KGLFNgTCxjuHZigWQahiECdhoUqjrIg7j2UEbyzqn0RWxJPqkmSnSaRVJZl0JkiZCohomiJoiqQn4xeh/gVIUYd0JQvXEsTRdSBbehTtUmMMSJiKkZDqkmqdGhMTJJBoVh0GZGo9arXD9cUkmiMF5bQnsQ7hzFkaohO5MqjdZqgdxIc0LkIzomaDGIsmrGaRRGFJJJJkaDTQgqUEEUkyP8ADAnEiiUzgRWFRczSRMTpCIkqwX2GU/kS9D/FJNE/QSJidEIFYbGxBFGRaNQ3RjrIqIqfpXoJiZciJjEYFdGGXL1qiY1J+qfTIw1DpHBg9hHNKDVcBoaIHRUTo8M0RoSqEG3IlO4iyqZIogkkSRBckkmRoihUGQQR+CCDBM1kmiz9KDFIoqCYiERZAgLQGyGge34tXof4pJomOhFExMQbG6tUkTE6GIkYTo6OiCpEkYxelMdSZIkj9BdRPWqMK6Eo/U/Q6WCS8KSMNSJSS9keCCIH6hdMCckqGo9GAyGhA4UUCzGmTSSSSaTWKkLEeqCKQSST6JJJLvRBBBPoTExMQiOA3BCDNoLU/wABf+ATE6mMTJEE5GMKh0TEGxioxE0ikUmlP4CqNUTHdC3GJ0uQ8jUofqVXEo/XHokTsTcvkDkNkwMOjQyNchUtehUIEiNItShu1IIIGBcTRDVDhjUE1gh0j1SISiCCCKRSaQR6IIpImIT6II9CqXEjDLDz3fgXof4pJJEE6GOjYnQYbExMY6ST601dJig0ifgTog1VB1ahC/hQrqg/SqP0piErDsLcdhsmqE4RdIEA81TENFiwFgtdFrKGNdCDYho1pGFssXo0hqizME1Nkv1opNEkeiKR+CCKTQmJltyKQIQhCdGxhsf3vwSTV/majQyRujDGSMSP0r0OioxjCoMieqRMTGMit0VMowzD1p1ciUL6V+Cad+Kx+lMRERESH6XLMouVhIEptQxh0YnA01BsmB3GoJJq6ySSyaT6VUikEeifTNIqmIL0CQqJ0YxGr8lkn8X/2gAMAwEAAgADAAAAEHJa1fS0biO/MhIA6FKVQZZiaYzn/n4G3fXcQ0dbQHW4mrmo1eBN19G0FW2+nEDF5voII8DPFyBqPpvrxln2OOmrqkWNg9SKKcPQOkmJO6wuOJkb0D5/F686vsvVWdlX785qh02VXjVAPED3B8dXIOGpougnkuIXvDDPLAFPfzqOvsrrq3YTaCOF6yL24++GMHTpwqHGPAjE2MJzhqKEsymldFxBnEh6TuIQ8lXZLfQ/3CgRbCVWiQkz8Q91xzy8kxzEEKh/9to/iQ8LRJOhMDOPXbtyaZqhv3qwU/GA0EPKL/4BAh2nCGIOybv95lgk6x90PEdS41U7KMANOIoNLCGMNDDCEjMcNi07CJEv/PFv29iFAov1TrIqhS2sH109yiV/XceyyoQob18xbgLJETzTxrQ99/xhao4wotnvghPPBDIluFluZv387RSUcaTdSPqm97FGqeUmRXN2TzuzT9kDT7WI5Z9m2k0YTwMvSRy4bPnr1GHT6Jekpfyqb3GilggrjigjqihGTTPOKClqVs861YffSZeTZQPu40yLAanCX1MdSPKIQEolwxygsMVCw5Y3jMhspFIDvJPMPKMMDDQTGYaqPHtkvvorTUAAjycccccXPa1IgRVd6/y0ZXQSGZUtry7JGJzyknQrzHu3iRuviWO2KovYa+RtB87ggkgsGsOtsIEAw1LSkXv0Oljv28RSScccQQQQQQQUuQbOpcLA/wB/7Kc857bkwhavcrpPOs9pygqk8G/eq15KsnbcffhiDU11DM7/AOuuCCG8oEp7JK/6KD0rS/H51988BAIABRI09gStpBrKXDkcIBwMsssK+vpQuT/KWLV/9JA75hx7SDo14rd8jxvs+JHuKDfMLPDDyf8AkvLG3Mj6oqU6IH83AEf4xRCxx+umoPIHeHKQG8MIwu1cKhjr9VKlQNAN7zYMCDihvdPRVyKLK0McSEiFL1/Wt8JaIKgLwz/8sCMYQLskj/VPIIWEDm7mjU5kint6n28xF2zN5Y4zNHYABiNfYrZgtSUUu5LEsc5gENDpSqn1KA9MJKmBLO1ubRqwRZwRzSov4vIHQSjJN1aPATLG4wEpdhfNl/UhFRKDu+N4C+gm88Tfdv1PAh1PKr7aBdCiUGnJmPvcnPTq/e5oKzoIs+5z4B8ytT+geWPhMCMO2wfgJw3DSwE3sMffs1JMUUcJB8btndt/C/jtp34Avfk7DSesZTsmWETjmu6N1an7SSDSN+1sSq7Pgsov+2ZUUNOBqh3/AOuuZPMwNBuYd+s9aoof3qE0gxpZPZXFjmYujFbar0idjfEy045FH+ZW1bcGUJudz+UNHZdQeqX2nAPf3OPk8JtcBhA57qxg38v/AHnefAQnZTmLcxUNhoWGLseisTQqmzY7GlrUZqZ8wWQvMMjZ+MBBqTJvByrmMOYmYGO4hJdrUJPB3sWjiExa3KK/PjHHW6Se+dqlI0+T5T8XPDnYagZhc1/tCm2O3tjE5LajSwsHwkD81GyacWNAlCnw8Uu+wqntoV1Wxgk+wIdJNpG4OWETxwhQ88MPQYWun99FkE1I9FCnlYrAIgXzD2pJUFyFrJ/rU2xm5ecsUHmaL3pzi++A1dKIEMEOPIC5VPx63t+DkKvndQx6zke8qSuk9D6CW74Adge+pLx8+cqul6ksS80SZ2XR7Ym9yRSPOInRCVhrM79KlV7Eo52/441MZmLstTUDCDraKLpOjB4SqSPHDImCnrGRd/8AUaHPBIJeqT54tkpDWF6MPdDbrjjJbl90+pOfAGV5stF7yTCfFUCKNxN2DIg+KLXOLoZm2p8hISK8PFWy6l846J7ou2AoObKLMPfPfAZ6st00qyqKVYCWmio7pJdBjDwVYE5YBiZjdX816umwQsYcUae+B0dD41R7zH98bzhnTpMQAeBsoLg1MBS8Kn2y5eQV6h7jpsnye7/8t/55R3fA6Q3fA3I/ONas01Qm8NGrQDBHxvDxvC9pxqqtG3b8m2Zp+cs2W2deEp/dKv2N6nKqHZMDM+uBqvppzBYd1JGLWdh//e44XB4LvFPfVVxwy5umNfu32KqAgwgVsxoYhfXA4wVswKhAOuSbfzsIyXdl7MsxV23Ja3p0MDv3AgDmohhrkzLNLYj+PoTZ1oSBp5twY+GmqNXD01ogprc3uNpUsNs9jhRpM4na/wBHlTMnlgg4woUa4QiYKMO4GqHz91BjzBAKr3FTLUGQX+bIp4K/+nNtxvoOhdRZbHRXhPMNLFXNie8QJ9uytPw02aP9sHXl7GjXFuBEpOjK17d7LFOtfJYU4hUVYg80UFAPlMJvxKf81TijCzcMPwfJk3mMXCn43pYvc/xHc4wBpkwV8+xnbRbuIVzk05S3GrFQdENHqlnIe5NX5NhcWdqQqt0MKVTUT5g2f2jHLl9dIas0fmw8BzqaSttec28g+AAyglJJRzzTO4QIqRky8lMqfKrYYm7wl8lUM85IGRM11kagGv8Aa92Al7fbH9Jcy+LWQx/oH982BJ6s4vqsOZUH/vTmzYT9o/Dj1oBfaZZxtFKL0m4lNxYZGcCAjhjF0wPfZEjHJrKwqJR93ldaCaIgIbk+VdaymLmSJdH5pU8KIGDSoz8r2BRvOzNpL08xsQSUOC0vSCR9zPq+ijxgAww7HHmHcDjTXNSqpM8jOSvJKBVJZyJUkAyQNpE/IkEBt7FHI26uD6aAZct/wwmWOb8fmSQ4KoutcXQSogAf6/jq2TV8jqI0eiw+b+qXfeTeZu1KdVrU5FQ85fs79EnwvocllnwMttCfNaSabtKHsndZ1OQ+yoguZHjwMn7M14PtCsS0/Dt5Fyk8funsbpoLJv7SWRB/tS5bHXvkNU87LXIQ8GNKllXtiQR3WdWWcdyRpiDlyGunedGhqvhYTVGjvWXC9cgJ4+9lezRbXkH/AH2qA8U88DDIHJi3vem59igwAD5K3Cgeoe29Df8AlPhYmaNfQsN2SvrfEE4zRGsQ1+yV3i6cefT1zNl8jnpit6PtYm9N/KtNsTwbSV89AOejhkTL2EniJvAicxl3J+s4D0mri1WD7oS6JBHRDgzYGub8nXxS7zn6trMKWopKoACunLhlfebxUR3AF3bwC6mnugzsQ/8A+UJfczqhzon2mmxJ0WNlpWUGMMc0uc24qoDkd5cXHNdQ7DDzKeJx6TgKqLd5rKQl2CfhA46pzOwKQM9jGVA2nV1hL3jYBJHO7cmkEiULs/os7jzQmUu7mwhds1BlAHzJux4QmMFLghX1YfxJepDpWB2Q09MyJ3xRRbCHkWD/ANoZg2pgDfFvUaLiitD1jwSIGw0FDCFKWJlFiF286vQGsarryiSRgdh3zIVQbX557VRHygsFY/2xUdmrevxmxu3jp5WUi1ETFeruKmsv07R5PxMqdSnFvYWnK4IETKoRvZh/UKuD7fVGWTy0Po6MDWLrCCJV9rd9z05H2ritoTX6h5Jc7wEHeMUW3djfS7vQqr78PakWMXWByNxrGSFShcRjE6J58AqgUpyxT7Y8PC9M0V4iGFof/RUYTNsdoHiJTmYyfKcQya0ZripXiuccCP8A6KMJRamowgu7l7iybD2DjqJL830Btegwtxz0kMAcZMQtwRKy81Va+ayKqFm3lrqrwXvkrxGKdkdh+nEa/wD34Oyb8/jlcTgQ9fh9u7DIC81GhTp1S/07nSawJIZH8B6ggoUWSScgwjUrCboO7L0IMb/daczGWEENu/8AH3J0s3X7SWpLlmYJLHvXKhDkzBnv/HhZYIiGxLawRB4x3qDQbXYGzqNMIVmf1LtelHLOr7cS7u0NSLprsfCGyXQLmuO2iD5OoFxojyt4c53ZodVSo2go1O9yGLHG9WxDv/6CWe16BteguQg0jnWEhXUHaYW6ePyZm3NwCBmI7krsmb2Xl0bciLGDi3/C5d1okp0APZW1BHI3LfTO0r1Sk418oprYVb8CgrTkpA5MdT3iovacqiq3wJP+aE+YS7dEuR7ubbZchENYd08khgWDmv76ZA1LL0dPBEF7NUs/NsODaqfj7giIIpjnt2mpD2Br8BF8Xi160uMjGHnllWpHUXnmIol0AI0UvqJxoCBGwe/sKWhTxOzFlakUrVsXKF6ljMfZ9zYSKRfD0r8sjQuoYmabdeuX8BwEvlWrUFgnTlSlw9mZ8WkljQrioQJjWP7NAAIzG4rtCPolvjy3YVZ4PxfkP+C8l7PHacVYoy3d+Rq0MvRquRgAapfeaR5PUgwP8oUGiL5+3wJMkvjAYxHvvrufAj9M9T8sTEFHaEVejG0YKeZy+LYvEhxbE+seohcJN+BVnPSVvhUnmllgvRkuYgdXhbJY07YDv0o30Xj8TKVqTRukYaKAvtB7ah3UMjUc24JqP+4eH0cFWcXaXsfuE6rK2x9SgfhKO7VkQG7kVWMgLIqurVuqCyRVlbeezpILxzkZHUYgsPBVAWyCx2fLvijtGSPHPVqNQeKDIhQtmTVmpILid5Sw31I++EfFOkQnEqd5VW5f29sNVZuy+f6vEVVVmbLqU0KNsfsVBZN7Ak5MPZGzMvVXeGy3feiRWq3SJ70xoyCnsYitMA+r0M6m2wqEd3RKLeA8hIYPanmY0MDPvv8A/PXcrSs2GqGAXkwdAR5P/wAsz7nMwTjoPyLAEgnxtfzJ9PzF2XR4F0ENCRrzgs6H1Y2Hk151k057ZIfI4eq1RqQUFbJn28/3/XoeL+dmm/udSKrTHLw0n1ondHAbbhQV97KZ/YLvIEHcnYQlWRpX7WYqBEA0sDYtFvDdr8K8ZdqSV+O43JaIr9qDDaoYkdM5/BUqrU+6KW/5SrlJUJPiTSBPh6YRhOgcP1NSShOYRZAQLjwpK1OC+8O4hf6OBw19fWjyKyac+GpleXHr7V05JEWhUevUgSbAjCqODQCqS+j65CeHztIdyYTuUsAlTqcLKOV4U8pyM7w9cIvnghtZ5PhwNJF1PpCURS48cRdREpLUhAfNohrrtUPs8lQDTwBjD8/X65CrCrLqbPDjC+FN4mD9VxNGudFh11DsbDf4sHYgSsSERpekYsrJlR6TyJXT8lRI4i/1JIOFG/w5XeJtLYiZKL7Wl4J0DsrPyqWj/rq6SiVtDMi8BNyunROu1ZDXQQcgygXG8/ToHADIp4HA03ePDakIH+QMhjNt+TnNT9vZ6TwiahMuV/HA0jEDQs6dD83pA2KX7jUuAMwpD7W5c+Bo7Eg/4rGdsHNt2ZYzbQ8BMOE+HhtOVtZbvDdKtk/aa4dFbAXj1uqUeRKOhdosqWlw6DkfRokUDs7T8WrfjWsCi6KUogzKnQ777OMJp9+eKGmxB5Vdh4n7kkocCL0dQeyXfGTx2Tku0lg2bNhFMy0Q71L21JBtuG19SKd6YOB4P8qrc+rfjs1DrCoJ3+ymrtgka4gFH1+AJ1ZpaKLs+PIx3mUtekERGX57sTWPYfvliCXVimzwd+SN3BhtslsBtwL+1VaP4Fwv/wDFKtP714/A3/YZVowQzxFeh+7LyxqKenaEQohq7VlSb1HckWME/kfSX4bOP9sB/wA4LCjGUSUp7nWjTYXH2KUe3QBbzf8Ael5j7SO8crOXuUD/AA2uCSv9BG2APr3OFWltgDKjsqpxS7sWfTmAXdWqwDv1aDsaQ2bQXInKdJ1WPcf30bzdbijRV1kmVqXH91AOBa6PFPa70vlA9+4CzEFpr+cihyWC8B4GGBYwp7gQt2qtrbgbsRpqR/DdxrisVZHzoj+SOmcMBdjpNhJdskgbxssnTKM4IxD1OYoMoB717vgA9gdCDGBIA7Lcjym4VfJ2ipfHs4X6armnFVbvWrql+WWknleUTROcDzae0tSkZLNiB37mbUeRmXemia882g+0/lj+hHlV9FgSyLRxMoqjd2qPBUsZGXIn/MA8DURV5Fiv6idLoSp7qhroYWeUujv+U99hf02iDZJBfgfiXFouT+qUbfuLj79qSeK1FPksqXKb9GnY6sw3OP6QPguF1D1aWxxR4yFN5v8A28Vjl741DOZXdF3akHVKi2i8utvr97v3AIEnKZ31XxBXv58GZoVhqMIqUor4YKnSkPyjRycMcwwqCA98uidvfCmyQ95M880rHFpZxJGEPk+5M2K93Xoqvm/KIciM3sqCLwT6psPMI93ys6SfiHo1I8OI/wC/tzirUlDc/8QAKhEBAQEAAgIBAwMFAQEBAQAAAQARITEQQVEgYXGBofAwkbHB0UDh8VD/2gAIAQMBAT8QFLcGA/Ttvhp5yyzxnjLLPBCL774vHVrZZ9eWWWedtLbbm0+ObH9DZBNIleppT39Jct2rfoG2+MjysLIs8ha+L0l2z9PVuIF+rVi08mrPGWWWRCM+yN8ZZZZZZZYWlp4a3NnhhYedtt8bbJPc1+EvwKv9Qz6MgsssiPGPkDylAWHlveT1l/ixheyBBfdv0iIXuDCPXnLPiAj5FhsP0TLez7XBtkeRweLHxbtbGyzztnxZt24344s2/Ap9/Xln9eI+K17sfNiCMkTfJws3q+60e7+H82B0XKJKZT4TZpNo6sI+UCA/RkKQoHuC+/OF9kIvuLawbksPct8PgLnb9+OfJL3NI9Ev48Gvn+pln/i9vKPVw7jhxC+o10w15lcoabZ9s850/HkbOpTvxCHB8Gzsca0bB46nzttv0hp1aIgYm+MuoCPkQkc9WWG+2YAOkE4JL3No9Er0TC3v/wAB/wCb2iyUaOTI5D7QzcZHxcYWkjiTMLdebUFlTcXIDbnUuT4mt16Z7h8/6ulDgun9XLIW3EPAZfZaID3COyPdBZiLZz+nln/8D3ie47MPFgh3ZiYuZINwzMmXG2eGfN2RywxBHazl/Euci4H8xgfzq4hel0ssss/riIp90D3bSHpun6XBtS745sss/oZ5z6H/ANOPAs1nuwZmRvi9OXH6b9xPjBTZCH7TAJ94eJOH8XZ4dn5jOsXUuLbbf/DLLLHk/wALvPfg/wDGx/6I+J5s+GbBt8IeZb/ZDt9/9eWax6ftcJ6vX6R7XzshhF7tDmEmWehJpln0bb/X79PS9Z7iP/G/08/q26eJ8N72MLECuF/on+7/AF5DWYBn1ZGLP3WPVtscw3qT3afPjPGWed/p946+t0PAR9G22xr1a+IUND9vjwvf0sR/Ryz+pbp4hsu7tGx93TE+gjTMhEL0SnC352fLx+xZ+Lfr/F96U9wtp685Z5yyz+l3jr63Rdjwe/IPcH4vwsD3/q09thZOrfxfY8aV7e36XuIPpz68/py4l5l48HnIR6gkXGNEDx7mci7DGtjX0uEeDEd+Ms8tn9TvHVv09vHseD357W3ufGeA21mxOXcAPJ7fpYj698H9T3u10m9eBKsL25KO5cM6NsGwmqMLZWTH8eOF+8KEl6WLzLKbbJZZ9GWf0e8dfUePYvcdPkcnjPAfq5eYAjHUKS5Ke1n0MR9AnJ4iPvs+26BZ9Gec+j3u10m9SP0Ixcnmj3Kjn9pLym5Qh4XJllo3bZxcfhLhFThvgb70P5j2btv0bbb4z6c+rvHX0Hgidib289jw41GTdnhxHysHwK7JOVn0MR9A+H5vk23u1ZIcPCWWf0Pe7XSe71AQPxcAPCCE1sQ2znuOkuYcJdZPJNe7eX4i1eI54nNhwsS/o7/S7x1Z5PBE7Ew7ssjyT4XFsZxG+ocXyLBEGKe3jL14Yj6M4/n/AFDTwJdqHCyyyzw+M+j38Ok93q/bXIJBrpCJksHOMPhXhcmNHiSw/BbLzPzEDkcsgss85/Tzz2jr6Dy7LseDZZ4C8WobHgSJh7lxt8JN1b2s+h7iPo/3/wBeMWcx3keZlnhLJ+jPHv4dJ7vV+0g5RLmNdIlH4u9l6lzJzFg5E/fc/HaO8kjRgrwTPSFoQfX7LLPOec/oZ4yEdfSeHZdjwPpIEubedvSx5bxLzYaXAYOXxnjJiPoUP1/6uWxbzJhfKPMyyyZ8s+fae4cROmEer1UN0pojiPEnI+HYuTW0Xa+BfCsR3mGOG0g2EvhCZD7jzSzxlnnfOWec8un0EXtdl2IPEeH9tZkEHzASGQrG8SHfUcE4G+CvDExH0f5v9SBgcpBbTYfx+llkkkn1k3S9sjq210J5SFgFWpDg56jHhZjNuTveddzX48Ub3PwkcKcyM5ySRMgBg97s4deEsnbZfGeM8Z9ZdPCeCO72ujdiPEeLfw/ZsxLJF4vcZK8R7MJ7vQ7kw2/EsIuPD4PGWR39f+oCG8rW5pKTkj+evIkklnjPoJ7nwRbg2N5s5PkgyOni6XuxnNGXMwqMOXLpHHPiewW6BI+eW+yPgf7z8X7yvW/3lquyWf088EOIIWRHd7XVuiPEGGw6fZ/bP+yMiA34sBLkrC93KQz416tONyIZxGJPhiIjx/n/ANWniXSUuyPXgCMfATylnkm6l78HzPhLDGaAs3ZZFe5cvDulz/F6pczVyrHTCFi7j17lFkMwbu3x08n1gWFnjLILPAEPBHd1bq3YnxLg/nxcslvHrP30z/dnH4jwFvkz8tj3HwR8P+b7MfBYf/iDpfmO+dXKxMeCI8n9/wDqHJ17uLD1H+H4jwCHgyyfLEy4u2Wu0sMMYAz1k6S5sQRXu7Mczvu/8SzxPJRjswcSBr4ftffHFxDv/CbLPHFpaXFlxJnHllk0ZHgju6t1Z7LgswmPsf8A5Ng+7/iTkIP42yNft/8ALXp/xKnu0+77lo93MORYCfCvcbhsMiWPJEFkP3/68C3d1aI/z1Ez5Xw+GYk5ukjwkh7h+WM0sDM/z9bkkIHDcHmcuZQR2XIQkNaQDGwRrqxGE2Hiz4GNNN/e2Es+LEXTIr9T4yyzwzyUWn0HUSPXfk7Lo3Rnsk4FnwsMATwSb20bPmMb8ba9rb7NkMLm2G7mwPJ8PkRZbVvv33r+Oyv/ANuB/HqGZeR8MzMTczwTSzmBrFOaEHJDeHge43ouLTmYcMfIt+T+98q/vKvbZ8rlOYXpdusDfB2u0wO7VB+PG2w222tsvGRxlvk6ts587Z8NrliR6XZypiSt7RYfEfi/S/SyOI8Y/jknoj4R76fvOnfAfJ4Is2BAkWCT8Q+wlwHP4tDXiGu4/Of9j+v7f9vsv7k/dHRynOzdmYmHD5vNm5za0y4DdAQYz2FsOI2Znn/7b+9sULtSzqG1kl02y17X8/W01W+v5sv5fz9bj7fz9Zfy/wA/WVl/R5yT78EXrwDeXyXaO0ObPtPH9DY+jD4LksdweTwj3DtllkHWS97hNkySSWS8dpW+BmJ7vZL4O9yAsh8OMd5LweMPaN6fiEqg/wAZcvzLgufH5gOIzM/MTbOJ/wC/9lWsssMJ7h8b9KPchlkEHb6XBzLJ0B9Bw1tMHMGw48ZZ4zwzzlnj2hjkk4nwDw3myTj3JA72Z4zj4WiyyLYJx2CEklkcO3Y3WSYmONQKMndQHmYzbkLgFoCWpLmZWeYh/S5b+Jf8bu/Mu5PlAgZ1bGSjZTmWRv8ANkuS8+E0yIm+1sodzzLOvJG4A4Rys8X84j6S5HM8JNie7g2O/A4gsssg8b9YPlY9TdogZZFyxZ5uS7fbP+W5df2/5EYv7f8AJ863+fa1atFlkyfArfmSZ8GvEk2TccfiU4kvcj3J45uTu4N0z5u3ldS5G7Mv+N2z6kEWGZsP58Q+G7Dy/W3e4kddW3KnU3OZugnsSbIcjSLFcLoIcjDduwd3Mrm1Xi67+cSLJEmeCfPh7snqEEknjm1+bX5j5L+WH/L8H9jwHrY+RmEbtFkSHwNiXsOW4vwjvw32xXlbbZhAth2vDbYJyktzC7JaniLGHjpe/Bt7j2WjySLxcgXOdrILRcFH7lxXZclowlccQoPuOQ7/AGgLs/DEw9Lg+6L1lmy8zHhzi/tnglxZBBcDLmni1CJJyEmMacy4J58aj8w5ee1nG3uyHETww1kD2S/C+zL8b+f5sfn/AD9YPk/2/wDsfM/tfzEAcojfm6mzHcQ4TAI9F7y5lhxw5YdxIbxHR/phvL+0A07+uR1v8P0lTEWsf8Foaf6tB5ZD1Bl2bI7duh4OxZA4lvBZQLB9IFvxQ9IR1nOZY9pRyGhvd9yfkswHzOPcjNnkcllcvHHqQ8f4IBkVTLq05d2kpc2PH6ymt72EedgOMT91l2Sx44u7LIHLTIfD1d485A5JtLS4+Yz5g/CfuP7x9iTlHuLqmI6th5sPvEd5DWEd+D5kHkP3L7P+IPskvdmcRCK8kdyrl00T122cbmvD481IcZhA2e7Ot+9sQnUhSjPxHrwZBbqzr7wmLdswK27XTcg9QCwvuSXimBfXhEQcwa8SwrMb1rupDh2Y0gBSGOIHRZ85A9EO+od9P3tTnN+0cd3SOhs7tnzo+78QfMOIxqO7RJ6hwhzu/YXwcRAwX3fafv8A8vd7XtBxdXgdx1Ngck7WTP5/m+wP4P8As7xj9P8A7Af/AA2Dv7VxsoB2v9r4t/uSnp+0fB/tAu/4Mt3+y49wboz9C0+o1tjHHm7eJRjyzWFxvXMFQ48IXdJPN6LmY9QpHxHidCdw2mPb1IA/OTwi1wum9QtvPNnk7uZPZhB6ko56uSe4cMjqRWT1LXp7uUY37kuTbWjPVjyoe5eWH+IZzZHkg6WF0hnOp/VhXbcTas408nJdUOVzPz/uLtjc0lr3cJmc3te0XR4EHErOwBuwYGT5kdQfQ/vaciP6x2vgsqA8AXgPW33/ADx8H7H/ACe5Z8OM+PlsWGfrJFbNHzIxZ9JcS5jJG16bZS97Dv8ANyePR/iTKc/zcb8NoEhFz+UBokpZzHOZy5Ye4hr1cwlzxmKvUHbmS8NkyzL4OyVb7x48AAON2y8qb/OLQZIAQXOert58Dh8YcrD+XsgeFuQYr3DpyTDk/wA/9svqGLe0e46uh5Au8ubobhtuHcVG/wD8Q8NP2sqZfJQEXAdfxH1p4+108bbbM5Zc1EaYHlcyXFY9XEiLqCDLZ0lzMVRWnfuzyn3tH+Cwjkt+Z7+pAKR0becNwKS2MRanIyExFJ47v+YOBBs+JOrRx9wBBLbjtkQsnVztvfNtykOPAM8BWHDdZnvwP4feMHFP8f2Xa+19hcKb2SbhYHJFT1cHSRU3SOroXS7QcQ5nmYyy+5Pz3zZ/afsP7H/JxMyx8W+6/OFQ9Xedhp+8PxfavtMidzLw9E97t5yWeG77twMkbe4wmT3PtLiHmb8UwDYmr8yKz4ILhDl+f+XUlgOYfvL+kFD5cfWQXzbxarWTHGbkulr83/LFXxKcf9/7YnMnBMaoT6gg9kUOGUdbKnln5ht4uNBI+Qf7w9ONz7h+kg8En3y5z+yTOb+1heW/3/5JftP9l+8jScX4/wAJXjPHLgBCnomT8X+7PWQLXi5W/f8AzAI+MgdRPgeRnF3ievLH0Hm38nq6kO4STbN3DOmBc2OWDY8wuvDzwdwl5lsB5sebLVrNsE+y6Q83JCPmfoto85/aNt4h+v3gOCdBkPEKMnfU/oTsHCIy0uBatSxkHLYc+P49RyzN9RziYqZv9v8Adh6P0jCnbjRzHx/YubhgtM/vC5gTi3G3IbkyWAcMfJAekHOJAH5unN+7P8z0X7T/AGXGN0x2+3+F3w8EcUL3uUfz7G/oTpOcjz9+P8wcjl3+f3LMaXa/mMPu5/uO/wCn+46up5A8ePv6GPoEDrP43wEVR5H6xw0+0HJ+tzPw3dKRv86gOc+GHLzfMHE+WvufWRAZe9x2S4t58DYasSYXOIvZmWHXX6weqv0v9iH/ANEVzP1T/Vo6/wByYx+F8pD9lzcfugj/AKWJgf5n4H9pLg/aBJti2aNYS7IYYhmLxdd8Njfi09wrH4uYfBcD83Tc/wAx/m5csJz6P8kWA+S3cJ/J2QKthhjm1sgfkt9Azn9+5pH2576z7ffJOGFOv3/27sqF0yIfn/Nrl+P9zppF1Ju0PE47urfHuHHP0AST5P47uDvaPX+dxwR+1yT8MOX4f8wcrq/nosv0N2+PeUz1dvI8R6W4dQ8Pc9SLUs0n5gCJhU9ylZo6GEKF9ly9Z/cs+F+SQbyw9c2jCSi+RzcFtpYlH2YCe8h5Y8rmCT7EubgIeq06me3L4pkHBN6iGaxBjmDH+6f5ssg73AEH2Tptuq2rRimmXD87+T/Gy+W/Vf60jncf7n+oIf5ZP7kIVk0fiHNuGBs3eXEoOZ8seDx0WOP47hqXZA7g0X7wIf3uy/Z/zI1aJ/L/AKv9H/MMfj2l1sPch9z98M8FpcYcwb1HCMvHheGY4sZF/OJJZ+4lqsR727VyQfTZ+4PmfPuSfQPDa1+GyKzBj4g4u3kOG15bBwWvm3bbbbbDbFXT7f4J433P82Sx/j+f8kgfeybBkNC000hjauqWV5L+81w/b/5DPUjWSJxn62HH7G6dMv0GO82n+F9h/taTD4LG6b0/ju9D+c3ZLnft/uHDen62Uf1/1dj+JYfy/wCpcfgw8OBsdECe4T1I3JG6KTz7J+yQc5PVnM236cSoPdpFZOYm0FxflcemPg/vZ8LU9TqW39zySSCSG/zmxLRMdS6b3dy9xwt+ibbbbbbYOYHdy36bIzLQAjSF2SLc4+5lylef96x5kviGE/aQ0Ecsr0llx+0uLtdJsWShj5o0vXfcfsf8vs/5/wCx/B/+R8H+f3nfn/MrDA5vxn7yN5ab3+aWMfi26LPX5u38v3C7L+L0/P8Ay6/g38P7+HimK2Xm3ibTs9WETfTLBv6Rr/ya4fz+fmY+aC+Tv6yJhxP2uTEoFiWvhtxOWsMtgAfoPYzyflP8StLDkXAEuP1h5vSTJcS+dLHjqN9+MgnSAR6o/Jc+4z1JyZfCEaxTq018WEfpDwjh0hXzXxy8iiO5ilt2reZSXnLm0e/AB6vvLTuMYM9my3SHt+YUAP7fpcBxnEk6vHAF7Xae71c0Swjolhk88vgvTwfAzph9K9l+xAYC1/62nsW3Wf0ten/EL4f1JD1LJL1KXDwXqGojmHywGz2z3HiOmH34jbktbmyw8jWJ3aFp4O8n42ujyZawZXcu4rUGTV5M9sNmO8IjUo6/x/yH03xMhPx2/Z49/F87PrzwEPyhwUrtHLO67Pc9+b6lyXT8bv8AgXr9JT5PqJhS+7G2nsvtEsjyFpl1wNZ7LucOkM2xeojftse3wY9W+C0tbbfGthxtr5t2rtF2w22x5DuUf/2Ogxju2z5IPtCEqWQkT9HMfBqyyzx2ht8EeZ8zT1a9kp0/z95+Le1Lm9bv+EuX8R0n63qPB9BRwkfMt+02F1kzk9j9sQbdrLq4IpTbb5fGEh6+p7+o16hPVvhq7SrxODiVzOf9WncY7maWfeSwk+GvDPGLP0xiJqfoDvageG8wr3lD1dmRcfFvSX6CfJ4Po+xC9ZC9sAdtiluNgnSxPvbtJhrMoZ34LZz42225tXUs9fVjOY+X+I/LA+v8R35xEQsz/CQak9+eqPUXN4L7Mvrh+scDZPhAGZcuctPq+yPmSI+bl0yrmW0uLm/Swsv0jLCyZk3b5ZzF1l18CnhrqY8nkjwT51c+4T6j4oz3AXCEdWJH2X2pWUn2JM1kh5m4wNuA9yxHxOZ9XQzbX4tRGjrwae1j7p+khF8Ib7jU7semeJtwWF5tPUF5gO5WcIRy3bbbzl32WGz8yvVoubLLmwsWLmUNElhY+LF1cmx/oe/DHhifKrRlm2XpatNz4NWFhAeByE+JB7gOol1vlmSJ7hXiR8rg0/1E4OPq6Wtrx151WWWMObqXbcfK7uHu0zllLDqN9Fq9FkdQveQtsbySJB8yehgU5uvV8S/C0PVq6m5JZZAxEnHS+4ts+9krtcQeD9I9z4ImJ85EjjNge74FqWrB5My4nLfoBz1D5jDqQ9+L57L83TMtwvqL37bXzYdeBE4t88WSNkbKmw87jaOMjkSPVjhGOMsO9nYuPuXuXfdp7t+24c7AoPvabzZ6256SekKOLa/KOXGdPcx9VqW9SZHghZcVx9X4R9rm1t+k+DqJifP3YHu+RlPdvDNHcTfcwYViTw6hyPttJD02lx8WXEF7kerD2xkIvgsei5+H2r7civtbR1AnEuOYDLHHRc+r47KHqFuha8Zcn2k+Vq2mXsWHlbOhake2WDIdLDlnnGuy4ekeyXrw5y9ix8WOpzehGPd9ty6bXxJxClpYPgln02Y6iYnzttseINrdFOxQEZ4ywsHuSmkeifhbbfpmF3NjC7tbmxsbUDAxQDuzA7te4WZGHq5df6sO417tuNkerR7tzq0ZOOGCHZcnhhbUerRYwRo8Nlguy79WrgtDmWnDIZxDjiw31dEjufgwty9wYdSicR+Z5Tq5SnqBvc4ObdW2y5+h8ngnyETPGpAgs5gZEkn7Zcr5lW7VsCwmHfe+Dhb6R9vGj1axZ4YW3iUWDY+bnYO4EadQj9p1zA9TPVrIQ5LhzAhO4+yddFieoLuE92ehnDYXuC4vkYD0xr3OhzZ9zrlgs14Y5xn3Knc4XXIfaeXMH1dT8fH2We7JDwGP0Pj1ExPnB4sSZf0bl4U2rfuz8+APghT1K8BL77HzANghmD1Pxtpza2ofgvxa22wvgTNo9XwbCNwyerFyXvDULJ4Ya2lnTI6nYZ92wZI92nhnHJYQGIokb5sEaZcs57bpJDu+Hcvwyx9tktxZHjPHY+h8EeCfOvjm0wr77C48cfDfHNzb41tWNr3ZPjdtzxuWsL5d+LRuLhn4XJZvJakLcPDO+ETd4bUPbIdNhTWB4ILuOWJbyJOIHSWcWmd2twbPyuPZt8KQdNg8XA5bgw72WHzLkLyy/KwWvqBDa2+PT6H6T6OFpcbUq1a2mF5QC0k2LNh6lZXgXbLLW5s8Db4NW/HdsufHDHw8m7RJ6vQwxjiewnhp3KfMqdQM6e7DrI6ss+m1HuQ99wwYfe+9b92nqU8lxm5c2sIhzw0uLZ+tPHp9D4PJ9GQvEFnjiyeXla+MfDLA93Vh7sLiEIB6j4L7bXx5MPhq3fffZa8O3gC0uJ+VpYbS64hBja8L4NvxYOT7ka62mcye9ywDucfcFuEo9yp6juCE9txl+PG+csuS14bD9O+fX6HwXvwfQIebW58cWFg+qmrbfDbbbbbYbbfPVrb55gnbkbbbfDYR4e8Rp3GPHiJ90fVi8sR94HptziN9Fp7Y+y0dX5l8NPOeN8ZZZZ4222G4ZLL1+h8F7/pg3w2223wJhtk7gJi8eCfXtsMM5FngctG5LdJzZZ5HLvxnEdO7kbFkWW2cl7jfS+af4jDzxDSZbLL9O2222WWtvjLLPo3w9fqPD9O/TvjmEwoPuAL7JVtyybKxMOrQtifEuW2+RttuFu+NttvkkLJm2XqYTxEeSXq0MkyJsQwyaO4Mo2vuwzb4ZM/RsNtvnbYssss8dT6jw/TtzY27XiGCYTOWVDYMC6sNxB4OKW35kyzxkfQMNux8WpDImJJMM+B8btpDvN6XgOmwxvqEd2qRLZkTxvjXu0ufGeQ2xLfm3wHgt85Dg+h/o5Iy0mEzYTbIsLgmITZguonLwm3uPKZ9BFngfG22xC5CfByeRlpkLvNp1BdXoY+0fOEZU+7y2/TtvjLJ585HjLLLLIcH0P8ARFg2REATxE3bPGxJ42Mll8bbbly8Q+Ez6CDZPJb4Ib1PMfCk84NzbfK4u3EWcMLxB83UI6kdrE6vut3qfD536G+MiLY8b5CP0H+keAwzzdTCbMM25bDdyeRmGeSTPKZ9A5Jv07EORSE8yRM+FbuL0MOLYd7mDbZH3kyFOu7Pi2WjZ9JZcW+c8EMMAxNWCLtyfD4OvofOwz4GGfIzFv0KfoJIfAiTyxKGT4PoHIdJZtlvEx8PIY3LibtBcxpjZ8W/M2+M862njPr2HyREPkB7iCy23x6+h+kZthmGY8HjYm2HZ8jMkzE+WxEGkng+glCfAyj4GeYuZx4bHk8QVxGnN9k/aW2W223ztvjLPo48DHgRKWw7uR+jXw36f//EACoRAAMAAgIBAwMFAAMBAAAAAAABESExEEFRIGFxMKHwgZGxwdFAUPHh/9oACAECAQE/ECLhHzCLhCEJzS8UpSl5aca4RGC/QpfTCEIYI42V9FJsTCcSiJIuvQycIiEIQnNLwpX6mQdsaBcRE5i4R+mEIzJeFKUpSlGGEy+Rz0UpSl4jJwiKi8KK/TCEIJ30UL3iURJL6ZemlKUvD4pSl5GHY+J6i4DR6Y0aGja5nMXCh49McY0XkpeJv3MkKXhRUovhEVFLzCyuMED4aLJEgk/4RepoSfErKMSnOVLbGhy5Ke1ngRfI3bj8/Q82M1EaBCSXCbWhI7E3Y1exvH4MZNltcQhkiGpfQ2Xoo0j2lLjZL6Ei4y2YEdcaLwm8cCcSEkX/AD2nLc2WjQ0hxsRbQ3BwyukO9UYm7GCM2JX4Yha4DNrK4ELgtN40K2s7EQhCEIUrjU9lh+Iyaa2TnY1H4MboeC8qUbfQ2MsTuuJN2xJ5ECTx/wBM05Q8aEFVPLf9JDrbSK7YXcZaEJJ5YlpIUVwVRkeA0S7Ojg3GouhafH98Z8sWzHM+hSlImSMNxjPCobuhp0x9Q2QgmJK/9Y0GLRqUshtdFZW6JZ+ohIESiyo9J4Q9pj2hPC+RcDcaNfA4H+bMg7C3xSl+lPS2ByjToZbopCbWy5/URAlOaX/qgtC2HQR2j7CgJn9R0FxlJwVpl7iNmn7DWRdfPK0fHBuxdm3oE/4WlcM74LXD/wCsGNBbBNCKsi0ejANhC4biG2vcl8O/1G14Ds17BqYGO6ME46Uvon1s9LNuC1w/+rLhobLg08ldDaSvEuELhokJeRZyWCMfZOHjYltP3H0fwy3pvz5ZSlL6IT/gXwW2LXD9EJxogqIJ64ZnXpXD+jS/UI2NBlBs9IvgN/Yne2OFRDEtjbWfhNmWm/PmFtfuf+Uz8L93/hbf7F/rZfbfb+keS/u/9EvMfsJJaMHuc0omUvC8z16nfrLY04fLZF+eNb6J1Rcp7PkRwNTAWl6UMf8AxxMi0LhmOWC2Ni9BysMmnSFbSg7YixJ9+nXr0zmIhCemc6HZCeh64aMQ+dT2Beik6GzDQ3gdLi8oY/ov6rQe/QwlbOoVaGguYN4LCRMaEkKq4ZlSkyYuyCoSEx6L6aXmE5fGh36HwxjRi0PfFNR8UYfgVsYZSGg6XpQx+hqtkE8a8DVX6rQexHZcfI6kEHILTX3LWFDcDWQ9CUkjSChNfIgVTYj0T+SGUhOkjwRp9OlKX1Ox8vhjGjFofOvJwO2J54JgehI1C09KGP0S8jwSXRFxo/qdOGwjsq/IejfECdwUMFxoexMDVYlEIsMRLQllDxMUDYjXsNBj1pImIL/w9OLy+GMaMXoalGM0QwI8BZGxso6XpQx+hfw/sbIxcDgbD4pfpEbC4+8GsoRuNhO6IBCZ4JZGKHJCSzXyJdiWCk4OTY0ppFfWpS8Xj36Hwx6GjFwpTUYz0biNikU6I7CChujoUXK0MfoX8P74fOr+oxGwtcfeDeUMawNSjHJNeTUM7EE1qGPDF7THhgxvFFJTf5X4IMsi5HFDwNnfpvrnNLxRh79D5PaNHw5Sj44Y1gmDtQwglsJDIeCXFFwhj4omZfjyPA2BPJ0ailKL6DEPfCiRDHkafuNXQWmZfyNkcNCExDGJD0m8C838f4M/L/dmfy8Q1PQ4w6Gk3f8AYrqbbGSxobFFxf8AgHv0PlsjQbHHwfclvDfgY2iEwr2IetjdBvMK4IIYhj9D/b/Zkh1gVmw4pRMTL9BaN+EqJEpRswRDGptJJRw2ohgnk6EyikEpDBBAnBKnGU6lopNcEbMe0/aCvBMv0L9Ft6Hx0NkaDDcOxve6ExMo1GrwhUlkvgafWCvOhOkJKZMn7DM7S4XD5o/2f2NoaJ4FhoVM1YpRMQil9SNuJWjXBdEww2QuDY6KIWE0JhFpOHBUeRTdHWcYkYG9loIwH5l+x752ILKVC/XNkbE+Hx0N0aMbPFhfzv8AwT0kzXlfwXBIg16MBIXDV7ErMPAQ8jtFwhjHz/F/ZENLYmkoUbIYQQQT+guHXBMCZTNyCZY3INBDoXCH2aBeHi4J4MHRgSYzev0EaVGKITyQOyw/+AHyfGyN0LTEyLkyhSnv/wBHD5RdtpbES5tflL5D8hX5+42UvBMbswKxD5fo/i/viQyUbIYQYYYpfUuHQlQjwNGx0273RKU1Drh0aowbNPNsYYmONRjmoY7FogkJD7dP+Reqeti5IxcM6N0bIWhrJkFP3L/6Zj2QjBpz5hqF9xTtCSfREuieBh8Ng/zQ7bC5U6X9nZGJBD4Y/Q32/wBlIuU4n+eRsQ3IvQuUPZUJJ9DXhCdipu/j7DYEEbMlgQQplyEaMxxjGq4NzZW7GpbHXLRuS+w5RtfuhlsNMoxk10LWnfqvojWH6D2MXPRsh7R0OlllcpCdZivLEUQmJgdR+xHSRJ0UdMwCckRWxkFyx8PhCkPYPZPygj/4Zn47GhciF6ELhGwhOMowpD8o0JiN4DxDHQxbYxVwU2j2R7H9keNf2Qn0/Y+AoejaEkENPn7ENixNBHpJJt6YQnEyNc+h3wn6EpF3wXgzSCROiRaOgV+R/J+vLVGbGVbGo+sf2FGODXDHw+KVjbFJWEhvSZboa0Qbht8X/B3233PYYvYPZgLacELhG5pwwQiJjo9iZtjeOKKomHRgg0Ips8hTF6QyLybQo+r8fsJItPz2PF+P2F5fx+gvL+wUEP0T/wB/r6OKNJa9DsY/bhj0NYHsTwUX1cCiVEPXLHxXQ8cUpEUSzQ4KIT4pRWQlNQ34XCNxa46GzLbC3xtUQQuBuo4UXkQoL/IXD4EyzH9IzSeBMr2Euti9yCmn/wA/wSsISINdHwPmc0roZlGxPKt0atiy6NjIoxoeWYOijZ4peKUvFKXk3QhDG+DWwUM+vz+r+p02LWoXiRFLxAYo0GYwnwmPKhoNhC4Q8ltJCkLaGWTRmzEzFwzUQy1C1O+TqJfyNYlLx1lpykGINJ/2LcMSEc8QSwMQzTj6ESmhq75ZgLAY2muRpYYZRVGg2JYLmD1w2SlKUf0Tb8cEMY2paK49y6lLv8z4G8WPcYqNE3DIp/P+idWJSCClFkMpFwmIXDU4UxFEZWNGJGNUP4Gwa8S4NeU2LEzVCQ0i7EIbHuB+R+SKOqjjV+BY0UMIIYquBHYJVZGTViJmiqZG9iMiTX5+w1fI3QUIzKJKQSSGmJjGh64dFFwomJ84IvBHg/Cs/Cvgfah+NCGhDGZB2TaKPY2bhIVOj8jGhPoeWjXCl0g0IQhBI3ExGSmqEREiOsRudcEDd0SDpLIyqYI14bKmRg/4NFBGJI2JrIxo0Op/9HNC/KHza7/PIzwHQxizhD4sqQmOSqV4NHkSnUiDTTKJtrI4QmSEhE2JVXlsG2dcMMRkqR+RJ+SeQl5EH4/Ifn8g/AewM+xjng2wIYxrPBsDyOo1jhrFY3GGKcGu/wC0NrC+405j+g96+ww8gSaX92JGz/YldISaG6aIpoQ3Y9GodFGnbLc2pBg1Iw2NexxhJglNBXkaj2D2heI+BfgVdCQS+EyNUQsIMyJpn+eIgb/gbKYQiSSZiGLaiJgdQrawJNMey0h2PJooh7O+KLg2AmeSiMjMmfA28C9r/Y+LOxjNhDHw9FY8MehjWG/I88EWYzi/Znu/yNvZboq8hoBLWCFoQsm0CxQghowS4U04ChG2Gm6FGvYaNRag+0mhGRxyrZJJHv2FHGTRW2Ra+P8ASOxuB4gs5SzR2QpaE4x2PY6NwXkVKkOITtD0jHSMddjdGddH2MfvGhfwGX2GPY+0Roim9nXJbKGqhKCGwajQOOCsfC3XR7D+3+nQtjGbCGPinkV0Mt/P4K+y+X/gvzX6jb/9IVqfeMuhq3pL9zzz9mJHb+4/I/cbsfzEnX3mWi2W2E7MgcMkZLBpCTQ2BEWTMGjV8QazIiwM69w6G8nc2fDOJIOtj93Gkn7e46ngR1oiMJkrx/olj3kXAtEIyb7E6avDHbwnVTKrGjMmKHLPoWRKQsr2K9BpAkIGj2CVBajFRsPNCyIwtCdw+EDZOFxx2aMfEbAZQvA0JKXjsfG3BjEXBjcgyhDXwIuMTtoT9D6IwISRJJBI/Ce1yHufdiVa5Mhch8KUW0SpItXgWaQu+CYHTHotoUmS1P6IL8Dx/URQWZeDO+UQcJhr7DphCY2ZqCsrWhnlWTFtM7iuq7Hxw1MlFKEuJcChHsNk3KvxCliCZCatifBKvI6o1w9o3D4i/B7DhEFkMjMJ14Z8hOnY+hi3wfJMCkZwjXR5N5hrqiTCZiiQnCEttGMmrt8jdy2LgPfMIIThKsWrA2hgKqQ+zJjtQdNo7cGsCQpUCRPYSxfsNT9wmEYrPAgJtoKT2Z2VTMkxetj1DUbqoSmR4/rwLPQlMYp2CxVdDNo2QlwJWmymzAnEFgbIjghKQ3lGwh1w9r86HzHqC/F7PgIYmI6YvZ+UweGPCyoxSwYzZmw9FHFopT2D2ifxiTy/3f8Aprsr8k6HvXA2QiNbjJJI8nvCdEIM3EJiiV4SdEyxcUQdMKJkfHzyIeBpfgkh0kpo+DcmZ6Hg4/cbfWNd3/CFqETJMITTWBGTZBD+uhbz/n+GXAiyCWCbF5JnQZDeUJJ7EkLB7EJkyo0xvu/7GG8zFhmW3wJ1hCl2FpZU/b/RM/B8cZyT/P3EAjV2OaHQrN9kkWRVPzobirzRvIxM8NS54dHfK9Oh0H2JoY1qsa4WaJfQzKweNIw374k+CDJgSg4HeBq4ToqYiCGsGaGjFPaJf+le42d/YorFCaEyyNXJ2/yYzqWRjt8k9iUiGtVS9kaoz8/6UhVnY1Rik/8ARTZb/UbskH7Miv7hh0PoxnTGpCUaHlUYaPofhG3Q/tiabaNho32f8HbPwfBkUkjX6v8AITAZlnQOWEqT/Pl/yK0tYv4MAzJ+fcVI9mdL4C39T+h6fngfBGo+HXoQ/RoN7vn+hsBPAbCY+v1Lv9DB+vGmqg2vk0c9OFyi64E03BLB9iQ9CHLcFQQ02sewLI1xODfsJe0vuPxfcSdU/RMk2/Zi4PyPqH4Mf/kGX/gJzrf4F5Agq33KxOFkQpkiSKHaG8kbEIOFS0VFRgaELli2PsX/AAXLLZY7/pj638Mggq/JpjsF1tUUNK/hskpZGkxXX9/5RayScv2/wQhrsVU+P4Jh+ouuOwjUayIdcTjofoWGF38/0ahaDfj4GrX6ll/QbD9BsTZ+dsfXyjTx0NSi4YxckEDWGxcIUkSZZLwN12xTUn0JlJMUqN0ajF0zHv8AsyryJeGJmXb7GTVQoXCGZpEBXG9xMWMfBoIrR6Ha0NxzsQtKi7xCe8sS7E4hBNoa1mafZ/xw2sEbtrpiURDUUJMoZFGPLxPh/wAwQwi/RP7hLM/2f9ljv2iY9aGsDWRMge8aDQpcC5Q/Qti8/P8ARgDYQ2o8aXt/ha/2NEvj+BcSRv0/sfXyhseekRrQm11waMYmSso8poXCQp5IaT+NjSPTY9hIpXCCDBTaL9F/iKuWNlGgtpJGVDeTQ64Mlgp7JIITicwZJfv/ACZfAyn3szZew0G6PIKIkfgaoiNQP9BXmL7Elb7jUdgQvI17+w+diQx8ZpgqI8kYicMqFsfh+h+D4NAuP1Hw+Dv+hVX6f2ah5f4X9i6+Ufl+3GTg2GUWhtCY2OWUhfMXuFeKIomR+2RC2JmobELWGZPgfKHPBURPilC/05YiqbGrC/MCgySIezsjo04ayThCEIQhOGXA7WB70Q3sUTrGkyNC0S57+CrVa/qIbFTDbJ+RHA3vCFpCQNZNBbFwohBoROP2P7s94n4/9H7Pz9j9BNUhy15v2Ecjf4+Dd/JM/H9iPfwI5b2+zNUvkW/wv7N18o/L9uENRJQ6IIuhbEqFRR/7H4xGshDNE2eBBpnWE6jwgqjbMMi4QjEQgxla9DIFmngSUUNRbbEyPihrIlzGVwiG/HFKKMdD7AlfRjoy2LeEJMxI9BL2Sm+JkUatYlVGNTDgSjHtEEhBB0JehSmOBpxtaKq0aEEiB6LwNTrY8tVcitInG9Ogtc4tM2MExK0Zgh2IXDR7QztDoPuxhWZPQh2mQ39xLbiR+f2E7sSiRjQmX6NEJ2sRvLwLQ2R7Q1wRhkXqaoqeiMj4fCNnClJmxK4MNDYZEUYasr9BTkkKKZcUTp7/AJ/0TeDyITReQnzw04LipfXSlGkRDV7Ei0PC4bC1wuXubfI1R2IXL+g0j2hk8MYhKx86OM3MbiFg1oTI0GKlvgjwX44K+yEMGREJxgpmE+OTYI0ov0IQhOHoX4w7CHWhKsiHoomJiaEUrF6ATKUpSl5MnDGwJgS9kXTJ7X59heSLaFxx0QmF8jC9D9D+gwfMgKuJKEiEdDNmpTYmR4CkhOVxWK+pa9TxsauyEIPQklkUexBd4/s8I36ExGhP2EKxegLxXyUpSlKXhRmhBcNcdOGqHSSvngvQxel+hhr2NPA2/HBA3KMwyDIhohCDUSEjoRCEMEGxJi36kyez+Rl7n8j8gzexlv8AISXsXOg/IKNsXuF2Wf0GmsifkW3sxxSUP34QTdow2JDHGfRSiMlKJlEdC4uB8EscNJ8I2L6T9EXDRDUfiNsyI2UKOz3RLEoXVlsUTITlG0QNvoQSfkVvq3KY8kRHGSVoftEudSBq+LVdDi6K7Em+uCkiVsTQzehJciNo0hKwSaZAvwJeyHxS8VlZeFHiEylZTY8Iq+mxiGLlLxqLxQlJIkYI4UrK+GNMVQ2DVgjVFPBGzPRaGHdz6tiIj04kLwqHxwlBIPh8CPpCpTY42yJdkXY2tDWCYwJKNi8sbR+p5sryJPyRNiNEylE3U0xDUFCFKIamSlEyi9C4YxDFzZMz1Ic6Ej7IRIvJTIqQnI8DDTZDXF4wR4NqSS4J8HxLcSj9NGqIbg0Tg0pBGzR4Am7E2Q6KxQpkJ0JToadElpUh+wz0X4FFsqHwb7GsoST0hBN2SJVsTvBCbKZDInGCE+gYhi59g8IQ9Ikx1GBR6HwINGBiZTA1RmNCb7RCe/GSwn7I10ZIPMyu+S/J7xUPchoHHkSrwN0JD1ko8oQxpSUhkwy+BPChSxCvbHDH7ytFb2OsIWA47LNs9gh5MGKR0V+StisQO9HuMNonyJjRGVlEy+v3y/RBogyA0iN1ybY6UpRJvooJxN5PcYkCUSGCobNGDBUVFRUVDFbLKJaIro6++EMcdFLoVbJNEpGhe6Hb0e5DIoNRcHGtGOhpo96OllksjkTdydUaFrEmTyRGBsVT4glCeBI7G0E7kWeIL9WlLxExobgYw0J+CKUQRghCoaDXhRlk7cx5JxeFZSEUbK0J+FvQ3HGNNCjAliXYkEzeC3AzHodF5MqfY2mhi9tCWjQWyWMIb9ocWhRsT9C6IbGloeHBZ0ZNqRdC8Bv2bJOE/JeE+DX0L6MZZXqhOE0ieFFF9xpeRJGBtcjbKw0LYvISIiIhpwnkiIQaXLYlNntKDgaEXZIogYTC20QkYIW4exQTQ9kbqia0JFlGXgljdDEaY4MhpDCM9I2IPLQkvNMdL0X06+hfRnNQ14VmeMiE5wTiISGCoouJzKQi5IQyZQhhlmGYGkZWhTgsSZRAfQJvaDE4imxo9HkVhRUUtjVJ7DWVo1M9OFTsTvaK0ZjD+TDaFkeMF9itiQnrhOO/oX0ckfJBEREInmbZGV6NgScGIJl4wVEEEk+iyzHGUMXkhi8h9kND7obpiQ0TQkxJdlQokZ8j2Ursia0JloaQ1bPYI6M9jEsGSEEDV4QyT/kY4UXnPghhzSlLxX0VmRpsss95PnnpcI54QQhBsRmSEZSJsnQieT2E8l8ovgOcQlnBWpSvwfoNjIiYqlsa+SlovLiE9MIQnohOe/1cvhCLnJn1AnCE4QhCEIQhOLxPS3xshCcpeCeGYeh1Z4pw7hV0MbGfa4bXbL4Q/eVPfCXCPm+m8XiE4nCfHb6s9IQhCEJw0Q0KGwRpZKJ/Qg0NCoy8NUjNkgqKXmXmw7FmGWFEQoJTQ35ZPQgaMpcQSEvVCemcUpfRCHf6S+lgaEDbodZ7xIQwhINB+Ir2RkYvchCcTiE4ScQhB5YE2UQiCCGuF2sCdkHRZGJRprQ/ch8EmREgkQhRemEJ6ITil4vHf69RBPBhtmRDCIGiGKzfDPLEIZOL64QaJxExoRiYmJiGhcNcClGaO9wr6HRzskjQoyC5nERC8XluGGQnF9VGz9Jc2zJGIQo0RDGZM8mIIbNjEhCw6eU/Q+Fw+IQgwxRhcPYnwxI6NLoj3wbO5DGGmJ+SeOV6oTi8LA/VSlKPl+hepcxFK+NohiQT4gxD4YuYQnKa4T9DG4J+pjR2LA/CCfK1GSh4GahoauUOReGgmWip7PbwvTOYTi8zik4fDegvpMRCC4g0ThoRCDRoXEJxBYYs8rPoaFgXpY0OE2LAnyuGSOido24amimuKP2EyCU5Rr13ieljQ0N8JGtZo3yuH64QQhonoaEMnoaF6UxobhifoY0Ji4foao1GJCII06Ji4SjVDcyIDfDk8HyfAvVCcUvrnL4Y1wgjQ1z4n0pwiDQhoXL9CIPHMJwmIQ+Fy+HgT4foYnoNCeB+GhYYmBVZQq3xbTGLQmISILiE5nNL6mhrljEU0Sn0QnK5/8QAKRABAAICAQMEAgMBAQEBAAAAAQARITFBUWFxEIGRobHBINHw4fEwQP/aAAgBAQABPxA6hocOZop8NQPKvZ/U+gpl/wANS/XSDEasgND9TlPtBW0j2xNmPFBdx5RnBPOJRMZO0aRtuLR6WKiI2jFRIkSJUT1qOJmGPRHEUafQyMlTx6EHpOSvzBcCoAZDFDfuOku9oE3AmVOQietxzwRTmPUYtzMrrKSn8H+NfxJmBK9KuEV6KlSoEr0qVEHMpLcBMW427lQbofiDcjzBtghzL2IByfLDSXtD0PRj/FZcuXLizyjWMNvSGgeWOz7GYHQ/aLMD7xpHxf2m9J5qOWMqVK9KmKQcyrYmPlmGgI3ivEZrywPiDATuSrUROyX6+mszmZaFbhwJoDOZLANBKqdpZ0LOxMNsq7ynYlDvCuCJbx4Jhw+hbz8QG+TzKTvCB5fEsaPuYafiK5ZSeER2+ZgjUQm1zQ06XZNKfiojZdszlF0cQLkbOsLeuJXqGwPkieK8M/6EB1eMzJhV8Ta0dks4fDOhPMq6zFIsG+IgxXmMSVGMqVEiY9dxIkSZcRPWohBeksl+leUooFToRtSh7QK1j5lHm5iJ6VKlSvR9Lx6XLly8S/41/AH8AqVKlk7krK952E8UteWbgrhfEF4ryw5gTlJlHV5gWh8emPXX8LlxYsXvFlxYr6MPRabIvLBcHxBaScIPLHC9gTbD3iXlz6X6L6Znt/J0mRNS5c9/S+8uEv8ACLXiHhKeWU7wDpFgLDh2idoA0K3ETZOVwgJlWXoEegZZbr3iYtnRGVCuhfzF8/FRzxKzqF1iWeJY2wDzBVwTJlXYgmvsyoB91lc9oARmU97A721IvivEen5RDi/DFbCelSpRiFudmohoOy5V+Zfpmyb6CEWZ2bly7ly4s5hGnYM6I8QHXyg+B8Ms8k6Idyf8JnQj3lUtD4Y3F6yh4j0sX5jSVKiRIkPWokqJ2le0eozB/wBkDyPgg+F8sLQHgmeV+Z115jNYi+0+0N6n6YHV5QBhv1qIem/4V6V6VK9B2QjzgZX0VKOSJj0kv2lnmNvMqCdDB+UHcoQ6/iQHdsC4QA0B7Rz6VAuVKmJfouU9Fy4w/wAAWNN48x3PyQWnwEHk92L0D7i+nwTZN5ZX8N/xqVElety/XhNPeMASJXqy/SoHdlOkIBYNhJbrCUEqpSqvcqi3iNiM4WCG0itbQikXj0t7EprUE4/EvzZ5ahhv4LlQzfu1Pb9sRzKOsDtBsF2zkX8yuCexFzbhHAbTTB6R0xaC0cjDm3F5GDu/mGgkXsR4lIo0jENqVmUxlXARsfiYmj0c/mfSXhn9lZNoey0zLUuXLj6uY7wiOFIlqmXbz3Q0qu+YI0+zNsvkQMiE7MZUbiXiPSx6F+I0lSpqV6JGVKnMqFp707McY5FxJbtjRyh1H8KiSpUCWg/T5ynWVIAcHphuPWlO87CLRV5ZVwIN4YSy5hVth0IA4PQU0w6oCX/G/UuWxZf8A+hp15ZwR8ZgcfRRbQeWL0+An7RRV2r5lSv48xPSpXpUT/4b/gRqeY+YTXrU9/UMSoQegXAclZg4+40yjowGo5z894LWdEsDcW5wCCOodaHvBm2/E7Fysyw/pDOhfMt4AlTKqBF5gOkO2DgiFlaqHlh1icI/RGRC4j7JCmC7Er2FfcEUZsK+WzhA2tfYgVJaJfZXNe90PuZFvsx+LmcPbmPV4MkNJYHYMDyvaC815l9Bi/FeInj5R4S/EVsJ61G0+phm1R7kPlO6nVjsqC2gdm/Rcv0ualzYBHgUi72MuZpIazezmG3vGIbl+RBOyfeUkXqRfivETw/MelfiNPQ+hUqBAlz6LdIga9CviJEiQGV6hNuk8ZXqTylOs85jlIwU7x6CPWlrtlZlQH0eUpKdCXUuXLly5fpYbajvfJEuT4I7y8tRus3VyQYtR2Z2kekncnch1JR5lkQbQ8zbfNA6V4IbY+WL19icgPGJsV5ZtKgfyr+FSvRU1OPSv5PozX8CNfeJiEfU9NelBzMsVKgwq4Mt7y3WD3gSyvraLtB8ylsD8MqcxH2WWBvI9p0C/UodfkxfIntEen3Hoo9pS2sD0gZjEXuViiYNoeWBlz/rCBFX/ilf1LsHypPgH3ABANAXyz9TOo4Gf7AJ00oPsC/UwaWC1XsRHqA9we9kOTqAn4pFb/tC+WJx6KKO8XfTOWvvEOvw4xAU5OjLWy9Qt9TJv3KfcsvDuGBWoHl+IpQV3xK20BdDA8iQ4yORQxbVkUaSIcfHrVxEsrQe011HTKH1vdTcPlJ9djLf4PrQ7CKdorhIDhmlZ2YHR9Jth9k0I+GW4Yg6MpeSvEbafmL6XGWKrcqKWVXeYtfYhSyWKAEXkFEGoKbWeTKapm8bFc3FHHYceYwrpLvEE8TuSBOZWUbIRHjHusTx9pdqiNu2ZdypXoIpKlet+ly5bMZpl7xsb+CIaFFcPuxVw14I85+ots+Wd4Jb1TzmV2g7lbtOEe5LTDXmJdfiUaFOk+7F9DwI/iJjnefMqpVxJUqV/wDSvSv4J6JGPrUcf/Bge8YTj0IMz6E0JgEeCKLuHVB+Z/ZT+CGpPZn81B+13A/DBV7/APZal/SPSp+Jeu75WAWuPQW6RSlFt6nUPaWLFr1jDJXaK8R41Cm4haUvS4EDnSF81UJO7yr8Wv1D+hMT6B9xS2q3+XlBI6nW/jBEZK0LfWRZHtRCURwke9mWAk4H4CEe4W5LfuLOaJ2MAVfqVua6/tVExnXxw9C3Upf1wGtmgizPpdZMM0dOmR9zSfJR+o35xXOOroElazOo3MI12JcsrN64fiP+6zP6gptvYzLLCjDqnmCNh8Qbdk4iPmKmviJdfKIaB8MdgfVJTjE4ldFuf1mT+6+fXJamKxn+aDsuKcVF8MR4+Joi7OYP6DEwXuCbde8ROIuMkU4qPdFkV3OjTmSKlU+UXx+ZgECX6QryQA0lXVnR+0V1R7QLaMp6MH0i+pAHMolVx68+jXpiKE0S951D4IHSfUXwe7FNA9pyU8Yi7k+83yyneBcSg1K9N/x2YvqCBA9KlSpUqVNHo+lelXOZX8alSvSv41/8H05hBqowjqb9CUwtzAuO3DzUNAf50ggu16Kys0vyD9yrmdW/pFMIOw+6uffooX4jSYPKWW4lwdMXC7BjTclFSdZ1ENUf8va/Uru+cA90Ig5w+jmBnepA/P6Itqpwfmo+4cgHTcPkH1OnhYPuW+4ktxwF8LUFbovrFrFviDlhQMllixUCkeiR7/TeK8CkDdasOGLF56EPxSZbZG2+ZeugGZMe4vrZGGnVJZ3Dyd4pYgymKHEVuW5gvXn059KmnEwRR5uAbPonKDxmHRPMoyQ+GClIPki3j4xFNh5zOHb3mwL2hwKQPm/JDr+EG5rzO2orqyL4DE+XtEpjKiGJfGMRyPInXvIz9TKgi0Ds3L/hUJQlNMV4rxEcfKJ8X4hpdow0H0T+wCaVYh1jUQ5CKLQ3BPJPKMu5zBuhgvFQfKSnVnYlDVRiRJUr0ccTSLyzhD4zOAvtUC/yMXoHgn6KxHeV8st1nkynSBX89fyvv6bI+ogetej/APc9X/5vrXpXqfhOMdwnHoQy0Q5/dXOquF3iBG2oQQdsx2fMCtWBD9DEejn3SscOTLSfB/MyTDSfZ+kVwkoxfDBir6yzVAFPSDbDct66qK4ZWKZo01WbloaET8lHBzRiMeuzv2stxjxB9Z5TvZlzG4UHmUR6vhogWDXcIXlrySgAjWHDH4bA/KwVy10tg0Bku8muY4afRNyigLAyyuIIDRLReOkOV5ZHWZY48AAwZM/cuCna19sUQUVjncvos7tQFUB4lelfxqVKZUqV0hykA2kOUT7g39pa0wFkPki9ewz/AKJEuB8MdwT2hrKA7BgeUQwlPeORXxEul7xPVPvBbR61cqnCj2ZqEnuhsd4MTEDyFzDM94d/43N7myp4xA4+UpYDwZgLkEZgDsSUzLxB9SFtwcisp1FBQV/ChiRJqX5ZyF4zBaPaqf8AUYjQfa5wp4xNgvLNtzylN1KP/rqX19F9HbB9d3+AhD+FSsyrlSvWv5VGEqbnP8qj/wDTj2nH0JxEhMxHVQRqCEDo/BkQlv8Ajlf1BDmXBe1B9zpogF7JNzTdLL9/jHYnR/yH7lvrct/Yn1LeoPAP1I0bNrv2y1ijxLc9YFUsP5leDA1sbRviVI07PaINLUCVqMc6XtFSYbaxA/rKXAasgj6I/uXiulSog+zmUt5W/wBhDmSuSr2uYyG2/Ed6NK1tbibPH7gGi7ZksP0Euj7A7ci9y70HUG3XMTQuULL5YPK44Ko6S1IrweYwK+CXliOznMBqFnFwFgKrvcq5X8jv1ZfqNpfpqAcwXIM8xKOklTaCL6s8Mej5RPi/EV1kOZfmD5t4g+1JfURXqRroMT4vxGzD6VGNEu1x/AfFR267ZJyS6OH7lnvLy8pnlPKW5m1PtiK2HnMzCHwzgL8kyZR4Yopp5lXTZ2ir7owTd4zB6PaqAX9kJ+iLiOjxibdebTPUldWUSv4c/wDxvvLOsp6lvSAuGU8zyJTqyl6vzKrQEcRhCbozaEIQ/wDlXpj+Neh/Cv4V6PrUr+L68e0GEceioKhHbRIOizfutEBCEs9MlnJerMQITlBQ+lgqEOw/gIRkRbl2/LFnMt1iPMp5hJcgL7soR2qM+UUXuhsMrYUZ2V4IYhK8AGM2EZzYrJSsWXhiS2oIYGpRyRZG1dZl5QW8GDqMBaGj6i1eXmKoQFIOGYUwN5F/qM4OJA1UD6zRnxKp7Wta0xltYQhiOM5wnT9wh80F4eZQBRBlmnEO5oXdA4+Y675Z5i03SzAY0cxXHDWXDsoK5ijED1KqWQUd5OZWwvMIUG4P1klXFejMHFRqosSJKjO/8KgemTmXm+pSWVuMW2IrSkWaRgXTLeFIHunyQHJ8Qxqe8Tae0eJSPBTLbD6biDxEvhGbnxUqx76/ubSzoKgt94G5fosZcWPdG2wnBUiFlfQI3iD1jbh6KD+d/wAblynMp6LenopTulJTpKISraYD/wCso6k8l9oJ0fmX2CW614i7i6h6biPoIQhD/wCFSpX8n0P4cR9N+r/DmPrxL9TjxNHtHcN3GGoSxdG+4jzwhruUL92ZvGISXJ9zW/iYT+sh+4rBHopfqpWbvWr6CFgaFqt6ZfcJRtKnULAkg6wf1LO7AFZO641HSTeJhXsz2BLlJb+QfBZRQVReLqbIIXo75AmAqq4Gvf8AEG6BwdIlyR4EE6E4ATtBbAbHFxmqVoIFJKR5iKCWL9pgayoWcogGhGplq1qPnYCPa5XZF6s/mKjVsNdcEqqo0CWASPMAXQ4zmOV7yhN70CWcDvBnqXLPRCVKiRI36VH1q9SpX/xuLfo+lnERmPSzhXKeYV5JSl6nB+9UW18kBoPmPWPGYEwlRInaabFHqTUNOmUFudxqD2A+8B4WPdExEZeXsf8AxqMuU9FroldEs8k8pSUdoM+ZTPee8o7z2l+PiW9WMqv5OR8ThD03Rm0IQhD+L/JlfxSET1qMxK/+TH+Fa8TRGasCYrCfURB5JcSkgC8XW4NzL1QIghQUFa+1mUXAFAKNaIKkWRZV/MZWVNq8y9c7LJYGbOl1Kaqup8yhitKrPtKjcmbftK/KorCgMzZLhuZHiCvEeFlgFurCUPqiVUNPu38S0OCxS+veKtuzvvDdKCueuYq2t91NQKhrX/qZkFGg+I6S+AlQsMWrNQyBGqQ9vx4jCqmkuhjIfGj8JY4sbW4UOho8qiD6kEAbch94xXfnK3d0ApuOfYwC+c9IoHEuDLmD0d+mZmX6PonoqB/Cpr+PvLiVK9KLiHtOyWIEJDRd8IgSVbUFqnxAWyW0TyIL+pgGlrwjmFvDOUnnMDpH3gtqJmX+8/cpd9DApENHxAQtHPJLCOSsT+yRDcRx/BZct6TMplL6ASh0mOPxKXhleJXeUd5WNfcrxPeVK7fwr1367mfRjt4mhCE3RgzCWhD0Zx/DxK/mnqw//C/x6eJp8k2mZBbMF9GF/RAuOsBlUKhdZghjxaW9j3jalAtgHywdgKLXiMtsVVcGKsP6iOatqqj9S6gcKS01WOYgVLQytw8l+SI2ZzrF5slq+a/KMVKoAx2Ji4tMTaHmbJldsujR/cuiuAKFdYbwfcOLCw9F4izcDJRk2LjczK24uAmx8zU8M0TPvuMsxbkeJlkTrQfXC9NAGIcL6P5hpTMlwygsINDncZR1IrCniaCOa1lN15Vj0Wd4MRitLXeVKlel+lwfS5j+fH8+f/jj+FgWq4qhhs8wTrPE0o+0TqycIfOIItvJDmSB2DE6Dxmd67JUAgSrQUdgQbnhNDyQ6QMvKYno8JYlIBAOCZ6fUfae8o7yjp9z4JnrKz/8K/i+pNfwS46fEwDzDXpuj6CHofw9/wD51Kh6BH059cxjKf45/i+vPhM/cTacvMLc3fLCfbIlCOvIltTBLKO/Rj7FdRA3QuIGGZBTBtCSzgbvuxEXoojHCJiW+SC2rL3oyQIJlEDrmY8MLz29E7jt6Bw+J2kgctRYwUHJbM/mALn+MQ25cbUA4o5iT6SxUUMAWi/06RLc/wDhKvIQ5VBZefzNsXwfxE2AWvMNs1K2UU63NUSbXPuY6YO0yjZO0lyWlelRh/C/41K/iypUr1WX6PoejNwWdmZqw2QIBBlwe0RbxFW6ivHxOEvvErmCv8Nz6hNtdxbDyTBvSB9k0Jc4zaVM9fWpUolSv4b9K9D1ub/g/wDwdPiaHmGpzMV6bQ3DMIelfxr+OP8A4V6c/wAKj/N9eI+vMcHcjuG78w5mPkQmHmJe1iCbUrNR4jbs+U294A2pQQ2p4c5iYSwN12vN9pThjbYx+Je0cDNvMZyxAjoS4xcCvkiugWmWCgeT9wRBgmdkwWO2KXuIwI3gS1KaWzv+0EXqrndMCvpakXy63EA9XvyQbh53B/n4le1X4mH6Jk2afH5QBtHaf5iCFrQCD2W3EZ1cu8BFDdsBThPaFcnOWi7SzOn3icWccgyePxKqYNkA6I9kXGFSklSvRP8A6s3/AAqV6P8AF/BmjDTzKhNer+CMrpK9DW7fzBr0CZVepl2HkmLPKOB3c19OE0elSv4H8D1xK9KnHrv+R6vpcdM0PaHpt9DuG4Qh/D3/AIPoSpXp4/8AhUqJj1cxP5L/AAfVKfCfgTaHHlDn3g+RCH5SUD1iyd2ACLvJWoh0oDl2IfdQua+AVQfNwGh5SI57XfWOyEzHn/1cV75GK29X8wa+03TdnMJ1jWRw+Ib1ALbgrMvYSL2t+2IDdKP8ksCt5ytodAuDA7IwCErfiIUCNOd4ZU0KChf1KGM1dU3DQdvygZEKNp5Lu5VFXuGC0aoShs3V1uK6DGKw+YMANFSo5dpUV/MRG8rbC4DUpixp9dRWKvpiUQXKmo+r6Y/+VZ9Kh6VHXruEWR5i4hp5iJWPpWjaMr+AsPbBfgjo7oaPJMLQ6Pd6DOEdP41c16Ppfq/wfSv/AJp6cx0+Joe0MzmbYk5whCHq/wAKlSv4VKj/APF/i+mv4v8AF34T8kdwY8iG33n5n59BN4cxcvMNl04j2MuroZt9oFQa5WtZuoFwMN6z8zmMgLSAvEdEzbgvwfzDSPeBYzS/mYODWospszmEWhmRLYAbbl1A3nY6YeICFXS3W9WxAYYpBQcmYqo7SYGVIVOGrZeCEtdjKqLAWuscR0ODYj2lbmHKx2sIHp9RpnXnEo4HvHbPmnZ9pd6S2B3gOkCnEeiXLWXKmokyl5aLjLG0qV/Kv/hz636Z/g1V5i4YOSLfpUqVGqfH8N4rDshvypirvn5Car2QyXdPyRI6R0/hf/xv+Hv6V/P3gfwfR28TQ9px6b4znCEyh/KvWpUqVKlSpUqVKlRP/gxP4vrr1wfCDHv6PyE3PM/M9H5ZYKbfmWLSsjhZrF3zHXgLh8R6BAK/ZECADAQz56xjjLtWDHVjTQGkVeZcgGdi8QGeyX4lSt0W3MnN2cwRjdQe1ziQVqp0awOXmWF/5gm8O7HV3h/E2PaBYnyvAH5lix3/ADxHsP3WdA+BHe9qW8vmVcqAxRsHlgpA8OvwR8BXl+WAQ6js0Hs3gilDYV7KfcBqgdceEEMol6D/AMoETsLfQEH0ZdJf8G57xXrEeIW2RhhipUqVK6/wqJ/LUt4/jUfyRyQ2St+lkX0dPj+Jx+iaXZhv/esGXkn3j0Q1Z39HWOnj149K/lf/AMLJiMX0mib2hvaHVmGfdIOhW3pD50Grl/xTLxND+EznCEIE9pr/AOFYgSpXrUSVKz6O/TUuOv5Ppz6Pq+v0Zp7x4gv4Tc8zT/DM0hVwoYlTJC0PEBGA50Cy06+JivOUGcPXEKEuNtvzLhqLvARG73dV+IEpH2Pywp23kn4JvhWdrmLMufEUyh4H5YhUSjlc31OcO8CFmRObwwwvsoiY8AT8MWXsjy3ACCjRtDyzsaxn6JQ0TpC+QEE6pBDzd/qAlRNj4KawDzfakwvj5198mB0YvCfkfmS4vT1I+r6jdpcKZ7rYAhlyj8ViBfdt/wDLGzeTrUplowuXBly5cuXL4jiEPEtZkxC8ZchaJUr0uXf/AN7j+SMNnmXLly/RcMD0SbHoJZnZmb/nMXA6MP1egBXkfR0g4Kx6vqsuXLly5hBXQviC6+GpgtA6oIvB9tuV7+JBsgXaFPF3VEOfIf6gZvgu/wBR3+fPMV38tQTavLAzWVkBp+Z9+H8XTFYe049PxkZzhuHoPTf8GMqHpX8qlRlelRLiMY+j/Bl/yfTfxJ+8TU/RFR8xWf5Zm6WR3LAZnQp7RqYlcgg9+3bHmHXB+Yta6CyRV0PKsagMXQ/ub0ztj8TN+cb9CZupBcj1l5hxmGjXLMcQABLVCPuH/lk85ph9mWn/ANA5mIyibsHyINb81Q+4X5i8F0WQ+I+oFWdu2D3RBa6GA+CRco2bH5ZRbQXVzLGpj6fBl9DAXE8Ev1nmz3RQAqtAcy3ZuRlPliNAPRJCWsv0KlpaD6a5hV4ZVxhH0CpCwqVYUoNxFbipXp7R/lz6V6VOPT7DHUNkfVIRMQl9ozYh/wB3EWHxH8/3gpEDJ7HpD6B0mXghKlYlRW0PAWy50eQfmUF+NP1H6laKhpvYB+YN9hT9Qa/LF/c4DwH+ppUHYhuWBb+aHAvluGH4QlurHm/cp35Agd+3b+oLn8f3jxL7hOiPd/UE6V3Q3p6sNJdfynE6w16V39eHxND2hqE/X+Izl6Df8FYzK7yvRIyoSvS5f831cRj6MfR9XB/B9H029s/aaIr+EHIxWvL0GU8RXn6lnKW9WHpcuXL9FzLwxnBk/EqnLAo8RolQqvaDYFC94Qm0DcdOtIe6OO8SjcE8Slww41MWUPMuWlG25mSeH9QQZrYqDqJhiBTY4qWaCC6S0H0hZh2+i16jJDX5oV11bouYhZjFlQIkpldfXMEMHrKsikQRWXLhExwyx8y5tFuLNypUqVK9Kgercz6fkR1DZ5iZlQzKgdo8wIxmxMvB/Eb9hmmRQxu8ekP3QjI05XiB6LCJUkbZPJHqVF7g66wmvgiJh/EUNB3amwL2v4nAHyMD+kP3AbPh/RG7BeVZova/tGzV4ojvv5Up0hAQfMuLRxvUtxMv4YsvP5T7UCVK9eHxND2nE5mXtPxBOXoCE4lSqP4MqVCagfwv0r1fVm4zn1f4vqmIx9On0J+8WLcWXzFw+jf2ZWPSoCtbnYluUnlK95XpKOhAlTCx5In3MGzpLGXkLRcB9QxVqjcDMKh7M5u8O2KfcoFU9Lj5D8Q4Fcgf3S3BnC/4GBgJORPun1GpV9HfYWVNvHawiNC+ILv0h5uCq4LbuusrN4rV0fUMtJJiY56OesRgHHDALA9JRxKWhAJZT3Im6ntN+YLGgM4Zg2Wy5jtRaFjqKipbpKQhPPoDcS6j2x7Y11MOImZlMqVK9GajN/xPTDKICNJh5n00eYmZUqVUpiYYGIzc3IKPB+I/Y/EeKB8s/F6Z9n0ZZvgw1D0MTn9f5IbB6QYw+A/uPEvDX4mwPlSnSVXpZ4i6letSoEAjjMClxtBwHEG4i3LW8ezDXw/M+YoGJXokZw+Jqe0NQ3Pxn4jNmbQh/DX8tS5cUi59Lbg+rH0Jv15jGXX8WV6Oo+uj7E1HvNzdjtjr0fgZx61rAv1X1Fuka6VxF2HJPKWZZ3mF7+mllCwfRGK0sAlAXJqb5/8ASVFN29C4RKWuwRr/AIfgidfKf3CqC1XdSqq1KY4YjebsTRFZQMLb5nUZgOJKm3oVLiw3kOkAEBVC6ghCuDcRsBYFDxtrtKAVXA6dYtnSnQDwubOJ3cwiCw2cczKwotk3LsdCPxEZxEvglcEjdrEoYlOSInlFTGBXMGWSqKRDxASlzdcq2o1cx0j6nrULemmPoXKtn2WJiaPMf4Yjph6uMNHgn2X4jqYYur6wPu+jLcdmEr1wPN+SG5miBcrrEiVPMValkTEqUxXtCyQkTAiMcDgQNNkM9VBA8Qs7y/hhtDt+Zt9/4qnHhNfZD05+x+IzaEIQ/j29L9Lm4xxL/h39X05j/Co/yfV1Kj6bnZND3jiXuLbHUJ+BnHqbD1hqZ62qqLZi0orkyu/ioFRtKxlxcHLZAvTA5hEYbyjj3l5Zptrf1MIgklxIo7FwKPeYLl4/3BGAKaz7xCLLuVdb9zCxDwSiVWYwWuuJrZqYeB+oaZ1qaDnUs0fNH7jU1UQD5l1xsDVPLXMxBFlewSjBpeapnFdZZl5aYOrzKmBoqtK6dYQHq2aXzwzIAs0YK15lrQLtA57RgL5c4fEoLQPLL1OwljZWorStpHMAy9Rx1EDkiZglESPKWiWalePR2MZYe+JUpSLYoYxWYw+hVegXNNRpBdyyPmDBzLn2WOpq8xr0xPeVHT4hOEZwhs7JgHd+IPhn2PWR9yEYfmfwqfdfknyP7mhKjlj6MtTDCSuPQoVA7zQ2xdADrK9aOVrMRdgRC3URVWj8RxLpvMIl/wAGDBdXR9k7QIhKlejFy8TX2enMw9hEmzDcD0Hq59XU2zmXFJSCdjwT/pFTqU8iVv8AsQ6m0XQMJKf/AIV6MTH8n0r0qD0+pNfkjN7iUysVDc/A+i7AtuYLcNYrnm4VcQL4IHqAuzmV2SXpmHapMvDOVQUFwPT8BZdoSVdWSz3bYPslUR8Q99eaUr+okzqETkjtOkUzOLzDcCzMeXu/BDtvSGMvEz5Tb8mZmrkgkPDMq4jqjKGeesdB0qHz/wAJRWyOVl8OMzPBe6XDrxF0dCAGwNA/O6igqgdj4I/7csD3uVg7tTJ61HmLYhCGEOR1IZ9NoADgCbhoiGalpYti6zMLWcitl94sidZTqUAIaxUzQuKzOqZ3XzOYS9r5zDakMMCyt4jWOE0iRJSzmajA7yuqWdJXeU5iFzTqKRLlSkUQWCm5V3qUioHDGKqX1nM+0+mjzGXL9GOn029NIntB+I/n/ifUhzmrNHifY9Pzw7O8P4WHm/Uw/wANw2IYhlqWvUoOWJRwYmbUEOR57Rd4pL2Swrcqkb1L+TLMtrvHUXZHUVhrsi8xP+nDCoO/5EVt3fmBAhGOo6fE1PaGpU/CfiOobYeqevM16ViK6rSj3IL/AJLywTVPD+icsHlWF34VvzG4cErAIQYllv5LD8zVAtfhIxaVUeTx/Cv416Mr1r14/gkTE+tNfkjNoqjzAnW6MY+nlji1V5Xt3AcAorBuEhEGFmD2hnAzloKOj3mVMCyxl73AW57xcOGsb4jEHVZl5L6Mv4pUq7X18wq3QW2r6xIDraqb5iCoIabrMo4o0nSyyqv/AFwWPmOu2q+IUrckyl8S3Aphad5h1N/tHoRwWi5Xx7zCrMXwfmZ008jxLl3iq+peaggXW/7hi5FxdzL34crRLlXXb+oqDyDKvXKujzNv5vK9hiXKLyit93pMAG3JboiVF5sOj/UrBstQPHMVyhYXdnMoIh5LhDhJAy92GdkMjMA9IOMTD1lJluFXDCmAnNM0mu5E7VqCMQpFqVIs8yzKY00XC41xBJSy+8HMOsMIw3Epj3l9or9BSLZbLYsu595nE0eYuf4MTcqbe3ppDQOqitO/8eiHpww8T7HpXzy6rz/GgX6j7Jv/AOZlJURKxfWbFD5lR1Mnc7My/KyNMC1M5RXVZzEezLYRYy6vuGRlWonNQKwr7IZgX0iwFrxHeQHd2ZUy6/kSg6pn3DUC5UZxHT4hwe0PTj7H4jDcD1B/g1LojLn/ABUN0Tpcbx4hXA+Uzge2X9zFAuxm8DxRNqvfH7SKxDoRwMGHh+JuePWvSv4VGJ61mVKnb+LGfRmnyRm03viO5tKVOz+JxAv3yx1CABbZr3gz5M6WQ7ygMVCW1xb/AMJlZG5G2gaAMYga8jlEfMQUCrKq3xENt2iuDCO0F5ekeoDkJcKwuO0fLxN7on5md+8S1B0fuJ9zOx/6Ee4zOqlwr/Ll2UJWrqN3EqWq+ItAG8qsVddaCHYAm3Z7zbI1esUzBgbl5CBf7u0fkDwdbjvEAwyWL5WVPFUNHS4kgKXWr56R0daDXT/VHNC9I4lhXMsDzxctUKSlmyZjDNS5l2Q6uHALcvaWFWEuH8L9Ny0F0ldYYbmBzFHE3JTKXFtsmeCJek5csOSBZHugheUvPOWy1ly1lQDrK9ZQnAI1URxD8zOIaeY7/gx1OZv6aS8nifZ+j1el0eIfQ3P9nqHoL8n9TD/LcIcD+ZoqUyMBaTEN1iPu7TXeAREDQEtsAB3hLgniHAzLq1oICfRBrxGMVQrnRHBkUTMWzeY6kOfn8iVaW+TrlgxCVElVEw+IceyGpU/Gfj0Nw9BDvLl59GMw8f6z/d2IUMWwSsRN01KgS0SlmR/zU2PHpXokSVKj6MfV/hx/BjMPDNHkjqHcwcGWG/eYBOjMaltRihAaAA21/wBmwVq2dCVY0FVbHy5ltlQ4tjOA2No+OJn+2xhgXWYpAIlxUw3wFxhndRnNW6xnnmDZnbKH7QlAAG97zFXvlHviPTHkQ307owD0mcqYn0fmeBKwKOI8BysFflgINlClZW3mIJ0CpeiMJgKpR7CJVcSnQaicPYoK6wtAAgse4Q3jC+gyhqqitgEoH7n3KdOhLBGN9gKpt4I5FaqBQou4CAQBHmVrUAwHH8K9blwXWZYJKh0pbpCAyswGIQAzuKlDUE7S3TcR4lrzEGMWltxa4l5lvR9LzLlwZu7OJo8x9c+jKzN/TOvMYfyf4eb6E3RJUmCVKmYbPL+pZ/puaRpcdAEK0lBy1iID28QBYSm4t8hHaohbpCa1lYAhbicZmCsK8kaVql81qFl74Opty5i0RHmMYv2/JPsfzAxK9EzK7x58TT2TT02eD8ehuE0h61mHf0Zn4f0l2X/AjSq1KVSGNzZY+0cvEwYCLxl1NHxD9v4iz6qiSvSvWv5n1ScevB6TVDgmdzUO83eYbm8YM/LDR1UDULC4w1cEtx81KfXEJ6t6ndjsTiDOvvalw4mVpeHmAowlvSC2fT0NkC1DZAyqezChlqZ4hMHR+Zc0qIFr3UTI3xM28RV2SFAFhUBIXAD1mFABQHHaUQUUv3XdhbUuUlIeZlz8ksyIGBeYIF12sN+WemiC7AlnZG8lmU+BFsGwWGnUCXGLguyQuV6VKnvH0vEKQ7Z3IyCbu/QSmcoq6RVimZTZib3CvMHrEXuLm4dcEl6LGmNDAgWSiogyqcylQJ9plYmx5j/Pb00eSbXPvPQb0vIQ2R9BMEIeps8v5IMWv+4kunliEdxUBayAG8Y9mGmIaRC4uFZi0sLu8RdsoPSGewBwy6esAtsmpacGVt6wq6kz5jMQc77rHS6TBdwKWKiiqz7fkmwNl8w16V6uL8TT2Slem/wfj0Nw9B6HpXqMh/mIyy/4TmWHNQjkycRWZk25ZyipLAM28QHF4vzDf++IIVGbiRlSoyvR/g+r6b9XXpv9PEdT9Ec15n3H0ZPz6b2DpchcvKpZgViZ3dD8QGsylBhzFONqFwZYdtso53Cfc6ULMcRPHAOuYz6BbOss4hrBFUrMWcWR3mN3V4261Lk8SlHimU9ADWBs+YNuvkRX5ZtVLEAVFVekDpEVLjluBHdVBJDgTL3VgAcDXEpegBrF32hBZWNEYpS3FSlxTpOYi0C7rN3zfWLNCwMVTTyqiY9OZGCWKewZlUL4OKm/KZ1/GKFYXvNSv4sqBiVK9cwqskt1FnFy/KSrBG3cplRly2WlvWXysu+ZcOqDFuXzM3HUJ9t9DTzGoemvXmbzcfqR4QQaZn54ZaIM4+g/YwJUqVDX+WyO/wDTcHbbi33h8Y/qHlFWu4bTQu43M2vWPEUeAagwMDQG5c3yOc8RCjogF3V9IxktljINdZkZ02yTdzZTsxmZRq+EqtBVGIQI1wi6c4YlxuKRe35Jr98r136PPiaeyGvTf4PxHUNw3Alfwr1H+HQg+Q/EtmoqBywkbaqIhONVD89WLFKz1mc07tiA3xAvcN+vS1Ufr1ZzH1Ynr2/lxK9H0Tx/zTHUyIdJu8s2mXwzcdQD4MDPzDlMOI0zLA7kNFjErhRWtQpJRl2JhimrgcLqtxOhrCdKgOZvtioDvLvSXq7/AKhWvOccuDuzYUHeB6MgWcfuOxbhdBV0hNQeLi+D2ghEnhtC4us7MQBwfAjihgNQXK5gbKxqDYJjKDRHLqcOkG06rRxxMuUKmJdpiuSiBHAOjDhX7hU5VOw6+I5MSkslDchtDyn7lRJUSY9K9AxKlHpUqHCU6ZYl4pxE8vSoLC424iB5iXUVEYGZX8OZc1/D7zOIbPMdwnSPo+tcM+F+Zsi9Mv54paJviQPugYeWBUq/RUpw/wCXP9HeYrnmXat3NmE8E98ktlVV5mL7r4NQBCYXW6lTRKoDbAGIeWAlUFUdouAx5hBVOMMvGd2RlDDdccRAlvC1l3LZ+IXwPNTk64YDZFHV4mHiwS1pxsvklRHBhioTcLTVFyhtW+O0VVVtY8+Ga+yGok3+D8Rm0Nw9AlSs+rMj6f0lHkPxAIl/8jaOSMSgOG3B2hSXCzqVS1UamZe2oLxcvbHoaielR9DE9K9FZjGJ/Dfo+iekeHmOfQuH3Gcpz8PoqgIO8LIDB57xlLOJuo9PnMsHmO5dUXTkg2ZAUK31dQGZDFuphKtKjRTF0qENrUzVMO3RVuZSGvdKTDMiPLCNG6ZVstaCwejPFQyPlRrr5wAhXqpmpP2Y7aYSXb2CLN5fMVyt7w7bY2dRs3RoGKBBvYcRw6W7dwTHwXYOxUv+tVkHKmBgVJTRHhgEoqBRgjlNifMZvmo+6FHZguMNnlhdUi6el8y49UPLdGHNYX3l74qvRgGkWqcT/Ib9WZl+Z+iysSpUqMVKiVC09atlTIluIAgqzLuYcwDi4q9VFsg2J3EXmW7JqKhHSPs9Ayi7mEbGXL9M/I+hs8yofwvEcet9Z+ZtQZ/8z6f2Zt8zRN04mnyzA8/wDH20Ft0/aMVM2cQttmjmXtvPSIW2j1uKFb6usZGBs5hDAhh6RFlV7xxFVcuIROzPmJUF1ic0stqIggUVk9h0g0QGQnF/ogockZLdCvDMJGwBAxmKWLsd4N1RW/QSDhqYLk0+019kDEqb/B+JUNw3CaQTmBD0dzKqpp9EAe1+I1UYANS1YGy8SrqYwwIe7B95ap2fuMTHNS7lwJLj74+/6PonorfokqOJT05nOI+mv4Mr00TV5jmDEEN/mBWcxuq6IMRNyw7QtvYxa4Qa19JQ5fiHQU1bfMroV94sIYXQ6QFbUNtzCMKERuY7Wiu48XW+0PE4mTsKGCKW2H6LQuGrQ9Sa0N0H2yojjvvwn5IZ8jZnXff9eQLA/Z/y0qGdobcc18CPCCuEVzXjmWHoWhO+93EpJgOmXZ2hxUwQFHQKTvuXwDk2dqFGqutyu1CEbc/EIIobdvdN+0aNSwFPMzaoWukG1nRWreDgvN+bjNuUiRBt8N77LNP3ySYveiawkcVQriaiSonokqMEdy/UqmX6BVF1SLeI2RtlNalmMK+g7yI4IjqXl+sbG/QNy0VjcYyp9x9DZKzK9GJ6Mxfb0+m/MGPofv0l95t8zIQZSpYPLBj5/UJz9Okc7oobcef5lufMLzOYUtUXQ9ZcSv8A2AhLRaO5MA6R0i3er4iOTLzBTTpzNmZcpbpydyY5to5VegKgvPTbWfKrCjiZbeIi1tQQtB/2IwWGvGBVXWJAqaU4t1cLcuOZQIDd1UbNlQyWGQY+HBi5iHaa+yaen4z8ehG0CGp3TmBNSokaeb8CORcYx7ILdNalVPNmLATAy0VOQ64lT5GJkKkwLtLE1HKjPzyrJUYqVGMekqo6m0WPo9pzGb9U9GaZqefQRw7M+9E0R1viK2iHELtMDRdpl76l0R9fwTDz1VvobMr72/JifJdP0ImLWkEKVfY13l2ETSY6DlT+5jzHrzFDI+iTDrMtFPZ1VmNYR0pe5TrPXrHFC/xEEP8ASCq6hmkvNVGap8ROTXoq8PSUeDqqTK8sExHxMil5/wDVRGQqi7D14xHkKViniZiUKYd4s7OYvKibWTu63DfAQbZNXfBCmYpQ0cre7mXGICWVjlYRnCROQd4BbncO8Nkv5hJuBHUInTFbIvoBi0jUWRs9Zd1FHEVsTMuR9CKzhYinbFuX6VfpUqZQbzFkt0lTabeixxMPMzbBh5i7ljiWOJUrrBQxZw8Rn1k5n0D8xyN+82+SaYmXoGSFlu9fXoE2hDUeuXNzf8ymAQMAiVdRKrRaS7gk5uUyrPtNkt41NlA84TtT1UiSdC7HUS0X0uc0J6OosLIwBeOkVMfiPrv3gqsFiDCuvAQjUq24iF8kMVogYcF1jpMPgNrpTfvLtpe+dTDotFXo4KlducHTMjs8RgFqxTqonlBiuZmrFUx2niYMQyz8R+IwjaE0hKzAxA6yqYkHy/gSj3n0i6ZGviIaraQwLbucgsVhwRZljSx09IjBtpnUc0W7qUh6WKlRipW8xLiRMxiY9XErc49HX8WM0zX3lQ/hCad4cUORKwOlXW4C1FlvSJcCllFw673VG7dEh3vCxpgHfPciKExENjla1LIECgQ+yUJApA6yhxcYVyBjaDi6xcSC9po7voVDzKuEtKmKiDOBUBVOkGRmYsXbKBb1dTKGxAEqhTKb31lrnPlzDhdjqxNsLK90ULjGBzumNmryrZmsVxUtYQpmmPFWwIx6IvZz+UOiDdVjbXRlm46tNLbOaienKF4zYO4OkWgoSYZ5vUoCSKTJzn9QyhiZV/6dIKV7kk3hFzb8ywJEDaeSaimV4FWSrO1wJXWcysy3EaNXLOJbqRQajAsumHdIkQMoS3VIkyxNcMa8QlqX2jmV6VAqAPMyLG4wBGubg1zDMwlHcQiRjpG59lFmDDzNsTTUWuCPiUTM8TSfp6fQfmDBr2/z6e2dZ+UmmValdILYY2f8PTunVFFnymUN/p9QHOaiAgL44iNz7szjuQzIvNzktWUUWxrMS1Ac8zAGjkxc2XgI2CFwUu+JfkjvC7oeQWS+9xwQiFYtef8A2VvEUuG6bOWNe45kYvfEUbDRecX4ih0Wvu7Rt7XLUFACxjxBUthbh1DfsZ+BBiEOb4/EYQbhBZBKhqEYSH/Zwm45/CmLFbTfmVDWcMpB7wppbWGy4dEJ1io/cRfcmibvFzO/7t6CoE8o2jCMYTMYSDOZzK9WOpWP4MZqmvv6KHh7TLzJy+I27lTtoCK9dSmSKbxUVCWw8hGT2GYIsK1dZYW3aymKwXFqoBwwMPEYBeD/AEgZeYmExXeb1CFLerl9u0zIlM3eZXklKXmpjRpwv2lIuoYLcy3pIYgxy741GIDYc6uJYANX3QKPiOjlWoFHqf3CJgWzN35i004u5VjvNXiUgf1Q5dStkHmEdDVYrrjnuw7oigsLnPTzzKcnuqRxSc3LoxZDLd+1fqMRAUFaBgm+gmAwoiAcFSws1Wcl4lSgYLlZu9DWXpDB4KALJBqrTMDM9ZikYpJykTj0xjcKbT4idNHabCxHL6K+tS/SsypU49BTUW4IbJa5gthliWesFZmo1A6MsMy8ibQ/MTJj6XHvKZ9KLDNvb0+gjuD6fzDH25+QmuG18wwmWON5ZinRhGzEd7DZZW/9ZZF7sXgZapSE3tqY0ADSS2N2U9mOAgxTxf1MS6HVinoMMbgVve4rQ6W+YhKkAvG/1E2MbNctnKSu9qIl6vN8e8I3hq4GccXXWI2pbtK5Hr/UCQbqaBfFd+ITUq8m68sLKZGK5mnJW9+0GSi3OGz9S1MrOAlvshptTG4DWaUthrMELUA92Hp+j8RhAQenaMMmZWYmYIf9HCH/AG8JmutpnpKUtlj3hqFZeY+vhxK3vGjuxhyZdGQubKVfEwz1mfaD5oYQpCErUQjCRMxIAnZKlRMSuJ7TUPVybj6apqefTWFKX52HL7S8+8RY8s5gDkCrHh/cUQ87ljDZpQJ5gBwa4XnLiXEAHMOTxxGNR9QOiVVRaHvKvxgx7yjXfFypn0m7xKrcGXzFpi4ziodo2ow5i1HyBcKy1GxAULJqTZeMdxGHVCpZpl3Utl9G2MZkOW2PaL9yvFKqL4jHBgq7PMsCjLWY3iSyHeOjkW2qOh1uEv5dTdOsykRw2NxNWADFNMwqqCDkGUpW87B25c0Vu3CvHiAji1QM0BOuusUjc82+1aRq/LNpdKlWr92oFQUjfiIeIp0idokSXq+JUUegix6V/B/gQlxZbO3pcGXUXcu5rmOMyXuzefeJW5xI+CAozLGdReGO029PrZtMB6p+fRK3qIPvDBy+YFS2mfzDLKmTUxXUvNbgvaszprces/8AYgwUxb+Y8OOS5ZsL7ROQdrlnNxeaLTcpp8IMBDEADXaKZ9iyi4dA5uL6BXWALdjtDYigwLcY2rN64vUZzCcBFdY5DzCbFXaEzeHzM/msYaMN3hX+Zhqqxa9W9Vd1GS6wXzYU5wVVRGRKgnMYgUXlYCXkWmgeDpMDoVazIVIBKiqbHNO+8tAwVTxFslvV6H+oPYhq1Uwmb8RhBc0hhHxCBmJliT/U6IxRC8q9kBKlDT3l2gvEpRG6ZzKAO23u5hFCrJSgRABZKZU63AU2SqvbxLCLJ8kuxyD7y7ywFalukecVGnvLRIme0YPRUqJiJWo+lSpUfRyTfNfeXiYEPCVTd4MTa79JpgiigW2xT0i2jmZUAdIVNSKqKHZjtGiU2ml1uHFHCty5gpneOKO0GX4/MBZvN6lChvUV0ejFT8RXNmaJVKxtK2gEBcghcVhgyywQaCtGdQTom6qoag2z7Yiq+xlMw9M3oGWusyihHK7zuCKhvozPLMNH4MulbNt+MRHKgYPMUFiigXhqOYgVL218wsDa7tXu7RIKVmm7Yq7y4mV6XrfD1qWF0zd8qic/mZEJC1C6Wlz3hu1e1ppkz01Ku8rRbc+xLBQJFvj7QLadLdTeNfUTVFbfutNqXoURuC5sofuDkGOf3KiCKrd/wMQuEpgHonEDFkrPaJuyUjqW7iuB1lZjcpletP8AN9K9OYQPT7bMxBh5gzKeMRFG5klx/Axcovp9HMp9j8vQy8kw9/oCx8wwlI/xqM8S0/ESWkB1ZV1qNacXO3GsBrmUdP15AFah8Qo8Dlfdha5cdapjvVy1Q0qWaHUXd/czjbsTEq3XRHsNSIOQdYbapXWBCN1zMjbjTXEqhpmsxzCG7FJgeH6mwhQAHjtXDA1euygWhTTd5lmx1dvBLF7Q4qFoeWPgkqz+SBOyZKy83Cj4XW8nMr5VbXqZMIdalTDBi4KC+pBj0WfYjNobIHpJqYQM+hIYjHJ/4oJauXcWkHZUR1ure1YozWq1e5XUyclWuCJe4YRratrLbP8ADnyPpN41uZ9TJibSY9RZHfoTECVZEjElTfoxPRjZ/NLxNYWSGnuUNTvLFnMooLDK2niK8+sbTrxpRqMHLFi6bRAUDAVw4dRZKCJDrERuYvgmVxVP98y9NauWduiWWukWUfmZ3UWoq8E2f+Ui22oqxzXWHPuIXJ0mCrpFW96Hll7aLa+I7HYRA7GVYwSlAKuCqrFcx3PE6wicFdSMJLqj8Rqi6a+oKeTJuTsEtL1LAbgsCGAOTYZ1X2kq6YyWwp0LoqZVuiS2St0YX1ltFypVVrg+ZcyCizaK6hzfP9IOaitK/wA5lrQbTp/2OJLWUboz9wWmihd6/fMEw1hOntwXEpq0TmCtdqeTZ7kKFtTriG8RhdAmXDUTCjc6AnhRDVyjkiSoErG5v1r+dQXKjPts0TA8xbhCuIysSjwMzb+AXncw7omyfcJo9HEvoGJn49USi/X6oRVWRvAv1LFbgzFUp7lTrpKFbLf/AMIIzOQP1B4S7a53IKyA9pkriJ2ZniPslVr5nte7MX4wxrnrCjDRcVm1sazwz6I+gcQpuIQIQiXsrMcO2EiDFL0MJ1I21LlVdOD6gxW7LcovB4iGdqU8VRkCU2XMZsz4r8RDk7ama+GLHsmkqGvZHc2YbhNoHf0OZyeo3LGv8uEqYRGl+Y0SAaw8yhVcNW5Ze20ZtHXRrmMsG6HoZzCQXpqnadYWJaBz+TLvJEeIYxm5nDuZ3pD9OhWGJiBGJUSNTvGVuaj6M33NPf0rXlHh5mD7zrDTFjuKsQ4M9Mw3ikUGiX0nAWIb7szQw6rveZUlWFdzKiOX5mUdvxP1HmZDokyPEVg7RVHlmpzH8U/z9kdY+Ud37I1kss8TAd35Y682O/EgvzS6vGoLrxEJwxEsoLDlWuZerq+EdS5a5Yu4cDQaFuv+xm/oMHB7xjAGqJNh7RsCAl1fywGRKKiVzS9dNdoniqLSK8J1tgzKu29HLLdnMQK1wvQlBRBBXZcv9QxFUKOw9+txxUVQvFw0KsM3WLfnpC4qEWONe5khh4eTmU8Xs7jiifIOPZsikxl+ss8y0EMUsHpLGOGc4lQcHcG2VK3BOz6BjxBUytTeuYEq4wkEqJPsMNn3gQU4IUS0i2nZjEejL9GvRjYgp9xBkExHkjw9IfdjqP8Ay8EGu83h8SiFHSezAHUrMjAAzfFtTGIA1CrPzF6AkBHH/GDBURhdbLHcPSCGz5Uu6fNJ2T3P7mTh7P7hZkfJmOe6ZAwPvk/ErObsk5PsKC5vH/U25/ZAjK/CHWXs/qclv87QM7etpaU5dbwBhBrdxO+JcVRSZ27e7BgAW1yrL9zuYRXV8R9NOm4aCKMYzOXbtZRunhg+hBsmk/F6DcDMJyhqGoG/R9LIYy//ACJe8GZQ3filt0HSXsuGMs6VFFKRivMotbwX0gwOzmpsA8kqhmL6un3lwRiCprqbceIvNVcvIJcqzOkTI9Zv4lRIkTMSo8yvRjhiR3GOGjz6OjymAmfuj1iwxjuIQMAig4YiICixwDf5mVhc8n3jRDvH3Bh5mswjmRH3t/c88w5faJpnYl6eh2o8ExHiUB/uEyNEcPiYE9E1z6DHdOMfkytLHKPM7YqD+4ksWXxco0tXy8RypmpyAWuVRKYja7Of+QSh+KBolVKZvg/5BUgWUG+DncO2Bg5vvEBmZ3A5F81iXRixZBUuMnNOYTAWCkuYyz1ez/v4ht7jyV1/ESvdSjWX+PhjfKWb11563EC9K87B58THAZGx+Kjjykwfh/UDCtG6i21dmGVLqKZ7+Gn5iokr0YSu8qpSxt9CCIruNzdRNTHcU8eivTmEdp0EX09BbxBjFYgzEO7HUhqrrNuYFzDRGgeYAo4j09X4nEPT7v6lxevRP7m2LDyTOCw09yaMxf74Iqa+X9ROlfoy79j7TJorIUo6PiVaIAFzTG7q5eqvswglkVmFdUdmpfcbW4l5Huzl/OQH9KI/vnUgnuHEMYbLHaP/AC5QAxRs4aGp9satFBnMqSLba6BTPTNzhJ/vMUa8Nn9wXRhmFVX+4xO78pMPcURby3QLeAxDXjib36c0auZbK32dREHygo8CGoGJ+A/EYbhshOcMwzCcYiYlehZ/zcJVX3hYAF41CwVGtXDQLwJzlECAKAUZjuCd2VZMP1/LhP8AvzLsQueJfOJsxA4IVNk44xfWU3ctvt6WjHKJKiSoxLj6Ppu8z8k4mjLqvEde1sK1uqgaV7VDnX7P6mKW50/qMow0vmskbmjzZKlghgOkCARQWAeJZBBVKqW4ZdrjqzgWIQdMREi8d0COMKGnOZtF3/BiLlm82RR0HaUSef1ReJbUzzM29ICCN4GD4GIpXH5JY2XTMS08YnTqjO/aW1BsZUZczLeaDNTB27rpcMAULhkzNkPTQoaB/uB3EhZgHG/mOlVeOpDQ1TaDrfL3giyK9C2gAtNpSZ3FVu3MFzltDa54lOIigQz1Y4LhUtOBHdb2jiUQ0cgD3mwruV8X5l+rG13133lft0008H5uat7CujX/ALOACGkdu8KbMBojhm+626nD7lRd69ALlZqVNRSzDAjmZYEOYMtQIXUAOJXSVcqFcwCCh5fmNMQpxUXGJSRyiDHn201M+QJRCo6At6Tec5j+V+JxD0+7+pcsfD/cGcbU4s9P8EdPymkqHZ/omAP8VOcklukQyGjkW5PeYKEInYoCrdZgcFQI59LQ4gVHFBZTxeKX1issxQAbX2BhZdzqKFsNcESIdlMfU4IP87Sm/tzGjVC/DDZYn2xGx9i/U7lbpq4xSCkwtJhpU6XhvefyjZG0sUSqK4RG3vM0V9Fpjgz+osYu5DgHtTN6DExTb3lUzslkMIgJ1KvkiVsu/aL2YvaaLuJr4EJpPwES4bm0JymkNsyuGCcegw/6vD/m4Srl02cTPdl+CUOg7EOvyuiAMqFczpEP7RKjrPthVqCqzLE0kZd0SssJYUGZZtiYpmHWULqJtEZl5WVEiMqJPKeEcTljMlPzQ1HhioO4ZOksTAk9y4HSedI0YfsIfZMBrCUmBzbeIW2CL9nuhsATZFbizDiJZqBYL0tZmRObVmz4gVsaRdeYJEuKX9RBbl3dxWtMxV/gxKNzaPKFqhmASWa6wttCdSqgMW7A3FoCoMq/MToaGgwPuJ2KOzEFSi3qvMYdoGVX4mSYgUM4mXPuXDf7I6wGot2piIYo8n4lbKeFO5V4PZvGEhRMsUCnlfMQtAAVfftDiqNHMnbvCpcygKN2Yti8RlbdqIX4MSq86GD6lZNpajS9j3/cVgK4OuceJnDKZX511JTKr0WgvK8SsDtZRxwvWIFRJtyZOesbCYzKdbs/J7R2bAt/cG6zewv4Q7RY/cvyS2IzZcKhW5VxiZqmA6EXSoC2MevHlQWEuI6KhyBAdGaSCbJeGNpaC4aRwMoAaiDioUrLCp7REBKU+gKdxVzB8jMRMF7kGZZuGWSxZdXmWRTqJy9X4nEIzP8AzxEltLxh8TbFYOjFGU0D5ZepTtyvxHoaWtzKbBACd/q5YpYCBaWuZz2Ekmzp+WIwhbbl8HMz5BygZSotBpspL8P3AINNC1TYnkI5maiGPpMoHhF9H4izl+FGK8GpQUdmEgzEoUtRtRj/ADrFguHulAfJmB8kFvA/9hDtS68MYuBDKFv+IC0FU92XteuaoctdoNSrl4jkC14luKEW4UPS+BFuIsBSUhmcRTP2EZtNoQbgQ3Dx6ErM/wAFzn+90RfiUYwHff0lVks6wSoiRc3RftCQdX5YQXAVmZCrC5gwy0zBUzTNh6JXMcrOPSsRMSomIkTiJ6M18pq8zic43TtK4t0Q7IGHwywNwm47s1APdU2IHlEH7P6Rv/RF0c0CRMq6xjU5DxFrv2/+oBNXMFi/wH4i3cXMHKEO2rrcQYi/QPsxHceqn9w+X3BNSHuMBv6k6DJuF9kU5hwftcvLpjoQIpPBcs3wqfqCYBWqgOt1HMh8XO1GZyUrKf0Q0HbtvPJBs1onL6RfpCgsYU41hiewGPFAlkOKz0yu0EFqO2KWPeNy9sOKazWjHl4IuDG9d5rLK3Ku6dnQxqAiEuQSVnZUWlFsXJKUFdmDHUSwVDNljYnvs8w7CVq2tav7JpmhVP8AcIcIYbsvh+YEYEpOjPeU6yxElMtKZadiA1qVMwTAeEp26gnE0iHheZRnglUisRGQMm8JDL6WsbiTMW59hhuL5IYdROYkCQBen+qMMCvK/E4hGfa/UFVn+rtNswOeYur0Wl+ZfWAWql10/wDkNef+AvFqcdGKnbKtIBzviNU2vQ14zU3idIMo4aK3TFQMTQW24awM1y5jlj5hqCc3KzSdGDHiI2Yi6jS24dGPWfmZQ6FtFoijOugHweJTEAYX9RcEAJgU76QSqjvBQ0V5UaqusewBTVMTl5EdETAwuDy1f4IsimQZeYFgU6QMAE59pZQ3Yi0mj+obQcJ28EZqyo6IPaJfE7JkPMITeMCNvQ49HPoIRntQ+0HHWKDJRxBuPyYOZD3f1DmP/HSKtSr/ADidcoBfhr+4ifSX9wbfx/6lYcXKulmU3f7mXZIio63PKMx4qKlm+Id4lOUEbzHXoxPQQRLbiRxEj+UOHmHM5xJr3WaYQVqjBlD9S3c8YglP2YBVb8sUblVLNGtX+5ovLbGEqOdar9w6AvASoAxBTEzdj8R5ibmag943qMBavvEvW1Sz8Q0M7A3zQiRfP8xQMp2fthOF735J+pI1Ch8OgwNnH4yBMP8ABMRUpc7IPwTMlFihh8Re8P8AvrBAjQodEWkiJD0NF2AOPaCrkW8uD5I6I1At5AtbRei5gNhdwjVOLuVoU0Xq6CXO3a8rBIXNMMEZmFaAAJw95Vf0SqcoWAbhx0cBtthgSowdXm5pVjS6ZxEtptw/cVqTvlf8jhqTaGx3/vENsg0N/QRTC0ybE4fEqWN9RK1K+xzPeZlwe0vtKuY6wCU6yt+kygwwyoxFu4AOalnWUaEcRHJEt3dLJTkGE0iRgzv1fdfRfMSsxCWsetA1iufMV+Mldp9VgelTQ7/qZZRdrL8Q5w17oJ0x5fMHfzpoa46ZieeJhSbW2axxD4CC7MppTrudIpx6Z/cO4VUGXgpFpplmW2g85Y2NhpcLo1OxUU+harq9y2UXFfHFuPxGH4gi/tEaW0NbAqKRst0CaacQGSjQVDANe6MIwJ5tzHl+DLDR7QRCfGDSDSWb7QuiMDEqu1Sg8i2Ipoj3uCtiAduwp837S2lqAGrgViFy45gQvr6DU2juG5semkNPoQ5hKuW/xeUMd0xwhfdB0JOslDB8/GTB8oUCFLvJ+o2cntnm2HvfuCuCeSE7/ifmOKCRCBoc6zOt+oNsaSztOrHZU1acRttsds3ENajuHEESiJEr1Y7zGMekZu6XNDzLoZuxXkuYh2X7nT0uRggsS9QNZa4YLRYs238QJW3lq/E4pRag9Xp8Y/UFGdz7zxoHy/8AIdspYLVxkgTsxxBI1jgfiUC9BWxE9LjeayvqpfxDY4WNpxmWNVmA6QagE1A0ypHmEo1kaK3EOpwrYHg3HpSnasUK7ZSEBHRqCtRdFvaGebrtHIAC2tvmXOaVjhvP1Ll6QaCoazuKqckdr+It70CjPusd1skL4t9+kpzwtW9ExIOoeM/mLTEavgH7/qaWpdDx3Iw4WJ6Xr2jOirC7/wB/qiDQjHYYOLmzdtnxDMWmpZ1lnFy0Vgy2FO8ItLj6R1pa9yrxNYYxgWKXmjLHyBnRmsDU1o7VUWEMILobM9Z5huNQcQKlT7sJufeIbYZYFwyBWIIuTEviD5X4nHosSqoajiOS3rASxYJ3qIEWiHQh7RqhnpcvVHuRKuDPWWIfGUCGudkFhTW5twzuXCiMEHAQLlAhhwRu/aoA4ri35C5RHwo2KLVi68bhUN2yr8TPKJmoFVpXlG0K6gxbCm7/ABP/ACJQmp3giipXa8wrz8CYuh3lq4+cBeWKLBMCA3k/LEur7sWELeL/ALxaWmC1/eXbPkP3F8R1v/cHAYayjwitRV7rK8+Gn7gUoK6t+RjBQZzQ1FOnwJHRVZoX4olvHzS3U+YtL4YNly4uYzmBmamnodeggQiCiTsPzDoPzDoPzAePuH/ohB0CdAhHEPpBxWJyxE7RLz9wTF/ceVQ94ldB948zZUDUqczWp2iYnibMZGJUrtEYIx1GM3T8kdTdho85TU6ATaOH2iqghlghRf6m+g6Q0NWRdHSV4NsSQTyVcUbCFq8s9ofAErBi0fTA2+in3iQgNF3DtjiGh/jEJVIMpWcYxDM6y2rgGtZS/aXsbYYW8XKAtCKOxKRC/H9SmwrLx/Esw3VRuoQ1lV/5cuG9RK7TLOCBvazUeIBcuAk/EZQk1sMxRGBksTHmVG5kzd8RUclq+VYqL1tLBq8kwpkdhPH/AGaalrARegzG6Nhnp3YAIoCHmG0rwO9cS9txas3W4yaCVTvm5YAi9M9IsAWbVt+JugoROv8A2CJUGS69yKVSiIN4mVZt6/U6VXZ4itqxTTs7+m/SoHpYOpcuX6VMSu8rMGXkl1N0Wit6m/VrECZuG4sRj+YgWw03HxS9KDOiPQqUZCdyUrMfC/iX6Lljmoi693aVG7W/eXhYPeKmBeS4GY+CX/1y/fxz/wAGCcfGU8iI8T4l2/mlvD5J2nyR6D5JwV+SP/pI/wDsiv8A1O6jLcvFFdKK0p8wf/aZf3yn/Vng+5/uWGkPhRfKz5zi+xDJb5FyXYtfKKOX98G7sJ2iyl/IhbE1iq/qW5LfT/UQiwK0bqL0vxFFHS+gEckc1H0G/TWaehAhA9RmB6EshY0tZ32dZam1pBfDVe0sZzyn7g4+CYx/+47hkpoT237mpTvEP6kp/rnkq2qc9IJIi3AXm1t+Ioa3AA/UIbfg/pFXXwf0muX/AB0jNf6O0ZofOPS/KKav7Qqi0AA8sTFsNhZ8YJdhDMK0gPV0nEeYk16Em6fknCbsFp2CXVbtWZwM32jqAXLR4gFYL0hKG07dn3ECqcL1AXaSNksC6uVQNtfcy3VfmUckKS92agczmGk57wZ2EMHWDFd3aYpf/hFDfOc0lZ4zMyVQIDCUFtxaFoHyGxc1UqpbyrKJFKwnZ2xmZKqx2VFwnIHmJ9StQ5MMIg6N2qCN/mYd0L7xK6KabzcdZWxV5lfpgDE5OkVM12nwZYLPIahQ9QU0Dd3nMvoUQXjMqsLIAANcTZdXCgpnc+kFfyRVXn3X9EZyHpRjtEeaRgMXgC6yS+LTvl+ogyzuEXWr3UFwQTm6DlC1eqENqP2j8ktA3+mRDS8TEHotKMnmMA7PX+HHpUqVKlSpUMQgY2JeLlQnLoqLct+8XQeEgJhbYu9VXpslRxxDMMpquI2T7B+Zi2Xj0m0aC2BFL5oPiDOQT2bWjS8ZvETMdX9X4g/iOos3xKb6MzksLKl9HE2xKu8php56MF1+Uv1+Ue75SvX5RQLG84YPpBdp4egr19UHhPZK8TPQnxK7krvFEKOj7lHRCuiY6JiPd8Su6Y6pi7tAqFYtDMq+RfEKZfkIavrQ5PhQZohk2xEXFJk9pq+T0VQbDxH0G/QYmk5gzBQXaGy/jdd4QgQpAgSqg9BQkpFD4uKf2ZlF+6G03yzLcK6HxGu3xMIt3bFKlq8XuoJKqMNInoQ9DsVVXwDn+5mDsOCFo+Ud+ycxzOsT1DlZiY4J3MEE8i/iPEd/CYIekdTl5lXAfMAjvBnzywx5uf8A1GKngXxHZGYC35lbeiz2t/UanmERi1OdR1rvnzLCQB0ywsx2O4q/01GxCynOEIXPEsIeJalz456kzVJWHYrdvxODHZY4l3twToOI2Rhsl6Top+Y7IF5tMRbmhf49ZZilyLUq+4MpgjRXkSZNBUKqGDUOi/mXew2cu4lgVqkW6lC7bOK506cwEVsoWCNjXMIpI2Co6Xjr0zHYCq1Y+8wyTu3n+qAc3m8Wgbl4Ew7j/mjXPZpWCdb2JOE/AYbVz9CfghyUOzPxMxc9ZAUId2o+8L/JlqwMPBC5NBdXKxAN7AulyyhN56VKgXiVUrn0q/RtKgSoVkxUXuwcKxhy3MMDZuNOzrA0NM3pw6rG4QPQl1G9AXNQp9Z+Ze4KJxHtYAGGmBy1awUrkB9Bi+ppLdxBQR1CbdW/EMczql/DKKxdURLZbY+fTqDOcyVYpuW+Mxo1DEhv8zGlVVG4D3+Z7vmW7/Mp7/Mp7/MV/mK/zK7fcrsfMt2+ZboTxIdsX6EH0i/SLdPgw7PtPD7S3b4lu3xKzx8RO3wjfp8QJCydQxiqC5x/VG4KX++kuc1/rtAOAf74lqrOOA47Snr9RoXiORm7zAgQ0eJxCDcIMPR3Kd4+Yk1CF1+RffpFOUe83q4UgQLYQErM8JU+cEV73BDEsHRBPD8xq1BcRHONRiMRjczepviZidpUp7pChLCdbjseIRcxjB6N2aM/4TiCynV8CPgCvnH9xYjt+SbGcQ58wLqLs3eYwZNMlH/UICE6QOsShcldGKWXL2z9V+5i0jKNlNU0w2bZYtvmO0YNC7jN8tZRUV2IP0m2G8uULNJYwHCjsuIKEyO9hqqx1ywhvQPuGxnIfl0i7tNucClhjpmUOMqlrvHmEXwUxAHf9oNsZQ9z2hXHfF+Y5RavK9YNUrWzrmUkpFQdIuRBIGeFu4dZ4PmXKV2BSFy9cKQg2yJYtuhL2lpACh09/uKtkyxKKlxYrtA01R1fwCAUbX+vIwykm7t36CLGXDCPdLdZbCVyRqiFZy1OnQQ5WDo5ZdxjaE+IQ9NymBKlYlSr4gTEObUWDVVn9QWW3cnJMMWZ0L9ho7sCFIblkBzOcKHe6NR1pUtLSF6qm3niL22VQ/mGB6JLVLe9ROsBZJcKts61lKsBymGWhNb8vdqVdMR1u4mcqnEYczcb3IIKCytQg+CpcBddXUwHwEc0Xf1AUjTrEVRfUmfpdpnzMaCD5oJSPEp7SrcSzpKHiL2qW7SntKesp7QHt8RRyRHafEtez4jRhK8Suo+JSYv6luv1LOT4ncPidz6lLn6iPX6lXBZdiOQq7sLUFdgotbf3Cbmm8z8T8TrNkNMOXmBAlYPQINxc5iORrHjbLPhEVYHWaRbKmoo4mpFu25BaC/hD0qlSoYgK04Y+FWEfMDmI6RjjGBuLuGJek95RzE6xHrEj29G+sz6XziLuYeQmAPMNxmo6j6MWDgd5WIC3SvykVO2n9x4it11ibPM2Q58wRnKsdZZizXWJYa6oQ0jWb5lnQShxwPcf1Az7yuNALZ5zGS3Bqlg8X1lSl7z+Yafj8QWxN0NovWOh8Sh3Lxen5mJLb+w/TMWDZa5uLrV9/wDsbyFAIAClX3Ja+itaK4mWm7r4hS93euY9tdRrMLPLLexX4kGToP2xh2Fg27OlTbp71pvL0IkdkCqyK6GxqY4cPSXtCkdbFj7DMyRADczUYSgbr+YKLe2u0GX6KqFk7zMFXcZFtity5Vr2lEREWxODb4OekCVHe5T0VUKI0TlC0JRNjRcs4Zo77RUq9zcKUu65qDUK9swtZZFFYrN5l9RK5tla7y0diX1B8mpgoRlxQCWDnySrDcQYC+8LLxUVbAwbiq94d5FK1HbuW38xtZEqvmMCtVpaiFMPGcMz1z0lh4G+19yGlTgXAoONy8roQYG3pghV0FDd8wYo2cQicwFxTR8SsUnGoxxVXWbuBmC33m0cXdFTMpaYsy/8943V74iurzAUjyQq4ZhhO+fCUGomI9YFwuzGZPSJmU1VzLyy3rNmWJKplJNaYTmaeiwrdEERSQUGCcws57z8CcvoVhn5JcZgZgkMtBK4ifAMyl/EpfKBfCInZhi1y3RBWVaGc7lJu/3DZ2JdlAveB2Ow4tJpuahBdxZb6lrVnaF3IA46HzCMKLwdpUqV6KEbp2nyRiqHbuC8W9oeFUdYzdBfCupZaxXlgICId4hKHmIdYl9ZRMA94wu2OwnRKh5l1iMYSCMql1zDhnmf1Db6p+FgAuFfxLVCvdjVrv1j0DyzFp9/6QZf5n+oTk0JhYCiyY7olTzGgtxVbQUFOJiz3HtI+E/uARTzGOYUI+eI5LV0myXlvp+Je5snLGDhJSx+FW02DF3O6O+UqcioD2ZThxWEIJr+xHZK0HHtAD6Qh/z3E8Rflgowv9CMSG2r5S6U2BMQqVWW5YC0MqvmKLZHMCvBY1jrRqETejnHasoJuVSmdmC7DcoGQ3VaSVBulBpS7d/LVwVa1S8N/PeG+2LiXRBVF59BKB6/ccbPsxLCXeYLcAJalqHIjZ0xiKiPVuV6H9GTYgOHNbqFrMgIYoWViCprUKYPEILwC9DUNRHDobqY4RitXB2hZQQkBXeau0aMWk11CqKV/JL3NahRYETGtxSz8QLtmJYY3LCp0TPgKUC+64IV806otRsLLKsnbREzLRFQPDHtMSer+EfdaiBnBl4g2fJLDEwj8tkUpLPmKlrkHAeO8rlvJAWJbuslcygrJvEGsg4fMQQguVdSuFALezvAtYrhxmgikcRtelYKqbbrb/yU3RLf8qUpux3h8fuyzTMGNLv+3G0RXDm9yczKoHSaJualZlBe4FQNo6mW5VN9ZuWaXEQuV3lYczF7iHDMVv1vOYty8zMV2ga3cVw+02OFmHmI7ms4g+0OIMwaTZO1K+rIiBGwdMGgII4NXuDOkGnNNzNh5Xa5SL/O7sZpEoYIX9g1bi3NniOBpS/uQ1tvT8qEAmIAnrqp1cNipqjlj+2N7HxLIxrTZ8pZA6nenvvtNRlyuYQFw6pwohDAh1AopgBAonXJMFWIdSYLHD2lymveBwwq4vdPzGDjgl9ozUW6Jc+hj95J8t9I4Qweh9HRzmVBZ3P5CWdMX5Ydi2u8DR7CTu+aUbmb7gGxMA/jg14pYOXzBNGLZ30/gH6mFALNt55YIgrKRy8S1or8H4nLFlht9A1Ko2HqEAWgp9pX739S6FatIvhmyS8PxDl6/sQCb0fhiDqvdF/v1junpFGSHw6wlNWv2MK3Qh5wKzSDvUOnMbZva1GGt/RLiIuW1lOV2J55lMrPwn/ZiTLY13+59kb2+IYKWaEVbyZyrjRApIFhoLb85cwqS7cwoTaLdzRcdA0DUSYpaaDJHpZUgrYwHjNaltiqHjpLQYiqvlhXNtmv7joBLWNUswWFmnOCr6xXi4CKYWjY+6RLCC0VA8cwn9oBi8vtAbRkcXk8ko7VbV9JkQbNy02tLgZ29ojcqxOeJklVivpUGIouFHS7gZC7nIe1wKx0lKcZO8FSabBi2C4sF5N13mBVNFrdb8RpW/dh0DsBGEL0EW3vCEPeod4QugWK7yqivN5rBGwIp3rwV1e0OCkC7pBc3+H7hymLLekadQS2hSmxHj+o63Q+RlAYTFNJCpyaqHXOsidOkPGpC9i24WbKsDhbCbw5qPFKvY9IbYKbG1a3LdWgWs+COS1GquQ6sFatXvALBZzDQTOLQoh5YAcXA3AzMd1d13i8QbGmLOE9p/zDLDX0M/0GY8J7QHRiY0xHseII4T2lOr+I/wCiX6HxLu3tL6xLI3UwOJdmiUHB8RzwfEvoB7TwPiWvR8Qpx7iPb8UocnzMshFPA+YEMk8IEMvh/cDqxnKvrHme34jv0OJ+aaTaf4O7GoOsSeTxDwH7Nig29FMp3DLVPDimt30LlGBtMwIMmkV7wqyj8pTI0ll9MQKmBaVpyKlQMlZnjKsGj0v9RoTN3KhYguW1XvRHtD3VzAXmHLAOIB4gwbxF8E4aA6IpLCUx3jKEaMz1b6C3RG4YkpABUSlu3mW8pFe57xUNy3WNzM9o/E4m95zME7z48ZoMTYsCxIJsgweY8Q5XKD+WUoGwH1EmrzPwMvEW5XUpsrMEbGY4pdQviVCacAMOKX4wX+VZ8hHh0PRCjuzoYIWZdM5grc5p+p18RbfQno69sdm+YAIrZo1qKjXMUeOVE7H4mG8fkjodn4mcDX+u4LtZiKKcGLIOf2EForo8gZvHxEdSpY00xbksUo1uEumhq+Sv4WISDB6qTmgPmHVxdC9sruE7zXovokRqMisveYk7GEVY52UXK6FAJS3HYtJ2JeLB5NscViFFOc5j7yXDgFq1A1LvciyhWRYLe/eWh25Rk5XeudwuJ4ygeVV8wLiQUUANYFoIQldXtBp53ftqU5MFvKOy7VSzBjFTBwEhRdgxxqZYioswg2a8efSBtAWCOTe3xMPaYh9hoiU5AvOJncLcrFAQ82OrIEXtHTut+I3soQxXu6a4mWl8AvC7Wo6ikCV5bTDdN7ImtraqIppxTwBDZGgoRNtxMdq4BUK9BSPOpb1XAr4ucdBWcofMmKDqV4CEUmDSMtvlsqtc3MlWJxFBUUtxrzLVEENsnh7RFTSXNWUbXnhgC5/kBe7XrqBd8SjIQMcX0v2YIQwg22ZK4wnvMtGvxghLnWxcvSExOEK3W7jnERaSlXKoiPS0PUw1REViJakOLgGNr2tTN4DlYa6JpvyTR2t42nL36wKq9eRNO0P76QapW+ZgaXpl3EBmuUzXSLIRCra1HUcq2YiAm4qeLnOqDaPgK9FZyhXfzWUDmQ3D1Qe8u4+RirbfW2GTb3YDf2YgdIKCK1gifP3O/HqSrllEzXueSc+fmef5hor7i2W8V/UaOTrSKmY8op5fsxFG92WatXz/AFynIXvci66sr+1Icwic46qQZsTtAvu9g/ASjkFUZ+CNdIFajz5n5vSEoDp+zLwqJaw1rRtIxV4qu4qp2bu4Zay79Be0Yk8Gid0defiEX0gi3bLeW28QTSvLoo8jv8wHoEIy4qGk4zuoXQ08WaZR9ZBJkIeRpUuFqrmNBAIG6UuozhoDbwAHSEqu6Ff1Bf2ksKvAbrls3EECIEet4iDEo6gAWx7mGLMojdV8zPtPOeBPGdxLRXKRjFixeIQt6naWBGHgQiy9WhxekBdAo1luM4fZ/uK6+sKABF0s6XLJECqrdhWPLKdwaWheBeWV+UVHszA+A96CGVq/9TSfkjt4YuJe5fShRWMSoILeM1UIli014hqkFNineoGB0mA6B8CIo/zMGzLXYfuBdFVWu3cRSsCz5zCIYUR/D+CLuPoZsgpLwShFj2ll20oCuqsN+ZyEDQx4MIQHyLGpwoQmKdxKAIyPDtD7V7VU1v8Aty0WRmmIYKG6N9yopIje3MYIWsshygRwKkupNdjDfWBUu0wKMvehO/mKRLNo5nEnJeKQPMNFwgP3DPWNWFa8oLfmN6xKhW3oveM3LJyg4dqXd28cxtztNMFm6rpcpgpsbI3asvPQAqMN1pLyD7xFbFth3Q0XmIuB1NThMJ2jQMSM4JbKDZoorcO8SAgNC6mQGVao5lYDyjsqAZrnsjdUaYouZh1FCm7zm8du8oXjivEGoBe2MbLdmniW7yMbw8WxECbdeDLl7VAAKN2aT2hRnnarTQ3RmoJgYvQNgt6Kgq4o6lANsqiqt6rmUxLAFki5H9kzusBFoQquyCWSoQpAlb4R59AUiObbCvM53UMqah4KrH7hEbWrAKCFFhffMPRNOgBYLT2le5VVCgaUosHiFO4S0C8C8xXUKowSoEpkuFmYCHBwdzMmC+IILgemWFMOyPVWZV6YiTQcge3FeY4bWlxjmBeVwczRAtoXo6RZ/cYZdadZVyww6ZlTnUmM5eJi0hfiUmIVOKiunGJe465mDiFEareopEVVy7xcZfvGL6Evt6XL7QJVwJRcSV0IdRKJWYrOkFj7oEXT1lLb8ECAo1jHiIzWcM19/SOZWXaWheLrF3URMKV8nn5lgDLaHAll90azcxXYN0Exhgi8HPhdMqrMnqALHg31iPAlCVQPCnMNC4tX4H1m4isJjiCHtLmm0pZeYl0VEVebnPEoV0ZU/KNMnD8xLQLbg2gPaYIv4TmLLzFFcrvB8y4LrB7xCpzDtFQIJVAu1zdFOYf4JQAl+TEXtFziWy5vqX8xwE4Y6lb7H4neBo7ssI4NL0jplQOhMn3S6HmdyEPuCK0fhn9Szexy+jb3jkfDHjliKQUbD4JyV8E/pAlgxAo7sQbNrFWkThVK+GbbSzhf3HQyd8rg0YMxi2yrtivuB+CLvxHUugW03Ef0f9g3KpyVMHSHGWIdZC3YHtZfzCscNiyfa2Uiw82ICCNAZuF4SqdNwe6hWywdxa4mJwKbQhNc+KVABhpvSGroTk/uBQN8hP3NIr2/3FlCvWsPJxpYcw+p3sD+4WOVdaaytPW9QHR4DcbR8hiVj2bhTTBF8mVf65wV3EDOqhCgBXkIqgvRXgyjaZ4YtVdw1d03vMIqhSsi3avKXR2ItG2ymOF3xNUbLUQNuK4uNr3wY1eGZQNI2JwxD/ArLIdjejksRp1KzDODMLNEa0TPnUWaxt1LpkPMGYgnM6uGDWMsFtmHdgqF3zd0GEsWmNOIAu5UBa20GAnQXvMslMZbqWFEhzK0DELB0Cr7ECvOBdxCZz5iF/qAgIQcsYvhGOQK9JAXFveDcF8TMIoV2xEaFUrzmYm1XgIUCkui3BKCQItX7OsChbi9QWo3h/MZgXVbWRh2yrlmdfcdYzHM2alUUL91UAVXVlzMnAVKASc9YvWFKO2XeFVHPTH3K/wEDegO3SLEw5Fy/iWNF1Dp3JmEOuSyB1i4gTd6EeCZNIYHoOU+Jsp5l+JSu0T/AMx4pleiVgkj/uz/AHZZqQfmQuvogj+hA+HwgPL5lVRTq+ZSuI5VGqaGvmcgA5/pmAmHl/E03jdAH4grzH4jNJeIse/p5lAdIncV4VLtdJELW+dEGOtw66W93EpAWENDWr6sUbjljA/uMisBYkGdHXzL3p1vL37R1rBpxHgixKL8SublVZbOT4XUxoFt0cS1+WAqdn5j2rrNxxsLX1KBEEw4igFnhRq/CKcTjj9/AT/WkGjM66GMk5Xs9iDhrc/zIvAuFX3TMJwpqKCEVbHuVoZs24zDkrt/aVMJ5X9I2338mGVoC19RY7RRgKw2v3MdCaFs9k2DxeesL1+Y34uBeWPsr/aGWOszp3U2TYvpFoCwX2d5o3at9SLcqr2hkGvMFDy+MxZo5b+5RcTFnSbStLpSJgtNZ0K9lRDmUcvmPQcvG6iU2oxkYBkbq9zxIfLLViral8IZUFWhiYdn5x12veX9e9mIFp3Ba8H4INyrJnjVlF5O0OCy8wefSw2nsp7j1p9hMiw+YFFlrRmL2+0UN/s/uIZE9z+4XZq7Q/8ATR3q5WtFvT/lL/HdS/UBsfLgzh+IF59BPB8CWtEIyGBPgkTP+x/cLMB4/ugd4jXgQs1V38QZRYqM04zuHgR4GKKIVyrTzuNZxY4V3qwrWN4xEhJQBzVRlVFYoNu5i7bqBgyWsZgROJjPaBsAWbyKsO7BQW1Ysr2lKBxzBSV3CFFnVcVW42kNMc/EAUqgMrbjG6b8yvFWortbHnA9opyvvHBLFi1pAk6cwvZquvEc7FeW7uCINgLPKXe9QFaBzoIZUTm63uQL97bpeFq/MYYoYSqsNG50MrjCBJbMJSirfYObihanOGLbOjZBMFLttekQRYDwHQ+ZwOgJutDZWKO65klCcwGe+LK7wEXVkhyYusXKMtXDphZiUKFfiYhOs4wWXumGNCelQWdUMXPQJsChOApm3cba0ZOrt2ipXmXzFQiueCVa1rvAN5ZgOOJUuYlutzWI4dJRm5Z0HjrBVe5FXcmQPV+EBnNOZeNSnf5hyF+YPq/Mvx8kSwfuz/0Z/wCnHj+ef+xAYAFfgQPQ+H9QD9/9EBc38r+oC585/wBQrP8AieJftfa/Es23w/DKNeaCEV09hf3NCDajR6YNPB+ZWi8n9yxXtBk8Zj9Nzm/mae/qeCYRQNBloyvVirRathxASRW0qi8dIytcko8b8QjjLZVNOO/mLrBT/KcI1X3l4XNNsLrcLI5WZde189+OJRMFtL5RceiKQoQvsT7xqMM8/wBkDGdzh1m1ca2IJS86ijxP3DqBrT6L7IdGnoXvglwG6WB7BALJsHr53iyPzJoVOqQfdLAF4Icmk2XqVs8agRR4roIVgXdjYVUq5TTIXlSvuU8BYoGIOvzBlK4wksikt1eSrTvFJlE7IIYAtdZwFVKo0UwTfdOojmWabiQE6SWNlq0N5HZArUYZuEd6Y4vYAvvFjY10WDXWNUx/SKB68zd1D5xFpZekA1WZ92bzBOiSzqFklDLjeEPMZKGqEfzKx90J1732RZUG6fxh3CMU6uG0Dk+MwCWwuIikp3BAXOrslBofDEfEFdEd27PwTl4gWwrZgQVt+CD13WZXpqMzi0fEwM0vR+YAyx2gRhxBoWlTR4IZ1epgy17xabPvE5VPMwKvfmKW6fYgvY8iXV/BnI+PCODl0QHBBV+Yr1ZTebIYzaPmGoAEpsAPsNQvvxWAAogxavOxRrdwUFt0UdiC5lmPwttWOB3is9WJYbmOLSwXQypUKKUHmuIpaVJjpAwt1ZMHJ4GjtOksdjhLNdkgaGxYUpDa8bUWCMwN8jQG9yAyDuWTqkBV4Bx7csE0A60cLqIBGC2HkaDim9MT1nWiyGgepriDMNh6R/M0rXv7czPppaLNNU2rjUsiraOPNY3cYm8eqpsHPN9oJJNDC0TC3R6Su0SNzZjVPUrUSZ7gMKZFqWB0YM41ZpQ2Ls46wDAT5aGsOzlrtC0Bbga6ZghSiA7lwZlWLTq8yOxTaYMdY4I0cyhRn3/UY7C25SFBKw2Obzc2ScdcWgWt4Js8kGQ8lyxqNJi4dw3KbKLFXVArQxASgogLLq8OY9Im2hd1W91FTNN5a7qj85mniEo1G8uJYx3iFKbIZil4GV0Ia5KIw5l8Ea1HyjCE6AS4WAH4gSjnmZN2tQVbeJzdyVzE4/4omJT/AGoZ75rkHtK7PxFuI6yzmKdZZ1mPQqYlkxAJRKBgEoZXiGpLFZiB9vzEVzl/uYNsDGZvq1FmjmDEr1dQwGY2ibsYoqMGFlLOpKJuY1wvj4lhcQJCEQZXz0iC4ALQOJlRNy6f4YQSoIzC454ipQVKLJEqn9zWTaWUs3BvnnUTM1BEFEKNabi45IVkJpT8OC0Ud0F+gH8k2a+V/UokHlX+pazhwhR8VEQQnJ/TEZutr/VOZv8AHSDr/p7SmNoLxnbEFsQVXRTBrQcRfXfVYSe7BGYrrBXtiryr7yiJYJRL+4PwSle8V0KYvlG/MKHPE+xP3h+MfcqXAiFDtKu0iXDzKQdUfZGwKu0KDtUwdNHxEN07vvFz1RXPWdMA0XfiNzwwi4bFfUFais3+yO18cmAbgum3xMCai82UkwyUE2HpE3DmZmGr934hAGJbXGlAM3BRfZc/USOcJQv5IBoQyrGY7TTdKl/MRwuJdE1WopS2pYNQQLXjZYZR/Evq6jZksy0hywPli7ubdPIKRsI6X6hUTasW13jO25Y3LhXzPOJb5RMwFESgC1YJC1l4rU9ofuJad3M1+41O00IHJABeKHOxV9txFmq0fNdVKEdsxJdGwTbbCwAxAp3R1msV1ilnIHC3V+Yu+ZR9g8bQAu29XxmFEOJAigBzTuXjV1AqK1QF4jJrFjWIqg89AoELOUWuLqMa3dV1BnMwhAQOUvHMxKwFRG6ac+8csNPgDa+VtnWDetqZbddM8uXrFpmRwuxV3dpviLd8TSJTdVslziUO8e7h0eZiqhEoOcW5YltxbIFrRSwPE7WhwUCmHBWR6yu8bdyQcF9cxACijdL1cP3gFG1WXUTWo2cXG25pdQY6ghY3gq3qtsLAcwWups7kyLpmIAFHHMK0ValStFYYKxlGHVs3CyHBf3BgrrGGNeQSxQ6kW5RACpZVTLirQ6EFdPQYrbpeFYqUsd1iXdzF6tr4moepEWhs5/8AAldEho8wC0QFwKHdztPgn/kJbu8d+9orv4YV2nvOv8YHc+1/zDk9k/1P0h/VGuPvP9TLq96b36+fhR7Xnf0ZTFNhxntUNRWvaOSoQNBeLfeMMFv/AGXcr6Xy/iYGRzBl7emnvBj0JcWkCxuUdQ3ucdDR0lYRFovWYNEKqAvbLmdeVYFjw7sw2WrHTKCU8ywPiInbENu7TopjeWBLjL3DJr2l2abaFg7ai/3D/UtXC7h+oULRdoEGkKVUOMm8QaURVd4cv7l5WU7XcMQQhQVJkZZ1gpmh0QZtfaADOMljGiOQVwU3rpD3K6QBZGlKN06QDYoYLWiAVUxkaG+faI8AyzmS8RBJjKukZnaVjLzFwwj2tYhtF6fiXRGlu9ZnLtLoHYjymEdd78JqHLKfsmE/4swg+Zpf8MUq2xJDtG4Z2WwVzsrpCFC25yNsbKboi7Lpuz2mbvbEsOL5E0CD7sW0eYtiHZZiGhqrYzcyHFY+5s+kcjqQWsC4Aw5I7DW/0RlKCIolq2w0Rmdg5I73ncys0EruX01kh2zEtw3o2jumFBbNZzirlJrj5MUjmeNC/wDkmJEHgBWYspL/AF0guiaSLgWkSul0BsXp3momVLOfDEFPGOYSCDwKJt6mtBd3VcVCSpyCP1BTElxqoFdBfohBEdAyk6s6RJsSAkxaCsKmKiojTfmH9urEaF78xc/H7iy6K2vBcKjFVF61z1jsKUoEF5HU3EKqUB0p57zGG1VjKtlV3iZDI5F4Ytg48DG/nfMx1hJSd4kGqCqVAuz1c1xcxVjauHX3gJbAM4eUhGRfhDLUHXFn1Mr17x1mJIW0LxcyZFe8wlZ45LVJ2tmKbFCsKB+rmlUCl6Q7g8xujLu3MLqOiorRRoIXqwGyxahksK5qKrdzhoxM4W7LXeIyDDjY+ZSPObvwhMGQFh3Cx7QB2BkrHquI5cRgIibHFRfaVI3ZXzEgr01yQHaM5lNAUUa3z5lXrUgN5NFy1IUHjNl8+8oBZNGnMekx7NqBNYFx3lChAY7kWmmAgCGLHcSYnqqAPqW+8yvSk5XDukM9YLVxUGGA7SxKSMXsF3eJZuQ1Nx7RjV1JYQ7B/qia/wCdQwPMwzTeKlOgQph1XxP9idj6ldH1KeSYJlzKP8yj0+Y/5cL6IB3RAQJH4IAq6ose0yt4GMvRDDz7wfK/mV8EeR3alm/dJsJs8ziYHvNZVtsd1FhUKowipgP9qJgGmgp+JSH4GVz+sOKmao6jMWh1HIsK1XYY7ynxUWRFy63NxIOUAXYlkeRIgaHXvCXDibxQxajgJQU6yfiIhPacav8AEpV7dNmjEeD9n9RUJVGv6lgYe5lzBqcSQRFLIl0eF+mbD/J3gvfiIh5B/vaHEoXGBoRWuxCgg2F2mNzHzp+4rwj/AB1ghj/V3lHHjlUtB85bRCCBHEpAuWc8Qej5lOsGeYolAyoIIxX/AI4nEOHrxGjVzob+JYY4i2HiHNz9oK6wv5ZeUAA1BR2WWQrUormG7L+YxdWhq91FvehKw3QG/GaISC5OeIhLUK1bcFhA3bdot1eruVdi1hKbG9rX9Rogl1Y94TYCjBKTwS8K6wEhQC81cC3WKTnDiKex4gqj1mzzHZ4Q7HT9CYoMSolhYF46subvlS+hfaLiCQUsVCneZWKklVtjLvEOMSy53y7wjMZBUZ5uYVbktO6OcRIS2AtDjXaNh1Pgu1L3G1AXOC/E2BqE0WUsTMQgfJmWDnDGtEoFug6z1mf26ckyqbZa5/y95QtlVFORFzDQp5iPUX7hy54UIl+wCuheX7laGAwk6z/ctkKPUlgB7AhUeVowO4SAjZhxMaCKlDYjkZdfBVZynmGQwZpaX2llWwzL4gIAIQaUdK+5hk9+kWc5FS9iLZq8rATd2urGbVV454j0uLDGGOrbtbKqUsFRQGVZ7BI47F5ZpMcAwGI2Eqoji2ZaV3IgcvioLfMS/kaXB78HMtq205fnIWYls33TVJ71BFKFiiTnp4iPhASYlTqdT/kWSkTVSsjhTS9feXGWC0+0xCzsZlq4KgW2LMuMkurBW1H+OhMUYryALgPgIGDYj3IwthI0oWPhEjNVIVVa4mcih5mIxVcgWlB037Slq6S0bTJr2ucV+jJKuLAY7SiSyhpSjlvmtbhSalEAYCXY4jLomiNEAgqB2e0yIAoNCNhvjMpOj/SNKg0C2r3BEQCgqh46yjx9oEBDhwpvydZavFshGjBxKH8QfSDCd34JV/jpifIQ15k577iYLJljpDa5TpNrF1PzDV9kS7XzOqfBLmVvJm2W8iZiu6G/gywI9pjVN/3ysFEJdJUOlxfImkefBl2ROKvFHvBmOv7Ytuukrbyz6abMWE7k4mZ7+gZLm0fMSgsDdTCU1zZb8VCDR4UJr4KNY+fOWvmn8kotFVfmoz2p/wAtSjVVWn8VKINpz+EjprxvysWiv3/1Hj7Jzn1/3tAFJQRTo4mX+uEiT+FN77wf3Ff4vzG39lFf8mclnz/UEMRCa9yD8yt3/j3l+m8J+5drxMzv/hM+wYP1FVIPlOVTzcvxabOXtCItpnFULPm4iwbQsDoYW4R7Qp2udqZVWjGhJRXJL7kxuB7xDK8mQzogccMOIt58R1cKUOKQaNZZjKCN24xERmCmSJqCdZIjVuL1FOfhFrjCAtLZcJ0BrG5Sf0WRbBcWhQaDsYGnA/XsfqBIkpa5sbfx8RuQ1g68sR1Zbex8sbE6D6/7HrRFtrnLBAf9d5yPWaXmfERDb/AlFtqoFWVS47bwzRZpO70eJQkSSqrWfeGTRJwQPuYeXfK0F9UsxHV8S7vk94Lcv9IV4jYX1jV3RgU1cQAClGLc4gHeQ+ZCanbRtb/qN/nEAqz/ALpOA0h5uhmIV8iW5jvCpq8leZuMQlDHISEKWDMt+/zEBWwvLCAdiH5SnrAhqcDG6zkytrrMbRCUGlOc8S9vdigzvQud0RSqFblLWHF8TgsJZKAWp0BMqZsNMcN1WeNzaWV3ebj7tqbFArZ0zvzEWhawSg5mmVVvddow+iIPKLhfG4BFUUBRKqQHa7q5f+iA2SK0uladCU7LlXwxq1g0XVS49yyI4TGoGuJrpPsx6nZM3pOC9SsQZZODoXy/QwehRUvZkydP3FAIqHg05Tgu5aQsC5tiq47nWPjgrVpwjfyRKfzV4DRg1+YR0ZlZnPc26jTRW1K3p2gYBoJnlyV2gyZSD7vCBn9w9eWC6OclZ37EFYjOi82HO6+5aFsopbzjx9zHNNb6G/J5j3WIAJzAELZf9JakcJSNGGa+8wL0YbA5MuG45RtQiX0Mq+IXm9lvUM4vGCAYlKFM5X/SEse0qKcq34iQzMJbcVwd4GmLBGx94ydHFdYbr/1qDDKsr1cJcS1Q7RIUTV1M1nQ1b7QP3JqpsovvMIdQUmY8TJ/EVWXHbO/6TAf9xGveJQP+MQt4WUAU+YnYlDeFxsh8iYhY+S4XOB7Qq6IKyD7sAECPW2ItP1iir0Mn/iFizroP6jRijpT+oreAxHEwIFN3zRn1I9ov98winR/cGV9JYrUX+p9JFmZDCa+8JzgZqKllzgJVhwOxEvTDiH4iXCQPeLMC+SagWlnCH3j/ANeW7g9T6R6p8TunxPH8RMW8tRR0iGKIo4PmFd/aCc/mIefzO4ndfBAdWRdF7pygeHMiKofmQv5nVHmmC5fLfqKLTyf0Sjtv8cT9YfiQulj1BXAjAO0/NwRgO1/zLFCyRUqhbmH0Iv8AvDRCpTZeITRZhcGJgHUH3BFPFrKZ63GDLVKK/L/MGL3h+J/ENMoKJm44fI9WK0sMwq1bF8GNf7b7j2N/ttiOTZiPHmDVZzEIUVodYZnX+iZK9Q7xGrEVE9vzHmyLm5i7CLGVZ/RGoZiWpqwKZ8yz4sKKZ5p1uKILFFgMG/aDtIbEXMHtc2y2JEqxz+ZQ+gqAFnOHN9YACAxKAOa3wQNlNFvRvo7lQKPgivGty2db4jJVc/m3MiByti+GVmxQtd4dS5WwC5wd+0d9TSwb0N5/5AXNuR65j4SphDOCApFmFJXyY0cvrL8EBCyrqGUJcEA5OCMdVpZfEOFfEtiRwlQ5RMjHezWb5jmCoRktLsTvpjhvq0dpdveIijihWlvMQRMTJbowOqffbBagW0HEYXB5sEKGcALcQce85nTupVDPvL7F4uQRSDpmIDZzxADADoZXpmn8zNgm3YnSotWhbiOlGOwEvMYKqxHwy8FDV17wLshY1sya3zGRoJdpdHTgu/qChKBdW/e7iJiNRYuAjRoMt1147QBIWupeayuqmKFI2GQ5e0MF7uheM0DKMyBo63jxNAyLVgz35icAUIWxn88yrQp5PDrEGUDsKaevvKGMpXkz/fzLxTW9VI2qd5TSjmFNQrqgtq14MzO6q2pcKXh07otzWKOBd1LhwBpBqoqaLd2okCqJgmTut4i8FGdS15WVOkI+zOQKFB0zMRdvF4JUstAhLozcsscEW+tJlIgkw3OrBcTq5hcNJcOoM5zFf5qUf56grzENI/4qXYeIOinmJcGAyy9OIrargYtrrOQYqWVEdx1tbyRzSpUQLzFJYs3G9THtxD7M0Z9SVFsfb3jrHv8AmXae0YWdZl4UGUxuGSDHuQeyGeJui5hLepINOxPE6TIotss4p27xFbIFUNlKVlO0gsRwUaSxPklwObOQFJuXTySmJe+eIJl0hRiunvGrhC2nk88R6dLmg2hzA46VKOgKyx0XKAg2IlyzY0JTQ0JXEe98xPeLj7RcRYosN+tMcTD04nzPE+Ino+I2aTsI1f2mLn5levyl/wDp6Wlr3iaJ3ICvMpS7bm2G2dH0Zg1zCOcVJ1xPuPzNx6M+o/iaE9K9sVDMnasfm4F3XMVEaAI2keEAoUvUUVnD1YBtlS+UqJQZMdyGwwMtdZfP/syvKLEuKKvJ+pWM5l3NDpe0tx0BhVs45iFhJtiOSY4LixRwV3qMwFKZG3eBAFFiuz31HSVi+M8xLdbIVsDrxK213hAQsULaqu3Muw1mPMkMvaY25e8NFCpwbbdJjJRDZdYTfDHRSvi5vgBROYNuQMuYRf1T3Lf1GVjYVlrq1C21RpvBlBHuwaSgesKMFcKXTDOEzMZd9VuNI9Vg+5xIHrdpDFFEps5I7MXXmLXhqVIjhQld4o6MSqICvHSFYZEe86o8bmTWmN7BaOTpM/tlE0MreX5wfdxDUqC6SNzcivuV/UfWnBgcnMEUotFEOtGlpdY1LgTbFRQviXA6MsdYpSsAkE3a51UocpIs2cHO+hK5UwALbwa+9QF4MKdDL58woGI4Frk17fuLUKrBauChZMlGllWLlSuhun3hANzAbR6S5tgyG1+P1CgACs8u8sS0YH/HpEiqiPEIs8mXl271U2kL3COdgG9BpgdM54gJW9msc7l7SnUeOxnADpmN4dqd5ww+aRALdOrHhj0Sejw6KiXsO8QtYWC6p3EsVgOxLjQFS73mMAjQLEwh6o2s9iUQbSwvi5Y7GFCnzcu3cahLv0ZVXBBIabr+7HcNl2/AjEaYu5+Y5ug/RLKdfykq3PJqYgmNWv8AUS92ngw/cBSZ+MmJ33vCBSHuUlOPdu/U0Ak6hjWoiuU/cVoTFvRxuDA2WstXxAVZVQzwsuLIfMP1BNL4MsBRqsiP4j96GnxMYLj8Wv3Fp5/MurhDd5uQczvDv2hNXklQgTAu82iTb/VPgSqh94rHmZozVm6oLaQoOAR5Fp3KL1qQBTniUZLVpvkV7t7nGRbUM9HCGrUJKquheG4Y8G9XD6ZmZkUsr1KK3EhAhFB04c1iL6JXNttGNnEVRNt0SFFKx8EaQx3E1cO78SiQPbCgIsosezBqWgLKWy11gSonC1siS1rpCgSOg/kiS2cxSqfEIGusz1j59N8+l95ZMTU2ZgQYsIsvMuYW6L+v3HS9QQcM1Dq3PvPzHid4rPYfxEhhSu80YVFhpqJ2ee8wHX9pa5R2v+LlLs8kVVTsrGtBKyTndDmCGm+00YuovtDHk/UzeI5SQ4DntCTStDdg4W4xSkt08wORo0LbN5lvEvtC+3ei7HfMqmjkVyVcBpGClWdgYmU1zUEaxksgrOt5/MVYAWnzUVWkThi30OVncMyCEDQXAVSojZaHaJQFg7VHJVApKQRfbsgbCxI5vGPuJ2vP8RKVVXPEy6Qp3IB0bRm+PEwosLTImdRw5dOsqdztNcXWHpTrdwZyN4TEWMZwM+lGtvFvzALfIdWcZq00aiC1Kqu6ROU7XRFzxtqoZ/uDLMSumpVh4EwORXjuA5yOIWJFlf7DrEvgnBEPEpMcMq7GYiS6l1WoHVKltTPD5NRw3kV9bBn/AGpQlYZ2XUrOyEG0DTvgB1vlgCItK5H+iCFtGy8K6+JgHb1enWLwC2NAjJYA2BQL1dxBvLER+6gDglyg1fnvEu3sMqobHMRVjsY1VQEGpWC0Ly1zLtAPgBuFdum7iMHHuyFOrF+0MhnC3sqEWcDtibBpz7M7OO8HHBNw2W9pUH0xfv2YAVrCk66wtdmj0mFKTC8d4NjJVmm+O1VBCAHs5Xp4llXSMLZhllRYsLK8ckrJOsI5EFP1f5ZmTI6WvhE6QJc+Q/MEfQvomNKcDnJGEQpNFTxEjo1WYqxqWOcS3UQHfM5W2Y0vAfmM3haboGopPI0xg4Y1qxe+8wCMvC7iji72QBYmnDfidkREIA94zAicEWvmAt54iShqLJ3I8/M3YQYeZcKlZn2IzFKr18zeDh4IHsV4kTZ8JdgursNuJTVrwona4pZN7V/Utm0AOi2Bqu0EACkKR+5SFMEtyN4p6wojEA2jyiZRU2s6vVlKi5QD2oKCVsrFOpbTfWXZlJsNa6RRZx8EXE4JVp5hmIaatF+4UF5bIsui91pieOsqtB77juKB5jh+YKudxR3ahOEdia8Zi2hQ7jni4+K+zQgZqqgQcmWB3ld4j1lPWDThZFrs6C3LRe8umLc2QcRYxYfM4nSbo/cp3KmdrIjbNSzg2rm/6jWLZ4gq4HWyUOXhIMPP0jICaQs2TQEqz1zzKC2ZYeK6X4C+hyP8XEpxG06x1VQdVxKw2G0TbpUWyUQ9rmsWVHvGj5fqKqy4EA55QjI0iirq86nO2x5WIIOgj/38owL0GA0OX7l9F1Hk7/lDcVN3gbNBxwb1BwMgtumpju2E7GuqzcqN/wDSdOHOr5lRbrthe0cUEUBdona5nXLpXeZqEmIEMoKdR8TaVxa1buxCWwrXnXqfaYVRhq83B+HBegb4Dsx6UArNfRdLym+ZylKewgUDEMUtwUF6kUA9hq3rLaZQhorYu5mcVnUsTCYG7fFfuHpJrxefqA2sUHqTuAXLsl+0Akrhc8CPUb+Zf2UpX3xzBitX0gVMMuzJLtufZCN6Gr6PDFC6qtgO72/EMKhkm38Lt0mWsDhRVXRTzMVYRLNGKH8sHao4wTDg3zFgMmsFfDpAhgcVxbL0INnGs95egAKBwnaC4D1duhMgXYqkwsimm7Y1Bcpz1HULJ0zN/Gf1NDzZU5LDnPXibaNL4CZipXlbXmWOUyQOgvHiNwrXD1jm7S4c0F4ijZQw9L/shsYWPpDKOWHl2YbGCoMJhD8o5Mqmu0OT/VplUNjFWY4+T8wh2Zn+9aSu9cn5i8ApmsQAqjjSFlWDi1/E3fqMA0eSZlFN3cpBR5pEIYOoaCoF7Ws9oksjnNJd4cQqQC20y8h3bYXVktHoowoxK8wAAMQNh8cunRmUbbHg0S0tHHlrP3FZ3jxzwTjb1lJeaol8nrX1Kr8np5J9DhBwEycQfJMYqJV0PaU1/JKPB8zn+ghkh7YA4bsv7h/aqcz7m/JKVeY/qh+Rr8D0yRWy/wDFsZ+mRiu2XZRhCKJcQdjMzf0nTEaBi+aj1L4R/cvW0eU3k/dAtfYgq6fZNqIdsjeGYJBC+i/uUmqec8/cGbvaNaFLFJcpXmIprOZZ0l+0957ypjpKZVcRi9I8oMUrKEYYdWNY6F/c2KgRreFpHIw0zMpMv/wj3fiHW+ocRJVpfMRtbEtM/wBjH7grSYGXpExXVX7n6Qv9xqR3lEyNbMlwm5QzWTEFyWwhfh6KjEVmsFWZWBQNI8jrFneIuEKWc5ldUQlwvSMKRLo9nMEGeIVPd+4Q75xOv5RQSIdVYPmH4lTdG4NwBXcLXkVMSnbTkPuO4yv3g4HQGAljy35iDYdQwIcRTT7u4xF1imSmQlHlaeOuzzXLiZxuHWNtd7lYybW3czHmDYjKG4kCRgC1hY02X3xk71LaFza2b/CYsecCw90fuaKmGW7ITlDi5qMqQLQ0yAjdQsfUJBUGw+GX4h0FdMsqcTBWzBnkyfiY6RnKd7i1uopbLj1gpfSZNhUXMoz0gBjABTD1f1OzsUgZ4P3Aqtgaw2qE2LWxddX2yu4u7FwO0VxXWyY/qIKLaXvIeOYNKOcOTpcSUsZwNpXWDTbVRqzx1iQdh0S4WFC72x22LDackYUQBm4RbwsDWXpmu8XJ+9bDDTadYXHEGooLK71iNEoBAQgbvWIFeXjthdv4qLSu22JjymYL7QFBgNp7ofshA9hp2pHjjovhkgS/WMAh+UHr0i2+0P8Ag5mpAL1dPKU30nV2ZPRLA34wlW7/ACIJODEmJUKnSVVUGlvwhF2VQy2JZ0gptTatJBAYqNlWOmBIM0RSV3nNWHaDQ2S0gaznrceKSOEX9wLUAjg0wgIKDC1usRUhCVeO5ncv9DYjJdlNLxm4SldW/mEWS8dYBgFGy2wd+8bnpK1OxFR8zlNwhbv+pih3ZNnn03DYgcShKnyT6LTV4mjmO2OJfENeIRKJeI5tFDsH2ghp8TZiomnfzL9D3l6f0T/QnY/EaFVjMSaPaPUfgnMfCDOS+YI4Z5l394Qe7zIJSnep+5/0Q/DE7UeB/ctaS8f8z9kr9QR9hv2S4aN/zpQVwfh/gY717o/mD8aB+aly0+R/cHLC8n4idPd/6oNh+UR6Q94c5VTQi4YGAmidrm4OAfURB3mL5i+djpTb5ljCTHhgb0ythftBSwHXFSpV4D7/AOR+HBwpPmYt/E20AqqdyLlI9sQt2F3m5kDtFZU95rKWIvD8S22MxABb0yT3KlAm4CqZ38SwNOIJd3nmNoDgVog48zAUZbZ2OhKd+hhpzzHoM1Rp5IQwQM1PeJqxE6j3hSrdhyuDULF2Ce0Kpg23uAKJdmFpg1Sl+GBIdAUVxbKjkGxFFSOqFsrgoETNQnoA1oTkgIslqlqI+ENr/UsHb7lQ2hbVOl8St2pSxrgL6ZzBk8zxiNBILf3APEWFVS8Xorr3l6DVpiTa5w1FLd26EHXmCjECFgLAjZu47IhrXzzaUNIhUWVcu4VmZQJp3u6Y5FgIQ6j8oBAtVwdXbOQ0nUl82DktuPOossWI2qCBcRBBanniNB0lQPVUVkuP/YlSL50Hpk/uACUEaUHbvA3igaar3qKV8Ac9ywxc8LE6zcsBRRz3GWQBUw1VkQOSjTFLxGsVg2jnOe8Kyy9msy60PBDv7uWYRGZ1h9oshwAqgqZ1VCrWiT5dJbqMqlN6Fv4ji1WwvwgR+olrhftMsEUVutWi3LwwxFoPi44VBdHa/wC4uEAAFPBT8zKEvBY4jagdbQFuZRgegkBmhiz9xg5mz/i5mVAon+XKoeyBn6QMXufjwaFK4PeMQV4kjrUsKDgtr6l8oOqd+sXQgdq4lA2MRUW4jb4Pla1V8Q6uBMKFPQbeZhCXvF0Jtzz/AHCCch0D1+pRe81h8oIl8YVVsjc0egqFOeT7iRShh4owFETqLzK8DEBMha/qmZvrHIzOkxZZLHFUUTZ5inWZHglbqDiVt8s5+nV4nMi0sdx0RUQhgfEuQ5mhqDuOOfQYjmctx/eEQ3XaBZ6QV5r+4peOdOjW5uAayurLihuqp0qN6hoeFujzKBRdqO8yYLqnrG9dFbzCzlnRXzAtQNRfBK+R9p1j4zqD5gt/ef8AUw6B4qaFHh/7DGDf65lZ0Pd+Ym0uGpeGBgh9jEsXdNEGhFa+YwVwR54iToQbOKlmo1HdlIjr+B/2YHYM7DLHKe8D/ZP/AEIc8MtpiH0xToi3GiyHzEafZxcu1ewwO7pAmYB3Z+JURVWj8jE7F/pogm/HpgBUDYLw+yzCHdg/UVaCbS/1A1wBX04lLYYdQ0Igr7uCZg7Bf3KgVNFnR2g9QeCV8kSu4lRgfBUWSN1pBZ14YsvSiYtH9S/Tk2BGm6OxCyODCAHXNbexVSvKFl3hVmYxGAwXbpctsfzMI7aZA3dNsUcBNjQXrMQykZWY8QOBRVhhTzUMQ4fuiRkQ5xyzoqveCzpTYcW6i1HKAGXYCdZajuqgGgRbzYBkd9R5SinYi5Dw5mXfKw1btUKxjrCEDfcShC5g8EyL1hbouveNsbWSsddn3FSh1Le9o6bopMveC0DALR7yrHWraEPnUsBL3Tee71nClTbXSBbZQ2W4i3VZcDWIqK1WUY3kgYav/wAS8TByH8QAghqi0svXO3TbChHRql1Hw4LV9GaDzF5S57iKulbNPWIGi4loCwX9xSsqjhF34q2YprkNBLLvtWIPoBVxdf8AUeQoobQ9iWl0HQMTPGjQCoq5c6xXeIs1bMjw946N4whK7mIXUeM5B66h7X/rSTnb1/aJehRDEBW1zdDDLXiz9zrO8G7/AEsGCcPieyZN+yErmiaYO4SpQ4PpMtAoUqnzKwKKH3DRnWiEW6SPwy9Jb7TZ3iFKgF1lj9xWxN2KqVsQjN2A9OV94GBYNDwPEFRCNOJcC1VFBZt0YoSdLpQe8t7rXDfviY0zcYIgImumdn1MB8RWrbOwGAaPTpl3m+jMT8QW1Sh7j8R5VqkdvTW/EFi7JYBKNmHPkzlH0mjx6G0d3DJ4isg5g4Zf1/cNwzHdanE9/TiJip+aYnwzGdlnx/aAs5EkPoKcLjfeqFBDgW7szDsj9ynrkTJbhz9w7Og/mItnCeECvCv4f6htRsreOP8AsbwHF4xh+WAGWaaZylBVdIirrCusI82DQoXAyE1e2o9IJdWMKXtq459xI8/Q1FxDdTtNHRmLdt7zPwS8k2izBzGbShUqlkA6BkZEUBQatg++vxP8HrGIjF2QuVoWuHSActWURKn6pZWhgbBxMoYqXzHuZW7E5g7Be8B180FTl5CHc3jqL4Ugbb36RblN9ojDX2/7BtDypSye/Apn+CJkJ5P7hhB++G03wGP75HxY3+ohU3xG4KFfAwFVEpML3lMKBi5hbbgKps4EWu6qz5I9QKuAOYAaDhZw8kVdSjGKXrgPJVOzMdKhybiN8garRyZdpeiTI2+6Mv0YGj5l+GTumXKO4oQhqUqgl7Ey7xC8y2sYmCXthQQgS3WzQ+IOyqiMFq5rpHwSqaqjYd4z04l7rV2mpoumj5Ysq6Bs8iaqTFKqy6zbZSq9ipQCcAWAuqdgq3rKHNarizhX66wWlXPPbEog7bdu8MeBr2lfWpYpRwBWe52OtxvZCBMh/ukRbqDVN17QFSZHQZ944VVg5V8QDBmcOV3iylI4HnqQIG0C/PWCqrbKSrHqC14ZkoQa+JVh5GOkobxk8S4uVWdSB2aqHssFYOSivxLGZ2CW3RDSuqjy3L4rZKsDlW2A0688m4IKGhmJ4ZcwON06LaPEUVG5Q3S3QYCwDRV+YXkljI0wLYgv1m7eLLyvWPVWNjS15Q4JkZ7XP/CFfZK0IRHROsWyYzAq1CqEAptum/gl8tlV3Pyxr1eBV74xDZTQQzviIxgOsQqytYlmut8vaKyobtSflIQ8oKc5Lr3lzxl0Bd5/1xEKkudPO3iItgbUA1nkT7jadMTkNwTIOXBvzCdoVOQEK39xtdxezYe0S14YXaAtMwmeo+IQIFsr9yYBGrS4bW9H1Pwo7fQeZenjEV3i4YmHuYa9OjxCHc6+hg9OGb9v7hlqDllls7RIGycR1DtfMAV1bVx2tKAX4IodcnoAR7PB8gX9Rbzhq9kjZLVsYS1auNMEWfaAZwCVsT/2WKlCl99yjFKb3IGbjLMK3Oh8sUrf+DlISjeuN1+4HQfqIVvNDstKLcF2hZOLfX/YEvcgC8/2hP8ADrN0IMdTkMUX9R0t1SmicmPoNw3GbMbBjBWI9JAFas7xiAFb4CYD3fLCAt7AqMeMmNSjbAlByQWNyBLT1zMvkpVu6/tjLUWukythGCLubQ2+0Y2cMuROh1YDZM63ima7iSxtCWciBZxB9HSjmLiWLb0Y/lhL20A/Ef3QYrl8xZ2hJ/Uw3wCKng5gwcUt5bQMILlUY7LHo5tM7CoMYum47L4K/wATDkgRyODevaKBEEaRHCRsG3TCu7eWYOKUVvN6EqgDjI5mbVWwv2wYIaxPymYo9rlE8Mj0ZmwPaNysaLTycQHlSSaGbTGB1EPeyBd2pEUGQQTzWIQirZdQcZvMcwKrKWfEtk0hQ6rgPtgdk1AazaMldx2tU9AqLCU4Bglrq7RdFXvH3HsYEJQ8DitJautlu1a522lfOZXNopMtXFX046wTQad1OFece0YoXodPqY5DfmJbaIrYyi6L88QuwZKQ805MONlhR6thBV/VoJe9/uXFHQmvvGBpbzp/7Klikdu89phjpjtFRs2PBUezlgXgiuDWJobobthtgaFLlpV6mYhTDCil4jxhGSKNjK82XzL0rFS8DmAoui9xp9wCZIoOAb4tMvx8TMIyyzZCaZfKjDmYYtt+8F7z4x+0Nj/MRSvEKq9rAUdAQwTd/qMQ028PaMrKGbYxTYA5wpDDbABzbrzLjClVwDHPMUKqZG8YX7QmblCdjekWWMIaWUQ8JZytkwJW99CVVUjOS3K4RhBQ8Xi91z2gtIljHGdQgbHAmy9wCMH01hyL3R0H/tBbToxsRwFuikoVmWgErO7B+orqC2Bn7fww0s3knL0GZiO2LTFah27vrUVeSDm1jrfoc9pjM5jg36SyQcLNM8x8y5x1jq4PvNWKnG/tCotNFdcf6iDCUpXf/pLUXYUHTIygAJV6eiUrf+JDR5T6mItviGn7lR9T+4HDzI9H+yVor/D+p/oer+pTTlFDbu78ITef7IKytqGsgpDVlBmOtU596hLyYVGXBKu3f9pqvqu5i3sIg6qgf72jBtE1OiG2EZszgplKOgOQ/wBS0Zq+gD6lhl3A8xgUwsWUdtgwoEF6XUpTMtXdUejWceX0LMds5ocdEEXEF+iqqiN6ys0y/of0QEOolD5ofZl6B2irGz+45aAdiIMsqzVxnDjwezDTLfMXNPiUFewWAfFqcg+UY6BO0xL39oy59wh4TOan8y9JA4EfmNEy8WH4mW9wiASqZuLrUfohC6K7XZCw7Rp8jLBRHcP1K65olNZ7zND4rL+5VnwYz7iIqJRCLR5kpwFToMX7L8sx85G4eaWIO9NZF/MaxnW5fqDpArD/AKjD7uv2xYLjUBXg1TPlgpPYw+BiY9kVya6nFkOrE1t6ZDngBPMSpZKuauvbEyWpyZVjc2x4lnJBOGAwB7wxAPgfyQ50dSWVUNWNNlPmGY1SGO9mCeZlxMBCs2GdhniUZo2wcMaSVPAo7Iikqucxa+Sqjcp4wdpvF1XJLLc0a3SJujyU3m5StGhnEuXlLl49BBmZGxSJXeY7Pp+XHi41BdW+pvnMYl1tG5rtwY73LcZjk5D0A0o85xEDkAa5p3iV1bQwzB18UBaqzwkJZQxvLt1afv0fLLpF0vaEpTzOeMzMCBp0QYoipQpV1fmKVKXdMgvF3fGAhK7NJmu9Ov1FJcUW0LoY77h/ctkG1ecRdZhyHAXreoPMFENF3fuOrWtElUjFrUuo5EgtDqVuBXfVpAvDa8a8QhrLF0cJfz3qKS20u9w6SHptuw/MeyzebFY45jcqCyVZQfqBO0qhbDfgEaj8xc1FgvFGvaDPz6goTXwyoipWnyzaaTTCyCBMVMOj4grbBwwdYgDAypT0l3T7oat45Jol2sKJhMRYjrEIB5We0MFV0fkmWTTA4zeYrxIQyNq2fpmPXFVmHJo2d0p4CH1C9GM8jZG5+H+H+yBapbUAeytH2mwbCYilY0K6L/ogTBklmxdr9I2hcMb4q1v6/uMBdfrhgKN18mUKskgGhqzruPL0Nx5moKuuT9R3MHxEyQbhuBmM2fRVMOD8QLfLUBt3YnyYbIAKBT2FYYlKzGCTj3gGQJlDRAPE4K9GeApjLYqnA2/qHiq8k1Rm05TeO9RUQwkBXu1MocqDpXTrqYrXVaareeMfmZ+FSJyKSqrfJ2dL6ygGKV+YWGMFFcQCzuCBK6jOLvrK+DsK6U7TNBOvCGxZ5IOaStgRXCBeQgK2MX3SiPQJbLyiPplZbA+m2+8ZYdfYEAva8QzgOSoojnMR0I6KfEo/ogX9EzfqJjQDwROsUuWCmM+Jkwn2l6gchoW5caIJsw0tE+TZiJpGhwBrbu4qsokaDpnIxWAsoKbXiubT4lo9W+7FOUT0s9dSlX9pxDCyGIdVoPmC+RKlxvBz7TBi2KuyHwmiy18CGWZjM4cSe07mKbb9rl1RF5uZPRxlZy0PD9od0fMv/wCoTK9/FLrcDKupzOmIHUMH16ACrQB+n02XSNqSIe0Qz3AJILIgPQ8XcHDeyg0lD7YDBLWLV9uuIV0I27BeveeO/pDazYbX6QfqArBs9/8AiNSG7xOCOHaopBFZ2j8S38TZ9lwBqAuh3ZVOIDRxEOcoyvghJLvorecDrOW+KhtbprjvFtv6O1QyywcJWJXAGcA4xEemeEb7vwwj3EDoyyL6x3fGORrcIioRzXN5b3iPZawBULytShLDKXSWr2Dcy13mttXQFYmLtKISC0O8WNnn9Tf5PQ6nExBKkrqPMWHyxTSa4e6O300fEGyDRDdy5VM94pep4iZgNzO9RWHA4GWaDp34fmNUuHH3tjo8HyrJlC1A9KgaeyhOkqwp0MwsInOLhj/hpW4SN7W+Y4iYm+chCUlQ7JDbjsK40CbnH9qbnScBdsoe+BQIWwucCBTWkPtqXfwT8y3ALLrOa59o11VRK6ZTJr0Qx/tzNX0NxirsLljRq3yx3BRXSbSDLNLDcWbM0gIOxMvNLuo8PMyEQuvSPI95WbY8qP4I7fM3mzN4yo23GaGSDiDuAriiIzZhW43zLRDJtxkYnWpCVEG9yxzoXuJTj2cjwPszl1AfBKPTS5uZFdY1qmX1iTZLqluJqBJ1EVEdxtPwxwGu7+yBQ7ppzd7M36YP9k/URgLJoq/cSaHw2ZL2FoiPJuKLD46drGxO2NRUJqB2dc3VTtMA4Uz+I2OY8geCqRke8unKLA3GTOemescPSX6wYlbY6LYbZZrZuuwOUX2mBiglNYg8uJZapC8OgdcxCriqaSkq9QNGQOKHhOXvMkwENBc0nPSLXqGtKtcrv2jPe+NRUc8uJ0JWUzHQqG4ZEFHOTEvGgAKi5iWyy2zIVmsEAcfLCmog6D6lWKnDQ78zrDwT8yB9S/Po6fBzFdmLUPvCa66u1+M5h7EHRH5imCd6T5llTe0HBI0M76VFD9EdqTxiElJhXDiJGFNA1zBGkHvBXeLfcyP1CG0AWJxEWVzHWFmID11o0Dm2HFKUGqVau/iAZLQK1uljoABDdDE5m26ZSVFAt5pgWUB+UFyoeQcwkQRTbVS6EgdaPFYgF4DZq/HedUsuHguHUs9wzWDZ8tXzKtyWJ+SANSxCj2ajQq/4MwEGBFzvmIKepLf1Fhpa/Qwj4hJPA4dnFxwHsaKu4dFL1rqmviYCcsbbkhlc6IXeChDZ5ZWUN3nma0M4lNcfEKZZxjROkW4sM75p7z6U6x2whp8Q1OJ1IXLU1uP4jhm0Nzh9MD5hE3SZd7Bg9czQ95pSZIvTHawUF80n9zM1CiN0xccQ4LdXSO3G3wOYMn5jgLgJgQHSsPxGRCjl9kLI0rcl0/cr9g2tZ4it6hfihX3BK0FGlztqIRthz5X9wO6sDHjMmlAVgEK/DL6JjBcutSugqg5co2PSAWFZfvM3NQYx6dBM12A+olLGrjFyQq6Zjyw29D6AXouxP3KBLkUCyupsnV0GLVeIzglgniE7ehx8wSosQwirEW0NXOqLN4tRfGirYIpWIgxS6A8KxEOssXC4GK+AHuwNQwjHdaWeBh3aVeU2nHSE65NiI187YtAZHqMQ7XsAfSKFEX6PRPzOjT7zYplbbg7Ta25S9yt3K3ubnjGL4XvgSiqGDStlNmukOOWIyeG8NdmHiLcLn5iYi2y0ZcSg7bqZMWGYsCGHEUFI/CEOOdgnaMo6UZLMpWntRLwWvrd+X8y5XImST0rQGcxAA0ClU0nPVhxoCiP8qJjQF7KvHWDJ5mhFWTcGEz6Zv4TmLMUvMMEAM4xL+R7xrxcGcEnQCEqoLB27YlwZLxPyjGaNZUfCmC4EzVh0up4bJWkAwbk79fMw6HqcMYtTyy8RcOyK6y9I6nvHRj0XmCvN1HuPmZcxi1ZbExDCJmzeaH2i4Ep3hmBSukKuEFpKrBavfUz1AIFWq2kBLhWtk3LpgoaVIx7Ts4Yipa12q5mQumuswsqaLwQ9lxzbcAa3CoU17C/aWlBs0aqisDxLCSIWTkKpri7gFF0ATZbbsRKyrdixYV2mZMSizeguizMASwVMtjyGx3DcUZy3AKer3maFvKDNDrt8x7au5IVOxp7RBJozSUnWGyaF5cWS8QjS3yeMQWNxdBDUpQ5gGgNW1dEQo/wuLluvLL+RGJzjrajzd4xnEqR2SyIJsL9AWQ4eIbjtqalbmpx1jv2nDP8AjPf0cS+ZTcqe84n5Zb28dcT90s8Cz6xHBFuW7xfUYA/ykWR1H4YSrJV0xl1nuIgHGH948DXlY+ivavEKFirM9iDdKXfFf1jwqBeWUftGHgaXYy+Ygwrh8o1wDS3Tt+ppV7b41jeksHZZ/wBiawx+2OikDe4gQw2vvUvigtot1AylzmJmOV5qWd0wDzNCPeFZ7sv1F7tdw/Ay1jW7wX4R/MEMjdqH6nDLzSvhYLde5ZfySyovhGADhbExNdP3HjzGWzcGpm8LnzuXANWqV8Qq4M8KjmUy2PxLbQ9GHLNc5R3NpxmRmAOiFGRGZXkXZWE7R8amDGil94gVWjQFS5Typm3nrEJYeVvFIaYLlwW1XvEuPL9QC2xXMuYw26ha160RUYBAJL1DqJwK8wVYu9Q2H9ydWj0U949ZjXUdIQvFx6zOkXRbh7iwddx2Pcl96Y5H+KeYqIYojdScTeO4a9D0EIg0b8y1gg6CxAAqWq+YLyXUgrSc6jwSAas555I4yC1YpssXjz0lCNQeKrrngiLZtWZqsaL6QUG9OpwhLVOTpOl0lQ3b0jFTcXKK2lO8Ezl7xLQ1BPsieadZvpS0cuNx9riqILfNMo2HlJS38My+a+ELVy92FrWHm2U5wPBKefklci/M06mDmWXE6QhHuJeITJ3/AKIKHiNtS76UNjnbBGQR5P7Q8Cpl7jX1L+uhfhBh59Al/L6QGFnUQMqPbGkAuVD+47GdVUaH/S2GVl2Qvyg9Xe175owoS62sfRKd1P8A7UuXz6PxByjoDo+CAK0c3GrB9wgbCkUuMyzDlyUTRA1kD+JWNvcr9xK11s/ouNhv+L91Ael3w3HuzqLhqOl7JlI98yPmWLHXzDi9obm7jh9ecR/Uuj/m5e4TlHUdtahjmXBzO9zBZXwhHVflIXQY/jMhGj9eBtz+aOwWaQ0VwpaTS2eNf3AF12T1htTocPdwJ/YfuCA4+ESQ1VeQzYe8V5hzlr7V/uNTtncbDWs2JPcBEc1ib9FWfeBbRblg3DpFpaLMjcba1LhLo5SDTdLY5zLvEZyA46S2iK7TFC4YK8wHr9S3Qj2SnSHTywZPepebfK6VX5uWmi9ppUPUhxv4DHgHl/Upfsh+ZiaG+g/uNt9tXKAr0u5tLKgxM4inWZmMBdYW47YjCuNg2M26huBscVvpFACnglnrKKzZ/UVCgtXfzAzCXgUwVqNIxSiwr9OIhxO4Y56Hvj90hlVhDS+YBz+YcqqUkw2VG+0IhjC+S+TUcxeSPdKYR6LuVikNlseVgYmoq+UGkIHrfobYamiENJD3RiLglJ04fqGAEDYtF17OZWxjAsDdUd3iBCbbmeAUWsrfiYMoW6oOO0VznrKlYPMbBdcLFrQoSw+I8czDMGw6mxzHcVY78ShXHVtD2gOm430VdwlB8mIbPulOprkUbWCX4JkVprmMlsL7XErL8QS72vvEeC98yg6D2lusurlgZdO5bWWXiXLjknM5HAZ8kQxR8yw1Ms4X8oadnWVWT7iVKOnLQF4UuvEYYKuQys9pd11AauyrnF6ywGhvYYujnoSxZWs5BA2cXJn8RbAmXZ6N9ZIIYDqJniBDIcCDDIYhSvdjkvEa9JoKFpbMHvAto8u8CD8R7RL5lnAQ6U7DFtMojVXjR2sX4m8Ogp9wQMmhChfOplIJxeYXMLupd8+kngXdBAUVp27h2S76fZAtpUob5hVX4PfmoNr659MLs2VFOog2n5ihF3gSngzqCbgnD5glyfMuvcqCinQaYWh/qdoM4flfpYgUQ6i/JLVeWv7jeoHUSfUFiy6Cpa4D4YDeeIuOeIPPoXfmfiViFiwhYSpd2wgfMK+LHksrD3I1Hiz4wGOP6sIqzxnVp/U/xLaCEZUCLyxag4b2grd1X/fMykaUvhv+pQqW4WzxXh3Cp3b9ZUUvyxH6ZYHSfFf3EqW8X0SgjkSUAtB4oisK8NeWYjX2lo0tk8OmMF2f5bNvqLD0LHY7V6XeKAbQqs+yw2wZqUgOmpSSy0FXQZhcUTKFMAAd2Nw0AlvvBL8ikBXQdaf3FbYhdFoWV/khdfEwTi/vKGtXrMHEeYkMM1gKqG9miIcPkhBlzJ9kKs2RdDfWAqaQ6L7gGlCMG7yg1DrAmuWoGQKEGsI6KHEHQD+YLCX48Pwsd3zn9kyY+1Ed4/8AOmfl2v5EaMV2Ztl8ZmM84oCErJLCsMYbydJvXxAEbbRyVCBdqrFzDc5RMQMS6YKVx/VnJHzCMgRklZ4gm7CrwP8AksWQLXacb6OSHyNjWBjAY8S+azVwewjabo4qM3E8Shi8OOko48kxzMp19pwblOsCb8Hp96LXVlZVmBFLvPWBH+sN28s2HWFb6wz7EtLkjk+i8rc38ReZdxlx63GXUuXLlbpn8p/UTlVnUlPfRbpoACjxuNsnb9RU2FexZgZ4wNF9DcWUzdFK2sOYZEZZw1awOcdKiLdJV2LzCyQHQkLt3MxflxHuE7R9R97pP1Gj1g0S/N4id37HxWc8S7NlAOuO0GGgSLErWKshoM3TlMS3l51+Z9xB+iP6gf3Nt7Rf4lCqx5GOWw2PSI2gvKi5qiQ5Bu7OvTEMTXLR02uvaKywANy14same7nrcGCHtRGCwNKf6hA62SyF0VC5OoFkwLPqNyq4N+jAMJsVL9/mUcPuXKEc+Jd5jif+pDrX5InNQS8p5jlr7Y/EGUVdET4Zev8Az/IDFCkv/faRKbScm/T+0sfgP7D+pR3Tt/OS5/17qkoXW/0qO888kKArCeHzEW5iw8wpIWC61N0sQVVKp+pjwBhb/wAYjQQQDxhAQp462J9y5/1lBQeW/cB+94YYcD+YfBHzT9x92KX7hOg+cf7QSdz9IDgPMb/tAJZyHaHdEQjus8ELb+0mBar9kyf+7RNAQDPvjMHuj8kHpEOewH3Me8noaQ5YxIgLFbdWMtiyRLL2wS0LvaH8zPjPIifczBGXrRVY8kxQ+5gOmCVBuxD3ifsUs/JDdp7DNc91IYRrombD6jr5gxINuLF+olovqYUHrVEqanoZQ8KdWNTQ7wlWXCN4kr8sQAsB7wqFdzZDyhdMTJfSBD0uZW3qrGELkMS0HJKE0RO1KKh6xSizTAxuWbgucXZLXQFuok1jMbScwJheGd/8ss0DFOsRvuOhiOC36iscR7KBQCgI7ubQyiOoELmEDYT8wPQQAGDP7YS4ala1Lt6RnKquG2ig+cr3JwL03wUO+FnYF31nTAZLVMSlTZvtOaoSeMRdT0izKtRUHdX3HbPtTHUsKzFz6mBLoY4EuXLl+i8QZcuXM9GeaPeU9fgjxD+IChs4CK4B5YsXKtpggQUdzGsn7lOpeD+jFylLpK/uG++v+UeJj/0gm3EWwfzN7a7VCVMrKqXn/mZUSSALzjPWWAYBVBfeV22GBoZeHe5zRgxwYsF92Z2/mWP0g32MLsLrLfOGPoWlhXcYowPgT8gElacZch8ZgMwzDhcGGpUi3+HMv6X3v+GCZiyIp8d4oyV8kwmqqrzmK5HmOANO477hZglCWx7b6R3efS50OkXMvMJRiHW54ibRZzF6TPoGGJYV0j2vmPmgXUgz907o+SHOGWbfsxSxTsQD2SqUekr+yIz8w/kIm/N/3cAWA7H9ITuVlgn5lZhBtjIm/LKdiAIsNnN9SZOS4juuIC1IZKRoFU+IMtGKdiFMwVC3AcnEG4sCK6BO6/UA4xSQbpQS4AFZerBMtcL7UjBrEod1/EXj6FOmbgVis1kNQoeS/dxCd8/0i4LgBr2Yr7DMx7QoXT90N8T9LKnjNWXen8T0JkP8VHovm/SpetsNJOZsw2zhHTOXmNZBpjfvDD9j6mCOgH1M/BC6VHamYcfa05i1sKtBTkpCAc7h2PKHEjBKD7DUdDbHbBBrxHEDsG3Hh2uN2npefqGuewYz7r7I5d51XL2INux6Qu37ynYesHavYYzRB1Yjan5RDQiMU6SdglDlF6kEPJBmlBlU61MNXDF2iir6WCKz1h0QgSNswiELXR4g5IIZ8R9F4YoIdzsAH7gc/dACzst3/wDUfsozl/SKGCmVYVl6mD2m5ppYXBvwvtL2CkfJiZMOECYJfvGyaD6irxMcLYGZpGLMB4jhjqB8jNHmcI6M5mSMLLLmTFtiy4CmmW/9ZXUfmeT2JR1+Y9AhdoZ7EVtgHKsAcVCLxSMCCrnNEPwfbcUnzShcUXfSnlMBbXFl9QckDpeKdlMG8scdDrtMaPsYiz4EDJicwA69bXuPRAFoouMK6IIwo/KtY+5gfxtfvlVKC0XetsGaewENYGoy/wABZezMwLVU4WucQGBWMR7kAVC1sPciTrgdJgtxxjCysLe7cc0TmgxhZ7dQlAB9ZL29YFu74Rguv44F5xLEq5h7IHlBXwQXBcSzDKdU8noHPPT0cw9HmUsmiZlPEX0F1QWVGLy0w6wOAcAdGDfpYPwntKtDPdIDXyRho9lT8Mptq6v7igilsETDOlZ3/wC4aUgj0rzEDYTgsDUXBfPO1cR3ISnJv+5aWgWV4Uf3FkSYyCgAQ4sm5TqYHCumT7lgxhLlWGxl8adbLs1KWZVbNFOXtGCFBFehtOKP3HQQDI5Yxtbwxv8A9zPeDAAdbU94/gehgI3I8TZhlhtCM5+Zj0XmFVylWDqx23dKG7jH5hFyQ7FzULSXtiN8VLhEbpTxUPL3AmBXzAPV/wBstn/yo8HodYgyr9Eba7Ij3x6mKC9p+RC4N7Z+Jj2PLYR74egzPeSviatKlFIE2bgM2Lb6TB7D5hlv7JNm5pl7RHMPRi2iJdZ2qJwh0lO4H0DbieGYlAHU8zSPp5jt6DuLTfSHMcQAHCF4shhNZDSzTnpUqPu2ChyBZxiXiMTJ0DsYz2YANKTRsu3T0m2VamS7+mO1b8RCGHcZQbE3VTImVR4e0rSuah+ZjhuG1EIpQliKsljAzvveYcjyzDZ9iCd2+oj/AGZVo+FxfWvBUb9X3lukslLrLcpAdYOI8+i14gPRiPEsQSSk2xhQiIOLeSHCvwwEG0W0+YrxIQFfF7qIShe9guStdiWdO5tg7scYyo555mAACc1HQoOgSztVx4DEjZRSCdbYvzNCw52baG67TfEKFHPtC2jSiAETbzcZ+Lhe5crKuhfuJUL4hsWSsF2oYbEuswFzcZ1N8QDm1O5cZx+pibi94eYAC4GrWGEof5KYDffFB1H4liRg6QviBslsh1B4Zo2Qcn54FFlvtC7qHeDgx8IFlLnUpHvzzStTtESF3JQlupnG0fQEG4XX8KIhPCJ6SnSeUv19DJ1IBr5oB/aHIKA5+LBDKJwWfMz1eMAgdwYts1lNWMFfoP7Io2N2Fv2YypOxu3tG1cbRFve2YENwjF1V4llUyBH7g+sYUcircNB29CYXoI/aagKh1gwribxck2Q3MaYs5+ZYEO0TXjrAX73EVdW4bwOHeUBYmK2ytC3WLYc4DrtRcTeS/aLJIzdVhKZDkLhg6IF3XiakXcXHoowcwemrLi2EuGswNXDI8ciKHt7lsO2AfZND2kX4mBJ5UUdnXpiJuZMlwfEvVxwMvuOWh7GU32JJvnN58U2il94QQniO3f8AgZaPksdenmJnNYmYNxWQ2X6igADj0ltsl3qb2xAcXbO5nn+oKR8KqAZpfLceXh6TaXpVhGVqpdy9hC226gkbp+YtbRd9kIQI4FxZZB2oIsYatXSKcvmWuL9C3qylndKdZQS/EYV6G5lor2b/AOx8Cbxp+ItiegT8yniHZJlipzPKE3cB1kxq5i0X1R7yjevDCot+ZXxA9D4mOkvpFmGgpGZbAdSZoVApPWAWSveJTRAXhIacJLa1OtSX4/UcNbadJ3LcVFyiWLGIZYqJbIPuVtfNlFqqHsI7H9WAGSRz+FYXH2MfgTj393/uEZRdUftqZinON/AzNe54ox7DOyHMYNg+YLuKcks2PsxXkeSXvDe8R4mIHdkGococEQ6PhHoPhO4iuxmHmVnlK7yvER6TM8pfrz68yiI6SniJ9HYyn0E6R7wcAYwwS/3hyL8xK0XYr8TCBOksgvira+auCsXoWQ6x2witdWC/JFxFbc5iyhuPUZz8ypoOTjiVW6r6hBvvKYQEm1YouDkYOSoMFhsrcCJwQU9pS6RWHo5l0CsR2rwiVLX33qaRRnPpWyEYTVjFs9DE5IsQ7zmO4+lXEPTRLwzXqAFWfOZRv3IPvsjicf8AqFn1MnZlbBPBMvlrH3NqjqbTmVamrHZ6BqLw59o4BVpZeksKAkm9N1FZjJiwA1YiFETpa265X8R97XcHMrq4rG7Dr3lscMnGcTgrWZXI2tyhnMNHOJ1usWXiAJomrCKoL3alDxKlHrcv+O4vk+02kA/R8CygVPkcQKaeGmPWsy7Pus+pe3vNH8KinFU5LfGE/c1vlh9MQF8tR+yFtL7JVcQi70jGaucNI/IlR8SYuKcjGvE0lHtKygblytuoefWzP4yRypqNwlHWA6h5lW/lmGQ94ixDYhjM6KX7ifqJw7118ATNr7trPlm+31Eu25S9y+DDdf3lVw/PvKbqhgU0v2YHv3C4pyveoBhV1jjU0DC3ZJ5JSbb4MS6HikHn3AYWj4YsfBNR7n4YszJ3mTvI9QTkGFjRKOn3EvP1N8UwN6hSSziI6MelipaZPSh4leYnee8zL7Ms/lp9btgxCbuUlTJHbDzB7S3eUjB97io7CwhtPRM6mcPWNxaizn5hJyop2C4iE7flCVUQhbdOJliO0ZqLM0XG4K/4iTYGgFY6yqtCkyXOJ5Z4K4ihd+hubTSEYbhaYLalUTj0cHEWYw7i+lRPSvWsQOoMAbyYb2kfmZG32A/uGCYAqb8MVqOgqM6ocIGGE2IlQjqJRHyzN030w1tuW4MoahYogyg/Ea5FbbuZIEN0VmAEdEOFr83Eg8sxW5Zc3FfhCNPsn1MOF9Jij3jt/kF6zNJ8dQb8qMnCdVc6+nCvfMEwHjEo9fmZ8mJ3Ra3UdX2lShbtqGhbzB3b8IJuyWOyWPJH0A0HhgOvlmthmTANMfU8jAn4qCQoc0r8SZr8GNR/m8wjrxB/uP8A5p/kRu0HsQo4GxGr5IOdqGp8CXRnVYtlveKeX5mXcIQymMb6lvo5ypWvkn2Rn7SHLfyqvmhALeeoB+TLEs4Qj/8AMcWr4mWF7QR2+xl2FuoH/IN7OzZHsfQjXNCdRuJyqLmhBDRYhhQ9mZFCpwMzAq72gJlnjMqVKVN+PmNeGdyKgJK7D7TsV4ZR1cV1iHSPRlPJKOkRKdY90tKp1PaPglYnuy2W+txzy8+iRjthD0qZvUP6mZelSjslVi5hauFDbwP01Kug618DcyBvUB+Ihwrwy9apqrjzMn3jWutbuPLXL7L/AF6e0qE2SoXXL7TEeifiPQzQbrDEwQS12hZ+/wCo9+Y8whOUYRnM0Y7jr+HkQ3Fh3H0u6jH0CGpWIdDLOHzNjU7MqcE8k5MfadixJZG2nZ5+EuPcWf8APQ4GEySJayl7nZ95qYQKgdiYVSVt+vEe0q462W/6jY5N94My6zgyYoEHWgfMdqtCujpFa8xoW6xUdKS8zJnaHuOZzenoDqV4J+wlROfdFgWx4BDb95hwp7lxAooO2I9ZnKTBuWHdS7Hsl1L9YA2M6jcd36wkIbj6Ez1hfp7xLIdpD/DM+J4ep4egUuXL9b7we8uX6DLxGlYPkPzGSDNpm8t4gECd0hT4SVRBtuvvSYdBpqU8BIKK6Ok592fiW+CYyHtT8wyCq1HD7pItRM0Iv9ynecyUCr+IrCPIgQ0M9JSYV6XDlgX1nGHwxrDady4twe8QXZ4ZuQeSKeViktl9UaeSWvh94vp9TxlTrEuCKOEi9xB1ivOY9lRDwfEy4fMu5SU/7luEfeJcMcbJh4lGeUXxKoo9TOHMtL9vS7YQgXBTIda/aPPuwRFVwriYL07Ro5PkhoHnH4xi6vu1f5S4ZZlVml9cNfUa/m1+SH5imU8xXumZ+hzin0CKMgKlwr6xHS6/gf8AZe48X1COYLL/AJJZ5IzdtD8Q2oxf5R8H+E5eYw3DCw5j0nMZzK5m0deumawxDDuM4l+puG4wcQBOnE1GHW4KrI75gzXcgpn0IRxU+T8T/QJ2YuvszLyf1G0ztHK95yjsnMUCTs+I54jmqgRZtXRvcKkq226PEreJZ0mCLRkucdZgLUyBuGoyUu279KAJblihKezPs4Ji9pYJxMp4hZtVTuBNTzc5A8kC8Jl+WM26xZmVC+sfaJFqLOQHxO6uJ7L2YcPMcyobj6ECEqam2EIQ/wDiM95xNS/RTrKj1iPbxCLt4Z944Wx1YfuVBU80XUCCVLs48xzjPzAFROFINuwxbVvzLIYKn9RC0N8P8Kix3m0T1emKg1ojJ9zEAMpjNr1BsmTJjVgV+KjWBZLo/APuI2m6mvzYiNhfSbqe6JqQdwYbZ/EoG094FUgdyK3XwxOg8lyjSfJFHHxErdyujHuZb1JS7BiOo94nd95nhGb3UR2+YmtMR3ierFcJEOIHUJ3IpyPiJ0J4ZXhYhBNZ94vlfESUdICxCYQcyq5JiM8JTBeqCOR9olOsrqPA8sdwaOW4KqIobqWdtxagg2wg7TAJSMoZ0X7mBHj5Gv1C4oDrHMzNtcOiRqirXrA2Elxn+CIAvmK4Oj8R2e/5T/B2jyx5hDNPQejv07R1n0IMakOU3G0Yalaj6Xn+GPKzyQTbF9YrLMsoMdlK10J1GDmFEgnM6OY2Nnew+0v0OJvieIuSWxm2JabVqxmV2XCn7g5lCjToijzFUxUhTwRV7xVBrtHzG7QvBW4lbzQdn8QEoq3Xpm3HMw4HzGFYvMTy+wgpZZZVdJY+MSzzL9F+i53Yl+81LlszG4DDQ+aN9tnWUQqurHYvrKlU/wADEAQTrD1ggQlfy8yzqfMu9Ixin+4xZVx2w/Qgvm/REt0S0V6sH0deiAurOfeXiDhSv3DLv2ssp72ilfEFFOwsPxE2S8AGAavtgv8AFz3lCKiiE1YofqBlQlUrXtcoC20iGUWNDtqDLw5uFSe8b4KjaXUzfJhafUZWNNkpfzJRXdQ/G1HKELQWHvTF1R5rR7pX3HZW6h+LEEwTh3G7/wCRt0j2QajTAzxPiI6RHWNdDE/zEzqJHxOdS5diLMtfpO99mJTmzzNYuJ49yIvRKzruI8MRvJ9S6/5F8/cU3AMG2G9xu2ynCMozpETivTHJKdIiX6yqI9IsToegYHQj6ncPRe8PCfCBC7Yft/cVLdUkSYxcbJWCmAggKrSdYwoFRY2SmLiCEb9XMUwq4NnMx+5FOzEeWLuG4QY9YXcY7jzMGPoQg4Q3GEp9BxHRExLnP8MK37uEUx30yzPdkCiY4+9jLXwROCztiOgFd0JmsPQvHAzOIGn3hPsEk/DCFF0NvhczifT9xLaRgWxb6NS/IE3wN46e9xUtqDktveSWW7U1mPO1M0zLNRDQV8XLaDJF8r/pEaZ0vURlgFJhvRFc+hlKpw8TBcYl94r03l3L7y4p6EnMpAPModFmIQ9iNxge4IivQLZXmUg29lK+oAuqrSvRPTn+OmC6y2qr2aSUlFHBX9xo1eAZ/aGvD4WPuVqDC+r2gSk1vOz2IEk/MsXPRu2vaMqQ5X/ccX8rIs9mDAK5pNvmyCV+dL9pe9sIHwRCI0VYRP3DKC2P7iEKpb2hu6Zh0zUfQf4EEmxfS5ngRxgGJApS/wBmJ2YTNCvhiL6573+iPqx9gK8MspSLwcxso0bQs+FxG2CjQAB9zG4vUT+4pV+i1/5BVgcOQiZDmi3GVUtM388xostOGfzcySXN3tmKYdlArFGC85gMQvCx4RzDwcULfVRLLNg53xaO3Zc0+1Y+3LvW8v7iVawcVL8pc9lo/pd/Us/OqS+j4iw3Fp2kdUVdhLP6Mb8p7SzQjbj4jR38ksaSZGX6ssdhFOvsy62PyRL+kw4lEr1iXu8RtuKdYERYy0zKjbFHYfEpcfcB3lOiX7Phmtd6iuQWDvEyzxE9e0OYhVwFwDFlUd9mj4COzPF/Mab+yFtiUXAMXK9SvqMYDkdfEolZa0n7ivgtdlrxHljNoQ5jr0dR3NppEuG5zDSZQeg29XBHUd+txxDcs+85clhv2qbAe8BKIerMNk7Es2CC0+AxMdWc0/MUgNcqyb5vSAUEdgmQue5Uyw+bb6Yk6rtl5OIzA11c4/uIl2SwFQ/uCzx7h3viLq4wR0dJexqO4Jcm2sRtCi6x6H0FWGBlfRO8StMyMF0lukuaC2f1xTPjG6SoAuHkYNnPAFxIQDvVfliVZngW/wDJa6hvRZjJAx6BNs28sCYZ31L3vf8AT0qJ/wDDBnUZaqKwHEu6SOhpIRL+UMzB9smRA6lhbAQauw7x4xCogxduFaG3JafOYEtQwA+0paQNHV5YXMK1+YqAzaoGj+5k9OMIRuJOefqXKZ1Tl4Ir8z8/wz6sZQCPRiG1ClKL+pbUR+PqUafGgR5ULnGn4GaEBz/cEZpWMq/UHPtSr+4+T9mH5ljNogp3zLFaNf6SBlALyQMtqnWT3xiKBcHCf1CsA+/++I43arLRBkbxwJSJZ4xhpgXbb9xiw23j/kHB2RfZAWxc2X01EsjsWCh53C71HF/kXqPZIZMZ94Sopu0Hi6j4T0LH6PtFQC4SPi35lRkuiPlfqIEDQ3vtSIVeq8F49ojJeZVi8RCWmHEEgwoWK5p9oJunhmXRHpT3gNj5lPVghlpS2fqA1TzENI+GbL4Jm8y0ixyy/X6leftMupEvJHti5eXItp8xWOrBfkiyi9DmIYIdel3kl53lncBTOaOsp1I25GKHp4ZtuXyqK3UvvxLrdh7zLrAzOs4jgnMdR3MX1czmGkY1G0NPodJwRMep6Mqws+YNZa6TFrtbhqX9AK2B5YL64bgLj8TTe8QFa+jZAtKnmxjuEdFIZLW7soUu6qfmAg/jiI+9gheHtiYQaTZiS6S+XM0g+HG3Xjl/UCAU0G/iHIuXV2pdg7Q3C6johXvHl9hcx9T3Aq/mHDxyLrUFK8xq5AnD3l1lnLL9QZSLsQNTLWXPxAl2j0LShvTrLosF8/zEgBzRG+fmuZtl9DBoo/BGkqOoBCoSGEW/MyAwsmhGhSdJEtdlDRZLq14C36haAK0sDMwA52acemyJ/MTDCVopp4J1JQAfiFoCsAyPsRHF7S8CAcrDAO+yjAE5W4jQn8S1ER2b9oUKnsyXzBlLjloB8xhqbhbQkpgu19CIgjugjEDa6/RFA7wKL+J996XLly79EJwgkcLLtS3DFLL8r+ZZjnh5/LLq5WVVHgYoC3VH4YxHAvBYkut+buUFdlszMBxWVz7xxKcWh4jsBFk/SBRe8NvxUtCicPGGtsNlhfTF5b837SkrQ2h/OMVzrQfNSqKnyXcHmXtMvpuYIh0Cn5ZVEG6vllYI+Y4guQ8bEI2I3WFitS4sJXm9xYYWkKvzHMP9nxN6TdGT/Us5qaGk+4FNKxeX5lGsm2q+y5c2M7YAwj21n4ZeXuyr7Iddcjfpi9BXcqM2aWyN6gaJxOfJcS7HtiC+p9yh18lS9a+I9UKaK8MW7L8lxQ09sRXo+49I/EQ4v3liX6y5BTlluafJEas9mKreh6ByGqIt7zG2FPaXbPszpCS7n6lDQ+IrszwqMWVwLXtEh7Mu7XnMITYeYW6MXOos5zEJUSJxEpdRcTUOfR16OozBmnp1nMNIuJcbE3PQ36LiMuE59HJDqp4fvEGFus0x+I5Q1zWJ5YRn2hDSyeZW7+quaig6GJY/ZKeVHTtK5oE6wDpFOQlxlKi66kS/9R5j5R4B+ZXsJk41FDIR+Q7EuX1j3UNXjmQ+oLiO8r43FFAGxagwC6ln4lEKJVukFBQb1uIM2PJV8wmADHH3GJhd0kfG4BZfs2zLAOysf5iBYj2WPG/hQD7rEVZGBmPeNZUeZa9+JYHScSfMYNK4oF+NQapuvFT4R1kVqz9xclXYUgKcZBAdol0Uer5levPqofC7gcYZltW8u795brsC5ia8rxLryttcEECmNZMxO7pvjCIaC97iNpbigzHqB6sqODccRI4FxKSgVyZZzJxVpeoh90OGQOd4indly5cv1wtV0mFmhu5qUKl2q5ekG51VQsI57riuFuUMR6SzTSCsjsqP1KwHGNFPmPUwq+FfOIEKHkUPsQ0ICsuSKVVzlx/E2hbflupjYZFjZM4J0F68xxhHS7I31Cm7D9yw2Ft0MY6Mc2A9oJlC+fyLgGXHdU/lAwD2KQtGFzonxf6gwFTypMLgaKxn2G5n3qFIoiiM1KvMnItq79IB7zq/1FodeBf2Sw7rzSHUheQw/MyVBXXl5IYldiSvDAVcDg17pLDadGt7NksjOzaH3BpJpgrft9wFnspSD3LI6ppeUfbD9T7tgluvxLHPzEwNbgOsWsKvaohOEehiXEz4ipHsJbmIdgy1x9xTmpnofMTPzHS9AVpeAjXcnlEqPhld5XeZ8yxxUwtfEcdAMzqCEhG3pFcOU8j5Jhu/hl1sTyS3oRoYnvN9zb4i3D0ZcXEZtNJepeX0NTiOIS0g1HEN+jqOvQz6DETuPpctpcrymcud0lDQTjsUwXBsCJ1QOky7lPKL1jxRe3H5S+pKGVnXaJ0TXibYp4maC+I0Fp5MrlbrcwyIYUHdlFND7RvusZewe0J7q0L87imz9br33D+2rqr46doWoOV8t3EzFKCO/EArBoO/YkqlUvl+pdNgnVyRFAJhEfqEtQOLRXaOhHk/ZjmYwUJXfnMADUq6aPBUoDLoK/BcboWbdlc8RjEMsI44JQd1qH4mLhBoFkiMANmLBrv6EqP80MsLzMFLDgwfUBxnFVaQEYrrklJs6Fyhsle13Gi2hOUeUXBdzRstVVjbQS8XUBKwe7UBum8XiU1m+qNRrpH2i+Xp6hP0xBlnctK/jn0Wk1bH0lwptcPECVCtVO5d7DRHeri0rD4IbKntB0gHFuDLNQy7vIwkCzVZ/cvMYddH3A0y4ICvMxd627e0oFoXnBD33H24ebM3liGyhd03uW4D1V+pal71nx7VNApcpV8kJj1gBm/VDQmt2rjpTAigsyl0+iEBL4yfSyhbaGB+YW5ReFPzBZdOxL+SBhz3LPpjcIW2r5pIFm15P2RJBXBUju66hQr4iN0BzapQvsyiFRBrIIQat3dBe5WhXWy2KWvXKahAClkofhgxzC8U+yO8pyqO2YCl8cT8kMINk0CnyB/MWSN4CfK/UXCMULyeFJ8oKq+Zk1t5lvVF9n3irU/9Ey4MRemOe4s4uW6RDuS3DLob84v2sh4BVGAvUAfHowyteJbyk6SMR0iL2y3WW6y3aC8fmZNxU/g+/R21bZc3FdZTKZURsjwYjTSjHZAG0+8XSq9vV9HUrBNvWuczWOox09D6cRcR9D1C29PeIR20HUFW6iscR6gl3GnLUKYJJbhXsEFNn2mIw7sDpzg/wQfCvzK2B9441juSjHtiFaB8Thoe0CYyweDSNmkhjUEpeREGqIpceww0MBWpIb+RBFF9oVGbZe44g6LiHS4Wks0dXmWKyYG73lNCOVN5o35iBtrYWO+ktNcGhGI4gOoCqxCyOMRnaIZX77hIwZGR71EKouKUp1WF17UITzc0ErkDcEg7eJf1KUyZqxvriOKIMtsPR9GP8QppTDki7su6wWQsd6mVrTaxBbGKilb7kVxNvSLresTMqvudJfzKqpCOa9vMElaTF79xJav6uK83NJ5QlKynxHTbcs5B7xFrLxDpU2cQDqjpFZrXRqOywOBY9E+8bFvXmPcn7sDYR63piGMFdVb8XLQA4R+Jhuor3Mysbbv0zKBmHdfPEdGXZELlQi+1Uf7zMK8GmpcF1FExQrqlVBAVxdmIXRyYb/EJHEulqFRYduTpMaBYYWVQoFx5FcQg8oFj5lBFBfBDtmNctcYWlNDOzX8S8RehQ/LGA5DzT+IodyuzSz2/Mo4V4TT6zEgI5sj9QmcPamiZVDvWFxTMWnSA7cfNVDNEO+pUoFZbgoheOdvaGhxnB/ZhzxRs+aid9gUe0wRdTbXtLUaHlox5lDnatofuZAXdkfF5lgFvKCvimEuhdun2sMxNP4EPsuHBCeLH43DeT0CR6jUe9imm5c5Z5qZbv2bjcx8o6rigOG7cvmf0iBpoxBqvmPCY3tFeY9qCuZThPiPAD4mssR1XlT0sGAYtDrBiuH2mX9pthIqPZBTGe0dM59H0Y6hv0r9dYw7uPHofTKNIz3hN+g4ZOagCmAm+pA4K9ozKfiGVYQrnnNzHcjzmGsvBBdKYrhEVOUxfVw5oerMORfaL8n2il3INgemT5IDIogtr6GZZFDhuLFkLMVpCorg7jB5p0ZTsjtFsokdLgbbD2j0zeAII2tkintRtjSMsVyexctdRXdgR8EwhJe2CKZEvYRTxUqIY2gXvUxwActoys7Vpl3NAF+0IGRwTwl4CM0A/9iW3IwUfEzHEWLL9aeBlPVBopMxiurx1qVyX5GV4x73LLC3FUWnzEuLfBjyPeM21A8wzInZnOw30l4COzAtg35jQRv4hzv2i+54l+G5iljmG6gZ7dZVMDPQiJZbrESOhFhuoYuq3qv6gJldZEVadOoE3wd4MbIGKsLPJBQW6xdfxGVIcsJCFq70QUQMcNQDVA2YPmNZLeTBIZKivJ8zSN1NmZ0Q1YOGUlgdVnsuDfQTsD6iNY4xp63L1LLGQ92VK+9F3vMJd7hLii0p6IuAJUJecnaGeTsKx+oCpDlK1Emb8BNpdTALcEwRmMjE0CHFkGKorZKjfYVr7jchekYiLU7yXBIUAaQ/EIeBAJ95lpAWl4/UwkndmG2fJAHNG33JaSVKbXP8AuscpYdIhK1a4BaNKrCkH9QJiiTOPdjV7ZwsxSuii/EZTK8rCNoBjy/KCWC1dqhMEFrQ1KeurFZUqVHgLH3MpLebD5EXmIl3YIEtDu/cslKGbtPxuOV5YIo3OyFnA+8ZvMxZSauImYkSC8DB4GV6sq0yzBqrLqPB3v0Hkup5fM8z5lEUG49hPAl3bAZzsleGClh1OY+rVS8Q2TS/UgxHTOZw9KuJcxJpHU5iz6MN1SL4b3g9PumoTj/wEpIpFKiIvlSrFMvzBnBGmo3KQLc8luHwB9GMAZ8hMcNx1pqCQhTcNMMuVox9geCVJ3F6xqubxshusuiBU4mLDMu8pBjSNlncBVbxTlpleQ11O68R4ZEu28mfzNVSYHDtAikwtA/DCXJwJh94EUKcigebuN1TjAx7xwlbLt6aOI15AXgJWAN95AT0CVJbPZqblqgaWNfMWgJ1HcZDJBdq4DtL7xCTWfNMys6wvGHhloOu7FV9/ChowbyVlroIfMLNsdoPYkd9Z7JKMUvvHJsfmUSkh0uIqZnYl8Rek76Iobwc1HFMdFzHGHmgVtjm1MAC/EtWwzgq5ol7mPzEyG60P+QcGKrN1FvVzwexC1q8FK98MAE+WCIWPcQybXlEfqLgteaXtiYEtX2S4Ojamqc8N1eAyoIcCU/MAX0XRUiQBN/8ASHStgiq8GVgEaFY+oVUqKf6cs7KmF8iSlLrUiyhFjtFPeGwPDGsZhrdyclFYMo0qryGQ7XCroGwa+YMktMBS3Ly37qxGUp4iVG5DVwtTHLSMpdjG0iw+GKuA2LVYxVglTsFuUno8H2MRAU5HCe1RylTAEJEsHZNQMK02q+xKl7yiv3E2zTOQXBWuXiR9mbs4FOTBBukX4mNSqpt2iS2mGgfUGBA82IuVGKyMEVlWRVS7nxW6pcNBZsGHYOTIB8w8dkv/ABG61NUcTFlxpW36laEl0BfaVwQ4zPvCKOawn4Y1D1taHmLsT5CPcafuVYbst/yS8/6M5ibp0wyk5ZbUC7nUX7R8/JFzqX3ikPP3FTbSkBfkjJUo2Wp9la9omwpEGI7uEIcEt7PiLaY14R6GNnqrXo+vEvE2jp/g8MXDOY6IowcwmBOITaGYwkQeZbv5II3eO4bmnZNeczkmcIjTRNCjHTLFXUQRU4zF8pTXHsuWWjM9YtrjlQci4lckZZl8tUlkMrZ5hCzZEcNUxxRTGJUVsPeXNpQEIxH0sJe5Xqwup77xwnxTYrDSXFdT5AYMIHODFhE97V9RX6Tb68GpaRBQ1XWgiHvmwnWctrFw7SfmXIM6wFYDuNmM0tjbSRkACbQx1YxR7GJNh7wpAWHb/KALb7wQhfvClZS9YQtRil1zDo0btdpZBCJt0R6ce8U4BorHal3UH1FhivYzBLVbosKoBnSSg4EuZK4C/UcRQLG+j5ijjaZHzLQ2+JSDYvZCH/VGCaAoCx9RCpdYPxAtGctpa2fAYQfKb/2UbrTwRSrzolTGAiimmKA5axn5gZJ43t95uszpMFI+8vwRTvao0+0H24wSkX3GqsSlaG5aCtOSdOuqkvLaO1wbNMU2bzELp3nczpW2hL6k3Qblza4tgyr26LfaHTbwWiyCcLiDTts1EUA2ddJZKDQDKM5RnF6lYLbQgfzHbS4C1GPgqfglHY5KUvaoiGb1xMMStJ5+SAyTyhf4CCQIMZBYJTC0Xu/eGcJBeDZ8ykpK8Ch77hX26lkruCnzAZJyKL7RVRjwQJKblIJKAvCin3jZeyMUL1Yz/rHDcLsbQBZ0cSUt7ORYpkLQXMYKfb7heCOVp7RF30RTBmpe5CPblNsWnEMLQQNXtxiytr1aHs3mBS6tE18EiWW9p/E/3F+Z0Hf7i49YD9TM1/GEmXX2iHXynnfhlJwzZA4SWMOZrAfM90pWoGGumY9ZXKKdIwu5mHMUWox9XVwhucpz66sXENwbN1HcdVLqXFxOIQYb9A4PmAGHhGM1OUgsKcBIMaDA4Ig1EK1LhzUyDcsqVEYi7YPVeJQKZZoYlHcWgEfUm4xtod5mAiH6QWyEblZ3Yo0RJq2N2w3baguWJNlwZ6QJvDCVnOLYeASPsldopULG7MpAV7wYu18zh9eY3jX3myna5cBtczBq2MDNTKimCKgxFax6w9FRK8HWLpvB2TMFZr8w1oXHSK2Fd45kpFqKieaLcgDiAwYEQIUw0jQuHmWYYQ3nMvDj0iNViyvAniHYO0QNDZrUTLtEVkOBxKVS8ASCiH3AlblvYFfMAbC1ZcqRk2mn4Y6EhmwYg0uTTFfPWMt4S04snqzFWVm7X5iKIdFl+ZUkh1LTEQmylKV7BSVGE0gjVV4z+YFqUcjd/cAYb4PmWS71VFKU2VLMWVoSUwCdhfeDiwGMGP8AyA4Bd1NR+EZw0iddK9tRo1n8L/sRKr9rp/czdIdUfuWx5aNssjnrh94+53TpEoscXRb8xJZMmCJS6gsD5CAlF6hXzDhQ5VkfcvYb5VufbUQpcH/QQS1jNjWWytfKx4HOrEoWXnKkJYDkNk1A8hMKLaTD9S3QNYFqIqi96/MWhXsPkSlCwdG+GL0luP8AlFGAMigEbdBzgXxKWHbV1/cpkuzhiViPUT4ZRJ4hcZ000vzQXhr2ubjbqbKlMcByYILxqJTFF/Y2w9kDXQlF5ONrKEyeXZ9o27PF0yKC9iKgC2l7WfUVWXOopCwB4foYdzYofiU8vtJPbczbqdR/cBvqBH4S+0E2CmCzNImZhzFrDB9YlaIB2JG2kiW4jtOzHsr0bbxOf4Xh9Dc49eZtjr0PQ69D+A3CrjudhD0lmW6nUQs3Fi7QKbnIRRcFADHAio5wsip0Ql3SAkXbiOUjH7UHVlIzSi1LA0feYMA8ENCBBSBDKXMQ6cB4SA8QygHERDoRz/klC2CpTLEtxNRiWpGEQqsS0qBg1oeZ/bEE7eI/avmddRvlxPJGhZmBfMa6JVAXFVVXeCNFUDkoJefmYFFgrro+qZhTVLieQuPxiI7WGqVLmIurhrdQ2DU7azSO460WKpFCN6qiLWQ3oS6wo8MoW/UdRLoL6Ym2T76xcaTaJGCKhNll+9SqsB2f7j6lXVhiNwTtGPeAo6IjfzDwmN3RcSwlYXT3uPKd0Bv6hg00ZELUMa0lUDt3lFW9Rv6mdB7o+zHFY6n6iIQHNpZAh1qR7II5EWN4UHzATbg43K+RT0lm27uzf1LaBK7tUQIL3dgTRcNjMsCWXwJhivYZsqICGeUajAAC+YsCqcNpNAABdm0yI9QOnzBH0lljYVIZtuNo/u/MpwvxV+MxI3QC3EoT3tkJkg4phOxLyoaWDWe8q0jq5+iEgXsA/MCAk4yMIWw5L2JhDbBWnmEtixdWy+UXWZ9pYETZKvzxNVoG3zFkrHIFPMEUAZxfmILu+EgU6yvr2lYTggYkL1TZ4htmlzjiUtA5swAUIXVWXyn1ATuAK8sCEfBVxUvOwrqPCh1lEo6BwG4iQVq6SVgZeUKZRWRwV34lgaA8kBDxaMrQsGG4kvcxpXP3i5zdkihdOq2/zLpbHdgfqXFBPRL3Jeq00ZPhjGDXIWfJEMJcrvLlryzvinWFPJMljXq6hzLxOYbnE59OZvjqcziMfVj6cwjErFpBY5hjvMq2YME6RjqtQSQqEmi5YrY6RUQYWpYxvr0mNk6S6C3vLUBM+H2iizLM+SU8QTZKivN1FLEcJPeJdiWDRrvGUAsHglYFSxunhg5mHmAW3PM71rqxt2RXQIIbwYo6QCpsS8saIFtoFVXMWsYM5ms3CkSpWBjTEFd5oBvvAm2oCyuJaygGxfSWMqsqo2IHbdwhcm3bUtdIrkzLdhG/FlrkJs6hN0mJiQdJog7bw9CDPO4SRVrJDF2HzGwsyjRcM0qYEW8z/hAlkl7ElpYd3YmmNs2vmYtWbMrjYOhsxfiX0RHRmOAlPHURxpYLZmjeWMysOFdw3lNt3uHKxatHxQdSCRQRb0a/EpLiPC3LlgCIKa8PEQUXZKxlFyD+oCQbozCQH0qA2EnOayvgGXA0PNzArIvu8EbWiSWLWLN0xvFnnG4YjPJUipK+hZYY9p3Al2Ry60ZYSly0sOy6gWfaLBQlVVEy5Y6uWVpcZ/7B70N4rc36t1vUQSoVggqJ8FIRZBVgawULZzC1wgZx4i0JBr6TGCcLRR5lSad5H6hoA6wkPmJDzybnXMYiSaMa0uRgx5fr/IlGVGhhaQl3SoC6VjUayqlhrcfCOVldAqJ4FdYcj2FELDlcbLKlhQ1w9MqzLyMR66Tnn5YtLtcYA/EolLzmJghDwbgSxOhLPeUAPLnEtBTwGz4msqkLaRytgUqRv/FxHVActh7RCFVgYpbBHLD8S8ZmadvfcvA+FhfhiOeygcQTI8gl1GulRDdxxCMzx6s5hHc5nE59dkdS5xH+Dr0fQjlh0GcInRxGyObgOEohoCLMWoDThvqzeRSqkqXCuJZlPlLoVKAbmYOWCrE95jRcf/bHqV+8d4EzZRFXDHcHmMyt7zAZZzDMI2WjiLU9zKNR3LJSYlh1bGAXAxFEIQ3CkbhdJj2haoYlGEQaWJS8sGftME9+YSgFxNlGcVLiBfEUtQ8S5irxAbgRz19ZlXlHAcJggRWQBrLuUrBfeDxjMEXFplbg7HcwjeDxioBwG+0GtgGxn7I8omfUTCJUyIpg6OYCkMsNkBqMUSW4lA2QKsy1BiOsFt4jqt9i5jdTpEy2faKF5RB1CzMxMmeY1Nj3hQSPAtUYnvBLlJPmR7PcKZg0dbViDoSKEfLttDUrBiZBhFeRBAAC7BH3L1Q4NH5EEC1ehBfoGmKeCgXcbDhBRlUFlxeK/Mcqy9sKzE4bu2X3W5XATno61jVpA4zCFoRy1B2tHm5roC6aRGjhwt/cRqa8sHvcCYnZErYvNlYiaHA6i6iTPLgK5PNsVLrwK6fuLHttsARJwK/cCH9H5UBA+7MDWCOx4jAscZKlQKR1sVdGnJZAlDeKMtanStxcUfKKBYHTyRAZfyhRIOW6fuALLHKWv2lWqA2rz7kF5VRiyaFLqI6VXdpoiATHQtOInyxhQPBf2QVlZ1uoHIPADFmnF119EVBvghZpO42TeAuExLtSajZvAN7LhM0fS6I6t+jCIDIlN34I3NrwK/caluoKPLEVYf8AGI7lRb/2NwxJ6ykwkGXicy4w36O5z6O/XbHU5nEdfwfXbLzFh1khBQSguocaIpAxklLZK+petRLNwhXMeL2pMMUrJtlyFQqgYu6MHoXzL+75lq3rzDsyfMMZZiuYwZBVrMsrLpZHMDqgbFgh6MVyKzkL7QoiiMjBwETkyC39syRTOxHaNYqYGzCnVy/WJEdsAyZsGYBcseYI2qEsHFyhckwVwfRlMKwBxCdyVF2Ujs8QzEGpToFTgpiB0CY7EVdKhbkFTMYBd8cRYFYj0uAcWROATgBA0gMbIZS+QRgmvtL1oQcQuBOmaSjLd6OJrkMxCQ/k6kNEue7KAb5j1KE6sT3HJINrh0MMI7tS1tA1tLcHBTcAqcukQyW7S9oHrlMIp9kYXBwGiWLpg0cQjaO1WQUnqBCMX04YFzqkWoA7FRd++YMFXuwZd1jhFUd6oyDKs06gIVw3V+Zg3ol5UfWcuo+KPJgeZiFlkQqXnaWMd3j2ELhRe24Y1hkFGWrk6LCGjZ66h3iiFlel9cCCHBhVfBHMgZ/sIRcB5RIhcsie0RafoUHzcp3HFUWV8qfUrZ1N3UGVbrAIgzzWSOLXUKmKLXJY12K1FC5kmUDAXNWGYPccBsfaObk4wvxAm+rMweQ+cHxEq0rtViV1niqRdbGwbC9kPNFit51BkCN4SJs11N/iUWK3JT8xA3L7J71NAdLH/sbKS/JsZ0aO8R8y0tkqrD7wDuBV8bxL3isileIHb8JXR6e8xHzKTUV5JjpCaDTCO4w3CM5l49QiyjknMIzj0uPqVcZohAJC6jcUTqCG2LmwhOocgLiyzvMTgj3j390L3PlmW6JhwETowR5LHeYuFiWxLKImJSbiqoFobBMWmqVBWWIf3TZl95uV7QxFALC9poj2JtCQGbMBC5t2qMmNzmNwV0zlMa0mIjYMxRz6AKP2gtpM8wog/CKvR9o/XGAWqIlwS2zqN6oLlpUUYQTdzIVhYhmChlM9JBZJaiwTa2KVW4VxUtuagC7girSJduGbb8R7cgtpDNVeZdkHiAuJnDLi5MwqI0LsiY3LJYMLtzJiFKrA9IKruaXLalHBJtWDlA9iSkEJ2YLhAM078Swva8koPdt4YCIVii8COWAd7g5AXq6mICeGFsOfmHUzV0KjALjrC0xLlbhtjfFqhFBddbM+VycZfBjZwghBaghoXyP6i4cvGF+8Vto9SwlDG3wcTLjbHTAfYN+kA+mHLGskMXafUofZLcAqC+VMADNFlTOtlxioBDjhzqUFv9iKSWNorcfYsM/EN0Q2YoV3iHmWgjhgPhmWI4SFYwDncEkNGmllEwHKye0pzxwmpYPh9wT4KsY6EVzcBYxdjuZ5E0dHzAeV4MogUh8FRSgA46ykUD1XGNZWHKFQNoNMkmxW8iEXb+yA4XRgMjFzqF9NQ6DKauZl6/Ls8BF76IEVHMhV5ymeJhwzbDDugcwCVmOpbw1FnU8xHrMzJxLviE9lhr15hFzOf4jygzmEfQ9H+XMHzCHCMMUYY5xc2KxgrmikAuUYvZihSy92LnPahTTZLbJqp7iZPLBFDPiO0VLgoTakw6sOuIvsD4nOjBKxYYYLZxs0pbFTFjDmc7KYhM0pFlOhnonG3KRljmg930DJgIPgzLTgj6bQswI7SwuTjzKcsxm6ZuDCjKYLtsCWJPcIu1LhlAGBKLidXTJQqWWjUX2kLnCNlGVMViKQQ8SkohcxlmliDLXA5hJRYg+ic6QTS5glQpMlkd4WEWIUNRi2qBq2yA0jOgwsHcEZYnMjKN4PSILkIWAAe8tqKdCIXq5qgj5ZuIEKuGssdCh74I8HvmVxhMUsiae6GmNIh4QGsXRlc535mzF0mEIGfkZTPtIMQDYQXSZI/wADIGQjpaltxeuyIIIKzjHZF5gSoq8xjBhiDSTZxZIbULqrHjScC2KH0SiamB4K/MZyDkyj0LmC02Yv0WjidHS5TQKdXUMx81Al03plEAncHSIQqegl/L6hKGBemFkRfOmUHVEQZdeibuWsN7FRIoL2Mxigsd6grR91ssF9eRM+0uAE7BmEA8vxHq7UUuIEExU22lblgVWdCgl8VoXNzkU1YVUwxjdhG1CcVT4lho3ix+Y1qi9Vyg1R4l1LlzmW5qVYX3LtNTDm4BwzPiZ3dsHUiy/8QT/0hHxPM4jLjBOf4nM2QnM0j6G/Rj/GllM3hhPeUOGL2iRUbSu5hExhuBYNxy0ZrI6AiBuoohtUoNkpjVQbAZmgVM5pC7bwuq2C0YbuWIHaM5dQKpHCU4ZO8EukGZVk2H2hWAstYgrAPaJYVAMxflRSrYAjCzV1LVBMjKTI2xUM3W43bZYymFwTkRWU1WJQ3Oc5jdmxD8kVLuZBXC4ZgOmYbweZtiSsqxYGpGYbohNkAXcCxyjGWEVkgmlEdpbJdpxFEeqXEdxluYImcMHnmJ0MogkIylLxcCp1HOVK4kZW9+e0u5cweZZfdDhG4ql8I7QjvA6bvVYEM291xBLM/KFAOnCp2p5WpaBfvKxyPM6pYJmWpfcjsI0ksnAEyIVgoVaiJCU+2WW5AaAol4VbssiLae6pcK91Kmn2uMosAHJUI2gnCslMbNYozRHfXtN6KESJ3QAkd9mhY5t+olepwpj7dAkUKUYSYD2IyyB6S45FekVR6dZbeynJMpb+GouVm9XJLFBnIURbLu6t+YrQbby2RBKDctQD6hti0x3KoEy94P2yz2eq3MgR1SqlJsANrESu4oQpFYUgyeudRdsG1ZkWp4xG2kecyuFeEVNieZhmesXqRzOPQK3DzDqMIDHY8kdSnwyycwMYQGzhl49eYR36am3pz6nPoYw59H059OPQGP0mI5KZtGH4Z5gzVRQtYRZsWrE6FA8EsXVzoiWsoEcaMNr9y0ckWmoK3KC5QWxN9YnthfYVLDKg21V9/QAGKljEGbLLVTEobTJrg8kphVowTOltgDVgwMzKniNBWJQaYQbqoRh5jUCpfRY1xNi1MbcxcGOyLWYiWS1SwWYIUxGJl+1CgHEKFMLFuGkZaZxUyzG4iLYJSruovVjWZZqLEhUBgPchaq1EgPkIWIzpBAjBlBscSixEDYd4hdLl+LSKFLiVU11PEUpwzfKg4BaC2yO5myw6q+ZRh1GPAa6oglUubj0DVmM+B08ysNrZcNoLrKdKm8QsnJzywwuHQlAPfTSFxGd43OZ2CJFg9VcQWzxWUFvMltQv6B4zGifSJiWl31TLI7Iflj0ajILVtVQtk3tLJUH1WI1CiZzwR+2DzCljM28wFIfHMZ0nZbCXRuqYiixsGLs7tTR/2JSiHIbqNNBOi2ULC64qDr9wYNMU64lxycNJkZPItCFr13dItVT0MNzSqzpg0x2YPmDoMd31aiRVONA9iWZ3XV1F9ovW4rwy3mW8QvnEVq2Iv+ETuRu43CUdyUSuiQs6QepMGmPZGzSnhiuvzLXcsIr1aY+nE5hH+JzCOZzDmOvQnv6cR9OPRN1qJuQgMYlPNQDkjqBhmomqNS42oYWtxFbEcoIZcwFdy8ogrm2B0tjbTBrpiuVibKZqiWrYBYgCCKrhhllnBMEpAJSkykSFuycOqmu3EMHp2Eryw3jOSSxgcq0jXKFBcyAzMCmgMocTk7iuIuiwtLwuAGotagEzLFkEzLGEhVcXozNki7CILumO5Zs9xMyFXbUsWsAVHrSpRiNyoKogZpFdmYLmIzCjJD4YiV1qFlLHMDc3KFZd5mVe0FTVRFWUAuMzlJnhUnVZT25bcVOFuPCsRZTCO05rRLTyyG4w7E/JEaih9wlBsdglsPHcV2R5mHt1NlHNStbyPELKgOLhYc8wwqhxcwBrguGA2tYi+1a6RNrZww2hd0YgqPjzMUh2ZU8DmMQuo2TU3QeIK2eiLCieXEUWwPsJeifDAbInpWoAlO9t4FM1wwwC7R3/AEQCzsYJJ7hMWA0EUhZ6KLuMLP1eT2lrTHHVx0FRhVozHY6oYcsLerliWSeGHDncnSPg3P2E1+ZtivEpIPsdYDrcdVh4zEVgXyx4KPEt1Zd8+lpCn/kroynpBL6QXpGGWpXkidviOOvvE9LiteJ2h6MG4+rv12ejuE49Df8AB36cSp1ca7mRuYC4kzCtWh14msh9Rji5c0wwLTpagFqxaFY7KQwqIhwR3AoIdIiZpMsvuE7JohDMkTrNy6nKIrlgm0cs1BBdxlq4u5q4rYxlZiSxljUIXOHEHiUME5SZ6CEadwuWyVjrMRwou/VBsHweiMlaNbyvnEl3nZI9tlIwYjxkEyVOICbVCcDE3mpYVrvLC1nH1BMjMKQnkYIahdQM15YlwMEoMwxkhMoNfEcKqhgfzBTmJXSVdVc0GC5igjE5Iyqj3mQI0mczYIypqWIZAlStUcNhGri3aZc8DmMRATSFOhEmmeVg26Mwill4uJK7wxoEKWrkfMZdO+7BsqUcxbY6RCADBMdYQOp6kbAbCmlepBAPIZiizzQiDzOEUyHsEpv5NTAAdDLDcO9xcwbvMtCLpDTd5R9R0jEcwOObudOnTBNMw5C7lUvTmogoIi2t094C7q4viMFIapUc7VXVbhSPuTPWWOIdUB1lvpKOJgkOwwRhOiSxlTtwSlcNxs2T3jnvOfTTLSCMCEA5LlOqQNDcsbPmKbILMMSV2gQtq6Tn1YN+riO/S5p6lTj0PS4xlw1GOzPplAq5WpzOMQGrUPFAYKK81OGEV5gA4jbQTnKVaHMciyKaQB4j6KRQzG5Cq1nQZQ3DYwvuIJHCUYIgalt4Y2wMA4puG2dS5sREK5MRspuJOZ2KjXCVytmpftD5ij9ktEYiBWahm1FORBGDLEHUEA0Ai1UgVkRQ0yu6grdzS1GrMSmIuuO8OiYrLG4trHoAlaSo6uI5CIag1xSiEYCpYsqWIS4VQwV51L1WXHcva4jDOlCCtfiNN2MyQhCCqzUdYDFWGom9wAhtkTiJqWo7a7ZclI2YYjOVVQRQvvLjYpgDUXW8pSsHhZUY003CEIeYHRHmXiDUENKCFtAHARriviK2D3JeAXKXGyUcHyyoWq6BLH2okuDpczBTV1K4BMOqddJcQB0vMFgTh0CPVjs0dCVY394y39+EbPzKyzWZjADOJ44Zli9EYxd1Fg9Go22PMx4lSoKZJTNOpnrUtNp8yvWWd3mV4fmUaVeZRMD3MTsR5mez4gneYld5UquYXCkLdp1SWjpB4qIPMzzPJ9yjuQls8eg+nMI6lzZHfrpGO4TiahD0Ys/HpctwTrfpFbtmwEQrAiRwgGCOUxc5RHgCmoJwEaajOY7JYVUSoEqLjvzG/mWZTQMQm2dCwTmAzCQXxEuSUYxAOYRbMOTSoLl1As1HUZjl3CQRzA6swZYQbgnS+YG3aXqtErLADcA7gNMr2soMMAdsKKtgG7ZXzHYWLu2AZSFRKuUvO8BkYPU2mGNW1GYMKdsBN1FdjHwUa8uIkrTF1lpESskadZY2WMSNBcw7KNhaOUygzQohdiD1lGBJkKiIGYxKoIsYgmWcsGzikBaGJjjcpl940yQsKzBFGU7SejAiySm0cyk1XVLBaeJWrq8McQF7EQXR7YcgvwQez85m3R7FR5QguivbUXCXIQTXIALEW40NXOajZYe0OgK6VcbAX2oieWd7ZZQjrqB1UasXK4z0MEqrpcQ9SZRHhmeYvSCQa5lzDC+tzDhi+KYrxBZbmIN/hiIj1mTp8z69LTwlnWCOb8wDs+IU6fmJXrmqh4nyS29/Mti4+hc2eI8wnE5fR1OIajuc+mnptA9ef4MJx6Ask4P6OCuNSlFRlhtRawVFuYs5YXzZUsuJ5S1S7FBCWZpXK2UswcNGIDhM9QhSdyhVpYWsXVDLBuZO5lq50mLZgBUQ1iI7lzmWXcscyzbFG7nFcu8wSme5kmZuDHc6iW7inMSl3FqCHrNajfNzAojNxYxH0yrkl6EQzcTTBBB1GFqN1mYF3FXabQiLv2hfBL5NlLSVYRcMMH0svallI6kF8JmUu2YLUt1aRulEZPxDPC4NkMxVjEDuVqjlLw8TAEbK3LUQrmG7Zi1EzZAumyItMO0MtBm8EgBlZn5Sxbt7RmVX4mXsPMo01yzX1xrBoQS0diFDCd2NwYO0H+wZQivrhGb7HkwFDj3iItD5S2cT/ASpur9VuNcFRe8OYxxErxK6jw+gW5PSukVG6MQmCmX1JVaZdMtLHcrozIVXxKOvzLucxvszHJOyVXErrFSWsIUIE6w9pqagyy9Su8aRIjPaD5mQzZ8w16c+iYhk9OZz6KczaDGc+rF9Dc4lxek0i4u3mYICysRzOq5U2yg4gjREI17ICxC7uAlGCVTEZzBG2KsMRvcCFLM2/TX4iLLHM4iYRbLqLCrTKOsvG80y5cv0tBzGszlrgiJeINJ3pYlhK3tL8Rt6g+EeGWGVRRGxzBpZKFA7l6giOsogDKH2RxhmEBaXHoQzjJBjdQc25dogDuokSjlZjbbLDeZaqWDDkWBvzBYcSwXxKzG4aAXThlgVcRUC/mLxEJviVSMKmBtJbkINS8x3BEz2RmdInLKdpoKEOy1dJtWC2C3LBtEgKZ30lBplFWwUw1VukoyB1cRJVI3bMoiqailO8BFLR7YTqB3bjp+CcBsgQrJFmlZa3cb8enLvFhoIiO5bwyxsmXaYeJXdikxU002Raesu5ddvQPvANlniNvRie0rp9S6abuUY98p6Qs5mR4gz3gowRzMvQWB0teYp0+GIdzz6NtSiDDN3mHo79OIenMd+rmbQjcd/wZcH1rInoJO4AJTD0laoV5Za9zWDcSJbiLGo0i3mCJpFvMVFjTmXMdQdAs4OKjt3OYTg0FupUwGJFqX6X/BOnoGO4mK3TAVkshRqF2ot7muWUGJc5izZCAhcvVAsqJSkVM7lGExWRDDCTOYmmOGJhDLUtmRxBhrEOCPtFYSyK4ImDiFWogx6RUuO7ahs8y+HENlI5b0xCswojLAQpEwi9EwLWYziahsYzDAiNS5foI5gF9nSMIHtEsBnKAYBgzYSvJZRGTrUwEpU41wQVhTkSjnLnHqlAisXaWGmuzLKziV3iXGYOHzDbGGM8jEWTEst6dI0Fwb0xJUYPC5Y7Pcm8CRHs8zLZLGVnIMocfcccPzDLMQNNwp2n+sGUplKcnfMV4fDMUOEjJsqYZRL8QElowkD0mJzuW9LlnSpc5udx8TpPzMdZ5TZ5hr059KxBz6M59DXo5fRjv1f4Goy7mY8y/DEW4g5l8OVxuxJZnl6TvlusvmWxR/CPoWw0BmuhLaEaTb0SrgGdklTVEt1m5SzmUhHojehUAwXSVXqRPRdMXUHEEuJu7g0pjcrcxA2QrPOj5ozNkECrxEpqIbuNOZSpYg1HOYiuHBe/wARJBJgIeYLlZalEpypgK7i+ELBjLZqHcIueiIFO4GxYgMEDFOhMBYxWYVOZXlxGoEIiVUreGFSzPMUuyJLzLv0TZKTcpaymup2I2VHqpRQXSB6h8Q6YzFCJyX0WLrRQQqjsSxTbn9Qg4KR6iztLOFPMVz8kz0xaqJ0MVFRRFHeIjw3ETOoJWZQ4bJb09GHi4tQYYY9Z8SvD7MuuEhbvMcMwlDEf+yxqF8k94U4+J5fMw7JRw/MryfERx8o8RqeEEdk7ErKfS/QvaPmc5ieLg6eZvHr68+nENziM16LHoufVh6Po+g2RloNxahTBFly5cv1XLl+hZfpZoZxkTlGDsSkuprAwHAilzGO4rFdZepaBu4Mg5rBZroSRvoUUlQWCsVNwTmLK1uJZhCLJcWmXZNM1l1qXeZdcsszFiHNidYIu5xMzkybgXcNZH0hfTEO4Ii7xpkY4BZq99I98VGw8QObiaLuOWGBqkiFoIai7sgnfoUDNJSwyrELLqIMvZmuQXnmI5JQjLqCCh5Zngw+h6EpOkEpzWSqPEEyHbiZAz67g9KqdJqAYHuS3ftsArH1IpeL3mVbHUiDCHozDSHZlHcaOGPeWNMtzcu7TsqNdIkecbMRrxKTWYsATcaaZnrG+T49F2QxprxLFyF9TEodZd5e4aiBAPNeYrZnxLSWr0i2Eh4lpy+8x2TLTUpP+Te/uWdp2VFEzyTEqOXERuZZTmVXMNT7Hrz6OoS/V1NZc29HUYejGMuaRly6ly+kv1uX6Zl+lwTQwXhiI207E2EM1EGMRV3Lmo01cVs+hfQTQs0ROJnUprVEdxtwnRIAIxlSoojoRqC6wLmDiMYWnpGZctlsyly5fos9MAglG8wdwCFHEVauBs3CMMRRmaRgeYo5YKzBCxjslNI6KzKo5FEJrUqw3E4MpVj4QKrFxVLzcHn0TgXUcMMVLTEsuYjuKzyoKrAzLKoEbTDdmTUZxmoJBLzBcMdtqGUM3Z3m8xO2i6MSIjZO7HIT3gqog6MzJLim+ssVctyfEa6fmJdka4Yj0uNPQvdiPUijZcs7Rx3mHmo9nxBTvKdQyhzAu30F30l9bm9MNBZngnvO+8o5qs7Sw1C1zKOZVabgubjhiFtkLJ4J4h3QtlEtlDx6WkqIxI2gY6wwVBXmnHpzLzFxCcTmM4mno79HUderH0IRhLlx9RcublMG8QTLty9kjTRE2iAOoPRKNoCYHMbrG8ZbQLhc6hGTJAkBZqcPOknVEU2BAMGIgSk7ImIkLsMPUC4ioMZphIsETCMJ1EWYRivSv4ETqMv0tUMy7Yi9ZtdysolB3lMJZVk1OYxCMxzmKDNwYtuJMNRFh1MzM0Q4MSLLizOcwamTcq9GFGWQYqxMGSWa2RcZriETiNQRJYMygUDdVDMIsc1NCZjVkjTUAjm5fwZx6PRgjBTLdYMvQ2QDsjZqXCt+YCsxFYLjpF2MTmMFLvcRMnMuXkgtIJ3nBae8QMZj3uCOZY7JThlJKgzfMsTRcrdRmPIyu87El6mWKAO8NtPtB8YjbmneGEofR2QTTTECU9IIxcEbBguyonC01qMYSVA9BrySvTmcx1COpcW5mazNx3OIx7Q1/IjLmYNoYJxOEiIrrKNxJxKcIg1A9JQahBXuFzcBBCo7FI5NjCDJOmnGQwUD00hWCbwzKiLylHM5zMlLCBR1LlsFUoNxVAS/QjihLRpl3KTMEYYAiKDKuJ/Eg5hqVNRblxg1LYrIi3EO8xDJMEsAzBUNPaUtM5iW4YjZA3lKmo9hCDcuhxiOGXcVTFs6IKYQZpdyoqIhua6YwvImMZQYQLLTEYGGIZhhizuOANkVVWYdUFSrpinWWHcbww+8I7Nh0gG0guUQ7Jk036KbSjJOBlIVfQ9U3pnUJVaYPgFhO+OjEjIy2V7SnzKiXZLQpyRRkbmemUOILtEOmMUQSnJ3nI9iAdDMlJAlHmYdYQqcwB5l+spivMtLcy79D3en3fTmMcx1COoMu3009Npx6Pqx9D0MC2QRySpmp0c6UhuBAcBL6EfaIYUsGdkW3EtcDHcRHcN4iWDvU6LBMBH4jkHaE8wRslXUIwh2R2wsxEJm4LlCvMvlRDeoqS7bLCGGyJZCKKfQly1KDGy4gyriel+twcQcxiTUuEGpRMzcZXA0QfQi7koYsNzNlgG2AU3LGWyGAO4zxLOsXFlJccEeYbhKFJY3BcqousLFQyiJKi7hi4lkCwKjKbhYpRIceSRRSdOWGIrjXS5ZWhgpKNxPJDmKmGTJDEwZmWyCcRwZfiIcVOcyie8adlRhT0LEoy3W427R7o9kqtMAg/B4gDoYibK/hURI27MFJYcx1ZqFdMq6MR6TuJhzAu5DYR3JnoMYAdkC6YIepK8ywj1i9pfb0PEJZgrz+rBuMI69OYvoXHc4j/HfqehDROjFW5yEVW47eYnOAG2HEnVIzuJTUy0lSM5UH1KOKwRzO7EVMEsS+0CMQYxzFOYWJlE1MmXphldItyw7iHM78LcxCS1BdpEHUBySoUIqD6QJGqAslbcKTZE9a9FNMF+ikSEuDC0UNSnKO4qpipcR3MGCqChaxxAILiIa1KLWo5Z7QWkCuIa36EGY5KYKpGGBheog3FTMelaTI0YlDNhVEFgHYZaQ8ZVwscQnYQQslnMwcah3xCDtOg4htmGNynDKasUcRs4hTuIPMRIoyqcRL3HsuGYqXURHPMYRlV2gPN+YNsgLyN+tDLeYntMGyYYYGbUcacMtZg1tljpJ4RK6kF6wZLHkqHS3DGyWTHJKXaPfGvEwgSjpAhoO8qcxg3H0dej6a+juNR1FhGN/xMt1ljO3L5RacwsQxmdcitkPyTHgi1CW2oZzAHcIGUQKlZLjGWzuK2YGVKVDmC8QRzB9ZkzIuGJkr0gYxdQrO7OsnXFKIbYaSpTOpEVOvKGLpLOI43BmGPpcSag3KGFGYnSJ630g5l3NMSqY4ZlBhglSlqPSQrKRIyl4nMRiXGhkM1GuailTCk7xLsguo6gVNQVyhnKcMOWVCr5iwYmUWZC2plCI5R3ARFpGql5hcslSqzcFFe2JswXKlvMSq0gtJHw01Gm40xK0y+pEOsUajDJmACzMs61LSd0QY9E1OcNQLCDAG7d4+7xBEpyRDpimWJfWURo9GUkFAJKMGahTZAdJaVuAjpO1gJYh1Mr0AneBbiCi7+nM2nMfR1L9dPR36MYa9H+Jg/DE5IfMSdRLFQmWkqaghgJc4mjFUOO4vDGOYUZhuZqIo2Uog7mYhHJiSlzRGMZmhJuOLHIsNwuxEcxIKSuNz03uVO4XKgLiXTHDLCYRssgElLcGVfoTcYYZvMzQNsRRIlehBhKWNmEEzcZgiBEpFxF4wwAmW0sJlK+JtEmpjEuWE2iJEl1id4o4mYChbSWa1Q6GUoZRyZEeKynMQs1NgRjbEuDxBdReCdxg7wXmIMEReYzchOVEgpuAjuRQxEciS3mWMb4Zm8kQxENypkbjR6yj2lsuJK7y07wppqHIDDWa8ykzVnou8RHiWJSQZ/2PglackF3hhTmWSztM9VO4g+ZR2yohTmCNQhLUlR94+jOY+jr+JxHcfUajFj/AzDgiBolDOBFFZYY3WKcwx3AMwYgVzKT0ipMOYUVcKeYCBBpg1HmGbTKKjEuUG5ZzLblLGOZSgWECIkWEMOYPoJcqb9QIrWSpSO24uksxEjcaEdQ6R9B9VOZXiClw0x16HoMC/RVQnKb9Iri3IUqgerM4uoggAjATUpY7ilQhC4fTXEYQZcSwWMStYcTG4g1cISRuSYTdRb3LiGXGpQscxZxcs7JnWydkqIcMStNzIy5uHQw65Tao7MVxENzuQDuJY++MWj6bIESamJYMuPmXBmUT2JsG2L1QE5Ey2uKNwZYxbsxRBExtuAnchQxOrAhVSzZLtSrTcLMJMVqW4fmWNqMGZgvebnMZzcYR9H01jGPqPR1/Acy/UHMxwXBSy4Ij1uN1gLLY1mSYYtxzmKRXmNyckdyuDqWxzMI4TRDKO/TTcxikO4LLgy4oZ5gwxafRvgFJkIKzFcMoIBIEHD6PqxZ9KMy+ckDK9SDXockumDBhRjJASmOtGMuJQgiHcUkl6u5Q16AQoYxyhPqjU4ipg0WMtYNmUgLHSWFpQ2TNcIYYqpgiQlhqGNozoQUgkL8k1Ktw8iOiKUPRxlBAYo0wRud2odco6ih1ERQ4ly4g8ypQxIYczPJDrYJoRXKVLSUh0MEbyQewy3GYibKhcxySnELUKe0ygJMkBr0EVmCaYcCHLO/MJnDslu5EKp7o+2fMSmnHpxDpH+Nj5/gG/Rj/ADL9A2TNGpHHp1wq3DZZOYlnp1UIz+hrHmOGHpK8xbPQbixLblUa5YSpiFLigjU5ly/TyIJaRYN5lKyCsQaZslTUFLh0ZyQ/lkSpQykK2VB6EuDBg6Q7wahv0BZFtFVAwdQLuIMyqBlE6S6gLlKLm9F+YuCMSEtiRlzXDKrwLWSlGvqO6m4XBjajNKBYZeQYlRdp0dwXeY4jnJHDMpUwY9kp4lrzLvcoY0gpD2ehS7RR3iErrErUuVcyleZWKMRRpgjfqYYkdwcBeYUcMKM0wDhqUvEAn0nhLGmC5mFlLzLSKyyKc4juAS4iylRY1IW2PaDPVuSWxbl59Hf87Lh/I16n0JssYSYkfoDD0SGYw1MnpOYal1M/oXkeZvOI8xeirI0YlxgxCj6GRce45ZqLFzLhkgpgWehRNa9DMlHoYqnNx4Ia9ABH+LFWPS69G8iV/EECJxGnoehAQOGA/MRa7JipZiDUJjziGooNwaFFMkB6DlmoOYrmLhiWEMqdzCDZLHsjgYFQuToZjqCG6jWJKOyIdRZcGblGJpEOGV0iQXEQJVxR6X6JcBOYM9EbZEJhi4wAi3FbuWkQzDuUiiDLm+J2RR6FOfRCECMphMiEmINyqcej6ShBYgQwyw3EMXGLpierVBSXD+J9XMf4VOPTy9BFUv8AQ4ISomWLGTc7vp3zOYS4Q3Its2i4jlgRIQZlYgxEjDPKXpJmOosWDBqX6TSSz0ESC+hpBzBsjDBZceanL/DUuDTDJKzHTGUM6cFP8D0u4pzBxLl3EuoCxgNiOoxrehiio+inMRSi4lDiNuTCHUZRKYdOhmZOZV2iRhrLEm2LhIt4I91HgRUyJeOYPkpmaVIqYSIimRgzCRhnRuI5l1qW5lriVQXJDPEfWiImTUGMHXWAWdRGyWMq4wnoLJhgeoyh9NiXUKQjLuDyXKWoUOrnkmWmWHMFsKMfSPzFsxEqdyA8wkIv+VdIUgeYJcfRzDcfRmvS/wCFwfTcnpY7jR9AczqMyI4ZeihJt6XFjHmOpWfRS4oMp6M/rbQiDHMYkuoMIogsUEYSobJj6KDTBPQKMOF/li9LmWpypSyo+h6VzHUNwZcEhuBqVMNyYZisgfXfoMXUPMtESrLQg3H0uFZMGSGUQBzA1udJYZoGI7NRJTMd1L+JarjpAnDAtEuOFuyKqnDAQmnoy2RekvrBFJUuYIsYJLG4N6j1TxH0GIQPMQczDUvrEOoolSoWQEqY9BeYdUoYwnmFkUmSIcyjsgDpgPoGBWYCUy60xJGO8S35RgW6f/gyvS0tBJz6M368en//2Q=="


def render_room_lobby():
    """Full-screen guest room with small, furniture-aligned interactive hotspots."""
    st.markdown("""
    <style>
      [data-testid="stSidebar"] { display:none !important; }
      [data-testid="stHeader"] { display:none !important; }
      .main .block-container { max-width:none !important; padding:0 !important; margin:0 !important; }
      .st-key-room_fullscreen {
        position:relative !important; width:100vw !important;
        height:calc(100vh - 2px) !important; min-height:620px !important;
        margin-left:calc(50% - 50vw) !important; padding:0 !important;
        overflow:hidden !important; background:#100905 !important;
      }
      .st-key-room_fullscreen > div[data-testid="stVerticalBlock"] {
        position:relative !important; height:100% !important; min-height:620px !important;
        gap:0 !important;
      }
      .room-photo-background {
        position:absolute; inset:0; width:100%; height:100%; z-index:0;
        background-size:cover; background-position:center center; background-repeat:no-repeat;
      }
      .room-photo-background:after {
        content:""; position:absolute; inset:0;
        background:linear-gradient(180deg,rgba(10,5,3,.24),transparent 22%,transparent 70%,rgba(10,5,3,.28));
        pointer-events:none;
      }
      .st-key-room_hotspot_fireplace, .st-key-room_hotspot_lp, .st-key-room_hotspot_bookshelf, .st-key-room_hotspot_checkout {
        position:absolute !important; z-index:5 !important; padding:0 !important; margin:0 !important;
      }
      .st-key-room_hotspot_fireplace { left:31.5% !important; top:43% !important; width:142px !important; }
      .st-key-room_hotspot_lp { left:60.5% !important; top:41% !important; width:142px !important; }
      .st-key-room_hotspot_bookshelf { right:5.5% !important; top:38% !important; width:142px !important; }
      .st-key-room_hotspot_checkout { right:2.4% !important; top:2.5% !important; width:118px !important; }
      .st-key-room_fullscreen .st-key-room_hotspot_fireplace div[data-testid="stButton"] > button,
      .st-key-room_fullscreen .st-key-room_hotspot_lp div[data-testid="stButton"] > button,
      .st-key-room_fullscreen .st-key-room_hotspot_bookshelf div[data-testid="stButton"] > button {
        min-height:42px !important; height:42px !important; width:100% !important;
        padding:0 10px !important; border-radius:3px !important;
        background:rgba(18,10,6,.58) !important; color:rgba(244,214,168,.82) !important;
        border:1px solid rgba(218,177,116,.44) !important; box-shadow:none !important;
        font-family:Georgia,serif !important; font-size:10px !important; letter-spacing:1.4px !important;
        transition:background .18s ease,border-color .18s ease,color .18s ease,transform .18s ease !important;
      }
      .st-key-room_fullscreen .st-key-room_hotspot_fireplace div[data-testid="stButton"] > button:hover,
      .st-key-room_fullscreen .st-key-room_hotspot_lp div[data-testid="stButton"] > button:hover,
      .st-key-room_fullscreen .st-key-room_hotspot_bookshelf div[data-testid="stButton"] > button:hover {
        background:rgba(50,31,17,.92) !important; color:#fff0d3 !important;
        border-color:#e4bc7e !important; transform:translateY(-1px) !important;
      }
      .st-key-room_fullscreen .st-key-room_hotspot_checkout div[data-testid="stButton"] > button {
        min-height:34px !important; height:34px !important; width:100% !important;
        background:rgba(15,8,5,.48) !important; color:#d5b58c !important;
        border:1px solid rgba(218,177,116,.32) !important; border-radius:3px !important;
        box-shadow:none !important; font-size:10px !important; letter-spacing:1.5px !important;
      }
      .st-key-room_fullscreen .st-key-room_hotspot_checkout div[data-testid="stButton"] > button:hover {
        background:rgba(50,31,17,.9) !important; border-color:#e4bc7e !important; color:#fff0d3 !important;
      }
      .room-corner-brand { position:absolute; z-index:3; top:22px; left:28px; color:#e1bc85;
        font-family:'Cormorant Garamond',Georgia,serif; font-size:17px; letter-spacing:3px;
        text-shadow:0 2px 8px #000; pointer-events:none; }
      .room-corner-brand span { display:block; margin-top:5px; font:10px Georgia,serif; letter-spacing:3px; color:#b18c61; }
      .room-bottom-note { position:absolute; z-index:3; left:28px; bottom:22px; color:#d6b88f;
        font-family:'Noto Serif KR',serif; font-size:12px; text-shadow:0 2px 8px #000; pointer-events:none; }
      @media (max-width: 760px) {
        .st-key-room_fullscreen { height:calc(100vh - 2px) !important; min-height:600px !important; }
        .room-photo-background { background-position:52% center; }
        .st-key-room_hotspot_fireplace { left:28% !important; top:43% !important; width:112px !important; }
        .st-key-room_hotspot_lp { left:54% !important; top:39% !important; width:112px !important; }
        .st-key-room_hotspot_bookshelf { right:4% !important; top:34% !important; width:112px !important; }
        .st-key-room_fullscreen .st-key-room_hotspot_fireplace div[data-testid="stButton"] > button,
        .st-key-room_fullscreen .st-key-room_hotspot_lp div[data-testid="stButton"] > button,
        .st-key-room_fullscreen .st-key-room_hotspot_bookshelf div[data-testid="stButton"] > button { font-size:9px !important; letter-spacing:.5px !important; }
        .room-corner-brand { top:15px; left:15px; font-size:13px; }
        .room-bottom-note { left:15px; bottom:15px; font-size:10px; }
      }
    </style>
    """, unsafe_allow_html=True)

    with st.container(key="room_fullscreen"):
        st.markdown(
            f'<div class="room-photo-background" style="background-image:url(data:image/jpeg;base64,{ROOM_BACKGROUND_JPEG_B64});"></div>'
            '<div class="room-corner-brand">RECORD HOTEL<span>MY ROOM · PRIVATE SUITE</span></div>'
            '<div class="room-bottom-note">오늘도, 당신의 방은 따뜻합니다.</div>',
            unsafe_allow_html=True
        )
        with st.container(key="room_hotspot_fireplace"):
            if st.button("♨  FIREPLACE", key="room_click_fireplace", use_container_width=True):
                st.session_state.my_room_view = "fireplace"
                st.rerun()
        with st.container(key="room_hotspot_lp"):
            if st.button("♫  LP PLAYER", key="room_click_lp", use_container_width=True):
                st.session_state.my_room_view = "lp"
                st.rerun()
        with st.container(key="room_hotspot_bookshelf"):
            if st.button("▤  BOOKSHELF", key="room_click_shelf", use_container_width=True):
                st.session_state.my_room_view = "bookshelf"
                st.rerun()
        with st.container(key="room_hotspot_checkout"):
            if st.button("CHECK-OUT", key="room_scene_checkout", use_container_width=True):
                logout_user()


def render_fireplace():

    st.markdown(
        '<div class="fireplace-container">'
        '<div class="fireplace-title">FIREPLACE</div>'
        '<div class="fireplace-subtitle">불빛을 바라보며 잠시 쉬어가세요.</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="fireplace">'
        '<div class="wood"></div>'
        '<div class="wood two"></div>'
        '<div class="fire"></div>'
        '<div class="fire-small"></div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="fireplace-note">'
        '이곳에서는 아무것도 하지 않아도 괜찮습니다.<br>'
        '불멍을 하거나, 아래의 소리를 틀어두고 천천히 쉬어가세요.'
        '</div>',
        unsafe_allow_html=True
    )

    ambient_html = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin:0;
    background:transparent;
    font-family:Georgia, serif;
}
.row {
    display:flex;
    gap:10px;
    justify-content:center;
    flex-wrap:wrap;
    padding:12px 0;
}
button {
    background:rgba(247,238,219,.05);
    color:#c49a70;
    border:1px solid rgba(190,145,92,.45);
    padding:11px 18px;
    cursor:pointer;
    font-family:Georgia, serif;
    letter-spacing:2px;
}
button:hover {
    background:rgba(197,145,88,.10);
}
#status {
    text-align:center;
    color:#96765d;
    font-size:12px;
    letter-spacing:2px;
    margin-top:8px;
}
</style>
</head>
<body>
<div class="row">
    <button id="fire">FIREPLACE</button>
    <button id="rain">RAIN</button>
    <button id="white">WHITE NOISE</button>
    <button id="stop">STOP</button>
</div>
<div id="status">AMBIENT OFF</div>

<script>
let ctx = null;
let master = null;
let source = null;
let gain = null;
let timer = null;

function setup() {
    if (!ctx) {
        ctx = new (window.AudioContext || window.webkitAudioContext)();
        master = ctx.createGain();
        master.gain.value = 0.055;
        master.connect(ctx.destination);
    }
    if (ctx.state === "suspended") ctx.resume();
}

function stopAll() {
    if (source) {
        try { source.stop(); } catch(e) {}
        source = null;
    }
    if (gain) {
        try { gain.disconnect(); } catch(e) {}
        gain = null;
    }
    if (timer) {
        clearInterval(timer);
        timer = null;
    }
    document.getElementById("status").textContent = "AMBIENT OFF";
}

function noiseBuffer() {
    const length = ctx.sampleRate * 2;
    const buffer = ctx.createBuffer(1, length, ctx.sampleRate);
    const data = buffer.getChannelData(0);

    for (let i = 0; i < length; i++) {
        data[i] = Math.random() * 2 - 1;
    }

    return buffer;
}

function playNoise(type) {
    setup();
    stopAll();

    source = ctx.createBufferSource();
    source.buffer = noiseBuffer();
    source.loop = true;

    gain = ctx.createGain();
    gain.gain.value = type === "white" ? 0.12 : 0.07;

    const filter = ctx.createBiquadFilter();

    if (type === "rain") {
        filter.type = "lowpass";
        filter.frequency.value = 2200;
    } else {
        filter.type = "lowpass";
        filter.frequency.value = 900;
    }

    source.connect(filter);
    filter.connect(gain);
    gain.connect(master);
    source.start();

    document.getElementById("status").textContent =
        type === "rain" ? "RAIN PLAYING" : "WHITE NOISE PLAYING";
}

function playFire() {
    setup();
    stopAll();

    const osc = ctx.createOscillator();
    const fireGain = ctx.createGain();

    osc.type = "sine";
    osc.frequency.value = 65;
    fireGain.gain.value = 0.02;

    osc.connect(fireGain);
    fireGain.connect(master);
    osc.start();

    source = osc;
    gain = fireGain;

    timer = setInterval(() => {
        if (!ctx) return;

        const crack = ctx.createOscillator();
        const crackGain = ctx.createGain();

        crack.type = "triangle";
        crack.frequency.value = 100 + Math.random() * 900;

        crackGain.gain.setValueAtTime(0.0001, ctx.currentTime);
        crackGain.gain.exponentialRampToValueAtTime(
            0.035 + Math.random() * 0.025,
            ctx.currentTime + 0.01
        );
        crackGain.gain.exponentialRampToValueAtTime(
            0.0001,
            ctx.currentTime + 0.09
        );

        crack.connect(crackGain);
        crackGain.connect(master);
        crack.start();
        crack.stop(ctx.currentTime + 0.1);
    }, 700);

    document.getElementById("status").textContent = "FIREPLACE PLAYING";
}

document.getElementById("fire").onclick = playFire;
document.getElementById("rain").onclick = () => playNoise("rain");
document.getElementById("white").onclick = () => playNoise("white");
document.getElementById("stop").onclick = stopAll;
</script>
</body>
</html>
"""

    components.html(ambient_html, height=100, scrolling=False)

# =========================================================
# MAIN
# =========================================================

if st.session_state.page == "main":

    if not st.session_state.main_entered:
        st.markdown(
            '<div class="welcome-area">'
            '<div class="welcome-small">WELCOME TO</div>'
            '<div class="welcome-title">RECORD HOTEL</div>'
            '<div class="welcome-line"></div>'
            '<div class="welcome-description">'
            '음악을 듣고, 발견하고, 잠시 머무는 작은 방'
            '</div></div>',
            unsafe_allow_html=True
        )
        left, center, right = st.columns([2, 1, 2])
        with center:
            if st.button("ENTER HOTEL", key="enter_room", use_container_width=True):
                st.session_state.main_entered = True
                st.rerun()
    else:
        letter_html = (
            '<div class="letter-wrap"><div class="letter-paper">'
            '<div class="letter-date">SEPTEMBER 28, 2026</div>'
            '<div class="letter-title">DEAR, GUEST</div>'
            '<div class="letter-body">'
            '이곳에는 조금 오래 머물러도 괜찮습니다.<br><br>'
            '누군가에게는 스쳐 지나갈 한 곡이, 누군가에게는 오래 기억될 밤이 되기도 하니까요.<br><br>'
            '이 호텔에서는 당신이 원하는 음악을 찾아 객실로 가져갈 수 있습니다.<br><br>'
            '그리고 음악이 필요한 밤에는, 당신만의 방에서 조용히 음악을 틀어보세요.<br><br>'
            '문은 이미 열려 있습니다.'
            '</div><div class="letter-sign">— RECORD HOTEL</div>'
            '</div></div>'
        )
        st.markdown(letter_html, unsafe_allow_html=True)
        if st.button("← BACK TO LOBBY", key="back_main_letter"):
            st.session_state.main_entered = False
            st.rerun()

# =========================================================
# ROOM SERVICE
# =========================================================

elif st.session_state.page == "choice":

    if st.session_state.choice_mode is None:
        st.markdown(
            '<div class="section-area">'
            '<div class="section-title">ROOM SERVICE</div>'
            '<div class="section-subtitle">오늘 밤 객실로 가져갈 음악을 골라보세요.</div>'
            '</div>',
            unsafe_allow_html=True
        )
        with st.container(key="room_service_actions"):
            left, right = st.columns(2, gap="large")
            with left:
                if st.button("노래 듣기", key="listen_choice", use_container_width=True):
                    st.session_state.choice_mode = "listen"
                    st.session_state.room_service_step = "search"
                    st.rerun()
            with right:
                if st.button("추천받기", key="recommend_choice", use_container_width=True):
                    st.session_state.choice_mode = "recommend"
                    st.session_state.cocktail_mood = None
                    st.session_state.cocktail_sips = 0
                    st.session_state.cocktail_recommendations = []
                    st.rerun()
        st.markdown(
            '<div style="text-align:center;color:#76563e;font-family:Georgia,serif;'
            'margin-top:35px;letter-spacing:2px;">ROOM SERVICE · OPEN ALL NIGHT</div>',
            unsafe_allow_html=True
        )

    elif st.session_state.choice_mode == "listen":
        st.markdown(
            '<div class="room-service-container">'
            '<div class="room-service-title">ROOM SERVICE</div>'
            '<div class="room-service-subtitle">객실로 가져갈 음악을 검색하세요. 선택한 음악은 MY ROOM의 LP로 이동합니다.</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("← BACK TO ROOM SERVICE", key="room_service_back_top", use_container_width=True):
            st.session_state.choice_mode = None
            st.session_state.search_results = []
            st.session_state.search_text = ""
            st.rerun()

        st.markdown('<div class="listen-search">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">FIND A RECORD</div>', unsafe_allow_html=True)
        search_col, button_col = st.columns([5, 1])
        with search_col:
            query = st.text_input(
                "SEARCH", value=st.session_state.search_text,
                placeholder="예: 아이유 / IU / 보이넥스트도어 / BOYNEXTDOOR / Love wins all",
                label_visibility="collapsed", key="music_search_input"
            )
        with button_col:
            search_clicked = st.button("SEARCH", key="music_search_button", use_container_width=True)

        search_type = st.radio("검색 기준", ["자동", "가수", "곡"], horizontal=True, label_visibility="collapsed")
        type_map = {"자동": "auto", "가수": "artist", "곡": "song"}

        if search_clicked and query.strip():
            st.session_state.search_text = query
            with st.spinner("호텔에서 음악을 찾는 중..."):
                st.session_state.search_results = search_music(query, type_map[search_type])
            st.rerun()

        if st.session_state.search_text:
            display_results(st.session_state.search_results)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.choice_mode == "recommend":
        # ---------------- COCKTAIL BAR ----------------
        st.markdown(
            '<div class="cocktail-header">'
            '<div class="cocktail-kicker">ROOM SERVICE · NIGHT CONCIERGE</div>'
            '<div class="cocktail-title">COCKTAIL BAR</div>'
            '<div class="cocktail-subtitle">오늘의 기분을 한 잔 골라주세요. 음악은 그 다음에 고를게요.</div>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.session_state.cocktail_mood is None:
            mood_cols = st.columns(4, gap="medium")
            for col, (key, config) in zip(mood_cols, MOOD_CONFIG.items()):
                with col:
                    mini_visual = cocktail_visual_html(config["color"], mini=True)
                    st.markdown(
                        f'<div class="order-slip {config["color"]}">'
                        f'<div class="slip-no">ORDER NO. {list(MOOD_CONFIG).index(key)+1:02d}</div>'
                        f'<div class="slip-label">{config["label"]}</div>'
                        + mini_visual
                        + f'<div class="slip-drink">{config["drink"]}</div>'
                        + f'<div class="slip-desc">{config["description"]}</div>'
                        + '</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown('<div class="cocktail-order-button-gap"></div>', unsafe_allow_html=True)
                    if st.button("ORDER THIS", key=f"order_mood_{key}", use_container_width=True):
                        st.session_state.cocktail_mood = key
                        st.session_state.cocktail_sips = 0
                        st.session_state.cocktail_recommendations = []
                        st.session_state.cocktail_recommendation_requested = False
                        st.rerun()

        else:
            if st.button("← BACK TO COCKTAIL BAR", key="cocktail_back_top", use_container_width=True):
                st.session_state.cocktail_mood = None
                st.session_state.cocktail_sips = 0
                st.session_state.cocktail_recommendations = []
                st.rerun()

            mood_key = st.session_state.cocktail_mood
            config = MOOD_CONFIG[mood_key]
            sips = st.session_state.cocktail_sips
            fill = max(0, 100 - sips * 17)

            st.markdown(
                f'<div class="selected-order">'
                f'<div class="selected-order-small">ROOM SERVICE ORDER</div>'
                f'<div class="selected-order-title">{config["label"]}</div>'
                f'<div class="selected-order-sub">{config["description"]}</div>'
                '</div>',
                unsafe_allow_html=True
            )

            # 칵테일과 마시기 버튼을 먼저 보여줍니다. 추천은 사용자가 원할 때 시작합니다.
            # Streamlit의 동기 실행 특성상 추천 API 호출 중 화면 상호작용을 막지 않도록
            # 음료를 먼저 제공하고 추천 요청은 별도 버튼으로 분리했습니다.
            recs = st.session_state.cocktail_recommendations
            drink_col, info_col = st.columns([1.02, 1.28], gap="large", vertical_alignment="top")

            with drink_col:
                st.markdown(
                    cocktail_visual_html(config["color"], fill=fill),
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="drink-name">{config["drink"]}</div>'
                    f'<div class="drink-state">{("FULL" if sips == 0 else f"{fill}% REMAINING")}</div>',
                    unsafe_allow_html=True
                )

                st.write("")
                sip_col, refill_col = st.columns(2, gap="small")
                with sip_col:
                    if st.button("TAKE A SIP", key="take_sip", use_container_width=True):
                        if sips < 6:
                            st.session_state.cocktail_sips += 1
                        st.rerun()
                with refill_col:
                    if st.button("다시 먹기", key="refill_drink", use_container_width=True):
                        st.session_state.cocktail_sips = 0
                        st.rerun()

            with info_col:
                st.markdown(
                    '<div class="concierge-card">'
                    '<div class="concierge-label">NIGHT CONCIERGE</div>'
                    '<div class="concierge-title">오늘의 한 잔 옆에<br>어울리는 레코드를 골랐어요.</div>'
                    '<div class="concierge-copy">현재 대한민국에서 인기 있는 음악을 우선으로, 선택한 기분과 장르에 맞는 실제 Apple 음악 카탈로그의 곡을 골라옵니다.</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                if not st.session_state.cocktail_recommendations:
                    st.markdown(
                        '<div class="ai-note" style="font-size:11px;line-height:1.8;margin:8px 0 12px;">'
                        '칵테일을 먼저 즐겨보세요. 준비되면 아래 버튼으로 오늘의 레코드를 불러올 수 있어요.'
                        '</div>',
                        unsafe_allow_html=True
                    )
                    if st.button("오늘의 노래 추천받기", key="start_cocktail_recommendations", use_container_width=True):
                        with st.spinner("CONCIERGE IS CHOOSING RECORDS..."):
                            recs, used_ai = get_ai_recommendations(mood_key)
                        st.session_state.cocktail_recommendations = recs
                        st.session_state.cocktail_ai_used = used_ai
                        st.session_state.cocktail_recommendation_requested = True
                        st.rerun()

                st.markdown(
                    '<div class="recommendation-title">TONIGHT\'S RECORDS</div>',
                    unsafe_allow_html=True
                )
                if recs and st.session_state.get("cocktail_ai_used", False):
                    st.markdown('<div class="ai-note">AI CONCIERGE · MOOD MATCHED · KOREA POPULAR FIRST</div>', unsafe_allow_html=True)
                elif recs:
                    st.markdown('<div class="ai-note">CONCIERGE · FALLBACK MENU · KOREA POPULAR FIRST</div>', unsafe_allow_html=True)

                if recs:
                    for index, result in enumerate(recs[:5]):
                        artwork = result.get("artworkUrl100", "")
                        track = escape(result.get("trackName", "제목 없음"))
                        artist = escape(result.get("artistName", "아티스트 없음"))
                        album = escape(result.get("collectionName", "앨범 정보 없음"))

                        with st.container(border=True):
                            image_col, text_col = st.columns([0.8, 3.4], gap="small", vertical_alignment="center")
                            with image_col:
                                if artwork:
                                    st.image(artwork, width=68)
                            with text_col:
                                st.markdown(
                                    f'<div class="compact-rec-title">{track}</div>'
                                    f'<div class="compact-rec-meta">{artist}<br>{album}</div>',
                                    unsafe_allow_html=True
                                )

                            if result.get("previewUrl"):
                                st.audio(result["previewUrl"])

                            if st.button(
                                "TAKE TO MY ROOM",
                                key=f"cocktail_take_{index}_{result.get('trackId')}",
                                use_container_width=True
                            ):
                                add_to_room(result)
                                st.session_state.my_room_view = "lp"
                                st.session_state.page = "my_room"
                                st.rerun()
                elif st.session_state.get("cocktail_recommendation_requested", False):
                    st.markdown(
                        '<div class="no-result" style="margin-top:20px;">'
                        '오늘 밤에 맞는 레코드를 찾지 못했어요.<br>'
                        '다시 추천을 요청하면 다른 레코드를 찾아볼게요.'
                        '</div>',
                        unsafe_allow_html=True
                    )

            st.write("")
            if st.button("← BACK TO ROOM SERVICE", key="recommend_back", use_container_width=True):
                go_room_service()

# =========================================================
# MY ROOM
# =========================================================

elif st.session_state.page == "my_room":

    if not st.session_state.logged_in:
        st.markdown(
            '<div class="section-area" style="margin-bottom:30px;">'
            '<div class="section-title">MY ROOM</div></div>',
            unsafe_allow_html=True
        )

        if not st.session_state.my_room_checkin_open:
            st.markdown(
                '<div class="auth-box" style="margin-top:0;">'
                '<div class="auth-subtitle">객실에 들어가려면 먼저 CHECK-IN이 필요합니다.</div>'
                '</div>', unsafe_allow_html=True
            )
            gate_left, gate_center, gate_right = st.columns([2,1,2])
            with gate_center:
                with st.container(key="checkin_gate_action"):
                    if st.button("CHECK-IN", key="open_checkin", use_container_width=True):
                        st.session_state.my_room_checkin_open = True
                        st.session_state.auth_mode = "login"
                        st.rerun()
            with st.container(key="checkin_gate_back"):
                if st.button("← BACK TO LOBBY", key="my_room_back_gate", use_container_width=True):
                    st.session_state.page = "main"
                    st.session_state.my_room_checkin_open = False
                    st.rerun()
        else:
            st.markdown(
                '<div class="auth-box"><div class="auth-title">CHECK-IN</div>'
                '<div class="auth-subtitle">ROOM KEY를 입력하거나 새로운 GUEST로 등록하세요.</div></div>',
                unsafe_allow_html=True
            )
            auth_left, auth_right = st.columns(2)
            with auth_left:
                if st.button("CHECK-IN", key="auth_login_tab", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()
            with auth_right:
                if st.button("NEW GUEST", key="auth_signup_tab", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.rerun()

            if supabase is None and SUPABASE_CONFIG_ERROR:
                st.error(SUPABASE_CONFIG_ERROR)
            email = st.text_input("EMAIL", placeholder="guest@example.com", key="auth_email")
            password = st.text_input("ROOM KEY", type="password", placeholder="비밀번호", key="auth_password")
            password_confirm = ""
            if st.session_state.auth_mode == "signup":
                password_confirm = st.text_input("ROOM KEY AGAIN", type="password", placeholder="비밀번호를 다시 입력하세요", key="auth_password_confirm")

            if st.session_state.auth_mode == "login":
                if st.button("ENTER MY ROOM", key="login_submit", use_container_width=True):
                    if not email.strip() or not password:
                        st.warning("이메일과 비밀번호를 입력해 주세요.")
                    else:
                        ok, message = login_user(email.strip(), password)
                        if ok:
                            st.session_state.my_room_view = "room"
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            else:
                if st.button("CREATE ROOM KEY", key="signup_submit", use_container_width=True):
                    if not email.strip() or not password:
                        st.warning("이메일과 비밀번호를 입력해 주세요.")
                    elif password != password_confirm:
                        st.warning("두 비밀번호가 일치하지 않습니다.")
                    elif len(password) < 6:
                        st.warning("비밀번호는 6자 이상으로 입력해 주세요.")
                    else:
                        ok, message = signup_user(email.strip(), password)
                        if ok:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

            if st.button("← BACK", key="my_room_back_auth", use_container_width=True):
                st.session_state.my_room_checkin_open = False
                st.rerun()

    else:
        user_email = ""
        if st.session_state.current_user is not None:
            user_email = getattr(st.session_state.current_user, "email", "") or ""

        view = st.session_state.my_room_view

        if view == "room":
            render_room_lobby()
            st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_room", use_container_width=True):
                go_room_service()

        elif view == "fireplace":
            render_fireplace()
            st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
            nav_left, nav_center, nav_right = st.columns([1,2,1])
            with nav_center:
                if st.button("← BACK TO MY ROOM", key="back_room_from_fire", use_container_width=True):
                    st.session_state.my_room_view = "room"
                    st.rerun()
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_fire", use_container_width=True):
                go_room_service()

        elif view == "lp":
            st.markdown('<div class="room-tabs">PLAY YOUR RECORD</div>', unsafe_allow_html=True)
            render_lp_player(st.session_state.current_record)
            nav_left, nav_center, nav_right = st.columns([1,2,1])
            with nav_center:
                if st.button("← BACK TO MY ROOM", key="back_room_from_lp", use_container_width=True):
                    st.session_state.my_room_view = "room"
                    st.rerun()
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_lp", use_container_width=True):
                go_room_service()

        elif view == "bookshelf":
            st.markdown(
                '<div class="room-service-container"><div class="room-service-title">BOOKSHELF</div>'
                '<div class="room-service-subtitle">책장에 두고 싶은 책을 모아두세요.</div></div>',
                unsafe_allow_html=True
            )
            with st.form("add_room_book_form", clear_on_submit=True):
                book_title = st.text_input("책 제목", placeholder="예: 책 제목을 입력하세요")
                book_author = st.text_input("작가", placeholder="작가 이름")
                book_note = st.text_input("짧은 메모 (선택)", placeholder="이 책을 고른 이유")
                submitted_book = st.form_submit_button("책장에 추가")
                if submitted_book:
                    if book_title.strip():
                        st.session_state.room_books.append({"title": book_title.strip(), "author": book_author.strip(), "note": book_note.strip()})
                        st.rerun()
                    else:
                        st.warning("책 제목을 입력해 주세요.")

            if not st.session_state.room_books:
                st.markdown(
                    '<div class="room-record-empty">아직 책장에 등록한 책이 없습니다.<br>위에서 실제 책 제목과 작가를 추가해 주세요.</div>',
                    unsafe_allow_html=True
                )
            else:
                for book_index, book in enumerate(st.session_state.room_books):
                    book_col, detail_col, remove_col = st.columns([1, 5, 1.2], vertical_alignment="center")
                    with book_col:
                        st.markdown('<div style="font-size:32px;text-align:center;">📖</div>', unsafe_allow_html=True)
                    with detail_col:
                        st.markdown(
                            '<div class="room-record-title">' + escape(book.get("title", "책")) + '</div>'
                            '<div class="room-record-meta">' + escape(book.get("author", "")) + '</div>'
                            + ('<div class="room-record-meta">' + escape(book.get("note", "")) + '</div>' if book.get("note") else ''),
                            unsafe_allow_html=True
                        )
                    with remove_col:
                        if st.button("꺼내기", key=f"remove_room_book_{book_index}", use_container_width=True):
                            st.session_state.room_books.pop(book_index)
                            st.rerun()
                    st.markdown('<div style="height:1px;background:rgba(199,157,109,0.10);margin:8px 0 16px 0;"></div>', unsafe_allow_html=True)

            st.caption("참고: 현재 책 목록은 이 앱 세션에 저장됩니다. 계정별로 영구 저장하는 기능은 별도 DB 연동 단계에서 추가할 수 있어요.")

            # Keep the existing saved-record collection available separately from physical books.
            st.markdown('<div class="room-tabs" style="margin-top:34px;">MY RECORDS · 객실에 가져온 음반</div>', unsafe_allow_html=True)
            if not st.session_state.room_records:
                st.caption("아직 객실로 가져온 음반이 없습니다. ROOM SERVICE에서 음악을 선택해 주세요.")
            else:
                for record_index, record in enumerate(st.session_state.room_records):
                    record_art_col, record_info_col, record_action_col = st.columns([1, 4, 1.5], vertical_alignment="center")
                    with record_art_col:
                        if record.get("artwork"):
                            st.image(record["artwork"], width=72)
                    with record_info_col:
                        st.markdown(
                            '<div class="room-record-title">' + escape(record.get("track", "RECORD")) + '</div>'
                            '<div class="room-record-meta">' + escape(record.get("artist", "")) + '<br>' + escape(record.get("album", "")) + '</div>',
                            unsafe_allow_html=True
                        )
                    with record_action_col:
                        if st.button("PLAY ON LP", key=f"cabinet_play_{record_index}_{record.get('track_id')}", use_container_width=True):
                            st.session_state.current_record = record
                            st.session_state.my_room_view = "lp"
                            st.rerun()
                        if st.button("RETURN", key=f"cabinet_return_{record_index}_{record.get('track_id')}", use_container_width=True):
                            remove_from_room(record.get("track_id"))
                            st.rerun()

            nav_left, nav_center, nav_right = st.columns([1,2,1])
            with nav_center:
                if st.button("← BACK TO MY ROOM", key="back_room_from_shelf", use_container_width=True):
                    st.session_state.my_room_view = "room"
                    st.rerun()
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_shelf", use_container_width=True):
                go_room_service()

