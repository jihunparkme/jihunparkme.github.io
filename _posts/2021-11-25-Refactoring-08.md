---
layout: post
title: 기능 이동 Refactoring
summary: Chapter 8. 기능 이동
categories: (Book)Refactoring
featured-img: refactoring
# mathjax: true
---

# Refactoring

# Chapter 8. 기능 이동

- 요소를 다른 컨텍스트(class, module.. )로 옮기는 일도 리팩터링의 중요한 축이다.

## 함수 옮기기

`모듈성을 높이기 위해 요소들을 이리저리 옮겨야 할 수 있다.`

`모듈성을 높이려면 서로 연관된 요소들을 함께 묶고, 요소 사이의 연결 관계를 쉽게 찾고 이해할 수 있도록 해야 한다.`

**개요**

Before

```javascript
class Account {
    get bankCharge() {
        //...
    }

    get overdraftCharge() {
        //...
    }
}
```

After

```javascript
class Account {
    get bankCharge() {
        //...
    }
}

class AccountType {
    overdraftCharge(daysOverdrawn) {
        //...
    }
}
```

**절차**

1. 선택한 함수가 있는 현재 클래스에서 함께 옮길 요소가 있는지 살펴보자.
   - 외부 영향이 적은 함수부터 옮기자.
   - 하위 함수 -> 고수준 함수에 인라인 -> 고수준 함수 옮기기 -> 개별 함수로 다시 추출
2. 선택한 함수가 다형 메서드인지 확인
   - 슈퍼클래스, 서브클래스에 같은 메서드가 선언되어 있는지 고려
3. 선택한 함수를 타깃 클래스로 `복사`
   - 함수 본문에서 클래스 요소를 사용할 경우 매개변수로 넘기거나 클래스 자체를 참조로 넘기자.
4. 정적 분석 수행
5. 소스 클래스에서 타깃 함수를 참조할 방법 찾아 반영
6. 소스 함수를 타깃 함수의 위임 함수가 되도록 수정
7. 테스트
8. 소스 함수 인라인 고민

## 필드 옮기기

`프로그램의 진짜 힘은 데이터 구조에서 나온다.`

`데이터 구조가 적절하지 않음을 깨달았다면 바로 수정하자.`

`한 클래스를 변경하려고 할 때, 다른 클래스의 필드까지 변경해야만 한다면 필드의 위치가 잘못되었다는 신호다.`

**개요**

Before

```javascript
class Customer {
    constructor(name, discountRate) {
        this._name = name;
        this._discountRate = discountRate; //이동할 필드
        this._contract = new CustomerContract(dateToday());
    }
    get discountRate() { return this._discountRate; } // 1. 캡슐화
    becomePreferred() { this._discountRate += 0.03; ... }
    applyDiscount(amount) { return amount.subtract(amount.multiply(this._discountRate)); }
}

class CustomerContract {
    constructor(startDate) {
        this._startDate = startDate;
    }
}
```

After

```javascript
class Customer {
  constructor(name, discountRate) {
    this._name = name;
    this._contract = new CustomerContract(dateToday());
    this._setDiscountRate(discountRate);
  }
  get discountRate() { return this._contract.discountRate; } //5. 소스 클래스에서 타깃 클래스 참조
  _setDiscountRate(aNumber) { this._contract.discountRate = aNumber; }
  becomePreferred() { this._setDiscountRate(this.discountRate + 0.03); ... }
  applyDiscount(amount) { return amount.subtract(amount.multiply(this.discountRate)); }
}

class CustomerContract {
    // 3. 타깃 클래스 필드와 Getter/Setter
    constructor(startDate, discountRate) {
        this._startDate = startDate;
        this._discountRate = discountRate;
    }
    get discountRate() { return this._discountRate; }
    set discountRate(arg) { this._discountRate = arg; }
}
```

**절차**

1. 필드가 캡슐화되어 있지 않다면 캡슐화하자.
   - 캡슐화를 하면 필드 옮기기 리팩터링이 수월해진다.
2. 테스트
3. 타깃 클래스에 필드와 Getter/Setter 생성
4. 정적 검사 수행
5. 소스 클래스에서 타깃 클래스를 참조할 수 있는지 확인
6. 접근자들이 타깃 클래스를 사용하도록 수정
7. 테스트
8. 소스 클래스 제거
9. 테스트

