---
layout: post
title: 클래스, 인터페이스, 제네릭
summary: 클래스와 인터페이스, 제네릭
categories: (Book)Effective-JAVA-3/E JAVA
featured-img: EFF_JAVA
# mathjax: true
---

# 4장. 클래스와 인터페이스

클래스와 인터페이스를 사용하기 편하고, 견고하며, 유연하게 만드는 방법

## item 15. 클래스와 멤버의 접근 권한을 최소화하라.

> 프로그램 요소의 접근성은 가능한 한 최소한으로 하자. 
>
> 꼭 필요한 것만 골라 최소한의 public API를 설계하자.
>
> 그 외에는 클래스, 인터페이스, 멤버가 의도치 않게 API로 공개되는 일이 없도록 해야 한다.
>
> public 클래스는 상수용 public static final 필드 외에는 어떠한 public 필드도 가져서는 안 된다. 
> 
> public static final 필드가 참조하는 객체가 불변인지 확인하자.

📖

잘 설계된 컴포넌트는 클래스 내부 데이터와 내부 구현 정보를 외부 컴포넌트로부터 얼마나 잘 숨겼는지에 달려 있다.

- 오직 API를 통해서만 다른 컴포넌트와 소통하며 서로의 내부 동작 방식에는 전혀 개의치 않는다.

**정보 은닉의 장점**

- 시스템 개발 속도를 높인다. -> 여러 컴포넌트를 병렬로 개발
- 시스템 관리 비용을 낮춘다. -> 각 컴포넌트를 빠르게 파악, 디버깅하고, 컴포넌트 교체 부담도 적음
- 성능을 높여주진 않지만 성능 최적화에 도움을 준다. -> 다른 컴포넌트에 영향을 주지 않고 특정 컴포넌트만 최적화
- 소프트웨어 재사용성을 높인다.
- 큰 시스템을 제작하는 난이도를 낮춰준다. -> 개별 컴포넌트 검증 가능

각 요소의 접근성은 그 요소가 선언된 위치와 접근 제한자로 정해진다. 이 접근 제한자를 제대로 활용하는 것이 정보 은닉의 핵심!

- 모든 클래스와 멤버의 접근성을 가능한 좁혀야 한다.
- 테스트 코드를 위해 클래스, 인터페이스, 멤버의 접근 범위를 넓히는 것은 적당한 수준까지는 괜찮지만, 공개 API로 만들어서는 안 된다.
- public 클래스의 인스턴스 필드는 되도록 public이 아니어야 한다.
- public 가변 필드를 갖는 클래스는 일반적으로 스레드 안전하지 않다.
- 클래스에서 public static final 배열 필드를 두거나 이 필드를 반환하는 접근자 메서드를 제공해서는 안 된다.
  - public 배열을 private으로 만들고 public 불변 리스트를 추가하거나
  - 배열을 private으로 만들고 public으로 그 복사본을 반환하자.

**접근 수준**

- private: 멤버 선언 톱레벨 클래스에서만 접근 가능
- package-private: 멤버가 소속된 패키지 안의 모든 클래스에서 접근 가능 (default. 단, interface는 public)
- protected: package-private 접근 범위를 포함하고, 멤버를 선언한 클래스의 하위 클래스에서도 접근 가능
- public: 모든 곳에서 접근 가능

<br>

## item 16. public 클래스에서는 public 필드가 아닌 접근자 메서드를 사용하라.

> public 클래스는 절대 가변 필드를 직접 노출해서는 안 된다.
>
> 불변 필드라면 노출해도 덜 위험하지만 완전히 안심할 수는 없다.
>
> 하지만 package-private 클래스나 private 중첩 클래스에서는 종종 (불변이든 가변이든) 필드를 노출하는 편이 나을 때도 있다.

📖

**패키지 바깥에서 접근할 수 있는 클래스라면 접근자를 제공**함으로써 클래스 내부 표현 방식을 언제든 바꿀 수 있는 유연성을 얻을 수 있다.

<br>

## item 17. 변경 가능성을 최소화하라.

> 클래스는 꼭 필요한 경우가 아니라면 불변으로 만들자.
> 
> 불변으로 만들 수 없는 클래스라면 변경할 수 있는 부분을 최소한으로 줄여보자.
> 
> 다른 합당한 이유가 없다면 모든 필드는 private final 이어야 한다.

📖

불변 클래스는 가변 클래스보다 설계하고 구현하고 사용하기 쉬우며, 오류가 생길 여지도 적고 훨씬 안전하다.
- 생성된 시점의 상태를 파괴할 때까지 그대로 간직
- 불변 객체는 근본적으로 스레드에 안전하여 따로 동기화할 필요가 없음
- 방어적 복사 불필요(불변 객체를 자유롭게 공유 가능)
- 불변 객체는 자유롭게 공유할 수 있음을 물론, 불변 객체끼리는 내부 데이터를 공유할 수 있음
- 객체를 만들 때 다른 불변 객체들을 구성요소로 사용하면 이점이 많음(Map.key, Set.element)
- 불변 객체는 그 자체로 실패 원자성을 제공
- 단점이라면, 값이 다를 경우 반드시 독립된 객체로 만들어야 함

