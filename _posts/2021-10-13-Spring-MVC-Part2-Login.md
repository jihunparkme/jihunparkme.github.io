---
layout: post
title: Login
summary: Spring MVC Part 2. 백엔드 웹 개발 활용 기술
categories: Spring-Conquest
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

**쿠키 생성**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/cookie-login.png?raw=true 'Result')

**쿠키 전달**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/cookie-store.png?raw=true 'Result')

**영속 쿠키와 세션 쿠키**

- `영속 쿠키`: 만료 날짜를 입력하면 `해당 날짜까지` 유지
- `세션 쿠키`: 만료 날짜를 생략하면 `브라우저 종료시 까지`만 유지

```java
Cookie idCookie = new Cookie("memberId", String.valueOf(loginMember.getId()));
response.addCookie(idCookie);
```

- 요청이에 성공하면 쿠키를 생성하고 HttpServletResponse 에 담기
- 만료 날짜를 생략(세션 쿠키)하였으므로 웹 브라우저는 종료 전까지 회원의 id 를 서버에 계속 전달

## 쿠키 조회

```java
@GetMapping("/")
public String homeLogin(@CookieValue(name = "memberId", required = false) Long memberId, Model model) {
  // ...
}
```

- `@CookieValue` 를 사용하면 편리하게 쿠키 조회
- 쿠키가 없는 요청도 접근할 수 있으므로, `required = false` 적용

## 쿠키 제거

```java
@PostMapping("/logout")
public String logout(HttpServletResponse response) {
    Cookie cookie = new Cookie("memberId", null);
    cookie.setMaxAge(0);
    response.addCookie(cookie);

    return "redirect:/";
}
```

- 응답 쿠키 생성 시 `Max-Age: 0` 으로 설정해 주면 해당 쿠키는 즉시 종료

## 보안 문제

**쿠키 값은 임의로 변경 가능**
- 클라이언트가 쿠키를 강제로 변경 가능.

**쿠키에 보관된 정보는 도난 가능**
- 쿠키에 민감한 정보가 있다면, 이 정보가 웹 브라우저에도 보관되고, 네트워크 요청마다 계속 클라이언트에서 서버로 전달되어 도난 가능성 존재.

**해커가 쿠키를 한번 훔쳐가면 평생 사용 가능**
- 해커가 쿠키를 훔쳐가서 그 쿠키로 악의적인 요청을 계속 시도할 수 있음.

---

**대안**

- 사용자 별로 예측 불가능한 `임의의 토큰`을 `서버에서 관리`
  - 서버에서 토큰과 사용자 id를 매핑해서 인식
- 해커가 임의의 값을 넣어도 찾을 수 없도록 `토큰은 예상 불가능` 해야 함
  - UUID 사용
- 해커가 토큰 정보를 가져가도 시간이 지나면 사용할 수 없도록 서버에서 해당 토큰의 `만료시간을 짧게 유지`
  - 해킹이 의심되는 경우 서버에서 해당 토큰을 강제로 제거

# Session

`서버에 중요한 정보를 보관하고 연결을 유지하는 방법`

- 서버의 세션 저장소에 중요한 정보를 보관하고 해당 정보를 토큰으로 변환 후 쿠키로 연결을 유지

**로그인 요청**

- 사용자 정보가 서버로 전달되면 올바른 정보인지 확인

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/session-request.png?raw=true 'Result')

**세션 생성**

- 추정 불가능한 `UUID` 로 session ID 생성
- `세션 저장소`에 생성된 `session ID` 와 보관할 값(사용자 기본 정보) 저장

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/session-store.png?raw=true 'Result')

**서버의 세션 ID 쿠키 응답**

- 서버는 클라이언트에 `UUID Session ID` 로 응답 쿠키를 생성해서 전달
  - 클라이언트와 서버는 결국 쿠키로 연결
- 클라이언트는 쿠키 저장소에 UUID Session ID 쿠키 보관

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/session-response.png?raw=true 'Result')

**클라이언트의 세션 ID 쿠키 전달**

