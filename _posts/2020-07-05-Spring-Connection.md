---
layout: post
title: Spring Connection
summary: Let's learn Spring Framework
categories: Spring
featured-img: spring
# mathjax: true
---

# Table of Contents

* [세션, 쿠키](#세션-쿠키)
* [Redirect, Interceptor](#Redirect,-Interceptor)
* [Database](#DataBase)
* [JDBC](#JDBC)
* [JdbcTemplate]
* [커넥션풀]

<br/>

<br/>

# 연결

## 세션-쿠키

### **Connectionless Protocol**

- 웹 서비스는 HTTP 프로토콜을 기반으로 하는데, HTTP 프로토콜은 클라이언트와 서버의 관계를 유지 하지 않는 특징이 있음

  - 서버에 연결되는 클라이언트가 수많을 경우, 서버에 연결된 클라이언트가 많아질 것이고 부화가 걸릴 수 있기 때문

  - 서버의 효율적인 운영을 위해 요청 응답 후 바로 서버 연결 해제

- 서버의 부하를 줄일 수 있는 장점은 있나, 클라이언트의 요청 시마다 서버와 매번 새로운 연결이 생성되기 때문에 일반적인 로그인 상태 유지, 장바구니 등의 기능을 구현하기 어려움

- 이러한 Connectionless Protocol의 불편함을 해결하기 위해서 세션과 쿠키를 이용

- 세션과 쿠키는 클라이언트와 서버의 연결 상태를 유지해주는 방법으로, 

  - 세션은 서버에서 연결 정보를 관리하는 반면
  - 쿠키는 클라이언트에서 연결 정보를 관리하는데 차이



### 세션(Session)

- 서버와 클라이언트 사이의 연결을 유지
- 세션은 서버에 정보를 저장
- 스프링 MVC에서 HttpServletRequest를 이용해서 세션을 이용하려면 컨트롤러의 메소드에서 파라미터로 HttpServletRequest를 받으면 된다

####  세션 생성

- HttpServletRequest를 이용한 세션 생성

```java
// MemberController.java
// ...
@RequestMapping(value = "/login", method = RequestMethod.POST)
public String memLogin(Member member, HttpServletRequest request) {

    Member mem = service.memberSearch(member);

    HttpSession session = request.getSession();
    session.setAttribute("member", mem);

    return "/member/loginOk";
}
// ...
```

- HttpSession을 이용한 세션 생성
  - HttpServletRequest와 HttpSession의 차이점은 거의 없으며, 단지 세션객체를 얻는 방법에 차이
  - HttpServletRequest는 파라미터로 HttpServletRequest를 받은 후 getSession()으로 세션을 얻음.
  - HttpSession은 파라미터로 HttpSession을 받아 세션을 바로 사용

```java
// MemberController.java
//...
@RequestMapping(value = "/login", method = RequestMethod.POST)
public String memLogin(Member member, HttpSession session) {

    Member mem = service.memberSearch(member);

    session.setAttribute("member", mem);

    return "/member/loginOk";
}
//...
```

#### 세션(Session) 삭제

- 세션을 삭제하는 방법은 세션에 저장된 속성이 더 이상 필요 없을 때 이루어지는 과정으로 주로 로그아웃 또는 회원 탈퇴 등에 사용

- 로그아웃

```java
// MemberController.java
//...
@RequestMapping("/logout")
public String memLogout(Member member, HttpSession session) {

    session.invalidate();

    return "/member/logoutOk";
}
```

- 회원탈퇴

```java
// MemberController.java
//...
@RequestMapping(value = "/remove", method = RequestMethod.POST)
public String memRemove(Member member, HttpServletRequest request) {

    service.memberRemove(member);

    HttpSession session = request.getSession();
    session.invalidate();

    return "/member/removeOk";
}
```

#### 세션 주요 메소드

- getId() : 세션 ID 반환
- setAttribute() : 세션 객체에 속성을 저장
- getAttribute() : 세션 객체에 저장된 속성을 반환
- removeAttribute() : 세션 객체에 저장된 속성을 제거
- setMaxInactiveInterval() : 세션 객체의 유지시간을 설정
- getMaxInactiveInterval() : 세션 객체의 유지시간을 반환
- invalidate() : 세션 객체의 모든 정보를 삭제

#### 세션 플로어

<img src="..\post_img\session.JPG" alt="img" style="zoom: 70%;" />

### 쿠키(Cookie)

- 서버와 클라이언트 사이의 연결을 유지
- 쿠키는 클라이언트 에 정보를 저장

#### 쿠키 생성

- mallMain()에서 쿠키를 생성하고, 파라미터로 받은 HttpServletResponse에 쿠키를 담고 있다. 
- 쿠키를 생성할 때는 생성자에 두 개의 파라미터를 넣어주는 데 첫 번째는 쿠키이름을 넣어 주고 두 번째는 쿠키값을 넣어 준다.

- MallController.java

```java
//...
@RequestMapping("/main")
public String mallMain(Mall mall, HttpServletResponse response){

    Cookie genderCookie = new Cookie("gender", mall.getGender());

    if(mall.isCookieDel()) {  // 쿠키를 삭제하라는 옵션이 있을 경우
        genderCookie.setMaxAge(0);  // 서버와 연결을 끊는 과정
        mall.setGender(null);
    } else { // 쿠키를 삭제하라는 옵션이 없을 경우
        // 쿠키 생성(한 달 동안 쿠키를 유지)
        genderCookie.setMaxAge(60*60*24*30);
    }
    // response에 Cookie 삽입
    response.addCookie(genderCookie);

    return "/mall/main";
}
```

#### 쿠키 사용

- mallMain()에서 생성된 쿠키를 mallIndex()에서 사용
- 쿠키를 사용할 때는 @CookieValue 를 사용
  - @CookieValue value = 쿠키 이름, required = 해당 쿠키가 없어도 excaption이 발생하지 않도록 false 로 설정 (default는 true)

- MallController.java

```java
@RequestMapping("/index")
public String mallIndex(Mall mall, 
        @CookieValue(value="gender", required=false) Cookie genderCookie, 
        HttpServletRequest request) {
	
    // 쿠키가 존재한다면
    if(genderCookie != null) 
        mall.setGender(genderCookie.getValue());

    return "/mall/index";
}
```

<br/>

## Redirect,-Interceptor

### Redirect

- 컨트롤러에서 뷰를 분기하는 방법
- 현재 페이지에서 특정 페이지로 전환하는 기능
- MemberController.java
  - 세션이 존재하지 않으면 main 으로 redirect

```java
// 회원 정보 수정 ...
@RequestMapping(value = "/modifyForm")
public String modifyForm(Model model, HttpServletRequest request) {

    HttpSession session = request.getSession();
    Member member = (Member) session.getAttribute("member");

    if(member == null) {
        return "redirect:/";
    } else {
        model.addAttribute("member", service.memberSearch(member));
    }

    return "/member/modifyForm";
}
```

```java
// 회원 정보 삭제 ...
@RequestMapping("/removeForm")
public ModelAndView removeForm(HttpServletRequest request) {

    ModelAndView mav = new ModelAndView();

    HttpSession session =  request.getSession();
    Member member = (Member) session.getAttribute("member");

    if(member == null) {
        mav.setViewName("redirect:/");
    } else {
        mav.addObject("member", member);
        mav.setViewName("/member/removeForm");
    }
    
    return mav;
}
```

### Interceptor

- 컨트롤러 실행 전/후에 특정 작업을 가능하게 하는 방법

- 리다이렉트를 사용해야 하는 경우가 많은 경우 HandlerInterceptor를 이용

- HandlerInterceptor Interface

  - preHandle() : Controller가 작동하기 전 (가장 많이 사용)
  - postHandle() : Controller가 작동한 후
  - afterCompletion()  : Controller와 View가 모두 작업한 후

  <img src="..\post_img\Interceptor.JPG" alt="img" style="zoom: 70%;" />

- src\main\java\com\bs\lec21\member\MemberLoginInterceptor.java

```java
// ...
public class MemberLoginInterceptor extends HandlerInterceptorAdapter {

    @Override	// Controller가 작동하기 전
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response, 
                             Object handler) throws Exception {

        HttpSession session = request.getSession(false);
        
        // Session이 있을 경우
        if(session != null) {
            Object obj = session.getAttribute("member");
            if(obj != null) 
                return true;
        }
		
        // Session이 없을 경우 main page로 redirect
        response.sendRedirect(request.getContextPath() + "/");
        return false;
    }

    @Override
    public void postHandle(HttpServletRequest request,
                           HttpServletResponse response, Object handler,
                           ModelAndView modelAndView) throws Exception {

        super.postHandle(request, response, handler, modelAndView);
    }

    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response, 
                                Object handler, Exception ex)
        throws Exception {

        super.afterCompletion(request, response, handler, ex);
    }
}
```

- src\main\webapp\WEB-INF\spring\appServlet\servlet-context.xml

  - 해당 interceptor가 적용되는 범위 mapping

  - 메소드마다 반복해서 redirect 처리를 해주는 수고를 줄일 수 있음

    ```java
    <!-- ... -->
    	<interceptors>
    		<interceptor>
    			<mapping path="/member/modifyForm"/>
    			<mapping path="/member/removeForm"/>
    			<beans:bean class="com.bs.lec21.member.MemberLoginInterceptor"/>
    		</interceptor>
    	</interceptors>
    ```

  - 멤버 하위에 있는 모든 경로에 대한 interceptor 요청

    - exclude-mapping 에 해당되는 경로는 제외 처리

    ```java
    <!-- ... -->
    	<interceptors>
    		<interceptor>
    			<mapping path="/member/**"/>
    			<exclude-mapping path="/member/joinForm"/>
    			<exclude-mapping path="/member/join"/>
    			<exclude-mapping path="/member/loginForm"/>
    			<exclude-mapping path="/member/login"/>
    			<exclude-mapping path="/member/logout"/>
    			<exclude-mapping path="/member/modify"/>
    			<exclude-mapping path="/member/remove"/>
    		</interceptor>
    	</interceptors>
    ```

<br/>

## DataBase

### 오라클 설치

1. [다운로드](#https://www.oracle.com/database/technologies/xe-downloads.html)

2. 설치

   - setup.exe 실행

3. 계정 생성

   - 명령프롬프트 접속(cmd)

   - ```cmd
     # sqlplus 접속
     C:\> sqlplus
     
     # system 계정 로그인
     C:\> system
          oracle
       
     # 계정 생성, user ID : scott, user PW : tiger
     SQL>  create user scott identified by tiger;
     	    	  
     # 권한(connect, resource 접근 권한 부여)
     SQL> grant connect, resource to scott;
     
     # 계정 삭제
     SQL> drop user scott cascade;
     ```

### SQL developer 설치

1. [다운로드](#https://www.oracle.com/tools/downloads/sqldev-v192-downloads.html)
2. sqldeveloper.exe 실행
   - 초기 실행 시 JDK 경로 설정

<br/>

## JDBC