---
layout: post
title: Validation
summary: Spring MVC Part 2. 백엔드 웹 개발 활용 기술
categories: Spring-Conquest
featured-img: spring_mvc_2
# mathjax: true
---

# Spring MVC Part 2. Validation

영한님의 [스프링 MVC 2편 - 백엔드 웹 개발 활용 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-2/) 강의 노트

[Project](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2)

# Spring Verification

컨트롤러의 중요한 역할중 하나는 HTTP 요청이 정상인지 검증하는 것
- 클라이언트 검증은 조작할 수 있으므로 보안에 취약
- 그렇다고 서버만으로 검증하면 즉각적인 고객 사용성이 부족
- 서버, 클라이언트 검증을 적절히 섞어서 사용하되 서버 검증은 필수
- API 방식 사용 시, API 스펙을 잘 정의해서 검증 오류를 API 응답 결과에 잘 남겨야 함

# BindingResult

스프링이 제공하는 검증 오류를 보관하는 객체

```java
@PostMapping("/add")
public String addItemV2(@ModelAttribute Item item, 
                        BindingResult bindingResult, 
                        RedirectAttributes redirectAttributes, 
                        Model model) {

    if (!StringUtils.hasText(item.getItemName())) {
        bindingResult.addError(new FieldError("item", "itemName", item.getItemName(), false, null, null, "상품 이름은 필수 입니다."));
    }
    
    if (item.getPrice() == null || item.getPrice() < 1000 || item.getPrice() > 1000000) {
        bindingResult.addError(new FieldError("item", "price", item.getPrice(), false, null, null, "가격은 1,000 ~ 1,000,000 까지 허용합니다."));
    }
    
    if (item.getQuantity() == null || item.getQuantity() >= 9999) {
        bindingResult.addError(new FieldError("item", "quantity", item.getQuantity(), false, null ,null, "수량은 최대 9,999 까지 허용합니다."));
    }

    // 글로벌 예외
    if (item.getPrice() != null && item.getQuantity() != null) {
        int resultPrice = item.getPrice() * item.getQuantity();
        if (resultPrice < 10000) {
            bindingResult.addError(new ObjectError("item",null ,null, "가격 * 수량의 합은 10,000원 이상이어야 합니다. 현재 값 = " + resultPrice));
        }
    }

    // 검증 실패 시 입력 폼으로
    if (bindingResult.hasErrors()) {
        log.info("errors={} ", bindingResult);
        return "validation/v2/addForm";
    }

    Item savedItem = itemRepository.save(item);
    redirectAttributes.addAttribute("itemId", savedItem.getId());
    redirectAttributes.addAttribute("status", true);
    return "redirect:/validation/v2/items/{itemId}";
}

...

/** 
 * FieldError class
 * 필드에 오류가 있으면 FieldError 객체를 생성해서 bindingResult 에 담아두자.
 */
public FieldError(
  String objectName, // @ModelAttribute 이름
  String field, // 오류가 발생한 필드 이름
  String defaultMessage // 오류 기본 메시지 
) {}

public FieldError(
  String objectName, // 오류가 발생한 객체 이름
  String field, // 오류 필드
  @Nullable Object rejectedValue, // 사용자가 입력한 값(거절된 값)
  boolean bindingFailure, // 타입 오류 같은 바인딩 실패인지, 검증 실패인지 구분 값
  @Nullable String[] codes, // 메시지 코드
  @Nullable Object[] arguments, // 메시지에서 사용하는 인자
  @Nullable String defaultMessage // 기본 오류 메시지
)

/**
 * ObjectError
 * 특정 필드를 넘어서는 오류가 있으면 ObjectError 객체를 생성해서 bindingResult 에 담아두자.
 */
public ObjectError(
  String objectName, // @ModelAttribute 의 이름
  String defaultMessage // 오류 기본 메시지
) {}
```

`BindingResult`

- @ModelAttribute 객체 다음 위치
- BindingResult 가 있으면 @ModelAttribute 에 데이터 바인딩 시 오류가 발생해도 컨트롤러 호출
  - BindingResult 가 없으면 400 오류 발생 후, 오류 페이지로 이동
  - BindingResult 가 있으면 오류 정보(FieldError)를 BindingResult 에 담아서 컨트롤러 정상 호출
- Model 에 자동으로 포함
- 어떤 객체를 대상으로 검증하는지 타겟을 알고 있음

.

