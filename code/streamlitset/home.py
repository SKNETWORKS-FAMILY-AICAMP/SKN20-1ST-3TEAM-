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

#_______________________________________________________
# 용도별 비중
  
    import plotly.express as px

    st.title("용도별 비중")
    st.write("관용.자가용.영업용 용도별 비중")

    # 데이터
    data = {"카테고리": ["관용", "자가용", "영업용"],
            "값": [40,60, 20]}
    df_pie = pd.DataFrame(data)

    # 데이터 미리보기
    st.dataframe(df_pie)

    # 변수 정의
    sizes = df_pie["값"]
    labels = df_pie["카테고리"]

    # 파이 차트
    # fig, ax = plt.subplots(figsize=(3, 3), dpi=100)  # dpi 높이면 차트가 더 작아짐
    # ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    # ax.axis("equal")

    fig = px.pie(df_pie, names="카테고리", values="값",
                title="용도별 비중",
                color_discrete_sequence=["skyblue", "lightgreen", "salmon"],)  # 색상 변경
    st.plotly_chart(fig, use_container_width=False)

#______________________________________________________


def show_info_page():
    """FAQ(현대/기아) 페이지를 표시하는 함수"""
    st.title("FAQ(현대/기아)")
    st.write("이곳에 프로젝트에 대한 설명을 추가할 수 있습니다.")
    st.info("이 앱은 Streamlit을 사용하여 제작되었습니다.")
    
    faq_categories = {
        '홈페이지': ['회원', '로그인', '기타'],
        '블루링크': ['가입/해지/변경', '서비스 이용', '요금', '오류 및 A/S'],
        '모젠서비스': ['사용법', '이용단말'],
        '현대 디지털 키': ['일반'],
        '차량구매': ['일반'],
        '차량정비': ['일반'],
        '기타': ['기타']
    }

    # 버튼 3개를 가로로 배치하기 위해 컬럼을 생성합니다.
    col1, col2, col3 = st.columns(3)

    # 각 컬럼에 버튼을 추가합니다.
    # 버튼 클릭 상태를 session_state에 저장하여 페이지가 새로고침 되어도 유지되도록 합니다.
    with col1:
        if st.button('전체', use_container_width=True):
            st.session_state.view = '전체'

#______________________________________________
    import mysql.connector
    from dotenv import load_dotenv
    import os

    load_dotenv()
    db_config = {
        'host': os.getenv("DB_HOST"), 'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"), 'database': 'sknfirst'
    }

    with col2:
        if st.button('현대', use_container_width=True):
            st.session_state.view = '현대'
            # 현대 FAQ DB 조회 및 화면 표시
            conn = mysql.connector.connect(**db_config)
            sql = "SELECT * FROM faq WHERE faq_company = '현대';"
            df = pd.read_sql(sql, conn)
            st.dataframe(df)
            conn.close()

    with col3:
        if st.button('기아', use_container_width=True):
            st.session_state.view = '기아'
            # 추후 '기아' 버튼 클릭 시의 로직을 추가할 수 있습니다.
            conn = mysql.connector.connect(**db_config)
            sql = "SELECT * FROM faq WHERE faq_company = '기아';"
            df = pd.read_sql(sql, conn)
            st.dataframe(df)
            conn.close()


    # st.session_state의 'view' 값이 '전체'일 경우에만 아래 코드를 실행합니다.
    # .get()을 사용하여 초기 실행 시 오류가 발생하는 것을 방지합니다.
    if st.session_state.get('view') == '전체':
        
        # 2개의 셀렉트 박스를 가로로 배치하기 위해 컬럼을 생성합니다.
        select_col1, select_col2 = st.columns(2)

        with select_col1:
            # 첫 번째 셀렉트 박스를 생성합니다. (옵션은 딕셔너리의 키 값들)
            first_options = list(faq_categories.keys())
            first_selection = st.selectbox(
                label="대분류",
                options=first_options
            )

        with select_col2:
            # 첫 번째 선택에 따라 두 번째 셀렉트 박스의 옵션을 동적으로 결정합니다.
            second_options = faq_categories[first_selection]
            second_selection = st.selectbox(
                label="소분류",
                options=second_options
            )
            query = f"SELECT * FROM faq WHERE faq_major_category = '{first_selection}' AND faq_sub_category = '{second_selection}'"
            conn = mysql.connector.connect(**db_config)
            df = pd.read_sql(query, conn)
            st.dataframe(df)
            conn.close()

        
        # (선택 사항) 사용자가 최종적으로 선택한 항목을 화면에 표시합니다.
        st.write(f"**선택된 카테고리:** {first_selection} > {second_selection}")

# Streamlit 앱을 실행하기 위한 코드 (로컬 테스트 시 사용)
# if __name__ == "__main__":
#     show_info_page()


if __name__ == "__main__":
    main()