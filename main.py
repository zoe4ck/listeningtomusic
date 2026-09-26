import streamlit as st
import urllib.parse
import urllib.request
import json
import io
import re
import difflib
import random

from PIL import Image, ImageDraw, ImageFont


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="RECORD ROOM",
    page_icon="🎵",
    layout="wide",
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "page": "home",
    "search_query": "",
    "search_results": [],
    "selected_song": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# COLORS
# =========================================================

DARK = (28, 18, 11)
DARKER = (19, 12, 8)
WOOD = (72, 45, 27)
WOOD_LIGHT = (104, 68, 40)
WOOD_HIGHLIGHT = (132, 88, 51)

CREAM = (244, 228, 199)
CREAM_DARK = (215, 188, 145)

GOLD = (187, 145, 77)

BLACK = (12, 12, 12)
WHITE = (250, 247, 239)


# =========================================================
# FONT
# =========================================================

def get_font(size, bold=False):

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
        except OSError:
            continue

    return ImageFont.load_default()


def fit_text(draw, text, font, max_width):

    text = str(text or "")

    if draw.textbbox(
        (0, 0),
        text,
        font=font
    )[2] <= max_width:
        return text

    while len(text) > 1:

        text = text[:-1]

        candidate = text.rstrip() + "..."

        if draw.textbbox(
            (0, 0),
            candidate,
            font=font
        )[2] <= max_width:

            return candidate

    return "..."


# =========================================================
# WOOD BACKGROUND
# =========================================================

@st.cache_data
def make_wood_panel(
    width=1500,
    height=900,
    seed=7
):

    img = Image.new(
        "RGB",
        (width, height),
        DARK
    )

    draw = ImageDraw.Draw(img)

    random.seed(seed)

    # 나무 판자
    board_width = 220

    for x in range(
        0,
        width,
        board_width
    ):

        shade = random.choice(
            [
                WOOD,
                WOOD_LIGHT,
                (61, 37, 22),
                (87, 54, 32),
            ]
        )

        draw.rectangle(
            (
                x,
                0,
                min(
                    x + board_width,
                    width
                ),
                height
            ),
            fill=shade
        )

        draw.line(
            (
                x,
                0,
                x,
                height
            ),
            fill=DARKER,
            width=4
        )

    # 나무결
    for _ in range(110):

        y = random.randint(
            0,
            height
        )

        points = []

        for x in range(
            -50,
            width + 50,
            45
        ):

            points.append(
                (
                    x,
                    y + random.randint(
                        -18,
                        18
                    )
                )
            )

        draw.line(
            points,
            fill=random.choice(
                [
                    WOOD_LIGHT,
                    WOOD_HIGHLIGHT,
                    (52, 31, 18),
                    (143, 94, 55),
                ]
            ),
            width=random.randint(
                1,
                5
            )
        )

    # 어두운 테두리
    draw.rectangle(
        (
            0,
            0,
            width - 1,
            height - 1
        ),
        outline=DARKER,
        width=20
    )

    return img


# =========================================================
# HEADER
# =========================================================

@st.cache_data
def make_header(
    title="RECORD ROOM",
    subtitle="오늘의 음악을 한 장의 레코드처럼."
):

    width = 1400
    height = 300

    img = Image.new(
        "RGB",
        (
            width,
            height
        ),
        DARK
    )

    draw = ImageDraw.Draw(img)

    # 나무 줄무늬
    for y in range(
        0,
        height,
        40
    ):

        if (y // 40) % 2 == 0:
            fill = WOOD
        else:
            fill = WOOD_LIGHT

        draw.rectangle(
            (
                0,
                y,
                width,
                y + 20
            ),
            fill=fill
        )

    title_font = get_font(
        80,
        True
    )

    subtitle_font = get_font(
        25,
        False
    )

    title_box = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )

    title_width = (
        title_box[2] -
        title_box[0]
    )

    draw.text(
        (
            (width - title_width) / 2,
            58
        ),
        title,
        fill=CREAM,
        font=title_font
    )

    subtitle_box = draw.textbbox(
        (0, 0),
        subtitle,
        font=subtitle_font
    )

    subtitle_width = (
        subtitle_box[2] -
        subtitle_box[0]
    )

    draw.text(
        (
            (width - subtitle_width) / 2,
            165
        ),
        subtitle,
        fill=CREAM_DARK,
        font=subtitle_font
    )

    draw.line(
        (
            240,
            215,
            width - 240,
            215
        ),
        fill=GOLD,
        width=2
    )

    return img


