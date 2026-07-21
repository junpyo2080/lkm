import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 초기화
ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 세션 상태(Session State) 초기화
if 'ee_topics' not in st.session_state:
    st.session_state.ee_topics = [
        ["옴의 법칙(Ohm's Law) 이해 및 회로 해석", False],
        ["키르히호프 법칙(KCL/KVL) 실습", False],
        ["반도체 P-N 접합 원리 학습", False]
    ]
if 'learning_goal' not in st.session_state:
    st.session_state.learning_goal = "전기전자공학 핵심 개념 마스터!"
if 'goal_updated' not in st.session_state:
    st.session_state.goal_updated = False


@st.dialog("학습 목표 수정")
def edit_goal():
    goal = st.text_input("새로운 전기전자공학 학습 목표를 입력하세요.")
    if st.button("목표 저장"):
        if goal.strip():
            st.session_state.learning_goal = goal
            st.session_state.goal_updated = True
            st.rerun()


def page_goal():
    st.header("⚡ 1. 오늘의 공학 목표")
    st.info(f"현재 목표: {st.session_state.learning_goal}")
    
    if st.button("목표 수정하기"):
        edit_goal()
        
    if st.session_state.goal_updated:
        st.success("학습 목표가 수정되었습니다!")
        st.session_state.goal_updated = False
        
    st.markdown("---")
    st.subheader("📚 주요 핵심 개념 요약")
    st.markdown("""
    * **옴의 법칙 ($V = IR$)**: 전압($V$), 전류($I$), 저항($R$) 간의 기본 관계식입니다.
    * **키르히호프 법칙**:
      * **KCL (전류 법칙)**: 마디로 들어오는 전류의 합은 나가는 전류의 합과 같습니다.
      * **KVL (전압 법칙)**: 닫힌 회로 내의 모든 전압 강하의 합은 0입니다.
    * **맥스웰 방정식**: 전자기학의 기초가 되는 4가지 선형 부분분수 방정식입니다.
    """)


def add_topic():
    topic = st.session_state.topic_input
    if topic.strip():
        st.session_state.ee_topics.append([topic, False])
        st.toast("학습 주제가 추가되었습니다!")
        st.session_state.topic_input = ""


def page_topics():
    st.header("✅ 2. 전기전자공학 학습 체크리스트")
    st.write(f"현재 목표: **{st.session_state.learning_goal}**")
    
    st.text_input("추가할 학습 주제나 문제 항목을 입력하세요", key="topic_input")
    st.button("주제 추가하기", on_click=add_topic)
    
    st.markdown("---")
    for i, item in enumerate(st.session_state.ee_topics):
        col_task, col_btn, col_status = st.columns([4, 1, 1])
        with col_task:
            st.write(f"{i+1}. {item[0]}")
        with col_btn:
            if st.button("완료", key=f"btn_{i}"):
                st.session_state.ee_topics[i][1] = True
                st.rerun()
        with col_status:
            if item[1]:
                st.write("✅ **달성!**")
    st.markdown("---")


def page_report():
    st.header("📈 3. 전기전자공학 학습 진도율")
    
    if not st.session_state.ee_topics:
        st.write("등록된 학습 주제가 없습니다.")
        return

    total = len(st.session_state.ee_topics)
    completed = sum(1 for item in st.session_state.ee_topics if item[1])
    progress = (completed / total) * 100

    st.metric("학습 달성률", f"{progress:.1f}%")
    st.progress(progress / 100)

    if progress == 100:
        st.balloons()
        st.success("모든 학습 목표를 달성하셨습니다! 정복 완료! 🏆")
        
    if st.button("학습 기록 초기화"):
        st.session_state.ee_topics = []
        st.rerun()


def page_ai_tutor():
    st.header("🧐 전기전자공학 AI 튜터")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "너는 전기전자공학(Electrical & Electronic Engineering) 전문 AI 튜터야. "
                    "회로이론, 전자기학, 신호 및 시스템, 반도체 공학 등 전기전자 개념을 쉽고 명확하게 설명해줘. "
                    "코드나 수식이 필요하면 깔끔하게 정리해 주고, 정중하면서도 친절하게 답변해줘."
                )
            }
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    question = st.chat_input("전기전자공학 질문을 입력하세요 (예: KVL이 뭐야?, RLC 회로 해석법)")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            status_context = f"현재 사용자의 학습목록 및 달성상태: {st.session_state.ee_topics}"
            prompt = st.session_state.messages + [{"role": "system", "content": status_context}]
            
            with st.spinner("AI 튜터가 회로와 개념을 분석 중...⚡"):
                response = ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=prompt
                )
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                
        st.session_state.messages.append({"role": "assistant", "content": ai_response})


# 네비게이션 설정
pg = st.navigation([
    st.Page(page_goal, title="오늘의 공학 목표", icon="⚡"),
    st.Page(page_topics, title="학습 체크리스트", icon="✅"),
    st.Page(page_report, title="학습 진도율", icon="📈"),
    st.Page(page_ai_tutor, title="EE AI 튜터", icon="🧐")
], position="top")

st.title("🔌 전기전자공학 학습 플래너")
pg.run()


