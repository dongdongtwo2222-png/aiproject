import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="서울 외국인 인기 관광지 TOP 10", page_icon="🗺️", layout="wide")

# 위도·경도는 각 관광지의 대표 지점 기준입니다.
# TOP 10은 외국인 여행객에게 잘 알려진 대표 명소를 주제별로 선정한 편집 목록이며,
# 실시간 방문객 통계에 따른 공식 순위는 아닙니다.
PLACES = [
    {"rank": 1, "name": "경복궁", "en": "Gyeongbokgung Palace",
     "lat": 37.5796, "lon": 126.9770, "area": "종로구",
     "desc": "조선 왕조의 법궁으로, 웅장한 근정전과 아름다운 궁궐 풍경을 만날 수 있습니다. 한복을 입고 방문하면 특별한 추억을 만들 수 있어요.",
     "tip": "수문장 교대의식 시간과 휴궁일을 방문 전에 확인하세요."},
    {"rank": 2, "name": "N서울타워", "en": "N Seoul Tower",
     "lat": 37.5512, "lon": 126.9882, "area": "용산구·남산",
     "desc": "남산 정상에서 서울의 전경을 감상할 수 있는 랜드마크입니다. 특히 해 질 무렵과 야경이 아름답습니다.",
     "tip": "케이블카 또는 남산 순환버스를 이용할 수 있습니다."},
    {"rank": 3, "name": "명동", "en": "Myeongdong",
     "lat": 37.5636, "lon": 126.9869, "area": "중구",
     "desc": "화장품·패션 쇼핑과 길거리 음식으로 유명한 번화가입니다. 다양한 한국 간식과 K-뷰티 매장을 둘러보기 좋습니다.",
     "tip": "노점 운영 시간은 요일과 날씨에 따라 달라질 수 있습니다."},
    {"rank": 4, "name": "북촌한옥마을", "en": "Bukchon Hanok Village",
     "lat": 37.5826, "lon": 126.9830, "area": "종로구",
     "desc": "전통 한옥이 이어지는 골목에서 서울의 옛 주거 문화를 느낄 수 있습니다. 사진 명소로도 인기가 높습니다.",
     "tip": "실제 주민이 거주하는 곳이므로 조용히 관람하고 출입 제한 안내를 지켜주세요."},
    {"rank": 5, "name": "인사동", "en": "Insadong",
     "lat": 37.5740, "lon": 126.9855, "area": "종로구",
     "desc": "전통 공예품과 갤러리, 찻집이 모여 있는 문화 거리입니다. 한국적인 기념품을 찾기에 좋습니다.",
     "tip": "쌈지길과 주변 골목을 함께 둘러보세요."},
    {"rank": 6, "name": "홍대·연남동", "en": "Hongdae & Yeonnam-dong",
     "lat": 37.5563, "lon": 126.9236, "area": "마포구",
     "desc": "젊은 문화와 거리 공연, 개성 있는 카페·상점으로 유명한 지역입니다. 서울의 트렌디한 분위기를 경험할 수 있습니다.",
     "tip": "주말 저녁에는 사람이 많으니 대중교통 이용을 추천합니다."},
    {"rank": 7, "name": "동대문디자인플라자(DDP)", "en": "Dongdaemun Design Plaza",
     "lat": 37.5669, "lon": 127.0095, "area": "중구",
     "desc": "독특한 곡선형 건축물이 인상적인 디자인·전시·문화 공간입니다. 주변 동대문 쇼핑 지역과 함께 방문하기 좋습니다.",
     "tip": "전시별 운영 시간과 입장료를 미리 확인하세요."},
    {"rank": 8, "name": "광장시장", "en": "Gwangjang Market",
     "lat": 37.5700, "lon": 126.9997, "area": "종로구",
     "desc": "빈대떡, 마약김밥 등 다양한 한국 길거리 음식을 맛볼 수 있는 전통시장입니다.",
     "tip": "점포마다 영업시간이 다르며 현금·카드 결제 여부를 확인하세요."},
    {"rank": 9, "name": "롯데월드타워·서울스카이", "en": "Lotte World Tower & Seoul Sky",
     "lat": 37.5125, "lon": 127.1025, "area": "송파구",
     "desc": "높은 전망대에서 서울과 한강을 파노라마로 감상할 수 있습니다. 쇼핑몰과 아쿠아리움 등 주변 즐길 거리도 풍부합니다.",
     "tip": "전망대는 날씨와 시야에 따라 풍경이 달라집니다."},
    {"rank": 10, "name": "청계천", "en": "Cheonggyecheon Stream",
     "lat": 37.5692, "lon": 126.9788, "area": "종로구·중구",
     "desc": "도심 한가운데를 흐르는 산책로로, 야간 조명과 계절별 행사도 즐길 수 있습니다.",
     "tip": "광화문에서 동대문 방향으로 걷는 코스가 편리합니다."},
]
# 청계천 청계광장 부근 대표 좌표
PLACES[-1]["lon"] = 126.9788

st.title("🗺️ 외국인 여행객을 위한 서울 인기 관광지 TOP 10")
st.caption("서울의 대표 명소 10곳을 지도에서 확인하고, 아래에서 간단한 여행 팁을 살펴보세요.")
st.info("참고: 아래 TOP 10은 외국인에게 잘 알려진 대표 관광지를 종합해 구성한 안내용 목록입니다. 특정 연도의 공식 방문객 순위나 실시간 통계 순위는 아닙니다.")

m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, tiles="OpenStreetMap", control_scale=True)
for p in PLACES:
    popup_html = f"""
    <div style='font-family: sans-serif; width:220px'>
      <b>TOP {p['rank']}. {p['name']}</b><br>
      <span style='color:#555'>{p['en']}</span><br>
      <small>{p['area']}</small><br><br>{p['desc']}
    </div>"""
    folium.Marker(
        location=[p["lat"], p["lon"]],
        tooltip=f"TOP {p['rank']} · {p['name']}",
        popup=folium.Popup(popup_html, max_width=280),
        icon=folium.DivIcon(html=f"""
          <div style="background:#e53935;color:white;border:2px solid white;
          border-radius:50%;width:30px;height:30px;text-align:center;
          line-height:26px;font-weight:bold;box-shadow:0 1px 5px #555;">
          {p['rank']}</div>""")
    ).add_to(m)

# 지도 아래 관광지 설명
st.subheader("서울 인기 관광지 지도")
st_folium(m, width=None, height=590, returned_objects=[])

st.subheader("관광지 한눈에 보기")
for row_start in range(0, len(PLACES), 2):
    cols = st.columns(2)
    for col, p in zip(cols, PLACES[row_start:row_start+2]):
        with col:
            with st.container(border=True):
                st.markdown(f"### {p['rank']}. {p['name']}")
                st.caption(f"{p['en']} · {p['area']}")
                st.write(p["desc"])
                st.markdown(f"💡 **여행 팁:** {p['tip']}")

st.divider()
st.caption("지도 데이터: OpenStreetMap · 위치는 관광지 대표 지점의 대략적인 좌표입니다. 방문 전 공식 홈페이지에서 운영 정보를 확인하세요.")
