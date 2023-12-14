---
layout: post
title: GoF Design Pattern
summary: GoF Design Pattern
categories: JAVA
featured-img: design-pattern
---

# GoF Design Patterns

[Refactoring.Guru](https://refactoring.guru/design-patterns) 의 [Design Patterns](https://refactoring.guru/design-patterns) 주제를 정리하며 실습한 내용들을 다루는 글입니다.

.

# Creational Design Patterns

생성 디자인 패턴은 기존 코드의 유연성과 재사용을 증가시키는 `객체를 생성하는 다양한 방법`을 제공

.

## Factory Method

[factory-method](https://refactoring.guru/design-patterns/factory-method)

부모 클래스에서 객체들을 생성할 수 있는 인터페이스를 제공하지만, `자식 클래스들이 생성될 객체들의 유형을 변경`할 수 있도록 하는 생성 패턴

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/factory-method-ko-2x.png?raw=true 'Result')

.

**`Problem`**

트럭 물류 관리 어플을 개발했다.

요즘들어 어플이 유명해지면서 해상 물류 회사들로부터 해상 물류 기능을 추가해 달라는 요청이 들어오고 있다.

하지만.. 지금 대부분 코드는 트럭 클래스에 의존되어 있고, 선박 클래스를 추가하기 위해 전체 코드 베이스 변경이 필요한 상황이다. 이후 다른 유형의 물류 교통수단도 추가된다면 다시 전체 코드 베이스 수정이 필요할 것이다.

이대로라면 운송 수단 객체들이 추가될 때마다 많은 조건문들이 생겨나는 매우 복잡한 코드가 작성될텐데..

어떻게 하는 게 좋을까? 😭

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/structure-2x.png?raw=true 'Result')

Factory Method Pattern은 `객체 생성 호출을 특별한 팩토리 메소드에 대한 호출로 대체`
- 자식 클래스들은 팩토리 메서드가 반환하는 객체들의 클래스를 변경 가능
  - 생성자 호출을 팩토리 메소드에게 위임하면서 자식 클래스에서 팩토리 메소드를 오버라이딩하고 생성되는 제품들의 클래스를 변경 가능
- 약간의 제한이 있지만, 자식 클래스들은 다른 유형의 제품들을 해당 제품들이 공통 기초 클래스 또는 공통 인터페이스가 있는 경우에만 반환 가능
  - ConcreteCreatorA 클래스에 포함된 팩토리 메소드는 ConcreteProductA 객체들을 반환
  - ConcreteCreatorB 클래스에 포함된 팩토리 메소드는 ConcreteProductB 객체들을 반환

.

모든 제품 클래스들이 공통 인터페이스를 구현하는 한, 제품 클래스들의 객체들을 손상시키지 않고 클라이언트 코드 작성 가능
- 클라이언트는 다양한 자식 클래스들에서 실제로 반환되는 클래스를 알지 못함
- 클라이언트는 모든 제품을 추상 클래스로 간주하고 메소드가 어떻게 동작하는지 중요하지 않음

```java
public class App {

    private static Logistics creator;

    public void initialize(String type) {
        if ("truck".equals(type)) {
            creator = new RoadLogistics();
            return;
        }

        if ("ship".equals(type)) {
            creator = new SeaLogistics();
            return;
        }

        throw new IllegalArgumentException("Unknown operating system.");
    }

    public static void main(String[] args) {
        App app = new App();

        app.initialize("truck");
        creator.planDelivery(); //=> Truck deliver

        app.initialize("ship");
        creator.planDelivery(); //=> Ship deliver
    }
}
```

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/factory-method-example.png?raw=true 'Result')