- 클라이언트는 요청 시 항상 Session ID 쿠키를 함께 전달
- 서버는 클라이언트가 전달한 Session ID 쿠키 정보로 세션 저장소를 조회해서 로그인 시 보관한 세션 정보를 사용

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/session-client.png?raw=true 'Result')

> URL에 jsessionid 를 포함하지 않고 쿠키를 통해서만 세션을 유지할 경우 아래 옵션추가
>
> ```properties
> server.servlet.session.tracking-modes=cookie
> ```

## HttpSession

**서블릿은 세션을 위해 HttpSession 기능 제공**

- 서블릿을 통해 HttpSession 생성 시 아래와 같은 쿠키 생성
  ```yml
  Cookie: JSESSIONID=5B78E23B513F50164D6FDD8C97B0AD05
  ```

### 세션 생성

Session 정보는 서버 메모리에 저장

- request.getSession(true) : default
  - 세션이 있으면 기존 세션 반환
  - 세션이 없으면 새로운 세션을 생성해서 반환
- request.getSession(false)
  - 세션이 있으면 기존 세션 반환
  - 세션이 없으면 새로운 세션을 생성하지 않고, null 반환

```java
@PostMapping("/login")
public String login(@Valid @ModelAttribute LoginForm form, BindingResult bindingResult, HttpServletRequest request) {

    //... 로그인 성공

    // 
    // 세션이 있으면 기존 세션 반환, 없으면 신규 세션 생성
    HttpSession session = request.getSession();
    // 세션에 로그인 회원 정보 보관
    session.setAttribute(SessionConst.LOGIN_MEMBER, loginMember);

    return "redirect:/";
}
```

## 세션 조회

스프링은 세션을 더 편리하게 사용할 수 있도록 `@SessionAttribute` 지원
- 세션과 세션 데이터를 찾는 번거로운 과정을 스프링이 한번에 처리

```java
@GetMapping("/")
public String homeLoginV3Spring(@SessionAttribute(name = SessionConst.LOGIN_MEMBER, required = false) Member loginMember, Model model) {
    // 세션에 회원 데이터가 있을 경우
    if (loginMember == null) {
        return "home";
    }

    // 세션이 있을 경우
    model.addAttribute("member", loginMember);
    return "loginHome";
}
```

## 세션 제거

```java
@PostMapping("/logout")
public String logout(HttpServletRequest request) {
    HttpSession session = request.getSession(false); 
    if (session != null) {
        session.invalidate(); // 세션 삭제
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

---

**스프링 완전 정복 로드맵**

- 스프링 입문 > 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술
- [스프링 핵심 원리 > 기본편](https://jihunparkme.github.io/Spring-Core/)
- 모든 개발자를 위한 HTTP 웹 기본 지식
  - [Basic](https://jihunparkme.github.io/Http-Web-Network_basic/)
  - [Method](https://jihunparkme.github.io/Http-Web-Network_method/)
  - [Header](https://jihunparkme.github.io/Http-Web-Network_header/)
- 스프링 웹 MVC 1편
  - [Servlet](https://jihunparkme.github.io/Spring-MVC-Part1-Servlet/)
  - [MVC](https://jihunparkme.github.io/Spring-MVC-Part1-MVC/)
- 스프링 웹 MVC 2편
  - [Thymeleaf](https://jihunparkme.github.io/Spring-MVC-Part2-Thymeleaf/)
  - [etc](https://jihunparkme.github.io/Spring-MVC-Part2-Etc/)
  - [Validation](https://jihunparkme.github.io/Spring-MVC-Part2-Validation/)
  - [Login](https://jihunparkme.github.io/Spring-MVC-Part2-Login/)
  - [Exception](https://jihunparkme.github.io/Spring-MVC-Part2-Exception/)
- [스프링 DB 1편 > 데이터 접근 핵심 원리](https://jihunparkme.github.io/Spring-DB-Part1/)
- [스프링 DB 2편 > 데이터 접근 활용 기술](https://jihunparkme.github.io/Spring-DB-Part2/)
- [스프링 핵심 원리 > 고급편](https://jihunparkme.github.io/Spring-Core-Principles-Advanced/)
- [실전! 스프링 부트](https://jihunparkme.github.io/spring-boot/)