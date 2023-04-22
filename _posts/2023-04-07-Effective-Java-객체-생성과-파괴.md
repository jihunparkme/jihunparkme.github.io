---
layout: post
title: 02. 객체 생성과 파괴
summary: 객체 생성과 파괴
categories: (Book)Effective-JAVA-3/E JAVA
featured-img: EFF_JAVA
# mathjax: true
---

# 객체 생성과 파괴

## item 1. 생성자 대신 정적 팩터리 메서드를 고려하라.

- 클래스는 생성자와 별도로 정적 팩터리 메서드(static factory method)를 제공할 수 있다.

```java
public static Boolean valueOf(boolean b) {
    return b ? Boolean.TRUE : Boolean.FALSE;
}
```

**장점**

1. `이름`을 가질 수 있다.
   - 반환될 객체의 특성을 쉽게 묘사 가능
2. 호출될 때마다 `인스턴스를 새로 생성하지 않아`도 된다.
   - 불필요한 객체 생성을 피하여 성능을 올려줄 수 있음
   - 인스턴스 통제 클래스(instance-controlled)
3. 반환 타입의 `하위 타입 객체를 반환할 수 있는 능력`이 있다.
   - 반환할 객체의 클래스를 자유롭게 선택할 수 있는 유연성 보유
   - 인터페이스 기반 프레임워크를 만드는 핵심 기술
4. 입력 매개변수에 따라 `매번 다른 클래스의 객체를 반환`할 수 있다.
   - 클라이언트는 팩터리가 건네주는 객체가 어느 클래스의 인스턴스인지 알 수도 없고 알 필요도 없다.
   - EnumSet.java
   ```java
   public static <E extends Enum<E>> EnumSet<E> noneOf(Class<E> elementType) {
        Enum<?>[] universe = getUniverse(elementType);
        if (universe == null)
            throw new ClassCastException(elementType + " not an enum");

        if (universe.length <= 64)
            return new RegularEnumSet<>(elementType, universe);
        else
            return new JumboEnumSet<>(elementType, universe);
    }
   ```
5. 정적 팩터리 메서드를 작성하는 시점에는 반환할 객체의 클래스가 존재하지 않아도 된다.

**단점**

1. 상속을 하려면 public 이나 protected 생성자가 필요하니 정적 팩터리 메서드만 제공하면 `하위 클래스를 만들 수 없다.`
2. 정적 팩터리 메서드는 `프로그래머가 찾기 어렵다`.

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

🔔
> 정적 팩터리 메서드와 public 생성자는 각자의 쓰임새가 있으니 상대적인 장단점을 이해하고 사용하는 것이 좋다.
>
> 그렇다고 하더라도 정적 팩터리를 사용하는 게 유리한 경우가 더 많으므로 무작정 public 생성자를 제공하던 습관이 있다면 고치자.

<br>

## item 2. 생성자에 매개변수가 많다면 빌더를 고려하라.

**빌더 패턴**

- 점층적 생성자 패턴의 안전성과 자바 빈즈 패턴의 가독성을 겸비한 패턴
- 클라이언트는 필요한 객체를 직접 만드는 대신, 필수 매개변수만으로 생성자를 호출해 빌더 객체를 얻는다.
  - 그 후 빌더 객체가 제공하는 일종의 세터 메서드들로 원하는 선택 매개변수들을 설정

[📝 점층적 생성자 패턴과 자바빈즈 패턴의 장점만 적용](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter2/item2/builder/NutritionFacts.java)

- 빌더 패턴은 계층적으로 설계된 클래스와 함께 사용하기 좋다.
  - 각 계층의 클래스에 관련 빌더를 멤버로 정의
  - 추상 클래스는 추상 빌더를, 구체 클래스는 구체 빌더를 갖도록 하자.
- 빌더를 이용하면 가변인수 매개변수를 여러 개 사용할 수도 있다.

