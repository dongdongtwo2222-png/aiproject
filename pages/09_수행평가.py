
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from pathlib import Path

# ==========================================
# 기본 설정
# ==========================================

st.set_page_config(
    page_title="인공지능 기초 수행평가",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 인공지능 기초 수행평가")
st.caption("MBTI로 알아보는 나의 진로, 책, 영화 그리고 세계 데이터 분석!")

st.sidebar.title("📚 수행평가 메뉴")
menu = st.sidebar.radio(
    "원하는 메뉴를 선택하세요!",
    [
        "🏠 처음 화면",
        "🧠 MBTI 진로 추천",
        "📚 MBTI 책 추천",
        "🎬 MBTI 영화 추천",
        "🗺️ 서울 관광지 지도",
        "📊 국가별 MBTI 데이터 분석"
    ]
)

# ==========================================
# MBTI 데이터
# ==========================================

mbti_data = {
    "ISTJ": {
        "career": [
            ("회계사", "회계학과, 경영학과", "꼼꼼하고 책임감이 강하며 숫자와 규칙을 잘 다루는 사람"),
            ("공무원", "행정학과, 법학과", "성실하고 계획적이며 맡은 일을 끝까지 해내는 사람")
        ],
        "books": [
            ("아주 작은 습관의 힘", "제임스 클리어", "체계적인 계획과 꾸준한 실천을 좋아하는 ISTJ에게 잘 맞는 책이야."),
            ("팩트풀니스", "한스 로슬링", "사실과 데이터를 바탕으로 세상을 바라보는 능력을 키워줘.")
        ],
        "movies": [
            ("히든 피겨스", "2016", "성실함과 정확한 계산 능력으로 자신의 실력을 증명하는 이야기야."),
            ("이미테이션 게임", "2014", "논리적인 사고와 끈기로 어려운 문제를 해결하는 모습을 보여줘.")
        ]
    },
    "ISFJ": {
        "career": [
            ("간호사", "간호학과", "다른 사람을 배려하고 세심하게 돌볼 수 있는 사람"),
            ("초등교사", "초등교육과", "책임감이 강하고 다른 사람의 성장을 돕는 사람")
        ],
        "books": [
            ("모모", "미하엘 엔데", "사람들의 이야기를 귀 기울여 듣는 따뜻한 마음을 생각하게 해."),
            ("아몬드", "손원평", "감정과 공감의 의미를 돌아보게 하는 책이야.")
        ],
        "movies": [
            ("원더", "2017", "다름을 이해하고 서로 배려하는 마음을 알려줘."),
            ("인사이드 아웃", "2015", "다양한 감정을 이해하고 공감하는 데 도움을 줘.")
        ]
    },
    "INFJ": {
        "career": [
            ("상담사", "심리학과, 상담심리학과", "다른 사람의 마음을 이해하고 깊이 공감하는 사람"),
            ("작가", "문예창작학과, 국어국문학과", "상상력이 풍부하고 자신의 생각을 글로 표현하는 사람")
        ],
        "books": [
            ("데미안", "헤르만 헤세", "자신의 정체성과 삶의 의미를 고민하는 사람에게 추천해."),
            ("연금술사", "파울로 코엘료", "자신만의 꿈과 목표를 찾아가는 과정을 담고 있어.")
        ],
        "movies": [
            ("죽은 시인의 사회", "1989", "자신만의 삶과 꿈을 찾아가는 용기를 보여줘."),
            ("굿 윌 헌팅", "1997", "자신의 가능성과 내면을 발견하는 과정을 담고 있어.")
        ]
    },
    "INTJ": {
        "career": [
            ("AI 연구원", "컴퓨터공학과, 인공지능학과", "논리적이고 분석적이며 새로운 기술을 연구하는 사람"),
            ("건축가", "건축학과", "전체적인 구조를 설계하고 장기적인 계획을 세우는 사람")
        ],
        "books": [
            ("생각에 관한 생각", "대니얼 카너먼", "인간의 사고방식을 분석하고 논리적으로 생각하는 데 도움을 줘."),
            ("코스모스", "칼 세이건", "과학적 호기심과 깊이 있는 탐구심을 키워줘.")
        ],
        "movies": [
            ("인터스텔라", "2014", "과학적 상상력과 복잡한 문제 해결 과정을 보여줘."),
            ("마션", "2015", "논리와 계획을 바탕으로 위기를 해결하는 이야기야.")
        ]
    },
    "ISTP": {
        "career": [
            ("기계공학자", "기계공학과", "기계를 직접 다루고 문제를 해결하는 것을 좋아하는 사람"),
            ("소방관", "소방방재학과", "침착하고 상황 판단이 빠르며 실전 대응 능력이 좋은 사람")
        ],
        "books": [
            ("이기적 유전자", "리처드 도킨스", "과학적인 원리를 탐구하고 분석하는 재미를 느낄 수 있어."),
            ("정의란 무엇인가", "마이클 샌델", "다양한 문제를 논리적으로 생각해 볼 수 있어.")
        ],
        "movies": [
            ("아이언맨", "2008", "기술과 창의적인 문제 해결 능력이 돋보이는 영화야."),
            ("탑건: 매버릭", "2022", "위기 상황에서 침착하게 판단하는 모습을 보여줘.")
        ]
    },
    "ISFP": {
        "career": [
            ("디자이너", "시각디자인학과, 산업디자인학과", "감각적이고 창의적이며 자신만의 표현을 좋아하는 사람"),
            ("수의사", "수의학과", "동물을 사랑하고 세심하게 돌보는 사람")
        ],
        "books": [
            ("어린 왕자", "생텍쥐페리", "따뜻한 감성과 관계의 소중함을 느낄 수 있어."),
            ("나미야 잡화점의 기적", "히가시노 게이고", "사람들의 고민과 감정을 따뜻하게 바라보게 해.")
        ],
        "movies": [
            ("리틀 포레스트", "2018", "자연과 일상의 아름다움을 느낄 수 있는 영화야."),
            ("소울", "2020", "자신이 좋아하는 것과 삶의 의미를 생각하게 해.")
        ]
    },
    "INFP": {
        "career": [
            ("작가", "문예창작학과, 국어국문학과", "풍부한 상상력과 자신만의 가치관을 가진 사람"),
            ("심리상담사", "심리학과, 상담심리학과", "다른 사람의 감정에 공감하고 진심으로 돕는 사람")
        ],
        "books": [
            ("나미야 잡화점의 기적", "히가시노 게이고", "따뜻한 위로와 사람 사이의 연결을 느낄 수 있어."),
            ("데미안", "헤르만 헤세", "자신만의 가치관과 진정한 자아를 고민하게 해.")
        ],
        "movies": [
            ("월터의 상상은 현실이 된다", "2013", "상상에 머무르지 않고 꿈을 실천하는 용기를 줘."),
            ("코코", "2017", "가족과 꿈, 자신의 정체성에 대해 생각하게 해.")
        ]
    },
    "INTP": {
        "career": [
            ("데이터 과학자", "통계학과, 컴퓨터공학과", "논리적으로 분석하고 새로운 규칙을 발견하는 사람"),
            ("연구원", "자연과학계열 학과", "호기심이 많고 깊이 있게 탐구하는 사람")
        ],
        "books": [
            ("괴델, 에셔, 바흐", "더글러스 호프스태터", "논리와 수학, 예술의 연결을 탐구하는 흥미로운 책이야."),
            ("코스모스", "칼 세이건", "과학적 질문을 좋아하는 사람에게 추천해.")
        ],
        "movies": [
            ("소셜 네트워크", "2010", "아이디어와 기술이 세상을 바꾸는 과정을 보여줘."),
            ("엑스 마키나", "2014", "인공지능과 인간의 관계에 대해 생각하게 해.")
        ]
    },
    "ESTP": {
        "career": [
            ("기업가", "경영학과, 창업학과", "도전정신이 강하고 빠른 실행력을 가진 사람"),
            ("응급구조사", "응급구조학과", "긴급한 상황에서도 침착하고 행동력이 좋은 사람")
        ],
        "books": [
            ("그릿", "앤절라 더크워스", "목표를 향해 도전하고 끝까지 노력하는 태도를 알려줘."),
            ("타이탄의 도구들", "팀 페리스", "다양한 성공 전략과 실천 방법을 배울 수 있어.")
        ],
        "movies": [
            ("캐치 미 이프 유 캔", "2002", "빠른 판단과 대담한 행동이 돋보이는 영화야."),
            ("미션 임파서블: 폴아웃", "2018", "위기 속에서 행동력과 순발력이 얼마나 중요한지 보여줘.")
        ]
    },
    "ESFP": {
        "career": [
            ("방송인", "미디어커뮤니케이션학과", "사람들과 소통하고 즐거움을 전달하는 사람"),
            ("이벤트 기획자", "광고홍보학과, 문화콘텐츠학과", "활동적이고 사람들과 함께 일하는 것을 좋아하는 사람")
        ],
        "books": [
            ("미움받을 용기", "기시미 이치로, 고가 후미타케", "다른 사람의 시선보다 자신의 삶에 집중하도록 도와줘."),
            ("아몬드", "손원평", "사람들의 감정과 관계를 이해하는 계기가 될 수 있어.")
        ],
        "movies": [
            ("맘마미아!", "2008", "밝고 활기찬 분위기와 즐거운 음악이 매력적이야."),
            ("라라랜드", "2016", "꿈을 향해 도전하는 열정과 낭만을 느낄 수 있어.")
        ]
    },
    "ENFP": {
        "career": [
            ("광고기획자", "광고홍보학과, 미디어학과", "아이디어가 풍부하고 사람들의 관심을 끄는 것을 좋아하는 사람"),
            ("콘텐츠 크리에이터", "영상학과, 미디어커뮤니케이션학과", "창의적이고 새로운 콘텐츠를 만드는 것을 즐기는 사람")
        ],
        "books": [
            ("연금술사", "파울로 코엘료", "자신의 꿈을 믿고 도전하는 용기를 얻을 수 있어."),
            ("모모", "미하엘 엔데", "상상력과 사람 사이의 소중한 시간을 생각하게 해.")
        ],
        "movies": [
            ("위대한 쇼맨", "2017", "자신만의 개성과 꿈을 세상에 보여주는 이야기야."),
            ("인사이드 아웃", "2015", "다양한 감정을 이해하고 자신을 알아가는 데 좋아.")
        ]
    },
    "ENTP": {
        "career": [
            ("벤처 창업가", "경영학과, 산업공학과", "새로운 아이디어를 만들고 도전하는 것을 좋아하는 사람"),
            ("변호사", "법학과", "논리적으로 토론하고 다양한 관점에서 문제를 바라보는 사람")
        ],
        "books": [
            ("사피엔스", "유발 하라리", "기존의 생각을 넘어 인류의 역사를 새로운 관점에서 바라보게 해."),
            ("생각에 관한 생각", "대니얼 카너먼", "인간의 판단과 사고 과정에 대해 흥미롭게 배울 수 있어.")
        ],
        "movies": [
            ("소셜 네트워크", "2010", "새로운 아이디어로 세상을 바꾸는 도전이 흥미로워."),
            ("나이브스 아웃", "2019", "추리와 반전, 논리적인 사고를 즐길 수 있어.")
        ]
    },
    "ESTJ": {
        "career": [
            ("경영자", "경영학과, 경제학과", "조직을 이끌고 목표를 달성하는 능력이 좋은 사람"),
            ("경찰관", "경찰행정학과", "책임감이 강하고 규칙과 질서를 중요하게 생각하는 사람")
        ],
        "books": [
            ("성공하는 사람들의 7가지 습관", "스티븐 코비", "체계적으로 목표를 세우고 실천하는 방법을 배울 수 있어."),
            ("아주 작은 습관의 힘", "제임스 클리어", "꾸준한 습관과 자기관리의 중요성을 알려줘.")
        ],
        "movies": [
            ("머니볼", "2011", "데이터를 활용해 조직의 문제를 해결하는 모습이 인상적이야."),
            ("인턴", "2015", "조직에서 책임감과 협력의 중요성을 배울 수 있어.")
        ]
    },
    "ESFJ": {
        "career": [
            ("교사", "교육학과, 사범대학", "사람들과 잘 어울리고 다른 사람의 성장을 돕는 사람"),
            ("호텔리어", "호텔관광학과", "친절하고 배려심이 있으며 서비스 정신이 좋은 사람")
        ],
        "books": [
            ("어린 왕자", "생텍쥐페리", "사람들과의 관계와 배려의 가치를 생각하게 해."),
            ("완득이", "김려령", "다양한 사람들의 삶과 관계를 따뜻하게 바라볼 수 있어.")
        ],
        "movies": [
            ("원더", "2017", "배려와 친절이 얼마나 큰 힘을 가지는지 보여줘."),
            ("인턴", "2015", "세대와 관계를 넘어 서로 배우고 협력하는 모습을 담고 있어.")
        ]
    },
    "ENFJ": {
        "career": [
            ("교육 컨설턴트", "교육학과, 교육공학과", "다른 사람의 가능성을 발견하고 성장을 돕는 사람"),
            ("사회복지사", "사회복지학과", "공감 능력이 뛰어나고 사회에 긍정적인 영향을 주고 싶은 사람")
        ],
        "books": [
            ("미움받을 용기", "기시미 이치로, 고가 후미타케", "타인과의 관계 속에서 자신의 삶을 주체적으로 바라보게 해."),
            ("죽음의 수용소에서", "빅터 프랭클", "삶의 의미와 인간의 내면에 대해 깊이 생각하게 해.")
        ],
        "movies": [
            ("죽은 시인의 사회", "1989", "다른 사람의 가능성을 믿고 꿈을 응원하는 이야기야."),
            ("굿 윌 헌팅", "1997", "진심 어린 관심과 격려가 사람을 변화시킬 수 있음을 보여줘.")
        ]
    },
    "ENTJ": {
        "career": [
            ("CEO", "경영학과, 경제학과", "목표 지향적이고 조직을 이끄는 리더십이 강한 사람"),
            ("변호사", "법학과", "논리적이고 결단력이 있으며 전략적으로 사고하는 사람")
        ],
        "books": [
            ("타이탄의 도구들", "팀 페리스", "성공한 사람들의 전략과 실행 방법을 배울 수 있어."),
            ("성공하는 사람들의 7가지 습관", "스티븐 코비", "리더십과 자기관리 능력을 키우는 데 도움을 줘.")
        ],
        "movies": [
            ("머니볼", "2011", "전략적인 판단과 리더십으로 성과를 만들어가는 이야기야."),
            ("악마는 프라다를 입는다", "2006", "경쟁적인 환경에서 성장하고 자신의 목표를 찾아가는 모습을 보여줘.")
        ]
    }
}

# ==========================================
# 처음 화면
# ==========================================

if menu == "🏠 처음 화면":
    st.header("🌟 인공지능 기초 수행평가에 오신 것을 환영합니다!")
    st.markdown("""
    ### 이번 수행평가에서는 무엇을 할까요?

    - 🧠 MBTI를 활용하여 나에게 어울리는 진로를 찾아봐요.
    - 📚 나의 성격 유형에 어울리는 책을 추천받아요.
    - 🎬 나의 성격 유형에 맞는 영화를 알아봐요.
    - 🗺️ 서울의 대표적인 관광지를 지도에서 확인해요.
    - 📊 여러 나라의 MBTI 데이터를 그래프로 분석해요.

    **자신을 알아보고, 데이터를 통해 세상을 이해해 봅시다! 🚀**
    """)
    st.info("왼쪽 메뉴에서 원하는 활동을 선택해 보세요!")

# ==========================================
# MBTI 선택
# ==========================================

elif menu in ["🧠 MBTI 진로 추천", "📚 MBTI 책 추천", "🎬 MBTI 영화 추천"]:

    st.header(menu)

    mbti = st.selectbox(
        "🧩 나의 MBTI 유형을 선택해 주세요!",
        list(mbti_data.keys())
    )

    data = mbti_data[mbti]

    st.subheader(f"✨ 당신의 MBTI는 {mbti}입니다!")

    if menu == "🧠 MBTI 진로 추천":

        st.write("나의 성격과 장점을 살릴 수 있는 진로를 추천할게!")

        for i, (career, major, personality) in enumerate(data["career"], 1):
            with st.container(border=True):
                st.subheader(f"💼 추천 진로 {i}: {career}")
                st.write(f"🎓 **추천 학과:** {major}")
                st.write(f"💡 **이런 성격에 잘 어울려요:** {personality}")

        st.success("MBTI는 진로를 결정하는 기준이 아니라 나를 이해하는 참고 자료야!")

    elif menu == "📚 MBTI 책 추천":

        st.write("나의 성격과 관심사에 어울리는 책을 골라봤어!")

        for i, (book, author, review) in enumerate(data["books"], 1):
            with st.container(border=True):
                st.subheader(f"📖 추천 도서 {i}: {book}")
                st.write(f"✍️ **저자:** {author}")
                st.write(f"💬 **한 줄 서평:** {review}")

        st.caption("도서는 실제 출간된 작품이며, 판매 여부와 재고는 서점에서 확인해 주세요.")

    elif menu == "🎬 MBTI 영화 추천":

        st.write("나의 성격과 어울리는 영화를 추천할게!")

        for i, (movie, year, review) in enumerate(data["movies"], 1):
            with st.container(border=True):
                st.subheader(f"🍿 추천 영화 {i}: {movie}")
                st.write(f"📅 **개봉 연도:** {year}년")
                st.write(f"💬 **한 줄 영화평:** {review}")

# ==========================================
# 서울 관광지 지도
# ==========================================

elif menu == "🗺️ 서울 관광지 지도":

    st.header("🗺️ 외국인이 좋아하는 서울 관광지 TOP 10")
    st.write("서울의 대표적인 관광지를 지도에서 확인해 보세요!")

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
        ("한강공원 여의도", 37.5283, 126.9327)
    ]

    map_seoul = folium.Map(
        location=[37.5665, 126.9780],
        zoom_start=12
    )

    for name, lat, lon in places:
        folium.Marker(
            [lat, lon],
            popup=name,
            tooltip=name,
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(map_seoul)

    st_folium(
        map_seoul,
        width=None,
        height=550,
        key="seoul_map"
    )

    st.subheader("📍 서울의 주요 관광지 목록")

    for i, (name, lat, lon) in enumerate(places, 1):
        st.write(f"**{i}. {name}**")

    st.caption("관광지 목록은 대표적인 서울 명소를 선정한 예시이며, 공식 방문객 순위는 아닙니다.")

# ==========================================
# 국가별 MBTI 데이터 분석
# ==========================================

elif menu == "📊 국가별 MBTI 데이터 분석":

    st.header("📊 나라별 MBTI 데이터 분석")
    st.write("판다스와 Plotly를 이용하여 국가별 MBTI 비율을 분석해 봅시다!")

    # CSV 파일은 pages 폴더의 상위 폴더에 있어야 함
    csv_path = Path(__file__).resolve().parent.parent / "countriesMBTI_16types.csv"

    if not csv_path.exists():
        st.error("❌ countriesMBTI_16types.csv 파일을 찾을 수 없습니다.")
        st.write("CSV 파일을 pages 폴더의 상위 폴더에 업로드해 주세요.")
        st.stop()

    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")

        st.subheader("1️⃣ 데이터 기본 정보")

        col1, col2, col3 = st.columns(3)

        col1.metric("전체 행 개수", f"{len(df):,}개")
        col2.metric("전체 열 개수", f"{len(df.columns):,}개")
        col3.metric("결측치 개수", f"{int(df.isna().sum().sum()):,}개")

        with st.expander("📋 데이터 미리보기"):
            st.dataframe(df, use_container_width=True)

        with st.expander("🔍 판다스 데이터 분석"):
            st.write("**컬럼 이름**")
            st.write(df.columns.tolist())

            st.write("**데이터 자료형**")
            st.dataframe(
                df.dtypes.astype(str).rename("자료형"),
                use_container_width=True
            )

            st.write("**기초 통계량**")
            st.dataframe(
                df.describe(include="all").T,
                use_container_width=True
            )

            st.write("**결측치 확인**")
            missing = df.isnull().sum().to_frame("결측치 개수")
            st.dataframe(missing, use_container_width=True)

        # 국가 컬럼 찾기
        country_candidates = [
            "Country", "country", "COUNTRY",
            "국가", "나라", "Country Name"
        ]

        country_col = next(
            (c for c in country_candidates if c in df.columns),
            None
        )

        # MBTI 컬럼 찾기
        mbti_types = [
            "ISTJ", "ISFJ", "INFJ", "INTJ",
            "ISTP", "ISFP", "INFP", "INTP",
            "ESTP", "ESFP", "ENFP", "ENTP",
            "ESTJ", "ESFJ", "ENFJ", "ENTJ"
        ]

        available_types = [
            m for m in mbti_types if m in df.columns
        ]

        # 국가 컬럼이 없으면 국가 이름이 들어 있는 첫 번째 문자열 컬럼 사용
        if country_col is None:
            string_cols = df.select_dtypes(
                include=["object", "string"]
            ).columns.tolist()

            if string_cols:
                country_col = string_cols[0]

        if country_col is None:
            st.error("국가 이름이 들어 있는 컬럼을 찾지 못했습니다.")
            st.write("실제 CSV 컬럼:", df.columns.tolist())
            st.stop()

        if len(available_types) == 0:
            st.error("MBTI 16개 유형의 컬럼을 찾지 못했습니다.")
            st.write("실제 CSV 컬럼:", df.columns.tolist())
            st.info(
                "CSV의 MBTI 컬럼 이름을 ISTJ, ISFJ 등 16개 유형으로 "
                "확인해 주세요."
            )
            st.stop()

        st.subheader("2️⃣ 국가 선택")

        countries = sorted(
            df[country_col].dropna().astype(str).unique().tolist()
        )

        if not countries:
            st.warning("CSV 파일에 국가 데이터가 없습니다.")
            st.stop()

        selected_country = st.selectbox(
            "분석하고 싶은 국가를 선택하세요.",
            countries
        )

        country_df = df[
            df[country_col].astype(str) == selected_country
        ]

        # 선택 국가의 MBTI 값 계산
        values = country_df[available_types].apply(
            pd.to_numeric,
            errors="coerce"
        ).mean().fillna(0)

        # 1위부터 정렬
        result = values.sort_values(ascending=False)

        result_df = pd.DataFrame({
            "MBTI": result.index,
            "비율": result.values
        })

        # 1위 빨간색, 나머지는 순위별 색상
        colors = [
            "#FF3030" if i == 0 else px.colors.sample_colorscale(
                "Blues",
                [0.35 + 0.6 * (i / max(len(result)-1, 1))]
            )[0]
            for i in range(len(result))
        ]

        st.subheader(f"3️⃣ {selected_country}의 MBTI 비율")

        fig = px.bar(
            result_df,
            x="MBTI",
            y="비율",
            text="비율",
            title=f"{selected_country} MBTI 유형별 데이터",
            color="MBTI",
            color_discrete_map={
                name: colors[i]
                for i, name in enumerate(result.index)
            }
        )

        fig.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="MBTI 유형",
            yaxis_title="비율",
            template="plotly_white",
            yaxis_rangemode="tozero"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("4️⃣ 분석 결과")

        if len(result) > 0:
            st.success(
                f"🏆 {selected_country}에서 가장 높은 값을 보인 MBTI는 "
                f"**{result.index[0]}**입니다."
            )

            st.write(
                f"해당 유형의 데이터 값은 **{result.iloc[0]:.2f}**입니다."
            )

            st.write(
                f"가장 낮은 값을 보인 유형은 **{result.index[-1]}**입니다."
            )

        st.subheader("5️⃣ MBTI 유형별 순위표")

        result_df.index = range(1, len(result_df) + 1)
        st.dataframe(
            result_df.style.format({"비율": "{:.2f}"}),
            use_container_width=True
        )

        csv_data = result_df.to_csv(
            index=False,
            encoding="utf-8-sig"
        )

        st.download_button(
            "📥 분석 결과 CSV 다운로드",
            data=csv_data,
            file_name=f"{selected_country}_MBTI_analysis.csv",
            mime="text/csv"
        )

        st.caption(
            "※ CSV에 저장된 수치의 단위와 집계 방식에 따라 비율 해석이 달라질 수 있습니다. "
            "위 분석은 선택한 국가의 행들을 평균한 결과입니다."
        )

    except Exception as e:
        st.error("데이터 분석 중 오류가 발생했습니다.")
        st.write("오류 내용:", str(e))
        st.info(
            "CSV 파일의 인코딩, 컬럼 이름 및 데이터 형식을 확인해 주세요."
        )

# ==========================================
# 마무리
# ==========================================

st.sidebar.divider()
st.sidebar.success("🤖 인공지능 기초 수행평가")
st.sidebar.caption("나를 이해하고 데이터를 분석하는 즐거운 시간!")
