---
layout: post
title: Spring Boot
summary: Spring Boot 핵심 원리와 활용
categories: Spring-Boot 자동구성 외부설정 모니터링
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

## 외부설정

환경에 따라 변하는 설정값을 실행 시점에 주입

설정값 외부 설정을 하는 일반적인 네 가지 방법
- `OS 환경 변수`: OS에서 지원하는 외부 설정. 해당 OS를 사용하는 모든 프로세스에서 사용
  - [commit](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/8dafc144067cbb603716e428fffe901b2cb5aab0)
- `자바 시스템 속성`: 자바에서 지원하는 외부 설정. 해당 JVM 안에서 사용
  - `java -Durl=devdb -Dusername=dev_user -Dpassword=dev_pw -jar app.jar`
  - [commit](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/83e5b951d1ffd06b21c05d9b4317527405ae99e6)
- `자바 커맨드 라인 인수`: 커맨드 라인에서 전달하는 외부 설정. 실행시 main(args) 메서드에서 사용
  - `java -jar app.jar dataA dataB`
  - [commit](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/bb6f9af170da552493bffab90bc24fc9e028276f)
- `자바 커맨드 라인 옵션 인수`: 스프링에서 커맨드 라인 인수를 key=value 형식으로 편리하게 사용할 수 있도록 표준 방식(--) 정의
  - `java -jar app.jar --url=devdb --username=dev_user --password=dev_pw mode=on`
  - [commit](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/f505f48acd33fb89a4a4a0738c5dd9f29832b1ca)
  - [스프링 부트에서 사용](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/51ac6770d986e8bd5db4d058d3f6a11cbebb68c5)
- `외부 파일(설정 데이터)`: 프로그램에서 외부 파일을 직접 읽어서 사용
  - 로딩 시점에 파일(`.properties`, `.yml`)을 자동으로 읽어서 그 속의 값들을 외부 설정값으로 사용
  - 프로필: `spring.profiles.active={profile}` 설정으로 프로필 지정
    - 아래 규칙으로 설정 프로필에 맞는 내부 파일(설정 데이터) 조회 
    - `application-{profile}.properties`
  - 커맨드 라인 옵션 인수 실행: `--spring.profiles.active=dev`
  - 자바 시스템 속성 실행: `-Dspring.profiles.active=dev`
  - [내부 파일 통합](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/12819ba26ceacc67954c715832f6e5e8a35b00ed)

**[스프링 통합](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/028f460681fea8cc22d385169d5a4f4b0378e5de)**

- 추상화(Environment, PropertySource)를 통해 외부 설정값이 어디에 위치하든 일관성 있고, 편리하게 설정값을 읽을 수 있음
- PropertySource: 스프링은 로딩 시점에 필요한 PropertySource 들을 생성하고, Environment 에서 사용할 수 있게 연결
- Environment: 모든 외부 설정(*커멘드 라인 옵션 인수, 자바 시스템 속성, OS 환경변수, 설정 파일*)은 Environment 를 통해 조회

**우선순위**

- 더 유연한 것이 우선권
- 범위가 넒은 것 보다 좁은 것이 우선권

```yml
url=local.db.com
username=local_user
password=local_pw
#---
spring.config.activate.on-profile=dev
url=dev.db.com
username=dev_user
password=dev_pw
#---
spring.config.activate.on-profile=prod
url=prod.db.com
username=prod_user
password=prod_pw
```

- 단순하게 문서를 위에서 아래로 순서대로 읽으면서 값을 설정. 기존 데이터가 있으면 덮어쓰기
- 논리 문서에 `spring.config.activate.on-profile` 옵션이 있으면 해당 프로필을 사용할 때(*--spring.profiles.active*)만 논리 문서 적용

[**외부 설정 우선순위**](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config)

(내려갈수록 우선순위 높아짐)

- 설정 데이터(application.properties)
- OS 환경변수
- 자바 시스템 속성
- 커맨드 라인 옵션 인수
- @TestPropertySource(in Test)

[**설정 데이터 우선순위**](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config.files)