# =========================================================
# VINYL
# =========================================================

@st.cache_data
def make_record(
    cover_url="",
    size=720
):

    img = Image.new(
        "RGB",
        (
            size,
            size
        ),
        DARK
    )

    draw = ImageDraw.Draw(img)

    cx = size // 2
    cy = size // 2

    # 그림자
    draw.ellipse(
        (
            18,
            28,
            size - 8,
            size - 18
        ),
        fill=(7, 7, 7)
    )

    # LP
    draw.ellipse(
        (
            8,
            8,
            size - 28,
            size - 28
        ),
        fill=(18, 18, 18),
        outline=(75, 75, 75),
        width=3
    )

    # LP 홈
    for radius in range(
        110,
        size // 2 - 28,
        14
    ):

        draw.ellipse(
            (
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius
            ),
            outline=(36, 36, 36),
            width=1
        )

    # 빛 반사
    draw.arc(
        (
            60,
            60,
            size - 80,
            size - 80
        ),
        start=205,
        end=310,
        fill=(92, 92, 92),
        width=3
    )

    # 중앙 라벨
    label = 112

    draw.ellipse(
        (
            cx - label,
            cy - label,
            cx + label,
            cy + label
        ),
        fill=(137, 88, 43),
        outline=GOLD,
        width=4
    )

    # 앨범 커버
    if cover_url:

        try:

            req = urllib.request.Request(
                cover_url,
                headers={
                    "User-Agent":
                    "Mozilla/5.0"
                }
            )

            with urllib.request.urlopen(
                req,
                timeout=8
            ) as response:

                data = response.read()

            cover = Image.open(
                io.BytesIO(data)
            ).convert("RGB")

            cover = cover.resize(
                (
                    190,
                    190
                )
            )

            img.paste(
                cover,
                (
                    cx - 95,
                    cy - 95
                )
            )

        except Exception:
            pass

    # 중앙 구멍
    draw.ellipse(
        (
            cx - 10,
            cy - 10,
            cx + 10,
            cy + 10
        ),
        fill=BLACK
    )

    return img


# =========================================================
# TONEARM
# =========================================================