[📝 계층적으로 설계된 클래스와 잘 어울리는 빌더 패턴](https://github.com/WegraLee/effective-java-3e-source-code/tree/master/src/effectivejava/chapter2/item2/hierarchicalbuilder)

**빌더의 단점**

  - 빌더 생성 비용이 크지는 않지만 성능에 민감한 상황에서는 문제가 될 수 있음
  - 점층적 생성자 패턴보다는 코드가 장황해서 매개변수 4개 이상은 되어야 값어치를 함

🔔
> 생성자나 정적 팩터리가 처리해야 할 매개변수가 많다면 빌더 패턴을 선택하는 게 더 낫다.
> 
> 매개변수 중 다수가 필수가 아니거나 같은 타입이면 특히 더 그렇다.
> 
> 빌더는 점층적 생성자보다 클라이언트 코드를 읽고 쓰기가 훨씬 간결하고, 자바빈즈보다 훨씬 안전하다.

<br>

## item 3. private 생성자나 열거 타입으로 싱글턴임을 보증하라.

싱클턴을 만드는 방식

**public static final 방식의 싱글턴**

- public, protected 생성자가 없으므로 클래스 초기화 시 만들어진 인스턴스가 전체 시스템에서 하나뿐임을 보장
 - 해당 클래스가 싱글턴인 것이 API에 명백히 드러남(final 이므로 다른 객체 참조 불가)
 - 간결함

```java
public class Elvis {
    public static final Elvis INSTANCE = new Elvis();
    private Elvis() { }

    public void leaveTheBuilding() { ... }
}

..

Elvis elvis = Elvis.INSTANCE;
elvis.leaveTheBuilding();
```

**정적 팩터리 방식의 싱글턴**

- API 변경 없이 싱글턴이 아니도록 변경 가능
- 정적 팩터리를 제네릭 싱글턴 팩터리로 만들 수 있음
- 정적 팩터리의 메서드 참조를 공급자(Supplier<>)로 사용할 수 있음

```java
public class Elvis {
    private static final Elvis INSTANCE = new Elvis();
    private Elvis() { }
    public static Elvis getInstance() { return INSTANCE; }

    public void leaveTheBuilding() { ... }        
}

..

Elvis elvis = Elvis.getInstance();
elvis.leaveTheBuilding();
```

참고.

- 위 두 방식으로 싱글턴 클래스를 직렬화하려면 모든 인스턴스 필드를 일시적이라고 선언하고 readResolve 메서드를 제공 필요
  - 이렇게 하지 않을 경우 직렬화된 인스턴스를 역직렬화할 때마다 새로운 인스턴스가 생성.

```java
private Object readResolve() {
    // 진짜 Elvis를 반환하고, 가짜 Elvis는 가비지 컬렉터에..
    return INSTANCE;
}
```

**원소가 하나인 열거 타입을 선언**

 - public 필드 방식과 비슷하지만, 더 간결하고, 추가 노력 없이 직렬화 가능.
 - 아주 복잡한 직렬화 상황이나 리플렉션 공격에서도 제 2의 인스턴스가 생기는 일을 완벽하게 방어
 - <u>*대부분 상황에서 원소가 하나뿐인 열거 타입이 싱글턴을 만드는 가장 좋은 방법*</u>
 - 단, 만들려는 싱글턴이 Enum 이외의 클래스를 상속해야 한다면 이 방법은 사용할 수 없음.

```java
public enum Elvis {
    INSTANCE;

    public void leaveTheBuilding() { ... }
}

..

Elvis elvis = Elvis.INSTANCE;
elvis.leaveTheBuilding();
```

🔔
> 만들려는 싱글턴이 Enum 이외의 클래스를 상속하지 않는다면, "원소가 하나인 열거 타입을 선언" 방식을 선택해 보자.

<br>

## item 4. 인스턴스화를 막으려거든 private 생성자를 사용하라.

- 추상 클래스로 만드는 것으로는 인스턴스화를 막을 수 없다. (기본 생성자가 자동으로 생성)
- 컴파일러가 기본 생성자를 만드는 경우는 오직 명시된 생성자가 없을 때뿐이니 <u>*private 생성자를 추가하면 클래스의 인스턴스화를 막을 수 있다.*</u>
- ex. 인스턴스를 만들 수 없는 유틸리스 클래스

```java
public class UtilityClass {
    // 기본 생성자가 만들어지는 것을 방지(인스턴스화 방지로 상속 불가능)
    private UtilityClass() {
        throw new AssertionError();
    }
    // ...
}
```

<br>

## item 5. 자원을 직접 명시하지 말고 의존 객체 주입을 사용하라.

- 사용하는 자원에 따라 동작이 달라지는 클래스에는 정적 유틸리티 클래스나 싱글턴 방식이 비적합
- 대신 클래스가 `여러 자원 인스턴스를 지원`해야 하며, `클라이언트가 원하는 자원`을 사용해야 한다.
- 이 패턴은 바로! <u>*인스턴스를 생성할 때 생성자에 필요한 자원을 넘겨주는 방식*</u>의 `의존 객체 주입 패턴`
- 의존 객체 주입 프레임워크(Dagger, Guice, Spring)를 사용하면 큰 프로젝트에서 코드가 어지러워지는 단점 개선 가능

```java
public class SpellChecker {
    private final Lexicon dictionary;
    // 생성자에 필요한 자원을 넘겨준다.
    public SpellChecker(Lexicon dictionary) {
        this.dictionary = Object.requireNonNull(dictionary);
    }
    
    public boolean isValid(String word) { ... }
    public List<String> suggestions(String typo) { ... }
}
```

🔔
> 클래스가 내부적으로 하나 이상의 자원에 의존하고, 그 자원이 클래스 동작에 영향을 준다면 
> 싱글턴과 정적 유틸리티 클래스는 사용하지 않는 것이 좋다.
> 
> 이 자원들을 클래스가 직접 만들게 해서도 안 된다.
> 
> 대신 필요한 자원을(혹은 그 자원을 만들어주는 팩터리를) 생성자에(혹은 정적 팩터리나 빌더에) 넘겨주자.
> 
> 의존 객체 주입이라 하는 이 기법은 클래스와의 유연성, 재사용성, 테스트 용이성을 기막히게 개선해준다.

<br>

## item 6. 불필요한 객체 생성을 피하라.

- 똑같은 기능의 객체를 매번 생성하기보다 `객체 하나를 재사용`하는 편이 나을 때가 만다.
- 생성자 대신 정적 팩터리 메서드를 제공하는 불변 클래스에서는 정적 팩터리 메서드를 사용해 불필요한 객체 생성을 피할 수 있다. (ex.Boolean.valueOf(String))
  - 생성자는 호출할 때마다 새로운 객체를 만들지만, 팩터리 메서드는 그렇지 않다.

비싼 객체가 반복해서 필요하다면 캐싱해서 재사용해보자.
- 인스턴스를 클래스 초기화 과정에서 직접 생성해 캐싱해두고, 나중에 해당 인스턴스를 재사용할 수 있다.

```java
// 값비싼 객체를 재사용해 성능을 개선
public class RomanNumerals {
    private static final Pattern ROMAN = Pattern.compile(
                "^(?=.)M*(C[MD]|D?C{0,3})"
                + "(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$");

    static boolean isRomanNumeralFast(String s) {
        return ROMAN.matcher(s).matches();
    }
}
```

박싱된 기본 타입보다는 기본 타입을 사용하고, 의도치 않은 오토박싱이 숨어들지 않도록 주의하자.

```java
// Long으로 선언해서 불필요한 인스턴스가 약 2^31개나 만들어진다.
private static long sum() {
    Long sum = 0L; 
    for (long i = 0; i <= Integer.MAX_VALUE; i++)
        sum += i;
    return sum;
}
```

## item 7. 다 쓴 객체 참조를 해제하라.

가비지 컬렉션 언어에서는 메모리 누수를 찾기가 아주 까다로움

- 메모리 누수로 단 몇 개의 객체가 매우 많은 객체를 회수되지 못하게 할 수 있고, 잠재적으로 성능에 악영향을 줄 수 있음
- 해법은 해당 참조를 다 썻을 때 null 처리(참조 해제)
- 참조 해제의 더 좋은 방법은 <u>*그 참조를 담은 변수를 유효 범위 밖으로 밀어내는 것*</u>

자기 메모리를 직접 관리하는 클래스(ex. Stack)라면 항시 메모리 누수에 주의

- 해당 참조를 다 썻을 때 `null 처리(참조 해제)`

메모리 누수의 두 번째 주범은 캐시

- LinkedHashMap 의 removeEldestEntry 메서드로 처리

메모리 누수의 세 번째 주범은 리스너(listener) 혹은 콜백(callback)

- 약한 참조로 저장(WeakHashMap에 Key로 저장)하면 가비지 컬렉터가 즉시 수거


🔔
> 메모리 누수는 겉으로 잘 드러나지 않아 시스템에 수년간 잠복하는 사례도 있다.
> 
> 이런 누수는 철저한 코드 리뷰나 힙 프로파일러 같은 디버깅 도구를 동원해야만 발견되기도 한다.
> 
> 그래서 이런 종류의 문제는 예방법을 익혀두는 것이 매우 중요하다.

<br>

## item 8. finalizer와 cleaner 사용을 피하라.

자바는 두 가지 객체 소멸자를 제공

- finalizer는 예측할 수 없고, 상황에 따라 위험할 수 있어 일반적으로 불필요
- cleaner는 finalizer보다는 덜 위험하지만, 여전히 예측할 수 없고, 느리고, 일반적으로 불필요
- finalizer와 cleaner로는 제때 수행되어야 하는 작업은 절대 할 수 없음
  - 즉시 수행된다는 보장이 없고, 가비지 컬렉터 알고리즘에 달려있어 가비지 컬렉터 구현마다 천차만별
- 상태를 영구적으로 수정하는 작업에서는 절대 finalizer, cleaner에 의존하지 말자
- finalizer와 cleaner는 심각한 성능 문제도 동반
- finalizer를 사용한 클래스는 finalizer 공격에 노출되어 심각한 보안 문제를 일으킬 수도 있음
  - final이 아닌 클래스를 finalizer 공격으로부터 방어하려면 아무 일도 하지 않는 finalize 메서드를 만들고 final로 선언하기

.

cleaner와 finalizer의 사용

1. 자원의 소유자가 close 메서드를 호출하지 않는 것에 대비한 안전망 역할
2. Native peer와 연결된 객체에서 자원을 즉시 회수해야 한다면 close 메서드를 사용 (Native peer는 자바 객체가 아니라 가비지 컬렉터는 그 존재를 알지 못함)

[📝 cleaner를 안전망으로 활용하는 AutoCloseable Class](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter2/item8/Room.java)
- cleaner 동작은 구현하기 나름이고 청소가 이뤄질지는 보장하지 않음

[📝 cleaner 안전망을 갖춘 자원을 제대로 활용하는 클라이언트](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter2/item8/Adult.java)

[📝 cleaner 안전망을 갖춘 자원을 제대로 활용하지 못하는 클라이언트](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter2/item8/Teenager.java)

🔔
> cleaner(java8 까지는 finalizer)는 안전망 역할이나 중요하지 않은 네이티브 자원 회수용으로만 사용하자.
> 
> 물론 이런 경우라도 불확실성과 성능 저하에 주의해야 한다.

<br>

## item 9. try-finally 보다는 try-with-resources를 사용하라.

- 자원 닫기는 클라이언트가 놓치기 쉬워서 예측할 수 없는 성능 문제로 이어지기도 한다.
- try-with-resources 구조를 사용하려면 해당 자원이 AutoCloseable 인터페이스를 구현해야 한다.

📝복수의 자원을 처리하는  try-with-resources 짧고 매혹적
- 프로그래머에게 보여줄 예외 하나만 보존되고 여러 개의 다른 예외가 숨겨짐
- 숨겨진 예외들도 스택 추적 내역에 숨겨졌다는 꼬리표를 달고 출력
- catch 절을 사용해서 다수 예외 처리 가능

```java
static void copy(String src, String dst) throws IOException {
    try (InputStream   in = new FileInputStream(src);
         OutputStream out = new FileOutputStream(dst)) {
        byte[] buf = new byte[BUFFER_SIZE];
        int n;
        while ((n = in.read(buf)) >= 0)
            out.write(buf, 0, n);
    }
}
```

🔔

> 꼭 회수해야 하는 자원을 다룰 때는 try-finally 말고, try-with-resources를 사용하자.
> 
> 예외는 없다. 코드는 더 짧고 분명해지고, 만들어지는 예외 정보도 훨씬 유용하다.
> 
> try-finally로 작성하면 실용적이지 못할 만큼 코드가 지저분해지는 경우라도, 
> try-with-resources로 정확하고 쉽게 자원을 회수할 수 있다.

📝🔔🔍

- [effective-java-3e-source-code (KOR)](https://github.com/WegraLee/effective-java-3e-source-code)

- [effective-java-3e-source-code (EN)](https://github.com/jbloch/effective-java-3e-source-code)