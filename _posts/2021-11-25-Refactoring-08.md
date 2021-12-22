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

## 89L

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
