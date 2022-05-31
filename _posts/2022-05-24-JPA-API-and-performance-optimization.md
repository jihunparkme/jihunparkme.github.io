---
layout: post
title: JAP API and Performance Otimization
summary: JPA Programming Part 3. API 개발과 성능 최적화
categories: (Inflearn)JPA-Programming
featured-img: jpa-spring-uses-2
# mathjax: true
---

# JAP API and Performance Optimization

영한님의 [실전! 스프링 부트와 JPA 활용2 - API 개발과 성능 최적화](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8-JPA-API%EA%B0%9C%EB%B0%9C-%EC%84%B1%EB%8A%A5%EC%B5%9C%EC%A0%81%ED%99%94/dashboard) 강의 노트

[Project](https://github.com/jihunparkme/inflearn-spring-jpa-roadmap/tree/main/jpa-web-jpashop)

## API Basic

API와 Template Engin은 공통 처리를 해야 하는 요소가 다르므로 패키지를 분리하여 관리하는 것이 좋음.

```text
ㄴ src.main.java
    ㄴ example
        ㄴ api
        ㄴ controller
```

### 회원 등록 API

엔티티 대신 **API 요청 스펙에 맞는 별도 DTO를 사용**하기.

- 엔티티와 프레젠테이션 계층을 위한 로직 분리할 수 있음
- 엔티티가 변경되어도 API 스펙이 변하지 않음
  - 엔티티 필드가 변경되더라도 컴파일 에러로 바로 체크 가능
- 엔티티와 API 스펙을 명확하게 분리할 수 있음
- 실무에서는 절대 엔티티를 API 스펙에 노출하지 말자!

```java
@PostMapping("/api/members")
public CreateMemberResponse saveMember(@RequestBody @Valid CreateMemberRequest request) {
    Member member = new Member();
    member.setName(request.getName());
    member.setAddress(request.getAddress());

    Long id = memberService.join(member);
    return new CreateMemberResponse(id);
}

@Data
static class CreateMemberRequest {
    @NotEmpty
    private String name;

    @Embedded
    private Address address;
}

@Data
static class CreateMemberResponse {
    private Long id;

    public CreateMemberResponse(Long id) {
        this.id = id;
    }
}
```

### 회원 수정 API

### 회원 조회 API

## 지연 로딩과 조회 성능 최적화

## 컬렉션 조회 최적화

## 실무 필수 최적화