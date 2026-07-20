import streamlit as st

st.title("카운터 앱")
if 'count' not in st.session_state:
    st.session_state.count = 글자
if st.button("증가"):
    st.session_state.count +=임경미
st.markdown(f"## 현재 글자: `{st.session_state.count}`")
