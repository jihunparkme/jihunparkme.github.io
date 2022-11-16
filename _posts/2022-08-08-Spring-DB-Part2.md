---
layout: post
title: 데이터 접근 활용 기술
summary: Spring DB Part 2. 데이터 접근 활용 기술
categories: Spring-DB 데이터-접근-기술 Transaction
featured-img: spring-db-part-2
# mathjax: true
---

영한님의 [스프링 DB 2편 - 데이터 접근 활용 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-db-2) 강의 노트

[Project](https://github.com/jihunparkme/Inflearn-Spring-DB)

---

# Init

**프로젝트 구조**

[project settings](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/fcbab133e9dd4d2fcfc86fe0b9aad156d68d857b)

> [Profiles](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.profiles)

**테스트 코드**

인터페이스를 테스트하자

- 기본적으로 인터페이스를 대상으로 테스트하면 구현체가 변경되었을 때 같은 테스트로 해당 구현체가 잘 동작하는지 검증 가능

**식별자 선택 전략**

- 데이터베이스 기본키가 만족해야하는 조건
  - null 값은 허용하지 않는다.
  - 유일해야 한다.
  - 변해선 안 된다.

- 테이블의 기본키를 선택하는 두 가지 전략
  - `자연키(natural key)`
    - 비즈니스에 의미가 있는 키 (ex. 주민등록번호, 이메일, 전화번호)
  - `대리키, 대체키(surrogate key)`
    - 비즈니스와 관련 없는 임의로 만들어진 키 (ex, 오라클 시퀀스, auto_increment, identity, 키생성 테이블 사용)

- `자연키보다는 대리키 권장`
  - 기본키의 조건을 만족하려면 대리키가 일반적으로 좋은 선택
  - 비즈니스 환경은 언젠가 변한다..

# Spring JdbcTemplate

간단하고 실용적인 방법

**장점**
- 설정이 편리
  - spring-boot-starter-jdbc 라이브러리만 추가하고 별도의 추가 설정은 불필요
- 반복 문제 해결
  - 템플릿 콜백 패턴이 대부분의 반복 작업을 대신 처리
  - SQL 작성, 파리미터 정의, 응답 값 매핑만 필요
  - 대신 처리해주는 반복 작업
    - 커넥션 획득
    - statement 준비/실행
    - 결과 반복 루프 실행
    - 커넥션/statement/resultset 종료
    - 트랜잭션을 다루기 위한 커넥션 동기화
    - 예외 발생시 스프링 예외 변환기 실행...

**단점**
- 동적 쿼리 작성의 어려움(개발자가 직접 작성해 주어야 함..)

## JdbcTemplate

**순서 기반 파라미터 바인딩**

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/cda214cbc34892473c3a20600284f54ddf106377)

[Memory to JdbcTemplate](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/8af0157ca827a31bd215e7ca8f3e3093ab7a177d)

## NamedParameterJdbcTemplate

**이름 기반 파라미터 바인딩**

- 바인딩으로 인한 문제를 줄이기 위해 NamedParameterJdbcTemplate는 SQL에서 `?` 대신 `:parameterName` 을 사용
- 코드를 줄이는 것도 중요하지만, 모호함을 제거해서 코드를 명확하게 만드는 것이 유지보수 관점에서 매우 중요

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/af14a0761fc26287e70c4a25e6646f2a8cc7144f)

**SqlParameterSource**

BeanPropertySqlParameterSource
- 자동으로 파라미터 객체를 생성
- getXXX()를 활용해 자동 생성

```java
String sql = "insert into item (item_name, price, quantity) " +
                "values (:itemName, :price, :quantity)";

SqlParameterSource param = new BeanPropertySqlParameterSource(item);
KeyHolder keyHolder = new GeneratedKeyHolder();
template.update(sql, param, keyHolder);
```

MapSqlParameterSource
- SQL에 더 특화된 기능 제공

```java
String sql = "update item " +
        "set item_name=:itemName, price=:price, quantity=:quantity " +
        "where id=:id";

SqlParameterSource param = new MapSqlParameterSource()
        .addValue("itemName", updateParam.getItemName())
        .addValue("price", updateParam.getPrice())
        .addValue("quantity", updateParam.getQuantity())
        .addValue("id", itemId); // 별도로 필요
```

**Map**

```java
String sql = "select id, item_name, price, quantity from item where id = :id ";

Map<String, Object> param = Map.of("id", id);
Item item = template.queryForObject(sql, param, itemRowMapper());
```

**BeanPropertyRowMapper**

- ResultSet 결과를 받아서 자바빈 규약에 맞춰 데이터 변환
- 언더스코어 표기법을 카멜로 자동 변환

```java
BeanPropertyRowMapper<Item> rowMapper = BeanPropertyRowMapper.newInstance(Item.class);
```

## SimpleJdbcInsert

**INSERT SQL을 편의기능 제공**

생성 시점에 데이터베이스 테이블의 메타 데이터를 조회해서 테이블에 어떤 컬럼이 있는지 확인

- `withTableName` : 데이터를 저장할 테이블명 지정
- `usingGeneratedKeyColumns` : key를 생성하는 PK 컬럼명 지정
- `usingColumns` : INSERT SQL에 사용할 컬럼 지정(생량 가능)
  - 특정 컬럼만 지정해서 저장하고 싶을 경우 사용

```java
private final NamedParameterJdbcTemplate template;
private final SimpleJdbcInsert jdbcInsert;

public JdbcTemplateItemRepositoryV3(DataSource dataSource) {
    this.template = new NamedParameterJdbcTemplate(dataSource);
    this.jdbcInsert = new SimpleJdbcInsert(dataSource)
            .withTableName("item")
            .usingGeneratedKeyColumns("id");
            .usingColumns("item_name", "price", "quantity");
}

@Override
public Item save(Item item) {
    SqlParameterSource param = new BeanPropertySqlParameterSource(item);
    Number key = jdbcInsert.executeAndReturnKey(param);
    item.setId(key.longValue());
    return item;
}
```

## SimpleJdbcCall

**스토어드 프로시저를 편리하게 호출**

