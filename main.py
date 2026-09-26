import streamlit as st
import urllib.parse
import urllib.request
import json
import io
import random
import math

from PIL import Image, ImageDraw, ImageFont


# =========================================================
# 기본 설정
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

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "selected_song" not in st.session_state:
    st.session_state.selected_song = None

if "is_playing" not in st.session_state:
    st.session_state.is_playing = False


# =========================================================
# 색상
# =========================================================

WOOD_DARK = "#24170F"
WOOD = "#3A2417"
WOOD_LIGHT = "#65432C"
CREAM = "#F4E7CF"
CREAM_DARK = "#D9C19D"
GOLD = "#B68A4A"
BROWN = "#754C2D"
BLACK = "#111111"
WHITE = "#FFFFFF"


# =========================================================
# Python으로만 만드는 기본 디자인
# =========================================================

st.markdown(
    """
    # 🎵 RECORD ROOM
    """
)

st.caption("오늘의 음악을 한 장의 레코드처럼.")


# =========================================================
# iTunes API
# =========================================================

@st.cache_data(ttl=600)
def request_json(url):
    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = response.read().decode("utf-8")

        return json.loads(data)

    except Exception:
        return None


@st.cache_data(ttl=600)
def search_songs(keyword):
    """
    노래 제목 / 가수 이름 모두 검색
    """

    keyword = keyword.strip()

    if not keyword:
        return []

    encoded = urllib.parse.quote(keyword)

    url = (
        "https://itunes.apple.com/search?"
        f"term={encoded}"
        "&country=KR"
        "&media=music"
        "&entity=song"
        "&limit=30"
    )

    data = request_json(url)

    if not data:
        return []

    results = data.get("results", [])

    songs = []

    for item in results:

        track_name = item.get("trackName")
        artist_name = item.get("artistName")

        if not track_name or not artist_name:
            continue

        song = {
            "track_name": track_name,
            "artist_name": artist_name,
            "album_name": item.get(
                "collectionName",
                "Unknown Album"
            ),
            "artwork": item.get(
                "artworkUrl100",
                ""
            ).replace(
                "100x100",
                "600x600"
            ),
            "preview": item.get(
                "previewUrl",
                ""
            ),
            "track_url": item.get(
                "trackViewUrl",
                ""
            ),
            "artist_id": item.get(
                "artistId"
            ),
        }

        songs.append(song)

    return songs


@st.cache_data(ttl=600)
def search_artist(keyword):
    """
    검색 결과가 없을 때 가수 자체를 찾아서
    해당 가수의 곡을 가져오는 보조 검색
    """

    keyword = keyword.strip()

    if not keyword:
        return []

    encoded = urllib.parse.quote(keyword)

    url = (
        "https://itunes.apple.com/search?"
        f"term={encoded}"
        "&country=KR"
        "&media=music"
        "&entity=musicArtist"
        "&limit=10"
    )

    data = request_json(url)

    if not data:
        return []

    artists = data.get("results", [])

    for artist in artists:

        artist_id = artist.get("artistId")

        if not artist_id:
            continue

        songs_url = (
            "https://itunes.apple.com/lookup?"
            f"id={artist_id}"
            "&entity=song"
            "&country=KR"
            "&limit=30"
        )

        songs_data = request_json(songs_url)

        if not songs_data:
            continue

        songs = []

        for item in songs_data.get("results", []):

            if item.get("wrapperType") != "track":
                continue

            if item.get("kind") != "song":
                continue

            track_name = item.get("trackName")

            if not track_name:
                continue

            songs.append(
                {
                    "track_name": track_name,
                    "artist_name": item.get(
                        "artistName",
                        artist.get(
                            "artistName",
                            keyword
                        )
                    ),
                    "album_name": item.get(
                        "collectionName",
                        "Unknown Album"
                    ),
                    "artwork": item.get(
                        "artworkUrl100",
                        ""
                    ).replace(
                        "100x100",
                        "600x600"
                    ),
                    "preview": item.get(
                        "previewUrl",
                        ""
                    ),
                    "track_url": item.get(
                        "trackViewUrl",
                        ""
                    ),
                    "artist_id": artist_id,
                }
            )

        if songs:
            return songs

    return []


def search_music(keyword):

    keyword = keyword.strip()

    if not keyword:
        return []

    # 1차: 노래 검색
    results = search_songs(keyword)

    if results:
        return results

    # 2차: 가수 검색
    results = search_artist(keyword)

    if results:
        return results

    return []


# =========================================================
# 폰트
# =========================================================

def get_font(size, bold=False):

    paths = []

    if bold:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass

    return ImageFont.load_default()


# =========================================================
# 레코드판 이미지
# =========================================================

