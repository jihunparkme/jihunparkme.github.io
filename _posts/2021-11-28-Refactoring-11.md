---
layout: post
title: API Refactoring
summary: Chapter 11. API 리팩터링
categories: (Book)Refactoring
featured-img: refactoring
# mathjax: true
---

# Refactoring

# Chapter 11. API 리팩터링

`API를 이해하고 사용하기 쉽게 만드는 일은 중요한 동시에 어렵기도 하다.`

- 좋은 API는 데이터를 갱신하는 함수와 조회만 하는 함수를 명확히 구분한다.

`개선 방법을 깨달을 때마다 리팩터링을 해보자.`

## 질의 함수와 변경 함수 분리하기

`겉보기 사이드 이펙트가 있는 함수와 없는 함수를 명확히 구분하자.`

`질의(읽기) 함수는 모두 사이드 이펙트가 없어야 한다는(명령-질의 분리) 규칙을 따르자.`

`겉보기 사이드 이펙트 없이 어떤 순서로 호출하든 모든 호출에 항상 똑같은 값이 반환되어야 한다.`

**개요**

Before

```javascript
function getTotalOutstandingAndSendBill() {
    const result = customer.invoices.reduce((total, each) => each.amount + total, 0,);
    sendBill();
    return result;
}

const total = getTotalOutstandingAndSendBill();
```

After

```javascript
function totalOutstanding() {
    return customer.invoices.reduce((total, each) => each.amount + total, 0);
}
function sendBill() {
    emailGateway.send(formatBill(customer));
}

const total = totalOutstanding();
sendBill();
```

**절차**

1. 대상 함수를 복제하고 질의 목적에 충실한 이름 짓기
   - 무엇을 반환하는지 찾아보자
2. 새 질의 함수에서 사이드 이펙트 제거하기
3. 정적 검사 수행
4. 기존 변경 함수를 질의 함수로 수정하고, 바로 아래 줄에 원래 함수 호출하기
5. 원래 함수에서 질의 관련 코드 제거하기
6. 테스트

참고 : 중복 코드가 많이 보인다면 변경 함수에서 질의 함수를 사용하도록 수정해보자.

## 함수 매개변수화하기

`두 함수의 로직이 유사하고 리터럴 값만 다르다면, 다른 값만 매개변수로 받아 처리하는 함수 하나로 합치자.`

**개요**

Before

```javascript
function tenPercentRaise(aPerson) {
    aPerson.salary = aPerson.salary.multiply(1.1);
}
function fivePercentRaise(aPerson) {
    aPerson.salary = aPerson.salary.multiply(1.05);
}
```

After

```javascript
function tenPercentRaise(aPerson, factor) {
    aPerson.salary = aPerson.salary.multiply(1 + factor);
}
```

**절차**

1. 비슷한 함수 중 하나 선택
2. `함수 선언 바꾸기`로 리터럴들을 매개변수로 추가
3. 이 함수를 호출하는 곳 모두에 `적절한 리터럴` 값 추가
4. 테스트
5. 함수 본문에서 매개변수로 받은 값을 사용하도록 수정
6. 기존 코드를 매개변수화된 함수를 호출하도록 수정

**Example**

```javascript
/**
 * Before
 */
function baseCharge(usage) {
    if (usage < 0) return usd(0);
    const amount = bottomBand(usage) * 0.03 + middleBand(usage) * 0.05 + topBand(usage) * 0.07;
    return usd(amount);
}
function bottomBand(usage) {
    return Math.min(usage, 100);
}
function middleBand(usage) { //.1
    return usage > 100 ? Math.min(usage, 200) - 100 : 0; //.5
}
function topBand(usage) {
    return usage > 200 ? usage - 200 : 0;
}

/**
 * After
 */
function withinBand(usage, bottom, top) { //.2
    return usage > bottom ? Math.min(usage, top) - bottom : 0; //.5
}
function baseCharge(usage) {
    if (usage < 0) return usd(0);
    const amount =
          withinBand(usage, 0, 100) * 0.03 + //.6
          withinBand(usage, 100, 200) * 0.05 + //.3
          withinBand(usage, 200, Infinity) * 0.07; //.6
    return usd(amount);
}
```