@st.cache_data
def make_tonearm(
    width=700,
    height=300
):

    img = Image.new(
        "RGBA",
        (
            width,
            height
        ),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(img)

    # 받침대
    draw.ellipse(
        (
            505,
            35,
            625,
            155
        ),
        fill=(83, 55, 33),
        outline=GOLD,
        width=3
    )

    draw.ellipse(
        (
            537,
            67,
            593,
            123
        ),
        fill=(24, 17, 12)
    )

    # 톤암
    points = [
        (566, 96),
        (470, 105),
        (400, 145),
        (326, 205),
    ]

    draw.line(
        points,
        fill=(210, 188, 151),
        width=13
    )

    draw.line(
        points,
        fill=(105, 91, 72),
        width=3
    )

    # 바늘
    draw.polygon(
        [
            (312, 198),
            (342, 210),
            (326, 244),
        ],
        fill=(205, 175, 127)
    )

    return img


# =========================================================
# ALBUM CARD
# =========================================================

@st.cache_data
def make_album_card(
    song,
    width=430,
    height=500
):

    img = Image.new(
        "RGB",
        (
            width,
            height
        ),
        DARK
    )

    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle(
        (
            4,
            4,
            width - 4,
            height - 4
        ),
        radius=20,
        fill=(52, 31, 19),
        outline=GOLD,
        width=2
    )

    cover_size = width - 50

    try:

        url = song.get(
            "artwork",
            ""
        )

        if not url:
            raise ValueError

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(
            req,
            timeout=8
        ) as response:

            data = response.read()

        cover = Image.open(
            io.BytesIO(data)
        ).convert("RGB")

        cover = cover.resize(
            (
                cover_size,
                cover_size
            )
        )

        img.paste(
            cover,
            (
                25,
                25
            )
        )

    except Exception:

        draw.rectangle(
            (
                25,
                25,
                25 + cover_size,
                25 + cover_size
            ),
            fill=(27, 20, 14)
        )

        note_font = get_font(
            80,
            True
        )

        draw.text(
            (
                width // 2 - 27,
                width // 2 - 45
            ),
            "♪",
            fill=GOLD,
            font=note_font
        )

    title_font = get_font(
        22,
        True
    )

    artist_font = get_font(
        18,
        False
    )

    title = fit_text(
        draw,
        song.get(
            "track_name",
            ""
        ),
        title_font,
        width - 50
    )

    artist = fit_text(
        draw,
        song.get(
            "artist_name",
            ""
        ),
        artist_font,
        width - 50
    )

    draw.text(
        (
            25,
            height - 90
        ),
        title,
        fill=CREAM,
        font=title_font
    )

    draw.text(
        (
            25,
            height - 54
        ),
        artist,
        fill=CREAM_DARK,
        font=artist_font
    )

    return img


# =========================================================
# ITUNES API
# =========================================================

@st.cache_data(ttl=600)
def fetch_json(url):

    try:

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=12
        ) as response:

            return json.loads(
                response.read().decode(
                    "utf-8"
                )
            )

    except Exception:

        return None


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize(text):

    text = str(
        text or ""
    ).lower().strip()

    text = re.sub(
        r"\([^)]*\)",
        " ",
        text
    )

    text = re.sub(
        r"\[[^\]]*\]",
        " ",
        text
    )

    return re.sub(
        r"[^0-9a-z가-힣]+",
        "",
        text
    )


def similarity(
    a,
    b
):

    a = normalize(a)
    b = normalize(b)

    if not a or not b:
        return 0.0

    if a == b:
        return 1.0

    if a in b or b in a:
        return 0.9

    return difflib.SequenceMatcher(
        None,
        a,
        b
    ).ratio()


# =========================================================
# ARTIST ALIASES
# =========================================================

ARTIST_ALIASES = {

    "뉴진스": {
        "뉴진스",
        "newjeans"
    },

    "newjeans": {
        "뉴진스",
        "newjeans"
    },

    "아이유": {
        "아이유",
        "iu"
    },

    "iu": {
        "아이유",
        "iu"
    },

    "지코": {
        "지코",
        "zico"
    },

    "zico": {
        "지코",
        "zico"
    },

    "에스파": {
        "에스파",
        "aespa"
    },

    "aespa": {
        "에스파",
        "aespa"
    },

    "아이브": {
        "아이브",
        "ive"
    },

    "ive": {
        "아이브",
        "ive"
    },

    "블랙핑크": {
        "블랙핑크",
        "blackpink"
    },

    "blackpink": {
        "블랙핑크",
        "blackpink"
    },

    "르세라핌": {
        "르세라핌",
        "le sserafim",
        "lesserafim"
    },

    "le sserafim": {
        "르세라핌",
        "le sserafim",
        "lesserafim"
    },

    "방탄소년단": {
        "방탄소년단",
        "bts"
    },

    "bts": {
        "방탄소년단",
        "bts"
    },
}


def artist_matches(
    query,
    artist
):

    q = normalize(
        query
    )

    a = normalize(
        artist
    )

    aliases = ARTIST_ALIASES.get(q)

    if aliases:

        for alias in aliases:

            if normalize(alias) == a:
                return True

        return False

    return similarity(
        query,
        artist
    ) >= 0.72


# =========================================================
# SONG CONVERSION
# =========================================================

def build_song(item):

    return {

        "track_name":
        item.get(
            "trackName",
            ""
        ),

        "artist_name":
        item.get(
            "artistName",
            ""
        ),

        "album_name":
        item.get(
            "collectionName",
            ""
        ),

        "artwork":
        (
            item.get(
                "artworkUrl100",
                ""
            ) or ""
        ).replace(
            "100x100",
            "600x600"
        ),

        "preview":
        item.get(
            "previewUrl",
            ""
        ) or "",

        "track_url":
        item.get(
            "trackViewUrl",
            ""
        ) or "",

        "artist_id":
        item.get(
            "artistId"
        ),
    }


