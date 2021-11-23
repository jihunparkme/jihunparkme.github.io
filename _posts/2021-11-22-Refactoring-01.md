---
layout: post
title: Refactoring Chapter 1,2
summary: Chapter 1. 리펙터링: 첫 번째 예시 / Chapter 2. 리펙터링 원칙
categories: (Book)Refactoring
featured-img: refactoring
# mathjax: true
---

# Refactoring

# Chapter 1. 리펙터링: 첫 번째 예시

```python
'프로그램이 새로운 기능을 추가하기에 편한 구조가 아니라면, 먼저 기능을 추가하기 쉬운 형태로 리팩터링하고 나서 원하는 기능을 추가하자.'
```

- 여러 함수와 프로그램 요소로 재구성

## 리팩터링의 첫 단계

```python
'리팩터링하기 전에 제대로 된 테스트부터 마련한다. 테스트는 반드시 자가진단하도록 만든다.'
```

```python
'리팩터링은 프로그램 수정을 작은 단계로 나눠 진행한다. 그래서 중간에 실수하더라도 버그를 쉽게 찾을 수 있다.'
```

```python
'컴퓨터가 이해하는 코드는 바보도 작성할 수 있다. 사람이 이해하도록 작성하는 프로그래머가 진정한 실력자다.'
```

- 조금씩 변경하고 매번 테스트하는 것은 리팩터링 절차의 핵심이다. (`컴파일-테스트-커밋`)

- 임시 변수는 자신이 속한 루틴에서만 의미가 있어서 루틴이 길고 복잡해진다. 그러므로 `함수로 추출해서 제거`하는 것이 좋다.

- 함수 추출 Example

  1. `반복문 쪼개기`로 변수 값을 누적시키는 부분 분리

     ```javascript
     function statment(invoice, plays) {
         // 일부 코드 생략
         
         let totalAmount = 0;
         let volumeCredits = 0;
         for (let perf of invoice.performances) {
             result += `${perf.play.name}: ${usd(perf.amount)} (${perf.audience} seats)\n`;
             totalAmount += amountFor(perf);
         }
         for (let perf of invoice.performances) { // 값 누적 로직을 별도 for 문으로 분리
             volumeCredits += volumeCreditsFor(perf);
         }
         result += `point: ${volumeCredits}점\n`
        	return result;
     }
     ```

  2. `문장 슬라이스하기`로 변수 초기화 문장을 변수 값 누적 코드 바로 앞으로 옮기기

     ```javascript
     function statment(invoice, plays) {
         // 일부 코드 생략
         
         let totalAmount = 0;
         for (let perf of invoice.performances) {
             result += `${perf.play.name}: ${usd(perf.amount)} (${perf.audience} seats)\n`;
             totalAmount += amountFor(perf);
         }
         
         let volumeCredits = 0; // 변수 선언(초기화)을 반복문 앞으로
         for (let perf of invoice.performances) {
             volumeCredits += volumeCreditsFor(perf);
         }
         result += `point: ${volumeCredits}점\n`
        	return result;
     }
     ```

  3. `함수 추출하기`로 계산 부분을 별도 함수로 추출

     ```javascript
     function statment(invoice, plays) {
         // 일부 코드 생략
         
         let totalAmount = 0;
         for (let perf of invoice.performances) {
             result += `${perf.play.name}: ${usd(perf.amount)} (${perf.audience} seats)\n`;
             totalAmount += amountFor(perf);
         }
         
         let volumeCredits = totalVolumeCredits(); // 값 계산 로직을 함수로 추출
         result += `point: ${volumeCredits}점\n`
        	return result;
     }
     
     function totalVolumeCredits() {
         let result = 0;
         for (let perf of invoice.performances) {
             result += volumeCreditsFor(perf);
         }
         return result;
     }
     ```

  4. `변수 인라인하기`로 임시 변수 제거

     ```javascript
     function statment(invoice, plays) {
         // 일부 코드 생략
     
         let totalAmount = 0;
         for (let perf of invoice.performances) {
             result += `${perf.play.name}: ${usd(perf.amount)} (${perf.audience} seats)\n`;
             totalAmount += amountFor(perf);
         }
         result += `point: ${totalVolumeCredits()}점\n` // 변수 인라인
        	return result;
     }
     ```

```python
'코드를 모듈화하면 각 부분이 하는 일과 그 부분들이 맞물려 돌아가는 과정을 파악하기 쉬워진다.'
```

