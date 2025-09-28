![header](https://capsule-render.vercel.app/api?type=venom&height=150&color=gradient&text=SKN20-1st%20Project%20-%203TEAM&section=header&desc=/&descSize=20&textBg=false&fontSize=65&fontColor=FFAA28)

# Team Introduction 
**Team Name: 해야만하조?**  
**Members**:  
| 오학성 | 홍혜원 | 최소영 | 권규리 | 이승규 |
|--------|--------|--------|--------|--------|

---

# 1. Project Overview

## 1.1. Introduction
### **전국 차량등록 현황 및 FAQ 확인 시스템**
- '대한민국 국토교통부의 자동차등록 현황 데이터'와 '현대·기아 공식 홈페이지에서 수집한 FAQ 데이터'를 기반으로, <br>
<mark>지역별·기간별 차량 등록 추이</mark>와 <mark>브랜드별 자주 묻는 질문(FAQ)</mark>을 함께 제공하는 웹 대시보드 시스템입니다.

## 1.2. Purpose
- 매월 발표되는 차량 등록 데이터를 크롤링하여 시각화까지 진행하여 누구나 쉽게 차량등록 현황을 확인할 수 있는 환경 제공
- 제조사별 고객 FAQ를 통합하여 FAQ 검색 편의성 제공 

## 1.3. Key Features Summary
- 최신 데이터 반영 (2020-08 ~ 2025-08)
- **지역별(시/도 선택 ->시군구별 확인), 기간별 필터링**
- **현대·기아 FAQ 검색 (카테고리별/전체/키워드 검색)**
- Streamlit 기반 직관적 UI

---

# 2. System Architecture

## 2.1. Data Crawling
### 대한민국 국토교통 통계누리
- 자동차등록 현황 보고
- 월별 데이터 크롤링 (2020.08 ~ 2025.08)
### FAQ
- 현대·기아 공식 홈페이지
- 브랜드별 FAQ 및 카테고리 데이터 크롤링
  
## 2.2. Database (MySQL)
- `car_registration` TABLE: 월, 시도, 시군구, 차종별(승용·승합·화물·특수) 등록 현황 저장
- `region` TABLE: 시도, 시군구
- `faq` TABLE: 브랜드(현대/기아), 카테고리, 질문·답변 저장
### ERD
> <img src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/ERD.png" width="700">
### Table Specification
> <img src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/image/%ED%85%8C%EC%9D%B4%EB%B8%94%EB%AA%85%EC%84%B8%EC%84%9C1.png" width="700">
> <img src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/image/%ED%85%8C%EC%9D%B4%EB%B8%94%EB%AA%85%EC%84%B8%EC%84%9C2.png" width="700">

## 2.3. Backend (Python)
- 크롤링 스크립트 실행 후 DB 적재
- Streamlit과 연동해 DB 조회 및 쿼리 처리
## 2.4. Frontend (Streamlit)
- 차량등록현황 조회:  기간·지역 필터링 + 테이블/차트 시각화
- 현대·기아 FAQ 검색:  카테고리별/전체 검색 지원

<br>

### Architecture Diagram
<img src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/Architecture_Diagram.png" width="700">


---

# 3. KEY Features
## 3.1. 차량등록 현황 조회
### 필터링 기능
- 기간: **월별 선택 (2020.08 ~ 2025.08)**
- 지역: **시/도 선택 가능**
- 시각화: **차량 등록 현황을 표(Table) 및 차트(Line/Bar/Pie)로 제공**
- 차량 종류별(승용, 승합, 화물, 특수) 및 용도별(관용, 자가용, 영업용, 계) **분포 확인 가능**

### FAQ 검색
- **브랜드별 FAQ 제공**
- **현대(☰ Hyundai) / 기아(☰ Kia) / 전체(All) 검색 가능**
- **카테고리 기반 필터링**
- **검색 기능: 키워드 입력 시 해당 질문·답변 바로 확인**

---

# 4. Requirements Specification

## 4.1. User Requirements  

### 차량등록 현황 조회
- 사용자는 **특정 기간(월별)** 과 **지역(시/도)** 을 선택해 차량 등록 현황을 조회할 수 있다. 
- 조회 결과는 표와 그래프 형태로 제공된다.
### 차종별/용도별 분석
- 사용자는 **승용, 승합, 화물, 특수 차량 등록 현황**을 확인할 수 있다.
- 각 차종은 **관용, 자가용, 영업용, 계 단위**로 구분된다.
### FAQ 검색
- 사용자는 **현대, 기아 브랜드별 또는 전체 FAQ**를 검색할 수 있다.
- 사용자는 **카테고리별 FAQ를 조회**하거나 **전체 검색**을 수행할 수 있다.
- 검색 결과에서 질문과 답변을 확인할 수 있다.
### 편의성
- 사용자는 웹 기반 UI(Streamlit)를 통해 별도의 설치 없이 브라우저에서 시스템을 사용할 수 있다.
- 필터 및 검색은 즉시 반영되어 결과가 출력된다.

## 4.2. Functional Requirements
- 국토교통부 자동차등록 현황 데이터를 월 단위로 크롤링하여 MySQL DB에 저장해야 한다.
- 현대/기아 홈페이지에서 FAQ 데이터(브랜드, 카테고리, 질문, 답변)를 크롤링하여 DB에 반영해야 한다.
- 차량등록 현황 조회 기능은 년/월/시도 단위로 필터링을 지원해야 한다.
- 조회된 데이터는 표와 차트 형태로 제공되어야 한다.
- FAQ 검색 기능은 브랜드별/카테고리별/전체 검색을 지원해야 한다.
- Streamlit 대시보드는 사용자 요청에 따라 DB에서 데이터를 조회하고 결과를 시각화해야 한다.

---

## 5. Results

### 5.1. 메인 - 전체 지역 차량등록 현황 
- 기간 선택 가능
- 전체 지역 차량등록 현황 조회
<img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/dashboard/main_1.png" />

### 5.2. 메인 - 시/도별 챠랑등록 현황
- 지역을 선택하면 해당 지역의 시군구별 차량등록 현황 확인
<img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/dashboard/main_2.png" />

### 5.3. 메인 - 시/도별 자동차 총 등록대수
- Line chart를 통해 한 눈에 들어오게 표현
- 전체 지역 비교 / 원하는 지역의 시군구별로 비교
<img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/dashboard/main_3.png" />

### 5.4. 차종별 용도 비중 
<img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/dashboard/ratio_1.png" />
<img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/dashboard/ratio_2.png" />

### 5.5. FAQ  
 <img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/dashboard/faq_1.png" />
<img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/dashboard/faq_2.png" />
<img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/dashboard/faq_3.png" />


---

## 6. Retrospective

- **오학성** : 비전공자 팀원들과의 협업을 통하여 코드를 이해하기 쉽개 개선하는 작업이 중요하다는 것을 배웠습니다. 앞으로 제가 알고 있는 지식 혹은 코드를 다른 사람이 이해하고 함께 개선할 수 있도록 노력하겠습니다.
- **홍혜원** : 팀원들과 협업하며 각자의 장점을 살릴 수 있어 좋았습니다. 개발 과정에서 오류나 고민이 생겼을 때도 혼자 해결하기보다 함께 모여 코드를 리뷰하고 의견을 주고받으며 문제를 해결할 수 있어 의미 있었습니다. 다만 기간 내에 마무리하기 위해, 제가 잘 모르는 부분에 대해서 충분히 도전하지 못한 점이 아쉬움으로 남았습니다. 다음에는 부족한 부분에도 적극적으로 도전해 성장하고 싶습니다.
- **이승규** : 비전공자로서 데이터의 가능성을 직접 보여주고자 SQL과 파이썬의 기본부터 부딪히며 익혔고, 특히 Streamlit을 활용해 복잡한 웹 지식 없이도 데이터 분석 결과를 직관적인 대시보드로 신속하게 구현할 수 있었습니다.
- **최소영** : 직접 코드를 짜면서 데이터를 얻지는 못한 점은 아쉬웠지만, 코드를 수정하면서 직접 웹 화면으로 구현해볼 수 있어서 좋은경험이었습니다. 수업 중에 이해 못했던 부분들도 실제로 해보니 다시 정리해볼 수 있었던 것 같습니다. 모든 팀원분들 
많이 도와주셔서 감사합니다.
- **권규리** : 첫 프로젝트하면서, 이해못하는 부분이  많아서 속도가 느려서 다른 팀원분들의 코드를 보고 익혔지만 어떻게 구현되는지 확인 후에 앞으로의 공부방법과 동기부여가 되었습니다. 앞으로 조금 더 부족한 부분  채워서  조금 더 보완해서 참여하고 싶습니다. 팀원분들 모두 감사합니다.