(내려갈수록 우선순위 높아짐)

- jar 내부 application.properties
- jar 내부 프로필 적용 파일 application-{profile}.properties
- jar 외부 application.properties
- jar 외부 프로필 적용 파일 application-{profile}.properties

applicaiton.properties에 설정 데이터를 기본으로 사용하다가 일부 속성을 변경할 필요가 생기면 더 높은 우선순위를 가지는 자바 시스템 속성이나 커맨드 라인 옵션 인수를 사용할 수도 있다.

### 외부 설정 사용

**`Environment`**

- Environment로 외부 설정 조회
- Environment를 직접 주입받고, env.getProperty(key)를 통해 값을 꺼내는 과정을 반복해야 하는 단점
- [속성 변환기(Properties Conversion)](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config.typesafe-configuration-properties.conversion)
- [Environment example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/317f085f9d73d038d572c5827f828dc449fc2ed4)

```java
String url = env.getProperty("my.datasource.url");
String username = env.getProperty("my.datasource.username");
String password = env.getProperty("my.datasource.password");
int maxConnection = env.getProperty("my.datasource.etc.max-connection", Integer.class);
Duration timeout = env.getProperty("my.datasource.etc.timeout", Duration.class);
List<String> options = env.getProperty("my.datasource.etc.options", List.class);
```

**`@Value`**

- 외부 설정값을 편리하게 주입
- 내부에서는 Environment 사용
- 필드, 파라미터에 사용 가능
- 타입 컨버팅을 자동으로 수행
- 외부 설정 정보의 키 값을 하나하나 입력, 주입 받아야 하는 단점
- 기본값 사용 시: `@Value("${my.datasource.etc.max-connection:1}")`
- [@Value example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/7a031b7295ae4abb339c0fe578a9a3d54a52412d)

```java
@Value("${my.datasource.url}")
private String url;
@Value("${my.datasource.username}")
private String username;
@Value("${my.datasource.password}")
private String password;
@Value("${my.datasource.etc.max-connection}")
private int maxConnection;
@Value("${my.datasource.etc.timeout}")
private Duration timeout;
@Value("${my.datasource.etc.options}")
private List<String> options;
```

**`@ConfigurationProperties`**

- Type-safe Configuration Properties
- **외부 설정의 묶음, 계층 정보를 객체로 변환**해서 사용
- **타입 안전한 설정** 속성 사용(타입이 다르면 오류 발생)
- 캐밥 표기법을 낙타 표기법으로 중간에 자동으로 변환
- [@ConfigurationProperties example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/a22e7e3f9f31628a7f58c09f892e6ad01edb1d17)
- 값 변경 방지를 위해 세터 대신 **생성자**를 사용하자.
- **@DefaultValue**: 해당 값을 찾을 수 없는 경우 기본값을 사용
- [@ConfigurationProperties 생성자 활용](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/46cc8384974355a374ee5979185942c7b0d527f6)
- 숫자의 범위, 문자의 길이 검증을 위해 **자바 빈 검증기**(java bean validation) 사용 가능
  - dependency: *implementation 'org.springframework.boot:spring-boot-starter-validation*
- [@ConfigurationProperties 속성 검증](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/95601713aeb5d258ea31308edd139c41a187375d)

> 가장 좋은 예외는 컴파일 예외, 그리고 애플리케이션 로딩 시점에 발생하는 예외. 
> 
> 가장 나쁜 예외는 고객 서비스 중에 발생하는 런타임 예외

```java
my.datasource.url=local.db.com
my.datasource.username=username
my.datasource.password=password
my.datasource.etc.max-connection=1
my.datasource.etc.timeout=3500ms
my.datasource.etc.options=CACHE,ADMIN

...

@Getter
@ConfigurationProperties("my.datasource")
public class MyDataSourcePropertiesV2 {
    private String url;
    private String username;
    private String password;
    private Etc etc;

    public MyDataSourcePropertiesV2(String url, String username, String password, @DefaultValue Etc etc) {
        this.url = url;
        this.username = username;
        this.password = password;
        this.etc = etc;
    }

    @Getter
    public static class Etc {
        private int maxConnection;
        private Duration timeout;
        private List<String> options;

        public Etc(int maxConnection, Duration timeout, @DefaultValue("DEFAULT") List<String> options) {
            this.maxConnection = maxConnection;
            this.timeout = timeout;
            this.options = options;
        }
    }
}
```

