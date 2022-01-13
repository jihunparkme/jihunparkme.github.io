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

## 필드 올리기

`필드들이 비슷한 방식으로 쓰인다고 판단되면 슈퍼클래스로 올리자.`

`이 리팩터링을 통해 '데이터 중복 선언을 없앨' 수 있고, '해당 필드를 사용하는 동작을 서브클래스에서 슈퍼클래스로 옮길' 수 있다.`

- 반대 리팩터링 : 필드 내리기

**개요**.

Before

```java
class Employee {}
class Salesperson extends Employee {
    private String name;
}
class Engineer extends Employee {
    private String name;
}
```

After

```java
class Employee {
    protected String name;
}
class Salesperson extends Employee {}
class Engineer extends Employee {}
```

**절차**.

1. 후보 필드들이 똑같은 방식으로 사용되는지 살피기
2. 필드들의 이름을 똑같은 이름으로 바꾸기 -> `필드 이름 바꾸기`
3. 슈퍼클래스에 새로운 필드 생성하기 `protected 선언`
4. 서브클래스의 필드들을 제거
5. 테스트

## 생성자 본문 올리기

`이 리팩터링으로 간단하게 끝나지 않는다면 '생성자를 팩터리 함수로 바꾸기'를 고려해보자.`

**개요**.

Before

```javascript
class Party {}

class Employee extends Party {
    constructor(name, id, monthlyCost) {
        super();

        this._name = name;
        this._id = id;
        this._monthlyCost = monthlyCost;
	    // 모든 서브 클래스가 수행하는 공통 코드
        if (this.isPrivileged) { this.assignCar(); }
    }
}
```

After

```javascript
class Party {
    constructor(name) { //.1
        this._name = name; //.3
    }
    finishConstruction() {
        if (this.isPrivileged) this.assignCar();
    }
}

class Employee extends Party {
    constructor(name, id, monthlyCost) {
        super(name); //.3

        this._id = id;
        this._monthlyCost = monthlyCost;
        
        this.finishConstruction(); //.5
    }
}
```

**절차**.

1. 슈퍼클래스에 생성자 정의하기
   - 서브클래스 생성자에서 호출 확인
2. `문장 슬라이스하기`로 공통 문장을 모두 super() 호출 직후로 옮기기
3. 공통 코드를 슈퍼클래스에 추가하고 서브클래스에서 제거하기
   - 생성자 매개변수 중 공통 코드에서 참조하는 값들은 모두 super()로 건내기
4. 테스트
5. 공통 코드가 나중에 올 경우 공통 코드에 `함수 추출하기`와 `메서드 올리기`를 차례로 적용하기

## 177R

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

