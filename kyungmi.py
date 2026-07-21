import streamlit as st

# 1. 세션 상태 초기화
if 'transfer_list' not in st.session_state:
    st.session_state.transfer_list = []
if 'transfer_reason' not in st.session_state:
    st.session_state.transfer_reason = "원활한 학교 적응 지원"
if 'reason_updated' not in st.session_state:
    st.session_state.reason_updated = False

# 2. 전학 대상 추가 콜백 함수
def add_student():
    student = st.session_state.student_input
    if student:
        st.session_state.transfer_list.append([student, False])
        st.toast("전학 대상 학생이 등록되었습니다!")
        st.session_state.student_input = ""

# 3. 전학 사유 수정 모달 다이얼로그
@st.dialog("전학 사유/기준 수정")
def edit_reason():
    reason = st.text_input("전학 추진 사유나 기준을 적어주세요.")
    if st.button("사유 저장"):
        st.session_state.transfer_reason = reason
        st.session_state.reason_updated = True
        st.rerun()

# 4. 페이지 함수 정의
def page_reason():
    st.header("📣 1. 전학 사유 및 기준 설정")
    st.info(f"현재 전학 기준: {st.session_state.transfer_reason}")
    if st.button("사유 수정하기"):
        edit_reason()
    if st.session_state.reason_updated:
        st.success("새로운 전학 사유가 등록되었습니다!")
        st.session_state.reason_updated = False
    st.markdown("---")

def page_students():
    st.header("✅ 2. 누굴 전학 보낼까?")
    st.write(f"현재 전학 기준: **{st.session_state.transfer_reason}**")
    st.text_input("추가할 학생 이름을 입력하세요", key="student_input")
    st.button("추가하기", on_click=add_student)
    
    st.markdown("---")
    for i in range(len(st.session_state.transfer_list)):
        col_student, col_btn, col_status = st.columns([4, 1, 1])
        with col_student:
            st.write(f"{i+1}. {st.session_state.transfer_list[i][0]}")
        with col_btn:
            if st.button("완료", key=f"btn_{i}"):
                st.session_state.transfer_list[i][1] = True
                st.rerun()
        with col_status:
            if st.session_state.transfer_list[i][1]:
                st.write("✅ **전학 완료!**")
    st.markdown("---")

def page_report():
    st.header("📈 3. 어떻게 진행되고 있을까?")
    if not st.session_state.transfer_list:
        st.write("아직 등록된 전학 대상 학생이 없습니다.")
    else:
        total = len(st.session_state.transfer_list)
        count = sum(1 for item in st.session_state.transfer_list if item[1])
        
        progress = (count / total) * 100
        st.metric("전학 처리 진행률", f"{progress:.1f}%")
        st.progress(progress / 100)
        
        if progress == 100:
            st.balloons()
            st.success("모든 학생의 전학 절차가 완료되었습니다! 🏆")
            
        if st.button("기록 전체 초기화"):
            st.session_state.transfer_list = []
            st.rerun()

# 5. 네비게이션 설정 및 실행
pg = st.navigation([
    st.Page(page_reason, title="전학 사유", icon="📣"),
    st.Page(page_students, title="누굴 전학 보낼까?", icon="✅"),
    st.Page(page_report, title="어떻게 진행될까?", icon="📈")
], position="top")

st.title("🏫 전학 수속 및 명단 관리 시스템")
pg.run()