[Calling a Stored Procedure with SimpleJdbcCall](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#jdbc-simple-jdbc-call-1)

## Using JdbcTemplate

[Using JdbcTemplate](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#jdbc-JdbcTemplate)

**조회**

단건: `.queryForObject`, 목록: `.query`

- 단건 조회 (숫자)
```java
int rowCount = jdbcTemplate.queryForObject("select count(*) from t_actor", Integer.class);
```

- 단건 조회 (숫자 조회, 파라미터 바인딩)
```java
int countOfActorsNamedJoe = jdbcTemplate.queryForObject("select count(*) from t_actor where first_name = ?", Integer.class, "Joe");
```

- 단건 조회 (문자 조회)
```java
String lastName = jdbcTemplate.queryForObject("select last_name from t_actor where id = ?", String.class, 1212L);
```

- 단건 조회 (객체 조회)
```java
Actor actor = jdbcTemplate.queryForObject(
			"select first_name, last_name from t_actor where id = ?",
			(resultSet, rowNum) -> { // 결과 객체 매핑을 위해 RowMapper 사용
				Actor newActor = new Actor();
				newActor.setFirstName(resultSet.getString("first_name"));
				newActor.setLastName(resultSet.getString("last_name"));
				return newActor;
			},
			1212L);
```

- 목록 조회 (객체)
```java
List<Actor> actors = jdbcTemplate.query(
			"select first_name, last_name from t_actor",
			(resultSet, rowNum) -> {
				Actor actor = new Actor();
				actor.setFirstName(resultSet.getString("first_name"));
				actor.setLastName(resultSet.getString("last_name"));
				return actor;
			});
```

**변경(INSERT, UPDATE, DELETE)**

`.update()`, (반환값 int는 SQL 실행 결과에 영향받은 로우 수)

- 등록
```java
jdbcTemplate.update(
			"insert into t_actor (first_name, last_name) values (?, ?)",
			"Leonor", "Watling");
```

- 수정
```java
jdbcTemplate.update(
			"update t_actor set last_name = ? where id = ?",
			"Banjo", 5276L);
```

- 삭제
```java
jdbcTemplate.update(
			"delete from t_actor where id = ?",
			Long.valueOf(actorId));
```

**기타 기능**

- DDL
```java
jdbcTemplate.execute("create table mytable (id integer, name varchar(100))");
```

- 스토어드 프로시저 호출
```java
jdbcTemplate.update(
		"call SUPPORT.REFRESH_ACTORS_SUMMARY(?)",
		Long.valueOf(unionId));
```

## 🌞 JDBC TEST

`@SpringBootTest`는 `@SpringBootApplication`을 찾고 해당 설정을 사용

**데이터베이스 분리**
```text
DB 생성: jdbc:h2:~/testcase 
DB 접속: jdbc:h2:tcp://localhost/~/testcase
```

**테스트의 중요한 원칙**

- 테스트는 다른 테스트와 격리해야 한다.
- 테스트는 반복해서 실행할 수 있어야 한다

**데이터 롤백**

- 트랜잭션 관리자는 `PlatformTransactionManager`를 주입 받아서 사용
  - 스프링 부트는 적절한 트랜잭션 매니저를 스프링 빈으로 자동 등록
- `@BeforeEach`: 각의 테스트 케이스 실행 직전에 호출(트랜잭션 시작 위치)
  - transactionManager.getTransaction(new DefaultTransactionDefinition())
- `@AfterEach`: 각의 테스트 케이스 완료 직후에 호출(트랜잭션 롤백 위치)
  - transactionManager.rollback(status)

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/3318aa0cb576182582ac97168b49933efa5bd5c0)

🌞 **@Transactionanl**

- Spring @Transactional은 로직이 성공적으로 수행되면 커밋이 동작하지만
- 테스트에서 사용하면 테스트를 트랜잭션 안에서 실행하고, 테스트가 끝나면 트랜잭션을 자동으로 롤백
- 강제로 커밋을 하고 싶을 경우에는, `@Commit` 또는 `@Rollback(value = false)`를 같이 사용

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/ad3d94159de2b779016bca1141724df3ff7e45c3)

🌞 **Embedded mode DB**

- H2 데이터베이스는 JVM 안에서 메모리 모드로 동작하는 기능을 제공
  - DB를 애플리케이션에 내장해서 함께 실행
  - Spring Boot는 데이터베이스에 대한 설정이 없으면 **임베디드 데이터베이스를 기본으로 사용** ([commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/a856db143eb8df789e48dc9b7ec4e1f19701a78f))
- dataSource.setUrl("jdbc:h2:mem:db;DB_CLOSE_DELAY=-1");
  - `jdbc:h2:mem:db`: 임베디드(메모리) 모드로 동작하는 H2 데이터베이스 사용
  - `DB_CLOSE_DELAY=-1`: 임베디드 모드에서 데이터베이스 커넥션 연결이 모두 끊어지면
데이터베이스도 종료되는 현상을 방지
  - [commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/fbe9c0ec69ab5c3d7b1b135ebce304f4179c4f2f)

