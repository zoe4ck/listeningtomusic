import streamlit as st
import urllib.parse
import urllib.request
import json
import io
import math

from PIL import Image, ImageDraw, ImageFilter


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="RECORD ROOM",
    page_icon="♫",
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
# BASIC DESIGN
# ============================================================

def room_title(kicker, title, description=""):
    st.write("")

    st.caption(
        kicker.upper()
    )

    st.title(
        title
    )

    if description:
        st.write(
            description
        )

    st.divider()


def wood_panel():
    """
    Streamlit 기본 container를 이용한
    빈티지 패널 느낌의 구분용 영역
    """
    return st.container(
        border=True
    )


# ============================================================
# LP IMAGE GENERATOR
# ============================================================

@st.cache_data(max_entries=100)
def make_record_image(
    cover_url,
    size=720
):
    """
    실제 앨범 커버를 LP 중앙 라벨에 넣어서
    레코드판 이미지를 Python/PIL로 생성한다.
    """

    # --------------------------------------------------------
    # 배경
    # --------------------------------------------------------

    image = Image.new(
        "RGB",
        (size, size),
        (22, 18, 15)
    )

    draw = ImageDraw.Draw(
        image
    )

    center = size // 2

    # --------------------------------------------------------
    # LP 바깥 그림자
    # --------------------------------------------------------

    shadow = Image.new(
        "RGBA",
        (size, size),
        (0, 0, 0, 0)
    )

    shadow_draw = ImageDraw.Draw(
        shadow
    )

    shadow_draw.ellipse(
        (
            45,
            50,
            size - 25,
            size - 20
        ),
        fill=(0, 0, 0, 180)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(22)
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        shadow
    )

    draw = ImageDraw.Draw(
        image
    )

    # --------------------------------------------------------
    # LP 본체
    # --------------------------------------------------------

    margin = 45

    draw.ellipse(
        (
            margin,
            margin,
            size - margin,
            size - margin
        ),
        fill=(9, 9, 9),
        outline=(45, 45, 45),
        width=4
    )

    # --------------------------------------------------------
    # LP 그루브
    # --------------------------------------------------------

    for r in range(
        int(size * 0.09),
        int(size * 0.43),
        9
    ):

        box = (
            center - r,
            center - r,
            center + r,
            center + r
        )

        draw.ellipse(
            box,
            outline=(27, 27, 27),
            width=2
        )

    # --------------------------------------------------------
    # 빛 반사
    # --------------------------------------------------------

    highlight = Image.new(
        "RGBA",
        (size, size),
        (0, 0, 0, 0)
    )

    hd = ImageDraw.Draw(
        highlight
    )

    hd.arc(
        (
            margin + 35,
            margin + 35,
            size - margin - 35,
            size - margin - 35
        ),
        205,
        320,
        fill=(100, 100, 100, 45),
        width=8
    )

    image = Image.alpha_composite(
        image,
        highlight
    )

    draw = ImageDraw.Draw(
        image
    )

    # --------------------------------------------------------
    # 앨범 커버
    # --------------------------------------------------------

    try:

        if cover_url:

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

                cover_bytes = response.read()

            cover = Image.open(
                io.BytesIO(cover_bytes)
            ).convert("RGB")

            label_size = 235

            cover.thumbnail(
                (
                    label_size,
                    label_size
                ),
                Image.Resampling.LANCZOS
            )

            # 정사각형 캔버스
            label = Image.new(
                "RGB",
                (
                    label_size,
                    label_size
                ),
                (80, 50, 30)
            )

            x = (
                label_size -
                cover.width
            ) // 2

            y = (
                label_size -
                cover.height
            ) // 2

            label.paste(
                cover,
                (x, y)
            )

            # 원형 마스크
            mask = Image.new(
                "L",
                (
                    label_size,
                    label_size
                ),
                0
            )

            md = ImageDraw.Draw(
                mask
            )

            md.ellipse(
                (
                    0,
                    0,
                    label_size - 1,
                    label_size - 1
                ),
                fill=255
            )

            label_rgba = label.convert(
                "RGBA"
            )

            label_rgba.putalpha(
                mask
            )

            label_x = (
                center -
                label_size // 2
            )

            label_y = (
                center -
                label_size // 2
            )

            image.alpha_composite(
                label_rgba,
                (
                    label_x,
                    label_y
                )
            )

    except Exception:

        # 앨범 커버를 못 가져와도
        # LP 자체는 반드시 표시
        draw = ImageDraw.Draw(
            image
        )

        draw.ellipse(
            (
                center - 120,
                center - 120,
                center + 120,
                center + 120
            ),
            fill=(54, 37, 25),
            outline=(126, 91, 57),
            width=4
        )

    # --------------------------------------------------------
    # 중앙 구멍
    # --------------------------------------------------------

    draw = ImageDraw.Draw(
        image
    )

    draw.ellipse(
        (
            center - 12,
            center - 12,
            center + 12,
            center + 12
        ),
        fill=(205, 178, 132)
    )

    draw.ellipse(
        (
            center - 4,
            center - 4,
            center + 4,
            center + 4
        ),
        fill=(20, 17, 14)
    )

    return image.convert("RGB")


