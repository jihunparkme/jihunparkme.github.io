---
layout: post
title: 캡슐화 Refactoring
summary: Chapter 7.캡슐화
categories: (Book)Refactoring
featured-img: refactoring
# mathjax: true
---

# Refactoring

# Chapter 7. 캡슐화

## 레코드 캡슐화하기

`변수 조작 방식 통제를 위함`

`레코드는 연관된 여러 데이터를 직관적인 방식으로 묶을 수 있어서, 따로 취급할 때보다 의미 있는 단위로 전달할 수 있게 해준다.`

`캡슐화에서는 값을 수정하는 부분을 명확하게 드러내고 한 곳에 모아두는 일이 중요`

`가변 데이터를 저장할 경우 레코드보다 객체를 선호`

- 어떻게 저장했는지 숨기고, 각 값을 메서드로 제공

**개요**

?. Map type -> Class type

Before

```javascript
const organization = { name: '애크미 구스베리', country: 'GB' };
```

After

```javascript
class Organization {
    constructor(data) {
        this._name = data.name;
        this._country = data.country;
    }

    get name() { return this._name; }
    set name(arg) { this._name = arg; }
    get country() { return this._country; }
    set country(arg) { this._country = arg; }
}
```

**절차**

1. 레코드를 담은 변수 캡슐화 (변수를 반환하는 함수)
2. 레코드를 새로운 클래스로 정의 (Getter/Setter 생성)
3. 테스트
4. 새로 정의한 클래스 객체를 반환하는 함수 만들기
5. 기존 레코드 반환 코드를 새 함수로 변경
6. 클래스에서 원본 데이터 반환 접근자와 원본 레코드 반환 함수 제거
7. 테스트
8. 레코드 필드도 중첩 구조라면 레코드 캡슐화하기와 컬렉션 캡슐화하기를 재귀적으로 적용

## 컬렉션 캡슐화하기

`Collection 변수 접근을 캡슐화하면서 Getter가 Collection 자체를 반환한다면, 원본이 변경될 수 있다.`

- add(), remove() 라는 Collection 변경자 메서드를 만들자.

`Collection Getter 를 제공하되 내부 Collection의 복제본을 반환하자.`

`Collection 을 다루는 클래스는 불필요한 복제본을 만드는 편이 예상치 못한 수정으로 인한 오류를 디버깅하는 것보다 낫다.`

- 컬렉션 관리를 책임지는 클래스라면 항상 복제본을 제공하자.

**개요**

?. 컬렉션 관리는 복제본으로

Before

```javascript
class Person {
    constructor(name) {
        this._name = name;
        this._courses = [];
    }

    get name() { return this._name; }
    get courses() { return this.courses; }
    set courses(aList) { this._courses = aList; }
}
```

After

```javascript
class Person {
    constructor(name) {
        this._name = name;
        this._courses = [];
    }

    get name() { return this._name; }
    get courses() { return this.courses.slice(); }
    addCourse(aCourse) { this._courses.push(aCourse); }
    removeCourse(aCourse, fbIfAbsent = () => { throw new RangeError();} {
		const index = this._courses.indexOf(aCourse);
		if (index === -1) fbIfAbsent(); 
		else this._courses.splice(index, 1);
	}
	set courses(aList) { this._courses = aList.slice(); }
}
```

**절차**

1. 컬렉션 캡슐화가 되어있지 않다면 '변수 캡슐화하기' 진행
2. 컬렉션에 원소를 추가/제거하는 함수 추가
   - 컬렉션 자체를 통째로 바꾸는 Setter 는 제거하자.
3. 정적 검사
4. 기존 컬렉션 참조 코드를 추가/제거 함수 호출로 변경 및 테스트 
5. 컬렉션 Getter는 원본 내용을 수정할 수 없는 읽기 전용 프락시나 복제본 반환
6. 테스트

## 기본형을 객체로 바꾸기

`단순 출력 이상의 기능이 필요해지면 데이터를 표현하는 전용 클래스를 정의하자.`

**개요**

Before

```javascript
orders.filter((o) => 'high' === o.priority 
              	|| 'rush' === o.priority);
```

After

```javascript
orders.filter((o) => o.priority.higherThan(new Priority('normal')));
```

**절차**

1. 변수 캡슐화하기
2. 단순한 값 클래스 만들기
   - 기본 생성자와 Getter/Setter 추가
3. 정적 검사 수행
4. Getter/Setter 수정
5. 테스트
6. 함수 이름 검토

**Example**

