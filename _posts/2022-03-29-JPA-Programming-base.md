---
layout: post
title: JPA Programming Basic
summary: JPA Programming Part 1. 자바 ORM 표준 JPA 프로그래밍 - 기본편
categories: (Inflearn)JPA-Programming
featured-img: jpa-base
# mathjax: true
---

# JPA Programming Base

**JPA**

- Java Persistence API
- 자바 진영의 ORM 기술 표준 (인터페이스의 모음)
  - 구현체로는 Hibernate, EclipseLink, DataNucleus..
- Application과 JDBC 사이에서 동작

**ROM**

- Object-Relational Mapping
- Object는 Object대로, RDBMS는 RDBMS대로 설계
- ORM 프레임워크가 중간에서 매핑 

**EntityManagerFactory**
- persistence.xml 설정 정보 확인 후 persistence-unit name 에 맞는 EntityManagerFactory 생성
- Web Server 가 생성되는 시점에 하나만 생성해서 애플리케이션 전체에서 공유
  ```java
  EntityManagerFactory emf = Persistence.createEntityManagerFactory("hello");
  ```

**EntityManager**
- 요청 건마다 생성
- 쓰레드간 공유하면 안 되고, 사용 후 종료
  ```java
  EntityManager em = emf.createEntityManager();
  ```
**EntityTransaction**
- JPA의 모든 데이터 변경은 트랜젝션 안에서 실행
  ```java
  EntityTransaction tx = em.getTransaction();
  tx.begin();
  ```

# 영속성 관리

## 영속성 컨텍스트

`PersistenceContext` (엔티티를 영구 저장하는 환경)

- EntityManager 를 통해 PersistenceContext 에 접근
  - EntityManager, PersistenceContext 는 `1:1`, `N:1` 관계 존재

- 엔티티 생명주기
  - `비영속` (new / transient)
    - 영속성 컨텍스트와 전혀 관계가 없는 **새로운** 상태
      ```java
      Member member = new Member();
      member.setId(1L);
      member.setName("Aaron");
      ``` 
  - `영속` (managed)
    - 영속성 컨텍스트에 **관리**되는 상태
      ```java
      entityManager.persist(member);
      ```
  - `준영속` (detached)
    - 영속성 컨텍스트에 저장되었다가 **분리**된 상태
      ```java
      entityManager.detach(member);
      entityManager.clear()
      entityManager.close()
      ```
  - `삭제` (removed)
    - **삭제**된 상태
      ```java
      entityManager.remove(member);
      ``` 

.

**`영속성 컨텍스트의 이점`**

- `1차 캐시`에서의 조회
  - 사용자의 하나의 요청-응답(하나의 트랜젝션) 내에서만 효과가 있으므로 성능 이점을 기대하지는 않음.
  - 엔티티 조회 시 먼저 1차 캐시에서 조회 후, 없을 경우 DB에서 조회
- 영속 엔티티의 `동일성(identity) 보장`
  - 1차 캐시로 반복 가능한 읽기(REPEATABLE READ) 등급의 트랜잭션 격리 수준을 데이터베이스가 아닌 애플리케이션 차원에서 제공
- 트랜잭션을 지원하는 `쓰기 지연`(transactional write-behind)
  - Query를 쌓아 두다가 transaction.commit() 을 하는 순간 데이터베이스에 Query 전송
- `변경 감지`(Dirty Checking)
  - transaction.commit() 시점에 엔티티와 스냅샷(처음 읽어 온 엔티티 상태) 비교 후 변경이 감지되면 Update Query 를 쓰기 지연 SQL 저장소에 저장
  - 이후 DB에 Query 전송 및 Commit
- 지연 로딩(Lazy Loading)

.

**`Flush`**

**영속성 컨텍스트의 변경내용을 데이터베이스에 반영하는 역할**

발생 시점

- 변경 감지
- 쓰기 지연 SQL 저장소의 쿼리를 데이터베이스에 전송 (CUD Query)

호출 방법

- 직접 호출 : em.flush()
- 자동 호출 : 트랜잭션 커밋, JPQL 쿼리 실행

# 엔티티 매핑

**`객체와 테이블`**

객체와 테이블 매핑
- `@Entity`: JPA가 관리하는 클래스 (기본 생성자 필수)
- `@Table`: 엔티티와 매핑할 테이블 지정

필드와 컬럼 매핑
- `@Column`

기본 키 매핑
- `@Id`

연관관계 매핑
- `@ManyToOne`
- `@JoinColumn`

