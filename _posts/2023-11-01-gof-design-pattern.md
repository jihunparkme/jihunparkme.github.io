---
layout: post
title: GoF Design Pattern
summary: GoF Design Pattern
categories: JAVA
featured-img: design-pattern
---

# GoF Design Pattern

# Creational Patterns

생성 패턴

## Singleton Patterns

`인스턴스를 오직 한개만 제공`하는 클래스

- 시스템 런타임, 환경 세팅 정보 등.. 인스턴스가 여러개일 때 이슈가 생길 수 있는 경우
- 인스턴스를 한 개만 만들어서 제공하는 클래스 필요

(1) private 생성자와 public static 메소드를 사용
- 여러 스레드가 동시에 접근 가능한 위험 존재

```java
public class Settings {

    private static Settings instance;

    private Settings() {
    }

    public static Settings getInstance() {
        if (instance == null) {
            instance = new Settings();
        }

        return instance;
    }
}
```