@st.cache_data
def create_vinyl_image(size=650):

    image = Image.new(
        "RGB",
        (size, size),
        (36, 23, 15)
    )

    draw = ImageDraw.Draw(image)

    center = size // 2

    # 바깥쪽 그림자
    draw.ellipse(
        (
            15,
            15,
            size - 15,
            size - 15
        ),
        fill=(12, 10, 9)
    )

    # 레코드판
    draw.ellipse(
        (
            25,
            25,
            size - 25,
            size - 25
        ),
        fill=(18, 18, 18),
        outline=(70, 70, 70),
        width=2
    )

    # 레코드 홈
    for r in range(
        int(size * 0.43),
        int(size * 0.95),
        13
    ):

        box = (
            center - r,
            center - r,
            center + r,
            center + r
        )

        draw.ellipse(
            box,
            outline=(35, 35, 35),
            width=1
        )

    # 중앙 라벨
    label_radius = int(size * 0.15)

    draw.ellipse(
        (
            center - label_radius,
            center - label_radius,
            center + label_radius,
            center + label_radius
        ),
        fill=(137, 89, 46),
        outline=(190, 143, 84),
        width=3
    )

    # 중앙 구멍
    hole = 13

    draw.ellipse(
        (
            center - hole,
            center - hole,
            center + hole,
            center + hole
        ),
        fill=(12, 12, 12)
    )

    return image


# =========================================================
# 앨범 커버가 들어간 레코드판
# =========================================================

@st.cache_data
def create_record_with_cover(cover_url, size=650):

    record = create_vinyl_image(size).copy()

    if cover_url:

        try:

            request = urllib.request.Request(
                cover_url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=10
            ) as response:

                data = response.read()

            cover = Image.open(
                io.BytesIO(data)
            ).convert("RGB")

            cover_size = int(size * 0.27)

            cover = cover.resize(
                (
                    cover_size,
                    cover_size
                )
            )

            x = (
                size - cover_size
            ) // 2

            y = (
                size - cover_size
            ) // 2

            record.paste(
                cover,
                (x, y)
            )

        except Exception:
            pass

    return record


# =========================================================
# 홈 화면
# =========================================================

def show_home():

    st.write("")
    st.write("")
    st.write("")

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.markdown(
            "## 🎵 RECORD ROOM"
        )

        st.write(
            "오늘의 음악을 한 장의 레코드처럼."
        )

        st.write("")

        if st.button(
            "ENTER ROOM",
            use_container_width=True
        ):
            st.session_state.page = "choice"
            st.rerun()

        st.write("")
        st.caption(
            "A little room for your favorite music."
        )


# =========================================================
# 선택 화면
# =========================================================

def show_choice():

    st.subheader("RECORD ROOM")

    st.write(
        "무엇을 할까요?"
    )

    st.write("")

    left, right = st.columns(2)

    with left:

        if st.button(
            "🎧 노래듣기",
            use_container_width=True
        ):

            st.session_state.page = "listen"
            st.rerun()

    with right:

        if st.button(
            "💿 노래 추천받기",
            use_container_width=True
        ):

            st.session_state.page = "recommend"
            st.rerun()

    st.write("")

    if st.button(
        "← 처음으로"
    ):

        st.session_state.page = "home"
        st.rerun()


# =========================================================
# 검색 화면
# =========================================================

def show_listen():

    st.subheader("🎧 MUSIC LIBRARY")

    st.write(
        "가수 이름이나 노래 제목을 검색해보세요."
    )

    st.write("")

    # form을 사용해서 검색창에서 엔터를 눌러도 검색되게 함
    with st.form(
        "music_search_form"
    ):

        query = st.text_input(
            "검색",
            value=st.session_state.search_query,
            placeholder="예: 아이유 / 뉴진스 / 지코 / Love wins all",
            label_visibility="collapsed"
        )

        search_button = st.form_submit_button(
            "🔎 SEARCH",
            use_container_width=True
        )

    if search_button:

        query = query.strip()

        st.session_state.search_query = query

        if not query:

            st.session_state.search_results = []

            st.warning(
                "검색어를 입력해주세요."
            )

        else:

            with st.spinner(
                f"'{query}' 검색 중..."
            ):

                results = search_music(query)

            st.session_state.search_results = results

    results = st.session_state.search_results

    st.write("")

    # 검색 결과가 없는 최초 화면
    if not results:

        if st.session_state.search_query:

            st.info(
                f"'{st.session_state.search_query}'에 대한 검색 결과가 없습니다."
            )

            st.write(
                "다른 가수 이름이나 노래 제목으로 검색해보세요."
            )

        else:

            st.write("")
            st.write("")
            st.write("🎵")
            st.subheader(
                "검색해서 나만의 레코드를 찾아보세요."
            )

            st.write(
                "가수 이름 또는 노래 제목을 입력하면 "
                "음악 정보를 가져옵니다."
            )

        st.write("")

    else:

        st.success(
            f"검색 결과 {len(results)}개"
        )

        st.write("")

        # 한 줄에 3개
        for start in range(
            0,
            len(results),
            3
        ):

            row = results[
                start:start + 3
            ]

            columns = st.columns(
                len(row)
            )

            for col, song in zip(
                columns,
                row
            ):

                with col:

                    if song["artwork"]:

                        st.image(
                            song["artwork"],
                            use_container_width=True
                        )

                    st.write(
                        f"**{song['track_name']}**"
                    )

                    st.caption(
                        song["artist_name"]
                    )

                    st.caption(
                        song["album_name"]
                    )

                    if st.button(
                        "💿 레코드에 올리기",
                        key=f"select_{start}_{song['track_name']}_{song['artist_name']}",
                        use_container_width=True
                    ):

                        st.session_state.selected_song = song
                        st.session_state.is_playing = True
                        st.session_state.page = "player"

                        st.rerun()

                    st.write("")

    st.divider()

    if st.button(
        "← 메뉴로 돌아가기"
    ):

        st.session_state.page = "choice"
        st.session_state.search_results = []
        st.session_state.search_query = ""

        st.rerun()


