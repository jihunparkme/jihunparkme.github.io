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

## 27L