클래스를 불변으로 만들기 위한 규칙

- 객체의 상테를 변경하는 메서드(변경자)를 제공하지 않기
- 클래스를 확장(상속)할 수 없도록 하기
  - final 클래스로 선언하기
  - 생성자를 숨기고 정적 팩터리 제공하기 
    ```java
    public static Complex valueOf(double re, double im) {
        return new Complex(re, im);
    }
    ```
- 모든 필드를 final로 선언하기
- 모든 필드를 private으로 선언하기
- 자신 외에는 내부의 가변 컴포넌트에 접근할 수 없도록 하기

[불변 복소수 클래스(Complex.java)](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter4/item17/Complex.java)

- 각 메서드에서 인스턴스 자신은 수정하지 않고 새로운 Complex 인스턴스를 만들어 반환하고 있다.
- 정적 팩터리 방식은 다수의 구현 클래스를 활용한 유연성을 제공하고, 객체 캐싱 기능을 추가해 성능을 끌어올릴 수도 있다.

<br>

## item 18. 상속보다는 컴포지션을 사용하라.

> 상속은 강력하지만 캡슐화를 해친다는 문제가 있다.
>
> 상속은 상위 클래스와 하위 클래스가 순수한 is-a 관계일 때만 써야 한다.
>
> is-a 관계일 때도 안심할 수만은 없는 게, 하위 클래스의 패키지가 상위 클래스와 다르고, 상위 클래스가 확장을 고려해 설계되지 않았다면 여전히 문제가 될 수 있다.
>
> 상속의 취약점을 피하려면 상속 대신 컴포지션과 전달을 사용하자.
>
> 특히 래퍼 클래스로 구현할 적당한 인터페이스가 있다면 더욱 그렇다.
> 
> 래퍼 클래스는 하위 클래스보다 견고하고 강력하다.

📖

- 다른 패키지의 구체 클래스를 상속하는 일은 위험하다.
- 메서드 호출과 달리 상속은 캡슐화를 깨뜨린다.
  - 상위 클래스는 릴리스마다 내부 구현이 달라질 수 있고, 그로 인해 하위 클래스가 오동작할 수 있다.
- 새로운 클래스를 만들고 private 필드로 기존 클래스의 인스턴스를 참조하게 하자.
- 컴포지션: 기존 클래스가 새로운 클래스의 구성요소로 쓰이는 설계
  - 기존 클래스의 대응하는 메서드를 호출해 그 결과를 반환
  - [래퍼 클래스. 상속 대신 컴포지션 사용](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter4/item18/InstrumentedSet.java)
- 상속은 반드시 하위 클래스가 상위 클래스의 '진짜' 하위 타입인 상황에서만 쓰여아 한다.

컴포지션 대신 상속을 사용하기로 경정하기 전에 자문해야 할 질문

- 확장하려는 클래스의 API에 아무런 결함이 없는가?
- 결함이 있다면, 이 결함이 여러분 클래스의 API까지 전파되도 괜찮은가?
- 컴포지션으로는 이런 결함을 숨기는 새로운 API를 설계할 수 있지만, 상속은 상위 클래스의 API를 '그 결함까지도'그대로 승계한다.

<br>

## item 19. 상속을 고려해 설계하고 문서화하라. 그러지 않았다면 상속을 금지하라.

> 상속용 클래스를 설계하기란 결코 만만치 않다.
>
> 클래스 내부에서 스스로를 어떻게 사용하는지(자기사용 패턴) 모두 문서로 남겨야 하며, 일단 문서화한 것은 그 클래스가 쓰이는 한 반드시 지켜야 한다.
>
> 그렇지 않으면 그 내부 구현 방식을 믿고 활용하던 하위 클래스를 오동작하게 만들 수 있다.
>
> 다른 이가 효율 좋은 하위 클래스를 만들 수 있도록 일부 메서드를 protected로 제공해야 할 수도 있다.
>
> 그러니 클래스를 확장해야 할 명확한 이유가 떠오르지 않으면 상속을 금지하는 편이 나을 것이다.
>
> 상속을 금지하려면 클래스를 final로 선언하거나 생성자 모두를 외부에서 접근할 수 없도록 만들면 된다.

상속용 클래스는 재정의할 수 있는 메서드들을 내부적으로 어떻게 이용하는지 문서로 남겨야 한다.


java.util.AbstractCollection#remove
- 내부 동작 방식을 설명
- 메서드 주석에 @implSpec 태그를 붙여주면 자바독 도구가 생성

```java
/**
 * {@inheritDoc}
 *
 * @implSpec
 * This implementation iterates over the collection looking for the
 * specified element.  If it finds the element, it removes the element
 * from the collection using the iterator's remove method.
 *
 * <p>Note that this implementation throws an
 * {@code UnsupportedOperationException} if the iterator returned by this
 * collection's iterator method does not implement the {@code remove}
 * method and this collection contains the specified object.
 *
 * @throws UnsupportedOperationException {@inheritDoc}
 * @throws ClassCastException            {@inheritDoc}
 * @throws NullPointerException          {@inheritDoc}
 */
public boolean remove(Object o) {...}
```

