---
layout: post
title: ETC
summary: Spring MVC Part 2. 메시지, 국제화, 스프링 타입 컨버터, 파일 업로드
categories: Spring-Conquest
featured-img: spring_mvc_2
# mathjax: true
---

# Spring MVC Part 2. ETC

영한님의 [스프링 MVC 2편 - 백엔드 웹 개발 활용 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-2/) 강의 노트

[Project](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2)

# 메시지, 국제화

`메시지 기능`: 다양한 메시지를 한 곳에서 관리하는 기능

messages.properteis

```groovy
item=상품
item.id=상품 ID
item.itemName=상품명
item.price=가격
item.quantity=수량
```

`국제화 기능`: 메시지 파일을 각 나라별로 별도로 관리하는 국제화 기능
- messages_en.properties 와 같이 파일명 마지막에 언어 정보 추가
- 찾을 수 있는 국제화 파일이 없으면 messages.properties 를 기본으로 사용

messages_en.propertis

```groovy
item=Item
item.id=Item ID
item.itemName=Item Name
item.price=price
item.quantity=quantity
```

messages_ko.propertis

```groovy
item=상품
item.id=상품 ID
item.itemName=상품명
item.price=가격
item.quantity=수량
```

## Spring Message Source

SpringBoot 는 MessageSource 를 자동으로 스프링 빈으로 등록
  - Spring 사용 시 구현체인 ResourceBundleMessageSource 를 빈으로 등록
    ```java
    @Bean
    public MessageSource messageSource() {
        ResourceBundleMessageSource messageSource = new ResourceBundleMessageSource();
        // messages 지정 시 messages.properties 파일을 읽어서 사용
        messageSource.setBasenames("messages", "errors");
        messageSource.setDefaultEncoding("utf-8");
        return messageSource;
    }
    ```

**SpringBoot Message Source 설정**

application.properties
```groovy
spring.messages.basename=messages,config.i18n.messages
```

