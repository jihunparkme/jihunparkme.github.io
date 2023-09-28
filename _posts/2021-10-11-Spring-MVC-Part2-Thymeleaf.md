---
layout: post
title: Thymeleaf
summary: Thymeleaf
categories: Spring-Conquest
featured-img: spring_mvc_2
# mathjax: true
---

# Spring MVC Part 2. Thymeleaf

영한님의 [스프링 MVC 2편 - 백엔드 웹 개발 활용 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-2/) 강의 노트

[Project](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2)

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

**Safe Navigation Operator**

```html
<div th:if="${errors?.containsKey('globalError')}"></div>
```

- errors`?.` 은 errors 가 null 일때 NullPointerException 대신, null 을 반환하는 문법 [참고](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions-operator-safe-navigation)

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

# Form

## 입력 폼 처리

```html
<form action="item.html" th:action th:object="${item}" method="post">
  <div>
    <label for="itemName">상품명</label>
    <input
      type="text"
      id="itemName"
      th:field="*{itemName}"
      class="formcontrol"
      placeholder="이름을 입력하세요"
    />
  </div>
</form>
```

- `th:object` : 커맨드 객체를 지정
- `\*{...}` : 선택 변수 식 (th:object 에서 선택한 객체에 접근)
- `th:field` : HTML 태그의 id , name , value 속성을 자동으로 생성
- 렌더링 전/후

  ```html
  <input type="text" th:field="*{itemName}" />
  ```

  ```html
  <input type="text" id="itemName" name="itemName" th:value="*{itemName}" />
  ```

## 체크 박스

### 단일

**Register**

```html
<div>
  <div class="form-check">
    <input
      type="checkbox"
      id="open"
      th:field="*{open}"
      class="form-checkinput"
    />
    <label for="open" class="form-check-label">판매 오픈</label>
  </div>
</div>
```

- 타임리프가 자동으로 `<input type="hidden" name="_open" value="on"/>` 생성

  - 체크 박스를 체크할 경우 on 을 전달하지만, 체크하지 않을 경우 값 자체를 전달하지 않음 -> 이 경우 hidden type 의 \_name input 태그를 사용하게 되면, false 로 값을 전달 (\_open=on)

**View**

```html
<div>
  <div class="form-check">
    <input
      type="checkbox"
      id="open"
      th:field="${item.open}"
      class="form-check-input"
      disabled
    />
    <label for="open" class="form-check-label">판매 오픈</label>
  </div>
</div>
```

### 멀티

(참고) @ModelAttribute 를 사용하면 해당 Controller 호출 시 regions() 에서 반환한 값이 자동으로 Model에 항상 담기게 됨

```java
@ModelAttribute("regions")
public Map<String, String> regions() {
    Map<String, String> regions = new LinkedHashMap<>();
    regions.put("SEOUL", "서울");
    regions.put("BUSAN", "부산");
    regions.put("JEJU", "제주");
    return regions;
}
```

**Register**

```html
<div th:each="region : ${regions}" class="form-check form-check-inline">
  <input
    type="checkbox"
    th:field="*{regions}"
    th:value="${region.key}"
    class="form-check-input"
  />
  <label
    th:for="${#ids.prev('regions')}"
    th:text="${region.value}"
    class="form-check-label"
    >서울</label
  >
</div>
```

- 타임리프는 each로 체크박스 생성 시 동적으로 id에 순번을 매겨준다. `#ids`는 동적으로 생성된 id를 인식

- result

  ```html
  <input
    type="checkbox"
    value="SEOUL"
    class="form-check-input"
    id="regions1"
    name="regions"
  />
  <input
    type="checkbox"
    value="BUSAN"
    class="form-check-input"
    id="regions2"
    name="regions"
  />
  <input
    type="checkbox"
    value="JEJU"
    class="form-check-input"
    id="regions3"
    name="regions"
  />
  ```

**View**

```html
<div th:each="region : ${regions}" class="form-check form-check-inline">
  <input
    type="checkbox"
    th:field="${item.regions}"
    th:value="${region.key}"
    class="form-check-input"
    disabled
  />
  <label
    th:for="${#ids.prev('regions')}"
    th:text="${region.value}"
    class="form-check-label"
    >서울</label
  >
</div>
```

- 타임리프는 `th:field`에 지정한 값과 `th:value`의 값을 비교해서 체크를 자동으로 처리

## 라디오 버튼

```java
public enum ItemType {

    BOOK("도서"), FOOD("식품"), ETC("기타"); // NAME(description)

    private final String description;

    ItemType(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}
```

```html
<div th:each="type : ${itemTypes}" class="form-check form-check-inline">
  <input
    type="radio"
    th:field="*{itemType}"
    th:value="${type.name()}"
    class="form-check-input"
  />
  <label
    th:for="${#ids.prev('itemType')}"
    th:text="${type.description}"
    class="form-check-label"
  >
    BOOK
  </label>
</div>
```

- 라디오 버튼은 항상 하나의 값이 선택되어야 하므로 히든 버튼을 따로 생성하지 않음.

## 셀렉트 박스

**Register**

```html
<select th:field="*{deliveryCode}" class="form-select">
  <option value="">==배송 방식 선택==</option>
  <option
    th:each="deliveryCode : ${deliveryCodes}"
    th:value="${deliveryCode.code}"
    th:text="${deliveryCode.displayName}"
  >
    FAST
  </option>
</select>
```

---

**스프링 완전 정복 로드맵**

- 스프링 입문 > 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술
- [스프링 핵심 원리 > 기본편](https://jihunparkme.github.io/Spring-Core/)
- 모든 개발자를 위한 HTTP 웹 기본 지식
  - [Basic](https://jihunparkme.github.io/Http-Web-Network_basic/)
  - [Method](https://jihunparkme.github.io/Http-Web-Network_method/)
  - [Header](https://jihunparkme.github.io/Http-Web-Network_header/)
- 스프링 웹 MVC 1편
  - [Servlet](https://jihunparkme.github.io/Spring-MVC-Part1-Servlet/)
  - [MVC](https://jihunparkme.github.io/Spring-MVC-Part1-MVC/)
- 스프링 웹 MVC 2편
  - [Thymeleaf](https://jihunparkme.github.io/Spring-MVC-Part2-Thymeleaf/)
  - [etc](https://jihunparkme.github.io/Spring-MVC-Part2-Etc/)
  - [Validation](https://jihunparkme.github.io/Spring-MVC-Part2-Validation/)
  - [Login](https://jihunparkme.github.io/Spring-MVC-Part2-Login/)
  - [Exception](https://jihunparkme.github.io/Spring-MVC-Part2-Exception/)
- [스프링 DB 1편 > 데이터 접근 핵심 원리](https://jihunparkme.github.io/Spring-DB-Part1/)
- [스프링 DB 2편 > 데이터 접근 활용 기술](https://jihunparkme.github.io/Spring-DB-Part2/)
- [스프링 핵심 원리 > 고급편](https://jihunparkme.github.io/Spring-Core-Principles-Advanced/)
- [실전! 스프링 부트](https://jihunparkme.github.io/spring-boot/)