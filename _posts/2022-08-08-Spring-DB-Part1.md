---
layout: post
title: 데이터 접근 핵심 원리
summary: Spring DB Part 1. 데이터 접근 핵심 원리
categories: (Inflearn)Spring-DB-Part-1
featured-img: spring-db-part-1
# mathjax: true
---

# Spring DB Part 1. 데이터 접근 핵심 원리

영한님의 [스프링 DB 1편 - 데이터 접근 핵심 원리](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-db-1/) 강의 노트

[Project](https://github.com/jihunparkme/Inflearn-Spring-DB)

## H2 데이터베이스 설정

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

## 등록

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

## 조회

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

## 수정, 삭제

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

# ConnectionPool & DataSource

**데이터베이스 커넥션 획득 과정**

- 서버에서 DB 드라이버를 통해 커넥션 조회
- DB 드라이버는 DB와 TCP/IP 커넥션 연결 (3 way handshake 동작 발생)
- TCP/IP 커넥션이 연결되면, ID/PW와 기타 부가정보를 DB에 전달
- DB는 ID/PW를 통해 내부 인증을 완료하고, 내부 DB 세션 생성
- DB는 커넥션 생성이 완료되었다는 응답 전달
- DB 드라이버는 커넥션 객체를 생성해서 클라이언트에 반환

## ConnectionPool

커넥션을 관리하는 수영장(!) 

- 데이터베이스 커넥션을 매번 새로 만드는 과정에서 발생하는 응답 속도 저하 문제를 해결하기 위해 **커넥션을 미리 생성해두고 사용**

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

# Transaction

# Transaction Problem

# Java Excaption

# Spring Problem