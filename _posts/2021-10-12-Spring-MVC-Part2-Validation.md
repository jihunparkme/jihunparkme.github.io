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

- BindingResult 가 있으면 @ModelAttribute 에 데이터 바인딩 시 오류가 발생해도 컨트롤러가 호출

- Model에 자동으로 포함

## Setting

**application.properties**

```properties
spring.messages.basename=messages,errors
```

**errors.properties**

```properties
required.item.itemName=상품 이름은 필수입니다.
range.item.price=가격은 {0} ~ {1} 까지 허용합니다.
max.item.quantity=수량은 최대 {0} 까지 허용합니다.
totalPriceMin=가격 * 수량의 합은 {0}원 이상이어야 합니다. 현재 값 = {1}
required.default = 기본 오류 메시지
```

## FieldError

**필드 오류 처리**

- 오류 발생시 사용자 입력 값을 저장하는 기능을 제공 (rejectedValue)

```java
bindingResult.addError(new FieldError(
  "item", // objectName (오류가 발생한 객체 이름)
  "price", // field (오류 필드)
  item.getPrice(), //rejectedValue (사용자가 입력한 값)
  false, // bindingFailure(바인딩 실패 여부)
  new String[]{"range.item.price", "required.default"}, // codes (메시지 코드)
  new Object[]{1000, 1000000}, // arguments (메시지에서 사용하는 인자)
  "상품 가격 오류" // defaultMessage
  ));
```

- `th:field`는 평소에는 모델 객체의 값을 사용하지만, 오류가 발생하면 FieldError 에서 보관한 값을 사용해서 값을 출력

```html
<input
  type="text"
  id="price"
  th:field="*{price}"
  th:errorclass="field-error"
  class="form-control"
  placeholder="가격을 입력하세요"
/>
<div class="field-error" th:errors="*{price}">가격 오류</div>
```

## ObjectError

**글로벌 오류 처리**

```java
bindingResult.addError(new ObjectError(
  "item", // objectName
  null, // codes
  null, // arguments
  "가격 * 수량의 합은 10,000원 이상이어야 합니다. 현재 값 = " + resultPrice // defaultMessage
  ));
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
