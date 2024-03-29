---
layout: post
title: 객체, 공통 메서드
summary: 객체 생성과 파괴, 모든 객체의 공통 메서드
categories: (Book)Effective-JAVA-3/E
featured-img: EFF_JAVA
# mathjax: true
---

# 2장. 객체 생성과 파괴

객체를 만들어야 할 때와 만들지 말아야 할 떄를 구분하는 법, 올바른 객체 생성 방법과 불필요한 생성을 피하는 방법, 제때 파괴됨을 보장하고 파괴 전에 수행해야 할 정리 작업을 관리하는 요렁

## item 1. 생성자 대신 정적 팩터리 메서드를 고려하라.

> 정적 팩터리 메서드와 public 생성자는 각자의 쓰임새가 있으니 상대적인 장단점을 이해하고 사용하는 것이 좋다.
>
> 그렇다고 하더라도 정적 팩터리를 사용하는 게 유리한 경우가 더 많으므로 무작정 public 생성자를 제공하던 습관이 있다면 고치자.

👍

**장점 1.**
- `생성자의 시그니처가 중복되는 경우` 팩터리 메서드를 통해 표현이 가능하다.
- 팩터리 메서드를 통해 `객체의 특징을 이름으로` 더 자세하게 표현(반환될 객체의 특성을 쉽게 묘사) 가능하다.

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

**장점 2.**
- 호출될 때마다 `인스턴트를 새로 생성하지 않아도 된다.`
  - 불필요한 객체 생성을 피하여 성능을 올려줄 수 있음
  - 인스턴스 통제 클래스(instance-controlled)
- java.lang.Boolean.valueOf()
  ```java
  public static Boolean valueOf(boolean b) {
      return b ? Boolean.TRUE : Boolean.FALSE;
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

**장점 3.**
- 반환 타입의 `하위 타입 객체를 반환`할 수 있는 능력이 있다.
  - 반환할 객체의 클래스를 자유롭게 선택할 수 있는 유연성 보유
  - 인터페이스 기반 프레임워크를 만드는 핵심 기술

**장점 4.**
- 입력 매개변수에 따라 `매번 다른 클래스의 객체를 반환`할 수 있다.
  - 클라이언트는 팩터리가 건네주는 객체가 어느 클래스의 인스턴스인지 알 수도 없고 알 필요도 없다.
- java.util.EnumSet.noneOf()

```java
public interface HelloService {

    String hello();

    /**
     * 장점 3.
     * 
     * @return HelloService interface
     * 리턴 타입은 인터페이스지만 실제 리턴 인스턴스는 인터페이스의 구현체.
     * 또는 
     * 리턴 타입은 클래스지만 실제 리턴 인스턴스는 하위 클래스.
     */
    static HelloService of(String lang) {
        /**
         * 장점 4.
         * 
         * 매개변수에 따라 각기 다른 인스턴스 제공
         */
        if (lang.equals("ko")) {
            return new KoreanHelloService();
        } else {
            return new EnglishHelloService();
        }
    }
}

...

// 인테스이스 기반 프레임워크를 사용하도록 강제하고, 구현체는 숨길 수 있음
HelloService ko = HelloServiceFactory.of("ko");
```

**장점 5.**
- 정적 팩터리 메서드를 작성하는 시점에는 반환할 객체의 클래스가 존재하지 않아도 된다.
- java.util.ServiceLoader (Service Provider Framework)

```java
ServiceLoader<HelloService> loader = ServiceLoader.load(HelloService.class);
Optional<HelloService> helloServiceOptional = loader.findFirst();
helloServiceOptional.ifPresent(h -> {
    System.out.println(h.hello());
});
```

👎

**단점 1.**
- 정적 팩터리 메서드만 제공하면 하위 클래스를 만들 수 없다.(`상속 불가`)
- 상속을 위해 public/protected 생성자 필요

**단점 2.**
- 정적 팩터리 메서드는 javadoc 에서 프로그래머가 찾기 어렵다.

📖

참고. **정적 팩터리 메서드에 흔히 사용하는 명명 방식**

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

정적 팩터리와 생성자에 선택적 매개변수가 많을 때 고려할 수 있는 방안

- **점층적 생성자 패턴 또는 생성자 체이닝**
  - 매개변수가 늘어나면 클라이언트 코드를 작성하거나 읽기 어려움
- **자바빈즈 패턴**
  - 완전한 객체를 만들려면 (setter)메서드를 여러번 호출 필요
  - 객체의 일관성이 무너질 수 있음
  - 클래스를 불변으로 만들 수 없음

.

**빌더 패턴**

```java
new NutritionFacts.Builder(240, 8)
        .calories(100)
        .sodium(35)
        .carbohydrate(27)
        .build(); 
```

- [📝 점층적 생성자 패턴과 자바빈즈 패턴의 장점만 적용한 빌드 패턴](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter2/item2/builder/NutritionFacts.java)
  - 점층적 생성자보다 클라이언트 코드를 읽고 쓰기가 훨씬 **간결**
  - 필수 필드의 값은 강제하고, 옵셔널한 값은 선택적으로 세팅할 수 있으므로 자바빈즈보다 훨씬 **안전**
- 플루언트 API 또는 메서드 체이닝 적용
- [📝 계층적으로 설계된 클래스와 함께 사용하기 좋음](https://github.com/WegraLee/effective-java-3e-source-code/tree/master/src/effectivejava/chapter2/item2/hierarchicalbuilder)
  - 각 계층의 클래스에 관련 빌더를 멤버로 정의
  - 추상 클래스는 [추상 빌더](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter2/item2/hierarchicalbuilder/Pizza.java)를, 구체 클래스는 [구체 빌더](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter2/item2/hierarchicalbuilder/Calzone.java)를 갖도록 하자.
  - 계층 구조에서 self() 메소드를 통해 형변환을 줄이고, 하위 빌더에 메서드를 추가할 수 있음
- 클라이언트는 필요한 객체를 직접 만드는 대신, 필수 매개변수만으로 생성자를 호출해 빌더 객체를 얻는다.
  - 그 후 빌더 객체가 제공하는 일종의 세터 메서드들로 원하는 선택 매개변수들을 설정
- **빌더 패턴의 단점도 존재**
  - 빌더 생성 비용이 크지는 않지만 성능에 민감한 상황에서는 문제가 될 수 있음
  - 점층적 생성자 패턴보다는 코드가 장황해서 매개변수 4개 이상은 되어야 값어치를 함

.

**@Builder**

- 장점.
  - 애노테이션 하나로 **간결**하게 빌더 패턴을 구현
  - target.classes.. 에서 생성된 Builder 클래스 확인 가능
- 단점.
  - 빌더뿐만 아니라 모든 매개변수를 파라미터로 받는 생성자 자동 생성
  - **필수값 지정 불가**(필수 값을 생성자에 넣어주고 싶을 경우 어려움)

```java
@Builder
// 모든 매개변수를 파라미터로 받는 생성자를 외부에서 호출하지 못 하도록 AccessLevel 설정
@AllArgsConstructor(access = AccessLevel.PRIVATE) 
public class NutritionFacts {
  private final int servingSize;
  private final int servings;
  private final int calories;
  //..
}

...

new NutritionFacts.NutritionFactsBuilder()
        .servingSize(10)
        .servings(10)
        .build();
```

<br>

## item 3. private 생성자나 열거 타입으로 싱글턴임을 보증하라.

> 만들려는 싱글턴이 Enum 이외의 클래스를 상속하지 않는다면, "원소가 하나인 열거 타입을 선언" 방식을 선택해 보자.

📖

싱클턴을 만드는 세 가지 방법

.

**`private 생성자 + public static final 필드 방식의 싱글턴`**

```java
public class Elvis {
    public static final Elvis INSTANCE = new Elvis();
    private Elvis() { }

    public void leaveTheBuilding() { ... }

    public void sing() { ... }
}

...

Elvis elvis = Elvis.INSTANCE;
elvis.leaveTheBuilding();
```

장점.

- public, protected 생성자가 없으므로 클래스 초기화 시 만들어진 인스턴스가 전체 시스템에서 **하나뿐임을 보장**
- 간결하고 해당 클래스가 싱글턴인 것이 API(javadocs)에 명백히 드러남
  - final 이므로 **다른 객체 참조 불가**

단점.

- (인터페이스가 없다면) 싱글톤을 사용하는 클라이언트가 **테스트하기 어려움**
  - 인터페이스를 생성해서 Mock 객체로 테스트 가능
- 리플렉션으로 private 생성자 호출 가능
  - 생성자 두 번째 호출 시 인스턴스 생성 막는 방법 필요
    ```java
    // 선언 되어 있는 기본 생성자에 접근(접근 지시자에 상관 없이 접근 가능)
    Constructor<Elvis> defaultConstructor = Elvis.class.getDeclaredConstructor();
    defaultConstructor.setAccessible(true);
    Elvis elvis1 = defaultConstructor.newInstance();
    Elvis elvis2 = defaultConstructor.newInstance();

    ...

    // 생성자 두 번째 호출 시 인스턴스 생성 막는 방법 필요
    private static boolean created;

    private Elvis() {
        if (created) {
            throw new UnsupportedOperationException("can't be created by constructor.");
        }
        created = true;
    }
    ```
- 역직렬화 시 새로운 인스턴스가 생성될 수 있음
  - 역직렬화 시 새로운 인스턴스가아닌 기존 인스턴스 리턴하도록 재정의
    ```java
    // 직렬화
    try (ObjectOutput out = new ObjectOutputStream(new FileOutputStream("elvis.obj"))) {
        out.writeObject(Elvis.INSTANCE);
    } catch (IOException e) {
        e.printStackTrace();
    }

    // 역직렬화
    try (ObjectInput in = new ObjectInputStream(new FileInputStream("elvis.obj"))) {
        Elvis elvis3 = (Elvis) in.readObject();
        System.out.println(elvis3 == Elvis.INSTANCE);
    } catch (IOException | ClassNotFoundException e) {
        e.printStackTrace();
    }

    ...

    public class Elvis implements IElvis, Serializable {
      //...

      // 역직렬화 시 새로운 인스턴스가아닌 기존 인스턴스 리턴하도록 재정의
      // 진짜 Elvis를 반환하고, 가짜 Elvis는 가비지 컬렉터에
      private Object readResolve() {
          return INSTANCE;
      }
    }
    ```

.

**`private 생성자 + 정적 팩터리 방식의 싱글턴`**

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

장점

- API 변경 없이 싱글턴이 아니도록 변경 가능
  - 클라이언트 코드는 유지하면서 내부 코드 변경 가능
- 정적 팩터리를 제네릭 싱글턴 팩터리로 만들 수 있음
  - 클라이언트가 원하는 타입을 사용할 수 있도록 지원
  ```java
  public class MetaElvis<T> {
      private static final MetaElvis<Object> INSTANCE = new MetaElvis<>();
      private MetaElvis() { }

      @SuppressWarnings("unchecked")
      public static <E> MetaElvis<E> getInstance() { return (MetaElvis<E>) INSTANCE; }

      public void say(T t) { ... }

      public void leaveTheBuilding() { ... }

      public static void main(String[] args) {
          MetaElvis<String> elvis1 = MetaElvis.getInstance();
          MetaElvis<Integer> elvis2 = MetaElvis.getInstance();
          elvis1.say("hello");
          elvis2.say(100);
      }
  }
  ```
- 정적 팩터리의 메서드 참조를 공급자(Supplier<>)로 사용 가능
  ```java
  public class Concert {
      public void start(Supplier<Singer> singerSupplier) {
          Singer singer = singerSupplier.get();
          singer.sing();
      }
      public static void main(String[] args) {
          Concert concert = new Concert();
          concert.start(Elvis::getInstance);
      }
  }
  ```

단점

- private 생성자 + public static final 필드 방식의 싱글턴과 동일한 단점

.

**`원소가 하나인 열거 타입을 선언`**

```java
public enum Elvis {
    INSTANCE;

