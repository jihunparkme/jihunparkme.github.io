---
layout: post
title: Exception
summary: Spring MVC Part 2. 백엔드 웹 개발 활용 기술
categories: (Inflearn)Spring-MVC-2
featured-img: spring_mvc_2
# mathjax: true
---

# Spring MVC Part 2. Exception

영한님의 [스프링 MVC 2편 - 백엔드 웹 개발 활용 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-2/) 강의 노트

[Project](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2)

# 예외 처리와 오류 페이지

## 서블릿 예외 처리

순수 서블릿 컨테이너의 예외 처리

**서블릿의 예외 처리 지원**

### Exception

- WAS는 서버 내부에서 처리할 수 없는 오류가 발생한 것으로 인지하고 HTTP Status Code 500 error return

- 예외 전달

  - 컨트롤러에서 예외가 발생하면 `WAS 까지 전파` 및 `500 Error` 적용

  - `컨트롤러 -> 스프링 인터셉터 -> 서블릿 -> 필터 -> WAS`

  ```java
  @GetMapping("/error-ex")
  public void errorEx() {
      throw new RuntimeException("예외 발생!");
  }
  ```

### response.sendError()

- HttpServletResponse 가 제공

  - response.sendError(HTTP 상태 코드, 오류 메시지)

- WAS(Servlet container) 에게 오류 발생 전달

- sendError 흐름

  - 컨트롤러에서 sendError 호출 시 `WAS 에서 sendError 호출 기록 확인`
    - Servlet Container 는 Client 에게 응답 전 response 에 sendError() 호출 확인 및 설정 `오류 페이지`에 맞는 페이지 출력
  - `컨트롤러 -> 스프링 인터셉터 -> 서블릿 -> 필터 -> WAS`

  ```java
  @GetMapping("/error-404")
  public void error404(HttpServletResponse response) throws IOException {
      response.sendError(404, "404 오류!");
  }
  ```

## 서블릿 오류 페이지

- 서블릿은 Exception 발생 후 서블릿 밖으로 전달되거나 response.sendError() 호출 시 설정된 오류 페이지를 찾음

- 오류 페이지 요청 흐름
  - `컨트롤러(예외 발생) -> 스프링 인터셉터 -> 서블릿 -> 필터 -> WAS`
  - `WAS(/error-page/500) 요청 -> 필터 -> 서블릿 -> 스프링 인터셉터 -> 컨트롤러(/error-page/500) -> View`
    - WAS 는 오류 페이지 요청 시 오류 정보를 request attribute 에 추가해서 전달

**서블릿 오류 페이지 등록**

```java
@Component
public class WebServerCustomizer implements WebServerFactoryCustomizer<ConfigurableWebServerFactory> {

    @Override
    public void customize(ConfigurableWebServerFactory factory) {

        ErrorPage errorPage404 = new ErrorPage(HttpStatus.NOT_FOUND, "/error-page/404"); //response.sendError(404)
        ErrorPage errorPage500 = new ErrorPage(HttpStatus.INTERNAL_SERVER_ERROR, "/error-page/500"); //response.sendError(500)

        ErrorPage errorPageEx = new ErrorPage(RuntimeException.class, "/error-page/500"); // RuntimeException 또는 그 자식 타입의 예외

        factory.addErrorPages(errorPage404, errorPage500, errorPageEx);
    }
}
```

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

**오류 정보 추가**

- [Code](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/97855ce96a102b8462dad02d1ae03a267df63787)

### DispatcherType

- 오류 발생 시 오류페이지 출력을 위해 WAS 내부에서 필터, 서블릿, 인터셉터 등 모두 다시 한 번 호출이 발생

- 클라이언트로 부터 발생한 정상 요청(REQUEST)인지, 오류 페이지를 출력하기 위한 내부 요청(ERROR)인지 구분을 위해 서블릿은 `DispatcherType` 정보 제공

- DispatcherType
  - `REQUEST` : 클라이언트 요청
  - `ERROR` : 오류 요청
  - `FORWARD` : 다른 서블릿이나 JSP를 호출할 경우
    <i>RequestDispatcher.forward(request, response);</i>
  - `INCLUDE` : 다른 서블릿이나 JSP의 결과를 포함할 경우
    <i>RequestDispatcher.include(request, response);</i>
  - `ASYNC` : 서블릿 비동기 호출

