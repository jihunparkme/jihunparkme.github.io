---
layout: post
title: GoF Design Pattern
summary: GoF Design Pattern
categories: JAVA
featured-img: design-pattern
---

# GoF Design Pattern

# Creational Patterns

생성 패턴

## Singleton Patterns

`인스턴스를 오직 한개만 제공`하는 클래스

- 시스템 런타임, 환경 세팅 정보 등.. 인스턴스가 여러개일 때 이슈가 생길 수 있는 경우
- 인스턴스를 한 개만 만들어서 제공하는 클래스 필요

.

**`싱글톤 패턴을 만드는 방법`**

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

**`싱글톤 패턴을 깨뜨리는 방법`**

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

**`실무에서의 사용`**

- 스프링 빈 스코프 중 하나(싱글톤 스코프)
- java.lang.Runtime
- 다른 디자인 패턴(빌더, 퍼사드, 추상 팩토리..) 구현체의 일부 사용
