---
layout: post
title: GoF Design Pattern
summary: GoF Design Pattern
categories: JAVA
featured-img: design-pattern
---

# GoF Design Patterns

[Refactoring.Guru](https://refactoring.guru/design-patterns) 의 [Design Patterns](https://refactoring.guru/design-patterns) 주제를 정리하며 실습한 내용들을 다루는 글입니다.

.

# Creational Design Patterns

생성 디자인 패턴은 기존 코드의 유연성과 재사용을 증가시키는 `객체를 생성하는 다양한 방법`을 제공

.

## Factory Method

부모 클래스에서 객체들을 생성할 수 있는 인터페이스를 제공하지만, `자식 클래스들이 생성될 객체들의 유형을 변경`할 수 있도록 하는 생성 패턴

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/factory-method-ko-2x.png?raw=true 'Result')

.

**`Problem`**

트럭 물류 관리 어플을 개발했다.

요즘들어 어플이 유명해지면서 해상 물류 회사들로부터 해상 물류 기능을 추가해 달라는 요청이 들어오고 있다.

하지만.. 지금 대부분 코드는 트럭 클래스에 의존되어 있고, 선박 클래스를 추가하기 위해 전체 코드 베이스 변경이 필요한 상황이다. 이후 다른 유형의 물류 교통수단도 추가된다면 다시 전체 코드 베이스 수정이 필요할 것이다.

이대로라면 운송 수단 객체들이 추가될 때마다 많은 조건문들이 생겨나는 매우 복잡한 코드가 작성될텐데..

어떻게 하는게 좋을까? 😭

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/structure-2x.png?raw=true 'Result')

Factory Method Pattern은 `객체 생성 호출을 특별한 팩토리 메소드에 대한 호출로 대체`
- 자식 클래스들은 팩토리 메서드가 반환하는 객체들의 클래스를 변경 가능
  - 생성자 호출을 팩토리 메소드에게 위임하면서 자식 클래스에서 팩토리 메소드를 오버라이딩하고 생성되는 제품들의 클래스를 변경 가능
- 약간의 제한이 있지만, 자식 클래스들은 다른 유형의 제품들을 해당 제품들이 공통 기초 클래스 또는 공통 인터페이스가 있는 경우에만 반환 가능
  - ConcreteCreatorA 클래스에 포함된 팩토리 메소드는 ConcreteProductA 객체들을 반환
  - ConcreteCreatorB 클래스에 포함된 팩토리 메소드는 ConcreteProductB 객체들을 반환

.

모든 제품 클래스들이 공통 인터페이스를 구현하는 한, 제품 클래스들의 객체들을 손상시키지 않고 클라이언트 코드 작성 가능
- 클라이언트는 다양한 자식 클래스들에서 실제로 반환되는 클래스를 알지 못함
- 클라이언트는 모든 제품을 추상 클래스로 간주하고 메소드가 어떻게 동작하는지 중요하지 않음

```java
public class App {

    private static Logistics creator;

    public void initialize(String type) {
        if ("truck".equals(type)) {
            creator = new RoadLogistics();
            return;
        }

        if ("ship".equals(type)) {
            creator = new SeaLogistics();
            return;
        }

        throw new IllegalArgumentException("Unknown operating system.");
    }

    public static void main(String[] args) {
        App app = new App();

        app.initialize("truck");
        creator.planDelivery(); //=> Truck deliver

        app.initialize("ship");
        creator.planDelivery(); //=> Ship deliver
    }
}
```

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/factory-method-example.png?raw=true 'Result')

