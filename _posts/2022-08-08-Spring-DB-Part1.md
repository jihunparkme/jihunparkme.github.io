---
layout: post
title: 데이터 접근 핵심 원리
summary: Spring DB Part 1. 데이터 접근 핵심 원리
categories: (Inflearn)Spring-DB-Part-1
featured-img: spring-db-part-1
# mathjax: true
---

영한님의 [스프링 DB 1편 - 데이터 접근 핵심 원리](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-db-1/) 강의 노트

[Project](https://github.com/jihunparkme/Inflearn-Spring-DB)

---

**`H2 데이터베이스 설정`**

**Download**

- [H2](https://www.h2database.com/)
- [download-archive](https://www.h2database.com/html/download-archive.html)

**실행**

- 실행 권한: `chmod 755 h2.sh`
- 실행: `./h2.sh`
- mv.db 파일 생성: `jdbc:h2:~/test`
- 접속: `jdbc:h2:tcp://localhost/~/test`

# JDBC

**Java Database Connectivity**

- 자바에서 데이터베이스에 접속하기 위해 사용되는 자바 API

**Server <-> DB**

- `Connection 연결`: 주로 TCP/IP를 사용해서 커넥션 연결
- `SQL 전달`: 서버는 DB가 이해할 수 있는 SQL을 커넥션으로 DB에 전달
- `Response`: DB는 전달된 SQL을 수행하고 그 결과를 응답 -> 서버는 응답 결과 활용

**JDBC 표준 인터페이스**

- `java.sql.Connection`: 연결
- `java.sql.Statement`: SQL을 담은 내용
- `java.sql.ResultSet`: SQL 요청 응답

**JDBC 데이터 접근 기술**

- SQL Mapper
  - Spring JdbcTemplate
  - MyBatis
- ORM
  - JPA
  - hibernate
  - eclipse link

**데이터베이스 연결**

- JDBC는 `java.sql.Connection` 표준 커넥션 인터페이스를 정의
  - H2 데이터베이스 드라이버는 JDBC Connection 인터페이스를 구현한 `org.h2.jdbc.JdbcConnection` 구현체 제공
- JDBC가 제공하는 `DriverManager` 는 라이브러리에 등록된 DB 드라이버들을 관리하고, 커넥션을 획득하는 기능 제공

.

DriverManager 커넥션 요청 흐름

- 애플리케이션 로직에서 커넥션이 필요하면 `DriverManager.getConnection()` 호출
- `DriverManager` 는 라이브러리에 등록된 드라이버 목록을 자동으로 인식
  - 드라이버들에게 순서대로 URL, d이름, 비밀번호 등 접속이 필요한 정보를 넘겨 커넥션을 획득할 수 있는지 확인
  - 각각의 드라이버는 URL 정보를 체크해서 본인이 처리할 수 있는 요청인지 확인
- 찾은 커넥션 구현체를 클라이언트에 반환
  - 처리가 가능한 드라이버의 경우 실제 데이터베이스에 연결해서 커넥션을 획득하고 이 커넥션을 클라이언트에 반환
  - 반면 URL이 jdbc:h2 로 시작했는데 MySQL 드라이버가 먼저 실행될 경우, 처리할 수 없다는 결과를 반환하게 되고, 다음 드라이버에게 순서가 전달

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/07ceef6ef29e47d9b2a0ffaefbeb397791d1281f)

---

**`getConnection() & close()`**

**DriverManager**

```java
@Slf4j
public class MemberRepository {
    private void close(Connection con, Statement stmt, ResultSet rs) {

        if (rs != null) {
            try {
                rs.close();
            } catch (SQLException e) {
                log.info("error", e);
            }
        }

        if (stmt != null) {
            try {
                stmt.close();
            } catch (SQLException e) {
                log.info("error", e);
            }
        }

        if (con != null) {
            try {
                con.close();
            } catch (SQLException e) {
                log.info("error", e);
            }
        }
    }

    private Connection getConnection() {
        return DBConnectionUtil.getConnection();
    }
}
```

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/b93bc90231003c3eaa0852d4fc6d073ca6f4b6eb)

**DataSource**

```java
@Slf4j
public class MemberRepository {

    private final DataSource dataSource;

    public MemberRepositoryV1(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    private void close(Connection con, Statement stmt, ResultSet rs) {
        JdbcUtils.closeResultSet(rs);
        JdbcUtils.closeStatement(stmt);
        JdbcUtils.closeConnection(con);
    }

    private Connection getConnection() throws SQLException {
        Connection con = dataSource.getConnection();
        log.info("get connection={}, class={}", con, con.getClass());
        return con;
    }
}
```

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/4a040f96418607642bad23b60bb505c68f2cbdfa)