#### 필터

- <i>filterRegistrationBean.setDispatcherTypes(DispatcherType.REQUEST, DispatcherType.ERROR);</i> DispatcherType 설정으로 중복 호출 제거

  - default : DispatcherType.REQUEST

- [Code](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/b8723959bbd7be824db14985c834e642fa018fba)

#### 인터셉터

- <i>excludePathPatterns</i> 경로 설정으로 중복 호출 제거

- [Code](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/38ea95fa9de3563ebc6a8111a38d2e6059cddcf8)

### DispatcherType 흐름

1\. WAS(/error-ex, dispatchType=REQUEST) -> 필터 -> 서블릿 -> 인터셉터 -> 컨트롤러

- 컨트롤러에서 예외발생

2\. 컨트롤러 -> 인터셉터 -> 서블릿 -> 필터 -> WAS

- WAS 에서 오류 페이지 확인

3\. WAS(/error-page/500, dispatchType=ERROR) -> ~~필터(x)~~ -> 서블릿 -> ~~인터셉터(x)~~ -> 컨트롤러(/error-page/500) -> View

## 스프링 부트 오류 페이지

개발자는 오류 페이지 화면만 BasicErrorController 가 제공하는 룰과 우선순위에 따라서 등록하면 끝!

**Spring Boot 제공 오류 페이지**

- ErrorPage 자동 등록

  - /error 경로를 기본 오류 페이지를 설정
  - ErrorMvcAutoConfiguration 클래스가 오류 페이지 자동 등록 역할

- BasicErrorController 스프링 컨트롤러를 자동 등록

  - ErrorPage 에서 등록한 /error 를 매핑해서 처리하는 컨트롤러

**BasicErrorController 의 View 선택 순서**

1\. 뷰 템플릿

- resources/templates/error/500.html
- resources/templates/error/5xx.html

2\. 정적 리소스( static , public )

- resources/static/error/400.html
- resources/static/error/404.html
- resources/static/error/4xx.html

3\. 적용 대상이 없을 때 뷰 이름( error )

- resources/templates/error.html

### BasicErrorController

**BasicErrorController 는 기본 정보를 model에 담아 View 에 제공**

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

- message, exception, errors, trace 정보는 보안상 default 로 포함이 되어있지 않다
- 오류 정보 포함을 위해 properties 설정 필요

```properties
server.error.include-exception=true
server.error.include-message=always
server.error.include-stacktrace=always
server.error.include-binding-errors=always
```

- never : 사용하지 않음
- always : 항상 사용
- on_param : 파라미터가 있을 때 사용
  - ?message=&errors=&trace=

`단, 실무에서 오류는 서버에 로그를 남겨서 확인하자!`

**기능 확장 시**

- 에러 공통 처리 Controller 기능을 변경하고 싶을 경우 ErrorController 인터페이스를 상속 받아서 구현하거나, BasicErrorController 상속 받아서 기능을 추가

# API 예외 처리

- `produces = MediaType.APPLICATION_JSON_VALUE` 설정
  - Client 가 요청하는 HTTP Header Accept 값이 application/json 일 때 해당 메서드가 호출

1\. 예외 발생

```java
@Slf4j
@RestController
public class ApiExceptionController {

    @GetMapping("/api/members/{id}")
    public MemberDto getMember(@PathVariable("id") String id) {

        if (id.equals("ex")) {
            throw new RuntimeException("잘못된 사용자");
        }

        return new MemberDto(id, "hello " + id);
    }
}
```

2\. 예외에 따른 오류 URL 처리

```java
@Component
public class WebServerCustomizer implements WebServerFactoryCustomizer<ConfigurableWebServerFactory> {

    @Override
    public void customize(ConfigurableWebServerFactory factory) {

        ErrorPage errorPage404 = new ErrorPage(HttpStatus.NOT_FOUND, "/error-page/404"); //response.sendError(404)
        ErrorPage errorPage500 = new ErrorPage(HttpStatus.INTERNAL_SERVER_ERROR, "/error-page/500"); //response.sendError(500)

        ErrorPage errorPageEx = new ErrorPage(RuntimeException.class, "/error-page/500"); // RuntimeException 또는 그 자식 타입의 예외

        factory.addErrorPages(errorPage404, errorPage500, errorPageEx);
    }
}
```