## 문장을 함수로 옮기기

`특정 함수 앞, 뒤에 똑같은 코드가 추가로 실행되면 반복되는 부분을 피호출 함수로 합치자.`

`만일 피호출 함수에서 동작을 여러 변형들로 나눠야 한다면 반대 리팩터링을 적용하자. `

- 반대 리팩터링 : 문장을 호출한 곳으로 옮기기

**개요**

Before

```javascript
result.push(`<p>제목: ${person.photo.title}</p>`);
result.concat(photoData(person.photo));

function photoData(aPhoto) {
    return [
        `<p>위치: ${aPhoto.location}</p>`,
        `<p>날짜: ${aPhoto.date.toDateString()}</p>`,
    ];
}
```

After

```javascript
result.concat(photoData(person.photo));

function photoData(aPhoto) {
    return [
        `<p>제목: ${aPhoto.title}</p>`,
        `<p>위치: ${aPhoto.location}</p>`,
        `<p>날짜: ${aPhoto.date.toDateString()}</p>`,
    ];
}
```

**절차**

1. 반복 코드를 함수 호출 부분 근처로 옮기기(문장 슬라이드하기)
2. 타깃 함수 호출 코드가 한 곳뿐이라면, 단순히 해당 코드를 잘라내어 피호출 함수로 복사 및 테스트
3. 호출자가 둘 이상이라면 호출자 중 하나를 택하여 `반복 코드와 호출문을 함께 함수 추출하기` 진행
4. 다른 호출자가 (3)에서 추출한 함수를 사용하도록 수정 및 테스트
5. 원래 함수를 새로운 함수 안으로 인라인 후 원래 함수 제거
6. 새로운 함수 이름 수정

## 문장을 호출한 곳으로 옮기기

`여러 곳에서 사용하던 기능이 일부 호출자에게 다르게 동작하도록 바뀌어야 할 경우 적용`

- 반대 리팩터링 : 문장을 함수로 옮기기

**개요**

Before

```javascript
emitPhotoData(outStream, person.photo);

function emitPhotoData(outStream, photo) {
    outStream.write(`<p>제목: ${photo.title}</p>\n`);
    outStream.write(`<p>위치: ${photo.location}</p>\n`);
}
```

After

```javascript
emitPhotoData(outStream, person.photo);
outStream.write(`<p>위치: ${person.photo.location}</p>`);

function emitPhotoData(outStream, photo) {
    outStream.write(`<p>제목: ${photo.title}</p>`);
}
```

**절차** (각 단계별 테스트)

1. 호출자가 적을 경우 달라지는 로직(들)을 피호출 함수에서 잘라내어 호출자(들)로 복사
2. 호출자가 많거나 복잡한 상황에서는, 이동하지 않을 코드를 함수로 추출한 후 임시 이름으로 적용
3. 호출자 코드에 있던 원래 함수 인라인
4. 원래 함수 삭제
5. 추출된 함수의 이름 수정

## 인라인 코드를 함수 호출로 바뀌기

`함수의 이름이 코드의 목적을 말해주므로 코드 이해가 쉬워진다.`

`함수는 중복을 없애는 데도 효과적`

`함수 이름이 말이 되지 않는다면 함수 이름이 적절하지 않거나, 그 함수 목적이 인라인 코드의 목적과 다르기 때문일 것이다.`

`인라인 코드를 대체할 함수를 새로 만들어야 한다면 함수 추출하기를 적용하자.`

**개요**

Before

```javascript
let appliesToMass = false;
for (const s of states) {
    if (s === 'MA') { appliesToMass = true; }
}
```

After

```javascript
let appliesToMass = states.includes('MA');
```

**절차**

1. 인라인 코드를 함수 호출로 대체
2. 테스트

## 문장 슬라이드하기

`하나의 데이터 구조를 이용하는 문장들은 모여 있어야 좋다.`

`변수를 처음 사용할 때 선언하는 스타일을 선호`

`슬라이드할 코드 조각과 건너뛸 코드 중 어느 한쪽이 다른 쪽에서 참조하는 데이터를 수정한다면 슬라이드는 불가하다.`