# =========================================================
# SEARCH SONG
# =========================================================

@st.cache_data(ttl=600)
def search_songs(
    query
):

    url = (
        "https://itunes.apple.com/search?"
        +
        urllib.parse.urlencode(
            {
                "term": query,
                "country": "KR",
                "media": "music",
                "entity": "song",
                "limit": 50,
            }
        )
    )

    data = fetch_json(
        url
    )

    if not data:
        return []

    songs = []

    for item in data.get(
        "results",
        []
    ):

        if item.get(
            "wrapperType"
        ) != "track":

            continue

        if item.get(
            "kind"
        ) != "song":

            continue

        song = build_song(
            item
        )

        if (
            song["track_name"]
            and
            song["artist_name"]
        ):

            songs.append(
                song
            )

    return songs


# =========================================================
# SEARCH ARTIST
# =========================================================

@st.cache_data(ttl=600)
def search_artists(
    query
):

    url = (
        "https://itunes.apple.com/search?"
        +
        urllib.parse.urlencode(
            {
                "term": query,
                "country": "KR",
                "media": "music",
                "entity": "musicArtist",
                "attribute": "artistTerm",
                "limit": 20,
            }
        )
    )

    data = fetch_json(
        url
    )

    if not data:
        return []

    scored = []

    for item in data.get(
        "results",
        []
    ):

        artist_name = item.get(
            "artistName",
            ""
        )

        if not artist_name:
            continue

        if artist_matches(
            query,
            artist_name
        ):

            scored.append(
                (
                    similarity(
                        query,
                        artist_name
                    ),
                    item
                )
            )

    scored.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        item
        for _, item in scored[:3]
    ]


# =========================================================
# GET ARTIST SONGS
# =========================================================

@st.cache_data(ttl=600)
def artist_songs(
    artist_id
):

    if not artist_id:
        return []

    url = (
        "https://itunes.apple.com/lookup?"
        +
        urllib.parse.urlencode(
            {
                "id": artist_id,
                "entity": "song",
                "country": "KR",
                "limit": 50,
            }
        )
    )

    data = fetch_json(
        url
    )

    if not data:
        return []

    songs = []

    for item in data.get(
        "results",
        []
    ):

        if item.get(
            "wrapperType"
        ) != "track":

            continue

        if item.get(
            "kind"
        ) != "song":

            continue

        song = build_song(
            item
        )

        if (
            song["track_name"]
            and
            song["artist_name"]
        ):

            songs.append(
                song
            )

    return songs


# =========================================================
# FINAL SEARCH
# =========================================================

def search_music(
    query
):

    query = query.strip()

    if not query:
        return []

    query_normalized = normalize(
        query
    )

    # -----------------------------------------------------
    # 1. 유명 가수면 가수 검색을 먼저
    # -----------------------------------------------------

    if query_normalized in ARTIST_ALIASES:

        artists = search_artists(
            query
        )

        if artists:

            songs = artist_songs(
                artists[0].get(
                    "artistId"
                )
            )

            songs = [
                song
                for song in songs
                if artist_matches(
                    query,
                    song["artist_name"]
                )
            ]

            if songs:
                return songs[:30]

    # -----------------------------------------------------
    # 2. 일반 노래 검색
    # -----------------------------------------------------

    songs = search_songs(
        query
    )

    if songs:

        # 가수명으로 검색했을 경우
        artist_results = [
            song
            for song in songs
            if artist_matches(
                query,
                song["artist_name"]
            )
        ]

        if artist_results:
            return artist_results[:30]

        # 노래 제목 검색
        ranked = sorted(
            songs,
            key=lambda song:
            similarity(
                query,
                song["track_name"]
            ),
            reverse=True
        )

        ranked = [
            song
            for song in ranked
            if similarity(
                query,
                song["track_name"]
            ) >= 0.35
        ]

        if ranked:
            return ranked[:30]

    # -----------------------------------------------------
    # 3. 마지막 가수 검색
    # -----------------------------------------------------

    artists = search_artists(
        query
    )

    if artists:

        songs = artist_songs(
            artists[0].get(
                "artistId"
            )
        )

        songs = [
            song
            for song in songs
            if artist_matches(
                query,
                song["artist_name"]
            )
        ]

        if songs:
            return songs[:30]

    return []


