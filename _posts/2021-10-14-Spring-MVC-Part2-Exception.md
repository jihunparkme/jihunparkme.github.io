---
layout: post
title: Exception
summary: 예외 처리와 오류 페이지
categories: Spring-Conquest
featured-img: spring_mvc_2
# mathjax: true
---

# Spring MVC Part 2. Exception

영한님의 [스프링 MVC 2편 - 백엔드 웹 개발 활용 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-2/) 강의 노트

[Project](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2)

# 예외 처리와 오류 페이지

## 서블릿 예외 처리

순수 서블릿 컨테이너의 예외 처리 지원 방식

.

**`Exception`**

자바 직접 실행 시 예외 발생

- 자바 메인 메서드를 직접 실행할 경우 main 쓰레드 실행
- main 쓰레드 실행 도중에 예외를 잡지 못하고 예외가 던져지면, `예외 정보를 남기고 해당 쓰레드 종료`

웹 애플리케이션에서 예외 발생

```java
@GetMapping("/error-ex")
    public void errorEx() {
    throw new RuntimeException("예외 발생!");
}
```

- 사용자 요청별로 별도의 쓰레드가 할당되고, 서블릿 컨테이너 안에서 실행
- 애플리케이션에서 예외 발생 시, try~catch 로 예외를 잡아서 처리하면 문제가 없음.
- 하지만, 예외를 잡지 못하고, `서블릿 밖으로 예외가 전달될 경우 WAS(tomcat)까지 예외 전달`
  ```text
  WAS <- 필터 <- 서블릿 <- 인터셉터 <- 컨트롤러(예외발생)
  ```
- WAS 는 Exception 예외가 올라오면 서버 내부에서 처리할 수 없는 오류가 발생한 것으로 인지하고 `HTTP Status 500 – Internal Server Error 반환`
  ```properties
  # 스프링 부트가 제공하는 기본 예외 페이지 OFF
  server.error.whitelabel.enabled=false
  ```

.

**`response.sendError(HTTP 상태 코드, 오류 메시지)`**

```java
@GetMapping("/error-404")
public void error404(HttpServletResponse response) throws IOException {
    response.sendError(404, "404 오류!"); // HTTP 상태 코드와 오류 메시지 추가 가능
}
```

- 오류 발생 시 `HttpServletResponse.sendError` 메서드 사용 가능
  - sendError 호출 시 바로 예외가 발생하는 것은 아니지만, `response 내부에 오류 발생 상태를 저장`하여 WAS(Servlet container) 에게 전달
  - WAS(Servlet container) 는 클라이언트에게 응답 전에 response 에 `sendError() 호출 기록 확인` 후, 호출되었다면 `설정한 오류 코드에 맞는 기본 오류 페이지 출력`
- sendError 흐름
  ```text
  WAS(sendError 호출 기록 확인) <- 필터 <- 서블릿 <- 인터셉터 <- 컨트롤러
  ```

## 서블릿 오류 페이지

서블릿은 `Exception` 이 서블릿 밖으로 전달되거나 `response.sendError()` 호출 시 각 상황에 맞춘 오류 처리 기능 제공

**서블릿 오류 페이지 등록**

```java
@Component
public class WebServerCustomizer implements WebServerFactoryCustomizer<ConfigurableWebServerFactory> {

    @Override
    public void customize(ConfigurableWebServerFactory factory) {

        ErrorPage errorPage404 = new ErrorPage(HttpStatus.NOT_FOUND, "/error-page/404"); // response.sendError(404)
        ErrorPage errorPage500 = new ErrorPage(HttpStatus.INTERNAL_SERVER_ERROR, "/error-page/500"); // response.sendError(500)

        ErrorPage errorPageEx = new ErrorPage(RuntimeException.class, "/error-page/500"); // RuntimeException 또는 그 자식 타입의 예외

        factory.addErrorPages(errorPage404, errorPage500, errorPageEx);
    }
}
```

- 오류 페이지는 예외를 다룰 때 해당 예외와 그 자식 타입의 오류를 함께 처리

**오류 처리 컨트롤러**

