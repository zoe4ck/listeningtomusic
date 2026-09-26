import streamlit as st
import urllib.parse
import urllib.request
import json
import time

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="RECORD ROOM",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "songs" not in st.session_state:
    st.session_state.songs = []

if "search_word" not in st.session_state:
    st.session_state.search_word = ""

if "selected_song" not in st.session_state:
    st.session_state.selected_song = None


# ============================================================
# NAVIGATION
# ============================================================

def go(page):
    st.session_state.page = page
    st.rerun()


# ============================================================
# MUSIC API
# ============================================================

@st.cache_data(ttl=600)
def request_itunes(term, country):
    """
    Apple iTunes Search API 호출
    """

    params = urllib.parse.urlencode(
        {
            "term": term,
            "country": country,
            "media": "music",
            "entity": "song",
            "limit": 50,
            "lang": "ko_kr",
            "explicit": "Yes",
        }
    )

    url = "https://itunes.apple.com/search?" + params

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
    )

    with urllib.request.urlopen(
        request,
        timeout=15,
    ) as response:

        raw = response.read()

    return json.loads(
        raw.decode("utf-8")
    )


@st.cache_data(ttl=600)
def search_music(term):
    """
    검색 안정성을 위해
    1. 한국 스토어
    2. 미국 스토어
    순서로 검색.
    """

    term = term.strip()

    if not term:
        return [], None

    all_results = []

    countries = ["KR", "US"]

    for country in countries:

        try:

            data = request_itunes(
                term,
                country
            )

            results = data.get(
                "results",
                []
            )

            if results:
                all_results.extend(
                    results
                )

        except Exception:
            continue

    # --------------------------------------------------------
    # 중복 제거
    # --------------------------------------------------------

    unique = {}

    for item in all_results:

        track_id = item.get(
            "trackId"
        )

        # trackId가 없는 경우
        # 제목+아티스트를 키로 사용
        if track_id is None:

            track_id = (
                item.get("trackName", ""),
                item.get("artistName", ""),
            )

        if track_id not in unique:
            unique[track_id] = item

    # --------------------------------------------------------
    # 우리 앱에서 사용할 형식으로 정리
    # --------------------------------------------------------

    songs = []

    for item in unique.values():

        title = item.get("trackName")
        artist = item.get("artistName")
        album = item.get("collectionName")
        cover = item.get("artworkUrl100")
        preview = item.get("previewUrl")

        # 제목이나 아티스트가 실제로 없는 데이터만 제외
        if not title:
            continue

        if not artist:
            continue

        # 커버가 있으면 큰 이미지로 변경
        if cover:

            cover = cover.replace(
                "100x100bb",
                "600x600bb"
            )

            cover = cover.replace(
                "100x100-75",
                "600x600-75"
            )

        songs.append(
            {
                "id": item.get(
                    "trackId",
                    time.time()
                ),

                "title": title,

                "artist": artist,

                "album": album or "Single",

                "cover": cover,

                "preview": preview,

                "store_url": item.get(
                    "trackViewUrl",
                    ""
                ),

                "genre": item.get(
                    "primaryGenreName",
                    ""
                ),
            }
        )

    # --------------------------------------------------------
    # 같은 곡 중복 제거
    # --------------------------------------------------------

    final_songs = []

    seen = set()

    for song in songs:

        key = (
            song["title"].lower(),
            song["artist"].lower(),
        )

        if key in seen:
            continue

        seen.add(key)

        final_songs.append(song)

    return final_songs, None


# ============================================================
# HOME
# ============================================================

def home_page():

    st.write("")
    st.write("")
    st.write("")

    # 상단 작은 문구
    st.caption(
        "E S T . 2 0 2 6   ·   M U S I C & M E M O R Y"
    )

    st.write("")

    # 메인 타이틀
    st.title(
        "🎵 RECORD ROOM"
    )

    st.subheader(
        "오늘의 음악을 한 장의 레코드처럼."
    )

    st.write("")

    st.divider()

    st.write("")

    # 장식
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "ROOM",
            "01"
        )

    with c2:
        st.metric(
            "MOOD",
            "VINYL"
        )

    with c3:
        st.metric(
            "MUSIC",
            "∞"
        )

    with c4:
        st.metric(
            "YEAR",
            "2026"
        )

    with c5:
        st.metric(
            "STATUS",
            "OPEN"
        )

    st.write("")
    st.write("")
    st.write("")

    # Enter 버튼
    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        if st.button(
            "ENTER ROOM  →",
            key="enter_room",
            use_container_width=True,
        ):
            go("choice")

    st.write("")
    st.write("")

    st.caption(
        "A SMALL ROOM FOR MUSIC"
    )


# ============================================================
# CHOICE
# ============================================================

