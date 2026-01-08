"""Streamlit 요소 예제 페이지

이 파일은 단일 페이지에서 가능한 많은 Streamlit UI 요소들을 보여주기 위한 데모입니다.
각 요소 위에 한국어 각주(설명)가 있어 학습에 도움이 됩니다.

실행: `streamlit run streamlit_app.py`
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, time


def cached_heavy_calculation(x):
    # 각주: st.cache_data는 호출 비용이 큰 작업을 캐시하는 데 사용합니다.
    # 최신 Streamlit에서는 `st.cache_data` 사용을 권장합니다.
    @st.cache_data
    def _inner(val):
        # 모의 무거운 작업
        return val * 2

    return _inner(x)


def main():
    # 기본 텍스트 계층 구조
    st.title("Streamlit 요소 모음 페이지")
    st.header("기본 텍스트 및 마크다운")
    st.subheader("subheader 예시")
    st.markdown("**강조된 마크다운**과 [링크](https://docs.streamlit.io)")
    st.write("st.write는 가장 범용적인 출력 함수입니다. 문자열, 데이터프레임, 위젯 출력 모두 가능")
    st.text("일반 텍스트 출력: st.text")
    st.latex(r"E = mc^2")  # 각주: LaTeX 수식
    st.code("print('Hello, Streamlit')", language="python")

    st.header("위젯 — 상호작용 입력들")
    # 단순 버튼
    if st.button("클릭 버튼 — st.button"):
        st.success("버튼이 클릭되었습니다")

    # 체크박스
    chk = st.checkbox("체크박스 — 체크 시 보이는 텍스트")
    if chk:
        st.info("체크박스가 선택됨")

    # 라디오 / 셀렉트박스 / 멀티셀렉트
    choice = st.radio("라디오 선택", ("옵션 A", "옵션 B", "옵션 C"))
    st.write("선택된 라디오:", choice)

    sel = st.selectbox("셀렉트박스", ["사과", "배", "포도"])  # 한 항목 선택
    st.write("선택된 과일:", sel)

    multi = st.multiselect("멀티셀렉트", ["파이썬", "자바스크립트", "R"], default=["파이썬"])  # 복수 선택
    st.write("선택된 언어:", multi)

    # 슬라이더, 숫자 입력, 텍스트 입력
    num = st.slider("숫자 슬라이더", 0, 100, 25)
    st.write("슬라이더 값:", num)

    fnum = st.number_input("숫자 입력 (float)", value=3.14)
    st.write("입력된 숫자:", fnum)

    txt = st.text_input("텍스트 입력", "초기값")
    st.write("입력한 텍스트:", txt)

    ta = st.text_area("텍스트 영역", "여기에 긴 텍스트를 입력하세요")
    st.write("텍스트 길이:", len(ta))

    # 날짜/시간 입력
    d = st.date_input("날짜 선택", date.today())
    t = st.time_input("시간 선택", time(hour=12, minute=30))
    st.write("선택된 날짜와 시간:", d, t)

    st.header("파일 및 미디어")
    uploaded = st.file_uploader("파일 업로드", type=["csv", "png", "jpg", "txt"])  # 각주: 파일 업로더
    if uploaded is not None:
        st.write("업로드된 파일 이름:", uploaded.name)
        try:
            df = pd.read_csv(uploaded)
            st.dataframe(df.head())
        except Exception:
            st.write("이미지나 텍스트 파일일 수 있습니다. 아래에 미리보기 표시:")
            st.write(uploaded.read(200))

    # 카메라 입력 (브라우저에서 허용 필요)
    img = st.camera_input("카메라로 사진 찍기")
    if img:
        st.image(img)

    # 색상 선택
    color = st.color_picker("색상 선택", "#00f900")
    st.write("선택한 색:", color)

    st.header("레이아웃 — 컬럼, 익스팬더, 사이드바")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("온도", "22 °C", "+3 °C")  # 각주: metric은 KPI처럼 사용
    with col2:
        st.metric("습도", "60%", "-5%")

    with st.expander("추가 정보 (Expander)"):
        st.write("여기에 숨겨진 정보나 옵션을 넣을 수 있습니다.")

    # 사이드바 위젯
    st.sidebar.header("사이드바 예시")
    sidebar_choice = st.sidebar.selectbox("사이드바 선택", ["A", "B", "C"])
    st.sidebar.write("사이드바에서 선택한 값:", sidebar_choice)

    st.header("데이터 표시 — table, dataframe, map")
    df = pd.DataFrame(np.random.randn(10, 3), columns=["a", "b", "c"])
    st.dataframe(df)  # 상호작용 가능한 테이블
    st.table(df.head())  # 정적 테이블

    # 간단한 지도 표시 — 위도/경도 열 필요
    map_df = pd.DataFrame(np.random.randn(100, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"])
    st.map(map_df)

    st.header("미니 애니메이션/진행 상태")
    my_bar = st.progress(0)
    for i in range(0, 101, 10):
        my_bar.progress(i)

    with st.spinner("작업 실행 중..."):
        # 각주: 긴 작업이 있을 때 spinner로 사용자에게 알려줄 수 있습니다.
        pass

    st.balloons()  # 축하 이펙트

    st.header("폼 (폼 내부의 위젯은 한 번에 제출) ")
    with st.form("my_form"):
        name = st.text_input("이름")
        age = st.number_input("나이", min_value=0, max_value=120, value=30)
        submitted = st.form_submit_button("제출")
        # 각주: 폼 내부에서 제출 버튼이 눌리면 제출 플래그가 True가 됩니다.
    if submitted:
        st.success(f"제출 완료 — {name}님, {age}세")

    st.header("상태 저장 — session_state")
    # 각주: session_state를 이용하면 위젯 상태를 유지하거나 값 공유 가능
    if "counter" not in st.session_state:
        st.session_state.counter = 0

    if st.button("카운터 증가"):
        st.session_state.counter += 1
    st.write("카운터:", st.session_state.counter)

    st.header("캐시 예시")
    val = cached_heavy_calculation(10)
    st.write("캐시된 계산 결과:", val)

    st.header("응답형 메시지")
    st.success("성공 메시지" )
    st.info("정보 메시지")
    st.warning("경고 메시지")
    st.error("에러 메시지")

    st.header("미디어 출력: 이미지, 비디오, 오디오")
    # 샘플: 이미지 URL 또는 로컬 파일을 사용
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=150)
    # 비디오/오디오는 로컬 파일이나 URL을 넣을 수 있습니다.


if __name__ == "__main__":
    main()
