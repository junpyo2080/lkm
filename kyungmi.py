import streamlit as st

if 'todo_list' not in st.session_state:
    st.session_state.todo_list = [
        ["옴의 법칙(V=IR) 정리하기", False],
        ["키르히호프 법칙 문제 풀기", False],
        ["P형/N형 반도체 차이점 공부하기", False],
        ["전기전자공학에 관한 선택과목과 대학 찾아보기",False]
    ]
if 'user_motto' not in st.session_state:
    st.session_state.user_motto = "오늘도 전기전자 마스터!"
if 'motto_updated' not in st.session_state:
    st.session_state.motto_updated = False

def add_todo():
    task = st.session_state.todo_input
    if task:
        st.session_state.todo_list.append([task, False])
        st.toast("학습 항목이 추가되었습니다!")
        st.session_state.todo_input = ""

@st.dialog("오늘의 다짐 수정")
def edit_motto():
    motto = st.text_input("나의 한 줄 학습 목표를 적어주세요.")
    if st.button("목표 저장"):
        st.session_state.user_motto = motto
        st.session_state.motto_updated = True
        st.rerun()

def page_motto():
    st.header("📣 1. 오늘의 학습 다짐")
    st.info(f"현재 목표: {st.session_state.user_motto}")
    if st.button("목표 수정하기"):
        edit_motto()
    if st.session_state.motto_updated:
        st.success("새로운 학습 목표가 등록되었습니다!")
        st.session_state.motto_updated = False
    st.markdown("---")
    st.subheader("💡 고1 통합과학/공학 핵심 요약")
    st.markdown("""
    * **전압 ($V$)**: 전하를 흐르게 하는 능력 (단위: $V$)
    * **전류 ($I$)**: 전하의 흐름 (단위: $A$)
    * **저항 ($R$)**: 전류의 흐름을 방해하는 작용 (단위: $\Omega$)
    * **옴의 법칙**: $V = I \\cdot R$
    """)

def page_todo():
    st.header("✅ 2. 전기전자 학습 체크리스트")
    st.write(f"현재 목표: **{st.session_state.user_motto}**")
    st.text_input("추가할 학습 주제를 입력하세요", key="todo_input")
    st.button("추가하기", on_click=add_todo)
    st.markdown("---")
    for i in range(len(st.session_state.todo_list)):
        col_task, col_btn, col_status = st.columns([4, 1, 1])
        with col_task:
            st.write(f"{i+1}. {st.session_state.todo_list[i][0]}")
        with col_btn:
            if st.button("완료", key=f"btn_{i}"):
                st.session_state.todo_list[i][1] = True
                st.rerun()
        with col_status:
            if st.session_state.todo_list[i][1]:
                st.write("✅ **달성!**")
    st.markdown("---")

def page_report():
    st.header("📈 3. 나의 학습 달성률")
    if not st.session_state.todo_list:
        st.write("아직 등록된 학습 항목이 없습니다.")
    else:
        total = len(st.session_state.todo_list)
        count = sum(1 for item in st.session_state.todo_list if item[1])
        progress = (count / total) * 100
        st.metric("오늘의 학습 달성률", f"{progress:.1f}%")
        st.progress(progress / 100)
        if progress == 100:
            st.balloons()
            st.success("오늘의 모든 공학 목표를 달성했습니다! 🏆")
        if st.button("기록 전체 초기화"):
            st.session_state.todo_list = []
            st.rerun()

def page_quiz():
    st.header("🧐 전기전자 기초 퀴즈")
    q1 = st.radio("1. 전압($V$)이 10V이고 저항($R$)이 5$\Omega$일 때, 전류($I$)는 얼마일까요?", ["1A", "2A", "50A"])
    if st.button("1번 정답 확인"):
        if q1 == "2A":
            st.success("정답입니다! ($I = V / R = 10 / 5 = 2A$)")
        else:
            st.error("다시 생각해보세요!")
    st.markdown("---")
    q2 = st.radio("2. P형 반도체와 N형 반도체를 접합하여 한쪽 방향으로만 전류가 흐르게 하는 부품은?", ["저항", "다이오드", "트랜지스터"])
    if st.button("2번 정답 확인"):
        if q2 == "다이오드":
            st.success("정답입니다!")
        else:
            st.error("다시 생각해보세요!")

pg = st.navigation([
    st.Page(page_motto, title="오늘의 목표", icon="📣"),
    st.Page(page_todo, title="학습 체크리스트", icon="✅"),
    st.Page(page_report, title="학습 달성률", icon="📈"),
    st.Page(page_quiz, title="기초 퀴즈", icon="🧐")
], position="top")

st.title("⚡ 고교 전기전자 기초 플래너")
pg.run()
