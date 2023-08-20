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

**`Flyweight Pattern`**

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

**`Java8 Interface`**

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

**`Service Provider Framework`**

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

**`Reflection`**

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

**`JavaBean`**

(주로 GUI에서) 재사용 가능한 소프트웨어 컴포넌트

자바빈이 지켜야 할 규약
- 아규먼트 없는 기본 생성자 → 객체를 쉽게 생성
- Serializable 인터페이스 구현 → 직렬화된 객체 재사용
- getter, setter 메소드 이름 규약 → 필드에 접근하는 일관적인 방법
  - 스프링, JPA 같은 여러 프레임워크에서 리플렉션을 통한 특정 객체의 값을 조회하거나 설정하기 위해 주로 사용

.

**`Object freezing`**

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

**`Builder Pattern`**

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

**`IllegalArgumentException`**

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

**`가변인수`**

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

**`메서드 참조`**

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

**`함수형 인터페이스`**

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

**`객체 직렬화`**

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

**`생성자에 자원 팩터리를 넘겨주는 방식`**

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

**`팩터리 메소드 패턴`**


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

**`Spring Ioc`**

**BeanFactory** 또는 **ApplicationContext**

- Ioc(Inversion of Control): 뒤짚힌 제어권
  - 코드에 대한 제어권(인스턴스 생성, 메소드 실행, 의존성을 주입 등)을 자기 자신이 가지고 있지 않고 외부에서 제어하는 경우
- Spring IoC Container 사용 장점
  - 많은 개발자에게 검증되었으며 자바 표준 스팩(@Inject)도 지원
  - 손쉽게 싱글톤 Scope 사용
  - 객체 생성(Bean) 관련 라이프사이클 인터페이스 제공
- [Spring Ioc](https://github.com/jihunparkme/Effective-JAVA/tree/main/effective-java/src/main/java/me/whiteship/chapter01/item05/springioc)