```java
@Slf4j
@Controller
public class ErrorPageController {

    @RequestMapping("/error-page/404")
    public String errorPage404(HttpServletRequest request, HttpServletResponse response) {
        log.info("errorPage 404");
        return "error-page/404";
    }

    @RequestMapping("/error-page/500")
    public String errorPage500(HttpServletRequest request, HttpServletResponse response) {
        log.info("errorPage 500");
        return "error-page/500";
    }
}
```

**오류 페이지 요청 흐름**

```text
# 예외 발생 흐름
컨트롤러(예외 발생) ➔ 스프링 인터셉터 ➔ 서블릿 ➔ 필터 ➔ WAS

# sendError 흐름
컨트롤러(response.sendError()) ➔ 스프링 인터셉터 ➔ 서블릿 ➔ 필터 ➔ WAS(sendError 호출 기록 확인)

---

# 오류 페이지 요청 흐름
WAS '/error-page/500' 요청 ➔ 필터 ➔ 서블릿 ➔ 스프링 인터셉터 ➔ 컨트롤러(/error-page/500) ➔ View
```

- WAS 까지 예외가 전파될 경우, WAS 는 해당 예외를 처리하는 `오류 페이지 정보` 확인 후 오류 페이지를 다시 요청
- WAS 는 오류 페이지 요청 시 오류 정보를 request.attribute 에 추가해서 전달

```java
private void printErrorInfo(HttpServletRequest request) {
    log.info("ERROR_EXCEPTION: ex=", request.getAttribute(RequestDispatcher.ERROR_EXCEPTION));
    log.info("ERROR_EXCEPTION_TYPE: {}", request.getAttribute(RequestDispatcher.ERROR_EXCEPTION_TYPE));
    log.info("ERROR_MESSAGE: {}", request.getAttribute(RequestDispatcher.ERROR_MESSAGE)); // ex의 경우 NestedServletException 스프링이 한번 감싸서 반환
    log.info("ERROR_REQUEST_URI: {}", request.getAttribute(RequestDispatcher.ERROR_REQUEST_URI));
    log.info("ERROR_SERVLET_NAME: {}", request.getAttribute(RequestDispatcher.ERROR_SERVLET_NAME));
    log.info("ERROR_STATUS_CODE: {}", request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE));
    log.info("dispatchType={}", request.getDispatcherType());
}
```

### DispatcherType 🌞

클라이언트로 부터 발생한 정상 요청인지, 오류 페이지를 출력하기 위한 내부 요청인지 구분하기 위해 서블릿은 `DispatcherType` 정보 제공 
- 오류 발생 시 오류 페이지 출력을 위해 WAS 내부에서 필터, 서블릿, 인터셉터를 다시 호출
- 이미 초기 요청에서 검증이 완료된 부분은 재호출 될 경우 비효율적

.

**DispatcherType**

- 서블릿 스펙은 실제 고객이 요청한 것인지, 서버가 내부에서 오류 페이지를 요청하는 것인지 `DispatcherType` 으로 구분할 수 있는 방법을 제공

```java
public enum DispatcherType {
    FORWARD, // 다른 서블릿이나 JSP 호출 ➔ RequestDispatcher.forward(request, response)
    INCLUDE, // 다른 서블릿이나 JSP 결과 포함 ➔ RequestDispatcher.include(request, response)
    REQUEST, // 클라이언트 요청
    ASYNC, // 서블릿 비동기 호출
    ERROR // 오류 요청
}
```

.

**필터와 DispatcherType**

- DispatcherType 로그 필터
  ```java
  @Slf4j
  public class LogFilter implements Filter {

      @Override
      public void init(FilterConfig filterConfig) throws ServletException {
          log.info("log filter init");
      }

      @Override
      public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
          HttpServletRequest httpRequest = (HttpServletRequest) request;
          String requestURI = httpRequest.getRequestURI();
          String uuid = UUID.randomUUID().toString();
          try {
              log.info("REQUEST [{}][{}][{}]", uuid, request.getDispatcherType(), requestURI);
              chain.doFilter(request, response);
          } catch (Exception e) {
              throw e;
          } finally {
              log.info("RESPONSE [{}][{}][{}]", uuid, request.getDispatcherType(), requestURI);
          }
      }

      @Override
      public void destroy() {
          log.info("log filter destroy");
      }
  }
  ```

