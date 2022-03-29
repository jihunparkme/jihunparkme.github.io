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
      ```
  - `삭제` (removed)
    - **삭제**된 상태
      ```java
      entityManager.remove(member);
      ``` 

## 영속성 컨텍스트의 이점

- `1차 캐시`에서의 조회
  - 사용자의 하나의 요청-응답(하나의 트랜젝션) 내에서만 효과가 있으므로 성능 이점을 기대하지는 않음.
  - 엔티티 조회 시 먼저 1차 캐시에서 조회 후, 없을 경우 DB에서 조회
- 영속 엔티티의 `동일성(identity) 보장`
  - 1차 캐시로 반복 가능한 읽기(REPEATABLE READ) 등급의 트랜잭션 격리 수준을 데이터베이스가 아닌 애플리케이션 차원에서 제공
- 트랜잭션을 지원하는 `쓰기 지연`(transactional write-behind)
  - Query를 쌓아 두다가 transaction.commit() 을 하는 순간 데이터베이스에 Query 전송
- 변경 감지(Dirty Checking)
  - transaction.commit() 시점에 엔티티와 스냅샷(처음 읽어 온 엔티티 상태) 비교 후 변경이 감지되면 Update Query 를 쓰기 지연 SQL 저장소에 저장
  - 이후 DB에 Query 전송 및 Commit
- 지연 로딩(Lazy Loading)