---

**`등록`**

```java
@Slf4j
public class MemberRepository {

    public Member save(Member member) throws SQLException {
        String sql = "insert into member(member_id, money) values(?, ?)";

        Connection con = null;
        PreparedStatement pstmt = null;

        try {
            con = getConnection();
            pstmt = con.prepareStatement(sql); // 데이터베이스에 전달할 SQL과 파라미터로 전달할 데이터들을 준비
            pstmt.setString(1, member.getMemberId());
            pstmt.setInt(2, member.getMoney());
            pstmt.executeUpdate(); // 준비된 SQL을 커넥션을 통해 실제 데이터베이스로 전달
            return member;
        } catch (SQLException e) {
            log.error("db error", e);
            throw e;
        } finally {
            close(con, pstmt, null);
        }
    }
}
```

---

**`조회`**

```java
public Member findById(String memberId) throws SQLException {
    String sql = "select * from member where member_id = ?";

    Connection con = null;
    PreparedStatement pstmt = null;
    ResultSet rs = null;

    try {
        con = getConnection();
        pstmt = con.prepareStatement(sql);
        pstmt.setString(1, memberId);

        rs = pstmt.executeQuery();
        if (rs.next()) {
            Member member = new Member();
            member.setMemberId(rs.getString("member_id"));
            member.setMoney(rs.getInt("money"));
            return member;
        } else {
            throw new NoSuchElementException("member not found memberId=" + memberId);
        }
    } catch (SQLException e) {
        log.error("db error", e);
        throw e;
    } finally {
        close(con, pstmt, rs);
    }
}
```

---

**`수정, 삭제`**

```java
public void update(String memberId, int money) throws SQLException {
    String sql = "update member set money=? where member_id=?";

    Connection con = null;
    PreparedStatement pstmt = null;

    try {
        con = getConnection();
        pstmt = con.prepareStatement(sql);
        pstmt.setInt(1, money);
        pstmt.setString(2, memberId);
        int resultSize = pstmt.executeUpdate();
        log.info("resultSize={}", resultSize);
    } catch (SQLException e) {
        log.error("db error", e);
        throw e;
    } finally {
        close(con, pstmt, null);
    }
}

public void delete(String memberId) throws SQLException {
    String sql = "delete from member where member_id=?";

    Connection con = null;
    PreparedStatement pstmt = null;

    try {
        con = getConnection();
        pstmt = con.prepareStatement(sql);
        pstmt.setString(1, memberId);
        pstmt.executeUpdate();
    } catch (SQLException e) {
        log.error("db error", e);
        throw e;
    } finally {
        close(con, pstmt, null);
    }
}
```

# Connection Pool & DataSource

**데이터베이스 커넥션 획득 과정**

- 서버에서 DB 드라이버를 통해 커넥션 조회
- DB 드라이버는 DB와 TCP/IP 커넥션 연결 (3 way handshake 동작 발생)
- TCP/IP 커넥션이 연결되면, ID/PW와 기타 부가정보를 DB에 전달
- DB는 ID/PW를 통해 내부 인증을 완료하고, 내부 DB 세션 생성
- DB는 커넥션 생성이 완료되었다는 응답 전달
- DB 드라이버는 커넥션 객체를 생성해서 클라이언트에 반환

## ConnectionPool

커넥션을 관리하는 수영장(!) 

