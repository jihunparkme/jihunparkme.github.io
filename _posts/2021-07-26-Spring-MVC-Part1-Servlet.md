---
layout: post
title: Spring MVC Part 1. Servlet
summary: 스프링 MVC 1편 - 백엔드 웹 개발 핵심 기술
categories: (Inflearn)Spring-MVC
featured-img: spring_mvc
# mathjax: true
---

# Spring MVC Part 1. Servlet

영한님의 [스프링 MVC 1편 - 백엔드 웹 개발 핵심 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-1/dashboard) 강의 노트

# Table Of Contents

- Web Application
  - Web Server / Web Application Server
  - Servlet
  - Multi Thread
  - HTML, API, SSR, CSR
- Servlet
  - HttpServletRequest
  - Http Request Data
  - HttpServletResponse
  - Http Response Data
- Servlet, JSP, MVC pattern
  - 개요
  - 적용
  - 한계
- MVC 프레임워크 만들기
- 스프링 MVC (구조 이해)
- 스프링 MVC (기본 기능)
- 스프링 MVC (웹 페이지 만들기)

# Web Application

## Web Server

- HTTP 기반으로 동작
- 정적 리소스(HTML, CSS, JS, Img, Video ..) 제공
- ex) NGINX, APACHE

## Web Application Server (WAS)

- HTTP 기반 동장
- Web server 기능 포함 + 정적 리소스
- Application Logic 수행
  - 동적 HTML, REST API, Servlet, JSP, Spring MVC
- ex) Tomcat, Undertow

## Web System

- Client -> Web Server -> WAS -> DB
  - WAS의 서버 과부하 문제 해결
  - Web Server 에서 정적 리소스 처리
  - WAS 에서는 Application Logic 동적 처리
  - 효율적인 리소스 관리 (필요에 따라 서버 증설)

## Servlet

**Servlet**

- urlPatterns의 URL이 호출되면 서블릿 코드 실행
- HttpServletRequest 로 HTTP 요청 정보를 편리하게 사용
- HttpServletResponse 로 HTTP 응답 정보를 편리하게 제공

**Servlet Container**

- Servlet 을 지원하는 WAS
- Servlet 객체를 생성/초기화/호출/종료하는 생명주기 관리
- Servlet 객체는 싱글톤으로 관리
- JSP 도 Servlet 으로 변환 되어 사용
- 동시 요청을 위한 **멀티 쓰레드 처리** 지원

## Multi Thread

**Thread**

- Application 코드를 하나하나 순차적으로 실행하는 것

**Thread pool**

- 필요한 Thread 를 Thread Pool 에 보관하고 관리
- Thread Pool 에 생성 가능한 Thread 의 최대치를 관리
  - Tomcat default : 최대 200개
- WAS 주요 튜닝 포인트는 `Max Thread`
  - 너무 낮을 경우 : 동시 요청이 많으면, 서버 리소스는 여유롭지만, 클리이언트는 응답 지연
  - 너무 높을 경우 : 동시 요청이 많으면, CPU, 메모리 리소스 임계점 초과로 서버 다운
  - 장애 발생 시 : 클라우드일 경우 서버를 늘린 후 튜닝, 아니면 그냥 빡튜닝..
- 개발자가 Multi Thread 관련 코드를 신경쓰지 않아도 됨 (Multi Thread 에 대한 부분은 WAS가 처리)
  - 단, Max Thread 튜닝이 중요
- 성능 테스트 Tool : <i>nGrinder</i>, Apache ab, JMeter

## HTML, API, SSR, CSR

### HTMl

**Static Resources**

- HTML, CSS, JS, image, vedio ..
- Web Browser ➜ Web Server ➜ Static Resources

**HTML 페이지**

- 동적 HTML 파일을 생성해서 전달
- JSP, Thymeleaf ..
- Web Browser ➜ WAS (HTML) ➜ DB

**HTML API**

- 데이터(주로 JSON) 전달
- Web Browser ➜ WAS (DATA) ➜ DB
- Web/App Client, Server to Server

### SSR

- Server Side Rendering
- 서버에서 최종 HTML을 생성해서 클라이언트에 전달 (주로 **정적** 화면)
- JSP, Thymeleaf ..

### CSR

- HTML 결과를 Javascript를 사용해 웹 브라우저에서 **동적**으로 생성해서 적용 (Google Map, Gmail ..)
- React, Vue.js

---

# Servlet

## Project

**IntelliJ**

- JSP 사용을 위해 War Packaging 사용
- Java 직접 실행 설정
  - Preferences Build ➜ Execution ➜ Deployment Build Tools Gradle
- Lombok 적용
  - Preferences ➜ plugin ➜ lombok
  - Preferences ➜ Annotation Processors ➜ Enable annotation processing check

**HTTP 요청 메시지 로그 확인**

- application.properties
  - logging.level.org.apache.coyote.http11=debug

## HttpServletRequest

- HTTP Start Line 조회

