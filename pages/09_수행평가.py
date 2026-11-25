
import streamlit as st

st.set_page_config(
    page_title="나의 공부 습관 분석소",
    page_icon="📚",
    layout="wide"
)

st.title("📚 나의 공부 습관 분석소")
st.subheader("나의 공부 습관을 분석하고 똑똑하게 공부하자!")

st.write("""
안녕하세요! 😊

이 프로그램은 과목별 공부 시간을 기록하고
나의 공부 습관을 분석해 주는 프로그램입니다.

공부 시간을 입력하면 자동으로 계산하고
나에게 맞는 학습 전략을 추천해 줍니다.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("⏰")
    st.write("공부 시간 기록")

with col2:
    st.subheader("📊")
    st.write("데이터 분석")

with col3:
    st.subheader("💡")
    st.write("학습 전략 추천")

st.divider()

st.header("🎯 프로그램 사용 방법")

st.write("""
1. 왼쪽 메뉴에서 공부 습관 분석을 선택합니다.
2. 이름을 입력합니다.
3. 과목별 공부 시간을 입력합니다.
4. 분석하기 버튼을 누릅니다.
5. 나의 공부 결과와 그래프를 확인합니다.
""")

st.success("오늘도 열심히 공부해 봐요! 화이팅! 💪")

st.info("작은 노력이 모이면 큰 결과가 됩니다. 🌟")

st.caption("인공지능 기초 수행평가")