.

**`데이터베이스 스키마 자동 생성`**

@Entity가 있는 클래스 DDL을 애플리케이션 실행 시점에 자동 생성 (개발 환경에서만 사용)

```xml
<property name="hibernate.hbm2ddl.auto" value="create" />
```

- `create`: 기존테이블 삭제 후 다시 생성 (DROP + CREATE)
- `create-drop`: create와 같으나 종료시점에 테이블 DROP
- `update`: 변경분만 반영(운영DB에는 사용하면 안됨)
- `validate` 엔티티와 테이블이 정상 매핑되었는지만 확인
- `none`: 사용하지 않음

**주의**

- 운영 장비에는 절대 create, create-drop, update 사용하면 안됨.

  - 개발 초기 단계는 create 또는 update

  - 테스트 서버는 update 또는 validate

  - 스테이징과 운영 서버는 validate 또는 none

.

**`필드와 컬럼`**

```java
@Entity
public class Member {

    @Id
    private Long id;

    /**
     * @Column : 컬럼 매핑
     * - name : 필드와 매핑할 테이블 컬럼명 (default. 객체 필드명)
     * - insertable : 등록 가능 여부 (default. TRUE)
     * - updatable : 수정 가능 여부 (default. TRUE)
     *
     * 아래는 DDL 조건
     * - nullable : null 허용 여부 (default. TRUE)
     * - unique : 유니크 제약 조건, 제약조건명이 랜덤키로 생성되어 주로 사용하지는 않음 (default. FALSE)
     * - columnDefinition : 데이터베이스 컬럼 정보 직접 설정 (ex. varchar(100) default ‘EMPTY')
     * - length : 문자(String) 길이 제약조건 (default. 255)
     *
     * BigDecimal, BigInteger 타입에 사용
     * - precision : 소수점을 포함한 전체 자릿수 (default. 19)
     * - scale : 소수 자릿수 (default. 2)
     */
    @Column(name = "name")
    private String username;

    private Integer age;

    /**
     * @Enumerated : enum 타입 매핑
     * 주의. ORDINAL 사용 X! (enum 순서를 저장)
     */
    @Enumerated(EnumType.STRING)
    private RoleType roleType;

    /**
     * @Temporal : 날짜 타입 매핑
     * DATE, TIME, TIMESTAMP
     * (LocalDate, LocalDateTime 사용할 시 생략)
     */
    @Temporal(TemporalType.TIMESTAMP)
    private Date createdDate;
    @Temporal(TemporalType.TIMESTAMP)
    private Date lastModifiedDate;

    /**
     * @Lob : BLOB, CLOB 매핑
     * 매핑 필드 타입이 문자면 CLOB, 나머지는 BLOB으로 매핑
     * - CLOB: String, char[], java.sql.CLOB
     * • BLOB: byte[], java.sql. BLOB
     */
    @Lob
    private String description;

    /**
     * @Transient : 해당 필드를 컬럼에 매핑하지 않음
     * 메모리상에서만 임시로 데이터를 보관할 경우 사용
     */
    @Transient
    private String temp;
}
```
.

**`기본 키`**

- `@Id` : 직접 할당할 경우
- `@GeneratedValue` : 자동 생성할 경우
  - **AUTO** : 방언에 따라 자동 지정 (default)
  - **IDENTITY** : 데이터베이스에 위임 (MYSQL)
    - 주로 MySQL, PostgreSQL, SQL Server, DB2 에서 사용
    - 참고) **DB INSERT Query 실행 후에 ID 값을 알 수 있으므로, *em.persist() 시점에 즉시 INSERT Query 실행 및 DB 식별자 조회***
  - **SEQUENCE** : 데이터베이스 시퀀스 오브젝트 사용 (ORACLE, @SequenceGenerator)
    - 주로 오라클, PostgreSQL, DB2, H2 에서 사용
  - **TABLE** : 키 생성용 테이블 사용, (모든 DB, @TableGenerator)

Long Type + 대체키 + 키 생성전략 사용 권장

**AUTO & IDENTITY**

```java
@Id
@GeneratedValue(strategy = GenerationType.AUTO)
private Long id;
```

**SEQUENCE**

`allocationSize`
- 시퀀스를 한 번 호출할 때 증가하는 수 (성능 최적화에 사용, default. 50)
  - 웹 서버를 내리는 시점에 메모리에 저장되어있던 시퀀스들이 날라가서 구멍이 생기므로, 50~100이 적절
  - DB 시퀀스 값이 하나씩 증가하도록 설정되어 있다면, 이 값을 반드시 1로 설정
