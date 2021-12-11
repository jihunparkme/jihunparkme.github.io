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

**상태 유지**

- HTTP 응답에 쿠키를 담아서 브라우저에 전달
- 이후 브라우저는 해당 쿠키를 지속해서 전송

## 쿠키 생성

- 세션 쿠키: 만료 날짜를 생략하면 브라우저 종료시 까지만 유지
- 영속 쿠키: 만료 날짜를 입력하면 해당 날짜까지 유지

```java
Cookie idCookie = new Cookie("memberId", String.valueOf(loginMember.getId()));
response.addCookie(idCookie); // HttpServletResponse
```

## 쿠키 조회

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

## 쿠키 제거

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

- 사용자 별로 예측 불가능한 임의의 토큰을 `서버에서 관리`

  - 서버에서 토큰과 사용자 id를 매핑해서 인식

- 해커가 임의의 값을 넣어도 찾을 수 없도록 `토큰은 예상 불가능` 해야 함

  - UUID 사용

- 해커가 토큰 정보를 가져가도 시간이 지나면 사용할 수 없도록 서버에서 해당 토큰의 `만료시간을 짧게 유지`

  - 해킹이 의심되는 경우 서버에서 해당 토큰을 강제로 제거

# Session

`서버에 중요한 정보를 보관하고 연결을 유지하는 방법`

- 서버의 세션 저장소에 중요한 정보를 보관하고 해당 정보를 토큰으로 변환 후 쿠키로 연결을 유지

1. 사용자 정보가 서버로 전달되면 올바른 정보인지 확인
2. 해당 사용자의 `세션 ID 생성`(UUID) 및 `세션 저장소`에 보관
3. 서버는 클라이언트에게 `세션 ID`를 `쿠키`에 담아 전달
4. 클라이언트는 쿠키 저장소에 세션 ID 를 보관하여 서버와 연결

**URL에 jsessionid 를 포함하지 않고 쿠키를 통해서만 세션을 유지할 경우 추가**

```properties
server.servlet.session.tracking-modes=cookie
```

## 세션 생성

Session 정보는 서버 메모리에 저장

- request.getSession(true) : default
  - 세션이 있으면 기존 세션을 반환
  - 세션이 없으면 새로운 세션을 생성해서 반환
- request.getSession(false)

  - 세션이 있으면 기존 세션을 반환
  - 세션이 없으면 새로운 세션을 생성하지 않고, null 반환

<i>로그인</i>

```java
HttpSession session = request.getSession();
session.setAttribute(SessioinConst.LOGIN_MEMBER, loginMember);
```

```java
@PostMapping("/login")
public String login(@Valid @ModelAttribute LoginForm form, BindingResult bindingResult, HttpServletRequest request) {

    if (bindingResult.hasErrors()) {
        return "login/loginForm";
    }

    Member loginMember = loginService.login(form.getLoginId(), form.getPassword());
    log.info("login? {}", loginMember);

    if (loginMember == null) {
        bindingResult.reject("loginFail", "아이디 또는 비밀번호가 맞지 않습니다.");
        return "login/loginForm";
    }

    HttpSession session = request.getSession();
    session.setAttribute(SessioinConst.LOGIN_MEMBER, loginMember);

    return "redirect:/";
}
```

## 세션 조회

<i>Home</i>

```java
HttpSession session = request.getSession(false);
if (session == null){
    return "home";
}

Member loginMember = (Member) session.getAttribute(SessioinConst.LOGIN_MEMBER);
```

- 스프링은 세션을 더 편리하게 사용할 수 있도록 `@SessionAttribute` 지원

```java
@GetMapping("/")
public String homeLogin(
        @SessionAttribute(name = SessioinConst.LOGIN_MEMBER, required = false) Member loginMember, Model model) {

    if (loginMember == null) {
        return "home";
    }

    model.addAttribute("member", loginMember);
    return "loginHome";
}
```

## 세션 제거

<i>로그아웃</i>

```java
HttpSession session = request.getSession(false);
if (session != null){
    session.invalidate();
}
```

```java
@PostMapping("/logout")
public String logout(HttpServletRequest request) {
    HttpSession session = request.getSession(false);
    if (session != null){
        session.invalidate();
    }
    return "redirect:/";
}
```

## 세션 타임아웃

