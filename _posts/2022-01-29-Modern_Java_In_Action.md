---
layout: post
title: Modern Java In Action
summary: Modern Java In Action
categories: (Book)Modern-Java-In-Action
featured-img: modern-java
# mathjax: true
---

# Modern Java In Action

## 소개

자바 8 설계의 밑바탕을 이루는 세 가지 프로그래밍 개념

- \1. `스트림 처리`
  - 한 번에 한 개씩 만들어지는 연속적인 데이터 항목들의 모임을 처리
  - 물리적인 순서가 있지만 각 단계에서 동시에 작업을 처리하는 자동차 조립 라인을 생각해보자.
- \2. `동작 파라미터화로 메서드에 코드 전달`
  - 코드 일부를 API 로 전달하는 기능
  - 메서드를 다른 메서드의 인수로 넘겨주는 기능
- \3. `병렬성과 공유 가변 데이터`
  - 기존의 자바 스레드 API보다 쉽게 병렬성을 활용

# 기초

## 동적 파라미터화 코드 전달하기

`자주 바뀌는 요구사항에 효과적으로 대응하자.`

- 동적 파라미터 : 아직은 어떻게 실행할지 결정하지 않은 코드 블록
- 동작(코드)을 메서드 인수로 전달

**Before**

```java
public static List<Apple> filterGreenApples(List<Apple> inventory) {
    List<Apple> result = new ArrayList<>();
    for (Apple apple : inventory) {
        if ("green".equals(apple.getColor())) {
            result.add(apple);
        }
    }
    return result;
}
```

**After**

선택 조건을 결정하는 인터페이스를 정의하자. (전략 디자인 패턴)

- 각 항목에 적용할 동작을 분리

```java
public interface Predicate<T> {
    boolean test(T t);
}

public class weightPredicate implements Predicate {
    @Override
    public boolean test(T t) {
        return t.getWeight() > 150;
    }
}

public class colorPredicate implements Predicate {
    @Override
    public boolean test(T t) {
        return t.getColor() == Color.GREEN;
    }
}

public <T> List<T> filter(List<T> list, Predicate<T> p) {
    List<T> result = new ArrayList<>();
    for (T e : list) {
        if (p.test(e)) {
            result.add(e);
        }
    }
    return result;
}

//
List<Apple> greenApples = filter(inventory, new colorPredicate());
```

## 람다 표현식

`메서드로 전달할 수 있는 익명 함수를 단순화한 것.`

`익명 함수의 일종이다 -> 이름은 없지만, 파라미터 리스트, 바디, 반환 형식을 가지고 예외를 던질 수 있다.`

- 람다 표현식의 구성

  - 파라미터 리스트
  - 화살표
  - 람다 바디

  ```java
  (Apple a1, Apple a2) -> a1.getWeight().compareTo(a2.getWeight());
  '----람다 파라미터---화살표-------------람다 바디------------------'
      
  List<Apple> greenApples = filter(inventory, (Apple a) -> Color.GREEN.equals(a.getColor()));
  ```

### 함수형 인터페이스

- 함수형 인터페이스 : 오직 하나의 추상 메서드만을 정의하는 인터페이스
  - 함수형 인터페이스를 기대하는 곳에서만 람다 표현식 사용 가능
- 제네릭 파라미터에는 참조형(Byte, Integer, Object, List..)만 사용 가능

**Predicate**

- 추상 메서드를 정의하여 제네릭 형식 T의 객체를 인수로 받아 `Boolean 반환`

  ```java
  @FunctionalInterface
  public interface Predicate<T> {
      boolean test(T t);
  }
  
  public <T> List<T> filter(List<T> list, Predicate<T> p) {
      List<T> result = new ArrayList<>();
      for (T t : list) {
          if (p.test(t)) {
              result.add(t);
          }
      }
      return result;
  }
  
  Predicate<String> nonEmptyStringPredicate = (String s) -> !s.isEmpty();
  List<String> nonEmpty = filter(listOfString, nonEmptyStringPredicate)
  ```

**Consumer**

- 추상 메서드를 정의하여 제네릭 형식 T의 객체를 인수로 받아 `void 반환` (특정 동작 수행)

  ```java
  @FunctionalInterface
  public interface Consumer<T> {
      void accept(T t);
  }
  
  public <T> void forEach(List<T> list, Consumer<T> c) {
      for(T t : list) {
          c.accept(t);
      }
  }
  forEach(
      Arrays.asList(1,2,3,4,5),
      (Integer i) -> System.out.println(i);
  )
  ```