    public void leaveTheBuilding() { ... }
}

..

Elvis elvis = Elvis.INSTANCE;
elvis.leaveTheBuilding();
```

- 가장 간결한 방법이고, 직렬화와 리플렉션에도 안전
  - 아주 복잡한 직렬화 상황이나 리플렉션 공격에서도 제 2의 인스턴스가 생기는 일을 완벽하게 방어
  - enum 은 리플렉션 내부 코드에서 생성자를 가져올 수 없도록 설정
  - new 키워드로 enum 을 생성할 수 없는 특성을 반영
- <u>*대부분 상황에서 원소가 하나뿐인 열거 타입이 싱글턴을 만드는 가장 좋은 방법*</u>
- 단, 만들려는 싱글턴이 Enum 이외의 클래스를 상속해야 한다면 이 방법은 사용 불가

<br>

## item 4. 인스턴스화를 막으려거든 private 생성자를 사용하라.

```java
public class UtilityClass {
    /**
     * 이 클래스는 인스턴스를 만들 수 없습니다.
     * 기본 생성자가 만들어지는 것을 방지(인스턴스화 방지로 상속 불가능)
     */
    private UtilityClass() {
        throw new AssertionError();
    }
    // ...
}
```

- 추상(abstract) 클래스로 만드는 것으로는 인스턴스화를 막을 수 없다
  - 기본 생성자가 자동으로 생성
  - 상속받은 자식 클래스의 인스턴스 생성 시 상위 클래스의 생성자를 자동으로 호출하는 자바 특성
- 컴파일러가 기본 생성자를 만드는 경우는 오직 명시된 생성자가 없을 때뿐이니 `private 생성자를 추가하면 클래스의 인스턴스화를 막을 수 있다.`
  - 생성자에 주석으로 인스턴스화 불가한 이유를 설명하는 것이 좋다
  - 상속을 방지할 때도 같은 방법을 사용할 수 있다
- ex. 인스턴스를 만들 수 없는 유틸리스 클래스
  - 정적(static) 메서드만 담은 유틸리티 클래스는 인스턴스로 만들어 쓰려고 설계한 클래스가 아님

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

```java
// 자원을 직접 명시하지 말고
private static final Dictionary dictionary = new Dictionary();

...

// 의존 객체 주입 사용
public class SpellChecker {
    // Dictionary interface 를 주입받아서 코드의 재사용성을 높일 수 있음
    private final Dictionary dictionary; 
    // 생성자에 필요한 자원을 넘겨준다.
    public SpellChecker(Dictionary dictionary) {
        this.dictionary = Object.requireNonNull(dictionary);
    }
    
    public boolean isValid(String word) { ... }
    public List<String> suggestions(String typo) { ... }
}
```
- 사용하는 자원에 따라 동작이 달라지는 클래스에는 정적 유틸리티 클래스나 싱글턴 방식이 비적합
- 대신 클래스가 `여러 자원 인스턴스를 지원`해야 하며, `클라이언트가 원하는 자원`을 사용해야 한다.
- `의존 객체 주입 패턴`: <u>*인스턴스를 생성할 때 생성자에 필요한 자원을 넘겨주는 방식*</u>
  - 변형 방식으로 생성자에 자원 팩터리를 넘겨줄 수 있음
  - 의존 객체 주입 통해 클래스의 유연성, 재사용성, 테스트 용이성 개선 가능
- 의존 객체 주입 프레임워크(Dagger, Guice, Spring)를 사용하면 큰 프로젝트에서 코드가 어지러워지는 단점 개선 가능

<br>

## item 6. 불필요한 객체 생성을 피하라.

`문자열`

```java
/**
 * 불필요한 객체 생성으로 인한 메모리 낭비 개선
 */
String hello = "hello"; // JVM은 내부적으로 문자열을 pool에 캐싱
String hello2 = new String("hello"); // 강제로 새로운 문자열 생성
```
- new String("str")을 사용하지 않고, 문자열 리터럴("str)을 재사용하는 것을 권장
- 문자열 리터럴은 사실상 동일한 객체라서 매번 새로 만들 필요가 없음
  - 똑같은 기능의 객체를 매번 생성하기보다 **객체 하나를 재사용**하는 편이 나을 때가 많음
- 생성자 대신 정적 팩터리 메서드를 제공하는 불변 클래스에서는 정적 팩터리 메서드를 사용해 불필요한 객체 생성을 피할 수 있음 
  - 생성자는 호출할 때마다 새로운 객체를 만들지만, 팩터리 메서드는 그렇지 않다.
  - ex. Boolean.valueOf(String)

`정규식 Pattern`

```java
/**
 * 값비싼 객체를 재사용해 성능을 개선
 */ 
public class RomanNumerals {
    private static final Pattern ROMAN = Pattern.compile(
                "^(?=.)M*(C[MD]|D?C{0,3})"
                + "(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$");

    static boolean isRomanNumeralFast(String s) {
        return ROMAN.matcher(s).matches();
    }
}
```
- 생성 비용(CPU 리소스)이 비싼 객체라서 반복해서 생성하기 보다, 캐싱하여 재사용하는 것을 권장
- 동일한 패턴이 여러번 사용된다면 필드로 선언해서 사용 권장

`오토박싱`(Auto Boxing)

```java
/**
 * 불필요한 객체 생성으로 인한 메모리 낭비 개선
 */
private static long sum() {
    Long sum = 0L; // Long으로 선언해서 불필요한 인스턴스가 약 2^31개나 생성
    for (long i = 0; i <= Integer.MAX_VALUE; i++)
        sum += i;
    return sum;
}
```
- 기본 타입(int)을 그에 상응하는 박싱된 기본 타입(Integer)으로 상호 변환해주는 기술
- 기본 타입과 박싱된 기본 타입을 섞어서 사용하면 변환하는 과정에서 불필요한 객체가 생성될 수 있음
- 박싱된 기본 타입보다는 기본 타입을 사용하고, 의도치 않은 오토박싱이 숨어들지 않도록 주의하자

<br>

## item 7. 다 쓴 객체 참조를 해제하라.

> 메모리 누수는 겉으로 잘 드러나지 않아 시스템에 수년간 잠복하는 사례도 있다.
> 
> 이런 누수는 철저한 코드 리뷰나 힙 프로파일러 같은 디버깅 도구를 동원해야만 발견되기도 한다.
> 
> 그래서 이런 종류의 문제는 예방법을 익혀두는 것이 매우 중요하다.

📖

CG(가비지 컬렉션) 언어에서는 메모리 누수를 찾기가 아주 까다로움
- 메모리 누수로 단 몇 개의 객체가 매우 많은 객체를 회수되지 못하게 할 수 있고, 잠재적으로 성능에 악영향을 줄 수 있음
  - 어떤 객체에 대한 레퍼런스가 남아있다면 해당 객체는 가비지 컬렉션의 대상이 되지 않음
- 해법은 해당 참조를 다 썻을 때 **참조 해제(null 처리)하기**
  - 참조 해제의 가장 좋은 방법은 <u>*그 참조를 담은 변수를 유효 범위 밖으로 밀어내는 것*</u>
- 자기 메모리를 직접 관리하는 클래스(Stack, Cache, Listener/Callback)라면 항시 메모리 누수에 주의
  
.

**`참조 해제 방법`**

(1) 해당 참조를 다 사용했을 경우 `null 처리`
```java
public Object pop() {
    if (size == 0) {
        throw new EmptyStackException();
    }
    Object result = elements[--size];
    elements[size] = null; // 다 쓴 참조 해제
    return result;
}
```

(2) `WeakHashMap` 자료구조
- 약한 참조로 저장(WeakHashMap애 Key로 저장) 시 가비지 컬렉터가 즉시 수거

```java
public class PostRepository {
    private Map<CacheKey, Post> cache;

    public PostRepository() {
        this.cache = new WeakHashMap<>();
    }

    public Post getPostById(CacheKey key) {
        if (cache.containsKey(key)) {
            return cache.get(key);
        } else {
            // DB, REST API를 통한 조회
            Post post = new Post();
            cache.put(key, post);
            return post;
        }
    }
    //...
}
...

PostRepository postRepository = new PostRepository();
CacheKey key1 = new CacheKey(1);
postRepository.getPostById(key1);

assertFalse(postRepository.getCache().isEmpty());

key1 = null;
// WeakHashMap Key 는 GC가 즉시 수거
System.out.println("run gc");
System.gc();
System.out.println("wait");
Thread.sleep(3000L);

assertTrue(postRepository.getCache().isEmpty());
```

(3) `Background Threads` & `LRU Cache`
- LRU(Least Recently Used) cache
- 가장 오랫동안 사용되지 않은 캐시 제거

```java
ScheduledExecutorService executor = Executors.newScheduledThreadPool(1);
PostRepository postRepository = new PostRepository();
CacheKey key1 = new CacheKey(1);
postRepository.getPostById(key1);

// 백그라운드 스레드에서 가장 오랫동안 사용되지 않은 캐시 제거
Runnable removeOldCache = () -> {
    System.out.println("running removeOldCache task");
    Map<CacheKey, Post> cache = postRepository.getCache();
    Set<CacheKey> cacheKeys = cache.keySet();
    Optional<CacheKey> key = cacheKeys.stream().min(Comparator.comparing(CacheKey::getCreated));
    key.ifPresent((k) -> {
        System.out.println("removing " + k);
        cache.remove(k);
    });
};

// 처음에 1초 있다가 3초마다 러너 실행
executor.scheduleAtFixedRate(removeOldCache, 1, 3, TimeUnit.SECONDS);
// 20초동안 애플리케이션을 돌리는 동안 별도의 스레드기 수행
Thread.sleep(20000L);
executor.shutdown();
```

<br>

## item 8. finalizer와 cleaner 사용을 피하라.

> cleaner(java8 까지는 finalizer)는 안전망 역할이나 중요하지 않은 네이티브 자원 회수용으로만 사용하자.
> 
> 물론 이런 경우라도 불확실성과 성능 저하에 주의해야 한다.

📖

자바는 두 가지 객체 소멸자(`finalizer`, `cleaner`)를 제공

- finalizer는 예측할 수 없고, 상황에 따라 위험할 수 있어 일반적으로 불필요
- cleaner는 finalizer보다는 덜 위험하지만, 여전히 예측할 수 없고, 느리고, 일반적으로 불필요
- finalizer와 cleaner로는 제때 수행되어야 하는 작업은 절대 할 수 없음
  - 즉시 수행된다는 보장이 없고, GC 알고리즘에 달려있어 GC 구현마다 천차만별
- 상태를 영구적으로 수정하는 작업에서는 절대 finalizer, cleaner에 의존하지 말자
- finalizer와 cleaner는 심각한 성능 문제도 동반
- finalizer를 사용한 클래스는 finalizer 공격에 노출되어 심각한 보안 문제를 일으킬 수도 있음
  - final이 아닌 클래스를 finalizer 공격으로부터 방어하려면 아무 일도 하지 않는 finalize 메서드를 만들고 final로 선언하기

.

반납할 자원이 있는 클래스는 `AutoCloseable`을 구현하고, 클라이언트에서 `close()`를 호출하거나 `try-with-resource`를 사용하도록 하자.

```java
public class AutoClosableIsGood implements Closeable {