```javascript
class Order {
    constructor(data) { 
        this._priority = data.priority;
    }
    // 1, 2
    get priority() { return this._priority; }
    get priorityString() { return this._priority.toString(); } // 6
    set priority(aString) { this._priority = new Priority(aString); } // 4
}
```

```javascript
class Priority {
    constructor(value) {
        if (value instanceof Priority) { return value; }
        // 우선순위 값 검증 및 비교 로직
        if (Priority.legalValues().includes(value)) {
            this._value = value;
        } else {
            throw new Error(`<${value}}> is invalid for Priority`);
        }
    }

    static legalValues() { return ['low', 'normal', 'high', 'rush']; }
    get _index() { return Priority.legalValues().findIndex((s) => s === this._value); }
    toString() { return this._value; }
    equals(other) { return this._index === other._index; }
    higherThan(other) { return this._index > other._index; }
    lowerThan(other) { return this._index < other._index; }
}
```

## 임시 변수를 질의 함수로 바꾸기

`다른 함수에서도 사용할 수 있어 코드 중복을 줄일 수 있다.`

`여러 곳에서 똑같은 방식으로 계산되는 변수를 발견하면 질의 함수로 바꿀 수 있을지 살펴보자.`

`값이 대입된 변수가 있는데, 복잡한 로직에서 여러 차례 다시 대입되는 경우 모두 질의 함수로 추출하자.`

**개요**

Before

```javascript
class Order {
    constructor(quantity, item) {
        this._quantity = quantity;
        this._item = item;
    }

    get price() { //
        var basePrice = this._quantity * this._itemPrice;
        var discountFactor = 0.98;
        if (basePrice > 1000) {
            discountFactor -= 0.03;
        }
        return basePrice * discountFactor;
    }
}
```

After

```javascript
class Order {
    constructor(quantity, item) {
        this._quantity = quantity;
        this._item = item;
    }

    get basePrice() { return this._quantity * this._itemPrice; }
    get discountFactor() {
        var discountFactor = 0.98;
        if (basePrice > 1000) {
            discountFactor -= 0.03;
        }
        return discountFactor;
    }
    get price() { return this.basePrice * this.discountFactor; } //
}
```

**절차**

1. 변수를 사용할 때마다 매번 다른 결과를 갖는지 확인
2. 변수를 읽기 전용으로 만들 수 있다면 읽기 전용으로 만들기
3. 테스트
   - 재대입 코드가 있는지 발견할 수 있다.
4. 변수 대입문을 함수로 추출
   - 사이드 이펙트가 있다면 질의 함수와 변경 함수로 분리하기로 대처
5. 테스트
6. 변수 인라인하기로 임시 변수 제거

## 클래스 추출하기

- 반대 리팩터링 : 클래스 인라인하기

`클래스는 명확하게 추상화하고 소수의 주어진 역할만 처리하자.`

`따로 묶을 수 있는 데이터와 메서드가 보인다면 어서 분리하자.`

**개요**

Before

```javascript
class Person {
    get officeAreaCode() { return this._officeAreaCode; }
    get officeNumber() { return this._officeNumber; }
}
```

After

```javascript
class Person {
    get officeAreaCode() { return this._telephoneNumber.areaCode; }
    get officeNumber() { return this._telephoneNumber.number; }
}

class TelephoneNumber {
    get areaCode() { return this._areaCode; }
    get number() { return this._number; }
}
```

**절차**

1. 클래스 역할 분리 방법 정하기
2. 분리될 역할을 담당할 클래스 만들기
3. 원래 클래스 생성자에서 새로운 클래스의 인스턴스 생성
4. 분리된 역할에 필요한 필드들을 새로운 클래스로 옮기기
5. 메서드들도 새로운 클래스로 옮기기(함수 옮기기)
   - 호출을 당하는 일이 많은 메서드부터 옮기자
6. 양쪽 클래스의 인터페이스를 살피며 불필요 메서드 제거 및 환경에 맞게 이름 수정(함수 선언 바꾸기)
7. 새로운 클래스를 외부로 노출할지 결정
   - 외부로 노출할 경우 "새로운 클래스에 참조를 값으로 바꾸기" 적용 고민

**Example**

```javascript
class Person {
    constructor() {
        this._telephoneNumber = new TelephoneNumber();
    }
    get officeAreaCode() { return this._telephoneNumber.areaCode; }
    set officeAreaCode(arg) { this._telephoneNumber.areaCode = arg; }
    get officeNumber() { return this._telephoneNumber.number; }
    set officeNumber(arg) { this._telephoneNumber.number = arg; }
    get telephoneNumber() { return this._telephoneNumber.toString(); }
}
```

