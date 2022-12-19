---
layout: post
title: Spring Core Principles Advanced
summary: 스프링 핵심 원리 고급편
categories: Spring-core-advanced Pattern ThreadLocal Proxy
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

**다형성(상속과 오버라이딩)을 활용해서 `변하는 부분`(핵심 기능)과 `변하지 않는 부분`(로그 추적기, 트랜잭션..)을 `분리`하는 디자인 패턴**

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

**Template Method Pattern 의 상속으로 인한 `단점을 위임으로` 해결한 디자인 패턴**

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

### Template Callback Pattern

**전략을 필드로 가지지 않고 파라미터로 전달**
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

Example 
- [commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/aa3dc38e1ebbefc28e10b05020d6e65e5d1fc95b)

적용
- [commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/205afaf5f93c7702a377484af3345ad4c5880db8)

## Proxy

**프록시의 주요 기능**
- `접근 제어`
  - 권한에 따른 접근 차단
  - 캐싱
  - 지연 로딩
- `부가 기능 추가`
  - 기존 제공 기능에 부가 기능 수행
  - ex. 요청/응답 값 변형, 추가 로그
- 단점
  - 대상 클래스만 다를 뿐 로직은 유사하고, 대상 클래스 개수만큼 프록시 클래스 생성 필요
  - `동적 프록시 기술`을 통해 프록시 클래스를 하나만 만들어서 모든 곳에 적용 가능

### Proxy Pattern

**프록시를 적용하여 접근을 제어하는 패턴**

**의도(intent)** : 다른 개체에 대한 **접근을 제어**하기 위해 대리자 제공

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/proxy-pattern.png?raw=true 'Result')

- 실제 객체와 클라이언트의 코드를 변경하지 않고, 프록시 도입으로 접근을 제어
- 실제 클라이언트 입장에서 프록시 객체가 주입되었는지, 실제 객체가 주입되었는지 알 수 없음

프록시 객체

```java
@Slf4j
public class CacheProxy implements Subject {

    private Subject target; // 프록시가 호출하는 대상
    private String cacheValue;

    public CacheProxy(Subject target) {
        this.target = target;
    }

    /**
     * 프록시도 실제 객체와 모양이 같아야 하므로 인터페이스 구현
     */
    @Override
    public String operation() {
        log.info("프록시 호출");
        if (cacheValue == null) {
            // 클라이언트가 프록시를 호출하면 프록시가 최종적으로 실제 객체 호출
            cacheValue = target.operation();
        }
        return cacheValue;
    }
}
```

프록시 객체 적용

```java
Subject realSubject = new RealSubject(); // 실제 객체
Subject cacheProxy = new CacheProxy(realSubject); // 실제 객체 참조를 전달
ProxyPatternClient client = new ProxyPatternClient(cacheProxy); // 프록시 객체 주입
client.execute(); // 이후에는 캐시 데이터 반환
client.execute(); 
client.execute();
```

[commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/3ecddfb00fa3efd73b2470fd52e41ea1bc73ed45)

### Decorator Pattern

**프록시를 적용하여 부가 기능을 추가하는 패턴**

**의도(intent)** : **객체에 추가 책임(기능)을 동적으로 추가**하고, 기능 확장을 위한 유연한 대안 제공

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/decorator-pattern.png?raw=true 'Result')

- client -> messageDecorator(proxy) -> realComponent 객체 의존
  - [commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/e4b4259f939424fded208fa43272534683f6c559)
- client -> timeDecorator(proxy) -> messageDecorator(proxy) -> realComponent 객체 의존
  - [commit](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/24d4e14af5948368a1341d12d7974ccb5fa8c5f0)

### 적용

프록시를 사용해 **기존 코드를 수정하지 않고 새로운 기능을 도입**

- 실제 객체 대신 프록시 객체를 스프링 빈으로 등록(프록시 내부에서 실제 객체 참조)
  - `프록시 객체`는 스프링 컨테이너가 스프링 빈으로 관리하고 자바 힙 메모리에 올라가는 반면
  - `실제 객체`는 자바 힙 메모리에는 올라가지만 스프링 컨테이너가 관리하지 않음
    - 프록시 객체를 통해서 참조되는 존재

**인터페이스와 구현 클래스(스프링 빈 수동 등록)**

- 인터페이스 기반 프록시 도입
  - 프록시 클래스를 다수 생성해야 하는 단점 존재
- [init](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/919994e2dde6469c8dc25e7b842d7fafca5e54b9)
- [프록시 적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/4ad297c74f25cf9697d0896078c5a21ffbda4f5d)

**인터페이스 없는 구체 클래스(스프링 빈 수동 등록)**

- 클래스 기반 프록시 도입
  - 인터페이스가 없더라도 다형성으로 클래스를 상속받아서 프록시를 적용
  - 인터페이스 기반 프록시에 비해 여러 단점이 존재
    - 부모 클래스의 생성자 호출 필요
    - final 클래스 상속 불가
    - final 메서드 오버라이딩 불가
