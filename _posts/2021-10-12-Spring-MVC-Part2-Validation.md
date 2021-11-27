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

# Bean Validation

- 검증 로직을 모든 프로젝트에 적용할 수 있게 공통화하고, 표준화 한 것

- 특정한 구현체가 아니라 Bean Validation 2.0(JSR-380)이라는 기술 표준 (검증 애노테이션과 여러 인터페이스의 모음)

- 일반적으로 사용하는 구현체는 HIBERNATE Validator

**Reference**

> [HIBERNATE](http://hibernate.org/validator/)
>
> [HIBERNATE Validator](https://docs.jboss.org/hibernate/validator/6.2/reference/en-US/html_single/)
>
> [HIBERNATE Validator Annotations](https://docs.jboss.org/hibernate/validator/6.2/reference/en-US/html_single/#validator-defineconstraints-spec)

## Apply Spring

**Dependence**

```gradle
implementation 'org.springframework.boot:spring-boot-starter-validation'
```

- 자동으로 Bean Validator를 인지하고 스프링에 통합
- Spring Boot는 자동으로 LocalValidatorFactoryBean 을 글로벌 Validator로 등록
  - LocalValidatorFactoryBean 은 Annotation 기반 검증
- @Valid, @Validated 만 적용하여 검증 사용 가능
- 검증 오류 발생 시 FieldError, ObjectError 를 생성해서 BindingResult 에 담아 준다.

**Item.java**

```java
import lombok.Data;
import org.hibernate.validator.constraints.Range;

import javax.validation.constraints.Max;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Data
public class Item {

    private Long id;

    @NotBlank //빈값+공백 검증
    private String itemName;

    @NotNull
    @Range(min = 1000, max = 1000000)
    private Integer price;

    @NotNull
    @Max(9999)
    private Integer quantity;

    public Item() {
    }

    public Item(String itemName, Integer price, Integer quantity) {
        this.itemName = itemName;
        this.price = price;
        this.quantity = quantity;
    }
}

```

- 기존에 등록한 ItemValidator 제거

```java
@PostMapping("/add")
public String addItem(@Validated @ModelAttribute Item item, BindingResult bindingResult, RedirectAttributes redirectAttributes) {
    // ..
}
```

**검증 순서**

1/.@ModelAttribute 각각의 필드에 타입 변환 시도

- 성공하면 다음으로
- 실패하면 typeMismatch 로 FieldError 추가

2/.Validator 적용

- 바인딩에 성공한 필드만 Bean Validation 적용
- BeanValidator는 바인딩에 실패한 필드는 BeanValidation을 적용하지 않음

## 에러 코드

**@NotBlank**

- NotBlank.item.itemName
- NotBlank.itemName
- NotBlank.java.lang.String
- NotBlank

**@Range**

- Range.item.price
- Range.price
- Range.java.lang.Integer
- Range

```properties
NotBlank.item.itemName=상품 이름을 입력해주세요.
NotBlank={0} 공백X
Range={0}, {2} ~ {1} 허용
Max={0}, 최대 {1}
```

**BeanValidation 메시지 찾는 순서**

1. 생성된 메시지 코드 순서대로 messageSource 에서 메시지 찾기

2. 애노테이션의 message 속성 사용 @NotBlank(message = "공백! {0}")

3. 라이브러리가 제공하는 기본 값 사용 공백일 수 없습니다

## 오브젝트 오류

- `@ScriptAssert()` 사용은 제약이 많으므로 추천하지 않음.

```java
if (item.getPrice() != null && item.getQuantity() != null) {
    int resultPrice = item.getPrice() * item.getQuantity();
    if (resultPrice < 10000) {
        bindingResult.reject("totalPriceMin", new Object[]{10000, resultPrice}, null);
    }
}
```

## Form(add/edit) Validation 분리

### groups

- groups 기능은 실제 잘 사용되지는 않음
- 실무에서는 주로 등록용 폼 객체와 수정용 폼 객체를 분리해서 사용

**SaveCheck.java**

```java
public interface SaveCheck {
}
```

**UpdateCheck**

```java
public interface UpdateCheck {
}
```

**item.java**

```java
@Data
public class Item {

    @NotNull(groups = UpdateCheck.class)
    private Long id;

    @NotBlank(message = "{0} 공백은 입력할 수 없습니다.", groups = {SaveCheck.class, UpdateCheck.class}) //빈값+공백 검증
    private String itemName;

    @NotNull(groups = {SaveCheck.class, UpdateCheck.class})
    @Range(min = 1000, max = 1000000, groups = {SaveCheck.class, UpdateCheck.class})
    private Integer price;

    @NotNull(groups = {SaveCheck.class, UpdateCheck.class})
    @Max(value = 9999, groups = SaveCheck.class)
    private Integer quantity;

    public Item() {
    }

    public Item(String itemName, Integer price, Integer quantity) {
        this.itemName = itemName;
        this.price = price;
        this.quantity = quantity;
    }
}
```

**Controller.java**

- @Validated 에 validation interface 명시

```java
@PostMapping("/add")
public String addItem2(@Validated(SaveCheck.class) @ModelAttribute Item item, BindingResult bindingResult, RedirectAttributes redirectAttributes) {
  //...
}

@PostMapping("/{itemId}/edit")
public String edit2(@PathVariable Long itemId, @Validated(UpdateCheck.class) @ModelAttribute Item item, BindingResult bindingResult) {
  //...
}
```

## 실무 사용 방법

### Form 전송 객체 분리

- 수정의 경우 등록과 수정은 완전히 다른 데이터가 넘어온다.
- 따라서 Save/Update 별도의 객체로 데이터를 전달받는 것이 좋다.

**item.java**

```java
@Data
public class Item {
    private Long id;
    private String itemName;
    private Integer price;
    private Integer quantity;
}
```

**itemSaveForm.java**

```java
@Data
public class ItemSaveForm {

    @NotBlank(message = "{0} 공백은 입력할 수 없습니다.")
    private String itemName;

    @NotNull
    @Range(min = 1000, max = 1000000)
    private Integer price;

    @NotNull
    @Max(value = 9999)
    private Integer quantity;
}
```

**itemUpdateForm.java**

```java
@Data
public class ItemUpdateForm {

    @NotNull
    private Long id;

    @NotBlank(message = "{0} 공백은 입력할 수 없습니다.")
    private String itemName;

    @NotNull
    @Range(min = 1000, max = 1000000)
    private Integer price;

    //수정에서 수량은 자유로 변경 가능
    private Integer quantity;
}
```

- Form 객체를 Item 으로 변환

```java
Item item = new Item();
item.setItemName(form.getItemName());
item.setPrice(form.getPrice());
item.setQuantity(form.getQuantity());

Item savedItem = itemRepository.save(item);
```

[Validation Annotation Docs](https://docs.jboss.org/hibernate/validator/6.2/reference/en-US/html_single/#validator-defineconstraints-spec)
