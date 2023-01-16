---
layout: post
title: Spring Core Principles Advanced
summary: 스프링 핵심 원리 고급편
categories: Spring-core-advanced Pattern ThreadLocal Proxy AOP
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

**리플렉션**

- 클래스/메서드 `메타정보`를 `동적으로 획득`하고, 코드를 `동적으로 호출`
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

대상 클래스에 인터페이스가 있을 경우(인터페이스 기반 프록시)

- `인터페이스 기반` 동적 프록시 생성(런타임)
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

대상 클래스에 인터페이스가 없을 경우(구체 클래스 기반 프록시)

- 인터페이스 없이 `구체 클래스 기반`(상속) 동적 프록시 생성
  - 상속 사용으로 인한 제약
    - 부모 클래스의 기본 생성자 필요
    - final 클래스는 상속 불가
    - final 메서드는 오버라이딩 불가
- JDK 동적 프록시 실행 로직에 InvocationHandler를 제공하듯, `MethodInterceptor` 제공

MethodInterceptor.java

```java
package org.springframework.cglib.proxy;

/**
 * obj : CGLIB 적용 객체
 * method : 호출된 메서드
 * args : 메서드 호출에 전달된 인수
 * proxy : 메서드 호출에 사용
 */
public interface MethodInterceptor extends Callback {
    Object intercept(Object obj, Method method, Object[] args, MethodProxy proxy) throws Throwable;
}
```

```java
@Override
public Object intercept(Object obj, Method method, Object[] args, MethodProxy proxy) throws Throwable {
    Object result = proxy.invoke(target, args); // 실제 대상 동적 호출(CGLIB는 성능상 Method 대신 MethodProxy 사용)
    return result;
}
```

[CGLIB 예제](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/b5f3e1b8da984c1e91fc29365fcf606861340238)

## Spring Proxy Factory

프록시 생성은 `ProxyFactory` 로직은 `Advice`

남은 문제점.. -> 빈 후처리기로 처리 가능

- 너무 많은 설정이 필요
  - 스프링 빈이 100개 있다면, 프록시 부가 기능 적용을 위해 100개의 동적 프록시 생성 필요
- 컴포넌트 스캔을 사용하는 경우 Proxy Factory 적용 불가능
  - 실제 객체가 스프링 컨테이너 스프링 빈으로 등록된 상태이므로

ㅇ 인터페이스가 있는 경우 JDK 동적 프록시, 그렇지 않은 경우에는 CGLIB 적용
- 동적 프록시를 통합해서 만들어주는 `ProxyFactory` 제공
- 인터페이스가 있으면 JDK 동적 프록시 사용, 구체 클래스만 있다면 CGLIB 사용(default)
- [Proxy Factory 적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/ee2c610435c25a333dd1ee1ca5f2e2eb11257538)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-factory.png?raw=true 'Result')

ㅇ JDK 동적 프록시, CGLIB 를 함께 사용할 경우 **부가 기능 적용**

- InvocationHandler,MethodInterceptor 를 신경쓰지 않고, `Advice` 만 생성
- org.aopalliance.intercept.`MethodInterceptor` 구현으로 Advice 생성
- [Proxy Factory 적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/b64c8fe13fb180ea7b958d4081f9b17f1b18b5ba)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-factory-advice.png?raw=true 'Result')

ㅇ **특정 조건**에 프록시 로직을 적용하는 공통 기능
- `Pointcut` 개념 도입으로 일관성있게 해결

```java
/** new ProxyFactory(target)
  * 프록시 호출 대상을 함께 전달
  * target 인스턴스에 인터페이스가 있다면, JDK 동적 프록시를 기본으로 사용
  * 인터페이스가 없고 구체 클래스만 있다면, CGLIB를 통해서 동적 프록시를 생성
  */
ProxyFactory proxyFactory = new ProxyFactory(target);

/** setProxyTargetClass(true)
 * 인터페이스가 있어도 CGLIB 사용 및 타겟 클래스 기반 프록시(CGLIB) 사용
 */
proxyFactory.setProxyTargetClass(true);

/** .addAdvice(new TimeAdvice())
  * 프록시 팩토리를 통해서 만든 프록시가 사용할 부가 기능 로직을 설정
  * JDK 동적 프록시가 제공하는 InvocationHandler 와 CGLIB가 제공하는 MethodInterceptor 의 개념과 유사
  */
proxyFactory.addAdvice(new TimeAdvice());

/** proxyFactory.getProxy()
  *  프록시 객체를 생성하고 그 결과 반환
  */
ServiceInterface proxy = (ServiceInterface) proxyFactory.getProxy();
```

[MethodInterceptor 구현으로 Advice 생성 예제](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/57f8131041985a547e82d22d6724f4059f72717b)

[Spring Proxy Factory 사용 예제](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/554b72d8cade3842305382d7eea85a064a67df56)

### Pointcut, Advice, Advisor

