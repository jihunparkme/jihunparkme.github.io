---
layout: post
title: Login
summary: Cookie, Session, Filter, Interceptor
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

## 세션 생성

Session 정보는 서버 메모리에 저장

- `request.getSession(true)` : default
  - 세션이 있으면 기존 세션 반환
  - 세션이 없으면 새로운 세션을 생성해서 반환
- `request.getSession(false)`
  - 세션이 있으면 기존 세션 반환
  - 세션이 없으면 새로운 세션을 생성하지 않고, null 반환

```java
@PostMapping("/login")
public String login(@Valid @ModelAttribute LoginForm form, BindingResult bindingResult, HttpServletRequest request) {

    //... 로그인 성공

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
## 세션 정보

```java
HttpSession session = request.getSession(false);

session.getAttributeNames()
        .asIterator()
        .forEachRemaining(name -> log.info("session name={}, value={}", name, session.getAttribute(name)));

// Session ID (JSESSIONID 값)
log.info("sessionId={}", session.getId()); 
// 세션 유효 시간 (sec.)
log.info("maxInactiveInterval={}", session.getMaxInactiveInterval()); 
// 세션 생성 일시 (Long)
log.info("creationTime={}", new Date(session.getCreationTime())); 
// 세션과 연결된 사용자가 최근에 서버에 접근한 시간 (Long) ->  클라이언트에서 서버로 sessionId(JSESSIONID)를 요청한 경우 갱신
log.info("lastAccessedTime={}", new Date(session.getLastAccessedTime())); 
// 새로 생성된 세션인지 확인
log.info("isNew={}", session.isNew()); 
```

## 세션 타임아웃

사용자가 로그아웃을 직접 호출하지 않고 웹 브라우저를 종료할 경우 세션이 무한정 남아있는 문제 발생

- 세션과 관련된 쿠키(JSESSIONID)를 탈취 당했을 경우 오랜 시간이 지나도 해당 쿠키로 악의적인 요청을 할 수 있음.
- 세션은 기본적으로 메모리에 생성
  - 메모리 크기가 무한하지 않으므로 `세션에는 최소한의 데이터만 보관`하는 것이 중요
  - `메모리 사용량`(보관한 데이터 용량 * 사용자 수)이 급격하게 늘어나 장애 발생 가능성 존재
  - `세션 시간`을 너무 길게 가져가면 메모리 사용이 계속 누적 될 수 있으므로 적당한 시간을 선택하는 것이 필요
  

**세션 종료 시점**

- 사용자가 서버에 최근에 요청한 시간을 기준으로 30분 정도를 유지
- 사용자가 서비스를 사용하고 있으면, 세션의 생존 시간이 30분으로 계속 증가
- HttpSession 은 이 방식을 사용

**세션 타임아웃 설정**

- 글로벌 설정

  ```properties
  server.servlet.session.timeout=1800 # sec
  ```

- 특정 세션 단위 설정

  ```java
  session.setMaxInactiveInterval(1800); // sec.
  ```

**세션 타임아웃 발생**

- 세션의 타임아웃 시간은 해당 세션과 관련된 JSESSIONID 를 전달하는 HTTP 요청이 있으면 현재 시간을 기준으로 다시 초기화
- 이렇게 초기화되면 세션 타임아웃으로 설정한 시간동안 세션을 추가로 사용 가능
  - session.getLastAccessedTime(): 최근 세션 접근 시간
  - LastAccessedTime 이후로 timeout 시간이 지나면, WAS 가 내부에서 해당 세션 제거

# Filter, Interceptor

- 공통 관심사(cross-cutting concern): 애플리케이션의 여러 로직에서 공통으로 관심을 갖는 것
  - ex. 여러 컨트롤러에서 로그인 여부 확인
- 웹과 관련된 공통 관심사는 `서블릿 필터` 또는 `스프링 인터셉터` 사용 권장
  - `HttpServletRequest` 제공 (HTTP header, URL 정보 등..)

## Servlet Filter

**필터는 서블릿이 지원하는 수문장.**

.

**필터 흐름**

`HTTP Request ➔ WAS ➔ filter ➔ (dispatcher)Servlet ➔ Controller`

- 필터를 적용하면 `필터 호출 이후 서블릿 호출`
  - 필터에서 적절하지 않은 요청으로 판단되면 서블릿을 호출하지 않음
- 모든 고객의 요청 로그를 남기려면 필터를 사용해 보자
- 필터는 특정 URL 패턴에 적용 가능 ➔ `/*` 설정 시 모든 요청에 필터 적용
- 필터는 체인으로 구성되어 여러 필터로 구성 가능

.

**Filter Interface**

```java
public interface Filter {

    public default void init(FilterConfig filterConfig) throws ServletException {}

    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException;

    public default void destroy() {}
}
```

- 필터 인터페이스를 구현/등록하면 서블릿 컨테이너가 필터를 싱글톤 객체로 생성/관리
  - `init()` : 필터 초기화 메서드 ➔ 서블릿 컨테이너가 생성될 때 호출
  - `doFilter()` : 고객의 요청이 올 때마다 호출(필터 로직 구현)
  - `destroy()` : 필터 종료 메서드 ➔ 서블릿 컨테이너가 종료될 때 호출

### 요청 로그

**로그 필터 구현**

- 필터 사용을 위해 필터 인터페이스 구현

```java
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
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        String requestURI = httpRequest.getRequestURI(); // 요청 URI 정보

        String uuid = UUID.randomUUID().toString(); // HTTP 요청 구분 목적

        try {
            log.info("REQUEST [{}][{}]", uuid, requestURI);
            /**
             * 다음 필터가 있으면 필터 호출. 필터가 없으면 서블릿 호출
             * (doFilter 를 호출하지 않으면 다음 단계로 진행되지 않음)
             */
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
public class FilterWebConfig {
    /**
     * FilterRegistrationBean 를 사용하여 필터 등록
     *
     * @ServletComponentScan, @WebFilter(filterName = "logFilter", urlPatterns = "/*") 로 필터 등록이 가능하지만 필터 순서 조절 불가
     * Spring Boot 는 WAS 를 들고 함께 띄우기 때문에, WAS 를 띄울 때 필터를 같이 세팅
     */
    @Bean
    public FilterRegistrationBean logFilter() {
        FilterRegistrationBean<Filter> filterRegistrationBean = new FilterRegistrationBean<>();
        filterRegistrationBean.setFilter(new LogFilter()); // 등록할 필터 지정
        filterRegistrationBean.setOrder(1); // 필터는 체인으로 동작하므로 순서 지정
        filterRegistrationBean.addUrlPatterns("/*"); // 필터를 적용할 URL 패턴 지정
        return filterRegistrationBean;
    }
}
```

**실행 로그**
```text
hello.login.web.filter.LogFilter: REQUEST [0a2249f2-cc70-4db4-98d1-492ccf5629dd][/items]

