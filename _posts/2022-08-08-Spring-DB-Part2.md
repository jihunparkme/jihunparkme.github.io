---
layout: post
title: 데이터 접근 활용 기술
summary: Spring DB Part 2. 데이터 접근 활용 기술
categories: (Inflearn)Spring-DB-Part-2
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

**기본 적용**

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/cda214cbc34892473c3a20600284f54ddf106377)

[Memory to JdbcTemplate](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/8af0157ca827a31bd215e7ca8f3e3093ab7a177d)

## NamedParameterJdbcTemplate

**이름 지정 파라미터**

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

**INSERT SQL을 직접 작성하지 않아도 되도록 편의기능 제공**

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