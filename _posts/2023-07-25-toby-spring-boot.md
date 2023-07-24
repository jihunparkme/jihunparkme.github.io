---
layout: post
title: Toby Spring Boot
summary: 토비의 스프링 부트 이해와 원리
categories: Spring-Conquest
featured-img: toby-spring-boot
# mathjax: true
---

# Spring Boot

[Spring Boot Documentation](https://spring.io/projects/spring-boot)

> 스프링 부트는 **스프링 기반**으로 실무 환경에 사용 가능한 수준의 **독립실행형 애플리케이션**을 
> 
> 복잡한 고민 없이 빠르게 작성할 수 있게 도와주는 여러가지 `도구의 모음`

**특징**

- 독립형 스프링 애플리케이션 생성
- Tomcat, Jetty, Undertow 등을 포함(WAR 파일 배포 불필요)
- 빌드 구성을 단순화하기 위해 독자적인 'startor' 종속성 제공
- 가능할 때마다 자동으로 스프링 및 타사 라이브러리 구성
- 메트릭, 상태 확인 및 외부화된 구성과 같은 프로덕션 준비 기능 제공
- 코드 생성 및 XML 구성에 대한 요구 사항 불필요

.

**Containerless**

- 스프링 애플리케이션 개발에 요구되는 Servlet Container 관련 설정 지원을 위한 개발 도구와 아키텍처 지원
  - 애플리케이션 개발의 핵심이 아닌 단순 반복 작업 제거
  - 서블릿 컨테이너 설치, WAR 폴더 구조, web.xml, WAR 빌드, 컨테이너로 배치, 포트 설정, 클래스 로더, 로깅 ... 
- 독립실행형(standalone) 자바 애플리케이션으로 동작
  - main 메서드 실행만으로 Servlet Container 관련 모든 필요 작업이 수행