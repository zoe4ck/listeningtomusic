import streamlit as st
import urllib.parse
import urllib.request
import json
import io
import re
import difflib
import random
import math

from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ============================================================
# 1. PAGE SETTING
# ============================================================

st.set_page_config(
    page_title="RECORD ROOM",
    page_icon="🎵",
    layout="wide"
)


# ============================================================
# 2. SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "selected_song" not in st.session_state:
    st.session_state.selected_song = None

if "playing" not in st.session_state:
    st.session_state.playing = False


# ============================================================
# 3. COLORS
# ============================================================

DARK = (28, 18, 11)
DARK2 = (42, 27, 17)
WOOD = (75, 47, 28)
WOOD2 = (103, 66, 38)
WOOD3 = (128, 84, 48)

CREAM = (242, 226, 198)
CREAM2 = (221, 198, 158)

GOLD = (183, 140, 72)
GOLD2 = (211, 169, 94)

BLACK = (12, 12, 12)
WHITE = (249, 245, 235)


# ============================================================
# 4. FONT
# ============================================================

def get_font(size, bold=False):

    if bold:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]

    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            pass

    return ImageFont.load_default()


# ============================================================
# 5. WOOD TEXTURE
# ============================================================

def create_wood_background(width=1400, height=800):

    img = Image.new(
        "RGB",
        (width, height),
        DARK2
    )

    draw = ImageDraw.Draw(img)

    random.seed(10)

    # 나무결
    for _ in range(90):

        y = random.randint(0, height)

        points = []

        for x in range(0, width + 40, 40):

            yy = y + random.randint(-12, 12)

            points.append((x, yy))

        draw.line(
            points,
            fill=random.choice(
                [
                    WOOD,
                    WOOD2,
                    WOOD3,
                    (56, 34, 20),
                ]
            ),
            width=random.randint(1, 4)
        )

    # 어두운 테두리
    draw.rectangle(
        (0, 0, width - 1, height - 1),
        outline=DARKER,
        width=18
    )

    # 빈티지 빛
    overlay = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0)
    )

    odraw = ImageDraw.Draw(overlay)

    for r in range(700, 100, -25):

        alpha = int(
            3 + (700 - r) / 40
        )

        odraw.ellipse(
            (
                width // 2 - r,
                height // 2 - r,
                width // 2 + r,
                height // 2 + r
            ),
            fill=(255, 220, 170, alpha)
        )

    img = Image.alpha_composite(
        img.convert("RGBA"),
        overlay
    ).convert("RGB")

    return img


# ============================================================
# 6. TITLE IMAGE
# ============================================================

def create_title():

    width = 1100
    height = 240

    img = Image.new(
        "RGB",
        (width, height),
        DARK
    )

    draw = ImageDraw.Draw(img)

    title_font = get_font(
        74,
        True
    )

    sub_font = get_font(
        24,
        False
    )

    title = "RECORD ROOM"

    bbox = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )

    tw = bbox[2] - bbox[0]

    draw.text(
        (
            (width - tw) // 2,
            45
        ),
        title,
        fill=CREAM,
        font=title_font
    )

    subtitle = "오늘의 음악을 한 장의 레코드처럼."

    bbox = draw.textbbox(
        (0, 0),
        subtitle,
        font=sub_font
    )

    sw = bbox[2] - bbox[0]

    draw.text(
        (
            (width - sw) // 2,
            145
        ),
        subtitle,
        fill=CREAM2,
        font=sub_font
    )

    draw.line(
        (
            180,
            195,
            width - 180,
            195
        ),
        fill=GOLD,
        width=2
    )

    return img


# ============================================================
# 7. ITUNES API
# ============================================================

@st.cache_data(ttl=600)
def api_request(url):

    try:

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(
            req,
            timeout=12
        ) as response:

            raw = response.read()

        return json.loads(
            raw.decode("utf-8")
        )

    except Exception:

        return None


# ============================================================
# 8. TEXT NORMALIZATION
# ============================================================

def normalize(text):

    if not text:
        return ""

    text = str(text).lower().strip()

    # 괄호 제거
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

    # 특수문자 제거
    text = re.sub(
        r"[^0-9a-z가-힣]+",
        "",
        text
    )

    return text


