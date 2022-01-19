---
layout: post
title: 상속 다루기
summary: Chapter 12. 상속 다루기
categories: (Book)Refactoring
featured-img: refactoring
# mathjax: true
---

# Refactoring

# Chapter 12. 상속 다루기

`특정 기능을 상속 계층구조의 위나 아래로 옮겨야 하는 상황은 드물지 않다`

`상속은 막강한 도구지만, 잘못된 곳에서 사용되거나 나중에 환경이 변해 문제가 생기기도 한다.`

## 메서드 올리기

`메서드들의 본문 코드가 똑같을 경우 적용해보자.`

`해당 메서드의 본문에서 참조하는 필드들이 서브클래스에만 있는 경우 '필드들 먼저 슈퍼클래스로 올린' 후 메서드를 올리자.`

`두 메서드의 전체 흐름은 비슷하지만 세부 내용이 다르다면 '템플릿 메서드 만들기'를 고려해보자.`

- 반대 리팩터링 : 메서드 내리기

**개요**.

Before

```javascript
class Employee {}
class Salesperson extends Employee {
    get name() {}
}
class Engineer extends Employee {
    get name() {}
}
```

After

```javascript
class Employee {
    get name() {}
}
class Salesperson extends Employee {}
class Engineer extends Employee {}
```

**절차**.

1. 똑같이 동작하는 메서드인지 살펴보기
2. 메서드 안에서 호출하는 다른 메서드, 참조 필드들을 슈퍼클래스에서도 호출, 참조할 수 있는지 확인하기
3. 메서드 시그니처가 다르다면 `함수 선언 바꾸기`로 슈퍼클래스에서 사용하고 싶은 형태로 통일하기
4. 슈퍼클래스에 새로운 메서드를 생성하고 대상 메서드 코드 복사하기
5. 정적 검사
6. 서브 클래스 중 하나의 메서드 제거
7. 테스트
8. 다른 서브클래스의 메서드를 하나씩 제거

## 필드 올리기

`필드들이 비슷한 방식으로 쓰인다고 판단되면 슈퍼클래스로 올리자.`

`이 리팩터링을 통해 '데이터 중복 선언을 없앨' 수 있고, '해당 필드를 사용하는 동작을 서브클래스에서 슈퍼클래스로 옮길' 수 있다.`

- 반대 리팩터링 : 필드 내리기

**개요**.

Before

```java
class Employee {}
class Salesperson extends Employee {
    private String name;
}
class Engineer extends Employee {
    private String name;
}
```

After

```java
class Employee {
    protected String name;
}
class Salesperson extends Employee {}
class Engineer extends Employee {}
```

**절차**.

1. 후보 필드들이 똑같은 방식으로 사용되는지 살피기
2. 필드들의 이름을 똑같은 이름으로 바꾸기 -> `필드 이름 바꾸기`
3. 슈퍼클래스에 새로운 필드 생성하기 `protected 선언`
4. 서브클래스의 필드들을 제거
5. 테스트

## 생성자 본문 올리기

`이 리팩터링으로 간단하게 끝나지 않는다면 '생성자를 팩터리 함수로 바꾸기'를 고려해보자.`

**개요**.

Before

```javascript
class Party {}

class Employee extends Party {
    constructor(name, id, monthlyCost) {
        super();

        this._name = name;
        this._id = id;
        this._monthlyCost = monthlyCost;
        // 모든 서브 클래스가 수행하는 공통 코드
        if (this.isPrivileged) { this.assignCar(); }
    }
}
```

After

```javascript
class Party {
    constructor(name) { //.1
        this._name = name; //.3
    }
    finishConstruction() {
        if (this.isPrivileged) this.assignCar();
    }
}

class Employee extends Party {
    constructor(name, id, monthlyCost) {
        super(name); //.3

        this._id = id;
        this._monthlyCost = monthlyCost;
        
        this.finishConstruction(); //.5
    }
}
```

**절차**.

1. 슈퍼클래스에 생성자 정의하기
   - 서브클래스 생성자에서 호출 확인