## 플래그 인수 제거하기

`플래그 인수를 사용하면 어떻게 호출해야 하는지 이해하기가 어려워 진다.`

- 플래그 인수 : 실행할 로직을 선택하기 위해 전달하는 인수

`플래그 인수 대신 특정한 기능 하나만 수행하는 명시적인 함수를 제공하자.`

**개요**

Before

```javascript
function setDimension(name, value) {
    if (name === 'height') {
        this._height = value;
        return;
    }
    if (name === 'width') {
        this._width = value;
        return;
    }
}

setDimension("height", 130)
setDimension("width", 50)
```

After

```javascript
function setHeight(value) { this._height = value; }
function setWidth(value) { this._width = value; }

setHeight(130)
setWidth(50)
```

**절차**

1. 플래그 인수에 대응하는 명시적 함수 생성
2. 기존 코드를 명시적 함수를 호출하도록 수정

**참고.** 매개변수를 까다로운 방식으로 사용한다면 래핑 함수를 생각해보자.

```javascript
function rushDeliveryDate(anOrder) {return deliveryDate(anOrder, true);}
function regularDeliveryDate(anOrder) {return deliveryDate(anOrder, false);}
```

## 객체 통째로 넘기기

`레코드를 통째로 넘기면 변화에 대응하기 쉽다.`

**개요**

Before

```javascript
class HeatingPlan {
    withinRange(bottom, top) {
        return (bottom >= this._temperatureRange.low && top >= this._temperatureRange.high);
    }
}

const low = aRoom.daysTempRange.low;
const high = aRoom.daysTempRange.high;
if (!aPlan.withinRange(low, high)) { alerts.push('방 온도가 지정 범위를 벗어났습니다.'); }
```

After

```javascript
class HeatingPlan {
    withinRange(aNumberRange) {
        return (aNumberRange.low >= this._temperatureRange.low && aNumberRange.high >= this._temperatureRange.high);
    }
}

if (!aPlan.withinRange(aRoom.daysTempRange)) { alerts.push('방 온도가 지정 범위를 벗어났습니다.'); }
```

**절차**

1. 매개변수들을 원하는 형태로 받는 빈 함수 만들기
2. 새 함수의 본문은 원래 함수를 호출하고, 새 매개변수와 원래 함수의 매개변수를 매핑
3. 정적 검사 수행
4. 새 함수를 호출하도록 수정
5. 원래 함수를 인라인
6. 새 함수의 이름을 적절히 수정하고 모든 호출자에 반영

**참고.** 추출과 인라인 리팩터링을 이용한 방법

```javascript
class HeatingPlan {
    xxNEWwithinRange(tempRange) { // 함수 추출하기
        const low = tempRange.low; // 입력 매개변수 추출하기
        const high = tempRange.high;
        const isWithinRange = this.withinRange(low, high);
        return isWithinRange;
    }
    withinRange(bottom, top) {
        return (bottom >= this._temperatureRange.low && top >= this._temperatureRange.high);
    }
}

const tempRange = aRoom.daysTempRange;
const isWithinRange = aPlan.xxNEWwithinRange(tempRange);
if (!isWithinRange) {
    alerts.push('방 온도가 지정 범위를 벗어났습니다.');
}
```

## 매개변수를 질의 함수로 바꾸기

`매개변수에서 얻을 수 있는 값을 별도 매개변수로 전달하는 것은 의미가 없다.`

- 함수에 원치 않는 의존성이 생길 경우는 제외.

`대상 함수는 참조 투명(함수에 똑같은 값을 건네 호출하면 항상 똑같이 동작)해야 한다.`

- 반대 리팩터링 : 질의 함수를 매개변수로 바꾸기

**개요**

Before

```javascript
availableVacation(anEmployee, anEmployee.grade);

function availableVacation(anEmployee, grade) {
    // ...
}
```

After

```javascript
availableVacation(anEmployee);

function availableVacation(anEmployee) {
    const grade = anEmployee.grade;
    // ...
}
```

**절차**