hello.login.web.filter.LogFilter: RESPONSE [0a2249f2-cc70-4db4-98d1-492ccf5629dd][/items]
```

**참고**

> [Spring logback mdc](https://oddblogger.com/spring-boot-mdc-logging) (HTTP 요청 로그에 각 요청자별 식별자를 자동으로 남기기)
> 
> [spring logback mdc test](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/58fe53325290f3f5709c9fa86bf315bc7341a5b2)

### 인증 체크

**로그인 체크 필터 구현**

```java
@Slf4j
public class LoginCheckFilter implements Filter {
    private static final String[] whitelist = {"/", "/members/add", "/login", "/logout", "/css/*"}; // 인증과 무관하게 항상 허용하는 경로

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        String requestURI = httpRequest.getRequestURI();
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        try {
            if (isLoginCheckPath(requestURI)) {
                HttpSession session = httpRequest.getSession(false);

                if (session == null || session.getAttribute(SessionConst.LOGIN_MEMBER) == null) {
                    /**
                     * 미인증 사용자는 로그인 화면으로 리다이렉트 처리
                     * 로그인 이후 요청 경로로 이동하기 위해 쿼리 파라미터로 요청 경로를 함께 전달
                     */
                    httpResponse.sendRedirect("/login?redirectURL=" + requestURI);
                    // 미인증 사용자는 다음(필터, 서블릿, 컨트롤러)으로 진행하지 않고 종료.
                    return;
                }
            }

            chain.doFilter(request, response);
        } catch (Exception e) {
            /**
             * 예외 로깅 가능 하지만, 톰캣까지 예외를 보내주어야 함
             * (ServletFilter 에서 터진 예외를 ServletContainer(WAS) 까지 올려줘야 함)
             */
            throw e;
        } finally {
            log.info("인증 체크 필터 종료 {}", requestURI);
        }
    }

    /**
     * 화이트 리스트의 경우 인증 체크 X
     */
    private boolean isLoginCheckPath(String requestURI) {
        return !PatternMatchUtils.simpleMatch(whitelist, requestURI);
    }
}
```

**필터 설정**

```java
@Configuration
public class FilterWebConfig {
    // ...
    
