---
layout: post
title: Modern Java In Action II
summary: Modern Java In Action II
categories: (Book)Modern-Java-In-Action
featured-img: modern-java
# mathjax: true
---

# Modern Java In Action

# Every day with Java

## Optional Class

Optional 형식을 통해 도메인 모델의 의미를 명확히 만들고, null 참조 대신 값이 없는 상황을 표현해 보자.

**Null 참조의 문제점**

- `에러의 근원` : NullPointerException
- `코드를 어지럽힘` : null 확인 코드
- `아무 의미가 없음` : null 은 아무 의미도 표현하지 않는다.
- `자바 철학에 위배` : 자바는 개발자로부터 모든 포인터를 숨겼지만 null 포인터는 예외
- `형식 시스템에 구멍을 만듦` : null의 의미를 알 수 없음

**java.util.Optional`<T>`**

- 값이 있을 경우 Optional 클래스는 값을 감싼다.
- 값이 없으면 Optional.empty

### Optional 적용 패턴

**Optional 객체 만들기**

- 빈 Optional

  ```java
  Optional<Car> optCar = Optional.empty();
  ```

- null이 아닌 Optional

  ```java
  Optional<Car> optCar = Optional.of(car);
  ```

- null 값으로 Optional 만들기

  ```java
  Optional<Car> optCar = Optional.ofNullable(car);
  ```

**Map으로 Optional 값을 추출하고 변환하기**

```java
Optional<Insurance> optInsurance = Optional.ofNullable(insurance);
Optional<String> name = optInsurance.map(Insurance::getName);
```

**flatMap으로 Optional 객체 연결**

```java
Optional<Person> optPerson = Optional.of(person);
Optional<String> name = optPerson.flatMap(Person::getCar)
    							.flatMap(Car::getInsurance)
							    .map(Insurance::getName)
    							.orElse("Unkown");
```

**Optional의 직렬화 불가**

- Optional은 Serializable Interface를 구현하지 않는다.

- Optional 클래스를 필드 형식으로 사용할 수 없으니, Optional 로 값을 반환받을 수 있는 메서드를 추가하자.

  ```java
  public class Person {
      private Car car;
      public Optional<Car> getCarAsOptional() {
          return Optional.ofNullable(car);
      }
  }
  ```

**Optional 스트림 조작**

```java
public Set<String> getCarInsuranceNames(List<Person> persons) {
    Stream<Optional<String>> stream =  persons.stream()
        .map(Person::getCar) //return Stream<Optional<Car>>
        .map(optCar -> optCar.flatMap(Car::getInsurance)) //return Optional<Insurance>
        .map(optInsurance -> optInsurance.map(Insurance::getName)) //return Optional<String> mapping
        .flatMap(Optional::stream) //return Stream<Optional<String>>
        .collect(toSet());
    
    return stream.filter(Optional::isPresent) //null이 아닌 값만 전달
        		.map(Optional::get)
        		.collect(toSet());
}
```

**Default Action & Optional unwrap**

- `get()` : Optional 에 값이 반드시 있을 경우 사용하자. (없을 경우 NoSuchElementException 발생)
- `orElse(T other)` : Optional이 값을 포함하지 않을 때 기본값 제공
- `orElseGet(Supplier<? extends T> other)` : Optional 이 비어있을 경우 기본값 생성
- `orElseThrow(Supplier<? extends X> exceptionSupplier)` : Optional이 비어있을 때 예외 발생
- `ifPresent(Comsumer<? super T> consumer)` : 값이 존재할 경우 인수로 넘겨준 동작 실행
- `ifPresentOrElse(Comsumer<? super T> action, Runnable emptyAction)` : Optional 이 비었을 때 실행할 수 있는 Runnable을 인수로 받음

**두 Optional 합치기**

- Before

```java
public Optional<Insurance> nullSafeFindCheapestInsurance(Optional<Person> person, Optional<Car> car) {
    if (person.isPresent() && car.isPresent()) {
        return Optional.of(findCheapestInsurance(person.get(), car.get()));
    } else {
        return Optional.empty();
    }
}
```

- After

```java
public Optional<Insurance> nullSafeFindCheapestInsurance(Optional<Person> person, Optional<Car> car) {
    return person.flatMap(p -> car.map(c -> findCheapestInsurance(p, c)));
}
```

**필터로 특정 값 거르기**

- Optional 에 값이 있을 경우 filter 동작

```java
Optional<Insurance> optInsurance = Optional.of(insurance);
optInsurance.filter(insurance ->
                   "CambridgeInsurance".equals(insurance.getName()))
    			.ifPresent(x -> System.out.pringln("ok"));
```

```java
int minAge = 20;
Optional<Person> optPerson = Optional.of(person);
//Person이 minAge 이상의 나이일 경우에만 보험회사 이름 반환
Optional<String> name = optPerson.filter(p -> p.getAge() >= minAge)
							    .flatMap(Person::getCar)
    							.flatMap(Car::getInsurance)
							    .map(Insurance::getName)
    							.orElse("Unkown");
```

**Reference**

