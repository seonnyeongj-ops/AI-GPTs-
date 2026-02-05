import streamlit as st

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="Smart Work Portal",
    page_icon="🚀",
    layout="centered"
)

# ==========================================
# 2. 데이터 & 설정
# ==========================================
ACCESS_PASSWORD = "team2026"

gpt_tools = [
    {
        "category": "📝 문서/작문",
        "name": "비즈니스 이메일 봇",
        "desc": "상황만 말하면 격식 있는 메일 초안을 작성해줍니다.",
        "link": "https://chatgpt.com/",
        "prompt": "상황: [거래처에 단가 인상 요청].\n톤앤매너: 정중하지만 단호하게.\n위 내용으로 이메일 초안 작성해줘."
    },
    {
        "category": "📊 업무 효율",
        "name": "회의록 3줄 요약기",
        "desc": "녹취록이나 메모를 넣으면 핵심 내용과 할 일을 정리합니다.",
        "link": "https://chatgpt.com/",
        "prompt": "다음 회의 내용을 요약하고, 담당자별 Action Item을 표로 정리해줘."
    },
    {
        "category": "💡 아이디어",
        "name": "마케팅 카피라이터",
        "desc": "상품 특징을 입력하면 블로그/인스타용 홍보 문구를 뽑아줍니다.",
        "link": "https://chatgpt.com/",
        "prompt": "2030 직장인을 타겟으로 한 '거북목 교정기' 인스타그램 홍보 문구 5개 추천해줘."
    }
]

# ==========================================
# 3. 로그인 로직 (Session State 사용)
# ==========================================
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def check_password():
    if st.session_state['password_input'] == ACCESS_PASSWORD:
        st.session_state['authenticated'] = True
        st.session_state['password_input'] = ""  # 입력창 초기화
    else:
        st.error("비밀번호가 틀렸습니다. 다시 시도해주세요.")

# ==========================================
# 4. 화면 구성
# ==========================================

# (A) 로그인 전 화면
if not st.session_state['authenticated']:
    st.title("🔒 접속 권한 인증")
    st.write("사내 코드를 입력해주세요.")
    
    st.text_input(
        "비밀번호", 
        type="password", 
        key="password_input", 
        on_change=check_password
    )
    st.button("로그인", on_click=check_password)

# (B) 로그인 후 메인 화면
else:
    # 헤더 및 로그아웃 버튼
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("🚀 AI담당관 업무비서")
    with col2:
        if st.button("로그아웃"):
            st.session_state['authenticated'] = False
            st.rerun() # 화면 새로고침

    st.markdown("---")

    # 도구 카드 리스트 출력
    for tool in gpt_tools:
        # 카드 컨테이너 생성
        with st.container(border=True):
            # 카테고리 뱃지처럼 표시
            st.caption(f"📌 {tool['category']}")
            st.subheader(tool['name'])
            st.write(tool['desc'])
            
            # 프롬프트 영역 (Streamlit은 st.code를 쓰면 자동으로 복사 버튼이 생깁니다!)
            st.text("👇 아래 내용을 복사해서 사용하세요")
            st.code(tool['prompt'], language="text")
            
            # 링크 버튼
            st.link_button("GPT 실행하기 👉", tool['link'], type="primary")