3\. 오류 URL 선택

```java
@RequestMapping(value = "/error-page/500", produces = MediaType.APPLICATION_JSON_VALUE)
public ResponseEntity<Map<String, Object>> errorPage500Api(
        HttpServletRequest request, HttpServletResponse response) {

    log.info("API errorPage 500");

    Map<String, Object> result = new HashMap<>();
    Exception ex = (Exception) request.getAttribute(ERROR_EXCEPTION);
    result.put("status", request.getAttribute(ERROR_STATUS_CODE));
    result.put("message", ex.getMessage());

    Integer statusCode = (Integer) request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE);

    return new ResponseEntity(result, HttpStatus.valueOf(statusCode));
}

@RequestMapping("/error-page/500")
public String errorPage500(HttpServletRequest request, HttpServletResponse response) {
    log.info("errorPage 500");
    return "error-page/500";
}
```

## Spring Boot 기본 오류 처리

- Spring Boot 는 기본 설정으로 오류 발생 시 `/error` 를 요류 페이지로 요청
  - BasicErrorController 는 properties 의 `server.error.path` 를 기본 경로로 받음

**BasicErrorController.java**

```java
@RequestMapping(produces = MediaType.TEXT_HTML_VALUE)
public ModelAndView errorHtml(HttpServletRequest request, HttpServletResponse
response) {}

@RequestMapping
public ResponseEntity<Map<String, Object>> error(HttpServletRequest request) {}
```

## ExceptionResolver

`컨트롤러에서 예외가 발생해도 ExceptionResolver 에서 예외를 처리`

- 예외 상태 코드 변환

  - 예외를 `response.sendError(xxx)` 호출로 변경 후 상태 코드에 따른 오류를 서블릿이 처리하도록 위임 (이후 WAS는 서블릿 오류 페이지를 찾아서 내부 호출)
  - ex) 실제 서버에서는 500 에러가 발생하였지만 Client 에게는 4xx 코드 전달
  - ExceptionResolver 로 예외를 해결해도 postHandle() 은 호출되지 않음

- 뷰 템플릿 처리

  - `ModelAndView` 를 채워서 예외에 따른 새로운 오류 화면을 뷰 렌더링하여 Client 에게 제공
  - return new ModelAndView("error/400");

- API 응답 처리
  - HTTP Response Body 에 직접 데이터를 넣어서 전달
  - `response.getWriter().write(result);`

<center><img src="https://raw.githubusercontent.com/jihunparkme/jihunparkme.github.io/master/assets/img/posts/ExceptionResolver.jpg"></center>

### HandlerExceptionResolver 기본

**HandlerExceptionResolver Interface 구현**

```java
@Slf4j
public class MyHandlerExceptionResolver implements HandlerExceptionResolver {

    @Override
    public ModelAndView resolveException(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {

        try {
            if (ex instanceof IllegalArgumentException) {
                log.info("IllegalArgumentException resolver to 400");
                //예외를 HTTP 상태 코드 400으로 전달
                response.sendError(HttpServletResponse.SC_BAD_REQUEST, ex.getMessage());
                 //1. 빈 ModelAndView 반환 시 뷰 렌더링을 하지 않고 정상 흐름으로 서블릿 반환
                 //2. ModelAndView 에 View, Model 정보를 지정하여 반환하면 뷰 렌더링
                 return new ModelAndView();
            }
        } catch (IOException e) {
            log.error("resolver ex", e);
        }

        //3. null 반환 시
        //다음 ExceptionResolver 찾아서 실행
        //처리 가능한 ExceptionResolver 가 없을 경우 기존 발생한 예외를 서블릿 밖으로 전달
        return null;
    }
}
```

**ExceptionResolver 등록**

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void extendHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {
        resolvers.add(new MyHandlerExceptionResolver());
    }
}
```

### HandlerExceptionResolver 기본

[Code](https://github.com/jihunparkme/Inflearn_Spring_MVC_Part-2/commit/034fb3bcfa609fc0e4d0b7b155a03b2a090963b7)