def similarity(a, b):

    a = normalize(a)
    b = normalize(b)

    if not a or not b:
        return 0

    if a == b:
        return 1.0

    if a in b:
        return 0.9

    if b in a:
        return 0.85

    return difflib.SequenceMatcher(
        None,
        a,
        b
    ).ratio()


# ============================================================
# 9. KNOWN ARTIST ALIASES
# ============================================================

ARTIST_ALIASES = {

    "뉴진스": [
        "뉴진스",
        "newjeans"
    ],

    "newjeans": [
        "뉴진스",
        "newjeans"
    ],

    "아이유": [
        "아이유",
        "iu"
    ],

    "iu": [
        "아이유",
        "iu"
    ],

    "지코": [
        "지코",
        "zico"
    ],

    "zico": [
        "지코",
        "zico"
    ],

    "르세라핌": [
        "르세라핌",
        "le sserafim",
        "lesserafim"
    ],

    "aespa": [
        "aespa",
        "에스파"
    ],

    "에스파": [
        "aespa",
        "에스파"
    ],

    "아이브": [
        "아이브",
        "ive"
    ],

    "ive": [
        "아이브",
        "ive"
    ],

    "블랙핑크": [
        "블랙핑크",
        "blackpink"
    ],

    "blackpink": [
        "블랙핑크",
        "blackpink"
    ],

    "bts": [
        "bts",
        "방탄소년단"
    ],

    "방탄소년단": [
        "bts",
        "방탄소년단"
    ]
}


def is_artist_match(query, artist):

    q = normalize(query)
    a = normalize(artist)

    if not q or not a:
        return False

    # 알려진 가수
    if q in ARTIST_ALIASES:

        for alias in ARTIST_ALIASES[q]:

            if normalize(alias) == a:
                return True

        return False

    # 일반 검색
    score = similarity(
        query,
        artist
    )

    return score >= 0.72


# ============================================================
# 10. SONG SEARCH
# ============================================================

