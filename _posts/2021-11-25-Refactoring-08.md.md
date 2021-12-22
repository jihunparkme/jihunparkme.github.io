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

## 79R

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



