---
layout: post
title: 03. 모든 객체의 공통 메서드
summary: 모든 객체의 공통 메서드
categories: (Book)Effective-JAVA-3/E JAVA
featured-img: EFF_JAVA
# mathjax: true
---

# 3장. 모든 객체의 공통 메서드

## item 10. equals는 일반 규약을 지켜 재정의하라.

equals 메서드의 재정의에는 함정이 도사리고 있는데, 이 문제를 회피하는 가장 쉬운 길은 아예 재정의를 하지 않는 것.

🔍아래 상황 중 하나에 해당한다면 equals 메서드를 재정의하지 않는 것이 최선

- **각 인스턴스가 본질적으로 고유할 경우**
    - 값을 표현하는 것이 아닌 동작하는 개체를 표현하는 클래스(ex. Thread)
- **인스턴스의 '논리적 동치성'을 검사할 일이 없을 경우**
- **상위 클래스에서 재정의한 equals가 하위 클래스에도 딱 들어맞을 경우**
    - Set, List, Map 구현체들은 상속을 받아 그대로 사용
- **클래스가 private, package-private이고 equals 메서드를 호출할 일이 없을 경우**
    - equals가 실수로라도 호출되는 것을 막고 싶다면 아래와 같이 구현해두자.

```java
@Override public boolean equals(Object o) {
    throw new AssertioniError(); // 호출 금지!
}
```

🔍equals를 재정의해야 하는 경우

- 객체 식별성이 아닌 논리적 동치성을 확인해야 하는데, 상위 클래스의 equals가 논리적 동치성을 비교하도록 재정의되지 않았을 경우
  - (ex. 주로 값 클래스. Integer, String ..)
- 값 클래스라 해도, 값이 같은 인스턴스가 둘 이상 만들어지지 않음을 보장하는 인스턴스 통제 클래스라면 equals를 재정의하지 않아도 된다. (ex. Enum)

🔍equals 메서드를 재정의할 때는 반드시 일반 규약을 따라야 함

- equals 메서드는 동치관계(equivalence relation)를 만족하며 다섯 가지 요건을 만족
  - 동치관계: 집합을 서로 같은 원소들로 이뤄진 부분집합으로 나누는 연산
    - 이 부분집합들을 동치류(equivalence class; 동치 클래스)라고 함
  
**`반사성(reflexivity)`**
- null이 아닌 모든 참조 값 x에 대해, x.equals(x)는 true다.
- 객체는 자기 자신과 같아야 한다.

**`대칭성(symmetry)`**
- null이 아닌 모든 참조 값 x, y에 대해, x.equals(y)가 true면 y.equals(x)도 true다.
- 두 객체는 서로에 대한 동치 여부에 똑같이 답해야 한다.
  - equals 규약을 어기면 그 객체를 사용하는 다른 객체들이 어떻게 반응할지 알 수 없다.

[📝 대칭성 위배 코드](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter3/item10/CaseInsensitiveString.java)

📝 대칭성을 위배하지 않는 코드

```java
private final String s;
// ...
@Override public boolean equals(Object o) {
    return o instanceof CaseInsensitiveString &&
        ((CaseInsensitiveString) o).s.equalsIgnoreCase(s);
}
```

**`추이성(transitivity)`**
- null이 아닌 모든 참조 값 x, y, z에 대해, x.equals(y)가 true고, y.equals(z)도 true면 x.equals(z)도 true다.
- 첫 번째 객체와 두 번째 객체가 같고, 두 번째 객체와 세 번째 객체가 같다면, 첫 번째 객체와 세 번째 객체도 같아야 한다.
  - 구체 클래스를 확장해 새로운 값을 추가하면서 equals 규약을 만족시킬 방법은 존재하지 않는다.

[📝equals 규약을 지키면서 값 추가하기 (상속 대신 컴포지션을 사용)](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter3/item10/composition/ColorPoint.java)

`일관성(consistency)`
- null이 아닌 모든 참조 값 x, y에 대해, x.equals(y)를 반복해서 호출하면 항상 true를 반환하거나 항상 false를 반환한다.
- 두 객체가 같다면 앞으로도 영원히 같아야 한다.
  - 클래스가 불변이든 가변이든 equals의 판단에 신뢰할 수 없는 자원이 끼어들게 해서는 안 된다.
  - 모든 객체가 null과 같지 않아야 한다.

