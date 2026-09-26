import streamlit as st

st.set_page_config(
    page_title="RECORD ROOM",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# STREAMLIT 기본 설정
# =========================================================

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    margin: 0 !important;
    padding: 0 !important;
    background: #17100b !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

footer {
    display: none !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# RECORD ROOM 전체 웹페이지
# =========================================================

html = r"""
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
    background: #17100b;
}

body {
    color: #f4e5d2;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Pretendard",
        "Apple SD Gothic Neo",
        sans-serif;
    overflow-x: hidden;
}

button,
input {
    font-family: inherit;
}


/* =====================================================
   WOOD BACKGROUND
===================================================== */

#record-room-app {
    position: relative;
    width: 100%;
    min-height: 100vh;
    background:
        linear-gradient(
            90deg,
            rgba(255,255,255,0.015),
            transparent 20%,
            rgba(255,255,255,0.012) 50%,
            transparent 80%
        ),
        repeating-linear-gradient(
            90deg,
            rgba(255,255,255,0.018) 0px,
            rgba(255,255,255,0.018) 2px,
            transparent 2px,
            transparent 10px
        ),
        #1b1009;
}


/* =====================================================
   PAGE
===================================================== */

.rr-page {
    display: none;
    width: 100%;
    min-height: 100vh;
}

.rr-page.active {
    display: block;
}


/* =====================================================
   OPENING
===================================================== */

#rr-opening {
    align-items: center;
    justify-content: center;
    text-align: center;
}

#rr-opening.active {
    display: flex;
}

.opening-inner {
    width: min(90%, 760px);
    padding: 40px 20px;
}

.est {
    font-family: Georgia, serif;
    font-size: 11px;
    letter-spacing: 7px;
    color: #b99a78;
    margin-bottom: 25px;
}

.logo {
    font-family: Georgia, "Times New Roman", serif;
    font-weight: 700;
    font-size: clamp(55px, 10vw, 105px);
    line-height: 0.9;
    letter-spacing: 5px;
    color: #f2dfc7;
    text-shadow:
        0 3px 0 #6b452a,
        0 10px 30px rgba(0,0,0,0.55);
}

.subtitle {
    margin-top: 30px;
    color: #c6aa8c;
    font-size: 15px;
    letter-spacing: 2px;
}

.enter-button {
    margin-top: 55px;
    min-width: 295px;
    height: 64px;
    padding: 0 35px;
    border: 1px solid #a77d54;
    border-radius: 2px;
    background:
        linear-gradient(
            180deg,
            #523520,
            #2b190e
        );
    color: #f1dfca;
    font-size: 14px;
    letter-spacing: 5px;
    cursor: pointer;
    box-shadow:
        inset 0 1px rgba(255,255,255,0.08),
        0 15px 35px rgba(0,0,0,0.4);
    transition: 0.25s;
}

.enter-button:hover {
    transform: translateY(-3px);
    background: #62432a;
}

.enter-button:active {
    transform: scale(0.98);
}


/* =====================================================
   CHOICE
===================================================== */

#rr-choice {
    padding: 35px 20px;
}

.choice-header {
    text-align: center;
    font-family: Georgia, serif;
    font-size: 25px;
    letter-spacing: 5px;
    color: #e7cfb0;
}

.choice-content {
    min-height: calc(100vh - 100px);
    display: flex;
    align-items: center;
    justify-content: center;
}

.choice-inner {
    width: min(900px, 100%);
    text-align: center;
}

.choice-title {
    font-family: Georgia, serif;
    font-size: clamp(32px, 6vw, 52px);
    color: #efddc6;
    margin-bottom: 12px;
}

.choice-desc {
    color: #a98b70;
    font-size: 14px;
    margin-bottom: 48px;
}

.choice-buttons {
    display: flex;
    justify-content: center;
    gap: 22px;
    flex-wrap: wrap;
}

.choice-button {
    width: 260px;
    height: 165px;
    border: 1px solid #765337;
    background:
        linear-gradient(
            145deg,
            rgba(99,65,40,0.9),
            rgba(35,20,12,0.95)
        );
    color: #ead8c1;
    cursor: pointer;
    transition: 0.25s;
    box-shadow:
        0 18px 40px rgba(0,0,0,0.4);
}

.choice-button:hover {
    transform: translateY(-6px);
    border-color: #bd9161;
}

.choice-icon {
    font-family: Georgia, serif;
    font-size: 38px;
    margin-bottom: 15px;
}

.choice-name {
    font-family: Georgia, serif;
    font-size: 22px;
    letter-spacing: 2px;
}

.choice-sub {
    margin-top: 9px;
    font-size: 10px;
    letter-spacing: 2px;
    color: #96785d;
}


/* =====================================================
   LISTEN PAGE
===================================================== */

#rr-listen {
    padding: 25px 25px 60px;
}

.listen-header {
    max-width: 1250px;
    margin: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.room-logo {
    font-family: Georgia, serif;
    font-size: 25px;
    letter-spacing: 4px;
    color: #e7d0b1;
}

.back-button {
    border: 1px solid #664830;
    background: #21140c;
    color: #bfa287;
    padding: 10px 17px;
    cursor: pointer;
}

.back-button:hover {
    border-color: #a37c53;
    color: #f0dfca;
}

.search-area {
    max-width: 1250px;
    margin: 50px auto 30px;
}

.search-title {
    font-family: Georgia, serif;
    font-size: clamp(28px, 5vw, 40px);
    color: #eddac1;
    margin-bottom: 22px;
}

.search-row {
    display: flex;
    gap: 10px;
}

.search-input {
    flex: 1;
    height: 55px;
    border: 1px solid #64462d;
    outline: none;
    background: #170d08;
    color: #f3e3d0;
    padding: 0 18px;
    font-size: 14px;
}

.search-input::placeholder {
    color: #755d48;
}

.search-input:focus {
    border-color: #ad8258;
}

.search-button {
    width: 100px;
    border: 1px solid #8b6746;
    background: #3d2718;
    color: #ead7bf;
    cursor: pointer;
}

.search-button:hover {
    background: #5a3b24;
}

.search-status {
    margin: 15px 0 25px;
    color: #937861;
    font-size: 12px;
}


/* =====================================================
   MUSIC GRID
===================================================== */

.music-grid {
    max-width: 1250px;
    margin: auto;
    display: grid;
    grid-template-columns:
        repeat(
            auto-fill,
            minmax(175px, 1fr)
        );
    gap: 22px;
}

.music-card {
    padding: 10px;
    border: 1px solid #4e3523;
    background:
        linear-gradient(
            145deg,
            #2c1b10,
            #160c07
        );
    cursor: pointer;
    transition: 0.25s;
}

.music-card:hover {
    transform: translateY(-7px);
    border-color: #a37a51;
    box-shadow:
        0 18px 35px rgba(0,0,0,0.45);
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

.drag-label {
    position: absolute;
    right: 8px;
    bottom: 8px;
    padding: 5px 7px;
    font-size: 8px;
    letter-spacing: 1px;
    background: rgba(20,10,5,0.85);
    color: #d8b996;
    border: 1px solid rgba(255,220,180,0.2);
}

.song-title {
    margin-top: 12px;
    color: #ead9c4;
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.song-artist {
    margin-top: 5px;
    color: #987d62;
    font-size: 11px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}


/* =====================================================
   PLAYER
===================================================== */

#rr-player {
    padding: 25px;
}

.player-header {
    max-width: 1100px;
    margin: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.player-content {
    min-height: calc(100vh - 100px);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: clamp(45px, 9vw, 130px);
    flex-wrap: wrap;
}


/* =====================================================
   LP
===================================================== */

.record-area {
    position: relative;
    width: min(76vw, 510px);
    height: min(76vw, 510px);
    display: flex;
    justify-content: center;
    align-items: center;
}

.record-shadow {
    position: absolute;
    width: 90%;
    height: 90%;
    border-radius: 50%;
    background: rgba(0,0,0,0.65);
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
            #111 0px,
            #111 2px,
            #292929 3px,
            #101010 5px
        );
    box-shadow:
        0 20px 55px rgba(0,0,0,0.75),
        inset 0 0 30px rgba(255,255,255,0.04);
    transition: 0.4s;
}

.record.spinning {
    animation:
        vinylSpin
        2.2s
        linear
        infinite;
}

@keyframes vinylSpin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.record-label {
    position: absolute;
    width: 35%;
    height: 35%;
    left: 32.5%;
    top: 32.5%;
    border-radius: 50%;
    overflow: hidden;
    border: 5px solid #282019;
    background: #855a37;
}

.record-label img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.center-hole {
    position: absolute;
    left: calc(50% - 7px);
    top: calc(50% - 7px);
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #d9d4ca;
    border: 4px solid #292929;
    z-index: 5;
}


/* =====================================================
   DROP MESSAGE
===================================================== */

.drop-message {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    color: #776250;
    text-align: center;
    font-family: Georgia, serif;
    font-size: 15px;
    width: 55%;
    pointer-events: none;
    z-index: 3;
}

.record.has-song .drop-message {
    display: none;
}


/* =====================================================
   TONEARM
===================================================== */

.tonearm {
    position: absolute;
    width: 180px;
    height: 180px;
    right: -4%;
    top: 1%;
    z-index: 20;
    transform-origin: 86% 16%;
    transform: rotate(25deg);
    transition:
        transform 0.7s
        cubic-bezier(.4,.1,.2,1);
    cursor: pointer;
}

.tonearm.lifted {
    transform: rotate(-22deg);
}

.arm-base {
    position: absolute;
    right: 8px;
    top: 4px;
    width: 58px;
    height: 58px;
    border-radius: 50%;
    background:
        radial-gradient(
            circle at 35% 30%,
            #c3bcb0,
            #6c665f 55%,
            #33312e
        );
    box-shadow:
        0 6px 15px rgba(0,0,0,0.6);
}

.arm {
    position: absolute;
    right: 34px;
    top: 28px;
    width: 125px;
    height: 14px;
    border-radius: 20px;
    background:
        linear-gradient(
            180deg,
            #c2bbb0,
            #595550
        );
    transform: rotate(27deg);
    transform-origin: right center;
}

.needle {
    position: absolute;
    left: 18px;
    bottom: 18px;
    width: 24px;
    height: 35px;
    background:
        linear-gradient(
            90deg,
            #4b4842,
            #d4cec1,
            #514e49
        );
    clip-path:
        polygon(
            20% 0,
            80% 0,
            100% 75%,
            50% 100%,
            0 75%
        );
}


/* =====================================================
   PLAYER INFO
===================================================== */

.player-info {
    width: min(90vw, 320px);
    text-align: center;
}

.now-label {
    color: #8f765e;
    font-size: 10px;
    letter-spacing: 4px;
    margin-bottom: 15px;
}

.now-cover {
    width: 115px;
    height: 115px;
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
    margin-top: 9px;
    color: #9d8268;
    font-size: 13px;
}

.player-hint {
    margin-top: 32px;
    color: #765f4a;
    font-size: 11px;
    line-height: 1.8;
}

.preview-note {
    margin-top: 20px;
    color: #665341;
    font-size: 10px;
}


/* =====================================================
   MOBILE
===================================================== */

@media (max-width: 700px) {

    #rr-listen {
        padding: 20px 14px 50px;
    }

    .room-logo {
        font-size: 20px;
    }

    .music-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
        gap: 12px;
    }

    .music-card {
        padding: 7px;
    }

    .song-title {
        font-size: 12px;
    }

    .song-artist {
        font-size: 10px;
    }

    .drag-label {
        display: none;
    }

    .record-area {
        width: min(90vw, 430px);
        height: min(90vw, 430px);
    }

    .tonearm {
        transform: scale(.8) rotate(25deg);
        right: -8%;
        top: -2%;
    }

    .tonearm.lifted {
        transform: scale(.8) rotate(-22deg);
    }

    .choice-buttons {
        flex-direction: column;
        align-items: center;
    }

    .choice-button {
        width: min(90vw, 310px);
    }

    .search-row {
        gap: 7px;
    }

    .search-button {
        width: 75px;
    }

    .search-input {
        font-size: 13px;
        padding: 0 13px;
    }
}

</style>


<div id="record-room-app">


<!-- =====================================================
     OPENING
===================================================== -->

<section
    id="rr-opening"
    class="rr-page active"
>

    <div class="opening-inner">

        <div class="est">
            EST. 2026 · MUSIC & MEMORY
        </div>

        <div class="logo">
            RECORD<br>ROOM
        </div>

        <div class="subtitle">
            오늘의 음악을 한 장의 레코드처럼.
        </div>

        <button
            class="enter-button"
            id="enterRoom"
        >
            ENTER ROOM
        </button>

    </div>

</section>


<!-- =====================================================
     CHOICE
===================================================== -->

<section
    id="rr-choice"
    class="rr-page"
>

    <div class="choice-header">
        RECORD ROOM
    </div>

    <div class="choice-content">

        <div class="choice-inner">

            <div class="choice-title">
                What would you like?
            </div>

            <div class="choice-desc">
                오늘은 어떤 음악을 만나볼까요?
            </div>

            <div class="choice-buttons">

                <button
                    class="choice-button"
                    id="listenChoice"
                >

                    <div class="choice-icon">
                        ♫
                    </div>

                    <div class="choice-name">
                        노래듣기
                    </div>

                    <div class="choice-sub">
                        SEARCH & PLAY
                    </div>

                </button>


                <button
                    class="choice-button"
                    id="recommendChoice"
                >

                    <div class="choice-icon">
                        ✦
                    </div>

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


<!-- =====================================================
     LISTEN
===================================================== -->

<section
    id="rr-listen"
    class="rr-page"
>

    <div class="listen-header">

        <div class="room-logo">
            RECORD ROOM
        </div>

        <button
            class="back-button"
            id="listenBack"
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
            >

            <button
                class="search-button"
                id="searchButton"
            >
                검색
            </button>

        </div>

        <div
            id="searchStatus"
            class="search-status"
        >
            검색어를 입력해 음악을 찾아보세요.
        </div>

    </div>


    <div
        id="musicGrid"
        class="music-grid"
    ></div>

</section>


<!-- =====================================================
     PLAYER
===================================================== -->

<section
    id="rr-player"
    class="rr-page"
>

    <div class="player-header">

        <div class="room-logo">
            RECORD ROOM
        </div>

        <button
            class="back-button"
            id="playerBack"
        >
            ← 음악 목록
        </button>

    </div>


    <div class="player-content">


        <!-- LP -->

        <div class="record-area">

            <div class="record-shadow"></div>

            <div
                class="record"
                id="record"
            >

                <div class="drop-message">

                    <div>
                        DROP THE RECORD
                    </div>

                    <div
                        style="
                            margin-top:8px;
                            font-size:10px;
                        "
                    >
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


            <div
                class="tonearm lifted"
                id="tonearm"
                title="톤암 클릭"
            >

                <div class="arm-base"></div>
                <div class="arm"></div>
                <div class="needle"></div>

            </div>

        </div>


        <!-- INFO -->

        <div class="player-info">

            <div class="now-label">
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

            <div class="player-hint">
                음악 카드를 선택하면<br>
                레코드가 재생됩니다.<br><br>
                톤암을 클릭하면 재생을<br>
                일시정지할 수 있습니다.
            </div>

            <div class="preview-note">
                Apple Music / iTunes 미리듣기
            </div>

        </div>

    </div>

</section>


</div>


<audio
    id="rr-audio"
    preload="none"
></audio>


<script>

/* =====================================================
   RECORD ROOM JAVASCRIPT
===================================================== */

(function () {

    "use strict";


    /* -------------------------------------------------
       ELEMENTS
    ------------------------------------------------- */

    const opening =
        document.getElementById("rr-opening");

    const choice =
        document.getElementById("rr-choice");

    const listen =
        document.getElementById("rr-listen");

    const player =
        document.getElementById("rr-player");

    const enterButton =
        document.getElementById("enterRoom");

    const listenChoice =
        document.getElementById("listenChoice");

    const recommendChoice =
        document.getElementById("recommendChoice");

    const listenBack =
        document.getElementById("listenBack");

    const playerBack =
        document.getElementById("playerBack");

    const searchButton =
        document.getElementById("searchButton");

    const searchInput =
        document.getElementById("searchInput");

    const searchStatus =
        document.getElementById("searchStatus");

    const musicGrid =
        document.getElementById("musicGrid");

    const audio =
        document.getElementById("rr-audio");

    const record =
        document.getElementById("record");

    const tonearm =
        document.getElementById("tonearm");

    const recordCover =
        document.getElementById("recordCover");

    const nowCover =
        document.getElementById("nowCover");

    const nowTitle =
        document.getElementById("nowTitle");

    const nowArtist =
        document.getElementById("nowArtist");


    let currentSong = null;
    let callbackNumber = 0;


    /* -------------------------------------------------
       PAGE
    ------------------------------------------------- */

    function showPage(target) {

        const pages = [
            opening,
            choice,
            listen,
            player
        ];

        pages.forEach(function (page) {

            page.classList.remove("active");

        });


        target.classList.add("active");


        window.scrollTo({
            top: 0,
            behavior: "instant"
        });
    }


    /* -------------------------------------------------
       ENTER ROOM
    ------------------------------------------------- */

    enterButton.addEventListener(
        "click",
        function () {

            showPage(choice);

        }
    );


    /* -------------------------------------------------
       LISTEN
    ------------------------------------------------- */

    listenChoice.addEventListener(
        "click",
        function () {

            showPage(listen);

            searchInput.focus();

        }
    );


    /* -------------------------------------------------
       RECOMMEND
    ------------------------------------------------- */

    recommendChoice.addEventListener(
        "click",
        function () {

            alert(
                "노래 추천 기능은 다음 단계에서 추가할 예정이에요!"
            );

        }
    );


    /* -------------------------------------------------
       BACK
    ------------------------------------------------- */

    listenBack.addEventListener(
        "click",
        function () {

            stopAudio();

            showPage(choice);

        }
    );


    playerBack.addEventListener(
        "click",
        function () {

            stopAudio();

            showPage(listen);

        }
    );


    /* -------------------------------------------------
       SEARCH BUTTON
    ------------------------------------------------- */

    searchButton.addEventListener(
        "click",
        function () {

            searchMusic();

        }
    );


    searchInput.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter"
            ) {

                searchMusic();

            }

        }
    );


    /* -------------------------------------------------
       SEARCH
    ------------------------------------------------- */

    function searchMusic() {

        const term =
            searchInput.value.trim();


        if (!term) {

            searchStatus.textContent =
                "검색어를 입력해주세요.";

            return;

        }


        searchStatus.textContent =
            "'" +
            term +
            "' 검색 중...";


        musicGrid.innerHTML = "";


        const callbackName =
            "recordRoomCallback" +
            (++callbackNumber);


        window[callbackName] =
            function (data) {

                const results =
                    data.results || [];


                renderSongs(results);


                if (
                    results.length === 0
                ) {

                    searchStatus.textContent =
                        "검색 결과가 없습니다.";

                }
                else {

                    searchStatus.textContent =
                        "'" +
                        term +
                        "' 검색 결과";

                }


                const oldScript =
                    document.getElementById(
                        callbackName
                    );


                if (oldScript) {
                    oldScript.remove();
                }


                try {
                    delete window[
                        callbackName
                    ];
                }
                catch (e) {}

            };


        const script =
            document.createElement("script");


        script.id =
            callbackName;


        script.src =
            "https://itunes.apple.com/search" +
            "?term=" +
            encodeURIComponent(term) +
            "&country=KR" +
            "&media=music" +
            "&entity=song" +
            "&limit=30" +
            "&callback=" +
            callbackName;


        script.onerror =
            function () {

                searchStatus.textContent =
                    "음악 검색에 실패했습니다. 잠시 후 다시 시도해주세요.";

                script.remove();

                try {
                    delete window[
                        callbackName
                    ];
                }
                catch (e) {}

            };


        document.body.appendChild(
            script
        );

    }


    /* -------------------------------------------------
       SONGS
    ------------------------------------------------- */

    function renderSongs(songs) {

        musicGrid.innerHTML = "";


        let count = 0;


        songs.forEach(
            function (song) {

                if (
                    !song.previewUrl
                ) {

                    return;

                }


                count++;


                let artwork =
                    song.artworkUrl100 ||
                    "";


                artwork =
                    artwork.replace(
                        "100x100bb",
                        "600x600bb"
                    );


                artwork =
                    artwork.replace(
                        "100x100-75",
                        "600x600-75"
                    );


                const card =
                    document.createElement(
                        "div"
                    );


                card.className =
                    "music-card";


                card.innerHTML = `

                    <div class="cover-wrap">

                        <img
                            class="cover"
                            src="${escapeHTML(artwork)}"
                            alt=""
                        >

                        <div class="drag-label">
                            PLAY
                        </div>

                    </div>

                    <div class="song-title">
                        ${escapeHTML(
                            song.trackName ||
                            "Unknown"
                        )}
                    </div>

                    <div class="song-artist">
                        ${escapeHTML(
                            song.artistName ||
                            "Unknown Artist"
                        )}
                    </div>

                `;


                const songData = {

                    title:
                        song.trackName ||
                        "Unknown",

                    artist:
                        song.artistName ||
                        "Unknown Artist",

                    artwork:
                        artwork,

                    preview:
                        song.previewUrl

                };


                /* -------------------------------------
                   클릭
                ------------------------------------- */

                card.addEventListener(
                    "click",
                    function () {

                        loadSong(
                            songData
                        );

                    }
                );


                /* -------------------------------------
                   PC 드래그
                ------------------------------------- */

                card.draggable = true;


                card.addEventListener(
                    "dragstart",
                    function (event) {

                        event.dataTransfer.setData(
                            "text/plain",
                            JSON.stringify(
                                songData
                            )
                        );

                    }
                );


                musicGrid.appendChild(
                    card
                );

            }
        );


        if (count === 0) {

            musicGrid.innerHTML = `

                <div
                    style="
                        grid-column:1/-1;
                        text-align:center;
                        padding:70px 20px;
                        color:#806954;
                    "
                >
                    미리듣기를 제공하는 곡이 없습니다.
                </div>

            `;

        }

    }


    /* -------------------------------------------------
       LOAD SONG
    ------------------------------------------------- */

    function loadSong(song) {

        if (
            !song ||
            !song.preview
        ) {

            return;

        }


        currentSong =
            song;


        nowTitle.textContent =
            song.title;


        nowArtist.textContent =
            song.artist;


        nowCover.src =
            song.artwork;


        recordCover.src =
            song.artwork;


        record.classList.add(
            "has-song"
        );


        audio.pause();


        audio.currentTime = 0;


        audio.src =
            song.preview;


        tonearm.classList.remove(
            "lifted"
        );


        record.classList.add(
            "spinning"
        );


        showPage(player);


        /*
           iOS Safari에서는
           사용자의 클릭 이벤트 안에서
           audio.play()가 호출되어야
           자동재생 제한에 걸릴 가능성이 낮음.
        */

        const promise =
            audio.play();


        if (
            promise &&
            typeof promise.catch === "function"
        ) {

            promise.catch(
                function () {

                    /*
                       자동재생이 막힌 경우에도
                       플레이어 화면은 정상적으로 표시.
                    */

                    record.classList.remove(
                        "spinning"
                    );

                }
            );

        }

    }


    /* -------------------------------------------------
       DRAG & DROP
    ------------------------------------------------- */

    record.addEventListener(
        "dragover",
        function (event) {

            event.preventDefault();

        }
    );


    record.addEventListener(
        "drop",
        function (event) {

            event.preventDefault();


            const data =
                event.dataTransfer.getData(
                    "text/plain"
                );


            if (!data) {
                return;
            }


            try {

                const song =
                    JSON.parse(data);


                loadSong(song);

            }
            catch (error) {

                console.error(error);

            }

        }
    );


    /* -------------------------------------------------
       TONEARM
    ------------------------------------------------- */

    tonearm.addEventListener(
        "click",
        function () {

            if (!currentSong) {
                return;
            }


            if (
                audio.paused
            ) {

                tonearm.classList.remove(
                    "lifted"
                );


                record.classList.add(
                    "spinning"
                );


                const promise =
                    audio.play();


                if (
                    promise &&
                    typeof promise.catch === "function"
                ) {

                    promise.catch(
                        function () {}
                    );

                }

            }
            else {

                audio.pause();


                tonearm.classList.add(
                    "lifted"
                );


                record.classList.remove(
                    "spinning"
                );

            }

        }
    );


    /* -------------------------------------------------
       AUDIO END
    ------------------------------------------------- */

    audio.addEventListener(
        "ended",
        function () {

            record.classList.remove(
                "spinning"
            );


            tonearm.classList.add(
                "lifted"
            );

        }
    );


    /* -------------------------------------------------
       STOP AUDIO
    ------------------------------------------------- */

    function stopAudio() {

        audio.pause();


        audio.currentTime = 0;


        audio.removeAttribute(
            "src"
        );


        audio.load();


        record.classList.remove(
            "spinning"
        );


        tonearm.classList.add(
            "lifted"
        );


        currentSong = null;

    }


    /* -------------------------------------------------
       ESCAPE HTML
    ------------------------------------------------- */

    function escapeHTML(value) {

        return String(value)

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


    /* -------------------------------------------------
       INITIAL STATE
    ------------------------------------------------- */

    showPage(opening);

})();

</script>
"""


# =========================================================
# HTML 실행
# =========================================================

st.html(
    html,
    width="stretch",
    unsafe_allow_javascript=True
)