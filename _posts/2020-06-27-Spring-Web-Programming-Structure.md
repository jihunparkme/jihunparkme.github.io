---
layout: post
title: Spring Web Programming Structure
summary: Let's learn Spring Framework
categories: Spring
featured-img: spring
# mathjax: true
---

# Table of Contents

* [웹 프로그래밍 설계 모델](#웹-프로그래밍-설계-모델)
  * [스프링 MVC Framework 기반의 웹 프로그래밍-구조](#스프링-MVC-Framework-기반의-웹-프로그래밍-구조)
  * [스프링 MVC framework 설계 구조](#스프링-MVC-framework-설계-구조)
  * [DispatcherServlet 설정](#DispatcherServlet-설정)
  * [Controller 객체](#Controller-객체)
  * [View 객체](#View-객체)
  * [전체적인 웹 프로그래밍 구조](#전체적인-웹-프로그래밍-구조)
  * [Final Pjt Structure](#Final-Pjt-Structure)

<br/>

<br/>

# 웹-프로그래밍-설계-모델

## 스프링-MVC-Framework-기반의-웹-프로그래밍-구조

- Model 1

  - JSP, Service, DAO를 한 파일로 관리
    - 개발 속도는 빠르지만 여러 언어를 하나의 문서에 다 작성하다보니 유지보수가 어려움

  <img src="..\post_img\M1.jpg" alt="img" style="zoom: 70%;" />

  - Request
    1. 사용자가 필요한 정보를 Web에 request
    2. WAS는 필요한 데이터를 DB에 request
  - Response
    1. DB로부터 response한 데이터를 WAS에서 가공한 후
    2. 사용자는 WAS로부터 정보를 response



- Model 2

  - Model 1 의 단점을 보완하기 위해 나온 모델
    - 각 기능을 MVC를 기본으로 모듈화 (쉬운 유지보수)
      - Model : DB와 통신하기 위한 모듈
      - View : 사용자에게 보여주기 위한 모듈
      - Controller : Service(기능)와 View를 컨트롤하기 위한 모듈

  <img src="..\post_img\M2.jpg" alt="img" style="zoom: 70%;" />

  - Request
    1. 사용자가 필요한 정보를 Web에 request 하면
    2. 먼저 Controller가 사용자에게 필요한 정보를 제공해줄 수 있는 Service(기능)를 선택한 후
    3. Service를 제공해주기 위해 필요한 데이터를 데이터베이스에 request 하기 위해
    4. 데이터베이스 접근을 위한 DAO 모듈에 요청 후 Model이라는 객체를 통해 DB와 통신
  - Response 
    1. Model이라는 객체를 통해 DB와 통신하면서 필요한 데이터를 response
    2. Service는 DB로부터 데이터를 response한 후 
    3. Controller는 Service를 response하고
    4. 이 Service를 사용자에게 다시 response해주기 위해
    5. Controller는 View 객체(JSP)를 통해 사용자에게 response

<br/>

## 스프링-MVC-framework-설계-구조

<img src="..\post_img\MVC.jpg" alt="img" style="zoom: 70%;" />

- 사용자는 필요한 정보를 DispatcherServlet에게 요청
- DispatcherServlet은 
  1. 받은 요청을 `HandlerMapping`에 토스
     - HandlerMapping은 다양한 Controller 중 <u>적합한 Controller를 선택</u>
  2. 다시 `HandlerAdapter`에 토스
     - HandlerAdapter는 해당 Controller가 가지고 있는 다양한 method 중 <u>적합한 method를 선택</u>
     - 데이터가 담긴 Model을 반환
  3. 다음 `ViewResolver`에 토스
     - ViewResolver는 받은 Model에 <u>적합한 JSP 문서를 선택</u>
  4. 다음 `View`에 토스
     - View는 받은 JSP 문서로 response 생성
  5. 사용자에게 response 
- 개발자가 실질적으로 개발해야할 부분은 Controller와 View
  - Controller는 Back-End
  - View는 Front-End

<br/>

## DispatcherServlet-설정

Web application 진입의 첫 번째 관문

- web.xml에 servlet 매핑

  ```xml
  <servlet> 
      <servlet-name>서블릿 별칭</servlet-name> 
      <servlet-class>서블릿명(패키지 이름을 포함한 전체서블릿명)</servlet-class> 
  </servlet> 
  
  <servlet-mapping> 
      <servlet-name>서블릿별칭</servlet-name> 
      <url-pattern>/맵핑명</url-pattern> 
  </servlet-mapping>
  ```

- 적용

  ```xml
  <servlet> 
      <servlet-name>appServlet</servlet-name> 
      <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class> 
      <init-param> 
          <param-name>contextConfigLocation</param-name> 
          <param-value>/WEB-INF/spring/appServlet/servlet-context.xml</param-value> 
      </init-param> 
      <load-on-startup>1</load-on-startup> 
  </servlet>
  
  <servlet-mapping> 
      <servlet-name>appServlet</servlet-name> 
      <url-pattern>/</url-pattern> 
  </servlet-mapping>
  ```

  1. DispatcherServlet을 appServlet로 이름을 지정

     - ```xml
       <servlet-name>appServlet</servlet-name> 
       ```

  2. 웹어플리케이션에서 사용자로부터 request가 발생하면 가장 먼저 DispatcherServlet을 사용자의 요청을 받음.  따라서 개발자는 DispatcherServlet을 서블릿으로 등록 해주는 과정을 설정

     - ```xml
       <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
       ```

  3. DispatcherServlet이 등록될 때 init-param, 초기 파라미터에 스프링 설정 파일도 설정

     - Spring Container가 생성되면 HandlerMapping, HandlerAdapter, ViewResolver도 Spring Container 안에 자동으로 생성
     - 스프링 설정 파일을 명시하지 않을 경우, 자동으로 appServlet-context.xml 이라는 파일을 설정

       - 일반적으로 초기 파라미터로 스프링 설정 파일을 설정 (servlet-context.xml파일이 스프링 설정의 역할)

         ```xml
         <param-value>/WEB-INF/spring/appServlet/servlet-context.xml</param-value> 
         ```

  4. appServlet은 루트(/)에 들어온 모든 기능을 처리

        - 사용자의 모든 요청을 받기 위해서 서블릿 맵핑 경로는 ‘/’로설정

        - ```xml
          <servlet-name>appServlet</servlet-name> 
          <url-pattern>/</url-pattern> 
          ```

<br/>

## Controller-객체

`DispatcherServlet` <- `HandlerAdapter` -> `Controller`

Controller는 (Server, Dao-DB)와 연결되어있고 (Model, View)를 response

- @Controller

  - Controller는 개발자가 직접 만들어줘야 함

  - servlet-context.xml 스프링 설정 파일에 annotation-driven TAG 추가

    - spring container를 사용하기 위한 여러 class들이 빈 객체로 설정 파일로 존재
    - @Controller annotation 사용을 위함

    ```xml
    <annotation-driven />
    ```

  - Controller로 사용할 객체는 class로 정의하고 class 위에 @Controller annotation 추가

    - 이 class 파일은 Controller 기능을 수행

    ```java
    @Controller
    public class HomeController {
        // ...
    }
    ```

- @RequestMapping
  - @Controller 안에 있는 method들은 @RequestMapping을 이용하여

  - 사용자로부터 들어오는 요청에 적절한 method가 실행될 수 있도록 매핑

    - Ex) `https://localhost:3000/example/success` 를 request할 경우,
    
    ```java
    @RequestMapping("/success")
    public string success(Model model) {
        return "success";
  }
    ```
  
- Model 타입의 파라미터

    - Controller에서 모든 작업이 완료되고 Model과 View를 response하기 위해

        - method의 파라미터로 model 객체 명시

          ```java
          @RequestMapping("/success")
          public string success(Model model) {
              // ...
          }
          ```

        - Model 데이터를 View에서 사용하기 위해 setAttribute()

          ```java
          model.setAttribute("tmpData", "model has data!!")
          ```

    - 개발자는 Model 객체에 데이터를 담아서 DispatcherServlet에 전달할 수 있음
    - DispatcherServler에 전달된 Model데이터는 View에서 가공되어 클라이언트한테 응답

<br/>

## View-객체

`DispatcherServlet` <- `ViewResolver` -> `View`

- spring 설정 파일에 InternalResourceViewResolver라는 Bean 객체 생성

  - 해당하는 적합한 View를 선택

  ```xml
  <beans:bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
      <beans:property name="prefix" value="/WEB-INF/views/" /> 
      <beans:property name="suffix" value=".jsp" /> 
  </beans:bean>
  ```

- 적합한 View를 선택하는 방법은

  - @Controller 안에 매핑되는 mothod의 return값과

    - Ex) `https://localhost:3000/example/success` 를 request할 경우,
  
    ```java
    @RequestMapping("/success")
    public string success(Model model) {
        return "success";
  }
    ```
  
  - InternalResourceViewResolver에서 만들어준 prefix, suffix값이 합쳐져서 
  
  - /WEB-INF/views/success.jsp 라면 JSP 파일을 찾아주게 된다.
  
    <img src="..\post_img\success.JPG" alt="img" style="zoom: 80%;" />

<br/>

## 전체적인-웹-프로그래밍-구조

<img src="..\post_img\structure.jpg" alt="img" style="zoom: 100%;" />

1. 사용자가 `https://localhost:3000/example/success` 를 요청하면 DispatcherServlet이 받음
   - DispatcherServlet은 Spring Framework에 있는 것이고, web.xml에서 servlet 등록을 하고, 하면서 초기 파라미터로 spring 설정 파일을 설정
2. `HandlerMapping`을 통해 적합한 Controller를 선택
   - Controller는 @Controller annotation으로 생성
3. 적합한 Controller를 찾았다면 다시 DispatcherServlet으로
4. `HandlerAdapter`를 통해 해당 Controller로부터 적합한 Method를 선택
   - @RequestMapping('사용자 요청 값') annotation 탐색
   - Method가 실행되면 Service, DAO, DB가 있을 것이고,
5. 적합한 Method를 찾았다면 Model과 View를  DispatcherServlet로
6. Model과 View를 가지고 `ViewResolver`를 통해 적합한 View를 선택
   - prefix + '사용자 요청 값' + suffix.jsp 실행
7. 적합한 View에 데이터를 씌워서 JSP로 response

<br/>

<br/>

## Final-Pjt-Structure

```cmd
> src
	> main
		> java.com.ho.lec
			> config
				# DBConfig.java
            > member
            	> controller
            		# MemberController.java
            	> dao
            		# IMemberDao.java
            		# MemberDao.java
            	> service
            		# IMemberService.java
            		# MemberService.java
            	# Member.java
            	# MemberLoginInterceptor.java
           	# HomeController.java
        > resources
        	> META-INF
        	# log4j.xml
        > webapp
        	> resources\css
        		# normal.css
        	> WEB-INF
        		> classes
        		> spring
        			> appServlet
        				# servlet-context.xml
        			# root-context.xml
        		> views
        			> member
        				# joinForm.jsp
        				# joinOk.jsp
        				# loginForm.jsp
        				# loginOk.jsp
        				# ...
        			# index.jsp
        		# web.xml
# pom.xml
```