`null-아님`
- null이 아닌 모든 참조 값 x에 대해, x.equals(null)은 false다.

📝명시적 null 검사는 불필요

```java
@Override public boolean equals(Object o) {
    // equals가 타입을 확인하지 않으면 잘못된 타입이 인수로 주어졌을 때,
    // ClassCastException을 던져 일반 규약을 위배
    if (o == null)
        return false;
    // ...
}
```

📝묵시적 null 검사를

```java
@Override public boolean equals(Object o) {
    // null이 인수로 주어지면 false를 반환
    if (!(o instanceof MyType))
        return false;
    MyType mt = (MyType) o;
    // ...
}
```

🔍**양질의 equals 메서드 구현 방법**

1. `== 연산자를 사용해 입력이 자기 자신의 참조인지 확인한다.`
   - 자기 자신이면 true 반환
2. `instanceof 연산자로 입력이 올바른 타입인지 확인한다.`
3. `입력을 올바른 타입으로 형변환한다.`
4. `입력 객체와 자기 자신의 대응되는 핵심필드들이 모두 일치하는지 하나씩 검사한다.`

- Float.compare()와 Double.compare()을 제외한 기본 타입 필드는 == 연산자로 비교
- equals의 성능을 위해 다를 가능성이 더 크거나 비교 비용이 싼 필드를 먼저 비교하자.
- equals를 다 구현했다면 `대칭적`, `추이성`, `일관적`인지 자문해보자.

📝전형적인 equals 메서드의 예

```java
public final class PhoneNumber {
    private final short areaCode, prefix, lineNum;

    public PhoneNumber(int areaCode, int prefix, int lineNum) {
        this.areaCode = rangeCheck(areaCode, 999, "지역코드");
        this.prefix   = rangeCheck(prefix,   999, "프리픽스");
        this.lineNum  = rangeCheck(lineNum, 9999, "가입자 번호");
    }

    private static short rangeCheck(int val, int max, String arg) {
        if (val < 0 || val > max)
            throw new IllegalArgumentException(arg + ": " + val);
        return (short) val;
    }

    @Override public boolean equals(Object o) { // 입력 타입은 반드시 Object (다중정의)
		// 필드들의 동치성만 검사해도 equals 규약을 어렵지 않게 지킬 수 있다.
        if (o == this) return true;
        if (!(o instanceof PhoneNumber)) return false;

        PhoneNumber pn = (PhoneNumber)o;
        return pn.lineNum == lineNum && pn.prefix == prefix
                && pn.areaCode == areaCode;
    }

    // equals를 재정의할 땐 hashCode도 반드시 재정의하자!
}
```

🔔

> 꼭 필요한 경우가 아니면 equals를 재정의하지 말자.
> 많은 경우에 Object의 equals가 여러분이 원하는 비교를 정확히 수행해준다.
> 재정의해야 할 때는 그 클래스의 핵심 필드 모두를 빠짐없이,
> 다섯 가지 규약을 확실히 지켜가며 비교해야 한다.

<br>

## item 11. equals를 재정의하려거든 hashCode도 재정의하라

- equals를 재정의한 클래스 모두에서 hashCode도 재정의해야 한다.

**Object 명세에서 발췌한 규약**

- equals 비교에 사용되는 정보가 변경되지 않았다면, 애플리케이션이 실행되는 동안 그 객체의 hashCode 메서드는 몇 번을 호출해도 일관되게 항상 같은 값을 반환해야 한다.
- equals(Object)가 두 객체를 같다고 판단했다면, 두 객체의 hashCode는 똑같은 값을 반환해야 한다.
- equals(Object)가 두 객체를 다르다고 판단했더라도, 두 객체의 hashCode가 서로 다른 값을 반환할 필요는 없다. 단, 다른 객체에 대해서는 다른 값을 반환해야 해시테이블의 성능이 좋아진다.

**좋은 hashCode를 작성하는 간단한 요령**