[Factory Method Pattern Practice](https://github.com/jihunparkme/GoF-Design-Pattern/tree/main/src/main/java/com/pattern/design/creationalDesignPatterns/factoryMethod)

.

**`Apply`**

- 함께 작동해야 하는 객체들의 정확한 유형들과 의존관계들을 미리 모르는 경우 사용
- 라이브러리 또는 프레임워크의 사용자들에게 내부 컴포넌트들을 확장하는 방법을 제공하고 싶을 때 사용
- 기존 객체들을 매번 재구축하는 대신 이들을 재사용하여 시스템 리소스를 절약하고 싶을 때 사용

.

**`pros and cons`**

장점.
- Creator, Product 가 강하게 결합되지 않도록 할 수 있으
- 단일 책임 원칙(SRP). 제품 생성 코드를 한 곳으로 이동
- 개방/폐쇄 원칙(OCP). 기존 클라이언트 코드를 훼손하지 않고 새로운 유형의 제품을 추가

단점.
- 패턴을 구현하기 위해 많은 (자식)클래스 생성이 필요하여 코드가 복잡해질 수 있음

.

## Abstract Factory

[abstract-factory](https://refactoring.guru/design-patterns/abstract-factory)

관련 객체들의 구상 클래스들을 지정하지 않고도 `관련 객체들의 모음을 생성`할 수 있도록 하는 생성패턴

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/abstract-factory-ko-2x.png?raw=true'Result')

**`Problem`**

의자, 소파, 테이블을 판매하는 프로그램을 만들고 있다.

취향별로 디자인을 묶어 제품을 세트로 판매하고 싶다.

A 디자인 세트, B 디자인 세트, C 디자인 세트..

새로운 디자인 세트가 나오게 되면 추가할 때마다 기존 코드를 변경해야 하는 번거로움을 피하고 싶은데..

어떻게 하는 게 좋을까? 😭

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/abstract-factory-solution.png?raw=true 'Result')

\1. 각 제품 디자인 세트​에 해당하는 개별적인 인터페이스를 명시적으로 선언하기
- 제품의 모든 변형이 위 인터페이스를 따르도록 하기
  - ex. 모든 의자의 변형들은 Chair 인터페이스를 구현
  - ex. 모든 테이블 변형들은 ­Table 인터페이스를 구현.. 등의 규칙을 명시

\2. 추상 팩토리 패턴을 선언하기
- 추상 팩토리 패턴은 제품 디자인 새트 내의 모든 개별 제품들의 생성 메서드들이 목록화되어있는 인터페이스
  - ex. create­Chair, create­Sofa, create­­Table

\3. 제품 변형 다루기
- 패밀리의 각 변형에 대해 Abstract­Factory 추상 팩토리 인터페이스를 기반으로 별도의 팩토리 클래스를 생성
- 팩토리는 특정 종류의 제품을 반환하는 클래스
  - ex. Modern­Furniture­Factory​에서는 다음 객체들만 생성(Modern­Chair, Modern­Sofa​, Modern­Coffee­Table​)

\4. 클라이언트
- 클라이언트는 자신에 해당하는 추상 인터페이스를 통해 팩토리들과 제품들 모두와 함께 작동해야 한다.
- 그래야 클라이언트 코드에 넘기는 팩토리의 종류와 제품 변형들을 클라이언트 코드를 손상하지 않으며 자유자재로 변경 가능
- 클라이언트는 함께 작업하는 팩토리의 구상 클래스에 대해 신경을 쓰지 않아야 한다.

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/abstract-factory-method-pattern-practice.png?raw=true'Result')

[Abstract Factory Pattern Practice](https://github.com/jihunparkme/GoF-Design-Pattern/tree/main/src/main/java/com/pattern/design/creationalDesignPatterns/abstractFactory)

.

**`Apply`**

- 관련된 제품군의 다양한 세트들과 작동해야 하지만 해당 제품들의 구상 클래스들에 의존하고 싶지 않을 경우 사용
  - 새로 추가될 클래스를 미리 알 수 없고, 확장성을 고려할 경우
  - 추상 팩토리가 각 세트에 포함되는 제품들을 다른 제품으로 잘못 생성할 일이 없음
- 클래스가 있고, 이 클래스의 팩토리 메소드들의 집합의 기본 책임이 뚜렷하지 않을 경우 고려
  - 잘 설계된 프로그램에서 각 클래스는 하나의 책임만 가짐(SRP. 단일 책임 원칙)

.

**`pros and cons`**

장점.
- 팩토리에서 생성되는 제품들의 `상호 호환 보장`.
- 구상 제품들과 클라이언트 코드 사이의 단단한 결합을 피할 수 있음.
- 단일 책임 원칙(`SRP`). 제품 생성 코드를 한 곳으로 추출하여 쉬운 유지보수 가능.
- 개방/폐쇄 원칙(`OCP`). 기존 클라이언트 코드를 훼손하지 않고 제품의 새로운 변형들을 생성 가능.

단점.
- 새로운 패턴이 추가되면 인터페이스, 클래스가 많이 도입되므로 코드가 필요 이상으로 복잡해질 수 있음.

.

## Builder

[builder](https://refactoring.guru/design-patterns/builder)

빌더는 `복잡한 객체들을 단계별로 생성`할 수 있도록 하는 생성 디자인 패턴
- 같은 제작 코드를 사용하여 객체의 다양한 유형들과 표현 제작 가능

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/builder-pattern.png?raw=true'Result')

.

**`Problem`**

많은 필드와 중첩된 객체들을 단계별로 힘들게 초기화해야 하는 복잡한 객체들을 만나보았을 것이다.

이러한 초기화 코드는 일반적으로 많은 매개변수가 있는 거대한 생성자 내부에 묻혀 있다.

더 최악의 상황에는.. 클라이언트 코드 전체에 흩어져 있을 수도 있다.

여기에 특정 케이스에만 사용되는 매개변수들이 조금씩 추가되다 보면 생성자 호출 코드는 알아볼 수 없을 지경이 되어 버릴 것이다..

어떻게 하는 게 좋을까? 😭

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/builder-pattern-structure.png?raw=true 'Result')

