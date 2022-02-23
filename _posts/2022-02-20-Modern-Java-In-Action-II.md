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

**java.util.Optional<T>**

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

  





165R

## Date & Time API

## Default Method

## Java Module System

