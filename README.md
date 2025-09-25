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
- 지역별(시도/시군구), 기간별 필터링
- 현대·기아 FAQ 검색 (카테고리별/전체 검색)
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
> ### ERD
<img src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/ERD.png" width="700">

## 2.3. Backend (Python)
- 크롤링 스크립트 실행 후 DB 적재
- Streamlit과 연동해 DB 조회 및 쿼리 처리
## 2.4. Frontend (Streamlit)
- 차량등록현황 조회:  기간·지역 필터링 + 테이블/차트 시각화
- 현대·기아 FAQ 검색:  카테고리별/전체 검색 지원

<br>

> ### Architecture Diagram
<img src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/Architecture_Diagram.png" width="700">

> ### Table Specification
<img src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/image/%ED%85%8C%EC%9D%B4%EB%B8%94%EB%AA%85%EC%84%B8%EC%84%9C1.png" width="700">
<img src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/image/%ED%85%8C%EC%9D%B4%EB%B8%94%EB%AA%85%EC%84%B8%EC%84%9C2.png" width="700">

---

# 3. KEY Features
## 3.1. 차량등록 현황 조회
### 필터링 기능
- 기간: **월별 선택 (2020.08 ~ 2025.08)**
- 지역: **시도/시군구 단위 선택 가능**
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
- 사용자는 **특정 기간(월별)** 과 **지역(시도/시군구)** 을 선택해 차량 등록 현황을 조회할 수 있다. 
- 조회 결과는 표와 그래프 형태로 제공된다.
### 차종별/용도별 분석
- 사용자는 **승용, 승합, 화물, 특수 차량 등록 현황**을 확인할 수 있다.
- 각 차종은 **관용, 자가용, 영업용, 계 단위**로 구분된다.
### FAQ 검색
- 사용자는 **현대, 기아 브랜드별 FAQ**를 검색할 수 있다.
- 사용자는 **카테고리별 FAQ를 조회**하거나 **전체 검색**을 수행할 수 있다.
- 검색 결과에서 질문과 답변을 확인할 수 있다.
### 편의성
- 사용자는 웹 기반 UI(Streamlit)를 통해 별도의 설치 없이 브라우저에서 시스템을 사용할 수 있다.
- 필터 및 검색은 즉시 반영되어 결과가 출력된다.

## 4.2. Functional Requirements
- 국토교통부 자동차등록 현황 데이터를 월 단위로 크롤링하여 MySQL DB에 저장해야 한다.
- 현대/기아 홈페이지에서 FAQ 데이터(브랜드, 카테고리, 질문, 답변)를 크롤링하여 DB에 반영해야 한다.
- 차량등록 현황 조회 기능은 년/월/시도/시군구 단위로 필터링을 지원해야 한다.
- 조회된 데이터는 표와 차트 형태로 제공되어야 한다.
- FAQ 검색 기능은 브랜드별/카테고리별/전체 검색을 지원해야 한다.
- Streamlit 대시보드는 사용자 요청에 따라 DB에서 데이터를 조회하고 결과를 시각화해야 한다.

---

## 5. Results

### 5.1. 메인 대시보드 (지역별 자동차 등록 현황 대시보드) 
<img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/image/%EB%A9%94%EC%9D%B8%EB%8C%80%EC%8B%9C%2C%EC%9E%90%EB%8F%99%EC%B0%A8%EB%93%B1%EB%A1%9D%ED%98%84%ED%99%A9.png" />

### 5.2.시도별 자동차 총 등록대수  
- 기간, 시도별 자동차 등록 정보 제공  
<img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/image/%EC%8B%9C%EB%8F%84%EB%B3%84%20%EC%9E%90%EB%8F%99%EC%B0%A8%20%EC%B4%9D%20%EB%93%B1%EB%A1%9D%EB%8C%80%EC%88%98.png" />

### 5.3. 차종별 합계 및 비중 
- 기간, 차종별 합계 비중 제공  
<img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/image/%EC%B0%A8%EC%A2%85%EB%B3%84%EB%93%B1%EB%A1%9D%EB%B9%84%EC%A4%91.png" />

### 5.4. FAQ(현대/기아)  
- 현대/기아 자동차 관련 질문과 답변 제공  
<img width="1280" alt="image" src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN20-1ST-3TEAM-/blob/main/output/image/FAQ.png" />

---

## 6. Retrospective

- **오학성** : 이번 프로젝트를 통해 실무에서의 데이터 수집과 활용 방식을 직접 경험할 수 있었습니다. 크롤링부터 MySQL 연동까지 전 과정을 거치면서, 단순한 학습을 넘어 실제 적용 가능한 역량을 키울 수 있었습니다. 특히 팀원들과 협업하며 문제를 해결하는 과정이 값진 배움이었고, 앞으로도 더 발전해야겠다는 동기부여가 되었습니다. 모두 고생 많으셨습니다!
- **홍혜원** : 첫 프로젝트라 많이 긴장했지만 다들 열심히 해주셨고, 결과적으로 잘 마무리할 수 있어서 좋았습니다.
- **이승규** : 첫 번째 챕터 동안 배운 내용이 총집합으로 단위 프로젝트에 적용되는 것을 크게 느꼈고, 다음 챕터의 수업부터는 더욱 열심히 듣고 이해 해야겠다는 생각이 들었습니다. 크롤링 부분에서 많이 부족하다고 느껴 더 노력해야할 것 같습니다. 주로 DB 부분을 맡았는데, 그동안 학습했던 내용을 복습할 수 있어 좋았고 팀원으로부터 도움을 받아 보완할 수 있었습니다.
- **최소영** : 작은 팀 단위로 배웠던 것을 직접 사용해보고, 미숙한 부분을 직접 다시 해보며 정리해볼 수 있는 좋은 경험이었습니다. 프로젝트 기간동안 팀원 분들 다들 너무 고생 많으셨습니다!
- **권규리** : 첫 프로젝트였기에 많이 떨렸고 저의 개인적인 기량을 보완해주었던 팀원 분들께 정말 감사드립니다. 처음으로 배운 크롤링을 실전에서 써보는 값진 경험이었으며 이를 통해 데이터 구축과 mysql 데이터베이스를 만드는 작업을 할 수 있어서 좋은 시간이었습니다. 특히, 너무 고생하신 팀원 분들께 다시 한번 무한한 감사를 드리고 싶습니다!
