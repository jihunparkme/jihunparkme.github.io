---
layout: post
title: Spring Boot
summary: Spring Boot 핵심 원리와 활용
categories: Spring-Boot
featured-img: spring
# mathjax: true
---

# Spring Boot

스프링 프레임워크를 쉽게 사용할 수 있게 도와주는 도구

**핵심 기능**

- `WAS`: Tomcat 같은 웹 서버를 내장해서 별도의 웹 서버 설치 불필요
- `라이브러리 관리` : 손쉬운 빌드 구성을 위한 스타터 종속성 제공 및 라이브러리 버전 관리
- `자동 구성`: 프로젝트 시작에 필요한 스프링과 외부 라이브러리의 빈을 자동 등록
- `외부 설정`: 환경에 따라 달라져야 하는 외부 설정 공통화
- `프로덕션 준비`: 모니터링을 위한 메트릭, 상태 확인 기능 제공

## 웹 서버와 서블릿 컨테이너

**방식의 변화**

전통 방식

- 자바 웹 애플리케이션 개발 시 서버에 톰캣 같은 WAS(웹 애플리케이션 서버) 설치가 필요
- WAS에서 동작하도록 서블릿 스펙에 맞추어 코드를 작성하고 WAR 형식으로 빌드해서 .war 파일을 생성
- 생성된 .war 파일을 WAS에 전달해서 배포하는 방식으로 전체 개발 주기가 동작
- 과거 방식은 WAS 기반 위에서 개발하고 실행이 필요하고, IDE 같은 개발 환경에서도 WAS와 연동해서 실행되도록 복잡한 추가 설정이 필요

최근 방식

- 최근에는 스프링 부트가 내장 톰캣을 포함(애플리케이션 코드 안에 WAS가 라이브러리로 내장)
- 개발자는 코드를 작성하고 JAR로 빌드한 다음에 해당 JAR를 원하는 위치에서 실행하기만 하면 WAS도 함께 실행
- IDE 개발 환경에서 WAS 설치와 연동하는 복잡한 일은 불필요

**JAR & WAR**

JAR (Java Archive)

`java -jar abc.jar`

- 자바는 여러 클래스와 관련 리소스를 압축한 .jar 라는 압출 파일이 존재
- JAR 파일은 JVM 위에서 직접 실행되거나 다른 곳에서 사용하는 라이브러리로 제공
- 직접 실행할 경우 main() 메서드가 필요하고, MANIFEST.MF 파일에 실행할 메인 메서드가 있는 클래스 지정 필요

WAR (Web Application Archive)

- .war 파일은 웹 애플리케이션 서버(WAS)에 배포할 때 사용하는 파일
- JAR 파일이 JVM 위에서 실행된다면, WAR는 웹 애플리케이션 서버 위에서 실행
- 웹 애플리케이션 서버 위에서 실행되고, HTML 같은 정적 리소스와 클래스 파일을 모두 함께 포함하기 때문에 JAR 대비 구조가 복잡하고 WAR 구조를 지켜야 함

**서블릿 컨테이너 초기화**

- 서블릿은 초기화 인터페이스(ServletContainerInitializer)를 제공
  - 서블릿 컨테이너를 초기화 하는 기능 제공
  - 서블릿 컨테이너는 실행 시점에 초기화 메서드인 onStartup() 을 호출
  - 여기서 애플리케이션에 필요한 기능들을 초기화 하거나 등록

```java
public interface ServletContainerInitializer {

    /**
     * Set<Class<?>> c
     * - 더 유연한 초기화 기능 제공
     * - @HandlesTypes 애노테이션과 함께 사용
     * 
     * ServletContext ctx
     * - 서블릿 컨테이너 자체 기능 제공
     * - 이 객체를 통해 필터나 서블릿 등록 가능
     */
    public void onStartup(Set<Class<?>> c, ServletContext ctx) throws
ServletException;
}
```

