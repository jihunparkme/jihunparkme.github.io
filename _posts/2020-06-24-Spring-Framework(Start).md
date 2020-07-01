---
layout: post
title: Spring Framework(Start)
summary: Let's learn Spring Framework
categories: Spring
featured-img: spring
# mathjax: true
---

# Table of Contents

* [개요 소개](#개요-소개)
  * [스프링 개요](#스프링-개요)
* [스프링 프레임워크](#스프링-프레임워크)
  * [개발 환경 구축](#개발-환경-구축) : pom.xml
* [프로젝트 생성](#프로젝트-생성)
  * [test](#test)

<br/>

<br/>

# 개요-소개

## 스프링-개요

#### 주요 기능
- DI
- AOP
- MVC
- JDBC

#### 스프링 프레임워크에서 제공하고 있는 모듈
- spring-core : 스프링의 핵심인 DI(Dependency Injection)와 IoC(Inversion of Control)를 제공 
- spring-aop : AOP구현 기능 제공 
- spring-jdbc : 데이터베이스를 쉽게(적은 양의 코드) 다룰 수 있는 기능 제공 
- spring-tx : 스프링에서 제공하는 트랜잭션 관련 기능 제공 
- spring-webmvc : 스프링에서 제공하는 컨트롤러(Controller)와 뷰(View)를 이용한 스프링MVC 구현 기능 제공

#### 스프링 컨테이너(IoC)
- 스프링에서 객체를 생성하고 조립하는 컨테이너(container)로, 컨테이너를 통해 생성된 객체를 빈(Bean)이라고 부름

<br/>

<br/>

# 스프링-프레임워크

## 개발-환경-구축

#### 폴더 및 pom.xml 파일 이해
- pjt project : 스프링 프로젝트
- pjt/src/main/java : .java 파일 관리
  - 앞으로 만들어지는 자바 파일들이 관리되는 폴더이
- pjt/src/main/resources : 자원파일 관리
  - 스프링 설정 파일(XML) 또는 프로퍼티 파일 등이 관리

pom.xml 파일은 메이븐 설정파일로 메이븐은 라이브러리를 연결해주고, 빌드를 위한 플랫폼

pom.xml에 의해서 필요한 라이브러리만 다운로드 해서 사용

<br/>

<br/>

# 프로젝트-생성

## test

스프링 방식의 ‘의존’을 이용하기 위해서는 Main에서 TransportationWalk 객체를 직접 생성하지 않고, 스프링 설정 파일(XML)을 이용

가장 큰 차이점은 Java 파일에서 이용한 new 연산자를 이용하지 않고 스프링 설정파일(XML)을 이용

1. 스프링 설정 파일(applicationContext.xml)에 Bean tag로 명시된 tag들이
2. GenericXmlApplicationContext  class에 의해
3.  Spring Containr 안에 객체로 생성
   - DI가 적용된 객체들도 존재
4. 이렇게 생성된 Bean 객체들은 getBean() method로 사용

```xml
<?xml version="1.0" encoding="UTF-8"?>

<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
 		http://www.springframework.org/schema/beans/spring-beans.xsd">

	<!-- 객체(Bean) 등록 -->
	<bean id="tWalk" class="lec03Pjt001.TransportationWalk" />
	
</beans>
```

```java
package lec03Pjt001;

import org.springframework.context.support.GenericXmlApplicationContext;

public class MainClass {

	public static void main(String[] args) {
		
///////////////////////
//일반 java framework
///////////////////////
		// TransportationWalk transportationWalk = new TransportationWalk();
		// transportationWalk.move();
		

///////////////////////
//spring framework
///////////////////////
		// xml 파일을 이용하여 객체를 생성

		/*
		1. Spring Container 생성
		xml을 사용하므로 GenericXmlApplicationContext class 를 사용
		이 class를 생성할 때, 그 안쪽에 리소스(xml)의 내용을 작성.
		*/
		GenericXmlApplicationContext ctx = 
				new GenericXmlApplicationContext("classpath:applicationContext.xml");
		
		/* 
		컨테이너에서 어떠한 객체를 가져올지 ID와 dataType 을 작성
		*/
		TransportationWalk transportationWalk = 
            ctx.getBean("tWalk", TransportationWalk.class);

		transportationWalk.move();
		
        // 외부 자원은 반환하여 리소스를 남기지 않도록 해준다.
		ctx.close();
	}
}
```