# ============================================================
# TURNTABLE IMAGE
# ============================================================

@st.cache_data
def make_turntable():
    """
    LP 플레이어 자체를 Python으로 만든다.
    """

    width = 1000
    height = 420

    img = Image.new(
        "RGB",
        (width, height),
        (48, 29, 18)
    )

    draw = ImageDraw.Draw(
        img
    )

    # --------------------------------------------------------
    # 나무 패널
    # --------------------------------------------------------

    for y in range(
        0,
        height,
        8
    ):

        shade = 45 + int(
            10 * math.sin(y / 35)
        )

        draw.line(
            (
                0,
                y,
                width,
                y
            ),
            fill=(
                shade + 12,
                shade,
                max(10, shade - 12)
            ),
            width=3
        )

    # --------------------------------------------------------
    # 테이블
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            70,
            55,
            930,
            365
        ),
        radius=25,
        fill=(35, 23, 16),
        outline=(139, 99, 63),
        width=3
    )

    # --------------------------------------------------------
    # 왼쪽 컨트롤
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            105,
            105,
            275,
            315
        ),
        radius=15,
        fill=(25, 20, 17),
        outline=(94, 70, 48),
        width=2
    )

    draw.ellipse(
        (
            155,
            145,
            225,
            215
        ),
        fill=(13, 13, 13),
        outline=(151, 112, 76),
        width=3
    )

    draw.rectangle(
        (
            140,
            240,
            240,
            260
        ),
        fill=(126, 92, 61)
    )

    # --------------------------------------------------------
    # LP 받침
    # --------------------------------------------------------

    draw.ellipse(
        (
            330,
            75,
            725,
            360
        ),
        fill=(15, 15, 15),
        outline=(91, 91, 91),
        width=5
    )

    # 그루브
    for r in range(
        55,
        145,
        11
    ):

        draw.ellipse(
            (
                527 - r,
                217 - r,
                527 + r,
                217 + r
            ),
            outline=(36, 36, 36),
            width=2
        )

    draw.ellipse(
        (
            515,
            205,
            539,
            229
        ),
        fill=(190, 156, 111)
    )

    # --------------------------------------------------------
    # 톤암
    # --------------------------------------------------------

    draw.ellipse(
        (
            790,
            90,
            850,
            150
        ),
        fill=(20, 18, 16),
        outline=(173, 135, 95),
        width=4
    )

    draw.line(
        (
            820,
            120,
            750,
            185,
            675,
            200
        ),
        fill=(184, 148, 105),
        width=13,
        joint="curve"
    )

    draw.polygon(
        (
            670,
            194,
            690,
            201,
            682,
            220,
            663,
            211
        ),
        fill=(77, 52, 35)
    )

    return img


# ============================================================
# ITUNES API
# ============================================================

@st.cache_data(ttl=600)
def request_itunes(
    term,
    country
):

    params = urllib.parse.urlencode(
        {
            "term": term,
            "country": country,
            "media": "music",
            "entity": "song",
            "limit": 50,
            "lang": "ko_kr",
        }
    )

    url = (
        "https://itunes.apple.com/search?"
        + params
    )

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=15
    ) as response:

        data = json.loads(
            response.read().decode(
                "utf-8"
            )
        )

    return data