핵심. **하나의 Target 에 여러 AOP가 동시에 적용되어도, 스프링의 AOP는 Target 마다 하나의
프록시만 생성**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-proxy-factory-advisor.png?raw=true 'Result')

`Pointcut` : 대상 여부를 확인하는 필터 역할 
- 부가 기능을 어느 곳에 적용/미적용할지 판단하는 필터링 로직
- 주로 클래스와 메서드 이름으로 필터링
- [Pointcut 만들기](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/a7583c7cd317d3fbc131109f0f3d228860a4f92f)
- [스프링 제공 Pointcut](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/efe15544a0439467a7705444700ecb2106d0d1c4)
  - 스프링이 제공하는 대표적인 Pointcut
    - `AspectJExpressionPointcut` : aspectJ 표현식 매칭 (실무에서 주로 많이 사용)
    - `NameMatchMethodPointcut` : 메서드 이름 기반 매칭한다
    - `JdkRegexpMethodPointcut` : JDK 정규 표현식 기반 매칭
    - `TruePointcut` : 항상 참 반환
    - `AnnotationMatchingPointcut` : 애노테이션 매칭
- **Pointcut 의 두 가지 역할 ‼️**
  - `생성 단계` -> 프록시 적용 여부 판단 (클래스, 메서드 조건 모두 비교)
  - `사용 단계` -> advice(부가 기능) 적용 여부 판단

`Advice` : 부가 기능 로직 담당
- 프록시가 호출하는 부가 기능(=프록시 로직)

`Advisor` : 하나의 Pointcut, 하나의 Advice를 갖는 것
- 조언(`Advice`)을 어디(`Pointcut`)에 할 것인가? 
- 조언자(`Advisor`)는 어디(`Pointcut`)에 조언(`Advice`)을 해야할지 알고 있다.
- [프록시에 여러 Advisor 함께 적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/b7193eacc32a91b7bf730023558587c7d7d92531)

```java
ServiceInterface target = new ServiceImpl();
ProxyFactory proxyFactory = new ProxyFactory(target);

DefaultPointcutAdvisor advisor = new DefaultPointcutAdvisor(Pointcut.TRUE, new TimeAdvice()); // Advisor 인터페이스의 가장 일반적인 구현체

proxyFactory.addAdvisor(advisor);
ServiceInterface proxy = (ServiceInterface) proxyFactory.getProxy();
```

## ⭐️ BeanPostProcessor

빈 저장소에 객체를 등록하기 직전 조작을 하고 싶을 경우 빈 후처리기(BeanPostProcessor)를 사용(빈 생성 후 처리 용도)

- Spring Proxy Factory 의 단점(많은 설정, 컴포넌트 스캔 대상 객체 적용의 어려움)을 해결

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/bean-post-processor.png?raw=true 'Result')

1. `생성`: 스프링 빈 대상 객체 생성(@Bean, @ComponentScan..)
2. `전달`: 생성된 객체를 빈 저장소에 등록하기 직전에 빈 후처리기에 전달
3. `후 처리 작업`: 빈 후처리기는 전달된 스프링 빈 객체를 조작하거나 다른 객체로 바뀌치기 가능
4. `등록`: 빈 후처리기는 빈 반환. 전달 된 빈을 그대로 반환하면 해당 빈이 등록되고, 바꿔치기 하면
다른 객체가 빈 저장소에 등록

**BeanPostProcessor** interface

- 빈 후처리기를 사용하기 위해 `BeanPostProcessor` 인터페이스 구현 후 스프링 빈 등록
- `postProcessBeforeInitialization` : 객체 생성 이후 @PostConstruct 같은 **초기화 발생 전** 호출되는 포스트 프로세서
- `postProcessAfterInitialization` : 객체 생성 이후 @PostConstruct 같은 **초기화 발생
후** 호출되는 포스트 프로세서

```java
public interface BeanPostProcessor {
  Object postProcessBeforeInitialization(Object bean, String beanName) throws
BeansException
 Object postProcessAfterInitialization(Object bean, String beanName) throws
BeansException
}
```
- [빈 후처리기로 객체 바꿔치기](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/8d08c11e6ac146c321dc8256363add26f4449a8c)

**적용**

- BeanPostProcessor 를 사용해서 **실제 객체 대신 프록시를** 스프링 빈으로 등록 가능
  - 수동 등록 빈을 포함하여 컴포넌트 스캔을 사용하는 빈까지 모두 프록시 적용이 가능
  - 설정 파일에서 프록시를 생성하는 코드가 불필요

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/apply-bean-post-processor.png?raw=true 'Result')

[빈 후처리기 적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/ac7d18374be2e755cec90c3d1ee3e4e8a85ce092)

### 스프링 제공 빈 후처리기

스프링 AOP 는 Pointcut 을 사용해서 프록시 적용 대상 여부 체크
  - 프록시가 필요한 곳에만 프록시 적용
  - 프록시 내부 특정 메서드가 호출 되었을 때 어드바이스 적용