### YAML

YAML(YAML Ain't Markup Language)은 읽기 좋은 데이터 구조를 목표

- 확장자는 yaml, yml(주로 사용)
- application.properties, application.yml 동시 사용 시 application.properties 우선권
- `---`로 논리 파일 구분
- spring.config.active.on-profile 로 프로필 적용
- `--spring.profiles.active=dev`
- [yaml example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/1bad8b61c94df81c99ae32c4d225e86119168abc)

### @Profile

@Profile 애노테이션을 사용하면 해당 프로필이 활성화된 경우에만 빈 등록
- 특정 조건에 따라 해당 빈을 등록할지 말지 선택
- 각 환경 별로 외부 설정 값, 등록되는 스프링 빈 분리
- 스프링은 @Conditional 기능을 활용해서 @Profile 기능을 제공
- [profile example](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/212c129d47786cdf3a38b392c66ad898e9c621e2)

## 액츄에이터

[Production-ready Features](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)

모니터링 대응을 위해 서비스에 문제가 없는지 모니터링하고, 지표들을 심어서 감시하는 활동이 중요

프로덕션 준비 기능: 프로덕션을 운영에 배포할 때 준비해야 하는 비 기능적 요소

- 애플리케이션이 살아있는지, 로그 정보는 정상 설정 되었는지, 커넥션 풀은 얼마나 사용되고 있는지 등 확인 필요
  - 지표(metric): CPU 사용량
  - 추적(trace): 이슈 코드 추적
  - 감사(auditing): 고객 로그인, 로그아웃 이력 추적
  - 모니터링: 시스템 상태

Dependency

```groovy
implementation 'org.springframework.boot:spring-boot-starter-actuator'
```

- `http://localhost:8080/actuator` 로 확인 가능
  - 애플리케이션 상태 정보: `http://localhost:8080/actuator/health`
  - 각 엔드포인트는 /actuator/{엔드포인트명} 형식으로 접근
  - 더 많은 기능을 제공받기 위해 엔드포인트 노출 설정 추가(모든 엔드포인트를 웹에 노출)
    - 엔드포인트는 shutdown 제외하고 대부분 기본으로 활성화
    - 특정 엔드포인트 활성화 시 `management.endpoint.{엔드포인트명}.enabled=true`
    ```yml
    management:
      endpoints:
        web:
          exposure:
            include: "*"
    ```

[Endpoints](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.endpoints)

- /actuator: 
- /actuator/`beans`: 스프링 컨테이너에 등록된 스트링 빈 목록
- /actuator/`caches`:
  - /actuator/caches/{cache}:  
- /actuator/`health`: 애플리케이션 문제를 빠르게 인지(전체 상태, db, mongo, redis, diskspace, ping 등 확인 가능)
  - /actuator/health/{*path}: 
  - 헬스 컴포넌트 중 하나라도 문제가 있으면 전체 상태는 DOWN
  - 헬스 정보를 더 자세히 보기 위한 옵션 `management.endpoint.health.show-details=always`
  - 간략히 보기 위한 옵션 `management.endpoint.health.show-components=always`
  - [Auto-configured HealthIndicators](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.endpoints.health.auto-configured-health-indicators)
  - [Writing Custom HealthIndicators](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.endpoints.health.writing-custom-health-indicators)
- /actuator/`info`: 애플리케이션 기본 정보 (default 비활성화)
  - `management.info.<id>.enabled=true`
  - java : 자바 런타임 정보
  - os : OS 정보
  - env : Environment 에서 info. 로 시작하는 정보
  - build : 빌드 정보 (META-INF/build-info.properties 파일 필요)
    ```groovy
    // build.gradle 에 아래 코드를 추가하면 자동으로 빌드 정보 파일 생성
    springBoot {
      buildInfo()
    }
    ```
  - git : git 정보 (git.properties 파일 필요)
    ```groovy
    // git.properties plugin 추가
    id "com.gorylenko.gradle-git-properties" version "2.4.1"
    ```
  - [Writing Custom InfoContributors](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.endpoints.info.writing-custom-info-contributors)
  - [info endpoints sample](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/d079267ec76a83406061158a6bfef60eb7d7fb2c)
- /actuator/`conditions`: condition을 통해 빈 등록 시 평가 조건과 일치하거나 일치하지 않는 이유 표시
- /actuator/`configprops`: @ConfigurationProperties 목록
- - /actuator/configprops/{prefix}: 
- /actuator/`env`: Environment 정보
  - /actuator/env/{toMatch}: 
- /actuator/`loggers`: 로깅 관련 정보 확인. 실시간 변경
  - 특정 패키지에 로그 레벨 설정(default. INFO)
    ```properties
    logging.level.hello.controller: debug
    ```
  - 특정 로거 이름 기준으로 조회. /actuator/`loggers/{name}`
    - /actuator/loggers/hello.controller
  - 애플리케이션을 다시 시작하지 않고, (메모리에) 실시간으로 로그 레벨 변경
    ```json
    POST http://localhost:8080/actuator/loggers/hello.controller

    {
      "configuredLevel": "TRACE"
    }
    ```
- /actuator/`heapdump`: 
- /actuator/`threaddump`: 쓰레드 덤프 정보
- /actuator/`metrics`: : 애플리케이션의 메트릭 정보
  - /actuator/metrics/{requiredMetricName}
    ```text
    /actuator/metrics/jvm.memory.used : JVM 메모리 사용량
    --- availableTags
    /actuator/metrics/jvm.memory.used?tag=area:heap

    /actuator/metrics/http.server.requests : HTTP 요청수
    --- availableTags
    /actuator/metrics/http.server.requests?tag=uri:/log
    /actuator/metrics/http.server.requests?tag=uri:/log&tag=status:200
    ```
- /actuator/`scheduledtasks`: 
- /actuator/`mappings`: @RequestMapping 정보 목록
- /`httpexchanges`: HTTP 호출 응답 정보. HttpExchangeRepository 구현 빈 등록 필요
  - 최대 100개의 HTTP 요청 제공(최대 요청 초과 시 과거 요청을 삭제
  - setCapacity() 로 최대 요청수를 변경 가능
  - 단순하고 제한이 많은 기능이므로 개발 단계에서만 주로 사용하고, 실제 운영 서비스에서는 모니터링 툴이나 핀포인트, Zipkin 같은 다른 기술 사용 추천
- /`shutdown`: 애플리케이션 종료. 기본으로 비활성화

보안을 위해 내부망에서만 사용 가능하도록 포트 설정

```properties
management.server.port=9292
```
- 외부망을 통해 접근이 필요하다면 /actuator 경로에 서블릿 필터, 스프링 인터셉터, 스프링 시큐티리를 통해 인증된 사용자만 접근 가능하도록 설정 필요

## 모니터링

서비스 운영 시 애플리케이션의 CPU, 메모리, 커넥션 사용, 고객 요청 수 같은 수 많은 지표들을 확인하는 것이 필요하다.

그래야 어디에 어떤 문제가 발생했는지 사전 대응이 가능하고, 실제 문제가 발생해도 원인을 빠르게 파악하고 대처할 수 있다. 

### 마이크로미터

수 많은 모니터링 툴이 있고, 각 툴마다 전달 방식이 다른데 이 모든 것들을 추상화한 라이브러리가 마이크로미터(Micrometer)

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/micrometer.png?raw=true 'Result')

- 마이크로미터는 application metric facade 라고 불리는데, 애플리케이션의 메트릭(측정 지표)을 마이크로미터가 정한 표준 방법으로 모아서 제공 (추상화된 마이크로미터로 구현체를 쉽게 갈아끼울 수 있음)
- spring boot actuator 는 마이크로미터를 기본 내장해서 사용
- 개발자는 마이크로미터가 정한 표준 방법으로 메트릭(측정 지표)를 전달
  - 사용하는 모니터링 툴에 맞는 구현체 선택
  - 이후 모니터링 툴이 변경되어도 해당 구현체만 변경해주면 끝
  - 애플리케이션 코드는 모니터링 툴이 변경되어도 그대로 유지 가능

[Micrometer Documentation](https://micrometer.io/docs)

<details>
<summary>마이크로미터가 지원하는 모니터링 툴</summary>
AppOptics

Atlas

CloudWatch

Datadog

Dynatrace

Elastic

Ganglia

Graphite

Humio

Influx

Instana

JMX

KairosDB

New Relic

Prometheus

SignalFx

Stackdriver

StatsD

Wavefront
</details>

### 메트릭

[Supported Metrics and Meters](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.metrics.supported)

마이크로미터와 액츄에이터가 기본으로 제공하는 다양한 메트릭
- JVM 메트릭 `jvm.*`
  - 메모리 및 버퍼 풀 세부 정보
  - 가비지 수집 관련 통계
  - 스레드 활용
  - 로드 및 언로드된 클래스 수
  - JVM 버전 정보
  - JIT 컴파일 시간
- 시스템 메트릭 `system.*, process.*, disk.*`
  - CPU 지표
  - 파일 디스크립터 메트릭
  - 가동 시간 메트릭
  - 사용 가능한 디스크 공간
- 애플리케이션 시작 메트릭 `application.*`
  - application.started.time: 애플리케이션 시작에 걸리는 시간
  (ApplicationStartedEvent로 측정 - 스프링 컨테이너가 완전히 실행된 상태. 이후에 커맨드 라인 러너가 호출)
  - application.ready.time : 애플리케이션 요청을 처리할 준비가 되는데 걸리는 시간
    (ApplicationReadyEvent 로 측정- 커맨드 라인 러너가 실행된 이후에 호출)
- 스프링 MVC 메트릭
  - http.server.requests: 스프링 MVC 컨트롤러가 처리하는 모든 요청 정보
  - TAG 로 정보를 분류해서 확인 가능
    - uri : 요청 URI
    - method : HTTP 메서드(GET, POST..)
    - status : HTTP Status 코드(200, 400, 500..)
    - exception : 예외
    - outcome : 상태코드 그룹(1xx:INFORMATIONAL, 2xx:SUCCESS, 3xx:REDIRECTION, 4xx:CLIENT_ERROR, 5xx:SERVER_ERROR)
- 톰캣 메트릭 `tomcat.`
  - 톰캣의 최대 쓰레드, 사용 쓰레드 수를 포함한 다양한 메트릭 확인 가능
    ```yml
    server:
      tomcat:
        mbeanregistry:
          enabled: true
    ```
- 데이터 소스 메트릭: DataSource, Connection Pool 관련 메트릭 정보 `jdbc.connections.`
  - 최대 커넥션, 최소 커넥션, 활성 커넥션, 대기 커넥션 수 등 확인 가능
- 로그 메트릭 : logback 로그에 대한 메트릭 정보
  - trace, debug, info, warn, error 각 로그 레벨에 따른 로그 수 확인 가능
- 기타
  - HTTP 클라이언트 메트릭(RestTemplate , WebClient)
  - 캐시 메트릭
  - 작업 실행과 스케줄 메트릭
  - 스프링 데이터 리포지토리 메트릭
  - 몽고DB 메트릭
  - 레디스 메트릭
- 커스텀 메트릭

### 프로메테우스 & 그라파나

- `프로메테우스` : 메트릭을 지속해서 수집하고 DB에 저장하는 역할
  - [Prometheus Docs](https://prometheus.io/docs/introduction/overview/) 
- `그라파나` : 프로메테우스에 있는 데이터를 불러서 데이터를 그래프로 보여주는 툴
  - 다양한 그래프를 제공하고, 프로메테우스를 포함한 다양한 데이터소스 지원

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-boot/prometheus.png?raw=true 'Result')

\1. 스프링 부트 액츄에이터, 마이크로미터를 사용하면 수 많은 메트릭 자동 생성
- 마이크로미터 프로메테우스 구현체는 프로메테우스가 읽을 수 있는 포멧으로 메트릭을 생성

\2. 프로메테우스는 이렇게 만들어진 메트릭을 지속해서 수집

\3. 프로메테우스는 수집한 메트릭을 내부 DB에 저장

\4. 사용자는 그라파나 대시보드 툴을 통해 그래프로 편리하게 메트릭을 조회(필요한 데이터는 프로메테우스를 통해 조회)

#### 프로메테우스

메트릭을 수집하고 보관하는 DB

.

**설치**

- https://prometheus.io/download/
- https://github.com/prometheus/prometheus/releases/download/v2.42.0/prometheus-2.42.0.darwin-amd64.tar.gz
- Mac OS: darwin 

**실행**

- 시스템 환경설정 - 보안 및 개인 정보 보호 - 일반 - 확인 없이 허용
- terminal - `./prometheus` 
- http://localhost:9090/

**애플리케이션 설정**

- 애플리케이션 설정
  - 프로메테우스가 애플리케이션의 메트릭을 가져갈 수 있도록, 프로메테우스 포멧에 맞추어 메트릭 생성
  - 각 메트릭들은 내부에서 마이크로미터 표준 방식으로 측정되어 어떤 구현체를 사용할지만 지정
    ```groovy
    // 스프링 부트와 액츄에이터가 자동으로 마이크로미터 프로메테우스 구현체를 등록해서 동작하도록 설정
    implementation 'io.micrometer:micrometer-registry-prometheus'
    ```
  - 액츄에이터에 프로메테우스 메트릭 수집 엔드포인트가 자동 추가
    - `/actuator/prometheus`
- 프로메테우스 설정
  - 프로메테우스가 애플리케이션의 메트릭을 주기적으로 수집하도록 설정

**수집 설정**

prometheus.yml 

```yml
scrape_configs:
 - job_name: "prometheus"
   static_configs:
     - targets: ["localhost:9090"]
 # 하단 추가
 - job_name: "spring-actuator" # 수집하는 임의 이름
   metrics_path: '/actuator/prometheus' # 수집 경로 지정(1초에 한 번씩 호출해서 메트릭 수집)
   scrape_interval: 1s # 수집 주기 (10s~1m 권장)
   static_configs: # 수집할 서버 정보(IP, PORT)
     - targets: ['localhost:8080']
```

http://localhost:9090/
- 프로메테우스 메뉴 -> Status -> Configuration, Targets 에서 추가한 설정 확인

**자주 사용하는 기능**

- 기본기능
  - Table: Evaluation time 을 수정해서 과거 시간 조회
  - Graph: 메트릭을 그래프로 조회
- 필터: 레이블 기준으로 필터 사용. 중괄호(`{}`) 문법 사용
  - 레이블 일치 연산자
    - `=` : 제공된 문자열과 정확히 동일한 레이블 선택
    - `!=` : 제공된 문자열과 같지 않은 레이블 선택
    - `=~` : 제공된 문자열과 정규식 일치하는 레이블 선택
    - `!~` : 제공된 문자열과 정규식 일치하지 않는 레이블 선택
    ```text
    example.
    
    uri=/log , method=GET 조건으로 필터
      -> http_server_requests_seconds_count{uri="/log", method="GET"}

    /actuator/prometheus 는 제외한 조건으로 필터
      -> http_server_requests_seconds_count{uri!="/actuator/prometheus"}

    method 가 GET, POST 인 경우를 포함해서 필터
      -> http_server_requests_seconds_count{method=~"GET|POST"}

    /actuator 로 시작하는 uri 는 제외한 조건으로 필터
      -> http_server_requests_seconds_count{uri!~"/actuator.*"}
    ```
- 연산자 쿼리와 함수
  - `+` (덧셈), `-` (빼기), `*` (곱셈), `/` (분할), `%` (모듈로), `^` (승수/지수)
  - sum: 합계
    - `sum(http_server_requests_seconds_count)`
  - sum by: SQL group by 와 유사
    - `sum by(method, status)(http_server_requests_seconds_count)`
  - count: 메트릭 자체의 수 카운트
    - `count(http_server_requests_seconds_count)`
  - topk: 상위 메트릭 조회
    - `topk(3, http_server_requests_seconds_count)`
  - 오프셋 수정자
    - `http_server_requests_seconds_count offset 10m`
    - 현재 기준 특정 과거 시점의 데이터 반환
  - 범위 벡터 선택기
    - `http_server_requests_seconds_count[1m]`
    - 지난 1분간의 모든 기록값 선택
    - 차트에 바로 표현할 수 없고, 데이터로는 확인 가능
    - 결과를 차트에 표현하기 위해서는 약간의 가공 필요

**게이지와 카운터**

`게이지`(Gauge)
- 임의로 오르내일 수 있는 값(ex. CPU 사용량, 메모리 사용량, 사용중인 커넥션)

`카운터`(Counter)
- 단순하게 증가하는 단일 누적 값(ex. HTTP 요청 수, 로그 발생 수)
- increase()
  - 지정한 시간 단위별로 증가 확인
  - `increase(http_server_requests_seconds_count{uri="/log"}[1m])`
- rate()
  - 범위 백터에서 초당 평균 증가율 계산
- irate()
  - rate 와 유사. 범위 벡터에서 초당 순간 증가율 계산

> [기본기능](https://prometheus.io/docs/prometheus/latest/querying/basics/)
>
> [연산자](https://prometheus.io/docs/prometheus/latest/querying/operators/)
> 
> [함수](https://prometheus.io/docs/prometheus/latest/querying/functions/)

#### 그라파나


- https://grafana.com/grafana/download
- https://dl.grafana.com/enterprise/release/grafana-enterprise-9.3.6.darwin-amd64.tar.gz

**실행**

- 압축을 풀고 bin 폴더 이동 후 `./grafana-server`
- http://localhost:3000/
- 초기 계정 -> admin/admin

**연동**

- 데이터소스 추가
  - 설정(Configuration) ->  Data sources -> Add data source -> Prometheus
  - URL 정보: http://localhost:9090
  - Save & test

**대시보드**

- 애플리케이션, 프로메테우스, 그라파나가 모두 실행중인 상태여야 한다.

  - \1. 왼쪽 Dashboards 메뉴

  - \2. New 버튼 -> New Dashboard

  - \3. 오른쪽 상단 Save dashboard 저장 

  - \4. Dashboard name 입력

- [공유 대시보드 활용](https://grafana.com/grafana/dashboards/)

### 매트릭 활용

비즈니스에 특화된 부분(주문수, 취소수, 재고 수량 등)을 모니터링하기 위해 직접 메트릭 등록 가능

- [등록할 메트릭 기능](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/46e84a81d8c3143cbfcb2271685dedf258be01fe)

**MeterRegistry**

- 마이크로미터 기능을 제공하는 핵심 컴포넌트
- 스프링을 통해서 주입 받아서 사용하고, 카운터, 게이지 등을 등록
- [카운터]((https://prometheus.io/docs/concepts/metric_types/#counter))
  - 단조롭게 증가하는 단일 누적 측정 항목
    - 단일 값, 보통 하나씩 증가, 누적이므로 전체 값을 포함(total)
  - 값을 증가하거나 0으로 초기화 하는 기능만 가능
  - 마이크로미터에서 값을 감소하는 기능도 지원하지만, 목적에 맞지 않음
  - 예) HTTP 요청수 (increase() , rate() 활용)
  - [MeterRegistry 적용 commit](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/fc8582db6e4360a81e6ddfb572fbe2d437dbc2e6)
  - [@Counted 적용 commit](https://github.com/jihunparkme/Inflearn-Spring-Boot/commit/a141a816d1a9370dd5e9f5c3c4523be37952ae2a)
- 게이지