- [Optional Class Method](https://docs.oracle.com/javase/9/docs/api/java/util/Optional.html)

### Optional 활용

**잠재적으로 null이 될 수 있는 대상을 Optional로 감싸기**

```java
Optional<Object> value = Optional.ofNullable(map.get("key"));
```

**예외와 Optional 클래스**

- 예외를 빈 Optional로 처리하기

  ```java
  //OptionalUtility.java
  public static Optional<Integer> stringToInt(String s) {
      try {
          return Optional.of(Integer.parseInt(s));
      } catch {
          return Optional.empty();
      }
  }
  ```

**기본형 Optional 을 사용하지 말자**

- 기본형 Optional 에는 `OptionalInt`, `OptionalLong`, `OptionalDouble` 등이 있다.
  - 이 기본형 특화 Optional은 다른 일반 Optional과 혼용할 수 없다.

**응용**

- Optional로 프로퍼티에서 지속 시간 읽기

  ```java
  public int readDuration(Properties props, String name) {
      return Optional.ofNullable(props.getProperty(name)) //null일 경우 Optional 처리
          			.flatMap(OptionalUtility::stringToInt) //OptionalUtility.stringToInt 메서드 참조
          			.filter(i -> i > 0) //음수 필터링
          			.orElse(0); //기본값 0
  }
  ```

## Date & Time API

### java.time

- [java.time package](https://docs.oracle.com/javase/8/docs/api/java/time/package-summary.html) 는 `LocalDate`, `LocalTime`, `LocalDateTime`, `Instant`, `Duration`, `Period` 등 새로운 클래스를 제공

**`LocalDate`**

- 시간을 제외한 날짜를 표현하는 불변 객체

- 생성

  ```java
  LocalDate date = LocalDate.of(2022, 1, 1);
  
  //현재 날짜 정보
  LocalDate today = LocalDate.now();
  
  //parse 정적 메서드 사용
  LocalDate date = LocalDate.parse("2022-01-01");
  ```

- 사용

  ```java
  int year = date.getYear(); // 2022
  int monthValue = date.getMonthValue(); // 1
  Month month = date.getMonth(); // JANUARY
  int day = date.getDayOfMonth(); // 1
  DayOfWeek dow = date.getDayOfWeek(); // SATURDAY
  int len = date.lengthOfMonth(); // 31 (days in JANUARY)
  boolean leap = date.isLeapYear(); // false (not a leap year), 윤년 여부
  System.out.println(date); //2022-01-01
  
  //TemporalField를 이용한 LocalDate 값 읽기
  int year = date.get(ChronoField.YEAR); // 2022
  int month = date.get(ChronoField.MONTH_OF_YEAR); // 1
  int day = date.get(ChronoField.DAY_OF_MONTH); // 1
  ```

**`LocalTime`**

- 날짜를 제외한 시간을 표현하는 불변 객체

- 생성

  ```java
  LocalTime time = LocalTime.of(12, 34, 56); // 12:34:56
  
  //parse 정적 메서드 사용
  LocalTime time = LocalTime.parse("12:34:56");
  ```

- 사용

  ```java
  int hour = time.getHour(); // 12
  int minute = time.getMinute(); // 34
  int second = time.getSecond(); // 56
  ```

**`LocalDateTime`**

- 날짜와 시간을 모두 표현

- 생성

  ```java
  //2022-01-01T12:34:56
  LocalDateTime dt1 = LocalDateTime.of(2022, Month.JANUARY, 1, 12, 34, 56);
  
  // LocalDate + LocalTime
  LocalDateTime dt2 = LocalDateTime.of(date, time);
  
  // LocalDate <- atTime
  LocalDateTime dt3 = date.atTime(12, 34, 56);
  
  // LocalDate <- LocalTime
  LocalDateTime dt4 = date.atTime(time);
  
  // LocalTime <- LocalDate
  LocalDateTime dt5 = time.atDate(date);
  ```

- 사용

  ```java
  LocalDate date1 = dt1.toLocalDate();
  LocalTime time1 = dt1.toLocalTime();
  ```

**`Instant`**

- 기계 전용 유틸리티

- Unix epoch time 기준으로 특정 지점까지의 시간을 초로 표현

- 나노초(10억분의 1초)의 정밀도 제공

  ```java
  Instant.ofEpochSecond(3);
  Instant.ofEpochSecond(3, 0);
  Instant.ofEpochSecond(2, 1_000_000_000); //1초 후의 나노초
  Instant.ofEpochSecond(4, -1_000_000_000); //4초 전의 나노초
  ```

**`Duration`**

- 두 시간 객체 사이의 지속시간 [Docs](https://docs.oracle.com/javase/8/docs/api/java/time/Duration.html)

  ```java
  Duration d1 = Duration.between(time1, time2);
  Duration d2 = Duration.between(dateTime1, dateTime2);
  Duration d3 = Duration.between(instant1, instant2);
  
  //시간 객체를 사용하지 않고 생성
  Duration threeMinutes = Duration.ofMinutes(3);
  Duration threeMinutes = Duration.ofMinutes(3, ChronoUnit.MINUTES);
  ```

**`Period`**

- 두 시간 객체 사이의 지속 시간을 년,월,일로 표현할 경우 [Docs](https://docs.oracle.com/javase/8/docs/api/java/time/Period.html)

  ```java
  Period tenDays = Period.between(LocalDate.of(2022, 1, 1),
                                 LocalDate.of(2022, 1, 11));
  
  //시간 객체를 사용하지 않고 생성
  Period tenDays = Period.ofDays(10);
  Period threeWeeks = Period.ofWeeks(3);
  Period twoYearsSixMonthsOneDay = Period.of(2, 6, 1);
  ```

**간격을 표현하는 날짜와 시간 클래스의 공통 메서드**

```text
- between
- from
- of
- parse
- addTo
- get
- isNegative
- isZero
- minus
- multipliedBy
- negated
- plus
- subtractFrom
```
