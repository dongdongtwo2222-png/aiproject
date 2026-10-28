import streamlit as st
st.title('먹방1일차!!')6
a=st.text_input('이름을 입력하새요!')
b=st.selectbox('좋아하는 음식을 선택하세요!",['온지음','산','윤서울'])
if st.button('인사말 생성'):
  st.write('반갑습니다')