- 스프링 부트 메시지 소스 기본 값: `spring.messages.basename=messages`
- MessageSource 를 스프링 빈 등록하지 않고, 스프링 부트 관련 설정을 하지 않으면 messages 라는 이름으로 기본 등록
- 따라서 messages.properties, messages_en.properties .. 파일만 등록하면 자동으로 인식
- 추가 옵션은 [Spring-Boot Docs](https://docs.spring.io/spring-boot/docs/current/reference/html/application-properties.html#application-properties) 참고

- `/resources/messages.properties` 경로에 Message 파일 저장

  ```properties
  hello=안녕
  hello.name=안녕 {0}
  ```

**Message Source 사용**

- SpringBoot 는 MessageSource 를 자동으로 Spring Bean 으로 등록하므로 바로 사용 가능
- MessageSource 는 message.properties 파일 정보를 가지고 있음

```java
@Autowired
MessageSource ms;

@Test
void helloMessage() {
    // locale 정보가 없으면 basename 에서 설정한 기본 이름 메시지 파일(messages.properties) 조회
    String result = ms.getMessage("hello", null, null);
    assertThat(result).isEqualTo("안녕");
}

@Test
void notFoundMessageCode() {
    // 메시지가 없는 경우 NoSuchMessageException 발생
    assertThatThrownBy(() -> ms.getMessage("no_code", null, null))
            .isInstanceOf(NoSuchMessageException.class);
}
@Test
void notFoundMessageCodeDefaultMessage() {
    // 메시지가 없어도 defaultMessage 를 사용하면 기본 메시지 반환
    String result = ms.getMessage("no_code", null, "기본 메시지", null);
    assertThat(result).isEqualTo("기본 메시지");
}

@Test
void argumentMessage() {
    // 메시지의 {0} 부분은 매개변수를 전달해서 치환
    String result = ms.getMessage("hello.name", new Object[]{"Aaron"}, null);
    assertThat(result).isEqualTo("안녕 Aaron");
}
```

**Message Source 국제화 사용**

- locale 정보 기반으로 국제화 파일 선택
- Locale 이 en_US 일 경우 messages_en_US ➜ messages_en ➜ messages(default) 순서 탐색

```java
@Test
void defaultLang() {
    // locale 정보가 없으므로 messages 사용
    assertThat(ms.getMessage("hello", null, null)).isEqualTo("안녕");
    // locale 정보가 있지만, message_ko 가 없으므로 messages 사용
    assertThat(ms.getMessage("hello", null, Locale.KOREA)).isEqualTo("안녕");
}

@Test
void enLang() {
    // locale 정보가 Locale.ENGLISH 이므로 messages_en 사용
    assertThat(ms.getMessage("hello", null, Locale.ENGLISH)).isEqualTo("hello");
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

- 웹 브라우저의 언어 설정 값이 변하면 요청시 Accept-Language 의 값이 변경되고, 이 정보를 Spring 은 Locale 로 인식해 자동으로 국제화 처리

- `LocaleResolver`
  - Spring 은 Locale 선택 방식을 변경할 수 있도록 LocaleResolver 인터페이스 제공
  - Spring Boot 는 언어 선택 시 기본적으로 Accept-Language 헤더값을 활용하는 AcceptHeaderLocaleResolver 사용
  - Locale 선택 방식을 변경하려면 LocaleResolver 구현체를 변경해서 쿠키나 세션 기반의 Locale 선택 기능 사용

# 스프링 타입 컨버터

## 소개

**스프링 타입 변환 적용 예**

- HTTP Query String 으로 전달되는 데이터는 모두 String Type 이지만, 스프링은 타입을 변환해 제공
- `@RequestParam`, `@ModelAttribute`, `@PathVariable`, `@Value`, `XML Spring Bean 정보 변환`, `View Rendering` ...
  ```java
  @GetMapping("/hello")
  public String hello(@RequestParam Integer data) {}

  //---

  @GetMapping("/hello")
  public String hello(@ModelAttribute UserData data) {}

  class UserData {
      Integer data;
  }

  //---

  @GetMapping("/users/{userId}")
  public String hello(@PathVariable("data") Integer data) {}

  //---

  @Value("${api.key}")
  private String key;
  ``` 

**컨버터 인터페이스**

- 스프링에 커스텀 타입 변환이 필요하면 타입 컨버터 인터페이스를 구현해서 등록해 보자.

```java
package org.springframework.core.convert.converter;

public interface Converter<S, T> {
    T convert(S source);
}
```

ex. 숫자를 문자로 변환하는 타입 컨버터

```java
public class IntegerToStringConverter implements Converter<Integer, String> {
    @Override
    public String convert(Integer source) {
        return String.valueOf(source);
    }
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

## 🌞View Template 에 Converter 적용

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
  - 변수 표현식 : `${...}`
  - 컨버전 서비스 적용 : `${{...}}`

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

- Converter 는 범용(객체 ➜ 객체)에 사용
- Formatter 는 문자(객체 ➜ 문자, 문자 ➜ 객체, 현지화)에 특화

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

`DefaultFormattingConversionService`

- `FormattingConversionService` 에 추가로 기본적인 통화, 숫자 관련 포맷터 제공
- `FormattingConversionService` 는 `ConversionService` 관련 기능을 상속받기 때문에 결과적으로 컨버터도 포맷터도 모두 등록 가능

- FormattingConversionServiceTest

- 스프링 부트는 `DefaultFormattingConversionService` 를 상속 받은 WebConversionService` 를 내부에서 사용

[Code](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/97990bebf3fcefc61b775b4fb8f24f08cdf48eb2)

## 🌞Spring 에 Formatter 적용

- 참고로, Converter 의 우선순위가 더 높다.

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addFormatters(FormatterRegistry registry) {
        registry.addFormatter(new MyNumberFormatter());
    }
}
```

### Spring 기본 Formatter

- 객체의 각 필드마다 다른 형식의 formatter을 지정하고 싶다면 annotation 기반 formatter 를 사용하자

  - `@NumberFormat` : 숫자 관련 형식
  - `@DateTimeFormat` : 날짜 관련 형식

  ```java
  @Data
  static class Form {
      @NumberFormat(pattern = "###,###")
      private Integer number;
      @DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss")
      private LocalDateTime localDateTime;
  }
  ```

  [Annotation-driven Formatting](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#format-CustomFormatAnnotations)

# 파일 업로드

## 전송 방식

**기본적인 HTML Form 전송 방식**

- `application/x-www-form-urlencoded`
- HTML Form
  ```html
  <form action="/save" method="post">
    <inpout type="text" name="username" />
    <inpout type="text" name="age" />
    <button type="submit">전송</button>
  </form>
  ```
- HTTP Message

  ```text
  HTTP/1.1 200 OK

  POST /save HTTP/1.1
  Host: localhost:8080
  Content-Type: application/x-www-form-urlencoded

  username=kim&age=20
  ```

**Form 내용과 여러 파일을 함께 전송하는 HTML Form 전송 방식**

- `multipart/form-data`
- HTML Form
  - form tag 에 enctype="multipart/form-data" 지정
  ```html
  <form action="/save" method="post" enctype="multipart/form-data">
    <inpout type="text" name="username" />
    <inpout type="text" name="age" />
    <inpout type="file" name="file1" />
    <button type="submit">전송</button>
  </form>
  ```
- HTTP Message

  - 각각의 전송 항목이 구분
  - Content-Disposition 라는 항목별 헤더와 부가 정보가 분리

  ```text
  HTTP/1.1 200 OK

  POST /save HTTP/1.1
  Host: localhost:8080
  Content-Type: multipart/form-data; boundary=----XXX
  Content-Length: 10457

  ----XXX
  Content-Disposition: form-data; name="username"

  Kim
  ----XXX
  Content-Disposition: form-data; name="age"

  20
  ----XXX
  Content-Disposition: form-data; name="file1"; filename="sample.jpg"
  Content-Type: image/png

  102941as9d86f7aa9807sd6fas987df6...
  ----XXX--
  ```

[HTTP 메시지 참고](https://developer.mozilla.org/ko/docs/Web/HTTP/Messages)

## 서블릿과 파일 업로드

**Multipart 관련 설정**

```properties
# HTTP 요청 메시지 확인
logging.level.org.apache.coyote.http11=debug

# 파일 업로드 경로 설정
file.dir=C:/Users/Aaron/file/

# 업로드 사이즈 제한 (사이즈 초과 시 SizeLimitExceededException 예외 발생)
# max-file-size : 파일 하나 사이즈 (default > 1MB)
# max-request-size : 여러 파일 요청의 경우 전체 사이즈 (default > 10MB)
spring.servlet.multipart.max-file-size=1MB
spring.servlet.multipart.max-request-size=10MB

# Multipart 데이처 처리 여부 (default > true)
spring.servlet.multipart.enabled=true
```

- multipart.enabled 옵션이 켜져 있다면, Spring `DispatcherServlet` 에서 `MultipartResolver` 실행
- multipart 요청인 경우 Servlet Container 가 전달하는 `HttpServletRequest` 를 `MultipartHttpServletRequest` 로 변환해서 반환
- Spring 이 제공하는 기본 `MultipartResolver` 는 `MultipartHttpServletRequest` Interface 를 구현한
  `StandardMultipartHttpServletRequest` 를 반환

**ServletUploadController.java**

```java
@Slf4j
@Controller
@RequestMapping("/servlet/")
public class ServletUploadControllerV2 {

    /**
     * properties 설정 값 주입
     */
    @Value("${file.dir}")
    private String fileDir;

    @GetMapping("/upload")
    public String newFile() {
        return "upload-form";
    }

    @PostMapping("/upload")
    public String saveFile(HttpServletRequest request) throws ServletException, IOException {
        log.info("request={}", request);

        String itemName = request.getParameter("itemName");
        log.info("itemName={}", itemName);

        /**
         * Multipart 형식은 전송 데이터를 각 Part 로 나누어 전송
         */
        Collection<Part> parts = request.getParts();
        log.info("parts={}", parts);

        for (Part part : parts) {
            log.info("==== PART ====");
            log.info("name={}", part.getName());
            Collection<String> headerNames = part.getHeaderNames();
            for (String headerName : headerNames) {
                log.info("header {}: {}", headerName, part.getHeader(headerName));
            }

            /*
             *편의 메서드
             */
            //Content-Disposition: form-data; name="file"; filename="image.png"
            //Content-Type: image/png
            log.info("submittedFileName={}", part.getSubmittedFileName()); // 클라이언트가 전달한 파일명
            log.info("size={}", part.getSize()); //part body size

            //데이터 읽기
            InputStream inputStream = part.getInputStream(); // Part의 전송 데이터 읽기
            String body = StreamUtils.copyToString(inputStream, StandardCharsets.UTF_8);
            log.info("body={}", body);

            //파일에 저장하기
            if (StringUtils.hasText(part.getSubmittedFileName())) {
                String fullPath = fileDir + part.getSubmittedFileName();
                log.info("파일 저장 fullPath={}", fullPath);
                part.write(fullPath); // Part를 통해 전송된 데이터를 저장
            }
        }

        return "upload-form";
    }
}
```

```text
request=org.springframework.web.multipart.support.StandardMultipartHttpServletRequest@2b82974a
itemName=Spring
parts=[org.apache.catalina.core.ApplicationPart@367a8c9f, org.apache.catalina.core.ApplicationPart@33180a33]
==== PART ====
name=itemName
header content-disposition: form-data; name="itemName"
submittedFileName=null
size=6
body=Spring
==== PART ====
name=file
header content-disposition: form-data; name="file"; filename="image.png"
header content-type: image/png
submittedFileName=image.png
size=191492
body=�PNG
...
...
```

## 🌞스프링과 파일 업로드

- 스프링은 `MultipartFile` Interface 로 Multipart File 을 매우 편리하게 지원

```java
@PostMapping("/upload")
public String saveFile(@RequestParam String itemName,
                        @RequestParam MultipartFile file, HttpServletRequest request) throws IOException {

    if (!file.isEmpty()) {
        String fullPath = fileDir + file.getOriginalFilename(); //업로드 파일 명
        log.info("파일 저장 fullPath={}", fullPath);
        file.transferTo(new File(fullPath)); //파일 저장
    }

    return "upload-form";
}
```

### 파일 업로드, 다운로드 구현

[예제로 구현하는 파일 업로드, 다운로드 (1)](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/8b208405d5104f87e0e055bc163408cc96937d3e)

[예제로 구현하는 파일 업로드, 다운로드 (2)](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/c20895f7e420339dd0e7fc6ae528d2c0c243bdd4)


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