의존성 추가록

```groovy
implementation 'org.springframework.boot:spring-boot-starter-aop'
```

- `aspectjweaver`: aspectJ 관련 라이브러리 등록 및 스프링 부트가
AOP 관련 클래스를 자동으로 스프링 빈에 등록
  - `AnnotationAwareAspectJAutoProxyCreator` 빈 후처리기가 스프링 빈에 자동으로 등록

**`AutoProxyCreator`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/auto-proxy-creator.png?raw=true 'Result')

- 자동으로 프록시를 생성해주는 빈 후처리기
- 스프링 빈으로 등록된 Advisor 들을 자동으로 찾아서 프록시가 필요한 곳에 자동으로
프록시 적용
- 프록시를 모든 곳에 생성하는 것은 비용 낭비이므로 포인트컷으로 필터링 후 필요한 곳에 최소한의 프록시 적용
- Advisor1, Advisor2, 3, 4.. 가 제공하는 포인트컷의 조건을 모두 만족하더라도 프록시를 한 개만 생성하고 프록시는 조건에 만족하는 여러 Advisor를 소유

[스프링이 제공하는 빈 후처리기 적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/217425d52a8c7feb4391a55ff50ade13b846c6f4)

**`AspectJExpressionPointcut`**

- AOP에 특화된 정밀한 포인트컷 표현식(AspectJ) 적용

```java
/** package 기준 포인트컷 적용
  * AspectJExpressionPointcut : AspectJ 포인트컷 표현식 적용
  * execution(* hello.proxy.app..*(..)) : AspectJ가 제공하는 포인트컷 표현식
  *      * : 모든 반환 타입
  *      hello.proxy.app.. : 해당 패키지와 그 하위 패키지
  *      *(..) : * 모든 메서드 이름, (..) 파라미터는 상관 없음
  * -> hello.proxy.app 패키지와 그 하위 패키지의 모든 메서드는 포인트컷의 매칭 대상
  */
@Bean
public Advisor advisor2(LogTrace logTrace) {
    AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
    pointcut.setExpression("execution(* hello.proxy.app..*(..))");
    LogTraceAdvice advice = new LogTraceAdvice(logTrace);
    //advisor = pointcut + advice
    return new DefaultPointcutAdvisor(pointcut, advice);
}

/** method 기준 포인트컷 적용
  * hello.proxy.app 패키지와 하위 패키지의 모든 메서드는 포인트컷의 매칭하되,
  * noLog() 메서드는 제외
  */
@Bean
public Advisor advisor3(LogTrace logTrace) {
    AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
    pointcut.setExpression("execution(* hello.proxy.app..*(..)) && !execution(* hello.proxy.app..noLog(..))");
    LogTraceAdvice advice = new LogTraceAdvice(logTrace);
    //advisor = pointcut + advice
    return new DefaultPointcutAdvisor(pointcut, advice);
}
```
  - 스프링에 프록시를 적용하려면 Advisor(pointcut, advice 로 구성)를 만들어서 스프링 빈으로 등록하면 자동 프록시 생성기가 자동으로 처리
  - 자동 프록시 생성기는 스프링 빈으로 등록된 Advisor 들을 찾고, 스프링 빈들에 자동으로 포인트컷이 매칭되는 경우 프록시를 적용

`@Aspect` 애노테이션을 사용해서 더 편리하게 pointcut 과 advice 를 만들고 프록시에 적용할 수 있다.

## ⭐️ @Aspect Proxy

- `@Aspect` 애노테이션으로 pointcut 과 advice 로 구성되어 있는 Advisor 의 편리한 생성 지원
- 자동 프록시 생성기(AnnotationAwareAspectJAutoProxyCreator)를 통해 @Aspect 를 찾아서 Advisor 로 변환/저장, Advisor 기반으로 필요한 곳에 프록시를 생성

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/aspect-annotation.png?raw=true 'Result')

**@Aspect -> Advisor 변환 과정**

1. 실행: 스프링 애플리케이션 로딩 시점에 자동 프록시 생성기 호출
2. 모든 @Aspect 빈 조회: 자동 프록시 생성기는 스프링 컨테이너에서 @Aspect 이 붙은
스프링 빈을 모두 조회
3. 어드바이저 생성: @Aspect 어드바이저 빌더(BeanFactoryAspectJAdvisorsBuilder)를 통해 @Aspect 애노테이션 정보를 기반으로 어드바이저 생성
4. @Aspect 기반 어드바이저 저장: 생성한 어드바이저를 @Aspect 어드바이저 빌더 내부에 저장

@Aspect 어드바이저 빌더(BeanFactoryAspectJAdvisorsBuilder)
- @Aspect 정보를 기반으로 포인트컷, 어드바이스, 어드바이저 생성 및 보관(캐싱)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/BeanFactoryAspectJAdvisorsBuilder.png?raw=true 'Result')

