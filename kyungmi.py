art streamlit as st

from openai import OpenAI
ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def page_ai_coach():
    st.header("🧐 AI 코치와 대화하기")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "너는 사용자의 할 일 목록과 달성 정도를 분석하여 조언하는 열정적인 코치야. 사용자가 더 멋진 삶을 살 수 있도록 명확한 조언과 응원해줘."}
        ]
        
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
    question = st.chat_input("질문을 입력하세요")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            status_context = f"현재 나의 할 일과 달성 여부: {st.session_state.todo_list}"
            prompt = st.session_state.messages + [{"role": "system", "content": status_context}]
            with st.spinner("AI 코치가 생각 중...🤔"):
                response = ai_client.chat.completions.create(
                    model="gpt-5.4-mini",
                    messages=prompt)
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

pg = st.navigation([
    st.Page(page_motto, title="오늘의 다짐", icon="📣"),
    st.Page(page_todo, title="오늘의 할 일", icon="✅"),
    st.Page(page_report, title="나의 갓생 지수", icon="📈"),
    st.Page(page_ai_coach, title="AI 코칭", icon="🧐")], position="top")

st.title("🌱 갓생 살기 플래너")
pg.run()
