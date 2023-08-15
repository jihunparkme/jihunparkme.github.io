---
layout: post
title: 객체, 공통 메서드
summary: 객체 생성과 파괴, 모든 객체의 공통 메서드
categories: (Book)Effective-JAVA-3/E JAVA
featured-img: EFF_JAVA
# mathjax: true
---

# 2장. 객체 생성과 파괴

객체를 만들어야 할 때와 만들지 말아야 할 떄를 구분하는 법, 올바른 객체 생성 방법과 불필요한 생성을 피하는 방법, 제때 파괴됨을 보장하고 파괴 전에 수행해야 할 정리 작업을 관리하는 요렁

## item 1. 생성자 대신 정적 팩터리 메서드를 고려하라.

> 정적 팩터리 메서드와 public 생성자는 각자의 쓰임새가 있으니 상대적인 장단점을 이해하고 사용하는 것이 좋다.
>
> 그렇다고 하더라도 정적 팩터리를 사용하는 게 유리한 경우가 더 많으므로 무작정 public 생성자를 제공하던 습관이 있다면 고치자.

📖

장점1. 
- 생성자의 시그니처가 중복되는 경우 팩터리 메서드를 통해 표현이 가능하다.
- 팩터리 메서드를 통해 객체의 특징을 표현한 더 자세한 표현이 가능하다.

```java
public class Order {
  private boolean prime;

  private boolean urgent;

  private Product product;

  /* 생성자의 시그니처가 중복되는 경우 */
  public Order(Product product, boolean prime) {
      this.product = product;
      this.prime = prime;
  }

  // 'Order(Product, boolean)' is already defined in 'Order'
  public Order(Product product, boolean urgent) {
      this.product = product;
      this.urgent = urgent;
  }
}

...

public class Order {
  private boolean prime;

  private boolean urgent;

  private Product product;

  /* 팩터리 메서드로 더 자세한 표현(객체의 특징) 가능 */
  public static Order primeOrder(Product product) {
      Order order = new Order();
      order.prime = true;
      order.product = product;
      return order;
  }

  public static Order urgentOrder(Product product) {
      Order order = new Order();
      order.urgent = true;
      order.product = product;
      return order;
  }
}
```


```java
public class Settings {
    private boolean useAutoSteering;

    private boolean useABS;

    private Difficulty difficulty;

    private Settings() {}

    private static final Settings SETTINGS = new Settings();

    /* 객체 생성을 자신이 컨트롤 */
    public static Settings getInstance() {
        return SETTINGS;
    }
}

...

Settings settings1 = Settings.getInstance();
Settings settings2 = Settings.getInstance();
```















클래스는 생성자와 별도로 정적 팩터리 메서드(static factory method)를 제공할 수 있다.

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

<br>

## item 2. 생성자에 매개변수가 많다면 빌더를 고려하라.

> 생성자나 정적 팩터리가 처리해야 할 매개변수가 많다면 빌더 패턴을 선택하는 게 더 낫다.
> 
> 매개변수 중 다수가 필수가 아니거나 같은 타입이면 특히 더 그렇다.
> 
> 빌더는 점층적 생성자보다 클라이언트 코드를 읽고 쓰기가 훨씬 간결하고, 자바빈즈보다 훨씬 안전하다.

📖

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

<br>

## item 3. private 생성자나 열거 타입으로 싱글턴임을 보증하라.

> 만들려는 싱글턴이 Enum 이외의 클래스를 상속하지 않는다면, "원소가 하나인 열거 타입을 선언" 방식을 선택해 보자.

📖

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

> 클래스가 내부적으로 하나 이상의 자원에 의존하고, 그 자원이 클래스 동작에 영향을 준다면 
> 싱글턴과 정적 유틸리티 클래스는 사용하지 않는 것이 좋다.
> 
> 이 자원들을 클래스가 직접 만들게 해서도 안 된다.
> 
> 대신 필요한 자원을(혹은 그 자원을 만들어주는 팩터리를) 생성자에(혹은 정적 팩터리나 빌더에) 넘겨주자.
> 
> 의존 객체 주입이라 하는 이 기법은 클래스와의 유연성, 재사용성, 테스트 용이성을 기막히게 개선해준다.

