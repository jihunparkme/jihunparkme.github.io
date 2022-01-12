---
layout: post
title: 상속 다루기
summary: Chapter 12. 상속 다루기
categories: (Book)Refactoring
featured-img: refactoring
# mathjax: true
---

# Refactoring

# Chapter 12. 상속 다루기

`특정 기능을 상속 계층구조의 위나 아래로 옮겨야 하는 상황은 드물지 않다`

`상속은 막강한 도구지만, 잘못된 곳에서 사용되거나 나중에 환경이 변해 문제가 생기기도 한다.`

## 메서드 올리기

`메서드들의 본문 코드가 똑같을 경우 적용해보자.`

`해당 메서드의 본문에서 참조하는 필드들이 서브클래스에만 있는 경우 '필드들 먼저 슈퍼클래스로 올린' 후 메서드를 올리자.`

`두 메서드의 전체 흐름은 비슷하지만 세부 내용이 다르다면 '템플릿 메서드 만들기'를 고려해보자.`

- 반대 리팩터링 : 메서드 내리기

**개요**.

Before

```javascript
class Employee {}
class Salesperson extends Employee {
    get name() {}
}
class Engineer extends Employee {
    get name() {}
}
```

After

```javascript
class Employee {
    get name() {}
}
class Salesperson extends Employee {}
class Engineer extends Employee {}
```

**절차**.

1. 똑같이 동작하는 메서드인지 살펴보기
2. 메서드 안에서 호출하는 다른 메서드, 참조 필드들을 슈퍼클래스에서도 호출, 참조할 수 있는지 확인하기
3. 메서드 시그니처가 다르다면 `함수 선언 바꾸기`로 슈퍼클래스에서 사용하고 싶은 형태로 통일하기
4. 슈퍼클래스에 새로운 메서드를 생성하고 대상 메서드 코드 복사하기
5. 정적 검사
6. 서브 클래스 중 하나의 메서드 제거
7. 테스트
8. 다른 서브클래스의 메서드를 하나씩 제거

## 174R

명칭

**개요**.

Before

```javascript

```

After

```javascript

```

**절차**.

명칭

**개요**.

Before

```javascript

```

After

```javascript

```

**절차**.

명칭

**개요**.

Before

```javascript

```

After

```javascript

```

**절차**.

명칭

**개요**.

Before

```javascript

```

After

```javascript

```

**절차**.

명칭

**개요**.

Before

```javascript

```

After

```javascript

```

**절차**.

명칭

**개요**.

Before

```javascript

```

After

```javascript

```

**절차**.

명칭

**개요**.

Before

```javascript

```

After

```javascript

```

**절차**.

명칭

**개요**.

Before

```javascript

```

After

```javascript

```

**절차**.

명칭

**개요**.

Before

```javascript

```

After

```javascript

```

**절차**.

명칭

**개요**.

Before

```javascript

```

After

```javascript

```

**절차**.

명칭

**개요**.

Before

```javascript

```

After

```javascript

```

**절차**.