> [Initialize a Database Using Basic SQL Scripts](https://docs.spring.io/spring-boot/docs/current/reference/html/howto.html#howto.data-initialization.using-basic-sql-scripts)
> 
> [Embedded Database Support](https://docs.spring.io/spring-boot/docs/current/reference/html/data.html#data.sql.datasource.embedded)


# MyBatis

- 기본적으로 JdbcTemplate이 제공하는 대부분 기능 제공
- SQL을 XML에 작성하고 동적 쿼리를 편리하게 작성할 수 있는 장점
- 동적 쿼리와 복잡한 쿼리가 많다면 `MyBatis`, 단순한 쿼리가 많으면 `JdbcTemplate` 선택

> [Mybatis](https://mybatis.org/mybatis-3/ko/index.html)

## 설정

`mybatis.type-aliases-package`
- 타입 정보 사용 시 패키지 이름 생략을 위한 설정 (지정한 패키지와 그 하위 패키지가 자동으로 인식)
  - 여러 위치 지정 시 `,`, `;` 로 구분

`mybatis.configuration.map-underscore-to-camel-case`
- JdbcTemplate#BeanPropertyRowMapper처럼 언더바를 카멜로 자동 변경해주는 기능 활성화

`logging.level.hello.itemservice.repository.mybatis=trace`
- MyBatis에서 실행되는 쿼리 로그 확인을 위한 설정

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/d99d40f4f091f0a6e0c60e96df6e60b8aa735d35)

## 적용

- XML 파일 경로를 지정할 경우
  - resources/mapper 를 포함한 그 하위 폴더에 있는 XML
  - `application.properties`
    ```gradle
    mybatis.mapper-locations=classpath:mapper/**/*.xml
    ```
- INSERT `<insert>`
  - `id`: Mapper Class에 설정한 메서드 이름 지정
  - `파라미터`:  #{} 문법을 사용하고 매퍼에서 넘긴 객체의 프로퍼티 이름을 기입
  - `#{}` : PreparedStatement 를 사용(like. JDBC ? 치환)
  - `useGeneratedKeys`: 데이터베이스가 키를 생성해 주는 IDENTITY 전략일 때 사용
  - `keyProperty`: 생성되는 키의 속성 이름 지정
- UPDATE `<update>`
  - 파라미터가 한 개만 있으면 `@Param`을 지정하지 않아도 되지만, 두 개 이상이면 `@Param`으로 이름을 지정해서 파라미터 구분
- SELECT `<select>`
  - `resultType`: 반환 타입 명시(결과를 객체에 매핑) -> 결과를 객체로 바로 변환
  - 반환 객체가 하나이면 Item, Optional<Item> 사용, 하나 이상이면 컬렉션 사용
- 동적 쿼리
  - `<if>`: 해당 조건이 만족하면 구문을 추가
  - `<where>`: 적절하게 where 문장 생성
- 특수문자
  ```xml
  < : &lt;
  > : &gt;
  & : &amp;

  and price <![CDATA[<=]]> #{maxPrice}  
  ```
  
[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/f8d293fd5d6c099d2884f41ae6b4546bc1522e83)

## 실행

- ItemRepository 를 구현한 `MyBatisItemRepository` 생성
  - 단순히 ItemMapper 에 기능을 위임

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/1f5f2d6ebd8e90508784d8f8d6b32004999382f6)

**Mapper Interface 의 동작**

1. 애플리케이션 로딩 시점에 MyBatis 스프링 연동 모듈은 **@Mapper가 붙은 인터페이스를 탐색**
2. 해당 인터페이스가 발견되면 동적 프록시 기술을 사용해서 **Mapper Interface의 구현체 생성**(class `com.sun.proxy.$Proxy66`)
3. 생성된 구현체를 **스프링 빈으로 등록**

**MyBatis 스프링 연동 모듈**

- 인터페이스만으로 XML 데이터를 찾아서 호출 (Mapper 구현체 사용)
- Mapper 구현체는 스프링 예외 추상화도 함께 적용
  - MyBatis에서 발생한 예외를 DataAccessException(스프링 예외 추상화)에 맞게 변환
- JdbcTemplate의 기본적인 설정들은 모두 자동으로 설정 (데이터베이스 커넥션, 트랜잭션 관련 기능 등..)

> MyBatis 스프링 연동 모듈이 자동으로 등록해주는 부분은 `MybatisAutoConfiguration` class 참고

## 기능

> [MyBatis](https://mybatis.org/mybatis-3/ko/index.html)
> 
> [MyBatis-Spring](https://mybatis.org/spring/ko/index.html)

**if**

```xml
 <select id="findActiveBlogWithTitleLike" resultType="Blog">
    SELECT * FROM BLOG
    WHERE state = ‘ACTIVE’
    <if test="title != null">
        AND title like #{title}
    </if>
</select>
```

**choose (when, otherwise)**

```xml
<select id="findActiveBlogLike" resultType="Blog">
    SELECT * FROM BLOG WHERE state = ‘ACTIVE’
    <choose>
        <when test="title != null">
            AND title like #{title}
        </when>
        <when test="author != null and author.name != null">
            AND author_name like #{author.name}
        </when>
        <otherwise>
            AND featured = 1
        </otherwise>
    </choose>
</select>
```

**trim (where, set)**

```xml
<select id="findActiveBlogLike" resultType="Blog">
    SELECT * FROM BLOG
    <where>
        <if test="state != null">
            state = #{state}
        </if>
        <if test="title != null">
            AND title like #{title}
        </if>
        <if test="author != null and author.name != null">
            AND author_name like #{author.name}
        </if>
    </where>
</select>
```

- `<where>`는 문장이 있으면 `where`를 추가 (만약 and가 먼저 시작된다면 and를 제거)

**foreach**

```xml
<select id="selectPostIn" resultType="domain.blog.Post">
    SELECT *
    FROM POST P
    <where>
        <foreach item="item" index="index" collection="list"
                  open="ID in (" separator="," close=")" nullable="true">
            #{item}
        </foreach>
    </where>
</select>
```

> [MyBatis 동적 SQL](https://mybatis.org/mybatis-3/ko/dynamic-sql.html)
> 
> [MyBatis Annotation SQL](https://mybatis.org/mybatis-3/ko/java-api.html)

**재사용을 위한 SQL 조각**

```xml
<sql id="userColumns"> ${alias}.id,${alias}.username,${alias}.password </sql>

<select id="selectUsers" resultType="map">
    select
    <include refid="userColumns"><property name="alias" value="t1"/></include>,
    <include refid="userColumns"><property name="alias" value="t2"/></include>
    from some_table t1
    cross join some_table t2
</select>
```

**Result Maps**

- 컬럼명과 객체 프로퍼티명이 다를 경우 유용

```xml
<resultMap id="userResultMap" type="User">
    <id property="id" column="user_id" />
    <result property="username" column="username"/>
    <result property="password" column="password"/>
</resultMap>
<select id="selectUsers" resultMap="userResultMap">
    select user_id, user_name, hashed_password
    from some_table
    where id = #{id}
</select>
```

> [Result Maps](https://mybatis.org/mybatis-3/ko/sqlmap-xml.html#Result_Maps)

# JPA

**SQL 중심적인 개발의 문제점**

- SQL에 의존적인 개발
  - CRUD 코드의 반복
  - 필드 수정 시 많은 양의 SQL 수정이 필요 
- 객체와 관계형 데이터베이스간의 패러다임 불일치
  - 객체 <-> SQL 매핑 작업에 많은 노력이 필요
- 계층분할의 어려움
  - 처음 실행하는 SQL에 따라 탐색 범위 결정
  - 객체 그래프 탐색에서 엔티티 신뢰 문제

**JPA(Java Persistence API)**

- 자바 진영의 ORM(Object-relational mapping) 기술 표준
- 애플리케이션과 JDBC 사이에서 동작
- 장점
  - 객체 중심 개발(생산성, 유지보수)
    - 상속, 연관관계
  - 패러다임의 불일치 해결
    - 객체 그래프 탐색
  - 성능 최적화 기능
    - 1차 캐시와 동일성 보장
    - 쓰기 지연(insert query 모으기)
    - 지연 로딩(객체 실제 사용 시 로딩)
  - 데이터 접근 추상화 독립성
  - 표준

[JPA INTRO](https://jihunparkme.github.io/JPA-Programming-base/)

## 설정

**application.properties**

- `org.hibernate.SQL=DEBUG` : hibernate가 생성하고 실행하는 SQL 확인
- `org.hibernate.type.descriptor.sql.BasicBinder=TRACE` : SQL에 바인딩 되는 파라미터 확인

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/80892c5dd1b2a62ff2a2d564f3a46c626520d077)

## 개발

- JPA에서 가장 중요한 부분은 객체와 테이블을 매핑하는 것

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/5c7c08ed7b01c462043d9949dc7391c2d8ecb58c)

## 예외

- EntityManager는 예외가 발생하면 JPA 관련 예외를 발생
  - `@Repository`를 통해 스프링이 예외 변환을 처리하는 AOP 생성
- JPA는 `PersistenceException` 과 그 하위 예외를 발생
  - 추가로 `IllegalStateException` , `IllegalArgumentException` 발생

**@Repository의 기능**

- 컴포넌트 스캔의 대상 + 예외 변환 AOP 적용 대상
- 스프링 + JPA 사용 시 스프링은 JPA 예외 변환기(PersistenceExceptionTranslator) 등록
- 예외 변환 AOP Proxy는 JPA 관련 예외가 발생하면 JPA 예외 변환기를 통해 발생한 예외를 스프링
데이터 접근 예외로 변환 (PersistenceException -> DataAccessException)
- 실제 JPA 예외를 변환하는 코드: 
`EntityManagerFactoryUtils#convertJpaAccessExceptionIfPossible()`

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/repository-annotation.png?raw=true 'Result')

# Spring Data JPA

JPA를 편리하게 사용할 수 있도록 도와주는 라이브러리

대표적인 기능
- 공통 인터페이스 기능
- 쿼리 메서드 기능

참고
- Spring Data JPA가 Repository 구현 클래스(Proxy)를 자동으로 생성하고 스프링 빈으로 등록
- 스프링 예외 추상화 지원 (Spring Data JPA가 만들어주는 Proxy에서 예외 변환을 처리)
  
**적용**

```gradle
implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
```

- JPA, hibernate, Spring Data JPA, Spring JDBC 기능이 모두 포함

**Spring Data**

- Repository interface

```java
@Indexed
public interface Repository<T, ID> {
}
```

- CrudRepository interface

```java
@NoRepositoryBean
public interface CrudRepository<T, ID> extends Repository<T, ID> {
	<S extends T> S save(S entity);
	<S extends T> Iterable<S> saveAll(Iterable<S> entities);
	Optional<T> findById(ID id);
	boolean existsById(ID id);
	Iterable<T> findAll();
	Iterable<T> findAllById(Iterable<ID> ids);
	long count();
	void deleteById(ID id);
	void delete(T entity);
	void deleteAllById(Iterable<? extends ID> ids);
	void deleteAll(Iterable<? extends T> entities);
	void deleteAll();
}
```

- PagingAndSortingRepository interface

```java
@NoRepositoryBean
public interface PagingAndSortingRepository<T, ID> extends CrudRepository<T, ID> {
	Iterable<T> findAll(Sort sort);
	Page<T> findAll(Pageable pageable);
}
```
**Spring Data JPA**

- JpaRepository interface
  - 기본적인 CRUD 기능 제공

```java
@NoRepositoryBean
public interface JpaRepository<T, ID> extends PagingAndSortingRepository<T, ID>, QueryByExampleExecutor<T> {

	@Override
	List<T> findAll();

	@Override
	List<T> findAll(Sort sort);

	@Override
	List<T> findAllById(Iterable<ID> ids);

	@Override
	<S extends T> List<S> saveAll(Iterable<S> entities);
  
  void flush();

	<S extends T> S saveAndFlush(S entity);

	<S extends T> List<S> saveAllAndFlush(Iterable<S> entities);

	void deleteAllInBatch(Iterable<T> entities);

	void deleteAllByIdInBatch(Iterable<ID> ids);

	void deleteAllInBatch();

	T getOne(ID id);

	T getById(ID id);

	@Override
	<S extends T> List<S> findAll(Example<S> example);

	@Override
	<S extends T> List<S> findAll(Example<S> example, Sort sort);
}
```

**Using JpaRepository example**

```java
public interface SpringDataJpaItemRepository extends JpaRepository<Item, Long> {

    List<Item> findByItemNameLike(String itemName);

    List<Item> findByPriceLessThanEqual(Integer price);

    // Query Method (아래 메서드와 같은 기능 수행)
    List<Item> findByItemNameLikeAndPriceLessThanEqual(String itemName, Integer price);

    // JPQL
    @Query("select i from Item i where i.itemName like :itemName and i.price <=:price")
    List<Item> findItems(@Param("itemName") String itemName, @Param("price") Integer price);
}
```

> [Spring Data](https://spring.io/projects/spring-data)
> 
> [Query Creation](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.query-methods.query-creation)
> 
> [Limiting Query Results](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories.limit-query-result)

# QueryDSL

**기존 방식의 문제점**

- 일반 쿼리는 문자이므로 Type-check가 불가능하고, 실행 전까지는 작동 여부 확인 불가
- 쿼리를 Java로 type-safe하게 개발할 수 있도록 지원하는 프레임워크가 QueryDSL -> 주로 JPQL에 사용

**해결**

- **DSL(DomainSpecificLanguage)** : 특정 도메인에 특화되어 제한적인 표현력을 가진 프로그래밍 언어
- **QueryDSL(QueryDomainSpecificLanguage)** : 쿼리에 특화된 프로그래밍 언어
  - JPA, MongoDB, SQL 같은 기술들을 위해 type-safe SQL을 만드는 프레임워크
  - type-safe, 단순, 쉬운 장점
  - Q코드 생성을 위한 APT(Annotation Processing Tool) 설정이 필요

## 설정

Build Tool에 따른 QClass 생성 방법

- Gradle : Gradle을 통해 빌드
  - Gradle IntelliJ
    - Gradle -> Tasks -> build -> clean
    - Gradle -> Tasks -> other -> compileJava
  - Gradle Console
    - `./gradlew clean compileJava`
  - build/generated/sources/annotationProcessor 하위에 생성
- IntelliJ IDEA : IntelliJ가 직접 자바를 실행해서 빌드
  - Build Project / Start
  - src/main/generated 하위에 생성

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/6bd2802887abe667304be95f03ced1333bf48766)

## 적용

- Querydsl 사용을 위해 JPAQueryFactory 필요
  - JPAQueryFactory 는 JPA 쿼리인 JPQL을 만들기 위해 EntityManager 필요
- JdbcTemplate 설정과 유사

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/2c739a4b50e9b908d9291757a37109bd8d91a119)

# 활용 방안

**구조의 안정성 vs 단순한 구조와 개발의 편리성**

- Trade Off
  - DI, OCP 를 지키기 위해 어댑터를 도입하고, 더 많은 코드를 유지
  - 어댑터 제거로 구조가 단순해 지지만, DI, OCP를 포기하고, Service 코드를 직접 변경
- 다만, 상황에 따라서 **구조의 안정성**이 중요할 수도 있고, **단순함**이 더 나은 선택일 수 있다. 
  - 추상화 비용을 넘어설 만큼 효과가 있을 경우 추상화 도입이 실용적
  - 상황에 맞는 선택이 중요
  - 먼저, 간단하고 빠르게 해결할 수 있는 방법을 선택하고, 이후 리펙토링을 추천

**실용적인 구조**

- SpringDataJPA와 QueryDSL Repository를 분리해서 기본 CRUD와 단순 조회는 SpringDataJPA 담당, 복잡한 조회 쿼리는 Querydsl 담당

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/a4f987a8f7e7f723ede6f6d9a1371bd0ce0cd72b)

**데이터 접근 기술 조합**

- JPA, SpringDataJPA, Querydsl 을 기본으로 사용하고, 복잡한 쿼리를 사용할 경우, 해당 부분에는 JdbcTemplate 이나 MyBatis 를 함께 사용
- 트랜잭션 매너지의 경우 `JpaTransactionManager` 하나만 스프링 빈에 등록하면, JPA, JdbcTemplate, MyBatis 를 하나의 트랜잭션으로 묶어서 사용 가능
- JPA, JdbcTemplate을 함께 사용할 경우 JPA의 플러시 타이밍이 다르다면 변경한 데이터를 읽지 못할 수 있음
  - JPA는 기본적으로 트랜잭션이 커밋되는 시점에 변경 사항을 데이터베이스에 반영
  - JPA 호출이 끝난 시점에 플러시를 사용하고, JdbcTemplate 를 호출하여 해결 가능

# Spring Transaction

- Spring Transaction 추상화
  - `PlatformTransactionManager` 인터페이스를 통해 트랜잭션 추상화
  - 데이터 접근 기술마다 모두 다른 트랜잭션 처리 방식을 추상화

```java
package org.springframework.transaction;

public interface PlatformTransactionManager extends TransactionManager {

	TransactionStatus getTransaction(@Nullable TransactionDefinition definition) throws TransactionException;

	void commit(TransactionStatus status) throws TransactionException;

	void rollback(TransactionStatus status) throws TransactionException;
}
```

- Spring은 Transaction을 추상화해서 제공하고, 데이터 접근 기술에 대한 TransactionManager의 구현체도 제공
  - 사용자는 필요한 구현체를 Spring Bean으로 등록하고, 주입 받아서 사용
- Spring Boot는 어떤 데이터 접근 기술을 사용하는지를 자동으로 인식해서 적절한 TransactionManager 선택 및 스프링 빈으로 등록 (선택, 등록 과정 생략)
  - JdbcTemplate, MyBatis 사용 시 `DataSourceTransactionManager(JdbcTransactionManager)`를 스프링 빈으로 등록
  - JPA 사용 시 `JpaTransactionManager`을 스프링 빈으로 등록

**사용 방식**

선언적 트랜잭션 관리 vs 프로그래밍 방식 트랜잭션 관리

**`선언적 트랜잭션 관리`(Declarative Transaction Management)**

- `@Transactional` 하나만 선언하여 편리하게 트랜잭션을 적용(과거에는 XML에 설정)
- 이름 그대로 "해당 로직에 트랜잭션을 적용하겠다."라고 선언하면 트랜잭션이 적용되는 방식
- 기본적으로 프록시 방식의 AOP 적용
- 트랜잭션을 처리하는 객체와 비즈니스 로직을 처리하는 서비스 객체를 명확하게 분리

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/transaction-aop.png?raw=true 'Result')

- 트랜잭션은 커넥션에 `setAutocommit(false)` 지정으로 시작
- 같은 데이터베이스 커넥션을 사용하여 같은 트랜잭션을 유지하기 위해 스프링 내부에서는 트랜잭션 동기화 매니저를 사용
- JdbcTemplate을 포함한 대부분의 데이터 접근 기술들은 트랜잭션을 유지하기 위해 내부에서 트랜잭션 동기화 매니저를 통해 리소스(커넥션)를 동기화

[참고](https://jihunparkme.github.io/Spring-DB-Part1/#%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98-aop-%EB%8F%99%EC%9E%91-%ED%9D%90%EB%A6%84)

**`프로그래밍 방식의 트랜잭션 관리`(programmatic transaction management)**

- TransactionManager 또는 TransactionTemplate 등을 사용해서 트랜잭션 관련 코드를 직접 작성
- 프로그래밍 방식의 트랜잭션 관리를 사용하게 되면, 애플리케이션 코드가 트랜잭션이라는 기술 코드와 강하게 결합되는 단점
- 선언적 트랜잭션 관리가 훨씬 간편하고 실용적이기 때문에 실무에서는 대부분 선언적 트랜잭션 관리를 사용

## 적용

AOP 적용 방식에 따라서 인터페이스에 @Transactional 선언 시 AOP가 적용이 되지 않는 경우도 있으므로, 가급적 구체 클래스에 @Transactional 사용 권장

- Transaction 적용 확인

```java
TransactionSynchronizationManager.isActualTransactionActive();

TransactionSynchronizationManager.isCurrentTransactionReadOnly();
```

- 트랜잭션 프록시가 호출하는 트랜잭션 로그 확인을 위한 설정

```properties
logging.level.org.springframework.transaction.interceptor=TRACE
```

```console
Getting transaction for [hello.springtx.apply...BasicService.tx]

.. 실제 메서드 호출

.. 트랜젝션 로직 커밋 또는 롤백

Completing transaction for [hello.springtx.apply...BasicService.tx]
 
```

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/8abd275c39be2090caf854ac3c82066fe8470b9d/post_img/spring/spring-container-proxy.png?raw=true 'Result')

- @Transactional 이 특정 클래스나 메서드에 있다면, Transaction AOP는 프록시를 만들어서 스프링 컨테이너에 등록 -> 실제 객체 대신 프록시를 스프링 빈에 등록되고 프록시는 내부에 실제 객체를 참조
- 프록시는 객체를 상속해서 만들어지기 때문에 다형성을 활용

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/f6640a9085f7bd7349a036dce6c8a310a39c93ba)