📖

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

> 메모리 누수는 겉으로 잘 드러나지 않아 시스템에 수년간 잠복하는 사례도 있다.
> 
> 이런 누수는 철저한 코드 리뷰나 힙 프로파일러 같은 디버깅 도구를 동원해야만 발견되기도 한다.
> 
> 그래서 이런 종류의 문제는 예방법을 익혀두는 것이 매우 중요하다.

📖

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

<br>

## item 8. finalizer와 cleaner 사용을 피하라.

> cleaner(java8 까지는 finalizer)는 안전망 역할이나 중요하지 않은 네이티브 자원 회수용으로만 사용하자.
> 
> 물론 이런 경우라도 불확실성과 성능 저하에 주의해야 한다.

📖

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

<br>

## item 9. try-finally 보다는 try-with-resources를 사용하라.

> 꼭 회수해야 하는 자원을 다룰 때는 try-finally 말고, try-with-resources를 사용하자.
> 
> 예외는 없다. 코드는 더 짧고 분명해지고, 만들어지는 예외 정보도 훨씬 유용하다.
> 
> try-finally로 작성하면 실용적이지 못할 만큼 코드가 지저분해지는 경우라도, 
> try-with-resources로 정확하고 쉽게 자원을 회수할 수 있다.

📖

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

# 3장. 모든 객체의 공통 메서드

final이 아닌 Object 메서드(equals, hashCode, toString, clone, finalize)들을 언제, 어떻게 재정의해야 하는지.

## item 10. equals는 일반 규약을 지켜 재정의하라.

> 꼭 필요한 경우가 아니면 equals를 재정의하지 말자.
> 
> 많은 경우에 Object의 equals가 여러분이 원하는 비교를 정확히 수행해준다.
> 
> 재정의해야 할 때는 그 클래스의 핵심 필드 모두를 빠짐없이, 다섯 가지 규약을 확실히 지켜가며 비교해야 한다.

📖

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

📝 명시적 null 검사는 불필요

```java
@Override public boolean equals(Object o) {
    // equals가 타입을 확인하지 않으면 잘못된 타입이 인수로 주어졌을 때,
    // ClassCastException을 던져 일반 규약을 위배
    if (o == null)
        return false;
    // ...
}
```

📝 묵시적 null 검사를

```java
@Override public boolean equals(Object o) {
    // null이 인수로 주어지면 false를 반환
    if (!(o instanceof MyType))
        return false;
    MyType mt = (MyType) o;
    // ...
}
```

🔍 **양질의 equals 메서드 구현 방법**

1. `== 연산자를 사용해 입력이 자기 자신의 참조인지 확인`
2. `instanceof 연산자로 입력이 올바른 타입인지 확인`
3. `입력을 올바른 타입으로 형변환`
4. `입력 객체와 자기 자신의 대응되는 핵심필드들이 모두 일치하는지 하나씩 검사`

- Float.compare()와 Double.compare()을 제외한 기본 타입 필드는 == 연산자로 비교, 참조 타입 필드는 각각의 equals 메서드로 비교
- 배열 필드는 원소 각각을 앞서의 지침대로 비교하고, 모든 원소가 핵심 필드라면 Arrays.equals 메서드들 중 하나를 사용
- null 가능성이 있을 경우 Objects.equals(Object, Object) 비교로 NPE 방지
- equals의 성능을 위해 다를 가능성이 더 크거나 비교 비용이 싼 필드를 먼저 비교
- equals를 다 구현했다면 `대칭적`, `추이성`, `일관적`인지 자문
- equals를 재정의할 땐 hashCode도 반드시 재정의
- Object 외의 타입을 매개변수로 받는 equals 메서드는 선언하지 말자

