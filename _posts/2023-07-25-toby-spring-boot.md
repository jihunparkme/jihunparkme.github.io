---
layout: post
title: Toby Spring Boot
summary: 토비의 스프링 부트 이해와 원리
categories: Spring-Conquest
featured-img: toby-spring-boot
# mathjax: true
---

# Spring Boot

토비님의 [토비의 스프링 부트 - 이해와 원리](https://www.inflearn.com/course/%ED%86%A0%EB%B9%84-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8-%EC%9D%B4%ED%95%B4%EC%99%80%EC%9B%90%EB%A6%AC/dashboard) 강의 노트

[Project](https://github.com/jihunparkme/inflearn-toby-spring-boot)

---


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

**@Component Scan**

- 클래스에 애노테이션을 선언하고, 이를 스캔해서 스프링 컨테이너의 빈으로 자동 등록
  - 애플리케이션의 메인 클래스에는 @ComponentScan 선언
  - 등록 대상이 될 클래스에는 @Component 선언
  - @Component 는 메타 애노테이션으로 가지고 있는 애노테이션도 사용 가능
    - @Controller, @RestController, @Service 등..
- @RestController
  - @RestController 는 @Controller 를 메타 애노테이션으로 가지고 있고, 
  - @Controller 는 @Component를 메타 애노테이션으로
  - 이 경우 @RestController 는 @Component 애노테이션이 붙은 것과 같은 효과
  - @RestController 가 붙은 경우 DispatcherServlet 의 매핑 정보 탐색 대상이 되므로 클래스 레벨에 매핑 애노테이션(@RequestMapping) 불필요
  ```java
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.RUNTIME)
  @Documented
  @Controller
  @ResponseBody
  public @interface RestController {}
  ```

**Bean의 생명주기 메소드**

```java
/** 
 * @Bean 메소드에서 독립적으로 생성
 * 
 * DispatcherServlet 이 필요로 하는 WebApplicationContext 타입 컨테이너 오브젝트는 -> dispatcherServlet.setApplicationContext(this);
 * 스프링 컨테이너의 빈 생애주기 메소드를 이용해서 주입 빋게 된다.
 */
@Bean
public DispatcherServlet dispatcherServlet() {
    return new DispatcherServlet();
}
```

- DispatcherServlet 은 `ApplicationContextAware` 라는 스프링 컨테이너를 setter 메소드로 주입해주는 메소드를 가진 인터페이스를 구현
- 이러한 `생애주기 빈 메소드`를 가진 빈이 등록되면 스프링은 자신을 직접 주입
- `빈 생애주기 메소드`를 통해 주입되는 오브젝트는 스프링 컨테이너가 스스로 빈으로 등록해서 빈으로 가져와 사용할 수도 있도록 지원
- 그밖에 스프링이 제공하는 생애주기 메소드
  ```text
  BeanNameAware's setBeanName,
  BeanClassLoaderAware's setBeanClassLoader,
  BeanFactoryAware's setBeanFactory,
  EnvironmentAware's setEnvironment,
  EmbeddedValueResolverAware's setEmbeddedValueResolver,
  ResourceLoaderAware's setResourceLoader (only applicable when running in an application context),
  ApplicationEventPublisherAware's setApplicationEventPublisher (only applicable when running in an application context),
  MessageSourceAware's setMessageSource (only applicable when running in an application context),
  ApplicationContextAware's setApplicationContext (only applicable when running in an application context),
  ServletContextAware's setServletContext (only applicable when running in a web application context),
  postProcessBeforeInitialization methods of BeanPostProcessors,
  InitializingBean's afterPropertiesSet,
  a custom init-method definition,
  postProcessAfterInitialization methods of BeanPostProcessors
  ```

## TEST

**TestRestTemplate**

- 웹 서버에 HTTP 요청을 보내고 응답을 받아서 검증하는 테스트에서는 `TestRestTemplate` 를 사용해 보자.
```java
@Test
void hello() {
    TestRestTemplate restTemplate = new TestRestTemplate();

    ResponseEntity<String> res =
            restTemplate.getForEntity("http://localhost:8080/hello?name={name}", String.class, "Spring");

    assertThat(res.getStatusCode()).isEqualTo(HttpStatus.OK);
    assertThat(res.getHeaders().getFirst(HttpHeaders.CONTENT_TYPE).startsWith(MediaType.TEXT_PLAIN_VALUE)).isTrue();
    assertThat(res.getBody().trim()).isEqualTo("Hello Spring");
}
```

**단위 테스트**

- 의존 오브젝트가 있는 경우, 테스트가 실행되는 동안에 수행될 최소한의 기능을 가진 의존 오브젝트 코드를 테스트용으로 만들어서 사용

```java
@Test
void helloController() {
    HelloController helloController = new HelloController(name -> name);
    String ret = helloController.hello("Test");
    Assertions.assertThat(ret).isEqualTo("Test");
}
```

**Decorator Pattern and Proxy Pattern**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/decorator-pattern.png?raw=true 'Result')

- Decorator Pattern
  - 기존 코드에 동적으로 책임을 추가할 때 사용하는 패턴
  - 오브젝트 합성 구조로 확장이 가능하도록 설계
  - DI를 적용해서 의존관계를 런타임에 주입할 수 있다면 의존 오브젝트와 동일한 인터페이스를 구현한 확장기능(데코레이터)을 동적으로 추가 가능
  - 재귀적인 구조로 여러 개의 책임을 부가하는 것도 가능

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/proxy-pattern.png?raw=true 'Result')

