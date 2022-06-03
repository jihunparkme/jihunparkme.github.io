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

- 엔티티와 프레젠테이션(API) 계층을 위한 로직 분리할 수 있음
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

등록과 마찬가지로 **별도 DTO 사용**하기

- 변경감지를 활용해서 데이터 수정하기
- CQS(Command-Query Separation) : 가급적이면 Command와 Query를 분리하자.

**Controller**

```java
@PutMapping("/api/members/{id}")
public UpdateMemberResponse updateMember(@PathVariable("id") Long id, @RequestBody @Valid UpdateMemberRequest request) {

    memberService.update(id, request.getName()); // Command
    Member findMember = memberService.findOne(id); // Query
    return new UpdateMemberResponse(findMember.getId(), findMember.getName());
}

@Data
static class UpdateMemberRequest {
    private String name;
}

@Data
@AllArgsConstructor
static class UpdateMemberResponse {
    private Long id;
    private String name;
}
```
**Service**

```java
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class MemberService {

    //...

    @Transactional
    public void update(Long id, String name) {
        Member member = memberRepository.findOne(id);
        member.setName(name);
        // Transactional commit -> flush (변경감지)
    }
}
```

### 회원 조회 API

등록, 수정과 마찬가지로 **엔티티를 API 응답 스펙 맞는 별도 DTO로 변환하여 반환**하기

- 엔티티가 변경되어도 API 스펙이 변경되지 않음
- Result 클래스로 컬렉션을 감싸주면서 향후 필요한 필드를 자유롭게 추가 가능
- API 요청에 필요한 필드만 노출 (용도에 따라 DTO를 생성)

```java
@GetMapping("/api/members")
public Result member() {
    List<Member> findMembers = memberService.findMembers();
    List<MemberDto> collect = findMembers.stream()
            .map(m -> new MemberDto(m.getName()))
            .collect(Collectors.toList());

    return new Result(collect.size(), collect);
}

@Data
@AllArgsConstructor
static class Result<T> {
    private int count;
    private T data;
}

@Data
@AllArgsConstructor
static class MemberDto {
    private String name;
}
```

## 지연 로딩과 조회 성능 최적화

지연 로딩으로 발생하는 성능 문제를 해결해보자.

.

**엔티티를 직접 노출할 경우**

- 순환 참조 문제 발생 `StackOverflowError`
  - @JsonIgnore 설정으로 해결 가능
- @JsonIgnore 을 추가하더라도 지연로딩으로 인한 proxy(bytebuddy) 객체를 jackson 라이브러리가 읽을 수 없는 문제 발생 `Type definition error`
  - Hibernate5Module 을 Spring Bean 으로 등록하면 해결 가능
  - 단, 지연 로딩 객체는 null 출력, 강제 지연 로딩도 가능하지만 성능 악화 발생

**엔티티를 DTO로 변환**

- 엔티티를 직접 노출하지 않고, 엔티티를 DTO로 변환
- 1 + N 문제 발생 (엔티티 직접 노출과 동일)
  - 첫 번째 쿼리의 결과 N번 만큼 쿼리가 추가로 실행되는 문제

## 컬렉션 조회 최적화

## 실무 필수 최적화