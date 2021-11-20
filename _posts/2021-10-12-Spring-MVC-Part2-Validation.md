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

[Project](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2)

# Spring Verification

- 서버단에서 입력 데이터 검증
- 검증 실패 시 검증 오류 결과를 포함한 Model 반환 및 안내

# BindingResult

- BindingResult bindingResult 은 @ModelAttribute 객체 다음에 와야 함

  - BindingResult 가 있으면 @ModelAttribute 에 데이터 바인딩 시 오류가 발생해도 컨트롤러가 호출
  - Model에 자동으로 포함

- BindingResult는 어떤 객체를 대상으로 검증하는지 target을 이미 알고 있음

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
required.default=기본 오류 메시지

required=필수 값 입니다.
```

- errorCode.ObjectName.fieldName
  - 위 Message가 없을 경우 errorCode에 해당하는 Message를 사용

## FieldError

**필드 오류 처리**

- 오류 발생시 사용자 입력 값을 저장하는 기능을 제공 (rejectedValue)

```java
bindingResult.rejectValue(
  "price", // field (오류 필드)
  "range", // errorCode (메시지 코드)
  new Object[]{1000, 1000000}, // errorArgs (메시지 인자)
  "상품 가격 오류" // defaultMessage
  );
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
bindingResult.reject(
  "totalPriceMin",  // errorCode
  new Object[]{10000, resultPrice}, // errorArgs
  null // defaultMessage
  );
```

```html
<div th:if="${#fields.hasGlobalErrors()}">
  <p
    class="field-error"
    th:each="err : ${#fields.globalErrors()}"
    th:text="${err}"
  >
    전체 오류 메시지
  </p>
</div>
```

> [Validation and Error Messages](https://www.thymeleaf.org/doc/tutorials/3.0/thymeleafspring.html#validation-and-error-messages)

## DefaultMessageCodesResolver 기본 메시지 생성 규칙

- MessageCodesResolver는 검증 오류 코드로 메시지 코드들을 생성

- MessageCodesResolver는 인터페이스, DefaultMessageCodesResolver는 기본 구현체

- rejectValue() , reject()는 내부에서 MessageCodesResolver를 사용

**필드 오류 (FieldError)**

`error code` : typeMismatch

`object name` : user

`field` : age

`field type` : int

1. typeMismatch.user.age

2. typeMismatch.age

3. typeMismatch.int

4. typeMismatch

**객체 오류 (ObjectError)**

`error code` : required

`object name` : item

1. required.item

2. required

## 오류 코드 관리 전략

- 중요하지 않은 메시지는 범용성 있는 requried 같은 간단한 메시지로 끝내고, 정말 중요한 메시지는 꼭 필요할 때 구체적으로 적어서 사용하는 방식이 효과적

1. rejectValue() 호출

2. MessageCodesResolver 를 사용해서 검증 오류 코드로 메시지 코드들을 생성

3. new FieldError() 를 생성하면서 메시지 코드들을 보관

4. th:erros 에서 메시지 코드들로 메시지를 순서대로 메시지에서 찾고 출력

## Spring 자체 검증 오류 메시지 처리

- 주로 타입 정보가 맞지 않을 경우 Spring 직접 검증

- Spring은 타입 오류가 발생하면 typeMismatch 오류 코드를 사용

  - typeMismatch.item.price
  - typeMismatch.price
  - typeMismatch.java.lang.Integer
  - typeMismatch

```properties
typeMismatch.java.lang.Integer=숫자를 입력해주세요.
typeMismatch=타입 오류입니다.
```

## Validator 분리

- Validator 분리를 위한 ItemValidator class

```java
@Component
public class ItemValidator implements Validator {

    /**
     * 해당 검증기를 지원하는 여부 확인
     * item ==clazz
     * item == subItem
     *
     * @param clazz
     */
    @Override
    public boolean supports(Class<?> clazz) {
        return Item.class.isAssignableFrom(clazz);

    }

    /**
     * 검증 대상 객체과 BindingResult
     *
     * @param target
     * @param errors
     */
    @Override
    public void validate(Object target, Errors errors) {

        Item item = (Item) target;
        ValidationUtils.rejectIfEmptyOrWhitespace(errors, "itemName", "required");

        if (item.getPrice() == null || item.getPrice() < 1000 || item.getPrice() > 1000000) {
            errors.rejectValue("price", "range", new Object[]{1000, 1000000}, null);
        }

        if (item.getQuantity() == null || item.getQuantity() > 10000) {
            errors.rejectValue("quantity", "max", new Object[]{9999}, null);
        }

        //특정 필드 예외가 아닌 전체 예외
        if (item.getPrice() != null && item.getQuantity() != null) {
            int resultPrice = item.getPrice() * item.getQuantity();
            if (resultPrice < 10000) {
                errors.reject("totalPriceMin", new Object[]{10000,
                        resultPrice}, null);
            }
        }
    }
}

```

- Controller에서 WebDataBinder를 통해 ItemValidator 호출

```java
// WebDataBinder에 검증기 추가 시 해당 컨트롤러에서는 검증기 자동 적용
@InitBinder
public void init(WebDataBinder dataBinder) {
    dataBinder.addValidators(itemValidator);
}
```

- @Validated 는 검증기를 실행하라는 애노테이션
  - WebDataBinder 에 등록한 검증기를 찾아서 실행
  - bindingResult 에 검증 결과가 담기게 됨

```java
 @PostMapping("/add")
public String addItem(@Validated @ModelAttribute Item item, BindingResult bindingResult, RedirectAttributes redirectAttributes) {
```

commit