```python
'리팩터링은 대부분 코드가 하는 일을 파악하는 데서 시작한다. 그래서 코드를 읽고, 개선점을 찾고, 리팩터링 작업을 통해 개선점을 코드에 반영하는 식으로 진행한다.'
-> '좋은 코드를 가늠하는 확실한 방법은 `얼마나 수정하기 쉬운가`다.
```

- 적절한 이름의 작은 함수들로 만드는 방식을 선호하는 마틴 파울러의 방식을 따라해보자.

## Result Code

**plays.json**

```json
{
    "hamlet": {"name": "Hamlet", "type": "tragedy"},
    "as-like": {"name": "As You Like It", "type": "comedy"},
    "othello": {"name": "Othello", "type": "tragedy"}
};
```

**invoices.json**

```json
[
    {
        "customer": "BigCo",
        "performances": [
            {
                "playID": "hamlet",
                "audience": 55
            },
            {
                "playID": "as-like",
                "audience": 35
            },
            {
                "playID": "othello",
                "audience": 40
            }
        ]
    }
];
```

**statement.js** 

- 출력 구조 코드

```javascript
export {statement}
export {htmlStatement}

import {createStatementData} from './createStatementData.js'

function usd(aNumber) {
    return new Intl.NumberFormat("en-US",
        {
            style: "currency", currency: "USD",
            minimumFractionDigits: 2
        }).format(aNumber / 100);
}

function renderPlainText(statementData) {
    let result = `Statement for ${statementData.customer}\n`;
    for (let perf of statementData.performances) {
        result += `  ${perf.play.name}: ${usd(perf.amount)} (${perf.audience} seats)\n`;
    }

    result += `Amount owed is ${usd(statementData.totalAmount)}\n`;
    result += `You earned ${statementData.totalVolumeCredits} credits\n`;
    return result;
}

function renderHtml(data) {
    let result = `<h1>Statement for ${data.customer}</h1>\n`;
    result += "<table>\n";
    result += "<tr><th>play</th><th>seats</th><th>cost</th></tr>";
    for (let perf of data.performances) {
        result += `  <tr><td>${perf.play.name}</td><td>${perf.audience}</td>`;
        result += `<td>${usd(perf.amount)}</td></tr>\n`;
    }
    result += "</table>\n";
    result += `<p>Amount owed is <em>${usd(data.totalAmount)}</em></p>\n`;
    result += `<p>You earned <em>${data.totalVolumeCredits}</em> credits</p>\n`;
    return result;
}

function htmlStatement(invoice, plays) {
    return renderHtml(createStatementData(invoice, plays));
}

function statement(invoice, plays) {
    return renderPlainText(createStatementData(invoice, plays));
}
```

**createStatementData.js**

- 데이터 구조 코드

```javascript
export {createStatementData}

/**
 * 조건부 로직을 다형성으로
 */
class PerformanceCalculator {
    constructor(aPerformance, aPlay) {
        this.performance = aPerformance;
        this.play = aPlay; // 공연 정보
    }
    
    get amount() {
        throw new Error('subclass responsibility');
    }
}

class TragedyCalculator extends PerformanceCalculator {
    get amount() { // 공연료 계산
        let result = 40000;
        if (this.performance.audience > 30) {
            result += 1000 * (this.performance.audience - 30);
        }
        return result;
    }

    get volumeCredits() { // 적립 포인트 계산
        return Math.max(this.performance.audience - 30, 0);
    }
}

class ComedyCalculator extends PerformanceCalculator {
    get amount() {
        let result = 30000;
        if (this.performance.audience > 20) {
            result += 10000 + 500 * (this.performance.audience - 20);
        }
        result += 300 * this.performance.audience;
        return result;
    }

    get volumeCredits() {
        let volumeCredits = Math.max(this.performance.audience - 30, 0);
        // add extra credit for every ten comedy attendees
        volumeCredits += Math.floor(this.performance.audience / 5);
        return volumeCredits
    }
}
/* End of Class */

function createPerformanceCalculator(aPerformance, aPlay) {
    switch (aPlay.type) {
        case "tragedy":
            return new TragedyCalculator(aPerformance, aPlay);
        case "comedy" :
            return new ComedyCalculator(aPerformance, aPlay);
        default:
            throw new Error(`unknown type: ${aPlay.type}`);
    }
    //장르가 추가되면 해당 장르의 서브클래스를 작성하고 여기에 추가해주면 된다.
    //(같은 타입의 다형성을 기반으로 실행되는 함수가 많을수록 이렇게 구성하는 쪽이 유리)
}

function createStatementData(invoice, plays) {
    let statementData = {};
    statementData.customer = invoice.customer;
    statementData.performances = invoice.performances.map(enhancePerformance);
    statementData.totalVolumeCredits = totalVolumeCredits(statementData);
    statementData.totalAmount = totalAmount(statementData);
    return statementData;

    function enhancePerformance(aPerformance) {
        const calculator = createPerformanceCalculator(aPerformance, playFor(aPerformance));
        const result = Object.assign({}, aPerformance);
        result.play = calculator.play
        result.amount = calculator.amount; // 함수 인라인으로 class 함수 이용
        result.volumeCredits = calculator.volumeCredits;
        return result;
    }


    function totalVolumeCredits(statementData) {
        return statementData.performances.reduce((total, performance) => total + performance.volumeCredits, 0) // 반복문 파이프라인
    }

    function totalAmount(statementData) {
        return statementData.performances.reduce((total, aPerformance) => total + aPerformance.amount, 0)
    }

    function playFor(aPerformance) {
        return plays[aPerformance.playID];
    }
}
```