java.util.AbstractList#removeRange
- 클래스의 내부 동작 과정 중간에 끼어들 수 있는 훅을 잘 선별하여 protected 메서드 형태로 공개
  
```java
/**
 * Removes from this list all of the elements whose index is between
 * {@code fromIndex}, inclusive, and {@code toIndex}, exclusive.
 * Shifts any succeeding elements to the left (reduces their index).
 * This call shortens the list by {@code (toIndex - fromIndex)} elements.
 * (If {@code toIndex==fromIndex}, this operation has no effect.)
 *
 * <p>This method is called by the {@code clear} operation on this list
 * and its subLists.  Overriding this method to take advantage of
 * the internals of the list implementation can <i>substantially</i>
 * improve the performance of the {@code clear} operation on this list
 * and its subLists.
 *
 * @implSpec
 * This implementation gets a list iterator positioned before
 * {@code fromIndex}, and repeatedly calls {@code ListIterator.next}
 * followed by {@code ListIterator.remove} until the entire range has
 * been removed.  <b>Note: if {@code ListIterator.remove} requires linear
 * time, this implementation requires quadratic time.</b>
 *
 * @param fromIndex index of first element to be removed
 * @param toIndex index after last element to be removed
 */
protected void removeRange(int fromIndex, int toIndex) {
    ListIterator<E> it = listIterator(fromIndex);
    for (int i=0, n=toIndex-fromIndex; i<n; i++) {
        it.next();
        it.remove();
    }
}
```

- 상속용 클래스를 시험하는 방법은 직접 하위 클래스를 만들어 보는 것이 **유일**
- 상속용으로 설계한 클래스는 배포 전에 반드시 하위 클래스를 만들어 검증하자.
- 상속용 클래스의 생성자는 직접적으로든 간접적으로든 재정의 가능 메서드를 호출해서는 안 된다.
- clone, readObject 모두 직접적으로든 간접적으로든 재정의 가능 메서드를 호출해서는 안 된다.
- 상속용으로 설계하지 않은 클래스는 상속을 금지하자.
  - 클래스를 final 로 선언
  - 모든 생성자를 private/package-private 선언 후 public 정적 팩터리 제공
  - 좋은 예. Set, List, Map

<br>

## item 20. 추상 클래스보다는 인터페이스를 우선하라.

> 일반적으로 다중 구현용 타입으로는 인터페이스가 가장 적합
>
> 복잡한 인터페이스라면 구현하는 수고를 덜어주는 골격 구현을 함께 제공하는 방법을 꼭 고려해보자.
>
> 골격 구현은 '가능한 한' 인터페이스의 디폴트 메서드로 제공하여 그 인터페이스를 구현한 모든 곳에서 활용하도록 하는 것이 좋다.
>
> '가능한 한'의 이유는, 인터페이스에 걸려 있는 구현상의 제약 때문에 골격 구현을 추상클래스로 제공하는 경우가 더 흔하기 때문.

기존 클래스에도 손쉽게 새로운 인터페이스를 구현해 넣을 수 있다.
- 인터페이스는 믹스인(mixin, 대상 타입의 주된 기능에 선택적 기능을 혼합) 정의에 안성맞춤
- 인터페이스로는 계층구조가 없는 타입 프레임워크를 만들 수 있음
- 인터페이스는 기능을 향상시키는 안전하고 강력한 수단

골격 구현 클래스
- 추상 클래스처럼 구현을 도와주는 동시에, 추상 클래스로 타입을 정의할 때 따라오는 심각한 제약에서는 자유로움
- [골격 구현을 사용해 완성한 구체 클래스](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter4/item20/IntArrays.java)
- [골격 구현 클래스](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter4/item20/AbstractMapEntry.java)
- 단순 구현(simple implementation)은 골격 구현의 작은 변종으로, AbstractMap.SimpleEntry가 좋은 예

<br>

## item 21. 인터페이스는 구현하는 쪽을 생각해 설계하라.

> 기존 인터페이스에 디폴트 메서드로 새 메서드를 추가하는 일은 꼭 필요한 경우가 아니면 피하자.
> 
> 추가하려는 디폴트 메서드가 기존 구현체들과 충돌하지 않을지 심사숙고해야 한다.
> 
> 반면, 새로운 인터페이스를 만드는 경우라면 표준적인 메서드 구현을 제공하는 데 아주 유용한 수단이며, 그 인터페이스를 더 쉽게 구현해 활용할 수 있게 해준다.

📖

생각할 수 있는 모든 상황에서 불변식을 해치지 않는 디폴트 메서드를 작성하기란 어려운 법이다.

- 디폴트 메서드는 (컴파일에 성공하더라도) 기존 구현체에 런타임 오류를 일으킬 수 있다.
- 디폴트 메서드로 기존 인터페이스에 새로운 메서드를 추가하면 커다란 위험도 딸려온다.

<br>

## item 22. 인터페이스는 타입을 정의하는 용도로만 사용하라.

> 인터페이스는 타입을 정의하는 용도로만 사용해야 한다. 
>
> 상수 공개용 수단으로 사용하지 말자.

📖

