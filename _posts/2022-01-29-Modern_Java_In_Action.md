---
layout: post
title: Modern Java In Action
summary: Modern Java In Action
categories: (Book)Modern-Java-In-Action
featured-img: modern-java
# mathjax: true
---

# Modern Java In Action

**소개**

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

## Stream

Stream : `데이터 처리 연산을 지원하도록 소스에서 추출된 연속된 요소`

- 선언형으로 컬렉션 데이터를 처리
- 멀티스레드 코드를 구현하지 않아도 데이터를 투명하게 병렬로 처리
- 복잡한 루프, 조건문 등이 필요 없이 선언형 코드와 동작 파라미터화를 활용하면 변하는 요구사항에 쉽에 대응할 수 있다.
- 스트림 API 를 통해 데이터 처리를 병렬화로 진행하면서 스레드와 락을 걱정할 필요가 없다.

**특징**

- 선언형 : 간결성 + 가독성 향상
- 조립 : 유연성 향상
- 병렬화 : 성능 향상

**상태 있는 연산과 상태 없는 연산**

- 상태 있는 연산(stateful operation) : 값을 계산하는 데 필요한 상태를 저장하는 연산 (`reduce`, `sorted`, `distinct`)
- 상태 없는 연산(stateless operation) : 상태를 저장하지 않는 연산 (`filter`, `map`)

**Java7**

```java
List<Dish> lowCaloricDishes = new ArrayList<>();
for (Dish d : dishes) {
    if (d.getCalories() < 400) {
        lowCaloricDishes.add(d);
    }
}

Collections.sort(lowCaloricDishes, new Comparator<Dish>() {
    @Override
    public int compare(Dish d1, Dish d2) {
        return Integer.compare(d1.getCalories(), d2.getCalories());
    }
});
List<String> lowCaloricDishesName = new ArrayList<>();
for (Dish d : lowCaloricDishes) {
    lowCaloricDishesName.add(d.getName());
}
```

**Java8**

```java
//stream()
List<String> lowCaloricDishesName =
            menu.stream()
                .filter(d -> d.getCalories() < 400) //조건
                .sorted(comparing(Dish::getCalories)) //정렬
                .map(Dish::getName) //추출
                .collect(toList()); //리스트화

//parallelStream()
List<String> lowCaloricDishesName =
            menu.parallelStream()
                .filter(d -> d.getCalories() < 400)
                .sorted(comparing(Dish::getCalories))
                .map(Dish::getName)
                .collect(toList());
```

**Example**

```java
//stream()
List<String> threeHighCaloricDishNames =
                menu.stream()
                    .filter(dist -> dist.getCalories() < 300) //필터링 
                    .map(Dish::getName) //추출
                    .limit(3) //축소
                    .collect(toList()); //리스트화 
```

- `filter` : 스트림에서 특정 요소 제외
- `map` : 한 요소를 다른 요소로 변환하거나 정보 추출
- `limit` : 정해진 요소 개수 제한
- `sorted` : 요소 정렬
- `collect` : 스트림을 다른 형식으로 변환
- 중간 연산 : filter, map, limit, sorted, distinct ...
  - 중간 연산을 합친 다음 합쳐진 중간 연산을 최종 연산으로 한 번에 처리(LAZY)
- 최종 연산 : collect, forEach, count ..
  - 스트림 파이프라인에서 결과를 도출

**Stream VS Collection**

**데이터 계산 시점**

- `Collection` : 현재 자료구조가 포함하는 모든 값을 메모리에 저장하고 모든 요소는 컬렉션에 추가 전에 요소는 미리 계산되어야 함
  - 모든 정보가 로딩될 때까지 기다려야만 한다. ex) DVD
- `Stream` : 요청할 때만 요소를 계산 (LAZY)
  - 로딩된 일부 데이터를 먼저 볼 수 있다. ex) 스트리밍
  - 단 한 번만 소비할 수 있다. -> 다시 탐색 시 새로운 스트림 생성이 필요

**데이터 반복 처리 방법**

- `Collection` : 사용자가 직접 요소를 반복 (외부 반복)
- `Stream` : 반복을 알아서 처리하고 결과 스트림값을 어딘가에 저장 (내부 반복)
  - 내부 반복의 경우 투명하게 병렬 처리, 더 최적화된 다양한 순서로 처리가 가능

## Stream 활용

### Filtering

- `filter, distinct` : Predicate 를 인수로 받아 일치하는 모든 요소를 포함하는 스트림 반환

  ```java
  List<Dish> vegetarianMenu = menu.stream()
                                  .filter(Dish::isVegetarian)
                                  .distinct() //중복 필터링(hashCode, equals 로 결정)
                                  .collect(toList());
  ```

### Slicing

- `takeWhile, dropWhile` : Predicate 를 이용한 슬라이싱 (필터에 걸리면 반복 중단) 

  ```java
  List<Dish> sliceMenu1 = specialMenu.stream()
                                      .takeWhile(dish -> dish.getCalories() < 320)
                                      .collect(toList());
  ```

- 슬라이싱 후 나머지 요소 선택

  ```java
  List<Dish> sliceMenu2 = specialMenu.stream()
                                      .dropWhile(dish -> dish.getCalories() < 320)
                                      .collect(toList());
  ```

- `limit` : 스트림 축소

  ```java
  List<Dish> dishes = specialMenu.stream()
                                  .filter(dish -> dish.getCalories() > 300)
                                  .limit(3)
                                  .collect(toList());
  ```

- `skip` : 건너뛰기(처음 n개 요소 제외)

  ```java
  List<Dish> dishes = menu.stream()
                          .filter(dish -> dish.getCalories() > 300)
                          .skip(2)
                          .collect(toList());
  ```

