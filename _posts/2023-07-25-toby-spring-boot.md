---
layout: post
title: Toby Spring Boot
summary: 토비의 스프링 부트 이해와 원리
categories: Spring-Conquest
featured-img: toby-spring-boot
# mathjax: true
---

# Spring Boot

[Spring Boot Documentation](https://spring.io/projects/spring-boot)

> 스프링 부트는 **스프링 기반**으로 실무 환경에 사용 가능한 수준의 **독립실행형 애플리케이션**을 
> 
> 복잡한 고민 없이 빠르게 작성할 수 있게 도와주는 여러가지 `도구의 모음`

**특징**

- 독립형 스프링 애플리케이션 생성
- Tomcat, Jetty, Undertow 등을 포함(WAR 파일 배포 불필요)
- 빌드 구성을 단순화하기 위해 독자적인 'startor' 종속성 제공
- 가능할 때마다 자동으로 스프링 및 타사 라이브러리 구성
- 메트릭, 상태 확인 및 외부화된 구성과 같은 프로덕션 준비 기능 제공
- 코드 생성 및 XML 구성에 대한 요구 사항 불필요

.

**`Containerless`**

- 스프링 애플리케이션 개발에 요구되는 Servlet Container 관련 설정 지원을 위한 개발 도구와 아키텍처 지원
  - 애플리케이션 개발의 핵심이 아닌 단순 반복 작업 제거
  - 서블릿 컨테이너 설치, WAR 폴더 구조, web.xml, WAR 빌드, 컨테이너로 배치, 포트 설정, 클래스 로더, 로깅 ... 
- 독립실행형(standalone) 자바 애플리케이션으로 동작
  - main 메서드 실행만으로 Servlet Container 관련 모든 필요 작업이 수행

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/Containerless.png?raw=true 'Result')

.

**`Opinionated Tool`**

**Spring**
- 극단적 유연함을 추구하고 다양한 관점을 수용하는 것이 설계 철학이었지만..
- 각종 라이브러리의 의존관계와 버전 호환성을 체크하는 작업은 고되고 쉽지 않은 작업

  
**Spring Boot**
- opinionated 설계: 자기 주장이 강하고 자신의 의견을 고집한 설계 철학
  - 일단 정해주는 대로 빠르게 개발하고 나중에 고민. 스프링을 잘 활용할 수 있는 방법 제공
- 스프링 부트는 각 라이브러리의 버전마다 사용할 기술의 종류 선정
  - 사전 검증된 추천 기술, 라이브러리 구성, 의존 관계와 적용 버전, 세부 구성(DI)과 디폴트 설정 등 제공
  - 디폴트 구성을 커스터마이징 할 수 있는 유연한 방법 제공

## Start to Develop

**`JDK`**