1. 필요 시 대상 매개변수의 값을 계산하는 코드를 별도 함수로 추출
2. 함수 본문에서 대상 매개변수를 참조하는 코드를 질의 함수 호출로 수정
3. 함수 선언 바꾸기로 대상 매개변수 없애기

**Example**

```javascript
class Order {
    get finalPrice() {
        const basePrice = this.quantity * this.itemPrice;
        return this.discountedPrice(basePrice); 
    }
    get discountLevel() { return this.quantity > 100 ? 2 : 1; } // 임시 변수를 질의 함수로 바꾸기

    discountedPrice(basePrice) {
        switch (this.discountLevel) { // 매개변수 참조 코드를 함수 호출로 바꾸기
            case 1: return basePrice * 0.95;
            case 2: return basePrice * 0.9;
        }
    }
}
```

## 질의 함수를 매개변수로 바꾸기

`전역 변수를 참조하거나, 제거하길 원하는 원소를 참조한다면 매개변수로 바꾸자.`

`단점이라면 호출자가 함수의 매개변수를 바꾸면 어떤 값을 제공할지 알아내야 한다.`

- 반대 리팩터링 : 매개변수를 질의 함수로 바꾸기

**개요**

Before

```javascript
targetTemperature(aPlan);

function targetTemperature(aPlan) {
    currentTemperature = thermostat.currentTemperature;
    // ...
```

After

```javascript
targetTemperature(aPlan, thermostat.currentTemperature);

function targetTemperature(aPlan, currentTemperature) {
	// ...
```

**절차**

1. `변수 추출하기`로 질의 코드가 매개변수를 사용할 수 있도록 준비
2. 함수 본문 중 해당 질의를 호출하지 않는 코드들을 별도 `메서드로 추출`
3. 새로 만든 `변수를 인라인`하여 제거 
   - 호출 코드만 남겨진다.
4. 원래 함수도 인라인
5. 새 함수의 이름을 원래 함수 이름으로 수정

**Example**

```javascript
class HeatingPlan {
    get targetTemperature(selectedTemperature) { // 매개변수로 사용, 함수 추출하기
        if (selectedTemperature > this._max) return this._max;
        else if (selectedTemperature < this._min) return this._min;
        else return selectedTemperature;
    }
}

if (thePlan.targetTemperature(thermostat.selectedTemperature) > thermostat.currentTemperature) setToHeat();
else if (thePlan.targetTemperature(thermostat.selectedTemperature) < thermostat.currentTemperature) setToCool();
else setOff();
```

## 세터 제거하기

세터 제거하기 리팩터링은 아래 두 경우에 주로 필요하다.

`사람들이 무조건 접근자 메서드를 통해서만 필드를 다루려고 할 때`

`Client 에서 생성 스크립트를 사용해 객체를 생성할 때`

**개요**

Before

```javascript
class Person {
    get name() { return this._name; }
    set name(arg) { this._name = arg; }
    get id() { return this._id; }
    set id(arg) { this._id = arg; }
}
```

After

```javascript
class Person {
    constructor(id) {
        this._id = id;
    }
    get name() { return this._name; }
    set name(arg) { this._name = arg; }
    get id() { return this._id; }
}
```

**절차**

1. 설정해야 할 값을 생성자에 추가 (`함수 선언 바꾸기`)
2. 생성자 밖에서 세터를 호출하는 곳을 찾아서 제거
   - 대신 새로운 생성자를 사용하도록 수정 (이 방법으로도 세터 호출을 대체할 수 없다면 이 리팩터링 취소)
3. 세터 메서드를 인라인으로 (가능하면 해당 필드를 불변으로 만들자)
4. 테스트

## 생성자를 팩터리 함수로 바꾸기

`생성자는 일반 함수에는 없는 제약이 따라붙기도 한다.`

- 생성자를 정의한 클래스 인스턴스 반환
- 서브클래스 인스턴스나 프락시 반환 불가
- 생성자 이름 고정 등..

`팩터리 함수는 생성자 호출뿐만 아니라 다른 무언가로 대체할 수도 있다.`

**개요**

Before

```javascript
loadEngineer = new Employee(document.loadEngineer, 'E');
```

After

