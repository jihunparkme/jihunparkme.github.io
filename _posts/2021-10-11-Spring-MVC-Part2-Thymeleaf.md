---
layout: post
title: Spring MVC Part 2. Thymeleaf
summary: (MVC) 스프링 MVC 2편 - 백엔드 웹 개발 활용 기술
categories: (Inflearn)Spring-MVC-2
featured-img: spring_mvc_2
# mathjax: true
---

# Spring MVC Part 2. Thymeleaf

영한님의 [스프링 MVC 2편 - 백엔드 웹 개발 활용 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-2/) 강의 노트

# Reference

> [공식 사이트](https://www.thymeleaf.org/)
>
> [공식 메뉴얼 - 기본 기능](https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html)
>
> [공식 메뉴얼 - 스프링 통합](https://www.thymeleaf.org/doc/tutorials/3.0/thymeleafspring.html)

# 기본 기능

- 사용 선언

  ```html
  <html xmlns:th="http://www.thymeleaf.org"></html>
  ```

- 속성 변경

  ```html
  th:href="@{/css/bootstrap.min.css}"
  ```

- URL 링크 표현식

  ```html
  th:href="@{/css/bootstrap.min.css}"
  <!-- -->
  th:href="@{/basic/items/{itemId}(itemId=${item.id})}"
  th:href="@{/basic/items/{itemId}(itemId=${item.id}, query='test')}"
  th:href="@{|/basic/items/${item.id}|}"
  ```

- 속성 변경

  ```html
  th:onclick="|location.href='@{/basic/items/add}'|"
  ```

- 반복 출력

  ```html
  <tr th:each="item : ${items}"></tr>
  ```

- 변수 표현식

  ```html
  <td th:text="${item.price}">10000</td>
  ```

- 속성 변경
  ```html
  <input
    type="text"
    id="price"
    name="price"
    value="10000"
    th:value="${item.price}"
  />
  ```

## 기본 표현식

<https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html#standard-expression-syntax>

```
ㅇ 간단한 표현
  - 변수 표현식: ${...}
  - 선택 변수 표현식: \*{...}
  - 메시지 표현식: #{...}
  - 링크 URL 표현식: @{...}
  - 조각 표현식: ~{...}

ㅇ 리터럴
  - 텍스트: 'one text', 'Another one!',…
  - 숫자: 0, 34, 3.0, 12.3,…
  - 불린: true, false
  - 널: null
  - 리터럴 토큰: one, sometext, main,…

ㅇ 문자 연산
  - 문자 합치기: +
  - 리터럴 대체: |The name is ${name}|

ㅇ 산술 연산
  - Binary operators: +, -, \*, /, %
  - Minus sign (unary operator): -

ㅇ 불린 연산
  - Binary operators: and, or
  - Boolean negation (unary operator): !, not

ㅇ 비교와 동등
  - 비교: >, <, >=, <= (gt, lt, ge, le)
  - 동등 연산: ==, != (eq, ne)

ㅇ 조건 연산
  - If-then: (if) ? (then)
  - If-then-else: (if) ? (then) : (else)
  - Default: (value) ?: (defaultvalue)

ㅇ 특별한 토큰
  - No-Operation: \_
```

## 텍스트

- 텍스트 출력

  - 기본적으로 escape 를 제공

    - escape : HTML 에서 사용하는 특수 문자를 HTML 엔티티로 변경하는 것
    - HTML 엔티티 : `<` 문자를 태그의 시작이 아닌 문자로 표현하는 방법

  ```html
  <ul>
    <li>th:text 사용 = <span th:text="${data}"></span></li>
    <li>컨텐츠 안에서 직접 출력하기 = [[${data}]]</li>
  </ul>
  ```

- Unescape

  - `th:text` --> `th:utext`
  - `[[...]]` --> `[(...)]`

  ```html
  <ul>
    <li>th:utext = <span th:utext="${data}"></span></li>
    <li><span th:inline="none">[(...)] = </span>[(${data})]</li>
  </ul>
  ```

## SpringEL 표현식

**Object**

- `${user.username}` = userA
- `${user['username']}` = userA
- `${user.getUsername()}` = userA

**List**

- `${users[0].username}` = userA
- `${users[0]['username']}` = userA
- `${users[0].getUsername()}` = userA

**Map**

- `${userMap['userA'].username}` = userA
- `${userMap['userA']['username']}` = userA
- `${userMap['userA'].getUsername()}` = userA

**지역변수**

```html
<div th:with="first=${users[0]}">
  <p>first member name : <span th:text="${first.username}"></span></p>
</div>
```

## 기본 객체

**Thymeleaf 기본 객체**

- `${#request}`
- `${#response}`
- `${#session}`
- `${#servletContext}`
- `${#locale}`

**편의 객체**

- HTTP 요청 파라미터 접근: `${param.paramData}`
- HTTP 세션 접근: `${session.sessionData}`
- 스프링 빈 접근: `${@helloBean.hello('Spring!')}`

## 유틸리티 객체와 날짜

- #message : 메시지, 국제화 처리
- #uris : URI 이스케이프 지원
- #dates : java.util.Date 서식 지원
- #calendars : java.util.Calendar 서식 지원
- #temporals : 자바8 날짜 서식 지원
- #numbers : 숫자 서식 지원
- #strings : 문자 관련 편의 기능
- #objects : 객체 관련 기능 제공
- #bools : boolean 관련 기능 제공
- #arrays : 배열 관련 기능 제공
- #lists , #sets , #maps : 컬렉션 관련 기능 제공
- #ids : 아이디 처리 관련 기능 제공, 뒤에서 설명

**Reference**

> [타임리프 유틸리티 객체](https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html#expression-utilityobjects)
>
> [유틸리티 객체 예시](https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html#appendix-b-expressionutility-objects)

## URL 링크

- 단순 URL

  - /hello
    ```html
    <a th:href="@{/hello}"></a>
    ```

- query parameter

  - /hello?param1=data1&param2=data2
    ```html
    <a th:href="@{/hello(param1=${param1}, param2=${param2})}"></a>
    ```

- path variable

  - /hello/data1/data2
    ```html
    <a
      th:href="@{/hello/{param1}/{param2}(param1=${param1}, param2=${param2})}"
    ></a>
    ```

- query parameter + path variable

  - /hello/data1?param2=data2
    ```html
    <a th:href="@{/hello/{param1}(param1=${param1}, param2=${param2})}"></a>
    ```

**Reference**

> <https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html#link-urls>

## 리터럴

- 문자: 'hello' (문자 리터럴은 항상 작은따옴표로 감싸야 함)
  ```html
  <span th:text="'hello'"></span>
  ```
- 숫자: 10
- 불린: true , false
- null: null

## 연산

- 산술 연산

  ```html
  10 + 2 = <span th:text="10 + 2"></span>
  ```

- 비교 연산

  ```html
  <!-- 
    > (gt)
    < (lt)
    >= (ge)
    <= (le)
    ! (not)
    == (eq)
    != (neq, ne)`
  -->
  1 >= 10 = <span th:text="1 >= 10"></span>
  ```

- 조건식

  ```html
  (10 % 2 == 0) ? = <span th:text="(10 % 2 == 0)?'짝수':'홀수'"></span>
  ```

- Elvis 연산자

  ```html
  <!-- 데이터가 없을 경우 설정 문자열 출력 -->
  ${data} = <span th:text="${data}?: '데이터가 없습니다.'"></span>
  ```

- No-Operation
  ```html
  <!-- 데이터가 없을 경우 tag 데이터 그대로 출력 (Thymeleaf 가 실행되지 않는 것 처럼 동작) -->
  ${data} = <span th:text="${data}?: _">데이터가 없습니다.</span>
  ```

## 속성 값 설정

- 속성 설정
  ```html
  <input type="text" name="mock" th:name="userA" />
  ```
- 속성 추가
  ```html
  <input type="text" class="text" th:classappend="large" /><br />
  ```
- checked 처리
  ```html
  <input type="checkbox" name="active" th:checked="true" /><br />
  <input type="checkbox" name="active" th:checked="false" /><br />
  <input type="checkbox" name="active" th:checked="${isChecked}" /><br />
  ```

## 반복

- 반복

  ```html
  <tr th:each="user : ${users}">
    <td th:text="${user.username}">username</td>
    <td th:text="${user.age}">0</td>
  </tr>
  ```

- 상태 유지

  ```html
  <!-- 생략 시 userStat 로 사용 -->
  <tr th:each="user, state : ${users}"></tr>
  ```

  - index : 0부터 시작
  - count : 1부터 시작
  - size : 전체 사이즈
  - even , odd : 홀/짝수 여부
  - first , last :처음/마지막 여부
  - current : 현재 객체

## 조건부 평가

- if, unless

  ```html
  <span th:text="'어른'" th:if="${user.age gt 20}"></span>
  <span th:text="'어른'" th:unless="${user.age le 20}"></span>
  ```

- switch

  ```html
  <td th:switch="${user.age}">
    <span th:case="10">10살</span>
    <span th:case="20">20살</span>
    <span th:case="*">기타</span>
  </td>
  ```

## 주석

- 표준 HTML 주석

  - 타임리프가 렌더링하지 않고 유지

  ```html
  <!-- <span th:text="${data}"></span> -->
  ```

- 타임리프 파서 주석

  - 렌더링에서 주석 부분을 제거 (타임리프 주석)

  ```html
  <!--/* [[${data}]] */-->

  <!--/*-->
  <span th:text="${data}">html data</span>
  <!--*/-->
  ```

- 타임리프 프로토타입 주석

  - 타임리프 렌더링을 거쳐야만 이 부분이 정상 렌더링 (HTML 에서만 주석 처리)

  ```html
  <!--/*/
  <span th:text="${data}">html data</span>
  /*/-->
  ```

## 블록

- th:each 로 해결이 어려울 때 사용

```html
<th:block th:each="user : ${users}">
  <div>
    name: <span th:text="${user.username}"></span> age:
    <span th:text="${user.age}"></span>
  </div>
  <div>요약 <span th:text="${user.username} + ' / ' + ${user.age}"></span></div>
</th:block>
```

## JavaScript Inline

- javascript inline

  ```html
  <script th:inline="javascript">
    var username = [[${user.username}]];
    var age = [[${user.age}]];
    //자바스크립트 내추럴 템플릿
    var username2 = /*[[${user.username}]]*/ "test username";
    //객체
    var user = [[${user}]];
  </script>

  <!--
      var username = "userA";
      var age = 10;
      var username2 = "userA";
      var user = {"username":"userA","age":10};
  -->
  ```

- each

  ```html
  <script th:inline="javascript">
    [# th:each="user, stat : ${users}"]
    var user[[${stat.count}]] = [[${user}]];
    [/]
  </script>
  <!--
    var user1 = {"username":"userA","age":10};
    var user2 = {"username":"userB","age":20};
    var user3 = {"username":"userC","age":30};
  -->
  ```

## 템플릿 조각

- `/resources/templates/template/fragment/footer.html`

  ```html
  <!DOCTYPE html>
  <html xmlns:th="http://www.thymeleaf.org">
    <body>
      <footer th:fragment="copy">푸터 자리 입니다.</footer>

      <footer th:fragment="copyParam (param1, param2)">
        <p>파라미터 자리 입니다.</p>
        <p th:text="${param1}"></p>
        <p th:text="${param2}"></p>
      </footer>
    </body>
  </html>
  ```

- `/resources/templates/template/fragment/fragmentMain.html`

  ```html
  <!DOCTYPE html>
  <html xmlns:th="http://www.thymeleaf.org">
    <head>
      <meta charset="UTF-8" />
      <title>Title</title>
    </head>
    <body>
      <h1>부분 포함</h1>
      <h2>부분 포함 insert (div tag 안에 삽입)</h2>
      <div th:insert="~{template/fragment/footer :: copy}"></div>

      <h2>부분 포함 replace (div tag 대체)</h2>
      <div th:replace="~{template/fragment/footer :: copy}"></div>

      <h1>파라미터 사용</h1>
      <div
        th:replace="~{template/fragment/footer :: copyParam ('데이터1', '데이터2')}"
      ></div>
    </body>
  </html>
  ```

## 템플릿 레이아웃

**동적인 레이아웃**

- `/resources/templates/template/layout/base.html`

  - 레이아웃이라는 큰 틀

  ```html
  <html xmlns:th="http://www.thymeleaf.org">
    <head th:fragment="common_header(title,links)">
      <title th:replace="${title}">레이아웃 타이틀</title>

      <!-- 공통 -->
      <link
        rel="stylesheet"
        type="text/css"
        media="all"
        th:href="@{/css/awesomeapp.css}"
      />
      <link rel="shortcut icon" th:href="@{/images/favicon.ico}" />
      <script
        type="text/javascript"
        th:src="@{/sh/scripts/codebase.js}"
      ></script>

      <!-- 추가 -->
      <th:block th:replace="${links}" />
    </head>
  </html>
  ```

- `/resources/templates/template/layout/layoutMain.html`

  - 틀 안에 필요한 코드 조각들을 전달
  - ::title 은 현재 페이지의 title tag 들을 전달
  - ::link 은 현재 페이지의 link tag 들을 전달

  ```html
  <!DOCTYPE html>
  <html xmlns:th="http://www.thymeleaf.org">
    <head
      th:replace="template/layout/base :: common_header(~{::title},~{::link})"
    >
      <title>메인 타이틀</title>
      <link rel="stylesheet" th:href="@{/css/bootstrap.min.css}" />
      <link rel="stylesheet" th:href="@{/themes/smoothness/jquery-ui.css}" />
    </head>
    <body>
      메인 컨텐츠
    </body>
  </html>
  ```

**메인 레이아웃**

- `/resources/templates/template/layoutExtend/layoutFile.html`

  - 기본 레이아웃(header, footer) 틀은 유지하고 title, content 만 변경

  ```html
  <!DOCTYPE html>
  <html
    th:fragment="layout (title, content)"
    xmlns:th="http://www.thymeleaf.org"
  >
    <head>
      <title th:replace="${title}">레이아웃 타이틀</title>
    </head>
    <body>
      <h1>레이아웃 H1</h1>
      <div th:replace="${content}">
        <p>레이아웃 컨텐츠</p>
      </div>
      <footer>레이아웃 푸터</footer>
    </body>
  </html>
  ```

- `/resources/templates/template/layoutExtend/layoutExtendMain.html `

  - 기본 레이아웃 틀로 교체하는데 하는데 title, content 는 전달

  ```html
  <!DOCTYPE html>
  <html
    th:replace="~{template/layoutExtend/layoutFile :: layout(~{::title}, ~{::section})}"
    xmlns:th="http://www.thymeleaf.org"
  >
    <head>
      <title>메인 페이지 타이틀</title>
    </head>
    <body>
      <section>
        <p>메인 페이지 컨텐츠</p>
        <div>메인 페이지 포함 내용</div>
      </section>
    </body>
  </html>
  ```