    @Bean
    public FilterRegistrationBean loginCheckFilter() {
        FilterRegistrationBean<Filter> filterRegistrationBean = new FilterRegistrationBean<>();
        filterRegistrationBean.setFilter(new LoginCheckFilter()); // 로그인 필터 등록
        filterRegistrationBean.setOrder(2); // 로그 필터 이후 로그인 필터 적용
        filterRegistrationBean.addUrlPatterns("/*"); // 모든 요청에 로그인 필터 적용
        return filterRegistrationBean;
    }
}

```

**로그인 성공 시 처리**

```java
@PostMapping("/login")
public String login(
        @Valid @ModelAttribute LoginForm form, BindingResult bindingResult,
        @RequestParam(defaultValue = "/") String redirectURL,
        HttpServletRequest request) {

    // ...

    /**
     * 미인증 사용자는 요청 경로를 포함해서 /login 에 redirectURL 요청 파라미터를 추가해서 요청
     * 로그인 성공시 해당 경로로 고객을 redirect
     */
    return "redirect:" + redirectURL;
}
```

.

**참고.**

> 스프링 인터셉터에서는 제공하지 않는 필터의 강력한 기능
> 
> `chain.doFilter(request, response);` 를 호출해서 다음 필터 또는 서블릿을 호출할 때 request, response 를 다른 객체로 변경 가능
> 
> `ServletRequest`, `ServletResponse` 를 구현한 다른 객체를 만들어서 넘기면 해당 객체가 다음 필터 또는 서블릿에서 사용

## 스프링 인터셉터 🌞

**서블릿과 동일하게 웹 관련 공통 관심사항을 해결하는 기술**
- Spring MVC 구조에 특화된 필터 기능을 제공
  - 특별히 필터를 사용해야 하는 것이 아니라면 스프링 인터셉터 사용 권장
- 서블릿 필터보다 편리하고, 더 정교하고, 다양한 기능을 지원
  - 필터와 적용 순서와 범위, 사용법에 차이

.

**인터셉터 흐름**

`HTTP Request ➔ WAS ➔ Filter ➔ Dispatcher Servlet ➔ Spring Interceptor ➔ Controller`

- Dispatcher Servlet 과 Controller 사이에 호출
- 스프링 인터셉터에서 적절하지 않은 요청으로 판단되면 컨트롤러를 호출하지 않음
- 정밀한 URL 패턴 적용 가능

![Result](https://raw.githubusercontent.com/jihunparkme/blog/main/img/interceptor.jpg?raw=true 'Result')

.

**인터셉터 인터페이스**

```java
public interface HandlerInterceptor {

    default boolean preHandle(HttpServletRequest request,  HttpServletResponse response, Object handler) throws Exception {}

