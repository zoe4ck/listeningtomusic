import html
import json
import re
from typing import Any, Dict, List
from urllib.parse import quote

import requests
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# RECORD ROOM
# =========================================================

st.set_page_config(
    page_title="RECORD ROOM",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 20% 10%, rgba(186,126,72,.12), transparent 25%),
        radial-gradient(circle at 80% 80%, rgba(0,0,0,.28), transparent 40%),
        repeating-linear-gradient(
            92deg,
            rgba(255,255,255,.018) 0px,
            rgba(255,255,255,.018) 2px,
            transparent 2px,
            transparent 13px
        ),
        linear-gradient(180deg,#3a2115 0%,#25150e 52%,#1b0f0a 100%);
    color:#f1dfc1;
}

[data-testid="stHeader"] {
    background:transparent;
}

[data-testid="stToolbar"],
[data-testid="stSidebar"] {
    display:none;
}

.block-container {
    max-width:1400px;
    padding:1.5rem 2rem 3rem !important;
}

.stButton > button {
    border:1px solid #a98252 !important;
    border-radius:10px !important;
    background:#3b2115 !important;
    color:#f1dfc1 !important;
    min-height:44px !important;
}

.stButton > button:hover {
    background:#684027 !important;
    border-color:#d2b078 !important;
}

div[data-testid="stTextInput"] input {
    background:#21120b !important;
    color:#f4e7cf !important;
    border:1px solid #89633f !important;
    border-radius:12px !important;
    min-height:48px !important;
}

.record-title {
    font-family:Georgia,serif;
    letter-spacing:.22em;
    color:#ead3aa;
}

.record-subtitle {
    color:#b99a74;
    font-size:14px;
    letter-spacing:.08em;
}

.music-card {
    background:linear-gradient(145deg,#5a3521,#2a170e);
    border:1px solid rgba(205,166,105,.42);
    border-radius:14px;
    padding:10px;
    box-shadow:0 12px 30px rgba(0,0,0,.28);
    transition:.2s;
}

.music-card:hover {
    transform:translateY(-4px);
    border-color:#d4ae72;
}

.music-card img {
    width:100%;
    aspect-ratio:1/1;
    object-fit:cover;
    border-radius:9px;
}

.music-name {
    margin-top:9px;
    color:#f0ddbd;
    font-weight:600;
    font-size:14px;
}

.artist-name {
    margin-top:3px;
    color:#b99a74;
    font-size:12px;
}

.player-shell {
    background:
        linear-gradient(145deg,rgba(118,72,42,.9),rgba(35,19,11,.96));
    border:1px solid #9b7047;
    border-radius:24px;
    padding:35px;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.05),
        0 25px 60px rgba(0,0,0,.4);
}

.player-title {
    text-align:center;
    font-family:Georgia,serif;
    color:#ecd6ad;
    letter-spacing:.13em;
}

.turntable {
    position:relative;
    width:430px;
    height:430px;
    max-width:80vw;
    margin:35px auto;
    border-radius:50%;
    background:
        repeating-radial-gradient(
            circle,
            #151515 0px,
            #151515 2px,
            #1d1d1d 3px,
            #101010 5px
        );
    box-shadow:
        0 20px 45px rgba(0,0,0,.55),
        inset 0 0 0 9px #272727,
        inset 0 0 0 11px #090909;
    cursor:pointer;
    transition:transform .2s;
}

.turntable:hover {
    transform:scale(1.015);
}

.turntable.spinning {
    animation:spin 1.8s linear infinite;
}

@keyframes spin {
    from { transform:rotate(0deg); }
    to { transform:rotate(360deg); }
}

.vinyl-label {
    position:absolute;
    width:128px;
    height:128px;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    border-radius:50%;
    overflow:hidden;
    border:4px solid #252525;
    box-shadow:0 3px 10px rgba(0,0,0,.5);
}

.vinyl-label img {
    width:100%;
    height:100%;
    object-fit:cover;
}