빌더 패턴은 자신의 클래스에서 객체 생성 코드를 추출하여 builders(건축업자들)​라는 별도의 객체들로 이동하도록 제안
- 객체 생성을 일련의 단계들로 정리
- 객체를 생성하고 싶다면 단계들을 builder 객체에 실행
- 객체의 특정 설정을 제작하는 데 필요한 단계들만 호출

디렉터
- 제품을 생성하는 데 사용하는 빌더 단계들에 대한 일련의 호출을 디렉터(관리자)라는 별도의 클래스로 추출
- `Director` 클래스는 제작 단계들을 실행하는 **순서를 정의**하는 반면 `Builder`는 이러한 단계들에 대한 **구현을 제공**
- 디렉터 클래스는 필수가 아니지만, 다양한 생성 루틴들을 배치하여 재사용할 수 있는 좋은 장소가 될 수 있다.
- 또한, 디렉터 클래스는 클라이언트 코드에서 제품 생성의 세부 정보를 완전히 숨길 수 있다.
  - 클라이언트는 빌더를 디렉터와 연관시키고 디렉터와 생성을 시행한 후 빌더로부터 결과를 얻기만 하면 됩니다.

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/builder-pattern-practice.png?raw=true'Result')

[Builder Pattern Practice](https://github.com/jihunparkme/GoF-Design-Pattern/tree/main/src/main/java/com/pattern/design/creationalDesignPatterns/builder)

.

**`Apply`**

- '점층적 생성자'를 제거하기 위해 빌더 패턴 사용
  - 필요한 단계들만 사용하여 단계별로 객체들을 생성 가능
  - 패턴 구현 후에는 수십 개의 매개변수를 생성자에 집어넣는 일은 불필요
- 코드가 일부 제품의 다른 표현(ex. SUV)들​을 생성할 수 있도록 하고 싶을 때 사용
- 복합체 트리, 기타 복잡한 객체들을 생성


.

**`pros and cons`**

장점.
- 객체들을 단계별로 생성하거나, 생성 단계들을 연기하거나, 재귀적으로 단계들을 실행 가능
- 제품들의 다양한 표현을 만들 때 같은 생성 코드를 재사용 가능
- 단일 책임 원칙(SRP). 제품의 비즈니스 로직에서 복잡한 생성 코드 고립 가능

단점.
- 패턴이 여러 개의 새 클래스들을 생성해야 하므로 코드의 전반적인 복잡성이 증가

.

## Prototype

[prototype](https://refactoring.guru/design-patterns/prototype)

코드를 각 클래스들에 의존시키지 않고 `기존 객체들을 복사`할 수 있도록 하는 생성 디자인 패턴

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/prototype-pattern.png?raw=true'Result')

.

**`Problem`**

특정한 객체의 복사본을 만들고 싶다.

그렇다면.. 먼저 같은 클래스의 새 객체를 생성하고.. 원본 객체의 모든 필드를 살피고.. 해당 값들을 새 객체에 복사해야 한다.

하지만.. 객체 필드들 중 일부가 비공개라면 모든 객체에 이 방법을 적용할 수 없을 것이다.

그리고.. 객체의 복제본을 생성하려면 객체의 클래스를 알아야 하므로, 코드는 해당 클래스에 의존하게 될 것이다.

또, 인터페이스의 구현 클래스라면 인터페이스만 알고, 그 객체의 구상 클래스는 알지 못할 수 있다.

그렇다면.. 어떻게 하는 게 좋을까? 😭

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/prototype-pattern-structure.png?raw=true 'Result')

