import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
from dotenv import load_dotenv
import conn_db
import os
import plotly.express as px

load_dotenv()

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

    try :
        table_data = conn_db.load_home_data()
    except Exception as e:
        print(e)
        st.warning('Cannot Connected Database')
        # 샘플 데이터
        table_data = {
            '1분기': [150, 200, 180],
            '2분기': [170, 210, 190],
            '3분기': [180, 230, 200],
            '4분기': [210, 250, 220]
        }
        row_headers = ['제품 A', '제품 B', '제품 C']
    
    df = pd.DataFrame(table_data)

     # st.dataframe을 사용하여 엑셀과 유사한 표를 표시합니다.
    st.dataframe(df, hide_index=True)
    
    import plotly.express as px

    # --- 막대 그래프 표시 (sido별 total_subtotal) ---
    fig = px.bar(
        df,
        x="시도명",        # x축: sido 컬럼
        y="총계",          # y축: total_subtotal 컬럼
        title="시도별 자동차 총 등록대수",
        labels={'시도명': '시/도', '총계': '총 등록대수'}
    )
    
    # x축 레이블이 겹치지 않도록 각도를 조절합니다.
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    st.write("---")  # 구분선

    # 5. 참조 문구
    #st.markdown('<p class="reference-text">※ 이 데이터는 예시용으로 생성된 데이터입니다.</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

#====================================================================================================================1페이지

def show_data_page():
    """차종별 합계 및 비중 차트 페이지를 표시하는 함수"""
    st.title("📊 차종별/용도별 등록 비중 분석")
    st.write("해당 월의 차종별, 용도별 등록 비중을 확인할 수 있습니다.")
    st.write("---")

    db_config = {
        'host': os.getenv("DB_HOST"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'database': 'sknfirst'
    }

    # DB 연결 및 데이터 조회를 위한 try-except-finally 블록
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)

        # --- 2. 월 선택 UI 생성 ---
        # DB에서 선택 가능한 'report_month' 목록을 가져옵니다.
        # ※ 아래 쿼리의 'car_registrations' 부분은 실제 테이블 이름으로 변경해야 합니다.
        query_months = "SELECT DISTINCT report_month FROM car_registeration ORDER BY report_month DESC"
        month_df = pd.read_sql(query_months, conn)

        if month_df.empty:
            st.warning("데이터베이스에서 조회할 수 있는 월 정보가 없습니다.")
            return

        available_months = month_df['report_month'].tolist()
        selected_month = st.selectbox("🗓️ 월을 선택하세요:", options=available_months)

        # --- 3. 선택된 월의 데이터 가져오기 ---
        if selected_month:
            # 사용자가 선택한 월에 해당하는 데이터를 DB에서 조회합니다.
            # ※ 아래 쿼리의 'car_registrations' 부분은 실제 테이블 이름으로 변경해야 합니다.
            query_data = f"""
                SELECT
                    passenger_official, passenger_private, passenger_commercial,
                    van_official, van_private, van_commercial,
                    truck_official, truck_private, truck_commercial,
                    special_official, special_private, special_commercial
                FROM car_registeration
                WHERE report_month = '{selected_month}'
            """
            data_df = pd.read_sql(query_data, conn)

            if data_df.empty:
                st.warning(f"'{selected_month}'에 대한 데이터가 없습니다.")
                return

            # 조회된 데이터의 첫 번째 행을 사용합니다.
            vehicle_data = data_df.iloc[0]

            # --- 4. 파이 차트 생성 및 표시 ---
            st.subheader(f"'{selected_month}' 차종별 용도 비중")

            # 차트 생성을 위한 헬퍼 함수 (코드 중복 방지)
            def create_pie_chart(data, title, categories):
                """데이터를 받아 Plotly 파이 차트를 생성하는 함수"""
                pie_data = {
                    "용도": ["관용", "자가용", "영업용"],
                    "대수": [data[categories[0]], data[categories[1]], data[categories[2]]]
                }
                df_pie = pd.DataFrame(pie_data)

                fig = px.pie(df_pie,
                             names="용도",
                             values="대수",
                             title=f"<b>{title}</b>",
                             color_discrete_sequence=px.colors.sequential.Blues_r,
                             hole=0.3) # 도넛 차트 효과
                fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.05, 0, 0])
                fig.update_layout(title_x=0.5) # 제목 가운데 정렬
                return fig

            # 2x2 그리드로 차트들을 배치합니다.
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            with col1:
                fig_passenger = create_pie_chart(vehicle_data, "승용차", ['passenger_official', 'passenger_private', 'passenger_commercial'])
                st.plotly_chart(fig_passenger, use_container_width=True)

            with col2:
                fig_van = create_pie_chart(vehicle_data, "승합차", ['van_official', 'van_private', 'van_commercial'])
                st.plotly_chart(fig_van, use_container_width=True)

            with col3:
                fig_truck = create_pie_chart(vehicle_data, "화물차", ['truck_official', 'truck_private', 'truck_commercial'])
                st.plotly_chart(fig_truck, use_container_width=True)

            with col4:
                fig_special = create_pie_chart(vehicle_data, "특수차", ['special_official', 'special_private', 'special_commercial'])
                st.plotly_chart(fig_special, use_container_width=True)

    except mysql.connector.Error as err:
        st.error(f"데이터베이스 연결에 실패했습니다: {err}")
        st.info("`.env` 파일의 DB 연결 정보를 확인하거나 MySQL 서버가 실행 중인지 확인해주세요.")
    finally:
        # --- 5. DB 연결 종료 ---
        if conn and conn.is_connected():
            conn.close()


