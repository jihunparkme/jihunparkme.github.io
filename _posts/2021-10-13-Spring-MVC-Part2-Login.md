---
layout: post
title: Spring MVC Part 2. Login
summary: (MVC) 스프링 MVC 2편 - 백엔드 웹 개발 활용 기술
categories: (Inflearn)Spring-MVC-2
featured-img: spring_mvc_2
# mathjax: true
---

# Spring MVC Part 2. Login

영한님의 [스프링 MVC 2편 - 백엔드 웹 개발 활용 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-2/) 강의 노트

# Cookie

## 상태 유지

- HTTP 응답에 쿠키를 담아서 브라우저에 전달
- 이후 브라우저는 해당 쿠키를 지속해서 전송

**쿠키 생성**

- 세션 쿠키: 만료 날짜를 생략하면 브라우저 종료시 까지만 유지
- 영속 쿠키: 만료 날짜를 입력하면 해당 날짜까지 유지

```java
Cookie idCookie = new Cookie("memberId", String.valueOf(loginMember.getId()));
response.addCookie(idCookie); // HttpServletResponse
```

**쿠키 조회**

```java
@GetMapping("/")
public String homeLogin(@CookieValue(name = "memberId", required = false) Long memberId, Model model) {

    if (memberId == null) {
        return "home";
    }

    //로그인
    Member loginMember = memberRepository.findById(memberId);
    if (loginMember == null) {
        return "home";
    }

    model.addAttribute("member", loginMember);
    return "loginHome";
}
```

**쿠키 제거**

```java
@PostMapping("/logout")
public String logout(HttpServletResponse response) {
    expireCookie(response, "memberId");
    return "redirect:/";
}

private void expireCookie(HttpServletResponse response, String cookieName) {
    Cookie cookie = new Cookie(cookieName, null);
    cookie.setMaxAge(0);
    response.addCookie(cookie);
}
```

## 쿠키와 보안 문제

- 쿠키 값은 임의로 변경할 수 있음
- 쿠키에 보관된 정보는 훔쳐갈 수 있음

**대안**

- 사용자 별로 예측 불가능한 임의의 토큰을 서버에서 관리

  - 서버에서 토큰과 사용자 id를 매핑해서 인식

- 토큰은 해커가 임의의 값을 넣어도 찾을 수 없도록 예상 불가능 해야 함

- 해커가 토큰 정보를 가져가도 시간이 지나면 사용할 수 없도록 서버에서 해당 토큰의 만료시간을 짧게 유지
  - 해킹이 의심되는 경우 서버에서 해당 토큰을 강제로 제거