[Factory Method Pattern Practice](https://github.com/jihunparkme/GoF-Design-Pattern/commit/d5c67235c2f954912dddb713a7e062ca0f52a083)

.

**`Apply`**

- 함께 작동해야 하는 객체들의 정확한 유형들과 의존관계들을 미리 모르는 경우 사용
- 라이브러리 또는 프레임워크의 사용자들에게 내부 컴포넌트들을 확장하는 방법을 제공하고 싶을 때 사용
- 기존 객체들을 매번 재구축하는 대신 이들을 재사용하여 시스템 리소스를 절약하고 싶을 때 사용

.

**`pros and cons`**

장점.
- Creator, Product 가 강하게 결합되지 않도록 할 수 있으
- 단일 책임 원칙(SRP). 제품 생성 코드를 한 곳으로 이동
- 개방/폐쇄 원칙(OCP). 기존 클라이언트 코드를 훼손하지 않고 새로운 유형의 제품을 추가

단점.
- 패턴을 구현하기 위해 많은 (자식)클래스 생성이 필요하여 코드가 복잡해질 수 있음

.


## Abstract Factory

## Builder

## Prototype

## Singleton

.

# Structural Design Patterns

## Adapter

## Bridge

## Composite

## Decorator

## Facade

## Flyweight

## Proxy

.

# Behavioral Design Patterns

## Cain of Responsibility

## Command

## Iterator

## Mediator

## Memento

## Observer

## State

## Strategy

## Template Method

## Visitor





















생성 패턴

## Singleton Pattern

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/singleton-pattern.png?raw=true 'Result')

`인스턴스를 오직 한개만 제공`하는 클래스

- 시스템 런타임, 환경 세팅 정보 등.. 인스턴스가 여러개일 때 이슈가 생길 수 있는 경우
- 인스턴스를 한 개만 만들어서 제공하는 클래스 필요

.

**`Singleton Pattern 구현 방법`**

(1) private 생성자와 public static 메소드를 사용
- 단점. 여러 스레드가 동시에 접근할 경우 여러 인스턴스 생성 가능성 존재

```java
public class Settings {

    private static Settings instance;

    private Settings() {
    }

    public static Settings getInstance() {
        if (instance == null) {
            instance = new Settings();
        }

        return instance;
    }
}
```

(2) 동기화를 사용한 멀티쓰레드에 안전한 싱글톤 패턴
- sychronized 키워드로 해결 가능하지만 성능상 불이득 가능성 존재

```java
public static synchronized Settings getInstance() {
    if (instance == null) {
        instance = new Settings();
    }
    return instance;
}
```

(3) 이른 초기화(eager initialization)를 사용하는 방법
- 초기화에 많은 비용이 사용되었는데 해당 인스턴스가 사용되지 않을 경우 비용 낭비 발생

```java
private static final Settings INSTANCE = new Settings();
private Settings() {}
public static Settings getInstance() {
    return INSTANCE;
}
```

(4) double checked locking 이 적용된 효율적인 동기화 블럭
- 해당 클레스를 락으로 사용
- 멀티 스레드에 안전하고, 필요한 시점에 인스턴스 생성
- 복잡한 이론적인 배경

```java
private static volatile Settings3 instance;
...

public static Settings getInstance() {
    if (instance == null) {
        synchronized (Settings.class) {
            if (instance == null) {
                instance = new Settings();
            }
        }
    }
    return instance;
}
```

(5) static inner 클래스를 사용하는 방법 > `권장 방법`
- 멀티 스레드에 안전하고, 필요한 시점에 인스턴스 생성(lazy initialization)

```java
private Settings() {}

private static class SettingsHolder {
    private static final Settings SETTINGS = new Settings();
}

public static Settings getInstance() {
    return SettingsHolder.SETTINGS;
}
```

(6) enum 사용하는 방법 > `권장 방법`
- 리플렉션에서 인스턴스를 생성할 수 없도록 방어
- 단점. 클래스를 로딩하는 순간 인스턴스를 생성하고 상속 불가
- Serializable 를 기본적으로 구현
  - extends Enum implements Serializable

```java
public enum Settings {
    INSTANCE;
}
```

.

**`Singleton Pattern 깨뜨리는 방법`**

- 리플렉션 사용
  - declaredConstructor 로 newInstance() 호출 가능
- 직렬화 & 역직렬화 사용
  - 역직렬화 시 생성자를 사용해서 다시 한 번 인스턴스를 생성
  - 직렬화/역직렬화 시 사용되는 메서드에서 싱글톤 인스턴스를 반환하여 해결 가능
  
  ```java
  protected Object readResolve() {
        return getInstance();
  }
  ```

  .

