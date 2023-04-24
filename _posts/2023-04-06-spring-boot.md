---
layout: post
title: Spring Boot
summary: Spring Boot 핵심 원리와 활용
categories: Spring-Boot
featured-img: spring
# mathjax: true
---

# Spring Boot

스프링 프레임워크를 쉽게 사용할 수 있게 도와주는 도구

**핵심 기능**

- `WAS`: Tomcat 같은 웹 서버를 내장해서 별도의 웹 서버 설치 불필요
- `라이브러리 관리` : 손쉬운 빌드 구성을 위한 스타터 종속성 제공 및 라이브러리 버전 관리
- `자동 구성`: 프로젝트 시작에 필요한 스프링과 외부 라이브러리의 빈을 자동 등록
- `외부 설정`: 환경에 따라 달라져야 하는 외부 설정 공통화
- `프로덕션 준비`: 모니터링을 위한 메트릭, 상태 확인 기능 제공

## 웹 서버와 서블릿 컨테이너

**방식의 변화**

전통 방식

- 자바 웹 애플리케이션 개발 시 서버에 톰캣 같은 WAS(웹 애플리케이션 서버) 설치가 필요
- WAS에서 동작하도록 서블릿 스펙에 맞추어 코드를 작성하고 WAR 형식으로 빌드해서 .war 파일을 생성
- 생성된 .war 파일을 WAS에 전달해서 배포하는 방식으로 전체 개발 주기가 동작
- 과거 방식은 WAS 기반 위에서 개발하고 실행이 필요하고, IDE 같은 개발 환경에서도 WAS와 연동해서 실행되도록 복잡한 추가 설정이 필요

최근 방식

- 최근에는 스프링 부트가 내장 톰캣을 포함(애플리케이션 코드 안에 WAS가 라이브러리로 내장)
- 개발자는 코드를 작성하고 JAR로 빌드한 다음에 해당 JAR를 원하는 위치에서 실행하기만 하면 WAS도 함께 실행
- IDE 개발 환경에서 WAS 설치와 연동하는 복잡한 일은 불필요

**JAR & WAR**

JAR (Java Archive)

`java -jar abc.jar`

- 자바는 여러 클래스와 관련 리소스를 압축한 .jar 라는 압출 파일이 존재
- JAR 파일은 JVM 위에서 직접 실행되거나 다른 곳에서 사용하는 라이브러리로 제공
- 직접 실행할 경우 main() 메서드가 필요하고, MANIFEST.MF 파일에 실행할 메인 메서드가 있는 클래스 지정 필요

WAR (Web Application Archive)

- .war 파일은 웹 애플리케이션 서버(WAS)에 배포할 때 사용하는 파일
- JAR 파일이 JVM 위에서 실행된다면, WAR는 웹 애플리케이션 서버 위에서 실행
- 웹 애플리케이션 서버 위에서 실행되고, HTML 같은 정적 리소스와 클래스 파일을 모두 함께 포함하기 때문에 JAR 대비 구조가 복잡하고 WAR 구조를 지켜야 함

**서블릿 컨테이너 초기화**

- 서블릿은 초기화 인터페이스(ServletContainerInitializer)를 제공
  - 서블릿 컨테이너를 초기화 하는 기능 제공
  - 서블릿 컨테이너는 실행 시점에 초기화 메서드인 onStartup() 을 호출
  - 여기서 애플리케이션에 필요한 기능들을 초기화 하거나 등록

```java
public interface ServletContainerInitializer {

    /**
     * Set<Class<?>> c
     * - 더 유연한 초기화 기능 제공
     * - @HandlesTypes 애노테이션과 함께 사용
     * 
     * ServletContext ctx
     * - 서블릿 컨테이너 자체 기능 제공
     * - 이 객체를 통해 필터나 서블릿 등록 가능
     */
    public void onStartup(Set<Class<?>> c, ServletContext ctx) throws
ServletException;
}
```

[서블릿 컨테이너 초기화를 위한 설정](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/ac5cd44f85a8a2751ee73d641bf97b33943ffcf4)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/servlet-container.png?raw=true 'Result')


초기화 순서

- 서블릿 컨테이너 초기화 실행
  - ServletContainerInitializer 를 구현하고, `resources/META-INF/services/jakarta.servlet.ServletContainerInitializer` 파일에 등록된 컨테이너를 실행
- 애플리케이션 초기화 실행
  - 컨터이너를 실행하면서 `@HandlesTypes(AppInit.class)` 가 선언되어 있을 경우 AppInit 구현체를 모두 찾아서 생성 및 실행

애플리케이션 초기화 개념 생성 이유

- 서블릿 컨테이너는 초기화를 위해 ServletContainerInitializer 인터페이스 구현과 META-INF/services/
jakarta.servlet.ServletContainerInitializer 파일에 해당 클래스를 직접 지정해야 하지만, 애플리케이션 초기화는 특정 인터페이스만 구현하면 되는 편리함
- 애플리케이션 초기화는 서블릿 컨테이너에 상관없이 원하는 모양으로 인터페이스 생성이 가능하여 애플리케이션 초기화 코드가 서블릿 컨테이너에 대한 의존을 줄일 수 있음

[서블릿 컨테이너 / 애플리케이션 초기화](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/a64d0c2224db274f839d175ce626add47288c2f3)

**스프링 컨테이너 등록**

- 스프링 컨테이너 만들기
- 스프링MVC 컨트롤러를 스프링 컨테이너에 빈으로 등록하기
- 스프링MVC를 사용하는데 필요한 디스패처 서블릿을 서블릿 컨테이너 등록하기

[스프링 컨테이너 등록](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/309038cec60f458c80ab06bd86f650b80c3bc515)

**스프링 MVC 서블릿 컨테이너 초기화 지원**

번거롭고 반복적인 서블릿 컨테이너 초기화 과정을 스프링 MVC이 지원

- 개발자는 서블릿 컨테이너 초기화 과정은 생략하고, 애플리케이션 초기화 코드만 작성
- `WebApplicationInitializer` 인터페이스만 구현
 - spring-web 라이브러리를 보면, 아래 파일들을 이미 등록해둔 것을 확인
 - META-INF/services/jakarta.servlet.ServletContainerInitializer
 - org.springframework.web.SpringServletContainerInitializer

```java
package org.springframework.web;

public interface WebApplicationInitializer {
  void onStartup(ServletContext servletContext) throws ServletException;
}
```

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/WebApplicationInitializer.png?raw=true 'Result')

[스프링 MVC 서블릿 컨테이너 초기화 지원(WebApplicationInitializer 구현)](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/75febc7e060a0f49b77090352ebf7e8732667ee5)

## 스프링 부트와 내장 톰캣

**WAR 배포 방식의 단점**

- WAS(ex. tomcat) 별도 설치 필요
- 개발 환경 설정 복잡
- 배포 과정 복잡
- 버전 변경 시 WAS 재설치 필요