- [SDK-MAN(The Software Development Kit Manager)](https://sdkman.io/)
  - Unix 기반 시스템에서 여러 소프트웨어 개발 키트의 병렬 버전을 관리하기 위한 도구
  - java 버전 확인 ➔ `sdk list java`
  - 특정 identifier 설치 ➔ `sdk install java {id}`
  - 해당 디렉토리에서 특정 버전의 java 사용 ➔ `sdk use java {id}`
- [jabba](https://github.com/shyiko/jabba)
  - Java 버전 관리자

.

**API Test Method**

- 웹 브라우저 개발자 도구 - Network
- curl
- [HTTPie](https://httpie.io/)
- Intellij IDEA Ultimate- http request
- [Postman API Platform](https://www.postman.com/)
- JUnit Test
- ...

.

**HTTP Request and Response**

```http
❯ http -v ":8080/hello?name=Spring"
GET /hello?name=Spring HTTP/1.1
Accept: */* --> 클라이언트가 선호하는 미디어 타입
Accept-Encoding: gzip, deflate --> 클라이언트가 선호하는 압축 인코딩
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/3.2.1

HTTP/1.1 200
Connection: keep-alive
Content-Length: 12
Content-Type: text/plain;charset=UTF-8 --> 표현 데이터의 형식
Date: Thu, 01 Dec 2022 01:45:15 GMT
Keep-Alive: timeout=60
Hello Spring
```

## Standalone Servlet Application

**Start Servlet Container**

```java
import org.springframework.boot.web.embedded.tomcat.TomcatServletWebServerFactory;
import org.springframework.boot.web.server.WebServer;
import org.springframework.boot.web.servlet.server.ServletWebServerFactory;

public class HellobootApplication {
	public static void main(String[] args) {
		ServletWebServerFactory serverFactory = new TomcatServletWebServerFactory();
		WebServer webServer = serverFactory.getWebServer();
		webServer.start();
	}
}
```

**Register Servlet in ServletContext**

```java
ServletWebServerFactory serverFactory = new TomcatServletWebServerFactory();
		WebServer webServer = serverFactory.getWebServer(servletContext -> {
			servletContext.addServlet("hello", new HttpServlet() {
				@Override
				protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
					String name = req.getParameter("name");

					resp.setStatus(HttpStatus.OK.value());
					resp.setHeader(HttpHeaders.CONTENT_TYPE, MediaType.TEXT_PLAIN_VALUE);
					resp.getWriter().println("hello " + name);
				}
			}).addMapping("/servlet/hello");
		});
		webServer.start();
```

**Front Controller Pattern**

- 여러 요청을 처리하는데 반복적으로 등장하는 공통 작업을 하나의 오브젝트에서 일괄적으로 처리하게 만드는 방식
- 모든 요청, 혹은 일정 패턴을 가진 요청을 하나의 서블릿이 담당하도록 매핑
- 프론트 컨트롤러의 두 가지 중요한 기능은 매핑과 바인딩
  - 매핑:프론트 컨트롤러가 HTTP 요청을 처리할 핸들러를 결정하고 연동하는 작업
  - 바인딩: 핸들러에게 웹 요청 정보를 추출하고 의미있는 오브젝트에 담아서 전달하는 작업
- 프론트 컨트롤러로 전환
  ```java
  ServletWebServerFactory serverFactory = new TomcatServletWebServerFactory();
		WebServer webServer = serverFactory.getWebServer(servletContext -> {
			HelloController helloController = new HelloController();

			servletContext.addServlet("frontController", new HttpServlet() {
				@Override
				protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
					// 인증, 보안, 다국어, 공통 기능 ..
					if (req.getRequestURI().equals("/servlet/hello") && req.getMethod().equals(HttpMethod.GET.name())) {
						String name = req.getParameter("name");

						String ret = helloController.hello(name);

						resp.setStatus(HttpStatus.OK.value());
						resp.setHeader(HttpHeaders.CONTENT_TYPE, MediaType.TEXT_PLAIN_VALUE);
						resp.getWriter().println(ret);
					}
					else if (req.getRequestURI().equals("/user")) {
						// ...
					}
				 	else {
						resp.setStatus(HttpStatus.NOT_FOUND.value());
					}

				}
			}).addMapping("/*");
		});
		webServer.start();
  ```

## Standalone Spring Application

스프링 컨테이너는 애플리케이션 로직이 담긴 평범한 자바 오브젝트(POJO)와 구성 정보(Configuration Metadata)를 런타임에 조합해서 동작하는 최종 애플리케이션을 생성

```java
// 스프링 컨테이너 생성
GenericApplicationContext applicationContext = new GenericApplicationContext(); 
// 빈 오브젝트 클래스 정보 등록
applicationContext.registerBean(HelloController.class); 
// 구성 정보로 컨테이너 초기화(빈 오브젝트를 직접 생성)
applicationContext.refresh(); 

...

// 컨테이너가 관리하는 빈 오브젝트 획득
HelloController helloController = applicationContext.getBean(HelloController.class); 
```

스프링 컨테이너는 `싱글톤 레지스트리`라고도 불린다.
- 싱글톤 패턴과 유사하게 애플리케이션이 동작하는 동안 단 하나의 오브젝트만을 만들고 사용되도록 지원

**Dependency Injection**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/assembler.png?raw=true 'Result')

- `DI`를 위해 N개의 오브젝트(인터페이스 구현체)가 동적으로 의존관계를 가지도록 도와주는 `어셈블러`가 필요
- `스프링 컨테이너`(어셈블러)는 DI를 가능하도록 도와주는 `어셈블러`로 동작
  - 의존관계가 없는 클래스들의 오브젝트로 서로 관계를 연결시켜주고 사용할 수 있도록 설정
- 스프링 컨데이너는 메타 정보를 가지고 클래스에 싱글톤 오브젝트를 생성
  - 생성된 오브젝트가 사용할 다른 의존 오브젝트가 있다면 의존성 주입
  - 의존성 주입 방법으로는 생성자 주입, 팩터리 메서드 등 존재

**DispatcherServlet**

- 스프링은 프론트 컨트롤러와 같은 역할을 담당하는 DispatcherServlet 을 가지고 있다.
- DispatcherServlet 은 서블릿으로 등록되어서 동작하면서, 스프링 컨테이너를 이용해서 요청을 전달할 핸들러인 컨트롤러 오브젝트를 가져와 사용
- DispatcherServlet 이 사용하는 스프링 컨테이너는 GenericWebApplicationContext 를 이용해서 작성

**애노테이션 매핑 정보**

- DispatcherServlet 은 스프링 컨테이너에 등록된 빈 클래스에 있는 매핑 애노테이션 정보를 참고해서 웹 요청을 전달할 오브젝트와 메소드를 선정
- 클래스 레벨의 @RequestMapping 과 메소드 레벨의 @GetMapping 두 가지의 정보를 조합해서 매핑에 사용할 최종 정보 생성
- 컨트롤러 메소드의 리턴값을 웹 요청의 바디에 적용하도록 @ResponseBody 선언
  - 그렇지 않으면 String 타입의 응답은 뷰 이름으로 해석하고 Thymeleaf 같은 뷰 템플릿을 탐색(이 경우 404 에러 발생)
  - @RestController 는 @ResponseBody 를 포함하고 있으므로 메소드 레벨의  @ResponseBody 를 넣지 않아도 적용된 것처럼 동작
  ```java
  @RequestMapping("/hello")
  public class HelloController {
      ...
      @GetMapping
      @ResponseBody
      public String hello(String name) {
          return helloService.sayHello(Objects.requireNonNull(name));
      }
  }
  ```

**스프링 컨테이너로 통합**
- 스프링 컨테이너의 초기화 작업 중에 호출되는 훅 메소드에 서블릿 컨테이너(톰캣)을 초기화하고 띄우는 코드 삽입

```java
GenericWebApplicationContext applicationContext = new GenericWebApplicationContext() {
    @Override
    protected void onRefresh() {
        super.onRefresh();

        ServletWebServerFactory serverFactory = new TomcatServletWebServerFactory();
        WebServer webServer = serverFactory.getWebServer(servletContext -> {
            servletContext.addServlet("dispatcherServlet",
                    new DispatcherServlet(this)
            ).addMapping("/*");
        });
        webServer.start();
    }
}; 
```