**`Singleton Pattern Example`**

- 스프링 빈 스코프 중 하나(싱글톤 스코프)
- java.lang.Runtime
- 다른 디자인 패턴(빌더, 퍼사드, 추상 팩토리..) 구현체의 일부 사용

.

> [Singleton Design Pattern](https://sourcemaking.com/design_patterns/singleton)
>
> [Singleton](https://refactoring.guru/design-patterns/singleton)

.

## Factory Method Pattern

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/factory-method-pattern.png?raw=true 'Result')

구체적으로 어떤 인스턴스를 만들지는 `서브 클래스`가 정한다.
- 다양한 구현체(Product)가 있고, 그 중에서 특정한 구현체를 만들 수 있는 다양한 팩토리(Creator) 제공
- Loosely Coupled: Creator, Product 간의 느슨한 결합
- 장점) 기존 코드를 건드리지 않으면서 새로운 기능 확장 가능, 간결한 코드
- 단점) 역할을 나누면서 늘어나는 클래스

.

**`Factory Method Pattern 구현 방법`**

확장에는 열려있고, 변경에 닫혀있는 구조([OCP](https://ko.wikipedia.org/wiki/%EA%B0%9C%EB%B0%A9-%ED%8F%90%EC%87%84_%EC%9B%90%EC%B9%99), Open-Closed Principle)
- [factory-method-pattern sample](https://github.com/jihunparkme/GoF-Design-Pattern/commit/7a1e9caf0e84d54c7f906d5747491ef432c6fa32)
  
![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/factory-method-pattern-example.png?raw=true 'Result')

.

**`Factory Method Pattern Example`**

**단순한 팩토리 패턴**
- 매개변수 값 또는 메소드에 따라 각기 다른 인스턴스를 리턴하는 단순한 버전의 팩토리 패턴

`java.util.Calendar`

```java
System.out.println(Calendar.getInstance().getClass()); // class java.util.GregorianCalendar
System.out.println(Calendar.getInstance(Locale.forLanguageTag("th-TH-x-lvariant-TH")).getClass()); // class sun.util.BuddhistCalendar
System.out.println(Calendar.getInstance(Locale.forLanguageTag("ja-JP-x-lvariant-JP")).getClass()); // class java.util.JapaneseImperialCalendar
```

.

**Spring BeanFactory**
- Object 타입의 Product 를 만드는 BeanFacotry Creator
- 스프링의 가장 핵심적인 IOC

`org.springframework.beans.factory.BeanFactory`

```java
BeanFactory xmlFactory = new ClassPathXmlApplicationContext("config.xml");
String hello = xmlFactory.getBean("hello", String.class);
System.out.println(hello);

BeanFactory javaFactory = new AnnotationConfigApplicationContext(Config.class);
String hi = javaFactory.getBean("hello", String.class);
System.out.println(hi);
```

.

> [Factory Method Design Pattern](https://sourcemaking.com/design_patterns/factory_method)
>
> [Factory Method](https://refactoring.guru/design-patterns/factory-method)

.

## Abstract Factory Method Pattern

서로 관련있는 여러 객체를 만들어주는 인터페이스
- 구체적인 팩토리에서 구체적인 인스턴스를 만드는 것은 팩토리 메소드와 유사하지만 클라이언트 쪽에 초점

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/abstract-factory-method-pattern.png?raw=true 'Result')

- 구체적으로 어떤 클래스의 인스턴스(concrete product)를 사용하는지 감출 수 있음.

.

**`Abstract Factory Method Pattern 구현 방법`**

클라이언트 코드에서 구체적인 클래스의 의존성을 제거
- [abstract-factory-method-pattern sample](https://github.com/jihunparkme/GoF-Design-Pattern/commit/7ecf36d53b8a0e37ed06b18228c0b5407e451985)


![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/abstract-factory-method-pattern-sample.png?raw=true 'Result')

.

**`팩토리 메소드 패턴과 차이`**

둘 다 구체적인 객체 생성 과정을 추상화한 인터페이스 제공

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/factory-mathod.png?raw=true 'Result')

팩토리 메소드 패턴
- *팩토리를 구현하는 방법*(inheritance)에 초점
- 구체적인 객체 생성 과정을 하위 또는 구체적인 클래스로 옮기는 것이 목적

추상 팩토리 메소드 패턴
- *팩토리를 사용하는 방법*(composition)에 초점
- 관련있는 여러 객체를 구체적인 클래스에 의존하지 않고 만들 수 있게 해주는 것이 목적

.

**`Abstract Factory Method Pattern Example`**

Java Library
- javax.xml.xpath.XPathFactory#newInstance()
- javax.xml.transform.TransformerFactory#newInstance()
- javax.xml.parsers.DocumentBuilderFactory#newInstance() 

Spring 
- FactoryBean & 구현체

.

> [Abstract Factory Design Pattern](https://sourcemaking.com/design_patterns/abstract_factory)
>
> [Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory)

.

## Builder Pattern

동일한 프로세스를 거쳐 다양한 구성의 인스턴스를 만드는 방법
- 복잡한 객체를 만드는 프로세스를 독립적으로 분리

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/builder-pattern.png?raw=true 'Result')

장점)
- 만들기 복잡한 객체를 순차적으로 생성 가능. (ex. 다른 빌더 리턴)
- 복잡한 객체를 만드는 구체적인 과정을 숨길 수 있음.
- 동일한 프로세스를 통해 각기 다르게 구성된 객체 생성 가능.
- 불완전한 객체를 사용하지 못하도록 방지 가능.

단점)
- 원하는 객체를 만들려면 빌더부터 생성 필요.
- 구조가 복잡. (trade-off)

.

**`Builder Pattern 구현 방법`**

- [builder-pattern sample](https://github.com/jihunparkme/GoF-Design-Pattern/commit/2d96bf1013e6d0bf06eafb244d809d2441b17a75)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/builder-pattern-example.png?raw=true 'Result')

.

**`Builder Pattern Example`**

Java 8
- StringBuilder (Synchronized 미사용)
- Stream.Buidler

Lombok
- [@Builder](https://projectlombok.org/features/Builder)

스프링
- UriComponentsBuilder
- MockMvcWebClientBuilder
- xxxBuilder

.

> [Builder Design Pattern](https://sourcemaking.com/design_patterns/builder)
>
> [Builder](https://refactoring.guru/design-patterns/builder)

.

## Prototype Pattern

기존 인스턴스를 복제하여 새로운 인스턴스를 만드는 방법
- 복제 기능을 갖추고 있는 기존 인스턴스를 프로토타입으로 사용해 새 인스턴스 생성

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/prototype-pattern.png?raw=true 'Result')

장점)
- 복잡한 객체를 만드는 과정을 숨길 수 있음.
- 기존 객체를 복제하는 과정이 새 인스턴스를 만드는 것보다 비용(시간 또는 메모리)적인면에서 효율적일 수도 있음.
- 추상적인 타입 리턴 가능.

단점)
- 복제한 객체를 만드는 과정 자체가 복잡할 수 있음
- 특히, 순환 참조가 있는 경우

.

**`Prototype Pattern 구현 방법`**


- [builder-pattern sample](https://github.com/jihunparkme/GoF-Design-Pattern/commit/a53c2e878cb9dcd9c42a17d88c9d33823532288f)

.

**`Prototype Pattern Example`**

- Java Object class clone method
  - 컬렉션은 clone 을 지원하지 않는 추상타입으로 받을 수 있으므로 clone 보다 생성자를 통한 복사를 주로 사용
  
  ```java
  List<Student> students = new ArrayList<>();
  students.add(aaron);
  students.add(park);

  List<Student> clone = new ArrayList<>(students);
  ```
- Cloneable Interface
- [ModelMapper](https://modelmapper.org/)

  ```java
  GithubIssue githubIssue = new GithubIssue();
  githubIssue.setId(1);
  githubIssue.setTitle("This is title");

  ModelMapper modelMapper = new ModelMapper();
  GithubIssueData githubIssueData = modelMapper.map(githubIssue, GithubIssueData.class);
  ```

.

> [Prototype Design Pattern](https://sourcemaking.com/design_patterns/prototype)
>
> [Prototype](https://refactoring.guru/design-patterns/prototype)

.

# Structural Patterns

## Adapter Pattern

기존 코드를 클라이언트가 사용하는 인터페이스의 구현체로 바꿔주는 패턴
- 클라이언트가 사용하는 인터페이스를 따르지 않는 기존 코드 재사용 가능

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/adapter-pattern.png?raw=true 'Result')

.

**`Adapter 구현 방법`**

- [Adapter-pattern sample](https://github.com/jihunparkme/GoF-Design-Pattern/commit/6b04e19c02f43891635d4abc8e6b22e3ac12ea39)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/adapter-pattern-example.png?raw=true 'Result')

- Target
  - UserDetails
  - UserDetailsService
- Adapter
  - AccountUserDetailsService
  - AcconutUserDetails
- Adaptee
  - Account
  - AccountService


```java
AccountService accountService = new AccountService();
// Target target = Adapter(Adaptee) 
UserDetailsService userDetailsService = new AccountUserDetailsService(accountService);
LoginHandler loginHandler = new LoginHandler(userDetailsService);

String login = loginHandler.login("keesun", "keesun");
System.out.println(login);
```

장점)
- 기존 코드를 변경하지 않고 원하는 인터페이스 구현체를 만들어 재사용 가능 -> 패방-폐쇄 원칙(OCP, Open–closed principle)
- 기존 코드가 하던 일과 특정 인터페이스 구현체로 변환하는 작업을 각기 다른 클래스로 분리하여 관리 가능-> 단일 책임 원칙(SRP, Single Responsibility Principle)

단점)
- 새 클래스가 생기면 복잡도 증가
- 경우에 따라서 기존 코드가 해당 인터페이스를 구현하도록 수정하는 것이 좋은 선택이 될 수도 있음.

.

**`Adapter Pattern Example`**

JAVA
- java.util.Arrays#asList(T…)
- java.util.Collections#list(Enumeration)
- java.util.Collections#enumeration()
- java.io.InputStreamReader(InputStream)
- java.io.OutputStreamWriter(OutputStream)

```java
// collections
List<String> strings = Arrays.asList("a", "b", "c");
Enumeration<String> enumeration = Collections.enumeration(strings);
ArrayList<String> list = Collections.list(enumeration);

// io
try(InputStream is = new FileInputStream("input.txt");
    InputStreamReader isr = new InputStreamReader(is);
    BufferedReader reader = new BufferedReader(isr)) {
    while(reader.ready()) {
        System.out.println(reader.readLine());
    }
} catch (IOException e) {
    throw new RuntimeException(e);
}
```

Spring
- Spring Security
  - `UserDetails`, `UserDetailsService`
- Spring MVC
  - `HandlerAdpter`: 다양한 형태의 핸들러 코드를 스프링 MVC가 실행할 수 있는 형태로 변환해주는 어댑터용 인터페이스
    - 가장 흔히 사용하는 어댑터: RequestMappingHandlerAdapter

.

> [Adapter Design Pattern](https://sourcemaking.com/design_patterns/adapter)
>
> [Adapter](https://refactoring.guru/design-patterns/adapter)

.

## Bridge Pattern

추상적/구체적인 것을 분리하여 연결하는 패턴
- 하나의 계층 구조일 때보다 각기 나누었을 때 독립적인 계층 구조로 발전시킬 수 있음
- Implementation이 변경되더라도 Abstraction은 변경이 필요 없음

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/bridge-pattern.png?raw=true 'Result')

장점)
- 추상적인 코드를 구체적인 코드 변경 없이도 독립적으로 확장 가능
- 추상적인 코드와 구체적인 코드 분리 가능

단점)
- 계층 구조가 늘어나 복잡도가 증가할 수 있음

.

**`Bridge Pattern 구현 방법`**

- [builder-pattern sample](https://github.com/jihunparkme/GoF-Design-Pattern/tree/main/src/main/java/me/whiteship/designpatterns/_02_structural_patterns/_07_bridge)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/bridge-pattern-example.png?raw=true 'Result')

.

**`Bridge Pattern Example`**

JAVA
- JDBC API
  - Abstraction: DriverManager, Connection, Statement
  - Implementation: Driver
- SLF4J (로깅 퍼사드와 로거)

Spring
- Portable Service Abstraction
  - MailSender
  - PlatformTransactionManager

.

> [Bridge Design Pattern](https://sourcemaking.com/design_patterns/bridge)
>
> [Bridge](https://refactoring.guru/design-patterns/bridge)

.

## Composite Pattern

그룹 전체와 개별 객체를 동일하게 처리할 수 있는 패턴
- 클라이언트 입장에서는 전체/부분 모두 동일한 컴포넌트로 인식할 수는 계층 구조를 만든다.
  - 클라이언트는 구체적인 정보를 알 필요가 없다.
  - Part-Whole Hierarchy

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/composite-pattern.png?raw=true 'Result')

장점)
- 복잡한 트리 구조를 편리하게 사용 가능(공통 인터페이스를 구현하므로)
- 다형성과 재귀 활용 가능
- 클라이언트 코드를 변경하지 않고 새로운 엘리먼트 타입(Leaf) 추가 가능

단점)
- 트리를 만들어야 하므로(공통된 인터페이스를 정의해야 하기 때문에) 지나치게 일반화해야 하는 경우도 발생

.

**`Composite Pattern 구현 방법`**

- [Composite Pattern sample](https://github.com/jihunparkme/GoF-Design-Pattern/tree/main/src/main/java/me/whiteship/designpatterns/_02_structural_patterns/_08_composite)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/composite-pattern-example.png?raw=true 'Result')

.

**`Composite Pattern Example`**

JAVA
- Swing Library
- JSF(JavaServer Faces) Library

.

> [Composite Design Pattern](https://sourcemaking.com/design_patterns/composite)
>
> [Composite](https://refactoring.guru/design-patterns/composite)

.

## Decorator Pattern

동작을 포함하는 특수 래퍼 개체 안에 다른 개체를 배치하여 개체에 새로운 동작을 추가할 수 있는 구조 설계 패턴
- 기존 코드를 변경하지 않고 부가 기능을 추가
- 상속이 아닌 위임을 사용해서 보다 유연하게 부가 기능을 추가(런타임에도 가능)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/decorator-2x.png?raw=true 'Result')

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/decorator-pattern.png?raw=true 'Result')

.

**`Decorator Pattern 구현 방법`**

- [Decorator Pattern sample](https://github.com/jihunparkme/GoF-Design-Pattern/tree/main/src/main/java/me/whiteship/designpatterns/_02_structural_patterns/_09_decorator)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/decorator-pattern-example.png?raw=true 'Result')

장점)
- 새로운 클래스를 만들지 않고 기존 기능 조합 가능
- 컴파일 타임이 아닌 런타임에 동적으로 기능 변경 가능

단점)
- 데코레이터를 조합하는 코드가 복잡할 수 있음

.

**`Decorator Pattern Example`**

JAVA
- InputStream, OutputStream, Reader, Writer의 생성자를 활용한 Wrapper
  - InputStream < InputStreamReader < BufferedReader
- java.util.Collections가 제공하는 메소드들 활용한 Wrapper
  - checkedList
  - synchronizedList
  - unmodifiableCollection
- javax.servlet.http.HttpServletRequest/ResponseWrapper : 서블릿 요청/응답 랩퍼

Spring
- BeanDefinitionDecorator : Bean 설정 데코레이터
- ServerHttpRequestDecorator : WebFlux Http 요청 데코레이터
- ServerHttpResponseDecorator : WebFlux Http 응답 데코레이터

.

> [Decorator Design Pattern](https://sourcemaking.com/design_patterns/decorator)
> 
> [Decorator](https://refactoring.guru/design-patterns/decorator)

















## -- Pattern

![Result]( 'Result')

.

**`-- 구현 방법`**

- [Pattern sample]()

![Result]( 'Result')

.

**`-- Pattern Example`**

.

> [xxx](https://sourcemaking.com/design_patterns)
> 
> [xxx](https://refactoring.guru/design-patterns/)