2. `문장 슬라이스하기`로 공통 문장을 모두 super() 호출 직후로 옮기기
3. 공통 코드를 슈퍼클래스에 추가하고 서브클래스에서 제거하기
   - 생성자 매개변수 중 공통 코드에서 참조하는 값들은 모두 super()로 건내기
4. 테스트
5. 공통 코드가 나중에 올 경우 공통 코드에 `함수 추출하기`와 `메서드 올리기`를 차례로 적용하기

## 메서드 내리기

`특정 서브클래스 하나|소수 에만 관련된 메서드는 슈퍼클래스에서 제거하고 해당 서브클래스에 추가하자.`

`해당 기능을 제공하는 서브클래스가 정확히 무엇인지를 호출자가 알고 있을 경우에만 적용하자.`

- 반대 리팩터링 : 메서드 올리기

**개요**.

Before

```javascript
class Employee {
    get quota() {}
}

class Engineer extends Employee {}
class Salesperson extends Employee {}
```

After

```javascript
class Employee {} //.2

class Engineer extends Employee {} //.4
class Salesperson extends Employee { //.1
    get quota() {}
}
```

**절차**.

1. 대상 메서드를 모든 서브클래스에 복사하기
2. 슈퍼클래스에서 해당 메서드 제거하기
3. 테스트
4. 사용하지 않는 해당 메서드를 모든 서브클래스에서 제거하기
5. 테스트

## 필드 내리기

`서브클래스 하나|소수에만 사용되는 필드는 해당 서브클래스로 옮기자.`

- 반대 리팩터링 : 필드 올리기

**개요**.

Before

```javascript
class Employee {
    private String quota;
}

class Engineer extends Employee {}
class Salesperson extends Employee {}
```

After

```javascript
class Employee {} //.2

class Engineer extends Employee {} //.4
class Salesperson extends Employee { //.1
    protected String quota;
}
```

**절차**.

1. 대상 필드를 모든 서브클래스에 정의
2. 슈퍼클래스에서 해당 필드 제거
3. 테스트
4. 사용하지 않는 해당 필드를 모든 서브클래스에서 제거하기 
5. 테스트

## 타입 코드를 서브클래스로 바꾸기

`타입 코드는 구분을 위해 주로 사용된다.`

`서브클래스는 조건에 따라 다르게 동작하도록 해주는 다형성을 제공한다.`

`특정 타입에서만 의미가 있는 값을 사용하는 필드나 메서드가 있을 때 관계를 명확히 드러내준다.`

- 반대 리팩터링 : 서브클래스 제거하기
- 하위 리팩터링
  -  타입 코드를 상태/전략 패턴으로 바꾸기
  - 서브클래스 추출하기

**개요**.

Before

```javascript
function createEmployee(name, type) {
    return new Employee(name, type);
}
```

After

```javascript
function createEmployee(name, type) {
    switch (type) {
        case 'engineer': return new Engineer(name);
        case 'salesperson': return new Salesperson(name);
        case 'manager': return new Manager(name);
    }
}
```

**절차**.

1. 타입 코드 필드를 `자가 캡슐화`하기
2. 타입 코드 값 하나를 선택하여 그 값에 해당하는 `서브클래스` 만들기
3. 매개변수로 받은 타입 코드와 새로운 서브클래스를 매핑하는 `선택 로직` 만들기
4. 테스트
5. 타입 코드 값 각각에 대해 서브클래스 생성과 선택 로직 추가를 반복
6. 타입 코드 필드 제거
7. 테스트
8. 타입 코드 접근자를 이용하는 메서드를 모두 메서드 내리기와 조건부 로직을 다형성으로 바꾸기 적용

**Example**

- Employee 직접 상속

```javascript
class Employee {
    constructor(name) { //.6 타입 코드 필드 제거
        this._name = name;
    }
    set type(type) { this.type = Employee.createEmployee(this._name, arg); }
    toString() { return `${this._name} (${this.capitalizedType})`; }
    get capitalizedType() { 
        return (this.type.charAt(0).toUpperCase() + this.type.substr(1).toLowerCase());
    }
    function createEmployee(name, type) { //.3 생성자를 팩터리 함수로 바꾸기
        switch (type) { //.5
            case 'engineer': return new Engineer(name);
            case 'salesperson': return new Salesperson(name);
            default: throw new Error(`${type}라는 직원 유형은 없습니다.`);
        }
    }
}

class Engineer extends Employee { //.2 서브클래싱
    get type() { return 'engineer'; } //.1 타입 코드 필드 캡슐화
}
class Salesperson extends Employee {
    get type() { return 'salesperson'; }
}
```