- [init](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/f6df360609144e82f90cb6242c05bc375fd7d131)
- [프록시 도입 전](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/d7f881f63b2666bd49ee5e6932e8908c9d11d6ea)
- [프록시 도입](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/6945eaea9f2ff1ea1cd4666b1873e8004abb3027)
- [적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/2b4b6d5ada1fd29bb87ce7a8fc3145bbeac675a8)

**컴포넌트 스캔 스프링 빈 자동 등록**

- [init](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/b139e5df727f4ac39d1819815c0def0acbc21e61)

## 동적 프록시

참고. 리플렉션

- 클래스/메서드 메타정보를 동적으로 획득하고, 코드를 동적으로 호출
- 런타임에 동작하므로 컴파일 시점에 오류를 잡을 수 없는 단점
  - 일반적으로 사용하지 않는 것이 좋고, 프레임워크 개발이나 일반적인 공통 처리가 필요할 경우 부분적으로 주의해서 사용

```java
@Test
void reflectionTest() throws Exception {
    Class classHello = Class.forName("hello.proxy.jdkdynamic.ReflectionTest$Hello"); // 클래스 메타 정보 획득

    Hello target = new Hello();

    Method methodCallA = classHello.getMethod("callMethodA"); // 메서드 메타 정보 획득
    dynamicCall(methodCallA, target);

    Method methodCallB = classHello.getMethod("callMethodB");
    dynamicCall(methodCallB, target);
}

private void dynamicCall(Method method, Object target) throws Exception {
    Object result = method.invoke(target); // 획득한 메서드 메타 정보로 실제 인스턴스의 메서드 호출
}
```

### JDK 동적 프록시

프록시 클래스를 런타임에 동적으로 생성

- 인터페이스 기반 동적 프록시 생성
  - 각각의 대상 객체 프록시를 직접 만들지 않고, 프록시 동적 생성(JDK 동적 프록시) 후 `InvocationHandler` 인터페이스 구현체(프록시 로직 정의) 하나를 공통 사용
  - 동적 프록시는 핸들러 로직만 호출하고 메서드와 인수를 가지고 실행
  - **객체의 인터페이스가 반드시 필요**해서, 클래스만 있는 경우에는 적용할 수 없는 한계

InvocationHandler.java

```java
package java.lang.reflect;

public interface InvocationHandler {
    public Object invoke(Object proxy, Method method, Object[] args)
        throws Throwable;
}
```

TimeInvocationHandler.java (InvocationHandler 인터페이스 구현체)
  - Object proxy : 프록시 자신
  - Method method : 호출한 메서드
  - Object[] args : 메서드를 호출할 때 전달한 인수

```java
@Slf4j
public class TimeInvocationHandler implements InvocationHandler {
    private final Object target;

    public TimeInvocationHandler(Object target) {
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        log.info("TimeProxy 실행");
        long startTime = System.currentTimeMillis();

        Object result = method.invoke(target, args);

        long endTime = System.currentTimeMillis();
        long resultTime = endTime - startTime;
        log.info("TimeProxy 종료 resultTime={}", resultTime);
        return result;
    }
}
```

**적용 예제**

```java
@Test
void dynamic() {
    AInterface target = new AImpl();
    TimeInvocationHandler handler = new TimeInvocationHandler(target);

    /**
      * Proxy.newProxyInstance (동적 프록시 생성)
      *
      * ClassLoader loader, Class<?>[] interfaces, InvocationHandler h
      * 클래스 로더 정보, 인터페이스, 핸들러 로직
      *
      * 해당 인터페이스 기반으로 동적 프록시 생성 및 핸들러 로직의 결과 반환
      */
    AInterface proxy = (AInterface) Proxy.newProxyInstance(AInterface.class.getClassLoader(), new Class[]{AInterface.class}, handler);

    proxy.call();
    log.info("targetClass={}", target.getClass()); // targetClass=class hello.proxy.jdkdynamic.code.AImpl
    log.info("proxyClass={}", proxy.getClass()); // proxyClass=class com.sun.proxy.$Proxy12
}
```

**실행 순서**

1. JDK 동적 프록시의 call() 실행 `proxy.call();`
2. JDK 동적 프록시는 `InvocationHandler.invoke()` 호출
3. TimeInvocationHandler 내부 로직 수행 및 `method.invoke(target, args)` 호출.
4. target의 실제 객체 AImpl 인스턴스의 `call()` 실행
5. AImpl 인스턴스의 call() 실행이 끝나면 TimeInvocationHandler 응답

[example](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/4da1abe77926fc50e45e378e988899ac981e41b4)

**적용**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/jdk-dynamic-proxy.png?raw=true 'Result')

- [JDK 동적 프록시 적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/1ec3675562a30563c79d0cab4d8ce82d3088f1e3)
- [메서드 이름 필터 적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/b51f05662a1bdb74922c23e2d925182cbae1b22c)

### CGLIB

- 바이트코드 조작을 통한 클래스 동적 생성 기술 제공 라이브러리
- 인터페이스 없이 구체 클래스만으로 동적 프록시 생성









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