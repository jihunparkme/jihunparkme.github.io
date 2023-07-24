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

**`Containerless`**

- 스프링 애플리케이션 개발에 요구되는 Servlet Container 관련 설정 지원을 위한 개발 도구와 아키텍처 지원
  - 애플리케이션 개발의 핵심이 아닌 단순 반복 작업 제거
  - 서블릿 컨테이너 설치, WAR 폴더 구조, web.xml, WAR 빌드, 컨테이너로 배치, 포트 설정, 클래스 로더, 로깅 ... 
- 독립실행형(standalone) 자바 애플리케이션으로 동작
  - main 메서드 실행만으로 Servlet Container 관련 모든 필요 작업이 수행

.

**`Opinionated Tool`**

**Spring**
- 극단적 유연함을 추구하고 다양한 관점을 수용하는 것이 설계 철학이었지만..
- 각종 라이브러리의 의존관계와 버전 호환성을 체크하는 작업은 고되고 쉽지 않은 작업

  
**Spring Boot**
- opinionated 설계: 자기 주장이 강하고 자신의 의견을 고집한 설계 철학
  - 일단 정해주는 대로 빠르게 개발하고 나중에 고민. 스프링을 잘 활용할 수 있는 방법 제공
- 스프링 부트는 각 라이브러리의 버전마다 사용할 기술의 종류 선정
  - 사전 검증된 추천 기술, 라이브러리 구성, 의존 관계와 적용 버전, 세부 구성(DI)과 디폴트 설정 등 제공
  - 디폴트 구성을 커스터마이징 할 수 있는 유연한 방법 제공