```javascript
loadEngineer = createEngineer(document.loadEngineer);
```

**절차**

1. 팩터리 함수 만들기
   - 원래의 생성자 호출
2. 기존 생성자 호출 코드를 팩터리 함수 호출로 수정
3. 매 수정마다 테스트
4. 생성자의 가시 범위가 최소가 되도록 제한

## 함수를 명령으로 바꾸기

`평범한 함수 메커니즘보다 훨씬 유연하게 함수를 제어하고 표현`

`명령 객체 or 명령 : 함수를 캡슐화한 객체(메서드 하나로 구성)`

`명령을 사용하면 서브함수들을 테스트와 디버깅에 활용할 수 있음`

`명령은 가급적 명령보다 더 간단한 방식의 기능을 얻을 수 없는 경우 선택하자.`

- 반대 리팩터링 : 명령을 함수로 바꾸기

**개요**

Before

```javascript
function score(candidate, medicalExam, scoringGuide) {
    let result = 0;
    let healthLevel = 0;
    // ...
}
```

After

```javascript
class Scorer {
    constructor(candidate, medicalExam, scoringGuide) { //.3
        this._candidate = candidate;
        this._medicalExam = medicalExam;
        this._scoringGuide = scoringGuide;
    }
    execute() {
        this._result = 0; // 모든 지역변수를 필드로 바꾸기
        this._healthLevel = 0;
        // ...
    }
}
```

**절차**

1. 대상 함수를 옮길 빈 클래스 만들기
   - 클래스 이름은 함수 이름을 기초
2. 생성한 클래스로 함수 옮기기
3. 함수의 인수들은 명령 필드로 만들어 생성자를 통해 설정할지 고민해보기

## 명령을 함수로 바꾸기

`로직이 크게 복잡하지 않다면 명령 객체의 단점이 커지니 평범한 함수로 바꾸자.`

- 큰 메서드를 여러 작은 메서드로 쪼개고 필드를 이용해 메서드들끼리 정보를 공유하는 정도가 아니라면..

- 반대 리팩터링 : 함수를 명령으로 바꾸기

**개요**

Before

```javascript
class ChargeCalculator { //.7
    constructor(customer, usage, provider) {
        this._customer = customer;
        this._usage = usage;
        this._provider = provider;
    }
    get baseCharge() { return this._customer.baseRate * this._usage; }
    get charge() { return this.baseCharge * this._provider.connectionCharge;}
}

monthCharge = new ChargeCalculator(customer, usage, provider).charge;
```

After

```javascript
function charge(customer, usage, provider) { //.1, 3, 4
    const baseCharge = customer.baseRate * usage; //.2
    return baseCharge * provider.connectionCharge; //.5
}

monthCharge = charge(customer, usage, provider);
```

**절차**

1. 명령 생성, 명령의 실행 메서드 호출 코드를 함께 함수로 추출
2. 명령의 실행 메서드가 호출하는 보조 메서드들을 인라인
3. `함수 선언 바꾸기`를 적용하여 생성자의 매개변수를 명령의 실행 메서드로 옮기기
4. 명령의 실행 메서드에서 참조하는 필드를 매개변수로 수정하기
5. 생성자 호출과 명령의 실행 메서드 호출을 대체 함수 안으로 인라인
6. 테스트
7. `죽은 코드 제거하기`로 명령 클래스 없애기

## 수정된 값 반환하기

`데이터가 수정된다면 그 사실을 명확히 알려주자.`

`어느 함수가 무슨 일을 하는지 쉽게 알 수 있게 해주는 것이 중요하다.`

**개요**

Before

```javascript
let totalAscent = 0;
calculateAscent();

function calculateAscent() {
    for (let i = 1; i < points.length; i++) {
        const verticalChange = points[i].elevation - points[i - 1].elevation;

        totalAscent += verticalChange > 0 ? verticalChange : 0;
    }
}
```

After

```javascript
const totalAscent = calculateAscent(); //.1, 3

function calculateAscent() { //.4
    let result = 0; //.2
    for (let i = 1; i < points.length; i++) {
        const verticalChange = points[i].elevation - points[i - 1].elevation;

        result += verticalChange > 0 ? verticalChange : 0;
    }
    return result; //.1
}
```

