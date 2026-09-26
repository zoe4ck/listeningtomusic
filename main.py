import json
import html
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

# ---------------------------------------------------------
# Vintage wood / record bar design
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 18% 8%, rgba(196,139,82,.13), transparent 27%),
            radial-gradient(circle at 82% 90%, rgba(0,0,0,.30), transparent 42%),
            repeating-linear-gradient(
                90deg,
                rgba(255,255,255,.012) 0px,
                rgba(255,255,255,.012) 2px,
                transparent 2px,
                transparent 15px
            ),
            linear-gradient(180deg, #3a2114 0%, #24140d 55%, #160c08 100%);
        color: #ead8ba;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"],
    [data-testid="stSidebar"] {
        display: none;
    }

    .block-container {
        max-width: 1400px;
        padding: 1.2rem 2rem 3rem !important;
    }

    .stButton > button {
        min-height: 44px !important;
        border-radius: 10px !important;
        border: 1px solid #a67b4c !important;
        background: linear-gradient(145deg, #4c2b1a, #2c180e) !important;
        color: #ead8ba !important;
        font-weight: 500 !important;
    }

    .stButton > button:hover {
        border-color: #d5b27d !important;
        background: linear-gradient(145deg, #694026, #3a2114) !important;
    }

    div[data-testid="stTextInput"] input {
        height: 50px !important;
        background: #1e110a !important;
        color: #f0dfc2 !important;
        border: 1px solid #8f6843 !important;
        border-radius: 12px !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #8f7257 !important;
    }

    .rr-header {
        text-align: center;
        margin: 10px 0 28px;
    }

    .rr-title {
        font-family: Georgia, "Times New Roman", serif;
        color: #ead1a5;
        letter-spacing: .22em;
        font-size: 38px;
        margin: 0;
    }

    .rr-small {
        color: #a98a67;
        font-size: 12px;
        letter-spacing: .14em;
        margin-top: 8px;
    }

    .rr-divider {
        width: 90px;
        height: 1px;
        background: #a67b4c;
        margin: 18px auto 0;
        opacity: .65;
    }

    .hero {
        min-height: 72vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .hero-title {
        font-family: Georgia, "Times New Roman", serif;
        color: #ead1a5;
        font-size: clamp(46px, 8vw, 88px);
        letter-spacing: .20em;
        margin: 0;
        text-shadow: 0 8px 30px rgba(0,0,0,.5);
    }

    .hero-sub {
        color: #b99970;
        letter-spacing: .12em;
        margin-top: 18px;
        font-size: 14px;
    }

    .choice-box {
        max-width: 760px;
        margin: 90px auto;
        text-align: center;
    }

    .choice-title {
        font-family: Georgia, "Times New Roman", serif;
        color: #ead1a5;
        font-size: 34px;
        letter-spacing: .12em;
    }

    .choice-sub {
        color: #a98a67;
        margin: 12px 0 38px;
    }

    .section-label {
        color: #a98a67;
        font-size: 11px;
        letter-spacing: .18em;
        margin: 24px 0 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# Session state
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "query" not in st.session_state:
    st.session_state.query = ""

if "results" not in st.session_state:
    st.session_state.results = []


# =========================================================
# iTunes Search
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def itunes_song_search(term, limit=24):
    try:
        response = requests.get(
            "https://itunes.apple.com/search",
            params={
                "term": term,
                "country": "KR",
                "media": "music",
                "entity": "song",
                "limit": limit,
                "lang": "ko_kr",
            },
            timeout=8,
        )
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception:
        return []


@st.cache_data(ttl=600, show_spinner=False)
def itunes_artist_search(term):
    try:
        response = requests.get(
            "https://itunes.apple.com/search",
            params={
                "term": term,
                "country": "KR",
                "media": "music",
                "entity": "musicArtist",
                "limit": 10,
                "lang": "ko_kr",
            },
            timeout=8,
        )
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception:
        return []


@st.cache_data(ttl=600, show_spinner=False)
def itunes_artist_tracks(artist_id, limit=30):
    try:
        response = requests.get(
            "https://itunes.apple.com/lookup",
            params={
                "id": artist_id,
                "entity": "song",
                "country": "KR",
                "limit": limit,
            },
            timeout=8,
        )
        response.raise_for_status()
        data = response.json().get("results", [])
        return [
            item for item in data
            if item.get("wrapperType") == "track"
            and item.get("kind") == "song"
        ]
    except Exception:
        return []


def normalize_tracks(items):
    result = []
    seen = set()

    for item in items:
        track = (item.get("trackName") or "").strip()
        artist = (item.get("artistName") or "").strip()
        artwork = item.get("artworkUrl100")
        preview = item.get("previewUrl")

        if not track or not artist or not artwork or not preview:
            continue

        key = (track.lower(), artist.lower())
        if key in seen:
            continue
        seen.add(key)

        artwork = artwork.replace("100x100bb", "600x600bb")

        result.append(
            {
                "track": track,
                "artist": artist,
                "album": item.get("collectionName") or "",
                "cover": artwork,
                "preview": preview,
                "url": item.get("trackViewUrl") or "",
            }
        )

    return result


def search_music(term):
    term = term.strip()
    if not term:
        return []

    # 1. 먼저 가수명으로 정확히 일치하는 아티스트를 찾는다.
    artists = itunes_artist_search(term)

    exact = None
    normalized_term = term.casefold()

    for artist in artists:
        name = (artist.get("artistName") or "").strip().casefold()
        if name == normalized_term:
            exact = artist
            break

    if exact:
        tracks = normalize_tracks(
            itunes_artist_tracks(exact["artistId"])
        )
        if tracks:
            return tracks

    # 2. 일반 곡 검색.
    songs = itunes_song_search(term)

    # 3. artistName이 검색어와 정확히 같은 결과를 우선한다.
    exact_artist_songs = [
        item
        for item in songs
        if (item.get("artistName") or "").strip().casefold()
        == normalized_term
    ]

    if exact_artist_songs:
        return normalize_tracks(exact_artist_songs)

    # 4. 제목/아티스트가 검색어를 포함하는 결과.
    return normalize_tracks(songs)


# =========================================================
# HTML music room
# =========================================================

def render_music_room(results):
    safe_results = []

    for item in results[:24]:
        safe_results.append(
            {
                "track": item["track"],
                "artist": item["artist"],
                "album": item["album"],
                "cover": item["cover"],
                "preview": item["preview"],
                "url": item["url"],
            }
        )

    data_json = json.dumps(
        safe_results,
        ensure_ascii=False,
    ).replace("</", "<\\/")

    component_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: transparent;
    color: #ead8ba;
    font-family: Arial, sans-serif;
}

.room {
    width: 100%;
}

.records {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
}

.card {
    background: linear-gradient(145deg, #5b3520, #2a170d);
    border: 1px solid rgba(211,173,115,.40);
    border-radius: 14px;
    padding: 10px;
    cursor: grab;
    box-shadow: 0 12px 28px rgba(0,0,0,.27);
    transition: transform .18s, border-color .18s, box-shadow .18s;
    user-select: none;
}

.card:hover {
    transform: translateY(-5px);
    border-color: #d5b27d;
    box-shadow: 0 16px 35px rgba(0,0,0,.36);
}

.card:active {
    cursor: grabbing;
}

.cover {
    width: 100%;
    aspect-ratio: 1;
    display: block;
    object-fit: cover;
    border-radius: 9px;
    pointer-events: none;
}

.track {
    margin-top: 9px;
    color: #f0dfc2;
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.artist {
    color: #ad8d69;
    font-size: 12px;
    margin-top: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.player-wrap {
    margin-top: 42px;
    padding: 34px 22px 32px;
    background:
        linear-gradient(145deg, rgba(91,54,31,.93), rgba(35,19,11,.98));
    border: 1px solid #916a43;
    border-radius: 24px;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.045),
        0 24px 55px rgba(0,0,0,.38);
    text-align: center;
}

.player-heading {
    color: #c6a37a;
    font-size: 10px;
    letter-spacing: .28em;
    margin-bottom: 8px;
}

.now-title {
    color: #ecd7b3;
    font-family: Georgia, serif;
    font-size: 20px;
    margin-bottom: 4px;
}

.now-artist {
    color: #a98a67;
    font-size: 13px;
}

.turntable {
    position: relative;
    width: min(410px, 72vw);
    aspect-ratio: 1;
    margin: 28px auto 20px;
    border-radius: 50%;
    cursor: pointer;

    background:
        repeating-radial-gradient(
            circle,
            #0d0d0d 0px,
            #0d0d0d 2px,
            #1a1a1a 3px,
            #090909 5px
        );

    box-shadow:
        0 20px 45px rgba(0,0,0,.60),
        inset 0 0 0 9px #272727,
        inset 0 0 0 11px #080808;

    transition: transform .15s, box-shadow .15s;
}

.turntable:hover {
    box-shadow:
        0 23px 50px rgba(0,0,0,.65),
        inset 0 0 0 9px #302f2e,
        inset 0 0 0 11px #080808;
}

.turntable.spinning {
    animation: vinylSpin 2.0s linear infinite;
}

@keyframes vinylSpin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.label {
    position: absolute;
    width: 128px;
    height: 128px;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid #252525;
    box-shadow:
        0 4px 13px rgba(0,0,0,.55),
        inset 0 0 0 2px rgba(255,255,255,.12);
}

.label img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.center-hole {
    position: absolute;
    z-index: 5;
    width: 13px;
    height: 13px;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background: #070707;
    border: 2px solid #555;
}

.drop-hint {
    color: #9f815f;
    font-size: 11px;
    letter-spacing: .08em;
    margin-top: 7px;
}

.turntable.drag-over {
    box-shadow:
        0 0 0 3px rgba(211,173,115,.75),
        0 24px 55px rgba(0,0,0,.65),
        inset 0 0 0 9px #302f2e,
        inset 0 0 0 11px #080808;
    transform: scale(1.02);
}

.empty {
    text-align: center;
    color: #9d7e5d;
    padding: 42px 10px;
    border: 1px dashed rgba(176,137,91,.32);
    border-radius: 14px;
}

@media (max-width: 900px) {
    .records {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
}

@media (max-width: 650px) {
    .records {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 11px;
    }

    .card {
        padding: 8px;
    }

    .track {
        font-size: 12px;
    }

    .artist {
        font-size: 11px;
    }
}
</style>
</head>

<body>

<div class="room">

    <div class="records" id="records"></div>

    <div class="player-wrap">

        <div class="player-heading">THE RECORD PLAYER</div>

        <div class="now-title" id="nowTitle">
            LP를 이곳에 올려주세요
        </div>

        <div class="now-artist" id="nowArtist">
            앨범 커버를 드래그해서 LP 위에 놓으면 재생됩니다.
        </div>

        <div
            class="turntable"
            id="turntable"
            title="클릭: 재생 / 일시정지 · 더블클릭: 정지"
        >
            <div class="center-hole"></div>
        </div>

        <div class="drop-hint">
            DRAG A RECORD HERE · CLICK TO PLAY / PAUSE · DOUBLE CLICK TO STOP
        </div>

    </div>

</div>

<audio id="audio" preload="none"></audio>

<script>
const songs = __SONGS_JSON__;

const records = document.getElementById("records");
const turntable = document.getElementById("turntable");
const audio = document.getElementById("audio");
const nowTitle = document.getElementById("nowTitle");
const nowArtist = document.getElementById("nowArtist");

let selected = null;
let playing = false;

function escapeText(value) {
    return String(value ?? "");
}

function createCards() {
    if (!songs.length) {
        records.innerHTML =
            '<div class="empty" style="grid-column:1/-1;">검색 결과가 없습니다.</div>';
        return;
    }

    songs.forEach((song, index) => {
        const card = document.createElement("div");
        card.className = "card";
        card.draggable = true;

        const img = document.createElement("img");
        img.className = "cover";
        img.src = song.cover;
        img.alt = "";

        const track = document.createElement("div");
        track.className = "track";
        track.textContent = escapeText(song.track);

        const artist = document.createElement("div");
        artist.className = "artist";
        artist.textContent = escapeText(song.artist);

        card.appendChild(img);
        card.appendChild(track);
        card.appendChild(artist);

        card.addEventListener("dragstart", function(event) {
            event.dataTransfer.effectAllowed = "copy";
            event.dataTransfer.setData(
                "text/plain",
                String(index)
            );
            card.style.opacity = ".55";
        });

        card.addEventListener("dragend", function() {
            card.style.opacity = "1";
        });

        records.appendChild(card);
    });
}

function setLabel(song) {
    const old = turntable.querySelector(".label");
    if (old) old.remove();

    const label = document.createElement("div");
    label.className = "label";

    const img = document.createElement("img");
    img.src = song.cover;
    img.alt = "";

    label.appendChild(img);

    const hole = document.createElement("div");
    hole.className = "center-hole";

    turntable.appendChild(label);
    turntable.appendChild(hole);
}

function startSong(song) {
    selected = song;

    nowTitle.textContent = escapeText(song.track);
    nowArtist.textContent = escapeText(song.artist);

    setLabel(song);

    audio.src = song.preview;
    audio.currentTime = 0;

    audio.play()
        .then(function() {
            playing = true;
            turntable.classList.add("spinning");
        })
        .catch(function() {
            playing = false;
            turntable.classList.remove("spinning");
        });
}

function pauseSong() {
    if (!selected) return;

    audio.pause();
    playing = false;
    turntable.classList.remove("spinning");
}

function resumeSong() {
    if (!selected) return;

    audio.play()
        .then(function() {
            playing = true;
            turntable.classList.add("spinning");
        })
        .catch(function() {});
}

function stopSong() {
    audio.pause();

    try {
        audio.currentTime = 0;
    } catch (e) {}

    playing = false;
    turntable.classList.remove("spinning");

    if (selected) {
        nowTitle.textContent = escapeText(selected.track);
        nowArtist.textContent = escapeText(selected.artist);
    }
}

turntable.addEventListener("dragover", function(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
    turntable.classList.add("drag-over");
});

turntable.addEventListener("dragleave", function() {
    turntable.classList.remove("drag-over");
});

turntable.addEventListener("drop", function(event) {
    event.preventDefault();
    turntable.classList.remove("drag-over");

    const index = Number(
        event.dataTransfer.getData("text/plain")
    );

    if (
        Number.isInteger(index) &&
        index >= 0 &&
        index < songs.length
    ) {
        startSong(songs[index]);
    }
});

turntable.addEventListener("click", function() {
    if (!selected) return;

    if (playing) {
        pauseSong();
    } else {
        resumeSong();
    }
});

turntable.addEventListener("dblclick", function(event) {
    event.preventDefault();
    stopSong();
});

audio.addEventListener("ended", function() {
    playing = false;
    turntable.classList.remove("spinning");
});

createCards();
</script>

</body>
</html>
"""

    component_html = component_html.replace(
        "__SONGS_JSON__",
        data_json,
    )

    components.html(
        component_html,
        height=790,
        scrolling=False,
    )


# =========================================================
# HOME
# =========================================================

def show_home():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">RECORD ROOM</div>
            <div class="hero-sub">오늘의 음악을 한 장의 레코드처럼.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 1.2, 1])

    with center:
        if st.button("ENTER ROOM", use_container_width=True):
            st.session_state.page = "choice"
            st.rerun()


# =========================================================
# CHOICE
# =========================================================

def show_choice():
    st.markdown(
        """
        <div class="choice-box">
            <div class="choice-title">WELCOME TO THE ROOM</div>
            <div class="choice-sub">오늘은 무엇을 해볼까요?</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 1.15, 1])

    with center:
        if st.button("♫  노래듣기", use_container_width=True):
            st.session_state.page = "listen"
            st.rerun()

        if st.button("✦  노래 추천받기", use_container_width=True):
            st.session_state.page = "recommend"
            st.rerun()


# =========================================================
# LISTEN
# =========================================================

def show_listen():
    if st.button("← BACK"):
        st.session_state.page = "choice"
        st.rerun()

    st.markdown(
        """
        <div class="rr-header">
            <div class="rr-title">RECORD ROOM</div>
            <div class="rr-small">SEARCH YOUR RECORD</div>
            <div class="rr-divider"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "music-search",
        value=st.session_state.query,
        placeholder="가수 이름이나 노래 제목을 검색해보세요.",
        label_visibility="collapsed",
    )

    # 수정된 조건문: 입력값이 변경되었거나, 값은 있는데 결과가 비어있는 경우 검색 수행[span_1](start_span)[span_1](end_span)
    if query != st.session_state.query or (query.strip() and not st.session_state.results):
        st.session_state.query = query

        if query.strip():
            with st.spinner("레코드를 찾는 중..."):
                st.session_state.results = search_music(query)
        else:
            st.session_state.results = []

    if not query.strip():
        st.markdown(
            """
            <div class="section-label">RECORDS</div>
            """,
            unsafe_allow_html=True,
        )

        render_music_room([])
        return

    st.markdown(
        f"""
        <div class="section-label">
            SEARCH RESULTS · {len(st.session_state.results)} RECORDS
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_music_room(st.session_state.results)


# =========================================================
# RECOMMEND
# =========================================================

def show_recommend():
    if st.button("← BACK"):
        st.session_state.page = "choice"
        st.rerun()

    st.markdown(
        """
        <div class="choice-box">
            <div class="choice-title">RECORD RECOMMENDATION</div>
            <div class="choice-sub">
                오늘의 기분을 골라보세요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    moods = {
        "오늘은 잔잔하게": "아이유",
        "기분 전환이 필요해": "지코",
        "밤에 듣기 좋은 음악": "검정치마",
        "신나는 음악이 듣고 싶어": "실리카겔",
    }

    c1, c2 = st.columns(2)

    for i, (mood, artist) in enumerate(moods.items()):
        with (c1 if i % 2 == 0 else c2):
            if st.button(mood, key=f"mood_{i}", use_container_width=True):
                st.session_state.query = artist
                st.session_state.results = search_music(artist)
                st.session_state.page = "listen"
                st.rerun()


# =========================================================
# ROUTER
# =========================================================

if st.session_state.page == "home":
    show_home()

elif st.session_state.page == "choice":
    show_choice()

elif st.session_state.page == "listen":
    show_listen()

elif st.session_state.page == "recommend":
    show_recommend()