[서블릿 컨테이너 초기화를 위한 설정 example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/ac5cd44f85a8a2751ee73d641bf97b33943ffcf4)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/servlet-container.png?raw=true 'Result')


초기화 순서

- 서블릿 컨테이너 초기화 실행
  - ServletContainerInitializer 를 구현하고, `resources/META-INF/services/jakarta.servlet.ServletContainerInitializer` 파일에 등록된 컨테이너를 실행
- 애플리케이션 초기화 실행
  - 컨터이너를 실행하면서 `@HandlesTypes(AppInit.class)` 가 선언되어 있을 경우 AppInit 구현체를 모두 찾아서 생성 및 실행

애플리케이션 초기화 개념 생성 이유

- 서블릿 컨테이너는 초기화를 위해 ServletContainerInitializer 인터페이스 구현과 META-INF/services/
jakarta.servlet.ServletContainerInitializer 파일에 해당 클래스를 직접 지정해야 하지만, 애플리케이션 초기화는 특정 인터페이스만 구현하면 되는 편리함
- 애플리케이션 초기화는 서블릿 컨테이너에 상관없이 원하는 모양으로 인터페이스 생성이 가능하여 애플리케이션 초기화 코드가 서블릿 컨테이너에 대한 의존을 줄일 수 있음

[서블릿 컨테이너 / 애플리케이션 초기화 example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/a64d0c2224db274f839d175ce626add47288c2f3)

**스프링 컨테이너 등록**

- 스프링 컨테이너 만들기
- 스프링MVC 컨트롤러를 스프링 컨테이너에 빈으로 등록하기
- 스프링MVC를 사용하는데 필요한 디스패처 서블릿을 서블릿 컨테이너 등록하기

[스프링 컨테이너 등록 example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/309038cec60f458c80ab06bd86f650b80c3bc515)

**스프링 MVC 서블릿 컨테이너 초기화 지원**

번거롭고 반복적인 서블릿 컨테이너 초기화 과정을 스프링 MVC이 지원

- 개발자는 서블릿 컨테이너 초기화 과정은 생략하고, 애플리케이션 초기화 코드만 작성
- `WebApplicationInitializer` 인터페이스만 구현
 - spring-web 라이브러리를 보면, 아래 파일들을 이미 등록해둔 것을 확인
 - META-INF/services/jakarta.servlet.ServletContainerInitializer
 - org.springframework.web.SpringServletContainerInitializer

```java
package org.springframework.web;

public interface WebApplicationInitializer {
  void onStartup(ServletContext servletContext) throws ServletException;
}
```

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/WebApplicationInitializer.png?raw=true 'Result')

[스프링 MVC 서블릿 컨테이너 초기화 지원(WebApplicationInitializer 구현) example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/75febc7e060a0f49b77090352ebf7e8732667ee5)

## 스프링 부트와 내장 톰캣

**Tomcat Library**

```gradle
implementation 'org.apache.tomcat.embed:tomcat-embed-core:10.1.5'
```

**WAR 배포 방식의 단점**

- WAS(ex. tomcat) 별도 설치 필요
- 개발 환경 설정 복잡
- 배포 과정 복잡
- 버전 변경 시 WAS 재설치 필요

**내장 톰캣: 서블릿**

- 내장 톰캣을 사용하면 톰캣 서버 설치, IDE에 별도의 복잡한 톰캣 설정 없이 main() 메서드만 실행하면 톰캣까지 매우 편리하게 실행

[스프링 부트와 내장 톰캣: 서블릿 example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/2de424bdf8f28456f739d918bca616b38fddc978)

**내장 톰캣: 스프링**

- 내장 톰캣에 스프링 연동

[스프링 부트와 내장 톰캣: 스프링 컨테이너 연결 example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/31c8afb99b0a6ca1e0cd791695ba0c73fa48dc80)

**내장 톰캣: 빌드와 배포**