프로토타입 패턴은 실제로 복제되는 객체들에 `복제 프로세스를 위임`
- 복제를 지원하는 모든 객체에 대한 공통 인터페이스를 선언
- 이 인터페이스를 사용하면 코드를 객체의 클래스에 결합하지 않고도 해당 객체를 복제 가능
- 일반적으로 이러한 인터페이스에는 단일 clone 메서드만 포함

`clone 메서드 구현`은 모든 클래스에서 매우 유사
- 이 메서드는 현재 클래스의 객체를 만든 후 이전 객체의 모든 필드 값을 새 객체로 전달
- 객체들이 같은 클래스에 속한 다른 객체의 비공개 필드들에 접근​ 가능

프로토타입: `복제를 지원하는 객체`
- 객체들에 수십 개의 필드와 수백 개의 가능한 설정들이 있는 경우 이를 복제하는 것이 서브클래싱의 대안이 될 수 있음
- 프로그래밍의 프로토타입의 경우 생산과정에 참여하지 않고 자신을 복제하므로 세포의 유사분열 과정과 유사

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/prototype-pattern-practice.png?raw=true'Result')

[Prototype Pattern Practice](https://github.com/jihunparkme/GoF-Design-Pattern/tree/main/src/main/java/com/pattern/design/creationalDesignPatterns/prototype)

.

**`Apply`**

- 복사해야 하는 객체들의 **구상 클래스들에 코드가 의존하면 안 될 경우** 사용
  - 클라이언트 코드가 복제하는 객체들의 구상 클래스들에서 클라이언트 코드를 독립
- 각자의 객체를 초기화하는 방식만 다른, 자식 클래스들의 수를 줄이고 싶을 경우 사용
  - 다양한 방식으로 설정된 미리 만들어진 객체들의 집합을 프로토타입들로 사용할 수 있도록 제공
  - 일부 설정과 일치하는 자식 클래스를 **인스턴스화하는 대신** 클라이언트는 간단하게 **적절한 프로토타입을 찾아 복제**

.

**`pros and cons`**

장점.
- 객체들을 그 구상 클래스들에 **결합하지 않고 복제** 가능
- 반복되는 초기화 코드를 제거한 후, 그 대신 **미리 만들어진 프로토타입들을 복제**하는 방법을 사용
- 복잡한 객체들을 더 쉽게 생성
- 복잡한 객체들에 대한 사전 설정들을 처리할 때 **상속 대신 사용할 수 있는 방법**

단점.
- 순환 참조가 있는 복잡한 객체들을 복제하는 것은 매우 까다로울 수 있음

.

## Singleton

[singleton](https://refactoring.guru/ko/design-patterns/singleton)

`클래스에 인스턴스가 하나만` 있도록 하면서 이 인스턴스에 대한 전역 접근 지점을 제공하는 생성 디자인 패턴

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/singleton-pattern.png?raw=true'Result')

.

**`Problem`**

싱글턴 패턴은 한 번에 두 가지의 문제를 동시에 해결함으로써 단일 책임 원칙(SRP)을 위반

클래스에 인스턴스가 하나만 존재
- 생성자 호출은 특성상 반드시 새 객체를 반환해야 하므로 위 행동은 일반 생성자로 구현 불가.

해당 인스턴스에 대한 전역 접근 지점을 제공
- 프로그램의 모든 곳에서부터 일부 객체에 접근 가능
- 그러나, 다른 코드가 해당 인스턴스를 덮어쓰지 못하도록 보호

최근에는 싱글턴 패턴이 워낙 대중화되어 패턴이 나열된 문제 중 한 가지만 해결하더라도 그것을 싱글턴이라고 부를 수 있음.

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/singleton-structure.png?raw=true 'Result')

싱글턴의 모든 구현에는 공통적으로 두 단계가 존재