# =========================================================
# NAVIGATION
# =========================================================

def go_choice():

    st.session_state.page = "choice"
    st.session_state.search_query = ""
    st.session_state.search_results = []


def go_list():

    st.session_state.page = "listen"
    st.session_state.selected_song = None


# =========================================================
# HOME
# =========================================================

def page_home():

    st.image(
        make_wood_panel(
            1500,
            850
        ),
        use_container_width=True
    )

    st.image(
        make_header(),
        use_container_width=True
    )

    st.write("")

    col1, col2, col3 = st.columns(
        [1, 1, 1]
    )

    with col2:

        if st.button(
            "ENTER ROOM",
            use_container_width=True
        ):

            st.session_state.page = "choice"
            st.rerun()


# =========================================================
# CHOICE
# =========================================================

def page_choice():

    st.image(
        make_header(),
        use_container_width=True
    )

    st.write("")

    st.subheader(
        "WELCOME TO THE RECORD ROOM"
    )

    st.caption(
        "듣고 싶은 음악을 찾거나 오늘의 음악을 추천받아보세요."
    )

    st.write("")

    left, right = st.columns(2)

    with left:

        st.image(
            make_album_card(
                {
                    "track_name":
                    "MUSIC LIBRARY",

                    "artist_name":
                    "SEARCH YOUR MUSIC",

                    "artwork":
                    ""
                },
                520,
                520
            ),
            use_container_width=True
        )

        if st.button(
            "🎧 노래듣기",
            use_container_width=True
        ):

            st.session_state.page = "listen"
            st.rerun()

    with right:

        st.image(
            make_album_card(
                {
                    "track_name":
                    "RECOMMEND",

                    "artist_name":
                    "FIND YOUR MOOD",

                    "artwork":
                    ""
                },
                520,
                520
            ),
            use_container_width=True
        )

        if st.button(
            "💿 노래 추천받기",
            use_container_width=True
        ):

            st.session_state.page = "recommend"
            st.rerun()

    st.write("")

    if st.button(
        "← 처음으로",
        use_container_width=True
    ):

        st.session_state.page = "home"
        st.rerun()


# =========================================================
# MUSIC LIBRARY
# =========================================================

def page_listen():

    st.image(
        make_header(),
        use_container_width=True
    )

    st.write("")

    st.subheader(
        "MUSIC LIBRARY"
    )

    st.caption(
        "가수 이름 또는 노래 제목을 검색하세요."
    )

    st.write("")

    with st.form(
        "music_search"
    ):

        query = st.text_input(
            "검색어",
            value=st.session_state.search_query,
            placeholder=
            "예: 뉴진스 / 아이유 / 지코 / Super Shy",
            label_visibility="collapsed"
        )

        submitted = st.form_submit_button(
            "🔎 SEARCH",
            use_container_width=True
        )

    if submitted:

        query = query.strip()

        st.session_state.search_query = query

        if not query:

            st.session_state.search_results = []

        else:

            with st.spinner(
                f"'{query}' 검색 중..."
            ):

                st.session_state.search_results = search_music(
                    query
                )

    results = st.session_state.search_results

    st.write("")

    # 검색 결과 없음
    if (
        st.session_state.search_query
        and
        not results
    ):

        st.warning(
            f"'{st.session_state.search_query}'에 맞는 결과를 찾지 못했어요."
        )

        st.caption(
            "가수 이름이나 노래 제목을 조금 더 정확하게 입력해보세요."
        )

    # 검색 전
    elif not results:

        st.image(
            make_record(
                "",
                400
            ),
            width=400
        )

        st.subheader(
            "SEARCH FOR A RECORD"
        )

        st.caption(
            "검색 결과에서 원하는 레코드를 골라보세요."
        )

    # 검색 결과
    else:

        st.success(
            f"{len(results)}개의 음악을 찾았어요."
        )

        st.write("")

        for start in range(
            0,
            len(results),
            3
        ):

            row = results[
                start:start + 3
            ]

            cols = st.columns(
                len(row)
            )

            for idx, (
                col,
                song
            ) in enumerate(
                zip(
                    cols,
                    row
                )
            ):

                with col:

                    st.image(
                        make_album_card(
                            song
                        ),
                        use_container_width=True
                    )

                    if st.button(
                        "💿 레코드에 올리기",
                        key=
                        f"song_{start}_{idx}_{song['track_name']}",
                        use_container_width=True
                    ):

                        st.session_state.selected_song = song
                        st.session_state.page = "player"

                        st.rerun()

    st.write("")

    if st.button(
        "← 메뉴로",
        use_container_width=True
    ):

        go_choice()
        st.rerun()


