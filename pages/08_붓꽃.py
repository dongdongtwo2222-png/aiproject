
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# --------------------------------------------------
# 1. 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="Iris 붓꽃 품종 예측",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 Iris 붓꽃 품종 예측 프로그램")
st.write("랜덤 포레스트 머신러닝 알고리즘을 이용한 붓꽃 품종 분류")

st.divider()

# --------------------------------------------------
# 2. 데이터 불러오기
# --------------------------------------------------

@st.cache_data
def load_data():

    try:
        df = pd.read_csv("Iris(1).csv", encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv("Iris(1).csv", encoding="utf-8-sig")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    return df


try:
    df = load_data()

except Exception as e:
    st.error("데이터 파일을 불러올 수 없습니다.")
    st.error(str(e))
    st.stop()


# --------------------------------------------------
# 3. 컬럼 설정
# --------------------------------------------------

# 한글 컬럼명과 영문 컬럼명 모두 지원

column_mapping = {
    "꽃잎길이": ["꽃잎길이", "PetalLengthCm", "petal_length"],
    "꽃잎너비": ["꽃잎너비", "PetalWidthCm", "petal_width"],
    "품종": ["품종", "Species", "species"]
}


def find_column(candidates):

    for col in candidates:
        if col in df.columns:
            return col

    return None


length_col = find_column(column_mapping["꽃잎길이"])
width_col = find_column(column_mapping["꽃잎너비"])
target_col = find_column(column_mapping["품종"])


if not all([length_col, width_col, target_col]):
    st.error("데이터의 컬럼명을 확인해주세요.")
    st.write("현재 컬럼:", list(df.columns))
    st.stop()


# --------------------------------------------------
# 4. 데이터 전처리
# --------------------------------------------------

data = df[[length_col, width_col, target_col]].copy()

data[length_col] = pd.to_numeric(
    data[length_col], errors="coerce"
)

data[width_col] = pd.to_numeric(
    data[width_col], errors="coerce"
)

data = data.dropna()

# 중복 제거
data = data.drop_duplicates()

# --------------------------------------------------
# 5. 입력 범위 계산
# --------------------------------------------------

min_length = float(data[length_col].min())
max_length = float(data[length_col].max())

min_width = float(data[width_col].min())
max_width = float(data[width_col].max())


# --------------------------------------------------
# 6. 머신러닝 학습
# --------------------------------------------------

X = data[[length_col, width_col]]
y = data[target_col]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    max_depth=None
)

model.fit(X_train, y_train)


# --------------------------------------------------
# 7. 모델 성능 평가
# --------------------------------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)


# --------------------------------------------------
# 8. 데이터 정보
# --------------------------------------------------

st.subheader("📊 데이터 분석 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 데이터", f"{len(data)}개")

with col2:
    st.metric("붓꽃 품종", f"{y.nunique()}종")

with col3:
    st.metric("모델 정확도", f"{accuracy * 100:.1f}%")


st.divider()


# --------------------------------------------------
# 9. 사용자 입력
# --------------------------------------------------

st.subheader("🌱 붓꽃 측정값 입력")

st.info(
    f"""
    입력 가능한 범위를 확인하세요.

    - 꽃잎길이: {min_length:.1f} ~ {max_length:.1f} cm
    - 꽃잎너비: {min_width:.1f} ~ {max_width:.1f} cm

    위 범위는 학습 데이터의 최소값과 최대값입니다.
    """
)

col1, col2 = st.columns(2)

with col1:

    petal_length = st.number_input(
        "꽃잎길이 (cm)",
        min_value=min_length,
        max_value=max_length,
        value=5.0 if min_length <= 5.0 <= max_length else min_length,
        step=0.1,
        format="%.1f"
    )

with col2:

    petal_width = st.number_input(
        "꽃잎너비 (cm)",
        min_value=min_width,
        max_value=max_width,
        value=1.5 if min_width <= 1.5 <= max_width else min_width,
        step=0.1,
        format="%.1f"
    )