- ex) 초기 1 ~ 51 까지 조회, 이후 시퀀스는 DB에서 조회하지 않고 메모리상에서 조회
  - 메모리에서 시퀀스 51을 만나는 순간 다시 DB에서 조회(next call)
- 미리 시퀀스 값을 올려두므로 동시성 문제가 되지 않음
- 이 부분은 Table 전략도 유사

```java
@Entity
@SequenceGenerator(
        name = "MEMBER_SEQ_GENERATOR", //생성 이름
        sequenceName = "MEMBER_SEQ", //매핑할 데이터베이스 시퀀스 이름
        initialValue = 1, allocationSize = 1)
public class Member {
  @Id
  @GeneratedValue(strategy = GenerationType.SEQUENCE,
          generator = "MEMBER_SEQ_GENERATOR")
  private Long id;
}
 ```

# 연관관계 매핑

*JPA는 객체의 참조와 테이블의 외래 키를 매핑*

## 방향(Direction)

- 단방향
  ```java
  @Entity
  public class Member {
      @Id @GeneratedValue
      private Long id;

      @Column(name = "USERNAME")
      private String name;

      @ManyToOne
      @JoinColumn(name = "TEAM_ID")
      private Team team;
  }

  //...
  //단방향 연관관계 설정 (참조 저장)
  Team team = new Team();
  team.setName("TeamA");
  em.persist(team);

  Member member = new Member();
  member.setName("member1");
  member.setTeam(team);

  em.persist(member);
  ```
- 양방향

  - 객체의 양방향 관계는 사실 서로 다른 단뱡향 관계 2개라는 사실.
    - 객체를 양방향으로 참조하려면 단방향 연관관계를 2개 만들어야 함
  - 테이블은 외래 키 하나로 두 테이블의 연관관계를 관리

  ```java
  @Entity
  public class Member {
      @Id @GeneratedValue
      private Long id;

      @ManyToOne
      @JoinColumn(name = "TEAM_ID")
      private Team team;
  }

  @Entity
  public class Team {
      @Id @GeneratedValue
      private Long id;
       
      @OneToMany(mappedBy = "team")
      List<Member> members = new ArrayList<Member>();
  }
  ```

## 연관관계의 주인(Owner)

외래키를 관리하는 참조

**양방향 매핑 규칙**

- 관계를 갖는 두 객체 중 하나의 객체를 연관관계의 주인으로 지정
  - 연관관계의 주인만이 외래 키를 관리(등록, 수정)하고, 주인이 아닌 쪽은 조회만 가능
  - 주인이 아닌 객체의 필드에 mappedBy 속성으로 주인 필드를 지정
- 연관관계의 주인은 **다(`N`:1)에 해당하는 객체**쪽이 갖도록(외래키를 갖는 테이블 기준)
  - 연관관계의 주인에 값 설정하기
    ```java
    Team team = new Team();
    team.setName("TeamA");
    em.persist(team);

    Member member = new Member();
    member.setName("member1");
    //연관관계의 주인에 값 설정
    member.setTeam(team);
    //순수 객체 상태를 고려해서 항상 양쪽에 값 설정하기
    team.getMembers().add(member);
    em.persist(member);
    ```
  - 연관관계 편의 메소드를 생성하는 것이 편리
    ```java
    @Entity
    public class Member {
      //..

      public void changeTeam(Team team) {
        this.tema = team;
        team.getMembers().add(this);
      }
    }

    // OR (두 객체 중 한 객체를 선택)

    @Entity
    public class Team {
      //...

      public void addMember(Member member) {
        member.setTeam(this);
        members.add(member);
      }
    }
    ```
- 양방향 매핑시에 무한 루프로 인한 StackOverflow 조심하기
  - toString(), lombok, JSON 생성 라이브러리(=> Controller DTO 반환으로 해결)

> 단방향 매핑만으로도 연관관계 매핑은 완료된 상태.
> 
> 추후 역방향 탐색이 필요할 경우에 추가하기!(테이블에 영향 X)

## 다중성(Multiplicity)

- 다대일(N:1) - @ManyToOne
  - 테이블 외래키 기준으로 연관된 참조를 설정(연관관계의 주인)
- 일대다(1:N) - @OneToMany
  - 반대 객체에도 방향 설정 추가(조회만 가능)
- 일대일(1:1) - @OneToOne
- 다대다(N:M) - @ManyToMany


