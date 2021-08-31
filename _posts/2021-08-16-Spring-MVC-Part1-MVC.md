---
layout: post
title: Spring MVC Part 1. MVC
summary: (MVC) 스프링 MVC 1편 - 백엔드 웹 개발 핵심 기술
categories: (Inflearn)Spring-MVC
featured-img: spring_mvc
# mathjax: true
---

# Spring MVC Part 1. MVC

영한님의 [스프링 MVC 1편 - 백엔드 웹 개발 핵심 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-1/dashboard) 강의 노트

# Table Of Contents

- 스프링 MVC (구조 이해)
- 스프링 MVC (기본 기능)
- 스프링 MVC (웹 페이지 만들기)

# Spring MVC Framework

## 스프링 MVC 전체 구조

![Result](https://raw.githubusercontent.com/jihunparkme/jihunparkme.github.io/master/post_img/spring_mvc.png 'Result')

1. 핸들러 조회 : 핸들러 매핑을 통해 요청 URL에 매핑된 핸들러(컨트롤러)를 조회

2. 핸들러 어댑터 조회 : 핸들러를 실행할 수 있는 핸들러 어댑터를 조회

3. 핸들러 어댑터 실행 : 핸들러 어댑터를 실행

4. 핸들러 실행 : 핸들러 어댑터가 실제 핸들러를 실행

5. ModelAndView 반환 : 핸들러 어댑터는 핸들러가 반환하는 정보를 ModelAndView로 변환해서 반환

6. viewResolver 호출 : viewResolver를 찾고 실행 (JSP의 경우 InternalResourceViewResolver 가 자동 등록&사용)

7. View 반환 : viewResolver는 뷰의 논리 이름을 물리 이름으로 바꾸고, 렌더링 역할을 담당하는 뷰 객체 반환 (JSP의 경우 InternalResourceView(JstlView) 를 반환하는데, 내부에 forward() 로직 존재)

8. 뷰 렌더링 : 뷰를 통해서 뷰를 렌더링

**주요 인터페이스**

`HandlerMapping`, `HandlerAdapter`, `ViewResolver`, `View`

## HandlerMapping & HandlerAdapter

**컨트롤러 호출 과정**

(1) 핸들러 매핑으로 핸들러 조회

- HandlerMapping 을 순서대로 실행해서, 핸들러 찾기

  - RequestMappingHandlerMapping : 애노테이션 기반의 컨트롤러인 @RequestMapping에서
    사용
  - BeanNameUrlHandlerMapping : 스프링 빈의 이름으로 핸들러를 찾는다.

- 빈 이름으로 핸들러를 찾을 경우, 빈 이름으로 핸들러를 찾아주는 BeanNameUrlHandlerMapping 가 실행에 성공하고 핸들러인 Controller 를 반환

(2) 핸들러 어댑터 조회

- HandlerAdapter 의 supports() 를 순서대로 호출

  - RequestMappingHandlerAdapter : 애노테이션 기반의 컨트롤러인 @RequestMapping에서사용

  - HttpRequestHandlerAdapter : HttpRequestHandler 처리

  - SimpleControllerHandlerAdapter : Controller 인터페이스 (애노테이션X, 과거에 사용) 처리

- SimpleControllerHandlerAdapter 가 Controller 인터페이스를 지원하므로 대상이 된다.

(3) 핸들러 어댑터 실행

- 디스패처 서블릿이 조회한 SimpleControllerHandlerAdapter 를 실행하면서 핸들러 정보도 함께 넘겨준다.

- SimpleControllerHandlerAdapter 는 핸들러인 Controller 를 내부에서 실행하고, 그 결과를 반환

## ViewResolver

**ViewResolver 호출 과정**

(1) 핸들러 어댑터 호출

- 핸들러 어댑터를 통해 논리 뷰 이름을 획득

(2) ViewResolver 호출

- 논리 뷰 이름으로 viewResolver를 순서대로 호출

  - BeanNameViewResolver : 빈 이름으로 뷰를 찾아서 반환
  - InternalResourceViewResolver : JSP를 처리할 수 있는 뷰를 반환

- 논리 뷰 이름의 스프링 빈으로 등록된 뷰가 없다면 InternalResourceViewResolver 가 호출

(3)InternalResourceViewResolver

- InternalResourceView 를 반환

(4) 뷰 - InternalResourceView

- InternalResourceView 는 JSP처럼 포워드 forward() 를 호출해서 처리할 수 있는 경우에 사용

(5) view.render()
view.render() 가 호출되고 InternalResourceView 는 forward() 를 사용해서 JSP를 실행

# Spring MVC 기본 기능

**프로젝트**

- Jar 사용 시 항상 내장 서버(tomcat..)를 사용 (내장 서버 최적화)

- War 사용 시 주로 외부 서버에 배포하는 목적으로 사용

## Logging

- SpringBoot 가 기본으로 제공하는 Logback
  을 대부분 사용

  - SLF4J interface 의 구현체인 Logback

- 로그 선언

  ```java
  private Logger log = LoggerFactory.getLogger(getClass());
  // OR
  private static final Logger log = LoggerFactory.getLogger(Xxx.class)
  ```

- 로그 호출

  ```java
  log.info("hello")
  ```