- DriverManager 를 통해 데이터베이스 커넥션을 매번 새로 생성하는 과정에서 발생하는 응답 속도 저하 문제를 해결하기 위해 **커넥션을 미리 생성해두고 사용**

**ConnectionPool 초기화**

- 애플리케이션 시작 시점에 필요한 만큼의 커넥션을 미리 확보해서 풀에 보관
  - 기본값은 보통 10개

**ConnectionPool 연결 상태**

- 커넥션 풀에 들어 있는 커넥션은 TCP/IP로 DB와 커넥션이 연결되어 있는 상태
  - 언제든지 SQL을 DB에 전달 가능

**ConnectionPool 사용**

- 커넥션 풀을 통해 이미 생성되어 있는 커넥션을 객체 참조로 얻어서 사용
- 커넥션을 요청하면 커넥션 풀은 자신이 가지고 있는 커넥션 중 하나를 반환
- 커넥션 풀로부터 받은 커넥션을 사용해서 SQL을 DB에 전달하고, 그 결과를 받아서 처리
- 커넥션을 모두 사용하면 커넥션을 종료하지 않고 다시 사용할 수 있도록 커넥션 풀에 반환

## DataSource

**커넥션을 획득하는 방법을 추상화 하는 인터페이스**

- 커넥션 풀 오픈소스 `commons-dbcp2`, `tomcat-jdbc pool`, `HikariCP`에 직접 의존하는 것이 아니라, DataSource 인터페이스에만 의존하면 된다!

### DriverManager

**DriverManager**

- 커넥션을 획득할 때 마다 URL/USERNAME/PASSWORD 를 파라미터로 계속 전달

**DataSourceDriverManager**

- 반면, 처음 객체를 생성할 때만 필요한 파리미터를 넘기고, 커넥션을 획득할 때는 단순히 dataSource.getConnection() 만 호출
- `설정`과 `사용`의 분리가 명확

```java
@Test
void driverManager() throws SQLException {
    Connection con1 = DriverManager.getConnection(URL, USERNAME, PASSWORD);
    Connection con2 = DriverManager.getConnection(URL, USERNAME, PASSWORD);
    log.info("connection={}, class={}", con1, con1.getClass());
    log.info("connection={}, class={}", con2, con2.getClass());
}

@Test
void dataSourceDriverManager() throws SQLException {
    DriverManagerDataSource dataSource = new DriverManagerDataSource(URL, USERNAME, PASSWORD);
    useDataSource(dataSource);
}

private void useDataSource(DataSource dataSource) throws SQLException {
    Connection con1 = dataSource.getConnection();
    Connection con2 = dataSource.getConnection();
    log.info("connection={}, class={}", con1, con1.getClass());
    log.info("connection={}, class={}", con2, con2.getClass());
}
```

### Connection Pool

- 커넥션 풀은 별도의 쓰레드 사용해서 커넥션 풀에 커넥션을 채운다.
- DriverManagerDataSource 는 항상 새로운 커넥션을 생성하는 반면, 커넥션 풀은 커넥션을 재사용

```java
@Test
void dataSourceConnectionPool() throws SQLException, InterruptedException {
    HikariDataSource dataSource = new HikariDataSource();
    dataSource.setJdbcUrl(URL);
    dataSource.setUsername(USERNAME);
    dataSource.setPassword(PASSWORD);
    dataSource.setMaximumPoolSize(10);
    dataSource.setPoolName("MyPool");
    
    useDataSource(dataSource);
    Thread.sleep(1000); // 커넥션 생성 시간 대기
}
```