```java
private void printStartLine(HttpServletRequest request) {

    System.out.println("request.getMethod() = " + request.getMethod()); //GET
    System.out.println("request.getProtocal() = " + request.getProtocol()); // HTTP/1.1
    System.out.println("request.getScheme() = " + request.getScheme()); //http
    System.out.println("request.getRequestURL() = " + request.getRequestURL()); // http://localhost:8080/request-header
    System.out.println("request.getRequestURI() = " + request.getRequestURI()); // request-header
    System.out.println("request.getQueryString() = " + request.getQueryString());  // username=park
    System.out.println("request.isSecure() = " + request.isSecure()); //https 사용 유무
}
```

- HTTP Header 편의 조회

```java
private void printHeaderUtils(HttpServletRequest request) {

    System.out.println("[Host]");
    System.out.println("request.getServerName() = " + request.getServerName()); //Host 헤더
    System.out.println("request.getServerPort() = " + request.getServerPort()); //Host 헤더

    System.out.println("[Accept-Language]");
    request.getLocales().asIterator()
            .forEachRemaining(locale -> System.out.println("locale = " + locale));
    System.out.println("request.getLocale() = " + request.getLocale());

    System.out.println("[cookie]");
    if (request.getCookies() != null) {
        for (Cookie cookie : request.getCookies()) {
            System.out.println(cookie.getName() + ": " + cookie.getValue());
        }
    }

    System.out.println("[Content]");
    System.out.println("request.getContentType() = " + request.getContentType()); //Get Method 일 경우 null
    System.out.println("request.getContentLength() = " + request.getContentLength());
    System.out.println("request.getCharacterEncoding() = " + request.getCharacterEncoding());
}
```

- HTTP 기타 정보

```java
private void printEtc(HttpServletRequest request) {

    System.out.println("[Remote 정보]");
    System.out.println("request.getRemoteHost() = " + request.getRemoteHost());
    System.out.println("request.getRemoteAddr() = " + request.getRemoteAddr());
    System.out.println("request.getRemotePort() = " + request.getRemotePort());

    System.out.println("[Local 정보]");
    System.out.println("request.getLocalName() = " + request.getLocalName());
    System.out.println("request.getLocalAddr() = " + request.getLocalAddr());
    System.out.println("request.getLocalPort() = " + request.getLocalPort());
}
```

## HTTP Request Data

**Client to Server (Http Request Data)**

### `Get` (URL Query Parameter)

- HTTP Message Body 를 사용하지 않으므로 Content-type 이 없음

- request.getParameter("name");

- ex) 검색, 필터, 페이징

### `Post` (HTML Form)

- Content-type: application/x-www-form-urlencoded

  - Query Parameter in Message Body
  - HTTP Message Body 에 데이터를 포함해서 전달하므로 Content-type 에 포함된 데이터 형식을 지정

- request.getParameter("name");

  - URL Query Parameter 형식과 동일

- ex) 회원가입, 상품주문

### `HTTP Message Body`

- 데이터 형식은 주로 JSON

- ex) HTTP API

## HttpServletResponse

- Status-line

```java
response.setStatus(HttpServletResponse.SC_OK); //200
```

- Content-type

```java
/**
 * response.setHeader("Content-Type", "text/plain;charset=utf-8");
 * response.setContentLength(2); //생략 시 자동 생성
 */
response.setContentType("text/plain");
response.setCharacterEncoding("utf-8");
```

- Cookie

```java
/**
 * response.setHeader("Set-Cookie", "myCookie=good; Max-Age=600");
 */
Cookie cookie = new Cookie("myCookie", "good");
cookie.setMaxAge(600); //초
response.addCookie(cookie);
```

- Redirect

```java
/**
 * response.setStatus(HttpServletResponse.SC_FOUND); //302
 * response.setHeader("Location", "/basic/hello-form.html");
 */
response.sendRedirect("/basic/hello-form.html");
```

- Response-headers

```java
response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate"); // 캐시 무효화
response.setHeader("Pragma", "no-cache"); // 캐시 무효화(과거 버전)
response.setHeader("my-header","hello");
```

- Mmessage body

```java
PrintWriter writer = response.getWriter();
writer.println("ok");
```

## HTTP Response Data

**Server to Client**

### `단순 텍스트`

```java
response.getWriter().println("ok");
```

### `HTML`

```java
//Content-Type: text/html;charset=utf-8
response.setContentType("text/html");
response.setCharacterEncoding("utf-8");

PrintWriter writer = response.getWriter();
writer.println("<html>");
writer.println("<body>");
writer.println(" <div>HTML Test</div>");
writer.println("</body>");
writer.println("</html>");
```

### `HTML API (MessageBody JSON)`

```java
//..
  private ObjectMapper objectMapper = new ObjectMapper();

  @Override
  protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

      //Content-Type: application/json
      response.setContentType("application/json");
      response.setCharacterEncoding("utf-8");

      HelloData data = new HelloData();
      data.setUsername("kim");
      data.setAge(20);

      //Object to Json
      //{"username":"kim","age":20}
      String result = objectMapper.writeValueAsString(data);
      response.getWriter().write(result);
  }
```

## MVC 프레임워크 만들기

- 목차
