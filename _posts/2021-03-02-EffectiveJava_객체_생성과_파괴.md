---
layout: post
title: 02. 객체 생성과 파괴
summary: 객체 생성과 파괴
categories: (Book)Effective-JAVA-3/E
featured-img: EFF_JAVA
# mathjax: true
---

# 2장. 객체 생성과 파괴

<br>
## item 1. 생성자 대신 정적 팩터리 메서드를 고려하라.

- 클래스는 생성자와 별도로 정적 팩터리 메서드(static factory method)를 제공할 수 있다.
```java
public static Boolean valueOf(boolean b) {
    return b ? Boolean.TRUE : Boolean.FALSE;
}
```

- static factory method가 생성자보다 좋은 장점
  1. 이름을 가질 수 있다.
     - ㅇㅇ
  2. 호출될 때마다 인스턴스를 새로 생성하지는 않아도 된다.