클래스가 어떤 인터페이스를 구현한다는 것은 자신의 인스턴스로 무엇을 할 수 있는지를 클라이언트에 이야기해 주는 것이다. 인터페이스는 오직 이 용도로만 사용해야 한다.
- 상수 인터페이스 안티패턴은 인터페이스를 잘못 사용한 예(내부 구현을 클래스의 API로 노출하는 행위)
- 상수를 공개할 목적이라면 열거 타입으로 나타내기 적합한 경우 열거 타입으로 만들어 공개하고, 인스턴스화할 수 없는 유틸리티 클래스에 담아 공개하자.

```java
public class PhysicalConstants {
  private PhysicalConstants() { }  // 인스턴스화 방지

  public static final double AVOGADROS_NUMBER = 6.022_140_857e23;
  public static final double BOLTZMANN_CONST  = 1.380_648_52e-23;
  public static final double ELECTRON_MASS    = 9.109_383_56e-31;
}
```

<br>

## item 23. 태그 달린 클래스보다는 클래스 계층구조를 활용하라.

> 태그 달린 클래스를 써야 하는 상황은 거의 없다.
>
> 새로운 클래스를 작성하는 데 태그 필드가 등장한다면 태그를 없애고 계층구조로 대체하는 방법을 생각해보자.
>
> 기존 클래스가 태그 필드를 사용하고 있다면 계층구조로 리팩터링하는 것을 고민해보자.

📖

태그 달린 클래스는 쓸데없는 코드가 많다.
- 열거 타입
- 태그 필드
- switch 문
- 여러 구현이 혼합
- 불필요한 코드

태그 달린 클래스는 장황하고, 오류를 내기 쉽고, 비효율적이다.

태그 달린 클래스를 클래스 계층구조를 변환해주자.

```java
abstract class Figure {
    abstract double area();
}

class Circle extends Figure {
    final double radius;

    Circle(double radius) { this.radius = radius; }

    @Override double area() { return Math.PI * (radius * radius); }
}

class Rectangle extends Figure {
    final double length;
    final double width;

    Rectangle(double length, double width) {
        this.length = length;
        this.width  = width;
    }
    @Override double area() { return length * width; }
}

class Square extends Rectangle {
    Square(double side) {
        super(side, side);
    }
}
```

<br>

## item 24. 멤버 클래스는 되도록 static으로 만들라.

> 중첩 클래스에서는 네 가지가 있으며, 각각의 쓰임이 다르다.
> 
> ---
>
> 멤버 클래스: 메서드 밖에서도 사용해야 하거나 메서드 안에 정의하기엔 너무 길 경우
>
> 비정적 멤버 클래스: 멤버 클래스의 인스턴스 각각이 바깥 인스턴스를 참조할 경우
> 
> 정적 멤버 클래스: 멤버 클래스의 인스턴스 각각이 바깥 인스턴스를 참조하지 않을 경우
>
> 익명 클래스: 중첩 클래스가 한 메서드 안에서만 쓰이면서 그 인스턴스를 생성하는 지점이 단 한 곳이고, 해당 타입으로 쓰기에 적합한 클래스나 인터페이스가 이미 있을 경우
> 
> 지역 클래스: 그 외의 경우.. (가장 드물게 사용)

📖

**중첩 클래스는 자신을 감싼 바깥 클래스에서만 쓰여야 하며, 그 외에 쓰임새가 있다면 톱레벨 클래스로 만들어야 한다.**

- 중첩 클래스의 종류
  - 정적 멤버 클래스(정적 멤버 클래스를 제외한 클래스들은 내부 클래스(inner class))
  - 비정적 멤버 클래스
  - 익명 클래스
  - 지역 클래스

`정적 멤버 클래스`

```java
public class OuterClass {
    private String name = "name";

    public enum Kinds { // 열거타입은 암시적으로 static 선언
        A, B, C, D, E
    }

    public static class InnerClass {
        private int temp;

        public void method() {
            OuterClass outerClass = new OuterClass();
            System.out.println(outerClass.name);
        }
    }
}
```

- 클래스 내부에 static 으로 선언
- 바깥 클래스의 private 멤버에 접근 가능
- private 선언 시 바깥 클래스에서만 접근 가능
- 버깥 인스턴스와 독립적으로 존재할 수 있을 경우 사용
  - priate 정적 멤버 클래스는 바깥 클래스가 표현하는 객체의 한 구성요소일 때 사용

`비정적 멤버 클래스`

```java
public class OuterClass {
    private String name = "test";

    
    public InnerClass createInnerClass() {
        return new InnerClass();
    }

    public void testMethod() {
        System.out.println("hello world");
    }

    public class InnerClass {
        public void printName() {              
            System.out.println(name); // 바깥 클래스 private 멤버
        }

        public void callOuterClassMethod() {  
            // 클래스명.this로 바깥 인스턴스의 메서드나 참조 가져올 수 있음            
            OuterClass.this.testMethod();
        }
    }
}
```

- 멤버 클래스에 static이 붙지 않은 형태
- 바깥 클래스의 인스턴스와 암묵적으로 연결
  - 클래스명.this 형태로 바깥 인스턴스의 메서드, 인스턴스 참조 접근 가능
  - 바깥 인스턴스 없이는 생성 불가
