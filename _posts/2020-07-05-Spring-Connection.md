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
* [리다이렉트, 인터셉트]
* [Database]
* [JDBC]
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



