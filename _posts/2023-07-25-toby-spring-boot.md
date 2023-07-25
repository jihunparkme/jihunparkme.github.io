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

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/Containerless.png?raw=true 'Result')

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

## Start to Develop

**`JDK`**

- [SDK-MAN(The Software Development Kit Manager)](https://sdkman.io/)
  - Unix 기반 시스템에서 여러 소프트웨어 개발 키트의 병렬 버전을 관리하기 위한 도구
  - java 버전 확인 ➔ `sdk list java`
  - 특정 identifier 설치 ➔ `sdk install java {id}`
  - 해당 디렉토리에서 특정 버전의 java 사용 ➔ `sdk use java {id}`
- [jabba](https://github.com/shyiko/jabba)
  - Java 버전 관리자

.

**API Test Method**

- 웹 브라우저 개발자 도구 - Network
- curl
- [HTTPie](https://httpie.io/)
- Intellij IDEA Ultimate- http request
- [Postman API Platform](https://www.postman.com/)
- JUnit Test
- ...

.

**HTTP Request and Response**

```http
❯ http -v ":8080/hello?name=Spring"
GET /hello?name=Spring HTTP/1.1
Accept: */* --> 클라이언트가 선호하는 미디어 타입
Accept-Encoding: gzip, deflate --> 클라이언트가 선호하는 압축 인코딩
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.1

HTTP/1.1 200
Connection: keep-alive
Content-Length: 12
Content-Type: text/plain;charset=UTF-8 --> 표현 데이터의 형식
Date: Thu, 01 Dec 2022 01:45:15 GMT
Keep-Alive: timeout=60
Hello Spring
```