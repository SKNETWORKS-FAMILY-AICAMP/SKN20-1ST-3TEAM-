# SKN20-1ST-3TEAM

## SK Networks Family AI Camp 1st Project


## 1. 팀 소개
---
**팀명: 할수있어조**  
**팀원**:  
| 오학성 | 홍혜원 | 최소영 | 권규리 | 이승규 |
|--------|--------|--------|--------|--------|



## 2. Project Overview
---
### 2.1. Introduction
- **전국 차량등록 정보 현황 및 FAQ 확인 시스템**
- 대한민국 국토교통부의 자동차등록현황 데이터와 현대·기아 공식 홈페이지에서 수집한 FAQ 데이터를 기반으로,
<mark>지역별·기간별 차량 등록 추이</mark>와 브랜드별 자주 묻는 질문(FAQ)을 함께 제공하는 웹 대시보드 시스템입니다.

### 2.2. Purpose
- 매월 발표되는 차량 등록 데이터를 크롤링하여 시각화까지 진행하여 누구나 쉽게 확인할 수 있는 환경 제공  

### 2.3. Key Features
- 최신 데이터 반영 (2023.08 ~ 2025.08)
- 지역별(시도/시군구), 기간별 필터링
- Streamlit 기반 직관적 UI
- 현대·기아 FAQ 검색 (카테고리별/전체 검색)

### 2.4. Data Overview
- 차량 구매 희망자에게 심플하고 간단 명료한 정보를 필터링하여 제공  
- 최근 1년간 브랜드, 모델 별 판매량 데이터를 제공  
- 브랜드별 FAQ 제공: 빈번히 발생하는 문의 내용에 쉽게 접근 가능  



## 3. 기술 스택
---
### 3.1. 프론트엔드  
- <img src="https://img.shields.io/badge/streamlit-F9AB00?style=plastic&logo=streamlit&logoColor=#FF4B4B"/> : 웹 대시보드 프레임워크 (데이터 시각화 및 조회 시스템)  

### 3.2. 백엔드  
- <img src="https://img.shields.io/badge/Python-3776AB?style=plastic&logo=Python&logoColor=white"/> : 데이터 처리 및 비즈니스 로직 구현  
- <img src="https://img.shields.io/badge/mysql-4479A1?style=plastic&logo=streamlit&logoColor=white"/> : 데이터베이스 관리 및 저장  
- <img src="https://img.shields.io/badge/pandas-150458?style=plastic&logo=streamlit&logoColor=white"/> : 데이터 분석 및 필터링 처리  


## 4. WBS (Work Breakdown Structure)
---
### 4.1. 프로젝트 기획  
- 기획 방향 회의  

### 4.2. 크롤링  
- 자동차 판매량 & 세부정보  
- 회사별 FAQ  

### 4.3. SQL 연결  
- 데이터베이스 입력  
- 자동차 판매량 & 세부정보 SQL 쿼리 연결 및 구현  
- FAQ 및 서비스센터 SQL 연결  

### 4.4. STREAMLIT 구현  
- Streamlit 대시보드 구축  
- 판매량 통계 데이터 제공 화면 구현  
- 브랜드별 FAQ 화면 구현  
- 검색 및 필터 기능 구현 (월별)  

### 4.5. 프로젝트 정리  


## 5. 요구사항 명세서
---
### 5.1. 사용자 요구사항  
- 2024년 특정 월에 어떤 차량이 많이 판매되었는지 조회할 수 있어야 한다.  
- FAQ 정보를 브랜드별로 조회할 수 있어야 하며 질문 및 답변 데이터를 가져올 수 있어야 한다.  

### 5.2. 시스템 요구사항  
- MySQL 데이터베이스를 사용하여 실시간 필터링 및 조회가 가능해야 한다.  
- Streamlit 대시보드를 통해 직관적인 사용자 인터페이스를 제공해야 한다.  

