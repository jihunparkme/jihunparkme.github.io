---
layout: page
title: About
permalink: /about/
---

# PARK JI HUN

朴 知勳

<br/>

# Project

## 고신뢰 ICT-제조설비를 위한 빅데이터 기반 자율제어 기술 개발

- 2018.03.01. ~ 2018.12.07.
- 한국연구재단

#### Description.

- 고신뢰성을 요구하는 ICT-제조설비들의 운영목표 및 필수 요구사항들을 분석하고, 문제/오류 발생 시에 대응할 수 있는 고신뢰 자율제어 SW의 핵심 기술을 개발

#### What did I do.

- 빅데이터 가공 기술 동향 조사
- 빅데이터 가공 기술 설계 연구 및 개발 (**HDFS, Pig, Hive** 활용)
  - 분산 저장된 데이터를 집계하는 **분산 처리 모듈 개발**
  - 질의 성능 향상을 위한 캐시 데이터 활용 및 중복을 제거하는 **필터링 모듈 개발**
- 빅데이터 분석 기술 동향 조사
- 빅데이터 분석 기술 연구 및 개발 (**R** 활용)
  - 데이터의 추이를 분석하여 문제를 예측하는 **회귀 분석 모듈 개발**
  - 데이터 간 유사성을 통해 패턴을 분석하는 **군집화 및 분류 모듈 개발**
  - 시간 흐름에 따라 데이터의 변화를 예측하는 **시계열 분석 모듈 개발**

#### Tech Stack.

- Flume, Sqoop, HDFS, Pig, Hive, R

---

## 빅데이터 기반 의료 임상 결과 분석

- 2018.05.01. ~ 2018.11.23.
- 한국산업기술대학교(현장맞춤형 이공계 인재양성 지원사업)

#### Description.

- 임상 결과를 분석하고 신뢰성을 확보하여 임상 시험 기간과 비용 등을 줄이고 임상 시험 설계 최적화를 위한 빅데이터 기반 분석 시스템 개발

#### What did I do.

- 데이터 수집: **Sqoop**을 활용하여 RDBMS에 저장된 데이터 수집
- 데이터 처리 : **Hive,** **R**을 활용한 임상 결과 **데이터 정제**
- 데이터 분석 : **R**을 활용한 **연관성 분석**(**Apriori Algorithm)**
- 데이터 시각화 : **R**을 활용한 시각화
- 연구 보고서 작성

#### Tech Stack.

- Mysql, Sqoop, HDFS, Hive, R
- Apriori Algorithm

> Seung-Yeon Hwang, Ji-Hun Park "Big Data-based Medical Clinical Results Analysis,” IIBC, Vol. 19, No. 1, pp.187-195, Feb. 28, 2019. 

---

## 빅데이터 기반 환자 간병방법 분석 연구

- 2018.03.02. ~ 2018.08.31.
- 한국산업기술대학교(산기대전)

#### Description.

- 기존 환자 진단 데이터를 분석하여 의학적 지식이 없는 간병인이나 병원에 가기 힘든 환자에게 보다 정확한 간병방법을 제공하기 위한 빅데이터 기반 분석 시스템 개발

#### What did I do.

- 팀장
- 데이터 수집 : 간병인 온라인 설문조사, 의료 홈페이지, 공공데이터
- 데이터 저장 : 1대의 Name Node와 3대의 Data Node로 이루어진 **하둡** **완전 분산 모드 구축**
- 데이터 처리 : **R**을 활용한 **데이터 정제**
- 데이터 분석 : **R**을 활용한 **분류 분석** (**KNN Algorithm**)
- 데이터 시각화 : **R shiny**을 활용한 R 시각화 **웹 페이지 구현**
- 공공데이터 시각화 및 분석 : **Tableau**를 활용한 **시각화 및 분석**

#### Tech Stack.

- JSP, TOMCAT, HDFS, R, R shiny, Tableau
- KNN(K-Nearest Neighbor) Algorithm

---

## **IoT** 환경을 위한 빅데이터 기반 센서 데이터 처리 및 분석 연구

- 2018.08.01. ~ 2018.08.31.
- 한국산업기술대학교

#### Description.

- IoT 환경에서 자주 사용되는 라즈베리 파이를 이용하여 데이터를 생성하고, 다양한 빅데이터 솔루션을 사용하여 데이터를 수집, 저장, 처리, 분석 및 시각화를 통해 관계를 검증
- 온도와 습도에 영향을 주는 요인으로 판단되는 기압, 밀도 등 다양한 센서를 활용하여 향후 날씨까지 예측할 수 있는 연구 기대

#### What did I do.

- 이상치 제거 : **R**의 ggplot, panels, boxplot을 활용한 **이상치 제거**
- 데이터 분석 : **R**을 활용한 **선형회귀분석**(**Linear Regression Analysis**)
- 데이터 시각화 : **R**을 활용한 시각화

#### Tech Stack.

