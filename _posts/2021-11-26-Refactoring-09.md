---
layout: post
title: 데이터 조직화 Refactoring
summary: Chapter 9. 데이터 조직화
categories: (Book)Refactoring
featured-img: refactoring
# mathjax: true
---

# Refactoring

# Chapter 9. 데이터 조직화

- 데이터 구조는 프로그램에서 중요한 역할을 수행한다.

## 변수 쪼개기

`역할이 둘 이상인 변수는 쪼개자.`

`여러 용도로 쓰인 변수는 코드를 읽는 과정에서 커다란 혼란을 주게 된다.`

**개요**

Before

```javascript
let temp = 2 * (height + width);
console.log(temp);
temp = height + width;
console.log(temp);
```

After

```javascript
const perimeter = 2 * (height + width);
console.log(perimeter);
const area = height * width;
console.log(area);
```

**절차**

1. 변수를 선언한 곳과 값을 처음 대입하는 곳에서 `변수 이름을 바꾸기`
   - 총합 계산, 문자열 연결, 스트림 쓰기 등에 흔히 사용되는 수집변수는 제외
2. 가능하면 `불변으로 선언`
3. 이 변수에 두 번째로 값을 대입하는 곳 앞까지의 모든 참조를 `새로운 변수 이름`으로 수정
4. 두 번째 대입 시 변수를 원래 이름으로 다시 선언
5. 테스트
6. 반복

**Example**

```javascript
function distanceTravelled(scenario, time) {
    let result;
    // 첫 번째 힘이 유발한 초기 가속도
    const primaryAcceleration = scenario.primaryForce / scenario.mass; // 1, 2
    let primaryTime = Math.min(time, scenario.delay);
    result = 0.5 * primaryAcceleration * primaryTime * primaryTime; // 3
    let secondaryTime = time - scenario.delay;
    if (secondaryTime > 0) {
        let primaryVelocity = primaryAcceleration * scenario.delay; // 3
        // 두 번째 힘까지 반영된 후의 가속도
        const secondaryAcceleration = (scenario.primaryForce + scenario.secondaryForce) / scenario.mass; // 4 -> 6 (1, 2)
        result += primaryVelocity * secondaryTime + 0.5 * secondaryAcceleration * secondaryTime * secondaryTime; // 3
    }
    return result;
}
```

## 필드 이름 바꾸기

`데이터 구조는 프로그램을 이해하는 데 큰 역할을 한다.`

`데이터는 무슨 일이 벌어지는지 이해하는 열쇠다.`

**개요**

Before

```javascript
class Organization {
  get name() {}
}
```

After

```javascript
class Organization {
  get title() {}
}
```

**절차**

1. 레코드의 유효 범위가 제한적이라면 필드에 접근하는 모든 코드를 수정 후 테스트
   - 유효 범위가 제한적인 레코드는 절차 끝
2. 레코드가 캡슐화되지 않았다면 `레코드 캡슐화`
3. 캡슐화된 객체 안의 private `필드명 변경 후` 그에 맞게 `내부 메서드 수정`
4. 테스트
5. 생성자의 매개변수 중 필드와 이름이 겹치는 게 있다면 `함수 선언 바꾸기`로 변경
6. 접근자 이름 변경

**Example**

```javascript
class Organization { // 2. 캡슐화
    constructor(data) {
        this._title = data.title; // 3. 필드명 변경 후 메서드 수정
        this._country = data._country;
    }
    get title() { return this._title; } // 3.
    set title(aString) { this._title = aString; } // 3.
    get country() { return this._country; }
    set country(aCountryCode) { this._country = aCountryCode; }
}

const organization = new Organization({ // 6. 접근자 이름 변경
    title: '애크미 구스베리',
    country: 'GB',
});
```

## 파생 변수를 질의 함수로 바꾸기

`가변 데이터의 유효 범위를 가능한 좁혀야 한다.`

`값을 쉽게 계산해낼 수 있는 변수들을 모두 제거하자.`