📝 전형적인 equals 메서드의 예

```java
// 입력 타입은 반드시 Object (다중정의)
@Override public boolean equals(Object o) { 
    // 필드들의 동치성만 검사해도 equals 규약을 어렵지 않게 지킬 수 있다.
    if (o == this) return true;
    if (!(o instanceof PhoneNumber)) return false;

    PhoneNumber pn = (PhoneNumber)o;
    return pn.lineNum == lineNum && pn.prefix == prefix
            && pn.areaCode == areaCode;
}
```

<br>

## item 11. equals를 재정의하려거든 hashCode도 재정의하라

> equals를 재정의할 때는 hashCode도 반드시 재정의해야 한다. 그렇지 않으면 프로그램이 제대로 동작하지 않을 것이다.
> 
> 재정의한 hashCode는 Object의 API 문서에 기술된 일반 규약을 따라야 하며, 서로 다른 인스턴스라면 되도록 해시코드도 서로 다르게 구현해야 한다.
> 
> 구현하기가 어렵지는 않지만 조금 따분한 일이긴 하다. 하지만 AutoValue 프레임워크를 사용하면 멋진 equals와 hashCode를 자동으로 만들어준다.

📖

equals를 재정의한 클래스 모두에서 hashCode도 재정의해야 한다.

- 그렇지 않으면 hashCode 일반 규약을 어기게 되어 해당 클래스의 인스턴스를 HashMap 이나 HashSet 같은 컬렉션의 원소로 사용할 때 문제를 일으키게 된다.

**Object 명세에서 발췌한 규약**

- equals 비교에 사용되는 정보가 변경되지 않았다면, 애플리케이션이 실행되는 동안 그 객체의 hashCode 메서드는 몇 번을 호출해도 일관되게 항상 같은 값을 반환해야 한다.
- equals(Object)가 두 객체를 같다고 판단했다면, 두 객체의 hashCode는 똑같은 값을 반환해야 한다.
- equals(Object)가 두 객체를 다르다고 판단했더라도, 두 객체의 hashCode가 서로 다른 값을 반환할 필요는 없다. 단, 다른 객체에 대해서는 다른 값을 반환해야 해시테이블의 성능이 좋아진다.

📝 [hashCode 메서드](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter3/item11/PhoneNumber.java)

<br>

## item 12. toString을 항상 재정의하라.

> 모든 구체 클래스에서 Object의 toString을 재정의하자.
> 
> 상위 클래스에서 이미 알맞게 재정의한 경우는 예외다. toString을 재정의한 클래스는 사용하기도 즐겁고 그 클래스를 사용한 시스템을 디버깅하기 쉽게 해준다.
> 
> toString은 해당 객체에 관한 명확하고 유용한 정보를 읽기 좋은 형태로 반환해야 한다.

📖

- toString을 잘 구현한 클래스는 사용하기에 훨씬 즐겁고, 그 클래스를 사용한 시스템은 디버깅하기 쉽다.
- 실전에서 toString은 그 객체가 가진 주요 정보 모두를 반환하는 게 좋다.
- 포맷을 명시하든 아니든 의도는 명확히 밝혀야 한다.
- toString이 반환한 값에 포함된 정보를 얻어올 수 있는 API를 제공하자.

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

<br>

## item 13. clone 재정의는 주의해서 진행하라.

> Cloneable이 몰고 온 모든 문제를 되짚어봤을 때, 새로운 인터페이스를 만들 때는 절대 Cloneable을 확장해서는 안 되며, 새로운 클래스도 이를 구현해서는 안 된다.
> 
> final 클래스라면 Cloneable을 구현해도 위험이 크지 않지만, 성능 최적화 관점에서 검토한 후 별다른 문제가 없을 때만 드물게 혀용해야 한다.
> 
> 기본 원칙은 '복제 기능은 생성자와 팩터리를 이용하는 게 최고!' 라는 것. 
> 
> 단, 배열만은 clone 메서드 방식이 가장 깔끔한, 이 규칙의 합당한 예외라고 할 수 있다.

