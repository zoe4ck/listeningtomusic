import html
import json
import re
from typing import Any, Dict, List

import requests
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# RECORD ROOM
# One-file Streamlit app
# - Vintage wood record-bar design
# - iTunes Search API
# - Drag an album card onto the vinyl -> preview starts
# - Click vinyl -> play/pause
# - Double-click vinyl -> stop
# - No bottom playback bar / no tonearm
# =========================================================


st.set_page_config(
    page_title="RECORD ROOM",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# THEME CSS
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@500;600;700&display=swap');

    :root{
        --wood-dark:#24150e;
        --wood:#4d2d1d;
        --wood-mid:#694128;
        --wood-light:#8a5a35;
        --cream:#f1dfc1;
        --cream-soft:#e6cfaa;
        --gold:#c6a06b;
        --gold-light:#e8c88e;
        --ink:#23150e;
        --muted:#b99a74;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"]{
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
            linear-gradient(
                180deg,
                #3a2115 0%,
                #25150e 52%,
                #1b0f0a 100%
            );
        color: var(--cream);
    }

    [data-testid="stHeader"]{
        background:transparent;
    }

    [data-testid="stToolbar"]{
        display:none;
    }

    [data-testid="stSidebar"]{
        display:none;
    }

    .block-container{
        padding:1.3rem 2rem 2.5rem !important;
        max-width:1400px;
    }

    div[data-testid="stTextInput"] input{
        background:rgba(19,10,6,.66) !important;
        color:#f4e7cf !important;
        border:1px solid rgba(210,173,117,.50) !important;
        border-radius:13px !important;
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,.04),
            0 8px 30px rgba(0,0,0,.18);
        min-height:48px !important;
        font-family:'DM Mono', monospace !important;
    }

    div[data-testid="stTextInput"] label{
        color:#c5a67d !important;
    }

    .stButton > button{
        width:100%;
        border:1px solid rgba(214,174,116,.45) !important;
        background:
            linear-gradient(
                180deg,
                rgba(118,72,44,.96),
                rgba(66,38,24,.96)
            ) !important;
        color:#f6e8ce !important;
        border-radius:12px !important;
        font-family:'DM Mono', monospace !important;
        letter-spacing:.05em;
        padding:.72rem 1rem !important;
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,.06),
            0 9px 24px rgba(0,0,0,.18);
        transition:.18s ease;
    }

    .stButton > button:hover{
        border-color:rgba(232,200,142,.72) !important;
        transform:translateY(-1px);
        filter:brightness(1.08);
    }

    .stButton > button:focus{
        box-shadow:
            0 0 0 2px rgba(232,200,142,.18) !important;
    }

    .rr-topline{
        border-top:1px solid rgba(215,177,119,.18);
        margin:6px 0 22px;
    }

    .rr-brand{
        display:flex;
        align-items:flex-end;
        justify-content:space-between;
        gap:20px;
        padding:2px 4px 10px;
    }

    .rr-brand-title{
        font-family:'Cinzel', serif;
        font-size:clamp(30px, 4vw, 46px);
        letter-spacing:.17em;
        color:#f0dfc2;
        text-shadow:0 2px 12px rgba(0,0,0,.35);
    }

    .rr-brand-sub{
        font-family:'DM Mono', monospace;
        color:#aa8b67;
        font-size:11px;
        letter-spacing:.09em;
        text-align:right;
    }

    .rr-rule{
        height:1px;
        margin:0 0 18px;
        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(209,171,112,.48),
                transparent
            );
    }

    .rr-kicker{
        font-family:'DM Mono', monospace;
        text-transform:uppercase;
        color:#bd9c6d;
        font-size:10px;
        letter-spacing:.15em;
    }

    .rr-title{
        font-family:'Playfair Display', serif;
        font-size:clamp(28px,4vw,48px);
        line-height:1.02;
        margin-top:7px;
        color:#f1dfc1;
    }

    .rr-copy{
        color:#bfa383;
        line-height:1.75;
        font-family:'DM Mono', monospace;
        font-size:12px;
        max-width:650px;
    }

    .rr-home-card{
        position:relative;
        min-height:56vh;
        display:flex;
        flex-direction:column;
        justify-content:center;
        padding:2rem clamp(1rem,6vw,6rem);
        border:1px solid rgba(208,169,111,.2);
        border-radius:26px;
        overflow:hidden;
        background:
            radial-gradient(
                circle at 72% 28%,
                rgba(228,191,131,.13),
                transparent 22%
            ),
            linear-gradient(
                145deg,
                rgba(106,63,39,.52),
                rgba(25,13,8,.7)
            );
        box-shadow:
            0 28px 80px rgba(0,0,0,.28),
            inset 0 1px 0 rgba(255,255,255,.025);
    }

    .rr-home-card:before{
        content:"";
        position:absolute;
        inset:18px;
        border:1px solid rgba(224,190,138,.09);
        border-radius:20px;
        pointer-events:none;
    }

    .rr-home-note{
        margin-top:16px;
        color:#987754;
        font-family:'DM Mono', monospace;
        font-size:10px;
        letter-spacing:.12em;
    }

    @media(max-width:760px){
        .block-container{
            padding:.8rem 1rem 2rem !important;
        }

        .rr-brand{
            align-items:flex-start;
        }

        .rr-brand-sub{
            text-align:left;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "search_term" not in st.session_state:
    st.session_state.search_term = ""

if "results" not in st.session_state:
    st.session_state.results = []


# =========================================================
# NAVIGATION
# =========================================================

def go(page: str):
    st.session_state.page = page
    st.rerun()


# =========================================================
# SEARCH HELPERS
# =========================================================

def normalized(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^0-9a-zA-Z가-힣]+", "", s)
    return s


def artwork_large(url: str) -> str:
    if not url:
        return ""

    return (
        url
        .replace("100x100bb", "600x600bb")
        .replace("100x100-75", "600x600-75")
    )


def normalize_track(item: Dict[str, Any]) -> Dict[str, str]:
    return {
        "track": item.get("trackName") or "Untitled",
        "artist": item.get("artistName") or "Unknown Artist",
        "album": item.get("collectionName") or "Single",
        "cover": artwork_large(
            item.get("artworkUrl100") or ""
        ),
        "preview": item.get("previewUrl") or "",
        "url": item.get("trackViewUrl") or "",
    }


# =========================================================
# ITUNES API
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def api_get(
    url: str,
    params: Dict[str, Any]
) -> Dict[str, Any]:

    response = requests.get(
        url,
        params=params,
        timeout=8,
        headers={
            "User-Agent": "RECORD ROOM/1.0"
        },
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# ARTIST SEARCH
# =========================================================

def artist_search(
    term: str
) -> List[Dict[str, str]]:

    out: List[Dict[str, str]] = []

    # 한국 + 미국 스토어 둘 다 검색
    for country in ("kr", "us"):

        try:

            data = api_get(
                "https://itunes.apple.com/search",
                {
                    "term": term,
                    "country": country,
                    "media": "music",
                    "entity": "musicArtist",
                    "limit": 8,
                },
            )

            for item in data.get("results", []):

                name = item.get("artistName") or ""

                if name:

                    out.append(
                        {
                            "id": str(
                                item.get("artistId") or ""
                            ),
                            "artist": name,
                        }
                    )

        except Exception:
            pass

    # 중복 제거
    seen = set()
    unique = []

    for item in out:

        key = (
            item["id"],
            normalized(item["artist"])
        )

        if key not in seen:

            seen.add(key)
            unique.append(item)

    return unique


# =========================================================
# ARTIST TRACK LOOKUP
# =========================================================

def artist_tracks(
    artist_id: str
) -> List[Dict[str, str]]:

    out: List[Dict[str, str]] = []

    if not artist_id:
        return out

    # 한국 + 미국 스토어 둘 다 확인
    for country in ("kr", "us"):

        try:

            data = api_get(
                "https://itunes.apple.com/lookup",
                {
                    "id": artist_id,
                    "entity": "song",
                    "country": country,
                    "limit": 30,
                    "sort": "recent",
                },
            )

            for item in data.get("results", []):

                if item.get("kind") == "song":

                    out.append(
                        normalize_track(item)
                    )

        except Exception:
            pass

    return out


# =========================================================
# SONG SEARCH
# =========================================================

def song_search(
    term: str,
    attribute: str = ""
) -> List[Dict[str, str]]:

    out: List[Dict[str, str]] = []

    # 한국 + 미국
    for country in ("kr", "us"):

        try:

            params = {
                "term": term,
                "country": country,
                "media": "music",
                "entity": "song",
                "limit": 100,
            }

            # ★ 핵심 수정
            #
            # attribute="artistTerm"이면
            # 검색어를 노래 제목에서만 찾는 것이 아니라
            # 실제 아티스트 이름 기준으로 검색한다.
            #
            # 예:
            # 지코
            # 아이유
            # 뉴진스
            #
            # 등을 검색했을 때 해당 가수의 곡을 가져온다.
            if attribute:
                params["attribute"] = attribute

            data = api_get(
                "https://itunes.apple.com/search",
                params,
            )

            for item in data.get("results", []):

                if item.get("kind") == "song":

                    out.append(
                        normalize_track(item)
                    )

        except Exception:
            pass

    return out


# =========================================================
# SEARCH RESULT SCORING
# =========================================================

def score_result(
    term: str,
    item: Dict[str, str]
) -> int:

    query = normalized(term)

    artist = normalized(
        item["artist"]
    )

    track = normalized(
        item["track"]
    )

    album = normalized(
        item["album"]
    )

    score = 0

    # 가수 이름 정확히 일치
    if artist == query:
        score += 1000

    # 곡 제목 정확히 일치
    if track == query:
        score += 920

    # 가수 이름에 검색어 포함
    if query and query in artist:
        score += 430

    # 곡 제목에 검색어 포함
    if query and query in track:
        score += 410

    # 앨범명에 검색어 포함
    if query and query in album:
        score += 120

    # 아무 관련 없는 결과는 낮춤
    if (
        query
        and query not in artist
        and query not in track
        and query not in album
    ):
        score -= 250

    return score


# =========================================================
# MAIN MUSIC SEARCH
# =========================================================

def search_music(
    term: str
) -> List[Dict[str, str]]:

    term = term.strip()

    if not term:
        return []

    candidates: List[
        Dict[str, str]
    ] = []

    query_normalized = normalized(term)

    # -----------------------------------------------------
    # 1. ★ 가수 이름 전용 검색
    # -----------------------------------------------------
    #
    # 기존 검색은 단순히
    #
    #     term = "지코"
    #
    # 로 검색했기 때문에 API 결과가 상황에 따라
    # 노래 제목 위주로 잡힐 수 있었다.
    #
    # 이제 artistTerm을 명시해서
    # "지코라는 가수가 부른 노래"를 먼저 찾는다.
    #

    artist_song_candidates = song_search(
        term,
        attribute="artistTerm"
    )

    exact_artist_songs = [
        item
        for item in artist_song_candidates
        if normalized(item["artist"])
        == query_normalized
    ]

    if exact_artist_songs:

        candidates.extend(
            exact_artist_songs
        )

    else:

        # 정확히 일치하지 않더라도
        # 검색어가 가수 이름에 포함된 결과를 사용
        candidates.extend(
            artist_song_candidates
        )

    # -----------------------------------------------------
    # 2. 기존 아티스트 검색 방식도 보조로 사용
    # -----------------------------------------------------

    artist_candidates = artist_search(term)

    for artist in artist_candidates[:4]:

        name_normalized = normalized(
            artist["artist"]
        )

        if (
            query_normalized == name_normalized
            or query_normalized in name_normalized
            or name_normalized in query_normalized
        ):

            candidates.extend(
                artist_tracks(
                    artist["id"]
                )
            )

    # -----------------------------------------------------
    # 3. 일반 노래 검색
    # -----------------------------------------------------

    candidates.extend(
        song_search(term)
    )

    # -----------------------------------------------------
    # 4. 혹시 결과가 없으면 아티스트 첫 결과를
    #    한 번 더 조회
    # -----------------------------------------------------

    if (
        not candidates
        and artist_candidates
    ):

        candidates.extend(
            artist_tracks(
                artist_candidates[0]["id"]
            )
        )

    # -----------------------------------------------------
    # 5. 중복 제거
    # -----------------------------------------------------

    unique: Dict[
        str,
        Dict[str, str]
    ] = {}

    for item in candidates:

        key = (
            normalized(item["artist"])
            + "|"
            + normalized(item["track"])
        )

        # 미리듣기 주소가 있는 곡만 사용
        if (
            item["preview"]
            and key not in unique
        ):

            unique[key] = item

    results = list(
        unique.values()
    )

    # -----------------------------------------------------
    # 6. 관련성이 높은 결과부터 정렬
    # -----------------------------------------------------

    results.sort(
        key=lambda item:
            score_result(term, item),
        reverse=True
    )

    return results[:24]


@st.cache_data(
    ttl=900,
    show_spinner=False
)
def seed_search(
    term: str
) -> List[Dict[str, str]]:

    return search_music(term)


# =========================================================
# HEADER
# =========================================================

def render_header(
    section: str
):

    st.markdown(
        f"""
        <div class="rr-brand">
            <div>
                <div class="rr-brand-title">
                    RECORD ROOM
                </div>

                <div class="rr-kicker">
                    {html.escape(section)}
                </div>
            </div>

            <div class="rr-brand-sub">
                VINYL · LISTEN · DISCOVER
            </div>
        </div>

        <div class="rr-rule"></div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# MUSIC PLAYER COMPONENT
# =========================================================

def track_cards_component(
    tracks: List[Dict[str, str]],
    key_suffix: str = "main"
):

    # JSON 안전 처리
    data = (
        json.dumps(
            tracks,
            ensure_ascii=False
        )
        .replace(
            "</",
            "<\\/"
        )
    )

    component_html = f"""
<!doctype html>

<html lang="ko">

<head>

<meta charset="utf-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1"
>

<style>

*{{
    box-sizing:border-box;
}}

body{{
    margin:0;
    padding:0;
    color:#f2dfbf;
    background:transparent;
    font-family:Arial, Helvetica, sans-serif;
}}


/* =====================================================
   ROOM
   ===================================================== */

.room{{
    border:1px solid rgba(224,188,137,.18);

    border-radius:22px;

    background:
        linear-gradient(
            180deg,
            rgba(77,45,28,.72),
            rgba(33,18,11,.84)
        ),
        repeating-linear-gradient(
            90deg,
            rgba(255,255,255,.02) 0 2px,
            transparent 2px 14px
        );

    box-shadow:
        0 22px 70px rgba(0,0,0,.27),
        inset 0 1px 0 rgba(255,255,255,.03);

    padding:22px;

    overflow:hidden;
}}


/* =====================================================
   LABEL
   ===================================================== */

.label{{
    font-size:10px;

    letter-spacing:.17em;

    color:#b99567;

    text-transform:uppercase;

    font-family:monospace;

    margin-bottom:8px;
}}


.hint{{
    font-size:11px;

    line-height:1.7;

    color:#9c7d59;

    font-family:monospace;

    margin-bottom:18px;
}}


/* =====================================================
   STUDIO
   ===================================================== */

.studio{{
    display:grid;

    grid-template-columns:
        minmax(0, 1.18fr)
        minmax(310px,.82fr);

    gap:18px;

    align-items:stretch;
}}


/* =====================================================
   DECK
   ===================================================== */

.deck{{
    min-height:530px;

    position:relative;

    border-radius:18px;

    border:1px solid rgba(222,190,143,.16);

    background:
        radial-gradient(
            circle at 50% 40%,
            rgba(171,111,60,.18),
            transparent 28%
        ),
        linear-gradient(
            145deg,
            #6e4328,
            #402513 62%,
            #2a170d
        );

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.03),
        inset 0 -20px 50px rgba(0,0,0,.18);

    overflow:hidden;
}}


.deck::before{{
    content:"";

    position:absolute;

    inset:12px;

    border:
        1px solid
        rgba(231,200,153,.09);

    border-radius:14px;

    pointer-events:none;
}}


.deck-top{{
    position:absolute;

    top:16px;
    left:18px;
    right:18px;

    display:flex;

    justify-content:space-between;

    align-items:center;

    font-family:monospace;

    font-size:9px;

    letter-spacing:.16em;

    color:#b89568;

    text-transform:uppercase;
}}


.deck-mark{{
    color:#d5b27b;
}}


/* =====================================================
   VINYL AREA
   ===================================================== */

.vinyl-wrap{{
    position:absolute;

    inset:72px 0 68px;

    display:flex;

    align-items:center;

    justify-content:center;
}}


/* =====================================================
   VINYL
   ===================================================== */

.vinyl{{
    width:min(62vw,390px);

    height:min(62vw,390px);

    max-width:390px;
    max-height:390px;

    min-width:230px;
    min-height:230px;

    position:relative;

    border-radius:50%;

    cursor:pointer;

    user-select:none;

    background:
        radial-gradient(
            circle at 35% 29%,
            rgba(255,255,255,.12),
            transparent 12%
        ),
        repeating-radial-gradient(
            circle at center,
            #161616 0 2px,
            #202020 2px 4px,
            #121212 4px 6px
        ),
        #151515;

    box-shadow:
        0 22px 55px rgba(0,0,0,.42),
        inset -12px -12px 25px rgba(0,0,0,.45),
        inset 10px 10px 18px rgba(255,255,255,.025);

    transition:
        transform .22s ease,
        box-shadow .22s ease;
}}


.vinyl:hover{{
    transform:scale(1.012);
}}


.vinyl.spinning{{
    animation:
        spin 1.8s linear infinite;
}}


@keyframes spin{{
    to{{
        transform:rotate(360deg);
    }}
}}


/* =====================================================
   CENTER LABEL
   ===================================================== */

.label-disc{{
    position:absolute;

    width:31%;
    height:31%;

    left:34.5%;
    top:34.5%;

    border-radius:50%;

    overflow:hidden;

    border:7px solid #1b1b1b;

    box-shadow:
        0 0 0 1px rgba(255,255,255,.07),
        0 3px 12px rgba(0,0,0,.35);

    background:#7f5d42;
}}


.label-disc img{{
    width:100%;
    height:100%;

    object-fit:cover;

    display:block;
}}


/* =====================================================
   SPINDLE
   ===================================================== */

.spindle{{
    position:absolute;

    left:48%;
    top:48%;

    width:4%;
    height:4%;

    min-width:8px;
    min-height:8px;

    border-radius:50%;

    background:#d8c29d;

    box-shadow:
        0 0 0 2px #343434,
        0 1px 5px rgba(0,0,0,.45);
}}


/* =====================================================
   DROP RING
   ===================================================== */

.drop-ring{{
    position:absolute;

    left:11%;
    top:11%;

    width:78%;
    height:78%;

    border-radius:50%;

    border:
        1px dashed
        rgba(215,180,132,.14);

    pointer-events:none;
}}


/* =====================================================
   DECK BOTTOM
   ===================================================== */

.deck-bottom{{
    position:absolute;

    left:18px;
    right:18px;
    bottom:16px;

    display:flex;

    align-items:center;

    justify-content:space-between;

    gap:14px;

    font-family:monospace;
}}


.status{{
    font-size:10px;

    color:#b99668;

    letter-spacing:.08em;
}}


.track-now{{
    font-size:11px;

    color:#ead8bb;

    white-space:nowrap;

    overflow:hidden;

    text-overflow:ellipsis;

    max-width:70%;
}}


/* =====================================================
   CARDS
   ===================================================== */

.cards{{
    display:grid;

    grid-template-columns:
        repeat(
            3,
            minmax(0,1fr)
        );

    gap:10px;

    max-height:530px;

    overflow:auto;

    padding-right:4px;

    scrollbar-width:thin;
}}


.cards::-webkit-scrollbar{{
    width:6px;
}}


.cards::-webkit-scrollbar-thumb{{
    background:#785033;

    border-radius:20px;
}}


/* =====================================================
   CARD
   ===================================================== */

.card{{
    background:
        linear-gradient(
            180deg,
            #51301e,
            #321b10
        );

    border:
        1px solid
        rgba(220,184,131,.15);

    border-radius:14px;

    padding:9px;

    cursor:grab;

    min-width:0;

    transition:.18s ease;

    box-shadow:
        0 10px 24px
        rgba(0,0,0,.18);
}}


.card:hover{{
    transform:translateY(-2px);

    border-color:
        rgba(229,196,144,.3);
}}


.card:active{{
    cursor:grabbing;
}}


/* =====================================================
   COVER
   ===================================================== */

.cover{{
    width:100%;

    aspect-ratio:1/1;

    border-radius:10px;

    object-fit:cover;

    display:block;

    background:#29170d;

    box-shadow:
        0 8px 18px
        rgba(0,0,0,.28);
}}


/* =====================================================
   META
   ===================================================== */

.meta{{
    padding:8px 2px 2px;
}}


.song{{
    font-size:11px;

    font-weight:700;

    line-height:1.35;

    color:#ead8ba;

    white-space:nowrap;

    overflow:hidden;

    text-overflow:ellipsis;
}}


.artist{{
    font-size:9px;

    line-height:1.5;

    color:#a98b68;

    white-space:nowrap;

    overflow:hidden;

    text-overflow:ellipsis;
}}


.small-tag{{
    font-size:8px;

    color:#816448;

    margin-top:5px;

    font-family:monospace;

    letter-spacing:.08em;
}}


/* =====================================================
   EMPTY
   ===================================================== */

.empty{{
    min-height:260px;

    display:flex;

    align-items:center;

    justify-content:center;

    border:
        1px dashed
        rgba(220,188,142,.14);

    border-radius:14px;

    color:#9d7e5b;

    font:
        12px/1.8
        monospace;

    text-align:center;

    padding:25px;
}}


/* =====================================================
   MESSAGE
   ===================================================== */

.message{{
    position:absolute;

    left:50%;

    bottom:58px;

    transform:
        translateX(-50%);

    font:
        10px/1.4
        monospace;

    letter-spacing:.05em;

    color:#c5a374;

    background:
        rgba(28,14,8,.82);

    border:
        1px solid
        rgba(222,189,140,.16);

    padding:7px 11px;

    border-radius:999px;

    opacity:0;

    pointer-events:none;

    transition:.18s ease;
}}


.message.show{{
    opacity:1;
}}


/* =====================================================
   RESPONSIVE
   ===================================================== */

@media(max-width:920px){{

    .studio{{
        grid-template-columns:1fr;
    }}

    .deck{{
        min-height:480px;
    }}

    .cards{{
        max-height:none;
    }}

    .track-now{{
        max-width:62%;
    }}
}}


@media(max-width:600px){{

    .room{{
        padding:14px;
    }}

    .cards{{
        grid-template-columns:
            repeat(
                2,
                minmax(0,1fr)
            );

        gap:8px;
    }}

    .deck{{
        min-height:400px;
    }}

    .vinyl-wrap{{
        inset:60px 0 58px;
    }}

    .vinyl{{
        min-width:205px;
        min-height:205px;
    }}
}}

</style>

</head>


<body>

<div class="room">

    <div class="label">
        RECORD PLAYER / LIVE PREVIEW
    </div>

    <div class="hint">
        앨범 카드를 잡아서 왼쪽 LP 위에 놓으세요.
        · LP 한 번 클릭 = 재생/일시정지
        · 두 번 클릭 = 정지
    </div>


    <div class="studio">


        <!-- =========================================
             RECORD PLAYER
             ========================================= -->

        <section
            class="deck"
            id="deck"
        >

            <div class="deck-top">

                <span>
                    RR / 01
                </span>

                <span class="deck-mark">
                    DRAG TO PLAY
                </span>

            </div>


            <div class="vinyl-wrap">

                <div
                    class="vinyl"
                    id="vinyl"
                    title="한 번 클릭: 재생/일시정지 · 두 번 클릭: 정지"
                >

                    <div class="drop-ring"></div>

                    <div
                        class="label-disc"
                        id="labelDisc"
                    ></div>

                    <div class="spindle"></div>

                </div>

            </div>


            <div
                class="message"
                id="message"
            >
                이 곡은 미리듣기가 없습니다.
            </div>


            <div class="deck-bottom">

                <div
                    class="status"
                    id="status"
                >
                    READY
                </div>

                <div
                    class="track-now"
                    id="trackNow"
                >
                    앨범을 LP 위로 끌어다 놓아주세요.
                </div>

            </div>

        </section>


        <!-- =========================================
             RECORD CARDS
             ========================================= -->

        <section>

            <div
                class="cards"
                id="cards"
            ></div>

        </section>


    </div>

</div>


<script>


// =====================================================
// DATA
// =====================================================

const TRACKS = {data};


// =====================================================
// ELEMENTS
// =====================================================

const cardsEl =
    document.getElementById("cards");

const vinyl =
    document.getElementById("vinyl");

const deck =
    document.getElementById("deck");

const labelDisc =
    document.getElementById("labelDisc");

const statusEl =
    document.getElementById("status");

const trackNow =
    document.getElementById("trackNow");

const message =
    document.getElementById("message");


// =====================================================
// PLAYER STATE
// =====================================================

let currentIndex = -1;

let audio = new Audio();

audio.preload = "auto";

let clickTimer = null;


// =====================================================
// HTML ESCAPE
// =====================================================

function esc(s){{
    return String(
        s ?? ""
    ).replace(
        /[&<>'\"]/g,
        c =>
            ({{
                "&":"&amp;",
                "<":"&lt;",
                ">":"&gt;",
                "'":"&#39;",
                "\"":"&quot;"
            }})[c]
    );
}}


// =====================================================
// MESSAGE
// =====================================================

function showMessage(text){{

    message.textContent = text;

    message.classList.add("show");

    clearTimeout(
        showMessage.t
    );

    showMessage.t =
        setTimeout(
            () =>
                message.classList.remove("show"),
            1800
        );
}}


// =====================================================
// LABEL
// =====================================================

function setLabel(track){{

    labelDisc.innerHTML = "";

    if(
        track &&
        track.cover
    ){{

        const img =
            document.createElement("img");

        img.src =
            track.cover;

        img.alt = "";

        labelDisc.appendChild(img);

    }} else {{

        labelDisc.style.background =
            "radial-gradient(circle,#b78d55 0 12%,#5a3821 13% 42%,#2c1a10 43% 100%)";
    }}
}}


// =====================================================
// PLAYER STATE UI
// =====================================================

function updateState(){{

    if(currentIndex < 0){{

        statusEl.textContent =
            "READY";

        trackNow.textContent =
            "앨범을 LP 위로 끌어다 놓아주세요.";

        vinyl.classList.remove(
            "spinning"
        );

        return;
    }}

    const track =
        TRACKS[currentIndex];

    trackNow.textContent =
        track.artist +
        " · " +
        track.track;
}}


// =====================================================
// LOAD + PLAY
// =====================================================

function loadAndPlay(index){{

    const track =
        TRACKS[index];

    if(!track)
        return;


    if(!track.preview){{

        currentIndex =
            index;

        setLabel(track);

        updateState();

        statusEl.textContent =
            "NO PREVIEW";

        showMessage(
            "이 곡은 미리듣기가 없습니다."
        );

        return;
    }}


    currentIndex =
        index;

    setLabel(track);


    audio.src =
        track.preview;

    audio.currentTime =
        0;


    const promise =
        audio.play();


    if(
        promise &&
        promise.catch
    ){{
        promise.catch(
            () =>
                showMessage(
                    "브라우저에서 재생을 허용해 주세요."
                )
        );
    }}


    vinyl.classList.add(
        "spinning"
    );

    statusEl.textContent =
        "PLAYING";

    updateState();
}}


// =====================================================
// PLAY / PAUSE
// =====================================================

function togglePlayback(){{

    if(currentIndex < 0){{

        showMessage(
            "먼저 앨범을 LP 위에 올려주세요."
        );

        return;
    }}


    if(!audio.src){{

        loadAndPlay(
            currentIndex
        );

        return;
    }}


    if(audio.paused){{

        const promise =
            audio.play();

        if(
            promise &&
            promise.catch
        ){{
            promise.catch(
                () => {{}}
            );
        }}

        vinyl.classList.add(
            "spinning"
        );

        statusEl.textContent =
            "PLAYING";

    }} else {{

        audio.pause();

        vinyl.classList.remove(
            "spinning"
        );

        statusEl.textContent =
            "PAUSED";
    }}
}}


// =====================================================
// STOP
// =====================================================

function stopPlayback(){{

    audio.pause();

    try{{
        audio.currentTime = 0;
    }}catch(e){{}}

    vinyl.classList.remove(
        "spinning"
    );

    statusEl.textContent =
        currentIndex >= 0
            ? "STOPPED"
            : "READY";
}}


// =====================================================
// AUDIO END
// =====================================================

audio.addEventListener(
    "ended",
    () => {{

        vinyl.classList.remove(
            "spinning"
        );

        statusEl.textContent =
            "ENDED";
    }}
);


// =====================================================
// VINYL CLICK
// =====================================================

vinyl.addEventListener(
    "click",
    () => {{

        clearTimeout(
            clickTimer
        );

        clickTimer =
            setTimeout(
                () =>
                    togglePlayback(),
                220
            );
    }}
);


// =====================================================
// VINYL DOUBLE CLICK
// =====================================================

vinyl.addEventListener(
    "dblclick",
    () => {{

        clearTimeout(
            clickTimer
        );

        stopPlayback();
    }}
);


// =====================================================
// MAKE CARD
// =====================================================

function makeCard(
    track,
    index
){{

    const card =
        document.createElement(
            "div"
        );

    card.className =
        "card";

    card.draggable =
        true;

    card.dataset.index =
        index;


    card.innerHTML = `
        <img
            class="cover"
            src="${{esc(track.cover)}}"
            alt=""
        >

        <div class="meta">

            <div
                class="song"
                title="${{esc(track.track)}}"
            >
                ${{esc(track.track)}}
            </div>

            <div
                class="artist"
                title="${{esc(track.artist)}}"
            >
                ${{esc(track.artist)}}
            </div>

            <div class="small-tag">
                DRAG ME TO LP
            </div>

        </div>
    `;


    // 드래그 시작
    card.addEventListener(
        "dragstart",
        event => {{

            event.dataTransfer.setData(
                "text/plain",
                String(index)
            );

            event.dataTransfer.effectAllowed =
                "copy";

            card.style.opacity =
                ".55";
        }}
    );


    // 드래그 종료
    card.addEventListener(
        "dragend",
        () => {{
            card.style.opacity =
                "1";
        }}
    );


    return card;
}}


// =====================================================
// RENDER CARDS
// =====================================================

function renderCards(){{

    if(!TRACKS.length){{

        cardsEl.innerHTML =
            `
            <div class="empty">
                검색 결과가 없습니다.
                <br>
                가수 이름이나 곡 제목으로
                다시 찾아보세요.
            </div>
            `;

        return;
    }}


    TRACKS.forEach(
        (track, index) => {{

            cardsEl.appendChild(
                makeCard(
                    track,
                    index
                )
            );
        }}
    );
}}


// =====================================================
// DRAG OVER
// =====================================================

deck.addEventListener(
    "dragover",
    event => {{

        event.preventDefault();

        event.dataTransfer.dropEffect =
            "copy";

        deck.style.filter =
            "brightness(1.09)";
    }}
);


// =====================================================
// DRAG LEAVE
// =====================================================

deck.addEventListener(
    "dragleave",
    () => {{

        deck.style.filter = "";
    }}
);


// =====================================================
// DROP
// =====================================================

deck.addEventListener(
    "drop",
    event => {{

        event.preventDefault();

        deck.style.filter = "";


        const index =
            Number(
                event.dataTransfer.getData(
                    "text/plain"
                )
            );


        if(
            Number.isFinite(index) &&
            TRACKS[index]
        ){{
            loadAndPlay(index);
        }}
    }}
);


// =====================================================
// INITIAL RENDER
// =====================================================

renderCards();


</script>

</body>

</html>
"""

    components.html(
        component_html,
        height=680,
        scrolling=False,
    )


# =========================================================
# HOME
# =========================================================

def home_page():

    st.markdown(
        """
        <div class="rr-home-card">

            <div class="rr-kicker">
                A LITTLE ROOM FOR MUSIC
            </div>

            <div class="rr-title">
                오늘의 음악을<br>
                한 장의 레코드처럼.
            </div>

            <div
                class="rr-copy"
                style="margin-top:18px;"
            >
                나무 향이 밴 작은 레코드 바.<br>
                한 장을 골라 올리고,
                잠깐 머물다 가세요.
            </div>

            <div class="rr-home-note">
                RECORD ROOM · EST. 2026
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.write("")


    if st.button(
        "ENTER ROOM",
        key="enter_home"
    ):

        go("choice")


# =========================================================
# CHOICE
# =========================================================

def choice_page():

    render_header(
        "THE ROOM"
    )


    st.markdown(
        """
        <div
            style="
                text-align:center;
                padding:18px 0 16px;
            "
        >

            <div class="rr-kicker">
                CHOOSE A MOMENT
            </div>

            <div
                class="rr-title"
                style="
                    font-size:
                    clamp(26px,3.2vw,42px);
                "
            >
                오늘은 어떻게 들을까요?
            </div>

            <div
                class="rr-copy"
                style="
                    margin:12px auto 0;
                "
            >
                한 곡을 찾아도 좋고,
                기분에 맞는 곡을 골라도 좋아요.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    c1, c2 = st.columns(2)


    with c1:

        if st.button(
            "노래듣기",
            key="choice_listen"
        ):

            go("listen")


    with c2:

        if st.button(
            "노래 추천받기",
            key="choice_recommend"
        ):

            go("recommend")


    st.write("")


    if st.button(
        "← 처음으로",
        key="back_home"
    ):

        go("home")


# =========================================================
# LISTEN
# =========================================================

def listen_page():

    render_header(
        "LISTEN"
    )


    st.markdown(
        """
        <div style="margin-bottom:10px;">

            <div
                class="rr-title"
                style="
                    font-size:
                    clamp(25px,3.2vw,40px);
                "
            >
                곡을 찾아서,
                LP 위에 올려보세요.
            </div>

            <div
                class="rr-copy"
                style="margin-top:9px;"
            >
                가수 이름이나 노래 제목으로
                검색한 뒤 앨범 카드를 끌어다
                LP에 놓으면 바로 미리듣기가
                시작됩니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # =====================================================
    # SEARCH FORM
    # =====================================================

    with st.form(
        "search_form",
        clear_on_submit=False
    ):

        query = st.text_input(
            "검색",
            value=st.session_state.search_term,
            placeholder=(
                "예: 뉴진스 / 아이유 / 지코 / "
                "Love wins all"
            ),
            label_visibility="collapsed",
        )


        submitted = st.form_submit_button(
            "SEARCH"
        )


    # =====================================================
    # SEARCH
    # =====================================================

    if submitted:

        term = query.strip()

        st.session_state.search_term = term


        if term:

            with st.spinner(
                "레코드 선반을 찾는 중..."
            ):

                st.session_state.results = (
                    search_music(term)
                )

        else:

            st.session_state.results = []


    # =====================================================
    # NO RESULT WARNING
    # =====================================================

    if (
        st.session_state.search_term
        and not st.session_state.results
    ):

        st.warning(
            "검색 결과를 찾지 못했어요. "
            "가수 이름이나 곡 제목을 "
            "조금 다르게 입력해 보세요."
        )


    # =====================================================
    # PLAYER / EMPTY SHELF
    # =====================================================

    if st.session_state.results:

        track_cards_component(
            st.session_state.results,
            "listen"
        )

    else:

        track_cards_component(
            [],
            "empty"
        )


    st.write("")


    # =====================================================
    # BACK
    # =====================================================

    if st.button(
        "← ROOM으로 돌아가기",
        key="back_choice_listen"
    ):

        go("choice")


# =========================================================
# RECOMMEND
# =========================================================

def recommend_page():

    render_header(
        "DISCOVER"
    )


    st.markdown(
        """
        <div style="margin-bottom:16px;">

            <div
                class="rr-title"
                style="
                    font-size:
                    clamp(25px,3.2vw,40px);
                "
            >
                지금 기분에 맞는 레코드
            </div>

            <div
                class="rr-copy"
                style="margin-top:9px;"
            >
                아래 무드를 누르면
                그 분위기의 곡을 골라드려요.
                마음에 드는 카드는 그대로
                LP에 드래그하면 됩니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    moods = {

        "새벽":
            "새벽 감성",

        "드라이브":
            "drive pop",

        "설렘":
            "love pop",

        "비 오는 날":
            "rainy day",

        "집중":
            "lofi",

        "퇴근길":
            "city pop",

    }


    cols = st.columns(3)

    chosen = None


    for i, mood in enumerate(
        moods.keys()
    ):

        with cols[i % 3]:

            if st.button(
                mood,
                key=f"mood_{i}"
            ):

                chosen = moods[mood]


    if chosen:

        with st.spinner(
            "오늘의 레코드를 고르는 중..."
        ):

            st.session_state.results = (
                seed_search(chosen)[:15]
            )

        st.session_state.search_term = chosen


    if st.session_state.results:

        track_cards_component(
            st.session_state.results,
            "recommend"
        )

    else:

        st.markdown(
            """
            <div
                style="
                    margin-top:20px;
                    border:
                        1px dashed
                        rgba(214,174,116,.18);
                    padding:34px;
                    border-radius:18px;
                    text-align:center;
                    color:#a88b68;
                    font:
                        12px/1.8
                        monospace;
                "
            >
                무드를 하나 골라보세요.
                <br>
                선택한 레코드가
                이 방에 놓입니다.
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.write("")


    if st.button(
        "← ROOM으로 돌아가기",
        key="back_choice_reco"
    ):

        go("choice")


# =========================================================
# ROUTER
# =========================================================

if st.session_state.page == "home":

    home_page()


elif st.session_state.page == "choice":

    choice_page()


elif st.session_state.page == "listen":

    listen_page()


elif st.session_state.page == "recommend":

    recommend_page()


else:

    st.session_state.page = "home"

    st.rerun()