- 다른 객체들이 싱글턴 클래스와 함께 new 연산자를 사용하지 못하도록 `디폴트 생성자를 비공개`로 설정
- `생성자 역할을 하는 정적 생성 메서드` 생성
  - 내부적으로 이 메서드는 객체를 만들기 위하여 비공개 생성자를 호출한 후 객체를 정적 필드에 저장
  - 이 메서드에 대한 그다음 호출들은 모두 캐시된 객체 반환
 
싱글턴 클래스에 접근할 수 있는 경우, 이 코드는 싱글턴의 정적 메서드 호출 가능
- 따라서 해당 메서드가 호출될 때마다 항상 같은 객체가 반환

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/singleton-practice.png?raw=true'Result')

[Singleton Pattern Practice](https://github.com/jihunparkme/GoF-Design-Pattern/tree/main/src/main/java/com/pattern/design/creationalDesignPatterns/singleton)

단일 스레드에서 기본 싱글턴
- 기본 싱글턴은 생성자를 숨기고 정적 생성 메서드를 구현

멀티 스레드에서 기본 싱글턴
- 여러 스레드가 생성 메서드를 동시에 호출할 수 있고, 싱글턴 클래스의 여러 인스턴스를 가져올 수 있음

지연 로딩이 있는 스레드 안전한 싱글턴
- 싱글턴 객체를 처음 생성하는 동안 스레드들을 동기화

.

**`Apply`**

- 클래스에 모든 클라이언트가 사용할 수 있는 `단일 인스턴스`만 있어야 할 경우
  - ex. 프로그램에서 공유되는 단일 데이터베이스 객체
  - 클래스의 객체를 생성할 수 있는 모든 수단을 비활성화
  - 새 객체를 생성하거나 객체가 이미 생성되었으면 기존 객체를 반환
- 전역 변수들을 더 엄격하게 제어해야 할 경우
  - 클래스의 인스턴스가 하나만 있도록 보장

.

**`pros and cons`**

장점.
- 클래스가 하나의 인스턴스만 갖는 것을 보장
- 인스턴스에 전역 접근 가능
- 처음 요청될 때만 초기화

단점.
- 단일 책임 원칙(SRP) 위반 (한 번에 두 가지의 문제를 동시에 해결)
- 다중 스레드 환경에서 여러 스레드가 싱글턴 객체를 여러번 생성하지 않도록 처리 필요
- 클라이언트 코드 유닛 테스트의 어려움
  - 많은 테스트 프레임워크들이 모의 객체들을 생성할 때 상속에 의존
  - 싱글턴 클래스의 생성자는 비공개이고 대부분 언어에서 정적 메서드를 오버라이딩하는 것이 불가능
- 컴포넌트들이 서로에 대해 너무 많이 알고 있을 수 있음

.

# Structural Design Patterns

구조 패턴은 `구조를 유연하고 효율적으로 유지`하면서 객체와 클래스들을 `더 큰 구조로 조립`하는 방법 제공

.

## Adapter

[Adapter, Wrapper](https://refactoring.guru/ko/design-patterns/adapter)

`호환되지 않는 인터페이스`를 가진 객체들이 `협업`할 수 있도록 하는 구조적 디자인 패턴

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/adapter-pattern.png?raw=true'Result')

.

**`Problem`**

XML 형식으로 데이터를 내려주는 API 가 있다.

하지만 우리가 사용하는 라이브러리는 JSON 형식의 데이터로만 동작한다.

XML 형식의 데이터를 주는 API와 JSON 형식의 데이터로 동작하는 라이브러리를 호환시키고 싶은데..

어떻게 하는 게 좋을까? 😭

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/adapter-pattern-structure.png?raw=true 'Result')

`어댑터`는 한 객체의 인터페이스를 다른 객체가 이해할 수 있도록 변환하는 특별한 객체
- 변환의 복잡성을 숨기기 위해 객체 중 하나를 래핑​(포장)
- ​래핑된 객체는 어댑터 인식 불가
- ex. km, m 단위로 동작하는 객체를 ft, mile 같은 영국식 단위로 변환하는 어댑터

데이터를 다양한 형식으로 변환 가능하고 다른 인터페이스를 가진 객체들이 협업하는 데 도움
- 양방향으로 호출을 변환할 수 있는 양방향 어댑터를 만드는 것도 가능

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/adapter-pattern-practice.png?raw=true'Result')

