---
layout: post
title: 02. 객체 생성과 파괴
summary: 객체 생성과 파괴
categories: (Book)Effective-JAVA-3/E
featured-img: EFF_JAVA
# mathjax: true
---

# 2장. 객체 생성과 파괴

<br>
## item 1. 생성자 대신 정적 팩터리 메서드를 고려하라.

- 클래스는 생성자와 별도로 정적 팩터리 메서드(static factory method)를 제공할 수 있다.
```java
public static Boolean valueOf(boolean b) {
    return b ? Boolean.TRUE : Boolean.FALSE;
}
```

- Static Factory Method가 생성자보다 좋은 장점
  1. `이름`을 가질 수 있다.
     - 반환될 객체의 특성을 쉽게 묘사할 수 있음
     - 한 클래스에 시그니처가 같은 생성자가 여러 개 필요할 것 같다면, 생성자를 정적 팩터리 메서드로 바꾸고 각각의 차이를 잘 드러내는 이름을 지어주자.
  2. 호출될 때마다 `인스턴스를 새로 생성하지는 않아`도 된다.
     - 불필요한 객체 생성을 피하여 성능을 올려줄 수 있음
     - 인스턴스 통제 클래스(instance-controlled)
  3. 반환 타입의 `하위 타입 객체를 반환할 수 있는 능력`이 있다.
     - 반환할 객체의 클래스를 자유롭게 선택할 수 있음
     - 인터페이스 기반 프레임워크를 만드는 핵심 기술
  4. 입력 매개변수에 따라 `매번 다른 클래스의 객체를 반환`할 수 있다.
     - 클라이언트는 팩터리가 건네주는 객체가 어느 클래스의 인스턴스인지 알 수도 없고 알 필요도 없다.
  5. 정적 팩터리 메서드를 작성하는 시점에는 반환할 객체의 클래스가 존재하지 않아도 된다.
     - dd


