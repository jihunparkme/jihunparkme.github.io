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
class Organization { // 2.
    constructor(data) {
        this._title = data.title; // 3.
        this._country = data._country;
    }
    get title() { return this._title; } // 3.
    set title(aString) { this._title = aString; } // 3.
    get country() { return this._country; }
    set country(aCountryCode) { this._country = aCountryCode; }
}

const organization = new Organization({ // 6.
    title: '애크미 구스베리',
    country: 'GB',
});
```

## 104L

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