**적용 위치**

- 스프링에서 **우선순위**는 항상 더 구체적이고 자세한 것이 높은 우선순위를 가짐.
- 클래스에 적용하면 메서드는 자동 적용

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/be15be175c0c2abb838762a7f14794d78700a7eb)

## 주의사항

- @Transactional을 선언하면 `스프링 트랜잭션 AOP` 적용
  - 트랜잭션 AOP는 기본적으로 `프록시 방식의 AOP` 사용
- 스프링은 대상 객체 대신 프록시를 스프링 빈으로 등록하므로 프록시 객체가 요청을 먼저 받고, 프록시 객체에서 트랜잭션 처리와 실제 객체 호출
- 따라서, 트랜잭션을 적용하려면 항상 프록시를 통해서 대상 객체를 호출해야 함
- ⭐️ **만약, 프록시를 거치지 않고 대상 객체를 직접 호출하게 되면 AOP가 적용되지 않고, 트랜잭션도 적용되지 않는다.**
  - **대상 객체의 내부에서 메서드 호출이 발생하면 프록시를 거치지 않고 대상 객체를 직접 호출하는 문제가 발생**


**프록시 호출**

```java
@Transactional
public void internal() {
    log.info("call internal");
}
```

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-transaction-internal.png?raw=true 'Result')