- 로그 필터 등록
  ```java
  @Configuration
  public class DispatcherTypeWebConfig implements WebMvcConfigurer {

      @Bean
      public FilterRegistrationBean logFilter() {
          FilterRegistrationBean<Filter> filterRegistrationBean = new FilterRegistrationBean<>();
          filterRegistrationBean.setFilter(new LogFilter());
          filterRegistrationBean.setOrder(1);
          filterRegistrationBean.addUrlPatterns("/*");
          // default: REQUEST. 클라이언트 요청 시에만 필터 적용
          filterRegistrationBean.setDispatcherTypes(DispatcherType.REQUEST, DispatcherType.ERROR);
          return filterRegistrationBean;
      }
  }
  ```

.

**필터와 Interceptor**

- DispatcherType 로그 인터셉터

  ```java
  @Slf4j
  public class LogInterceptor implements HandlerInterceptor {
      public static final String LOG_ID = "logId";

      @Override
      public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
          String requestURI = request.getRequestURI();
          String uuid = UUID.randomUUID().toString();
          request.setAttribute(LOG_ID, uuid);
          log.info("REQUEST [{}][{}][{}][{}]", uuid, request.getDispatcherType(), requestURI, handler);
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
          log.info("RESPONSE [{}][{}][{}]", logId, request.getDispatcherType(), requestURI);
          if (ex != null) {
              log.error("afterCompletion error!!", ex);
          }
      }
  }
  ```

- 로그 인터셉터 등록

```java
@Configuration
public class DispatcherTypeWebConfig implements WebMvcConfigurer {

    /**
     * 필터는 필터 등록 시 특정 DispatcherType 인 경우 필터가 적용되도록 설정이 가능했지만,
     * 인터셉터는 스프링이 제공하는 기능이라서 DispatcherType 와 무관하게 항상 호출
     * 
     * 대신 인터셉터의 excludePathPatterns 를 사용해서 특정 경로 제외 가능
     */
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LogInterceptor())
                .order(1)
                .addPathPatterns("/**")
                .excludePathPatterns(
                        "/css/**", "/*.ico"
                        , "/error", "/error-page/**" //오류 페이지 경로
                );
    }
}
```
.

**DispatcherType 흐름**

```text
1. WAS(/error-ex, dispatchType=REQUEST) ➔ 필터 ➔ 서블릿 ➔ 인터셉터 ➔ 컨트롤러
2. 컨트롤러(예외발생) ➔ 인터셉터 ➔ 서블릿 ➔ 필터 ➔ WAS
3. WAS 오류 페이지 확인
4. WAS(/error-page/500, dispatchType=ERROR) ➔ 필터(x) ➔ 서블릿 ➔ 인터셉터(x) ➔
컨트롤러(/error-page/500) ➔ View
```

## 스프링 부트 오류 페이지 🌞

스프링 부트는 서블릿 오류 페이지 호출에 필요했던 아래 복잡한 과정을 기본으로 제공
- WebServerCustomizer 만들기
- 예외 종류에 따라 ErrorPage 추가 ➔ ErrorPage 자동 등록
  - `/error` 경로를 기본 오류 페이지로 설정
  - 서블릿 밖으로 예외가 던져지거나, `response.sendError(...)` 호출 시 모든 오류는 `/error` 호출
  - `ErrorMvcAutoConfiguration` 클래스가 오류 페이지를 자동으로 등록하는 역할
- 예외 처리용 컨트롤러(ErrorPageController) 생성 ➔ 자동 등록(`BasicErrorController`)
  - ErrorPage 에서 등록한 /error 를 매핑해서 처리하는 컨트롤러

.

### BasicErrorController

- 기본적인 오류 페이지 로직이 모두 구현
- 개발자는 오류 페이지 화면만 BasicErrorController 가 제공하는 룰과 우선순위에 따라서 등록
  - 정적 HTML 일 경우 정적 리소스, 뷰 템플릿을 사용한 동적 오류 화면일 경우 뷰 템플릿 경로에 오류 페이지 파일 생성

.

**BasicErrorController View 선택 우선순위**

.1. 뷰 템플릿
- resources/templates/error/500.html
- resources/templates/error/5xx.html

.2. 정적 리소스(static, public)
- resources/static/error/400.html
- resources/static/error/404.html
- resources/static/error/4xx.html

