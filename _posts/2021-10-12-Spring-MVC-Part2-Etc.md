---
layout: post
title: ETC
summary: Spring MVC Part 2. 메시지, 국제화, 스프링 타입 컨버터, 파일 업로드
categories: (Inflearn)Spring-MVC-2
featured-img: spring_mvc_2
# mathjax: true
---

# Spring MVC Part 2. ETC

영한님의 [스프링 MVC 2편 - 백엔드 웹 개발 활용 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-2/) 강의 노트

[Project](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2)

# Table Of Contents

- 메시지, 국제화
- 스프링 타입 컨버터
- 파일 업로드

# 메시지, 국제화

## Spring Message Source

- SpringBoot는 MessageSource 를 자동으로 스프링 빈으로 등록

**Message Source 설정 (default: messages)**

- `application.properties`
  ```properties
  spring.messages.basename=messages,config.i18n.messages
  ```
- 추가 옵션은 [Docs](https://docs.spring.io/spring-boot/docs/current/reference/html/application-properties.html#application-properties) 참고

- `/resources/messages.properties` 경로에 Message 파일 저장

  ```properties
  hello=안녕
  hello.name=안녕 {0}
  ```

**Message Source 사용**

- SpringBoot는 MessageSource 를 자동으로 Spring Bean 으로 등록하므로 바로 사용 가능
- MessageSource는 message.properties 파일 정보를 가지고 있음

  ```java
  @Autowired
  MessageSource ms;

  @Test
  void helloMessage() {
    String result = ms.getMessage("hello", null, null);
    assertThat(result).isEqualTo("안녕");
  }
  ```

- 메시지가 없을 경우

  ```java
  @Test
  void notFoundMessageCode() {
    assertThatThrownBy(() -> ms.getMessage("no_code", null, null))
                .isInstanceOf(NoSuchMessageException.class);
  }
  ```

- 메시지가 없을 경우 기본 메시지로 대체

  ```java
  @Test
  void notFoundMessageCodeDefaultMessage() {
    String result = ms.getMessage("no_code", null, "기본 메시지", null);
    assertThat(result).isEqualTo("기본 메시지");
  }
  ```

- 매개변수 사용

  ```java
  @Test
  void argumentMessage() {
    String result = ms.getMessage("hello.name", new Object[]{"Spring"}, null);
    assertThat(result).isEqualTo("안녕 Spring");
  }
  ```

- 국제화
  ```java
  @Test
  void Lang() {
      assertThat(ms.getMessage("hello", null, null)).isEqualTo("안녕");
      assertThat(ms.getMessage("hello", null, Locale.KOREA)).isEqualTo("안녕"); // _ko 가 없으므로 default
      assertThat(ms.getMessage("hello", null, Locale.ENGLISH)).isEqualTo("hello"); // _en 메시지 파일 선
  }
  ```

## Web Application Message

**메시지 적용**

- 타임리프의 메시지 표현식 `#{...}` 를 사용하면 스프링 메시지를 편리하게 조회 가능

  - messages.properties
    ```properties
    label.item=상품
    hello.name=안녕 {0}
    ```
  - Thymeleaf
    ```html
    <div th:text="#{label.item}"></h2>
    <p th:text="#{hello.name(${item.itemName})}"></p>
    ```

**국제화 적용**

- 웹 브라우저의 언어 설정 값이 변하면 요청시 Accept-Language 의 값이 변경되고, 이 정보를 Spring은 Locale로 인식해 자동으로 국제화 처리를 해준다.

- `LocaleResolver`

  - Spring은 Locale 선택 방식을 변경할 수 있도록 LocaleResolver 인터페이스를 제공

  - Spring Boot는 언어 선택 시 기본적으로 Accept-Language 헤더값을 활용하는 AcceptHeaderLocaleResolver를 사용

  - Locale 선택 방식을 변경하려면 LocaleResolver 의 구현체를 변경해서 쿠키나 세션 기반의 Locale 선택 기능 사용

# 스프링 타입 컨버터

## 소개

**스프링 타입 변환 적용 예**

- HTTP Query String 으로 전달되는 데이터는 모두 String Type 이지만, 스프링은 타입을 변환해 제공

  - `@RequestParam`

    ```java
    @GetMapping("/hello")
    public String hello(@RequestParam Integer data) {}
    ```

  - `@ModelAttribute`

    ```java
    @GetMapping("/hello")
    public String hello(@ModelAttribute UserData data) {}

    class UserData {
        Integer data;
    }
    ```

  - `@PathVariable`

    ```java
    @GetMapping("/users/{userId}")
    public String hello(@PathVariable("data") Integer data) {}
    ```

- YML 정보 읽기

  - `@value`

    ```java
    @Value("${api.key}")
    private String key;
    ```

- XML 스프링 빈 정보 변환

- View Rendering

**컨버터 인터페이스**

- 스프링은 확장 가능한 컨버터 인터페이스를 제공

```java
package org.springframework.core.convert.converter;

public interface Converter<S, T> {
    T convert(S source);
}
```

## Type Converter

[Spring Type Conversion](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#core-convert)

- 스프링은 용도에 따라 다양한 방식의 타입 컨버터 제공
  - Converter : 기본 타입 컨버터
  - ConverterFactory : 전체 클래스 계층 구조가 필요할 경우
  - GenericConverter : 정교한 구현, 대상 필드의 애노테이션 정보 사용 가능
  - ConditionalGenericConverter : 특정 조건이 참인 경우에만 실행

### IpPort Converter

**IpPort.java**

```java
@Getter
@EqualsAndHashCode //-> 참조값이 아닌 데이터만 비교
public class IpPort {
    private String ip;
    private int port;

    public IpPort(String ip, int port) {
        this.ip = ip;
        this.port = port;
    }
}
```

**StringToIntegerConverter.java**

```java
public class StringToIntegerConverter implements Converter<String, Integer> {
    @Override
    public Integer convert(String source) {
        return Integer.valueOf(source);
    }
}
```

**StringToIpPortConverter.java**

```java
public class StringToIpPortConverter implements Converter<String, IpPort> {
    @Override
    public IpPort convert(String source) {
        String[] split = source.split(":");
        String ip = split[0];
        int port = Integer.parseInt(split[1]);
        return new IpPort(ip, port);
    }
}
```

## ConversionService

**ConversionService.interface**

- Converting 가능 여부와 기능 제공

```java
package org.springframework.core.convert;

import org.springframework.lang.Nullable;

public interface ConversionService {

	boolean canConvert(@Nullable Class<?> sourceType, Class<?> targetType);

    boolean canConvert(@Nullable TypeDescriptor sourceType, TypeDescriptor targetType);

	@Nullable
	<T> T convert(@Nullable Object source, Class<T> targetType);

	@Nullable
	Object convert(@Nullable Object source, @Nullable TypeDescriptor sourceType, TypeDescriptor targetType);

}
```

**ConversionServiceTest.java**

- 실제 사용 시에는 Converter 등록과 사용을 분리
- DefaultConversionService 는 사용 초점의 ConversionService 와 등록 초점의 ConverterRegistry 로 분리되어 구현 (ISP-Interface Segregation Principal 적용)

```java
@Test
void conversionService() {
    // DefaultConversionService 를 통해 Converter "등록"
    DefaultConversionService conversionService = new DefaultConversionService();
    conversionService.addConverter(new StringToIntegerConverter());
    conversionService.addConverter(new IntegerToStringConverter());
    conversionService.addConverter(new StringToIpPortConverter());
    conversionService.addConverter(new IpPortToStringConverter());

    //convert(데이터, 반환 타입) 으로 "사용"
    assertThat(conversionService.convert("10", Integer.class)).isEqualTo(10);
    assertThat(conversionService.convert(10, String.class)).isEqualTo("10");

    IpPort ipPort = conversionService.convert("127.0.0.1:8080", IpPort.class);
    assertThat(ipPort).isEqualTo(new IpPort("127.0.0.1", 8080));

    String ipPortString = conversionService.convert(new IpPort("127.0.0.1", 8080), String.class);
    assertThat(ipPortString).isEqualTo("127.0.0.1:8080");
}
```

## 🌞Spring 에 Converter 적용

- 스프링은 내부에서 ConversionService 를 제공

**WebConfig.java**

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addFormatters(FormatterRegistry registry) {
        registry.addConverter(new StringToIpPortConverter());
        registry.addConverter(new IpPortToStringConverter());
    }
}
```

**Controller**

```java
@GetMapping("/ip-port")
public String ipPort(@RequestParam IpPort ipPort) {
    return "ok";
}
```

## 뷰 템플릿에 컨버터 적용

`Thymeleaf 는 렌더링 시에 컨버터를 적용`

**View**

- ConverterController.java

```java
@GetMapping("/converter-view")
public String converterView(Model model) {
    model.addAttribute("number", 10000);
    model.addAttribute("ipPort", new IpPort("127.0.0.1", 8080));
    return "converter-view";
}
```

- converter-view.html
  - 변수 표현식 : ${...}
  - 컨버전 서비스 적용 : ${{...}}

```html
<li>${ipPort}: <span th:text="${ipPort}"></span></li>
<li>${{ipPort}}: <span th:text="${{ipPort}}"></span></li>
```

**Form**

- ConverterController.java
  - @ModelAttribute 내부에서 ConversionService 동작

```java
@GetMapping("/converter/edit")
public String converterForm(Model model) {
    IpPort ipPort = new IpPort("127.0.0.1", 8080);
    Form form = new Form(ipPort);
    model.addAttribute("form", form);
    return "converter-form";
}

@PostMapping("/converter/edit")
public String converterEdit(@ModelAttribute Form form, Model model) {
    IpPort ipPort = form.getIpPort();
    model.addAttribute("ipPort", ipPort);
    return "converter-view";
}
```

- converter-view.html
  - th:field 는 Converter 까지 자동 적용
  - th:value 는 보여주는 용도

```html
<form th:object="${form}" th:method="post">
  th:field <input type="text" th:field="*{ipPort}" /><br />
  th:value <input type="text" th:value="*{ipPort}" /><br />
  <input type="submit" />
</form>
```

## Formatter

`객체를 특정한 포멧에 맞추어 문자로 출력하거나, 그 반대의 역할을 하는 것에 특화된 기능`

[Spring Field Formatting](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#format)

- Converter 는 범용(객체->객체)에 사용
- Formatter 는 문자(객체->문자, 문자->객체, 현지화)에 특화

**Formatter Interface**

```java
public interface Printer<T> { // 객체 -> 문자
  String print(T object, Locale locale);
}

public interface Parser<T> { // 문자 -> 객체
  T parse(String text, Locale locale) throws ParseException;
}

public interface Formatter<T> extends Printer<T>, Parser<T> {}
```

- MyNumberFormatter.java

```java
@Slf4j
public class MyNumberFormatter implements Formatter<Number> {

    @Override
    public Number parse(String text, Locale locale) throws ParseException {
        log.info("text={}, locale={}", text, locale);
        NumberFormat format = NumberFormat.getInstance(locale);
        return format.parse(text);
    }

    @Override
    public String print(Number object, Locale locale) {
        log.info("object={}, locale={}", object, locale);
        return NumberFormat.getInstance(locale).format(object);
    }
}
```

- MyNumberFormatterTest.java

```java
class MyNumberFormatterTest {

    MyNumberFormatter formatter = new MyNumberFormatter();

    @Test
    void parse() throws ParseException {
        Number result = formatter.parse("1,000", Locale.KOREA);
        assertThat(result).isEqualTo(1000L);
    }

    @Test
    void print() {
        String result = formatter.print(1000, Locale.KOREA);
        assertThat(result).isEqualTo("1,000");
    }
}
```
