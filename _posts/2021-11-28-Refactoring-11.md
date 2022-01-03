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

## 143R

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
