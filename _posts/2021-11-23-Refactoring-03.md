---
layout: post
title: 코드에서 나는 악취
summary: Refactoring  Chapter 3.코드에서 나는 악취
categories: (Book)Refactoring
featured-img: refactoring
# mathjax: true
---

# Refactoring

# Chapter 3. 코드에서 나는 악취

악취와 리팩터링 기법

## 가변 데이터

`변수를 캡슐화하자. (getter/setter)`

`하나의 변수에 용도가 다른 값이 저장된다면 쪼개자.`

`갱신 코드는 다른 코드와 떨어뜨려 놓자.`

`변수로부터 얻어지는 파생 변수는 질의 함수로 바꾸자.`

`변수를 갱신하는 코드들의 스코프를 제한하자.`

`객체 내부의 객체라면 참조를 값으로 바꾸자.`

- [변수 캡슐화하기](https://jihunparkme.github.io/Refactoring-06/#%EB%B3%80%EC%88%98-%EC%BA%A1%EC%8A%90%ED%99%94%ED%95%98%EA%B8%B0)
- [변수 쪼개기](https://jihunparkme.github.io/Refactoring-09/#%EB%B3%80%EC%88%98-%EC%AA%BC%EA%B0%9C%EA%B8%B0)
- [문장 슬라이드하기](https://jihunparkme.github.io/Refactoring-08/#%EB%AC%B8%EC%9E%A5-%EC%8A%AC%EB%9D%BC%EC%9D%B4%EB%93%9C%ED%95%98%EA%B8%B0)
- [함수 추출하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)
- [질의 함수와 변경 함수 분리하기](https://jihunparkme.github.io/Refactoring-11/#%EC%A7%88%EC%9D%98-%ED%95%A8%EC%88%98%EC%99%80-%EB%B3%80%EA%B2%BD-%ED%95%A8%EC%88%98-%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0)
- [세터 제거하기](https://jihunparkme.github.io/Refactoring-11/#%EC%84%B8%ED%84%B0-%EC%A0%9C%EA%B1%B0%ED%95%98%EA%B8%B0)
- [파생변수를 질의 함수로 바꾸기](https://jihunparkme.github.io/Refactoring-09/#%ED%8C%8C%EC%83%9D-%EB%B3%80%EC%88%98%EB%A5%BC-%EC%A7%88%EC%9D%98-%ED%95%A8%EC%88%98%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [여러 함수를 클래스로 묶기](https://jihunparkme.github.io/Refactoring-06/#%EC%97%AC%EB%9F%AC-%ED%95%A8%EC%88%98%EB%A5%BC-%ED%81%B4%EB%9E%98%EC%8A%A4%EB%A1%9C-%EB%AC%B6%EA%B8%B0)
- [여러 함수를 변환 함수로 묶기](https://jihunparkme.github.io/Refactoring-06/#%EC%97%AC%EB%9F%AC-%ED%95%A8%EC%88%98%EB%A5%BC-%EB%B3%80%ED%99%98-%ED%95%A8%EC%88%98%EB%A1%9C-%EB%AC%B6%EA%B8%B0)
- [참조를 값으로 바꾸기](https://jihunparkme.github.io/Refactoring-09/#%EC%B0%B8%EC%A1%B0%EB%A5%BC-%EA%B0%92%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)

## 거대한 클래스

`클래스가 너무 많은 일을 담당하면 필드 수가 늘어나고 중복 코드가 생기기 쉽다.`

`연관된 필드를 묶고 상속 관계의 클래스로 추출하자.`

`코드량이 너무 많다면 중복을 제거하고 작은 메서드로 추출하자.`

- [클래스 추출하기](https://jihunparkme.github.io/Refactoring-07/#%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)
- [슈퍼클래스 추출하기](https://jihunparkme.github.io/Refactoring-12/#%EC%8A%88%ED%8D%BC%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)
- [타입 코드를 서브클래스로 바꾸기](https://jihunparkme.github.io/Refactoring-12/#%ED%83%80%EC%9E%85-%EC%BD%94%EB%93%9C%EB%A5%BC-%EC%84%9C%EB%B8%8C%ED%81%B4%EB%9E%98%EC%8A%A4%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)

## 기능 편애

`모듈 안에서의 상호작용은 늘리고, 모듈끼리의 상호 작용은 최소화해야 하는데, 이것이 제대로 이루어지지 않은 경우`

`해당 함수가 원하는 적절한 모듈로 옮겨주자.`

- [함수 옮기기](https://jihunparkme.github.io/Refactoring-08/#%ED%95%A8%EC%88%98-%EC%98%AE%EA%B8%B0%EA%B8%B0)
- [함수 추출하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)

## 기본형 집착

`기본형만 고집하지 말고 클래스로 만들어서 사용하자.`

- [기본형을 객체로 바꾸기](https://jihunparkme.github.io/Refactoring-07/#%EA%B8%B0%EB%B3%B8%ED%98%95%EC%9D%84-%EA%B0%9D%EC%B2%B4%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [타입 코드를 서브클래스로 바꾸기](https://jihunparkme.github.io/Refactoring-12/#%ED%83%80%EC%9E%85-%EC%BD%94%EB%93%9C%EB%A5%BC-%EC%84%9C%EB%B8%8C%ED%81%B4%EB%9E%98%EC%8A%A4%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [조건부 로직을 다형성으로 바꾸기](https://jihunparkme.github.io/Refactoring-10/#%EC%A1%B0%EA%B1%B4%EB%B6%80-%EB%A1%9C%EC%A7%81%EC%9D%84-%EB%8B%A4%ED%98%95%EC%84%B1%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [클래스 추출하기](https://jihunparkme.github.io/Refactoring-07/#%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)
- [매개변수 객체 만들기](https://jihunparkme.github.io/Refactoring-06/#%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98-%EA%B0%9D%EC%B2%B4-%EB%A7%8C%EB%93%A4%EA%B8%B0)

## 기이한 이름

`이름만 보고도 무슨 일을 하고 어떻게 사용해야 하는지 명확하게 알 수 있도록 신경쓰자.`

- [함수 선언 바꾸기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%84%A0%EC%96%B8-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [변수 이름 바꾸기](https://jihunparkme.github.io/Refactoring-06/#%EB%B3%80%EC%88%98-%EC%9D%B4%EB%A6%84-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [필드 이름 바꾸기](https://jihunparkme.github.io/Refactoring-09/#%ED%95%84%EB%93%9C-%EC%9D%B4%EB%A6%84-%EB%B0%94%EA%BE%B8%EA%B8%B0)

## 긴 매개변수 목록

`다른 매개변수에서 값을 얻어오는 매개변수가 있다면, 매개변수를 질의 함수로 바꾸자.`

`객체를 통째로 넘기거나, 매개변수 객체를 만들어 넘기자.`

`플래그 성향의 매개변수가 있다면 함수를 나눠서 해당 매개변수를 없애자.`

`여러 함수를 클래스로 묶는다면 매개변수를 줄일 수 있다.`

- [매개변수를 질의 함수로 바꾸기](https://jihunparkme.github.io/Refactoring-11/#%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98%EB%A5%BC-%EC%A7%88%EC%9D%98-%ED%95%A8%EC%88%98%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [객체 통째로 넘기기](https://jihunparkme.github.io/Refactoring-11/#%EA%B0%9D%EC%B2%B4-%ED%86%B5%EC%A7%B8%EB%A1%9C-%EB%84%98%EA%B8%B0%EA%B8%B0)
- [매개변수 객체 만들기](https://jihunparkme.github.io/Refactoring-06/#%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98-%EA%B0%9D%EC%B2%B4-%EB%A7%8C%EB%93%A4%EA%B8%B0)
- [플래그 인수 제거하기](https://jihunparkme.github.io/Refactoring-11/#%ED%94%8C%EB%9E%98%EA%B7%B8-%EC%9D%B8%EC%88%98-%EC%A0%9C%EA%B1%B0%ED%95%98%EA%B8%B0)
- [여러 함수를 클래스로 묶기](https://jihunparkme.github.io/Refactoring-06/#%EC%97%AC%EB%9F%AC-%ED%95%A8%EC%88%98%EB%A5%BC-%ED%81%B4%EB%9E%98%EC%8A%A4%EB%A1%9C-%EB%AC%B6%EA%B8%B0)

## 긴 함수

`짧은 함수는 코드를 이해하고, 공유하고, 선택하기가 쉽다.`

`함수 이름은 동작 방식이 아니라 의도(목적)가 드러나게 짓자.`

`함수 내용과 이름의 괴리가 크지 않도록 한다.`

`함수가 매개변수와 임시 변수를 많이 사용하면 추출 작업에 방해가 된다. 따라서 임시 변수의 수를 줄이고 매개변수를 객체로 묶어 정리하자.`

`코드가 단 한 줄이라도 설명할 필요가 있다면 함수로 추출하자.`

`조건문의 case 본문을 함수 호출 문 하나로 바꾸자.`

`반복문도 독립된 함수로 만들자.`

- [함수 추출하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0) 
- [임시 변수를 질의 함수로 바꾸기](https://jihunparkme.github.io/Refactoring-07/#%EC%9E%84%EC%8B%9C-%EB%B3%80%EC%88%98%EB%A5%BC-%EC%A7%88%EC%9D%98-%ED%95%A8%EC%88%98%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [매개변수 객체 만들기](https://jihunparkme.github.io/Refactoring-06/#%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98-%EA%B0%9D%EC%B2%B4-%EB%A7%8C%EB%93%A4%EA%B8%B0)
- [객체 통째로 넘기기](https://jihunparkme.github.io/Refactoring-11/#%EA%B0%9D%EC%B2%B4-%ED%86%B5%EC%A7%B8%EB%A1%9C-%EB%84%98%EA%B8%B0%EA%B8%B0)
- [함수를 명령으로 바꾸기](https://jihunparkme.github.io/Refactoring-11/#%ED%95%A8%EC%88%98%EB%A5%BC-%EB%AA%85%EB%A0%B9%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [조건문 분해하기](https://jihunparkme.github.io/Refactoring-10/#%EC%A1%B0%EA%B1%B4%EB%AC%B8-%EB%B6%84%ED%95%B4%ED%95%98%EA%B8%B0)
- [조건부 로직을 다형성으로 바꾸기](https://jihunparkme.github.io/Refactoring-10/#%EC%A1%B0%EA%B1%B4%EB%B6%80-%EB%A1%9C%EC%A7%81%EC%9D%84-%EB%8B%A4%ED%98%95%EC%84%B1%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [반복문 쪼개기](https://jihunparkme.github.io/Refactoring-08/#%EB%B0%98%EB%B3%B5%EB%AC%B8-%EC%AA%BC%EA%B0%9C%EA%B8%B0)

## 내부자 거래

`모듈 사이에 데이터 거래가 많으면 결합도가 높아진다. 적절하게 함수와 필드를 옮겨서 결합도를 낮춰보자.`

`여러 모듈이 관심사를 공유한다면 해당 부분을 제3의 모듈로 만들자.`

`상속 구조에서 자식 클래스는 부모 클래스의 데이터에 접근하고 싶은 경우가 많은데, 부모 품을 떠나야 할 때다. 인터페이스로 연결하여 결합도를 낮추자.`

- [함수 옮기기](https://jihunparkme.github.io/Refactoring-08/#%ED%95%A8%EC%88%98-%EC%98%AE%EA%B8%B0%EA%B8%B0)
- [필드 옮기기](https://jihunparkme.github.io/Refactoring-08/#%ED%95%84%EB%93%9C-%EC%98%AE%EA%B8%B0%EA%B8%B0)
- [위임 숨기기](https://jihunparkme.github.io/Refactoring-07/#%EC%9C%84%EC%9E%84-%EC%88%A8%EA%B8%B0%EA%B8%B0)
- [서브클래스를 위임으로 바꾸기](https://jihunparkme.github.io/Refactoring-12/#%EC%84%9C%EB%B8%8C%ED%81%B4%EB%9E%98%EC%8A%A4%EB%A5%BC-%EC%9C%84%EC%9E%84%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [슈퍼클래스를 위임으로 바꾸기](https://jihunparkme.github.io/Refactoring-12/#%EC%8A%88%ED%8D%BC%ED%81%B4%EB%9E%98%EC%8A%A4%EB%A5%BC-%EC%9C%84%EC%9E%84%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)

## 데이터 뭉치

`뭉쳐 다니는 데이터들을 하나의 클래스로 묶어주자.`

- [클래스 추출하기](https://jihunparkme.github.io/Refactoring-07/#%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)
- [매개변수 객체 만들기](https://jihunparkme.github.io/Refactoring-06/#%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98-%EA%B0%9D%EC%B2%B4-%EB%A7%8C%EB%93%A4%EA%B8%B0)
- [객체 통째로 넘기기](https://jihunparkme.github.io/Refactoring-11/#%EA%B0%9D%EC%B2%B4-%ED%86%B5%EC%A7%B8%EB%A1%9C-%EB%84%98%EA%B8%B0%EA%B8%B0)

## 데이터 클래스

`Getter와 Setter, 그리고 데이터 필드로 구성된 데이터 클래스는 다른 클래스가 함부로 다루는 경우가 많다.`

`필드를 캡슐화하고, 변경하지 못하는 필드는 세터를 제거해버리자.`

`다른 클래스에서 해당 데이터 클래스의 Getter나 Setter를 사용하는 코드를 찾아서 이를 데이터 클래스로 가져올 수 있는지 살펴보고 가능하다면 옮겨보자.`

- [레코드 캡슐화하기](https://jihunparkme.github.io/Refactoring-07/#%EB%A0%88%EC%BD%94%EB%93%9C-%EC%BA%A1%EC%8A%90%ED%99%94%ED%95%98%EA%B8%B0)
- [세터 제거하기](https://jihunparkme.github.io/Refactoring-11/#%EC%84%B8%ED%84%B0-%EC%A0%9C%EA%B1%B0%ED%95%98%EA%B8%B0)
- [함수 옮기기](https://jihunparkme.github.io/Refactoring-08/#%ED%95%A8%EC%88%98-%EC%98%AE%EA%B8%B0%EA%B8%B0)
- [함수 추출하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)
- [단계 쪼개기](https://jihunparkme.github.io/Refactoring-06/#%EB%8B%A8%EA%B3%84-%EC%AA%BC%EA%B0%9C%EA%B8%B0)

## 뒤엉킨 변경

`수정할 일이 생겼을 때 여러 곳을 손봐야 하는 경우`

`맥락을 잘 구분하자.`

- [단계 쪼개기](https://jihunparkme.github.io/Refactoring-06/#%EB%8B%A8%EA%B3%84-%EC%AA%BC%EA%B0%9C%EA%B8%B0)
- [함수 옮기기](https://jihunparkme.github.io/Refactoring-08/#%ED%95%A8%EC%88%98-%EC%98%AE%EA%B8%B0%EA%B8%B0)
- [함수 추출하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)
- [클래스 추출하기](https://jihunparkme.github.io/Refactoring-07/#%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)

## 메시지 체인

`객체를 통해 다른 객체를 얻는 과정이 연쇄적으로 이어질 경우`

`getter를 통해 캡슐화로 해결하자.`

`적절하게 함수로 추출하고 위치를 옮겨 체인을 숨겨보자.`

- [위임 숨기기](https://jihunparkme.github.io/Refactoring-07/#%EC%9C%84%EC%9E%84-%EC%88%A8%EA%B8%B0%EA%B8%B0)
- [함수 추출하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)
- [함수 옮기기](https://jihunparkme.github.io/Refactoring-08/#%ED%95%A8%EC%88%98-%EC%98%AE%EA%B8%B0%EA%B8%B0)

## 반복되는 switch문

`중복된 switch문은 조건절을 하나 추가할 때마다 다른 switch문들도 모두 찾아서 함께 수정해야 한다.`

`다형성을 이용해서 악취를 없애자.`

- [조건부 로직을 다형성으로 바꾸기](https://jihunparkme.github.io/Refactoring-10/#%EC%A1%B0%EA%B1%B4%EB%B6%80-%EB%A1%9C%EC%A7%81%EC%9D%84-%EB%8B%A4%ED%98%95%EC%84%B1%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)

## 반복문

`반복문보다는 filter, map 등의 파이프라인 연산을 이용하자.`

- [반복문을 파이프라인으로 바꾸기](https://jihunparkme.github.io/Refactoring-08/#%EB%B0%98%EB%B3%B5%EB%AC%B8%EC%9D%84-%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)

## 산탄총 수술

`코드를 변경할 때마다 함께 수정해야 하는 부분이 코드 전반에 퍼져 있을 경우`

`함수와 필드를 한 모듈에 묶자.`

`여러 함수를 클래스로 묶거나, 변환 함수로 묶자.`

`코드를 재구성할 때에는 덩어리로 뭉쳐지는 것을 개의치 말자.`

- [함수 옮기기](https://jihunparkme.github.io/Refactoring-08/#%ED%95%A8%EC%88%98-%EC%98%AE%EA%B8%B0%EA%B8%B0)
- [필드 옮기기](https://jihunparkme.github.io/Refactoring-08/#%ED%95%84%EB%93%9C-%EC%98%AE%EA%B8%B0%EA%B8%B0)
- [여러 함수를 클래스로 묶기](https://jihunparkme.github.io/Refactoring-06/#%EC%97%AC%EB%9F%AC-%ED%95%A8%EC%88%98%EB%A5%BC-%ED%81%B4%EB%9E%98%EC%8A%A4%EB%A1%9C-%EB%AC%B6%EA%B8%B0)
- [여러 함수를 변환 함수로 묶기](https://jihunparkme.github.io/Refactoring-06/#%EC%97%AC%EB%9F%AC-%ED%95%A8%EC%88%98%EB%A5%BC-%EB%B3%80%ED%99%98-%ED%95%A8%EC%88%98%EB%A1%9C-%EB%AC%B6%EA%B8%B0)
- [단계 쪼개기](https://jihunparkme.github.io/Refactoring-06/#%EB%8B%A8%EA%B3%84-%EC%AA%BC%EA%B0%9C%EA%B8%B0)
- [함수 인라인하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%9D%B8%EB%9D%BC%EC%9D%B8%ED%95%98%EA%B8%B0)
- [클래스 인라인하기](https://jihunparkme.github.io/Refactoring-07/#%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%9D%B8%EB%9D%BC%EC%9D%B8%ED%95%98%EA%B8%B0)

## 상속 포기

`부모 클래스의 특정 부분을 상속받기 원치 않는 경우`

`상속하지 않을 부모 코드를 따로 분리해내어, 공통된 부분만 남도록 한다.`

`부모의 인터페이스를 따르고 싶지 않으면 아예 상속 메커니즘에서 벗어나도록, 위임 클래스를 만들고 이를 이용하도록 만들자.`

- [매서드 내리기](https://jihunparkme.github.io/Refactoring-12/#%EB%A9%94%EC%84%9C%EB%93%9C-%EB%82%B4%EB%A6%AC%EA%B8%B0)
- [필드 내리기](https://jihunparkme.github.io/Refactoring-12/#%ED%95%84%EB%93%9C-%EB%82%B4%EB%A6%AC%EA%B8%B0)
- [서브클래스를 위임으로 바꾸기](https://jihunparkme.github.io/Refactoring-12/#%EC%84%9C%EB%B8%8C%ED%81%B4%EB%9E%98%EC%8A%A4%EB%A5%BC-%EC%9C%84%EC%9E%84%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [슈퍼클래스를 위임으로 바꾸기](https://jihunparkme.github.io/Refactoring-12/#%EC%8A%88%ED%8D%BC%ED%81%B4%EB%9E%98%EC%8A%A4%EB%A5%BC-%EC%9C%84%EC%9E%84%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)

## 서로 다른 인터페이스의 대안 클래스들

`서로 다른 클래스의 두 메서드가, 하는 일은 비슷한데, 인터페이스가 다른 경우, 인터페이스를 통일시키고, 가능하다면 추출하자.`

- [함수 선언 바꾸기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%84%A0%EC%96%B8-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [함수 옮기기](https://jihunparkme.github.io/Refactoring-08/#%ED%95%A8%EC%88%98-%EC%98%AE%EA%B8%B0%EA%B8%B0)
- [슈퍼클래스 추출하기](https://jihunparkme.github.io/Refactoring-12/#%EC%8A%88%ED%8D%BC%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)

## 성의 없는 요소

`구조를 잡기 위해 사용된 프로그램 요소가 필요 없어 보인다면, 인라인으로 처리해주자.`

- [함수 인라인하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%9D%B8%EB%9D%BC%EC%9D%B8%ED%95%98%EA%B8%B0)
- [클래스 인라인하기](https://jihunparkme.github.io/Refactoring-07/#%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%9D%B8%EB%9D%BC%EC%9D%B8%ED%95%98%EA%B8%B0)
- [계층 합치기](https://jihunparkme.github.io/Refactoring-12/#%EA%B3%84%EC%B8%B5-%ED%95%A9%EC%B9%98%EA%B8%B0)

## 임시 필드

`클래스의 특정 필드가 어떨 때는 값이 설정되고, 어떨 때는 설정되지 않는 경우`

`이런 필드들은 클래스 추출하기로 옮겨주고, 관련 함수도 같이 옮겨주자.`

`이런 필드의 유효성 체크 로직은 '유효하지 않은 경우'를 위한 대안 클래스를 만들어 제거하자.`

- [클래스 추출하기](https://jihunparkme.github.io/Refactoring-07/#%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)
- [함수 옮기기](https://jihunparkme.github.io/Refactoring-08/#%ED%95%A8%EC%88%98-%EC%98%AE%EA%B8%B0%EA%B8%B0)
- [특이 케이스 추가하기](https://jihunparkme.github.io/Refactoring-10/#%ED%8A%B9%EC%9D%B4-%EC%BC%80%EC%9D%B4%EC%8A%A4-%EC%B6%94%EA%B0%80%ED%95%98%EA%B8%B0)

## 전역 데이터

`함수 스코프에 넣어주자.`

- [변수 캡슐화하기](https://jihunparkme.github.io/Refactoring-06/#%EB%B3%80%EC%88%98-%EC%BA%A1%EC%8A%90%ED%99%94%ED%95%98%EA%B8%B0)

## 주석

`주석은 탈취제가 아니다.`

`주석 대신 함수 추출하기로 특정 코드 블록을 추출해보자.`

`주석 대신 함수 이름을 바꿔보자.`

`선행 조건을 명시하고 싶다면 어서션을 추가할 수도 있다.`

- [함수 추출하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)
- [함수 선언 바꾸기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%84%A0%EC%96%B8-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [어서션 추가하기](https://jihunparkme.github.io/Refactoring-10/#%EC%96%B4%EC%84%9C%EC%85%98-%EC%B6%94%EA%B0%80%ED%95%98%EA%B8%B0)

## 중개자

`클래스가 다른 클래스에 구현을 위임하는 '중간 역할'만을 하고 있다면 직접 소통하도록 바꿔주자.`

- [중개자 제거하기](https://jihunparkme.github.io/Refactoring-07/#%EC%A4%91%EA%B0%9C%EC%9E%90-%EC%A0%9C%EA%B1%B0%ED%95%98%EA%B8%B0)
- [함수 인라인하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%9D%B8%EB%9D%BC%EC%9D%B8%ED%95%98%EA%B8%B0)
- [서브클래스를 위임으로 바꾸기](https://jihunparkme.github.io/Refactoring-12/#%EC%84%9C%EB%B8%8C%ED%81%B4%EB%9E%98%EC%8A%A4%EB%A5%BC-%EC%9C%84%EC%9E%84%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [슈퍼클래스를 위임으로 바꾸기](https://jihunparkme.github.io/Refactoring-12/#%EC%8A%88%ED%8D%BC%ED%81%B4%EB%9E%98%EC%8A%A4%EB%A5%BC-%EC%9C%84%EC%9E%84%EC%9C%BC%EB%A1%9C-%EB%B0%94%EA%BE%B8%EA%B8%B0)

## 중복 코드

`중복 내용이 있다면, 함수로 추출하여 사용하자.`

`문장 슬라이스를 통해 비슷한 로직을 한 곳에 모으고, 함수로 추출 가능한지 보자.`

`서브 클래스에 중복 내용이 있다면 상위로 위치를 올려보자.`

- [함수 추출하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0)
- [문장 슬라이드하기](https://jihunparkme.github.io/Refactoring-08/#%EB%AC%B8%EC%9E%A5-%EC%8A%AC%EB%9D%BC%EC%9D%B4%EB%93%9C%ED%95%98%EA%B8%B0)
- [메서드 올리기](https://jihunparkme.github.io/Refactoring-12/#%EB%A9%94%EC%84%9C%EB%93%9C-%EC%98%AC%EB%A6%AC%EA%B8%B0)

## 추측성 일반화

` '이거 나중에 필요할 거야'라는 생각으로 필요 없는 로직과 후킹 포인트를 만든 경우`

`하는 일 없는 추상 클래스는 합쳐버리고, 인라인 코드 활용으로 걸리적거리는 코드를 치워버리자.`

- [계층 합치기](https://jihunparkme.github.io/Refactoring-12/#%EA%B3%84%EC%B8%B5-%ED%95%A9%EC%B9%98%EA%B8%B0)
- [함수 인라인하기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%9D%B8%EB%9D%BC%EC%9D%B8%ED%95%98%EA%B8%B0)
- [클래스 인라인하기](https://jihunparkme.github.io/Refactoring-07/#%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%9D%B8%EB%9D%BC%EC%9D%B8%ED%95%98%EA%B8%B0)
- [함수 선언 바꾸기](https://jihunparkme.github.io/Refactoring-06/#%ED%95%A8%EC%88%98-%EC%84%A0%EC%96%B8-%EB%B0%94%EA%BE%B8%EA%B8%B0)
- [죽은 코드 제거하기](https://jihunparkme.github.io/Refactoring-08/#%EC%A3%BD%EC%9D%80-%EC%BD%94%EB%93%9C-%EC%A0%9C%EA%B1%B0%ED%95%98%EA%B8%B0)
