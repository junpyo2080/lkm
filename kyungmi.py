import streamlit as st

if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []
if 'user_motto' not in st.session_state:
    st.session_state.user_motto = "오늘도 화이팅!"

def add_todo():
    task = st.session_state.todo_input
    if task:
        st.session_state.todo_list.append([task, False])
        st.toast("할 일이 추가되었습니다!")
        st.session_state.todo_input = ""
def page():
st.title("🌱 누구를 전학 보낼까?")
st.header("📣 1. 누구?")
motto = st.text_input("누구인지 적어주세요")
if st.button("정보 저장"):
    st.session_state.user_motto = motto
    st.success("전학 보낼 사람이 등록되었습니다!")
st.markdown("---")

st.header("✅ 2. 오늘의 할 일")
st.write(f"현재 다짐: **{st.session_state.user_motto}**")
new_todo = st.text_input("추가로 전학보낼 사람을 입력하세요", key="todo_input")
st.button("추가하기", on_click=add_todo)
if new_todo == "":
    st.warning("정보를 입력하고 버튼을 눌러주세요!")

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

st.header("📈 3. 나의 전학 지수")
if not st.session_state.todo_list:
    st.write("아직 등록된 할 일이 없습니다.")
else:
    total = len(st.session_state.todo_list)
    count = 0
    for item in st.session_state.todo_list:
        if item[1] == True:
            count += 1
    progress = (count / total) * 100
    st.metric("오늘의 달성률", f"{progress:.1f}%")
    st.progress(progress / 100)
    if st.button("기록 전체 초기화"):
        st.session_state.todo_list = []
        st.rerun()

