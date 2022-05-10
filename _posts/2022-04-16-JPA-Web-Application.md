---
layout: post
title: JPA Web Application
summary: JPA Programming Part 2. 웹 애플리케이션 개발
categories: (Inflearn)JPA-Programming
featured-img: jpa-spring-uses
# mathjax: true
---

# JPA Web Application Development

영한님의 [실전! 스프링 부트와 JPA 활용1 - 웹 애플리케이션 개발](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8-JPA-%ED%99%9C%EC%9A%A9-1/dashboard
) 강의 노트

[Project](https://github.com/jihunparkme/inflearn-spring-jpa-roadmap/tree/main/jpa-web-jpashop)

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

**@Transactional**

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

**Build**

```console
./gradlew clean build

cd build/libs/

java -jar XXX.jar
```

**Query Parameter Log**

[spring-boot-data-source-decorator Public](https://github.com/gavlyukovskiy/spring-boot-data-source-decorator)

```gradle
implementation 'com.github.gavlyukovskiy:p6spy-spring-boot-starter:1.5.6'
```

- 외부 라이브러리는 시스템 자원을 사용하므로 운영 적용 시 성능테스트 필요

## 도메인 분석 설계

`**도메인 모델과 테이블 설계**`

- 회원이 주문을 하기 때문에 회원이 주문리스트를 가지는 것이 잘 설계한 것처럼 보이지만, 객체 세상은 실제 세계와는 다르다 
  - 회원이 주문을 참조하지 않고, 주문이 회원을 참조하는 것으로 충분하다.
- 외래키가 있는 곳을 연관관계의 주인으로 정하자.

`**엔티티 클래스 개발**`

- 이론적으로 엔티티 클래스 설계 시 **Getter/Setter를 모두 제공하지 않고, 꼭 필요할 경우 별도의 메서드를 제공**하는 것이 이상적이다.
  - 실무에서는 엔티티 데이터를 조회할 일이 많으므로, Getter 정도는 열어두는 것이 편리
  - 단, 엔티티를 변경할 때는 Setter 대신 변경 지점이 명확하도록 별도 비즈니스 메서드를 제공하자.
- 테이블 ID는 관례상 **테이블명 + id**를 많이 사용
- 실무에서는 **@ManyToMany 를 사용하지 말자**
  - 중간 테이블에 컬럼 추가가 불가능하고, 쿼리를 세밀하게 실행하기 어려우므로 실무에서 사용하기에는 한계 존재
  - 대신, 중간 엔티티를 만들고 대다대 매핑을 일대다, 다대일 매핑으로 풀어내서 사용하자
- **값 타입**은 생성자에서 값을 모두 초기화해서 **변경 불가능한 클래스로 설계**하자.
  - JPA 스펙상 엔티티나 임베디드 타입은 자바 기본 생성자를 public 또는 (가급적) protected 로 설정해주자.
  - JPA 구현 라이브러리가 객체를 생성할 때 리플랙션, 프록시 같은 기술을 사용할 수 있도록 지원해야 하기 때문

`**엔티티 설계 주의사항**`

- **엔티티에는 가급적 Setter를 사용하지 않기**
- **모든 연관관계는 지연로딩으로 설정하기**
- **컬렉션은 필드에서 초기화 하기**