BindingResult 에 검증 오류를 적용하는 세 가지 방법
- @ModelAttribute 객체의 타입 오류 등, 바인딩 실패 시 스프링이 FieldError 생성 후 BindingResult 에 삽입
- 개발자가 직접 입력
- Validator 사용

## Error Message

오류 메시지 파일을 인식할 수 있도록 설정 추가

```groovy
spring.messages.basename=messages,errors
```

errors.properties

```groovy
required.item.itemName=상품 이름은 필수입니다.
range.item.price=가격은 {0} ~ {1} 까지 허용합니다.
max.item.quantity=수량은 최대 {0} 까지 허용합니다.
totalPriceMin=가격 * 수량의 합은 {0}원 이상이어야 합니다. 현재 값 = {1}
required.default=기본 오류 메시지
required=필수 값 입니다.
```

```java
bindingResult.addError(
  new FieldError("item", "itemName", item.getItemName(), false, 
  new String[]{"required.item.itemName"}, null, null)
);

bindingResult.addError(
    new FieldError("item", "price", item.getPrice(), false, 
    new String[]{"range.item.price"}, // codes : 메시지 코드
    new Object[]{1000, 1000000}, // arguments : 메시지에서 사용하는 인자
    null)
);
```

**`rejectValue()` , `reject()`**

BindingResult 는 검증해야 target 객체를 알고 있음
- BindingResult 의 `rejectValue()`, `reject()` 를 사용하면 FieldError, ObjectError 를 직접 생성하지 않고, 깔끔하게 검증 오류를 다룰 수 있음

```java
bindingResult.rejectValue("itemName", "required");

bindingResult.rejectValue("price", "range", new Object[]{1000, 10000000}, "상품 가격 오류");

bindingResult.reject("totalPriceMin", new Object[]{10000, resultPrice}, null);
...

void rejectValue(
  @Nullable String field, // 오류 필드명
  String errorCode, // 오류 코드(메시지에 등록된 코드가 아닌 messageResolver 를 위한 오류 코드)
  @Nullable Object[] errorArgs, // 메시지에서 사용하는 인자
  @Nullable String defaultMessage // 기본 메시지(오류 메시지를 찾을 수 없을 때 사용)
);

void reject(
  String errorCode, 
  @Nullable Object[] errorArgs,
  @Nullable String defaultMessage
);
```

### Apply Thymeleaf

**필드 오류 처리**

- `rejectedValue()`: 오류 발생 시 사용자 입력 값을 저장

```java
bindingResult.rejectValue("price", "range", new Object[]{1000, 10000000}, "상품 가격 오류");
```

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

- `th:field`는 평소에는 모델 객체의 값을 사용하지만, 오류가 발생하면 FieldError 에서 보관한 값을 사용해서 값을 출력

**글로벌 오류 처리**

```java
bindingResult.reject("totalPriceMin", new Object[]{10000, resultPrice}, null);
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


## MessageCodesResolver

- 검증 오류 코드로 메시지 코드들을 생성
- `MessageCodesResolver` 는 인터페이스, `DefaultMessageCodesResolver` 는 기본 구현체
- `ObjectError`, `FieldError` 와 주로 함께 사용

**DefaultMessageCodesResolver 기본 메시지 생성 규칙**

필드 오류

```text
필드 오류의 경우 다음 순서로 4가지 메시지 코드 생성

1. code + "." + ObjectName + "." + field
2. code + "." + field
3. code + "." + field type
4. code

---

(example)
error code: required
ObjectName: item
field: itemName
field type: String

1. "required.item.itemName"
2. "required.itemName"
3. "required.java.lang.String"
4. "required"

```

객체 오류

```text
객체 오류의 경우 다음 순서로 2가지 생성

1. code + "." + objectName
2. code

---

(example)
error code: totalPriceMin
ObjectName: item

1. "totalPriceMin.item"
2. "totalPriceMin"
```

**동작 방식**
- `rejectValue()` , `reject()` 는 내부에서 `MessageCodesResolver` 사용 ➜ 여기서 메시지 코드 생성
  - FieldError, ObjectError 생성자를 보면 알 수 있듯이, 여러 오류 코드를 가질 수 있음
- `MessageCodesResolver` 를 통해 생성된 순서대로 오류 코드 보관

```text
1. rejectValue() 호출
2. MessageCodesResolver 를 사용해서 검증 오류 코드로 메시지 코드들을 생성
3. new FieldError() 를 생성하면서 메시지 코드들을 보관
4. th:erros 에서 메시지 코드들로 메시지를 순서대로 메시지에서 찾고 출력
```

## 오류 코드 관리 전략

**구체적인 것 ➜ 덜 구체적인 것으로가 핵심**

- MessageCodesResolver 는 구체적인 것(required.item.itemName)을 먼저 생성하고, 덜 구체적인 것(required)을 나중애 생성
- 중요하지 않은 메시지는 범용성 있는 간단한 메시지(requried)로, 중요한 메시지는 필요할 때 구체적으로 사용하는 방식이 효과적

errors.properties
```groovy
#==ObjectError==
#Level1
totalPriceMin.item=상품의 가격 * 수량의 합은 {0}원 이상이어야 합니다. 현재 값 = {1}

