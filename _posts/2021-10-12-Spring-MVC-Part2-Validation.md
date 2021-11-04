---
layout: post
title: Spring MVC Part 2. Validation
summary: (MVC) 스프링 MVC 2편 - 백엔드 웹 개발 활용 기술
categories: (Inflearn)Spring-MVC-2
featured-img: spring_mvc_2
# mathjax: true
---

# Spring MVC Part 2. Validation

영한님의 [스프링 MVC 2편 - 백엔드 웹 개발 활용 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-2/) 강의 노트

# Spring Verification

- 서버단에서 입력 데이터 검증
- 검증 실패 시 검증 오류 결과를 포함한 Model 반환 및 안내

# BindingResult

- BindingResult bindingResult 은 @ModelAttribute 객체 다음에 와야 함

**필드 오류 처리**

```java
bindingResult.addError(new FieldError("item", "itemName", "상품 이름은 필수입니다."));
```

```html
<input
  type="text"
  id="itemName"
  th:field="*{itemName}"
  th:errorclass="field-error"
  class="form-control"
  placeholder="이름을
입력하세요"
/>
<div class="field-error" th:errors="*{itemName}">상품명 오류</div>
```

**글로벌 오류 처리**

```java
bindingResult.addError(new ObjectError("item", "가격 * 수량의 합은 10,000원 이상이어야 합니다. 현재 값 = " + resultPrice));
```

```html
<div th:if="${#fields.hasGlobalErrors()}">
  <p
    class="field-error"
    th:each="err : ${#fields.globalErrors()}"
    th:text="$
{err}"
  >
    전체 오류 메시지
  </p>
</div>
```

> [Validation and Error Messages](https://www.thymeleaf.org/doc/tutorials/3.0/thymeleafspring.html#validation-and-error-messages)
