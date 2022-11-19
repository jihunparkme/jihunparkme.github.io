---
layout: post
title: JPA Web Application
summary: JPA Programming Part 2. 웹 애플리케이션 개발
categories: JPA 도메인 변경-감지 병합
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

### 도메인 모델과 테이블 설계

- 회원이 주문을 하기 때문에 회원이 주문리스트를 가지는 것이 잘 설계한 것처럼 보이지만, 객체 세상은 실제 세계와는 다르다 
  - 회원이 주문을 참조하지 않고, 주문이 회원을 참조하는 것으로 충분하다.
- 외래키가 있는 곳을 연관관계의 주인으로 정하자.

**`엔티티 클래스 개발`**

- 이론적으로 엔티티 클래스 설계 시 **Getter/Setter를 모두 제공하지 않고, 꼭 필요할 경우 별도의 메서드를 제공**하는 것이 이상적이다.
  - 실무에서는 엔티티 데이터를 조회할 일이 많으므로, Getter 정도는 열어두는 것이 편리
  - 단, 엔티티를 변경할 때는 Setter 대신 변경 지점이 명확하도록 별도 비즈니스 메서드를 제공하자.
- 테이블 ID는 관례상 **테이블명 + id**를 많이 사용
- 실무에서는 **@ManyToMany 를 사용하지 말자**
  - 중간 테이블에 컬럼 추가가 불가능하고, 쿼리를 세밀하게 실행하기 어려우므로 실무에서 사용하기에는 한계 존재
  - 대신, 중간 엔티티를 만들고 대다대 매핑을 일대다, 다대일 매핑으로 풀어내서 사용하자
- **값 타입**은 생성자에서 값을 모두 초기화해서 **변경 불가능한 클래스로 설계**하자.
  - JPA 스펙상 엔티티나 임베디드 타입은 자바 기본 생성자를 public 또는 (가급적) protected 로 설정해주자. `@NoArgsConstructor(access = AccessLevel.PROTECTED)`
  - JPA 구현 라이브러리가 객체를 생성할 때 리플랙션, 프록시 같은 기술을 사용할 수 있도록 지원해야 하기 때문

### 엔티티 설계 주의사항

**엔티티에는 가급적 Setter를 사용하지 않기**

- Setter가 모두 열려있다면, 변경 포인트가 너무 많아서 유지보수가 어려워진다.

**모든 연관관계는 지연로딩(LAZY)으로 설정하기**

- 즉시로딩(EAGER)은 예측이 어렵고, 어떤 SQL이 실행될지 추적이 어려움
- 특히나 JPQL을 실행할 때 N+1 문제가 자주 발생
- 연관된 엔티티를 함께 DB에서 조회해야 한다면, **fetch join** 또는 **엔티티 그래프** 기능을 사용하자.
- @XToOne(OneToOne, ManyToOne) 관계는 기본이 즉시로딩(EAGER)이므로 직접 지연로딩(LAZY)으로 설정해야 한다.

**컬렉션은 필드에서 초기화 하기**

- 컬렉션은 필드에서 바로 초기화 하는 것이 null 문제에서 안전
- 하이버네이트는 엔티티를 영속화 할 때, 컬랙션을 감싸서 하이버네이트가 제공하는 내장 컬렉션으로 변경 `org.hibernate.collection.internal.PersistentBag`
- 만약 getOrders() 처럼 임의의 메서드에서 컬력션을 잘못 생성하면 하이버네이트 내부 메커니즘에 문제가 발생할 수 있다. 따라서 필드레벨에서 생성하는 것이 가장 안전하고, 코드도 간결하다.
```java
private List<OrderItem> orderItems = new ArrayList<>();
```

**영속성 전이**

- 특정 엔티티를 영속 상태로 만들 때, 연관된 엔티티도 함께 영속 상태로 만들고 싶을 경우 사용
- 단, 엔티티의 소유자가 하나일 때만 사용해야 한다.
```java
@OneToMany(mappedBy = "parent", cascade = CascadeType.ALL)
```

**연관관계 편의 메서드**

- 양방향 연관관계 시 객체간 값 세팅에 필요
```java
  public void setMember(Member member) {
      this.member = member;
      member.getOrders().add(this);
  }

  public void addOrderItem(OrderItem orderItem) {
      orderItems.add(orderItem);
      orderItem.setOrder(this);
  }

  public void setDelivery(Delivery delivery) {
      this.delivery = delivery;
      delivery.setOrder(this);
  }
```

**테이블, 컬럼명 생성 전략**

- `SpringPhysicalNamingStrategy`
  - 하이버네이트의 기존 구현은 엔티티의 필드명을 그대로 테이블의 컬럼명으로 사용
  - 스프링 부트 기본 설정은 (엔티티/필드 > 테이블/컬럼)
    - `CamelCase` -> `_`(underscore)
    - `.`(dot) -> `_`(underscore)
    - `대문자` -> `소문자`
- 논리명 적용
  - 명시적으로 컬럼/테이블명을 직접 적지 않으면 `ImplicitNamingStrategy` 사용
  ```properties
  spring.jpa.hibernate.naming.implicit-strategy : 
  org.springframework.boot.orm.jpa.hibernate.SpringImplicitNamingStrategy
  ```
