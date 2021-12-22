---
layout: post
title: 기본적인 리펙터링 Refactoring
summary: Chapter 6.기본적인 리펙터링
categories: (Book)Refactoring
featured-img: refactoring
# mathjax: true
---

# Refactoring

## 리팩터링 전에 테스트 구축하기

- 모든 테스트를 완전히 자동화하고 그 결과까지 스스로 검사하게 만들자.
- 실패해야 할 상황에서는 반드시 실패하게 만들자.
- 문제가 생길 가능성이 있는 경계 조건을 생각해보고 그 부분을 집중적으로 테스트하자.
- 어차피 모든 버그를 잡아낼 수는 없다고 생각하여 테스트를 작성하지 않는다면 대다수의 버그를 잡을 수 있는 기회를 날리는 셈이다.
- 너무 많은 테스트는 의욕을 떨어지게 만들 수 있다. 따라서 위험한 부분에 집중하자. 처리 과정이 복잡하거나 함수에서 오류가 생길만한 부분을 찾아보자.
- 버그 리포트를 받으면 가장 먼저 그 버그를 드러내는 단위 테스트부터 작성하자.
- 누군가 결함을 심으면 테스트가 발견할 수 있다는 믿음을 기준으로 테스트 코드를 작성하자.

# Chapter 6. 기본적인 리팩터링

## 함수 추출하기

`목적과 구현을 분리하는 방식`

- 반대 리팩터링 : 함수 인라인하기

**개요**

Before

```javascript
function printOwing(invoice) {
    printBanner();

    let outstanding = calculatorOutstanding();

    // 세부 사항 출력
    console.log(`고객명: ${invoice.customer}`);
    console.log(`채무액: ${outstanding}`);
}
```

After

```javascript
function printOwing(invoice) {
    printBanner();
    let outstanding = calculatorOutstanding();
    printDetails(outstanding);

    function printDetails(outstanding) {
        console.log(`고객명: ${invoice.customer}`);
        console.log(`채무액: ${outstanding}`);
    }
}
```

**절차**

1. 함수를 새로 만들고 목적(무엇을 하는지)을 잘 드러내는 이름 붙이기.
2. 추출할 코드를 새 함수에 복사
3. 참조하는 변수는 매개변수로 전달
   - 원본 함수의 지역 변수
   - 추출한 함수의 유효범위를 벗어나는 변수
4. 추출한 코드 부분을 새로 만든 함수를 호출하는 문으로 수정
5. 테스트
6. 유사한 코드 확인

## 함수 인라인하기

`함수 본문이 이름만큼 명확한 경우, 함수 코드를 이름만큼 깔끔하게 리팩터링할 경우`

- 반대 리팩터링 : 함수 추출하기

**개요**

Before

```javascript
function raiting(aDriver) { return moreThanFiveLateDeliveries(aDriver) ? 2 : 1; }
function moreThanFiveLateDeliveries(aDriver) { return aDriver.numberOfLaterDeliveries > 5; }
```

After

```javascript
function raiting(aDriver) {  return aDriver.numberOfLaterDeliveries > 5 ? 2 : 1; }
```

**절차**

1. 다형 메서드인지 확인
   - 서브클래스에서 오버라이드하는 메서드는 인라인 금지
2. 인라인할 함수를 호출하는 곳을 모두 찾기
3. 각 호출문을 함수 본문으로 교체
4. 하나씩 교체할 때마다 테스트
5. 함수 정의 삭제

## 변수 추출하기

`표현식이 복잡하여 이해하기 어려울 경우 지역 변수를 활용하여 표현식을 관리`

- 디버거 breakpoint를 지정하거나 상태 출력 문장을 추가하면 디버깅에 도움이 된다.
- 문맥을 고려하여 현재 선언된 함수보다 더 넓은 문맥에서까지의 의미가 된다면 함수로 추출 권장

- 반대 리팩터링 : 변수 인라인하기

**개요**

Before

```javascript
function price(order) {
    // 가격(price) = 기본 가격 - 수량 할인 + 배송비
    return (
        order.quantity * order.itemPrice -
        Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
        Math.min(order.quantity * order.itemPrice * 0.1, 0.05)
    );
}
```

After

```javascript
function price(order) {
    const basePrice = order.quantity * order.itemPrice;
    const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
    const shipping = Math.min(basePrice * 0.1, 100);

    return basePrice - quantityDiscount + shipping;
}
```

**절차**

1. 추출할 표현식에 사이드이펙트가 없는지 확인
2. 불변 변수를 하나 선언 후 이름을 붙일 표현식의 복제본 대입해보기
   - 함수가 클래스 전체에 영향을 줄 떄는 변수가 아닌 메서드로 추출
3. 원본 표현식을 새로 만든 변수로 교체
4. 테스트
5. 표현식을 여러 곳에서 사용할 경우 각각을 새로 만든 변수로 교체

## 변수 인라인하기

`변수명이 원래 표현식과 다를 바 없을 때`