> [HikariCP](https://github.com/brettwooldridge/HikariCP)

# Transaction

**DB에서 트랜잭션은 하나의 작업를 안전하게 처리하도록 보장**

- `커밋(Commit)` : 모든 작업이 성공해서 DB에 정상 반영하는 것
- `롤백(Rollback)` : 작업이 하나라도 실패해서 작업 이전으로 되돌리는 것

## 트랜잭션 ACID

트랜잭션은 원자성(Atomicity), 일관성(Consistency), 격리성(Isolation), 지속성(Durability)을 보장해야 한다.

- `원자성(Atomicity)` : 트랜잭션 내에서 실행한 작업들은 마치 하나의 작업인 것처럼 모두 성공 하거나 모두 실패해야 한다.
- `일관성(Consistency)` : 모든 트랜잭션은 일관성 있는 데이터베이스 상태를 유지해야 한다. 
-  데이터베이스에서 정한 무결성 제약 조건을 항상 만족해야 한다.
- `격리성(Isolation)` : 동시에 실행되는 트랜잭션들이 서로에게 영향을 미치지 않도록 격리한다. 
  - 동시에 같은 데이터를 수정하지 못하도록 해야 한다.
  - 트랜잭션 간에 격리성을 완벽히 보장하려면 트랜잭션을 거의 순서대로 실행해야 하므로 ANSI 표준은 트랜잭션의 격리 수준을 4단계로 나누어 정의
  - 격리성은 동시성과 관련된 성능 이슈로 인해 트랜잭션 격리 수준(Isolation level)을 선택할 수 있다.
    - **READ UNCOMMITED**(커밋되지 않은 읽기)
    - **READ COMMITTED**(커밋된 읽기)
    - **REPEATABLE READ**(반복 가능한 읽기)
    - **SERIALIZABLE**(직렬화 가능)
- `지속성(Durability)` : 트랜잭션을 성공적으로 끝내면 그 결과가 항상 기록되어야 한다.
  - 중간에 시스템에 문제가 발생해도 데이터베이스 로그 등을 사용해서 성공한 트랜잭션 내용을 복구해야 한다.

> [트랜잭션 ACID](http://en.wikipedia.org/wiki/ACID)
> 
> [@Transactional 잘 사용해보기](https://data-make.tistory.com/738)

**트랜잭션의 사용 예시**

- 데이터 변경 쿼리를 실행하고 데이터베이스에 결과를 반영하려면 commit 을 호출하고,
- 결과를 반영하고 싶지 않다면 rollback 을 호출
- 커밋을 호출하기 전까지는 임시로 데이터를 저장 -> 해당 트랜잭션을 시작

## 자동커밋과 수동커밋

**자동 커밋**

- 각각의 쿼리 실행 직후 자동으로 커밋 호출
- 커밋이나 롤백을 직접 호출하지 않아도 되는 편리함
- 하지만, 원하는 트랜잭션 기능을 제대로 사용할 수 없는 단점 존재

```sql
set autocommit true; -- default
```

**수동 커밋**

- 수동 커밋 모드로 설정하는 것이 **트랜잭션 시작**
- 이후 commit, rollback 호출 필요
- 수동/자동 커밋 모드는 한번 설정하면 해당 세션에서 계속 유지 (중간 변경도 가능)

```sql
set autocommit false;
-- ...
commit;
```

## Lock

- 세션이 트랜잭션을 시작하고 데이터를 수정하는 동안 커밋 or 롤백 전까지 다른 세션에서 해당 데이터를 수정할 수 없도록 락을 제공
- 다른 세션은 락을 획득할 때까지 대기
  - 락 대기 시간을 넘어가면 락 타임아웃 오류 발생(락 대기 시간을 설정 가능)

**Lock Timeout 시간 설정**

```sql
SET LOCK_TIMEOUT <milliseconds>
```

**Lock Timeout Error**

```text
Timeout trying to lock table {0}; SQL statement:
...
```

**조회와 락**

- 일반적인 조회는 락을 사용하지 않지만,
- 락을 획득해서 변경을 막고 싶다면, `select .. for update` 구문을 사용
  - 트랜잭션 종료 시점까지 해당 데이터를 다른 곳에서 변경하지 못하도록 강제로 막아야 할 경우 사용
  - 해당 세션이 조회 시점에 락을 가져가버리기 때문에 다른 세션에서 해당 데이터를 변경할 수 없다(트랜잭션 커밋 시 락 반납)

## 과거 트랜잭션 적용

- 트랜잭션은 서비스 계층에서부터 시작
  - 비즈니스 로직이 잘못되면 문제가 되는 부분을 함께 롤백해주어야 한다.
- 트랜잭션을 시작하려면 커넥션이 필요. `set autocommit false;`
- 같은 세션을 사용하기 위해 트랜잭션을 사용하는 동안 같은 커넥션을 유지해야 한다.
  - 가장 단순한 방법은 커넥션을 파라미터로 전달하는 방법
- 과거 서버에서의 트랜젝션 적용은 서비스 계층이 매우 지저분해지고 생각보다 매우 복잡한 코드를 요구..

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/a7c5b2dafc32c69e59263bff7f1e4821cba8f79f)

---

**기존 트랜잭션의 문제점**

- **[트랜잭션 문제](https://jihunparkme.github.io/Spring-DB-Part1/#transaction-problem)**
  - JDBC 구현 기술이 서비스 계층에 누수되는 문제
- **[예외 누수 문제](https://jihunparkme.github.io/Spring-DB-Part1/#java-excaption)**
  - 데이터 접근 계층의 JDBC 구현 기술 예외가 서비스 계층으로 전파
- **[JDBC 반복 문제]((https://jihunparkme.github.io/Spring-DB-Part1/#jdbc-repetitive-problem))**
  - try, catch, finally .. 유사한 코드의 반복

---

# Transaction Problem

## Spring Transaction Manager

**트랜잭션 추상화**

- `PlatformTransactionManager` interface
  - JdbcTransactionManager
  - JpaTransactionManager
  - HibernateTransactionManager
  - EtcTransactionManager

```java
public interface PlatformTransactionManager extends TransactionManager {

	TransactionStatus getTransaction(@Nullable TransactionDefinition definition) throws TransactionException;

	void commit(TransactionStatus status) throws TransactionException;

	void rollback(TransactionStatus status) throws TransactionException;
}
```

**리소스 동기화**

- 트랜잭션을 유지하기 위해 트랜잭션의 시작부터 끝까지 같은 데이터베이스 커넥션을 유지해야 한다.
  - 과거에는 파라미터로 커넥션을 전달했지만
  - 스프링은 `org.springframework.transaction.support.TransactionSynchronizationManager`를 통해 `ThreadLocal`로 커넥션을 동기화
    - `TransactionManager`는 내부에서 `TransactionSynchronizationManager`를 사용하고, `TransactionManager`를 통해 커넥션을 획득
    - `ThreadLocal`을 사용해서 멀티쓰레드 상황에 안전하게 커넥션을 동기화가 가능

.

- 동작 방식
  - 1.**TransactionManager는 dataSource를 통해 커넥션을 만들고** 트랜잭션 시작
  - 2.TransactionManager는 트랜잭션이 시작된 커넥션을 **TransactionSynchronizationManager에 보관**
  - 3.Repository는 **TransactionSynchronizationManager에 보관된 커넥션을 꺼내서** 사용
  - 4.트랜잭션이 종료되면 TransactionManager는 **TransactionSynchronizationManager에 보관된 커넥션을 통해** 트랜잭션을 종료하고, 커넥션도 닫음

## TransactionManager

트랜잭션 동기화를 사용하려면 DataSourceUtils를 사용

**DataSourceUtils.getConnection()**

```java
private Connection getConnection() throws SQLException {
    Connection con = DataSourceUtils.getConnection(dataSource);
    return con;
}
```

- TransactionSynchronizationManager가 관리하는 커넥션이 있으면 해당 커넥션을 반환
- 커넥션이 없는 경우 새로운 커넥션을 생성해서 반환

**DataSourceUtils.releaseConnection()**

```java
private void close(Connection con, Statement stmt, ResultSet rs) {
    //...
    DataSourceUtils.releaseConnection(con, dataSource);
}
```

- 트랜잭션을 사용하기 위해 동기화된 커넥션은 커넥션을 닫지 않고 그대로 유지
- TransactionSynchronizationManager가 관리하는 커넥션이 없는 경우 해당 커넥션을 닫음
- commit(status), rollback(status) 호출 시 알아서 release 수행

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/3e878dca32eaf1faecfbbf86272450d1d1174af2)

## Transaction Template

템플릿 콜백 패턴 적용을 위해 `TransactionTemplate` 템플릿 클래스 작성
- Transaction의 반복되는 try, catch, finally 코드 제거
- 단, 서비스 로직에 트랜잭션 처리 코드가 포함되어 있는 단점이 존재

```java
public class TransactionTemplate {
    private PlatformTransactionManager transactionManager;

    // 응답값이 있을 경우 사용
    public <T> T execute(TransactionCallback<T> action) {..}
    // 응답값이 없을 경우 사용
    void executeWithoutResult(Consumer<TransactionStatus> action) {..}
}
```

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/2f35347a20031d957e86c5af1281675344b12859)

## Transaction AOP

**TransactionalProxy 도입을 통해 트랜잭션 처리 객체와 비즈니스 로직 처리 서비스 객체를 명확하게 분리**

- `@Transactional`을 트랜잭션 처리가 필요한 곳에 추가해주면, 스프링의 트랜잭션 AOP가 트랜잭션이 적용된 프록시를 생성하고 자동으로 트랜잭션 처리
- `TransactionalProxy`를 도입하면 `@Transactional`이 붙어 있는 메서드나 클래스에 Spring이 해당 서비스 로직을 상속받아서 자동으로 트랜잭션 코드를 생성
  - `xxxService$$EnhancerBySpringCGLIB$$..`

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/dfef452d4a4570a7b8666deed961da7af7ff13cc)

## 트랜잭션 AOP 동작 흐름

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/transaction-aop.png?raw=true 'Result')

0. Transaction이 적용된 클래스/메서드 호출
1. Transaction이 적용된 `Spring AOP Proxy 호출`
2. Spring Container에 등록된 `Transaction Manager` 획득
3. `트랜잭션 시작`. transactionManager.getTransaction()
4. transactionManager는 내부에서 DataSource를 사용해 `커넥션 생성`
5. 커넥션을 `수동 커밋 모드로 변경`해서 실제 데이터베이스 트랜잭션 시작. setAutoCommit(false)
6. 커넥션을 `TransactionSynchronizationManager`에 보관
7. TransactionSynchronizationManager는 `ThreadLocal`에 커넥션을 보관
   - ThreadLocal: 멀티 쓰레드 환경에서도 안전하게 커넥션 보관
8. Spring AOP Proxy에서 실제 비즈니스 로직을 실행하면서 리포지토리의 `메서드들을 호출` (커넥션을 파라미터로 전달할 필요가 없어짐)
9. 리포지토리는 DataSourceUtils.getConnection()을 통해 `TransactionSynchronizationManager`에 보관된 `커넥션을 꺼내서 사용`
    - 같은 커넥션을 사용하고, 트랜잭션도 유지
10. 획득한 커넥션을 사용해서 `SQL`을 데이터베이스에 `전달 및 실행`
11. 비즈니스 로직이 끝나고 `트랜잭션을 종료`를 위해 `TransactionSynchronizationManager`를 통한 `동기화된 커넥션을 획득`
    - 획득한 커넥션을 통해 커밋/롤백 후 트랜잭션 종료
12. 전체 `리소스`(TransactionSynchronizationManager, ThreadLocal, setAutoCommit(true), con.close()..) `정리`

## SpringBoot 자동 리소스 등록

**기존에는 데이터소스와 트랜잭션 매니저를 XML로 등록하거나 직접 스프링 빈으로 등록해야 했지만, SpringBoot를 통해 많은 부분이 자동화**

### 자동 등록

**DataSource**

- `application.properties`에 있는 속성을 사용해서 DataSource를 생성하고 스프링 빈에 자동으로 등록
  - 직접 DataSource를 빈으로 등록하면 스프링 부트는 자동으로 등록하지
않음

```properties
spring.datasource.url=jdbc:h2:tcp://localhost/~/test
spring.datasource.username=sa
spring.datasource.password=
```

**TransactionManager**

- 스프링 부트는 적절한 트랜잭션 매니저(PlatformTransactionManager)를 자동으로 스프링 빈에 등록
  - 자동 등록 스프링 빈 이름: transactionManager
  - DataSource와 마찬가지로 직접 TransactionManager를 빈으로 등록하면 스프링 부트는 자동으로 등록하지 않음
- 자동으로 등록되는 트랜잭션 매니저는 현재 등록된 라이브러리를 보고 판단
  - JDBC: DataSourceTransactionManager
  - JPA: JpaTransactionManager 
  - JDBC + JPA: JpaTransactionManager

```java
@Slf4j
@SpringBootTest
class MemberServiceV3_4Test {

    @TestConfiguration
    static class TestConfig {

        private final DataSource dataSource;

        public TestConfig(DataSource dataSource) {
            this.dataSource = dataSource;
        }

        @Bean
        MemberRepositoryV3 memberRepositoryV3() {
            return new MemberRepositoryV3(dataSource);
        }

        @Bean
        MemberServiceV3_3 memberServiceV3_3() {
            return new MemberServiceV3_3(memberRepositoryV3());
        }
    }
}
```

- SpringBoot가 application.properties에 지정된 속성을 참고해서 데이터소스와 트랜잭션 매니저를 자동으로 생성
- 생성자를 통해 SpringBoot가 만들어준 데이터소스 빈을 주입 가능

### 직접 등록

```java
@TestConfiguration
static class TestConfig {
    @Bean
    DataSource dataSource() {
        return new DriverManagerDataSource(URL, USERNAME, PASSWORD);
    }

    @Bean
    PlatformTransactionManager transactionManager() {
        return new DataSourceTransactionManager(dataSource());
    }

    @Bean
    MemberRepositoryV3 memberRepositoryV3() {
        return new MemberRepositoryV3(dataSource());
    }

    @Bean
    MemberServiceV3_3 memberServiceV3_3() {
        return new MemberServiceV3_3(memberRepositoryV3());
    }
}
```

> [ Configure a DataSource](https://docs.spring.io/spring-boot/docs/current/reference/html/data.html#data.sql.datasource)
> 
> [Common Application Properties](https://docs.spring.io/spring-boot/docs/current/reference/html/application-properties.html)

# Java Excaption

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/java-exception.png?raw=true 'Result')

- `Object` : 모든 객체의 최상위 부모
- `Throwable` : 최상위 예외
  - 상위 예외를 잡으면 그 하위 예외(Error..)까지 함께 잡으므로, Throwable 예외는 잡지 말고, Exception부터 잡자.
- `Error` : 애플리케이션에서 복구 불가능한 시스템 예외 (메모리 부족이나 심각한 시스템 오류)
  - unchecked exception
- `Exception` : 애플리케이션 로직에서 사용할 수 있는 실질적인 최상위 예외
  - Exception과 그 하위 예외는 모두 컴파일러가 체크하는 checked exception
  - 컴파일러가 체크해 주기 때문에 잡거나 던지거나 하나를 필수로 선택
  - 단, RuntimeException은 예외
- `RuntimeException` : 컴파일러가 체크하지 않는 unchecked exception
  - RuntimeException과 그 자식 예외는 모두 unchecked exception

**예외의 기본 규칙**

- 예외는 잡아서 처리하거나 던져야 함.
- 예외를 잡거나 던질 때 지정한 예외뿐만 아니라 자식 예외들도 함께 처리

.

- 예외 잡기 `try-catch`
  - Repository 예외 발생 -> Service로 예외 throws -> Service에서 예외 처리 -> 이후 정상 흐름으로 동작
- 예외 던지기 `throws Exception`
  - Repository 예외 발생 -> Service로 예외 throws -> Controller로 예외 throws
  - 예외를 처리하지 못하고 계속 던지면 main() 쓰레드의 경우 예외 로그를 출력하면서 시스템이 종료되고, 웹 애플리케이션의 경우 WAS가 해당 예외를 받아서 처리하는데, 주로 사용자에게 지정한 오류 페이지를 전달

## Checked Exception

**컴파일러가 예외를 체크해주면, 잡아서 처리하거나, 밖으로 던지도록 선언**

예외를 잡아서 처리할 수 없을 경우에는 예외를 throws로 던져줘야 함.

- 장점: 실수로 예외를 누락하지 않도록 컴파일러를 통해 문제를 잡아주는 안전 장치
- 단점: 모든 체크 예외를 반드시 잡거나 던지도록 처리해야 하는 번거로움
  - 크게 신경쓰고 싶지 않은 예외까지 모두 챙겨야 하고, 의존관계에 따른 단점도 존재

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/e0376ce16d24366cc0cd90831eaa997f7683f948)

**`활용`**

\1. 기본적으로 Unchecked(Runtime) Exception를 사용하자.

- Checked Exception은 Service, Controller에서 처리할 수 없는 예외를 throws 선언으로 계속 던지다보면, `복구 불가능한 예외`, `의존 관계 문제` 발생
  - `복구 불가능한 예외`: 로그를 남기고 ServletFilter, SpringInterceptor, Spring ControllerAdvice를 통해 일관성있게 공통으로 처리하자. (실무의 대부분의 예외들은 복구 불가능한 시스템 예외)
  - `의존 관계 문제`: 처리할 수도 없는 SQLException에 의존하여 기술이 변경되면 의존 코드를 전부 고쳐주어야 하는 문제 발생(OCP, DI 위반). -> Exception을 던져서 문제를 해결할 수 있을 것 같지만, 모든 예외를 다 단지기 떄문에 체크 예외를 체크할 수 있는 기능이 무효화

\2. 체크 예외는 비즈니스 로직상 의도적으로 던지는 예외를 잡아서 반드시 처리해야 하는 경우에만 사용하자.

- 계좌 이체 실패 예외
- 결제시 포인트 부족 예외
- 로그인 ID, PW 불일치 예외

## Unchecked Exception

**컴파일러가 체크하지 않는 예외**

체크 예외와 언체크 예외는 기본적으로 동일하지만, 

- Checked Exception: 예외를 잡아서 처리하지 않으면 항상 throws 선언 필요
- Unchecked Exception: 예외를 잡아서 처리하지 않아도 throws 생략 가능

예외를 처리할 수 없을 때 예외를 밖으로 던지는데, throws를 필수로 선언해야 하는가 생략할 수 있는가의 차이가 큼

- 장점: 신경쓰고 싶지 않은 언체크 예외는 무시하고 throws 선언 생략 가능
- 단점: 컴파일러가 예외 누락을 잡아주지 않으므로, 실수로 예외를 누락할 수 있음

[commit](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/0124d2db88719152a47c8187bd928ba4ada69286)

**`활용`**

- CheckedException이 발생하면 RuntimeException으로 전환해서 예외를 던지자.
- 시스템에서 발생한 예외는 대부분 복구 불가능 예외이므로, Runtime Exception을 사용하면 서비스나 컨트롤러가 복구 불가능한 예외를 신경쓰지 않아도 되고 공통으로 처리할 수 있다.
- 해당 객체가 처리할 수 없는 예외는 무시하면 되므로, 예외를 강제로 의존하지 않아도 된다.
- RuntimeException은 놓칠 수 있기 때문에 문서화가 중요
  
JPA EntityManager

```java
/**
* Make an instance managed and persistent.
* @param entity entity instance
* @throws EntityExistsException if the entity already exists.
* @throws IllegalArgumentException if the instance is not an
* entity
* @throws TransactionRequiredException if there is no transaction when
* invoked on a container-managed entity manager of that is of type
* <code>PersistenceContextType.TRANSACTION</code>
*/
public void persist(Object entity);

```

JdbcTemplate

```java
/**
* Issue a single SQL execute, typically a DDL statement.
* @param sql static SQL to execute
* @throws DataAccessException if there is any problem
*/
void execute(String sql) throws DataAccessException;
```

# JDBC Repetitive Problem