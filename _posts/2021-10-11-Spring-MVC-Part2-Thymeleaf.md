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
