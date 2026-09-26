import streamlit as st
import urllib.parse
import urllib.request
import json

# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="RECORD ROOM",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# 세션 상태
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "songs" not in st.session_state:
    st.session_state.songs = []

if "keyword" not in st.session_state:
    st.session_state.keyword = ""

if "selected_song" not in st.session_state:
    st.session_state.selected_song = None


# =========================================================
# 페이지 이동
# =========================================================

def move_to(page):
    st.session_state.page = page
    st.rerun()


# =========================================================
# iTunes 음악 검색
# =========================================================

@st.cache_data(ttl=600)
def search_music(keyword):
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
            },
        )

        with urllib.request.urlopen(
            request,
            timeout=10,
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        songs = []

        for item in result.get("results", []):

            preview = item.get("previewUrl")
            cover = item.get("artworkUrl100")

            if not preview or not cover:
                continue

            cover = cover.replace(
                "100x100bb",
                "600x600bb",
            )

            cover = cover.replace(
                "100x100-75",
                "600x600-75",
            )

            songs.append(
                {
                    "title": item.get(
                        "trackName",
                        "제목 없음",
                    ),
                    "artist": item.get(
                        "artistName",
                        "아티스트 없음",
                    ),
                    "album": item.get(
                        "collectionName",
                        "",
                    ),
                    "cover": cover,
                    "preview": preview,
                    "store": item.get(
                        "trackViewUrl",
                        "",
                    ),
                }
            )

        return songs

    except Exception as e:

        st.error("음악을 검색하지 못했어요.")

        st.caption(
            f"오류 내용: {e}"
        )

        return []


# =========================================================
# 홈 화면
# =========================================================

def home_page():

    st.write("")

    st.write("")

    st.caption(
        "E S T .  2 0 2 6   ·   M U S I C   &   M E M O R Y"
    )

    st.title("RECORD ROOM")

    st.markdown(
        "### 오늘의 음악을 한 장의 레코드처럼."
    )

    st.divider()

    st.write("")

    st.write("")

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        if st.button(
            "ENTER ROOM",
            use_container_width=True,
        ):
            move_to("choice")

    st.write("")

    st.caption(
        "A SMALL ROOM FOR MUSIC"
    )


# =========================================================
# 선택 화면
# =========================================================

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

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("🎵 노래듣기")

            st.write(
                "원하는 곡이나 아티스트를 검색하고 "
                "레코드 플레이어에서 들어보세요."
            )

            if st.button(
                "노래듣기",
                key="listen_button",
                use_container_width=True,
            ):
                move_to("listen")

    with col2:

        with st.container(border=True):

            st.subheader("🎧 노래 추천받기")

            st.write(
                "나중에 취향을 바탕으로 "
                "음악을 추천받을 수 있어요."
            )

            if st.button(
                "노래 추천받기",
                key="recommend_button",
                use_container_width=True,
            ):
                move_to("recommend")

    st.write("")

    if st.button(
        "← 처음 화면으로",
        key="home_back",
    ):
        move_to("home")


# =========================================================
# 음악 검색 화면
# =========================================================

def listen_page():

    st.caption(
        "R E C O R D   R O O M   /   M U S I C"
    )

    st.title("MUSIC ROOM")

    st.write(
        "곡명이나 아티스트를 검색해보세요."
    )

    st.divider()

    # 뒤로가기
    if st.button(
        "← 선택 화면으로",
        key="music_back",
    ):
        move_to("choice")

    st.write("")

    # 검색창
    with st.form("music_search_form"):

        keyword = st.text_input(
            "검색",
            value=st.session_state.keyword,
            placeholder="예: 아이유, Oasis, 실리카겔",
            label_visibility="collapsed",
        )

        search_button = st.form_submit_button(
            "SEARCH",
            use_container_width=True,
        )

    if search_button:

        keyword = keyword.strip()

        st.session_state.keyword = keyword

        if keyword:

            with st.spinner(
                "레코드를 찾고 있어요..."
            ):

                st.session_state.songs = search_music(
                    keyword
                )

        else:

            st.session_state.songs = []

    songs = st.session_state.songs

    st.write("")

    # 검색 결과
    if songs:

        st.caption(
            f"{len(songs)}개의 레코드를 찾았어요."
        )

        st.write("")

        columns = st.columns(4)

        for index, song in enumerate(songs):

            with columns[index % 4]:

                with st.container(
                    border=True
                ):

                    # 앨범 커버
                    st.image(
                        song["cover"],
                        use_container_width=True,
                    )

                    st.subheader(
                        song["title"]
                    )

                    st.caption(
                        song["artist"]
                    )

                    if song["album"]:

                        st.caption(
                            song["album"]
                        )

                    st.write("")

                    if st.button(
                        "💿 레코드에 올리기",
                        key=f"select_{index}",
                        use_container_width=True,
                    ):

                        st.session_state.selected_song = song

                        move_to("player")

    elif st.session_state.keyword:

        st.warning(
            "검색 결과가 없어요. "
            "다른 곡이나 아티스트를 검색해보세요."
        )

    else:

        st.info(
            "위 검색창에서 음악을 검색해보세요."
        )


# =========================================================
# 플레이어 화면
# =========================================================

def player_page():

    song = st.session_state.selected_song

    if song is None:

        move_to("listen")
        return

    st.caption(
        "R E C O R D   R O O M   /   N O W   P L A Y I N G"
    )

    st.title("NOW PLAYING")

    st.divider()

    if st.button(
        "← 음악 목록으로",
        key="player_back",
    ):

        move_to("listen")

    st.write("")

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        # LP 느낌의 화면
        st.markdown(
            """
            # 💿
            """
        )

        st.image(
            song["cover"],
            width=280,
        )

    st.write("")

    st.markdown(
        f"## {song['title']}"
    )

    st.write(
        f"**{song['artist']}**"
    )

    if song["album"]:

        st.caption(
            song["album"]
        )

    st.divider()

    # 음악 재생
    st.subheader(
        "TURN THE RECORD"
    )

    st.audio(
        song["preview"],
        format="audio/mpeg",
    )

    st.caption(
        "현재 제공되는 음원은 미리듣기입니다."
    )

    st.write("")

    # 다른 곡 선택
    if st.button(
        "다른 레코드 고르기",
        use_container_width=True,
    ):

        move_to("listen")


# =========================================================
# 추천 화면
# =========================================================

def recommend_page():

    st.caption(
        "R E C O R D   R O O M   /   R E C O M M E N D"
    )

    st.title(
        "MUSIC RECOMMEND"
    )

    st.write(
        "취향 기반 음악 추천 기능을 준비 중이에요."
    )

    st.divider()

    st.info(
        "먼저 음악 검색과 레코드 플레이어를 완성한 뒤 "
        "추천 기능을 추가할 수 있어요."
    )

    st.write("")

    if st.button(
        "← 선택 화면으로",
        use_container_width=True,
    ):

        move_to("choice")


# =========================================================
# 실행
# =========================================================

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