1. int 변수 result를 선언한 후 값 c로 초기화한다. 이때 c는 해당 객체의 첫번째 핵심 필드를 단계 2.a 방식으로 계산한 해시코드다. (여기서 핵심 필드란 equals 비교에 사용되는 필드)
2. 해당 객체의 나머지 핵심 필드 f 각각에 대해 다음 작업을 수행한다.
   - a. 해당 필드의 해시코드 c를 계산한다.
     - 기본 타입 필드라면, Type.hashCode(f)를 수행한다. 여기서 Type은 해당 기본 타입의 박싱 클래스다.
     - 참조 타입 필드면서 이 클래스의 equals 메서드가 이 필드의 equals를 재귀적으로 호출해 비교한다면, 이 필드의 hashCode를 재귀적으로 호출한다. 계산이 더 복잡해질 것 같다면, 이 필드의 표준형을 만들어 그 표준형의 hashCode를 호출한다. 필드의 값이 null이면 보통 0을 사용)
     - 필드가 배열이라면, 핵심 원소 각각을 별도 필드처럼 다룬다. 이상의 규칙을 재귀적으로 적용해 각 핵심 원소의 해시코드를 계산한 다음, 단계 2.b 방식으로 갱신한다. 배열에 핵심 원소가 하나도 없다면 단순히 상수를 사용한다. 모든 원소가 핵심 원소라면 Arrays.hashCode를 사용한다.
   - b. 단계 2.a에서 계산한 해시코드 c로 result를 갱신한다. 코드로는 다음과 같다. `result = 31 * result + c;`
3. result를 반환한다.

- hashCode를 다 구현했다면 이 메서드가 동치인 인스턴스에 대해 똑같은 해시코드를 반환할지 자문해보자.
- 단계 2.b의 곱셈 31 \* result는 필드를 곱하는 순서에 따라 result 값이 달라지게 한다.
  - (31은 홀수이면서 소수이기 때문에 사용)

📝 전형적인 hashCode 메서드

```java
// 전화번호에 hashCode 부여
@Override public int hashCode() {
    int result = Short.hashCode(areaCode);
    result = 31 * result + Short.hashCode(prefix);
    result = 31 * result + Short.hashCode(lineNum);
    return result;
}
```

📝 한 줄짜리 hashCode 메서드 (성능이 아쉬움)

```java
@Override public int hashCode() {
    // 인수를 담기 위한 배열 생성, 박싱-언박싱 등으로 느리다.
    return Object.hash(lineNum, prefix, areaCode);
}
```

📝 해시코드를 지연(lazy initialization) 초기화하는 hashCode 메서드 (스레드 안정성까지 고려해야 함)

```java
private int hashCode; // 자동으로 0으로 초기화된다.

@Override public int hashCode() {
    int result = hashCode;
    if (result == 0) {
        result = Short.hashCode(areaCode);
        result = 31 * result + Short.hashCode(prefix);
        result = 31 * result + Short.hashCode(lineNum);
        hashCode = result;
    }
    return result;
}
```

🔔

> equals를 재정의할 때는 hashCode도 반드시 재정의해야 한다.
> 그렇지 않으면 프로그램이 제대로 동작하지 않을 것이다.
> 재정의한 hashCode는 Object의 API 문서에 기술된 일반 규약을 따라야 하며, 서로 다른 인스턴스라면 되도록 해시코드도 서로 다르게 구현해야 한다.
> 이렇게 구현하기가 어렵지는 않지만 조금 따분한 일이긴 하다.
> 하지만 AutoValue 프레임워크를 사용하면 멋진 equals와 hashCode를 자동으로 만들어준다.

<br>

## item 12. toString을 항상 재정의하라.

- toString을 잘 구현한 클래스는 사용하기에 훨씬 즐겁고, 그 클래스를 사용한 시스템은 디버깅하기 쉽다.
- 실전에서 toString은 그 객체가 가진 주요 정보 모두를 반환하는 게 좋다.

📝 포맷을 명시한 경우