# =========================================================
# 플레이어 화면
# =========================================================

def show_player():

    song = st.session_state.selected_song

    if not song:

        st.session_state.page = "listen"
        st.rerun()
        return

    st.subheader("💿 RECORD PLAYER")

    st.write("")

    left, right = st.columns(
        [1.25, 1]
    )

    # -----------------------------------------------------
    # 왼쪽 : 레코드
    # -----------------------------------------------------

    with left:

        record_image = create_record_with_cover(
            song.get("artwork", "")
        )

        st.image(
            record_image,
            use_container_width=True
        )

    # -----------------------------------------------------
    # 오른쪽 : 음악 정보
    # -----------------------------------------------------

    with right:

        st.write("")
        st.write("")

        st.caption("NOW PLAYING")

        st.title(
            song["track_name"]
        )

        st.subheader(
            song["artist_name"]
        )

        st.write(
            song["album_name"]
        )

        st.write("")

        st.divider()

        if song.get("preview"):

            st.write(
                "🎵 30초 미리듣기"
            )

            st.audio(
                song["preview"],
                format="audio/mp4",
                start_time=0
            )

        else:

            st.warning(
                "이 곡은 미리듣기를 제공하지 않습니다."
            )

        st.write("")

        if st.button(
            "⏹ 재생 중지",
            use_container_width=True
        ):

            st.session_state.is_playing = False

            st.session_state.selected_song = None

            st.session_state.page = "listen"

            st.rerun()

        st.write("")

        if st.button(
            "← 음악 목록으로",
            use_container_width=True
        ):

            st.session_state.is_playing = False

            st.session_state.selected_song = None

            st.session_state.page = "listen"

            st.rerun()


# =========================================================
# 추천 화면
# =========================================================

def show_recommend():

    st.subheader(
        "💿 MUSIC RECOMMENDATION"
    )

    st.write(
        "오늘 듣고 싶은 분위기를 골라보세요."
    )

    st.write("")

    moods = {
        "🌙 새벽 감성": [
            "아이유",
            "검정치마",
            "실리카겔",
        ],
        "☀️ 기분 좋은 날": [
            "뉴진스",
            "AKMU",
            "볼빨간사춘기",
        ],
        "🖤 힙합": [
            "지코",
            "크러쉬",
            "빈지노",
        ],
        "💗 설레는 날": [
            "아이유",
            "DAY6",
            "AKMU",
        ],
    }

    mood_names = list(
        moods.keys()
    )

    for i in range(
        0,
        len(mood_names),
        2
    ):

        columns = st.columns(2)

        for col, mood in zip(
            columns,
            mood_names[i:i + 2]
        ):

            with col:

                if st.button(
                    mood,
                    key=f"mood_{mood}",
                    use_container_width=True
                ):

                    artist = random.choice(
                        moods[mood]
                    )

                    with st.spinner(
                        f"{artist} 검색 중..."
                    ):

                        results = search_music(
                            artist
                        )

                    if results:

                        song = random.choice(
                            results
                        )

                        st.session_state.selected_song = song
                        st.session_state.page = "player"

                        st.rerun()

                    else:

                        st.error(
                            "추천 음악을 불러오지 못했습니다."
                        )

    st.write("")

    st.divider()

    if st.button(
        "← 메뉴로 돌아가기"
    ):

        st.session_state.page = "choice"
        st.rerun()


# =========================================================
# 페이지 실행
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
