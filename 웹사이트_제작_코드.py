import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ==========================================
# 1. 페이지 초기 설정 (가장 먼저 실행되어야 함)
# ==========================================
st.set_page_config(
    page_title="2026 AI Smart Portal",
    page_icon="🤖",
    layout="wide",  # 화면을 넓게 사용
    initial_sidebar_state="expanded"
)

# 커스텀 CSS (카드 디자인, 폰트 등 예쁘게 꾸미기)
st.markdown("""
<style>
    /* 카드 디자인 */
    div[data-testid="stMetric"] {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    /* 버튼 스타일 */
    .stButton button {
        width: 100%;
        border-radius: 8px;
    }
    /* 텍스트 영역 스타일 */
    .stTextArea textarea {
        background-color: #f9f9f9;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 & 설정
# ==========================================
ACCESS_PASSWORD = "team2026"

# 더 풍부해진 도구 데이터
gpt_tools = [
    {"category": "📝 문서/작문", "name": "비즈니스 이메일 봇", "desc": "상황에 맞는 격식 있는 메일 초안 작성", "link": "https://chatgpt.com/", "prompt": "상황: [거래처 단가 인상].\n톤앤매너: 정중하지만 단호하게.\n이메일 초안 작성해줘.", "tag": "BEST"},
    {"category": "📊 업무 효율", "name": "회의록 3줄 요약기", "desc": "녹취록을 핵심 내용과 Action Item으로 정리", "link": "https://chatgpt.com/", "prompt": "다음 회의 내용을 요약하고, 담당자별 할 일을 표로 정리해줘.", "tag": "필수"},
    {"category": "💡 마케팅", "name": "SNS 카피라이터", "desc": "인스타그램/블로그 홍보 문구 자동 생성", "link": "https://chatgpt.com/", "prompt": "타겟: 2030 직장인.\n상품: 거북목 교정기.\n감성적인 홍보 카피 5개 뽑아줘.", "tag": "인기"},
    {"category": "💻 개발/IT", "name": "파이썬 코드 리뷰어", "desc": "코드의 버그를 찾고 최적화 제안", "link": "https://chatgpt.com/", "prompt": "아래 파이썬 코드의 비효율적인 부분을 찾아서 수정해주고 설명을 달아줘.", "tag": "NEW"},
    {"category": "📝 문서/작문", "name": "보고서 목차 생성기", "desc": "주제만 주면 기획서/보고서 목차 구성", "link": "https://chatgpt.com/", "prompt": "주제: 2026년 AI 도입 전략 보고서.\n대상: 임원진.\n논리적인 목차를 구성해줘.", "tag": ""},
    {"category": "🌍 번역", "name": "한/영 비즈니스 번역", "desc": "뉘앙스를 살린 자연스러운 번역", "link": "https://chatgpt.com/", "prompt": "이 문장을 원어민이 쓰는 자연스러운 비즈니스 영어로 번역해줘.", "tag": ""}
]

# 공지사항 데이터
notices = [
    "[2026-02-05] 🚀 AI 포털 ver 2.0 오픈!",
    "[필독] 보안 유지를 위해 사내 데이터 입력 금지",
    "[팁] 크롬 브라우저 사용을 권장합니다."
]

# ==========================================
# 3. 함수 정의
# ==========================================
def check_login():
    if st.session_state['input_pw'] == ACCESS_PASSWORD:
        st.session_state['authenticated'] = True
        st.toast("로그인 성공! 환영합니다 👋", icon="✅")
    else:
        st.error("비밀번호가 올바르지 않습니다.")

# ==========================================
# 4. 메인 로직
# ==========================================

# 세션 상태 초기화
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- [로그인 화면] ---
if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.write("")
        st.write("")
        st.markdown("<h1 style='text-align: center;'>🔒 Team AI Portal</h1>", unsafe_allow_html=True)
        st.info("사내 업무 효율화를 위한 전용 공간입니다.")
        
        st.text_input("접속 코드", type="password", key="input_pw", on_change=check_login)
        st.button("입장하기", on_click=check_login, type="primary")
        
        st.divider()
        st.caption("문의: AI담당관 (admin@company.com)")

# --- [메인 대시보드] ---
else:
    # 1. 사이드바 (내 정보 및 메뉴)
    with st.sidebar:
        st.title("🤖 AI 담당관")
        st.markdown(f"**접속일:** {datetime.now().strftime('%Y-%m-%d')}")
        
        st.divider()
        st.subheader("📢 공지사항")
        for notice in notices:
            st.info(notice, icon="📌")
            
        st.divider()
        if st.button("로그아웃"):
            st.session_state['authenticated'] = False
            st.rerun()

    # 2. 메인 헤더
    st.title("🚀 스마트 업무 비서 센터")
    st.write("필요한 AI 도구를 선택하여 업무 시간을 단축하세요.")
    
    # 3. 탭 구성 (기능 분리)
    tab1, tab2, tab3 = st.tabs(["📂 전체 도구", "🏆 베스트 추천(추후 사용량 기반 재구성)", "📫 도구 요청함"])

    # --- [탭 1: 전체 도구 및 검색] ---
    with tab1:
        # 검색창 및 필터
        col_search, col_filter = st.columns([3, 1])
        with col_search:
            search_query = st.text_input("🔍 도구 검색 (이름, 기능 등)", placeholder="예: 이메일, 요약...")
        with col_filter:
            category_filter = st.selectbox("카테고리 필터", ["전체"] + list(set([t['category'] for t in gpt_tools])))

        st.divider()

        # 도구 필터링 로직
        filtered_tools = []
        for tool in gpt_tools:
            match_search = search_query in tool['name'] or search_query in tool['desc']
            match_category = category_filter == "전체" or category_filter == tool['category']
            
            if match_search and match_category:
                filtered_tools.append(tool)

        # 그리드 형태로 출력 (3열 배치)
        if not filtered_tools:
            st.warning("검색 결과가 없습니다.")
        else:
            cols = st.columns(3) # 3열 생성
            for idx, tool in enumerate(filtered_tools):
                with cols[idx % 3]: # 0,1,2, 0,1,2 순서로 배치
                    with st.container(border=True):
                        # 상단 태그 및 카테고리
                        top_c1, top_c2 = st.columns([1, 1])
                        with top_c1:
                            st.caption(tool['category'])
                        with top_c2:
                            if tool['tag']:
                                st.markdown(f"<span style='background:#ff4b4b; color:white; padding:2px 6px; border-radius:4px; font-size:10px; float:right;'>{tool['tag']}</span>", unsafe_allow_html=True)
                        
                        st.subheader(tool['name'])
                        st.write(tool['desc'])
                        
                        # 프롬프트 보기 (Expander로 숨김 처리하여 깔끔하게)
                        with st.expander("📝 프롬프트 보기"):
                            st.code(tool['prompt'], language='text')
                            st.caption("☝️ 위 코드를 복사해서 GPT에 붙여넣으세요.")
                        
                        st.link_button("GPT 실행하기 🚀", tool['link'], type="primary", use_container_width=True)

    # --- [탭 2: 베스트 추천 (통계 느낌)] ---
    with tab2:
        st.subheader("🔥 이번 주 가장 많이 사용된 도구")
        
        # 메트릭(숫자) 대시보드
        m1, m2, m3 = st.columns(3)
        m1.metric(label="이메일 봇 사용량", value="0,000회", delta="▲ 00%")
        m2.metric(label="회의록 요약기", value="000회", delta="▲ 0%")
        m3.metric(label="절약된 업무 시간", value="약 00시간", delta="positive")
        
        st.markdown("---")
        st.info("💡 **Tip:** 반복되는 엑셀 작업은 '파이썬 코드 리뷰어'에게 자동화 코드를 짜달라고 해보세요!")

    # --- [탭 3: 도구 요청함 (Form)] ---
    with tab3:
        st.subheader("📨 필요한 AI 도구가 있으신가요?")
        st.write("업무에 필요한 프롬프트나 기능을 제안해주세요. 개발팀에서 검토 후 추가해드립니다.")
        
        with st.form("request_form"):
            req_name = st.text_input("작성자 이름")
            req_tool = st.text_input("필요한 도구 제목")
            req_desc = st.text_area("구체적인 내용 (어떤 업무를 자동화하고 싶나요?)")
            
            submitted = st.form_submit_button("제안 보내기")
            
            if submitted:
                if req_tool and req_desc:
                    # 실제로는 DB에 저장하겠지만, 여기서는 성공 메시지만 출력
                    st.success(f"감사합니다, {req_name}님! '{req_tool}' 제안이 접수되었습니다.")
                    st.balloons()
                else:
                    st.warning("내용을 모두 입력해주세요.")

