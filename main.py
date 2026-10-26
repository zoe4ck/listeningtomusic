import streamlit as st
import requests
import json
import base64

# 페이지 설정
st.set_page_config(
    page_title="Record Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 전체 CSS 스타일 적용 (디자인 개편 내용 포함)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Nanum+Myeongjo:wght@400;700&display=swap');

    /* 배경 및 기본 폰트 설정 */
    .stApp {
        background: radial-gradient(circle at 50% 20%, #2a1810 0%, #120a07 70%, #0a0504 100%);
        color: #e6c687;
        font-family: 'Nanum Myeongjo', serif;
    }

    /* 메인 타이틀 */
    .main-title {
        font-family: 'Cinzel', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #d4af37;
        text-align: center;
        letter-spacing: 4px;
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
        margin-top: 20px;
        margin-bottom: 5px;
    }

    /* [개선 2] 체크인 안내문 소제목 스타일 */
    .auth-subtitle {
        font-family: 'Cinzel', 'Playfair Display', serif;
        font-size: 1.1rem;
        color: #d4af37;
        letter-spacing: 2px;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 30px;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
        opacity: 0.9;
    }

    /* [개선 1] 마이룸 게임 인터랙션 룸 디자인 및 상호작용 범위 축소 */
    .room-container {
        position: relative;
        width: 100%;
        max-width: 900px;
        height: 480px;
        margin: 20px auto;
        background: linear-gradient(180deg, #1a100c 0%, #2a1a14 70%, #3a241b 100%);
        border: 4px solid #5c3a21;
        border-radius: 12px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.8), 0 15px 35px rgba(0,0,0,0.6);
        overflow: hidden;
    }

    .room-wall {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 120px;
        background: repeating-linear-gradient(90deg, #22140e, #22140e 40px, #281811 40px, #281811 80px);
        border-bottom: 6px solid #422717;
    }

    .room-floor {
        position: absolute;
        bottom: 0; left: 0; right: 0; height: 120px;
        background: repeating-linear-gradient(45deg, #2b1810, #2b1810 20px, #22120b 20px, #22120b 40px);
    }

    .interact-item {
        position: absolute;
        cursor: pointer;
        transition: transform 0.25s ease, filter 0.25s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .interact-item:hover {
        transform: translateY(-5px) scale(1.03);
        filter: drop-shadow(0 0 12px rgba(212, 175, 55, 0.8));
    }

    .item-fireplace { left: 8%; bottom: 110px; width: 200px; }
    .item-lp { left: 42%; bottom: 110px; width: 160px; }
    .item-bookshelf { right: 8%; bottom: 110px; width: 180px; }

    .item-label {
        background: rgba(18, 11, 8, 0.85);
        border: 1px solid #d4af37;
        color: #e6c687;
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 12px;
        margin-top: 8px;
        letter-spacing: 1px;
        white-space: nowrap;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }

    /* 카드 스타일 공통 */
    .hotel-card {
        background: linear-gradient(145deg, #1f120c, #2a1a12);
        border: 1px solid #5c3a21;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "MY ROOM"

# 상단 네비게이션 메뉴바
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏨 MAIN LOBBY", use_container_width=True):
        st.session_state.current_page = "MAIN"
        st.rerun()
with col2:
    if st.button("🍸 ROOM SERVICE (COCKTAIL BAR)", use_container_width=True):
        st.session_state.current_page = "ROOM SERVICE"
        st.rerun()
with col3:
    if st.button("🗝️ MY ROOM", use_container_width=True):
        st.session_state.current_page = "MY ROOM"
        st.rerun()
st.markdown("---")

# ---------------------------------------------------------
# 1. MAIN LOBBY 페이지
# ---------------------------------------------------------
if st.session_state.current_page == "MAIN":
    st.markdown('<div class="main-title">RECORD HOTEL</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">VINTAGE MUSIC & ATMOSPHERE LOUNGE</div>', unsafe_allow_html=True)
    
    st.write("환영합니다, 호텔 게스트님. 아날로그 감성의 음악과 공간을 경험해 보세요.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="hotel-card">
            <h3>🍷 Night Concierge</h3>
            <p>오늘 밤 당신의 기분에 어울리는 음악과 칵테일을 추천해 드립니다. 룸 서비스 바를 이용해 보세요.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="hotel-card">
            <h3>🎧 Private Suite Room</h3>
            <p>나만의 방에서 LP 플레이어로 음악을 감상하고 보관된 음반을 관리할 수 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. ROOM SERVICE (COCKTAIL BAR) 페이지 - [개선 3] 칵테일 일러스트 고도화
# ---------------------------------------------------------
elif st.session_state.current_page == "ROOM SERVICE":
    st.markdown('<div class="main-title">COCKTAIL BAR</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">ROOM SERVICE · NIGHT CONCIERGE</div>', unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>오늘의 기분을 한 잔 골라주세요. 음악은 그 다음에 고를게요.</p>", unsafe_allow_html=True)
    
    # 칵테일 카드 4개 배치
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("""
        <div class="hotel-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #d4af37; margin-bottom: 5px;">ORDER NO. 01</div>
            <div style="font-weight: bold; margin-bottom: 10px;">조금 위로가 필요해요</div>
        """, unsafe_allow_html=True)
        
        # 핑크 칵테일 SVG 일러스트
        st.markdown("""
        <div style="display: flex; justify-content: center; margin: 10px 0;">
            <svg width="110" height="130" viewBox="0 0 100 120">
                <defs>
                    <linearGradient id="pinkGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#ff758c"/>
                        <stop offset="100%" stop-color="#ff7eb3"/>
                    </linearGradient>
                </defs>
                <path d="M20 20 L80 20 L50 65 Z" fill="url(#pinkGrad)" opacity="0.85"/>
                <path d="M15 15 L85 15 L50 68 L15 15 Z" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.7"/>
                <line x1="50" y1="68" x2="50" y2="105" stroke="#ffffff" stroke-width="2.5" opacity="0.7"/>
                <ellipse cx="50" cy="105" rx="20" ry="4" fill="#ffffff" opacity="0.6"/>
                <circle cx="68" cy="15" r="5" fill="#d63031"/>
            </svg>
        </div>
        <div style="font-size: 0.85rem; color: #d4af37; margin-top: 10px;">핑크 칵테일</div>
        <div style="font-size: 0.75rem; color: #aaa; margin-bottom: 15px;">마음을 가라앉히고 천천히 쉬어 가는 음악</div>
        """, unsafe_allow_html=True)
        if st.button("ORDER THIS", key="cocktail_1", use_container_width=True):
            st.success("핑크 칵테일과 어울리는 음악을 준비 중입니다!")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="hotel-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #d4af37; margin-bottom: 5px;">ORDER NO. 02</div>
            <div style="font-weight: bold; margin-bottom: 10px;">산뜻하게 기분 전환</div>
        """, unsafe_allow_html=True)
        
        # 멜론 소다 SVG 일러스트
        st.markdown("""
        <div style="display: flex; justify-content: center; margin: 10px 0;">
            <svg width="110" height="130" viewBox="0 0 100 120">
                <defs>
                    <linearGradient id="melonGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#55efc4"/>
                        <stop offset="100%" stop-color="#00b894"/>
                    </linearGradient>
                </defs>
                <rect x="30" y="25" width="40" height="75" rx="6" fill="url(#melonGrad)" opacity="0.85"/>
                <rect x="28" y="20" width="44" height="82" rx="8" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.7"/>
                <circle cx="50" cy="22" r="12" fill="#fffdd0"/>
                <line x1="42" y1="5" x2="60" y2="60" stroke="#ff7675" stroke-width="3" stroke-linecap="round"/>
            </svg>
        </div>
        <div style="font-size: 0.85rem; color: #d4af37; margin-top: 10px;">멜론 소다</div>
        <div style="font-size: 0.75rem; color: #aaa; margin-bottom: 15px;">가볍고 청량한 분위기로 전환하는 음악</div>
        """, unsafe_allow_html=True)
        if st.button("ORDER THIS", key="cocktail_2", use_container_width=True):
            st.success("멜론 소다와 어울리는 음악을 준비 중입니다!")
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="hotel-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #d4af37; margin-bottom: 5px;">ORDER NO. 03</div>
            <div style="font-weight: bold; margin-bottom: 10px;">신나는 노래가 필요해요</div>
        """, unsafe_allow_html=True)
        
        # 오렌지 주스 SVG 일러스트
        st.markdown("""
        <div style="display: flex; justify-content: center; margin: 10px 0;">
            <svg width="110" height="130" viewBox="0 0 100 120">
                <defs>
                    <linearGradient id="orangeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#ffeaa7"/>
                        <stop offset="100%" stop-color="#fdcb6e"/>
                    </linearGradient>
                </defs>
                <path d="M 25 30 A 25 25 0 0 0 75 30 Z" fill="url(#orangeGrad)" opacity="0.9"/>
                <path d="M 22 25 A 28 28 0 0 0 78 25 Z" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.7"/>
                <line x1="50" y1="58" x2="50" y2="100" stroke="#ffffff" stroke-width="2.5" opacity="0.7"/>
                <ellipse cx="50" cy="100" rx="18" ry="4" fill="#ffffff" opacity="0.6"/>
                <path d="M 65 18 A 10 10 0 0 1 80 28 Z" fill="#e17055"/>
            </svg>
        </div>
        <div style="font-size: 0.85rem; color: #d4af37; margin-top: 10px;">오렌지 주스</div>
        <div style="font-size: 0.75rem; color: #aaa; margin-bottom: 15px;">리듬을 타면서 기분을 끌어올리는 음악</div>
        """, unsafe_allow_html=True)
        if st.button("ORDER THIS", key="cocktail_3", use_container_width=True):
            st.success("오렌지 주스와 어울리는 음악을 준비 중입니다!")
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="hotel-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #d4af37; margin-bottom: 5px;">ORDER NO. 04</div>
            <div style="font-weight: bold; margin-bottom: 10px;">조용히 쉬고 싶어요</div>
        """, unsafe_allow_html=True)
        
        # 네이비 칵테일 SVG 일러스트
        st.markdown("""
        <div style="display: flex; justify-content: center; margin: 10px 0;">
            <svg width="110" height="130" viewBox="0 0 100 120">
                <defs>
                    <linearGradient id="navyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#0984e3"/>
                        <stop offset="100%" stop-color="#2d3436"/>
                    </linearGradient>
                </defs>
                <path d="M20 25 L80 25 L50 68 Z" fill="url(#navyGrad)" opacity="0.9"/>
                <path d="M16 20 L84 20 L50 72 L16 20 Z" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.7"/>
                <line x1="50" y1="72" x2="50" y2="105" stroke="#ffffff" stroke-width="2.5" opacity="0.7"/>
                <ellipse cx="50" cy="105" rx="20" ry="4" fill="#ffffff" opacity="0.6"/>
                <path d="M40 20 Q50 10 60 20" fill="none" stroke="#ffeaa7" stroke-width="3" stroke-linecap="round"/>
            </svg>
        </div>
        <div style="font-size: 0.85rem; color: #d4af37; margin-top: 10px;">네이비 칵테일</div>
        <div style="font-size: 0.75rem; color: #aaa; margin-bottom: 15px;">차분하게 집중하고 편안하게 쉴 수 있는 음악</div>
        """, unsafe_allow_html=True)
        if st.button("ORDER THIS", key="cocktail_4", use_container_width=True):
            st.success("네이비 칵테일과 어울리는 음악을 준비 중입니다!")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. MY ROOM (PRIVATE SUITE) 페이지
# ---------------------------------------------------------
elif st.session_state.current_page == "MY ROOM":
    st.markdown('<div class="main-title">MY ROOM</div>', unsafe_allow_html=True)
    
    # 로그인 상태에 따른 화면 분기
    if not st.session_state.logged_in:
        # [개선 2] 체크인 안내문 소제목 적용
        st.markdown('<div class="auth-subtitle">GUEST CHECK-IN & ROOM RESERVATION</div>', unsafe_allow_html=True)
        
        col_login1, col_login2, col_login3 = st.columns([1, 2, 1])
        with col_login2:
            st.markdown('<div class="hotel-card">', unsafe_allow_html=True)
            email_input = st.text_input("EMAIL", placeholder="guest@example.com")
            password_input = st.text_input("ROOM KEY (Password)", type="password", placeholder="비밀번호")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("CHECK-IN", use_container_width=True):
                    if email_input:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email_input
                        st.rerun()
                    else:
                        st.warning("이메일을 입력해 주세요.")
            with col_btn2:
                if st.button("NEW GUEST", use_container_width=True):
                    st.info("회원가입 기능 연동 영역입니다.")
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # [개선 1] 로그인 후 나의 룸 (정교화된 인터랙티브 그래픽 룸)
        st.markdown(f'<div class="auth-subtitle">GUEST PRIVATE ROOM — {st.session_state.user_email}</div>', unsafe_allow_html=True)
        
        # 상단 체크아웃 버튼
        col_top1, col_top2 = st.columns([6, 1])
        with col_top2:
            if st.button("CHECK-OUT"):
                st.session_state.logged_in = False
                st.session_state.user_email = ""
                st.rerun()

        # 인터랙티브 룸 HTML 컴포넌트 렌더링
        room_html = """
        <div class="room-container">
            <div class="room-wall"></div>
            <div class="room-floor"></div>
            
            <!-- 1. 벽난로 -->
            <div class="interact-item item-fireplace" onclick="alert('불멍 공간: 따뜻한 모닥불 ASMR과 함께 휴식합니다.')">
                <svg width="180" height="180" viewBox="0 0 200 200">
                    <rect x="20" y="40" width="160" height="140" rx="8" fill="#3a2312" stroke="#5a381d" stroke-width="4"/>
                    <rect x="40" y="70" width="120" height="110" rx="5" fill="#120b07"/>
                    <path d="M80 160 Q100 90 120 160 Q100 130 80 160 Z" fill="#ff4500">
                        <animate attributeName="d" dur="1s" repeatCount="indefinite" values="M80 160 Q100 90 120 160 Q100 130 80 160 Z; M80 160 Q100 110 120 160 Q100 140 80 160 Z; M80 160 Q100 90 120 160 Q100 130 80 160 Z"/>
                    </path>
                    <path d="M90 160 Q100 110 110 160 Q100 135 90 160 Z" fill="#ffaa00"/>
                </svg>
                <div class="item-label">🔥 FIREPLACE · 불멍 공간</div>
            </div>

            <!-- 2. LP 플레이어 -->
            <div class="interact-item item-lp" onclick="alert('LP 플레이어: 음악 재생 및 턴테이블을 작동합니다.')">
                <svg width="140" height="140" viewBox="0 0 160 160">
                    <rect x="10" y="50" width="140" height="90" rx="6" fill="#4a2e1b" stroke="#7a4b2c" stroke-width="3"/>
                    <circle cx="65" cy="95" r="35" fill="#111" stroke="#222" stroke-width="2"/>
                    <circle cx="65" cy="95" r="12" fill="#d4af37"/>
                    <circle cx="65" cy="95" r="3" fill="#000"/>
                    <line x1="120" y1="65" x2="85" y2="90" stroke="#c0c0c0" stroke-width="3" stroke-linecap="round"/>
                </svg>
                <div class="item-label">🎵 LP PLAYER · 레코드 듣기</div>
            </div>

            <!-- 3. 책장 -->
            <div class="interact-item item-bookshelf" onclick="alert('북셀프: 보관된 음반 컬렉션을 확인합니다.')">
                <svg width="150" height="170" viewBox="0 0 160 180">
                    <rect x="10" y="10" width="140" height="160" rx="4" fill="#361f12" stroke="#54321d" stroke-width="4"/>
                    <line x1="10" y1="65" x2="150" y2="65" stroke="#54321d" stroke-width="4"/>
                    <line x1="10" y1="120" x2="150" y2="120" stroke="#54321d" stroke-width="4"/>
                    <rect x="25" y="25" width="8" height="35" fill="#8b263e"/>
                    <rect x="36" y="20" width="8" height="40" fill="#d4af37"/>
                    <rect x="47" y="28" width="8" height="32" fill="#2b5b84"/>
                    <rect x="25" y="75" width="8" height="40" fill="#4b6b54"/>
                    <rect x="36" y="80" width="8" height="35" fill="#a85b32"/>
                </svg>
                <div class="item-label">📚 BOOKSHELF · 보관한 음반</div>
            </div>
        </div>
        """
        st.components.v1.html(room_html, height=520)