```java
public final class PhoneNumber {
    //..

    /**
     * 단점은 평생 이 포맷에 얽매이는 점.
     *
     * 이 전화번호의 문자열 표현을 반환한다.
     * 이 문자열은 "XXX-YYY-ZZZZ" 형태의 12글자로 구성된다.
     * XXX는 지역 코드, YYY는 프리픽스, ZZZZ는 가입자 번호다.
     * 각각의 대문자는 10진수 숫자 하나를 나타낸다.
     *
     * 전화번호의 각 부분의 값이 너무 작아서 자릿수를 채울 수 없다면,
     * 앞에서부터 0으로 채워나간다. 예컨대 가입자 번호가 123이라면
     * 전화번호의 마지막 네 문자는 "0123"이 된다.
     */
    @Override public String toString() {
        return String.format("%03d-%03d-%04d", areaCode, prefix, lineNum);
    }
}
```

🔔

> 모든 구체 클래스에서 Object의 toString을 재정의하자.
> 상위 클래스에서 이미 알맞게 재정의한 경우는 예외다. toString을 재젖의한 클래스는 사용하기도 즐겁고 그 클래스를 사용한 시스템을 디버깅하기 쉽게 해준다.
> toString은 해당 객체에 관한 명확하고 유용한 정보를 읽기 좋은 형태로 반환해야 한다.

<br>

## item 13. clone 재정의는 주의해서 진행하라.

- Cloneable을 구현한 클래스의 인스턴스에서 clone을 호출하면 그 객체의 필드들을 하나하나 복사한 객체를 반환하며, 그렇지 않은 클래스의 인스턴스에서 호출하면 CloneNotSupportedException을 던진다.

📝 가변 상태를 참조하지 않는 클래스용 clone 메서드

```java
public final class PhoneNumber implements Cloneable {
    // ...
    @Override public PhoneNumber clone() {
        try {
            // 재정의한 메서드의 반환 타입은 상위 클래스의 메서드가 반환하는 타입의 하위 타입일 수 있다.
            return (PhoneNumber) super.clone();
        } catch (CloneNotSupportedException e) {
            throw new AssertionError();  // 일어날 수 없는 일이다.
        }
    }
}
```

- clone 메서드는 사실상 생성자와 같은 효과를 낸다.
  - clone은 원본 객체에 아무런 해를 끼치지 않는 동시에 복제된 객체의 불변식을 보장해야 한다.

📝 가변 상태를 참조하는 클래스용 clone 메서드

```java
public class Stack {
    private Object[] elements;
    private int size = 0;
    // ...

    @Override public Stack clone() {
    try {
	    Stack result = (Stack) super.clone();
        // elements 필드가 복사본과 같은 메모리를 참조하지 않도록 배열의 clone을 재귀적으로 호출
        result.elements = elements.clone();
        return result;
    } catch (CloneNotSupportedException e) {
        throw new AssertionError();
    }
}
```

📝 복잡한 가변 상태를 갖는 클래스용 재귀적 clone 메서드

```java
public class HashTable implements Cloneable {
    private Entry[] buckets = ...;

    private static class Entry {
        final Object key;
        Object value;
        Entry next;

        Entry(Object key, Object value, Entry next) {
            this.key = key;
            this.value = value;
            this.next = next;
        }

        // 1. 이 엔트리가 가리키는 연결 리스트를 재귀적으로 복사
        // 재귀 호출로 리스트가 길면 stackOverFlow를 일으킬 위험
        Entry deepCopyRecursion() {
            return new Entry(key, value, next == null ? null : next.deepCopy());
        }

        // 2. 재귀 호출의 stackOverFlow 문제를 피하기 위해 반복자를 사용
        Entry deepCopy() {
            Entry result = new Entry(key, value, next);
            for (Entry p = result; p.next != null; p = p.next) {
                p.next = new Entry(p.next.key, p.next.value, p.next.next);
            }
            return result;
        }

        @Override public HashTable clone() {
            try {
                HashTable result = (HashTable) super.clone();
                result.bucket = new Entry[buckets.length];
                for (int i = 0; i < buckets.length; i++) {
                    if (buckets[i] != null) {
                        result.buckets[i] = buckets[i].deepCopy();
                    }
                }
                return result;
            } catch (CloneNotSupportedException e) {
                throw new AssertionError();
            }
        }

        // ..
    }
}
```

