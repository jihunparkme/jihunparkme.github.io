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

## Init

**프로젝트 구조**

[project settings](https://github.com/jihunparkme/Inflearn-Spring-DB/commit/fcbab133e9dd4d2fcfc86fe0b9aad156d68d857b)

> [Profiles](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.profiles)

**테스트 코드**

인터페이스를 테스트하자

- 기본적으로 인터페이스를 대상으로 테스트하면 구현체가 변경되었을 때 같은 테스트로 해당 구현체가 잘 동작하는지 검증 가능