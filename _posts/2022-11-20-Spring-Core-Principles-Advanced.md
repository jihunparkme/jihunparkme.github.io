---
layout: post
title: Spring Core Principles Advanced
summary: 스프링 핵심 원리 고급편
categories: Spring-core-advanced
featured-img: spring-core-advanced
# mathjax: true
---

# Spring Core Principles Advanced

영한님의 [스프링 핵심 원리 - 고급편](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%ED%95%B5%EC%8B%AC-%EC%9B%90%EB%A6%AC-%EA%B3%A0%EA%B8%89%ED%8E%B8/dashboard) 강의 노트

[Project](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced)

## ThreadLocal

**동시성 문제**

- 다수의 쓰레드가 동시에 같은 인스턴스 필드 값을 변경하면서 발생하는 문제
- 스프링 빈처럼 싱글톤 객체의 필드를 변경하며 사용할 때 주의

**ThreadLocal**

- **특정 스레드만 접근**할 수 있는 특별한 저장소
- 각 스레드마다 별도의 내부 저장소 제공
- 특정 스레드 로컬을 모두 사용면 `ThreadLocal.remove()` 호출로 저장된 값을 반드시 제거
  - 스레드 풀을 사용할 경우(ex. WAS) 스레드 로컬 값을 제거하지 않으면, 사용자B가 사용자A 데이터를 조회하게 되는 문제 발생
  - 스레드는 스레드 풀을 통해 재사용되지 때문에 스레드 로컬에서 제거되지 않고 남아있는 데이터를 다른 사용자가 조회할 수 있게 된다.

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/template-method-pattern.png?raw=true 'Result')

[commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/994962186e720e6c0248f48bf843a0538fc3ba7f)

## Template Method Pattern 

다형성(상속과 오버라이딩)을 활용해서 변하는 부분(핵심 기능)과 변하지 않는 부분(로그 추적기, 트랜잭션..)을 분리하는 디자인 패턴

- 템플릿 틀(부모 클래스)에 변하지 않는 부분을 두고, 변하는 부분(자식 클래스에서 상속과 오버라이딩으로 처리)은 별도로 호출
- 클래스는 단 한 개의 책임을 가져야 한다는 `단일 책임 원칙`(**S**ingle **R**esponsibility **P**rinciple)을 잘 지키는 패턴

[commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/54de44c4807c50838552fa6d95d023336ce3ec70)

**익명 내부 클래스**

- 지정 이름이 없고 클래스 내부에 선언되는 클래스
- 객체 인스턴스 생성과 동시에 생성할 클래스를 상속 받은 자식 클래스 정의

```java
AbstractTemplate template1 = new AbstractTemplate() {
    @Override
    protected void call() {
        log.info("비즈니스 로직1 실행");
    }
};
log.info("클래스 이름1={}", template1.getClass()); // class hello.advanced.trace.template.TemplateMethodTest$1
template1.execute();
```

---

**스프링 완전 정복 로드맵**

- 스프링 입문 > 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술
- [스프링 핵심 원리 > 기본편](https://jihunparkme.github.io/Spring-Core/)
- 모든 개발자를 위한 HTTP 웹 기본 지식
  - [Basic](https://jihunparkme.github.io/Http-Web-Network_basic/)
  - [Method](https://jihunparkme.github.io/Http-Web-Network_method/)
  - [Header](https://jihunparkme.github.io/Http-Web-Network_header/)
- 스프링 웹 MVC 1편
  - [Servlet](https://jihunparkme.github.io/Spring-MVC-Part1-Servlet/)
  - [MVC](https://jihunparkme.github.io/Spring-MVC-Part1-MVC/)
- 스프링 웹 MVC 2편
  - [Thymeleaf](https://jihunparkme.github.io/Spring-MVC-Part2-Thymeleaf/)
  - [etc](https://jihunparkme.github.io/Spring-MVC-Part2-Etc/)
  - [Validation](https://jihunparkme.github.io/Spring-MVC-Part2-Validation/)
  - [Login](https://jihunparkme.github.io/Spring-MVC-Part2-Login/)
  - [Exception](https://jihunparkme.github.io/Spring-MVC-Part2-Exception/)
- [스프링 DB 1편 > 데이터 접근 핵심 원리](https://jihunparkme.github.io/Spring-DB-Part1/)
- [스프링 DB 2편 > 데이터 접근 활용 기술](https://jihunparkme.github.io/Spring-DB-Part2/)
- [스프링 핵심 원리 > 고급편](https://jihunparkme.github.io/Spring-Core-Principles-Advanced/)