- Employee 간접 상속

```javascript
class Employee {
    constructor(name, type) { //.6 타입 코드 필드 제거
        this._name = name;
    }
    set type(arg) { this.type = Employee.createEmployee(arg); }
    get typeString() { return this.type.toString(); }
    get type() { return this.type; }
    toString() { return `${this._name} (${this.type.capitalizedName})`; }
    static createEmployee(aString) { //.3 생성자를 팩터리 함수로 바꾸기
        switch (aString) { //.5
            case 'engineer': return new Engineer();
            case 'salesperson': return new Salesperson();
            default: throw new Error(`${aString}라는 직원 유형은 없습니다.`);
        }
    }
}

class EmployeeType { //.1 타입 코드를 객체로 바꾸기
    get capitalizedName() {
        return this.toString().charAt(0).toUpperCase() + this.toString().substr(1).toLowerCase();
    }
}
class Engineer extends EmployeeType { 
    toString() { return 'engineer'; }
}
class Salesperson extends EmployeeType {
    toString() { return 'salesperson'; }
}
```

## 서브클래스 제거하기

`시스템이 성장하면서 활용되지 않거나, 필요로 하지 않는 방식으로 사용되는 서브클래스를 제거하자.`

- 반대 리팩터링 : 타입 코드를 서브클래스로 바꾸기

**개요**.

Before

```javascript
class Person {
    constructor(name) {
        this._name = name;
    }
    get name() { return this._name; }
    get genderCode() { return 'X'; }
    // ...
}

class Male extends Person {
    get genderCode() { return 'M'; }
}
class Female extends Person {
    get genderCode() { return 'F'; }
}

const numberOfMales = people.filter((p) => p instanceof Male).length;
```

After

```javascript
class Person {
    constructor(name, genderCode) {
        this._name = name;
        this._genderCode= genderCode; //.3 서브클래스의 타입을 나타내는 필드 생성
    }
    get name() { return this._name; }
    get genderCode() { return this._genderCode; }
    //.2 타입 검사 코드 .4 서브클래스 참조가 아닌 타입 필드 사용
    get isMale() { return 'M' === this._genderCode; } 
    // ...
}

function createPerson(aRecord) { //.1 생성자를 팩터리 함수로 바꾸기
    switch (aRecord.gender) {
        case 'M': return new Person(aRecord.name, 'M');
        case 'F': return new Person(aRecord.name, 'F');
        default: return new Person(aRecord.name, 'X');
    }
}
function loadFromInput(data) {
    return data.map((aRecord) => createPerson(aRecord));
}

const numberOfMales = people.filter(p => p.isMale).length;
```

**절차**.

1. 서브클래스의 생성자를 `팩터리 함수`로 바꾸기
2. 서브클래스 타입을 검사하는 코드가 있다면 검사 코드에 `함수 추출하기`, `함수 옮기기`를 적용하여 슈퍼클래스로 옮기기
3. 서브클래스의 타입을 나타내는 필드를 슈퍼클래스에 만들기
4. 서브클래스를 참조하는 메서드가 새로 만든 타입 필드를 이용하도록 수정
5. 서브클래스 지우기
6. 테스트

## 슈퍼클래스 추출하기

`슈퍼클래스로 끌어올리고 싶은 공통 요소를 발견했다면 슈퍼클래스 추출하기를 적용해보자.`

`상속은 프로그램이 성장하며 깨우쳐진다.`

**개요**.

Before

```javascript
class Department {
    get totalAnnualCost() {/**/}
    get name() {/**/}
    get headCount() {/**/}
}
class Employee {
    get annualCost() {/**/}
    get name() {/**/}
    get id() {/**/}
}
```

After

