---
layout: post
title: Spring MVC Part 1.
summary: 스프링 MVC 1편 - 백엔드 웹 개발 핵심 기술
categories: (Inflearn)Spring-MVC
featured-img: spring_mvc
# mathjax: true
---

# Spring MVC Part 1.

영한님의 [스프링 MVC 1편 - 백엔드 웹 개발 핵심 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-1/dashboard) 강의 노트

# Table Of Contents

- Web Application
  - Web Server / Web Application Server
  - Servlet
  - Multi Thread
- Servlet
- Servlet, JSP, MVC pattern
- MVC 프레임워크 만들기
- 스프링 MVC (구조 이해)
- 스프링 MVC (기본 기능)
- 스프링 MVC (웹 페이지 만들기)

# Web Application

## Web Server

- HTTP 기반으로 동작
- 정적 리소스(HTML, CSS, JS, Img, Video ..) 제공
- ex) NGINX, APACHE

## Web Application Server (WAS)

- HTTP 기반 동장
- Web server 기능 포함 + 정적 리소스
- Application Logic 수행
  - 동적 HTML, REST API, Servlet, JSP, Spring MVC
- ex) Tomcat, Undertow

## Web System

- Client -> Web Server -> WAS -> DB
  - WAS의 서버 과부하 문제 해결
  - Web Server 에서 정적 리소스 처리
  - WAS 에서는 Application Logic 동적 처리
  - 효율적인 리소스 관리 (필요에 따라 서버 증설)

## Servlet

**Servlet**

- urlPatterns의 URL이 호출되면 서블릿 코드 실행
- HttpServletRequest 로 HTTP 요청 정보를 편리하게 사용
- HttpServletResponse 로 HTTP 응답 정보를 편리하게 제공

**Servlet Container**

- Servlet 을 지원하는 WAS
- Servlet 객체를 생성/초기화/호출/종료하는 생명주기 관리
- Servlet 객체는 싱글톤으로 관리
- JSP 도 Servlet 으로 변환 되어 사용
- 동시 요청을 위한 **멀티 쓰레드 처리** 지원

## Multi Thread

**Thread**

- Application 코드를 하나하나 순차적으로 실행하는 것

**Thread pool**

- 필요한 Thread 를 Thread Pool 에 보관하고 관리
- Thread Pool 에 생성 가능한 Thread 의 최대치를 관리
  - Tomcat default : 최대 200개
- WAS 주요 튜닝 포인트는 `Max Thread`
  - 너무 낮을 경우 : 동시 요청이 많으면, 서버 리소스는 여유롭지만, 클리이언트는 응답 지연
  - 너무 높을 경우 : 동시 요청이 많으면, CPU, 메모리 리소스 임계점 초과로 서버 다운
  - 장애 발생 시 : 클라우드일 경우 서버를 늘린 후 튜닝, 아니면 그냥 빡튜닝..
- 개발자가 Multi Thread 관련 코드를 신경쓰지 않아도 됨 (Multi Thread 에 대한 부분은 WAS가 처리)
  - 단, Max Thread 튜닝이 중요
- 성능 테스트 Tool : <i>nGrinder</i>, Apache ab, JMeter
