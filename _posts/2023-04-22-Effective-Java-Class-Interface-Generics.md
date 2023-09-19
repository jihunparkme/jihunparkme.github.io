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

.

**구현과 API를 분리하는 '정보 은닉'의 장점**

- `시스템 개발 속도`를 높인다. (여러 컴포넌트를 병렬로 개발 가능)
- `시스템 관리 비용`을 낮춘다. (각 컴포넌트를 빠르게 파악, 디버깅하고, 컴포넌트 교체 부담도 적음)
- 성능을 높여주진 않지만 `성능 최적화`에 도움을 준다. (다른 컴포넌트에 영향을 주지 않고 특정 컴포넌트만 최적화 가능)
- 소프트웨어 `재사용성`을 높인다.
- 큰 시스템을 `제작하는 난이도`를 낮춰준다. (개별 컴포넌트 검증 가능)

.

**접근 수준**

각 요소의 접근성은 그 요소가 선언된 위치와 접근 제한자로 정해진다. 이 접근 제한자를 제대로 활용하는 것이 정보 은닉의 핵심!

- `private`: 멤버 선언 톱레벨 클래스에서만 접근 가능
- `package-private` (default): 멤버가 소속된 패키지 안의 모든 클래스에서 접근 가능
  - 단, interface는 public
- `protected`: package-private 접근 범위를 포함하고, 멤버를 선언한 클래스의 하위 클래스에서도 접근 가능
- `public`: 모든 곳에서 접근 가능

.

**클래스와 인터페이스의 접근 제한자 사용 원칙**

- 모든 클래스와 멤버의 `접근성을 가능한 좁혀`야 한다.
- 톱레벨 클래스와 인터페이스에 `public` 또는 `package-private`를 사용할 수 있다.
  - public으로 선언하면 API가 되므로 하위 호환성을 유지하려면 영원한 관리 필요
  - 패키지 외부에서 사용하지 않을 클래스나 인터페이스(구현체)라면 package-private으로 선언하자.
- 한 클래스에서만 사용하는 package-private 클래스나 인터페이스는 해당 클래스에 private static으로 중첩 시키자
  - 독립적인 중첩 클래스는 private static이 적합
  - private 클래스는 외부 클래스의 인스턴스를 참조

.

**멤버(필드, 메서드, 중첩 클래스/인터페이스)의 접근 제한자 원칙**

- private, package-private 멤버는 `내부 구현`(정보 은닉)
- public 클래스의 public, protected 멤버는 `공개 API`
- 테스트 코드를 위해 클래스, 인터페이스, 멤버의 접근 범위를 넓히는 것은 적당한 수준까지만 허용. 공개 API로 만들어서는 안 된다.
  - private → package-private으로 풀어주는 정도는 허용
  - 테스트를 같은 패키지에 만든다면 공개 API로 만들 필요가 없어진다.
- public 클래스의 인스턴스 필드는 되도록 public이 아니어야 한다.(아이템16)
- public 가변 필드를 갖는 클래스는 일반적으로 스레드 안전하지 않다
- 클래스에서 public static final 배열 필드를 두거나 이 필드를 반환하는 접근자 메서드를 제공해서는 안 된다.
  - 배열은 외부에서 변경이 가능한 레퍼런스 필드이므로
  - public 배열을 private으로 만들고 public 불변 리스트를 추가하거나
  - 배열을 private으로 만들고 public으로 그 복사본을 반환하자.

<br>

## item 16. public 클래스에서는 public 필드가 아닌 접근자 메서드를 사용하라.

> public 클래스는 절대 가변 필드를 직접 노출해서는 안 된다.
>
> 불변 필드라면 노출해도 덜 위험하지만 완전히 안심할 수는 없다.
>
> 하지만 package-private 클래스나 private 중첩 클래스에서는 종종 (불변이든 가변이든) 필드를 노출하는 편이 나을 때도 있다.

📖

**패키지 바깥에서 접근할 수 있는 클래스라면 접근자(getter)를 제공**함으로써 클래스 내부 표현 방식을 언제든 바꿀 수 있는 유연성을 얻을 수 있다.

- 클라이언트 코드가 필드를 직접 사용하면 캡슐화의 장점을 제공하지 못한다.
  - 필드를 변경하려면 API를 변경해야 한다.
  - 필드에 접근할 때 부수 작업을 할 수 없다.
- package-private 클래스 또는 private 중첩 클래스라면 데이터 필드를 노출해도 문제가 없다.

<br>

## item 17. 변경 가능성을 최소화하라.

> 클래스는 꼭 필요한 경우가 아니라면 불변으로 만들자.
> 
> 불변으로 만들 수 없는 클래스라면 변경할 수 있는 부분을 최소한으로 줄여보자.
> 
> 다른 합당한 이유가 없다면 모든 필드는 private final 이어야 한다.

📖

