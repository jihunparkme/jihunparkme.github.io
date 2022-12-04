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

[commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/994962186e720e6c0248f48bf843a0538fc3ba7f)

## Template Method Pattern 

**다형성(상속과 오버라이딩)을 활용해서 변하는 부분(핵심 기능)과 변하지 않는 부분(로그 추적기, 트랜잭션..)을 분리하는 디자인 패턴**

**구조**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/template-method-pattern-3.png?raw=true 'Result')

**인스턴스 호출 과정**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/template-method-pattern-instance-call.png?raw=true 'Result')

- 부모 클래스에 템플릿(변하지 않는 부분)을 정의하고, 일부 변경되는 로직은 자식 클래스에 정의
- 자식 클래스가 전체 구조를 변경하지 않고, 특정 부분만 재정의
- 결국 상속과 오버라이딩을 통한 다형성으로 문제 해결
- 클래스는 단 한 개의 책임을 가져야 한다는 `단일 책임 원칙`(**S**ingle **R**esponsibility **P**rinciple)을 잘 지키는 패턴
- 단, 상속에서 오는 단점들이 존재
  - 강한 의존성으로 부모 클래스의 기능을 사용하지 않더라도 부모 클래스를 알아야 하고
  - 부모 클래스를 수정하면 자식 클래스에 영향을 줄 수 있음
  - 상속 구조로 인해 생성되는 클래스나 익명 내부 클래스의 복잡성

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
log.info("클래스 이름1={}", template1.getClass()); // class hello...TemplateMethodTest$1
template1.execute();
```

**Template Example**

```java
public abstract class AbstractTemplate<T> {

    private final LogTrace trace;

    public AbstractTemplate(LogTrace trace) {
        this.trace = trace;
    }

    public T execute(String message) {
        TraceStatus status = null;
        try {
            status = trace.begin(message);

            //로직 호출
            T result = call();
            
            trace.end(status);
            return result;
        } catch (Exception e) {
            trace.exception(status, e);
            throw e;
        }
    }

    protected abstract T call();
}
```

[commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/bd55a6ea7ad39baae4761b33edec77da75728961)

## Strategy Pattern

**Template Method Pattern 의 상속으로 인한 단점을 위임으로 해결한 디자인 패턴**

**구조**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/strategy-pattern-1.png?raw=true 'Result')

**전략 패턴 실행 과정**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/strategy-pattern.png?raw=true 'Result')

- 변하지 않는 부분을 Context(변하지 않는 템플릿)에, 변하는 부분을 Strategy(변하는 알고리즘) 인터페이스에 두고, 해당 구현체를 통해 문제를 해결
  - Context에 원하는 Strategy 구현체 주입
  - 클라이언트는 Context 실행
  - Context는 Context 로직 시작
  - Context 로직 중간에 strategy.call() 호출로 주입 받은 Strategy 로직 실행
  - Context는 나머지 로직 실행

[commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/b31151eb57adfc7780f0aa860a0f4a7c3d0c4262)

**익명 클래스 사용**

- Context/Strategy 선 조립, 후 실행 방식에 적합
  - 필드에 Strategy 저장 방식의 전략 패턴
- 한 번 조립 이후 Context 실행만 하면 끝
  - 스프링 로딩 시점에 의존관계 주입을 통해 조립 후 요청을 처리하는 것과 유사
- 단점은, 조립 이후에 전략 변경이 번거로움 (싱글톤 사용 시 동시성 이슈 등 고려 사항이 존재)

[commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/ae539d6986872b6e47fad0d6a6741fb101a35a17)

**Template Callback Pattern**

전략을 필드로 가지지 않고 파라미터로 전달
- 전략 패턴에서 템플릿과 콜백 부분이 강조된 패턴(GOF 패턴은 아니고 스프링 내부에서 불리움)
- 코드가 Call 이후 코드를 넘겨준 곳의 Back 에서 실행(CallBack..)
- 스프링에서 XxxTemplate(JdbcTemplate, RestTemplate, TransactionTemplate, RedisTemplate) 형태는 템플릿 콜백 패턴이 사용되어 만들어진 클래스

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/strategy-pattern-parameter.png?raw=true 'Result')

- 파라미터에 Strategy 전달 방식의 전략 패턴
- 실행할 때마다 전략을 유연하게 변경
- 단점은, 실행할 때마다 전략을 계속 지정해 주어야 하는 번거로움

[commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/2c4c1bc0b4059acb4e864cc3d3d11cee56007706)

콜백을 사용할 경우 익명 내부 클래스나 람다를 사용하는 것이 편리

단, 여러 곳에서 함께 사용될 경우 재사용을 위해 콜백을 별도의 클래스로 만드는게 좋음

- Context -> Template
- Strategy -> Callback

[commit]()


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