    default void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable ModelAndView modelAndView) throws Exception {}

    default void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable Exception ex) throws Exception {}
}
```

- `preHandle()`: Controller 호출 전 호출(Handler Adapter 호출 전)
  - return true ➔ 다음으로 진행
  - return false ➔ 진행 중단(나머지 인터셉터, 핸들러 어댑터 호출 X)
- `postHandle()`: Controller 호출 후 호출(Handler Adapter 호출 후)
  - Controller 에서 `예외 발생 시` postHandle `호출 X`
- `afterCompletion()`: HTTP 요청 종료 후 호출(View rendering 후)
  - 예외 여부에 관계없이 `항상 호출`
  - 예외 발생 시 예외 정보를 파라미터로 받아서 로그 출력 가능

### 요청 로그

**요청 로그 인터셉터 구현**

```java
@Slf4j
public class LogInterceptor implements HandlerInterceptor {
    public static final String LOG_ID = "logId";

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String requestURI = request.getRequestURI();
        String uuid = UUID.randomUUID().toString();

        /**
         * 스프링 인터셉터는 호출 시점이 완전히 분리
         * preHandle 에서 지정한 값을 postHandle, afterCompletion 에서 함께 사용하기 위해 request 에 세팅
         * (HandlerInterceptor 구현체는 싱글톤처럼 사용되기 때문에 맴버변수를 사용하면 위험!)
         */
        request.setAttribute(LOG_ID, uuid);