### Mapping

- `map` : 특정 함수 적용 결과 매핑

  ```java
  List<String> dishNames = menu.stream()
                              .map(Dish::getName) //요리명 추출
                              .map(String::length) //요리명 글자 길이 추출
                              .collect(toList());
  ```

- `flatMap` : 생성된 스트림을 하나의 스트림으로 평명화

  ```java
  List<String> uniqueCharacters = 
      words.stream()
      	.map(word -> word.split("")) // 각 단어를 개별 문자를 포함하는 배열로 변환
          .flatMap(Arrays:stram)
          .distinct()
          .forEach(toList());
  ```

### Serching & Maching

- `allMatch` : 스트림에서 적어도 한 요소와 일치하는지 확인

  ```java
  boolean isVegetarian = menu.stream()
      						.anyMatch(Dish::isVegetarian)
  ```

- `anyMatch` : 스트림의 모든 요소가 일치하는지 검사

  ```java
  boolean isHealthy = menu.stream()
      					.allMatch(dish -> dish.getCalories() < 1000);
  ```

- `nonMatch` : 스트림의 요소 중 일치하는 요소가 없는지 확인

  ```java
  boolean isHealthy = menu.stream()
      					.noneMatch(dish -> dish.getCalories() >= 1000);
  ```

- `findFirst` : 스트림에서 첫 번째 요소 찾기

  ```java
  Optional<Integer> firstSquaredDivisibleByThree = someNumbers.stream()
      													.map(n -> n * n)
      													.filter(n -> n % 3 == 0)
      													.findFirst();
  ```

  

- `findAny` : 스트림에서 임의의 요소 반환

  ```java
  Optional<Dish> dish = menu.stream()
      					.filter(Dish:isVegetarian)
      					.findAny();
  ```

### Reducing

- `reduce` : 스트림의 모든 요소를 처리해서 값으로 도출 (초기값, BinaryOperator<T>)

- 누적자를 초깃값으로 설정한 다음 BinaryOperator 로 스트림의 각 요소를 반복적으로 누적자와 합쳐 스트림을 하나의 값으로 리듀싱

  ```java
  //덧셈
  int sum = numvers.stream()
      			.reduce(0, Integer::sum) //.reduce(0, (a, b) -> a + b);
  // 곱셈
  int product = numvers.stream()
      			.reduce(1, (a, b) -> a * b);
  // 최댓값
  Optional<Integer> max = numbers.stream()
      					.reduce(Integer::max);
  ```

## 숫자형 스트림

- `mapToInt`, `mapToDouble`, `mapToLong` 메서드는 map 과 같은 기능을 수행하지만 Stream 대신 특화된 스트림을 반환

  ```java
  int calories = menu.stream() //Stream<Dish> 반환
      				.mapToInt(Dish:getCalories) //IntStream 반환
      				.sum();
  ```

- `boxed` : 특화 스트림을 일반 스트림으로 변환하기

  ```java
  IntStream intStream = menu.stream().mapToInt(Dish::getCalories);
  Stream<Integer> stream = intStream.boxed();
  ```

- `OptionalInt`, `OptionalDouble`, `OptionalLong` 으로 이전 값의 존재 여부를 확인할 수 있다.

  ```java
  OptaionInt maxCalories = menu.stream()
      				.mapToInt(Dish:getCalories)
      				.max();
  
  int max = maxCalories.orElse(1);
  ```

- `range`(인수 미포함), `rangeClosed`(인수 포함) 로 숫자를 생성할 수 있다.

  ```java
  int count = IntStream.rangeClosed(1, 100) //1~100 범위
      				.filter(n -> n % 2 == 0) //짝수 스트림
      				.count(); //50
  ```

## 스트림 생성

**값으로 스트림 생성**

```java
Stream<String> stream = Stream.of("Modern", "Java", "in", "Action");
stream.map(String::toUpperCase).forEach(System.out::println);

Stream<String> emptyStream = Stream.empty();
```

**Null이 될 수 있는 객체로 스트림 생성**

```java
//null이 될 수 있는 객체를 포함하는 Stream
Stream<String> values = Stream.of("config", "home", "user")
    						.flatMap(key -> Stream.ofNullable(System.getProperty(key)));
```

**배열로 스트림 생성**

```java
int[] numbers = {2, 3, 5, 7, 11, 13, 15, 17};
int sum = Arrays.stream(numbers).sum();
```

**파일로 스트림 생성**

- `Files.lines` : 주어진 파일의 행 스트림을 문자열로 반환

```java
//고유 단어의 수 계산
long uniqueWords = 0;
try(Stream<String> lines = Files.lines(Paths.get("modernJavaInAction/data.txt"), Charset.defaultCharset())) { //AutoCloseable
    uniqueWords = lines.flatMap(line -> Arrays.stream(line.split(" "))) //고유 단어 수
                        .distinct()
                        .count();
} catch(IOException e) {
    
}   
```

**무한 스트림 생성**

- `Stream.iterate` : 생산된 각 값을 연속적으로 계산

  ```java
  //(iterate) 짝수 스트림 생성 : 생산된 각 값을 연속적으로 계산
  Stream.iterate(0, n -> n + 1)
      	.limit(10)
      	.forEach(System.out::println);
  
  //무한 스트림 생성을 중단하는 방법
  IntStream.iterate(0, n -> n<100, n -> n+4) 
      		.forEach(System.out::println);
  
  IntStream.iterate(0, n -> n+4) 
      		.takeWhile(n -> n<100)
      		.forEach(System.out::println);
  ```

- `Stream.generate` : 생산된 각 값을 연속적으로 계산하지 않음 (상태가 없는 메서드에 주로 사용)

  ```java
  Stream.generate(Math::random)
      	.limit(5)
      	.forEach(System.out::pringln);
  ```