- 반대 리팩터링 : 변수 추출하기

**개요**

Before

```javascript
((anOrder) => {
    let basePrice = anOrder.basePrice;
    return basePrice > 1000;
})(anOrder);
```

After

```javascript
((anOrder) => {
    return anOrder.basePrice > 1000;
})(anOrder);
```

**절차**

1. 인라인할 표현식에 사이드 이펙트가 없는지 확인
2. 상수인지 확인하고 상수로 수정 후 테스트
   - 이 경우 변수에 값이 단 한 번만 대입되는지 확인 가능
3. 변수를 표현식으로 교체
4. 테스트
5. 변수를 사용하는 부분 모두 교체 시까지 이 과정 반복
6. 변수 선언문과 대입문 지우기
7. 테스트

## 함수 선언 바꾸기

`호출문만 보고도 무슨 일을 하는지 파악할 수 있도록 함수 이름을 좋게 만들자.`

- 주석을 이용해 함수의 목적을 설명해보면 좋은 이름이 떠오를 것이다.

다른 이름 : 함수 이름 바꾸기, 매개변수 바꾸기

**개요**

간단한 절차

```javascript
// Before
function circum(radius) {}

// After
function circumference(radius) {}
```

마이그레이션 절차

```javascript
// Before
function circum(radius) {
    return 2 * Math.PI * radius;
}

// After
function circum(radius) {
    return circumference(radius);
}

function circumference(radius) {
    return 2 * Math.PI * radius;
}
```

**절차**

함수 이름 바꾸기, 매개변수 바꾸기에 모두 적용

마이그레이션 절차의 복잡도에 따라 **간단한 절차**와 **마이그레이션 절차**로 구분지어 따름

*간단한 절차*

1. 함수 본문에 제거 대상 매개변수를 참조하는 곳이 없는지 확인
2. 메서드 선언 형태 변경
3. 기존 메서드 선언을 참조하는 부분을 바뀐 형태로 수정
4. 테스트

*마이그레이션 절차* 

(간단한 절차 적용 문제 발생 시)

1. 함수 본문 리팩터링
   - 함수/변수 추출 등
2. 함수 본문에서 새로운 함수로 추출
3. 추출한 함수에 매개변수 추가 시 간단한 절차를 따라 추가
4. 어서션을 추가하여 새로 추가한 매개변수를 실제 사용하는지 확인 (javascript)
5. 테스트
6. 기존 함수 인라인 처리
7. 임시 이름을 붙인 새 함수를 원래 이름으로 수정
8. 테스트

## 변수 캡슐화하기

`자주 사용하는 가변 데이터에 대한 결합도가 높아지는 막기 위해, 데이터의 유효범위가 넓을수록 캡슐화하자.`

- 데이터 변경 전 검증이나 변경 후 추가 로직을 쉽게 끼워넣을 수 있다.

**개요**

Before

```javascript
let defaultOwner = { firstName: '마틴', lastName: '파울러'};
```

After

```javascript
let defaultOwnerData = { firstName: '마틴', lastName: '파울러' };
export function defaultOwner() { return defaultOwnerData; }
export function setDefaultOwner(arg) { defaultOwnerData = arg; }
```

**절차**

1. 변수 접근/갱신을 전담하는 Getter/Setter 만들기
2. 정적 검사 수행
3. 변수를 직접 참조하던 부분을 적절한 캡슐화 함수 호출로 변경 (테스트 병행)
4. 변수의 접근 범위 제한
5. 테스트
6. 변수 값이 레코드일 경우 레코드 캡슐화 적용 고려

`캡슐화할 데이터를 사용하는 방식과 어떻게 변경할지에 따라 캡슐화의 구체적인 대상과 방법을 정하자.`

```javascript
let defaultOwnerData = { firstName: '마틴', lastName: '파울러' };
export function defaultOwner() { return new Person(defaultOwnerData); }
export function setDefaultOwner(arg) { defaultOwnerData = arg; }

class Person {
    constructor(data) {
        this._lastName = data.lastName;
        this._firstName = data.firstName;
    }

    get lastName() { return this._lastName; }

    get firstName() { return this._firstName; }
}
```



## 변수 이름 바꾸기

`변수는 프로그래머가 하려는 일에 관해 많은 것을 설명해준다.`

**개요**

Before

```javascript
let a = height * width;
```

After

```javascript
let area = height * width;
```

**절차**

1. 폭넓게 쓰이는 변수라면 변수 캡슐화 고려하기
2. 변경할 변수를 참조하는 곳을 하나씩 변경하기
   - 해당 함수에서만 유효한 변수
3. 테스트

## 매개변수 객체 만들기

`데이터 뭉치를 데이터 구조로 묶으면 데이터 사이의 관계가 명확해진다.`

- +, 매개변수 수 감소, 원소 참조의 일관성
- 데이터 구조를 클래스로 만들어두면 관련 동작들을 해당 클래스로 옮길 수 있다.

**개요**

Before