**절차 (매 단계 테스트)**

1. 호출자는 함수가 반환하는 수정된 값을 자신의 변수에 저장하기
2. 피호출 함수 안에 반환할 값을 가리키는 새로운 변수 선언하기
3. 계산이 선언과 동시에 이루어지도록 통합하기 (+변수를 불변으로 만들기)
4. 피호출 함수의 변수 이름을 새 역할에 어울리도록 수정하기

## 오류 코드를 예외로 바꾸기

`예외는 프로그래밍 언어에서 제공하는 독립적인 오류 처리 메커니즘이다.`

`예외를 사용하면 오류 코드를 일일이 검사하거나 오류를 식별해 콜스택 위로 던지는 일을 신경쓰지 않아도 된다.`

`예외는 정확히 예상 밖의 동작일 때만 쓰자.`

**개요**

Before

```javascript
if (data) 
    return new ShippingRules(data);
else
    return -23;
```

After

```javascript
if (data)
    return new ShippingRules(data);
else
    throw new OrderProcessingError(-23);
```

**절차 (매 단계 테스트)**

1. 콜스택 상위에 해당 예외를 처리할 예외 핸들러 작성하기
2. 해당 오류 코드를 대체할 예외와 그 밖의 예외를 구분할 식별 방법 찾기
   - 예외를 클래스 기반으로 처리할 수 있다면 서브클래스 만들기
3. 정적 검사 수행하기
4. catch절을 수정하여 직접 처리할 수 있는 예외는 적절히 대처하고, 그렇지 않은 예외는 다시 던지기
5. 오류 코드를 반환하는 곳 모두에서 예외를 던지도록 수정하기
6. 오류 코드를 콜스택 위로 전달하는 코드 모두 제거하기

**Example**

```javascript
class OrderProcessingError extends Error { // 2. 예외를 클래스 기반으로 처리
    constructor(errorCode) {
        super(`주문 처리 오류 ${errorCode}`);
        this.code = errorCode;
    }
    get name() { return 'OrderProcessingError'; }
}

function localShippingRules(country) {
    const data = countryData.shippingRules[country];
    if (data) return new ShippingRules(data);
	else throw new OrderProcessingError(-23); // 5. 오류 코드 대신 예외 클래스 사용
}

function calculateShippingCosts(anOrder) {
    const shippingRules = localShippingRules(anOrder.country);
	// ...
}

try { // 1. 예외 핸들러 작성하기
    calculateShippingCosts(orderData);
} catch (e) {
    if (e instanceof OrderProcessingError) // 4. 예외 클래스를 처리
        errorList.push({order: orderData, errorCode: e.code,});
	else
        throw e;
}
```

## 예외를 사전확인으로 바꾸기

`예외는 '뜻밖의 오류'라는 말 그대로 예외적인 동작에만 사용하자.`

`함수 수행 시 문제가 될 수 있는 조건을 함수 호출 전에 검사하자.`

`예외를 던지는 대신 호출하는 곳에서 조건을 검사하도록 해보자.`

**개요**

Before

```java
private Deque<Resource> avaliable;
private List<Resource> allocated;

public ResourcePool get() {
    Resource result;
    try {
        result = avaliable.pop()
        allocated.add(result);
    } catch (NoSuchElementException e) {
        result = Resource.create();
        allocated.add(result)
    }
    return result;
}
```

After

```java
private Deque<Resource> available;
private List<Resource> allocated;

public ResourcePool get() {
	// 조건 검사 코드 (try, catch 문을 조건절로 이동)
    Resource result = available.isEmpty() ? Resource.create() : available.pop()
	allocated.add(result);
    return result;
}
```

**절차 (매 단계 테스트)**

1. 예외 유발 상황을 검사할 수 있는 조건문 추가
   - catch 블록의 코드를 조건문의 조건절 중 하나로 옮기기
   - 남은 try 블록의 코드를 다른 조건절로 옮기기
2. catch 블록에 어서션을 추가하고 테스트
3. try 문과 catch 블록 제거
4. 테스트