- 라이브러리로 포함된 내장 톰캣을 빌드 배포하기
- main() 메서드를 실행하기 위해서 jar 형식으로 빌드
- jar 안에는 `META-INF/MANIFEST.MF` 파일에 실행할 main() 메서드의 클래스를 지정
  ```groovy
  Manifest-Version: 1.0
  Main-Class: hello.embed.EmbedTomcatSpringMain
  ```
- `build.gradle` 적용 시
  - Jar 안에는 Jar를 포함할 수 없으므로, 라이브러리(jar)에서 제공되는 클래스들이 포함된 `fat jar` 또는 `uber jar` 를 활용
  ```groovy
  task buildFatJar(type: Jar) {
      manifest {
          attributes 'Main-Class': 'hello.embed.EmbedTomcatSpringMain'
      }
       // 파일명 중복 시 경고
      duplicatesStrategy = DuplicatesStrategy.WARN
      // 라이브러리들을 돌리면서 class 파일들을 뽑아내고, 빌드 시 포함
      from { configurations.runtimeClasspath.collect { it.isDirectory() ? it : zipTree(it) } }
      with jar
  }
  ```

  - 빌드: `./gradlew clean buildFatJar`
  - 실행: `java -jar embed-0.0.1-SNAPSHOT.jar`


**부트 클래스 만들어 보기**

[스프링 부트와 내장 톰캣: 편리한 부트 클래스 만들기 example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/b46935f67de40ee8a6a51f241e9daa51066c2a5e)

## 스프링 부트와 웹 서버

**실행 과정**

```java
@SpringBootApplication
public class BootApplication {

	public static void main(String[] args) {
		SpringApplication.run(BootApplication.class, args);
	}
}
```

- 스프링 부트 실행은 Java main() 메서드에서 SpringApplication.run() 호출
- 파라미터로 메인 설정 정보를 넘겨주는데, 보통 @SpringBootApplication 애노테이션이 있는 현재 클래스를 지정
- @SpringBootApplication 애노테이션 안에는 @ComponentScan을 포함한 여러 기능이 설정
  - 기본 설정은 현재 패키지와 그 하위 패키지 모두를 컴포넌트 스캔

`SpringApplication.run(BootApplication.class, args);` 코드 한 줄에서
- `스프링 컨테이너 생성` (new AnnotationConfigServletWebServerApplicationContext())
- `WAS(내장 톰캣) 생성` (Tomcat tomcat = new Tomcat())

### 실행 가능 Jar(Executable Jar)

Fat Jar의 문제점(라이브러리 확인 어려움, 파일명 중복 해결 어려움)을 해결하기 위해 jar 내부에 jar를 포함하여 실행할 수 있는 스프링 부트에서 새롭게 정의한 특별한 구조의 jar

```text
boot-0.0.1-SNAPSHOT.jar
  META-INF
    MANIFEST.MF
  org/springframework/boot/loader
    JarLauncher.class : 스프링 부트 main() 실행 클래스
  BOOT-INF
    classes : 개발한 class 파일과 리소스 파일
      hello/boot/BootApplication.class
      hello/boot/controller/HelloController.class
      …
    lib : 외부 라이브러리
        spring-webmvc-6.0.4.jar
        tomcat-embed-core-10.1.5.jar
        ...
    classpath.idx : 외부 라이브러리 모음
    layers.idx : 스프링 부트 구조 정보
```

**Jar 실행 정보**

- `java -jar xxx.jar` 를 실행하게 되면 `META-INF/MANIFEST.MF` 파일을 찾고, 여기에 있는 Main-Class 를 읽어서 main() 메서드를 실행

```yml
Manifest-Version: 1.0
Main-Class: org.springframework.boot.loader.JarLauncher
Start-Class: hello.boot.BootApplication
Spring-Boot-Version: 3.0.2
Spring-Boot-Classes: BOOT-INF/classes/
Spring-Boot-Lib: BOOT-INF/lib/
Spring-Boot-Classpath-Index: BOOT-INF/classpath.idx
Spring-Boot-Layers-Index: BOOT-INF/layers.idx
Build-Jdk-Spec: 17
```