def choice_page():

    st.caption(
        "R E C O R D   R O O M"
    )

    st.title(
        "What would you like?"
    )

    st.write(
        "오늘은 어떤 음악을 만나볼까요?"
    )

    st.divider()

    st.write("")

    left, right = st.columns(
        2,
        gap="large"
    )

    # --------------------------------------------------------
    # 노래듣기
    # --------------------------------------------------------

    with left:

        with st.container(
            border=True
        ):

            st.subheader(
                "💿 노래듣기"
            )

            st.write(
                "원하는 가수나 곡을 검색하고 "
                "레코드처럼 음악을 들어보세요."
            )

            st.write("")

            if st.button(
                "MUSIC ROOM  →",
                key="go_music",
                use_container_width=True,
            ):
                go("listen")

    # --------------------------------------------------------
    # 추천
    # --------------------------------------------------------

    with right:

        with st.container(
            border=True
        ):

            st.subheader(
                "🎧 노래 추천받기"
            )

            st.write(
                "나중에 취향에 맞는 음악을 "
                "추천받을 수 있도록 확장할 수 있어요."
            )

            st.write("")

            if st.button(
                "RECOMMEND  →",
                key="go_recommend",
                use_container_width=True,
            ):
                go("recommend")

    st.write("")
    st.write("")

    if st.button(
        "← HOME",
        key="choice_home",
    ):
        go("home")


# ============================================================
# LISTEN
# ============================================================

def listen_page():

    st.caption(
        "R E C O R D   R O O M   /   M U S I C"
    )

    st.title(
        "MUSIC ROOM"
    )

    st.write(
        "가수 이름이나 곡 제목을 검색해보세요."
    )

    st.divider()

    if st.button(
        "← CHOICE",
        key="listen_back",
    ):
        go("choice")

    st.write("")

    # ========================================================
    # SEARCH
    # ========================================================

    with st.form(
        "search_form",
        clear_on_submit=False
    ):

        search_col, button_col = st.columns(
            [5, 1]
        )

        with search_col:

            keyword = st.text_input(
                "music search",
                value=st.session_state.search_word,
                placeholder="예: 아이유 / Oasis / 실리카겔 / Bruno Mars",
                label_visibility="collapsed",
            )

        with button_col:

            search_pressed = st.form_submit_button(
                "SEARCH",
                use_container_width=True,
            )

    if search_pressed:

        keyword = keyword.strip()

        st.session_state.search_word = keyword

        if not keyword:

            st.session_state.songs = []

            st.warning(
                "검색어를 입력해주세요."
            )

        else:

            with st.spinner(
                f"'{keyword}' 레코드를 찾는 중..."
            ):

                songs, error = search_music(
                    keyword
                )

            st.session_state.songs = songs

            if not songs:

                st.error(
                    f"'{keyword}'에 해당하는 음악을 찾지 못했어요."
                )

                st.caption(
                    "한국 스토어와 미국 스토어를 모두 검색했습니다."
                )

    # ========================================================
    # RESULTS
    # ========================================================

    songs = st.session_state.songs

    if songs:

        st.write("")

        st.subheader(
            f"SEARCH RESULTS  ·  {len(songs)}"
        )

        st.caption(
            f"'{st.session_state.search_word}' 검색 결과"
        )

        st.write("")

        # ----------------------------------------------------
        # 최대 24개 먼저 표시
        # ----------------------------------------------------

        visible_songs = songs[:24]

        columns = st.columns(
            4,
            gap="medium"
        )

        for index, song in enumerate(
            visible_songs
        ):

            with columns[index % 4]:

                with st.container(
                    border=True
                ):

                    # 커버
                    if song["cover"]:

                        st.image(
                            song["cover"],
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "앨범 커버 없음"
                        )

                    st.write("")

                    # 제목
                    st.markdown(
                        f"**{song['title']}**"
                    )

                    # 아티스트
                    st.write(
                        f"🎤 {song['artist']}"
                    )

                    # 앨범
                    if song["album"]:

                        st.caption(
                            song["album"]
                        )

                    # 장르
                    if song["genre"]:

                        st.caption(
                            song["genre"]
                        )

                    st.write("")

                    if st.button(
                        "💿 이 레코드 듣기",
                        key=f"song_{song['id']}_{index}",
                        use_container_width=True,
                    ):

                        st.session_state.selected_song = song

                        go("player")

                    # 미리듣기 가능 여부
                    if song["preview"]:

                        st.caption(
                            "30초 미리듣기 가능"
                        )

                    else:

                        st.caption(
                            "미리듣기 없음"
                        )

        # ----------------------------------------------------
        # 더 많은 결과
        # ----------------------------------------------------

        if len(songs) > 24:

            st.info(
                f"검색 결과가 {len(songs)}개 있습니다. "
                "현재 상위 24개를 표시하고 있어요."
            )

    elif not st.session_state.search_word:

        st.write("")

        st.info(
            "🔎 위 검색창에서 원하는 가수나 곡을 검색해보세요."
        )

        st.write("")

        st.subheader(
            "QUICK SEARCH"
        )

        st.caption(
            "버튼을 누르면 바로 검색됩니다."
        )

        st.write("")

        quick = [
            "아이유",
            "실리카겔",
            "Oasis",
            "Bruno Mars",
            "NewJeans",
            "ZICO",
        ]

        quick_cols = st.columns(
            3
        )

        for index, artist in enumerate(
            quick
        ):

            with quick_cols[
                index % 3
            ]:

                if st.button(
                    artist,
                    key=f"quick_{artist}",
                    use_container_width=True,
                ):

                    st.session_state.search_word = artist

                    with st.spinner(
                        "검색 중..."
                    ):

                        result, error = search_music(
                            artist
                        )

                    st.session_state.songs = result

                    st.rerun()