- 자동 프록시를 생성기의 동작과 동일한데, @Aspect Advisor 조회 부분이 추가

**Aspect 적용 클래스**

```java
@Slf4j
@Aspect // 애노테이션 기반 프록시 적용 시 필요
public class LogTraceAspect {

    private final LogTrace logTrace;

    public LogTraceAspect(LogTrace logTrace) {
        this.logTrace = logTrace;
    }

    /**
     * Pointcut + Advice = Advisor
     *
     * Pointcut : @Around 값에 포인트컷 표현식 삽입 (표현식은 AspectJ 표현식 사용)
     * Advice : @Around 메서드 = Advice
     * ProceedingJoinPoint : 실제 호출 대상, 전달 인자, 어떤 객체와 메서드가 호출되었는지 정보 포함(MethodInvocation invocation 과 유사)
     */
    @Around("execution(* hello.proxy.app..*(..))") //=> Pointcut path
    public Object execute(ProceedingJoinPoint joinPoint) throws Throwable { //=> Advice Logic

        TraceStatus status = null;

        // log.info("target={}", joinPoint.getTarget()); //실제 호출 대상
        // log.info("getArgs={}", joinPoint.getArgs()); //전달인자
        // log.info("getSignature={}", joinPoint.getSignature()); //join point시그니처

        try {
            String message = joinPoint.getSignature().toShortString();
            status = logTrace.begin(message);

            // 실제 호출 대상(target) 호출
            Object result = joinPoint.proceed();

            logTrace.end(status);
            return result;
        } catch (Exception e) {
            logTrace.exception(status, e);
            throw e;
        }
    }
}
```

[@Aspect 프록시 - 적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/9258f3b402316bc3446693c00b28d7b915c697a5)

## ⭐️ Spring AOP

애플리케이션 로직은 크게 핵심 기능과 부가 기능으로 나눌 수 있음

여기서, 부가 기능 적용의 문제
- 적용 시 많은 반복 필요
- 여러 곳에 중복 코드 발생
- 변경 시 중복으로 많은 수정 필요
- 적용 대상 변경 시 많은 수정 필요

**`Aspect`**

- 부가 기능과 부가 기능을 어디에 적용할지 선택하는 기능을 하나로 합하여 만들어진 모듈
  - Advisor(Pointcut + Advice) 도 개념상 하나의 Aspect
- 애플리케이션을 바라보는 관점을 하나의 기능에서 횡단 관심사(cross-cutting concerns) 관점으로 보는 것
- Aspect 를 사용한 프로그래밍 방식을 관점 지향 프로그래밍 AOP(Aspect-Oriented
Programming)
- OOP 를 대체하기 위한 것이 아닌 횡단 관심사를 효율적으로 처리하기 어려운 OOP의 부족한 부분 보조 목적으로 개발

**`AspectJ Framework`**

- 스프링 AOP는 대부분 [AspectJ](https://www.eclipse.org/aspectj/) 문법을 차용하고, 프록시 방식의 AOP 적용(AspectJ 제공 기능 일부만 제공)
- AspectJ Framework는 횡단 관심사의 깔끔한 모듈화
  - 자바 프로그래밍 언어에 대한 완벽한 관점 지향 확장
  - 횡단 관심사의 깔끔한 모듈화
  - 오류 검사 및 처리
  - 동기화
  - 성능 최적화(캐싱)
  - 모니터링 및 로깅

### AOP 적용 방식

**컴파일 시점**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/aspect-compile.png?raw=true 'Result')

- .java 소스 코드를 컴파일러(AspectJ가 제공하는 특별한 컴파일러)를 사용해서 .class 를 만드는 시점에 부가 기능 로직 추가 (=Weaving / aspect 와 실제 코드를 연결)
- 단점, 컴파일 시점에 부가 기능을 적용하려면 특별한 컴파일러가 필요하고 복잡

**클래스 로딩 시점**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/aspect-class-road.png?raw=true 'Result')

- 자바를 실행하면 자바는 .class 파일을 JVM 내부의 클래스 로더에 보관. 이때 중간에서 .class 파일을 조작한 다음 JVM에 로드
  -  대부분 모니터링 툴들이 java Instrumentation 방식 사용
- 단점, 로드 타임 위빙은 자바를 실행할 때 특별한 옵션(java -javaagent)을 통해 클래스 로더 조작기를 지정해야 하는데, 이 부분이 번거롭고 운영이 어려움

**런타임 시점(프록시)**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/aspect-runtime.png?raw=true 'Result')

- 런타임 시점(컴파일이 끝나고, 클래스 로더에 클래스도 다 올라가고, 이미 자바가 실행되고 난 다음 상태, 자바의 main 메서드 실행 이후) 프록시를 통해 스프링 빈에 부가 기능을 적용(AOP)
- 단점, 프록시 사용으로 AOP 기능에 일부 제약(final, 상속, 생성자, ..)이 있지만, 다른 방법에서 복잡한 설정 단계가 불필요