@st.cache_data(ttl=600)
def search_music(term):

    term = term.strip()

    if not term:
        return []

    results = []

    # 한국 + 미국
    for country in ["KR", "US"]:

        try:

            data = request_itunes(
                term,
                country
            )

            results.extend(
                data.get(
                    "results",
                    []
                )
            )

        except Exception:
            pass

    songs = []
    seen = set()

    for item in results:

        title = item.get(
            "trackName"
        )

        artist = item.get(
            "artistName"
        )

        if not title or not artist:
            continue

        key = (
            title.lower(),
            artist.lower()
        )

        if key in seen:
            continue

        seen.add(key)

        cover = item.get(
            "artworkUrl100"
        )

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
                    len(songs)
                ),

                "title": title,

                "artist": artist,

                "album": item.get(
                    "collectionName",
                    "Single"
                ),

                "cover": cover,

                "preview": item.get(
                    "previewUrl"
                ),

                "genre": item.get(
                    "primaryGenreName",
                    ""
                ),

                "store": item.get(
                    "trackViewUrl",
                    ""
                ),
            }
        )

    return songs


# ============================================================
# HOME
# ============================================================

def home_page():

    st.write("")
    st.write("")

    # 큰 타이틀
    st.markdown(
        """
        # RECORD ROOM
        """
    )

    st.caption(
        "EST. 2026  ·  MUSIC & MEMORY"
    )

    st.write("")

    st.subheader(
        "오늘의 음악을 한 장의 레코드처럼."
    )

    st.write("")
    st.write("")

    # 턴테이블 장식
    st.image(
        make_turntable(),
        use_container_width=True
    )

    st.write("")
    st.write("")

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        if st.button(
            "ENTER ROOM  →",
            use_container_width=True
        ):

            go("choice")

    st.write("")

    st.caption(
        "A SMALL ROOM FOR MUSIC"
    )


# ============================================================
# CHOICE
# ============================================================

def choice_page():

    room_title(
        "RECORD ROOM",
        "What would you like?",
        "오늘은 어떤 음악을 만나볼까요?"
    )

    left, right = st.columns(
        2,
        gap="large"
    )

    with left:

        with wood_panel():

            st.subheader(
                "💿  노래듣기"
            )

            st.write(
                "가수나 곡을 검색해서 "
                "레코드 플레이어에서 들어보세요."
            )

            st.write("")

            if st.button(
                "MUSIC ROOM  →",
                use_container_width=True
            ):

                go("listen")

    with right:

        with wood_panel():

            st.subheader(
                "🎧  노래 추천받기"
            )

            st.write(
                "취향과 분위기를 바탕으로 "
                "음악을 추천받는 공간이에요."
            )

            st.write("")

            if st.button(
                "RECOMMEND  →",
                use_container_width=True
            ):

                go("recommend")

    st.write("")

    if st.button(
        "← HOME"
    ):

        go("home")


# ============================================================
# LISTEN
# ============================================================

def listen_page():

    room_title(
        "RECORD ROOM / MUSIC",
        "MUSIC ROOM",
        "가수 이름이나 곡 제목을 검색해보세요."
    )

    if st.button(
        "← CHOICE"
    ):

        go("choice")

    st.write("")

    with st.form(
        "search_form"
    ):

        col1, col2 = st.columns(
            [5, 1]
        )

        with col1:

            keyword = st.text_input(
                "검색",
                value=st.session_state.search_word,
                placeholder=(
                    "예: 아이유 / Oasis / "
                    "실리카겔 / Bruno Mars"
                ),
                label_visibility="collapsed"
            )

        with col2:

            search_button = st.form_submit_button(
                "SEARCH",
                use_container_width=True
            )

    if search_button:

        keyword = keyword.strip()

        st.session_state.search_word = keyword

        if keyword:

            with st.spinner(
                "레코드를 찾는 중..."
            ):

                st.session_state.songs = search_music(
                    keyword
                )

        else:

            st.session_state.songs = []

    songs = st.session_state.songs

    st.write("")

    # ========================================================
    # 검색 결과
    # ========================================================

    if songs:

        st.subheader(
            f"SEARCH RESULTS  ·  {len(songs)}"
        )

        st.caption(
            f"'{st.session_state.search_word}' 검색 결과"
        )

        st.write("")

        columns = st.columns(
            4,
            gap="medium"
        )

        for index, song in enumerate(
            songs[:24]
        ):

            with columns[index % 4]:

                with st.container(
                    border=True
                ):

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

                    st.markdown(
                        f"**{song['title']}**"
                    )

                    st.write(
                        f"🎤 {song['artist']}"
                    )

                    st.caption(
                        song["album"]
                    )

                    if song["genre"]:

                        st.caption(
                            song["genre"]
                        )

                    if st.button(
                        "💿 이 레코드 듣기",
                        key=(
                            f"song_"
                            f"{song['id']}_"
                            f"{index}"
                        ),
                        use_container_width=True
                    ):

                        st.session_state.selected_song = song

                        go("player")

    elif st.session_state.search_word:

        st.warning(
            "검색 결과가 없어요."
        )

    else:

        st.info(
            "🔎 가수 이름이나 곡 제목을 검색해보세요."
        )

        st.write("")

        st.subheader(
            "QUICK SEARCH"
        )

        quick = [
            "아이유",
            "실리카겔",
            "Oasis",
            "Bruno Mars",
            "NewJeans",
            "ZICO"
        ]

        quick_columns = st.columns(
            3
        )

        for i, name in enumerate(
            quick
        ):

            with quick_columns[
                i % 3
            ]:

                if st.button(
                    name,
                    key=f"quick_{i}",
                    use_container_width=True
                ):

                    st.session_state.search_word = name

                    st.session_state.songs = search_music(
                        name
                    )

                    st.rerun()


