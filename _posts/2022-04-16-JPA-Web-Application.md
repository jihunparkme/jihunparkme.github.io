---
layout: post
title: JPA Web Application
summary: JPA Programming Part 2. 웹 애플리케이션 개발
categories: (Inflearn)JPA-Programming
featured-img: jpa-spring-uses
# mathjax: true
---

# JPA Web Application Development

## Spring Boot Project

[Spring Boot Starter](https://start.spring.io/)

- web, thymeleaf, jpa, h2, lombok, validation..
- set Lombok
  - Prefrences - plugin - lombok
  - Prefrences - Annotation Processors - Enable annotation processing
- set Build Tools Gradle
  - Preferences - Build, Execution, Deployment - Build Tools - Gradle
    - Build and run using: Gradle IntelliJ IDEA
    - Run tests using: Gradle IntelliJ IDEA

## Thymeleaf

- [thymeleaf](https://www.thymeleaf.org/)

- [Spring Guides](https://spring.io/guides#getting-started-guides)

- [Spring menual - Template Engines](https://docs.spring.io/spring-boot/docs/2.1.6.RELEASE/reference/html/boot-features-developing-web-applications.html#boot-features-spring-mvc-template-engines)

## H2 Database

- [H2 Database](https://www.h2database.com)
- 데이터베이스 파일 생성
  - jdbc:h2:~/databaseName (jsessionid 포함 - 파일 모드)
  - ~/databaseName.mv.db 파일 생성 확인
- 데이터베이스 접속
  - jdbc:h2:tcp://localhost/~/databaseName (네트워크 모드)

## JPA & DB 설정


```yml
spring:
  datasource:
    url: jdbc:h2:tcp://localhost/~/jpashop
    username: sa
    password:
    driver-class-name: org.h2.Driver

  jpa:
    hibernate:
      # 애플리케이션 실행 시점에 테이블을 drop 하고, 다시 생성
      ddl-auto: create
  properties:
    hibernate:
      # System.out 에 하이버네이트 실행 SQL을 남긴다.
      show_sql: true
      format_sql: true

logging:
  level:
    # Logger를 통해 하이버네이트 실행 SQL을 남긴다.
    org.hibernate.SQL: debug
    # 쿼리 파라미터 로그
    org.hibernate.type: trace
```

### @Transactional

- @Transactional이 테스트 케이스에 적용될 경우, 테스트 종료 후 바로 롤백 실행
- 롤백을 원하지 않을 경우 @Rollback(false) 사용
  ```java
  @Test
  @Transactional
  @Rollback(false)
  public void testMember() {
      // given
      Member member = new Member();
      member.setUsername("memberA");

      // when
      Long savedId = memberRepository.save(member);
      Member findMember = memberRepository.find(savedId);

      // then
      Assertions.assertThat(findMember.getId()).isEqualTo(member.getId());
      Assertions.assertThat(findMember.getUsername()).isEqualTo(member.getUsername());
      Assertions.assertThat(findMember).isEqualTo(member); // JPA 엔티티 동일성 보장
  }
  ```

### Build

```console
./gradlew clean build

cd build/libs/

java -jar XXX.jar
```

### Query Parameter Log

[spring-boot-data-source-decorator Public](https://github.com/gavlyukovskiy/spring-boot-data-source-decorator)

```gradle
implementation 'com.github.gavlyukovskiy:p6spy-spring-boot-starter:1.5.6'
```

- 외부 라이브러리는 시스템 자원을 사용하므로 운영 적용 시 성능테스트 필요