import streamlit as st

# 1. 세션 상태 초기화
if 'suspect_list' not in st.session_state:
    st.session_state.suspect_list = []
if 'fifa_motto' not in st.session_state:
    st.session_state.fifa_motto = "왜 피파를 껐나 누가 그랬냐!"
if 'fifa_updated' not in st.session_state:
    st.session_state.fifa_updated = False

# 2. 용의자 추가 콜백 함수
def add_suspect():
    person = st.session_state.person_input
    if person:
        st.session_state.suspect_list.append([person, False])
        st.toast("용의자가 목록에 추가되었습니다!")
        st.session_state.person_input = ""

# 3. 질문 수정 모달 다이얼로그
@st.dialog("상황 및 질문 수정")
def edit_fifa():
    motto = st.text_input("질문/상황을 입력하세요", value="왜 피파를 껐나 누가 그랬냐!")
    if st.button("저장"):
        st.session_state.fifa_motto = motto
        st.session_state.fifa_updated = True
        st.rerun()

# 4. 페이지 함수 정의
def page_motto():
    st.header("📣 1. 문제 발생 상황")
    st.info(f"현재 상황: {st.session_state.fifa_motto}")
    if st.button("상황 질문 수정하기"):
        edit_fifa()
    if st.session_state.fifa_updated:
        st.success("상황 질문이 수정되었습니다!")
        st.session_state.fifa_updated = False
    st.markdown("---")

def page_suspects():
    st.header("✅ 2. 누가 그랬냐?")
    st.write(f"현재 핵심 질문: **{st.session_state.fifa_motto}**")
    st.text_input("피파 끈 사람(용의자) 입력", key="person_input")
    st.button("추가하기", on_click=add_suspect)
    
    st.markdown("---")
    for i in range(len(st.session_state.suspect_list)):
        col_name, col_btn, col_status = st.columns([4, 1, 1])
        with col_name:
            st.write(f"{i+1}. {st.session_state.suspect_list[i][0]}")
        with col_btn:
            if st.button("자백/확인", key=f"btn_{i}"):
                st.session_state.suspect_list[i][1] = True
                st.rerun()
        with col_status:
            if st.session_state.suspect_list[i][1]:
                st.write("✅ **범인 확인!**")
    st.markdown("---")

def page_report():
    st.header("📈 3. 수사 진행 현황")
    if not st.session_state.suspect_list:
        st.write("아직 등록된 용의자가 없습니다.")
    else:
        total = len(st.session_state.suspect_list)
        count = sum(1 for item in st.session_state.suspect_list if item[1])
        
        progress = (count / total) * 100
        st.metric("자백/확인 진행률", f"{progress:.1f}%")
        st.progress(progress / 100)
        
        if progress == 100:
            st.balloons()
            st.success("모든 범인이 밝혀졌습니다! 🎮⚽")
            
        if st.button("목록 전체 초기화"):
            st.session_state.suspect_list = []
            st.rerun()

# 5. 네비게이션 설정 및 실행
pg = st.navigation([
    st.Page(page_motto, title="왜 피파를 껐나", icon="📣"),
    st.Page(page_suspects, title="누가 그랬냐?", icon="✅"),
    st.Page(page_report, title="수사 현황", icon="📈")
], position="top")

st.title("🎮 왜 피파를 껐나 누가 그랬냐 관리기")
pg.run()