# 스트림으로 데이터 수집

- Collectors Class 에서 제공하는 메서드
  - 리듀싱과 요약
  - 요소 그룹화
  - 요소 분할

## Reducing

```java
// Collectors.counting
long howManyDishes1 = menu.stream().collect(Collectors.counting());
long howManyDishes2 = menu.stream().count();

// Collectors.maxBy (minBy)
//:주어진 비교자를 이용해서 스트림의 최솟값 요소를 Optional로 감싼 값을 반환 (요소가 없을 경우 return Optional.empty())
Comparator<Dish> dishCaloriesComparator = Comparator.comparingInt(Dish::getCalories);
Optional<Dish> mostCaloriesDish = menu.stream().collect(maxBy(dishCaloriesComparator));

// Collectors.summingInt (summingLong, summingDouble)
//:스트림 항목에서 정수 프로퍼티값의 합
int totalCalories = menu.stream().collect(summingInt(Dish::getCalories));

// Collectors.averagingInt (averagingLong, averagingDouble)
//:스트림 항목에서 정수 프로퍼티값의 평균값
double avgCalories = menu.stream().collect(averagingInt(Dish::getCalories));

// Collectors.summarizingInt (summarizingLong, summarizingDouble)
//:스트림 내 항목의 최대, 최소, 합계, 평균 등의 정수 정보 통계 수집
IntSummaryStatistics menuStatistics = menu.stream().collect(summarizingInt(Dish::getCalories));
IntSummaryStatistics{count=10, sum=4500, min=80, average=512.1221, max=780}

// Collectors.joining
//:내부적으로 StringBuilder를 이용하여 문자열 생성
String shortMenu = menu.strea().map(Dish::getName).collect(joining(", "));
```

**범용 리듀싱 요약 연산**

- 문제를 해결할 수 있는 다양한 해결 방법 중 문제에 특화된 해결책을 골라, 가독성과 성능을 모두 잡아보자.

```java
// max (시작값이 없으므로 Optional 반환)
Optional<Dish> mostCalorieDish = menu.stream()
    				.collect(reducing((d1, d2) -> d1.getCalories() > d2.getCalories() ? d1 : d2));

// sum
int totalCalories = menu.stream().collect(reducing(0, Dish::getCalories, (i, j) -> i + j));

int totalCalories = menu.stream().collect(Dish::getCalories, Integer::sum);

int totalCalories = menu.stream().map(Dish::getCalories).reduce(Integer::sum).get
    
int totalCalories = menu.stream().mapToInt(Dish::getCalories).sum()
```

## Grouping

- 분류 함수
  - `Collectors.groupingBy(f, toList())`
  - 하나의 프로퍼티값(Key)을 기준으로 스트림의 항목을 그룹화

```java
// Type Groupging
//{FISH=[salmon], OTHER=[fries, rice], MEAT=[pork, beef, chichen]}
Map<Dish.Type, List<Dish>> dishesByType = menu.stream().collect(groupingBy(Dish::getType));

// Calories Groupging
public enum CaloricLevel { DIET, NORMAL, FAT }
Map<CaloricLevel, List<Dish>> dishesByCaloricLevel = menu.stream().collect(
    groupingBy(dish -> {
        if (dish.getCalories() <= 400) return CaloricLevel.DIET;
        else if (dish.getCalories() <= 700) return CaloricLevel.NORMAL;
        else return CaloricLevel.FAT;
    }));
```

**그룹화된 요소 조작**

```java
// Type & Calories Groupging (데이터가 없는 Type 도 포함)
//{FISH=[], OTHER=[fries, rice], MEAT=[pork, beef, chichen]}
Map<Dish.Type, List<Dish>> caloricDishedByType = menu.stream()
    .collect(groupingBy(Dish::getType, filtering(dish -> dish.getCalories() > 500, toList())));

// 그룹의 각 요리를 관리 이름 목록으로 변환
Map<Dish.Type, List<String>> dishNamesByType = menu.stream()
    .collect(groupingBy(Dish::getType, mapping(Dish.getName, toList())));

// 각 형식의 요리 태그 추출
//{FISH=[roasted, tasty], OTHER=[fried, fresh], MEAT=[salty, greasy]}
Map<Dish.Type, Set<String>> dishNamesByType = menu.stream()
    .collect(groupingBy(Dish::getType, flatMapping(dish -> dishTags.get(dish.getName()).stream(), toSet())));
```

**다수준 그룹화**

```java
public enum CaloricLevel { DIET, NORMAL, FAT }
Map<Dish.Type, Map<CaloricLevel, List<Dish>>> dishesByTypeCaloricLevel = menu.stream()
    .collect(
    	groupingBy(Dish::getType, // 첫 번째 수준의 분류 함수    
            groupingBy(dish -> { // 두 번째 수준의 분류 함수
                if (dish.getCalories() <= 400) return CaloricLevel.DIET;
                else if (dish.getCalories() <= 700) return CaloricLevel.NORMAL;
                else return CaloricLevel.FAT;
            })
     )
);
//{FISH={DIET=[prawns], NORMAL=[salmon]}, MEAT={DIET=[chicken], NORMAL=[beef], FAT=[pork]}, ...} 
```

**서브그룹으로 데이터 수집**

- 처음부터 값이 존재하지 않는 Key 는 Map 에 추가되지 않으므로 Optional wrapper 를 사용할 필요가 없음
  - groupingBy Collector 는 Stream 첫 번째 요소를 찾은 이후에 그룹화 맵에 새로운 키를 추가(lazy)
    - 리듀싱 컬렉터는 절대 Optional.empty()를 반환하지 않음
  - collectingAndThen 는 적용할 컬렉터와 변환 함수를 인수로 받아 다른 컬렉터를 반환

