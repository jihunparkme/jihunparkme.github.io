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

**Static Factory Method가 생성자보다 좋은 장점**

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

**Static Factory Method의 단점**

1. 상속을 하려면 public이나 protected생성자가 필요하니 정적 팩터리 메서드만 제공하면 `하위 클래스를 만들 수 없다.`
2. 정적 팩터리 메서드는 `프로그래머가 찾기 어렵다.`

**정적 팩터리 메서드에 흔히 사용하는 명명 방식**

- `from` : 매개변수를 하나 받아서 해당 타입의 인스턴스를 반환하는 형변환 메서드
  - `Date d = Date.from(instant);
- `of` : 여러 매개변수를 받아 적합한 타입의 인스턴스를 반환하는 집계 메서드
  - `Set<Rank> faceCards = EnumSet.of(JACK, QUEEN, KING);`
- `valueOf` : from과 of의 더 자세한 버전
  - `BigInteger prime = BigInteger.valueOf(Integer.MAX_VALUE);`
- `instance` or `getInstance` : 매개변수로 명시한 인스턴스를 반환하지만, 같은 인스턴스임을 보장하지 않음
  - `StackWalker luke = StackWalker.getInstance(options);`
- `create` or `newInstance` : instance 혹은 getInstance와 같지만, 매번 새로운 인스턴스를 생성해 반환함을 보장
  - `Object newArray = Array.newIntance(classObject, arrayLen);`
- `getType` : getInstance와 같으나, 생성할 클래스가 아닌 다른 클래스에 팩터리 메서드를 정의할 경우 사용
  - `FileStore fs = Files.getFileStore(path)
- `newType` : newInstance와 같으나, 생성할 클래스가 아닌 다른 클래스에 팩터리 메서드를 정의할 경우 사용
  - `BufferedReader br = Files.newBufferedReader(path);`
- `type` : getType과 newType의 간결한 버전
  - `List<Complaint> litany = Collections.list(legacyLitany);`

> 정적 팩터리 메서드와 public 생성자는 각자의 쓰임새가 있으니 상대적인 장단점을 이해하고 사용하는 것이 좋다.
>
> 그렇다고 하더라도 정적 팩터리를 사용하는 게 유리한 경우가 더 많으므로 무작정 public 생성자를 제공하던 습관이 있다면 고치자 !!!

<br>

## item 2. 생성자에 매개변수가 많다면 빌더를 고려하라.

- 