[Adapter Pattern Practice](https://github.com/jihunparkme/GoF-Design-Pattern/tree/main/src/main/java/com/pattern/design/structuralDesignPatterns/adapter)

객체 어댑터
- 객체 합성 원칙을 사용
- 어댑터는 한 객체의 인터페이스를 구현하고 다른 객체는 래핑

클래스 어댑터
- 상속을 사용
- 어댑터는 동시에 두 객체의 인터페이스를 상속

.

**`Apply`**

- 기존 클래스를 사용하고 싶지만 그 인터페이스가 나머지 코드와 호환되지 않을 경우
- 어떤 공통 기능들이 없는 여러 기존 자식 클래스들을 재사용하려는 경우
  - 누락된 기능을 어댑터 클래스에 넣고 자식 클래스를 래핑하여 필요한 기능들을 동적으로 획득

.

**`pros and cons`**

장점.
- 단일 책임 원칙(SRP). 
  - 기본 비즈니스 로직에서 인터페이스 또는 데이터 변환 코드 분리 가능
- 개방/폐쇄 원칙(OCP)
  - 클라이언트 코드가 클라이언트 인터페이스를 통해 어댑터와 작동하는 한, 기존의 클라이언트 코드를 손상시키지 않고 새로운 유형의 어댑터들을 프로그램에 도입 가능

단점.
- 다수의 새로운 인터페이스와 클래스들을 도입해야 하므로 코드의 전반적인 복잡성이 증가
  - 때로는 코드의 나머지 부분과 작동하도록 서비스 클래스를 변경하는 것이 더 간단

.

## Bridge

[Bridge](https://refactoring.guru/ko/design-patterns/bridge)

브리지는 큰 클래스 또는 밀접하게 관련된 `클래스들의 집합을 두 개의 개별 계층구조​(추상화 및 구현)​로 나눈` 후 각각 독립적으로 개발할 수 있도록 하는 구조 디자인 패턴

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/bridge-pattern.png?raw=true'Result')

.

**`Problem`**

모양(원, 직사각형)과 색상(빨간색, 파란색)으로 조합을 만들려고 한다.

빨간색 원, 빨간색 직사각형, 파란색 원, 파란색 직사각형의 조합이 생기게 될텐데 새로운 모양과 색상이 추가될 떄마다 계층 구조는 기하급수적으로 많아지고 코드도 복잡해질 것이다.

복잡성을 줄이려면 어떻게 하는 게 좋을까? 😭

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/bridge-pattern-structure.png?raw=true 'Result')

브리지 패턴은 상속에서 객체 합성으로 전환하여 이 문제를 해결
- 차원 중 하나를 별도의 클래스 계층구조로 추출하여 원래 클래스들이 한 클래스 내에서 모든 상태와 행동들을 갖는 대신 새 계층구조의 객체를 참조

```text
[ AS-IS ]
모양
 ㄴ 빨간색 원
 ㄴ 빨간색 직사각형
 ㄴ 파랑색 원
 ㄴ 파란색 직사각형

[ TO-BE ]
모양
 ㄴ 원
 ㄴ 직사각형

색
 ㄴ 빨간색
 ㄴ 파란색
```

추상화와 구현
- 추상화: 앱의 GUI 레이어(IOS, Window, Linux)
- 구현: 운영 체제의 API

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/bridge-pattern-practice.png?raw=true'Result')