📖

- Cloneable을 구현한 클래스는 clone 메서드를 public으로 제공하며, 사용자는 당연히 복제가 제대로 이뤄지리라 기대하지만, 깨지기 쉽고, 위험하고, 모순적인 매커니즘이 탄생한다..

📝 가변 상태를 참조하지 않는 클래스용 clone 메서드

```java
@Override public PhoneNumber clone() {
    try {
        // 재정의한 메서드의 반환 타입은 상위 클래스의 메서드가 반환하는 타입의 하위 타입일 수 있다.
        return (PhoneNumber) super.clone();
    } catch (CloneNotSupportedException e) {
        throw new AssertionError();  // 일어날 수 없는 일이다.
    }
}
```

- clone 메서드는 사실상 생성자와 같은 효과를 낸다.
  - clone은 원본 객체에 아무런 해를 끼치지 않는 동시에 복제된 객체의 불변식을 보장해야 한다.

📝 가변 상태를 참조하는 클래스용 clone 메서드

```java
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

- 상속용 클래스는 Cloneable을 구형해서는 안 된다.
- Cloneable을 구현하는 모든 클래스는 clone을 재정의해야 한다.
- 복사 생성자와 복사 팩터리는 더 나은 객체 복사 방식을 제공할 수 있다.
  - 문서화된 규약에 기대지 않고, 정상적인 final 필드 용법과 충돌하지 않고, 불필요한 검사 예외를 던지지 않고, 형변환도 필요하지 않음
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

<br>

## item 14. Comparable을 구현할지 고려하라.

> 순서를 고려해야 하는 값 클래스를 작성한다면 꼭 Compareable 인터페이스를 구현하여, 그 인스턴스들을 쉽게 정렬하고, 검색하고, 비교 기능을 제공하는 컬렉션과 어우러지도록 해야 한다.
>
> compareTo 메서드에서 필드의 값을 비교할 때, <와 > 연산자는 쓰지 말자.
>
> 그 대신 박싱된 기본 타입 클래스가 제공하는 정적 compare 메서드나 Comarator 인터페이스가 제공하는 비교자 생성 메서드를 사용하자.

📖

알파벳, 숫자, 연대 같이 순서가 명확한 값 클래스를 작성한다면 반드시 Comparable 인터페이스를 구현하자.
- compareTo는 단순 동치성 비교에 더해 순서까지 비교하고, 제네릭하다.
- Compareable 구현으로 수많은 제네릭 알고리즘과 컬렉션의 힘을 누릴 수 있다.

```java
public interface Comparable<T> {
    int compareTo(T t);
}
```

compareTo 메서드의 일반 규약은 equals의 규약과 비슷

주어진 객체와 순서를 비교. 작으면 음수, 같으면 0, 크면 양수 반환. 비교할 수 없는 타입일 경우 ClassCastException

- Comparable을 구현한 클래스는 모든 x,y에 대한 sgn(x.compareTo(y)) == -sgn(y.compareTo(x))여야 한다.
  - x.compareTo(y)는 y.compareTo(x)가 예외를 던질 때에 한해 예외를 던져야 한다.
- Comparable을 구현한 클래스는 추이성을 보장해야 한다.
- Comparable을 구현한 클래스는 모든 z에 대해 x.compareTo(y) == 0 이면 sgn(x.compareTo(z)) == sgn(y.compareTo(z))
- (x.compareTo(y) == 0) == (x.equals(y))여야 한다.

compareTo 규약을 지키지 못하면 비교를 활용하는 클래스와 어울리지 못함

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

...

**Reference**

- [effective-java-3e-source-code (KOR)](https://github.com/WegraLee/effective-java-3e-source-code)

- [effective-java-3e-source-code (EN)](https://github.com/jbloch/effective-java-3e-source-code)