# ============================================================
# PLAYER
# ============================================================

def player_page():

    song = st.session_state.selected_song

    if not song:

        go("listen")
        return

    st.caption(
        "R E C O R D   R O O M   /   N O W   P L A Y I N G"
    )

    st.title(
        "NOW PLAYING"
    )

    st.divider()

    if st.button(
        "← MUSIC ROOM",
        key="player_back",
    ):
        go("listen")

    st.write("")
    st.write("")

    # ========================================================
    # PLAYER LAYOUT
    # ========================================================

    left, middle, right = st.columns(
        [1, 2, 1]
    )

    # --------------------------------------------------------
    # 왼쪽 정보
    # --------------------------------------------------------

    with left:

        st.subheader(
            "RECORD"
        )

        st.write(
            "NOW SPINNING"
        )

        st.metric(
            "FORMAT",
            "VINYL"
        )

        if song["genre"]:

            st.metric(
                "GENRE",
                song["genre"]
            )

    # --------------------------------------------------------
    # 가운데 LP
    # --------------------------------------------------------

    with middle:

        st.markdown(
            """
            ## ◎ ◎ ◎
            """
        )

        if song["cover"]:

            st.image(
                song["cover"],
                width=320
            )

        st.markdown(
            """
            ### ◉
            """
        )

    # --------------------------------------------------------
    # 오른쪽 정보
    # --------------------------------------------------------

    with right:

        st.subheader(
            "TRACK INFO"
        )

        st.write(
            f"**{song['title']}**"
        )

        st.write(
            f"🎤 {song['artist']}"
        )

        st.caption(
            song["album"]
        )

    st.divider()

    # ========================================================
    # AUDIO
    # ========================================================

    st.subheader(
        "♫ LISTEN"
    )

    if song["preview"]:

        st.audio(
            song["preview"],
            format="audio/mpeg"
        )

        st.caption(
            "Apple Music Search API에서 제공하는 30초 미리듣기입니다."
        )

    else:

        st.warning(
            "이 곡은 미리듣기를 제공하지 않습니다."
        )

    st.write("")

    # ========================================================
    # STORE
    # ========================================================

    if song["store_url"]:

        st.link_button(
            "Apple Music / iTunes에서 보기 →",
            song["store_url"],
            use_container_width=True,
        )

    st.write("")
    st.write("")

    col1, col2 = st.columns(
        2
    )

    with col1:

        if st.button(
            "다른 레코드 고르기",
            use_container_width=True,
        ):

            go("listen")

    with col2:

        if st.button(
            "처음으로",
            use_container_width=True,
        ):

            go("home")


# ============================================================
# RECOMMEND
# ============================================================

def recommend_page():

    st.caption(
        "R E C O R D   R O O M   /   R E C O M M E N D"
    )

    st.title(
        "MUSIC RECOMMEND"
    )

    st.write(
        "추천 기능을 위한 공간입니다."
    )

    st.divider()

    st.info(
        "현재는 음악 검색과 미리듣기 기능을 먼저 구현한 상태예요."
    )

    st.write("")

    st.subheader(
        "COMING SOON"
    )

    st.write(
        "좋아하는 가수, 장르, 분위기 등을 선택하면 "
        "그에 맞는 음악을 보여주는 방식으로 확장할 수 있습니다."
    )

    st.write("")
    st.write("")

    if st.button(
        "← CHOICE",
        use_container_width=True,
    ):

        go("choice")


# ============================================================
# ROUTER
# ============================================================

if st.session_state.page == "home":

    home_page()

elif st.session_state.page == "choice":

    choice_page()

elif st.session_state.page == "listen":

    listen_page()

elif st.session_state.page == "player":

    player_page()

elif st.session_state.page == "recommend":

    recommend_page()

else:

    st.session_state.page = "home"

    st.rerun()