- Main-Class
  - JarLauncher(org/springframework/boot/loader/JarLauncher)는 스프링 부트가 빌드 시 삽입
  - JarLauncher: 내부 jar(classes, lib)와 특별한 구조의 클래스 정보를 읽어들이는 기능
  - 이후 Start-Class 에 지정된 main() 호출
- Start-Class
  - main() 이 있는 hello.boot.BootApplication
- Spring-Boot-Version : 스프링 부트 버전
- Spring-Boot-Classes : 개발한 클래스 경로
- Spring-Boot-Lib : 라이브러리 경로
- Spring-Boot-Classpath-Index : 외부 라이브러리 모음
- Spring-Boot-Layers-Index : 스프링 부트 구조 정보

**스프링 부트 로더**

- org/springframework/boot/loader 하위에 있는 클래스
- JarLauncher 를 포함한 스프링 부트가 제공하는 실행 가능 Jar를 실제로 구동시키는 클래스들이 포함
- 스프링 부트는 빌드 시 이 클래스들을 포함

**실행 과정**

1.java -jar xxx.jar

2.MANIFEST.MF 인식

3.JarLauncher.main() 실행

- BOOT-INF/classes/ 인식
- BOOT-INF/lib/ 인식

4.BootApplication.main() 실행

## 스프링 부트 라이브러리 버전 관리