**Function**

- 추상 메서드를 정의하여 제네릭 형식 T의 객체를 인수로 받아 `제네릭 형식 R 객체를 반환` (입력을 출력으로 매핑할 경우)

  ```java
  @FunctionalInterface
  public interface Function<T, R> {
      R apply(T t);
  }
  
  public <T, R> List<R> map(List<T> list, Function<T, R> f) {
      List<R> result = new ArrayList<>();
      for(T t : list) {
          result.add(f.apply(t));
      }
      return result;
  }
  
  // [7, 2, 6]
  List<Integer> l = map(
      Arrays.asList("lambdas", "in", "action"),
      (String s) -> s.length()
  );
  ```

### 람다, 메서드 참조 활용

**1단계: 코드 전달**

- 객체 안에 동작을 포함시키는 방식으로 다양한 전략 전달
  - sort 동작은 파라미터화 되었다!

```java
static class AppleComparator implements Comparator<Apple> {
    @Override
    public int compare(Apple a1, Apple a2) {
        return a1.getWeight() - a2.getWeight();
    }
}
inventory.sort(new AppleComparator());
```

**2단계: 익명 클래스 사용**

- 일회성이 있는 경우 익명 클래스를 이용하는 것이 좋다.

```java
inventory.sort(new Comparator<Apple>() {
    @Override
    public int compare(Apple a1, Apple a2) {
        return a1.getWeight() - a2.getWeight();
    }
});
```

**3단계: 람다 표현식 사용**

- 함수형 인터페이스를 기대하는 곳 어디서나 람다 표현식을 사용할 수 있다.

```java
// 1. Comparator 함수 디스크림터는 (T, T) -> int
inventory.sort((Apple a1, Apple a2) ->  a1.getWeight() - a2.getWeight());

//2. 자바 컴파일러는 람다 표현식이 사용된 콘텍스트를 활용해서 람다의 파라미터 형식을 추론
inventory.sort((a1, a2) -> a1.getWeight() - a2.getWeight());

//3. comparing 메서드 사용
import static java.util.Comparator.comparing;
inventory.sort(comparing(apple -> apple.getWeight()));
```

**4단계: 메서드 참조 사용**

- 메서드 참조를 이용하면 람다 표현식의 인수를 더 깔끔하게 전달할 수 있다.

```java
inventory.sort(comparing(Apple::getWeight));
```

### 람다 표현식 조합 유용 메서드

**Comparator**

- 정적 메서드 Comparator.comparing를 이용해서 비교에 사용할 키 추출

````java
// 역정렬
inventory.sort(comparing(Apple::getWeight).reversed());

// Comparator 연결(thenComparing 메서드로 두 번째 비교자 만들기)
inventory.sort(comparing(Apple::getWeight)
               .reversed()
               .thenComparing(Apple::getContry));
````

**Predicate**

- 복잡한 Predicate를만들 수 있도록 negate, and, or 세 가지 메서드 제공

```java
// 기존 Predicate 객체 결과를 반전시킨 객체 생성 (negate)
Predicate<Apple> notRedApple = redApple.negate();

// 두 Predicate 를 연결해 새로운 Predicate 객체 생성
//(and)
Predicate<Apple> redAndHeavyApple = redApple.and(apple -> apple.getWeight() > 150);
//(or)
Predicate<Apple> redAndHeavyOrGreen = redApple.and(apple -> apple.getWeight() > 150)
    										.or(apple -> GREEN.equals(a.getColor()));
```

**Function**

- Function 인스턴스를 반환하는 andThen, compose 두 가지 default 메서드 제공

```java
//andThen (주어진 함수 결과를 다른 함수의 입력으로 전달하는 함수 반환)
Function<Integer, Integer> f = x -> x + 1;
Function<Integer, Integer> g = x -> x * 2;
Function<Integer, Integer> h = f.andThen(g);
int result = h.apply(1); // g(f(x)) -> 4

//compose (인수로 주어진 함수를 먼저 실행한 후 그 결과를 외부 함수의 인수로 제공)
Function<Integer, Integer> h = f.compose(g);
int result = h.apply(1); // f(g(x)) -> 3
```

# 함수형 데이터 처리

## 스트림

## 49R