predict_button = st.button(
    "🔍 붓꽃 품종 예측하기",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# 10. 품종 예측
# --------------------------------------------------

if predict_button:

    input_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=[length_col, width_col]
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    st.divider()

    st.subheader("🎯 예측 결과")

    st.success(
        f"예측된 붓꽃 품종은 **{prediction}** 입니다."
    )

    # 품종별 예측 확률
    probability_df = pd.DataFrame({
        "품종": model.classes_,
        "예측 확률": probabilities
    })

    probability_df["예측 확률"] *= 100

    st.write("### 품종별 예측 확률")

    st.dataframe(
        probability_df.style.format(
            {"예측 확률": "{:.2f}%"}
        ),
        use_container_width=True
    )

    # --------------------------------------------------
    # 11. 시각화
    # --------------------------------------------------

    st.subheader("📈 꽃잎길이와 꽃잎너비 분포")

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.scatterplot(
        data=data,
        x=length_col,
        y=width_col,
        hue=target_col,
        palette="Set1",
        s=90,
        alpha=0.8,
        ax=ax
    )

    # 사용자 입력값 초록색 별 표시
    ax.scatter(
        petal_length,
        petal_width,
        color="green",
        marker="*",
        s=500,
        edgecolors="black",
        linewidths=1.2,
        label="사용자 입력값",
        zorder=10
    )

    ax.set_xlabel("꽃잎길이 (cm)", fontsize=12)
    ax.set_ylabel("꽃잎너비 (cm)", fontsize=12)

    ax.set_title(
        f"예측 결과: {prediction}",
        fontsize=15
    )

    ax.legend()
    ax.grid(alpha=0.3)

    st.pyplot(fig)

    plt.close(fig)

    # --------------------------------------------------
    # 12. 변수 중요도
    # --------------------------------------------------

    st.subheader("🔎 품종 예측에 영향을 주는 요소")

    importance_df = pd.DataFrame({
        "측정 항목": ["꽃잎길이", "꽃잎너비"],
        "중요도": model.feature_importances_
    })

    importance_df = importance_df.sort_values(
        "중요도",
        ascending=False
    )

    fig2, ax2 = plt.subplots(figsize=(8, 4))

    sns.barplot(
        data=importance_df,
        x="중요도",
        y="측정 항목",
        hue="측정 항목",
        legend=False,
        palette="viridis",
        ax=ax2
    )

    ax2.set_title("Random Forest 변수 중요도")
    ax2.set_xlabel("중요도")
    ax2.set_ylabel("측정 항목")

    st.pyplot(fig2)

    plt.close(fig2)

    # --------------------------------------------------
    # 13. 예측 결과 설명
    # --------------------------------------------------

    st.subheader("💡 예측 이유")

    st.write(
        f"""
        입력한 꽃잎길이는 **{petal_length:.1f} cm**,
        꽃잎너비는 **{petal_width:.1f} cm**입니다.

        랜덤 포레스트는 여러 개의 의사결정나무가
        입력값을 각각 분류한 결과를 종합하여
        가장 많은 표를 받은 품종을 예측합니다.

        가장 높은 예측 확률을 가진 품종은
        **{prediction}** 입니다.
        """
    )

    st.caption(
        "변수 중요도는 모델 전체에서 각 특성이 분류에 기여한 상대적 정도이며, "
        "개별 예측의 직접적인 원인을 의미하지는 않습니다."
    )


# --------------------------------------------------
# 14. 데이터 미리보기
# --------------------------------------------------

with st.expander("📋 원본 데이터 확인하기"):

    st.dataframe(
        data,
        use_container_width=True
    )

    st.write("품종별 데이터 개수")

    st.bar_chart(data[target_col].value_counts())


# --------------------------------------------------
# 15. 알고리즘 안내
# --------------------------------------------------

with st.expander("🤖 사용된 머신러닝 알고리즘"):

    st.markdown(
        """
        ### Random Forest (랜덤 포레스트)

        - 여러 개의 의사결정나무를 학습합니다.
        - 각각의 나무가 독립적으로 품종을 예측합니다.
        - 다수결 방식으로 최종 품종을 결정합니다.
        - 여러 나무의 예측 결과를 이용해 확률을 계산합니다.

        **사용한 학습 설정**

        - 알고리즘: RandomForestClassifier
        - 의사결정나무 수: 200개
        - 학습 데이터: 80%
        - 테스트 데이터: 20%
        - random_state: 42
        """
    )

st.divider()

st.caption(
    "Iris Flower Classification | Pandas + Scikit-learn + Streamlit"
)
