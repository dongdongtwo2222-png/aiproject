
import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="나의 공부 습관 분석소",
    page_icon="📚",
    layout="wide"
)

# 제목
st.title("📚 나의 공부 습관 분석소")
st.write("과목별 공부 시간을 입력하면 나의 공부 습관을 분석하고 맞춤 조언을 해주는 프로그램입니다.")

st.divider()

# 이름 입력
name = st.text_input("이름을 입력하세요")

# 공부 시간 입력
st.subheader("✏️ 과목별 공부 시간 입력")
st.write("오늘 각 과목을 몇 시간 공부했는지 입력하세요.")

col1, col2, col3 = st.columns(3)

with col1:
    korean = st.number_input("국어 (시간)", min_value=0.0, max_value=24.0, step=0.5)
    english = st.number_input("영어 (시간)", min_value=0.0, max_value=24.0, step=0.5)

with col2:
    math = st.number_input("수학 (시간)", min_value=0.0, max_value=24.0, step=0.5)
    science = st.number_input("과학 (시간)", min_value=0.0, max_value=24.0, step=0.5)

with col3:
    social = st.number_input("사회 (시간)", min_value=0.0, max_value=24.0, step=0.5)
    other = st.number_input("기타 (시간)", min_value=0.0, max_value=24.0, step=0.5)

# 데이터 만들기
data = {
    "과목": ["국어", "영어", "수학", "과학", "사회", "기타"],
    "공부 시간": [korean, english, math, science, social, other]
}

df = pd.DataFrame(data)

st.divider()

# 분석 버튼
if st.button("📊 공부 습관 분석하기", use_container_width=True):

    total = df["공부 시간"].sum()

    if total == 0:
        st.warning("공부 시간을 하나 이상 입력해주세요.")

    else:
        st.subheader(f"🎯 {name if name else '학생'}님의 공부 습관 분석 결과")

        # 공부 시간 통계
        studied = df[df["공부 시간"] > 0]
        most_subject = studied.loc[studied["공부 시간"].idxmax(), "과목"]
        least_subject = studied.loc[studied["공부 시간"].idxmin(), "과목"]
        average = studied["공부 시간"].mean()

        col1, col2, col3 = st.columns(3)

        col1.metric("총 공부 시간", f"{total:.1f}시간")
        col2.metric("과목당 평균 공부 시간", f"{average:.1f}시간")
        col3.metric("가장 많이 공부한 과목", most_subject)

        st.write(f"**가장 적게 공부한 과목:** {least_subject}")

        st.divider()

        # 막대그래프
        st.subheader("📊 과목별 공부 시간")
        bar_chart = px.bar(
            df,
            x="과목",
            y="공부 시간",
            color="과목",
            title="과목별 공부 시간 비교",
            text="공부 시간"
        )
        st.plotly_chart(bar_chart, use_container_width=True)

        # 원그래프
        st.subheader("🥧 공부 시간 비율")
        pie_chart = px.pie(
            studied,
            names="과목",
            values="공부 시간",
            title="과목별 공부 시간 비율"
        )
        st.plotly_chart(pie_chart, use_container_width=True)

        # 맞춤 조언
        st.subheader("💡 나의 공부 습관 조언")

        if total < 2:
            st.info("공부 시간이 조금 부족해요. 하루에 조금씩 공부 시간을 늘려보세요.")
        elif total < 5:
            st.success("좋아요! 꾸준히 공부하고 있네요. 매일 규칙적인 학습 습관을 유지해보세요.")
        else:
            st.success("정말 열심히 공부했어요! 충분한 휴식도 함께 챙기는 것이 중요해요.")

        if least_subject:
            st.write(f"📌 **추천:** 상대적으로 공부 시간이 적은 {least_subject} 과목도 조금씩 공부해보세요.")

        # 결과 표
        st.subheader("📝 공부 시간 기록표")
        st.dataframe(df, use_container_width=True)

        # CSV 다운로드
        csv = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="📥 공부 기록 다운로드",
            data=csv,
            file_name="나의_공부습관.csv",
            mime="text/csv"
        )

        st.balloons()
