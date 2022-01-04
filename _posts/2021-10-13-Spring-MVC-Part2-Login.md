---
layout: post
title: Login
summary: Spring MVC Part 2. 백엔드 웹 개발 활용 기술
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
  - `HttpServletRequest` 제공 (HTTP header, URL 정보 등..)

## 서블릿 필터

- 필터는 서블릿이 지원하는 수문장.

**필터 흐름**

`HTTP 요청 -> WAS -> 필터 -> (dispatcher)서블릿 -> 컨트롤러`

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

[Code](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/3669eca5b08d2349869098a619e18d979912ebdf)

**참고**

- HTTP 요청 로그에 각 요청자별 식별자를 자동으로 남기려면 [Spring logback mdc](https://oddblogger.com/spring-boot-mdc-logging) 참고

- [spring logback mdc test](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/58fe53325290f3f5709c9fa86bf315bc7341a5b2)

### 인증 체크

[Code](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/79aabbb4e99124ded45cc7495ecc3730422e46b4)

## 🌞 스프링 인터셉터

- 서블릿과 동일하게 웹 관련 공통 관심사항을 해결하는 기술

- Spring MVC 구조에 특화된 필터 기능을 제공

  - 특별히 필터를 사용해야 하는 것이 아니라면 인터셉터 사용 권장

- 필터와 적용 순서와 범위, 사용법이 다름

**인터셉터 흐름**

`HTTP 요청 -> WAS -> 필터 -> 서블릿 -> 스프링 인터셉터 -> 컨트롤러`

- Dispatcher Servlet과 Controller 사이에서 호출

<center><img src="https://raw.githubusercontent.com/jihunparkme/blog/main/img/interceptor.jpg" width="100%"></center>

**인터셉터 인터페이스**

```java
public interface HandlerInterceptor {

    default boolean preHandle(HttpServletRequest request,  HttpServletResponse response, Object handler) throws Exception {}

    default void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable ModelAndView modelAndView) throws Exception {}

    default void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable Exception ex) throws Exception {}
}
```

- `preHandle()` :

  - Controller 호출 전 (Handler Adapter 호출 전)
  - return true 시 다음으로 진행, false 시 끝

- `postHandle()` :
  - Controller 호출 후 (Handler Adapter 호출 후)
  - Controller에서 예외 발생 시 호출되지 않음.
- `afterCompletion()` :
  - HTTP 요청 종료 후 (View rendering 후)
  - 예외 여부에 관계없이 호출 (예외 발생 시 예외 정보를 파라미터로 전달받음)

### 요청 로그

**로그 인터셉터**

[Code](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/0f084567b8105b4d7b88562a7020e25902e0b8f2)

**참고**

[PathPattern Docs](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/util/pattern/PathPattern.html)

### 인증 체크

[Code](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/7fc7ecec6ae9167352f2d14894216037d96c8c7e)

- 서블릿 필터에 비해 스프링 인터셉터가 더욱 사용법이 편리

## ArgumentResolver 활용

- Controller Method 인자로 임의의 값을 전달하는 방법 제공

**Login annotation**

```java
@GetMapping("/")
public String homeLogin(@Login Member loginMember, Model model) {}
```

```java
@Target(ElementType.PARAMETER) //PARAMETER에만 사용
@Retention(RetentionPolicy.RUNTIME) //리플렉션 활용을 위해 런타임까지 애노테이션 정보가 남도록 설정
public @interface Login {}
```

- @Target : annotation 대상 지정
- @Retention : 어느 시점까지 어노테이션의 메모리를 가져갈 지 설정

**HandlerMethodArgumentResolver 구현**

```java
@Slf4j
public class LoginMemberArgumentResolver implements HandlerMethodArgumentResolver {
    @Override
    public boolean supportsParameter(MethodParameter parameter) {

        boolean hasLoginAnnotation = parameter.hasParameterAnnotation(Login.class);
        boolean hasMemberType = Member.class.isAssignableFrom(parameter.getParameterType());

        return hasLoginAnnotation && hasMemberType;
    }

    @Override
    public Object resolveArgument(MethodParameter parameter, ModelAndViewContainer mavContainer, NativeWebRequest webRequest, WebDataBinderFactory binderFactory) throws Exception {

        HttpServletRequest request = (HttpServletRequest) webRequest.getNativeRequest();
        HttpSession session = request.getSession(false);
        if (session == null) {
            return null;
        }

        return session.getAttribute(SessionConst.LOGIN_MEMBER);
    }
}

```

- supportsParameter() : annotation(@Login) 과 class type(Member) 확인 후 해당 ArgumentResolver 사용
  - 결과가 true 일 경우 resolveArgument() 실행
- resolveArgument() : Controller 호출 직전에 호출되어 필요한 파라미터 정보 생성
  - ArgumentResolver 실행 시 어떤 값을 넣어 줄지 설정

**ArgumentResolver 설정**

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

  //...

  @Override
  public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {
      resolvers.add(new LoginMemberArgumentResolver());
  }
}
```