#Level2 - 생략
totalPriceMin=전체 가격은 {0}원 이상이어야 합니다. 현재 값 = {1}



#==FieldError==
#Level1
required.item.itemName=상품 이름은 필수입니다.
range.item.price=가격은 {0} ~ {1} 까지 허용합니다.
max.item.quantity=수량은 최대 {0} 까지 허용합니다.

#Level2 - 생략

#Level3
required.java.lang.String = 필수 문자입니다.
required.java.lang.Integer = 필수 숫자입니다.
min.java.lang.String = {0} 이상의 문자를 입력해주세요.
min.java.lang.Integer = {0} 이상의 숫자를 입력해주세요.
range.java.lang.String = {0} ~ {1} 까지의 문자를 입력해주세요.
range.java.lang.Integer = {0} ~ {1} 까지의 숫자를 입력해주세요.
max.java.lang.String = {0} 까지의 숫자를 허용합니다.
max.java.lang.Integer = {0} 까지의 숫자를 허용합니다.

#Level4
required = 필수 값 입니다.
min= {0} 이상이어야 합니다.
range= {0} ~ {1} 범위를 허용합니다.
max= {0} 까지 허용합니다.
```

### ValidationUtils

**ValidationUtils 사용 전**

```java
if (!StringUtils.hasText(item.getItemName())) {
    bindingResult.rejectValue("itemName", "required", "기본: 상품 이름은 필수입니다.");
}
```

**ValidationUtils 사용 후**

```java
ValidationUtils.rejectIfEmptyOrWhitespace(bindingResult, "itemName", "required");
```

## Spring 자체 검증 오류 메시지 처리

- 주로 타입 정보가 맞지 않을 경우 Spring 직접 검증
- Spring은 타입 오류가 발생하면 typeMismatch 오류 코드를 사용
- `typeMismatch` 오류 코드가 `MessageCodesResolver` 를 통해 4가지 메시지 코드로 생성
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

## 🌞 실무 사용 방법

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

### HTTP Message Converter

- `@Valid`, `@Validated` 는 HttpMessageConverter(@RequestBody)에도 적용 가능

> `@ModelAttribute` 는 HTTP 요청 파라미터(URL 쿼리 스트링, POST Form)를 다룰 때 사용
>
> `@RequestBody` 는 HTTP Body의 데이터를 객체로 변환할 때 사용 (주로 API JSON 요청)

```java
@Slf4j
@RestController
@RequestMapping("/validation/api/items")
public class ValidationItemApiController {

    @PostMapping("/add")
    public Object addItem(@RequestBody @Validated ItemSaveForm form, BindingResult bindingResult) {

        log.info("API 컨트롤러 호출");

        if (bindingResult.hasErrors()) {
            log.info("검증 오류 발생 errors={}", bindingResult);
            return bindingResult.getAllErrors();
        }

        log.info("성공 로직 실행");
        return form;
    }
}
```

**API 응답 결과**

1.성공 요청: 성공

2.실패 요청: JSON을 객체로 생성하는 것 자체가 실패

3.검증 오류 요청: JSON을 객체로 생성하는 것은 성공, 검증에서 실패

- 필요한 데이터만 뽑아 별도 API 스펙을 정의하고 객체를 만들어서 반환

**@ModelAttribute vs @RequestBody**

- `@ModelAttribute` 는 필드 단위로 정교하게 바인딩이 적용
  - 특정 필드가 바인딩 되지 않아도 나머지 필드는 정상 바인딩되고, Validator를 사용한 검증도 적용 가능
- `@RequestBody` 는 HttpMessageConverter 단계에서 JSON 데이터를 객체로 변경
  - 객체로 변경하지 못하면 이후 단계 자체가 진행되지 않고 예외 발생. 컨트롤러도 호출되지 않고, Validator도 적용 불가능



최종 코드 추가...

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