**부가 기능이 적용되는 차이**

- `컴파일 시점`: 실제 대상 코드에 애스팩트를 통한 부가 기능 호출 코드가 포함 (AspectJ 직접 사용 필요)
- `클래스 로딩 시점`: 실제 대상 코드에 애스팩트를 통한 부가 기능 호출 코드가 포함 (AspectJ 직접 사용 필요)
- `런타임 시점`: 실제 대상 코드는 그대로 유지하는 대신 프록시를 통해 부가 기능이 적용 (항상 프록시를 통해 부가 기능 사용 -> 스프링 AOP 사용 방식)

**Join Point(AOP를 적용할 수 있는 지점)**

- AOP는 메서드 실행 위치 뿐만 아니라, 다양한 위치에 적용 가능
  - 적용 가능 지점: 생성자, 필드 값 접근, static 메서드 접근, 메서드 실행
- **컴파일 시점 / 클래스 로딩 시점**
  - 바이트 코드를 실제 조작하기 때문에 해당 기능을 모든 지점에 다 적용 가능
- **스프링 AOP**
  - 프록시 방식을 사용(오버라이딩 개념으로 동작)하므로 `메서드 실행 지점에만 AOP 적용` 가능
  - 스프링 컨테이너가 관리할 수 있는 `스프링 빈에만 AOP 적용` 가능
- AspectJ는 더 섬세하고 다양한 기능을 제공하지만, 알아야 할 내용이 많고, 자바 관련 복잡한 설정이 많으므로, 실무에서는 별도 설정 없이 사용할 수 있는 스프링 제공 AOP 기능만 사용해도 대부분의 문제를 해결 가능

### AOP 용어

`Join point`
- AOP를 적용할 수 있는 모든 지점(위치, 메소드 실행, 생성자 호출, 필드 값 접근, static 메서드 접근)
- 프록시를 사용하는 스프링 AOP는 항상 메서드 실행 지점으로 제한

`Pointcut`
- Pointcut 중에서 Advice가 적용될 위치 선별(주로 AspectJ 표현식을 사용해서 지정)
- 프록시를 사용하는 스프링 AOP는 메서드 실행 지점만 Pointcut으로 선별 가능

`Target`
- Advice(부가 기능)를 받는 객체, Pointcut으로 결정

`Advice`
- 부가 기능
- Around, Before, After 같은 다양한 종류의 Advic 존재

`Aspect`
- Advice + Pointcut을 모듈화 한 것(@Aspect)
- 여러 Advice와 Pointcut 함께 존재 가능

`Advisor`
- 하나의 Advice와 하나의 Pointcut으로 구성
- 스프링 AOP에서만 사용되는 특별한 용어

`Weaving`
- Pointcut으로 결정한 타켓의 Join point에 Advice를 적용하는 것
- 핵심 기능 코드에 영향을 주지 않고 부가 기능을 추가 가능
- AOP 적용을 위해 애스펙트를 객체에 연결한 상태
  - 컴파일 타임(AspectJ compiler)
  - 로드 타임
  - 런타임, 스프링 AOP는 런타임, 프록시 방식

`AOP Proxy`
- AOP 기능을 구현하기 위해 만든 프록시 객체
- 스프링에서 AOP 프록시는 JDK 동적 프록시 또는 CGLIB 프록시

### ⭐️ AOP 구현

```groovy
implementation 'org.springframework.boot:spring-boot-starter-aop'
```

- AOP 기능 사용을 위해 spring-boot-starter-aop dependency 추가
- @Aspect 사용을 위해 @EnableAspectJAutoProxy 설정이 필요하지만, 스프링 부트가 자동으로 추가

**@Aspect 클래스를 스프링 빈으로 등록하는 방법**

- @Bean 을 사용해서 직접 등록
- @Component 컴포넌트 스캔을 사용해서 자동 등록
- @Import 주로 설정 파일을 추가할 때 사용(@Configuration)

[스프링 AOP 구현 기본](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/7aab61b3305ba068546c56200574dce46d9bd113)

**`@Pointcut`**

- 포인트컷 시그니처: 메서드 이름 + 파라미터
- 메서드의 반환 타입은 void
- [포인트컷 참조](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/d67add4a15b14f2eea0c12b05b518e82c1f5739f)

