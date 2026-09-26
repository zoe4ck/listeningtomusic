import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    page_title="RECORD ROOM",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# ---------------------------------------------------------
# 기본 Streamlit 스타일
# ---------------------------------------------------------
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Pretendard",
                     "Apple SD Gothic Neo", sans-serif;
    }
    .stApp {
        background: #17100b;
    }
    header[data-testid="stHeader"] {
        background: transparent;
    }
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------------
# RECORD ROOM 전체 HTML
# ---------------------------------------------------------
html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0,
               maximum-scale=1.0,
               user-scalable=no">
<title>RECORD ROOM</title>
<style>
/* =====================================================
   RESET
===================================================== */
* {
    box-sizing: border-box;
}
html,
body {
    margin: 0;
    padding: 0;
    width: 100%;
    min-height: 100%;
}
body {
    background:
        radial-gradient(
            circle at 50% 20%,
            rgba(255, 219, 173, 0.08),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #120c08 0%,
            #24160e 45%,
            #100a06 100%
        );
    color: #f6eadb;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Pretendard",
        "Apple SD Gothic Neo",
        sans-serif;
    overflow-x: hidden;
}
/* =====================================================
   WOOD TEXTURE
===================================================== */
body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        repeating-linear-gradient(
            90deg,
            rgba(255,255,255,0.015) 0px,
            rgba(255,255,255,0.015) 2px,
            transparent 2px,
            transparent 9px
        );
    opacity: 0.45;
}
/* =====================================================
   APP
===================================================== */
#app {
    width: 100%;
    min-height: 100vh;
}
/* =====================================================
   COMMON
===================================================== */
.page {
    width: 100%;
    min-height: 100vh;
    position: relative;
    display: none;
}
.page.active {
    display: block;
}
button {
    font-family: inherit;
}
/* =====================================================
   OPENING
===================================================== */
#opening {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    text-align: center;
}
.opening-inner {
    width: min(90%, 650px);
    padding: 40px 20px;
}
.small-label {
    letter-spacing: 7px;
    font-size: 11px;
    color: #b99a78;
    margin-bottom: 20px;
}
.logo {
    font-family: Georgia, serif;
    font-size: clamp(54px, 11vw, 105px);
    letter-spacing: 5px;
    line-height: 0.95;
    color: #f3dfc4;
    text-shadow:
        0 3px 0 #6b452a,
        0 8px 25px rgba(0,0,0,0.5);
}
.subtitle {
    margin-top: 28px;
    color: #c7ad91;
    font-size: 15px;
    letter-spacing: 2px;
}
.start-button {
    margin-top: 50px;
    padding: 16px 52px;
    border: 1px solid #a98460;
    border-radius: 2px;
    background:
        linear-gradient(
            180deg,
            #513522,
            #2c1a10
        );
    color: #f5e5d2;
    font-size: 14px;
    letter-spacing: 4px;
    cursor: pointer;
    box-shadow:
        inset 0 1px rgba(255,255,255,0.08),
        0 12px 30px rgba(0,0,0,0.4);
    transition: 0.25s;
}
.start-button:hover {
    transform: translateY(-3px);
    background: #614329;
}
/* =====================================================
   CHOICE
===================================================== */
.choice-page {
    padding: 50px 25px;
}
.top-logo {
    text-align: center;
    font-family: Georgia, serif;
    font-size: 28px;
    letter-spacing: 5px;
    color: #e8d1b3;
}
.choice-wrap {
    min-height: calc(100vh - 100px);
    display: flex;
    align-items: center;
    justify-content: center;
}
.choice-box {
    width: min(90%, 800px);
    text-align: center;
}
.choice-title {
    font-family: Georgia, serif;
    font-size: clamp(30px, 6vw, 52px);
    color: #f0dfc9;
    margin-bottom: 12px;
}
.choice-description {
    color: #a98e73;
    margin-bottom: 50px;
}
.choice-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}
.choice-button {
    width: 250px;
    height: 150px;
    border: 1px solid #795438;
    background:
        linear-gradient(
            145deg,
            rgba(104,69,43,0.8),
            rgba(36,21,12,0.9)
        );
    color: #ead8c0;
    cursor: pointer;
    transition:
        transform 0.25s,
        border 0.25s,
        background 0.25s;
    box-shadow:
        0 15px 40px rgba(0,0,0,0.35);
}
.choice-button:hover {
    transform: translateY(-7px);
    border-color: #c49b6c;
    background:
        linear-gradient(
            145deg,
            rgba(125,85,51,0.9),
            rgba(45,27,16,0.95)
        );
}
.choice-icon {
    font-size: 34px;
    margin-bottom: 16px;
}
.choice-name {
    font-family: Georgia, serif;
    font-size: 22px;
    letter-spacing: 2px;
}
.choice-sub {
    margin-top: 8px;
    font-size: 11px;
    color: #9d8065;
}
/* =====================================================
   LISTENING PAGE
===================================================== */
#listenPage {
    padding: 25px 30px 60px;
}
.listen-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    max-width: 1250px;
    margin: 0 auto;
}
.header-logo {
    font-family: Georgia, serif;
    letter-spacing: 4px;
    font-size: 26px;
    color: #e7d0b1;
    white-space: nowrap;
}
.back-button {
    border: 1px solid #65472f;
    background: #21140d;
    color: #bda184;
    padding: 10px 17px;
    cursor: pointer;
    transition: 0.2s;
}
.back-button:hover {
    color: #f0ddc6;
    border-color: #a37b53;
}
/* SEARCH */
.search-area {
    max-width: 1250px;
    margin: 45px auto 30px;
}
.search-title {
    font-family: Georgia, serif;
    font-size: 33px;
    color: #eddbc3;
    margin-bottom: 20px;
}
.search-row {
    display: flex;
    gap: 10px;
}
.search-input {
    flex: 1;
    height: 54px;
    background: rgba(24,15,9,0.9);
    border: 1px solid #64472e;
    padding: 0 20px;
    color: #f5e8d7;
    outline: none;
    font-size: 15px;
}
.search-input:focus {
    border-color: #b28a5d;
}
.search-button {
    width: 110px;
    border: 1px solid #8c6846;
    background: #3c2617;
    color: #ead5bb;
    cursor: pointer;
    transition: 0.2s;
}
.search-button:hover {
    background: #5b3b23;
}
/* STATUS */
.status {
    color: #967d64;
    font-size: 12px;
    margin: 16px 0 25px;
}
/* CARDS */
.music-grid {
    max-width: 1250px;
    margin: 0 auto;
    display: grid;
    grid-template-columns:
        repeat(auto-fill, minmax(180px, 1fr));
    gap: 22px;
}
.music-card {
    position: relative;
    background:
        linear-gradient(
            150deg,
            #2c1b10,
            #170e09
        );
    border: 1px solid #4e3523;
    padding: 12px;
    cursor: grab;
    transition:
        transform 0.25s,
        border 0.25s,
        box-shadow 0.25s;
    user-select: none;
}
.music-card:hover {
    transform: translateY(-7px);
    border-color: #9d754e;
    box-shadow:
        0 18px 35px rgba(0,0,0,0.45);
}
.music-card:active {
    cursor: grabbing;
}
.cover-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 1 / 1;
    overflow: hidden;
    background: #080604;
}
.cover {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}
.cover-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,0);
    transition: 0.2s;
}
.music-card:hover .cover-overlay {
    background: rgba(0,0,0,0.2);
}
.drag-label {
    position: absolute;
    bottom: 10px;
    right: 10px;
    background: rgba(20,12,7,0.85);
    border: 1px solid rgba(255,220,180,0.25);
    padding: 5px 8px;
    font-size: 9px;
    color: #d4b997;
}
.music-name {
    margin-top: 13px;
    color: #ead9c4;
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.artist-name {
    margin-top: 5px;
    color: #987d62;
    font-size: 11px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
/* =====================================================
   PLAYER PAGE
===================================================== */
#playerPage {
    min-height: 100vh;
    padding: 25px;
}
.player-top {
    max-width: 1100px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.player-title {
    font-family: Georgia, serif;
    letter-spacing: 4px;
    color: #dfc7a8;
}
.player-content {
    min-height: calc(100vh - 110px);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(50px, 9vw, 130px);
    padding: 30px 20px;
    flex-wrap: wrap;
}
/* RECORD */
.record-zone {
    position: relative;
    width: min(75vw, 510px);
    height: min(75vw, 510px);
    display: flex;
    align-items: center;
    justify-content: center;
}
.record-shadow {
    position: absolute;
    width: 92%;
    height: 92%;
    border-radius: 50%;
    background: rgba(0,0,0,0.6);
    filter: blur(25px);
    transform: translateY(20px);
}
.record {
    position: relative;
    width: 88%;
    height: 88%;
    border-radius: 50%;
    background:
        repeating-radial-gradient(
            circle,
            #161616 0px,
            #161616 2px,
            #252525 3px,
            #101010 5px
        );
    box-shadow:
        0 20px 50px rgba(0,0,0,0.7),
        inset 0 0 30px rgba(255,255,255,0.05);
    transition: 0.5s;
}
.record.spinning {
    animation: spin 2.1s linear infinite;
}
@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}
/* LABEL */
.record-label {
    position: absolute;
    width: 34%;
    height: 34%;
    left: 33%;
    top: 33%;
    border-radius: 50%;
    background:
        radial-gradient(
            circle,
            #b8895b 0%,
            #8b5e39 65%,
            #5b3b25 100%
        );
    border: 5px solid #2b1c13;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}
.record-label img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.8;
}
.center-hole {
    position: absolute;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #ddd;
    border: 4px solid #272727;
    z-index: 5;
}
/* TONEARM */
.tonearm {
    position: absolute;
    width: 180px;
    height: 180px;
    right: -2%;
    top: 1%;
    z-index: 20;
    transform-origin: 86% 16%;
    transform: rotate(25deg);
    transition:
        transform 0.7s cubic-bezier(.4,.1,.2,1);
    cursor: pointer;
}
.tonearm.lifted {
    transform: rotate(-22deg);
}
.arm-base {
    position: absolute;
    width: 58px;
    height: 58px;
    right: 8px;
    top: 4px;
    border-radius: 50%;
    background:
        radial-gradient(
            circle at 35% 30%,
            #bcb5aa,
            #6d675f 55%,
            #33312e
        );
    box-shadow:
        0 6px 15px rgba(0,0,0,0.6);
}
.arm {
    position: absolute;
    width: 125px;
    height: 14px;
    right: 34px;
    top: 28px;
    border-radius: 20px;
    background:
        linear-gradient(
            180deg,
            #bdb6aa,
            #595550
        );
    transform: rotate(27deg);
    transform-origin: right center;
    box-shadow:
        0 5px 10px rgba(0,0,0,0.5);
}
.needle {
    position: absolute;
    width: 24px;
    height: 35px;
    left: 18px;
    bottom: 18px;
    background:
        linear-gradient(
            90deg,
            #4b4842,
            #d4cec1,
            #514e49
        );
    clip-path: polygon(
        20% 0,
        80% 0,
        100% 75%,
        50% 100%,
        0 75%
    );
    filter: drop-shadow(
        0 4px 5px rgba(0,0,0,0.5)
    );
}
/* PLAYER INFO */
.player-info {
    width: min(90vw, 320px);
    text-align: center;
}
.now-playing-label {
    color: #8f765e;
    font-size: 10px;
    letter-spacing: 4px;
    margin-bottom: 14px;
}
.now-cover {
    width: 110px;
    height: 110px;
    object-fit: cover;
    display: block;
    margin: 0 auto 25px;
    border: 1px solid #765638;
    box-shadow:
        0 15px 35px rgba(0,0,0,0.5);
}
.now-title {
    font-family: Georgia, serif;
    font-size: 25px;
    color: #ebdac5;
    line-height: 1.25;
}
.now-artist {
    color: #9d8268;
    font-size: 13px;
    margin-top: 10px;
}
.hint {
    margin-top: 35px;
    color: #755f4b;
    font-size: 11px;
    line-height: 1.8;
}
.preview-note {
    margin-top: 20px;
    color: #665341;
    font-size: 10px;
}
/* EMPTY LP */
.drop-message {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 55%;
    text-align: center;
    color: #776250;
    font-family: Georgia, serif;
    font-size: 15px;
    pointer-events: none;
    z-index: 3;
}
.record.has-song .drop-message {
    display: none;
}
/* =====================================================
   MOBILE
===================================================== */
@media (max-width: 700px) {
    #listenPage {
        padding: 20px 15px 50px;
    }
    .listen-header {
        align-items: flex-start;
    }
    .header-logo {
        font-size: 20px;
    }
    .music-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
        gap: 12px;
    }
    .music-card {
        padding: 8px;
    }
    .music-name {
        font-size: 12px;
    }
    .artist-name {
        font-size: 10px;
    }
    .drag-label {
        display: none;
    }
    .player-content {
        gap: 25px;
        padding-top: 50px;
    }
    .record-zone {
        width: min(90vw, 430px);
        height: min(90vw, 430px);
    }
    .tonearm {
        transform: scale(0.8) rotate(25deg);
        right: -7%;
        top: -2%;
    }
    .tonearm.lifted {
        transform: scale(0.8) rotate(-22deg);
    }
    .player-info {
        margin-top: 0;
    }
    .choice-buttons {
        flex-direction: column;
        align-items: center;
    }
    .choice-button {
        width: min(90vw, 300px);
    }
}
</style>
</head>
<body>
<div id="app">
    <!-- =================================================
         OPENING
    ================================================== -->
    <section id="opening" class="page active">
        <div class="opening-inner">
            <div class="small-label">
                EST. 2026 · MUSIC & MEMORY
            </div>
            <div class="logo">
                RECORD<br>ROOM
            </div>
            <div class="subtitle">
                오늘의 음악을 한 장의 레코드처럼.
            </div>
            <button
                class="start-button"
                onclick="showPage('choicePage')"
            >
                ENTER ROOM
            </button>
        </div>
    </section>
    <!-- =================================================
         CHOICE
    ================================================== -->
    <section id="choicePage" class="page choice-page">
        <div class="top-logo">
            RECORD ROOM
        </div>
        <div class="choice-wrap">
            <div class="choice-box">
                <div class="choice-title">
                    What would you like?
                </div>
                <div class="choice-description">
                    오늘은 어떤 음악을 만나볼까요?
                </div>
                <div class="choice-buttons">
                    <button
                        class="choice-button"
                        onclick="showPage('listenPage'); initializeSearch();"
                    >
                        <div class="choice-icon">♫</div>
                        <div class="choice-name">
                            노래듣기
                        </div>
                        <div class="choice-sub">
                            SEARCH & PLAY
                        </div>
                    </button>
                    <button
                        class="choice-button"
                        onclick="alert('노래 추천 기능은 다음 단계에서 추가할 수 있어요!');"
                    >
                        <div class="choice-icon">✦</div>
                        <div class="choice-name">
                            노래 추천받기
                        </div>
                        <div class="choice-sub">
                            COMING SOON
                        </div>
                    </button>
                </div>
            </div>
        </div>
    </section>
    <!-- =================================================
         LISTEN
    ================================================== -->
    <section id="listenPage" class="page">
        <div class="listen-header">
            <div class="header-logo">
                RECORD ROOM
            </div>
            <button
                class="back-button"
                onclick="showPage('choicePage')"
            >
                ← 뒤로
            </button>
        </div>
        <div class="search-area">
            <div class="search-title">
                오늘 들을 레코드를 찾아보세요.
            </div>
            <div class="search-row">
                <input
                    id="searchInput"
                    class="search-input"
                    type="text"
                    placeholder="노래 제목이나 아티스트를 검색해보세요"
                    onkeydown="if(event.key === 'Enter') searchMusic();"
                >
                <button
                    class="search-button"
                    onclick="searchMusic()"
                >
                    검색
                </button>
            </div>
            <div
                id="searchStatus"
                class="status"
            >
                음악을 불러오는 중...
            </div>
        </div>
        <div
            id="musicGrid"
            class="music-grid"
        ></div>
    </section>
    <!-- =================================================
         PLAYER
    ================================================== -->
    <section id="playerPage" class="page">
        <div class="player-top">
            <div class="player-title">
                RECORD ROOM
            </div>
            <button
                class="back-button"
                onclick="goBackFromPlayer()"
            >
                ← 음악 목록
            </button>
        </div>
        <div class="player-content">
            <div class="record-zone">
                <div class="record-shadow"></div>
                <div
                    id="record"
                    class="record"
                    ondragover="event.preventDefault();"
                    ondrop="dropSong(event);"
                >
                    <div class="drop-message">
                        <div>DROP THE RECORD</div>
                        <div style="font-size:10px;margin-top:8px;">
                            음악 카드를 이곳에 놓아주세요
                        </div>
                    </div>
                    <div class="record-label">
                        <img
                            id="recordCover"
                            src=""
                            alt=""
                        >
                    </div>
                    <div class="center-hole"></div>
                </div>
                <!-- TONEARM -->
                <div
                    id="tonearm"
                    class="tonearm"
                    onclick="toggleTonearm()"
                    title="톤암 클릭"
                >
                    <div class="arm-base"></div>
                    <div class="arm"></div>
                    <div class="needle"></div>
                </div>
            </div>
            <!-- PLAYER INFORMATION -->
            <div class="player-info">
                <div class="now-playing-label">
                    NOW PLAYING
                </div>
                <img
                    id="nowCover"
                    class="now-cover"
                    src=""
                    alt=""
                >
                <div
                    id="nowTitle"
                    class="now-title"
                >
                    레코드를 올려주세요
                </div>
                <div
                    id="nowArtist"
                    class="now-artist"
                >
                    MUSIC PLAYER
                </div>
                <div class="hint">
                    음악 카드를 LP 위로 끌어놓으면<br>
                    톤암이 내려가며 재생됩니다.<br><br>
                    재생 중에는 톤암을 클릭해보세요.
                </div>
                <div class="preview-note">
                    Apple Music/iTunes 미리듣기
                </div>
            </div>
        </div>
    </section>
