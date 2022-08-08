---
layout: post
title: 데이터 접근 핵심 원리
summary: Spring DB Part 1. 데이터 접근 핵심 원리
categories: (Inflearn)Spring-DB-1
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