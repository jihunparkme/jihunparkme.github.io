---
layout: post
title: 02. 객체 생성과 파괴
summary: 객체 생성과 파괴
categories: (Book)Effective-JAVA-3/E
featured-img: EFF_JAVA
# mathjax: true
---

# Table of Contents

2장. 객체 생성과 파괴

- [item 1. 생성자 대신 정적 팩터리 메서드를 고려하라.](#item-1-생성자-대신-정적-팩터리-메서드를-고려하라)
- [item 2. 생성자에 매개변수가 많다면 빌더를 고려하라.](#item-2-생성자에-매개변수가-많다면-빌더를-고려하라)
- [item 3. private 생성자나 열거 타입으로 싱글턴임을 보증하라](#item-3-private-생성자나-열거-타입으로-싱글턴임을-보증하라)
- [item 4. 인스턴스화를 막으려거든 private 생성자를 사용하라.](#item-4-인스턴스화를-막으려거든-private-생성자를-사용하라)
- [item 5. 자원을 직접 명시하지 말고 의존 객체 주입을 사용하라](#item-5-자원을-직접-명시하지-말고-의존-객체-주입을-사용하라)
- [item 6. 불필요한 객체 생성을 피하라.](#item-6-불필요한-객체-생성을-피하라)
- [item 7. 다 쓴 객체 참조를 해제하라.](#item-7-다-쓴-객체-참조를-해제하라)
- [item 8. finalizer와 cleaner 사용을 피하라.](#item-8-finalizer와-cleaner-사용을-피하라)
- [item 9. try-finally 보다는 try-with-resources를 사용하라.](#item-9-try-finally-보다는-try-with-resources를-사용하라)

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

🔔
> 정적 팩터리 메서드와 public 생성자는 각자의 쓰임새가 있으니 상대적인 장단점을 이해하고 사용하는 것이 좋다.
>
> 그렇다고 하더라도 정적 팩터리를 사용하는 게 유리한 경우가 더 많으므로 무작정 public 생성자를 제공하던 습관이 있다면 고치자 !!!

<br>

## item 2. 생성자에 매개변수가 많다면 빌더를 고려하라.
- 빌더 패턴 : 점층적 생성자 패턴의 안전성과 자바 빈즈 패턴의 가독성을 겸비한 패턴
- 클라이언트는 필요한 객체를 직접 만드는 대신, 필수 매개변수만으로 생성자를 호출해 빌더 객체를 얻는다.
  - 그 후 빌더 객체가 제공하는 일종의 세터 메서드들로 원하는 선택 매개변수들을 설정

```java
public class NutritionFacts {
    private final int servingSize;
    private final int servings;
    private final int calories;
    private final int fat;
    private final int sodium;
    private final int carbohydrate;

    public static class Builder {
        // 필수 매개변수
        private final int servingSize;
        private final int servings;

        // 선택 매개변수 - 기본값으로 초기화한다.
        private int calories      = 0;
        private int fat           = 0;
        private int sodium        = 0;
        private int carbohydrate  = 0;

        public Builder(int servingSize, int servings) {
            this.servingSize = servingSize;
            this.servings    = servings;
        }

        public Builder calories(int val)
        { calories = val;      return this; }
        public Builder fat(int val)
        { fat = val;           return this; }
        public Builder sodium(int val)
        { sodium = val;        return this; }
        public Builder carbohydrate(int val)
        { carbohydrate = val;  return this; }

        public NutritionFacts build() {
            return new NutritionFacts(this);
        }
    }

    private NutritionFacts(Builder builder) {
        servingSize  = builder.servingSize;
        servings     = builder.servings;
        calories     = builder.calories;
        fat          = builder.fat;
        sodium       = builder.sodium;
        carbohydrate = builder.carbohydrate;
    }

    public static void main(String[] args) {
        NutritionFacts cocaCola = new NutritionFacts.Builder(240, 8)
                .calories(100).sodium(35).carbohydrate(27).build();
        		// 메서드 호출이 흐르듯 연결되는 플루언트 API or 메서드 연쇄
    }
}
```

- 빌더 패턴은 계층적으로 설계된 클래스와 함께 사용하기 좋다.
  - 각 계층의 클래스에 관련 빌더를 멤버로 정의
  - 추상 클래스는 추상 빌더를, 구체 클래스는 구체 빌더를 갖도록 하자.
- 빌더를 이용하면 가변인수 매개변수를 여러 개 사용할 수 있다.

📝Pizza
```java
public abstract class Pizza {
    public enum Topping { HAM, MUSHROOM, ONION, PEPPER, SAUSAGE }
    final Set<Topping> toppings;

    abstract static class Builder<T extends Builder<T>> {
        EnumSet<Topping> toppings = EnumSet.noneOf(Topping.class);
        public T addTopping(Topping topping) {
            toppings.add(Objects.requireNonNull(topping));
            return self();
        }

        abstract Pizza build();

        // 하위 클래스는 이 메서드를 재정의(overriding)하여
        // "this"를 반환하도록 해야 한다.
        protected abstract T self();
    }
    
    Pizza(Builder<?> builder) {
        toppings = builder.toppings.clone(); 
    }
}
```

📝NyPizza
```java
public class NyPizza extends Pizza {
    public enum Size { SMALL, MEDIUM, LARGE }
    private final Size size;

    public static class Builder extends Pizza.Builder<Builder> {
        private final Size size;

        public Builder(Size size) {
            this.size = Objects.requireNonNull(size);
        }
		// 상위 클래스의 메서드가 정의한 반환 타입이 아닌, 그 하위 타입을 반환 (공변 반환 타이핑)
        @Override public NyPizza build() {
            return new NyPizza(this);
        }

        @Override protected Builder self() { return this; }
    }

    private NyPizza(Builder builder) {
        super(builder);
        size = builder.size;
    }

    @Override public String toString() {
        return toppings + "로 토핑한 뉴욕 피자";
    }
}
```

📝Calzone
```java
public class Calzone extends Pizza {
    private final boolean sauceInside;

    public static class Builder extends Pizza.Builder<Builder> {
        private boolean sauceInside = false; // 기본값

        public Builder sauceInside() {
            sauceInside = true;
            return this;
        }

        @Override public Calzone build() {
            return new Calzone(this);
        }

        @Override protected Builder self() { return this; }
    }

    private Calzone(Builder builder) {
        super(builder);
        sauceInside = builder.sauceInside;
    }

    @Override public String toString() {
        return String.format("%s로 토핑한 칼초네 피자 (소스는 %s에)",
                toppings, sauceInside ? "안" : "바깥");
    }
}
```

📝PizzaTest
```java
public class PizzaTest {
    public static void main(String[] args) {
        NyPizza pizza = new NyPizza.Builder(SMALL)
                .addTopping(SAUSAGE).addTopping(ONION).build();
        Calzone calzone = new Calzone.Builder()
                .addTopping(HAM).sauceInside().build();
        
        System.out.println(pizza);
        System.out.println(calzone);
    }
}
```

- 빌더의 단점으로는,
  - 빌더 생성 비용이 크지는 않지만 성능에 민감한 상황에서는 문제가 될 수 있음
  - 점층적 생성자 패턴보다는 코드가 장황해서 매개변수 4개 이상은 되어야 값어치를 함

🔔
> 생성자나 정적 팩터리가 처리해야 할 매개변수가 많다면 빌더 패턴을 선택하는 게 더 낫다.
> 매개변수 중 다수가 필수가 아니거나 같은 타입이면 특히 더 그렇다.
> 빌더는 점층적 생성자보다 클라이언트 코드를 읽고 쓰기가 훨씬 간결하고, 자바빈즈보다 훨씬 안전하다.

<br>

## item 3. private 생성자나 열거 타입으로 싱글턴임을 보증하라.

- 싱클턴을 만드는 방식은 보통 둘 중 하나

1. **public static member 가 final 필드인 방식**
   - public이나 protected 생성자가 없으므로 Elvis 클래스가 초기화될 때 만들어진 인스턴스가 전체 시스템에서 하나뿐임이 보장
   - public 필드방식의 큰 장점
     - 해당 클래스가 싱글턴인 것을 API에 명백히 들어남
       - public static 필드가 final 이므로 절대 다른 객체를 참조할 수 없음
     - 간결함

```java
public class Elvis {
    // member가 public 
    public static final Elvis INSTANCE = new Elvis();

    private Elvis() { }

    public void leaveTheBuilding() {
        System.out.println("Whoa baby, I'm outta here!");
    }

    // 이 메서드는 보통 클래스 바깥(다른 클래스)에 작성해야 한다!
    public static void main(String[] args) {
        Elvis elvis = Elvis.INSTANCE;
        elvis.leaveTheBuilding();
    }
}
```

2. **정적 팩터리 메서드를 public static Member로 제공**
   - 정적 팩터리 방식의 장점
     - API를 바꾸지 않고도 싱글턴이 아니게 변경할 수 있음
     - 원한다면 정적 팩터리를 제네릭 싱글턴 팩터리로 만들 수 있음
     - 정적 팩터리의 메서드 참조를 공급자로 사용할 수 있음

```java
public class Elvis {
    private static final Elvis INSTANCE = new Elvis();
    private Elvis() { }
    public static Elvis getInstance() { return INSTANCE; }

    public void leaveTheBuilding() {
        System.out.println("Whoa baby, I'm outta here!");
    }

    // 이 메서드는 보통 클래스 바깥(다른 클래스)에 작성해야 한다!
    public static void main(String[] args) {
        Elvis elvis = Elvis.getInstance();
        elvis.leaveTheBuilding();
    }
}
```

- 위 둘 중 하나의 방식으로 만든 싱글턴 클래스를 직렬화하려면 단순히 Serializable을 구현한다고 선언하는 것 뿐만 아니라 모든 인스턴스 필드를 일시적이라고 선언하고 readResolve 메서드를 제공해야 한다.
  - 이렇게 하지 않으면 직렬화된 인스턴스를 역직렬화할 때마다 새로운 인스턴스가 만들어 짐..

```java
private Object readResolve() {
    // 진짜 Elvis를 반환하고, 가짜 Elvis는 가비지 컬렉터에..
    return INSTANCE;
}
```

3. 🔍**원소가 하나인 열거 타입을 선언**🔍
   - public 필드 방식과 비슷하지만, 더 간결하고, 추가 노력 없이 직렬화가 가능.
   - 아주 복잡한 직렬화 상황이나 리플렉션 공격에서도 제 2의 인스턴스가 생기는 일을 완벽하게 막아줌
   - <u>*대부분 상황에서 원소가 하나뿐인 열거 타입이 싱글턴을 만드는 가장 좋은 방법*</u>
   - 단, 만들려는 싱글턴이 Enum 이외의 클래스를 상속해야 한다면 이 방법은 사용할 수 없음.?

```java
public enum Elvis {
    INSTANCE;

    public void leaveTheBuilding() {
        System.out.println("기다려 자기야, 지금 나갈께!");
    }

    // 이 메서드는 보통 클래스 바깥(다른 클래스)에 작성해야 한다!
    public static void main(String[] args) {
        Elvis elvis = Elvis.INSTANCE;
        elvis.leaveTheBuilding();
    }
}
```

<br>

## item 4. 인스턴스화를 막으려거든 private 생성자를 사용하라.

- 추상 클래스로 만드는 것으로는 인스턴스화를 막을 수 없다. (기본 생성자가 자동으로 생성)
- 컴파일러가 기본 생성자를 만드는 경우는 오직 명시된 생성자가 없을 때뿐이니 <u>*private 생성자를 추가하면 클래스의 인스턴스화를 막을 수 있다.*</u>
- 아래 방법은 상속을 불가능하게 하는 효과도 있음

```java
public class UtilityClass {
    // 기본 생성자가 만들어지는 것을 막는다(인스턴스화 방지용).
    private UtilityClass() {
        throw new AssertionError();
    }
    // ...
}
```

<br>

## item 5. 자원을 직접 명시하지 말고 의존 객체 주입을 사용하라.

- 사용하는 자원에 따라 동작이 달라지는 클래스에는 정적 유틸리티 클래스나 싱글턴 방식이 적합하지 않다.
- 대신 클래스가 `여러 자원 인스턴스를 지원`해야 하며, `클라이언트가 원하는 자원`을 사용해야 한다.
- 이 패턴은 바로! <u>*인스턴스를 생성할 때 생성자에 필요한 자원을 넘겨주는 방식*</u>
- Dagger, Guice, Spring 같은 의존 객체 주입 프레임워크를 사용하면 큰 프로젝트에서 코드가 어지러워지는 단점을 개선할 수 있다.

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

> 클래스가 내부적으로 하나 이상의 자원에 의존하고, 그 자원이 클래스 동작에 영향을 준다면 
> 싱글턴과 정적 유틸리티 클래스는 사용하지 않는 것이 좋다.
> 
> 이 자원들을 클래스가 직접 만들게 해서도 안 된다.
> 대신 필요한 자원을 (혹은 그 자원을 만들어주는 팩터리를) 생성자에 (혹은 정적 팩터리나 빌더에) 넘겨주자.
> 의존 객체 주입이라 하는 이 기법은 클래스와의 유연성, 재사용성, 테스트 용이성을 기막히게 개선해준다.

<br>

## item 6. 불필요한 객체 생성을 피하라.

- 생성자 대신 정적 팩터리 메서드를 제공하는 불변 클래스에서는 정적 팩터리 메서드를 사용해 불필요한 객체 생성을 피할 수 있다.
- Boolean.valueOf(String) 팩터리 메서드를 사용하는 것이 좋다.
- 생성자는 호출할 때마다 새로운 객체를 만들지만, 팩터리 메서드는 그렇지 않다.

📝값비싼 객체를 재사용해 성능을 개선하자.

```java
public class RomanNumerals {
    // 값비싼 객체를 재사용해 성능을 개선
    private static final Pattern ROMAN = Pattern.compile(
                                            "^(?=.)M*(C[MD]|D?C{0,3})"
                                                    + "(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$");

    static boolean isRomanNumeralFast(String s) {
        return ROMAN.matcher(s).matches();
    }

    public static void main(String[] args) {
        int numSets = Integer.parseInt(args[0]);
        int numReps = Integer.parseInt(args[1]);
        boolean b = false;

        for (int i = 0; i < numSets; i++) {
            long start = System.nanoTime();
            for (int j = 0; j < numReps; j++) {
                b ^= isRomanNumeral("MCMLXXVI");
            }
            long end = System.nanoTime();
            System.out.println(((end - start) / (1_000. * numReps)) + " μs.");
        }

        // VM이 최적화하지 못하게 막는 코드
        if (!b)
            System.out.println();
    }
}
```

📝박싱된 기본 타입보다는 기본 타입을 사용하고, 의도치 않은 오토박싱이 숨어들지 않도록 주의하자.

```java
private static long sum() {
    Long sum = 0L; // Long으로 선언해서 불필요한 인스턴스가 약 2^31개나 만들어진다.
    for (long i = 0; i <= Integer.MAX_VALUE; i++)
        sum += i;
    return sum;
}
```

- 아주 무거운 객체가 아닌 다음에야 단순히 객체 생성을 피하고자 우리만의 풀(pool)을 만들지는 말자.

## item 7. 다 쓴 객체 참조를 해제하라.

- 가비지 컬렉션 언어에서는 메모리 누수를 찾기가 아주 까다롭다.
- 해법은 해당 참조를 다 썻을 때 null 처리(참조 해제)를 해주는 것
  - 단, 객체  참조를 null 처리하는 일은 예외적인 경우여야 한다!
- 다 쓴 참조를 해제하는 가장 좋은 방법은 <u>*그 참조를 담은 변수를 유효 범위 밖으로 밀어내는 것!*</u>
- 일반적으로 <u>*자기 메모리를 직접 관리하는 클래스라면 프로그래머는 항시 메모리 누수에 주의해야 한다.!*</u>
- 메모리 누수의 두 번째 주범은 캐시!
- 메모리 누수의 세 번째 주범은 리스너(listener) 혹은 콜백(callback)
  - 클라이언트가 콜백을 등록만 하고 명확히 해지하지 않는다면?
  - 콜백을 약한 참조로 저장하면 가비지 컬렉터가 즉시 수거해간다.
    - 예를 들어, WeakHashMap에 키로 저장하자. (다 쓴 엔트리는 그 즉시 자동으로 제거)
🔔
> 메모리 누수는 겉으로 잘 드러나지 않아 시스템에 수년간 잠복하는 사례도 있다.
> 이런 누수는 철저한 코드 리뷰나 힙 프로파일러 같은 디버깅 도구를 동원해야만 발견되기도 한다
> 그래서 이런 종류의 문제는 예방법을 익혀두는 것이 매우 중요하다.

## item 8. finalizer와 cleaner 사용을 피하라.

- finalizer는 예측할 수 없고, 상황에 따라 위험할 수 있어 일반적으로 불필요하다.
- cleaner는 finalizer보다는 덜 위험하지만, 여전히 예측할 수 없고, 느리고, 일반적으로 불필요하다.
- finalizer와 cleaner로는 제때 수행되어야 하는 작업은 절대 할 수 없다.
  - finalizer와 cleaner는 즉시 수행된다는 보장이 없다.
- finalizer와 cleaner는 심각한 성능 문제도 동반한다.
- finalizer를 사용한 클래스는 finalizer 공격에 노출되어 심각한 보안 문제를 일으킬 수도 있다.
- final이 아닌 클래스를 finalizer 공격으로부터 방어하려면 아무 일도 하지 않는 finalize 메서드를 만들고 final로 선언하자!
- cleaner와 finalizer의 적절한 쓰임새
  1. 자원의 소유자가 close 메서드를 호출하지 않는 것에 대비한 안전망 역할
  2. Native peer와 연결된 객체에서 (Native peer는 자바 객체가 아니라 가비지 컬렉터는 그 존재를 알지 못한다)
     - 단, 자원을 즉시 회수해야 한다면 close 메서드를 사용

📝cleaner를 안전망으로 활용하는 AutoCloseable Class
- System.exit 을 호출할 때의 cleaner 동작은 구현하기 나름이다 청소가 이뤄질지는 보장하지 않는다.

```java
import java.lang.ref.Cleaner;

public class Room implements AutoCloseable {
    private static final Cleaner cleaner = Cleaner.create();

    // 청소가 필요한 자원. 절대 Room을 참조해서는 안 된다!
    private static class State implements Runnable {
        int numJunkPiles; // Number of junk piles in this room

        State(int numJunkPiles) {
            this.numJunkPiles = numJunkPiles;
        }

        // close 메서드나 cleaner가 호출한다.
        @Override public void run() {
            System.out.println("Cleaning room");
            numJunkPiles = 0;
        }
    }

    // 방의 상태. cleanable과 공유한다.
    private final State state;

    // cleanable 객체. 수거 대상이 되면 방을 청소한다.
    private final Cleaner.Cleanable cleanable;

    public Room(int numJunkPiles) {
        state = new State(numJunkPiles);
        cleanable = cleaner.register(this, state);
    }

    @Override public void close() {
        cleanable.clean();
    }
}
```

📝cleaner 안전망을 갖춘 자원을 제대로 활용하는 클라이언트

```java
public class Adult {
    public static void main(String[] args) {
        try (Room myRoom = new Room(7)) {
            System.out.println("Hello~");
        }
    }
}

// Result
Hello~
Cleaning room
```

📝cleaner 안전망을 갖춘 자원을 제대로 활용하지 못하는 클라이언트

```java
public class Teenager {
    public static void main(String[] args) {
        new Room(99);
        System.out.println("Peace out");
        
        // System.gc()를 추가해보자.
        // 단, 가비지 컬렉러를 강제로 호출하는 이런 방식에 의존해서는 절대 안 된다!
	   //  System.gc();
    }
}

// Result
Peace out
```

🔔
> cleaner(java8 까지는 finalizer)는 안전망 역할이나 중요하지 않은 네이티브 자원 회수용으로만 사용하자.
> 물론 이런 경우라도 불확실성과 성능 저하에 주의해야 한다.

<br>

## item 9. try-finally 보다는 try-with-resources를 사용하라.

- 





📝🔔🔍

> Code Reference : [https://github.com/WegraLee/effective-java-3e-source-code/tree/master/src/effectivejava](https://github.com/WegraLee/effective-java-3e-source-code/tree/master/src/effectivejava)