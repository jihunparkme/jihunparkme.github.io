---
layout: post
title: Spring MVC Part 2. ETC
summary: (MVC) 스프링 MVC 2편 - 백엔드 웹 개발 활용 기술
categories: (Inflearn)Spring-MVC-2
featured-img: spring_mvc_2
# mathjax: true
---

# Spring MVC Part 2. ETC

영한님의 [스프링 MVC 2편 - 백엔드 웹 개발 활용 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-2/) 강의 노트

# Table Of Contents

- 메시지, 국제화
- 예외 처리와 오류 페이지
- API 예외 처리
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
