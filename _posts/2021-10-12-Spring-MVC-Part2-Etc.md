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