- Proxy Pattern
  - 프록시는 다른 오브젝트의 대리자 혹은 플레이스 홀더 역할
  - 프록시는 리모트 오브젝트에 대한 로컬 접근이 가능하게 하거나, 필요가 있을 때만 대상 오브젝트를 생성
  - 보안이나 접속 제어 등에 사용

## Auto Configuration

**Meta-annotation**

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component // Meta Annotation
public @interface Service {
}
```

- 애노테이션에 적용한 애노테이션
- 스프링은 메타 애노테이션의 효력을 적용

**Composed-annotation**

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Controller // Meta Annotation
@ResponseBody // Meta Annotation
public @interface RestController {
...
}
```

- 하나 이상의 메타 애노테이션이 적용된 애노테이션
- 모든 메타 애노테이션이 적용된 것과 동일한 효과

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/bean-object.png?raw=true 'Result')

**Application Logic Bean**
- 애플리케이션의 `비즈니스 로직`을 담고 있는 빈
- `컴포넌트 스캐너`에 의해서 빈 구성 정보가 생성되고 빈 오브젝트로 등록
- ex. HelloController, HelloDecorator ..

**Application Infrastructure Bean**
- 스프링 부트에서 `자동 구성 정보`에 의해 컨테이너에 등록되는 빈
- 애플리케이션이 동작하는데 꼭 필요한 기술 기반을 제공하는 빈
- ex. ServletWebServerFactory, DispatcherServlet..

**Container Infrastructure(Infra) Bean**
- 스프링 컨테이너의 기능을 확장해서 빈 등록과 생성, 관계설정, 초기화 등의 작업에 참여하는 빈
- 컨테이너가 직접 만들고 사용하는 빈이므로 애플리케이션 빈과 구분
- 필요한 경우 주입 받아서 활용 가능

**자동 구성 정보 동적 등록**

```java
public interface ImportSelector {
    String[] selectImports(AnnotationMetadata importingClassMetadata);
    ...
}

...

public class MyAutoConfigImportSelector implements DeferredImportSelector {
    @Override
    public String[] selectImports(AnnotationMetadata importingClassMetadata) {
        return new String[] {
                "tobyspring.config.autoconfig.DispatcherServletConfig",
                "tobyspring.config.autoconfig.TomcatWebServerConfig"
        };
    }
}
```

- `ImportSelector` 구현 클래스를 @Import 해주면 `selectImports` 가 리턴하는 클래스 이름으로 @Configuration 클래스를 찾아서 구성 정보로 사용
- @import 대상을 외부에서 코드로 가져오고 선택할 수 있는 동적인 방법 제공

**자동 구성 정보 파일 분리**

```java
@Override
public String[] selectImports(AnnotationMetadata importingClassMetadata) {
    ArrayList<Object> autoConfigs = new ArrayList<>();

    ImportCandidates.load(MyAutoConfiguration.class, classLoader).forEach(autoConfigs::add);

    return autoConfigs.toArray(new String[0]);
}
```