```javascript
function amountInvoiced(startDate, endDate) {}
function amountReceived(startDate, endDate) {}
function amountOverdue(startDate, endDate) {}
```

After

```javascript
function amountInvoiced(aDateRange) {}
function amountReceived(aDateRange) {}
function amountOverdue(aDateRange) {}
```

**절차**

1. 데이터 구조 만들기
2. 함수 선언 바꾸기로 매개변수에 새 데이터 구조 추가
3. 함수 호출 시 인스턴스 수정
4. 기존 매개변수를 사용하던 코드를 새 데이터 구조를 사용하도록 수정
5. 기존 매개변수 제거
6. 각 단계별 테스트

## 여러 함수를 클래스로 묶기

`클래스로 묶으면 함수들이 공유하는 공통 환경을 더 명확하게 표현`

`각 함수에 전달되는 인수를 줄여 객체 안에서의 함수 호출을 간결하게`

**개요**

Before

```javascript
function base(aReading) {}
function taxableCharge(aReading) {}
function calculateBaseChange(aReading) {}
```

After

```javascript
class Reading {
    base() {}
    taxableCharge() {}
    calculateBaseChange() {}
}
```

**절차**

1. 함수들이 공유하는 공통 데이터 레코드 캡슐화
2. 공통 레코드를 사용하는 함수 각각을 새 클래스로 옮기기
   - 멤버 변수는 함수 호출문의 인수에서 제거
3. 데이터를 조작하는 로직들은 함수로 추출하여 새 클래스로 옮기기

## 여러 함수를 변환 함수로 묶기

`변환 함수는 원본 데이터를 입력받아서 필요 정보를 모두 두출한 후, 각 출력 데이터 필드에 넣어 반환한다.`

`검색과 갱신을 일관된 장소에서 처리할 수 있고, 로직 중복도 막을 수 있다.`

`원본 데이터가 코드 안에서 갱신될 때는 클래스로 묶기를 적용하자.`

- 데이터 일관성을 지켜야 한다면(원본 데이터 변경을 막기 위한 목적이 있다면) 클래스 묶기를 적용하자.

**개요**

Before

```javascript
function base(aReading) {}
function taxableCharge(aReading) {}
```

After

```javascript
function enrichReading(argReading) {
    const aReading = _.cloneDeep(argReading);
    aReading.baseCharge = base(aReading);
    aReading.taxableCharge = taxableCharge(aReading);
    // 원본 데이터는 변경면 안됨. (원본 데이터 확인 테스트 작성 필요)
    return aReading;
}
```

**절차**

1. 입력된 값을 그대로 반환하는 변환 함수 생성
   - 깊은 복사 처리
2. 묶을 함수의 본문 코드를 변환 함수로 옮기고, 처리 결과를 새 필드로 기록
   - 로직이 복잡하면 함수 추출 먼저 적용
3. 테스트
4. 나머지 관련 함수도 적용

## 단계 쪼개기

`서로 다른 두 대상을 한꺼번에 다루는 경우 각각을 별개의 모듈로 나누자.`

`동작을 두 단계로 쪼개는 방법`

**개요**

Before

```javascript
const orderData = orderString.split(/\s+/);
const productPrice = priceList[orderData[0].split('-')[1]];
const orderPrice = parseInt(orderData[1]) * productPrice;
```

After

```javascript
const orderRecord = parseOrder(order)
const orderPrice = parseInt(orderData[1]) * productPrice;

function parseOrder(aString) {
    const values = aString.split(/\s+/);
    return ({
        productID: values[0].split('-')[1]
        quantity: parseInt(values[1])
	})
}
function price(order, priceList) {
    return order.quantity * priceList[order.productID]
}
```

**절차**

1. 두 번째 단계 처리 코드를 독립 함수로 추출
2. 테스트
3. 중간 데이터 구조(ex. Class)를 만들어 전 단계에서 추출한 함수의 인수로 추가
4. 테스트
5. 추출한 두 번째 단계 함수의 매개변수를 검토
   - 첫 번째 단계에 사용된 매개변수는 중간 데이터 구조(ex. Class)로 옮기기
6. 첫 번째 단계 코드를 함수로 추출하면서 중간 데이터 구조 반환

**Example**

```javascript
function priceOrder(product, quantity, shippingMethod) {
    const priceData = calculatePricingData(product, quantity);
    return applyShipping(priceData, shippingMethod, discount);
}

function calculatePricingData(product, quantity) {
    const basePrice = product.basePrice * quantity;
    const discount = Math.max(quantity - product.discountThreshold, 0) 
		    * product.basePrice * product.discountRate;
    return { basePrice: basePrice, quantity: quantity, discount: discount };
}

function applyShipping(priceData, shippingMethod) {
    const shippingPerCase = (priceData.basePrice > shippingMethod.discountThreshold) ? 
          	 shippingMethod.discountedFee : shippingMethod.feePerCase;
    const shippingCost = priceData.quantity * shippingPerCase;
    return priceData.basePrice - priceData.discount + shippingCost;
}
```