불변 클래스는 가변 클래스보다 `설계`하고 `구현`하고 `사용`하기 쉬우며, 오류가 생길 여지도 적고 훨씬 `안전`하다.
- 생성된 시점의 상태를 파괴할 때까지 그대로 간직
- 불변 객체는 근본적으로 스레드에 안전하여 따로 동기화할 필요가 없음
- 방어적 복사 불필요(불변 객체를 자유롭게 공유 가능)
- 불변 객체는 자유롭게 공유할 수 있음을 물론, 불변 객체끼리는 내부 데이터를 공유할 수 있음
- 객체를 만들 때 다른 불변 객체들을 구성요소로 사용하면 이점이 많음(Map.key, Set.element)
- 불변 객체는 그 자체로 실패 원자성을 제공
- 단점이라면, 값이 다를 경우 반드시 독립된 객체로 만들어야 함

.

**클래스를 불변으로 만들기 위한 규칙**

- 객체의 `상테를 변경하는 메서드`(변경자)를 제공하지 않기
- `클래스를 확장`(상속)할 수 없도록 하기
  - final 클래스로 선언하기
  - 생성자를 숨기고(private, package-private) 정적 팩터리 제공하기 
    ```java
    private Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }

    // 내부에서 확장 가능
    private static class MyComplex extends Complex {
        private MyComplex(double re, double im) {
            super(re, im);
        }
    }

    /**
     * 정적 팩터리 방식은 다수의 구현 클래스를 활용한 유연성을 제공
     * - 내부에서 확장된 중첩 클래스를 리턴해줄 수도 있음
     * - 객체 캐싱 기능을 추가해 성능 개선 가능
     */
    public static Complex valueOf(double re, double im) {
        return new Complex(re, im);
    }

    public static Complex myValueOf(double re, double im) {
        return new MyComplex(re, im);
    }

    ...

    Complex complex = Complex.valueOf(1, 0.222);

    /**
     * 확장이 가능한 클래스는 안전한 사용을 위해 방어적인 복사 사용
     */
    public static BigInteger safeInstance(BigInteger val) {
        return val.getClass() == BigInteger.class ? val : new BigInteger(val.toByteArray());
    }
    ```
- 모든 (외부에 공개하는) `필드를 final로` 선언하기
  - 계산 비용이 큰 값은 해당 값이 필요한 시점에 계산하여 final이 아닌 필(private)에 캐시해서 사용 가능
- 모든 `필드를 private으로` 선언하기
- 자신 외에는 `내부의 가변 컴포넌트에 접근할 수 없도록` 하기
  - 필요하다면 방어적인 복사를 통해 제공

.

**불변 클래스의 장점과 단점**

[불변 복소수 클래스(Complex.java)](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter4/item17/Complex.java)

```java
// 불변 객체는 안심하고 공유 가능
public static final Complex ZERO = new Complex(0, 0);

/**
 * 피연산자가 변경되지 않으면서 새로운 인스턴스를 생성하여 반환(함수형 프로그래밍의 특징)
 * 전달된 파라미터가 변경되지 않으므로 클라이언트도 안전하고 단순하게 사용 가능
 * 값이 다르다면 별도의 객체로 만들어야 하는 비용을 줄이기 위해 다단계 연산 제공
 */
public Complex plus(Complex c) {
    return new Complex(re + c.re, im + c.im);
}

public Complex minus(Complex c) {
    return new Complex(re - c.re, im - c.im);
}
```

장점

- 함수형 프로그래밍에 적합(피연산자에 함수를 적용한 결과를 반환하지만 피연산자가 변경되지는 않음)
- 불변 객체는 단순
- 불변 객체는 근본적으로 스레드 안전하여 따로 동기화할 필요 없음
- 불변 객체는 안심하고 공유 가능(상수, public static final)
- 불변 객체 끼리는 내부 데이터 공유 가능
- 객체를 만들 때 불변 객체로 구성하면 이점이 많음(Collection에서도 불변 유지)
- 실패 원자성을 제공(아이템 76, p407)
  - 연산이 실패하더라도 원자성을 보장(데이터 보존)

단점

- 값이 다르다면 반드시 별도의 객체로 만들어야 한다.
  - "다단계 연산"을 제공하거나, "가변 동반 클래스"(StringBuilder)를 제공하여 대처 가능

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

다른 패키지의 구체 클래스를 상속하는 일은 위험

- 메서드 호출과 달리 상속은 캡슐화를 깨뜨림
- 상위 클래스는 릴리스마다 내부 구현이 달라질 수 있고, 그로 인해 하위 클래스가 오동작할 수 있다.
  - 상위 클래스에서 제공하는 메서드 구현이 바뀐다면, 모든 하위 클래스의 구현도 변경되어야 함
  - 상위 클래스에서 새로운 메서드가 생긴다면, 알 수 없을 뿐더러 오버라이딩이 필요

.

`컴포지션`(Composition): 기존 클래스가 새로운 클래스의 구성요소로 쓰이는 설계

- 새로운 클래스를 만들고 private 필드로 기존 클래스의 인스턴스를 참조하게 하자.
- 기존 클래스의 구현이 바뀌거나, 새로운 메서드가 생기더라도 아무런 영향을 받지 않는다.
- 기존 클래스의 대응하는 메서드를 호출해 그 결과를 반환
- 상속은 반드시 하위 클래스가 상위 클래스의 '진짜' 하위 타입인 상황에서만 쓰여아 한다.
- Example
  - [잘못된 예](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter4/item18/InstrumentedHashSet.java)
  - [래퍼 클래스. 상속 대신 컴포지션 사용](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter4/item18/InstrumentedSet.java)
  - [전달 클래스](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter4/item18/ForwardingSet.java)