```javascript
class Party {
    get name() {/**/}
    get annualCost() {/**/}
}
class Department extends Party {
    get annualCost() {/**/}
    get headCount() {/**/}
}
class Employee extends Party {
    get annualCost() {/**/}
    get id() {/**/}
}
```

**절차**.

1. 빈 슈퍼클래스 만들기
   - 원래 클래스들이 새 클래스를 상속
2. 테스트
3. `생성자 본문 올리기` / `메서드 올리기` / `필드 올리기` 를 차례로 적용하여 공통 원소를 슈퍼클래스로 옮기기
4. 서브클래스에 남은 메서드 검토하기
   - 공통된 부분은 `함수 추출하기` 후 `메서드 올리기`를 적용하자.
5. 기존 클래스 사용 코드를 슈퍼클래스의 인터페이스를 사용할지 고민하기

**Example**

```javascript
class Party { //.1 빈 슈퍼클래스 만들기
    constructor(name) {
        this._name = name; //.3 필드 올리기
        this._monthlyCost = monthlyCost;
    }
    get name() { return this._name; } //.3 메서드 올리기
    get monthlyCost() { return this._monthlyCost; } //3. 함수 선언 바꾸기 + 메서드 올리기
    get annualCost() { return this.monthlyCost * 12; } //3. 함수 선언 바꾸기 + 메서드 올리기
}

class Department extends Party { //.1 슈퍼클래스 상속
    constructor(name, staff) {
        super(name); //.3 필드 올리기
        this._staff = staff;
    }
    get staff() { return this._staff.slice(); }
    get headCount() { return this.staff.length; }
    get totalMonthlyCost() { 
        return this.staff
            .map((e) => e.monthlyCost)
            .reduce((sum, cost) => sum + cost);
    }
}

class Employee extends Party { //.1 슈퍼클래스 상속
    constructor(name, id, monthlyCost) {
        super(name); //.3 필드 올리기
        this._id = id;
    }
    get id() { return this._id; }
}
```

## 계층 합치기

`어떤 클래스가 그 부모가 비슷해져서 더는 독립적으로 존재할 이유가 사라졌다면, 그 둘을 합쳐야 할 시점이다.`

**개요**.

Before

```javascript
class Employee {}
class Salesperson extends Employee {}
```

After

```javascript
class Employee {}
```

**절차**.

1. 제거할 클래스 고르기
2. `필드 올리기`, `메서드 올리기`/ `필드 내리기`, `메서드 내리기` 를 적용하여 하나의 클래스로 옮기기
3. 제거할 클래스를 참조하던 코드 수정
4. 빈 클래스 제거
5. 테스트

## 서브클래스를 위임으로 바꾸기

`서브클래싱 관련 문제에 직면할 경우 적용해보자.`

- 다양한 클래스에 서로 다른 이유로 위임을 할 수 없을 경우 (사람 객체를 '나이대'와 '소득 수준'을 기준으로 달리 하고 싶을 경우)
  - 서브클래스는 젊은이/어르신이 되거나 부자/서민이 되어야 하고 둘 다는 불가능
  - 동적 서브클래스 전환(서민 -> 부자)
- 상속 클래스들의 결합도가 강할 경우

`위임으로 바꾸었을 때의 장점이 상속을 없애는 단점보다 클 경우 적용해보자.`

**개요**.

Before

```javascript
class Order {
    get daysToShip() { return this._warehouse.daysToShip; }
}
class PriorityOrder extends Order {
    get daysToShip() { return this._priorityPlan.daysToShip; }
}
```

After

```javascript
class Order {
    get daysToShip() {
        return this._priorityDelegate ? this._priorityPlan.daysToShip : this._warehouse.daysToShip;
    }
}
class PriorityOrderDelegate {
    get daysToShip() { return this._priorityPlan.daysToShip; }
}
```

**절차**.

1. 생성자를 호출하는 곳이 많을 경우 `팩터리 함수로 바꾸기`
2. 위임클래스 만들기
   - 생성자는 서브클래스가 사용하던 매개변수와 슈퍼클래스를 가리키는 역참조를 필요
     - 위임에서 슈퍼클래스 데이터에 접근하려면 역참조가 필요