1. 클라이언트가 service.internal()을 호출하면 service의 트랜잭션 프록시 호출
2. internal() 메서드에 @Transactional이 선언되어 있으므로 트랜잭션 프록시는 트랜잭션을 적용
3. 트랜잭션 적용 후 실제 service 객체 인스턴스의 internal() 호출
4. 실제 service가 처리 완료되면 응답이 트랜잭션 프록시로 돌아오고, 트랜잭션 프록시는
트랜잭션을 완료

**대상 객체 직접 호출**

```java
public void external() {
    log.info("call external");
    internal();
}

@Transactional
public void internal() {
    log.info("call internal");
}
```

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-transaction-external.png?raw=true 'Result')


1. 클라이언트가 service.external()을 호출하면 service의 트랜잭션 프록시 호출
2. external() 메서드에는 @Transactional이 없으므로 트랜잭션 프록시는 트랜잭션을 적용하지 않고, 실제 service 객체 인스턴스의 external() 호출
3. external()은 내부에서 (this.)internal() 직접 호출
4. 내부 호출은 프록시를 거치지 않으므로 트랜잭션 적용이 불가능

**@Transactional을 사용하는 트랜잭션 AOP는 프록시를 사용하면서 메서드 내부 호출에 프록시를 적용할 수 없다.**
- 가장 단순한 방법으로 내부 호출을 외부 호출로 변경하기 위해 internal()를 별도 클래스로 분리하기

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/0c65a2c8df7e2e89d935dfe85489997adac0c72f)