    private BufferedReader reader;

    //...

    @Override
    public void close() {
        try {
            reader.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}

...

try (AutoClosableIsGood good = new AutoClosableIsGood()) {
    //...
}
```

.

cleaner 와 finalizer 의 사용

(1). 자원의 소유자가 close 메서드를 호출하지 않는 것에 대비한 `안전망 역할`
- PhantomReference 사용
- 호출되리라는 보장이 없지만 없는 것 보다는 나을 수 있음

(2). `Native peer` 와 연결된 객체에서 자원을 즉시 회수해야 한다면 close 메서드를 사용
- 성능 저하를 감당할 수 있고 네이티브 피어가 심각한 자원을 가지고 있지 않을 때에만 해당
- 네이티브 피어는 자바 객체가 아니라 가비지 컬렉터는 그 존재를 알지 못함


[📝 cleaner를 안전망으로 활용하는 AutoCloseable Class](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter2/item8/Room.java)

[📝 cleaner 안전망을 갖춘 자원을 제대로 활용하는 클라이언트](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter2/item8/Adult.java)

[📝 cleaner 안전망을 갖춘 자원을 제대로 활용하지 못하는 클라이언트](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter2/item8/Teenager.java)

<br>

## item 9. try-finally 보다는 try-with-resources를 사용하라.

> 꼭 회수해야 하는 자원을 다룰 때는 try-finally 말고, try-with-resources 를 사용하자.
> 
> 예외는 없다. 코드는 더 짧고 분명해지고, 만들어지는 예외 정보도 훨씬 유용하다.
> 
> try-finally 로 작성하면 실용적이지 못할 만큼 코드가 지저분해지는 경우라도,
> 
> try-with-resources 로 정확하고 쉽게 자원을 회수할 수 있다.

📖

자원 닫기는 클라이언트가 놓치기 쉬워서 예측할 수 없는 성능 문제로 이어지기도 한다.

📝 복수의 자원을 처리하는 try-with-resources 는 짧고 매혹적

- try-with-resources 구조를 사용하려면 해당 자원이 AutoCloseable 인터페이스를 구현해야 한다.
- 프로그래머에게 보여줄 예외 하나만 보존되고 여러 개의 다른 예외는 숨겨짐
- 숨겨진 예외들도 스택 추적 내역에 숨겨졌다는 꼬리표를 달고 출력
  - try-finally 는 마지막 발생 예외만 보여주고 숨겨진 예외는 알 수 없음
- catch 절을 사용해서 다수 예외 처리 가능

```java
/**
 * try-finally
 */
InputStream in = new FileInputStream(src);
try {
    OutputStream out = new FileOutputStream(dst);
    try {
        byte[] buf = new byte[BUFFER_SIZE];
        int n;
        while ((n = in.read(buf)) >= 0)
            out.write(buf, 0, n);
    } finally {
        out.close();
    }
} finally {
    in.close();
}

...

/**
 * try-with-resources
 */
try (InputStream   in = new FileInputStream(src);
      OutputStream out = new FileOutputStream(dst)) {
    byte[] buf = new byte[BUFFER_SIZE];
    int n;
    while ((n = in.read(buf)) >= 0)
        out.write(buf, 0, n);
}
```

<br>

# 3장. 모든 객체의 공통 메서드

final이 아닌 Object 메서드(equals, hashCode, toString, clone, finalize)들을 언제, 어떻게 재정의해야 하는가

## item 10. equals는 일반 규약을 지켜 재정의하라.

> 꼭 필요한 경우가 아니면 equals 를 재정의하지 말자.
> 
> 많은 경우에 Object 의 equals 가 원하는 비교를 정확히 수행해준다.
> 
> 재정의해야 할 때는 그 클래스의 핵심 필드 모두를 빠짐없이, 다섯 가지 규약을 확실히 지켜가며 비교해야 한다.

📖

equals 메서드의 재정의에는 함정이 도사리고 있는데, 이 문제를 회피하는 가장 쉬운 길은 아예 재정의를 하지 않는 것.

.

**🔍 아래 상황 중 하나에 해당한다면 equals 메서드를 재정의하지 않는 것이 최선**

- **각 `인스턴스가 본질적으로 고유`할 경우**
  - 인스턴스가 단 하나 존재하는 클래스 (ex. 싱글톤, Enum)
  - 값 표현이 아닌 동작하는 개체를 표현하는 클래스 (ex. Thread)
- **인스턴스의 `'논리적 동치성'을 검사할 일이 없을` 경우**
  - 단순한 값 비교만으로 충분할 경우 (ex. 문자열)
- **상위 클래스에서 `재정의한 equals 가 하위 클래스에도 적절`할 경우**
  - Set, List, Map 구현체들은 상속을 받아 그대로 사용
- **클래스가 `private, package-private` 이고 equals 메서드를 호출할 일이 없을 경우**
  - equals 가 실수로라도 호출되는 것을 막고 싶다면 아래와 같이 구현해두자.
    ```java
    @Override public boolean equals(Object o) {
        throw new AssertioniError(); // 호출 금지!
    }
    ```

.

**🔍 equals를 재정의해야 하는 경우**

- 객체 식별성이 아닌 논리적 동치성을 확인해야 하는데, 상위 클래스의 equals 가 논리적 동치성을 비교하도록 재정의되지 않았을 경우
- ex. 주로 값 클래스. Integer, String ..

equals 메서드를 재정의할 때는 반드시 일반 규약을 따라야 함

- equals 메서드는 동치관계(equivalence relation)를 만족하며 다섯 가지 요건을 만족
  - 동치관계: 집합을 서로 같은 원소들로 이뤄진 부분집합으로 나누는 연산
    - 이 부분집합들을 동치류(equivalence class; 동치 클래스)라고 함
  
**`반사성(reflexivity)`**
```java
A.equals(A) == true
```
- null이 아닌 모든 참조 값 x에 대해, x.equals(x) == true
- 객체는 자기 자신과 같아야 한다.

**`대칭성(symmetry)`**
```java
A.equals(B) == B.equals(A)
```
- null이 아닌 모든 참조 값 x, y에 대해, x.equals(y)가 true면 y.equals(x)도 true
- 두 객체는 서로에 대한 동치 여부에 똑같이 답해야 한다.
  - equals 규약을 어기면 그 객체를 사용하는 다른 객체들이 어떻게 반응할지 알 수 없다.
  - 다른 타입을 지원하면 문제가 복잡해지고 대칭성이 꺠지기 쉽다.
- [📝 대칭성, 추이성 위배 코드](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter3/item10/inheritance/ColorPoint.java)
- [📝 리스코프 치환 원칙 위배 코드](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter3/item10/Point.java)
- 다른 타입을 지원하지 않고 대칭성을 만족
    ```java
    @Override public boolean equals(Object o) {
        return o instanceof CaseInsensitiveString &&
            ((CaseInsensitiveString) o).s.equalsIgnoreCase(s);
    }
    ```

**`추이성(transitivity)`**
```java
A.equals(B) && B.equals(C) && A.equals(C)
```
- null이 아닌 모든 참조 값 x, y, z에 대해, x.equals(y)가 true고, y.equals(z)도 true면 x.equals(z)도 true
- 구체 클래스를 확장해 새로운 값을 추가하면서 equals 규약을 만족시킬 방법은 존재하지 않는다.
  ```java
  public class ColorPoint extends Point {
      private final Color color;
      ...
  }
  ```
- [📝 equals 규약을 지키면서 값을 추가하려면 상속 대신 컴포지션을 사용하자.](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter3/item10/composition/ColorPoint.java)
  ```java
  public class ColorPoint {
      private final Point point;
      private final Color color;
      ...
  }
  ```

`일관성(consistency)`
```java
A.equals(B) == A.equals(B)
```
- null이 아닌 모든 참조 값 x, y에 대해, x.equals(y)를 반복해서 호출하면 항상 true 또는 false 반환
- 두 객체가 같다면 앞으로도 영원히 같아야 한다.
  - 클래스가 불변이든 가변이든 equals의 판단에 신뢰할 수 없는 자원이 끼어들게 해서는 안 된다.
  - 모든 객체가 null과 같지 않아야 한다.

`null-아님`
```java
A.equals(null) == false
```
- null이 아닌 모든 참조 값 x에 대해, x.equals(null)은 false
- 명시적 null 검사(o == null)보다는 묵시적 null 검사 권장
  - null 검사와 함께 타입 확인
```java
@Override public boolean equals(Object o) {
    // null이 인수로 주어지면 false를 반환
    if (!(o instanceof MyType))
        return false;
    MyType mt = (MyType) o;
    // ...
}
```
.

🔍 **양질의 equals 메서드 구현 방법**

1. `== 연산자를 사용해 입력이 자기 자신의 참조인지 확인`
2. `instanceof 연산자로 입력이 올바른 타입인지 확인`
3. `입력을 올바른 타입으로 형변환`
4. `입력 객체와 자기 자신의 대응되는 핵심필드들이 모두 일치하는지 하나씩 검사`

전형적인 equals 메서드의 예

```java
// 입력 타입은 반드시 Object (다중정의)
@Override public boolean equals(Object o) { 
    // 1. 반사성을 만족(필드들의 동치성만 검사해도 equals 규약을 어렵지 않게 지킬 수 있음)
    if (o == this) return true;
    // 2. 타입 비교
    if (!(o instanceof PhoneNumber)) return false;
    // 3. 타입 변환
    PhoneNumber pn = (PhoneNumber)o;
    // 4. 핵심 필드 비교
    return pn.lineNum == lineNum 
            && pn.prefix == prefix
            && pn.areaCode == areaCode;
}
```

- Float.compare()와 Double.compare()을 제외한 기본 타입 필드는 == 연산자로 비교
  - 참조 타입 필드는 각각의 equals 메서드로 비교
- 배열 필드는 원소 각각을 앞서의 지침대로 비교하고, 모든 원소가 핵심 필드라면 Arrays.equals 메서드들 중 하나를 사용
- null 가능성이 있을 경우 Objects.equals(Object, Object) 비교로 NPE 방지
- equals의 성능을 위해 다를 가능성이 더 크거나 비교 비용이 싼 필드를 먼저 비교
- equals를 다 구현했다면 `대칭적`, `추이성`, `일관적`인지 자문
- equals를 재정의할 땐 hashCode도 반드시 재정의
- Object 외의 타입을 매개변수로 받는 equals 메서드는 선언하지 말자

.

equals, hashCode 메서드 자동 생성

- [Google AutoValue](https://github.com/google/auto/blob/main/value/userguide/index.md)
- [lombok](https://projectlombok.org/)
  - [@EqualsAndHashCode](https://projectlombok.org/features/EqualsAndHashCode)
  - [@ToString](https://projectlombok.org/features/ToString)
- [Record Class](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Record.html)
  - [Java 14 Record Keyword](https://www.baeldung.com/java-record-keyword)

<br>

## item 11. equals를 재정의하려거든 hashCode도 재정의하라

> equals를 재정의할 때는 hashCode도 반드시 재정의해야 한다. 그렇지 않으면 프로그램이 제대로 동작하지 않을 것이다.
> 
> 재정의한 hashCode는 Object의 API 문서에 기술된 일반 규약을 따라야 하며, 서로 다른 인스턴스라면 되도록 해시코드도 서로 다르게 구현해야 한다.

📖

equals 를 재정의한 클래스 모두에서 hashCode 도 재정의해야 한다.
- 그렇지 않을 경우, hashCode 일반 규약을 어기게 되어 해당 클래스의 인스턴스를 HashMap 이나 HashSet 같은 컬렉션의 원소로 사용할 때 문제를 유발

**Object 명세에서 발췌한 규약**

- equals 비교에 사용하는 정보가 `변경되지 않았다면`, hashCode 는 `매번 같은 값을 리턴`해야 한다.
  - equals 가 변경되거나, 애플리케이션을 다시 실행했다면 달라질 수 있다.
- 두 객체에 대한 `equals 가 같다`면, `hashCode 값도 같아`야 한다.
- 두 객체에 대한 `equals 가 다르`더라도, hashCode 값은 같을 수 있지만 해시 테이블 성능을 고려해 `다른 값을 리턴`하는 것이 좋다.
  
참고. **`해시 충돌`**

- 다른 두 객체가 같은 hashCode를 가지고 Hash Collection에 저장될 때 해시 충돌 발생
- 해시 충돌이 발생하면 Hash는 값을 Object가 아닌 LinkedList로 저장
- 해시 조회 시 LinkedList를 순회하면서 equals 비교로 같은 인스턴스를 탐색
- 해시맵의 장점(`O(1)`)이 없어지고 LinkedList를 사용하는 것과 동일(`O(N)`)한 성능
- java 8 에서 해시 충돌 개수가 8개를 넘어가면 LinkedList 대신 이진 트리(`O(logN)`)를 사용하도록 개선
  - [HashMap Performance Improvements in Java 8](https://dzone.com/articles/hashmap-performance)

**재정의 시 주의사항**

- 성능 때문에 핵심 필드를 해시코드 계산할 시 제외하면 안 된다.
- 해시코드 계산 규칙을 API에 노출하지 않는 것이 좋다.

**hashCode 메서드 재정의**

```java
/**
 * lombok @EqualsAndHashCode
 * - 사용 편의성 관점에서 권장하는 방법
 * - 이미 테스트를 거친 상태이므로 테스트 불필요
 */
@EqualsAndHashCode
public class PhoneNumber {
}

/**
 * IDE 에서 제공해 주는 hashCode 메서드
 * - Objects 클래스의 hash 메서드
 */
@Override public int hashCode() {
    return Objects.hash(lineNum, prefix, areaCode);
}

/**
 * 전형적인 hashCode 메서드
 * - 사전의 모든 단어에 31 을 사용했을 때, 해시 충돌이 가장 적었다는 연구 결과를 반영
 */
@Override public int hashCode() {
    int result = Short.hashCode(areaCode); // 핵심 필드 하나의 해쉬값 계산
    result = 31 * result + Short.hashCode(prefix);
    result = 31 * result + Short.hashCode(lineNum);
    return result;
}

/**
 * 구글 구아바의 com.google.common.hash.Hashing
 * - 좋은 성능을 가지고 있지만 hashCode 구현을 위해 라이브러리 추가 필요
 * - https://mvnrepository.com/artifact/com.google.guava/guava
 */
@Override public int hashCode() {
    return Hashing.goodFastHash(32)
            .hashObject(this, PhoneNumberFunnel.INSTANCE)
            .hashCode();
}

/**
 * 해시코드를 지연 초기화하는 hashCode 메서드
 * - 스레드 안정성을 위해 Double Checked Locking 기법 적용
 * - volatile field: Thread-safety 한 변수
 *   - 보통 변수를 CPU cache 에 저장해서 예전 캐시 값을 읽어올 수도 있지만,
 *   - volatile 는 변수를 Main Memory 에 저장해서 가장 최근에 업데이터된 데이터를 참조
 */
private volatile int hashCode;

@Override public int hashCode() {
    // First check outside synchronized
    if (this.hashCode != 0) {
        return hashCode;
    }

    synchronized (this) {
        int result = hashCode;
        // Second check in synchronized
        if (result == 0) {
            result = Short.hashCode(areaCode);
            result = 31 * result + Short.hashCode(prefix);
            result = 31 * result + Short.hashCode(lineNum);
            this.hashCode = result;
        }
        return result;
    }
}
```

📝 [hashCode 메서드 재정의](https://github.com/WegraLee/effective-java-3e-source-code/blob/master/src/effectivejava/chapter3/item11/PhoneNumber.java)

<br>

## item 12. toString을 항상 재정의하라.

> 모든 구체 클래스에서 Object의 toString을 재정의하자(상위 클래스에서 이미 알맞게 재정의한 경우는 예외)
> 
> toString을 재정의한 클래스는 사용하기도 즐겁고, 그 클래스를 사용한 시스템을 디버깅하기 쉽게 해준다.
> 
> toString은 해당 객체에 관한 명확하고 유용한 정보를 간결하고 읽기 좋은 형태로 반환해야 한다.

📖

- Object의 toString은 *클래스이름@16진수*로 표시한 해시 코드
- 객체가 가진 보여줄 수 있는 모든 정보를 보여주는 것이 좋다.
- 값 클래스라면 포맷을 문서에 명시하는 것이 좋으며, 해당 포맷으로 객체를 생성할 수 있는 정적 팩터리나 생성자를 제공하는 것이 좋다.
- toString이 반환한 값에 포함된 정보를 얻어올 수 있는 API(Getter)를 제공하는 것이 좋다.
- 경우에 따라 AutoValue, 롬복 또는 IDE를 사용하지 않는게 적절할 수 있다.
  - ex. 전화번호, 주소, 좌표, 위도, 경도 등 특정 포맷이 정해져있는 경우

📝 포맷을 명시한 경우

```java
public final class PhoneNumber {
    //..

    /**
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

    // 특정 포맷으로 객체를 생성할 수 있는 정적 팩터리나 생성자
    public static PhoneNumber of(String phoneNumberString) {
        String[] split = phoneNumberString.split("-");
        PhoneNumber phoneNumber = new PhoneNumber(
                Short.parseShort(split[0]),
                Short.parseShort(split[1]),
                Short.parseShort(split[2]));
        return phoneNumber;
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

Cloneable을 구현한 클래스는 clone 메서드를 public으로 제공
- 사용자는 당연히 복제가 제대로 이뤄지리라 기대하지만, 깨지기 쉽고, 위험하고, 모순적인 매커니즘이 탄생..

.

**clone 규약**

- x.clone() != x (clone은 원본과 다른 인스턴스)
- x.clone().getClass() == x.getClass()
- x.clone().equals(x) true가 아닐 수 있음 (객체마다 고유 식별자가 있을 경우)

.

📝 불변 상태를 참조하는 클래스용 clone 메서드

```java
public final class PhoneNumber implements Cloneable {
    // ...

    @Override public PhoneNumber clone() {
        try {
            // 재정의한 메서드의 반환 타입은 상위 클래스의 메서드가 반환하는 타입의 하위 타입일 수 있다.
            return (PhoneNumber) super.clone();
        } catch (CloneNotSupportedException e) {
            // checkedException → UncheckedException 변환
            throw new AssertionError();
        }
    }
}
```
- 불변 객체라면 Cloenable 인터페이스를 구현하고, super.clone()를 사용해서 clone 메서드를 재정의하면 충분
  - 접근 제한자는 public, 반환 타입은 자신의 클래스로 변경
  - Cloenable 인터페이스를 구현하지 않으면 CloneNotSupportedException 발생
- clone 메서드는 사실상 생성자와 같은 효과
  - clone은 원본 객체에 아무런 해를 끼치지 않는 동시에 복제된 객체의 불변식을 보장해야 한다.
  - 하지만, 정말 생성자를 사용하여 만든 객체를 반환하면 규약이 깨지게 된다.
    - 하위 타입이 상위 타입을 받을 수 없는 cannot be cast to class 예외 발생

.


📝 가변 상태를 참조하는 클래스용 clone 메서드

```java
public class Stack implements Cloneable {
    private Object[] elements;
    private int size = 0;

    //...

    @Override public Stack clone() {
        try {
            Stack result = (Stack) super.clone();
            // elements 필드가 복사본과 같은 메모리를 참조하지 않도록 배열의 clone을 재귀적으로 호출
            // 배열은 깊은 복사를 해주지 않으면 원본, 복사본 두 인스턴스가 동일한 배열을 참조
            result.elements = elements.clone();
            return result;
        } catch (CloneNotSupportedException e) {
            throw new AssertionError();
        }
    }
}
```

- 불변 상태를 참조하는 클래스용 clone 메서드와 기본적으로 동일
- 추가로, super.clone() 호출 후 필요한 필드를 적절히 수정
  - 배열 복제 시 배열의 clone 메서드 사용, 필요 시 deep copy
  - public 고수준 메서드(get, put)를 호출하는 방법 존재
  - clone 메서드 내에서 하위 클래스가 재정의할 수 있는 메서드는 사용하지 않기
    - 사용해야 한다면 재정의 불가능하도록 final 선언
  - 상속용 클래스(abstract class)는 Cloneable을 구현하지 않기
  - Cloneable을 구현한 스레드 안전 클래스를 작성할 때는 clone 메서드에 synchronized 선언으로 동기화
- 단점  
  - 모호한 규약
  - 필드에 final 사용 불가(clone 과정에서 필드 값 할당이 필요)
  - 생성자를 사용하지 않다보니 생성자에 있는 필드 검증 작업을 거치지 않음
  - 형변환 필요

.

`복사 생성자`와 `복사 팩터리`를 사용한 복사를 권장
- 문서화된 규약에 기대지 않고, 정상적인 final 필드 용법과 충돌하지 않고, 불필요한 검사 예외를 던지지 않고, 형변환도 필요하지 않음
  - 해당 클래스가 구현한 interface 타입의 인스턴스를 인수로 받을 수 있음
  - 클라이언트는 원본의 구현 타입에 얽매이지 않고 복제본의 타입을 직접 결정 가능
    ```java
    public TreeSet(Comparator<? super E> comparator) {
        this(new TreeMap<>(comparator));
    }

    ...

    TreeSet<PhoneNumber> numbers = new TreeSet<>(Comparator.comparingInt(PhoneNumber::hashCode));
    ```

📝 `복사 생성자` (변환 생성자, conversion constructor)

```java
// 자신과 같은 클래스의 인스턴스를 인수로 받는 생성자
public PhoneNumber(PhoneNumber phoneNumber) {
    this(phoneNumber.areaCode, phoneNumber.prefix, phoneNumber.lineNum);
}
```

📝 `복사 팩터리` (변환 팩터리, conversion factory)

```java
// 복사 생성자를 모방한 정적 팩터리
public static PhoneNumber newInstance(PhoneNumber phoneNumber) {
    return new PhoneNumber(phoneNumber.areaCode, phoneNumber.prefix, phoneNumber.lineNum);
}
```

<br>

## item 14. Comparable을 구현할지 고려하라.

> 순서를 고려해야 하는 값 클래스를 작성한다면 반드시 Compareable 인터페이스를 구현하여, 
> 
> 그 인스턴스들을 쉽게 정렬하고, 검색하고, 비교 기능을 제공하는 컬렉션과 어우러지도록 하자.
>
> compareTo 메서드에서 필드의 값을 비교할 때, < 와 > 연산자는 쓰지 말자.
>
> 그 대신 박싱된 기본 타입 클래스가 제공하는 정적 compare 메서드나 
> 
> Comarator 인터페이스가 제공하는 비교자 생성 메서드를 사용하자.

📖

알파벳, 숫자, 연대 같이 순서가 명확한 값 클래스를 작성한다면 반드시 Comparable 인터페이스를 구현하자.
- Compareable 구현으로 수많은 제네릭 알고리즘과 컬렉션의 힘을 누릴 수 있다.

```java
public interface Comparable<T> {
    int compareTo(T t);
}
```

.

**compareTo 규약은 equals 규약과 유사**

- 단순 동치성 비교(Object.equals)에 더해 `순서 비교`가 가능하며 `Generic 지원`
  - 자기 자신(this)이 compareTo에 전달된 객체보다 `작으면 음수`, `같으면 0`, `크다면 양수` 반환
  - 비교할 수 없는 타입일 경우 ClassCastException
- 반사성, 대칭성, 추이성, 일관성을 만족해야 한다.
  ```java
  // 반사성
  n1.compareTo(n1)

  // 대칭성
  // x.compareTo(y)는 y.compareTo(x)가 예외를 던질 때에 한해 예외를 던져야 한다.
  x.compareTo(y) == -y.compareTo(x)

  // 추이성
  n1.compareTo(n2) > 0
  n2.compareTo(n3) > 0
  n1.compareTo(n3) > 0

  // 일관성
  x.compareTo(y) == 0 이면 sgn(x.compareTo(z)) == sgn(y.compareTo(z))
  ```
- 반드시 따라야 하는 것은 아니지만 x.compareTo(y) == 0 이라면 x.equals(y) == true
  ```java
  BigDecimal oneZero = new BigDecimal("1.0");
  BigDecimal oneZeroZero = new BigDecimal("1.00");
  System.out.println(oneZero.compareTo(oneZeroZero)); // 0(Tree, TreeMap)
  System.out.println(oneZero.equals(oneZeroZero)); // false(순서가 없는 콜렉션)
  ```
- compareTo 규약을 지키지 못하면 비교를 활용하는 클래스와 어울리지 못함

.

**compareTo 구현 방법 (Compratable 구현)**

- (1) 자연적인 순서를 제공할 클래스에 implements Compratable<T> 선언
- (2) compareTo 메서드를 재정의
- (3) comprareTo 메서드 안에서 기본 타입은 박싱된 기본 타입의 compare을 사용해 비교
- (4) 핵심 필드가 여러 개라면 비교 순서가 중요
  - 순서를 결정하는데 있어서 가장 중요한 필드를 비교하고, 그 값이 0이라면 다음 필드를 비교

```java
// (1) 자연적인 순서를 제공할 클래스에 implements Compratable<T> 선언
public final class PhoneNumber implements Comparable<PhoneNumber> {
    private final short areaCode, prefix, lineNum;

    //...

    // (2) compareTo 메서드를 재정의
    @Override
    public int compareTo(PhoneNumber pn) {
        // (3) comprareTo 메서드 안에서 기본 타입은 박싱된 기본 타입의 compare을 사용해 비교
        int result = Short.compare(areaCode, pn.areaCode);
        // (4) 핵심 필드가 여러 개라면 비교 순서가 중요
        if (result == 0)  {
            result = Short.compare(prefix, pn.prefix);
            if (result == 0)
                result = Short.compare(lineNum, pn.lineNum);
        }
        return result;
    }
```

- 기존 클래스를 확장하고 필드를 추가하는 경우 compareTo 규약을 지킬 수 없음
  - 자식 클래스에서 Compratable 구현 불가
  - 이 경우, Composition 활용
    ```java
    public class NamedPoint implements Comparable<NamedPoint> {

        private final Point point;
        private final String name;

        // ...

        @Override
        public int compareTo(NamedPoint namedPoint) {
            // Point 비교는 Point 클래스에서 재정의한 compareTo 사용
            int result = this.point.compareTo(namedPoint.point);
            if (result == 0) {
                result = this.name.compareTo(namedPoint.name);
            }
            return result;
        }
    }

    ...

    public class Point implements Comparable<Point>{
        // ...
        @Override
        public int compareTo(Point point) {
            int result = Integer.compare(this.x, point.x);
            if (result == 0) {
                result = Integer.compare(this.y, point.y);
            }
            return result;
        }
    }
    ```

.

**compareTo 구현 방법 (Comprator 구현)**

- 자바 8부터 `함수형 인터페이스, 람다, 메서드 레퍼런스`와 Comprator가 제공하는 `기본 메서드, static 메서드`를 사용해서 Comprator 구현 가능
- 자바의 정적 임포트 기능을 이용하면 정적 비교자 생성 메서드들을 그 이름만으로 사용할 수 있어 코드가 간결
- Comparator가 제공하는 메서드 사용하는 방법
  - (1) Comparator의 static 메서드를 사용해서 Comparator 인스턴스 만들기
  - (2) 인스턴스를 만들었다면 default 메서드를 사용해서 메서드 호출(체이닝) 이어가기
    - static, default 메소드의 매개변수로는 람다 표현식 또는 메서드 레퍼런스 사용 가능

```java
// (1) Comparator가 제공하는 static 메서드를 사용하여 Comparator 인스턴스 생성
private static final Comparator<PhoneNumber> COMPARATOR =
        comparingInt((PhoneNumber pn) -> pn.areaCode)
          // (2) 인스턴스를 만들었다면 default 메서드를 사용해서 메서드 호출(체이닝) 이어가기
          .thenComparingInt(pn -> pn.prefix)
          // static, default 메소드의 매개변수로는 람다 표현식 또는 메서드 레퍼런스 사용 가능
          .thenComparingInt(PhoneNumber::getLineNum);

@Override
public int compareTo(PhoneNumber pn) {
    return COMPARATOR.compare(this, pn);
}

...

@FunctionalInterface
public interface Comparator<T> {
    // ...
   default Comparator<T> thenComparingInt(ToIntFunction<? super T> keyExtractor) {
        return thenComparing(comparingInt(keyExtractor));
    }
}
```

<br>

# 용어 정리

**`열거 타입`**

열거 타입(Enum)은 인스턴트가 하나만 만들어짐을 보장

- 상수 목록을 담을 수 있는 데이터 타입
- 특정한 변수가 가질 수 있는 값을 제한(Type-Safety 보장)
- 싱글톤 패턴을 구현할 때 사용
- 자바 클래스처럼 생성자, 메소드, 필드를 가질 수 있음
- Enum 값은 == 연산자로 동일성을 비교(하나의 인스턴스만 있음을 보장)
- 특정 enum 타입이 가질 수 있는 모든 값 순회
  ```java
  public enum OrderStatus {
      PREPARING(0), SHIPPED(1), DELIVERING(2), DELIVERED(3);

      private int number;

      OrderStatus(int number) {
          this.number = number;
      }
  }

  ...

  Arrays.stream(OrderStatus.values()).forEach(System.out::println);
  ```
- **EnumMap**
  - enum을 키로 가지는 Map의 구현체
  - 특정 열거형에 대한 key-value 쌍을 저장하고 검색하는 데 사용
  - 내부적으로 배열을 이용하여 빠른 접근 및 메모리 효율성 제공
  - 열거형 상수의 순서를 이용하여 맵 내부에서 데이터를 저장하므로, 맵의 키 순서는 열거형 상수의 순서와 동일
    ```java
    enum Days { MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY }

    EnumMap<Days, String> schedule = new EnumMap<>(Days.class);
    schedule.put(Days.MONDAY, "Work");
    schedule.put(Days.FRIDAY, "Party");
    ```
- **EnumSet**
  - enum을 기반으로 한 Set의 구현체
  - 특정 열거형의 상수를 원소로 가지는 집합
  - 내부적으로 비트 벡터를 이용하여 빠른 접근 및 메모리 효율성을 제공
  - 열거형 상수의 순서를 이용하여 집합의 원소를 저장하므로, 집합의 원소 순서는 열거형 상수의 순서와 동일
  - HashSet보다 더 효율적인 구현을 제공하며, 열거형 상수의 크기가 작을 경우 매우 유용
    ```java
    EnumSet<OrderStatus> allOrderStatus = EnumSet.allOf(OrderStatus.class);
    EnumSet<Days> weekend = EnumSet.of(Days.SATURDAY, Days.SUNDAY);
    ```

.

**`Flyweight Pattern`** / Item 01

같은 객체가 자주 요청되는 상황이라면 플라이웨이트 패턴을 사용해 보자.

- 객체를 가볍게 만들어 메모리 사용을 줄이는 패턴
- 자주 변하는 속성(외적인 속성, extrinsti)과 변하지 않는 속성(내적인 속성, intrinsit)을 분리하고 재사용하여 메모리 사용을 줄일 수 있음
  
```java
public class Character {
    private char value;
    private String color;
    private Font font;
}

...

public class FontFactory {
    // Factory 클래스에 자주 사용하는 알고리즘을 캐싱
    private Map<String, Font> cache = new HashMap<>();

    public Font getFont(String font) {
        if (cache.containsKey(font)) {
            return cache.get(font);
        } else {
            String[] split = font.split(":");
            Font newFont = new Font(split[0], Integer.paserInt(sptli[1]));
            cache.put(font, newFont);
            return newFont;
        }
    }
}
```

.

**`Java8 Interface`** / Item 01

자바 8부터는 인터페이스가 정적 메서드를 가질 수 없다는 제한이 풀렸기 때문에 인스턴스화 불가 동반 클래스를 둘 이유가 별로 없다.

- 기본 메소드와 정적 메소드를 가질 수 있음
- **기본 메소드(default method)**
  - 인터페이스에서 메소드 선언 뿐 아니라, 기본적인 구현체까지 제공 가능
  - 기존의 인터페이스를 구현하는 클래스에 새로운 기능 추가 가능
  - java.util.Comparator.reversed()
- **정적 메소드**
  - private static 메소드 사용 가능(java9~)
  - 단, private 필드는 선언 불가

```java
public interface HelloService {
    String hello();

    static String hi() {
        prepareMessage();
        return "hi";
    }

    // 정적 메소드
    static private void prepareMessage() {
    }

    static String hi1() {
        prepareMessage();
        return "hi";
    }

    // 기본 메소드
    default String bye() {
        return "bye";
    }
}
```

.

**`Service Provider Framework`** / Item 01

확장 가능한 애플리케이션을 만드는 방법

- 코드를 변경하지 않고, 외적인 무언가를 변경했을 때 애플리케이션이 다르게 동작
- 주요 구성 요소
  - **서비스 제공자 인터페이스**(SPI)와 서비스 제공자(서비스 구현체)
    ```java
    public interface HelloService {
        String hello();
    }
    ```
  - **서비스 제공자 등록 API**(서비스 인터페이스의 구현체를 등록하는 방법)
    ```java
    @Configuration
    public class AppConfig {
        @Bean
        public HelloService helloService() {
            return new ChineseHelloService();
        }
    }
    ```
  - **서비스 접근 API**(서비스의 클라이언트가 서비스 인터페이스의 인스턴스를 가져올 때 사용하는 API)
    ```java
    ApplicationContext applicationContext = new AnnotationConfigApplicationContext(AppConfig.class);
    HelloService helloService = applicationContext.getBean(HelloService.class);
    ```
- 다양한 변형
  - **브릿지 패턴**
    - 구현부에서 추상층을 분리하여 각자 독립적으로 변형이 가능하고 확장이 가능
    - 기능과 구현에 대해서 두 개를 별도의 클래스로 구현
      ```java
      Champion KdaAri = new Ari(new KDA());
      KdaAri.skillQ();
      KdaAri.skillW();

      Champion poolPartyAri = new Ari(new PoolParty());
      poolPartyAri.skillQ();
      poolPartyAri.skillW();
      ```
  - **의존 객체 주입 프레임워크(Dependency Injection, DI)**
  - [java.util.ServiceLoader](https://docs.oracle.com/javase/tutorial/sound/SPI-intro.html)

.

**`Reflection`** / Item 01

서비스 제공자 인터페이스가 없다면 각 구현체를 인스턴스로 만들 때 [리플렉션](https://docs.oracle.com/javase/tutorial/reflect/)을 사용해야 한다.

- 클래스로더를 통해 읽어온 (거울에 반사된)클래스 정보를 사용하는 기술
- 클래스/애노테이션 정보를 읽어오거나, 인스턴스를 만들거나, 메소드를 실행하거나, 필드의 값을 가져오거나 변경 가능
  ```java
  Class<?> aClass = Class.forName("me.whiteship.hello.ChineseHelloService");
  Constructor<?> constructor = aClass.getConstructor();
  HelloService helloService = (HelloService) constructor.newInstance();
  ```
  - 특정 애노테이션이 붙어있는 필드 또는 메소드 읽어오기 (JUnit, Spring)
  - 특정 이름 패턴에 해당하는 메소드 목록 가져와 호출하기 (getter, setter)
  - etc..

.

**`JavaBean`** / Item 02

(주로 GUI에서) 재사용 가능한 소프트웨어 컴포넌트

자바빈이 지켜야 할 규약
- 아규먼트 없는 기본 생성자 → 객체를 쉽게 생성
- Serializable 인터페이스 구현 → 직렬화된 객체 재사용
- getter, setter 메소드 이름 규약 → 필드에 접근하는 일관적인 방법
  - 스프링, JPA 같은 여러 프레임워크에서 리플렉션을 통한 특정 객체의 값을 조회하거나 설정하기 위해 주로 사용

.

**`Object freezing`** / Item 02

임의의 객체를 불변 객체로 만들어 주는 javascript 기능

- Object.freeze()에 전달한 객체는 그 뒤로 변경 불가
  - 새 프로퍼티 추가 불가
  - 기존 프로퍼티 제거 불가
  - 기존 프로퍼티 값 변경 불가
  - 프로토타입 변경 불가
- strict 모드에서만 동작 (use strict)
- 비슷한 류의 펑션으로 Object.seal(), Object.preverntExtensions() 존재
- 어느 시점에 프리징되는지 예측을 못 하므로 잘 사용되지 않는 기능

.

**`Builder Pattern`** / Item 02

동일한 프로세스를 거쳐 다양한 구성의 인스턴스를 만드는 방법

- 복잡한 객체를 만드는 프로세스를 독립적으로 분리 가능

```java
public interface TourPlanBuilder {
  TourPlanBuilder nightsAndDays(int nights, int days);
  TourPlanBuilder title(String title);
  TourPlanBuilder startDate(LocalDate localDate);
  TourPlanBuilder whereToStay(String whereToStay);
  TourPlanBuilder addPlan(int day, String plan);
  TourPlan getPlan();
}

...

tourPlanBuilder.title("제주 여행")
    .nightsAndDays(2, 3)
    .startDate(LocalDate.of(2023,08,20))
    .whereToStay("리조트")
    .addPlan(0, "체크인 후 짐 풀기")
    .addPlan(0, "저녁 식사")
    .getPlan();
```

.

**`IllegalArgumentException`** / Item 02

잘못된 인자를 넘겨 받았을 때 사용할 수 있는 기본 런타임 예외

- 어떤 필드가 잘못 되었는지 인자로 전달하는 것을 권장
  ```java
  throw new IllegalArgumentException("deliveryDate cant't be earlier than " + LocalDate.now());
  ```
- Checked Exception, Unchecked Exception 차이
  - Checked Exception(Exception): 다시 예외을 던지거나, 예외 처리 필요
  - Unchecked Exception(RuntimeException): 던지거나 잡을 필요가 없음
- 메소드 선언부에 Unchecked Exception 을 선언하는 이유
  - 클라이언트에게 명시적으로 알려주고 싶을 경우 사용
  - 단, 가독성 이유로 보통은 선언하지 않음
- Checked Exception 사용 이유
  - 클라이언트가 해당 오류에 대한 후속 작업을 하길 원하는 경우 사용
- RuntimeException 상속 클래스
  ```java
  AnnotationTypeMismatchException, ArithmeticException, 
  ArrayStoreException, BufferOverflowException, 
  BufferUnderflowException, CannotRedoException, 
  CannotUndoException, ClassCastException, CMMException, 
  CompletionException, ConcurrentModificationException, DataBindingException, 
  DateTimeException, DOMException, EmptyStackException, 
  EnumConstantNotPresentException, EventException, FileSystemAlreadyExistsException, 
  FileSystemNotFoundException, IllegalArgumentException, IllegalMonitorStateException, 
  IllegalPathStateException, IllegalStateException, IllformedLocaleException, 
  ImagingOpException, IncompleteAnnotationException, IndexOutOfBoundsException, 
  JMRuntimeException, LSException, MalformedParameterizedTypeException, 
  MalformedParametersException, MirroredTypesException, MissingResourceException, 
  NegativeArraySizeException, NoSuchElementException, NoSuchMechanismException, 
  NullPointerException, ProfileDataException, ProviderException, 
  ProviderNotFoundException, RasterFormatException, RejectedExecutionException, 
  SecurityException, SystemException, TypeConstraintException, TypeNotPresentException, 
  UncheckedIOException, UndeclaredThrowableException, UnknownEntityException, 
  UnmodifiableSetException, UnsupportedOperationException, 
  WebServiceException, WrongMethodTypeException
  ```
- [Unchecked Exceptions](https://docs.oracle.com/javase/tutorial/essential/exceptions/runtime.html)

.

**`가변인수`** / Item 02

빌더를 사용하면 (빌더의 각 메소드에 나눠서) 가변인수(varargs) 매개변수를 여러 개 사용할 수 있다.

```java
public void printNumbers(int... numbers) {
    System.out.println(numbers.getClass().getCanonicalName()); // int[]
    System.out.println(numbers.getClass().getComponentType()); // int
    Arrays.stream(numbers).forEach(System.out::println);
}
```

- 여러 인자를 받을 수 있는 가변적인 Argument (Var+args)
- 메소드에 오직 하나만 선언 가능
- 메소드의 가장 마지막 매개변수가 되어야 함

.

**`메서드 참조`** / Item 03

메소드 하나만 호출하는 람다 표현식을 줄여쓰는 방법

```java
// 익명 내부클래스 적용
people.sort(new Comparator<Person>() {
    @Override
    public int compare(Person a, Person b) {
        return a.birthday.compareTo(b.birthday);
    }
});

...

// 람다 표현식 적용
people.sort((a, b) -> a.birthday.compareTo(b.birthday));
```
- 스태틱 메소드 레퍼런스
  ```java
  public static int compareByAge(Person a, Person b) {
      return a.birthday.compareTo(b.birthday);
  }

  people.sort(Person::compareByAge);
  ```
- 인스턴스 메소드 레퍼런스
  ```java
  public int compareByAge(Person a, Person b) {
      return a.birthday.compareTo(b.birthday);
  }

  Person person = new Person();
  people.sort(person::compareByAge);
  ```
- 임의 객체의 인스턴스 메소드 레퍼런스
  - 첫 번째 인자를 자기 자신으로 인식(Person a 생략 가능)
    ```java
    public int compareByAge(Person b) {
        return this.birthday.compareTo(b.birthday);
    }

    people.sort(Person::compareByAge);
    ```
- 생성자 레퍼런스
  ```java
  dates.stream().map(Person::new)
          .collect(Collectors.toList());
  ```
- [Method References](https://docs.oracle.com/javase/tutorial/java/javaOO/methodreferences.html)

.

**`함수형 인터페이스`** / Item 03

자바가 제공하는 기본 함수형 인터페이스

```java
Predicate<LocalDate> localDatePredicate = d -> d.isBefore(LocalDate.of(2000, 1, 1));
Function<LocalDate, Integer> getYear = LocalDate::getYear;
List<Integer> before2000 = dates.stream()
        .filter(localDatePredicate)
        .map(getYear)
        .collect(Collectors.toList());
```

- 함수형 인터페이스는 람다 표현식과 메소드 참조에 대한 **타겟 타입**을 제공
- 타겟 타입은 변수 할당, 메소드 호출, 타입 변환에 활용 가능
- 자바에서 제공하는 기본 함수형 인터페이스([**java.util.function package**](https://docs.oracle.com/javase/8/docs/api/java/util/function/package-summary.html))
  - 핵심 인터페이스 → 나머지는 대부분 여기서 파생
    ```java
    // input:Integer, output: String
    Function<Integer, String> intToString = (i) -> "hello";
    Function<Integer, String> intToString = Object::toString;

    /* 인터페이스 타입에 따라 각기 다른 생성자 참조 */
    // output: Object (기본 생성자)
    Supplier<Person> personSupplier = Person::new;
    // input: LocalDate, output: Person (LocalDate 를 파라미터로 받는 생성자)
    Function<LocalDate, Person> personFunction = Person::new;
    
    // input: Integer
    Consumer<Integer> integerConsumer = System.out::println;

    // input: Person, output: boolean
    Predicate<Person> predicate;
    ```
- [Understanding Java method invocation with invokedynamic](https://blogs.oracle.com/javamagazine/post/understanding-java-method-invocation-with-invokedynamic)
- [LambdaMetaFactory](https://docs.oracle.com/javase/8/docs/api/java/lang/invoke/LambdaMetafactory.html)

.

**`객체 직렬화`** / Item 03

**객체를 바이트스트림으로** 상호 변환하는 기술

```java
public class Book implements Serializable {
    private static final long serialVersionUID = 1L; // serialVersionUID 선언
    private String isbn;
    private String title;
    private LocalDate published;
    private String name;
    private transient int numberOfSold; // transient: 직렬화 제외

    // constructor..

    @Override
    public String toString() {
        //...
    }
}

...

private void serialize(Book book) {
    try (ObjectOutput out = new ObjectOutputStream(new FileOutputStream("book.obj"))) {
        out.writeObject(book);
    } catch (IOException e) {
        throw new RuntimeException(e);
    }
}

private Book deserialize() {
    try (ObjectInput in = new ObjectInputStream(new FileInputStream("book.obj"))) {
        return (Book) in.readObject();
    } catch (IOException | ClassNotFoundException e) {
        throw new RuntimeException(e);
    }
}

public static void main(String[] args) {
    Book book = new Book("12345", "이팩티브 자바 완벽 공략", "백기선",
            LocalDate.of(2022, 3, 21));
    book.setNumberOfSold(200);

    SerializationExample example = new SerializationExample();

    example.serialize(book);
    System.out.println(book);

    Book deserializedBook = example.deserialize();  
    System.out.println(deserializedBook);
}
```

- Serializable 인터페이스 구현 필요
- 바이트스트림으로 변환한 객체를 파일로 저장하거나 네트워트를 통해 다른 시스템으로 전송 가능
- transient를 사용해서 직렬화 하지 않을 필드 선언
- **serialVersionUID**
  - 미선언 시 JVM 런타임 시점에 자동으로 임의 UID 생성
  - 직렬화 후 클래스가 변경되어도 역직렬화를 허용하려면 serialVersionUID 선언 필요
    - 미선언 시 클래스가 변경될 경우 serialVersionUID도 자동으로 변경
- [객체 직렬화 스팩](https://docs.oracle.com/javase/8/docs/platform/serialization/spec/serialTOC.html)
- [Difference between Externalizable and Serializable in Java](https://www.geeksforgeeks.org/difference-between-serializable-and-externalizable-in-java-serialization/)

.

**`생성자에 자원 팩터리를 넘겨주는 방식`** / Item 05

자원을 만들어주는 팩토리를 통해서 자원을 가져오는 방식
- 만들어지는 과정이 복잡한 인스턴스일 경우 팩토리를 통해 생성
- Supplier Interface 가 팩토리를 표현한 완벽한 예

```java
public class SpellChecker {
    private final Dictionary dictionary;

    // 생성자에 자원 팩터리를 전달
    // 한정적 와일드카드 타입을 사용해 팩터리의 타입 매개변수를 제한
    public SpellChecker(Supplier<? extends Dictionary> dictionarySupplier) {
        this.dictionary = dictionarySupplier.get();
    }

    //..
}


...

public class DictionaryFactory {
    public static DefaultDictionary get() {
        // Dictionary 구현체
        return new DefaultDictionary();
    }
}

...

SpellChecker spellChecker = new SpellChecker(DefaultDictionary::get);
```
.

**`팩터리 메소드 패턴`** / Item 05


![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/effective-java/factory-method-pattern.png?raw=true 'Result')

```java
public class SpellChecker {
    private Dictionary dictionary; // Dictionary Interface

    public SpellChecker(DictionaryFactory dictionaryFactory) {
        // 새로운 Product를 제공하는 팩토리(TempDictionaryFactory)를 추가해도
        // 팩토리를 사용하는 클라이언트 코드는 변경할 필요가 없음
        this.dictionary = dictionaryFactory.getDictionary();
    }
    //..
}

...

public interface DictionaryFactory {
    Dictionary getDictionary();
}

...

public class DefaultDictionaryFactory implements DictionaryFactory {
    // 구체적으로 어떤 인스턴스를 만들지는 서브 클래스가 결정
    @Override
    public Dictionary getDictionary() {
        return new DefaultDictionary();
    }
}

```

- 개방-폐쇄 원칙(Open-Closed Principle, **OCP**)
  - 확장에 대해 열려 있고, 변경에 대해 닫혀있는 구조
- Spring IOC 핵심인 **Bean Factory**가 대표전인 팩터리 메소드 패턴


.

**`Spring Ioc`** / Item 05

**BeanFactory** 또는 **ApplicationContext**

- Ioc(Inversion of Control): 뒤짚힌 제어권
  - 코드에 대한 제어권(인스턴스 생성, 메소드 실행, 의존성을 주입 등)을 자기 자신이 가지고 있지 않고 외부에서 제어하는 경우
- Spring IoC Container 사용 장점
  - 많은 개발자에게 검증되었으며 자바 표준 스팩(@Inject)도 지원
  - 손쉽게 싱글톤 Scope 사용
  - 객체 생성(Bean) 관련 라이프사이클 인터페이스 제공
- [Spring Ioc](https://github.com/jihunparkme/Effective-JAVA/tree/main/effective-java/src/main/java/me/whiteship/chapter01/item05/springioc)

.

**`Deprecation` (사용 자제 API)** / Item 06

클라이언트가 사용하지 않길 바라는 코드가 있다면 적용

```java
/**
 * @deprecated in favor of
 * {@link #Deprecation(String)}
 */
@Deprecated(forRemoval = true, since = "1.2")
public Deprecation() {
}

private String name;

public Deprecation(String name) {
    this.name = name;
}
```

- 사용 자제를 권장하고 대안을 제시하는 방법
- **@Deprecated**
  - 컴파일시 경고 메시지를 통해 사용 자제를 권장하는 API라는 것을 클라이언트에 공유
- **@deprecated**
  - 문서화(Javadoc)를 통해 해당 API 사용 지양 원인과 대체 API 표기 가능

.

**`정규 표현식`** / Item 06

내부적으로 Pattern이 사용되는 곳

- String.matches(String regex)
- String.split(String regex)
  - Pattern.compile(regex).split(str)
- String.replace*(String regex, String replacement)
  - Pattern.compile(regex).matcher(str).replaceAll(repl)
- [java.util.regex](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)
- [Regular Expressions](https://docs.oracle.com/javase/tutorial/essential/regex/)
- [regex101](https://regex101.com/), [regexr](https://regexr.com/)

.

**`가비지 컬렉션`** / Item 06

- 기본 개념
  - Mark: 필요한 자원인지 아닌지 마킹
  - Sweep: 필요없는 오브젝트를 힙에서 제거
  - Compact: 흩어져있는 메모리 공간을 모아서 큰 공간을 확보
- 인스턴스 영역
  - Young Generation(Eden, S0, S1): 금방 제거되는 객체 
  - Old Generation: 오래 살아 남는 객체
- Minor GC, Full GC
- Full GC 알고리즘: Serial, Parallel, CMS, G1, ZGC, Shenandoah
- GC 알고리즘 관점: Throughput, Latency(Stop-The-World), Footprint
- 기본 개념, 옵션, 모니터링툴 학습 필요
- [How to choose the best Java garbage collector](https://developers.redhat.com/articles/2021/11/02/how-choose-best-java-garbage-collector#)

.

**`NullPointerException`** / Item 07

Optional(Java 8)을 활용해서 NPE를 최대한 피하자

- 메소드에서 적절한 값을 리턴할 수 없는 경우에 선택할 수 있는 대안
  - 예외 던지기
    ```java
    throw new IllegalArgumentException();
    ```
  - null 리턴
    ```java
    return null;
    ```
  - Optional 리턴
    ```java
    public Optional<MemberShip> defaultMemberShip() {
        if (this.numOfSubscribers < 2000) {
            return Optional.empty();
        } else {
            return Optional.of(new MemberShip());
        }
    }

    ...

    Channel channel = new Channel();
    Optional<MemberShip> optional = channel.defaultMemberShip();
    optional.ifPresent(MemberShip::hello);
    ```

.

**`WeakHashMap`** / Item 07

더이상 사용하지 않는 객체를 GC 동작 시 자동으로 삭제해주는 Map

- Key 가 더이상 강한 참조(Strong Reference)되는 곳이 없다면 해당 엔트리를 제거
  - 단, Key 값을 Wrapper type(Integer, String)으로 사용할 경우 JVM 내부에 캐시가 되어 GC 대상으로 선정되지 않으므로 Reference Type(Object) 사용 권장 
- Map의 엔트리를 Value 가 아니라 Key 에 의존해야 하는 경우 사용
- 캐시 구현에 사용할 수 있지만, 직접 구현하는 것은 권장하지 않음
- 레퍼런스 종류
  - Strong Reference
    ```java
    // 일반적인 참조
    ChatRoom localRoom = new ChatRoom();
    ```
  - [Soft Reference](https://docs.oracle.com/javase/8/docs/api/java/lang/ref/SoftReference.html)
    - Strong Reference 가 없어지고 Soft Reference 만 남았다면, GC 대상이 되고 GC 공간에 메모리가 필요한 상황에 GC 동작
    ```java
    Object strong = new Object(); // Strong Reference
    SoftReference<Object> soft = new SoftReference<>(strong); // Soft Reference
    strong = null; // remove Strong Reference
    ```
  - [Weak Reference](https://docs.oracle.com/javase/8/docs/api/java/lang/ref/WeakReference.html)
    - GC 동작 시 무조건 제거
    ```java
    Object strong = new Object(); // Strong Reference
    WeakReference<Object> weak = new WeakReference<>(strong); // Weak Reference
    strong = null; // remove Strong Reference
    ```
  - [Phantom Reference](https://docs.oracle.com/javase/8/docs/api/java/lang/ref/PhantomReference.html)
    - Phantom Reference 만 남은 경우 GC 동작 시 원본은 정리되고 Reference Queue에 삽입
    
    ```java
    BigObject strong = new BigObject(); // Strong Reference
    ReferenceQueue<BigObject> rq = new ReferenceQueue<>(); // Phantom Reference 사용을 위한 Queue
    BigObjectReference<BigObject> phantom = new BigObjectReference<>(strong, rq);
    strong = null; // remove Strong Reference

    System.gc();
    Thread.sleep(3000L);
    System.out.println(phantom.enqueue()); // GC 동작으로 자원이 반납되고, Reference Queue 에 삽입

    Reference<? extends BigObject> reference = rq.poll();
    reference.clear(); // Phantom Reference 참조 해제
    ```
- Soft, Weak Reference 를 사용해서 자원을 반납하는 방법은 언제 해당 객체가 없어질지 불확실한 단점이 존재하여 권장하지 않음
  - Phantom Reference 또한 자원 반납 용도로 사용하기에 너무 복잡한 방법

.

**`ScheduledThreadPoolExecutor`** / Item07

```java
public static void main(String[] args) throws ExecutionException, InterruptedException {
    ExecutorService service = Executors.newFixedThreadPool(10);
    for (int i = 0; i < 100; i++) {
        service.submit(new Task());
    }

    System.out.println(Thread.currentThread() + " main");
    service.shutdown();
}

static class Task implements Runnable {
    @Override
    public void run() {
        try {
            Thread.sleep(2000L);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println(Thread.currentThread() + " run");
    }
}
```

- Thread, Runnable, ExecutorService
- ThreadPool 개수 선정 시 주의점
  - CPU: 최대 CPU 개수만큼만 할당 가능(*Runtime.getRuntime().availableProcessors()*)
  - I/O: 딜레이 발생 시 응답을 기다리는 동안 CPU 리소스가 놀게 되므로, 기본적으로 많은 스레드 필요
- ThreadPool 종류
  - **SingleThreadPool**: 쓰레드 하나로 모든 작업을 수행(여러 작업 수행 시 많은 시간 소요)
  - **FixedThreadPool**: 내부적으로 Blocking Queue 사용(동시성 안전 보장). 스레드 개수 설정 가능.
  - **CachedThreadPool**: 작업을 위한 큐가 하나 존재. 필요한 만큼 스레드 생성.
    - 사용 가능한 스레드 존재 시 재사용, 부족 시 추가 생성, 미사용 스레드는 60초 지나면 제거
  - **ScheduledThreadPool**: 스케줄을 감안해서 스레드 실행 순서 변경 가능
    - 작업을 몇초 뒤 혹은 주기적으로 실행하도록 설정 가능
- FunctionalInterface
  - Runnable
  - Callable
  - Future
    ```java
    static class Task implements Callable<String> {
        @Override
        public String call() throws Exception {
            Thread.sleep(2000L);
            return Thread.currentThread() + " call";
        }
    }

    ...

    ExecutorService service = Executors.newFixedThreadPool(10);

    Future<String> submit = service.submit(new Task());
    System.out.println(Thread.currentThread() + " main");
    // Blocking call() 호출
    System.out.println(submit.get());

    service.shutdown();

    ```
- CompletableFuture, ForkJoinPool

.

**`Finalizer 공격`** / Item 08

```java
public class Account {
    private String accountId;

    public Account(String accountId) {
        this.accountId = accountId;

        if (accountId.equals("푸틴")) {
            throw new IllegalArgumentException("푸틴은 계정을 막습니다.");
        }
    }

    public void transfer(BigDecimal amount, String to) {
        System.out.printf("transfer %f from %s to %s\n", amount, accountId, to);
    }
}

...

public class BrokenAccount extends Account {

    public BrokenAccount(String accountId) {
        super(accountId);
    }

    /**
     * finalize() 재정의
     * - GC 동작 시 finalize() 메서드가 실행되어 finalizer 공격
     */
    @Override
    protected void finalize() throws Throwable {
        this.transfer(BigDecimal.valueOf(100), "keesun");
    }
}

...

Account account = null;
try {
    account = new BrokenAccount("푸틴");
} catch (Exception exception) {} 

System.gc();
```

- Finalizer 공격을 방어하는 방법
  - 상속이 불가하도록 final 클래스로 만들기
    ```java
    public final class Account { )
    ```
  - 부모 클래스에서 finalize() 메소드를 오버라이딩하고 final 선언을 통해 하위 클래스에서 오버라이딩 불가하도록 설정
    ```java
    ...
    @Override
    protected final void finalize() throws Throwable {
    }
    ```

.

**`AutoClosable`** / Item 08

try-with-resource 를 지원하는 인터페이스
```java
void close() throws Exception
```
- 인터페이스에 정의된 close() 메서드는 Exception 타입으로 예외를 던지지만
- 실제 구현체에서는 구체적인 예외를 던지는 것을 추천하며, 가능하다면 예외를 던지지 않는 것도 권장

Closeable 클래스와 차이점
```java
public void close() throws IOException;
```
- IOException을 던지며, 반드시 idempotent(멱등성)가 지켜져야 함
  - 멱등법칙: 연산을 여러 번 적용하더라도 결과가 달라지지 않는 성질

.

**`정적이 아닌 중첩 클래스는 자동으로 바깥 객체의 참조를 갖는다.`** / Item 08

- 중첩 클래스는 static 으로 생성하자.
- 그렇지 않을 경우, 중첩 클래스는 바깥 객체를 참조하므로 바깥 객체가 GC를 통한 자원 반납이 제대로 이루어지지 않음.

```java
public class OuterClass {

    private void hi() {  }

    /*
     * 정적이 아닌 중첩 클래스(static 선언 필요)
     */ 
    class InnerClass {
        public void hello() {
            // InnerClass 에서 OuterClass 메서드 호출
            OuterClass.this.hi();
        }
    }

    public static void main(String[] args) {
        OuterClass outerClass = new OuterClass();
        // OuterClass 의 인스턴스로 InnerClass 생성
        InnerClass innerClass = outerClass.new InnerClass(); 
        outerClass.printFiled();
    }

    private void printFiled() {
        Field[] declaredFields = InnerClass.class.getDeclaredFields();
        // InnerClass 는 자동으로 OuterClass 의 참조를 가지고 있음
        for(Field field : declaredFields) {
            // class me.whiteship.chapter01.item08.outerclass.OuterClass
            System.out.println("field type:" + field.getType()); 
            // this$0
            System.out.println("field name:" + field.getName()); 
        }
    }
}
```

.

**`람다 역시 바깥 객체의 참조를 갖기 쉽다.`** / Item 08
- 클래스 내부의 람다가 바깥 객체의 필드를 참조할 경우 순환참조가 발생
- 바깥 객체가 GC를 통한 자원 반납이 제대로 이루어지지 않음.

```java
public class LambdaExample {
    // 해당 필드가 static 이라면 람다가 참조하지 않음
    private int value = 10;

    private Runnable instanceLambda = () -> {
        // 바깥 객체의 필드를 참조
        System.out.println(value);
    };

    public static void main(String[] args) {
        LambdaExample example = new LambdaExample();
        Field[] declaredFields = example.instanceLambda.getClass().getDeclaredFields();
        for (Field field : declaredFields) {
            // class me.whiteship.chapter01.item08.outerclass.LambdaExample
            System.out.println("field type: " + field.getType()); 
            // arg$1
            System.out.println("field name: " + field.getName()); 
        }
    }
}
```

.

**`try-with-resources 바이트코드`** / Item 09
- try-with-resources 가 코드를 만들어 주는 방법
- 중첩 try-catch 로 예외 처리

```java
try (BufferedReader br = new BufferedReader(new FileReader(path))) {
    return br.readLine();
} catch (IOException e) {
    return defaultVal;
}

...

/**
 * try-with-resources 바이트코(target..)
 */
try {
    BufferedReader br = new BufferedReader(new FileReader(path));

    String var3;
    try {
        var3 = br.readLine();
    } catch (Throwable var6) {
        try {
            br.close();
        } catch (Throwable var5) {
            // 예외를 던지기 전에 suppressed 에 추가
            var6.addSuppressed(var5);
        }

        throw var6;
    }

    br.close();
    return var3;
} catch (IOException var7) {
    return defaultVal;
}
```

.

**`Value Object`** / Item 10

값을 갖는 클래스

```java
@ToString
@EqualsAndHashCode
public class Point {
    private final int x;
    private final int y;
    // ...
}
```

- 식별자가 없고 불변(Point, Address, Country, Street, State, Name, Money ..)
- 식별자(id, reference)가 아니라 인스턴스가 가지고 있는 상태 기반으로 equals, hashCode, toString 구현
- == 오퍼레이션이 아니라 equals를 사용해서 동등성 비교
- 동일한(equals) 객체는 상호교환 가능
- [Value-based Classes](https://docs.oracle.com/javase/8/docs/api/java/lang/doc-files/ValueBased.html)
- [State of the Values](https://cr.openjdk.org/~jrose/values/values-0.html)

.

**`StackOverflowError`** / Item 10

- Stack: 스레드들이 사용하는 메모리 공간
  - 메소드 호출 시 스택에 스택 프레임이 쌓임 → 더이상 스택 프레임을 쌓을 수 없다면 StackOverflowError 발생
  - 스택 프레임에는 메소드에 전달하는 매개변수, 메소드 실행 후 돌아갈 곳, 힙에 들어있는 객채에 대한 레퍼런스 등의 정보들이 존재
- Heap: 객체(인스턴스)들이 있는 공간
- 스택의 사이즈를 조정하고 싶다면? **-Xss1M**
  - [-X Command-line Options](https://docs.oracle.com/cd/E13150_01/jrockit_jvm/jrockit/jrdocs/refman/optionX.html)

.

**`리스코프 치환 원칙`** / Item 10

객체 지향 5대 원칙 SO(**L**)ID 중에 하나
- 1994년, 바바라 리스코프의 논문 "[A Behavioral Notion of Subtyping](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf)" 에서 기원한 객체 지향 원칙.
- ‘하위 클래스의 객체’가 ‘상위 클래스 객체’를 대체하더라도 소프트웨어의 기능을 깨트리지 않아야 한다.
  - semantic over syntacic, 구문 보다는 의미

.

**`Thread-safety`** / Item 11

멀티 스레드 환경에서 안전한 코드

- 가장 안전한 방법은 여러 스레드 간에 공유하는 데이터가 없는 것
- 공유하는 데이터가 있다면
  - Synchronization
  - ThreadLocal
  - 불변 객체 사용
  - Synchronized 데이터(ex. Hashtable)
  - Concurrent 데이터
  - ...

.

**`UnChecked Exception`** / Item 13

비검사 예외(UnChecked Exception)는 컴파일 에러를 신경쓰지 않아도 되고, try-catch로 감싸거나 메서드 선언부에 선언하지 않아도 되므로 선호하는 예외 방식

.

잡지 않은 (체크)예외를 메서드에 선언하는 이유.
- 메서드에 선언한 예외는 프로그래밍 인터페이스의 일부(클라이언트가 반드시 알아야 하는 정보)
- 예외 정보를 알아야만 해당 예외가 발생했을 때 대처하는 코드 작성이 가능

비검사 예외는 메서드에 선언하지 않아도 되는 이유.
- 비검사 예외는 어떤 방법으로도 처리나 복구가 불가능 할 경우에 사용하는 예외
  - 숫자를 0으로 나누기, null 레퍼런스에 메서드 호는 등..
- 이러한 예외는 프로그램 전반에 걸쳐 어디서든 발생할 수 있기 때문에 이 모든 비검사 예외를 메서드에 선언하도록 강제한다면 프로그램의 명확도가 감소

.

예외의 사용
- 단순히 처리하기 쉽고 편하다는 이유만으로 RuntimeException을 선택하지 말자
- 클라이언트가 해당 예외 상황을 `복구할 수 있다`면, `검사 예외`를 사용
- 해당 예외가 발생했을 때 `아무것도 할 수 없다`면, `비검사 예외`를 사용

[Unchecked Exceptions](https://docs.oracle.com/javase/tutorial/essential/exceptions/runtime.html)

.

**`TreeSet`** / Item 13

AbstractSet을 확장한 `정렬된 컬렉션`

- 오름차순으로 정렬(엘리먼트를 추가한 순서는 중요하지 않음)
- 엘리먼트가 지닌 자연적인 순서(natural order, Comparable interface)에 따라 정렬 
- NTS(Non-Thread safety)
  - Thread safety 하려면 synchronizedSet 활용
  
  ```java
  TreeSet<PhoneNumber> numbers = new TreeSet<>(Comparator.comparingInt(PhoneNumber::hashCode));

  Set<PhoneNumber> phoneNumbers = Collections.synchronizedSet(numbers);
  phoneNumbers.add(new PhoneNumber(123, 456, 780));
  phoneNumbers.add(new PhoneNumber(123, 456, 7890));
  phoneNumbers.add(new PhoneNumber(123, 456, 789));
  ```
- HashSet은 이진 검색 트리(O(logn))/레드 블랙 트리 사용

.

**`정수 오버플로`**
- 기본 타입의 compare 메서드 사용 권장

```java
System.out.println(-2147483648 - 10); // 2147483638

System.out.println(Integer.compare(-2147483648, 10)); // -1
```

.

**`IEEE 754 부동소수점 계산 방식에 따른 오류`**
- BigDecimal 사용 권장

```java
int i = 1;
double d = 0.1;
System.out.println(i - d * 9); // 0.09999999999999998

BigDecimal bd = BigDecimal.valueOf(0.1);
System.out.println(BigDecimal.valueOf(1).min(bd.multiply(BigDecimal.valueOf(9)))); // 0.9
```

# Reference

- [effective-java-3e-source-code (KOR)](https://github.com/WegraLee/effective-java-3e-source-code)

- [effective-java-3e-source-code (EN)](https://github.com/jbloch/effective-java-3e-source-code)