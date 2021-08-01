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

# Servlet

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

# Servlet