- 새로운 데이터 구조를 생성하는 변형 연산은 예외다.

**개요**

Before

```javascript
get discountedTotal() { return this._discountedTotal; }
set discountedTotal(aNumber) {
    const old = this._discount;
    this._discount = aNumber;
    this._discountTotal += old - aNumber;
}
```

After

```javascript
get discountedTotal() { return this._baseTotal - this._discount; }
set discountedTotal(aNumber) { this._discount = aNumber; }
```

**절차**

1. 변수 값이 갱신되는 지점 찾기
   - 필요 시 `변수 쪼개기`로 각 갱신 지점에서 변수 분리하기
2. 해당 변수의 값을 계산해주는 `함수 만들기`
3. 함수의 계산 결과가 변수의 값과 같은지 테스트
4. 변수를 읽는 코드를 모두 함수 호출로 수정 후 테스트
5. 변수를 선언하고 갱신하는 코드에 `죽은 코드 제거하기` 적용

**Example**

```javascript
class ProductionPlan {
    constructor(production) {
        this._initialProduction = production; // 1. 변수 쪼개기
        this._productionAccumulator = 0; // 1.
        this._adjustments = [];
    }
    get production() { return this._initialProduction + this._productionAccumulator; } // 2. 변수 값 계산
    get calculatedProductionAccumulator() { return this._adjustments.reduce((sum, a) => sum + a.amount, 0); }
    applyAdjustment(anAdjustment) { this._adjustments.push(anAdjustment); }
}
```

## 참조를 값으로 바꾸기

`참조로 다루는 경우는 내부 객체를 그대로 둔 채 객체의 속성만 갱신`

`값으로 다루는 경우 새로운 속성을 담은 객체로 기존 내부 객체를 대체`

`값 객체는 불변이기 때문에 자유롭게 활용하기 좋고, 분산 시스템과 동시성 시스템에서 유용하다.`

- 단, 객체를 공유하고자 한다면 공유 객체를 참조로 다뤄야 한다.

- 반대 리팩터링 : 값을 참조로 바꾸기

**개요**

Before

```javascript
class Product {
    applyDiscount(arg) {
        this._price.amount -= arg;
    }
}
```

After

```javascript
class Product {
    applyDiscount(arg) {
        this._price = new Money(this._price.amount - arg, this._price.currency);
    }
}
```

**절차**

1. 후보 클래스가 불변인지 확인하기 (`불변으로 만들기`)
2. 필드들의 `세터 제거`하기
3. 값 객체의 필드들을 사용하는 `동치성 비교 메서드 만들기`
   - JAVA 에서는 Object.equals(), Object.hashCode() method override.

**Example**

```javascript
/** Person ********************************************/
class Person {
    constructor() { 
        this._telephoneNumber = new TelephoneNumber();
    }
    get officeAreaCode() { return this._telephoneNumber.areaCode; }
    set officeAreaCode(arg) { this._telephoneNumber = new TelephoneNumber(arg, this.officeNumber); } // 1.
    get officeNumber() { return this._telephoneNumber.number; }
    set officeNumber(arg) {  this._telephoneNumber = new TelephoneNumber(this.officeNumber, arg);} // 1.
}
/** TelephoneNumber ********************************************/
class TelephoneNumber {
    constructor(areaCode, number) { // 1. 불변으로 만들기
        this._areaCode = areaCode;
        this._number = number;
    }
    equals(other) { // 3. 동치성 비교
        if (!(other instanceof TelephoneNumber)) { return false; }
        return this.areaCode === other.areaCode && this.number === other.number;
    }
    get areaCode() { return this.areaCode; }
    get number() { return this.number; }
    // 2. 필드 세터 제거
}
```

## 108R

명칭

**개요**

Before

```javascript

```

After

```javascript

```

**절차**

명칭

**개요**

Before

```javascript

```

After

```javascript

```

**절차**

명칭

**개요**

Before

```javascript

```

After

```javascript

```

**절차**

명칭

**개요**

Before

```javascript

```

After

```javascript

```

**절차**
