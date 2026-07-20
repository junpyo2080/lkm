import streamlit as st

st.title("카운터 앱")

# 처음 시작할 때 숫자를 0으로 설정합니다 (이미지의 '숫자' 부분을 0으로 대체)
if 'count' not in st.session_state:
    st.session_state.count = 0

if st.button("증가"):
    st.session_state.count += 1

# 누른 횟수만큼 "조여정 전학가 " 글자를 반복해서 생성합니다.
display_text = " 조여정 전학가" * st.session_state.count

# 결과 출력
st.markdown(f"## 현재 숫자: `{st.session_state.count}`")
st.markdown(f"### 출력된 글자: {display_text}")