.3. 적용 대상이 없을 때 뷰 이름(error)
- resources/templates/error.html

> 해당 경로 위치에 HTTP 상태 코드 이름의 뷰 파일을 넣어두자.
>
> 뷰 템플릿이 정적 리소스보다 우선순위가 높고, 
> 
> 404, 500 처럼 구체적인 것이 5xx처럼 덜 구체적인 것 보다 우선순위가 높다.

.

**BasicErrorController 제공 기본 정보**

- 기본 정보를 model 에 담아 View 에 전달

```console
timestamp: Fri Feb 05 00:00:00 KST 2021
path: `/hello` (Client 요청 경로 )
status: 400
message: Validation failed for object='data'. Error count: 1
error: Bad Request
exception: org.springframework.validation.BindException
errors: Errors(BindingResult)
trace: 예외 trace
```

- `message`, `exception`, `errors`, `trace` 정보는 보안상 default 로 포함이 되어있지 않음
  - properties 설정을 통해 오류 정보를 model 에 포함할지 여부 선택
  ```properties
  # exception 포함 여부(true, false)
  server.error.include-exception=true
  # message 포함 여부
  server.error.include-message=always
  # trace 포함 여부
  server.error.include-stacktrace=always
  # errors 포함 여부
  server.error.include-binding-errors=always
  ```
  - `never`: 사용하지 않음
  - `always`: 항상 사용
  - `on_param`: 파라미터가 있을 때 해당 정보 노출
    - HTTP 요청시 파라미터(?message=&errorsa=&trace=)를 전달하면 해당 정보들이 model 에 담겨 뷰 템플릿에 출력
    - 운영 서버에서는 비권장

> 실무에서는 이 정보들을 노출하면 안된다.
> 
> 사용자에게는 깔끔한 오류 페이지와 고객이 이해할 수 있는 간단한 오류 메시지를 보여주고,
> 
> 오류는 서버에 로그로 남겨서 로그로 확인하자.

.

**스프링 부트 오류 관련 옵션**
```properties
# 오류 처리 화면을 못 찾을 경우, 스프링 whitelabel 오류 페이지 적용
server.error.whitelabel.enabled=true

# 오류 페이지 경로
# 스프링이 자동 등록하는 서블릿 글로벌 오류 페이지 경로와 BasicErrorController 오류 컨트롤러 경로에 함께 사용
server.error.path=/error
```

**확장 포인트**
- 에러 공통 처리 컨트롤러의 기능을 변경하고 싶을 경우 ErrorController 인터페이스를 상속 받아서 구현하거나, BasicErrorController 를 상속 받아서 기능을 추가해보자.

> 스프링 부트 기본 제공 오류 페이지를 활용하면 오류 페이지 관련 대부분의 문제는 손쉽게 해결 가능하다.

# API 예외 처리

`오류 페이지`는 단순히 고객에게 오류 화면을 보여주면 되지만, `API` 는 각 오류 상황에 맞는 오류 응답 스펙을 정하고, JSON으로 데이터를 응답해 주어야 한다.

**produces 설정**

```java
@RequestMapping(value = "/error-page/500", produces = MediaType.APPLICATION_JSON_VALUE)
public ResponseEntity<Map<String, Object>> errorPage500Api(HttpServletRequest request, HttpServletResponse response) {
    // ...
    return new ResponseEntity(result, HttpStatus.valueOf(statusCode));
}
```

- `produces = MediaType.APPLICATION_JSON_VALUE`
  - 클라이언트가 요청하는 HTTP Header Accept 값이 application/json 일 때 해당 메서드 호출
- ResponseEntity 는 메시지 컨버터가 동작하면서 클라이언트에게 JSON 구조로 변환하여 반환

## Spring Boot 기본 오류 처리

API 예외 처리도 스프링 부트가 제공하는 기본 오류 방식을 사용

`BasicErrorController` 코드 일부

```java
// 클라이언트 요청의 Accept 해더 값이 text/html 인 경우 호출(view 제공)
@RequestMapping(produces = MediaType.TEXT_HTML_VALUE)
public ModelAndView errorHtml(HttpServletRequest request, HttpServletResponse response) { ... }

// 그외 경우에 호출(ResponseEntity 로 HTTP Body 에 JSON 데이터 반환)
@RequestMapping
public ResponseEntity<Map<String, Object>> error(HttpServletRequest request) { ... }
```

