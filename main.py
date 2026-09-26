import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from urllib.request import Request, urlopen
from urllib.parse import quote
import io
import json
import math
import hashlib
# =========================================================
# 1. 기본 설정
# =========================================================
st.set_page_config(
    page_title="RECORD ROOM",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# =========================================================
# 2. 전체 디자인
# =========================================================
st.markdown(
    """
    <style>
    /* ================================
       전체 화면
    ================================= */
    .stApp {
        background:
            radial-gradient(
                circle at 20% 20%,
                rgba(160, 104, 58, 0.25),
                transparent 30%
            ),
            radial-gradient(
                circle at 80% 80%,
                rgba(30, 15, 8, 0.35),
                transparent 35%
            ),
            repeating-linear-gradient(
                0deg,
                #4c2b1b 0px,
                #4c2b1b 38px,
                #55311e 39px,
                #432518 76px
            );
        color: #f3dfbd;
    }
    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }
    /* Streamlit 기본 상단 영역 */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
    /* 기본 텍스트 */
    p, label, span, div {
        font-family:
            "Georgia",
            "Times New Roman",
            serif;
    }
    /* ================================
       공통 제목
    ================================= */
    .room-title {
        color: #f3d7a3;
        font-size: clamp(42px, 7vw, 86px);
        font-weight: 700;
        letter-spacing: 0.18em;
        text-align: center;
        text-shadow:
            0 3px 0 #24130b,
            0 6px 15px rgba(0,0,0,0.55);
        margin-top: 3vh;
        margin-bottom: 0.4rem;
    }
    .room-subtitle {
        color: #d8b986;
        font-size: clamp(15px, 2vw, 22px);
        letter-spacing: 0.16em;
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .small-logo {
        color: #d7b57d;
        font-size: 18px;
        letter-spacing: 0.22em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    /* ================================
       나무 판넬
    ================================= */
    .wood-panel {
        background:
            linear-gradient(
                90deg,
                rgba(255,255,255,0.025),
                transparent 15%,
                rgba(0,0,0,0.08) 50%,
                transparent 85%
            ),
            repeating-linear-gradient(
                0deg,
                #6a3d25 0px,
                #6a3d25 55px,
                #57301e 56px,
                #70442a 58px
            );
        border:
            1px solid rgba(214,171,108,0.35);
        border-radius: 8px;
        box-shadow:
            inset 0 0 35px rgba(0,0,0,0.45),
            0 18px 45px rgba(0,0,0,0.45);
        padding: 30px;
    }
    /* ================================
       시작 버튼
    ================================= */
    .st-key-enter_room button {
        background:
            linear-gradient(
                180deg,
                #d5ad72,
                #a8733f
            ) !important;
        color: #2a160c !important;
        border:
            2px solid #e4c58f !important;
        border-radius: 3px !important;
        font-family: Georgia, serif !important;
        font-size: 18px !important;
        font-weight: bold !important;
        letter-spacing: 0.18em !important;
        box-shadow:
            0 5px 0 #593319,
            0 10px 20px rgba(0,0,0,0.35) !important;
        min-height: 58px !important;
    }
    .st-key-enter_room button:hover {
        filter: brightness(1.1);
        transform: translateY(-1px);
    }
    /* ================================
       메뉴 버튼
    ================================= */
    .st-key-listen_menu button,
    .st-key-recommend_menu button {
        background:
            linear-gradient(
                180deg,
                #70432a,
                #4b2919
            ) !important;
        color: #f2d6a3 !important;
        border:
            1px solid #a77a4d !important;
        border-radius: 5px !important;
        min-height: 120px !important;
        font-family: Georgia, serif !important;
        font-size: 24px !important;
        font-weight: bold !important;
        letter-spacing: 0.08em !important;
        box-shadow:
            inset 0 0 20px rgba(0,0,0,0.25),
            0 9px 18px rgba(0,0,0,0.35) !important;
    }
    .st-key-listen_menu button:hover,
    .st-key-recommend_menu button:hover {
        background:
            linear-gradient(
                180deg,
                #8a5635,
                #5a321f
            ) !important;
        border-color: #d1a66c !important;
    }
    /* ================================
       뒤로가기
    ================================= */
    .back-button button {
        color: #d8b986 !important;
    }
    /* ================================
       검색창
    ================================= */
    div[data-testid="stTextInput"] input {
        background: rgba(35,19,11,0.78) !important;
        color: #f5dfbb !important;
        border:
            1px solid #9a7046 !important;
        border-radius: 4px !important;
        font-family: Georgia, serif !important;
        height: 48px !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #a98962 !important;
    }
    /* ================================
       일반 버튼
    ================================= */
    .stButton button {
        font-family: Georgia, serif !important;
        border-radius: 4px !important;
        border-color: #8e6540 !important;
        background: #55301e !important;
        color: #efd3a0 !important;
    }
    .stButton button:hover {
        border-color: #d3aa70 !important;
        color: #ffe6b8 !important;
    }
    /* ================================
       앨범 선택 버튼
    ================================= */
    .album-select button {
        background:
            linear-gradient(
                180deg,
                #9c6b3e,
                #68401f
            ) !important;
        color: #f8dfb3 !important;
        border: 1px solid #d0a66a !important;
        font-size: 14px !important;
        letter-spacing: 0.04em !important;
    }
    /* ================================
       LP 올리기
    ================================= */
    .st-key-load_lp button {
        background:
            linear-gradient(
                180deg,
                #d0a368,
                #8d5c31
            ) !important;
        color: #28150a !important;
        border: 2px solid #e8c992 !important;
        min-height: 54px !important;
        font-weight: bold !important;
        font-size: 17px !important;
        letter-spacing: 0.1em !important;
        box-shadow:
            0 5px 0 #4b2917,
            0 10px 20px rgba(0,0,0,0.35) !important;
    }
    /* ================================
       톤암 버튼
    ================================= */
    .st-key-tonearm_toggle button {
        background:
            linear-gradient(
                180deg,
                #d7b178,
                #9a6b3e
            ) !important;
        color: #26140b !important;
        border:
            2px solid #edd09a !important;
        min-height: 58px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        letter-spacing: 0.08em !important;
        box-shadow:
            0 5px 0 #4d2b18,
            0 12px 22px rgba(0,0,0,0.4) !important;
    }
    /* ================================
       플레이어 정보
    ================================= */
    .now-playing {
        background:
            linear-gradient(
                135deg,
                rgba(39,20,11,0.88),
                rgba(87,47,27,0.78)
            );
        border:
            1px solid rgba(214,174,112,0.42);
        border-radius: 5px;
        padding: 20px;
        box-shadow:
            inset 0 0 25px rgba(0,0,0,0.35),
            0 12px 30px rgba(0,0,0,0.3);
    }
    .track-name {
        color: #f4d9a8;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 6px;
    }
    .artist-name {
        color: #c69b65;
        font-size: 18px;
    }
    .status-playing {
        color: #dcb779;
        font-size: 14px;
        letter-spacing: 0.12em;
        margin-top: 12px;
    }
    /* ================================
       카드 정보
    ================================= */
    .album-title {
        color: #f0d3a0;
        font-size: 17px;
        font-weight: bold;
        line-height: 1.3;
        margin-top: 8px;
    }
    .album-artist {
        color: #bb9566;
        font-size: 14px;
        margin-top: 4px;
    }
    .album-meta {
        color: #98734d;
        font-size: 12px;
        margin-top: 5px;
    }
    /* ================================
       추천 카드
    ================================= */
    .recommend-title {
        color: #f2d4a0;
        font-size: 30px;
        font-weight: bold;
        text-align: center;
        letter-spacing: 0.1em;
        margin: 25px 0;
    }
    .hint {
        color: #a9875e;
        text-align: center;
        font-size: 13px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# =========================================================
# 3. Session State
# =========================================================
DEFAULT_STATE = {
    "page": "home",
    "selected_track": None,
    "playing": False,
    "search_query": "",
    "search_results": [],
    "recommend_results": [],
}
for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value
# =========================================================
# 4. iTunes Search API
# =========================================================
@st.cache_data(ttl=600, show_spinner=False)
def search_itunes(term, limit=12):
    """
    Apple iTunes Search API를 이용한 음악 검색.
    Google Cloud / API Key가 필요하지 않음.
    """
    if not term:
        return []
    url = (
        "https://itunes.apple.com/search"
        "?term="
        + quote(term)
        + "&country=kr"
        + "&media=music"
        + "&entity=song"
        + "&limit="
        + str(limit)
        + "&lang=ko_kr"
    )
    try:
        request = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 RECORD-ROOM"
            },
        )
        with urlopen(request, timeout=10) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )
        results = []
        for item in data.get("results", []):
            if not item.get("trackName"):
                continue
            if not item.get("artistName"):
                continue
            if not item.get("artworkUrl100"):
                continue
            results.append(
                {
                    "track_id": item.get(
                        "trackId",
                        hashlib.md5(
                            (
                                item.get("trackName", "")
                                + item.get("artistName", "")
                            ).encode()
                        ).hexdigest(),
                    ),
                    "track_name": item.get(
                        "trackName",
                        "Unknown Track",
                    ),
                    "artist_name": item.get(
                        "artistName",
                        "Unknown Artist",
                    ),
                    "album_name": item.get(
                        "collectionName",
                        "Unknown Album",
                    ),
                    "cover": item.get(
                        "artworkUrl600"
                    )
                    or item.get(
                        "artworkUrl100"
                    ),
                    "cover_small": item.get(
                        "artworkUrl100"
                    ),
                    "preview": item.get(
                        "previewUrl"
                    ),
                    "track_url": item.get(
                        "trackViewUrl"
                    ),
                    "genre": item.get(
                        "primaryGenreName",
                        "Music",
                    ),
                    "release_date": (
                        item.get(
                            "releaseDate",
                            "",
                        )[:10]
                    ),
                }
            )
        return results
    except Exception:
        return []
# =========================================================
# 5. 앨범 커버 다운로드
# =========================================================
@st.cache_data(ttl=3600, show_spinner=False)
def download_cover(url):
    if not url:
        return None
    try:
        request = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 RECORD-ROOM"
            },
        )
        with urlopen(request, timeout=10) as response:
            data = response.read()
        image = Image.open(
            io.BytesIO(data)
        ).convert("RGB")
        return image
    except Exception:
        return None
# =========================================================
# 6. 폰트
# =========================================================
@st.cache_resource
def get_font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(
                path,
                size,
            )
        except Exception:
            pass
    return ImageFont.load_default()
# =========================================================
# 7. LP 만들기
# =========================================================
def make_vinyl(
    cover,
    size=450,
    angle=0,
):
    """
    LP 한 장을 PIL로 제작.
    angle을 바꾸면 회전 프레임을 만들 수 있음.
    """
    canvas = Image.new(
        "RGBA",
        (size, size),
        (0, 0, 0, 0),
    )
    draw = ImageDraw.Draw(canvas)
    center = size // 2
    radius = size // 2 - 10
    # LP 바깥 테두리
    draw.ellipse(
        (
            center - radius,
            center - radius,
            center + radius,
            center + radius,
        ),
        fill=(10, 10, 10, 255),
        outline=(63, 59, 53, 255),
        width=3,
    )
    # 레코드 홈
    for r in range(
        radius - 12,
        65,
        8,
    ):
        shade = 23 + (
            (r // 8) % 3
        ) * 5
        draw.ellipse(
            (
                center - r,
                center - r,
                center + r,
                center + r,
            ),
            outline=(
                shade,
                shade,
                shade,
                255,
            ),
            width=2,
        )
    # 빛 반사
    draw.arc(
        (
            center - radius + 20,
            center - radius + 20,
            center + radius - 20,
            center + radius - 20,
        ),
        start=200,
        end=260,
        fill=(105, 105, 105, 90),
        width=8,
    )
    # 중앙 라벨
    label_radius = 78
    draw.ellipse(
        (
            center - label_radius,
            center - label_radius,
            center + label_radius,
            center + label_radius,
        ),
        fill=(117, 67, 41, 255),
        outline=(212, 165, 98, 255),
        width=3,
    )
    # 앨범 커버
    if cover is not None:
        cover_img = cover.copy()
        cover_img.thumbnail(
            (112, 112),
            Image.Resampling.LANCZOS,
        )
        cover_img = cover_img.resize(
            (112, 112),
            Image.Resampling.LANCZOS,
        )
        mask = Image.new(
            "L",
            (112, 112),
            0,
        )
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse(
            (0, 0, 111, 111),
            fill=255,
        )
        cover_layer = Image.new(
            "RGBA",
            (112, 112),
            (0, 0, 0, 0),
        )
        cover_layer.paste(
            cover_img,
            (0, 0),
            mask,
        )
        canvas.alpha_composite(
            cover_layer,
            (
                center - 56,
                center - 56,
            ),
        )
    # 스핀들
    draw = ImageDraw.Draw(canvas)
    draw.ellipse(
        (
            center - 8,
            center - 8,
            center + 8,
            center + 8,
        ),
        fill=(214, 189, 143, 255),
        outline=(50, 38, 27, 255),
        width=2,
    )
    # 작은 반사점
    draw.ellipse(
        (
            center - 3,
            center - 3,
            center + 3,
            center + 3,
        ),
        fill=(250, 239, 205, 255),
    )
    # 실제 회전
    rotated = canvas.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        expand=False,
    )
    return rotated
# =========================================================
# 8. 레코드바 장면 한 프레임
# =========================================================
def make_player_frame(
    cover,
    track_name,
    artist_name,
    playing=False,
    angle=0,
    width=1000,
    height=690,
):
    """
    나무 레코드바 + 앨범 + LP + 톤암을
    하나의 이미지로 만드는 함수.
    """
    base = Image.new(
        "RGB",
        (width, height),
        (70, 40, 25),
    )
    draw = ImageDraw.Draw(base)
    # ---------------------------------
    # 나무 배경
    # ---------------------------------
    wood_colors = [
        (76, 44, 27),
        (83, 48, 29),
        (69, 38, 24),
        (91, 53, 31),
        (74, 41, 25),
    ]
    plank_height = 58
    for y in range(
        0,
        height,
        plank_height,
    ):
        color = wood_colors[
            (y // plank_height)
            % len(wood_colors)
        ]
        draw.rectangle(
            (
                0,
                y,
                width,
                y + plank_height - 2,
            ),
            fill=color,
        )
        draw.line(
            (
                0,
                y + plank_height - 1,
                width,
                y + plank_height - 1,
            ),
            fill=(42, 24, 15),
            width=2,
        )
    # 나무결
    for x in range(
        20,
        width,
        120,
    ):
        draw.arc(
            (
                x,
                80,
                x + 180,
                height + 80,
            ),
            190,
            350,
            fill=(107, 62, 36),
            width=2,
        )
    # ---------------------------------
    # 상단 텍스트
    # ---------------------------------
    title_font = get_font(28)
    small_font = get_font(16)
    info_font = get_font(18)
    draw.text(
        (35, 25),
        "RECORD ROOM",
        font=title_font,
        fill=(235, 207, 160),
    )
    draw.text(
        (37, 60),
        "VINYL LISTENING ROOM",
        font=small_font,
        fill=(183, 142, 92),
    )
    # ---------------------------------
    # 앨범 커버
    # ---------------------------------
    if cover is not None:
        cover_big = cover.copy()
        cover_big = cover_big.resize(
            (175, 175),
            Image.Resampling.LANCZOS,
        )
        # 그림자
        shadow = Image.new(
            "RGBA",
            (185, 185),
            (0, 0, 0, 0),
        )
        shadow_draw = ImageDraw.Draw(
            shadow
        )
        shadow_draw.rectangle(
            (7, 7, 182, 182),
            fill=(0, 0, 0, 100),
        )
        base.paste(
            shadow,
            (31, 131),
            shadow,
        )
        base.paste(
            cover_big,
            (28, 128),
        )
        # 금속 프레임
        draw.rectangle(
            (
                25,
                125,
                206,
                306,
            ),
            outline=(206, 163, 102),
            width=3,
        )
    # ---------------------------------
    # LP
    # ---------------------------------
    vinyl = make_vinyl(
        cover=cover,
        size=480,
        angle=angle,
    )
    vinyl_position = (
        360,
        155,
    )
    base.paste(
        vinyl,
        vinyl_position,
        vinyl,
    )
    draw = ImageDraw.Draw(base)
    # ---------------------------------
    # 턴테이블 받침
    # ---------------------------------
    draw.rounded_rectangle(
        (
            325,
            130,
            885,
            655,
        ),
        radius=18,
        fill=(47, 29, 20),
        outline=(121, 82, 49),
        width=3,
    )
    # LP를 다시 올려서 받침 위에 보이게
    base.paste(
        vinyl,
        vinyl_position,
        vinyl,
    )
    draw = ImageDraw.Draw(base)
    # ---------------------------------
    # 톤암
    # ---------------------------------
    pivot = (
        820,
        205,
    )
    if playing:
        head = (
            665,
            335,
        )
    else:
        head = (
            715,
            250,
        )
    # pivot shadow
    draw.ellipse(
        (
            pivot[0] - 28,
            pivot[1] - 28,
            pivot[0] + 28,
            pivot[1] + 28,
        ),
        fill=(21, 17, 14),
        outline=(207, 165, 104),
        width=3,
    )
    # 암 바깥쪽
    draw.line(
        [pivot, head],
        fill=(201, 169, 124),
        width=19,
    )
    # 암 안쪽
    draw.line(
        [pivot, head],
        fill=(48, 43, 38),
        width=11,
    )
    # 암 하이라이트
    draw.line(
        [
            (
                pivot[0] - 2,
                pivot[1] - 2,
            ),
            (
                head[0] - 2,
                head[1] - 2,
            ),
        ],
        fill=(226, 203, 167),
        width=3,
    )
    # 헤드
    draw.ellipse(
        (
            head[0] - 17,
            head[1] - 17,
            head[0] + 17,
            head[1] + 17,
        ),
        fill=(36, 33, 29),
        outline=(213, 175, 119),
        width=3,
    )
    # 바늘
    draw.line(
        [
            (
                head[0],
                head[1] + 12,
            ),
            (
                head[0] - 4,
                head[1] + 23,
            ),
        ],
        fill=(226, 206, 169),
        width=3,
    )
    # ---------------------------------
    # 우측 장식
    # ---------------------------------
    draw.rounded_rectangle(
        (
            725,
            480,
            850,
            560,
        ),
        radius=7,
        fill=(37, 24, 17),
        outline=(126, 87, 53),
        width=2,
    )
    status = (
        "● PLAYING"
        if playing
        else "○ PAUSED"
    )
    status_color = (
        (224, 187, 117)
        if playing
        else (154, 121, 82)
    )
    draw.text(
        (745, 498),
        status,
        font=info_font,
        fill=status_color,
    )
    draw.text(
        (745, 525),
        "VINYL DECK",
        font=small_font,
        fill=(143, 108, 73),
    )
    # ---------------------------------
    # 하단 정보
    # ---------------------------------
    draw.text(
        (35, 620),
        track_name[:34],
        font=info_font,
        fill=(239, 215, 177),
    )
    draw.text(
        (35, 647),
        artist_name[:40],
        font=small_font,
        fill=(184, 145, 96),
    )
    return base
# =========================================================
# 9. LP GIF 생성
# =========================================================
@st.cache_data(
    ttl=3600,
    show_spinner=False,
)
def make_player_gif(
    cover_url,
    track_name,
    artist_name,
    playing=True,
):
    """
    JavaScript 없이 LP가 회전하는 것처럼 보이게
    Python/PIL로 GIF를 생성.
    """
    cover = download_cover(
        cover_url
    )
    frames = []
    # 24프레임 = 15도씩 회전
    for angle in range(
        0,
        360,
        15,
    ):
        frame = make_player_frame(
            cover=cover,
            track_name=track_name,
            artist_name=artist_name,
            playing=playing,
            angle=angle,
        )
        frames.append(
            frame.convert("P")
        )
    output = io.BytesIO()
    frames[0].save(
        output,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=70,
        loop=0,
        optimize=False,
    )
    return output.getvalue()
# =========================================================
# 10. 정지된 LP 이미지
# =========================================================
@st.cache_data(
    ttl=3600,
    show_spinner=False,
)
def make_static_player(
    cover_url,
    track_name,
    artist_name,
    playing=False,
):
    cover = download_cover(
        cover_url
    )
    image = make_player_frame(
        cover=cover,
        track_name=track_name,
        artist_name=artist_name,
        playing=playing,
        angle=0,
    )
    output = io.BytesIO()
    image.save(
        output,
        format="PNG",
    )
    return output.getvalue()
# =========================================================
# 11. 페이지 이동 함수
# =========================================================
def go_to(page):
    st.session_state.page = page
def clear_player():
    st.session_state.playing = False
    st.session_state.selected_track = None
# =========================================================
# 12. HOME
# =========================================================
def render_home():
    st.markdown(
        "<div style='height:8vh'></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='room-title'>RECORD ROOM</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='room-subtitle'>오늘의 음악을 한 장의 레코드처럼.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="
            width:140px;
            height:140px;
            margin:35px auto 45px auto;
            border-radius:50%;
            background:
                radial-gradient(circle at center,
                    #c89a5d 0 8%,
                    #1a1715 9% 12%,
                    #252321 13% 18%,
                    #111 19% 100%);
            box-shadow:
                0 20px 45px rgba(0,0,0,.55),
                inset 0 0 20px rgba(255,255,255,.08);
        "></div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )
    with col2:
        if st.button(
            "ENTER ROOM",
            key="enter_room",
            use_container_width=True,
        ):
            st.session_state.page = "choice"
            st.rerun()
# =========================================================
# 13. 선택 화면
# =========================================================
def render_choice():
    st.markdown(
        "<div class='room-title' style='font-size:55px;'>RECORD ROOM</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='room-subtitle'>WHAT WOULD YOU LIKE TO DO?</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='wood-panel'>",
        unsafe_allow_html=True,
    )
    left, right = st.columns(
        2,
        gap="large",
    )
    with left:
        st.markdown(
            """
            <div style="
                text-align:center;
                color:#d8b986;
                font-size:65px;
                margin-bottom:10px;
            ">♫</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "노래 듣기",
            key="listen_menu",
            use_container_width=True,
        ):
            st.session_state.page = "listen"
            st.session_state.search_query = ""
            st.session_state.search_results = search_itunes(
                "아이유",
                12,
            )
            st.rerun()
    with right:
        st.markdown(
            """
            <div style="
                text-align:center;
                color:#d8b986;
                font-size:65px;
                margin-bottom:10px;
            ">✦</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "노래 추천받기",
            key="recommend_menu",
            use_container_width=True,
        ):
            st.session_state.page = "recommend"
            st.session_state.recommend_results = []
            st.rerun()
    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='height:20px'></div>",
        unsafe_allow_html=True,
    )
    if st.button(
        "← 처음 화면",
        key="back_home_choice",
    ):
        st.session_state.page = "home"
        st.rerun()
# =========================================================
# 14. 앨범 카드
# =========================================================
def render_track_card(
    track,
    index,
):
    cover = track.get(
        "cover",
        track.get("cover_small"),
    )
    if cover:
        st.image(
            cover,
            use_container_width=True,
        )
    else:
        st.markdown(
            """
            <div style="
                height:220px;
                background:#21150e;
                border:1px solid #765334;
                display:flex;
                align-items:center;
                justify-content:center;
                color:#b99363;
            ">NO COVER</div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown(
        f"""
        <div class="album-title">
            {track['track_name']}
        </div>
        <div class="album-artist">
            {track['artist_name']}
        </div>
        <div class="album-meta">
            {track['album_name']}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='height:6px'></div>",
        unsafe_allow_html=True,
    )
    if st.button(
        "앨범 선택",
        key=f"select_album_{track['track_id']}_{index}",
        use_container_width=True,
    ):
        st.session_state.selected_track = track
        st.session_state.playing = False
        st.rerun()
# =========================================================
# 15. 노래 듣기
# =========================================================
def render_listen():
    top_left, top_right = st.columns(
        [1, 6]
    )
    with top_left:
        if st.button(
            "← 선택",
            key="back_choice_listen",
        ):
            st.session_state.playing = False
            st.session_state.selected_track = None
            st.session_state.page = "choice"
            st.rerun()
    with top_right:
        st.markdown(
            "<div class='small-logo'>RECORD ROOM / MUSIC LIBRARY</div>",
            unsafe_allow_html=True,
        )
    # ---------------------------------
    # 검색
    # ---------------------------------
    search_col, button_col = st.columns(
        [5, 1],
        vertical_alignment="bottom",
    )
    with search_col:
        query = st.text_input(
            "음악 검색",
            value=st.session_state.search_query,
            placeholder="가수, 노래 제목을 검색해보세요",
            label_visibility="collapsed",
            key="music_search_input",
        )
    with button_col:
        search_clicked = st.button(
            "SEARCH",
            key="search_music",
            use_container_width=True,
        )
    if search_clicked:
        if query.strip():
            with st.spinner(
                "레코드 선반을 뒤지는 중..."
            ):
                results = search_itunes(
                    query.strip(),
                    12,
                )
            st.session_state.search_query = (
                query.strip()
            )
            st.session_state.search_results = results
        else:
            st.session_state.search_results = []
        st.rerun()
    # ---------------------------------
    # 선택된 앨범
    # ---------------------------------
    selected = (
        st.session_state.selected_track
    )
    if selected:
        st.markdown(
            "<div style='height:25px'></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="wood-panel">
            """,
            unsafe_allow_html=True,
        )
        left, middle, right = st.columns(
            [1.2, 2.5, 1.2],
            vertical_alignment="center",
        )
        with left:
            st.image(
                selected["cover"],
                use_container_width=True,
            )
        with middle:
            st.markdown(
                "<div class='small-logo'>SELECTED RECORD</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="track-name">
                    {selected['track_name']}
                </div>
                <div class="artist-name">
                    {selected['artist_name']}
                </div>
                <div style="
                    color:#96704b;
                    margin-top:8px;
                ">
                    {selected['album_name']}
                </div>
                <div style="
                    color:#866343;
                    font-size:12px;
                    margin-top:14px;
                ">
                    아직 재생되지 않았어요.
                    LP에 올려야 음악을 들을 수 있습니다.
                </div>
                """,
                unsafe_allow_html=True,
            )
        with right:
            if st.button(
                "LP에 올리기",
                key="load_lp",
                use_container_width=True,
            ):
                st.session_state.playing = False
                st.session_state.page = "player"
                st.rerun()
        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='height:30px'></div>",
            unsafe_allow_html=True,
        )
    # ---------------------------------
    # 결과
    # ---------------------------------
    results = (
        st.session_state.search_results
    )
    if not results:
        st.markdown(
            """
            <div class="wood-panel"
                 style="text-align:center; padding:60px;">
                <div style="
                    font-size:32px;
                    color:#d8b986;
                    margin-bottom:12px;
                ">
                    ♫
                </div>
                <div style="
                    color:#b58c5b;
                    font-size:16px;
                ">
                    듣고 싶은 노래나 가수를 검색해보세요.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return
    st.markdown(
        f"""
        <div style="
            color:#c79b67;
            margin:20px 0;
            letter-spacing:.12em;
        ">
            RECORDS / {len(results)}
        </div>
        """,
        unsafe_allow_html=True,
    )
    # 4열
    for start in range(
        0,
        len(results),
        4,
    ):
        row = results[
            start:start + 4
        ]
        columns = st.columns(
            len(row),
            gap="medium",
        )
        for index, (
            column,
            track,
        ) in enumerate(
            zip(columns, row)
        ):
            with column:
                st.markdown(
                    """
                    <div style="
                        background:
                            linear-gradient(
                                145deg,
                                rgba(74,42,25,.88),
                                rgba(40,22,13,.92)
                            );
                        border:
                            1px solid rgba(190,145,91,.3);
                        padding:12px;
                        border-radius:5px;
                        box-shadow:
                            0 10px 25px rgba(0,0,0,.28);
                    ">
                    """,
                    unsafe_allow_html=True,
                )
                render_track_card(
                    track,
                    start + index,
                )
                st.markdown(
                    "</div>",
                    unsafe_allow_html=True,
                )
# =========================================================
# 16. 추천 페이지
# =========================================================
def render_recommend():
    if st.button(
        "← 선택 화면",
        key="back_choice_recommend",
    ):
        st.session_state.page = "choice"
        st.rerun()
    st.markdown(
        "<div class='recommend-title'>오늘은 어떤 음악?</div>",
        unsafe_allow_html=True,
    )
    moods = {
        "설레는 날": "K-pop love",
        "새벽 감성": "Korean ballad",
        "드라이브": "Korean hip hop",
        "기분전환": "K-pop",
        "잔잔하게": "Korean indie",
    }
    columns = st.columns(
        5,
        gap="small",
    )
    for column, mood in zip(
        columns,
        moods.keys(),
    ):
        with column:
            if st.button(
                mood,
                key=f"mood_{mood}",
                use_container_width=True,
            ):
                with st.spinner(
                    "오늘의 레코드를 고르는 중..."
                ):
                    results = search_itunes(
                        moods[mood],
                        8,
                    )
                st.session_state.recommend_results = results
                st.rerun()
    results = (
        st.session_state.recommend_results
    )
    if not results:
        st.markdown(
            """
            <div class="wood-panel"
                 style="
                    margin-top:35px;
                    text-align:center;
                    padding:60px 20px;
                 ">
                <div style="
                    font-size:42px;
                    color:#d7b178;
                ">
                    ♫
                </div>
                <div style="
                    margin-top:15px;
                    color:#c29a67;
                    font-size:16px;
                ">
                    오늘의 기분을 하나 골라주세요.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return
    st.markdown(
        "<div style='height:30px'></div>",
        unsafe_allow_html=True,
    )
    for start in range(
        0,
        len(results),
        4,
    ):
        row = results[
            start:start + 4
        ]
        columns = st.columns(
            len(row),
            gap="medium",
        )
        for index, (
            column,
            track,
        ) in enumerate(
            zip(columns, row)
        ):
            with column:
                st.markdown(
                    """
                    <div style="
                        background:
                            linear-gradient(
                                145deg,
                                rgba(74,42,25,.88),
                                rgba(40,22,13,.92)
                            );
                        border:
                            1px solid rgba(190,145,91,.3);
                        padding:12px;
                        border-radius:5px;
                    ">
                    """,
                    unsafe_allow_html=True,
                )
                render_track_card(
                    track,
                    start + index + 100,
                )
                st.markdown(
                    "</div>",
                    unsafe_allow_html=True,
                )
# =========================================================
# 17. LP 플레이어
# =========================================================
def render_player():
    track = (
        st.session_state.selected_track
    )
    if not track:
        st.session_state.page = "listen"
        st.rerun()
        return
    # ---------------------------------
    # 상단 뒤로가기
    # ---------------------------------
    back_col, title_col = st.columns(
        [1, 5]
    )
    with back_col:
        if st.button(
            "← 레코드 선반",
            key="back_listen_player",
        ):
            st.session_state.playing = False
            st.session_state.page = "listen"
            st.rerun()
    with title_col:
        st.markdown(
            "<div class='small-logo'>RECORD ROOM / VINYL PLAYER</div>",
            unsafe_allow_html=True,
        )
    # ---------------------------------
    # 플레이어 이미지
    # ---------------------------------
    if st.session_state.playing:
        gif_bytes = make_player_gif(
            track["cover"],
            track["track_name"],
            track["artist_name"],
            True,
        )
        st.image(
            gif_bytes,
            use_container_width=True,
        )
    else:
        static_bytes = make_static_player(
            track["cover"],
            track["track_name"],
            track["artist_name"],
            False,
        )
        st.image(
            static_bytes,
            use_container_width=True,
        )
    # ---------------------------------
    # 정보
    # ---------------------------------
    st.markdown(
        f"""
        <div class="now-playing">
            <div class="track-name">
                {track['track_name']}
            </div>
            <div class="artist-name">
                {track['artist_name']}
            </div>
            <div style="
                color:#96704b;
                margin-top:5px;
            ">
                {track['album_name']}
            </div>
            <div class="status-playing">
                {
                    "● NOW SPINNING"
                    if st.session_state.playing
                    else "○ NEEDLE UP"
                }
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='height:18px'></div>",
        unsafe_allow_html=True,
    )
    # ---------------------------------
    # 톤암 버튼
    # ---------------------------------
    tonearm_text = (
        "↗  톤암 올리기 · 정지"
        if st.session_state.playing
        else "↘  톤암 내리기 · 재생"
    )
    if st.button(
        tonearm_text,
        key="tonearm_toggle",
        use_container_width=True,
    ):
        st.session_state.playing = (
            not st.session_state.playing
        )
        st.rerun()
    st.markdown(
        """
        <div class="hint">
            톤암을 내리면 레코드가 회전하고 음악이 재생됩니다.
            다시 올리면 정지합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )
    # ---------------------------------
    # 오디오
    # ---------------------------------
    if st.session_state.playing:
        preview_url = track.get(
            "preview"
        )
        if preview_url:
            st.markdown(
                "<div style='height:18px'></div>",
                unsafe_allow_html=True,
            )
            st.audio(
                preview_url,
                format="audio/mp4",
                autoplay=True,
                loop=False,
            )
            st.markdown(
                """
                <div class="hint">
                    Apple Music/iTunes에서 제공하는 미리듣기입니다.
                    브라우저가 자동재생을 막는 경우 아래 플레이어의 ▶ 버튼을 눌러주세요.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning(
                "이 곡은 미리듣기 음원이 제공되지 않습니다."
            )
    # ---------------------------------
    # 앨범 바꾸기
    # ---------------------------------
    st.markdown(
        "<div style='height:20px'></div>",
        unsafe_allow_html=True,
    )
    if st.button(
        "다른 레코드 고르기",
        key="change_record",
        use_container_width=True,
    ):
        st.session_state.playing = False
        st.session_state.page = "listen"
        st.rerun()
# =========================================================
# 18. 페이지 라우팅
# =========================================================
page = st.session_state.page
if page == "home":
    render_home()
elif page == "choice":
    render_choice()
elif page == "listen":
    render_listen()
elif page == "recommend":
    render_recommend()
elif page == "player":
    render_player()
else:
    st.session_state.page = "home"
    st.rerun()