- Cloneable을 구현하는 모든 클래스는 clone을 재정의해야 한다.
- 복사 생성자와 복사 팩터리는 더 나은 객체 복사 방식을 제공할 수 있다.
  - 장점.
  - 문서화된 규약에 기대지 않고, 정상적인 final 필드 용법과 충돌하지 않고, 불필요한 검사 예외를 던지지 않고, 형변환도 필요하지 않고, ...
  - 해당 클래스가 구현한 interface 타입의 인스턴스를 인수로 받을 수 있음
  - 클라이언트는 원본의 구현 타입에 얽매이지 않고 복제본의 타입을 직접 선택할 수 있음

📝 복사 생성자 (변환 생성자, conversion constructor)

```java
// 자신과 같은 클래스의 인스턴스를 인수로 받는 생성자
public Yum(Yum yum) {
    //..
}
```

📝 복사 팩터리 (변환 팩터리, conversion factory)

```java
// 복사 생성자를 모방한 정적 팩터리
public static Yum newInstance(Yum yum) {
    // ..
}
```

> Cloneable이 몰고 온 모든 문제를 되짚어봤을 때,
> 새로운 인터페이스를 만들 때는 절대 Cloneable을 확장해서는 안 되며, 새로운 클래스도 이를 구현해서는 안 된다.
> final 클래스라면 Cloneable을 구현해도 위험이 크지 않지만, 성능 최적화 관점에서 검토한 후 별다른 문제가 없을 때만 드물게 혀용해야 한다.
> 기본 원칙은 '복제 기능은 생성자와 팩터리를 이용하는 게 최고 !!' 라는 것이다.
> 단, 배열만은 clone 메서드 방식이 가장 깔끔한, 이 규칙의 합당한 예외라고 할 수 있다.

<br>

## item 14. Comparable을 구현할지 고려하라.

- 알파벳, 숫자, 연대 같이 순서가 명확한 값 클래스를 작성한다면 반드시 Comparable 인터페이스를 구현하자.

```java
public interface Comparable<T> {
    int compareTo(T t);
}
```

- compareTo 메서드의 일반 규약은 equals의 규약과 비슷
  - Comparable을 구현한 클래스는 모든 x,y에 대한 sgn(x.compareTo(y)) == -sgn(y.compareTo(x))여야 한다.
    - 따라서, x.compareTo(y)는 y.compareTo(x)가 예외를 던질 때에 한해 예외를 던져야 한다.
  - Comparable을 구현한 클래스는 추이성을 보장해야 한다.
  - Comparable을 구현한 클래스는 모든 z에 대해 x.compareTo(y) == 0 이면 sgn(x.compareTo(z)) == sgn(y.compareTo(z))
  - (x.compareTo(y) == 0) == (x.equals(y))여야 한다.

📝 기본 타입 필드가 여럿일 때의 비교자

```java
public int compareTo (PhoneNumber pn) {
    int result = Short.compare(areaCode, pn.areaCode);	// 가장 중요한 필드
    if (result == 0) {
        result = Short.compare(prefix, pn.prefix);	// 두 번째로 중요한 필드
        if (result == 0) {
         	result = Short.compare(lineNum, pn.lineNum);	// 세 번째로 중요한 필드
        }
    }
    return result;
}
```

📝 비교자 생성 메서드를 활용한 비교자

- 자바의 정적 임포트 기능을 이용하면 정적 비교자 생성 메서드들을 그 이름만으로 사용할 수 있어 코드가 훨씬 깔끔해진다.

```java
private static final Comparator<PhoneNumber> COMPARATOR =
    	comparingInt((PhoneNumber pn) -> pn.areaCode)
    		.thenComparingInt(pn -> pn.prefix)
    		.thenComparingInt(pn -> pn.lineNum);

public int compareTo(PhoneNumber pn) {
    return COMPARATOR.compare(this, pn);
}
```

-

📝🔔🔍

- [effective-java-3e-source-code (KOR)](https://github.com/WegraLee/effective-java-3e-source-code)

- [effective-java-3e-source-code (EN)](https://github.com/jbloch/effective-java-3e-source-code)