.

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

`@implSpec`
- 내부 동작 방식을 설명
- 메서드 주석에 @implSpec 태그를 붙여주면 자바독 도구가 생성
    ```java
    /** java.util.AbstractCollection#remove
     * 
     * {@inheritDoc}
     *
     * @implSpec
     * This implementation iterates over the collection looking for the
     * specified element.  If it finds the element, it removes the element
     * from the collection using the iterator's remove method.
     *
     * ...
     *
     */
    public boolean remove(Object o) {...}
    ```
    ```shell
    javadoc -d {target-path} {source-path}/* -tag "implSpec:a:Implementation Requirements:
    ```
- 클래스의 내부 동작 과정 중간에 끼어들 수 있는 훅을 잘 선별하여 `protected 메서드 형태로 공개`
  - **java.util.AbstractList#removeRange**
- 상속용으로 설계한 클래스는 배포 전에 반드시 `하위 클래스`를 만들어 `검증`하자.
  - 상속용 클래스를 검증하는 방법은 직접 하위 클래스를 만들어 보는 것이 유일
- 상속용 클래스의 생성자는 직접적으로든 간접적으로든 `재정의 가능 메서드를 호출해서는 안` 된다.
  - 하위 클래스의 초기화되지 않은 필드를 참조하여 예상치 못한 상황이 발생할 수 있음
- 생성자와 비슷한 맥락으로 clone, readObject 모두 직접적으로든 간접적으로든 재정의 가능 메서드를 호출해서는 안 된다.
  - Cloneable(아이템 13), Serializable(아이템 86) 구현 시 주의 필요
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

📖

인터페이스의 장점

