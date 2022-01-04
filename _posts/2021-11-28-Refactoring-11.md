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

## 151R

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

명칭

**개요**

Before

```javascript

```

After

```javascript

```

**절차**
