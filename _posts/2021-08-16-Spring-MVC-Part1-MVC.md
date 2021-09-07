---
layout: post
title: Spring MVC Part 1. MVC
summary: (MVC) 스프링 MVC 1편 - 백엔드 웹 개발 핵심 기술
categories: (Inflearn)Spring-MVC
featured-img: spring_mvc
# mathjax: true
---

# Spring MVC Part 1. MVC

영한님의 [스프링 MVC 1편 - 백엔드 웹 개발 핵심 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-1/dashboard) 강의 노트

# Table Of Contents

- 스프링 MVC (구조 이해)
- 스프링 MVC (기본 기능)
- 스프링 MVC (웹 페이지 만들기)

# Spring MVC Framework

## 스프링 MVC 전체 구조

![Result](https://raw.githubusercontent.com/jihunparkme/jihunparkme.github.io/master/post_img/spring_mvc.png 'Result')

1. 핸들러 조회 : 핸들러 매핑을 통해 요청 URL에 매핑된 핸들러(컨트롤러)를 조회

2. 핸들러 어댑터 조회 : 핸들러를 실행할 수 있는 핸들러 어댑터를 조회

3. 핸들러 어댑터 실행 : 핸들러 어댑터를 실행

4. 핸들러 실행 : 핸들러 어댑터가 실제 핸들러를 실행

5. ModelAndView 반환 : 핸들러 어댑터는 핸들러가 반환하는 정보를 ModelAndView로 변환해서 반환

6. viewResolver 호출 : viewResolver를 찾고 실행 (JSP의 경우 InternalResourceViewResolver 가 자동 등록&사용)

7. View 반환 : viewResolver는 뷰의 논리 이름을 물리 이름으로 바꾸고, 렌더링 역할을 담당하는 뷰 객체 반환 (JSP의 경우 InternalResourceView(JstlView) 를 반환하는데, 내부에 forward() 로직 존재)

8. 뷰 렌더링 : 뷰를 통해서 뷰를 렌더링

**주요 인터페이스**

`HandlerMapping`, `HandlerAdapter`, `ViewResolver`, `View`

## HandlerMapping & HandlerAdapter

**컨트롤러 호출 과정**

(1) 핸들러 매핑으로 핸들러 조회

- HandlerMapping 을 순서대로 실행해서, 핸들러 찾기

  - RequestMappingHandlerMapping : 애노테이션 기반의 컨트롤러인 @RequestMapping에서
    사용
  - BeanNameUrlHandlerMapping : 스프링 빈의 이름으로 핸들러를 찾는다.

- 빈 이름으로 핸들러를 찾을 경우, 빈 이름으로 핸들러를 찾아주는 BeanNameUrlHandlerMapping 가 실행에 성공하고 핸들러인 Controller 를 반환

(2) 핸들러 어댑터 조회

- HandlerAdapter 의 supports() 를 순서대로 호출

  - RequestMappingHandlerAdapter : 애노테이션 기반의 컨트롤러인 @RequestMapping에서사용

  - HttpRequestHandlerAdapter : HttpRequestHandler 처리

  - SimpleControllerHandlerAdapter : Controller 인터페이스 (애노테이션X, 과거에 사용) 처리

- SimpleControllerHandlerAdapter 가 Controller 인터페이스를 지원하므로 대상이 된다.

(3) 핸들러 어댑터 실행

- 디스패처 서블릿이 조회한 SimpleControllerHandlerAdapter 를 실행하면서 핸들러 정보도 함께 넘겨준다.

- SimpleControllerHandlerAdapter 는 핸들러인 Controller 를 내부에서 실행하고, 그 결과를 반환

## ViewResolver

**ViewResolver 호출 과정**

(1) 핸들러 어댑터 호출

- 핸들러 어댑터를 통해 논리 뷰 이름을 획득

(2) ViewResolver 호출

- 논리 뷰 이름으로 viewResolver를 순서대로 호출

  - BeanNameViewResolver : 빈 이름으로 뷰를 찾아서 반환
  - InternalResourceViewResolver : JSP를 처리할 수 있는 뷰를 반환

- 논리 뷰 이름의 스프링 빈으로 등록된 뷰가 없다면 InternalResourceViewResolver 가 호출

(3)InternalResourceViewResolver

- InternalResourceView 를 반환

(4) 뷰 - InternalResourceView

- InternalResourceView 는 JSP처럼 포워드 forward() 를 호출해서 처리할 수 있는 경우에 사용

(5) view.render()
view.render() 가 호출되고 InternalResourceView 는 forward() 를 사용해서 JSP를 실행

# Spring MVC 기본 기능

**프로젝트**

- Jar 사용 시 항상 내장 서버(tomcat..)를 사용 (내장 서버 최적화)

- War 사용 시 주로 외부 서버에 배포하는 목적으로 사용

## Logging

- SpringBoot 가 기본으로 제공하는 Logback
  을 대부분 사용

  - SLF4J interface 의 구현체인 Logback

- 로그 레벨 설정

  - application.properties 에서 log level 설정 가능

    - TRACE > DEBUG > INFO > WARN > ERROR

    - 보통 개발 서버는 debug, 운영 서버는 info level

    ```properties
    # 전체 로그 레벨 설정 (default: info)
    logging.level.root=info

    # 특정 패키지와 그 하위 로그 레벨 셀정
    logging.level.hello.springmvc=trace
    ```

- 로그 선언

  - Lombok 사용 시

    ```java
    @Slf4j
    ```

  - java 코드로 선언 시

    ```java
    private final Logger log = LoggerFactory.getLogger(getClass());
    // OR
    private static final Logger log = LoggerFactory.getLogger(Xxx.class)
    ```

- 로그 호출

  ```java
  // 2021-08-31 22:11:10.267  INFO 6688 --- [nio-8080-exec-6] hello.springmvc.basic.LogTestController  :  info log = Spring
  // 시간 / 로그 / 프로세스 ID / Thread Name / Class Name // Message
  log.trace(" trace log = {}", name);
  log.debug(" debug log = {}", name);
  log.info("   info log = {}", name);
  log.warn("   warn log = {}", name);
  log.error(" error log = {}", name);
  ```

> [SLF4J](http://www.slf4j.org)
>
> [Logback](http://logback.qos.ch)
>
> [스프링 부트가 제공하는 로그 기능](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-bootfeatures.html#boot-features-logging)

## 요청 매핑

- Controller Annotation

  - @Controller : 반환 값이 String 이면 뷰 이름으로 인식(뷰를 찾고 랜더링)

  - @RestController : 반환 값으로 뷰를 찾는 것이 아니라, HTTP 메시지 바디에 바로 입력

- 축약 Annotation

  ```java
    /**
     * 회원 목록 조회: GET /users
     * 회원 등록:      POST /users
     * 회원 조회:      GET /users/{userId}
     * 회원 수정:      PATCH /users/{userId}
     * 회원 삭제:      DELETE /users/{userId}
     */
    @GetMapping(value = "/mapping-get-v2")
    public String mappingGetV2() {
        log.info("mapping-get-v2");
        return "ok";
    }
  ```

- @PathVariable : 최근 HTTP API는 리소스 경로에 식별자를 넣는 스타일을 선호

  ```java
  @GetMapping("/mapping/users/{userId}/orders/{orderId}")
  public String mappingPath(@PathVariable String userId, @PathVariable Long orderId) {

    log.info("mappingPath userId={}, orderId={}", userId, orderId);
    return "ok";
  }
  ```

- 특정 파라미터/헤더로 추가 매핑

  - 파라미터의 경우 params, 헤더의 경우 headers
  - params = {"mode=debug","data=good"}

  ```java
  /**
     * headers="mode",
     * headers="!mode"
     * headers="mode=debug"
     * headers="mode!=debug" (! = )
     */
    @GetMapping(value = "/mapping-header", headers = "mode=debug")
    public String mappingHeader() {
        log.info("mappingHeader");
        return "ok";
    }
  ```

- Content-Type 헤더 기반 추가 매핑 Media Type

  - Server 입장에서 특정 Media Type만 받을 수 있다고 요청 헤더의 Content-Type으로 전달

  ```java
    /**
     * Content-Type 헤더 기반 추가 매핑 Media Type
     * consumes="application/json"
     * consumes="!application/json"
     * consumes="application/*"
     * consumes="*\/*"
     * MediaType.APPLICATION_JSON_VALUE
     */
    @PostMapping(value = "/mapping-consume", consumes = MediaType.APPLICATION_JSON_VALUE)
    public String mappingConsumes() {
        log.info("mappingConsumes");
        return "ok";
    }
  ```

- Accept 헤더 기반 Media Type

  - Client 입장에서 특정 Media Type만 받을 수 있다고 요청 헤더의 Accept로 전달

  ```java
    /**
     * Accept 헤더 기반 Media Type
     * produces = "text/html"
     * produces = "!text/html"
     * produces = "text/*"
     * produces = "*\/*"
     */
    @PostMapping(value = "/mapping-produce", produces = MediaType.TEXT_HTML_VALUE)
    public String mappingProduces() {
        log.info("mappingProduces");
        return "ok";
    }
  ```

## HTTP Request

- HttpServletRequest request

- HttpServletResponse response

- HttpMethod httpMethod

  - HTTP 메서드를 조회 (org.springframework.http.HttpMethod)

- Locale locale

  - Locale 정보를 조회

- @RequestHeader MultiValueMap<String, String> headerMap

  - 모든 HTTP 헤더를 MultiValueMap 형식으로 조회

- @RequestHeader("host") String host

  - 특정 HTTP 헤더를 조회

  - 속성 (required, defaultValue)

- @CookieValue(value = "myCookie", required = false) String cookie

  - 특정 쿠키를 조회

  - 속성 (required, defaultValue)

> [Spring Method Arguments](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#mvc-ann-arguments)
>
> [Spring Return Values](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#mvc-ann-return-types)

## Http Request Data

**클라이언트에서 서버로 데이터를 전달하는 방법**

- **GET** - Query Parameter

  - /url?username=hello&age=20
  - URL Query Parameter에 데이터를 포함해서 전달
    - ex) 검색, 필터, 페이징 등

- **POST** - HTML Form

  - content-type: application/x-www-form-urlencoded
  - Message Body에 Query Parameter 형식으로 전달 (username=hello&age=20)
    - ex) 회원 가입, 상품 주문, HTML Form

- **HTTP message body**에 데이터를 직접 담아서 요청

  - HTTP API에서 주로 사용, JSON, XML, TEXT
  - POST, PUT, PATCH

## @RequestParam

```java
@RequestParam(value="name" required = false, defaultValue = "-1") String name
```

- 파라미터 이름으로 바인딩

  - request.getParameter("name") 와 동일한 효과

- 생략

  - HTTP 파라미터 이름이 변수 이름과 같으면 value name 생략 가능
  - String, int 등 단순 타입이면 @RequestParam 생략 가능

- required

  - 파라미터 필수 여부 (default = true )

- defaultValue

  - 기본 값 적용 (빈 문자도 기본 값으로 처리)

- requestParamMap
  - 모든 요청 파라미터 받기
  - @RequestParam Map<String, Object> paramMap
    - paramMap.get("username")
  - 파라미터 값이 여러개라면 MultiValueMap 사용

**@ResponseBody**

- String return 시 View 조회를 무시하고, HTTP message body에 직접 해당 내용 입력

**@ModelAttribute**

- 바인딩할 객체 생성

- 요청 파라미터의 이름으로 바인딩 객체의 프로퍼티를 찾고, 해당 프로퍼티의 setter를 호출해서 파라미터의 값을 입력(바인딩)

  - ex) 파라미터 이름이 username 이면 setUsername() 메서드를 찾아 호출하면서 값을 입력

## HTTP message body

- HTTP Message Body Data 를 InputStream 을 사용해서 직접 읽을 수도 있지만, Spring MVC는 HttpEntity 지원

  ```java
   /**
     * HttpEntity: HTTP header, body 정보를 편라하게 조회 및 응답
     * - HttpMessageConverter 사용 -> StringHttpMessageConverter 적용
     */
    @PostMapping("/request-body-string-v3")
    public HttpEntity<String> requestBodyStringV3(HttpEntity<String> httpEntity) {

        String messageBody = httpEntity.getBody();
        log.info("messageBody={}", messageBody);
        return new HttpEntity<>("ok");
    }
  ```

- HttpEntity를 상속받은 RequestEntity, ResponseEntity

  - RequestEntity : HttpMethod, url 정보 등 추가 정보 제공
  - ResponseEntity : HTTP 상태 코드 설정 가능
    ```java
    return new ResponseEntity<String>("Hello World", responseHeaders, HttpStatus.CREATED)
    ```

- @RequestBody 사용

  - header 가 필요하다면 @RequestHeader

  ```java
  @ResponseBody
  @PostMapping("/request-body-string-v4")
  public String requestBodyStringV4(@RequestBody String messageBody) {

      log.info("messageBody={}", messageBody);
      return "ok";
  }
  ```