@st.cache_data(ttl=600)
def search_song_api(query):

    encoded = urllib.parse.quote(
        query
    )

    url = (
        "https://itunes.apple.com/search?"
        f"term={encoded}"
        "&country=KR"
        "&media=music"
        "&entity=song"
        "&limit=50"
    )

    data = api_request(url)

    if not data:
        return []

    results = []

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

        track = item.get(
            "trackName",
            ""
        )

        artist = item.get(
            "artistName",
            ""
        )

        if not track or not artist:
            continue

        results.append(
            {
                "track_name": track,
                "artist_name": artist,
                "album_name": item.get(
                    "collectionName",
                    ""
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
        )

    return results


# ============================================================
# 11. ARTIST SEARCH
# ============================================================

@st.cache_data(ttl=600)
def search_artist_api(query):

    encoded = urllib.parse.quote(
        query
    )

    # 핵심:
    # 그냥 musicArtist 첫 결과를 가져오지 않음
    # artistTerm으로 가수 검색
    url = (
        "https://itunes.apple.com/search?"
        f"term={encoded}"
        "&country=KR"
        "&media=music"
        "&entity=musicArtist"
        "&attribute=artistTerm"
        "&limit=20"
    )

    data = api_request(url)

    if not data:
        return []

    artists = data.get(
        "results",
        []
    )

    # 점수 계산
    scored = []

    for artist in artists:

        name = artist.get(
            "artistName",
            ""
        )

        if not name:
            continue

        if is_artist_match(
            query,
            name
        ):

            score = similarity(
                query,
                name
            )

            scored.append(
                (
                    score,
                    artist
                )
            )

    # 가장 비슷한 가수부터
    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # 점수가 낮으면 아예 버림
    return [
        artist
        for score, artist in scored
        if score >= 0.72
    ][:3]


# ============================================================
# 12. ARTIST SONGS
# ============================================================

@st.cache_data(ttl=600)
def get_artist_songs(
    artist_id
):

    if not artist_id:
        return []

    url = (
        "https://itunes.apple.com/lookup?"
        f"id={artist_id}"
        "&entity=song"
        "&country=KR"
        "&limit=50"
    )

    data = api_request(url)

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

        track = item.get(
            "trackName",
            ""
        )

        artist = item.get(
            "artistName",
            ""
        )

        if not track or not artist:
            continue

        songs.append(
            {
                "track_name": track,
                "artist_name": artist,
                "album_name": item.get(
                    "collectionName",
                    ""
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

    return songs


# ============================================================
# 13. FINAL SEARCH
# ============================================================

def search_music(query):

    query = query.strip()

    if not query:
        return []


    # --------------------------------------------------------
    # A. 유명 가수의 경우 가수 검색을 먼저
    # --------------------------------------------------------

    if normalize(query) in ARTIST_ALIASES:

        artists = search_artist_api(
            query
        )

        if artists:

            artist = artists[0]

            artist_id = artist.get(
                "artistId"
            )

            songs = get_artist_songs(
                artist_id
            )

            # 혹시 API가 이상한 artist를 반환하면
            # 다시 한 번 가수명 검증
            songs = [
                song
                for song in songs
                if is_artist_match(
                    query,
                    song["artist_name"]
                )
            ]

            if songs:
                return songs


    # --------------------------------------------------------
    # B. 노래 검색
    # --------------------------------------------------------

    songs = search_song_api(
        query
    )

    if songs:

        # 가수 검색어로 판단되는 경우
        artist_results = [
            song
            for song in songs
            if is_artist_match(
                query,
                song["artist_name"]
            )
        ]

        if artist_results:

            return artist_results[:30]

        # 노래 제목 검색
        scored = []

        for song in songs:

            score = max(
                similarity(
                    query,
                    song["track_name"]
                ),
                similarity(
                    query,
                    song["album_name"]
                )
            )

            scored.append(
                (
                    score,
                    song
                )
            )

        scored.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            song
            for score, song in scored
            if score >= 0.35
        ][:30]


    # --------------------------------------------------------
    # C. 최종 가수 검색
    # --------------------------------------------------------

    artists = search_artist_api(
        query
    )

    if artists:

        artist = artists[0]

        songs = get_artist_songs(
            artist.get("artistId")
        )

        songs = [
            song
            for song in songs
            if is_artist_match(
                query,
                song["artist_name"]
            )
        ]

        if songs:
            return songs[:30]


    return []


# ============================================================
# 14. ALBUM COVER CARD
# ============================================================

def make_album_card(
    song,
    width=330,
    height=430
):

    img = Image.new(
        "RGB",
        (width, height),
        DARK2
    )

    draw = ImageDraw.Draw(img)

    # 바깥 프레임
    draw.rounded_rectangle(
        (
            5,
            5,
            width - 5,
            height - 5
        ),
        radius=18,
        fill=(54, 34, 21),
        outline=GOLD,
        width=2
    )

    # 커버
    cover_size = width - 50

    cover_x = 25
    cover_y = 22

    try:

        url = song.get(
            "artwork",
            ""
        )

        if url:

            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent":
                    "Mozilla/5.0"
                }
            )

            with urllib.request.urlopen(
                req,
                timeout=10
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
                    cover_x,
                    cover_y
                )
            )

    except:

        draw.rectangle(
            (
                cover_x,
                cover_y,
                cover_x + cover_size,
                cover_y + cover_size
            ),
            fill=(35, 25, 18)
        )

        note_font = get_font(
            70,
            True
        )

        draw.text(
            (
                width // 2 - 25,
                160
            ),
            "♪",
            fill=GOLD,
            font=note_font
        )


    # 제목
    title_font = get_font(
        21,
        True
    )

    artist_font = get_font(
        17,
        False
    )

    title = song.get(
        "track_name",
        ""
    )

    artist = song.get(
        "artist_name",
        ""
    )

    # 긴 제목 자르기
    if len(title) > 25:
        title = title[:25] + "..."

    if len(artist) > 24:
        artist = artist[:24] + "..."

    draw.text(
        (
            25,
            height - 91
        ),
        title,
        fill=CREAM,
        font=title_font
    )

    draw.text(
        (
            25,
            height - 56
        ),
        artist,
        fill=CREAM2,
        font=artist_font
    )

    return img


# ============================================================
# 15. VINYL
# ============================================================

def make_vinyl(
    cover_url=None,
    size=680
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
            25,
            25,
            size - 10,
            size - 10
        ),
        fill=(8, 7, 6)
    )

    # LP
    draw.ellipse(
        (
            10,
            10,
            size - 25,
            size - 25
        ),
        fill=VINYL,
        outline=(76, 76, 76),
        width=3
    )

    # 레코드 홈
    for radius in range(
        105,
        size // 2 - 20,
        13
    ):

        draw.ellipse(
            (
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius
            ),
            outline=(37, 37, 37),
            width=1
        )

    # 빛 반사
    draw.arc(
        (
            70,
            70,
            size - 85,
            size - 85
        ),
        start=215,
        end=320,
        fill=(70, 70, 70),
        width=3
    )

    # 중앙 라벨
    label = 105

    draw.ellipse(
        (
            cx - label,
            cy - label,
            cx + label,
            cy + label
        ),
        fill=(142, 89, 43),
        outline=GOLD2,
        width=4
    )

    # 커버
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
                timeout=10
            ) as response:

                data = response.read()

            cover = Image.open(
                io.BytesIO(data)
            ).convert("RGB")

            cover_size = 185

            cover = cover.resize(
                (
                    cover_size,
                    cover_size
                )
            )

            img.paste(
                cover,
                (
                    cx - cover_size // 2,
                    cy - cover_size // 2
                )
            )

        except:
            pass

    # 중앙 구멍
    hole = 10

    draw.ellipse(
        (
            cx - hole,
            cy - hole,
            cx + hole,
            cy + hole
        ),
        fill=BLACK
    )

    return img