3. 위임을 저장할 필드를 슈퍼클래스에 추가
4. 서브클래스 생성 코드를 수정하여 위임 인스턴스를 생성하고 위임 필드에 대입해 초기화
   - 팩터리 함수 혹은 생성자에서 작업 수행
5. 서브클래스의 메서드 중 위임 클래스로 이동할 것을 고르기
6. `함수 옮기기`를 적용해 위임 클래스로 옮기기
7. 서브클래스 호출하는 코드를 슈퍼클래스로 옮기기
8. 테스트
9. 서브클래스의 모든 메서드 옮기기 (5~8 반복)
10. 서브클래스 생성자를 호출하는 코드를 슈퍼클래스 생성자 호출로 수정
11. 테스트
12. 서브클래스 삭제

**Example**

- 서브 클래스가 하나일 때

```javascript
class Booking {
    constructor(show, date) {
        this._show = show;
        this._date = date;
    }
    get hasTalkback() { //.7 서브클래스 호출 코드를 슈퍼클래스로 옮기기
        return (this._premiumDelegate) ? this._premiumDelegate.hasTalkback : this._show.hasOwnProperty('talkback') && !this.isPeakDay;
    }
    get basePrice() { 
        let result = this._show.price;
        if (this.isPeakDay) result += Math.round(result * 0.15);
        return (this._premiumDelegate) ? this._premiumDelegate.extendBasePrice(result) : this._privateBasePrice;
    }
    get hasDinner() { return (this._premiumDelegate) ? this._premiumDelegate.hasDinner : undefined; }
    _bePremium(extras) { this._premiumDelegate = new PremiumBookingDelegate(this, extras); } //.3 위임을 저장할 필드
}

class PremiumBookingDelegate { //.2 위임클래스 만들기
    constructor(hostBooking, extras) {
        this._host = hostBooking; //.2 슈퍼클래스 역참조
        this._extras = extras;
    }
    get hasTalkback() { return this._host._show.hasOwnProperty('talkback'); } //.6 서브클래스 메서드 옮기기(역참조 이용)
    get hasDinner() { return this._extras.hasOwnProperty('dinner') && !this._host.isPeakDay; } //.9 서브클래스 메서드 옮기기
    extendBasePrice(base) { return Math.round(base + this._extras.premiumFee); } //.9 서브클래스 메서드 옮기기
}
function createBooking(show, date) { return new Booking(show, date); } //.1 생성자를 팩터리 함수로 바꾸기 (호출 캡슐화)
function createPremiumBooking(show, date, extras) { //.1 생성자를 팩터리 함수로 바꾸기 (호출 캡슐화)
    const result = new Booking(show, date, extras); //.10 팩터리 메서드가 슈퍼클래스를 반환하도록 수정
    result._bePremium(extras); //.4 위임 인스턴스를 생성하고 위임 필드에 대입해 초기화
    return result;
}

const aBooking = createBooking(show, date);
const aPremiumBooking = createPremiumBooking(show, date, extras);
```

- 서브 클래스가 여러 개일 때