#=============================================================================================================2페이지

def show_info_page():
    """FAQ(현대/기아) 페이지를 표시하는 함수"""
    st.title("FAQ")
    
    st.info("현대/기아 자동차 관련 질문과 답변을 제공합니다.")
    
    # 검색창 추가
    search_query = st.text_input("🔎 질문 검색:", placeholder="검색어를 입력하세요...")
    
    faq_categories = {
        '전체': ['전체'],
        '홈페이지': ['전체', '회원', '로그인', '기타'],
        '블루링크': ['전체', '가입/해지/변경', '서비스 이용', '요금', '오류 및 A/S'],
        '모젠서비스': ['전체', '사용법', '이용단말'],
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

    with col2:
        if st.button('현대', use_container_width=True):
            st.session_state.view = '현대'

    with col3:
        if st.button('기아', use_container_width=True):
            st.session_state.view = '기아'

    # DB 연결 정보
    import mysql.connector
    from dotenv import load_dotenv
    import os

    load_dotenv()
    db_config = {
        'host': os.getenv("DB_HOST"), 'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"), 'database': 'sknfirst'
    }

    # st.session_state의 'view' 값에 따라 다른 내용을 표시합니다.
    # .get()을 사용하여 초기 실행 시 오류가 발생하는 것을 방지합니다.
    view_state = st.session_state.get('view')

    if view_state == '현대':
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

        # DB 쿼리 생성 (가독성 및 유지보수성을 위해 동적으로 구성)
        query_parts = ["SELECT faq_company, faq_question, faq_answer FROM faq WHERE faq_company = '현대'"]
        if first_selection != '전체':
            query_parts.append(f"AND faq_major_category = '{first_selection}'")
        if second_selection != '전체':
            query_parts.append(f"AND faq_sub_category = '{second_selection}'")
        if search_query:
            query_parts.append(f"AND faq_question LIKE '%{search_query}%'")
        
        query = " ".join(query_parts)

        conn = mysql.connector.connect(**db_config)
        df = pd.read_sql(query, conn)
        st.write("---") # 구분선 추가

        if df.empty:
            st.warning("검색 결과가 없습니다.")
        else:
            for index, row in df.iterrows():
                faq_company = row['faq_company']
                with st.expander(f"Q.[{faq_company}] {row['faq_question']}"):
                    st.write(row['faq_answer'])
        
        # (선택 사항) 사용자가 최종적으로 선택한 항목을 화면에 표시합니다.
        st.write(f"**선택된 카테고리:** {first_selection} > {second_selection}")

    elif view_state == '전체':
        # 전체 FAQ DB 조회 및 화면 표시
        query = "SELECT faq_company, faq_question, faq_answer FROM faq"
        if search_query:
            query += f" WHERE faq_question LIKE '%{search_query}%'"
            
        conn = mysql.connector.connect(**db_config)
        df = pd.read_sql(query, conn)
        st.write("---") # 구분선 추가
        if df.empty:
            st.warning("검색 결과가 없습니다.")
        else:
            for index, row in df.iterrows():
                with st.expander(f"Q.[{row['faq_company']}] {row['faq_question']}"):
                    st.write(row['faq_answer'])

    elif view_state == '기아':
        # 기아 FAQ DB 조회 및 화면 표시
        query = "SELECT faq_company, faq_question, faq_answer FROM faq WHERE faq_company = '기아'"
        if search_query:
            query += f" AND faq_question LIKE '%{search_query}%'"

        conn = mysql.connector.connect(**db_config)
        df = pd.read_sql(query, conn)
        st.write("---") # 구분선 추가
        if df.empty:
            st.warning("검색 결과가 없습니다.")
        else:
            for index, row in df.iterrows():
                with st.expander(f"Q.[{row['faq_company']}] {row['faq_question']}"):
                    st.write(row['faq_answer'])


if __name__ == "__main__":
    main()