        /**
         * @Controller, @RequestMapping: HandlerMethod
         * 정적 리소스(/resources/static): ResourceHttpRequestHandler
         */
        if (handler instanceof HandlerMethod) {
            HandlerMethod hm = (HandlerMethod) handler; // 호출할 컨트롤러 메서드의 모든 정보가 포함
        }
        log.info("REQUEST [{}][{}][{}]", uuid, requestURI, handler);
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        log.info("postHandle [{}]", modelAndView);
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        String requestURI = request.getRequestURI();
        String logId = (String) request.getAttribute(LOG_ID);
        log.info("RESPONSE [{}][{}]", logId, requestURI);
        if (ex != null) {
            log.error("afterCompletion error!!", ex);
        }
    }
}
```

`HandlerMethod`:
- 핸들러 정보는 어떤 핸들러 매핑을 사용하는가에 따라 다름
- 스프링을 사용하면 일반적으로 @Controller, @RequestMapping 을 활용한 핸들러 매핑을 사용
  - 이 경우 핸들러 정보로 HandlerMethod 가 넘어온다.

`ResourceHttpRequestHandler`
- @Controller 가 아니라 정적 리소스(/resources/static)가 호출 되는 경우
- ResourceHttpRequestHandler 가 핸들러 정보로 넘어오기 때문에 타입에 따라서 처리가 필요

`postHandle`, `afterCompletion`
- 예외가 발생한 경우 postHandle 가 호출되지 않으므로, 종료 로그를 afterCompletion 에서 실행

.

**인터셉터 등록**

```java
@Configuration
public class InterceptorWebConfig implements WebMvcConfigurer {
    /**
     * WebMvcConfigurer 가 제공하는 addInterceptors() 를 사용해서 인터셉터 등록
     * 인터셉터는 addPathPatterns, excludePathPatterns 로 매우 정밀하게 URL 패턴 지정
     */
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LogInterceptor()) // 인터셉터 등록
                .order(1) // 인터셉터 호출 순서 지정
                .addPathPatterns("/**") // 인터셉터 적용 URL 패턴 지정
                .excludePathPatterns("/css/**", "/*.ico", "/error"); // 인터셉터 제외 패턴 지정
    }
}
```

**실행 로그**
```text
REQUEST [6234a913-f24f-461f-a9e1-85f153b3c8b2][/members/add]
[hello.login.web.member.MemberController#addForm(Member)]

postHandle [ModelAndView [view="members/addMemberForm"; 
model={member=Member(id=null, loginId=null, name=null, password=null),
org.springframework.validation.BindingResult.member=org.springframework.validat
ion.BeanPropertyBindingResult: 0 errors}]]

RESPONSE [6234a913-f24f-461f-a9e1-85f153b3c8b2][/members/add]
```

**참고**

> 스프링이 제공하는 URL 경로는 서블릿 기술이 제공하는 URL 경로와 완전히 다르다. 더욱 자세하고, 세밀하게 설정 가능하다.
>
> [PathPattern Docs](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/util/pattern/PathPattern.html)

### 인증 체크

**로그인 체크 인터셉터**

```java
@Slf4j
public class LoginCheckInterceptor implements HandlerInterceptor {
    /**
     * 인증은 컨트롤러 호출 전에만 호출되면 되므로 preHandle 만 구현
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String requestURI = request.getRequestURI();

        log.info("인증 체크 인터셉터 실행 {}", requestURI);
        HttpSession session = request.getSession(false);

        if (session == null || session.getAttribute(SessionConst.LOGIN_MEMBER) == null) {
            log.info("미인증 사용자 요청");
            response.sendRedirect("/login?redirectURL=" + requestURI); // 로그인으로 redirect
            return false;
        }

        return true;
    }
}
```

**로그인 체크 인터셉터 등록**

```java
@Configuration
public class InterceptorWebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LogInterceptor())
                .order(1)
                .addPathPatterns("/**")
                .excludePathPatterns("/css/**", "/*.ico", "/error");패턴 지정
        registry.addInterceptor(new LoginCheckInterceptor())
                .order(2)
                .addPathPatterns("/**")
                .excludePathPatterns(
                        "/", "/members/add", "/login", "/logout", "/css/**", "/*.ico", "/error"
                );
    }
}
```


> 서블릿 필터에 비해 스프링 인터셉터가 더욱 사용법이 편리
>
> 특별한 문제가 없다면 인터셉터를 사용하자.

## ArgumentResolver 활용 🌞

Controller Method 의 인자로 임의의 값을 전달하는 방법 제공

**Login Annotation 생성**

```java
@Target(ElementType.PARAMETER) // PARAMETER 에만 사용
@Retention(RetentionPolicy.RUNTIME) // 리플렉션 등의 활용을 위해 런타임까지 애노테이션 정보가 남도록 설정
public @interface Login {}
```

- @Target : annotation 대상 지정
- @Retention : 어느 시점까지 어노테이션의 메모리를 가져갈지 설정

.

**@Login 적용**

```java
@GetMapping("/")
public String homeLogin(@Login Member loginMember, Model model) { ... }
```
.

**HandlerMethodArgumentResolver 구현**

```java
@Slf4j
public class LoginMemberArgumentResolver implements HandlerMethodArgumentResolver {

    @Override
    public boolean supportsParameter(MethodParameter parameter) {
        boolean hasLoginAnnotation = parameter.hasParameterAnnotation(Login.class);
        boolean hasMemberType = Member.class.isAssignableFrom(parameter.getParameterType());

        /**
         * @Login 어노테이션이 있으면서 Member 타입이면 해당 ArgumentResolver 사용
         * 결과가 true 일 경우 resolveArgument() 실행
         */ 
        return hasLoginAnnotation && hasMemberType;
    }

    /**
     * 컨트롤러 호출 직전에 호출 되어서 필요한 파라미터 정보를 생성
     * - 세션에 있는 로그인 회원 정보인 member 객체를 찾아서 반환
     * - 이후 Spring MVC 는 컨트롤러의 메서드를 호출하면서 여기에서 반환된 member 객체를 파라미터에 전달
     */
    @Override
    public Object resolveArgument(MethodParameter parameter,
                                  ModelAndViewContainer mavContainer,
                                  NativeWebRequest webRequest,
                                  WebDataBinderFactory binderFactory) throws Exception {

        HttpServletRequest request = (HttpServletRequest) webRequest.getNativeRequest();
        HttpSession session = request.getSession(false);
        if (session == null) {
            return null;
        }

        return session.getAttribute(SessionConst.LOGIN_MEMBER);
    }
}
```

.

**ArgumentResolver 설정**

```java
@Configuration
public class ArgumentResolverWebConfig implements WebMvcConfigurer {

    @Override
    public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {
        resolvers.add(new LoginMemberArgumentResolver());
    }
}
```

> `ArgumentResolver` 를 활용하면 공통 작업이 필요할 때 애노테이션으로 컨트롤러를 더욱 편리하게 사용 가능

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