- 어댑터 정의에 자주 사용
  - 어떤 클래스의 인스턴스를 감싸 다른 인스턴스처럼 보이게 하는 뷰로 사용
    ```java
    public class HashMap<K, V> extends AbstractMap<K, V> implements Map<K, V>, Cloneable, Serializable {

      /* Map 인터페이스의 구현체들은 보통 자신의 컬섹션 뷰를 구현할 때 비정적 멤버 클래스를 사용 */

      final class EntrySet extends AbstractSet<Map.Entry<K, V>> {
          // size(), clear(), contains(), remove(), ...
      }

      final class KeySet extends AbstractSet<K> {
          // size(), clear(), contains(), remove(), ...
      }

      final class Values extends AbstractCollection<V> {
          // size(), clear(), contains(), remove(), ...
      }
    }
    ```
- 주의❗️ 멤버 클래스에서 바깥 인스턴스에 접근할 일이 없으면 무조건 static을 붙여서 정적 멤버 클래스로 만들자
  - static 생략 시
  - 바깥 인스턴스로 숨은 외부 참조를 갖고, 멤버 클래스 관계를 위한 시간과 공간 소모
  - 가비지 컬렉션이 바깥 클래스의 인스턴스 수거 불가로 메모리 누수 발생
  - 참조가 눈에 보이지 않아 문제의 원인을 찾기 어렵고 심각한 상황을 초래
- 인스턴스 생성(멤버 클래스가 인스턴스화될 때 확립)
  ```java
  TestClass test = new TestClass();
  // 바깥 클래스의 인스턴스 메서드에서 비정적 멤버 클래스의 생성자 호출
  PublicSample publicSample1 = test.createPublicSample();
  // 바깥 인스턴스 클래스.new 멤버클래스()
  PublicSample publicSample2 = test.new InnerClass();
  ```

`익명 클래스`

```java
Collections.sort(list, new Comparator<Integer>() {
    @Override
    public int compare(Integer n1, Integer n2) {
        return n1 - n2;
    }
});
```

- 이름이 없는 클래스
- 바깥 클래스의 멤버가 아님
- 쓰이는 시점에 선언과 동시에 인스턴스 생성
- 제약사항
  - 선언한 지점에서만 인스턴스 생성 가능
  - instanceof 검사나 클래스 이름이 필요한 작업은 수행 불가
  - 여러 인터페이스 구현 불가 + 동시에 다른 클래스 상속 불가
  - 익명 클래스의 상위 타입에서 상속한 멤버 외에는 호출 불가
  - 10줄 이하로 짧지 않으면 가독성 감소
- 과거에는 즉석으로 작은 함수 객체나 처리 객체를 만드는 데 주로 사용했지만, 람다 등장 이후로 람다가 이 역할을 대체
- 정적 팩토리 메소드 구현 시 사용
  ```java
  static List<Integer> intArrayAsList(int[] a) {
      Objects.requiredNonNull(a);
      
      return new AbstracktList<>() {
          @Override public Integer get(int i) {
              return a[i];
          }
      }
  }
  ```

`지역 클래스`

```java
public class SampleClass {
    private int number = 10;
    public SampleClass() {}

    public void foo() {
        
        class LocalClass { // 지역변수 클래스
            private String name;
            // private static int staticNumber; // 정적 멤버 가질 수 없음

            public LocalClass(String name) {
                this.name = name;
            }

            public void print() {
                // 비정적 문맥에선 바깥 인스턴스를 참조 가능(foo()가 static이면 number에서 컴파일 에러)
                System.out.println(number + name);
            }
        }
        // 멤버 클래스처럼 이름이 있고 반복 사용 가능
        LocalClass localClass1 = new LocalClass("local1");
        LocalClass localClass2 = new LocalClass("local2");
    }
}
```

- 지역번수를 선언할 수 있는 곳이면 어디서든 선언 가능
- 유효 범위는 지역변수와 동일
- 다른 세 중첩 클래스와 공통점을 하나씩 보유
  - 멤버 클래스처럼 이름이 있고 반복 사용 가능
  - 익명 클래스처럼 비정적 문맥에서 사용될 떄만 바깥 인스턴스를 참조 가능, 정적 멤버는 가질 수 없으며, 가독성을 위해 짧게 작성 필요