- 물리명 적용
  - 모든 논리명, 실제 테이블에 적용
  - `SpringPhysicalNamingStrategy` 를 참고해서 커스터마이징 룰로 변경 가능(username -> usernm)
  ```properties
  spring.jpa.hibernate.naming.physical-strategy: 
  org.springframework.boot.orm.jpa.hibernate.SpringPhysicalNamingStrategy
  ```
- Reference
  - [Configure Hibernate Naming Strategy](https://docs.spring.io/spring-boot/docs/2.1.3.RELEASE/reference/htmlsingle/#howto-configure-hibernate-naming-strategy)
  - [Naming strategies](https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#naming)

## 도메인 개발

### Repository

- `@Repository`
  - 스프링 빈으로 등록, JPA 예외를 스프링 기반 예외로 예외 변환
- `@PersistenceContext`
  - 엔티티 메니저( EntityManager) 주입
- `@PersistenceUnit`
  - 엔티티 메니터 팩토리( EntityManagerFactory) 주입

```java
@Repository
@RequiredArgsConstructor
public class MemberRepository {

    /**
     * SpringBoot(SpringDataJPA) 가
     * @PersistenceContext 대신 final, RequiredArgsConstructor (@Autowired)로 대체 가능하도록 지원
     */
    private final EntityManager em;

    public void save(Member member) {
        em.persist(member);
    }

    public Member findOne(Long id) {
        return em.find(Member.class, id);
    }

    public List<Member> findAll() {
        return em.createQuery("select m from Member m", Member.class)
                .getResultList();
    }

    public List<Member> findByName(String name) {
        return em.createQuery("select m from Member m where m.name = :name", Member.class)
                .setParameter("name", name)
                .getResultList();
    }
}
```

### Service

- `@Service`
- `@Transactional`
  - 트랜잭션, 영속성 컨텍스트
  - `readOnly=true`
    - 데이터의 변경이 없는 읽기 전용 메서드에 사용
    - 영속성 컨텍스트를 flush 하지 않으므로 약간의 성능 향상(읽기 전용에는 다 적용)
  - 데이터베이스 드라이버가 지원하면 DB에서 성능 향상
- `@Autowired`
  - 생성자 Injection으로 많이 사용, 생성자가 하나면 생략 가능

### DI 주입

공통적으로는 Spring 가동 시 의존성 주입 발생

**Field Injection**

  - 테스트 코드 작성 시 의존성 필드를 변경할 수 없어 **mock 객체 주입이 어려운 단점**
  ```java
  @Service
  public class MemberService {

      @Autowired
      private MemberRepository memberRepository;
  }
  ```
**Setter injection**

  - 테스트 코드 작성 시 **mock 객체 주입 가능**
  - 하지만, setter 메서드가 노출되어 **중간에 생성자 변경을 시도**할 수 있고, 의존성 필드 추가 시 **번거로운 코드 추가가 필요**
  ```java
  @Service
  public class MemberService {
      private MemberRepository memberRepository;

      @Autowired
      public voidMemberRepository(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
      }
  }
  ```
**Construct injection**

  - 생성자 주입 방식을 권장
  - 변경 불가능한 안전한 객체 생성
    - 생성자에서 injection 되므로 **중간에 생성자 변경 불가능**
  - 테스트 코드 작성 시 **생성자 주입 관련하여 컴파일 오류로 명확하게 인지 가능**
  - 생성자가 하나면, @Autowired 생략 가능
  ```java
  @Service
  public class MemberService {
      private MemberRepository memberRepository;

      @Autowired
      public MemberRepository(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
      }
  }
  ```
  
**Construct injection using lombok**
  - final 필드만 대상으로 생성자 생성
    - final 키워드를 추가하면 컴파일 시점에 memberRepository를 설정하지 않는 오류 체크 가능
    - 보통 기본 생성자를 추가할 때 발견
  - injection에 필요한 필드만 구분 가능
  
  ```java
  @Service
  @RequiredArgsConstructor
  public class MemberService {

      private final MemberRepository memberRepository;
  }
  ```

  > <https://data-make.tistory.com/657>

### Test

- `@RunWith(SpringRunner.class)`
  - 스프링과 테스트 통합
- `@SpringBootTest`
  - 스프링 부트 띄우고 테스트(이게 없으면 @Autowired 다 실패)
- `@Transactional`
  - 반복 가능한 테스트 지원
  - 각각의 테스트를 실행할 때마다 트랜잭션을 시작하고 **테스트가 끝나면 트랜잭션을 강제로 롤백**
  - 이 어노테이션이 테스트 케이스에서 사용될 때만 롤백

> [GivenWhenThen](https://martinfowler.com/bliki/GivenWhenThen.html)


### In-Memory DB

- 테스트는 케이스 격리된 환경에서 실행하고, 테스트 종료 시 데이터를 초기화하 하자.
  - In-Memory DB 사용이 가장 이상적!
- 테스트 케이스를 위한 스프링 환경(`src/test/resources/application.yml`)과 애플리케이션을 실행하는 환경(`src/main/resources/application.yml`) 설정 파일을 **분리해서 사용**하자.
- 스프링 부트는 datasource 설정이 없으면, 기본적을 In-Memory DB 사용
  - driver-class : 현재 등록된 라이브러리를 보고 결정
  - ddl-auto : create-drop 모드로 동작
  - **datasource, JPA 관련된 별도의 추가 설정을 하지 않아도 가능 (자동으로 인메모리 모드 전환)**

> [H2 Database Engine Cheat Sheet](https://www.h2database.com/html/cheatSheet.html)

### 도메인 모델 패턴

**도메인 모델 패턴**

- 엔티티가 비즈니스 로직을 가지고 객체 지향의 특성을 적극 활용하는 패턴
- 서비스 계층은 단순히 엔티티에 필요한 요청을 위임하는 역할
- JPA, ORM...
- [Domain Model](http://martinfowler.com/eaaCatalog/domainModel.html)

**트랜잭션 스크립트 패턴**

- 엔티티에 비즈니스 로직이 거의 없고 서비스 계층에서 대부분의 비즈니스 로직을 처리하는 패턴
- Mybatis
- [Transaction Script](http://martinfowler.com/eaaCatalog/transactionScript.html)

## 변경 감지와 병합

**준영속 엔티티**

- 영속성 컨텍스트가 더이상 관리하지 않는 엔티티
- 식별자를 가지고 있는 new Object 앤티티를 준영속 엔티티로 볼 수 있음

```java
Book book = new Book();
book.setId(form.getId());
book.setName(form.getName());
book.setPrice(form.getPrice());
book.setStockQuantity(form.getStockQuantity());
book.setAuthor(form.getAuthor());
book.setIsbn(form.getIsbn());
```

### 준영속 엔티티를 수정하는 방법

**변경 감지 기능 사용**

- 영속성 컨텍스트에서 엔티티를 다시 조회한 후에 데이터를 수정하는 방법
- 트랜잭션 안에서 엔티티를 다시 조회/변경할 경우 트랜잭션 커밋 시점에 변경 감지(Dirty Checking)가 동작해서 UPDATE 쿼리 실행
- 귀찮을 수 있지만 병합은 위험성이 존재하므로 Dirty Checking 을 잘 활용하자.

```java
/**
  * @param itemId
  * @param param : 파리미터로 넘어온 준영속 상태의 엔티티
  */
  @Transactional
  public void updateItem(Long itemId, Item param) {
    Item findItem = itemRepository.findOne(itemId); //같은 엔티티 조회(영속 상태)
    findItem.setPrice(param.getPrice()); //데이터 수정
    findItem.setName(param.getName());
    findItem.setStockQuantity(param.getStockQuantity());
    // Transactional commit -> flush
  }
```

**병합(merge) 사용**

- 준영속 상태의 엔티티를 영속 상태로 변경할 때 사용하는 기능
- `변경 감지 기능`을 사용하면 원하는 속성만 선택해서 변경할 수 있지만, `병합`을 사용하면 모든 필드가 변경되므로 **병합 시 값이 없으면 null 로 업데이트되는 위험성 존재**

\1. merge() 실행

\2. 파라미터로 넘어온 준영속 엔티티의 식별자 값으로 1차 캐시에서 엔티티를 조회

\2-1. 만약 1차 캐시에 엔티티가 없으면 데이터베이스에서 엔티티를 조회하고, 1차 캐시에 저장

\3. 조회한 영속 엔티티에 준영속 엔티티의 모든 값을 채워 넣는다.

\4. 영속 상태인 엔티티 반환

\5. 트랜잭션 커밋 시점에 변경 감지 기능이 동작해서 데이터베이스 UPDATE 쿼리 실행

```java
@Transactional
void update(Item itemParam) { //itemParam: 파리미터로 넘어온 준영속 상태의 엔티티
    Item mergeItem = em.merge(item);
}
```

**결론**

- 엔티티를 변경할 때 항상 `변경 감지`를 사용하자.
- 컨트롤러에서 어설프게 엔티티를 생성하지 말자. 
- `트랜잭션이 있는 서비스 계층`에 식별자와 변경할 데이터를 명확하게 전달하자.
  - parameter, dto 활용
- `트랜잭션이 있는 서비스 계층`에서 영속 상태의 엔티티를 조회하고, 엔티티의 데이터를 직접 변경하하자.
  - 트랜잭션 커밋 시점에 변경 감지 실행
  - Setter 없이 엔티티에서 바로 추적 가능한 메서드를 만들자.

```java
/**
 * Controller
 */ 
@PostMapping(value = "/items/{itemId}/edit")
public String updateItem(@PathVariable Long itemId, @ModelAttribute("form") BookForm form) {

    itemService.updateItem(itemId, form.getName(), form.getPrice(), form.getStockQuantity());

    return "redirect:/items";
}

/**
 * Service
 */
@Transactional
public void updateItem(Long itemId, String name, int price, int stockQuantity) {
    Item findItem = itemRepository.findOne(itemId); //같은 엔티티 조회(영속 상태)
    findItem.change(name, price, stockQuantity);
}
```