**대상 객체 외부 호출**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-transaction-external-class.png?raw=true 'Result')

1. 클라이언트가 service.external()을 호출하면 실제 service 객체 인스턴스 호출
2. service는 주입 받은 internalService.internal() 호출
3. internalService는 트랜잭션 프록시이므로(@Transactional) 트랜잭션 적용
4. 트랜잭션 적용 후 실제 internalService 객체 인스턴스의 internal() 호출

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/11cc4418af0d0b396e2ea0fdf43a0777d78cf50a)

> 참고
> 
> 스프링 트랜잭션 AOP 기능은 과도한 트랜잭션 적용을 막기 위해 public 메서드에만 적용되도록 기본 설정
> 
> public 이 아닌곳에 @Transactional 이 붙으면 트랜잭션 적용 무시

**초기화 시점**

- 초기화 코드(ex.@PostConstruct)와 @Transactional을 함께 사용하면 트랜잭션 적용 불가
  - 초기화 코드가 먼저 호출되고 이후 트랜잭션 AOP가 적용되기 때문

```java
@PostConstruct
@Transactional
public void initV1() {
    boolean isActive = TransactionSynchronizationManager.isActualTransactionActive();
    log.info("Hello init @PostConstruct tx active={}", isActive); // false
}
```

- 대안으로 `@ApplicationReadyEvent` 사용
  - ApplicationReadyEvent는 트랜잭션 AOP를 포함한 스프링 컨테이너가 완전히 생성된 이후 이벤트가 선언된 메서드 호출

```java
@EventListener(value = ApplicationReadyEvent.class)
@Transactional
public void init2() {
    boolean isActive = TransactionSynchronizationManager.isActualTransactionActive();
    log.info("Hello init ApplicationReadyEvent tx active={}", isActive); // true
}
```

[comomit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/d9b2790c8eaa0e2fbd08b8f42a63942d57e8934e)

## 옵션

- `String value()` default "";
- `String transactionManager()` default "";
  - @Transactional 에서 트랜잭션 프록시가 사용할 트랜잭션 매니저 지정
  - 생략 시 기본으로 등록된 트랜잭션 매니저 사용
  - 사용 트랜잭션 매니저가 둘 이상이라면, 트랜잭션 매니저 이름을 지정해서 구분
```java
@Transactional("memberTxManager")
@Transactional("orderTxManager")
```

- `Class<? extends Throwable>[] rollbackFor()` default {};
  - 특정 예외 발생 시 롤백을 하도록 지정
  - Exception(체크 예외)이 발생해도 롤백하도록 설정 가능

```java
@Transactional(rollbackFor = Exception.class)
```

- `Class<? extends Throwable>[] noRollbackFor()` default {};
  - rollbackFor 와 반대로 특정 예외 발생 시 롤백을 하지 않도록 지정

- `Propagation propagation()` default Propagation.REQUIRED;
  - 트랜잭션 전파 옵션