```javascript
class TelephoneNumber {
    get areaCode() { return this.areaCode; }
    set areaCode(arg) { this.areaCode = arg; }
    get number() { return this.number; }
    set number(arg) { this.number = arg; }
    get toString() { return `(${this.areaCode}) ${this.number}`; }
}
```

## 클래스 인라인하기

`역할 옮기기 리팩터링 후 더 이상 제 역할을 못 하는 클래스는, 자신을 가장 많이 사용하는 클래스로 흡수시키자.`

- 반대 리팩터링 : 클래스 추출하기

**개요**

Before

```javascript
class Person {
    get officeAreaCode() { return this._telephoneNumber.areaCode; }
    get officeNumber() { return this._telephoneNumber.number; }
}

class TelephoneNumber { 
    get areaCode() { return this._areaCode; }
    get number() { return this._number; }
}
```

After

```javascript
class Person {
  get officeAreaCode() { return this._officeAreaCode; }
  get officeNumber() { return this._officeNumber; }
}
```

**절차**

1. 소스 클래스의 각 public 메서드에 대응하는 메서드들을 타깃 클래스에 생성
2. 소스 클래스의 메서드를 사용하는 코드를 모두 타깃 클래스의 위임 메서드를 사용하도록 수정 (수정마다 테스트)
3. 소스 클래스의 메서드와 필드를 모두 타깃 클래스로 옮기기 (이동마다 테스트)
4. 소스 클래스를 삭제

## 위임 숨기기

`캡슐화는 모듈들이 시스템의 다른 부분에 대해 알아야 할 내용을 줄여준다.`

`인터페이스와의 의존성을 없애려면 위임 메서드를 만들어서 위임 객체의 존재를 숨기자.`

- 반대 리팩터링 : 중개자 제거하기

**개요**

Before

```javascript
manager = aPerson.department.manager;
```

After

```javascript
manager = aPerson.manager;

class Person {
  get manager() { return this.department.manager; }
}
```

**절차**

1. 위임 객체의 각 메서드에 해당하는 위임 메서드를 서버에 생성
2. 클라이언트가 서버를 호출하도록 수정
3. 서버로부터 위임 객체를 얻는 접근자 제거
4. 테스트

**example**

```javascript
manager = aPerson.manager;
```

```javascript
class Person {
    constructor(name) { 
        this._name = name;
    }
    get name() { return this._name; }
    get manager() { return this._department.manager; } // 부서 클래스를 숨기고 위임 메서드 생성
    set department(arg) { this._department = arg; }
}
```

```javascript
class Department {
    get chargeCode() { return this._chargeCode; }
    set chargeCode(arg) { this._chargeCode = arg; }
    get manager() { return this._manager; }
    set manager(arg) { this._manager = arg; }
}
```

## 중개자 제거하기

`중개자 역할로 전략하여 단순히 전달만 하는 클래스(위임 메서드들로 쌓인)는 차라리 위임 객체를 직접 호출하게 하자.`

`위임 숨기기나 중개자 제거하기를 적당히 섞어 상황에 맞게 처리하자.`

- 반대 리팩터링 : 위임 숨기기

**개요**

Before

```javascript
manager = aPerson.manager;

class Person {
  get manager() { return this.department.manager; }
}
```

After

```javascript
manager = aPerson.department.manager;
```

**절차**

1. 위임 객체를 얻는 Getter 생성
2. 위임 메서드를 호출하는 코드를 Getter 로 수정
3. 위임 메서드 삭제

## 알고리즘 교체하기

`더 간명한 방법을 찾으면 복잡한 기존 코드를 간명한 방식으로 고치자.`

`알고리즘 교체를 위해 반드시 메서드를 가능한 잘게 나누자.`

**개요**

Before

```javascript
function foundPerson(people) {
    for (let i = 0; i < people.length; i++) {
        if (people[i] === 'Don') {
            return 'Don';
        }
        if (people[i] === 'John') {
            return 'John';
        }
        if (people[i] === 'Kent') {
            return 'Kent';
        }
    }

    return "";
}
```

After

```javascript
function foundPerson(people) {
    const candidates = ['Don', 'John', 'Kent'];
    return people.find((p) => candidates.includes(p) || "");
}
```

**절차**

1. 교체할 코드를 하나의 함수에 모으기
2. 이 함수의 동작 검증 테스트 만들기
3. 대체 알고리즘 준비
4. 정적 검사 수행
5. 기존 알고리즘과 새 알고리즘의 결과를 비교하는 테스트 수행
   - if 결과가 같다면 리팩터링 종료
   - else 기존 알고리즘을 참고해서 새 알고리즘 테스트 및 디버깅







