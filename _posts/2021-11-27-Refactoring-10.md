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

## 113R

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
