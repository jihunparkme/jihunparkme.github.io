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

## 메서드 내리기

`특정 서브클래스 하나|소수 에만 관련된 메서드는 슈퍼클래스에서 제거하고 해당 서브클래스에 추가하자.`

`해당 기능을 제공하는 서브클래스가 정확히 무엇인지를 호출자가 알고 있을 경우에만 적용하자.`

- 반대 리팩터링 : 메서드 올리기

**개요**.

Before

```javascript
class Employee {
    get quota() {}
}

class Engineer extends Employee {}
class Salesperson extends Employee {}
```

After

```javascript
class Employee {} //.2

class Engineer extends Employee {} //.4
class Salesperson extends Employee { //.1
    get quota() {}
}
```

**절차**.

1. 대상 메서드를 모든 서브클래스에 복사하기
2. 슈퍼클래스에서 해당 메서드 제거하기
3. 테스트
4. 사용하지 않는 해당 메서드를 모든 서브클래스에서 제거하기
5. 테스트

## 필드 내리기

`서브클래스 하나|소수에만 사용되는 필드는 해당 서브클래스로 옮기자.`

- 반대 리팩터링 : 필드 올리기

**개요**.

Before

```javascript
class Employee {
    private String quota;
}

class Engineer extends Employee {}
class Salesperson extends Employee {}
```

After

```javascript
class Employee {} //.2

class Engineer extends Employee {} //.4
class Salesperson extends Employee { //.1
    protected String quota;
}
```

**절차**.

1. 대상 필드를 모든 서브클래스에 정의
2. 슈퍼클래스에서 해당 필드 제거
3. 테스트
4. 사용하지 않는 해당 필드를 모든 서브클래스에서 제거하기 
5. 테스트

## 타입 코드를 서브클래스로 바꾸기

`타입 코드는 구분을 위해 주로 사용된다.`

`서브클래스는 조건에 따라 다르게 동작하도록 해주는 다형성을 제공한다.`

`특정 타입에서만 의미가 있는 값을 사용하는 필드나 메서드가 있을 때 관계를 명확히 드러내준다.`

- 반대 리팩터링 : 서브클래스 제거하기
- 하위 리팩터링
  -  타입 코드를 상태/전략 패턴으로 바꾸기
  - 서브클래스 추출하기

**개요**.

Before

```javascript
function createEmployee(name, type) {
    return new Employee(name, type);
}
```

After

```javascript
function createEmployee(name, type) {
    switch (type) {
        case 'engineer': return new Engineer(name);
        case 'salesperson': return new Salesperson(name);
        case 'manager': return new Manager(name);
    }
}
```

**절차**.

1. 타입 코드 필드를 `자가 캡슐화`하기
2. 타입 코드 값 하나를 선택하여 그 값에 해당하는 `서브클래스` 만들기
3. 매개변수로 받은 타입 코드와 새로운 서브클래스를 매핑하는 `선택 로직` 만들기
4. 테스트
5. 타입 코드 값 각각에 대해 서브클래스 생성과 선택 로직 추가를 반복
6. 타입 코드 필드 제거
7. 테스트
8. 타입 코드 접근자를 이용하는 메서드를 모두 메서드 내리기와 조건부 로직을 다형성으로 바꾸기 적용

**Example**

- Employee 직접 상속

```javascript
class Employee {
    constructor(name) { //.6 타입 코드 필드 제거
        this._name = name;
    }
    set type(type) { this.type = Employee.createEmployee(this._name, arg); }
    toString() { return `${this._name} (${this.capitalizedType})`; }
    get capitalizedType() { 
        return (this.type.charAt(0).toUpperCase() + this.type.substr(1).toLowerCase());
    }
    function createEmployee(name, type) { //.3 생성자를 팩터리 함수로 바꾸기
        switch (type) { //.5
            case 'engineer': return new Engineer(name);
            case 'salesperson': return new Salesperson(name);
            default: throw new Error(`${type}라는 직원 유형은 없습니다.`);
        }
    }
}

class Engineer extends Employee { //.2 서브클래싱
    get type() { return 'engineer'; } //.1 타입 코드 필드 캡슐화
}
class Salesperson extends Employee {
    get type() { return 'salesperson'; }
}
```

- Employee 간접 상속

```javascript
class Employee {
    constructor(name, type) { //.6 타입 코드 필드 제거
        this._name = name;
    }
    set type(arg) { this.type = Employee.createEmployee(arg); }
    get typeString() { return this.type.toString(); }
    get type() { return this.type; }
    toString() { return `${this._name} (${this.type.capitalizedName})`; }
    static createEmployee(aString) { //.3 생성자를 팩터리 함수로 바꾸기
        switch (aString) { //.5
            case 'engineer': return new Engineer();
            case 'salesperson': return new Salesperson();
            default: throw new Error(`${aString}라는 직원 유형은 없습니다.`);
        }
    }
}

class EmployeeType { //.1 타입 코드를 객체로 바꾸기
    get capitalizedName() {
        return this.toString().charAt(0).toUpperCase() + this.toString().substr(1).toLowerCase();
    }
}
class Engineer extends EmployeeType { 
    toString() { return 'engineer'; }
}
class Salesperson extends EmployeeType {
    toString() { return 'salesperson'; }
}
```

## 서브클래스 제거하기

`시스템이 성장하면서 활용되지 않거나, 필요로 하지 않는 방식으로 사용되는 서브클래스를 제거하자.`

- 반대 리팩터링 : 타입 코드를 서브클래스로 바꾸기

**개요**.

Before

```javascript
class Person {
    constructor(name) {
        this._name = name;
    }
    get name() { return this._name; }
    get genderCode() { return 'X'; }
    // ...
}

class Male extends Person {
    get genderCode() { return 'M'; }
}
class Female extends Person {
    get genderCode() { return 'F'; }
}

const numberOfMales = people.filter((p) => p instanceof Male).length;
```

After

```javascript
class Person {
    constructor(name, genderCode) {
        this._name = name;
        this._genderCode= genderCode; //.3 서브클래스의 타입을 나타내는 필드 생성
    }
    get name() { return this._name; }
    get genderCode() { return this._genderCode; }
    //.2 타입 검사 코드 .4 서브클래스 참조가 아닌 타입 필드 사용
    get isMale() { return 'M' === this._genderCode; } 
    // ...
}

function createPerson(aRecord) { //.1 생성자를 팩터리 함수로 바꾸기
    switch (aRecord.gender) {
        case 'M': return new Person(aRecord.name, 'M');
        case 'F': return new Person(aRecord.name, 'F');
        default: return new Person(aRecord.name, 'X');
    }
}
function loadFromInput(data) {
    return data.map((aRecord) => createPerson(aRecord));
}

const numberOfMales = people.filter(p => p.isMale).length;
```

**절차**.

1. 서브클래스의 생성자를 `팩터리 함수`로 바꾸기
2. 서브클래스 타입을 검사하는 코드가 있다면 검사 코드에 `함수 추출하기`, `함수 옮기기`를 적용하여 슈퍼클래스로 옮기기
3. 서브클래스의 타입을 나타내는 필드를 슈퍼클래스에 만들기
4. 서브클래스를 참조하는 메서드가 새로 만든 타입 필드를 이용하도록 수정
5. 서브클래스 지우기
6. 테스트

## 185R

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