- `Isolation isolation()` default Isolation.DEFAULT;
  - 트랜잭션 격리 수준 지정
  - 기본값은 데이터베이스 설정 기준(DEFAULT)
  - 트랜잭션 격리 수준을 직접 지정하는 경우는 드묾 [(참고)](https://data-make.tistory.com/738#isolation)
    - **DEFAULT** : 데이터베이스에서 설정한 격리 수준을 따른다.
    - **READ_UNCOMMITTED** : 커밋되지 않은 읽기
    - **READ_COMMITTED** : 커밋된 읽기
    - **REPEATABLE_READ** : 반복 가능한 읽기
    - **SERIALIZABLE** : 직렬화 가능

- `int timeout()` default TransactionDefinition.TIMEOUT_DEFAULT;
  - 트랜잭션 수행 시간에 대한 타임아웃을 초 단위로 지정
  - 기본 값은 트랜잭션 시스템의 타임아웃

- `String[] label()` default {};
  - 트랜잭션 애노테이션에 있는 값을 읽어서 특정 동작을 할 경우 사용
  - 일반적으로 사용하지 않음

- `boolean readOnly()` default false;
  - readOnly=true 옵션 사용 시 읽기 전용 트랜잭션 생성
    - 드라이버나 데이터베이스에 따라 정상 동작하지 않는 경우도 있음.
  - 읽기에서 다양한 성능 최적화
  - 크게 세 곳에서 적용
    - 프레임워크
      - JdbcTemplate: 읽기 전용 트랜잭션 안에서 변경 기능을 실행하면 예외
      - JPA: 읽기 전용 트랜잭션의 경우 커밋 시점에 플러시를 호출하지 않고, 변경이 불필요하니 변경 감지를 위한 스냅샷 객체도 생성하지 않음
    - JDBC 드라이버
      - 읽기 전용 트랜잭션에서 변경 쿼리가 발생하면 예외
      - 읽기, 쓰기(master, slave) 데이터베이스를 구분해서 요청
      - DB / 드라이버 버전에 따라 다르게 동작
      - [참고](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-source-replicareplication-connection.html)
    - 데이터베이스
      - 읽기 전용 트랜잭션의 경우 읽기만 하면 되므로, 내부에서 성능 최적화 발생

## 예외와 롤백

내부에서 예외를 처리하지 못하고 트랜잭션 범위(@Transactional 적용 AOP) 밖으로 예외를 던질 경우 -> 스프링 트랜잭션 AOP는 예외의 종류에 따라 트랜잭션을 커밋하거나 롤백
- 언체크 예외(RuntimeException, Error, 그 하위 예외) 발생 시 트랜잭션 `롤백`
- 체크 예외(Exception, 그 하위 예외) 발생 시 트랜잭션 `커밋`
- 정상 응답(리턴) 시 트랜잭션을 `커밋`

**참고**

트랜잭션 커밋/롤백 로그 확인을 위한 설정

```gradle
# 사용중인 TransactionManager
logging.level.org.springframework.jdbc.datasource.DataSourceTransactionManager=DEBUG
logging.level.org.springframework.orm.jpa.JpaTransactionManager=DEBUG #JPA log
logging.level.org.hibernate.resource.transaction=DEBUG
```

- 트랜잭션 생성 로그(Creating new transaction with name)와 트랜잭션 커밋/롤백 로그(Committing JPA transaction on EntityManager) 확인

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/63ec1863dfc6beb3eb16a817dcc4b2eee1a72e18)

스프링 기본적으로 예외를 아래 정책에 따름
- 체크 예외 / Commit : 비즈니스 예외 (ex. 잔고 부족 ..)
  - 비즈니스 예외는 반드시 처리해야 하는 경우가 많으므로 중요하고, 체크 예외를 고려할 수 있음.
  - rollbackFor 옵션을 사용해서 비즈니스 상황에 따라 롤백 선택 가능
- 언체크 예외 / Rollback : 복구 불가능한 예외 (ex. DB 접근 오류, SQL 문법 오류 ..)

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/3270d88b3dd48afd5cf491e64f2262138f9428fa)

# 트랜잭션 전파

Spring Transaction Propagation commit and rollback
- [commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/ba863a50af0d57adc837c3f485214d19b6a7afad)

Spring Transaction Propagation Use transaction twice

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-transaction-connection.png?raw=true 'Result')

- 로그를 보면 트랜잭션1,2가 같은 conn0 커넥션을 사용중인데, 이것은 커넥션 풀 때문에 그런 것
- 트랜잭션1은 conn0을 모두 사용 후 커넥션 풀에 반납하고, 이후 트랜잭션2가 conn0을 커넥션 풀에서 획득
- 히카리 커넥션 풀에서 커넥션을 획득하면 실제 커넥션을 그대로 반환하는 것이 아니라 내부 관리를 위해
히카리 프록시 커넥션 객체를 생성해서 반환하는데, 이 객체의 주소를 확인하면 커넥션 풀에서 획득한 커넥션 구분이 가능
  - HikariProxyConnection@2120431435 wrapping conn0: ...
  - HikariProxyConnection@1567077043 wrapping conn0: ...
  - 커넥션이 재사용 되었지만, 각각 커넥션 풀에서 커넥션을 조회
- [commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/b2c4067730a00a0d32b84932cd7e1ca4cb989789)

## 기본

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-transaction-propagation.png?raw=true 'Result')

- 트랜잭션이 진행중인 상태에서 내부에 추가로 트랜잭션을 사용하는 경우, 스프링은 외부/내부 트랜잭션을 묶어서 하나의 트랜잭션을 생성
  - 트랜잭션 전파의 기본 옵션인 `REQUIRED` 기준
  - 내부 트랜잭션은 외부 트랜잭션에 참여(외/내부 트랜잭션이 하나의 물리 트랜잭션으로 묶임)
  - 옵션을 통해 다른 동작방식 선택 가능
- 논리 트랜잭션들은 하나의 물리 트랜잭션으로 묶임
  - `물리 트랜잭션`: 실제 데이터베이스에 적용되는 트랜잭션(시작, 커밋, 롤백 단위)
  - `논리 트랜잭션`: 트랜잭션 매니저를 통해 트랜잭션을 사용하는 단위
- 모든 트랜잭션 매니저가 커밋되어야 물리 트랜잭션이 커밋
  - 하나의 트랜잭션 매니저라도 롤백되면 물리 트랜잭션은 롤백
- 외부 트랜잭션만 물리 트랜잭션 시작/커밋
  - 처음 시작 트랜잭션이 실제 물리 트랜잭션을 관리

원칙

- 모든 `논리 트랜잭션`이 커밋되어야 `물리 트랜잭션`이 커밋
- 하나의 `논리 트랜잭션`이라도 롤백되면 `물리 트랜잭션`은 롤백

## 흐름

**`요청 흐름`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-transaction-request.png?raw=true 'Result')

**외부 트랜잭션**

\1. txManager.getTransaction() 호출로 외부 트랜잭션 시작

\2. 트랜잭션 매니저는 데이터소스를 통해 커넥션 생성

\3. 생성 커넥션을 수동 커밋 모드로 설정(물리 트랜잭션 시작)

\4. 트랜잭션 매니저는 트랜잭션 동기화 매니저에 커넥션을 보관