- 세션의 타임아웃 시간은 해당 세션과 관련된 JSESSIONID 를 전달하는 HTTP 요청이 있으면 현재 시간을 기준으로 다시 초기화

- 세션에는 최소한의 데이터만 보관하는 것이 중요
  - 메모리 사용량이 급격하게 늘어나 장애 발생 가능성

**글로벌 설정**

```properties
server.servlet.session.timeout=1800 # default
```

**특정 세션 단위 설정**

```java
session.setMaxInactiveInterval(1800); //1
```

## 세션 정보

```java
HttpSession session = request.getSession(false);

session.getAttributeNames().asIterator()
        .forEachRemaining(name -> log.info("session name={}, value={}",
                name, session.getAttribute(name)));

log.info("sessionId={}", session.getId()); //session ID (JSESSIONID)
log.info("maxInactiveInterval={}", session.getMaxInactiveInterval()); //세션 유효 시간 (초)
log.info("creationTime={}", new Date(session.getCreationTime())); //세션 생성 일시 (Long)
log.info("lastAccessedTime={}", new Date(session.getLastAccessedTime())); //세션과 연결된 사용자가 최근에 서버에 접근한 시간 (Long)
log.info("isNew={}", session.isNew()); //새로 생성된 세션인지 확인
```

# 필터, 인터셉터

- 웹과 관련된 공통 관심사는 `서블릿 필터` 또는 `스프링 인터셉터`를 사용
  - `HttpServletRequest` 제공

## 서블릿 필터

- 필터는 서블릿이 지원하는 수문장.

**필터 흐름**

`HTTP 요청 -> WAS -> 필터 -> (디스패처)서블릿 -> 컨트롤러`

- 필터는 체인으로 구성되어 여러 필터로 구성 가능

**필터 인터페이스**

```java
public interface Filter {
    public default void init(FilterConfig filterConfig) throws ServletException {}

    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException;

    public default void destroy() {}
}
```

- 필터 인터페이스를 구현/등록하면 서블릿 컨테이너가 필터를 싱글톤 객체로 생성하고, 관리
- `init()` : 필터 초기화 메서드 -> 서블릿 컨테이너가 생성될 때 호출
- `doFilter()` : 고객의 요청이 올 때 마다 호출 (필터의 로직 구현)
- `destroy()` : 필터 종료 메서드 -> 서블릿 컨테이너가 종료될 때 호출

### 요청 로그

**로그 필터**

```java
/**
 * 필터 사용을 위해 필터 인터페이스 구현
 */
@Slf4j
public class LogFilter implements Filter {

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        log.info("log filter init");
    }

    /**
     * HTTP 요청이 오면 호출
     * - 고객의 요청 응답 정보를 한 번에 확인 가능
     * - 시간 정보를 추가해서 요청 시간 확인 및 성능 최적화 가능
     */
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        log.info("log filter doFilter");

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        String requestURI = httpRequest.getRequestURI(); //요청 URI 정보

        String uuid = UUID.randomUUID().toString(); //요청 구분을 위한 uuid

        try {
            log.info("REQUEST [{}][{}]", uuid, requestURI);
            //다음 필터가 있으면 필터 호출, 필터가 없으면 서블릿 호출
            chain.doFilter(request, response);
        } catch (Exception e) {
            throw e;
        } finally {
            log.info("RESPONSE [{}][{}]", uuid, requestURI);
        }
    }

    @Override
    public void destroy() {
        log.info("log filter destroy");
    }
}

```

**필터 설정**

```java
@Configuration
public class WebConfig {

    /**
     * 필터 등록
     * Spring Boot 는 WAS 를 들고 띄우기 때문에, WAS 를 띄울 때 필터를 같이 넣어 준다.
     * @return
     */
    @Bean
    public FilterRegistrationBean logFilter() {

        FilterRegistrationBean<Filter> filterRegistrationBean = new FilterRegistrationBean<>();
        filterRegistrationBean.setFilter(new LogFilter()); //등록할 필터 설정
        filterRegistrationBean.setOrder(1); //필터 체인에서의 필터 순서
        filterRegistrationBean.addUrlPatterns("/*"); //필터를 적용할 URL Pattern 설정

        return filterRegistrationBean;
    }
}

```

**참고**

- HTTP 요청 로그에 각 요청자별 식별자를 자동으로 남기려면 [Spring logback mdc](https://oddblogger.com/spring-boot-mdc-logging) 참고