- @MyAutoConfiguration 애노테이션 생성
- `tobyspring.config.MyAutoConfiguration.imports` 파일을 `META-INF/spring` 폴더 아래 생성
- selectImports() 에서 파일에 작성된 클래스 정보를 가져와 컨테이너에 등록시킬 @Configuration 클래스 목록 저장

**@Configuration 동작 방식**

```java
@Configuration(proxyBeanMethods = false)
```

- `proxyBeanMethods = true` (default, 스프링 5.2 버전부터 지원)
  - true 일 경우, @Configuration 클래스는 CGLib 를 이용해서 프록시 클래스로 확장 후 @Bean 이 붙은 메소드의 동작 방식을 변경
  - @Bean 메소드를 직접 호출해서 다른 빈의 의존 관계를 설정할 때 여러번 호출되더라도 싱글톤 빈처럼 참조할 수 있도록 매번 같은 오브젝트를 리턴
    ```java
    /**
     * Spring 은 하나의 빈을 두 개 이상의 다른 빈에서 의존하고 있을 경우,
     * Factory Method 호출 시마다 새로운 빈이 생성되는 문제를 해결하기 위해
     * @Configuration class 는 기본적으로 proxy 를 만들어서 기능 확장
     * (proxyBeanMethods = true)
     */
    static class MyConfigProxy extends MyConfig {
        private Common common;

        @Override
        Common common() {
            if (this.common == null) {
                this.common = super.common();
            }

            return this.common;
        }
    }

    ...

    @Configuration
    static class MyConfig {
        @Bean
        Common common() {
            return new Common();
        }

        @Bean
        Bean1 bean1() {
            return new Bean1(common());
        }

        @Bean
        Bean2 bean2() {
            return new Bean2(common());
        }
    }
    ```
- 단, @Bean 메소드 직접 호출로 빈 의존관계 주입을 하지 않는다면 굳이 복잡한 프록시를 생성할 할 필요가 없음
  - 이 경우 `proxyBeanMethods = false` 로 지정해 보자.
  - @Bean 메소드는 평범한 팩토리 메소드처럼 동작

## 조건부 자동 구성

**Spring Boot AutoConfiguration**

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Configuration(proxyBeanMethods = false)
@AutoConfigureBefore
@AutoConfigureAfter
public @interface AutoConfiguration {
  ...
}
```

META-INF.spring.`org.springframework.boot.autoconfigure.AutoConfiguration.imports`
- 약 144 개의 autoConfiguration 이 Spring Boot 기본 등록

[Spring Boot application starters](https://docs.spring.io/spring-boot/docs/2.7.14/reference/html/using.html#using.build-systems.starters)

**@Conditional과 Condition**

```java
/**
 * 스프링 4.0에 추가된 애노테이션으로 모든 조건을 만족하는 경우에만 컨테이너에 빈으로 등록
 */
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Conditional {
    Class<? extends Condition>[] value();
}

...

/**
 *  @Conditional 에 지정되어서 구체적인 매칭 조건을 가진 클래스가 구현해야할 인터페이스
 */
@FunctionalInterface
public interface Condition {
    boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata);
}

...

/**
 * Condition interface 구현체
 */
static class BooleanCondition implements Condition {
    /**
     *  @Conditional 애노테이션의 엘리먼트 정보를 가져올 수 있는 AnnotatedTypeMetadata 전달
     */
    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        Map<String, Object> annotationAttributes = metadata.getAnnotationAttributes(BooleanConditional.class.getName());
        Boolean value = (Boolean) annotationAttributes.get("value");
        return value;
    }
}
```

- `@Conditional`은 @Configuration 클래스와 @Bean 메소드에 적용 가능
- 클래스 조건을 만족하지 못하는 경우 메소드는 무시
- [@Conditional Test](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/9beeb972cbfdc12bbaced3cdeb7daae404444b61)

**Costume @Conditional**
- `@Conditional` 의 가장 대표적인 방법은 클래스 존재 확인
- 어떤 기술의 클래스를 애플리케이션이 사용하도록 포함시켰다면, 이 기술을 사용할 의도가 있다는 것으로 보고 관련 자동 구성 클래스를 등록
- [Costume @Conditional](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/3fa7d3d3aac944089f2054916751c36bd0cab5f0)