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
    min-height: 82vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.section-title {