```javascript
function createBird(data) { return new Bird(data); }

class Bird {
    constructor(data) {
        this._name = data.name;
        this._plumage = data.plumage;
        this._specialDelegate = this.selectSpecialDelegate(data); //.3 위임 저장 필드 추가
    }
    get name() { return this._name; }
    get plumage() { return this._specialDelegate.plumage; } //.7 서브클래스 호출 코드를 슈퍼클래스로
    get airSpeedVelocity() { return this._specialDelegate.airSpeedVelocity; } //.7 서브클래스 호출 코드를 슈퍼클래스로
    selectSpecialDelegate(data) { //.10 서브클래스 생성자 호출 코드
        switch (data.type) {
            case '유럽 제비':
                return new EuropeanSwallowDelegate(data, this); //.4 위임 인스턴스 생성
            case '아프리카 제비':
                return new AfricanSwallowDelegate(data, this);
            case '노르웨이 파랑 앵무':
                return new NorwegianBlueParrotDelegate(data, this);
            default:
                return new SpeciesDelegate(data, this);
        }
    }
}

class SpeciesDelegate { //=> 슈퍼클래스 추출 (위임 클래스의 메서드, 역참조 코드의 중복 해결)
    constructor(data, bird) {
        this._bird = bird; //.2 슈퍼클래스 역참조
    }
    get plumage() { return this._bird._plumage || '보통이다'; } //=> 중복 메서드
    get airSpeedVelocity() { return null; }
}

class EuropeanSwallowDelegate extends SpeciesDelegate { //.2 위임클래스 만들기
    get airSpeedVelocity() { return 35; } //.6 함수 옮기기
}

class AfricanSwallowDelegate extends SpeciesDelegate { //.2 위임클래스 만들기
    constructor(data) {
        super(data, bird);
        this._numberOfCoconuts = data.numberOfCoconuts;
    }
    get airSpeedVelocity() { return 40 - 2 * this._numberOfCoconuts; } //.6 함수 옮기기
}

class NorwegianBlueParrotDelegate extends SpeciesDelegate { //.2 위임클래스 만들기
    constructor(data, bird) {
        super(data, bird);
        this._voltage = data.voltage;
        this._isNailed = data.isNailed;
    }
    get airSpeedVelocity() { return this._isNailed ? 0 : 10 + this._voltage / 10; } //.6 함수 옮기기
    get plumage() { //.6 함수 옮기기
        if (this._voltage > 100) return '그을렸다';
        else return this._bird_plumage || '예쁘다';
        }
    }
}
```

## 슈퍼클래스를 위임으로 바꾸기

`상속은 혼란과 복잡도를 키우는 방식으로 이뤄지기도 한다.`

- 슈퍼클래스의 기능들이 서브클래스에 어울리지 않는다면, 그 기능들은 상속을 통해 이용하면 안된다.
- 제대로된 상속이라면 서브클래스가 슈퍼클래스의 모든 기능을 사용해야 하고, 서브클래스의 인스턴스를 슈퍼클래스의 인스턴스로도 취급할 수 있어야 한다.

`위임을 이용하면 기능 일부만 빌려올 뿐, 서로 별개인 개념이 명확해진다.`

`상속을 먼저 적용해보고, 문제가 생길 경우 슈퍼클래스를 위임으로 바꾸어보자.`

**개요**.

Before

```javascript
class List {}
class Stack extends List {}
```

After

```javascript
class Stack {
    constructor() {
        this._storage = new List();
    }
}
class List {}
```

**절차**.

1. 슈퍼클래스 객체를 참조하는 필드를 서브클래스에 만들기
   - 위임 참조를 새로운 슈퍼클래스 인스턴스로 초기화
2. 슈퍼클래스의 동작 각각에 대응하는 전달 함수를 서브클래스에 만들기
   - 서로 관련된 함수끼리 그룹으로 묶어 진행
3. 슈퍼클래스의 동작 모두가 전달 함수로 오버라이드되었다면 상속 관계 끊기

**Example**

```javascript
class CatalogItem {
    constructor(id, title, tags) {
        this._id = id;
        this._title = title;
        this._tags = tags;
    }
    get id() { return this._id; }
    get title() { return this._title; }
    hasTag(arg) { return this._tags.includes(arg); }
}

class Scroll { //.3 슈퍼클래스와 상속 관계 끊기
    constructor(id, dataLastCleaned, catalogId, catalog) {
        this._id = id;
        this._catalogItem = catalog.get(catalogId); //.1 슈퍼클래스를 참조하는 속성
        this._lastCleaned = dataLastCleaned;
    }
    get id() { return this._id; } //.2 슈퍼클래스의 동작 각각에 대응하는 전달 메서드 생성
    get title() { return this._catalogItem.title; } //.2 
    hasTag(aString) { return this._catalogItem.tags.hasTag(aString); } //.2 
    needsCleaning(targetDate) {
        const threshold = this.hasTag('revered') ? 700 : 1500;
        return this.daysSinceLastCleaning(targetDate) > threshold;
    }
    daysSinceLastCleaning(targetDate) {
        return this._lastCleaned.until(targetDate, ChronoUnit.DAYS);
    }
}

const scrolls = aDocument
        .map((record) => new Scroll(record.id,
                                    LocalDate.parse(record.lastCleaned),
                                    record.catalogData.id,
                                    catalog,
    ),
);
```