[Bridge Pattern Practice](https://github.com/jihunparkme/GoF-Design-Pattern/tree/main/src/main/java/com/pattern/design/structuralDesignPatterns/bridge)

.

**`Apply`**

- 특정 기능의 여러 변형을 가진 모놀리식 클래스를 여러 클래스 계층구조로 나눌 경우
  - ex. 클래스가 다양한 데이터베이스 서버들과 작동하는 경우
- 여러 독립 차원에서 클래스를 확장해야 할 경우
  - 모든 작업을 자체적으로 수행하는 대신 추출된 계층구조들에 속한 객체들에게 관련 작업들을 위임
- 런타임​에 구현을 전환할 수 있어야 할 경우
  - 필드에 새 값을 할당하면 추상화 내부 구현 객체 변경 가능

.

**`pros and cons`**

장점.
- 플랫폼 독립적인 클래스와 앱을 만들 수 있음
- 클라이언트 코드는 상위 수준의 추상화를 통해 작동하며, 플랫폼 세부 정보에 노출되지 않음
- 개방/폐쇄 원칙(OCP). 새로운 추상화들과 구현들을 상호 독립적으로 도입 가능
- 단일 책임 원칙(SRP). 추상화의 상위 수준 논리와 구현의 플랫폼 세부 정보에 집중 가능

단점.
- 결합도가 높은 클래스에 패턴을 적용하여 코드를 더 복잡하게 만들 수 있음

.

## Composite

[Composite](https://refactoring.guru/ko/design-patterns/composite)

복합체 패턴은 객체들을 `트리 구조들로 구성`한 후, 이러한 구조들과 `개별 객체들처럼 작업`할 수 있도록 하는 구조 패턴

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/composite-pattern.png?raw=true'Result')

.

**`Problem`**

복합체 패턴은 앱의 핵심 모델이 트리로 표현될 수 있을 때만 사용.

.

아래와 같이 복잡한 주문이 들어왔다.

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/composite-pattern-example.png?raw=true'Result')

주문의 총 가격을 구해야 할 때, 현실 세계라면 모든 상자를 푼 후 내부의 모든 제품을 확인할 수 있을 것이다.

하지만, 프로그램이서는 상자의 중첩 수준과 세부 사항들을 미리 알고 있어야 하기 때문에 현실 세계와 같은 직접적인 접근 방식으로 총 가격을 구하기 어렵다.

어떻게 하는 게 좋을까? 😭

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/composite-pattern-structure.png?raw=true 'Result')

- 복합체 패턴를 적용하면, 총 가격을 계산하는 메서드가 선언된 공통 인터페이스를 통해 제품 및 상자 클래스들과 작업해볼 수 있다.
  - 제품: 단순히 제품 가격 반환
  - 상자: 상자에 포함된 각 항목과 가격을 확인 후 상자의 총 가격 반환
- 상자 안에 상자가 있는 객체 트리의 모든 컴포넌트들에 대해 재귀적으로 행동을 실행
  - 메서드를 호출하면 객체들은 트리 아래로 요청을 전달

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/composite-pattern-practice.png?raw=true'Result')

[Composite Pattern Practice](https://github.com/jihunparkme/GoF-Design-Pattern/tree/main/src/main/java/com/pattern/design/structuralDesignPatterns/composite)

.

**`Apply`**

- 트리와 같은 객체 구조를 구현해야 할 경우
- 클라이언트 코드가 단순 요소, 복합 요소들을 모두 균일하게 처리하도록 하고 싶을 경우
  - 모든 요소들은 공통 인터페이스를 공유

.

**`pros and cons`**

장점.
- 다형성과 재귀를 통해 복잡한 트리 구조를 편리하게 작업
- 개방/폐쇄 원칙(OCP). 객체 트리와 작동하는 기존 코드를 훼손하지 않고 앱에 새로운 요소 유형들을 도입 가능

단점.
- 기능이 너무 다른 클래스들에는 공통 인터페이스를 제공하기 어려울 수 있음
- 어떤 경우에는 컴포넌트 인터페이스를 과도하게 일반화해야 하여 이해하기 어렵게 만들어질 수 있음

.

## Decorator

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true'Result')

.

**`Problem`**

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true 'Result')

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true'Result')

[Decorator Pattern Practice]()

.

**`Apply`**

.

**`pros and cons`**

.


























## Facade

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true'Result')

.

**`Problem`**

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true 'Result')

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true'Result')

[XXX Pattern Practice]()

.

**`Apply`**

.

**`pros and cons`**

.

## Flyweight

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true'Result')

.

**`Problem`**

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true 'Result')

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true'Result')

[XXX Pattern Practice]()

.

**`Apply`**

.

**`pros and cons`**

.

## Proxy

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true'Result')

.

**`Problem`**

.

**`Solution`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true 'Result')

.

**`Practice`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/gof-design-pattern/.png?raw=true'Result')

[XXX Pattern Practice]()

.

**`Apply`**

.

**`pros and cons`**

.

# Behavioral Design Patterns

## Cain of Responsibility

## Command

## Iterator

## Mediator

## Memento

## Observer

## State

## Strategy

## Template Method

## Visitor




