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

# ConnectionPool & DataSource

# Transaction

# Transaction Problem

# Java Excaption

# Spring Problem