.vinyl-hole {
    position:absolute;
    width:13px;
    height:13px;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    background:#080808;
    border-radius:50%;
    border:2px solid #555;
    z-index:3;
}

.drop-zone {
    text-align:center;
    color:#a98a66;
    font-size:12px;
    letter-spacing:.08em;
    margin-top:-8px;
}

.now-playing {
    text-align:center;
    color:#ecd6ad;
    font-family:Georgia,serif;
    font-size:18px;
    margin-top:18px;
}

.now-playing-artist {
    text-align:center;
    color:#ad8c65;
    font-size:13px;
    margin-top:5px;
}

.hero {
    min-height:72vh;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    text-align:center;
}

.hero h1 {
    font-family:Georgia,serif;
    font-size:clamp(42px,7vw,86px);
    letter-spacing:.2em;
    margin:0;
    color:#ead1a4;
    text-shadow:0 5px 25px rgba(0,0,0,.5);
}

.hero p {
    color:#b99870;
    margin-top:18px;
    letter-spacing:.12em;
}

.choice-wrap {
    max-width:850px;
    margin:100px auto;
    text-align:center;
}

.choice-title {
    font-family:Georgia,serif;
    color:#e9d0a5;
    font-size:34px;
    letter-spacing:.12em;
}

.choice-sub {
    color:#a98b68;
    margin-bottom:45px;
}

