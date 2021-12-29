---
layout: post
title: 조건부 로직 간소화 Refactoring
summary: Chapter 10. 조건부 로직 간소화
categories: (Book)Refactoring
featured-img: refactoring
# mathjax: true
---

# Refactoring

# Chapter 10. 조건부 로직 간소화

- 조건부 로직은 프로그램을 복잡하게 만드는 주요 원흉이다.
- 조건부 로직을 이해하기 쉽게 바꿔보자.

## 조건문 분해하기

`복잡한 조건부 로직은 프로그램을 복잡하게 만드는 가장 흔한 원횽이다.`

`코드를 부위별로 분해한 후 분해된 코드 덩어리들을 의도를 살린 이름의 함수 호출로 바꾸자`

**개요**

Before

```javascript
if (!aDate.isBefore(plan.summerStart) && !aDate.isAfter(plan.summerEnd)) {
    charge = quantity * plan.summerRate;
} else {
    charge = quantity * plan.regularRate + plan.regularServiceCharge;
}
```

After

```javascript
if (summer()) {
    charge = summerCharge();
} else {
    charge = regularCharge();
}

function summer() {
    return !aDate.isBefore(plan.summerStart) && !aDate.isAfter(plan.summerEnd);
}

function summerCharge() {
    return quantity * plan.summerRate;
}

function regularCharge() {
    return quantity * plan.regularRate + plan.regularServiceCharge;
}
```

**절차**

1. 조건식과 조건절을 `함수로 추출`하기

**Example**

```javascript
//취향에 따라 3항 연산자로 변경 가능
charge = summer() ? summerCharge() : regularCharge();
```

## 조건식 통합하기

`비교하는 조건은 다르지만 결과 로직이 같다면 하나로 통합하자.`

- 여러 조각의 조건들을 통합하면 더 명확해진다.
- '무엇'이 아닌 '왜'를 말해주는 함수 추출하기로 이어질 수 있다.

`함수 추출하기를 적절히 활용하여 전체를 더 이해하기 쉽게 만들어보자.`

**개요**

Before

```javascript
if (anEmployee.seniority < 2) return 0;
if (anEmployee.monthDisabled > 12) return 0;
if (anEmployee.isPartTime) return 0;
```

After

```javascript
if (isNotEligibleForDisability()) return 0;

function isNotEligibleForDisability() {
    return ((anEmployee.seniority < 2)
            || (anEmployee.monthDisabled < 12)
            || (anEmployee.isPartTime));
}
```

**절차**

1. 해당 조건식에 사이드 이펙트가 없는지 확인
   - 사이드 이펙트가 있을 경우 `질의 함수와 변경 함수 분리하기` 선 적용
2. 조건문 두 개를 선택하여 논리 연산자로 결합
3. 테스트
4. 조건이 하나만 남을 때까지 2~3 반복
5. 하나로 합쳐진 조건식을 `함수로 추출`할지 고려

## 중첩 조건문을 보호 구문으로 바꾸기

`의도를 부각하는 것이 핵심이다.`

`두 경로 중 한 쪽만 정상이라면 비정상 조건을 if 에서 검사한 뒤, 조건이 참(비정상)이면 함수에서 빠져나오게 하자.`

**개요**

Before

```javascript
function getPayAmount() {
    let result;
    if (isDead)
        result = deadAmount();
    else {
        if (isSeparated)
            result = separateAmount();
		else {
            if (isRetired)
                result = retiredAmount();
            else
                result = normalPayAmount();
        }
    }
    return result;
}
```

After

```javascript
function getPayAmount() {
    if (isDead) return deadAmount();
    if (isSeparated) return separateAmount();
    if (isRetired) return retiredAmount();
    return normalPayAmount();
}
```

**절차**

1. 교체해야 할 조건 중 가장 바깥 것을 선택하여 보호 구문으로 바꾸기
2. 테스트
3. 필요에 따라 1.~2. 반복
4. 보호 구문들의 조건식 통합하기

## 조건부 로직을 다형성으로 바꾸기

`복잡한 조건부 로직은 클래스와 다형성을 이용하여 더 확실하게 분리하자.`

**개요**

Before

```javascript
function plumages(birds) {
    return new Map(birds.map((b) => [b.name, plumage(b)]));
}

function speeds(birds) {
    return new Map(birds.map((b) => [b.name, airSpeedVelocity(b)]));
}

function plumage(bird) {
    switch (bird.type) {
        case '유럽 제비':
            return '보통이다';
        case '아프리카 제비':
            return bird.numberOfCoconuts > 2 ? '지쳤다' : '보통이다';
        case '노르웨이 파랑 앵무':
            return bird.voltage > 100 ? '그을렸다' : '예쁘다';
        default:
            return '알 수 없다';
    }
}

function airSpeedVelocity(bird) {
    switch (bird.type) {
        //...
    }
}
```

After

```javascript
function plumages(birds) {
    return new Map(birds
                   .map((b) => createBird(b))
                   .map((bird) => [bird.name, plumage(bird)]),
    );
}

function speeds(birds) {
    return new Map(birds
                   .map((b) => createBird(b))
                   .map((bird) => [bird.name, bird.airSpeedVelocity]),
    );
}

function createBird(bird) {
    switch (bird.type) {
        case '유럽 제비':
            return new EuropeanSwallow(bird);
        case '아프리카 제비':
            return new AfricanSwallow(bird);
        case '노르웨이 파랑 앵무':
            return new NorwegianBlueParrot(bird);
        default:
            return new Bird(bird);
    }
}

class Bird {
  constructor(birdObject) {
    Object.assign(this, birdObject);
  }
  get plumage() { return '알 수 없다'; }
  get airSpeedVelocity() { return null; }
}

class EuropeanSwallow extends Bird {
    get plumage() { return '보통이다'; }
    get airSpeedVelocity() { return 35; }
}

class AfricanSwallow extends Bird {
    get plumage() { return this.numberOfCoconuts > 2 ? '지쳤다' : '보통이다'; }
    get airSpeedVelocity() { return 40 - 2 * bird.numberOfCoconuts; }
}

class NorwegianBlueParrot extends Bird {
    get plumage() { return this.voltage > 100 ? '그을렸다' : '예쁘다'; }
    get airSpeedVelocity() { return bird.isNailed ? 0 : 10 + bird.voltage / 10; }
}
```

**절차**

1. 다형적 동작을 표현하는 `클래스 만들기`
   - 적합한 인스턴스를 알아서 만들어 반환하는 `Factory 함수`도 만들기
2. 호출 코드에서 Factory 함수를 사용하도록 수정
3. 조건부 로직 함수를 슈퍼클래스로 옮기기
4. 서브 클래스 중 하나를 선택하여, 슈퍼클래스의 조건부 로직 메서드를 오버라이드하기
   - 해당 서브클래스에 해당하는 조건절을 메서드로 복사
5. 같은 방식으로 각 조건절을 해당 서브클래스에서 메서드로 구현하기
6. 슈퍼클래스 메서드에는 깁노 동작 부분만 남기기

## 129L

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