</div>
<!-- =====================================================
     AUDIO
===================================================== -->
<audio
    id="audioPlayer"
    preload="none"
></audio>
<script>
/* =====================================================
   GLOBAL STATE
===================================================== */
let currentSong = null;
let currentAudio = document.getElementById("audioPlayer");
let searchInitialized = false;
let jsonpCounter = 0;
/* =====================================================
   PAGE NAVIGATION
===================================================== */
function showPage(pageId) {
    const pages = document.querySelectorAll(".page");
    pages.forEach(page => {
        page.classList.remove("active");
    });
    const target = document.getElementById(pageId);
    if (target) {
        target.classList.add("active");
    }
    window.scrollTo({
        top: 0,
        behavior: "instant"
    });
}
/* =====================================================
   SEARCH INITIALIZATION
===================================================== */
function initializeSearch() {
    if (searchInitialized) {
        return;
    }
    searchInitialized = true;
    const input = document.getElementById("searchInput");
    if (input) {
        input.value = "K-pop";
    }
    searchMusic("K-pop");
}
/* =====================================================
   ITUNES JSONP SEARCH
===================================================== */
/*
    브라우저에서 Apple 검색 API를 호출하기 위해
    JSONP 방식을 사용합니다.
    API Key / Google Cloud 필요 없음.
*/
function searchMusic(customTerm) {
    let input =
        document.getElementById("searchInput");
    let term =
        customTerm ||
        (input ? input.value.trim() : "");
    if (!term) {
        term = "K-pop";
        if (input) {
            input.value = term;
        }
    }
    const status =
        document.getElementById("searchStatus");
    const grid =
        document.getElementById("musicGrid");
    status.textContent =
        "음악을 검색하는 중...";
    grid.innerHTML = "";
    /*
       JSONP callback 이름 생성
    */
    const callbackName =
        "itunesCallback_" +
        (++jsonpCounter);
    window[callbackName] = function(data) {
        try {
            renderSongs(data.results || []);
            if (data.results && data.results.length > 0) {
                status.textContent =
                    "'" +
                    term +
                    "' 검색 결과 " +
                    data.results.length +
                    "곡";
            } else {
                status.textContent =
                    "검색 결과가 없습니다.";
            }
        } catch(error) {
            console.error(error);
            status.textContent =
                "검색 결과를 표시하는 중 오류가 발생했습니다.";
        }
        /*
           script 제거
        */
        const script =
            document.getElementById(callbackName);
        if (script) {
            script.remove();
        }
        delete window[callbackName];
    };
    const script =
        document.createElement("script");
    const encodedTerm =
        encodeURIComponent(term);
    script.id = callbackName;
    script.src =
        "https://itunes.apple.com/search" +
        "?term=" +
        encodedTerm +
        "&country=KR" +
        "&media=music" +
        "&entity=song" +
        "&limit=30" +
        "&lang=ko_kr" +
        "&callback=" +
        callbackName;
    script.onerror = function() {
        status.textContent =
            "음악 검색에 실패했습니다. 잠시 후 다시 시도해주세요.";
        script.remove();
        delete window[callbackName];
    };
    document.body.appendChild(script);
}
/* =====================================================
   RENDER MUSIC CARDS
===================================================== */
function renderSongs(songs) {
    const grid =
        document.getElementById("musicGrid");
    grid.innerHTML = "";
    songs.forEach((song, index) => {
        /*
           preview가 없는 결과는 제외
        */
        if (!song.previewUrl) {
            return;
        }
        const card =
            document.createElement("div");
        card.className =
            "music-card";
        card.draggable = true;
        /*
           Apple artwork URL
        */
        let artwork =
            song.artworkUrl100 ||
            "";
        /*
           가능하면 더 큰 이미지 요청
        */
        artwork =
            artwork
            .replace(
                "100x100bb",
                "600x600bb"
            )
            .replace(
                "100x100-75",
                "600x600-75"
            );
        const title =
            escapeHTML(
                song.trackName ||
                "Unknown Song"
            );
        const artist =
            escapeHTML(
                song.artistName ||
                "Unknown Artist"
            );
        card.innerHTML = `
            <div class="cover-wrap">
                <img
                    class="cover"
                    src="${artwork}"
                    alt=""
                    draggable="false"
                >
                <div class="cover-overlay"></div>
                <div class="drag-label">
                    DRAG TO LP
                </div>
            </div>
            <div class="music-name">
                ${title}
            </div>
            <div class="artist-name">
                ${artist}
            </div>
        `;
        /*
           드래그 시작
        */
        card.addEventListener(
            "dragstart",
            function(event) {
                const songData = {
                    title:
                        song.trackName ||
                        "Unknown Song",
                    artist:
                        song.artistName ||
                        "Unknown Artist",
                    artwork:
                        artwork,
                    preview:
                        song.previewUrl,
                    store:
                        song.trackViewUrl ||
                        song.collectionViewUrl ||
                        ""
                };
                event.dataTransfer.setData(
                    "text/plain",
                    JSON.stringify(songData)
                );
                /*
                   모바일/터치 대체:
                   클릭하면 바로 LP 화면으로 이동
                */
                currentSong =
                    songData;
            }
        );
        /*
           카드 클릭:
           모바일에서는 drag/drop 대신
           카드 클릭으로 LP에 올림
        */
        card.addEventListener(
            "click",
            function() {
                const songData = {
                    title:
                        song.trackName ||
                        "Unknown Song",
                    artist:
                        song.artistName ||
                        "Unknown Artist",
                    artwork:
                        artwork,
                    preview:
                        song.previewUrl,
                    store:
                        song.trackViewUrl ||
                        song.collectionViewUrl ||
                        ""
                };
                loadSongToPlayer(songData);
            }
        );
        grid.appendChild(card);
    });
}
/* =====================================================
   DRAG → LP
===================================================== */
function dropSong(event) {
    event.preventDefault();
    let data =
        event.dataTransfer.getData("text/plain");
    if (!data) {
        return;
    }
    try {
        const song =
            JSON.parse(data);
        loadSongToPlayer(song);
    } catch(error) {
        console.error(error);
    }
}
/* =====================================================
   LOAD SONG
===================================================== */
function loadSongToPlayer(song) {
    if (!song || !song.preview) {
        return;
    }
    currentSong = song;
    /*
       화면 이동
    */
    showPage("playerPage");
    /*
       텍스트
    */
    document.getElementById(
        "nowTitle"
    ).textContent =
        song.title;
    document.getElementById(
        "nowArtist"
    ).textContent =
        song.artist;
    /*
       이미지
    */
    document.getElementById(
        "nowCover"
    ).src =
        song.artwork;
    document.getElementById(
        "recordCover"
    ).src =
        song.artwork;
    document.getElementById(
        "record"
    ).classList.add(
        "has-song"
    );
    /*
       audio
    */
    currentAudio.pause();
    currentAudio.currentTime = 0;
    currentAudio.src =
        song.preview;
    /*
       톤암 내려오기
    */
    const tonearm =
        document.getElementById("tonearm");
    tonearm.classList.remove("lifted");
    /*
       LP 회전
    */
    const record =
        document.getElementById("record");
    record.classList.add("spinning");
    /*
       재생
       drag/click이라는 사용자 동작 직후이므로
       대부분의 브라우저에서 재생 가능
    */
    const playPromise =
        currentAudio.play();
    if (playPromise !== undefined) {
        playPromise.catch(
            function(error) {
                console.log(
                    "Autoplay blocked:",
                    error
                );
            }
        );
    }
}
/* =====================================================
   TONEARM
===================================================== */
function toggleTonearm() {
    if (!currentSong) {
        return;
    }
    const tonearm =
        document.getElementById("tonearm");
    const record =
        document.getElementById("record");
    /*
       현재 재생 중
       → 톤암 들어올림
       → 일시정지
       → LP 정지
    */
    if (!currentAudio.paused) {
        currentAudio.pause();
        tonearm.classList.add("lifted");
        record.classList.remove("spinning");
    }
    /*
       현재 일시정지
       → 톤암 내려감
       → 다시 재생
    */
    else {
        tonearm.classList.remove("lifted");
        record.classList.add("spinning");
        const playPromise =
            currentAudio.play();
        if (playPromise !== undefined) {
            playPromise.catch(
                function(error) {
                    console.log(error);
                }
            );
        }
    }
}
/* =====================================================
   AUDIO ENDED
===================================================== */
currentAudio.addEventListener(
    "ended",
    function() {
        const record =
            document.getElementById("record");
        const tonearm =
            document.getElementById("tonearm");
        record.classList.remove(
            "spinning"
        );
        tonearm.classList.add(
            "lifted"
        );
    }
);
/* =====================================================
   BACK FROM PLAYER
===================================================== */
function goBackFromPlayer() {
    /*
       음악 정지
    */
    currentAudio.pause();
    currentAudio.currentTime = 0;
    currentAudio.removeAttribute("src");
    currentAudio.load();
    /*
       LP 정지
    */
    document
        .getElementById("record")
        .classList
        .remove("spinning");
    /*
       톤암 올리기
    */
    document
        .getElementById("tonearm")
        .classList
        .add("lifted");
    /*
       곡 정보 초기화
    */
    currentSong = null;
    /*
       음악 목록으로
    */
    showPage("listenPage");
}
/* =====================================================
   ESCAPE HTML
===================================================== */
function escapeHTML(text) {
    return String(text)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}
/* =====================================================
   INITIAL PAGE
===================================================== */
showPage("opening");
</script>
</body>
</html>
"""
# ---------------------------------------------------------
# HTML 실행
# ---------------------------------------------------------
components.html(
    html,
    height=1600,
    scrolling=True
)