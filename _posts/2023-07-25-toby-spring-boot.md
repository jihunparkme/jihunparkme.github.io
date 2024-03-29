---
layout: post
title: Toby Spring Boot
summary: AutoConfiguration
categories: Spring-Conquest
featured-img: toby-spring-boot
# mathjax: true
---

# Spring Boot

토비님의 [토비의 스프링 부트 - 이해와 원리](https://www.inflearn.com/course/%ED%86%A0%EB%B9%84-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8-%EC%9D%B4%ED%95%B4%EC%99%80%EC%9B%90%EB%A6%AC/dashboard) 강의 노트

[Github](https://github.com/tobyspringboot/helloboot)

[MY Project](https://github.com/jihunparkme/inflearn-toby-spring-boot)

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

**`API Test Method`**

- 웹 브라우저 개발자 도구 - Network
- curl
- [HTTPie](https://httpie.io/)
- Intellij IDEA Ultimate- http request
- [Postman API Platform](https://www.postman.com/)
- JUnit Test
- ...

.

**`HTTP Request and Response`**

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

**`Start Servlet Container`**

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

.

**`Register Servlet in ServletContext`**

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

.

**`Front Controller Pattern`**

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

.

**`Dependency Injection`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/assembler.png?raw=true 'Result')

- `DI`를 위해 N개의 오브젝트(인터페이스 구현체)가 동적으로 의존관계를 가지도록 도와주는 `어셈블러`가 필요
- `스프링 컨테이너`(어셈블러)는 DI를 가능하도록 도와주는 `어셈블러`로 동작
  - 의존관계가 없는 클래스들의 오브젝트로 서로 관계를 연결시켜주고 사용할 수 있도록 설정
- 스프링 컨데이너는 메타 정보를 가지고 클래스에 싱글톤 오브젝트를 생성
  - 생성된 오브젝트가 사용할 다른 의존 오브젝트가 있다면 의존성 주입
  - 의존성 주입 방법으로는 생성자 주입, 팩터리 메서드 등 존재

.

**`DispatcherServlet`**

- 스프링은 프론트 컨트롤러와 같은 역할을 담당하는 DispatcherServlet 을 가지고 있다.
- DispatcherServlet 은 서블릿으로 등록되어서 동작하면서, 스프링 컨테이너를 이용해서 요청을 전달할 핸들러인 컨트롤러 오브젝트를 가져와 사용
- DispatcherServlet 이 사용하는 스프링 컨테이너는 GenericWebApplicationContext 를 이용해서 작성

.

**`애노테이션 매핑 정보`**

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

.

**`스프링 컨테이너로 통합`**
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

.

**`@Component Scan`**

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

.

**`Bean의 생명주기 메소드`**

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

**`TestRestTemplate`**

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

.

**`단위 테스트`**

- 의존 오브젝트가 있는 경우, 테스트가 실행되는 동안에 수행될 최소한의 기능을 가진 의존 오브젝트 코드를 테스트용으로 만들어서 사용

```java
@Test
void helloController() {
    HelloController helloController = new HelloController(name -> name);
    String ret = helloController.hello("Test");
    Assertions.assertThat(ret).isEqualTo("Test");
}
```

.

**`Decorator Pattern and Proxy Pattern`**

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

**`Meta-annotation`**

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

**`Composed-annotation`**

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

.

**`자동 구성 정보 동적 등록`**

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

.

**`자동 구성 정보 파일 분리`**

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

.

**`@Configuration 동작 방식`**

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

**`Spring Boot AutoConfiguration`**

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

.

**`@Conditional과 Condition`**

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

.

**`Costume @Conditional`**
- `@Conditional` 의 가장 대표적인 방법은 클래스 존재 확인
- 어떤 기술의 클래스를 애플리케이션이 사용하도록 포함시켰다면, 이 기술을 사용할 의도가 있다는 것으로 보고 관련 자동 구성 클래스를 등록
- [Costume @Conditional](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/3fa7d3d3aac944089f2054916751c36bd0cab5f0)

.

**`자동 구성 정보 대체`**

- 자동 구성 정보는 다음의 과정으로 등록
  - imports 파일에서 자동 구성 정보 클래스 후보 로딩
  - @Conditional 조건 체크를 통해 선택된 클래스가 빈으로 등록

```java
/**
 * 자동 구성으로 등록되는 빈과 동일한 타입의 빈을 직접 정의(@Configuration/@Bean)하는 경우,
 * 직접 정의 빈 구성이 자동 구성을 대체
 */
@Configuration(proxyBeanMethods = false)
public class WebServerConfiguration {
    @Bean ServletWebServerFactory customerWebServerFactory() {
        TomcatServletWebServerFactory serverFactory = new TomcatServletWebServerFactory();
        serverFactory.setPort(9090);
        return serverFactory;
    }
}

...

/**
 * 자동 구성 클래스의 @Bean 메소드에 @ConditionalOnMissingBean 이 정의된 경우,
 * 유저 구성에 지정한 타입의 빈이 정의되어있으면 자동 구성 빈의 조건이 충족되지 않아 등록되지 않음.
 */
@Bean("tomcatWebServerFactory")
@ConditionalOnMissingBean
public ServletWebServerFactory servletWebServerFactory() {
    return new TomcatServletWebServerFactory();
}
```

[자동 구성 정보 대체하기](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/88040a3c503dfc9edeb11040eea56c83c94642a5)

.

**`Spring Boot @Conditional`**

스프링 부트의 자동 구성은 다양한 @Conditional 을 이용.

**Class Conditions**
- `@ConditionalOnClass`
- `@ConditionalOnMissingClass`
  ```text  
  • 프로젝트 내 지정한 클래스의 존재를 확인해서 포함 여부 결정
  • 주로 @Configuration 을 클래스 레벨에서 사용하지만, @Bean 메소드에도 적용 가능
  • (단, 클래스 레벨의 검증 없이 @Bean 메소드에만 적용하면 불필요한 @Configuration 클래스가 빈으로 등록되기 때문에 클래스 레벨 사용을 우선)
  ```

**Bean Conditions**
- `@ConditionalOnBean`
- `@ConditionalOnMissingBean`
  ```text
  • 빈의 존재 여부를 기준으로 포함 여부 결정
  • 빈의 타입 또는 이름을 지정할 수 있고, 지정된 빈 정보가 없으면 메소드의 리턴 타입을 기준으로 빈 존재 여부 체크
  • 컨테이너에 등록된 빈 정보를 기준으로 체크하기 때문에 자동 구성 사이에 적용하려면 @Configuration 클래스의 적용 순서가 중요
  • 개발자가 직접 정의한 커스텀 빈 구성 정보가 자동 구성 정보 처리보다 우선하기 때문에 이 관계에 적용하는 것은 안전하지만, 반대로 커스톰 빈 구성 정보에 적용하는 건 피하자.
  ```

> @Configuration 클래스 레벨의 `@ConditionalOnClass`
> 
> @Bean 메소드 레벨의 `@ConditionalOnMissingBean`
> 
> 조합은 가장 대표적으로 사용되는 방식
> 
> 클래스 존재로 해당 기술 사용 여부 확인 → 커스텀 빈 구성 존재를 확인해서 자동 구성의 빈 오브젝트를 이용할지 최종 결정

**Property Conditions**
- `@ConditionalOnProperty`
  ```text
  • 스프링의 환경 프로퍼티 정보를 이용
  • 지정된 프로퍼티가 존재하고 값이 false 가 아니면 포함 대상
  • 특정 값을 가진 경우를 확인하거나 프로퍼티가 존재하지 않을 때 조건을 만족하도록 설정 가능
  • 프로퍼티의 존재를 확인해서 빈 오브젝트를 추가하고, 해당 빈 오브젝트에서 프로퍼티 값을 이용해서 세밀하게 빈 구성 가능
  ```
**Resource Conditions**
- `@ConditionalOnResource`
  ```text
  • 지정된 리소스(파일) 존재 확인
  ```

**Web Application Conditions**
- `@ConditionalOnWebApplication`
- `@ConditionalOnNotWebApplication`
  ```text
  • 웹 애플리케이션 여부 확인
  • ex. 웹 기술을 사용하지 않는 배치
  ```

**SpEL Expression Conditions**
- `@ConditionalOnExpression`
  ```text
  • 스프링 SpEL(스프링 표현식) 처리 결과 기준으로 판단
  • 매우 상세한 조건 설정 가능
  ```

## 외부 설정을 이용한 자동 구성

**`스프링의 Environment 추상화`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/spring-environment-abstraction.png?raw=true 'Result')

```java
Environment.getProperty("property.name")
```

Environment 타입의 오브젝트를 가져와서 프로퍼티 이름을 제공하여 설정값 조회

- 프로퍼티 우선순위
  - ServletConfig Parameters
  - ServletContext Parameters
  - JNDI
  - System Properties
  - System Environment Variables
  - @PropertySource
  - xml, yml
- 제공되는 프로퍼티 이름을 변형해서 설정값 탐색
  - property.name
  - property_name
  - PROPERTY.NAME
  - PROPERTY_NAME

.

**`자동 구성에 Environment 프로퍼티 적용`**

```java
@Bean("tomcatWebServerFactory")
@ConditionalOnMissingBean
public ServletWebServerFactory servletWebServerFactory(Environment env) {
  TomcatServletWebServerFactory factory = new TomcatServletWebServerFactory();
  factory.setContextPath(env.getProperty("contextPath"));
  return factory;
}
```

- 자동 구성 클래스의 메소드에 `Environment` 를 주입 받아서 빈 속성으로 지정할 프로퍼티 값을 가져올 수 있음
- [commit](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/b15b94d95760907e6b82f5ac25664ea8dfa023a4)

.

**`@Value`**

- `@Value` 는 element 로 placeholder(치환자)를 지정하고 컨테이너 초기화시 프로퍼티 값으로 이를 대체
- 치환자를 프로퍼티 값으로 교체하려면 `PropertySourcesPlaceholderConfigurer` 타입의 빈 등록 필요
  - 팩토리의 후처리기로 동작해서 초기 구성 정보에서 치환자를 찾아서 교체하는 기능 담당
- [commit](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/eba19682f56e0bef2c65277ee5f2642b30039592)


```java
@MyAutoConfiguration
public class PropertyPlaceholderConfig {
    @Bean
    PropertySourcesPlaceholderConfigurer propertySourcesPlaceholderConfigurer() {
        return new PropertySourcesPlaceholderConfigurer();
    }
}
```

.

**`프로퍼티 클래스의 분리`**
- [commit](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/7afaa43a4863deddeff0b8864a5df455f61154ad)
- [commit - using Spring Binder](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/6025ef6c61ddc1034fdf58d119f7ab1760172669)

.

**`프로퍼티 빈의 후처리기 도입`**
- [commit](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/042ece85949d5e1cecdc6a30458ba9482b73fee2)

## Spring JDBC 자동 구성 구현

**`자동 구성 클래스와 빈 설계`**
- 새로운 기술의 자동 구성 클래스를 작성할 경우 자동 구성 클래스에 적용할 조건과 만들어지는 빈 오브젝트 종류 등을 먼저 설계

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/dataSourceConfig.png?raw=true 'Result')

- 두 개의 DataSource 구현 클래스를 조건에 따라 등록
  - DataSourceProperties 프로퍼티 클래스 이용

.

**`DataSource 자동 구성 클래스`**

- @TestPropertySource
  - application.properties 파일 등록은 스프링 프레임워크 기본 동작 방식이 아님
  - 스프링 부트 초기화 과정에서 추가해 주는 것이므로 테스트에서 별도 추가 필요
  - @TestPropertySource("classpath:/application.properties") 로 properties 정보를 읽어오도록 설정
- [DataSource 자동 구성 클래스 - commit](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/f50531f4dafd31b42f04a7988f44713b561fbf2e)

.

**`JdbcTemplate과 트랜잭션 매니저 구성`**
- @ConditionalOnSingleCandidate
  - 빈 구성정보에 해당 타입 빈이 한 개만 등록되어있는 경우 조건 매칭
- @EnableTransactionManagement
  - 애노테이션을 이용하는 트랜잭션 기능을 이용
- [JdbcTemplate과 트랜잭션 매니저 구성](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/e34e9f3fd785e57405188587eb1238caa8acab6a)

.

**`Hello Repository`**
- [Hello Repository](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/f0deca3857f524f94b69d91d63886e1dc4473b6e)
- [리포지토리를 사용하는 HelloService](https://github.com/jihunparkme/inflearn-toby-spring-boot/commit/68d55e7edecc820108af6f9810859ccf99cc25e9)

> 인터페이스에 default, static 메소드를 넣어서 활용하는 방법은 
> 
> 자바의 Comparator`<T`> 인터페이스를 참고해 보자.

## Spring Boot

**`스프링 부트의 자동 구성과 테스트`**

-  `@SpringBootApplication`
   -  Spring Boot Main Annotation
- `@JdbcTest`
  - Spring Boot Test 준비
  - 자동구성 중 JDBC 를 이용하기 위해 필요한 빈들만 로딩 ➔ 빠른 테스트
  - embedded db 로 dataSource 교체 ➔ 프로퍼티로 설정한 DB 접속 정보 사용 X
- `@SpringBootTest`
  - 스프링 컨테이너를 띄우고 자동 구성까지 적용해서 테스트
  - 서블릿 컨테이너 환경 여부 설정
    - 웹 환경 세팅 제외: webEnvironment = SpringBootTest.WebEnvironment.NONE
    - 웹 환경 세팅: webEnvironment = SpringBootTest.WebEnvironment.DEFINED_PORT

.

**`스프링 부트 자세히 살펴보기`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/into-spring-boot.png?raw=true 'Result')

- 스프링 부트의 `동작 방식 이해`
- `사용 기술`과 관련된 `자동 구성 빈`과 `구성`, `속성`, `프로퍼티 설정` 등을 분석
  - 자동 구성 빈과 조건에 따라 달라지는 빈 선택 기준
- 이를 어떻게 활용할 수 있는지 파악

.

**`자동 구성 분석 방법`**

자동 구성 후보 목록과 조건 판단 결과 조회하기

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/spring-boot-research.png?raw=true 'Result')

- `-Ddebug` or `--debug` 인자를 이용해서 스프링 부트 애플리케이션 실행
- `ConditionEvaluationReport` 타입의 빈을 주입 받고, 필요한 정보만 선택해서 자동 구성 결과 확인
- `ListableBeanFactory` 타입의 빈을 주입 받고, 빈 이름을 가져와서(필요 시 빈 오브젝트도) 등록된 빈 목록 확인
- 자동 구성 선정 결과를 기준으로 `스프링 부트 레퍼런스 문서`, `자동 구성 클래스 소스 코드`, `프로퍼티 클래스`, `Customizer` 등을 살펴보며 어떻게 어떤 조건으로 동작할지 분석

VM options: `-Ddebug`

```console
Positive matches:
-----------------

   AopAutoConfiguration matched:
      - @ConditionalOnProperty (spring.aop.auto=true) matched (OnPropertyCondition)

   AopAutoConfiguration.ClassProxyingConfiguration matched:
      - @ConditionalOnMissingClass did not find unwanted class 'org.aspectj.weaver.Advice' (OnClassCondition)
      - @ConditionalOnProperty (spring.aop.proxy-target-class=true) matched (OnPropertyCondition)

   ApplicationAvailabilityAutoConfiguration#applicationAvailability matched:
      - @ConditionalOnMissingBean (types: org.springframework.boot.availability.ApplicationAvailability; SearchStrategy: all) did not find any beans (OnBeanCondition)

...

Negative matches:
-----------------

   ActiveMQAutoConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required class 'javax.jms.ConnectionFactory' (OnClassCondition)

   AopAutoConfiguration.AspectJAutoProxyingConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required class 'org.aspectj.weaver.Advice' (OnClassCondition)

   ArtemisAutoConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required class 'javax.jms.ConnectionFactory' (OnClassCondition)

...
```

`ConditionEvaluationReport`
- 조건이 매칭된 자동 구성 클래스와 메소드를 출력

```java
@Bean
ApplicationRunner run(ConditionEvaluationReport report) {
    return args -> {
        long result = report.getConditionAndOutcomesBySource().entrySet().stream()
                .filter(co -> co.getValue().isFullMatch()) // 컨디션 조건을 모두 통과한 빈 목록
                .filter(co -> co.getKey().indexOf("Jmx") < 0) // Jmx 관련 구성 정보 제외
                .map(co -> {
                    System.out.println(co.getKey());
                    co.getValue().forEach(c -> {
                        System.out.println("\t" + c.getOutcome()); // 컨디셔널 통과 조건
                    });
                    System.out.println();
                    return co;
                }).count();

        System.out.println(result);
    };
}
```

`org.springframework.boot:spring-boot-starter` (springboot core)

- spring boot code 에서 Jmx 제외 빈이 목록

  <details>
  <summary>등록된 빈 목록 보기</summary>

  org.springframework.boot.autoconfigure.aop.AopAutoConfiguration
    @ConditionalOnProperty (spring.aop.auto=true) matched

  ,

  org.springframework.boot.autoconfigure.aop.AopAutoConfiguration$ClassProxyingConfiguration
    @ConditionalOnMissingClass did not find unwanted class 'org.aspectj.weaver.Advice'
    @ConditionalOnProperty (spring.aop.proxy-target-class=true) matched

  ,

  org.springframework.boot.autoconfigure.availability.ApplicationAvailabilityAutoConfiguration#applicationAvailability
    @ConditionalOnMissingBean (types: org.springframework.boot.availability.ApplicationAvailability; SearchStrategy: all) did not find any beans

  ,

  org.springframework.boot.autoconfigure.cache.GenericCacheConfiguration
    Cache org.springframework.boot.autoconfigure.cache.GenericCacheConfiguration automatic cache type
  ,

  org.springframework.boot.autoconfigure.cache.NoOpCacheConfiguration
    Cache org.springframework.boot.autoconfigure.cache.NoOpCacheConfiguration automatic cache type

  ,

  org.springframework.boot.autoconfigure.cache.SimpleCacheConfiguration
    Cache org.springframework.boot.autoconfigure.cache.SimpleCacheConfiguration automatic cache type

  ,

  org.springframework.boot.autoconfigure.context.LifecycleAutoConfiguration#defaultLifecycleProcessor
    @ConditionalOnMissingBean (names: lifecycleProcessor; SearchStrategy: current) did not find any beans

  ,

  org.springframework.boot.autoconfigure.context.PropertyPlaceholderAutoConfiguration#propertySourcesPlaceholderConfigurer
    @ConditionalOnMissingBean (types: org.springframework.context.support.PropertySourcesPlaceholderConfigurer; SearchStrategy: current) did not find any beans

  ,

  org.springframework.boot.autoconfigure.sql.init.SqlInitializationAutoConfiguration
    @ConditionalOnProperty (spring.sql.init.enabled) matched
    NoneNestedConditions 0 matched 1 did not; NestedCondition on SqlInitializationAutoConfiguration.SqlInitializationModeCondition.ModeIsNever @ConditionalOnProperty (spring.sql.init.mode=never) did not find property 'mode'

  ,

  org.springframework.boot.autoconfigure.task.TaskExecutionAutoConfiguration
    @ConditionalOnClass found required class 'org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor'

  ,

  org.springframework.boot.autoconfigure.task.TaskExecutionAutoConfiguration#applicationTaskExecutor
    @ConditionalOnMissingBean (types: java.util.concurrent.Executor; SearchStrategy: all) did not find any beans

  ,

  org.springframework.boot.autoconfigure.task.TaskExecutionAutoConfiguration#taskExecutorBuilder
    @ConditionalOnMissingBean (types: org.springframework.boot.task.TaskExecutorBuilder; SearchStrategy: all) did not find any beans

  ,

  org.springframework.boot.autoconfigure.task.TaskSchedulingAutoConfiguration
    @ConditionalOnClass found required class 'org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler'

  ,

  org.springframework.boot.autoconfigure.task.TaskSchedulingAutoConfiguration#taskSchedulerBuilder
    @ConditionalOnMissingBean (types: org.springframework.boot.task.TaskSchedulerBuilder; SearchStrategy: all) did not find any beans
  </details>

.

`org.springframework.boot:spring-boot-starter-web`

- spring boot web 에서 Jmx 제외 빈 목록

  <details>
    <summary>등록된 빈 목록 보기</summary>
    ...
    
    org.springframework.boot.autoconfigure.web.client.RestTemplateAutoConfiguration
      @ConditionalOnClass found required class 'org.springframework.web.client.RestTemplate'
      NoneNestedConditions 0 matched 1 did not; NestedCondition on RestTemplateAutoConfiguration.NotReactiveWebApplicationCondition.ReactiveWebApplication did not find reactive web application classes

    ,

    org.springframework.boot.autoconfigure.web.client.RestTemplateAutoConfiguration#restTemplateBuilder
      @ConditionalOnMissingBean (types: org.springframework.boot.web.client.RestTemplateBuilder; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.client.RestTemplateAutoConfiguration#restTemplateBuilderConfigurer
      @ConditionalOnMissingBean (types: org.springframework.boot.autoconfigure.web.client.RestTemplateBuilderConfigurer; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.embedded.EmbeddedWebServerFactoryCustomizerAutoConfiguration
      @ConditionalOnWebApplication (required) found 'session' scope
      @ConditionalOnWarDeployment the application is not deployed as a WAR file.

    ,

    org.springframework.boot.autoconfigure.web.embedded.EmbeddedWebServerFactoryCustomizerAutoConfiguration$TomcatWebServerFactoryCustomizerConfiguration
      @ConditionalOnClass found required classes 'org.apache.catalina.startup.Tomcat', 'org.apache.coyote.UpgradeProtocol'

    ,

    org.springframework.boot.autoconfigure.web.servlet.DispatcherServletAutoConfiguration
      @ConditionalOnClass found required class 'org.springframework.web.servlet.DispatcherServlet'
      found 'session' scope

    ,

    org.springframework.boot.autoconfigure.web.servlet.DispatcherServletAutoConfiguration$DispatcherServletConfiguration
      @ConditionalOnClass found required class 'javax.servlet.ServletRegistration'
      Default DispatcherServlet did not find dispatcher servlet beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.DispatcherServletAutoConfiguration$DispatcherServletRegistrationConfiguration
      @ConditionalOnClass found required class 'javax.servlet.ServletRegistration'
      DispatcherServlet Registration did not find servlet registration bean

    ,

    org.springframework.boot.autoconfigure.web.servlet.DispatcherServletAutoConfiguration$DispatcherServletRegistrationConfiguration#dispatcherServletRegistration
      @ConditionalOnBean (names: dispatcherServlet types: org.springframework.web.servlet.DispatcherServlet; SearchStrategy: all) found bean 'dispatcherServlet'

    ,

    org.springframework.boot.autoconfigure.web.servlet.HttpEncodingAutoConfiguration
      @ConditionalOnClass found required class 'org.springframework.web.filter.CharacterEncodingFilter'
      found 'session' scope
      @ConditionalOnProperty (server.servlet.encoding.enabled) matched

    ,

    org.springframework.boot.autoconfigure.web.servlet.HttpEncodingAutoConfiguration#characterEncodingFilter
      @ConditionalOnMissingBean (types: org.springframework.web.filter.CharacterEncodingFilter; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.MultipartAutoConfiguration
      @ConditionalOnClass found required classes 'javax.servlet.Servlet', 'org.springframework.web.multipart.support.StandardServletMultipartResolver', 'javax.servlet.MultipartConfigElement'
      found 'session' scope
      @ConditionalOnProperty (spring.servlet.multipart.enabled) matched

    ,

    org.springframework.boot.autoconfigure.web.servlet.MultipartAutoConfiguration#multipartConfigElement
      @ConditionalOnMissingBean (types: javax.servlet.MultipartConfigElement,org.springframework.web.multipart.commons.CommonsMultipartResolver; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.MultipartAutoConfiguration#multipartResolver
      @ConditionalOnMissingBean (types: org.springframework.web.multipart.MultipartResolver; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.ServletWebServerFactoryAutoConfiguration
      @ConditionalOnClass found required class 'javax.servlet.ServletRequest'
      found 'session' scope

    ,

    org.springframework.boot.autoconfigure.web.servlet.ServletWebServerFactoryAutoConfiguration#tomcatServletWebServerFactoryCustomizer
      @ConditionalOnClass found required class 'org.apache.catalina.startup.Tomcat'

    ,

    org.springframework.boot.autoconfigure.web.servlet.ServletWebServerFactoryConfiguration$EmbeddedTomcat
      @ConditionalOnClass found required classes 'javax.servlet.Servlet', 'org.apache.catalina.startup.Tomcat', 'org.apache.coyote.UpgradeProtocol'
      @ConditionalOnMissingBean (types: org.springframework.boot.web.servlet.server.ServletWebServerFactory; SearchStrategy: current) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration
      @ConditionalOnClass found required classes 'javax.servlet.Servlet', 'org.springframework.web.servlet.DispatcherServlet', 'org.springframework.web.servlet.config.annotation.WebMvcConfigurer'
      found 'session' scope
      @ConditionalOnMissingBean (types: org.springframework.web.servlet.config.annotation.WebMvcConfigurationSupport; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration#formContentFilter
      @ConditionalOnProperty (spring.mvc.formcontent.filter.enabled) matched
      @ConditionalOnMissingBean (types: org.springframework.web.filter.FormContentFilter; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration$EnableWebMvcConfiguration#flashMapManager
      @ConditionalOnMissingBean (names: flashMapManager; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration$EnableWebMvcConfiguration#localeResolver
      @ConditionalOnMissingBean (names: localeResolver; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration$EnableWebMvcConfiguration#themeResolver
      @ConditionalOnMissingBean (names: themeResolver; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration$WebMvcAutoConfigurationAdapter#defaultViewResolver
      @ConditionalOnMissingBean (types: org.springframework.web.servlet.view.InternalResourceViewResolver; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration$WebMvcAutoConfigurationAdapter#requestContextFilter
      @ConditionalOnMissingBean (types: org.springframework.web.context.request.RequestContextListener,org.springframework.web.filter.RequestContextFilter; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration$WebMvcAutoConfigurationAdapter#viewResolver
      @ConditionalOnBean (types: org.springframework.web.servlet.ViewResolver; SearchStrategy: all) found beans 'defaultViewResolver', 'beanNameViewResolver', 'mvcViewResolver'; @ConditionalOnMissingBean (names: viewResolver types: org.springframework.web.servlet.view.ContentNegotiatingViewResolver; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.error.ErrorMvcAutoConfiguration
      @ConditionalOnClass found required classes 'javax.servlet.Servlet', 'org.springframework.web.servlet.DispatcherServlet'
      found 'session' scope

    ,

    org.springframework.boot.autoconfigure.web.servlet.error.ErrorMvcAutoConfiguration#basicErrorController
      @ConditionalOnMissingBean (types: org.springframework.boot.web.servlet.error.ErrorController; SearchStrategy: current) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.error.ErrorMvcAutoConfiguration#errorAttributes
      @ConditionalOnMissingBean (types: org.springframework.boot.web.servlet.error.ErrorAttributes; SearchStrategy: current) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.error.ErrorMvcAutoConfiguration$DefaultErrorViewResolverConfiguration#conventionErrorViewResolver
      @ConditionalOnBean (types: org.springframework.web.servlet.DispatcherServlet; SearchStrategy: all) found bean 'dispatcherServlet'; @ConditionalOnMissingBean (types: org.springframework.boot.autoconfigure.web.servlet.error.ErrorViewResolver; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.error.ErrorMvcAutoConfiguration$WhitelabelErrorViewConfiguration
      @ConditionalOnProperty (server.error.whitelabel.enabled) matched
      ErrorTemplate Missing did not find error template view

    ,

    org.springframework.boot.autoconfigure.web.servlet.error.ErrorMvcAutoConfiguration$WhitelabelErrorViewConfiguration#beanNameViewResolver
      @ConditionalOnMissingBean (types: org.springframework.web.servlet.view.BeanNameViewResolver; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.web.servlet.error.ErrorMvcAutoConfiguration$WhitelabelErrorViewConfiguration#defaultErrorView
      @ConditionalOnMissingBean (names: error; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.websocket.servlet.WebSocketServletAutoConfiguration
      @ConditionalOnClass found required classes 'javax.servlet.Servlet', 'javax.websocket.server.ServerContainer'
      found 'session' scope

    ,

    org.springframework.boot.autoconfigure.websocket.servlet.WebSocketServletAutoConfiguration$TomcatWebSocketConfiguration
      @ConditionalOnClass found required classes 'org.apache.catalina.startup.Tomcat', 'org.apache.tomcat.websocket.server.WsSci'

    ,

    org.springframework.boot.autoconfigure.websocket.servlet.WebSocketServletAutoConfiguration$TomcatWebSocketConfiguration#websocketServletWebServerCustomizer
      @ConditionalOnMissingBean (names: websocketServletWebServerCustomizer; SearchStrategy: all) did not find any beans
  </details>

`org.springframework.boot:spring-boot-starter-jdbc`

- jdbc 관련 빈 목록

  <details>
    <summary>등록된 빈 목록 보기</summary>
    ...

    org.springframework.boot.autoconfigure.transaction.TransactionAutoConfiguration
      @ConditionalOnClass found required class 'org.springframework.transaction.PlatformTransactionManager'

    ,

    org.springframework.boot.autoconfigure.transaction.TransactionAutoConfiguration#platformTransactionManagerCustomizers
      @ConditionalOnMissingBean (types: org.springframework.boot.autoconfigure.transaction.TransactionManagerCustomizers; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.transaction.TransactionAutoConfiguration$EnableTransactionManagementConfiguration
      @ConditionalOnBean (types: org.springframework.transaction.TransactionManager; SearchStrategy: all) found bean 'transactionManager'; @ConditionalOnMissingBean (types: org.springframework.transaction.annotation.AbstractTransactionManagementConfiguration; SearchStrategy: all) did not find any beans

    ,

    org.springframework.boot.autoconfigure.transaction.TransactionAutoConfiguration$EnableTransactionManagementConfiguration$CglibAutoProxyConfiguration
      @ConditionalOnProperty (spring.aop.proxy-target-class=true) matched

    ,

    org.springframework.boot.autoconfigure.transaction.TransactionAutoConfiguration$TransactionTemplateConfiguration
      @ConditionalOnSingleCandidate (types: org.springframework.transaction.PlatformTransactionManager; SearchStrategy: all) found a single bean 'transactionManager'

    ,

    org.springframework.boot.autoconfigure.transaction.TransactionAutoConfiguration$TransactionTemplateConfiguration#transactionTemplate
      @ConditionalOnMissingBean (types: org.springframework.transaction.support.TransactionOperations; SearchStrategy: all) did not find any beans
  </details>