- 스프링 부트의 기본 설정은 오류 발생시 `/error` 를 오류 페이지로 요청
- `BasicErrorController` 는 `/error` 경로를 기본으로 받음.(`server.error.path` 로 수정 가능

> `BasicErrorController` 는 HTML 오류 페이지를 제공하는 경우 매우 편리
>
> 단, API 는 각 컨트롤러나 예외마다 서로 다른 응답 결과를 출력해야 하므로 `@ExceptionHandler` 사용 권장

## ExceptionResolver

**HandlerExceptionResolver**

```java
public interface HandlerExceptionResolver {
    ModelAndView resolveException(
        HttpServletRequest request, 
        HttpServletResponse response, 
        Object handler, // 핸들러(컨트롤러) 정보
        Exception ex // 핸들러(컨트롤러)에서 발생한 예외
    ); 
}
```

- 스프링 MVC 는 컨트롤러(핸들러) 밖으로 예외가 던져진 경우 예외를 해결하고, 동작을 새로 정의할 수 있는 `HandlerExceptionResolver` 제공
  - **ExceptionResolver 적용 전 예외처리**
    ![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/before-ExceptionResolver.png?raw=true 'Result')
  - **ExceptionResolver 적용 후 예외처리**
    ![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/after-ExceptionResolver.png?raw=true 'Result')
- 참고. ExceptionResolver 로 예외를 해결해도 postHandle() 호출 X

**HandlerExceptionResolver Interface 구현**

```java
@Slf4j
public class MyHandlerExceptionResolver implements HandlerExceptionResolver {
    /**
     * ModelAndView 를 반환하는 이유는 try-catch 처럼 Exception 을 처리해서 정상 흐름처럼 변경하여 예외를 해결하는 것이 목적
     */
    @Override
    public ModelAndView resolveException(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        try {
            // IllegalArgumentException 발생 시 예외를 HTTP 상태 코드 400으로 전달
            if (ex instanceof IllegalArgumentException) {
                log.info("IllegalArgumentException resolver to 400");
                response.sendError(HttpServletResponse.SC_BAD_REQUEST, ex.getMessage());
                
                //1. 빈 ModelAndView 반환 시 뷰 렌더링을 하지 않고 정상 흐름으로 서블릿 반환
                //2. ModelAndView 에 View, Model 등의 정보를 지정하여 반환하면 뷰 렌더링
                return new ModelAndView();
            }
        } catch (IOException e) {
            log.error("resolver ex", e);
        }

        //3. null 반환 시 다음 ExceptionResolver 찾아서 실행
        //처리 가능한 ExceptionResolver 가 없을 경우 기존 발생한 예외를 서블릿 밖으로 전달
        return null;
    }
}
```

.

**HandlerExceptionResolver 반환 값에 따른 DispatcherServlet 동작 방식**

- `빈 ModelAndView`
  - new ModelAndView() 처럼 빈 ModelAndView 를 반환하면 뷰를 렌더링 하지않고, 정상 흐름으로 서블릿이 리턴
- `ModelAndView 지정`
  - ModelAndView 에 View, Model 등의 정보를 지정해서 반환하면 뷰를 렌더링
- `nul`
  - null 을 반환하면, 다음 ExceptionResolver 를 찾아서 실행
  - 만약 처리할 수 있는 ExceptionResolver 가 없으면 예외 처리가 안되고, 기존에 발생한 예외를 서블릿 밖으로 던짐

.

**ExceptionResolver 활용**

- `예외 상태 코드 변환`
  - 예외를 response.sendError(..) 호출로 변경해서 서블릿에서 상태 코드에 따른 오류를 처리하도록 위임
  - 이후 WAS 는 서블릿 오류 페이지를 찾아서 내부 호출(default. /error)
  - ex. 실제 서버에서는 500 에러가 발생하였지만 Client 에게는 4xx 코드 전달
- `뷰 템플릿 처리`
  - ModelAndView 에 값을 채워서 예외에 따른 새로운 오류 화면을 뷰 렌더링을 통해 고객에게 제공
  - return new ModelAndView("error/400");
- `API 응답 처리`
  - response.getWriter().println("hello"); 처럼 HTTP 응답 바디에 직접 데이터를 넣어서 전달
  - 여기에 JSON 으로 응답하면 API 응답 처리

.

**WebMvcConfigurer 에 등록**

```java
@Override
public void extendHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {
    resolvers.add(new MyHandlerExceptionResolver());
}
```

- `configureHandlerExceptionResolvers` 사용 시 스프링이 기본으로 등록하는 `ExceptionResolver` 가 제거되므로 `extendHandlerExceptionResolvers` 를 사용

### ExceptionResolver 적용

**Exception**

```java
public class UserException extends RuntimeException {
    public UserException() {
        super();
    }

    public UserException(String message) {
        super(message);
    }

    public UserException(String message, Throwable cause) {
        super(message, cause);
    }

    public UserException(Throwable cause) {
        super(cause);
    }

    protected UserException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
        super(message, cause, enableSuppression, writableStackTrace);
    }
}

...

// 예외 생성
throw new UserException("사용자 오류");
```

**HandlerExceptionResolver 구현**

```java
@Slf4j
public class UserHandlerExceptionResolver implements HandlerExceptionResolver {
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public ModelAndView resolveException(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        try {
            if (ex instanceof UserException) {
                log.info("UserException resolver to 400");
                String acceptHeader = request.getHeader("accept");
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);

                // HTTP 요청 해더의 ACCEPT 값이 application/json 일 경우 JSON 응답
                if ("application/json".equals(acceptHeader)) {
                    Map<String, Object> errorResult = new HashMap<>();
                    errorResult.put("ex", ex.getClass());
                    errorResult.put("message", ex.getMessage());
                    String result = objectMapper.writeValueAsString(errorResult);
                    response.setContentType("application/json");
                    response.setCharacterEncoding("utf-8");
                    response.getWriter().write(result);

                    return new ModelAndView();
                } else { // 그 외의 경우에는 TEXT/HTML 오류 페이지 노출
                    return new ModelAndView("error/500");
                }
            }
        } catch (IOException e) {
            log.error("resolver ex", e);
        }

        return null;
    }
}
```

**WebConfig 에 HandlerExceptionResolver 등록**

```java
@Override
public void extendHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {
    resolvers.add(new MyHandlerExceptionResolver());
    resolvers.add(new UserHandlerExceptionResolver());
}
```

정리.

> 컨트롤러에서 예외가 발생해도 ExceptionResolver 에서 예외를 처리
> 
> 예외가 발생해도 서블릿 컨테이너까지 예외가 전달되지 않고(결과적으로 WAS 입장에서는 정상 처리)
> 
> 스프링 MVC 에서 예외 처리는 종료

## Spring ExceptionResolver

Spring Boot 기본적으로 제공하는 ExceptionResolver

`HandlerExceptionResolverComposite` 에 아래 순서로 등록
- `ExceptionHandlerExceptionResolver`
  - `@ExceptionHandler` 처리
  - API 예외 처리는 대부분 이 기능으로 해결
- `ResponseStatusExceptionResolver`
  - HTTP 상태 코드 변경
- `DefaultHandlerExceptionResolver`
  - 스프링 내부 기본 예외 처리

### ExceptionHandler 🌞

**ExceptionHandlerExceptionResolver**

스프링은 API 예외 처리 문제를 해결하기 위해 `@ExceptionHandler` 를 사용한 편리한 예외 처리 기능 제공
- 각 시스템마다 다른 응답 모양과 스펙
- 예외에 따른 각기 다른 데이터 응답
- 컨트롤러에 따라 다른 예외 응답
- ModelAndView 가 아닌 Json 형태로 반환
- 등.. 세밀한 제어 필요

.

**`@ExceptionHandler` 예외 처리 방법**

- @ExceptionHandler 선언 후 해당 컨트롤러에서 처리하고 싶은 예외 지정
- 해당 컨트롤러에서 예외 발생 시 해당 메서드가 호출
- 지정한 예외 또는 하위 자식 클래스 모두 처리
  
  ```java
  /**
   * 부모, 자식 클래스 모두 지정되어 있을 경우 자세한 것이 우선권
   */
  @ExceptionHandler(부모예외.class)
  public String 부모예외처리()(부모예외 e) {}
  
  @ExceptionHandler(자식예외.class)
  public String 자식예외처리()(자식예외 e) {}
  ```
- 다양한 예외를 한 번에 처리 가능
  ```java
  @ExceptionHandler({AException.class, BException.class})
  public String ex(Exception e) {
      log.info("exception e", e);
  }
  ```
- 예외 생략
  
  ```java
  /**
   * 예외 생략 시 메서드 파라미터의 예외(UserException)가 지정
   */
  @ExceptionHandler
  public ResponseEntity<ErrorResult> userExHandle(UserException e) {}
  ```
- 파라미터와 응답
  - 다양한 파라미터와 응답 지정 가능
  - [@ExceptionHandler's Method Arguments And Return Values](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-exceptionhandler.html#mvc-ann-exceptionhandler-args)

.

**`@ExceptionHandler` 실행 흐름**

```java
throw new IllegalArgumentException("잘못된 입력 값");

...

@ResponseStatus(HttpStatus.BAD_REQUEST)
@ExceptionHandler(IllegalArgumentException.class)
public ErrorResult illegalExHandle(IllegalArgumentException e) {
    return new ErrorResult("BAD", e.getMessage());
}
```

- 컨트롤러 호출 결과로 예외(IllegalArgumentException)가 컨트롤러 밖으로 던져짐
- DispatcherServlet 을 거쳐 예외 발생으로 `ExceptionResolver` 작동
  - 가장 우선순위가 높은 `ExceptionHandlerExceptionResolver` 실행
- `ExceptionHandlerExceptionResolver` 는 해당 컨트롤러에 `IllegalArgumentException` 을 처리할 수 있는 `@ExceptionHandler` 가 있는지 확인
- `@ExceptionHandler` 선언 메서드 실행
  - @RestController 이므로 @ResponseBody 적용 ➔ HTTP 컨버터가 사용되고 JSON 응답
- @ResponseStatus(HttpStatus.BAD_REQUEST) 를 지정했으므로 HTTP 상태 코드 400 응답
  - 서블릿 컨테이너까지 내려가지 않고 정상 흐름으로 반환

.

**상황에 따른 `@ExceptionHandler` 활용**

```java
/**
 * 에외 처리용 클래스를 만들어서 사용하는 경우
 * 현재 Controller 에서 IllegalArgumentException 발생 시 호출
 * 
 * @ResponseStatus 는 애노테이션이므로 HTTP 응답 코드를 동적으로 변경 불가
 */
@ResponseStatus(HttpStatus.BAD_REQUEST)
@ExceptionHandler(IllegalArgumentException.class)
public ErrorResult illegalExHandle(IllegalArgumentException e) {
    return new ErrorResult("BAD", e.getMessage());
}

/**
 * 현재 Controller 에서 UserException 발생 시 호출
 * 
 * ResponseEntity 를 사용해서 HTTP 메시지 바디에 직접 응답(HTTP 컨버터 사용)
 * HTTP 응답 코드를 프로그래밍해서 동적으로 변경 가능
 */
@ExceptionHandler
public ResponseEntity<ErrorResult> userExHandle(UserException e) {
    ErrorResult errorResult = new ErrorResult("USER-EX", e.getMessage());
    return new ResponseEntity<>(errorResult, HttpStatus.BAD_REQUEST);
}

/**
 * 현재 Controller 에서 RuntimeException(Exception 의 자식 클래스) 발생 시 호출
 * 
 * 처리되지 못한 남은 예외를 처리
 */
@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
@ExceptionHandler
public ErrorResult exHandle(Exception e) {
    return new ErrorResult("EX", "내부 오류");
}

/**
 * ModelAndView 를 사용해서 오류 화면(HTML) 응답
 */
@ExceptionHandler(ViewException.class)
public ModelAndView ex(ViewException e) {
    return new ModelAndView("error");
}
```

### @ControllerAdvice 🌞

여러 컨트롤러에서 발생하는 오류를 모아서 처리

- `@ExceptionHandler` 를 사용해서 예외를 깔끔하게 처리가 가능하지만, 정상 코드와 예외 처리 코드가 하나의 컨트롤러에 섞여 있는 단점이 존재
- `@ControllerAdvice` 또는 `@RestControllerAdvice` 를 사용해서 분리해 보자.

**`@ControllerAdvice`**

```java
@RestControllerAdvice
public class ExControllerAdvice {

    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(IllegalArgumentException.class)
    public ErrorResult illegalExHandle(IllegalArgumentException e) {
        return new ErrorResult("BAD", e.getMessage());
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResult> userExHandle(UserException e) {
        ErrorResult errorResult = new ErrorResult("USER-EX", e.getMessage());
        return new ResponseEntity<>(errorResult, HttpStatus.BAD_REQUEST);
    }

    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    @ExceptionHandler
    public ErrorResult exHandle(Exception e) {
        return new ErrorResult("EX", "내부 오류");
    }
}
```

- 대상으로 지정한 여러 컨트롤러에 `@ExceptionHandler`, `@InitBinder` 기능을 부여
  - [대상 컨트롤러 지정](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-advice.html) ➔ 보통 패키지명 정도 지정
    ```java
    // Target all Controllers annotated with @RestController
    @ControllerAdvice(annotations = RestController.class)
    public class ExampleAdvice1 {}

    // Target all Controllers within specific packages
    @ControllerAdvice("org.example.controllers")
    public class ExampleAdvice2 {}
    
    // Target all Controllers assignable to specific classes
    @ControllerAdvice(assignableTypes = {ControllerInterface.class, AbstractController.class})
    public class ExampleAdvice3 {}
    ```
- @ControllerAdvice 에 대상을 지정하지 않으면 모든 컨트롤러에 적용(글로벌 적용)
- `@RestControllerAdvice` 는 @ControllerAdvice 와 동일하고, @ResponseBody 가 추가
  - @Controller, @RestController 차이와 동일

> @ExceptionHandler 와 @ControllerAdvice 를 조합하면 예외를 깔끔하게 해결 가능

### ResponseStatusExceptionResolver

예외에 따라 HTTP 상태 코드 지정
- `@ResponseStatus` 가 달려있는 예외
- `ResponseStatusException` 예외

.

**@ResponseStatus 예외**

```java
@ResponseStatus(code = HttpStatus.BAD_REQUEST, reason = "잘못된 요청 오류")
public class BadRequestException extends RuntimeException { }

...

throw new BadRequestException();
```

- 해당 예외가 컨트롤러 밖으로 넘어가면 ResponseStatusExceptionResolver 예외가 해당 애노테이션을 확인해서 `HTTP 상태 코드를 변경`(HttpStatus.BAD_REQUEST(400))하고, 메시지 포함
  - ResponseStatusExceptionResolver 에서 response.sendError(statusCode, resolvedReason) 호출
- sendError(400) 호출로 WAS 에서 다시 `오류 페이지`(/error) `내부 요청`
- reason 을 MessageSource 에서 찾는 `메세지 기능` 제공 ➔ `reason = "error.bad"`

`

**ResponseStatusException 예외**

```java
throw new ResponseStatusException(HttpStatus.NOT_FOUND, "error.bad", new IllegalArgumentException());
```

- 직접 변경할 수 없는 예외에 `ResponseStatusException` 적용
  - @ResponseStatus 는 애노테이션을 사용하므로 직접 (조건에 따라 동적으로)변경할 수 없는 예외에는 적용 불가

### DefaultHandlerExceptionResolver

- 스프링 내부에서 발생하는 스프링 예외 처리
  - 스프링 내부 오류를 어떻게 처리할지에 대한 많은 내용이 정의
- `TypeMismatchException` 으로 발생하는 500 오류를 `DefaultHandlerExceptionResolver` 가 400 오류로 변경

**DefaultHandlerExceptionResolver.handleTypeMismatch**

```java
protected ModelAndView handleTypeMismatch(TypeMismatchException ex, HttpServletRequest request, HttpServletResponse response, @Nullable Object handler) throws IOException {
  // response.sendError() 를 통해 문제 해결.
  // sendError(400) 를 호출했으므로 WAS 에서 다시 오류 페이지(/error) 내부 요청
  response.sendError(HttpServletResponse.SC_BAD_REQUEST);
  return new ModelAndView();
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