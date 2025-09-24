import streamlit as st
import pandas as pd
import numpy as np

def main():
    """메인 애플리케이션 함수"""

    # --- 페이지 기본 설정 ---
    st.set_page_config(
        page_title="2년간 자동차 등록 현황 분석",
        page_icon="🚗",
        layout="wide"
    )

    # --- CSS 스타일 주입 ---
    # 메인 콘텐츠를 가운데 정렬하고, 폰트 스타일을 지정합니다.
    st.markdown("""
        <style>
            .main-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
            .main-container h1 {
                font-size: 3em;
                font-weight: bold;
            }
            .main-container h2 {
                font-size: 2em;
                font-weight: bold;
            }
            .source-text {
                font-size: 0.9em;
                color: gray;
            }
            .reference-text {
                margin-top: 20px;
                font-style: italic;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- 사이드바 (왼쪽 메뉴) ---
    with st.sidebar:
        st.header("📌메뉴")

        # st.session_state를 사용하여 현재 페이지를 추적합니다.
        if 'page' not in st.session_state:
            st.session_state.page = 'home' # 초기 페이지 설정

        # 각 버튼을 누르면 session_state의 값을 변경합니다.
        if st.button("🏠홈", use_container_width=True):
            st.session_state.page = 'home'
        if st.button("📊차종별 합계 및 비중", use_container_width=True):
            st.session_state.page = 'data'
        if st.button("❓FAQ(현대/기아)", use_container_width=True):
            st.session_state.page = 'info'

    # --- 메인 창 (오른쪽 콘텐츠) ---
    # session_state 값에 따라 다른 함수를 호출하여 페이지 내용을 표시합니다.
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'data':
        show_data_page()
    elif st.session_state.page == 'info':
        show_info_page()


def show_home_page():
    """홈 대시보드 페이지를 표시하는 함수"""
    # 가운데 정렬을 위한 컨테이너 클래스 적용
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # 1. 제목
    st.header("🚗2년간 자동차 등록 현황 분석🚗")
    

    # 2. 부제목
    st.subheader("자동차등록현황보고(Total Registered Motor Vehicles) ")

    # 3. 자료 출처
    st.markdown("""
    <p class="source">자료 출처 : 
    <a href="https://stat.molit.go.kr/portal/cate/statView.do?hRsId=58&hFormId=5498&hSelectId=5559&hPoint=00&hAppr=1&hDivEng=&oFileName=&rFileName=&midpath=&sFormId=5498&sStyleNum=1&settingRadio=xlsx" target="_blank">
    국토교통 통계 누리 데이터</a></p>
""", unsafe_allow_html=True)

    # 4. 대시보드 (수정된 부분: 막대 차트 -> 표)
    st.write("---") # 구분선
    st.subheader("지역별 자동차 등록 현황 대시보드")

    # 표 데이터 생성
    # columns로 열 제목, index로 행 제목을 지정합니다.
    table_data = {
        '1분기': [150, 200, 180],
        '2분기': [170, 210, 190],
        '3분기': [180, 230, 200],
        '4분기': [210, 250, 220]
    }
    row_headers = ['제품 A', '제품 B', '제품 C']
    df = pd.DataFrame(table_data, index=row_headers)

    # st.dataframe을 사용하여 엑셀과 유사한 표를 표시합니다.
    st.dataframe(df, use_container_width=True)

    st.write("---") # 구분선

    # 5. 참조 문구
    st.markdown('<p class="reference-text">※ 이 데이터는 예시용으로 생성된 데이터입니다.</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def show_data_page():
    """차종별 합계 및 비중 차트 페이지를 표시하는 함수"""
    st.title("상세 데이터 보기")
    st.write("이곳에 상세 데이터를 표시하는 표나 차트를 추가할 수 있습니다.")

    df = pd.DataFrame({
        '첫 번째 컬럼': [1, 2, 3, 4],
        '두 번째 컬럼': [10, 20, 30, 40],
    })
    st.dataframe(df, use_container_width=True)


def show_info_page():
    """FAQ(현대/기아) 페이지를 표시하는 함수"""
    st.title("FAQ(현대/기아)")
    st.write("이곳에 프로젝트에 대한 설명을 추가할 수 있습니다.")
    st.info("이 앱은 Streamlit을 사용하여 제작되었습니다.")


if __name__ == "__main__":
    main()