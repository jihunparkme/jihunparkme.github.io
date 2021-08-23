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