# ============================================================
# PLAYER
# ============================================================

def player_page():

    song = st.session_state.selected_song

    if song is None:

        go("listen")
        return

    room_title(
        "RECORD ROOM / NOW PLAYING",
        "NOW PLAYING",
        "한 장의 레코드처럼 음악을 들어보세요."
    )

    if st.button(
        "← MUSIC ROOM"
    ):

        go("listen")

    st.write("")
    st.write("")

    # ========================================================
    # 실제 LP
    # ========================================================

    left, center, right = st.columns(
        [1, 3, 1]
    )

    with left:

        with wood_panel():

            st.caption(
                "RECORD"
            )

            st.subheader(
                "NOW SPINNING"
            )

            st.write("")

            st.metric(
                "FORMAT",
                "VINYL"
            )

            if song["genre"]:

                st.metric(
                    "GENRE",
                    song["genre"]
                )

    with center:

        # ★ 핵심 ★
        # 실제로 보이는 LP 이미지
        record_image = make_record_image(
            song["cover"]
        )

        st.image(
            record_image,
            use_container_width=True
        )

    with right:

        with wood_panel():

            st.caption(
                "TRACK INFO"
            )

            st.subheader(
                song["title"]
            )

            st.write(
                f"🎤 {song['artist']}"
            )

            st.write("")

            st.caption(
                song["album"]
            )

            if song["genre"]:

                st.caption(
                    song["genre"]
                )

    # ========================================================
    # 플레이어 정보
    # ========================================================

    st.write("")
    st.divider()

    st.subheader(
        "♫  LISTEN"
    )

    st.markdown(
        f"### {song['title']}"
    )

    st.write(
        f"**{song['artist']}**"
    )

    if song["preview"]:

        st.audio(
            song["preview"],
            format="audio/mpeg"
        )

        st.caption(
            "Apple에서 제공하는 30초 미리듣기입니다."
        )

    else:

        st.warning(
            "이 곡은 미리듣기를 제공하지 않습니다."
        )

    st.write("")

    if song["store"]:

        st.link_button(
            "Apple Music / iTunes에서 보기 →",
            song["store"],
            use_container_width=True
        )

    st.write("")
    st.write("")

    col1, col2 = st.columns(
        2
    )

    with col1:

        if st.button(
            "다른 레코드 고르기",
            use_container_width=True
        ):

            go("listen")

    with col2:

        if st.button(
            "처음으로",
            use_container_width=True
        ):

            go("home")


# ============================================================
# RECOMMEND
# ============================================================

def recommend_page():

    room_title(
        "RECORD ROOM / RECOMMEND",
        "MUSIC RECOMMEND",
        "당신의 음악 취향을 위한 공간."
    )

    st.info(
        "추천 기능은 음악 검색 기능을 기반으로 "
        "다음 단계에서 확장할 수 있어요."
    )

    st.write("")

    if st.button(
        "← CHOICE",
        use_container_width=True
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