```java
//요리 수를 종류별로 연산
//{MEATH=3, FISH=5, OTHER=2}
Map<Dish.Type, Long> typesCount = menu.stream().collect(
											groupingBy(Dish::getType, counting()));

//요리 종류 중 가장 높은 칼로리를 갖는 요리
//{MEATH=Optional[pork], FISH=Optional[salmon], OTHER=Optional[buger]}
Map<Dish.Type, Optional<Dish>> mostCaloricByType = menu.stream().collect(
						groupingBy(Dish::getType, maxBy(comparingInt(Dish::getCalories))));

//{MEATH=pork, FISH=salmon, OTHER=buger}
Map<Dish.Type, Dish> mostCaloricByType = menu.stream().collect(
    groupingBy(Dish::getType, //분류 함수
               collectingAndThen(
                   maxBy(comparingInt(Dish::getCalories)), // 감싸인 컬렉터
                   Optional::get) // 변환 함수
              )
); 

//각 요리 형식에존재하는 모든 CaloricLevel 값
//{MEATH=[DIET, NORMAL], FISH=[NORMAL, FAT], OTHER=[DIET, NORMAL]}
Map<Dish.Type, Set<CaloricLevel>> caloricLevelsByType = menu.stream().collect(
    groupingBy(Dish::getType, mapping(dish -> {
        if (dish.getCalories() <= 400) return CaloricLevel.DIET;
        else if (dish.getCalories() <= 700) return CaloricLevel.NORMAL;
        else return CaloricLevel.FAT;
    },
	toCollection(HashSet::new)))
);
```

## Partitioning

- 분할 함수
  - return Boolean (true or false)
  - 분할 함수는 참, 거짓 두 가지 요소의 스트림 리스트를 모두 유지하는 장점이 있다.
  - 프레디케이트를 스트림의 각 항목에 적용한 결과로 항목 분할

```java
//{false=[pork, beef, salmon], true=[pizza, rice]}
Map<Boolean, List<Dish>> partitionedMenu = menu.stream().collect(
    										partitioningBy(Dish::isVegetarian));

//{false={MEATH=[DIET, NORMAL], FISH=[NORMAL, FAT]}, true={OTHER=[DIET, NORMAL]}}
Map<Boolean, Map<Dish.Type, List<Dish>>> vegetarianDishesByType = menu.stream().collect(
    										partitioningBy(Dish::isVegetarian, //- 분할 함수
                                                          groupingBy(Dish::getType))); //- 두 번째 컬렉터

//채식 요리와 채식이 아닌 요리 각 그룹에서 가장 칼로리가 높은 요리
//{false=pork, true=pizza}
Map<Boolean, Dish> mostCaloricPartitionedByVegetarian = menu.stream().collect(
								partitioningBy(Dish::isVegetarian,
                                              collectingAndThen(maxBy(comparingInt(Dish::getCalories)), 
                                                               Optional::get)));
```

**Example**

- 숫자를 소수와 비소수로 분할하기

```java
public boolean isPrime(int candidate) {
    int candidateRoot = (int) Math.sqrt((double) candidate);
    return IntStream.range(2, candidateRoot)
        .noneMatch(i -> candidate % i == 0);
}

public Map<Boolean, List<Integer>> partitionPrimes(int n) {
    return IntStream.rangeClosed(2, n).boxed()
        .collect(partitioningBy(candidate -> isPrime(candidate)));
}
```

## Collector

- Collector Interface

```java
/* T : 수집될 스트림 항목의 제네릭 형식
 * A : 수집 과정에서 중간 결과를 누적하는 객체의 형식(누적자)
 * R : 수집 연산 결과 객체의 형식
 * supplier() -> accumulator() -> combiner() -> finisher()
 */
public interface Collector<T, A, R> {
    //supplier() : 새로운 결과 컨테이너 만들기(수집 과정에서 빈 누적자 인스턴스를 만드는 파라미터가 없는 함수)
    Supplier<A> supplier();
    //accumulator() : 결과 컨테이너에 스트림 요소 추가하기(리듀싱 연산을 수행하는 함수 반환)
    BiConsumer<A, T> accumulator();
    //combiner() : 두 결과 컨테이너 병합(스트림의 서로 다른 서브파트를 병렬로 처리할 때 누적자가 결과를 어떻게 처리할지 정의)
    BinaryOperator<A> combiner();
    //finisher() : 최종 변환값을 결과 컨터네이너 적용하기
    Function<A, R> finisher();
    // characteristics() : 컬렉터의 연산을 정의하는 Characteristics 형식의 불변 집합 반환(어떤 최적화를 이용해 리듀싱 연산을 수행할 것인지 힌트 제공)
    Set<Characteristics> characteristics();
}
```

- Example toList()

```java
public class ToListCollector<T> implements Collector<T, List<T>, List<T>> {
    @Override
    public Supplier<List<T>> supplier() { //<- 수집 연산의 시작
        return () -> new ArrayList<T>(); //= return ArrayList::new; (생성자 참조)
    }
    @Override
    public BiConsumer<List<T>, T> accumulator() { //<- 탐색한 항목을 누적하고 바로 누적자를 수정
        return (list, item) -> list.add(item); //= return LisT::add;
    }
    @Override
    public Function<List<T>, List<T>> finisher() { 
        return Fcuntion.identity(); //<- 항등 함수
    }
    @Override
    public BinaryOperator<List<T>> combiner() {
        return (list1, list2) -> { //<- 두 번째 콘텐츠와 합쳐서 첫 번째 누적자 수정
            list1.addAll(list2); //<- 변경된 첫 번째 누적자 반환
            return list1;
        };
    }
    @Override
    public Set<Characteristics> characteristics() {
        /* UNORDERED: 리듀싱 결과는 스트림 요소의 방문 순서나 누적 순서에 영향을 받지 않음
      * CONCURRENT: 다중 스레드에서 accumulator 함수를 동시에 호출할 수 있으며, 스트림의 병렬 리듀싱 수행 가능
      * IDENTITY_FINISH: 리듀싱 과정의 최종 결과로 누적자 객체를 바로 사용
      */
        return Collections.unmodifiableSet(EnumSet.of(IDENTITY_FINISH, CONCURRENT));
    }
}
```

