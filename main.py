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
    min-height: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    text-align: center;
    padding: clamp(54px, 8vh, 88px) 20px 0;
    box-sizing: border-box;
}

.section-title {
    color: #d5a56d;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 48px;
    letter-spacing: 6px;
    margin-bottom: 12px;
}

.section-subtitle {
    color: #96765d;
    font-family: "Noto Serif KR", serif;
    font-size: 14px;
    letter-spacing: 2px;
    margin-bottom: 0;
    line-height: 1.9;
}

/* ROOM SERVICE home actions: keep them close enough to read as one composition. */
.st-key-room_service_actions {
    width: min(920px, 88vw);
    margin: clamp(38px, 6vh, 64px) auto 0;
}
.st-key-room_service_actions > div[data-testid="stHorizontalBlock"] {
    gap: clamp(16px, 3vw, 32px) !important;
}
.st-key-room_service_actions div[data-testid="stButton"] > button {
    min-height: 62px !important;
    background: rgba(247, 238, 219, .025) !important;
    border: 1px solid rgba(190, 145, 92, .48) !important;
    color: #dfbd91 !important;
    font-family: "Noto Serif KR", serif !important;
    font-size: 16px !important;
    letter-spacing: 2px !important;
    box-shadow: none !important;
}
.st-key-room_service_actions div[data-testid="stButton"] > button:hover {
    background: rgba(197, 145, 88, .10) !important;
    border-color: #d5a66c !important;
    color: #f2dfc1 !important;
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
    margin: 28px auto 18px;
    padding: 32px 38px;
    box-sizing: border-box;
    background: rgba(247,238,219,0.045);
    border: 1px solid rgba(199,157,109,0.28);
    border-radius: 2px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
}
.auth-title {
    color: #d5a56d;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 42px;
    font-weight: 400;
    line-height: 1.25;
    letter-spacing: 5px;
    text-align: center;
}
.auth-subtitle {
    color: #c1a58b;
    font-family: "Noto Serif KR", serif;
    font-size: 14px;
    font-weight: 400;
    text-align: center;
    margin: 10px 0 18px 0;
    line-height: 1.9;
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
    .section-area { padding-top: 46px; }
    .st-key-room_service_actions { width: 92vw; margin-top: 34px; }
    .st-key-room_service_actions > div[data-testid="stHorizontalBlock"] { gap: 12px !important; }
    .st-key-room_service_actions div[data-testid="stButton"] > button { min-height: 54px !important; font-size: 14px !important; letter-spacing: 1px !important; }
    .auth-box { padding: 24px 20px; }
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
</style>
"""

try:
    st.html(CSS)
except Exception:
    st.markdown(CSS, unsafe_allow_html=True)



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

ROOM_BACKGROUND_JPEG_B64 = "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"


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
        background:linear-gradient(180deg,rgba(10,5,3,.16),transparent 20%,transparent 74%,rgba(10,5,3,.22));
        pointer-events:none;
      }

      /* 투명 핫스팟: 평소에는 사진을 가리지 않고, 마우스를 올렸을 때만 표시 */
      .st-key-room_hotspot_fireplace, .st-key-room_hotspot_lp,
      .st-key-room_hotspot_bookshelf, .st-key-room_hotspot_checkout {
        position:absolute !important; z-index:5 !important;
        padding:0 !important; margin:0 !important; min-width:0 !important;
      }
      .st-key-room_hotspot_fireplace {
        left:29.5% !important; top:49.5% !important;
        width:10.5% !important; height:17.5% !important;
      }
      .st-key-room_hotspot_lp {
        left:57.1% !important; top:43% !important;
        width:11.5% !important; height:10.5% !important;
      }
      .st-key-room_hotspot_bookshelf {
        left:80.1% !important; top:8.5% !important;
        width:19.2% !important; height:57% !important;
      }
      .st-key-room_hotspot_checkout { right:2.4% !important; top:2.5% !important; width:118px !important; }

      .st-key-room_hotspot_fireplace > div,
      .st-key-room_hotspot_lp > div,
      .st-key-room_hotspot_bookshelf > div,
      .st-key-room_hotspot_fireplace div[data-testid="stVerticalBlock"],
      .st-key-room_hotspot_lp div[data-testid="stVerticalBlock"],
      .st-key-room_hotspot_bookshelf div[data-testid="stVerticalBlock"],
      .st-key-room_hotspot_fireplace div[data-testid="stButton"],
      .st-key-room_hotspot_lp div[data-testid="stButton"],
      .st-key-room_hotspot_bookshelf div[data-testid="stButton"] {
        height:100% !important; min-height:0 !important; gap:0 !important;
      }
      .st-key-room_fullscreen .st-key-room_hotspot_fireplace div[data-testid="stButton"] > button,
      .st-key-room_fullscreen .st-key-room_hotspot_lp div[data-testid="stButton"] > button,
      .st-key-room_fullscreen .st-key-room_hotspot_bookshelf div[data-testid="stButton"] > button {
        position:relative !important; display:block !important;
        min-height:0 !important; height:100% !important; width:100% !important;
        margin:0 !important; padding:0 !important; overflow:visible !important;
        border-radius:5px !important; background:transparent !important;
        color:transparent !important; font-size:0 !important; line-height:0 !important;
        border:1px solid transparent !important; box-shadow:none !important;
        cursor:pointer !important; transition:background .18s ease,border-color .18s ease,box-shadow .18s ease !important;
      }
      .st-key-room_fullscreen .st-key-room_hotspot_fireplace div[data-testid="stButton"] > button:hover,
      .st-key-room_fullscreen .st-key-room_hotspot_lp div[data-testid="stButton"] > button:hover,
      .st-key-room_fullscreen .st-key-room_hotspot_bookshelf div[data-testid="stButton"] > button:hover,
      .st-key-room_fullscreen .st-key-room_hotspot_fireplace div[data-testid="stButton"] > button:focus-visible,
      .st-key-room_fullscreen .st-key-room_hotspot_lp div[data-testid="stButton"] > button:focus-visible,
      .st-key-room_fullscreen .st-key-room_hotspot_bookshelf div[data-testid="stButton"] > button:focus-visible {
        background:rgba(236,183,101,.16) !important;
        border:1px solid rgba(255,220,157,.9) !important;
        box-shadow:inset 0 0 0 1px rgba(255,231,185,.24),0 0 22px rgba(237,169,80,.22) !important;
        outline:none !important;
      }
      .st-key-room_fullscreen .st-key-room_hotspot_fireplace div[data-testid="stButton"] > button:hover:after,
      .st-key-room_fullscreen .st-key-room_hotspot_lp div[data-testid="stButton"] > button:hover:after,
      .st-key-room_fullscreen .st-key-room_hotspot_bookshelf div[data-testid="stButton"] > button:hover:after {
        position:absolute; left:50%; bottom:7px; transform:translateX(-50%); white-space:nowrap;
        color:#ffe8c0 !important; font:10px/1.2 Georgia,serif !important;
        letter-spacing:1.5px !important; text-shadow:0 1px 5px #000;
        background:rgba(18,10,6,.82); border:1px solid rgba(226,183,120,.58);
        border-radius:2px; padding:6px 8px; pointer-events:none;
      }
      .st-key-room_fullscreen .st-key-room_hotspot_fireplace div[data-testid="stButton"] > button:hover:after { content:"FIREPLACE"; }
      .st-key-room_fullscreen .st-key-room_hotspot_lp div[data-testid="stButton"] > button:hover:after { content:"LP PLAYER"; }
      .st-key-room_fullscreen .st-key-room_hotspot_bookshelf div[data-testid="stButton"] > button:hover:after { content:"BOOKSHELF"; }
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
        .st-key-room_hotspot_fireplace { left:26% !important; top:51% !important; width:12% !important; height:17% !important; }
        .st-key-room_hotspot_lp { left:56% !important; top:44% !important; width:14% !important; height:11% !important; }
        .st-key-room_hotspot_bookshelf { left:78% !important; top:9% !important; width:21% !important; height:55% !important; }
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
            if st.button("FIREPLACE", key="room_click_fireplace", use_container_width=True):
                st.session_state.my_room_view = "fireplace"
                st.rerun()
        with st.container(key="room_hotspot_lp"):
            if st.button("LP PLAYER", key="room_click_lp", use_container_width=True):
                st.session_state.my_room_view = "lp"
                st.rerun()
        with st.container(key="room_hotspot_bookshelf"):
            if st.button("BOOKSHELF", key="room_click_shelf", use_container_width=True):
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