- Raspberry Pi, Python, HDFS, mysql, Sqoop, Hive, R
- Linear Regression Analysis

> D.J. Shin, **J.H. Park**, J.H. Kim, K.J. Kwak, J.M. Park, J.J. Kim "Big Data-based Sensor Data Processing and Analysis for IoT Environment,” IIBC, Vol. 19, No. 1, pp.117-126, Feb. 28, 2019. 

---

## 미세먼지 감소를 위한 대중교통 만족도 분석

- 2018.05.21. ~ 2018.06.24.
- 한국산업기술대학교

#### Description.

- 대중교통 이용률과 만족도에 영향을 미치는 요소를 분석하여 대중교통 이용률을 증가시키고 미세먼지를 감소시키기 위한 빅데이터 기반 분석 시스템 개발

#### What did I do.

- 팀장
- 공공데이터 수집
- 데이터 저장 : 1대의 Name Node와 3대의 Data Node로 이루어진 **하둡** **완전 분산 모드 구축**
- 데이터 처리 : **R**을 활용한 **데이터 정제**
- 데이터 분석 : **R**을 활용한 **다중선형회귀분석**(**Multiple Linear Regression Analysis**)
- 데이터 시각화 : **R**을 활용한 시각화

#### Tech Stack.

- HDFS, Pig, R
- Multiple Linear Regression Analysis

<br/>

<br/>

# Other Experiences.

## 마이셀럽스

- 2019.03.29. ~ 2019.06.28. (3개월)
- 데이터팀 인턴
  - 데이터 수집 및 전처리

#### What did I do.

- Web Crawling
  - 화장품 정보, 리뷰 수집 및 DB 관리
    - Glowpick, Oliveyoung
  - 블로그 이미지 및 텍스트 데이터 수집
    - 여행 / celeb
  - Celeb SNS 게시물 수집
    - facebook, instagram, twitter
  - YouTube 영상 데이터 수집
    - celeb 뮤직비디오 및 광고 /교회 설교 영상
- 데이터 처리
  - 수집한 화장품 리뷰의 각 개체별 키토크 추출
- 업무 자동화 프로그램 개발
  - 단순 반복 업무를 효율적으로 수행하기 위한 자동화 프로그램 개발
- App Q/A
  - Log 분석
  - 서비스 테스트, 기능 품질 관리
  - 음성인식 발화 테스트
  - 키토크 보완

#### Tech Stack.

- Python
  - Web Crawling
    - request
    - beautifulsoup
    - selenium
  - Google Image Crawling
    - google_images_download
  - YouTube Data Crawling
    - pytube
    - youtube_dl
  - Data Management
    - pymysql

- MySQL
  - Data Management
- Postman
  - API test

<br/>

<br/>

# Other Activity.

## 빅데이터 세미나 및 관련 연구

- 2017.04.05. ~ 2018.12.07.
- 한국산업기술대학교 ACLab

## PBL Study 동아리 그룹 활동

- 2018.04.16. ~ 2018.06.21.
- R 프로그래밍 기반 빅데이터 분석 기법 활용
- 한국산업기술대학교

## 제자사랑 멘토링 프로그램

- 2018.03.23. ~ 2018.05.25.

- 비정형 데이터베이스 연구
- 한국산업기술대학교

## 제자사랑 멘토링 프로그램

- 2017.09.04. ~ 2017.11.24.

- 빅데이터 시스템 분석 및 설계
- 한국산업기술대학교

<br/>

<br/>

# Education

## SSAFY 4기

- 2020.07.08. ~ 현재

## 핀테크 서비스 개발 실습 초급 과정

- 2020.06.15. ~ 2020.06.19. (40H)
- KISA(한국인터넷진흥원)

## 슬기로운 금융인생활 

- 2020.05.09. ~ 2020.05.23. (20H)
- WEPLAY WEWORK 3기
- 복합금융컨설팅

## 머신러닝 기반의 빅데이터 분석양성과정

- 2018.12.13. ~ 2019.03.28. (560H)
- KIC캠퍼스학원

## 청년 AI·BigData 아카데미

- 2018.11.09 ~ 2019.01.05 (80H)
- POSTECHx 자기주도적 학습 시스템 온라인 과정

<br/>

# certificate

2019.04.09.	ADsP(데이터 분석 준전문가)

2018.05.25.	정보처리기사

<br/>

# Language

2019.12.22   TOEIC (675)

2018.12.03   Opic (IM2)

<br/>

# Overseas Activity.

2020.07.04. ~ 2020.08.09.	베트남 랜선 선교

2020.01.19. ~ 2020.01.31.	파라과이 국외선교

2019.07.31. ~ 2019.08.03.	국내선교

2019.07.07. ~ 2019.07.13.	베트남 국외선교

2016.02.01. ~ 현재.				미디어 방송 팀

<br/>

[Tistory 블로그](https://data-make.tistory.com/)

- Description.
- What did I do.
- Tech Stack.