- 사용하기

```java
//Before
List<Dish> dishes = menu.stream().collect(toList());
//After
List<Dish> dishes = menu.stream().collect(new ToListCollector<Dish>());
```

# 병렬 데이터 처리와 성능

## 병렬 스트림

- `parallelStream()` : 각각의 스레드에서 처리할 수 있도록 스트림 요소를 여러 청크로 분할한 스트림
- 내부적으로 `ForkJoinPool` 을 사용

```java
//parallel() : 순차 스트림을 병렬 스트림으로
//sequential() : 병렬 스트림을 순차 스트림으로
public Long parallelSum(long n) {
    return Stream.iterate(1L, i -> i + 1)
                .limit(n)
                .parallel()
                .reduce(0L, Long::sum);
}
```

**스트림 성능 측정**

- Java Microbenchmark Harness(JMH) 라이브러리를 통해 벤치마크 구현이 가능

- [Microbenchmarking with Java](https://www.baeldung.com/java-microbenchmark-harness)

  ```java
  // https://mvnrepository.com/artifact/org.openjdk.jmh/jmh-core (핵심 JMH 구현 포함)
  implementation group: 'org.openjdk.jmh', name: 'jmh-core', version: '1.34'
      
  // https://mvnrepository.com/artifact/org.openjdk.jmh/jmh-generator-annprocess (JAR 파일 생성에 도움을 주는 어노테이션 프로세서 포함)
  testImplementation group: 'org.openjdk.jmh', name: 'jmh-generator-annprocess', version: '1.34'
  ```

- 함수 성능 측정

  - 올바른 자료구조를 선택해야 병렬 실행도 최적의 성능을 발휘할 수 있다.
  - 함수형 프로그래밍을 올바르게 사용하여 병렬 실행의 힘을 이용해보자.

  ```java
  @BenchmarkMode(Mode.AverageTime) //<- 벤치마크 대상 메서드 실행에 걸린 평균 시간 측정
  @OutputTimeUnit(TimeUnit.MILLISECONDS) //<- 벤치마크 결과를 밀리초 단위 출력
  @Fork(value = 2, jvmArgs = { "-Xms4G", "-Xmx4G" }) //<- 4GB 힙 공간을 제공한 환경에서 두 번의 수행을 통해 결과 신뢰성 확보
  public class ParallelStreamBenchmark {
  
      private static final long N = 10_000_000L;
  
      @Benchmark //<- 벤치마크 대상 메서드
      public long sequentialSum() {
          return Stream.iterate(1L, i -> i + 1).limit(N).reduce(0L, Long::sum);
      }
      
  	@Benchmark
  	public long parallelRangedSum() {
  		/* iterate() 대신 LongStream.rangeClosed()
  		 * 기본형 long을 직접 사용하여 박싱, 언박싱 오버헤드 해결
            * 청크로 분할할 수 있는 숫자 범위 생산
            */
  		return LongStream.rangeClosed(1, N).parallel().reduce(0L, Long::sum);
  	}
  
      @TearDown(Level.Invocation) //<- 매 벤치마크 실행 후 GC 동작 시도
      public void tearDown() {
          System.gc();
      }
  }
  ```

**병렬 스트림 주의점**

- 병렬화를 이용하려면, `스트림을 재귀적으로 분할`해야 하고,

- 각 서브 스트림을 `서로 다른 스레드의 리듀싱 연산으로 할당`해야 하고,

- 이들 `결과를 하나의 값으로 합쳐`야 한다.

- 멀티 코어 간의 데이터 이동은 생각보다 비싸므로, 코어 간 데이터 전송 시간보다 훨씬 오래 걸리는 작업만 병렬로 처리하자.

- 또한, 병렬 스트림과 병렬 계산에서는 공유된 가변 상태를 피하자. `상태 공유에 따른 부작용`

  ```java
  public static long sideEffectParallelSum(long n) {
      Accumulator accumulator = new Accumulator();
      LongStream.rangeClosed(1, n).parallel().forEach(accumulator::add);
      return accumulator.total;
  }
  
  public static class Accumulator {
      private long total = 0;
      public void add(long value) { total += value; }
  }
  
  // 여러 스레드에서 동시에 누적자를 수정하면서 올바른 결과값이 나오지 않게 된다.
  System.out.println(ParallelStreams.sideEffectParallelSum(10_000_000L))
  ```

**병렬 스트림 효과적으로 사용하기**

- 확신이 서지 않으면 직접 측정하자.
  - 순차 스트림과 병렬 스트림 중 어떤 것이 좋을지 모르겠다면 벤치마크로 성능을 측정해보자.
- 박싱을 주의하자.
  - 자동 박식/언박싱은 성능을 크게 저하시킬 수 있는 요소다.
  - 박싱 동작을 피하도록 되도록 기본형 특화 스트림을 사용해보자. (IntStream, LongStream, DoubleStream)
- 순차 스트림보다 병렬 스트림에서 성능이 떨어지는 연산이 있다.
  - 요소의 순서에 의존(limit, findFirst)하는 연산은 병렬 스트림에서 더 비싼 비용이 들어간다.
- 스트림에서 수행하는 전체 파이프라인 연산 비용을 고려하자.
  - N(처리해야 할 요소 수) * Q(하나의 요소 처리 비용)
  - Q가 높아지는 것은 병렬 스트림으로 성능 개선 가능성이 있음을 의미한다.
- 소량의 데이터에서는 병렬 스트림이 도움이 되지 않는다.
  - 소량의 데이터는 병렬화 과정에서 생기는 부가 비용을 상쇄할 만큼의 이득을 얻지 못한다.
- 스트림을 구성하는 자료구조가 적절한지 확인하자.
  - ex. ArrayList를 LinkedList 보다 효율적으로 분할할 수 있다.
- 스트림의 특성과 파이프라인의 중간 연산이 스트림의 특성을 어떻게 바꾸는지에 따라 분해 과정의 성능이 달라질 수 있다.
  - Sized 스트림은 정확히 같은 크기의 두 스트림으로 분할 가능하여 효과적이지만, 필터 연산은 스트림 길이 예측이 불가하여 효과적인지 알 수 없다.
- 최종 연산의 병합 과정 비용을 살펴보자.
  - 병합 과정 비용이 비싸다면 병렬 스트림으로 얻은 성능 이익이 상쇄


|소스|분해성|
|---|---|
|ArrayList|Excellence|
|LinkedList|Bad|
|IntStream.range|Excellence|
|Stream.iterate|Bad|
|HashSet|Good|
|TreeSet|Good|

## 포크/조인 프레임워크

병렬 스트림을 제대로 사용하기 위해 병렬 스트림 내부 구조를 살펴보자.

`병렬화할 수 있는 작업을 재귀적으로 작은 작업으로 분할한 후, 서브태스크 각각의 결과를 합쳐 전체 결과를 만들도록 설계`

`서브태스크를 스레드 풀(ForkJoinPool)의 작업자 스레드에 분산 할당하는 ExecutorService Intergace 구현`

- 스레드 풀을 이용하려면, RecursiveTask<R>의 서브클래스를 만들어야 한다.

`포크/조인 프레임워크의 알고리즘은 `분할/정복` 알고리즘의 병렬화 버전이다.`

**포크/조인 프레임워크 제대로 사용하기**

- join 메서드를 태스크에 호출하면 태스크가 생산하는 결과가 준비될 때까지 호출자를 블록시킨다.
- RecursiveTask 내에서는 ForkJoinPool의 invoke 메서드를 사용하지 말자.
  - 대신 compute나 fork 메서드 직접 호출하고, 순차 코드에서 병렬 계산을 시작 시에만 invoke 사용
- 서브태스크에서 fork 메서드를 호출해서 ForkJoinPool의 일정 조절
  - 한 쪽 작업에는 fork, 다른 한 쪽 작업에는 compute 를 호출하자.
  - 두 서브 태스크의 한 태스크에는 같은 스레드를 재사용할 수 있다.
- 포크/조인 프레임워크를 이용하는 병렬 계산은 디버깅이 어렵다.
- 멀티코어에 포크/조인 프레임워크를 사용하는 것이 순차 처리보다 무조건 빠른 것은 아니다.

**포크/조인 프레임워크의 작업 훔치기**

포크/조인 프레임워크의 병렬 처리 방법

- 풀에 있는 작업자 스레드의 태스크를 재분배하고 균형을 맞출 때 `작업 훔치기 알고리즘`을 사용
  - `작업 훔치기 알고리즘` : 스레드는 자신에게 할당된 태스크를 포함하는 `이중 연결 리스트를 참조`하며 작업이 끝날 때마다 큐의 헤드에서 다른 태스크를 가져와 작업을 처리 -> 할 일이 없어진 스레드는 유휴 상태로 바뀌는 것이 아니라 (모든 큐가 빌 때까지) `다른 스레드 큐의 꼬리에서 작업을 훔쳐`온다.
- 따라서, 태스크 크기를 작게 나누어야 작업자 스레드 간의 작업 부화를 비슷한 수준으로 유지할 수 있다.

# 스트림과 람다를 이용한 효과적 프로그래밍

## 컬렉션 API 개선

### 컬렉션 팩토리

반환 객체는 불변

**List Factory** 

```java
//Before
List<String> friends = Arrays.asList("Park", "Kim", "Jeong");

//After
List<String> friends = List.of("Park", "Kim", "Jeong")
```

**Set Factory**

```java
Set<String> friends = Set.of("Park", "Kim", "Jeong");
```

**Map Factory**

```java
// 열 개 이하의 키/값 쌍을 가진 작은 맵을 만들 경우
Map<String, Integer> ageOfFriends = Map.of("Park", 20, "Kim", 21, "Jeong", 25);

// 그 이상의 맵 생성 (Map.enty: Map.Entry 객체를 만드는 새로운 팩토리 메서드)
import static java.util.Map.entry;
Map<String, String> ageOfFriends = Map.ofEntries(
        entry("Park", 20),
        entry("Kim", 21),
        entry("Jeong", 25));
```

### 리스트와 집합 처리

기존 컬렉션 객체와 Iterator 객체를 혼용한 삭제, 수정은 쉽게 문제를 일으켰었다.

그래서, java8에서는 List, Set Interface 에 새로운 메서드가 추가되었다. (기존 컬렉션 자체를 수정)

**removeIf**

- Predicate를 만족하는 요소 제거 (List, Set)

```java
transactions.removeIf(transaction ->
                     Character.isDigit(transaction.getReferenceCode().charAt(0)));
```

**replaceAll**

- UnaryOperator 함수를 이용하여 요소 교체 (List)

```java
referenceCodes.replaceAll(code -> Character.toUpperCase(code.charAt(0)) + code.substring(1));
```

**sort**

- 리스트 정렬 (List)

```java
list.sort(Comparator.naturalOrder()); // 오름차순
list.sort(Comparator.reverseOrder());
list.sort(String.CASE_INSENSITIVE_ORDER); // 대소문자 구분없이 오름차순
list.sort(Collections.reverseOrder(String.CASE_INSENSITIVE_ORDER));
```

### 맵 처리

**1. forEach**

- 기존 맵에서 키/값을 반복하며 확인했다면, forEach 메서드를 사용해보자.

```java
ageOfFriens.forEach((friend, age) -> System.out.println(friens + " is" + age + " years old"));
```

**2. Order**

- Entry.comparingByValue / Entry.comparingByKey

```java
favouriteMovies.entrySet().stream()
    .sorted(Entry.comparingByKey()) // 오름차순
//    .sorted(Entry.comparingByKey(Comparator.reverseOrder())) // 내림차순
    .forEachOrdered(System.out::println);
```

**3. getOrDefault**

- 찾으려는 키가 존재하지 않으면 기본값을 반환 getOrDefault(key, default)

```java
Map<String, String> favouriteMovies = Map.ofEntries(
                                        entry("Raphael", "Star Wars"),
                                        entry("Olivia", "James Bond"));

System.out.println(favouriteMovies.getOrDefault("Olivia", "Matrix")); // James Bond
System.out.println(favouriteMovies.getOrDefault("Thibaut", "Matrix")); // Matrix
```

**4. Compute Pattern**

**computeIfAbsent**

- 제공된 키에 해당하는 값이 없으면(값이 없거나 널), 키를 이용해 새 값을 계산하고 맵에 추가
  - 현재 키와 관련된 값이 맵에 존재하며 널이 아닐 때만 새 값을 계산

```java
Map<String, byte[]> dataToHash = new HashMap<>();
MessageDigest messageDigest = MessageDigest.getInstance("SHA-256");

lines.forEach(line ->
        dataToHash.computeIfAbsent(line, // 맵에서 찾을 키
                                   this::calculateDigest)); // 키가 존재하지 않을 경우 동작

private byte[] calculateDigest(String key) {
    return messageDigest.digest(key.getBytes(StandardCharsets.UTF_8));
}

// Map이 여러 값을 저장하는 형태일 경우
friendsToMovies.computeIfAbsent("Raphael", name -> new ArrayList<>())
    						.add("Star Wars");
```

**computeIfPresent**

- 제공된 키가 존재하면 새 값을 계산하고 맵에 추가

**compute**

- 제공된 키로 새 값을 계산하고 맵에 저장

**5. Remove Pattern**

```java
//제공된 키에 해당하는 맵 항목 제거
favouriteMovies.remove(key)
    
//키가 특정한 값과 연관되어 있을 경우에만 항목을 제거하는 오버로드 버전 메서드
favouriteMovies.remove(key, value);

//특정 조건에 해당하는 항목 삭제
favouriteMovies.entrySet().removeIf(entry -> entry.getValue < 10);
```

**6. Replace Pattern**

**replaceAll**

- BiFunction 을 적용한 결과로 각 항목의 값을 교체

```java
Map<String, String> favouriteMovies = new HashMap<>();
favouriteMovies.put("Raphael", "Star Wars");
favouriteMovies.put("Olivia", "james bond");
favouriteMovies.replaceAll((friend, movie) -> movie.toUpperCase());
```

**Replace**

- 키가 존재하면 맵의 값 교체

**7. Merge**

두 개의 맵에서 값을 합치거나 교체할 경우 사용

- 중복된 키가 없을 경우

```java
Map<String, String> family = Map.ofEntries(
        entry("Teo", "Star Wars"), entry("Cristina", "James Bond"));
Map<String, String> friends = Map.ofEntries(
    	entry("Raphael", "Star Wars"));

Map<String, String> everyone = new HashMap<>(family);
everyone.putAll(friends);
```

- 중복된 키가 있을 경우

```java
Map<String, String> family = Map.ofEntries(
        entry("Teo", "Star Wars"), entry("Cristina", "James Bond"));
Map<String, String> friends = Map.ofEntries(
    	entry("Raphael", "Star Wars"), entry("Cristina", "Matrix"));

Map<String, String> everyone = new HashMap<>(family);
friends.forEach((k, v) -> // forEach + merge 로 key 충돌 해결
                everyone.merge(k, v, (movie1, movie2) -> movie1 + " & " + movie2));
```

- 초기 검사 구현이 필요할 경우
  - 지정된 키와 연관된 값이 없거나 널이면,  두 번째 인수를 키와 연결
  - 그렇지 않을 경우, 세 번째 인자의 BiFunction을 적용

```java
moviesToCount.merge(movieName, 1L, (key, count) -> count + 1L);
```

### ConcurrentHashMap

ConcurrentHashMap 클래스는 동시 친화적이며 내부 자료구조의 특정 부분만 잠궈 동시 추가, 갱신 작업을 허용

**forEach**

- 각 (키/값) 쌍에 주어진 액션 실행

**reduce**

- 모든 (키/값) 쌍을 제공된 리듀스 함수를 이용해 결과로 합침

**search**

- 널이 아닌 값을 반환할 떄까지 각 (키/값) 쌍에 함수 적용

**(키/값) 인수를 이용한 네 가지 연산 형태 지원**

ConcurrentHashMap  상태를 잠그지 않고 연산을 수행하므로, 연산에 제공한 함수는 계산이 진행되는 동안 바뀔 수 있는 객체, 값, 순서 등에 의존하면 안 됨!

- 키/값으로 연산 : `forEach`, `reduce`, `search`
- 키로 연산 : `forEachKey`, `reduceKeys`, `searchKeys`
- 값으로 연산 : `forEachValue`, `reduceValues`, `searchValues`
- Map.entry 객체로 연산 : `forEachEntry`, `reduceEntries`, `searchEntriess`

**Count**

mappingCount

- 맵의 매핑 개수를 반환 (매핑 개수가 int의 범위를 넘어서는 이후의 상황 대처)

## 리팩터링, 테스팅, 디버깅

### 리팩터링

**코드 가독성 개선**

코드 가독성이 좋다?란 '어떤 코드를 다른 사람도 쉽게 이해할 수 있음'을 의미한다.

**1. 익명 클래스를 람다 표현식으로 리팩터링하기**

- 익명 클래스에서 사용한 this와 super는 람다 표현식에서 다른 의미를 갖는다.
  - 익명 클래스에서 this는 익명 클래스 자신
  - 람다에서 this는 람다를 감싸는 클래스
- 익명 클래스는 감싸고 있는 클래스의 변수를 가릴 수 있다.
  - 람다 표현식으로는 불가

```java
/*
 * 익명 클래스 사용
 */
Runnable r1 = new Runnable() {
    public void run() {
        System.out.println("Hello");
    }
};

/*
 * 람다 표현식 사용
 */
Runnable r2 = () -> System.out.println("Hello");

interface Task {
    public void execute();
}
public static void doSomething(Runnable r) { r.run(); }
public static void doSomething(Task a) { r.execute(); }
// 람다 표현식의 대상 형식이 모호할 경우 명시적 형변환을 이용
doSomething((Task)() -> System.out.println("Hello"));
doSomething((Runnable)() -> System.out.println("Hello"));
```

**2. 람다 표현식을 메서드 참조로 리팩터링하기**

```java
/*
 * 람다 표현식 사용
 */
Map<CaloricLevel, List<Dish>< dishesByCaloricLevel = 
    menu.stream().collect(
            groupingBy(dish -> {
              if (dish.getCalories() <= 400) { return CaloricLevel.DIET; }
              else if (dish.getCalories() <= 700) { return CaloricLevel.NORMAL; }
              else { return CaloricLevel.FAT; }
    }));

/*
 * 메서드 참조 사용
 */
public class Dish {
    //...
    
    public CaloricLevel getCaloricLevel() {
        if (dish.getCalories() <= 400) { return CaloricLevel.DIET; }
        else if (dish.getCalories() <= 700) { return CaloricLevel.NORMAL; }
        else { return CaloricLevel.FAT; }
    }
}

Map<CaloricLevel, List<Dish>< dishesByCaloricLevel = 
    menu.stream().collect(groupingBy(Dish::getCaloricLevel));
```

```java
// 람다 표현식 사용
inventory.sort((Apple a1, Apple a2) -> a1.getWeight().compareTo(a2.getWeight()));
// 정적 헬퍼 메서드(comparing, maxBy) 참조 사용
inventory.sort(comparing(Apple::getWeight));

// 람다 표현식 사용
int totalCalories = menu.stream().map(Dish::getCalories).reduce(0, (c1, c2) -> c1 + c2);
// 내장 헬퍼 메서드(sum, maximum) 참조 사용
int totalCalories = menu.stream().collect(summingInt(Dish::getCalories));
```

**3. 명령형 데이터 처리를 스트림으로 리팩터링하기**

스트림 API로 데이터 처리 파이프라인의 의도를 더 명확하게 보여주자.

```java
/*
 * 명령형 코드
 */
List<String> dishNames = new ArrayList<>();
for(Dish dish: menu) {
    if(dish.getCalories() > 300) {
        dishNames.add(dish.getName());
    }
}

/*
 * 스트림 API
 */
menu.parallelStream()
    .filter(d -> d.getCalories() > 300)
    .map(Dish::getName)
    .collect(toList());
```

**4. 코드 유연성 개선**

람다 표현식을 이용해서 동작 파라미터화를 쉽게 구현해보자.

- 함수형 인터페이스 적용

  - 람다 표현식을 이용하기 위해 함수형 인터페이스를 추가

- 조건부 연기 실행

  ```java
  // Before : 복잡한 제어 흐름 코드 (상태 노출 및 매번 상태 체크)
  if (logger.isLoggable(Log.FINER)) {
      logger.finer("Problem: " + generateDiagnostic());
  }
  // After : 가독성과 캡슐화 강화
  public void log(Level level, Supplier<String> msgSupplier) {
      if(logger.isLoggable(level)) {
          log(level, msgSupplier.get());
      }
  }
  
  logger.log(Level.FINER, () -> "Problem: " + generateDiagnostic());
  ```

- 실행 어라운드

  - 준비, 종료 과정을 처리하는 로직을 재사용하여 코드 중복 줄이기

  ```java
  String oneLine = processFile((BufferedReader b) -> b.readLine()); // 람다 전달
  String twoLines = processFile((BufferedReader b) -> b.readLine() + b.readLine()); // 다른 람다 전달
  
  public static String processFile(BufferedReaderProcessor p) throws IOException {
      try (BufferedReader br = new BufferedReader(new FileReader("Aaron/MJIA/test.txt"))) {
          return p.process(br); // 인수로 전달된 BufferedReaderProcessor 실행
      }
  } // IOException을 던질 수 있는 람다의 함수형 인터페이스
  
  public interface BufferedReaderProcessor {
      String process(BufferedReader b) throws IOException;
  }
  ```

## 132R

### 테스팅

### 디버깅

람다를 이용한 도메인 전용 언어

