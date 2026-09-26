import streamlit as st
import urllib.parse
import urllib.request
import json
import html

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="RECORD ROOM",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# Session State
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "search_keyword" not in st.session_state:
    st.session_state.search_keyword = ""

if "songs" not in st.session_state:
    st.session_state.songs = []

if "selected_song" not in st.session_state:
    st.session_state.selected_song = None

if "playing" not in st.session_state:
    st.session_state.playing = False


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* 전체 페이지 */
    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top, #3f2919 0%, #21150d 45%, #120b07 100%) !important;
        color: #f4e7d2 !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    section.main > div {
        padding-top: 0 !important;
    }

    .block-container {
        max-width: 1250px !important;
        padding-top: 25px !important;
        padding-bottom: 50px !important;
    }

    /* 기본 버튼 */
    div.stButton > button {
        border-radius: 4px !important;
        border: 1px solid #b79268 !important;
        background: #2b1b11 !important;
        color: #f4e6d0 !important;
        font-family: Georgia, "Times New Roman", serif !important;
        letter-spacing: 1px !important;
        transition: 0.2s ease !important;
        box-shadow:
            inset 0 0 0 1px rgba(255,255,255,0.03),
            0 4px 15px rgba(0,0,0,0.2) !important;
    }

    div.stButton > button:hover {
        background: #62442d !important;
        border-color: #dfbc8f !important;
        color: white !important;
        transform: translateY(-1px);
    }

    div.stButton > button:active {
        transform: translateY(0);
    }

    /* 입력창 */
    div[data-baseweb="input"] {
        background: #2a1a10 !important;
        border: 1px solid #8d6a49 !important;
    }

    div[data-baseweb="input"] input {
        color: #f4e6d2 !important;
        background: transparent !important;
    }

    /* 모든 label 숨김 */
    .stTextInput label {
        display: none !important;
    }

    /* 구분선 */
    hr {
        border-color: rgba(193, 154, 107, 0.25) !important;
    }

    /* 카드 */
    .song-card {
        background:
            linear-gradient(
                145deg,
                rgba(85,58,37,0.95),
                rgba(37,23,14,0.98)
            );
        border: 1px solid rgba(196,157,111,0.35);
        padding: 14px;
        border-radius: 5px;
        min-height: 310px;
        box-shadow:
            0 10px 28px rgba(0,0,0,0.28),
            inset 0 0 25px rgba(255,255,255,0.02);
    }

    .song-cover {
        width: 100%;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        display: block;
        margin-bottom: 13px;
    }

    .song-title {
        font-size: 17px;
        color: #f5e5cd;
        font-weight: 600;
        margin-bottom: 4px;
        line-height: 1.3;
    }

    .song-artist {
        font-size: 13px;
        color: #bb9f7d;
        line-height: 1.4;
    }

    .song-album {
        font-size: 11px;
        color: #8d755d;
        margin-top: 6px;
        line-height: 1.4;
    }

    /* 작은 태그 */
    .eyebrow {
        color: #b99a76;
        font-size: 11px;
        letter-spacing: 4px;
        text-transform: uppercase;
    }

    /* LP */
    .record-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 500px;
        padding: 20px;
    }

    .record {
        width: 390px;
        height: 390px;
        border-radius: 50%;
        position: relative;

        background:
            repeating-radial-gradient(
                circle at center,
                #0c0c0c 0px,
                #111 2px,
                #070707 4px,
                #121212 7px,
                #080808 10px
            );

        box-shadow:
            0 20px 55px rgba(0,0,0,0.6),
            inset 0 0 0 3px #090909,
            inset 0 0 0 8px #181818;
    }

    .record:after {
        content: "";
        position: absolute;
        inset: 50%;
        width: 16px;
        height: 16px;
        transform: translate(-50%, -50%);
        background: #ceb28d;
        border-radius: 50%;
        box-shadow: 0 0 0 5px #272727;
    }

    .record-label {
        position: absolute;
        left: 50%;
        top: 50%;
        width: 145px;
        height: 145px;
        transform: translate(-50%, -50%);
        border-radius: 50%;
        overflow: hidden;
        background: #24170e;
        border: 2px solid #6f4a2f;
    }

    .record-label img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .record-label-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #b99165;
        font-size: 12px;
        text-align: center;
        letter-spacing: 2px;
    }

    /* 회전 */
    .record-spin {
        animation: spin 3s linear infinite;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }

        to {
            transform: rotate(360deg);
        }
    }

    /* 톤암 */
    .tonearm-area {
        position: relative;
        width: 300px;
        height: 340px;
        margin: auto;
    }

    .tonearm-base {
        position: absolute;
        right: 35px;
        top: 35px;
        width: 54px;
        height: 54px;
        border-radius: 50%;
        background: #17120e;
        border: 2px solid #98724e;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4);
    }

    .tonearm {
        position: absolute;
        width: 190px;
        height: 10px;
        background: linear-gradient(90deg, #a98865, #d4b894, #8f6b49);
        border-radius: 20px;
        right: 52px;
        top: 77px;
        transform-origin: right center;
        transform: rotate(38deg);
        box-shadow: 0 3px 8px rgba(0,0,0,0.4);
        transition: transform 0.4s ease;
    }

    .tonearm.down {
        transform: rotate(18deg);
    }

    .needle {
        position: absolute;
        left: -17px;
        top: -5px;
        width: 24px;
        height: 20px;
        background: #392519;
        border: 1px solid #b38d68;
        clip-path: polygon(0 0,100% 22%,75% 100%,15% 78%);
    }

    /* 플레이어 정보 */
    .player-info {
        text-align: center;
        padding: 15px 10px 5px;
    }

    .player-title {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 27px;
        color: #f0dcc1;
        margin-bottom: 5px;
    }

    .player-artist {
        font-size: 15px;
        color: #ac8c6a;
    }

    .player-status {
        margin-top: 15px;
        font-size: 11px;
        letter-spacing: 3px;
        color: #8f755b;
    }

    /* 홈 */
    .home-wrap {
        text-align: center;
        padding-top: 110px;
        padding-bottom: 120px;
    }

    .home-small {
        letter-spacing: 5px;
        color: #a98a68;
        font-size: 12px;
        margin-bottom: 30px;
    }

    .home-title {
        font-family: Georgia, "Times New Roman", serif;
        font-size: clamp(58px, 10vw, 125px);
        line-height: 0.95;
        color: #f1dfc5;
        letter-spacing: 5px;
        text-shadow: 0 7px 30px rgba(0,0,0,0.35);
        margin-bottom: 27px;
    }

    .home-subtitle {
        color: #ad9274;
        font-size: 16px;
        letter-spacing: 3px;
        margin-bottom: 50px;
    }

    .home-divider {
        width: 180px;
        height: 1px;
        background: #87694a;
        margin: 0 auto 45px;
        opacity: 0.7;
    }

    /* 선택 화면 */
    .choice-wrap {
        text-align: center;
        padding-top: 100px;
        padding-bottom: 100px;
    }

    .choice-title {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 62px;
        color: #ebd4b4;
        margin-bottom: 12px;
    }

    .choice-sub {
        font-size: 14px;
        color: #987b5d;
        letter-spacing: 2px;
        margin-bottom: 55px;
    }

    /* 상단 바 */
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }

    .topbar-title {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 34px;
        color: #ecd6b8;
    }

    .tiny-text {
        color: #93785b;
        font-size: 11px;
        letter-spacing: 2px;
    }

    /* 빈 검색 결과 */
    .empty-box {
        border: 1px dashed rgba(185,151,111,0.3);
        padding: 60px 20px;
        text-align: center;
        color: #8f7359;
        margin-top: 30px;
    }

    /* 모바일 */
    @media (max-width: 700px) {

        .block-container {
            padding-left: 14px !important;
            padding-right: 14px !important;
        }

        .home-wrap {
            padding-top: 80px;
        }

        .home-title {
            font-size: 54px;
            letter-spacing: 2px;
        }

        .choice-title {
            font-size: 42px;
        }

        .record {
            width: 290px;
            height: 290px;
        }

        .record-label {
            width: 108px;
            height: 108px;
        }

        .tonearm-area {
            transform: scale(0.85);
            transform-origin: top center;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 함수
# =========================================================

def go(page_name):
    st.session_state.page = page_name
    st.rerun()


def search_itunes(keyword):
    """
    iTunes Search API를 Python에서 직접 호출.
    외부 라이브러리 없이 urllib 사용.
    """

    keyword = keyword.strip()

    if not keyword:
        return []

    try:
        params = urllib.parse.urlencode(
            {
                "term": keyword,
                "country": "KR",
                "media": "music",
                "entity": "song",
                "limit": 40,
            }
        )

        url = "https://itunes.apple.com/search?" + params

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        results = data.get("results", [])

        songs = []

        for item in results:

            preview = item.get("previewUrl")
            artwork = item.get("artworkUrl100")

            if not preview or not artwork:
                continue

            artwork = artwork.replace(
                "100x100bb",
                "600x600bb"
            )

            artwork = artwork.replace(
                "100x100-75",
                "600x600-75"
            )

            songs.append(
                {
                    "title": item.get("trackName", "제목 없음"),
                    "artist": item.get("artistName", "아티스트 없음"),
                    "album": item.get("collectionName", ""),
                    "cover": artwork,
                    "preview": preview,
                    "store": item.get("trackViewUrl", ""),
                }
            )

        return songs

    except Exception as e:
        st.error("음악 검색 중 문제가 발생했어요.")
        st.caption(str(e))
        return []


def song_card(song, number):
    title = html.escape(song["title"])
    artist = html.escape(song["artist"])
    album = html.escape(song["album"])

    st.markdown(
        f"""
        <div class="song-card">
            <img
                src="{song['cover']}"
                class="song-cover"
                alt="cover"
            >

            <div class="song-title">
                {title}
            </div>

            <div class="song-artist">
                {artist}
            </div>

            <div class="song-album">
                {album}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "RECORD에 올리기",
        key=f"song_{number}",
        use_container_width=True,
    ):
        st.session_state.selected_song = song
        st.session_state.playing = True
        st.session_state.page = "player"
        st.rerun()


# =========================================================
# HOME
# =========================================================

def page_home():

    st.markdown(
        """
        <div class="home-wrap">

            <div class="home-small">
                EST. 2026 · MUSIC & MEMORY
            </div>

            <div class="home-title">
                RECORD<br>ROOM
            </div>

            <div class="home-divider"></div>

            <div class="home-subtitle">
                오늘의 음악을 한 장의 레코드처럼.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        if st.button(
            "ENTER ROOM",
            use_container_width=True,
            type="primary",
        ):
            go("choice")


# =========================================================
# CHOICE
# =========================================================

def page_choice():

    st.markdown(
        """
        <div class="choice-wrap">

            <div class="eyebrow">
                RECORD ROOM
            </div>

            <div class="choice-title">
                What would you like?
            </div>

            <div class="choice-sub">
                오늘은 어떤 음악을 만나볼까요?
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(
        [1, 1.4, 1.4, 1]
    )

    with col2:
        if st.button(
            "♫  노래듣기",
            use_container_width=True,
        ):
            go("listen")

    with col3:
        if st.button(
            "♬  노래 추천받기",
            use_container_width=True,
        ):
            st.session_state.page = "recommend"
            st.rerun()


# =========================================================
# RECOMMEND
# =========================================================

def page_recommend():

    st.markdown(
        """
        <div style="text-align:center;padding-top:90px;">

            <div class="eyebrow">
                RECORD ROOM
            </div>

            <div class="choice-title">
                MUSIC RECOMMEND
            </div>

            <div class="choice-sub">
                이 기능은 다음 단계에서 확장할 수 있어요.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:

        st.info(
            "먼저 노래듣기 기능을 완성한 뒤 "
            "취향 기반 추천 기능을 붙이는 구조예요."
        )

        if st.button(
            "← 돌아가기",
            use_container_width=True,
        ):
            go("choice")


# =========================================================
# LISTEN
# =========================================================

def page_listen():

    st.markdown(
        """
        <div class="topbar">

            <div>
                <div class="eyebrow">
                    RECORD ROOM
                </div>

                <div class="topbar-title">
                    MUSIC ROOM
                </div>
            </div>

            <div class="tiny-text">
                FIND YOUR RECORD
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "← 선택 화면으로",
        key="back_choice",
    ):
        go("choice")

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("search_form"):

        col1, col2 = st.columns([5, 1])

        with col1:
            keyword = st.text_input(
                "search",
                value=st.session_state.search_keyword,
                placeholder="곡명, 아티스트를 검색해보세요",
                label_visibility="collapsed",
            )

        with col2:
            submit = st.form_submit_button(
                "SEARCH",
                use_container_width=True,
            )

    if submit:

        keyword = keyword.strip()

        st.session_state.search_keyword = keyword

        if keyword:

            with st.spinner("레코드를 찾고 있어요..."):

                songs = search_itunes(keyword)

            st.session_state.songs = songs

        else:

            st.session_state.songs = []

    songs = st.session_state.songs

    if songs:

        st.markdown(
            f"""
            <div style="
                margin:28px 0 20px;
                color:#a68b6e;
                font-size:12px;
                letter-spacing:2px;
            ">
                {len(songs)} RECORDS FOUND
            </div>
            """,
            unsafe_allow_html=True,
        )

        cols = st.columns(4)

        for index, song in enumerate(songs):

            with cols[index % 4]:
                song_card(song, index)

                st.markdown(
                    "<div style='height:20px'></div>",
                    unsafe_allow_html=True,
                )

    else:

        if st.session_state.search_keyword:

            st.markdown(
                """
                <div class="empty-box">
                    검색 결과가 없어요.<br><br>
                    다른 곡이나 아티스트 이름으로 검색해보세요.
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                """
                <div class="empty-box">

                    <div style="
                        font-family:Georgia,serif;
                        font-size:24px;
                        color:#c4a783;
                        margin-bottom:15px;
                    ">
                        FIND A RECORD
                    </div>

                    곡 제목이나 아티스트를 검색해보세요.

                </div>
                """,
                unsafe_allow_html=True,
            )


# =========================================================
# PLAYER
# =========================================================

def page_player():

    song = st.session_state.selected_song

    if not song:
        go("listen")
        return

    st.markdown(
        """
        <div class="topbar">

            <div>
                <div class="eyebrow">
                    RECORD ROOM
                </div>

                <div class="topbar-title">
                    NOW PLAYING
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "← 음악 목록으로",
        key="back_list",
    ):
        st.session_state.playing = False
        go("listen")

    st.markdown("<br>", unsafe_allow_html=True)

    left, center, right = st.columns(
        [1.3, 2, 1.3]
    )

    # -----------------------------------------------------
    # 중앙 LP
    # -----------------------------------------------------

    with center:

        spin_class = "record-spin" if st.session_state.playing else ""

        st.markdown(
            f"""
            <div class="record-wrapper">

                <div class="record {spin_class}">

                    <div class="record-label">

                        <img
                            src="{song['cover']}"
                            alt="album cover"
                        >

                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # 오른쪽 톤암
    # -----------------------------------------------------

    with right:

        st.markdown(
            """
            <div style="height:80px;"></div>

            <div class="tonearm-area">

                <div class="tonearm-base"></div>

                <div class="tonearm down">
                    <div class="needle"></div>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # 음악 정보
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="player-info">

            <div class="player-title">
                {html.escape(song["title"])}
            </div>

            <div class="player-artist">
                {html.escape(song["artist"])}
            </div>

            <div class="player-status">
                {"NOW SPINNING" if st.session_state.playing else "PAUSED"}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # 오디오
    # -----------------------------------------------------

    if song.get("preview"):

        st.audio(
            song["preview"],
            format="audio/mpeg",
        )

    # -----------------------------------------------------
    # 컨트롤
    # -----------------------------------------------------

    c1, c2, c3 = st.columns([1, 1.5, 1])

    with c2:

        if st.session_state.playing:

            if st.button(
                "Ⅱ  PAUSE RECORD",
                use_container_width=True,
            ):
                st.session_state.playing = False
                st.rerun()

        else:

            if st.button(
                "▶  PLAY RECORD",
                use_container_width=True,
            ):
                st.session_state.playing = True
                st.rerun()

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#755c44;
            font-size:11px;
            margin-top:20px;
            letter-spacing:1px;
        ">
            MUSIC PREVIEW
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# PAGE ROUTER
# =========================================================

if st.session_state.page == "home":

    page_home()

elif st.session_state.page == "choice":

    page_choice()

elif st.session_state.page == "listen":

    page_listen()

elif st.session_state.page == "player":

    page_player()

elif st.session_state.page == "recommend":

    page_recommend()

else:

    st.session_state.page = "home"
    st.rerun()