# ============================================================
# 16. TONEARM IMAGE
# ============================================================

def make_tonearm(
    width=720,
    height=680
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
            555,
            65,
            665,
            175
        ),
        fill=(92, 61, 36),
        outline=GOLD2,
        width=3
    )

    draw.ellipse(
        (
            585,
            95,
            635,
            145
        ),
        fill=(35, 25, 18)
    )

    # 톤암
    draw.line(
        (
            610,
            120,
            510,
            170,
            430,
            245,
            365,
            330
        ),
        fill=(194, 169, 128),
        width=13
    )

    # 바늘
    draw.polygon(
        [
            (355, 318),
            (375, 325),
            (360, 355),
        ],
        fill=(190, 160, 115)
    )

    return img


# ============================================================
# 17. HOME
# ============================================================

def show_home():

    st.image(
        create_wood_background(
            1400,
            720
        ),
        use_container_width=True
    )

    st.image(
        create_title(),
        use_container_width=True
    )

    st.write("")

    c1, c2, c3 = st.columns(
        [1, 1, 1]
    )

    with c2:

        if st.button(
            "ENTER ROOM",
            use_container_width=True
        ):

            st.session_state.page = "choice"
            st.rerun()


# ============================================================
# 18. CHOICE
# ============================================================

def show_choice():

    st.image(
        create_title(),
        use_container_width=True
    )

    st.write("")

    left, right = st.columns(2)

    with left:

        st.image(
            create_album_card(
                {
                    "track_name":
                    "MUSIC LIBRARY",
                    "artist_name":
                    "SEARCH YOUR MUSIC",
                    "artwork":
                    ""
                },
                500,
                500
            ),
            use_container_width=True
        )

        if st.button(
            "🎧  노래듣기",
            use_container_width=True
        ):

            st.session_state.page = "listen"
            st.rerun()

    with right:

        st.image(
            create_album_card(
                {
                    "track_name":
                    "RECOMMEND",
                    "artist_name":
                    "FIND YOUR MOOD",
                    "artwork":
                    ""
                },
                500,
                500
            ),
            use_container_width=True
        )

        if st.button(
            "💿  노래 추천받기",
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


# ============================================================
# 19. MUSIC LIBRARY
# ============================================================

def show_listen():

    st.image(
        create_title(
        ),
        use_container_width=True
    )

    st.write("")

    st.subheader(
        "MUSIC LIBRARY"
    )

    st.caption(
        "가수 이름이나 노래 제목을 검색하세요."
    )

    with st.form(
        "search_form"
    ):

        query = st.text_input(
            "검색어",
            value=st.session_state.search_query,
            placeholder=
            "아이유 / 뉴진스 / 지코 / Love wins all",
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

                results = search_music(
                    query
                )

            st.session_state.search_results = results

    results = st.session_state.search_results

    st.write("")

    if not results:

        if st.session_state.search_query:

            st.warning(
                f"'{st.session_state.search_query}'에 맞는 음악을 찾지 못했어요."
            )

            st.caption(
                "가수 이름이나 정확한 노래 제목으로 다시 검색해보세요."
            )

        else:

            st.image(
                create_vinyl(),
                width=360
            )

            st.subheader(
                "SEARCH FOR A RECORD"
            )

            st.caption(
                "검색 결과에서 원하는 앨범을 골라보세요."
            )

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
                        create_album_card(
                            song
                        ),
                        use_container_width=True
                    )

                    if st.button(
                        "💿 레코드에 올리기",
                        key=
                        f"pick_{start}_{idx}",
                        use_container_width=True
                    ):

                        st.session_state.selected_song = song
                        st.session_state.playing = True
                        st.session_state.page = "player"

                        st.rerun()

    st.write("")
    st.divider()

    if st.button(
        "← 메뉴로",
        use_container_width=True
    ):

        st.session_state.page = "choice"
        st.session_state.search_results = []
        st.session_state.search_query = ""

        st.rerun()


# ============================================================
# 20. PLAYER
# ============================================================

def show_player():

    song = st.session_state.selected_song

    if not song:

        st.session_state.page = "listen"
        st.rerun()
        return

    st.image(
        create_title(),
        use_container_width=True
    )

    st.write("")

    left, right = st.columns(
        [1.4, 1]
    )

    with left:

        st.image(
            make_vinyl(
                song.get(
                    "artwork",
                    ""
                )
            ),
            use_container_width=True
        )

        st.image(
            make_tonearm(),
            use_container_width=True
        )

    with right:

        st.write("")
        st.write("")

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

        st.write("")
        st.divider()

        if song.get(
            "preview"
        ):

            st.write(
                "🎵  RECORD PREVIEW"
            )

            st.audio(
                song["preview"],
                format="audio/mp4"
            )

            st.caption(
                "Apple Music에서 제공되는 미리듣기입니다."
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

            st.session_state.playing = False
            st.session_state.selected_song = None
            st.session_state.page = "listen"

            st.rerun()

        if st.button(
            "← 음악 목록으로",
            use_container_width=True
        ):

            st.session_state.playing = False
            st.session_state.selected_song = None
            st.session_state.page = "listen"

            st.rerun()


# ============================================================
# 21. RECOMMEND
# ============================================================

def show_recommend():

    st.image(
        create_title(),
        use_container_width=True
    )

    st.write("")

    st.subheader(
        "CHOOSE YOUR MOOD"
    )

    moods = {

        "🌙 새벽 감성": [
            "아이유",
            "검정치마",
            "실리카겔"
        ],

        "💗 설레는 날": [
            "아이유",
            "뉴진스",
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
        moods.keys()
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

                    if results:

                        # 실제 artist 검증
                        valid = [
                            song
                            for song in results
                            if is_artist_match(
                                artist,
                                song["artist_name"]
                            )
                        ]

                        if valid:

                            song = random.choice(
                                valid
                            )

                            st.session_state.selected_song = song
                            st.session_state.playing = True
                            st.session_state.page = "player"

                            st.rerun()

                        else:

                            st.error(
                                "추천 음악을 정확하게 찾지 못했어요."
                            )

                    else:

                        st.error(
                            "음악을 불러오지 못했어요."
                        )

    st.write("")
    st.divider()

    if st.button(
        "← 메뉴로",
        use_container_width=True
    ):

        st.session_state.page = "choice"
        st.rerun()


# ============================================================
# 22. RUN
# ============================================================

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