```java
@Aspect
@Component
public class Aspect {

    /**
     * @Around 애노테이션의 값은 Pointcut
     * @Around 애노테이션의 메서드는 Advice
     * execution(* hello.aop.order..*(..)) -> hello.aop.order 패키지와 그 하위 패키지( .. )를 지정하는 AspectJ 포인트컷 표현식
     */
    @Around("execution(* hello.aop.order..*(..))")
    public Object doLog(ProceedingJoinPoint joinPoint) throws Throwable {
        log.info("[log] {}", joinPoint.getSignature()); // join point 시그니처
        return joinPoint.proceed();
    }

    //------------------------------------------------------

    /** pointcut signature
     *  pointcut expression : hello.aop.order 패키지와 하위 패키지
     */
    @Pointcut("execution(* hello.aop.order..*(..))")
    private void allOrder() {
    }

    @Around("allOrder()")
    public Object doLog2(ProceedingJoinPoint joinPoint) throws Throwable {
        log.info("[log] {}", joinPoint.getSignature());
        return joinPoint.proceed();
    }

    //------------------------------------------------------

    // 클래스 이름 패턴이 *Service
    @Pointcut("execution(* *..*Service.*(..))")
    private void allService() {
    }

    /**
     * hello.aop.order 패키지와 하위 패키지 이면서,
     * 클래스 이름 패턴이 *Service
     */
    @Around("allOrder() && allService()")
    public Object doTransaction(ProceedingJoinPoint joinPoint) throws Throwable {

        try {
            log.info("[트랜잭션 시작] {}", joinPoint.getSignature());
            Object result = joinPoint.proceed();
            log.info("[트랜잭션 커밋] {}", joinPoint.getSignature());
            return result;
        } catch (Exception e) {
            log.info("[트랜잭션 롤백] {}", joinPoint.getSignature());
            throw e;
        } finally {
            log.info("[리소스 릴리즈] {}", joinPoint.getSignature());
        }
    }
}
```

**`Advice 순서`**

- 어드바이스는 기본적으로 순서를 보장하지 않음
- @Order 를 사용할 수 있지만, 어드바이스 단위가 아니라 **클래스 단위로 적용** 필요
- [어드바이스 순서 지정](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/4f1815e105cdadfe0bfa83d46c21bba321b91bad)

**`Advice 종류`**

참고. 

- JoinPoint Interface 주요 기능
  - getArgs() : 메서드 인수 반환
  - getThis() : 프록시 객체 반환
  - getTarget() : 대상 객체 반환
  - getSignature() : 조언되는 메서드에 대한 설명 반환
  - toString() : 조언되는 방법에 대한 유용한 설명 반환

- ProceedingJoinPoint Interface 주요 기능
  - proceed() : 다음 어드바이스나 타켓 호출

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/aop-around.png?raw=true 'Result')

- `@Around` : 메서드 호출 전/후에 수행
  - 다른 어드바이스 기능 모두 처리(조인 포인트 실행 여부 선택, 반환 값 변환, 예외 변환 등)
  - 다음 어드바이스나 타켓 호출을 위해 ProceedingJoinPoint 사용하고, 나머지 어드바이스는 JoinPoint 사용
  - 항상 joinPoint.proceed() 호출 해야 하는 부분을 주의
- `@Before` : 조인 포인트 실행 전에 실행
  - 작업 흐름 변경 불가
  - 메서드 종료 시 다음 타켓(proceed()) 자동 호출
- `@After` : 조인 포인트가 정상 또는 예외에 관계없이 실행
  - 메서드 실행이 종료되면 실행(=finally)
  - 정상 및 예외 반환 조건을 모두 처리
  - 일반적으로 리소스 해제에 사용
- `@AfterReturning` : 조인 포인트 정상 완료 후 실행
  - returning 속성 이름은 어드바이스 메서드 매개변수 이름 일치
  - returning 절에 지정된 타입의 값(Obejct)을 반환하는 메서드만 대상
  - 반환되는 객체 변경 불가
- `@AfterThrowing` : 메서드가 예외를 던지는 경우 실행
  - @AfterReturning 특징과 동일

```java
@Before("hello.aop.order.aop.Pointcuts.orderAndService()")
public void doBefore(JoinPoint joinPoint) {
    log.info("[before] {}", joinPoint.getSignature());
}

@AfterReturning(value = "hello.aop.order.aop.Pointcuts.orderAndService()", returning = "result")
public void doReturn(JoinPoint joinPoint, Object result) {
    log.info("[return] {} return={}", joinPoint.getSignature(), result);
}

@AfterThrowing(value = "hello.aop.order.aop.Pointcuts.orderAndService()", throwing = "ex")
public void doThrowing(JoinPoint joinPoint, Exception ex) {
    log.info("[ex] {} message={}", joinPoint.getSignature(), ex.getMessage());
}

@After(value = "hello.aop.order.aop.Pointcuts.orderAndService()")
public void doAfter(JoinPoint joinPoint) {
    log.info("[after] {}", joinPoint.getSignature());
}
```

- @Around 가 가장 넓은 기능을 제공하지만, @Before, @After 와 같이 제약이 있는 어드바이스를 사용해서 명확하게 설계를 해보자.

[어드바이스 종류](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/5f4853ddf55dc2a64459739517be7f6955907998)

## 포인트컷

**`Pointcut 지시자`**

