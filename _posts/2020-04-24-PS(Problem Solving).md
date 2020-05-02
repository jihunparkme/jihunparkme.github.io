---
layout: post
title: PS Study
summary: Let's improve our PS.
categories: IT
featured-img: PS
# mathjax: true
---



# PS(Problem Solving)

1. 알고리즘 공부
   - 수단
     - 백준 강의
     - 유튜브 강의
  - 종만북
   - 구현력(**순서도** 활용)
     - 내가 어떤 프로그램을 만들고자 하는지 명확히
     - 무엇을 입력받아 어디에 저장하고 어떤 과정을 거쳐, 중간 결과로 무엇을 겅도 최종적으로 이런 결과물을 추력
   - 문제해결능력
     - 양질의 문제 풀기
     - 접근한 다양한 방법들을 잘 정리
   - 배경지식
     - 프로그래밍 문법
     - 알고리즘
     - 자료구조
     - 선형대수
     - 확률

2. 양보다는 질좋은 문제
   - **[USACO](https://www.acmicpc.net/category/106)**
   - **[한국정보올림피아드](https://www.acmicpc.net/category/55)**
   - **[AtCoder](https://atcoder.jp/)**
   - **[Codeforces](https://codeforces.com/)**

3. 좋은 랭작도 중요
   - 코테를 준비한다면
     - **배열, 트리, 그래프, 힙, BST, 스택, 큐** 등 자료구조
     - **DFS/BFS, 백트래킹, 정렬, DP, 분할 정복, 최단거리** 등 알고리즘
   - 구현 능력을 키우기 위해 많이 푸는 것도 중요
   - USACO Bronze, 정올 초등부, AtCoder/Codeforces 쉬운 문제
   - BOJ 문제집(C++ 배우기)
4. 오래 붙잡고 있는 것은 결코 도움이 되지 않음
   - 솔루션이 떠오르지 않아 아무 진척도 없는 단계
   - 약 1시간 정도
   - 솔루션을 보고 코드를 본다면, 자신이 안 보고 코드를 작성해서 제출해야 함
5. 좋은 멘토
6. 구체적은 목표, 스스로의 기준 설정
7. 함께 공부하기
   - 스터디
   - 블로그

---

#### 코딩테스트

- 개발자의 기초적인 소양을 보는 시험 : 주어진 시간 동안 주어진 문제를 요구사항에 맞게 프로그래밍
  - 기초 소양 :  (문제 > 모델링(추상화) > 절차적 사고 > 구현)
    - 추상화(상황 분석) : 배열이 들어오고, 최소와 최대를 뺀 값
    - 절차적 사고 : 정렬? 시간복잡도.. 내장함수? 반복문?
    - 구현 능력
  - 요구사항 : 구현 조건이 복잡한 언어 영역(조건문, 함수 구현), 문제를 읽고 분해하는 연습이 필요
    - 구현 : 파싱, 해싱, 정렬, 시뮬레이션
    - 탐색 : 탐색(BFS, DFS), 완전탐색(백트래킹)
    - 자료구조 : 스택, 큐 힙 등
    - 알고리즘 : Greedy, DP, 이분탐색 등
  - 환경 체크(사용 언어) : 장/단점에 따라 언어를 바꿔 사용하는 것이 포인트
    - C++ : 비교적 문법은 어렵지만 빠른 속도, STL 등의 장점(재귀함수, 자료구조 사용 시)
    - Python : 쉽고 문법이 간단, 범용성이 넓음, 하지만 느린 단점(string, 정렬, 파싱 등 객체를 다룰 시)
    - Java : 비교적 문법도 어렵고 느린 편, 하지만 Java를 필요하는 직군이 많음 
  - 에러
    - 컴파일 에러(CE) : 문법 오류
    - 시간 초과(TLE) : 최적화 필요 (반복문, 무한루프)
    - 메모리 초과(MLE) : 최적화 필요 (스택, 힙 메모리)
    - 런타임 에러(RE) : 과정 오류 (0으로 나눈 경우, index 오류, 무한 루프)
    - 틀렸습니다(WA) : 수 많은 이유..
      - 제한 및 대소 관계 (이상, 이하, 초과, 미만, mix, max)
      - 예외 처리 (단, 없는 경우 -1을 출력한다~)
      - 입력과 출력 (공백, 양식, 순서, 정렬 유무)
      - 시간 제한과 메모리 제한 (알고리즘, 자료구조 선택)
      - 알고리즘이 맞는가?
      - 생각한 로직대로 구현했는가? (중복 처리, 예외처리, 불필요한 반복문)
      - 불필요한 반복문이 있는가?
      - 중복을 처리했는가?
  - 디버깅의 반복 + 멘탈 관리가 중요
  - 각 단계별 보완
    - 모델링
      - 수치 및 조건 정리 (미리 변수와 함수를 세팅)
      - 전체적인 흐름 그리기
      - 입출력 예제 이해
    - 절차적 사고
      - 필수 알고리즘은 암기
      - 설명과 함께 풀어보기
      - 유형 많이 풀어보기
    - 구현
      - 디버깅 연습 필수
      - print() 를 활용하여 디버깅 
      - 쉽고 간단한 문제를 많이 풀기
      - 본인만의 스타일 만들기
- 가장 기본적인 준비
  - C++ / Python 기본 문법 공부
    - 코드업 기초 100제
      - https://codeup.kr/problemsetsol.php?psid=23
    - 그리디, 탐색유형(BFS, DFS), DP 유형 문제 풀이
    - BOJ
    - 특정 기업 대상 기출문제
      - 삼성전자(BOJ, SW역평기출)
      - 카카오(프로그래머스 기출)
- PS 연습
  - 삼성전자
    - https://swexpertacademy.com/main/identity/anonymous/loginPage.do
      - 난의도 3~5
    - https://www.acmicpc.net/workbook/view/1152
  - 브루트 포스, DP, 큐/스택, DFS, BFS, 탐욕법
  - 카카오
    - https://programmers.co.kr/learn/challenges?tab=all_challenges
    - https://www.hackerrank.com/
    - https://leetcode.com/
  - SW 역량테스트
    - https://swexpertacademy.com/main/capacityTest/main.do
    - [B형 공부](https://baactree.tistory.com/53)
- 운영체제
  - https://parksb.github.io/article/5.html

---

#### 취업

- 명확한 분야 선택
  - 웹, 앱, 4차산업관련(IOT, 인공지능, 음성처리 등)
    - 웹, 앱 쪽은 학원
      - JavaScript
      - node.js 서버
      - typeScript
      - vue
      - react
    - 코테 준비는 사용 언어를 선택하고 코딩스터디
      - 책으로 이론 병행하면서(세미나처럼) 문제도 풀고 풀이를 칠판에 or 구두로 설명하는 스터디
    - 토이 프로젝트 스터디
  - 백엔드
    - https://www.mindmeister.com/ko/530652609/_?fullscreen=1
    - https://okky.kr/article/467416
- 중소기업?
  - 보통 유지보수 업무가 대다수
    - 어떤 업무를 하고, 사용 기술스택이 무엇인지 확인, 최신 기술일수록 배울 수 있는게 많아짐
- 교육
  - [멀티캠퍼스](https://www.multicampus.com/system/menu/iframe?p_url=L3B1Ymxpc2gvcGFnZXMvZWR1XzR0aC5odG1s&p_menu=MTE3I01BSU4=&p_gubun=Qw==&param2=106000000000000&param3=106001000000000)
  - [KFQ](http://kcm.kfq.or.kr/)



> reference
>
> - [PS를 공부하는 방법](https://subinium.github.io/how-to-study-problem-solving/)
> - [PS/CP 공부 유형 및 보완법](https://subinium.github.io/PS-Study-Types-and-Complements/)
> - [문제 풀이 연습](https://koosaga.com/217)
> - [알고리즘 공부](https://baactree.tistory.com/52)
> - [알고리즘 공부 방법/순서](https://baactree.tistory.com/14)
> - [PS 시작하기](https://plzrun.tistory.com/entry/알고리즘-문제풀이PS-시작하기)
> - [코딩테스트 문제 리스트와 연습 팁](https://www.notion.so/580c3a42f21b49b497b7089f539a9f78)