- 자바 8부터 인터페이스도 [디폴트 메서드](https://docs.oracle.com/javase/tutorial/java/IandI/defaultmethods.html) 제공
  - 디폴트 메서드로 구현체를 깨지 않고 손쉬운 기능 확장 가능
  - 인스턴스 필드를 사용하는 경우 디폴트 메서드 제공이 불가하므로 추상 골격 클래스 사용 권장
- 인터페이스는 믹스인(mixtin) 정의에 안성맞춤(선택적인 기능 추가)
  - 기존 클래스에도 손쉽게 새로운 인터페이스 (다중)구현 가능
- 계층구조가 없는 타입 프레임워크 생성 가능
- 래퍼 클래스와 함께 사용하면 인터페이스는 기능을 향상시키는 안전하고 강력한 수단(아이템 18)
- 구현이 명백한 것은 인터페이스의 디폴트 메서드를 사용해 프로그래머의 일감을 덜어 줄 수 있음

.

추상 골격(skeletal) 클래스

- 추상 클래스처럼 구현을 도와주는 동시에, 추상 클래스로 타입을 정의할 때 따라오는 심각한 제약에서는 자유로움
- 인터페이스와 추상 클래스의 장점을 모두 소유
  - 인터페이스 → 디폴트 메서드 구현
  - 추상 골격 클래스 → 나머지 메서드 구현
  - 템플릿 메서드 패턴
- [시뮬레이트한 다중 상속](https://github.com/jihunparkme/Effective-JAVA/blob/main/effective-java-part2/src/main/java/me/whiteship/chapter04/item20/multipleinheritance/MyCat.java)
  - 인터페이스의 구현체에서 추상 클래스의 메서드 호출
- 골격 구현은 상속용 클래스이기 때문에 아이템 19를 따라야 한다.
- 단순 구현(simple implementation)은 골격 구현의 작은 변종으로, AbstractMap.SimpleEntry가 좋은 예

.

- [골격 구현을 사용해 완성한 구체 클래스](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter4/item20/IntArrays.java)
  - AbstractList 를 통해 필요한 메서드만 재정의하여 List 인터페이스 구현
  - 인터페이스와 추상클래스의 장점을 모두 소유
- [골격 구현 클래스](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter4/item20/AbstractMapEntry.java)

<br>

## item 21. 인터페이스는 구현하는 쪽을 생각해 설계하라.

> 기존 인터페이스에 디폴트 메서드로 새 메서드를 추가하는 일은 꼭 필요한 경우가 아니면 피하자.
> 
> 추가하려는 디폴트 메서드가 기존 구현체들과 충돌하지 않을지 심사숙고해야 한다.
> 
> 반면, 새로운 인터페이스를 만드는 경우라면 표준적인 메서드 구현을 제공하는 데 아주 유용한 수단이며, 
> 
> 그 인터페이스를 더 쉽게 구현해 활용할 수 있게 해준다.

📖

- 기존 인터페이스에 디폴트 메서드 구현을 추가하는 것은 위험한 일
  - 디폴트 메서드는 구현 클래스에 대해 아무것도 모른 채 합의 없이 `무작정 삽입`
  - 디폴트 메서드는 기존 구현체에 `런타임 오류`를 일으킬 수 있음
    - 동일한 스펙의 메서드를 슈퍼 클래스와 인터페이스가 가지고 있을 경우, 슈퍼 클래스의 메서드가 우선
  - `NTS`(Non-Thread Safe)
- 인터페이스를 설계할 때는 세심한 주의가 필요
  - 서로 다른 방식으로 최소한 세 가지는 구현을 해보자

생각할 수 있는 모든 상황에서 불변식을 해치지 않는 디폴트 메서드를 작성하기란 어려운 법이다.

<br>

## item 22. 인터페이스는 타입을 정의하는 용도로만 사용하라.

> 인터페이스를 상수 공개용 수단으로 사용하지 말자.

📖

클래스가 어떤 인터페이스를 구현한다는 것은 자신의 인스턴스로 무엇을 할 수 있는지를 클라이언트에 이야기해 주는 것. 인터페이스는 오직 이 용도로만 사용하자.

- 상수를 정의하는 용도로 안티패턴 인터페이스를 사용하지 말자
  - 클래스 내부에서 사용할 상수는 내부 구현에 해당
  - 내부 구현을 클래스의 API로 노출하는 행위
  - 클라이언트에 구현체에 대한 혼란 제공
- 상수를 정의하는 방법
  - 특정 클래스나 인터페이스
  - 열거형
  - 인스턴스화 할 수 없는 유틸리티 클래스 

```java
// 상수 유틸리티 클래스(권장하는 방법)
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

태그 달린 클래스의 단점
- 쓸데없이 많은 코드
  - 열거 타입, 태그 필드, switch 문, 여러 구현 혼합, 불필요한 코드
- 나쁜 가독성, 다량의 메모리 사용, 장황하고, 오류를 내기 쉽고, 비효율적
- 필드를 final로 선언하려면 불필요한 필드까지 초기화 필요
- 인스턴스 타입만으로는 현재 나타내는 의미를 알 방법이 없음

클래스 `계층 구조`로 바꾸면 모든 단점 해결

- [before](https://github.com/jihunparkme/Effective-JAVA/blob/main/effective-java-part2/src/main/java/me/whiteship/chapter04/item23/taggedclass/Figure.java)

```java
abstract class Figure {
    abstract double area();
}

...

class Circle extends Figure {
    final double radius;

    Circle(double radius) { this.radius = radius; }

    @Override double area() { return Math.PI * (radius * radius); }
}

...

class Rectangle extends Figure {
    final double length;
    final double width;

    Rectangle(double length, double width) {
        this.length = length;
        this.width  = width;
    }
    @Override double area() { return length * width; }
}

...

class Square extends Rectangle {
    Square(double side) {
        super(side, side);
    }
}
```

<br>

## item 24. 멤버 클래스는 되도록 static(정적 멤버 클래스)으로 만들라.

> 중첩 클래스에서는 네 가지가 있으며, 각각의 쓰임이 다르다.
> 
> 멤버 클래스: 메서드 밖에서도 사용해야 하거나, 메서드 안에 정의하기엔 너무 길 경우
>
> 정적 멤버 클래스: 멤버 클래스의 인스턴스 각각이 바깥 인스턴스를 참조하지 않을 경우
> 
> 비정적 멤버 클래스: 멤버 클래스의 인스턴스 각각이 바깥 인스턴스를 참조할 경우
>
> 익명 클래스: 중첩 클래스가 한 메서드 안에서만 쓰이면서 그 인스턴스를 생성하는 지점이 단 한 곳이고, 해당 타입으로 쓰기에 적합한 클래스나 인터페이스가 이미 있을 경우
> 
> 지역 클래스: 그 외의 경우.. 가장 드물게 사용

📖

**중첩 클래스는 바깥 클래스에서만 쓰여야 하며, 그 외에 쓰임새가 있다면 톱레벨 클래스로 만들자.**

- 정적 멤버 클래스(그외 클래스들은 내부 클래스(inner class))
- 비정적 멤버 클래스
- 익명 클래스
- 지역 클래스

.

**`정적 멤버 클래스`**

바깥 클래스와 함께 쓰일 때만 유용한 public 도우미 클래스. (ex. Calculator.Operation.PLUS)

```java
public class OuterClass {
    private String name = "name";

    public enum Kinds { // 열거타입은 암시적으로 static
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

- 클래스 내부에 **static** 으로 선언
- 바깥 클래스의 **private 멤버에 접근** 가능
- private 선언 시 **바깥 클래스에서만 접근** 가능
- 바깥 인스턴스와 **독립적**으로 존재할 수 있을 경우 사용
  - private 정적 멤버 클래스는 바깥 클래스가 표현하는 객체의 한 구성요소일 때 사용

.

**`비정적 멤버 클래스`**

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
            // 바깥 클래스 private 멤버 참조         
            System.out.println(name); 
        }

        public void callOuterClassMethod() {  
            // 클래스명.this로 바깥 인스턴스의 메서드나 참조 가져올 수 있음            
            OuterClass.this.testMethod();
        }
    }
}

...

// 인스턴스 생성 방법
InnerClass innerClass = new OutterClass().new InnerClass();

// 바깥 클래스의 인스턴스 메서드에서 비정적 멤버 클래스의 생성자 호출
OuterClass outerClass = new OuterClass();
InnerClass innerClass = outerClass.createInnerClass();

// 멤버 클래스를 인스턴스화
InnerClass publicSample2 = outerClass.new InnerClass();
```

- 멤버 클래스에 **static이 붙지 않은** 형태
- 바깥 클래스의 인스턴스와 **암묵적으로 연결**
  - 클래스명.this 형태로 바깥 인스턴스 접근 가능. 바깥 인스턴스 없이는 생성 불가.
- 어댑터 정의에 자주 사용
  - 어떤 클래스의 인스턴스를 감싸 다른 인스턴스처럼 보이게 하는 뷰로 사용
  - 구현체를 직접 반환하지 않고 인터페이스를 반환
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
- 주의❗️ 멤버 클래스에서 바깥 인스턴스에 접근할 일이 없으면 무조건 정적 멤버 클래스로 만들자.
  - static 생략 시...
  - 바깥 인스턴스로 숨은 외부 참조를 갖고, 멤버 클래스 관계를 위한 시간과 공간 소모
  - GC가 바깥 클래스의 인스턴스 수거 불가로 메모리 누수 발생
  - 참조가 눈에 보이지 않아 문제의 원인을 찾기 어렵고 심각한 상황을 초래

.

**`익명 클래스`**

```java
Collections.sort(list, new Comparator<Integer>() {
    @Override
    public int compare(Integer n1, Integer n2) {
        return n1 - n2;
    }
});

...

// 정적 팩터리 메서드 구현 시 사용
static List<Integer> intArrayAsList(int[] a) {
    Objects.requiredNonNull(a);
    
    return new AbstracktList<>() {
        @Override public Integer get(int i) {
            return a[i];
        }
    }
}
```

- 이름이 없는 클래스
- 바깥 클래스의 멤버가 아니며, 쓰이는 시점에 선언과 동시에 인스턴스 생성
- 제약사항
  - 선언한 지점에서만 인스턴스 생성 가능
  - instanceof 검사나 클래스 이름이 필요한 작업은 수행 불가
  - 여러 인터페이스 구현 불가, 동시에 다른 클래스 상속 불가
  - 익명 클래스의 상위 타입에서 상속한 멤버 외에는 호출 불가
  - 10줄 이하로 짧지 않으면 가독성 감소
- 람다, 메서드 레퍼런스가 역할을 대체

.

**`지역 클래스`**

```java
public class SampleClass {
    private int number = 10;
    public SampleClass() {}

    public void foo() {
        // 지역변수 클래스
        class LocalClass { 
            private String name;
            // private static int staticNumber; // 정적 멤버 가질 수 없음

            public LocalClass(String name) {
                this.name = name;
            }

            public void print() {
                // 비정적 문맥에선 바깥 인스턴스를 참조 가능
                // 단, foo()가 static이면 number에서 컴파일 에러 발생
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
- 가장 드물게 사용

[reference](https://yeonyeon.tistory.com/205)

<br>

## item 25. 톱레벨 클래스는 한 파일에 하나만 담으라.

> 소스 파일 하나에는 반드시 톱레별 클래스(혹은 톱레벨 인터페이스)를 하나만 담자.
>
> 이 규칙만 따른다면 컴파일러가 한 클래스에 대한 정의를 여러 개 만들어 내는 일은 사라진다.
>
> 소스 파일을 어떤 순서로 컴파일하든 바이너리 파일이나 프로그램의 동작이 달라지는 일은 결코 일어나지 않을 것이다.

📖

소스 파일 하나에 톱레벨 클래스를 여러 개 선언한다면, 아무런 득이 없을 뿐더러 컴파일 순서에 따라 결과가 달라질 수 있는 심각한 위험 감수 필요

💡 **해결책**

- 톱 레벨 클래스들을 서로 다른 소스 파일로 분리하기
- 여러 톱레벨 클래스를 한 파일에 담고 싶다면 `정적 멤버 클래스` 사용 고민해보기
  - 다른 클래스에 담긴 부차적 클래스라면 이 방법을 선호
  - 가독성이 좋고, private 선언 시 접근 범위도 최소화로 관리 가능

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

`로 타입`: 제네릭 타입에서 타입 매개변수를 전혀 사용하지 않을 경우(ex. List\<E\>의 로타입은 List)
- 다른 인스턴스로 넣어도 아무 오류 없이 컴파일되고 실행되지만, 원소를 꺼내기 전에는 오류를 알아내지 못하고, 코드 전체를 훑어봐야 오류를 발견 할 수 있을 것이다.
- **오류는 가능한 발생 즉시, 이상적으로는 컴파일할 때 발견하는 것이 좋다.**

.

로 타입을 사용하면 제네릭이 안겨주는 안전성과 표현력을 모두 잃게 된다.
- `안정성`: 런타임이 아닌 컴파일 타임에 문제를 찾을 수 있다.
- `표현력`: 타입 정보가 주석이 아닌 타입 선언 자체에 녹아든다.
  ```java
  // 안정성
  List<Integer> nuberms = new ArrayList<>();
  nuberms.add(10);
  nuberms.add("whiteship"); // 컴파일 오류 발생

  // 표현력
  List<Integer> nuberms = new ArrayList<>();
  ```

.

제네릭 타입을 사용하고 싶지만 실제 타입 매개변수가 무엇인지 신경 쓰고 싶지 않다면 물음표(?)를 사용하자.
- 로 타입은 안전하지 않고, 로 타입 컬렉션에는 아무 원소나 넣을 수 있으니 타입 불변식을 훼손하기 쉽다.
- 물음표는 어떤 타입이라도 담길 수 있는 가장 범용적인 매개변수화 타입 
- Collection\<?\>에는 null 외에 어떤 원소도 넣을 수 없다.(안정성)
  ```java
  static int numElementsInCommon(Set<?> s1, Set<?> s1) { ... }
  ```

.

로 타입을 사용해야 하는 경우
- 자바가 제네릭을 받아들이기 전 이미 짜여진 코드를 수용하면서 제네릭을 사용하는 새로운 코드와 맞물려 돌아가야 하므로 호환성을 위해 로 타입이 만들어졌다.
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

> 조금 복잡하더라도 와일드카드 타입을 적용하면 API가 훨씬 유연해진다.
>
> 그러니 널리 쓰일 라이브러리를 작성한다면 반드시 와일드카드 타입을 적절히 사용하자.
>
> PECS 공식을 기억하자.
>
> 즉, 생산자(produce)는 extends를 소비자(consumer)는 super를 사용한다.
>
> Comparable과 Comparator는 모두 소비자라는 사실도 잊지 말자.

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

**유연성을 극대화하려면 원소의 생산자나 소비자용 입력 매개변수에 와일드카드 타입을 사용하자.**
- 입력 매개변수가 생산자와 소비자 역할을 동시에 한다면 타입을 정확히 지정해야 하는 상황으로, 이 경우 와일드카드 타입을 사용하지 말아야 한다.
- 단, 반환 타입에는 한정적 와일드카드 타입을 사용하면 안 된다. 유연성은 커녕 클라이언트 코드에서도 와일드카드 타입을 써야 한다.
- 클래스 사용자가 와일드카드 타입을 신경 써야 한다면 그 API에 어떠한 문제가 있을 가능성이 크다.

`펙스(PECS): producer-extends, consumer-super`

- PECS 공식은 와일드카드 타입을 사용하는 기본 원칙
  
**참고.** 매개변수(parameteR)와 인수(argument)의 차이
- 매개변수: 메서드 선언에 정의한 변수
- 인수: 메서드 호출 시 넘기는 실젯값
    ```java
    void add(int value) { ... } // value = 매개변수
    add(10) // 10 = 인수
    ```

.

Comparable, Comparator은 언제나 소비자이므로, 일반적으로 `Compareable<E>` 보다는 `Compareable<? super E>` 를 사용하는 편이 낫다.

.

직접 구현한 다른 타입을 확장한 타입을 지원하기 위해 와일드카드가 필요하기도 하다.

```java
/*
ScheduledFuture는 Delayed의 하위 인터페이스고, Delayed는 Comparable<Delayed>를 확장

<<interface>>
Comparable<E>

<<interface>>
Delayed

<<interface>>
ScheduledFuture<V>
*/

...

public interface Comparable<E>
public interface Delayed extends Comparable<Delayed>
public interface ScheduledFuture<V> extends Delayed, Future<V>

...

public static <E extends Comparable<? super E>> E max(List<? extends E> list)
// Comparable 를 직접 구현하지 않고, 직접 구현한 다른 타입(Delayed)을 확장한 타입을 지원하기 위해 와일드 카드가 필요
List<ScheduledFuture<?>> scheduledFutures = max(...);
```

타입 매개변수와 와일드카드에는 공통되는 부분이 있어서, 메서드를 정의할 때 둘 중 어느 것을 사용해도 괜찮을 때가 많다.
- 비한정적 타입 매개변수
  ```java
  public static <E> void swap(List<E> list, int i, int j);
  ```
- 비한정적 와일드카드
  - public API 라면 간단한 비한정적 와일드카드를 사용하는 방법이 유리하다.
  - 메서드 선언에 타입 매개변수가 한 번만 나오면 와일드카드로 대체하자.
    ```java
    public static void swap(List<?> list, int i, int j);
    ```
  - List<?> 에는 null 외에 어떤 값도 넣을 수 없는 단점이 존재하는데, 이 경우 와일드카드 타입의 실제 타입을 알려주는 메서드를 private 도우미 메서드로 따로 작성하여 활용하자.
    ```java
    public static void swap(List<?> list, int i, int j) {
        swapHelper(list, i, j);
    }

    // 와일드카드 타입을 실제 타입으로 바꿔주는 private 도우미 메서드
    private static <E> void swapHelper(List<E> list, int i, int j) {
        list.set(i, list.set(j, list.get(i)));
    }
    ```

<br>

## item 32. 제네릭과 가변인수를 함께 쓸 때는 신중하라.

> --

📖

<br>

## item 33. 타입 안전 이종 컨테이너를 고려하라.

> --

📖

<br>

## 용어 정리

**`Serializable`** / Item 15

Serializable을 구현하면 의도치 않게 내부 정보임에도 불구하고 공개 API가 될 수 있다.

- 객체 직렬화 / Item 03 참고.

.

**`리스코프 치환 원칙`** / Item 15

하위클래스가 상위클래스의 메서드를 재정의할 때 접근 수준을 상위클래스보다 좁게 설정할 수 없다.

- 리스코프 치환 원칙 / Item 10 참고.
- ‘하위 클래스의 객체’가 ‘상위 클래스 객체’를 대체하더라도 소프트웨어의 기능을 깨트리지 않아야 한다.

.

**`자바 9 모듈 시스템`** / Item 15

JPMS(Java Platform Module System)

- [JSR-376](https://jcp.org/en/jsr/detail?id=376) 스팩으로 정의한 자바의 모듈 시스템
- 안정성
  - 순환 참조 미허용
  - 실행 시 필요한 모듈 확인
  - 한 패키지는 한 모듈에서만 공개 가능
- 캡슐화
  - public 인터페이스나 클래스라도 공개된 패키지만 사용 가능
  - 내부 구현을 보호하는 수단으로 사용 가능
- 확장성
  - 필요한 자바 플랫폼 모듈만 모아서 최적의 JRE 구성 가능
  - 작은 기기에서 구동할 애플리케이션을 개발할 때 유용

모듈이 아닌 곳에서 참조할 경우 public 인터페이스, 클래스 모두 사용 가능하다.

그렇기 때문에 모듈에서 사용할 경우에만 캡슐화의 의미가 있고, 그렇지 않은 경우 의미가 없으므로 잘 사용하지 않는다.

.

**`final과 자바 메모리 모델(JMM)`** / Item 17

final 사용 시 안전한 초기화 가능

- JMM(java memory model)
  - JMM, final의 완벽한 이해를 위해 [JLS 17.4](https://docs.oracle.com/javase/specs/jls/se14/html/jls-17.html#jls-17.4), [JLS 17.5](https://docs.oracle.com/javase/specs/jls/se14/html/jls-17.html#jls-17.5) 참고
  - 메모리 모델이 허용하는 범위 내에서 프로그램을 어떻게 실행하든 구현체(JVM)의 자유
    - 이 과정에서 실행 순서가 바뀔 수도 있음
- final 변수를 초기화 하기 전까지 해당 인스턴스를 참조하는 모든 쓰레스는 기다려야(freeze) 한다.
  - 즉, final 변수가 초기화가 되어야만 다른 스레드가 사용 가능하므로 안전한 초기화가 가능

.

**`java.util.concurrnet 패키지`** / Item 17

병행(concurrency) 프로그래밍에 유용하게 사용할 수 있는 유틸리티 묶음

- `병행`은 여러 작업을 번갈아 가며 실행
  - 마치 동시에 여러 작업을 처리하듯 보이지만, 실제로는 한번에 오직 한 작업만 실행
- `병렬`은 여러 작업을 동시에 처리
  - CPU가 여러개 있어야 가능
- 자바의 concurrent 패키지는 병행 애플리케이션에 유용한 다양한 툴을 제공
  - BlockingQueue, Callable, ConcurrrentMap, Executor, ExecutorService, Future, ...

.

**`CountDownLatch 클래스`** / Item 17

다른 여러 스레드로 실행하는 여러 오퍼레이션이 마칠 때까지 기다릴 때 사용할 수 있는 유틸리티

- java.util.concurrnet 패키지
- 초기화 할 때 숫자를 입력하고, await() 메서드를 사용해서 숫자가 0이 될때까지 대기
  ```java
  CountDownLatch startSignal = new CountDownLatch(1);
  ...
  startSignal.await();
  ```
- 숫자를 셀 때는 countDown() 메서드 사용
  ```java
  startSignal.countDown();
  ```
- 재사용할 수 있는 인스턴스가 아니고, 숫자를 리셋해서 재사용하려면 CyclicBarrier 사용
- 시작 또는 종료 신호로 사용 가능
- [ConcurrentExample.java](https://github.com/jihunparkme/Effective-JAVA/blob/main/effective-java-part2/src/main/java/me/whiteship/chapter04/item17/concurrent/ConcurrentExample.java)

.

**`데코레이터 패턴`** / Item 18

기존 코드를 변경하지 않고 부가 기능을 추가하는 패턴

- 상속이 아닌 위임을 사용해서 런타임에 보다 유연하게 부가 기능 추가 가능
- 새로운 클래스를 기존 클래스의 조합으로 만들 수 있음

.

**`콜백 프레임워크와 셀프 문제`** / Item 18

콜백 프레임워크와 래퍼를 같이 사용했을 때 발생할 수 있는 문제

콜백 함수
- 함수(A)의 인자로 전달된 함수(B)
- 함수(B)는 함수(A) 내부에서 필요한 시점에 호출 가능

SELF 문제
- 래퍼로 감싸고 있는 내부 객체가 클래스(A)의 콜백(B)으로 사용되는 경우
- this를 전달한다면, 해당 클래스(A)는 래퍼가 아닌 내부 객체를 호출
- [example](https://github.com/jihunparkme/Effective-JAVA/tree/main/effective-java-part2/src/main/java/me/whiteship/chapter04/item18/callback)

.

**`템플릿 메서드 패턴`** / Item 20

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/effective-java/template-method-pattern.png?raw=true 'Result')

알고리즘 구조를 서브 클래스가 확장할 수 있도록 템플릿으로 제공하는 패턴
- 추상 클래스는 템플릿을 제공하고, 하위 클래스는 구체적인 알고리즘을 제공

Template Method Pattern

```java
public abstract class FileProcessor {
    private String path;

    public FileProcessor(String path) {
        this.path = path;
    }

    /**
     * Template  Method
     */
    public final int process() {
        try(BufferedReader reader = new BufferedReader(new FileReader(path))) {
            int result = 0;
            String line = null;
            while((line = reader.readLine()) != null) {
                // 일부 메소드를 서브클래스로 확장 가능하도록 템플릿으로 제공
                result = getResult(result, Integer.parseInt(line));
            }
            return result;
        } catch (IOException e) {
            throw new IllegalArgumentException(path + "에 해당하는 파일이 없습니다.", e);
        }
    }

    /**
     * Step (서브 클래스에서 구체적인 기능을 확장)
     */
    protected abstract int getResult(int result, int number);
}
```

Template Callback Pattern

```java
public class FileProcessor {

    // ...

    public final int process(BiFunction<Integer, Integer, Integer> operator) {
        try(BufferedReader reader = new BufferedReader(new FileReader(path))) {
            int result = 0;
            String line = null;
            while((line = reader.readLine()) != null) {
                result = operator.apply(result, Integer.parseInt(line));
            }
            return result;
        // ...
    }
}

...

FileProcessor fileProcessor = new FileProcessor("number.txt");
System.out.println(fileProcessor.process(Integer::sum));
```

.

**`인터페이스의 디폴트 메서드로 Object 메서드를 재정의 할 수 없는 이유`** / Item 20

- 디폴트 메서드 핵심 목적은 **인터페이스의 진화**
- 두 가지 규칙
  - 클래스가 인터페이스를 이긴다.
    - 인터페이스는 어디까지나 선언이고, 디폴트 메서드도 클래스에서 오버라이딩이 가능
  - 더 구체적인 인터페이스가 이긴다.
    - 서브 인터페이스에서 재정의한 디폴트 메서드가 더 구체적
- 실용적이지 않고, 불안정
- [Allow default methods to override Object's methods](https://mail.openjdk.org/pipermail/lambda-dev/2013-March/008435.html)

.

**`ConcurrentModificationException`** / Item 21

- [ConcurrentModificationException](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/ConcurrentModificationException.html)
- 현재 변경되면 안되는 것을 수정할 때 발생하는 예외

```java
// 불변 리스트 생성
List<Integer> numbers = List.of(1, 2, 3, 4, 5);

// 가변 리스트 생성
List<Integer> numbers = new ArrayList<>();
numbers.add(1);
numbers.add(2);
numbers.add(3);
numbers.add(4);
numbers.add(5);

/**
 * fail-fast
 * 이터레이터를 사용해 콜렉션을 순회하는 중에 콜렉션이 변경될 경우 ConcurrentModificationException 발생
 * 싱글 스레드 상황에서도 발생 가능
 */
for (Integer number : numbers) {
    if (number == 3) {
        numbers.remove(number);
    }
}

/**
 * ConcurrentModificationException 피하려면 방법
 */
// 이터레이터의 remove 사용하기
for (Iterator<Integer> iterator = numbers.iterator(); iterator.hasNext();) {
    Integer integer = iterator.next();
    if(integer == 3) {
        iterator.remove();
    }
}

// 인덱스 사용하기
for (int i = 0; i < numbers.size() ; i++) {
    if (numbers.get(i) == 3) {
        numbers.remove(numbers.get(i));
    }
}

// removeIf 사용하기
numbers.removeIf(number -> number == 3);
```

.

**`Adapter Pattern`** / Item 24

기존 코드를 클라이언트가 사용하는 인터페이스의 구현체로 변경해주는 패턴
- 클라이언트가 사용하는 인터페이스를 따르지 않는 기존 코드를 재사용할 수 있도록 도움

```java
public class MySet<E> extends AbstractSet<E> {
    /**
     * 클라이언트가 사용하는 인터페이스(Iterator)를 구현하고
     * 해당 타입(Iterator<E>)으로 사용할 수 있도록 도움
     */
    @Override
    public Iterator<E> iterator() {
        return new MyIterator();
    }

    @Override
    public int size() {
        return 0;
    }

    // 클라이언트가 사용하는 인터페이스의 구현체로 변경(Adapter)
    private class MyIterator implements Iterator<E> {
        @Override
        public boolean hasNext() {
            return false;
        }

        @Override
        public E next() {
            return null;
        }
    }
}
```

.

**`GenericRepository`** / Item 26

자바 Generic을 활용한 중복 코드 제거

- [as-is](https://github.com/jihunparkme/Effective-JAVA/tree/main/effective-java-part2/src/main/java/me/whiteship/chapter05/item26/genericdao)
- to-be
  ```java
  public class GenericRepository<E extends Entity> {

      private Set<E> entities;

      public GenericRepository() {
          this.entities = new HashSet<>();
      }

      public Optional<E> findById(Long id) {
          return entities.stream().filter(a -> a.getId().equals(id)).findAny();
      }

      public void add(E entity) {
          this.entities.add(entity);
      }
  }

  ...

  public class MessageRepository extends GenericRepository<Message> {}

  ...

  public class AccountRepository extends GenericRepository<Account> {}
  ```

.

📝🔔🔍

# Reference

- [effective-java-3e-source-code (KOR)](https://github.com/WegraLee/effective-java-3e-source-code)

- [effective-java-3e-source-code (EN)](https://github.com/jbloch/effective-java-3e-source-code)