- 포인트컷 표현식(AspectJ pointcut expression)은 execution 같은 포인트컷 지시자(PCD, Pointcut Designator)로 시작
- 포인트컷 지시자 종류
  - execution : 메소드 실행 조인 포인트 매칭(가장 많이 사용하고, 기능도 복잡)
  - within : 특정 타입 내의 조인 포인트 매칭
  - args : 인자가 주어진 타입의 인스턴스인 조인 포인트
  - this : 스프링 빈 객체(스프링 AOP 프록시)를 대상으로 하는 조인 포인트
  - target : Target 객체(스프링 AOP 프록시가 가르키는 실제 대상)를 대상으로 하는 조인 포인트
  - @target : 실행 객체의 클래스에 주어진 타입의 애노테이션이 있는 조인 포인트
  - @within : 주어진 애노테이션이 있는 타입 내 조인 포인트
  - @annotation : 메서드가 주어진 애노테이션을 가지고 있는 조인 포인트를 매칭
  - @args : 전달된 실제 인수의 런타임 타입이 주어진 타입의 애노테이션을 갖는 조인 포인트
  - bean : 스프링 전용 포인트컷 지시자, 빈 이름으로 포인트컷 지정

- [예제](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/d70423e1c8db917158a6561975e035f8ead6141d)

**`execution 문법`**

- execution(modifiers-pattern? ret-type-pattern declaring-type-pattern namepattern(param-pattern) throws-pattern?)
  - execution(접근제어자패턴? 반환타입패턴 선언타입패턴? 메서드이름패턴(파라미터) 예외패턴?)
    - 메소드 실행 조인 포인트 매칭
    - `?`는 생략 가능한 패턴
    - `*` 패턴 지정 가능

패키지 패칭 규칙

  - hello.aop.member.*(1).*(2)
    - (1): 타입
    - (2): 메서드 이름
  - . : 정확하게 해당 위치의 패키지
  - .. : 해당 위치의 패키지와 그 하위 패키지도 포함

[메서드/패키지 이름 매칭](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/702beca0fe7a14c5ce4874fd823a1ab7c1faa724)

파라미터 매칭 규칙

- (String) : 정확하게 String 타입 파라미터
- () : 파라미터 없음
- (*) : 정확히 하나의 파라미터, 단 모든 타입 허용
- (*, *) : 정확히 두 개의 파라미터, 단 모든 타입 허용
- (..) : 숫자와 무관하게 모든 파라미터, 모든 타입 허용. 파라미터가 없어도 허용 (= 0..*)
- (String, ..) : String 타입으로 시작. 숫자와 무관하게 모든 파라미터, 모든 타입 허용
  - ex. (String) , (String, Xxx) , (String, Xxx, Xxx) 허용

[타입/파라미터 매칭](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/c8a41c5bcec924a1d36aa225f808d4c6ef8734f2)

**`within 지시자`**

- 특정 타입 내 조인 포인트에 대한 매칭 제한
  - 해당 타입이 매칭되면 그 안의 메서드(조인 포인트)들이 자동으로 매칭
  - execution 타입 부분만 사용
  - 부모 타입 지정 불가
  - 거의 사용하지 않고, 보통 execution 사용

[within 지시자](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/34bb387bd278b741e1d8c0571b057f0a971a20e9)

**`args 지시자`**

- 인자가 주어진 타입의 인스턴스인 조인 포인트로 매칭
- executionr vs args
  - executionr
    - 파라미터 타입의 정확한 매칭
    - 클래스에 선언된 정보(메서드 시그니처) 기반 판단 / 정적
  - args
    - 부모 타입 허용
    - 실제 넘어온 파라미터 객체 인스턴스(런타임에 전달된 인수) 기반 판단 / 동적
    - 단독으로 사용되기 보다 파라미터 바인딩에 주로 사용

[args](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/51b07aad489b3ad8253aff22e0b1f4bf003a6a51)

**`@target, @within 지시자`**

파라미터 바인딩에 함께 사용

- @target : 인스턴스 기준으로 모든 메서드의 조인 포인트를 선정
  - 부모 타입의 메서드도 적용
- @within : 선택된 클래스 내부에 있는 메서드만 조인 포인트로 선정
  - 부모 타입의 메서드는 적용되지 않음

[@target, @within](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/7c9bb26d95f1985b207eceaaeee35fe7b0e87518)

**참고.** args, @args, @target 지시자는 단독으로 사용하지 않기 !!!

- <u>**실제 객체 인스턴스가 생성, 실행될 때** 어드바이스 적용 여부를 확인 가능</u>하므로 프록시가 있어야만(실행 시점) 판단 가능
- 단, <u>프록시를 생성하는 시점은 스프링 컨테이너가 만들어지는 **애플리케이션 로딩 시점**</u>이므로 args, @args, @target 지시자는 스프링의 모든 빈에 AOP를 적용하려고 시도 -> 스프링 내부에서 사용하는 빈 중에는 final 지정 빈들도 있기 때문에 오류 발생
- 최대한 프록시 적용 대상을 축소하는 표현식(execution)과 함께 사용하기

