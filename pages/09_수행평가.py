
import streamlit as st
import pandas as pd
from pathlib import Path

# ======================================
# 기본 설정
# ======================================

st.set_page_config(
    page_title="인공지능 기초 수행평가",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 인공지능 기초 수행평가")
st.write("MBTI로 알아보는 진로, 책, 영화와 세계 데이터 분석!")

menu = st.sidebar.radio(
    "📚 메뉴 선택",
    [
        "🏠 처음 화면",
        "🧠 MBTI 진로 추천",
        "📚 MBTI 책 추천",
        "🎬 MBTI 영화 추천",
        "🗺️ 서울 관광지 지도",
        "📊 국가별 MBTI 데이터 분석"
    ]
)

# ======================================
# MBTI 데이터
# ======================================

data = {
"ISTJ": {
"career": [
("회계사", "회계학과, 경영학과", "꼼꼼하고 책임감이 강한 사람"),
("공무원", "행정학과, 법학과", "성실하고 계획적인 사람")],
"books": [
("아주 작은 습관의 힘", "제임스 클리어", "꾸준한 습관과 실천의 중요성을 알려줘."),
("팩트풀니스", "한스 로슬링", "데이터를 바탕으로 세상을 바라보게 해.")],
"movies": [
("히든 피겨스", "2016", "수학과 과학으로 편견을 극복하는 이야기야."),
("이미테이션 게임", "2014", "논리와 끈기로 문제를 해결하는 영화야.")]},

"ISFJ": {
"career": [
("간호사", "간호학과", "세심하고 배려심이 많은 사람"),
("초등교사", "초등교육과", "책임감 있고 다른 사람을 돕는 사람")],
"books": [
("모모", "미하엘 엔데", "다른 사람의 이야기를 듣는 소중함을 알려줘."),
("아몬드", "손원평", "감정과 공감의 의미를 생각하게 해.")],
"movies": [
("원더", "2017", "다름을 이해하고 배려하는 이야기야."),
("인사이드 아웃", "2015", "다양한 감정을 이해할 수 있어.")]},

"INFJ": {
"career": [
("상담사", "심리학과", "다른 사람의 마음을 이해하는 사람"),
("작가", "문예창작학과", "상상력과 표현력이 풍부한 사람")],
"books": [
("데미안", "헤르만 헤세", "자신의 정체성을 고민하게 해."),
("연금술사", "파울로 코엘료", "꿈을 향해 나아가는 용기를 줘.")],
"movies": [
("죽은 시인의 사회", "1989", "자신만의 꿈을 찾는 이야기야."),
("굿 윌 헌팅", "1997", "자신의 가능성을 발견하는 영화야.")]},

"INTJ": {
"career": [
("AI 연구원", "컴퓨터공학과", "분석적이고 논리적인 사람"),
("건축가", "건축학과", "계획적이고 창의적인 사람")],
"books": [
("생각에 관한 생각", "대니얼 카너먼", "인간의 사고방식을 분석해."),
("코스모스", "칼 세이건", "과학적 호기심을 키워줘.")],
"movies": [
("인터스텔라", "2014", "과학적 상상력이 돋보이는 영화야."),
("마션", "2015", "논리적으로 위기를 해결하는 이야기야.")]},

"ISTP": {
"career": [
("기계공학자", "기계공학과", "직접 만들고 문제를 해결하는 사람"),
("소방관", "소방방재학과", "침착하고 판단력이 빠른 사람")],
"books": [
("이기적 유전자", "리처드 도킨스", "생명과학의 원리를 탐구할 수 있어."),
("정의란 무엇인가", "마이클 샌델", "다양한 문제를 논리적으로 생각하게 해.")],
"movies": [
("아이언맨", "2008", "기술과 창의적인 문제 해결이 돋보여."),
("탑건: 매버릭", "2022", "위기 속에서 침착한 판단을 보여줘.")]},

"ISFP": {
"career": [
("디자이너", "시각디자인학과", "감각적이고 창의적인 사람"),
("수의사", "수의학과", "동물을 사랑하고 세심한 사람")],
"books": [
("어린 왕자", "생텍쥐페리", "따뜻한 감성과 관계의 소중함을 알려줘."),
("나미야 잡화점의 기적", "히가시노 게이고", "사람들의 고민을 따뜻하게 바라보게 해.")],
"movies": [
("리틀 포레스트", "2018", "자연과 일상의 아름다움을 보여줘."),
("소울", "2020", "삶의 의미를 생각하게 해.")]},

"INFP": {
"career": [
("작가", "문예창작학과", "상상력이 풍부한 사람"),
("심리상담사", "심리학과", "공감 능력이 뛰어난 사람")],
"books": [
("나미야 잡화점의 기적", "히가시노 게이고", "따뜻한 위로를 전해줘."),
("데미안", "헤르만 헤세", "자신만의 가치관을 고민하게 해.")],
"movies": [
("월터의 상상은 현실이 된다", "2013", "꿈을 실천하는 용기를 줘."),
("코코", "2017", "가족과 꿈의 소중함을 알려줘.")]},

"INTP": {
"career": [
("데이터 과학자", "통계학과, 컴퓨터공학과", "논리적으로 분석하는 사람"),
("연구원", "자연과학계열", "호기심이 많고 탐구심이 강한 사람")],
"books": [
("괴델, 에셔, 바흐", "더글러스 호프스태터", "논리와 수학의 재미를 알려줘."),
("코스모스", "칼 세이건", "과학적 질문과 탐구심을 키워줘.")],
"movies": [
("소셜 네트워크", "2010", "기술과 아이디어가 세상을 바꾸는 이야기야."),
("엑스 마키나", "2014", "인공지능과 인간의 관계를 생각하게 해.")]},

"ESTP": {
"career": [
("기업가", "경영학과", "도전정신과 실행력이 강한 사람"),
("응급구조사", "응급구조학과", "위기 상황에서 빠르게 행동하는 사람")],
"books": [
("그릿", "앤절라 더크워스", "목표를 향해 노력하는 태도를 알려줘."),
("타이탄의 도구들", "팀 페리스", "성공 전략과 실천 방법을 소개해.")],
"movies": [
("캐치 미 이프 유 캔", "2002", "대담하고 빠른 판단이 돋보여."),
("미션 임파서블: 폴아웃", "2018", "위기 상황에서의 행동력을 보여줘.")]},

"ESFP": {
"career": [
("방송인", "미디어커뮤니케이션학과", "사람들과 소통하는 것을 좋아하는 사람"),
("이벤트 기획자", "광고홍보학과", "활동적이고 사교적인 사람")],
"books": [
("미움받을 용기", "기시미 이치로, 고가 후미타케", "자신의 삶에 집중하도록 도와줘."),
("아몬드", "손원평", "감정과 관계를 생각하게 해.")],
"movies": [
("맘마미아!", "2008", "밝고 즐거운 음악이 매력적이야."),
("라라랜드", "2016", "꿈을 향한 열정과 낭만을 보여줘.")]},

"ENFP": {
"career": [
("광고기획자", "광고홍보학과", "아이디어가 풍부한 사람"),
("콘텐츠 크리에이터", "영상학과", "새로운 콘텐츠를 만드는 사람")],
"books": [
("연금술사", "파울로 코엘료", "꿈을 믿고 도전하는 용기를 줘."),
("모모", "미하엘 엔데", "상상력과 관계의 소중함을 알려줘.")],
"movies": [
("위대한 쇼맨", "2017", "자신만의 개성과 꿈을 보여줘."),
("인사이드 아웃", "2015", "감정을 이해하는 데 도움을 줘.")]},

"ENTP": {
"career": [
("창업가", "경영학과", "새로운 아이디어를 좋아하는 사람"),
("변호사", "법학과", "논리적인 토론을 즐기는 사람")],
"books": [
("사피엔스", "유발 하라리", "인류의 역사를 새로운 관점에서 바라봐."),
("생각에 관한 생각", "대니얼 카너먼", "인간의 판단과 사고를 탐구해.")],
"movies": [
("소셜 네트워크", "2010", "새로운 아이디어로 도전하는 이야기야."),
("나이브스 아웃", "2019", "추리와 반전을 즐길 수 있어.")]},

"ESTJ": {
"career": [
("경영자", "경영학과", "조직을 이끌고 목표를 달성하는 사람"),
("경찰관", "경찰행정학과", "책임감과 리더십이 있는 사람")],
"books": [
("성공하는 사람들의 7가지 습관", "스티븐 코비", "목표를 세우고 실천하는 방법을 알려줘."),
("아주 작은 습관의 힘", "제임스 클리어", "자기관리의 중요성을 알려줘.")],
"movies": [
("머니볼", "2011", "데이터를 활용해 문제를 해결해."),
("인턴", "2015", "협력과 책임감을 보여줘.")]},

"ESFJ": {
"career": [
("교사", "교육학과", "다른 사람의 성장을 돕는 사람"),
("호텔리어", "호텔관광학과", "친절하고 배려심이 많은 사람")],
"books": [
("어린 왕자", "생텍쥐페리", "관계와 배려의 가치를 생각하게 해."),
("완득이", "김려령", "다양한 사람들의 삶을 이해하게 해.")],
"movies": [
("원더", "2017", "배려와 친절의 힘을 보여줘."),
("인턴", "2015", "서로 배우고 협력하는 이야기야.")]},

"ENFJ": {
"career": [
("교육 컨설턴트", "교육학과", "다른 사람의 성장을 돕는 사람"),
("사회복지사", "사회복지학과", "공감 능력이 뛰어난 사람")],
"books": [
("미움받을 용기", "기시미 이치로, 고가 후미타케", "자신의 삶을 주체적으로 바라보게 해."),
("죽음의 수용소에서", "빅터 프랭클", "삶의 의미를 깊이 생각하게 해.")],
"movies": [
("죽은 시인의 사회", "1989", "다른 사람의 꿈을 응원하는 이야기야."),
("굿 윌 헌팅", "1997", "진심 어린 격려의 힘을 보여줘.")]},

"ENTJ": {
"career": [
("CEO", "경영학과", "목표 지향적이고 리더십이 강한 사람"),
("변호사", "법학과", "결단력과 전략적 사고가 뛰어난 사람")],
"books": [
("타이탄의 도구들", "팀 페리스", "성공 전략과 실행 방법을 알려줘."),
("성공하는 사람들의 7가지 습관", "스티븐 코비", "리더십과 자기관리 능력을 키워줘.")],
"movies": [
("머니볼", "2011", "전략적인 판단과 리더십을 보여줘."),
("악마는 프라다를 입는다", "2006", "경쟁 속에서 성장하는 이야기야.")]}
}

# ======================================
# 처음 화면
# ======================================

if menu == "🏠 처음 화면":
    st.header("🌟 환영합니다!")
    st.markdown("""
    ### 인공지능 기초 수행평가

    🧠 MBTI별 진로 추천

    📚 MBTI별 책 추천

    🎬 MBTI별 영화 추천

    🗺️ 서울 관광지 지도

    📊 나라별 MBTI 데이터 분석

    **나를 이해하고 데이터로 세상을 알아봐요! 🚀**
    """)

# ======================================
# MBTI 진로 / 책 / 영화
# ======================================

elif menu in [
    "🧠 MBTI 진로 추천",
    "📚 MBTI 책 추천",
    "🎬 MBTI 영화 추천"
]:

    st.header(menu)

    mbti = st.selectbox(
        "나의 MBTI를 선택하세요!",
        list(data.keys())
    )

    selected = data[mbti]

    st.subheader(f"✨ 나의 MBTI: {mbti}")

    if menu == "🧠 MBTI 진로 추천":

        for i, (career, major, personality) in enumerate(
            selected["career"], 1
        ):
            with st.container(border=True):
                st.subheader(f"💼 추천 진로 {i}: {career}")
                st.write("🎓 추천 학과:", major)
                st.write("💡 어울리는 성격:", personality)

    elif menu == "📚 MBTI 책 추천":

        for i, (book, author, review) in enumerate(
            selected["books"], 1
        ):
            with st.container(border=True):
                st.subheader(f"📖 {i}. {book}")
                st.write("✍️ 저자:", author)
                st.write("💬 한 줄 서평:", review)

    else:

        for i, (movie, year, review) in enumerate(
            selected["movies"], 1
        ):
            with st.container(border=True):
                st.subheader(f"🎬 {i}. {movie}")
                st.write("📅 개봉 연도:", year)
                st.write("💬 영화평:", review)

    st.info("MBTI는 진로를 결정하는 기준이 아니라 자기 이해를 위한 참고 자료야!")

# ======================================
# 서울 관광지 지도
# ======================================

elif menu == "🗺️ 서울 관광지 지도":

    st.header("🗺️ 서울 주요 관광지 TOP 10")

    places = [
        ("경복궁", 37.5796, 126.9770),
        ("남산서울타워", 37.5512, 126.9882),
        ("명동", 37.5636, 126.9869),
        ("북촌한옥마을", 37.5826, 126.9830),
        ("인사동", 37.5740, 126.9850),
        ("동대문디자인플라자", 37.5673, 127.0095),
        ("홍대거리", 37.5563, 126.9236),
        ("롯데월드", 37.5111, 127.0982),
        ("광장시장", 37.5700, 126.9998),
        ("여의도 한강공원", 37.5283, 126.9327)
    ]

    st.map(
        pd.DataFrame(
            [(lat, lon) for name, lat, lon in places],
            columns=["lat", "lon"]
        ),
        zoom=11
    )

    for i, (name, lat, lon) in enumerate(places, 1):
        st.write(f"📍 {i}. {name}")

    st.caption("서울의 대표 관광지를 표시한 예시 지도입니다.")

# ======================================
# 국가별 MBTI 데이터 분석
# ======================================

elif menu == "📊 국가별 MBTI 데이터 분석":

    st.header("📊 국가별 MBTI 데이터 분석")

    csv_path = (
        Path(__file__).resolve().parent.parent
        / "countriesMBTI_16types.csv"
    )

    if not csv_path.exists():
        st.error("CSV 파일을 찾을 수 없습니다.")
        st.write("countriesMBTI_16types.csv를 상위 폴더에 넣어 주세요.")
        st.stop()

    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")

        st.subheader("1️⃣ 데이터 미리보기")
        st.dataframe(df, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("전체 데이터", len(df))
        col2.metric("컬럼 개수", len(df.columns))
        col3.metric("결측치", int(df.isnull().sum().sum()))

        with st.expander("🔍 상세 데이터 분석"):
            st.write("컬럼 이름")
            st.write(df.columns.tolist())

            st.write("자료형")
            st.write(df.dtypes.astype(str))

            st.write("기초 통계량")
            st.dataframe(df.describe(include="all").T)

            st.write("결측치 분석")
            st.dataframe(df.isnull().sum())

        # 국가 컬럼 확인
        country_candidates = [
            "Country", "country", "COUNTRY",
            "국가", "나라", "Country Name"
        ]

        country_col = next(
            (c for c in country_candidates if c in df.columns),
            None
        )

        if country_col is None:
            text_cols = df.select_dtypes(
                include=["object", "string"]
            ).columns.tolist()

            if text_cols:
                country_col = text_cols[0]

        if country_col is None:
            st.error("국가 컬럼을 찾을 수 없습니다.")
            st.write(df.columns.tolist())
            st.stop()

        mbti_types = [
            "ISTJ", "ISFJ", "INFJ", "INTJ",
            "ISTP", "ISFP", "INFP", "INTP",
            "ESTP", "ESFP", "ENFP", "ENTP",
            "ESTJ", "ESFJ", "ENFJ", "ENTJ"
        ]

        available = [
            x for x in mbti_types if x in df.columns
        ]

        if not available:
            st.error("MBTI 16개 컬럼을 찾을 수 없습니다.")
            st.write("현재 CSV 컬럼:", df.columns.tolist())
            st.stop()

        countries = sorted(
            df[country_col].dropna().astype(str).unique()
        )

        if not countries:
            st.warning("국가 데이터가 없습니다.")
            st.stop()

        st.subheader("2️⃣ 국가 선택")

        country = st.selectbox(
            "분석할 국가를 선택하세요.",
            countries
        )

        country_df = df[
            df[country_col].astype(str) == country
        ]

        values = country_df[available].apply(
            pd.to_numeric,
            errors="coerce"
        ).mean().fillna(0)

        result = values.sort_values(ascending=False)

        result_df = pd.DataFrame({
            "MBTI": result.index,
            "비율": result.values
        })

        st.subheader(f"3️⃣ {country}의 MBTI 그래프")

        # Streamlit 기본 차트 사용
        # 1위 빨간색, 나머지 그라데이션 느낌
        chart_colors = [
            "#FF3030" if i == 0 else
            "#F4A3A8" if i == 1 else
            "#F6C6CA" if i == 2 else
            "#D9E8F5" if i % 2 == 0 else
            "#A8CBE8"
            for i in range(len(result))
        ]

        chart_data = result_df.set_index("MBTI")

        st.bar_chart(
            chart_data,
            color="#4A90E2",
            horizontal=True
        )

        st.subheader("🏆 MBTI 순위")

        if len(result) > 0:
            st.success(
                f"가장 높은 유형은 {result.index[0]}입니다!"
            )

            st.write(
                f"가장 높은 값: {result.iloc[0]:.2f}"
            )

            st.write(
                f"가장 낮은 유형: {result.index[-1]}"
            )

        result_df.index = range(1, len(result_df) + 1)

        st.dataframe(
            result_df.style.format({"비율": "{:.2f}"}),
            use_container_width=True
        )

        st.download_button(
            "📥 분석 결과 다운로드",
            data=result_df.to_csv(
                index=False,
                encoding="utf-8-sig"
            ),
            file_name="MBTI_분석결과.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error("데이터 분석 중 오류가 발생했습니다.")
        st.code(str(e))

# ======================================
# 마무리
# ======================================

st.sidebar.divider()
st.sidebar.success("수행평가 완료! 🎉")
st.sidebar.caption("인공지능 기초")