[reference](https://yeonyeon.tistory.com/205)

<br>

## item 25. 톱레벨 클래스는 한 파일에 하나만 담으라.

> 소스 파일 하나에는 반드시 톱레별 클래스(혹은 톱레벨 인터페이스)를 하나만 담자.
>
> 이 규치만 따른다면 컴파일러가 한 클래스에 대한 정의를 여러 개 만들어 내는 일은 사라진다.
>
> 소스 파일을 어떤 순서로 컴파일하든 바이너리 파일이나 프로그램의 동작이 달라지는 일은 결코 일어나지 않을 것이다.

📖

**소스 파일 하나에 톱레벨 클래스를 여러 개 선언한다면, 아무런 득이 없을 뿐더러 심각한 위험을 감수해야 한다.**

- 어느 소스 파일을 먼저 컴파일하냐에 따라 결과가 달라지게 된다.

💡**해결책**
- 톱 레벨 클래스들을 서로 다른 소스 파일로 분리하기
- 여러 톱레벨 클래스를 한 파일에 담고 싶다면 정적 멤버 클래스 사용 고민해보기
  - 다른 클래스에 담긴 부차적 클래스라면 이 방법을 선호
  - 읽기 좋고, private 선언 시 접근 범위도 최소화로 관리가 가능

```java
public class Sample {
    public static void main(String[] args) {
        System.out.println(Utensil.NAME + Dessert.NAME);
    }

    private static class Utensil {
        static final String NAME = "pan";
    }

    private static class Dessert {
        static final String NAME = "cake";
    }
}
```

<br>

# 5장. 제네릭

제네릭을 사용하면 컬렉션이 담을 수 있는 타입을 컴파일러에 알려주게 되고, 컴파일러는 알아서 형변환 코드를 추가할 수 있게 되어 엉뚱한 타입의 객체를 넣으려는 시도를 컴파일 과정에서 차단해준다.

.

제네릭의 이점을 최대로 살리고, 단점을 최소화하는 방법

|용어|예|
|---|---|
|매개변수화 타입(parameterized type)|List\<String\>|
|실제 타입 매개변수(actual type parameter)|String|
|제네릭 타입(generic type)|List\<E\>|
|정규 타입 매개변수(formal type parameter)|E|
|비한정적 와일드 카드(unbounded wildcard type)|List\<?\>|
|로 타입(raw type)|List|
|한정적 타입 매개변수(bounded type parameter)|\<E extends Number\>|
|재귀적 타입 한정(recursive type bound)|\<T extends Comparable\<T\>\>|
|한정적 와일드 카드 타입(bounded wildcard type)|List\<? extends Number\>|
|제네릭 메서드(generic method)|static \<E\> List\<E\> asList(E[] a)|
|타입 토큰(type token)|String.class|

## item 26. 로 타입은 사용하지 말라.

> 로 타입을 사용하면 런타임에 예외가 일어날 수 있으니 사용하지 말자.
> 
> 로 타입은 제네릭이 도입되기 이전 코드와의 호환성을 위해 제공될 뿐.
>
> Set\<Object\>는 어떤 타입의 객체도 저장할 수 있는 매개변수화 타입이고, Set\<?\>는 모종의 타입 객체만 저장할 수 있는 와일드카드 타입이다.
>
> 그리고 이들의 로 타입인 Set은 제네릭 타입 시스템에 속하지 않는다.
>
> Set\<Object\>와 Set\<?\>는 안전하지만, 로 타입인 Set은 안전하지 않다.

📖

로 타입: 제네릭 타입에서 타입 매개변수를 전혀 사용하지 않을 경우(ex. List\<E\>의 로타입은 List)
- 다른 인스턴스로 넣어도 아무 오류 없이 컴파일되고 실행되지만, 원소를 꺼내지 전에는 오류를 알아내지 못 한다.
- 코드 전체를 훑어봐야 오류를 발견 할 수 있을 것이다.
- **오류는 가능한 발생 즉시, 이상적으로는 컴파일할 때 발견하는 것이 좋다.**

로 타입을 사용하면 제네릭이 안겨주는 안전성과 표현력을 모두 잃게 된다.
- 자바가 제네릭을 받아들이기 전 이미 짜여진 코드를 수용하면서 제네릭을 사용하는 새로운 코드와 맞물려 돌아가야 하므로 호환성을 위해 로 타입이 만들어졌다.

제네릭 타입을 사용하고 싶지만 실제 타입 매개변수가 무엇인지 신경 쓰고 싶지 않다면 물음표(?)를 사용하자.
- 로 타입은 안전하지 않고, 로 타입 컬렉션에는 아무 원소나 넣을 수 있으니 타입 불변식을 훼손하기 쉽다.
- 반면, Collection\<?\>에는 null 외에 어떤 원소도 넣을 수 없다.
```java
static int numElementsInCommon(Set<?> s1, Set<?> s1) { ... }
```

로 타입을 사용해야 하는 경우
- class 리터럴에는 로 타입을 사용해야 한다.
  - ex. `List.class, String[].class, int.class` 는 혀용하고, `List<String>.class, List<?>.class`는 허용하지 않는다.
- 런타임에는 제네릭 타입(List\<E\>)정보가 지워지므로 instanceof 연산자는 비한정적 와일드카드 타입(List\<?\>) 이외의 매개변수화 타입에는 적용할 수 없다.
  - 로 타입이든 비한정적 와일드카드 타입이든 instanceof는 완전히 똑같이 동작므로, 깔끔한 코드를 위해 차라리 로 타입을 쓰는 편이 깔끔하다.

```java
if (o instanceof Set) {
  Set<?> s = (Set<?>) o;
  ...
}
```

<br>

## item 27. 비검사 경고를 제거하라.

> 비검사 경고는 중요하니 무시하지 말자.
>
> 모든 비검사 경고는 런타입에 ClassCastException을 일으킬 수 있는 잠재적 가능성을 뜻하니 최선을 다해 제거하자.
>
> 경고를 없앨 방법을 찾지 못하겠다면, 그 코드가 타입 안전함을 증명하고 가능한 범위를 좁혀 @SuppressWarnings("unchecked") 애너테이션으로 경고를 숨기자.
>
> 그런 다음 경고를 숨기기로 한 근거를 주석으로 남기자.

📖

**할 수 있는 한 모든 제네릭 비검사 경고(비검사 형변환, 비검사 메서드 호출, 비검사 매개변수화 가변인수 타입, 비검사 변환 등.)를 제거하라.**

- 경고를 제거할 수는 없지만 타입 안전하다고 확신할 수 있다면 `@SuppressWarnings("unchecked")`를 달아 경고를 숨기자.
- @SuppressWarnings("unchecked")은 좁은 범위에 적용하자. 그렇지 않으면 심각한 경고를 놓칠 수 있다.
- @SuppressWarnings("unchecked") 사용 시 그 경고를 무시해도 안전한 이유를 항상 주석으로 남기자.

<br>

## item 28. 배열보다는 리스트를 사용하라.

> 배열과 제네릭에는 매우 다른 타입 규칙이 적용된다.
>
> 배열은 공변이고 실체화되는 반면, 제네릭은 불공변이고 타입 정보가 소거된다.
>
> 그 결과 배열은 런타임에는 타입 안전하지만 컴파일타임에는 그렇지 않다.
>
> 제네릭은 그 반대다. 그래서 둘이 섞어 쓰기 쉽지 않다.
>
> 둘을 섞어 쓰다가 컴파일 오류나 경고를 만나면, 가장 먼저 배열을 리스트로 대체하는 방법을 적용해보자.

📖

**배열과 제네릭 타입의 중요한 차이**

공변과 비공변
  
- 배열은 공변(covariant): 함께 변함
  - Sub가 Super의 하위 타입일 때, Sub[]는 Super[]의 하위 타입이 된다.
    ```java
    // 런타임 시점에 실패. ArrayStoreException
    Object[] objectArray = new Long[1];
    objectArray[0] = "타입이 달라 넣을 수 없음.";
    ``` 
- 제네릭은 불공면(invariant)
  - 서로 다른 타입의 Type1, Type2는 List\<Type1\>은 List\<Type2\>의 하위 타입도, 상위 타입도 아니다.
    ```java
    // 컴파일 시점에 실패
    List<Object> ol = new ArrayList<Long>();
    ol.add("타입이 달라 넣을 수 없음.")
    ```

실체화와 소거

- 배열은 실체화되어 Long 배열에 String을 넣으려 하면 ArrayStoreException 발생
- 제네릭은 타입 정보가 런타임에는 소거(erasure)

배열은 제네릭 타입, 매개변수화 타입, 타입 매개변수로 사용할 수 없다.

```java
/**
 * 배열 적용
 * choose 메서드 호출 때마다 반환된 Object를 타입 형변환해야 한다.
 * 다른 타입의 원소가 들어 있었다면 런타임에 형변환 오류가 발생
 */
public class Chooser<T> {
    private final Object choiceArray;

    public Chooser(Collection choices) {
        choiceArray = choices.toArray();
    }

    public Object choose() {
        Random rnd = ThreadLocalRandom.current();
        return choiceArray[rnd.nextInt(choiceArray.length)];
    }
}

...

/**
 * 리스트 기반
 * 타입 안전성 확보
 */
public class Chooser<T> {
    private final List<T> choiceList;

    public Chooser(Collection<T> choices) {
        choiceList = new ArrayList<>(choices);
    }

    public T choose() {
        Random rnd = ThreadLocalRandom.current();
        return choiceList.get(rnd.nextInt(choiceList.size()));
    }

    public static void main(String[] args) {
        List<Integer> intList = List.of(1, 2, 3, 4, 5, 6);

        Chooser<Integer> chooser = new Chooser<>(intList);

        for (int i = 0; i < 10; i++) {
            Number choice = chooser.choose();
            System.out.println(choice);
        }
    }
}
```

<br>

## item 29. 이왕이면 제네릭 타입으로 만들라.

> 클라이언트에서 직접 형변환해야 하는 타입보다 제네릭 타입이 더 안전하고 쓰기 편하다.
>
> 그러니 새로운 타입을 설계할 때는 형변환 없이도 사용할 수 있도록 하라.
>
> 그렇게 하려면 제네릭 타입으로 만들어야 할 경우가 많다.
>
> 기존 타입 중 제네릭이었어야 하는 게 있다면 제네릭 타입으로 변경하자. 
>
> 기존 클라이언트에는 아무 영향을 주지 않으면서, 새로운 사용자를 훨씬 편하게 해주는 길이다.

📖

일반 클래스를 제네릭 클래스로 만들기
- 클래스 선언에 타입 매개변수를 추가하기.
- 배열 타입을 적절한 타입 매개변수로 바꾸기.
  - 방법1. E와 같이 실체화 불가 타입으로 배열을 만들 수 없으므로 Obejct 배열을 생성한 후 제네릭 배열로 형변환하기
    - 가독성이 좋고, 형병환을 배열 생성 시 단 합 번만 수행. 
    - 단, 힙 오염(배열의 런타임 타입이 컴파일타임 타입과 달라서 발생하는 현상)을 일으키는 단점이 존재
    ```java
    @SuppressWarnings("unchecked")
    public Stack() {
        elements = (E[]) new Object[DEFAULT_INITIAL_CAPACITY];
    }
    ```
  - 방법2. E[] 타입에서 Object[] 타입으로 바꾸기
    - 배열에서 원소를 읽을 때마다 해줘야 형변환 필요
    - 힙 오염이 밣생하지 않음
    ```java
    private Object[] elements;

    ...

    @SuppressWarnings("unchecked") E result = (E) elements[--size];
    ```

Before

```java
public class Stack {
    private Object[] elements;
    private int size = 0;
    private static final int DEFAULT_INITIAL_CAPACITY = 16;
    
    public Stack() {
        elements = new Object[DEFAULT_INITIAL_CAPACITY];
    }

    public void push(Object e) {
        ensureCapacity();
        elements[size++] = e;
    }

    public Object pop() {
        if (size == 0)
            throw new EmptyStackException();

        result = elements[--size];
        elements[size] = null; 
        return result;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    private void ensureCapacity() {
        if (elements.length == size)
            elements = Arrays.copyOf(elements, 2 * size + 1);
    }
}
```

After

```java
public class Stack<E> {
    private E[] elements;
    private int size = 0;
    private static final int DEFAULT_INITIAL_CAPACITY = 16;

    // 배열 elements는 push(E)로 넘어온 E 인스턴스만 담는다.
    // 따라서 타입 안전성을 보장하지만, 이 배열의 런타임 타입은 E[]가 아닌 Object[]
    @SuppressWarnings("unchecked")
    public Stack() {
        elements = (E[]) new Object[DEFAULT_INITIAL_CAPACITY];
    }

    public void push(E e) {
        ensureCapacity();
        elements[size++] = e;
    }

    public E pop() {
        if (size == 0)
            throw new EmptyStackException();
        E result = elements[--size];
        elements[size] = null; // 다 쓴 참조 해제
        return result;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    private void ensureCapacity() {
        if (elements.length == size)
            elements = Arrays.copyOf(elements, 2 * size + 1);
    }

    // 코드 29-5 제네릭 Stack을 사용하는 맛보기 프로그램 (174쪽)
    public static void main(String[] args) {
        Stack<String> stack = new Stack<>();
        for (String arg : args)
            stack.push(arg);
        while (!stack.isEmpty())
            System.out.println(stack.pop().toUpperCase());
    }
}
```

<br>

## item 30. 이왕이면 제네릭 메서드로 만들라.

> 제네릭 타입과 마찬가지로, 클라이언트에서 입력 매개변수와 반환값을 명시적으로 형변환해야 하는 메서드보다 제네릭 메서드가 더 안전하며 사용하기 쉽다.
>
> 타입과 마찬가지로, 메서드도 형변환 없이 사용할 수 있는 편이 좋으며, 많은 경우 그렇게 하려면 제네릭 메서드가 되어야 한다.
>
> 타입과 마찬가지로, 형변환을 해줘야 하는 기존 메서드는 제네릭하게 만들자.
>
> 기존 클라이언트는 그대로 둔 채 새로운 사용자의 삶을 훨씬 편하게 만들어줄 것이다.

📖

```java
public static <E> Set<E> union(Set<E> s1, Set<E> s2) {
    Set<E> result = new HashSet<>(s1);
    result.addAll(s2);
    return result;
}
```
제네릭 메서드는 형변환 경고 없이 컴파일되며, 타입 안전하고, 쓰기 쉽다.
- 한정적 와일드카드 타입(`List<? extends Number>`)을 사용하면 더 유연하게 개선할 수 있다.
- 

<br>

## item 31. 한정적 와일드카드를 사용해 API 유연성을 높이라.

> --

📖

E 생산자(producer) 매개변수에 와일드카드 타입 적용

```java
public void pushAll(Iterable<? extends E> src) {
    for (E e : src)
        push(e);
}
```

E 소비자(consumer) 매개변수에 와일드카드 타입 적용
```java
public void popAll(Collection<? super E> dst) {
    while (!isEmpty())
        dst.add(pop());
}
```

유연성을 극대화하려면 원소의 생산자나 소비자용 입력 매개변수에 와일드카드 타입을 사용하자.
- 입력 매개변수가 생산자와 소비자 역할을 동시에 한다면 타입을 정확히 지정해야 하는 상황으로, 이 경우 와일드카드 타입을 사용하지 말아야 한다.



<br>

## item 32. 제네릭과 가변인수를 함께 쓸 때는 신중하라.

> --

📖

<br>

## item 33. 타입 안전 이종 컨테이너를 고려하라.

> --

📖


📝🔔🔍

...

**Reference**

- [effective-java-3e-source-code (KOR)](https://github.com/WegraLee/effective-java-3e-source-code)

- [effective-java-3e-source-code (EN)](https://github.com/jbloch/effective-java-3e-source-code)