- 스프링 부트는 수 많은 라이브러리 버전을 직접 관리
- 라이브러리 버전을 생략해도 스프링 부트가 부트 버전에 맞춘 최적화된 라이브러리 버전을 선택
- 잘 알려지지 않거나 대중적이지 않아서 스프링 부트가 관리하지 않는 외부 라이브러리는 버전을 직접 명시
- 버전 관리 기능을 사용하려면 io.spring.dependency-management 플러그인 사용 필요
  - spring-boot-dependencies [BOM(Bill of materials) 정보](https://github.com/spring-projects/spring-boot/blob/main/spring-boot-project/spring-boot-dependencies/build.gradle)를 참고해서 버전 관리
  - [Managed Dependency Coordinates](https://docs.spring.io/spring-boot/docs/current/reference/html/dependency-versions.html#appendix.dependency-versions.coordinates)

```groovy
plugins {
  id 'org.springframework.boot' version '3.0.2'
  id 'io.spring.dependency-management' version '1.1.0' 
  id 'java'
}

...

dependencies {
 //스프링 웹, MVC
 implementation 'org.springframework:spring-webmvc'
 //내장 톰캣
 implementation 'org.apache.tomcat.embed:tomcat-embed-core'
 //JSON 처리
 implementation 'com.fasterxml.jackson.core:jackson-databind'
 //스프링 부트 관련
 implementation 'org.springframework.boot:spring-boot'
 implementation 'org.springframework.boot:spring-boot-autoconfigure'
 //LOG 관련
 implementation 'ch.qos.logback:logback-classic'
 implementation 'org.apache.logging.log4j:log4j-to-slf4j'
 implementation 'org.slf4j:jul-to-slf4j'
 //YML 관련
 implementation 'org.yaml:snakeyaml'
}
```

**스프링 부트 스타터**

[Spring Boot application starters](https://docs.spring.io/spring-boot/docs/current/reference/html/using.html#using.build-systems.starters)

- 간편한 라이브러리 관리를 위해 프로젝트 시작에 필요한 라이브러리 의존성을 모아둔 스프링 부트 스타터 제공

```groovy
dependencies {
  // 스프링 웹 MVC, 내장 톰캣, JSON 처리, 스프링 부트 관련, LOG, YML 등 포함
 implementation 'org.springframework.boot:spring-boot-starter-web'
 // 스프링 데이터 JPA, 하이버네이트 등 포함
 implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
}
```

**외부 라이브러리 버전 변경**

[Version Properties](https://docs.spring.io/spring-boot/docs/current/reference/html/dependency-versions.html#appendix.dependency-versions.properties)

```groovy
ext['tomcat.version'] = '10.1.4'
```

## Auto Configuration

[Auto Configuration example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/8534640b8d653e9efacf63343d7fe315a77c1703)

스프링 부트는 Auto Configuration 기능을 제공하는데, 자주 사용하는 빈들을 자동으로 등록해 준다.
- JdbcTemplate , DataSource , TransactionManager .. 등 스프링 부트가 자동 구성을 제공해서 스프링 빈으로 등록
- spring-boot-autoconfigure 프로젝트 안에서 수 많은 자동 구성 제공

ex. JdbcTemplateAutoConfiguration

```java
@AutoConfiguration(after = DataSourceAutoConfiguration.class)
@ConditionalOnClass({ DataSource.class, JdbcTemplate.class })
@ConditionalOnSingleCandidate(DataSource.class)
@EnableConfigurationProperties(JdbcProperties.class)
@Import({ DatabaseInitializationDependencyConfigurer.class,
JdbcTemplateConfiguration.class,
NamedParameterJdbcTemplateConfiguration.class })
public class JdbcTemplateAutoConfiguration {
}
```

`@AutoConfiguration` : 자동 구성을 사용하려면 이 애노테이션 등록

- 내부에 @Configuration 으로 빈을 등록하는 자바 설정 파일로 사용
- after = DataSourceAutoConfiguration.class
  - 자동 구성이 실행되는 순서 지정
  - JdbcTemplate 은 DataSource 가 필요므로 DataSource 를 자동으로 등록해주는 DataSourceAutoConfiguration 이후 실행하도록 설정

`@ConditionalOnClass`({ DataSource.class, JdbcTemplate.class })

- IF문과 유사한 기능 제공
- 해당 클래스가 있는 경우에만 설정이 동작
- 없다면 설정들이 모두 무효화 되고, 빈도 등록되지 않음
- JdbcTemplate 은 DataSource, JdbcTemplate 클래스가 있어야 동작이 가능

`@Import` : 스프링에서 자바 설정 추가 시 사용

참고. JdbcTemplateConfiguration

`@Configuration` : 자바 설정 파일로 사용

`@ConditionalOnMissingBean`(JdbcOperations.class)
- JdbcOperations(JdbcTemplate 부모 인터페이스) 빈이 없을 때 동작
- 내가 등록한 JdbcTemplate 과 중복 등록되는 문제 방지

[스프링 부트가 제공하는 자동 구성](https://docs.spring.io/spring-boot/docs/current/reference/html/auto-configuration-classes.html)

---

### @Conditional

- 특정 상황일 때만 특정 빈들을 등록해서 사용하도록 도와주는 기능
- Condition 인터페이스를 구현해서 사용
  ```java
  /**
   * ConditionContext : 스프링 컨테이너, 환경 정보등이 담은 클래스
   * AnnotatedTypeMetadata : 애노테이션 메타 정보를 담은 클래스
   */
  package org.springframework.context.annotation;
    public interface Condition {
    boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata);
  }
  ```

[@conditional example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/c7ea70233c8310bb16dacd5002c5378539f75339)
- 예를 들어, @Conditional(MemoryCondition.class) 선언이 되어 있을 경우
  - MemoryCondition matches() 실행
  - 결과가 true 일 경우
    - MemoryConfig 는 정상 동작 -> memoryController, memoryFinder 빈 등록
  - 결과가 false 일 경우
    - MemoryConfig 는 무효화 -> memoryController, memoryFinder 빈은 등록되지 않음
- 위 코드는 `@ConditionalOnProperty(name = "memory", havingValue = "on")` 한 줄로 처리가 가능

**스프링이 제공하는 다양한 Condition Annotations**

- @ConditionalOnClass, @ConditionalOnMissingClass
  - 클래스가 있는 경우 동작. 나머지는 그 반대
- @ConditionalOnBean, @ConditionalOnMissingBean
  - 빈이 등록되어 있는 경우 동작. 나머지는 그 반대
- @ConditionalOnProperty
  - 환경 정보가 있는 경우 동작.
- @ConditionalOnResource
  - 리소스가 있는 경우 동작.
- @ConditionalOnWebApplication, @ConditionalOnNotWebApplication
  - 웹 애플리케이션인 경우 동작.
- @ConditionalOnExpression
  - SpEL 표현식에 만족하는 경우 동작.

  참고. [Condition Annotations](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.developing-auto-configuration.condition-annotations)
  - 주로 스프링 부트 자동 구성에 사용

### 자동 구성

**자동 구성 라이브러리 만들기**

- 라이브러리 생성 프로젝트
  - Config 파일에 자동 구성 추가
    ```java
    @AutoConfiguration
    @ConditionalOnProperty(name = "memory", havingValue = "on")
    public class MemoryAutoConfig {
        @Bean
        public MemoryController memoryController() {
            return new MemoryController(memoryFinder());
        }
        @Bean
        public MemoryFinder memoryFinder() {
            return new MemoryFinder();
        }
    }
    ```
  - 자동 구성 대상 클래스 지정
    - `src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`
      ```text
      memory.MemoryAutoConfig
      ```
    - 스프링 부트는 시작 시점에 해당 파일의 정보를 읽어서 자동 구성으로 사용
    - 내부에 있는 MemoryAutoConfig가 자동으로 빈 등록
  - 빌드: `./gradlew clean build`
- 라이브러리를 사용할 프로젝트
  - dependencies 추가: `implementation files('libs/memory-v1.jar')`
  - 스프링 부트 자동 구성이 적용되어 라이브러리 사용을 위한 빈들이 자동으로 등록
  - 라이브러리 설정 필요 시 VM 옵션 추가: `-Dmemory=on` 

**스프링 부트의 자동 구성**

- 스프링 부트는 아래 경로에 있는 파일을 읽어서 스프링 부트 자동 구성으로 사용
  - `resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`
  - 스프링 부트가 제공하는 spring-boot-autoconfigure 라이브러리에서도 자동 구성을 사용
    - `org.springframework.boot.autoconfigure.AutoConfiguration.imports`
- 해당 파일을 읽고 동작하는 방식
  - `@SpringBootApplication` 실행 -> `@EnableAutoConfiguration`(자동 구성 활성화) -> `@Import(AutoConfigurationImportSelector.class)`(스프링 설정 정보) -> `resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 파일을 열어서 설정 정보 선택

**ImportSelector**

- [@Import에 설정 정보를 추가하는 방법](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/b504c09c362bc5e35841fac0a98d9511a3fbe187)
  - 정적인 방법: 코드에 대상을 지정
    ```java
    @Configuration
    @Import({AConfig.class, BConfig.class})
    public class AppConfig {...}
    ```
  - 동적인 방법: 설정으로 사용할 대상을 동적으로 선택
    - ImportSelector 인터페이스 구현 -> 단순히 hello.selector.HelloConfig 설정 정보 반환
      ```java
      package org.springframework.context.annotation;

      public interface ImportSelector {
      String[] selectImports(AnnotationMetadata importingClassMetadata);
      //...
      }
      ```
    - 반환되어 설정 정보로 사용할 클래스를 동적으로 프로그래밍
      ```java
      public class HelloImportSelector implements ImportSelector {
          @Override
          public String[] selectImports(AnnotationMetadata importingClassMetadata) {
              return new String[]{"hello.selector.HelloConfig"};
          }
      }

      ...

      @Configuration
      @Import(HelloImportSelector.class)
      public static class SelectorConfig {
      }
      ```

**자동구성의 사용**

- 보통 필요한 빈들은 컴포넌트 스캔하거나 직접 등록하기 때문에, 자동구성은 라이브러리를 만들어서 제공할 때 사용
- 라이브러리를 사용하면서 문제가 발생했을 경우 대처를 위해 스프링 부트의 자동 구성 코드를 읽고, 특정 빈들이 어떻게 등록된 것인지 확인을 할 수 있어야 한다.