- 상태 갱신에 신경써야 할 부분이 많으므로 상태 갱신 코드를 최대한 제거하자.

**개요**

Before

```javascript
const pricingPlan = retrievePricingPlan();
const order = retrieveOrder();
let charge;
const chargePerUnit = pricingPlan.unit; //이동할 조각 코드
```

After

```javascript
const pricingPlan = retrievePricingPlan();
const chargePerUnit = pricingPlan.unit;
const order = retrieveOrder();
let charge;
```

**절차**

1. 코드 조각을 이동할 목표 위치 찾기
   - 조각을 모으고 나면 동작이 달라지는 코드가 있는지 살피자.
   - 아래와 같은 간섭이 있다면 이 리팩터링을 포기하자..
     - 코드 조각에서 참조하는 요소를 선언하는 문장 앞으로 이동 불가
     - 코드 조각을 참조하는 요소 뒤로 이동 불가
     - 코드 조각에서 참조하는 요소를 수정하는 문장을 건너뛰어 이동 불가
     - 코드 조각이 수정하는 요소를 참조하는 요소를 건너뛰어 이동 불가
2. 코드 조각을 원래 위치에서 잘라내어 목표 위치에 붙여 넣자
3. 테스트

## 반복문 쪼개기

`하나의 반복문이 두 가지 일을 수행한다면, 각각의 반복문으로 분리하여 수정할 동작 하나만 이해하도록 해보자.`

`최적화는 리팩터링을 마친 이후에 수행하자`

**개요**

Before

```javascript
let averageAge = 0;
let totalSalary = 0;
for (const p of people) {
    averageAge += p.age;
    totalSalary += p.salary;
}
averageAge = averageAge / people.length;
```

After

```javascript
let totalSalary = 0;
for (const p of people) {
    totalSalary += p.salary;
}

let averageAge = 0;
for (const p of people) {
    averageAge += p.age;
}
averageAge = averageAge / people.length;
```

**절차**

1. 반복문을 복제해 두 개로 만들기
2. 반복문이 중복되서 생기는 사이드 이펙트를 파악해 제거
3. 테스트
4. 각 반복문을 함수로 추출할지 고민해보기

**Example**

- 함수 추출과 반복문 파이프라인으로 바꾸기를 적용하면 더 좋겠다.

```javascript
function totalSalary() {
    return people.reduce((total, p) => total + p.salary, 0);
}

function youngestAge() {
    return Math.min(...people.map((p) => p.age));
}

function example() {
    return `최연소: ${youngestAge()}, 총 급여: ${totalSalary()}`;
}
```

## 반복문을 파이프라인으로 바꾸기

`객체가 파이프라인을 따라 흐르며 어떻게 처리되는지를 읽을 수 있다.`

- `filter`는 함수를 사용해 입력 컬렉션을 필터링해 부분집합을 만들고, `map`은 또 다른 함수를 사용해 입력 컬렉션의 각 원소를 변환한다.

**개요**

Before

```javascript
function acquireData(input) {
    const lines = input.split('\n');
    let firstLine = true; 
    const result = [];
    for (const line of lines) {
        if (firstLine) { //.1
            firstLine = false;
            continue;
        }
        if (line.trim() === '') { //.2
            continue;
        }
        const record = line.split(','); //.3
        if (record[1].trim() === 'India') { //.4
            result.push({ city: record[0].trim(), phone: record[2].trim() }); //.5
        }
    }

    return result;
}
```

After

```javascript
function acquireData(input) {
    const lines = input.split('\n');
    return lines
        .slice(1) //.1
        .filter((line) => line.trim !== '') //.2
        .map((line) => line.split(',')) //.3
        .filter((fields) => fields[1].trim() === 'India') //.4
        .map((fields) => ({ city: fields[0].trim(), phone: fields[2].trim() })); //.5
}
```

**절차**

1. 반복문에서 사용하는 컬렉션을 가리키는 변수 만들기
2. 반복문의 첫 줄부터 각 단위 행위를 적절한 컬렉션 파이프라인 연산으로 대체하기
3. 반복문 지우기

## 98R

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