\5. 트랜잭션 매니저는 트랜잭션을 생성한 결과를 TransactionStatus에 담아서 반환 
- isNewTransaction로 신규 트랜잭션 여부 확인, true

\6. 로직1이 실행되고 커넥션이 필요한 경우 트랜잭션 동기화 매니저를 통해 트랜잭션이 적용된 커넥션 획득 후 사용

**내부 트랜잭션**

\7. txManager.getTransaction() 호출로 내부 트랜잭션 시작

\8. 트랜잭션 매너저는 트랜잭션 동기화 매니저를 통해 기존 트랜잭션 존재 확인

\9. 기존 트랜잭션이 존재하므로 기존 트랜잭션에 참여
- 물리적으로 아무 행동을 하지 않고, 트랜잭션 동기화 매니저에 보관된 기존 커넥션 사용

\10. isNewTransaction = false

\11. 로직2가 실행되고, 커넥션이 필요한 경우 트랜잭션 동기화 매니저를 통해 외부 트랜잭션이 보관한 기존 커넥션 획득 후 사용

**`응답 흐름`**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-transaction-response.png?raw=true 'Result')

**내부 트랜잭션**

\12. 로직2가 끝나고 트랜잭션 매니저를 통해 내부 트랜잭션 커밋

\13. 트랜잭션 매니저는 커밋 시점에 신규 트랜잭션 여부에 따라 다르게 동작 
   - 여기서는 신규 트랜잭션이 아니므로 실제 물리 커밋 호출을 하지 않음
   - 아직 물리 트랜잭션이 끝나지 않음

**외부 트랜잭션**

\14. 로직1이 끝나고 트랜잭션 매니저를 통해 외부 트랜잭션 커밋

\15. 트랜잭션 매니저는 커밋 시점에 신규 트랜잭션 여부에 따라 다르게 동작
- 외부 트랜잭션은 신규 트랜잭션이므로 데이터베이스 커넥션에 실제 커밋 호출

\16. 실제 데이터베이스에 커밋이 반영되고, 물리 트랜잭션도 끝.
- 논리적인 커밋: 트랜잭션 매니저에 커밋하는 것이 논리적인 커밋이라면, 
- 물리 커밋: 실제 커넥션에 커밋

**`흐름 핵심`**

- 트랜잭션 매니저에 커밋을 한다고 항상 실제 커넥션에 물리 커밋이 발생하지 않음
- 신규 트랜잭션인 경우에만 실제 커넥션을 사용해서 물리 커밋/롤백 수행

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/5ba85ccc8cf8eb5d4f65511730eb4fd7880c22b2)

**`외/내부 트랜잭션 롤백`**

**외부 롤백**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-transaction-outer-rollback.png?raw=true 'Result')

- 외부 트랜잭션에서 시작한 물리 트랜잭션의 범위가 내부 트랜잭션까지 사용
- 이후 외부 트랜잭션이 롤백되면서 전체 내용은 모두 롤백

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/a6c3f612dabb5186eed01df128f653f0508bd308)

**내부 롤백**

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-transaction-inner-rollback.png?raw=true 'Result')

- 내부 트랜잭션을 롤백하면 실제 물리 트랜잭션이 롤백되지는 않고, 기존 트랜잭션에 롤백
전용 마크 표시
  - `Participating transaction failed - marking existing transaction as rollbackonly`
- 이후 외부 트랜잭션이 커밋을 호출했지만, 전체 트랜잭션이 롤백 전용으로 표시되어 물리 트랜잭션 롤백 -> UnexpectedRollbackException
  - `Global transaction is marked as rollback-only`

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/d020250574754937b772641fa9b18795bf655dc8)

**`외부 트랜잭션과 내부 트랜잭션 분리`**

- REQUIRES_NEW 옵션 사용
- 외부/내부 트랜잭션이 각각 별도의 물리 트랜잭션(별도의 DB connection 사용)을 가짐
- 각 트랜잭션의 롤백이 서로에게 영향을 주지 않음
- 요청 흐름
  ![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-transaction-requires-new-request.png?raw=true 'Result')
- 응답 흐름
  ![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/spring-transaction-requires-new-response.png?raw=true 'Result')
  
[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/d80d6f0ebcc168670333c451d914bbbadc29afbf)

## 전파 옵션

실무에서 대부분 `REQUIRED` 옵션 사용, 아주 가끔 `REQUIRES_NEW` 사용
- 나머지는 거의 사용하지 않으니 참고만..

**REQUIRED**
- 가장 많이 사용하는 기본 설정(트랜잭션 필수)
- 기존 트랜잭션 X: 새로운 트랜잭션 생성
- 기존 트랜잭션 O: 기존 트랜잭션에 참여

**REQUIRES_NEW**
- 항상 새로운 트랜잭션 생성
- 기존 트랜잭션 X: 새로운 트랜잭션 생성
- 기존 트랜잭션 O: 새로운 트랜잭션 생성

**SUPPORT**
- 트랜잭션 지원
- 기존 트랜잭션 X: 트랜잭션 없이 진행
- 기존 트랜잭션 O: 기존 트랜잭션 참여

**NOT_SUPPORT**
- 트랜잭션 지원을 하지 않음
- 기존 트랜잭션 X: 트랜잭션 없이 진행
- 기존 트랜잭션 O: 트랜잭션 없이 진행(기존 트랜잭션은 보류)

**MANDATORY**
- 트랜잭션이 반드시 있어야 함
- 기존 트랜잭션 X: IllegalTransactionStateException 예외 발생
- 기존 트랜잭션 O: 기존 트랜잭션 참여

**NEVER**
- 트랜잭션을 사용하지 않음
- 기존 트랜잭션 X: 트랜잭션 없이 진행
- 기존 트랜잭션 O: IllegalTransactionStateException 예외 발생

**NESTED**
- 기존 트랜잭션 X: 새로운 트랜잭션 생성
- 기존 트랜잭션 O: 중첩 트랜잭션 생성
- 중첩 트랜잭션은 외부 트랜잭션의 영향을 받지만, 중첩 트랜잭션은 외부에 영향을 주지 않음

`isolation`, `timeout`, `readOnly` 는 트랜잭션 처음 시작 시에만 적용(참여하는
경우에는 적용되지 않음)

## 활용

- 예제 프로젝트 : [commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/2f765e3ff2122aba19fdf2fcb4ef15d6f145e6bc)
- 커밋과 롤백 : [commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/804ca810caa5fd486ef5251f98af3bab3e2ba95a)