# =========================================================
# PLAYER
# =========================================================

def page_player():

    song = st.session_state.selected_song

    if not song:

        st.session_state.page = "listen"
        st.rerun()

        return

    st.image(
        make_header(
            "NOW PLAYING",
            "레코드가 돌아가는 시간."
        ),
        use_container_width=True
    )

    st.write("")

    left, right = st.columns(
        [1.35, 1]
    )

    with left:

        st.image(
            make_record(
                song.get(
                    "artwork",
                    ""
                ),
                720
            ),
            use_container_width=True
        )

        st.image(
            make_tonearm(),
            use_container_width=True
        )

    with right:

        st.caption(
            "NOW PLAYING"
        )

        st.title(
            song["track_name"]
        )

        st.subheader(
            song["artist_name"]
        )

        st.write(
            song.get(
                "album_name",
                ""
            )
        )

        st.divider()

        if song.get(
            "preview"
        ):

            st.write(
                "🎵 30초 미리듣기"
            )

            st.audio(
                song["preview"],
                format="audio/mp4"
            )

        else:

            st.info(
                "이 곡은 미리듣기를 제공하지 않습니다."
            )

        st.write("")

        if st.button(
            "← 음악 목록으로",
            use_container_width=True
        ):

            go_list()
            st.rerun()

        if st.button(
            "← 메뉴로",
            use_container_width=True
        ):

            go_choice()
            st.session_state.selected_song = None
            st.rerun()


# =========================================================
# RECOMMEND
# =========================================================

def page_recommend():

    st.image(
        make_header(
            "RECORD ROOM",
            "오늘의 분위기에 맞는 음악을 골라보세요."
        ),
        use_container_width=True
    )

    st.write("")

    moods = {

        "🌙 새벽 감성": [
            "아이유",
            "검정치마",
            "실리카겔"
        ],

        "💗 설레는 날": [
            "뉴진스",
            "아이유",
            "AKMU"
        ],

        "🖤 힙합": [
            "지코",
            "크러쉬",
            "빈지노"
        ],

        "☀️ 기분 좋은 날": [
            "뉴진스",
            "아이브",
            "AKMU"
        ]
    }

    names = list(
        moods
    )

    for start in range(
        0,
        len(names),
        2
    ):

        cols = st.columns(2)

        for col, mood in zip(
            cols,
            names[start:start + 2]
        ):

            with col:

                if st.button(
                    mood,
                    key=f"mood_{start}_{mood}",
                    use_container_width=True
                ):

                    artist = random.choice(
                        moods[mood]
                    )

                    with st.spinner(
                        f"{artist}의 음악을 찾는 중..."
                    ):

                        results = search_music(
                            artist
                        )

                    valid = [
                        song
                        for song in results
                        if artist_matches(
                            artist,
                            song["artist_name"]
                        )
                    ]

                    if valid:

                        st.session_state.selected_song = random.choice(
                            valid
                        )

                        st.session_state.page = "player"

                        st.rerun()

                    else:

                        st.error(
                            "정확한 추천 결과를 찾지 못했어요."
                        )

    st.write("")

    if st.button(
        "← 메뉴로",
        use_container_width=True
    ):

        go_choice()
        st.rerun()


# =========================================================
# RUN
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