.back-text {
    color:#a88965;
    font-size:13px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "results" not in st.session_state:
    st.session_state.results = []

if "selected" not in st.session_state:
    st.session_state.selected = None

if "playing" not in st.session_state:
    st.session_state.playing = False


# =========================================================
# iTUNES SEARCH
# =========================================================

@st.cache_data(ttl=600)
def fetch_itunes(term: str, limit: int = 24):
    url = "https://itunes.apple.com/search"

    params = {
        "term": term,
        "country": "KR",
        "media": "music",
        "entity": "song",
        "limit": limit,
        "lang": "ko_kr",
    }

    try:
        response = requests.get(url, params=params, timeout=8)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception:
        return []


@st.cache_data(ttl=600)
def fetch_artist(term: str):
    url = "https://itunes.apple.com/search"

    params = {
        "term": term,
        "country": "KR",
        "media": "music",
        "entity": "musicArtist",
        "limit": 10,
        "lang": "ko_kr",
    }

    try:
        response = requests.get(url, params=params, timeout=8)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception:
        return []


@st.cache_data(ttl=600)
def fetch_artist_tracks(artist_id: int, limit: int = 24):
    url = "https://itunes.apple.com/lookup"

    params = {
        "id": artist_id,
        "entity": "song",
        "country": "KR",
        "limit": limit,
    }

    try:
        response = requests.get(url, params=params, timeout=8)
        response.raise_for_status()
        results = response.json().get("results", [])

        return [
            item for item in results
            if item.get("wrapperType") == "track"
            and item.get("kind") == "song"
        ]

    except Exception:
        return []


def normalize(items):
    output = []

    seen = set()

    for item in items:
        track = item.get("trackName")
        artist = item.get("artistName")
        artwork = item.get("artworkUrl100")
        preview = item.get("previewUrl")

        if not track or not artist or not artwork or not preview:
            continue

        key = (
            track.lower().strip(),
            artist.lower().strip()
        )

        if key in seen:
            continue

        seen.add(key)

        artwork = artwork.replace(
            "100x100bb",
            "600x600bb"
        )

        output.append({
            "track": track,
            "artist": artist,
            "album": item.get("collectionName", ""),
            "cover": artwork,
            "preview": preview,
            "url": item.get("trackViewUrl", ""),
        })

    return output


def search_music(term):
    term = term.strip()

    if not term:
        return []

    # 먼저 가수 검색
    artists = fetch_artist(term)

    exact_artist = None

    for artist in artists:
        name = artist.get("artistName", "").strip().lower()

        if name == term.lower():
            exact_artist = artist
            break

    if exact_artist:
        tracks = fetch_artist_tracks(
            exact_artist["artistId"]
        )

        result = normalize(tracks)

        if result:
            return result

    # 일반 곡 검색
    songs = fetch_itunes(term)

    # 검색어가 가수명이라면 artistName 일치 결과 우선
    artist_matches = [
        item for item in songs
        if item.get("artistName", "").strip().lower()
        == term.lower()
    ]

    if artist_matches:
        return normalize(artist_matches)

    return normalize(songs)


# =========================================================
# JAVASCRIPT DRAG & DROP BRIDGE
# =========================================================

def drag_album_card(song, index):

    card_id = f"album_{index}"

    components.html(
        f"""
        <div
            id="{card_id}"
            draggable="true"
            style="
                background:linear-gradient(145deg,#5a3521,#2a170e);
                border:1px solid rgba(205,166,105,.42);
                border-radius:14px;
                padding:10px;
                cursor:grab;
                color:#f0ddbd;
                box-shadow:0 12px 30px rgba(0,0,0,.28);
                font-family:Arial,sans-serif;
            "
        >
            <img
                src="{song["cover"]}"
                style="
                    width:100%;
                    aspect-ratio:1/1;
                    object-fit:cover;
                    border-radius:9px;
                    display:block;
                "
            >

            <div style="
                margin-top:9px;
                font-size:14px;
                font-weight:600;
                white-space:nowrap;
                overflow:hidden;
                text-overflow:ellipsis;
            ">
                {html.escape(song["track"])}
            </div>

            <div style="
                margin-top:3px;
                color:#b99a74;
                font-size:12px;
                white-space:nowrap;
                overflow:hidden;
                text-overflow:ellipsis;
            ">
                {html.escape(song["artist"])}
            </div>
        </div>

        <script>
        const card = document.getElementById("{card_id}");

        if (card) {{
            card.addEventListener("dragstart", function(event) {{
                event.dataTransfer.setData(
                    "text/plain",
                    JSON.stringify({{
                        index: {index}
                    }})
                );
            }});
        }}
        </script>
        """,
        height=245,
    )


# =========================================================
# HOME
# =========================================================

def show_home():

    st.markdown(
        """
        <div class="hero">

            <h1>RECORD ROOM</h1>

            <p>
                오늘의 음악을 한 장의 레코드처럼.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        if st.button(
            "ENTER ROOM",
            use_container_width=True,
        ):
            st.session_state.page = "choice"
            st.rerun()


# =========================================================
# CHOICE
# =========================================================

def show_choice():

    st.markdown(
        """
        <div class="choice-wrap">

            <div class="choice-title">
                WELCOME TO THE ROOM
            </div>

            <div class="choice-sub">
                오늘은 무엇을 해볼까요?
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.write("")

    with col2:

        if st.button(
            "♫  노래듣기",
            use_container_width=True,
        ):
            st.session_state.page = "listen"
            st.rerun()

        if st.button(
            "✦  노래 추천받기",
            use_container_width=True,
        ):
            st.session_state.page = "recommend"
            st.rerun()

    with col3:
        st.write("")


# =========================================================
# LISTEN
# =========================================================

def show_listen():

    top1, top2 = st.columns([1, 7])

    with top1:
        if st.button("← BACK"):
            st.session_state.page = "choice"
            st.session_state.playing = False
            st.rerun()

    st.markdown(
        """
        <div style="
            text-align:center;
            margin:15px 0 25px;
        ">
            <div class="record-title" style="font-size:34px;">
                RECORD ROOM
            </div>

            <div class="record-subtitle">
                SEARCH YOUR RECORD
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "검색",
        placeholder="가수 이름이나 노래 제목을 검색해보세요.",
        label_visibility="collapsed",
    )

    if query:

        if st.session_state.get("last_query") != query:

            st.session_state.results = search_music(query)
            st.session_state.last_query = query

    results = st.session_state.results

    if query and not results:

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:70px 20px;
                color:#ad8c65;
            ">
                검색 결과가 없습니다.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    if not results:

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:65px 20px;
                color:#ad8c65;
            ">
                가수 이름이나 노래 제목을 검색해보세요.<br>
                <span style="font-size:12px;">
                    예: 아이유 / 뉴진스 / 지코 / Love wins all
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    st.markdown(
        """
        <div style="
            color:#a98b68;
            font-size:12px;
            margin:20px 0 12px;
            letter-spacing:.08em;
        ">
            RECORDS
        </div>
        """,
        unsafe_allow_html=True,
    )

    columns = st.columns(4)

    for i, song in enumerate(results[:24]):

        with columns[i % 4]:

            drag_album_card(
                song,
                i,
            )

            if st.button(
                "PLAY",
                key=f"select_{i}",
                use_container_width=True,
            ):
                st.session_state.selected = song
                st.session_state.playing = True
                st.session_state.page = "player"
                st.rerun()


# =========================================================
# PLAYER
# =========================================================

def show_player():

    if not st.session_state.selected:

        st.session_state.page = "listen"
        st.rerun()

    song = st.session_state.selected

    top1, top2 = st.columns([1, 7])

    with top1:

        if st.button("← BACK"):

            st.session_state.playing = False
            st.session_state.page = "listen"

            st.rerun()

    st.markdown(
        """
        <div class="player-shell">

            <div class="player-title">
                NOW PLAYING
            </div>
        """,
        unsafe_allow_html=True,
    )

    playing_class = (
        "turntable spinning"
        if st.session_state.playing
        else "turntable"
    )

    audio_html = ""

    if st.session_state.playing:

        audio_html = f"""
        <audio
            id="recordAudio"
            autoplay
            src="{song["preview"]}"
        ></audio>

        <script>
        const audio = document.getElementById("recordAudio");

        if (audio) {{
            audio.play().catch(() => {{}});
        }}
        </script>
        """

    st.markdown(
        f"""
        <div
            class="{playing_class}"
            id="vinyl"
            title="클릭: 재생/일시정지 · 더블클릭: 정지"
        >

            <div class="vinyl-label">
                <img src="{song["cover"]}">
            </div>

            <div class="vinyl-hole"></div>

        </div>

        <div class="now-playing">
            {html.escape(song["track"])}
        </div>

        <div class="now-playing-artist">
            {html.escape(song["artist"])}
        </div>

        <div class="drop-zone">
            LP를 클릭해서 재생 / 일시정지 · 더블클릭해서 정지
        </div>

        {audio_html}

        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# =========================================================
# RECOMMEND
# =========================================================

def show_recommend():

    if st.button("← BACK"):

        st.session_state.page = "choice"
        st.rerun()

    st.markdown(
        """
        <div style="
            text-align:center;
            margin:80px 0;
        ">

            <div class="record-title" style="font-size:36px;">
                RECORD RECOMMENDATION
            </div>

            <div class="record-subtitle">
                당신의 오늘에 어울리는 한 장
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    moods = [
        "오늘은 잔잔하게",
        "기분 전환이 필요해",
        "밤에 듣기 좋은 음악",
        "신나는 음악이 듣고 싶어",
    ]

    cols = st.columns(2)

    for i, mood in enumerate(moods):

        with cols[i % 2]:

            if st.button(
                mood,
                key=f"mood_{i}",
                use_container_width=True,
            ):

                recommendations = {
                    "오늘은 잔잔하게": "아이유",
                    "기분 전환이 필요해": "지코",
                    "밤에 듣기 좋은 음악": "검정치마",
                    "신나는 음악이 듣고 싶어": "실리카겔",
                }

                artist = recommendations[mood]

                st.session_state.results = search_music(
                    artist
                )

                st.session_state.last_query = artist
                st.session_state.page = "listen"

                st.rerun()


# =========================================================
# APP
# =========================================================

if st.session_state.page == "home":
    show_home()

elif st.session_state.page == "choice":
    show_choice()

elif st.session_state.page == "listen":
    show_listen()

elif st.session_state.page == "player":
    show_player()

elif st.session_state.page == "recommend":
    show_recommend()