**`@annotation, @args 지시자`**

- @annotation : 주어진 애노테이션(@MethodAop)을 가지고 있는 메서드를 조인 포인트 매칭
- @args : 런타임 타입에 전달된 인수가 주어진 타입의(@Check) 애노테이션이 있는 경우에 매칭

[@annotation, @args](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/d21728239f7da375e01fafe498bbc6be54f47ca2)

**`bean 지시자`**

- 빈 이름으로 AOP 적용 여부 지정(스프링 전용 포인트컷 지시자)

[bean](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/1e511e71f2ea7db7bf40f3731920396624cfb480)

**`this, target 지시자`**

- this : 스프링 빈으로 등록되어 있는 **프록시 객체**를 대상으로 포인트컷 매칭
- target : 스프링 AOP 프록시 객체가 가르키는 **실제 target 객체**를 대상으로 포인트컷 매칭
  - 프록시 대상인 this 는 구체 클래스 지정 시 프록시 생성 전략에 따라 다른 결과가 나올 수 있음
    - * 와 같은 패턴 사용 불가
    - 부모 타입 허용
  - 단독으로 사용되기 보다는 파라미터 바인딩에 주로 사용

[this vs target](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/d63f17c69dab0d34e0125ad86902b7bfba641d5c)

**`매개변수 전달`**

- 포인트컷 표현식을 사용해서 어드바이스에 매개변수 전달 가능
  - this, target, args,@target, @within, @annotation, @args
  - 메서드에 지정한 타입으로 제한

[매개변수 전달](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/e9492d66db3a4ca8cce749f43a6f7a0fae70fbb8)

## ⭐️ AOP 실전예제

- [상황 설정](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/d82bd97dc0a3f7bedb848de4eef24705e1eb5521)
- [로그 출력 AOP 적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/75efa570f2a14e8273ab769e3d384ae5775fc0a8)
- [재시도 AOP 적용](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/01a8498b904f1501ea5b4e3d81f259dade214d8b)

참고. 스프링의 가장 대표적인 AOP는 @Transactional

## ⭐️ 주의사항

**`프록시 방식의 AOP 한계 - 대상 객체를 직접 호출`**

- 의존관계 주입 시 프록시 객체가 주입되므로 대상 객체를 직접 호출하는 문제는 일반적으로 발생하지 않지만, 대상 객체의 내부에서 메서드 호출(자신의 인스턴스 내부 메서드 호출)이 발생하면 프록시를 거치지 않고 대상 객체를 직접 호출하는 문제 발생
- 스프링은 프록시 방식의 AOP를 사용하는데, 메서드 내부 호출에 프록시를 적용할 수 없음

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-aop-external.png?raw=true 'Result')

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-aop-internal.png?raw=true 'Result')

[프록시 방식의 AOP 한계 - 프록시 방식의 AOP의 내부 호출 문제](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/b21a0c1e92f5931f32cf9e9eedea8d1e29c44a53)


**프록시 방식의 AOP 한계. 대안 I. 자기 자신 주입**

- 자신의 인스턴스 메서드를 호출하는 것이 아니라, 프록시 인스턴스를 통해서 호출

[대안 I. 자기 자신 주입](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/410c8474e98f5fd4f5cd69378f196bee5bbf5581)

**프록시 방식의 AOP 한계. 대안 II. 지연 조회**

- ObjectProvider(Provider), ApplicationContext 사용
  - ObjectProvider : 객체 조회를 스프링 컨테이너 스프링 빈 생성 시점에서 실제 객체 사용 시점(.getObject())으로 지연

[대안 II. 지연 조회](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/d6a072aed795c64156aaea14a6c35109c2384773)

**프록시 방식의 AOP 한계. 대안 III. 구조 변경**

- 내부 호출을 별도 클래스로 분리

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-aop-alternative-class.png?raw=true 'Result')

[대안 III. 구조 변경](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/564551693131205a1faf4e8a899e84f0dbdb63d3)

**`프록시 기술의 한계`**

**타입 캐스팅**

프록시 캐스팅 문제는 의존관계 주입 시 발생

- JDK 동적 프록시 : 인터페이스 기반 프록시 생성
  - 프록시를 인터페이스로 캐스팅 가능하지만, 구체 클래스로 타입 캐스팅이 불가능(인터페이스를 구현한 프록시이므로..)
- CGLIB : 구체 클래스 기반 프록시 생성
  - 구체 클래스 기반으로 프록시가 생성되므로, 구체 클래스로 타입 캐스팅 가능

[프록시 기술의 한계 - 타입 캐스팅](https://github.com/jihunparkme/Inflearn-Spring-Core-Principles-Advanced/commit/3efd8821579d30fa299af8a2bfd898113e237139)

























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