## 6. ERD (Entity-Relationship Diagram)
---
### 주요 테이블 구조
- **brand**: 브랜드 정보  
- **model**: 차량 정보  
- **brand_sales**: 브랜드 별 차량 판매 정보  
- **model_sales**: 차량 모델 별 차량 판매 정보  
- **faq**: 차량 FAQ 정보  

### ERD 다이어그램  
<img width="523" alt="erd_final" src="https://github.com/user-attachments/assets/82b41f79-2265-4156-9e4f-8937d22e0b2b" />


## 7. 주요 프로시저 및 수행 결과
---
### 7.1. 메인 프로시저  
<img width="1280" alt="image" src="https://github.com/user-attachments/assets/766aaa07-b9b0-4db7-b490-09d4db31376f" />

### 7.2. 모델 별 판매 순위 프로시저  
- 기간별 모델 판매 순위 정보 제공  
<img width="1280" alt="image" src="https://github.com/user-attachments/assets/5263dc3c-70f6-4baf-84f7-cc3ccf202e17" />

### 7.3. 브랜드 별 판매 순위 프로시저  
- 특정 브랜드 별 판매 순위 정보 제공  
<img width="1280" alt="image" src="https://github.com/user-attachments/assets/6bb067c7-0ce3-42c5-aabc-d7ab3982b149" />

### 7.4. 차량 세부 정보 조회 프로시저  
- 모델 별 세부 정보 제공  
<img width="1280" alt="image" src="https://github.com/user-attachments/assets/aecf25de-a78e-4a28-9bbd-e2ee0677a08c" />

### 7.5 FAQ 프로시저  
- 브랜드 별 빈도 높은 상위 10개 질문 정보 제공  
 <img width="1280" alt="image" src="https://github.com/user-attachments/assets/f1451a61-de1b-471a-9190-0493802edabc" />


## 8. 한 줄 회고
---
- **김도윤** : 이번 프로젝트를 통해 실무에서의 데이터 수집과 활용 방식을 직접 경험할 수 있었습니다. 크롤링부터 MySQL 연동까지 전 과정을 거치면서, 단순한 학습을 넘어 실제 적용 가능한 역량을 키울 수 있었습니다. 특히 팀원들과 협업하며 문제를 해결하는 과정이 값진 배움이었고, 앞으로도 더 발전해야겠다는 동기부여가 되었습니다. 모두 고생 많으셨습니다!
- **김원우** : 첫 프로젝트라 많이 긴장했지만 다들 열심히 해주셨고, 결과적으로 잘 마무리할 수 있어서 좋았습니다.
- **김이경** : 첫 번째 챕터 동안 배운 내용이 총집합으로 단위 프로젝트에 적용되는 것을 크게 느꼈고, 다음 챕터의 수업부터는 더욱 열심히 듣고 이해 해야겠다는 생각이 들었습니다. 크롤링 부분에서 많이 부족하다고 느껴 더 노력해야할 것 같습니다. 주로 DB 부분을 맡았는데, 그동안 학습했던 내용을 복습할 수 있어 좋았고 팀원으로부터 도움을 받아 보완할 수 있었습니다.
- **남의헌** : 작은 팀 단위로 배웠던 것을 직접 사용해보고, 미숙한 부분을 직접 다시 해보며 정리해볼 수 있는 좋은 경험이었습니다. 프로젝트 기간동안 팀원 분들 다들 너무 고생 많으셨습니다!
- **박진양** : 첫 프로젝트였기에 많이 떨렸고 저의 개인적인 기량을 보완해주었던 팀원 분들께 정말 감사드립니다. 처음으로 배운 크롤링을 실전에서 써보는 값진 경험이었으며 이를 통해 데이터 구축과 mysql 데이터베이스를 만드는 작업을 할 수 있어서 좋은 시간이었습니다. 특히, 너무 고생하신 팀원 분들께 다시 한번 무한한 감사를 드리고 싶습니다!