# Chapter 2. 리펙터링 원칙

## 리팩터링 정의

```python
[명사] '소프트웨어의 겉보기 동작은 그대로 유지한 채, 코드를 이해하고 수정하기 쉽도록 내부 구조를 변경하는 기법'

[동사] '소프트웨어의 겉보기 동작은 그대로 유지한 채, 여러 가지 리팩터링 기법을 적용해서 소프트웨어를 재구성하다.'
```

- 리팩터링하면
  - 소프트웨어 설계가 좋아진다
  - 소프트웨어를 이해하기 쉬워진다 (버그를 찾기 쉬워진다)
  - 버그를 쉽게 찾을 수 있다
  - 프로그래밍 속도를 높일 수 있다

```python
'보기 싫은 코드를 발견하면 리팩터링하자. 그런데 잘 작성된 코드 역시 수많은 리팩터링을 거쳐야 한다.''
```

## 언제 리팩터링해야 할까?

- 준비를 위한 리팩터링 : 기능을 쉽게 추가하게 만들기
- 이해를 위한 리팩터링 : 코드를 이해하기 쉽게 만들기
- 쓰레기 줍기 리팩터링
- 계획된 리팩터링과 수시로 하는 리팩터링
- 오래 걸리는 리팩터링
- 코드 리뷰에 리팩터링 활용하기

## 리팩터링 시 고려할 문제

- 새 기능 개발 속도 저하
  - 리팩터링은 개발 기간을 단축하고자 하는 것이다. 
  - 기능 추가 시간을 줄이고, 버그 수정 시간을 줄여준다.
- 코드 소유권
  - 코드 소유권을 팀에 두는 것을 선호한다.
- 브랜치
  - 팀원마다 코드베이스의 branch를 하나씩 맡아서 작업하다 결과물이 쌓이면 master branch에 통합해서 공유하자. (지속적 통합 적용, CI)
- 테스팅
  - 자가 테스트 코드를 갖추자.
- 레거시 코드
  - 테스트를 보강하자.
- 데이터베이스

## 리팩터링과 성능

리팩터링은 성능 좋은 소프트웨어를 만드는 데 기여한다.

**빠른 소프트웨어를 작성하는 방법**

- 시간 예산 분배 방식
  - 설계를 여러 컴포넌트로 나눠서 컴포넌트마다 자원 예산을 할당
- 끊임없이 관심을 기울이자
- 의도적으로 성능 최적화에 돌입하기 전까지 성능에 신경 쓰지 않고 코드를 다루기 쉽게 만드는 데 집중하자.

**리펙터링과 최적화의 관계**

- 리팩터링을 잘 해두면 서능 튜닝에 투입할 시간을 벌 수 있다.
- 리팩터링이 잘 되어 있는 프로그램은 성능을 더 세밀하게 분석할 수 있다.

## 참고 도서

[리팩터링 워크북](http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode=9788991268159)

[패턴을 활용한 리팩터링](http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode=9788991268920)

# Reference

[참고](https://github.com/yujeongJeon/yujeongJeon.github.io)