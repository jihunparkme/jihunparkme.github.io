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

엔티티 대신 `API 요청 스펙에 맞는 별도 DTO를 사용`하기.

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

등록과 마찬가지로 `별도 DTO 사용`하기

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

등록, 수정과 마찬가지로 `엔티티를 API 응답 스펙 맞는 별도 DTO로 변환하여 반환`하기

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

지연 로딩으로 발생하는 성능 문제를 단계적으로 해결해보자.

.

**엔티티를 직접 노출**

- 순환 참조 문제 발생 `StackOverflowError`
  - @JsonIgnore 설정으로 해결 가능
- @JsonIgnore 을 추가하더라도 지연로딩으로 인한 proxy(bytebuddy) 객체를 jackson 라이브러리가 읽을 수 없는 문제 발생 `Type definition error`
  - Hibernate5Module 을 Spring Bean 으로 등록하면 해결 가능
  - 단, 지연 로딩 객체는 null 출력, 강제 지연 로딩도 가능하지만 성능 악화 발생

```java
// OrderSimpleApiController.java

@GetMapping("/api/v1/simple-orders")
public List<Order> ordersV1() {
    List<Order> all = orderRepository.findAllByString(new OrderSearch());
    for (Order order : all) {
        order.getMember().getName(); // Lazy 강제 초기화
        order.getDelivery().getAddress(); // Lazy 강제 초기화
    }

    return all;
}
```

**엔티티를 DTO로 변환**

- 엔티티를 직접 노출하지 않고, `엔티티를 DTO로 변환`
- 1 + N 문제 발생 (엔티티 직접 노출과 동일)
  - 첫 번째 쿼리의 결과 N번 만큼 쿼리가 추가로 실행되는 문제
  - ex) Order 조회 시 Member - N번, Delivery - N 번, 총 1 + N + N 개의 쿼리 발생

```java
// OrderSimpleApiController.java

@GetMapping("/api/v2/simple-orders")
public List<SimpleOrderDto> ordersV2() {
    List<SimpleOrderDto> result = orderRepository.findAllByString(new OrderSearch()).stream()
            .map(SimpleOrderDto::new)
            .collect(toList());

    return result;
}

@Data
static class SimpleOrderDto {
    private Long orderId;
    private String name;
    private LocalDateTime orderDate;
    private OrderStatus orderStatus;
    private Address address;

    public SimpleOrderDto(Order order) {
        orderId = order.getId();
        name = order.getMember().getName(); // LAZY 초기화
        orderDate = order.getOrderDate();
        orderStatus = order.getStatus();
        address = order.getDelivery().getAddress(); // LAZY 초기화
    }
}
```

**페치 조인 최적화**

- 페치 조인을 사용해서 1 + N 문제를 쿼리 1번 만에 조회
- 코드가 간결하고, 다른 API에서 재사용이 쉬움
  
```java
// OrderRepository.java

public List<Order> findAllWithMemberDelivery() {
    return em.createQuery(
                    "select o from Order o" +
                            " join fetch o.member m" +
                            " join fetch o.delivery d", Order.class)
            .getResultList();
}
```

**DTO로 바로 조회**

조회된 엔티티를 DTO로 변환하는 과정 필요 없이, 바로 DTO 조회해서 성능 최적화하기

- 원하는 필드만 선택(SELECT)해서 조회
  - DB <-> 네트워크 용량 최적화 (생각보다 미비한 차이)
- new 명령어를 사용해서 JPQL의 결과를 DTO로 즉시 변환
- API 스펙에 맞추다보니 변경이 어려우므로, 다른 API에서 Repository 재사용이 어려움
- 사용할 경우 순수한 엔티티를 조회하는 레파지토리와 화면 종속적인 레파지토리를 분리하는 것을 추천

```java
// OrderRepository.java

public List<OrderSimpleQueryDto> findOrderDtos() {
    return em.createQuery(
                    "select new jpabook.jpashop.repository.order.simplequery.OrderSimpleQueryDto(o.id, m.name, o.orderDate, o.status, d.address)" +
                            " from Order o" +
                            " join o.member m" +
                            " join o.delivery d", OrderSimpleQueryDto.class)
            .getResultList();
}
```

⭐️ **쿼리 방식 선택 권장 순서** ⭐️

1. `엔티티를 DTO로 변환`
2. 필요 시 `페치 조인으로 성능 최적화` (대부분의 성능 이슈가 해결)
3. 그래도 안되면 `DTO로 직접 조회`
4. 최후의 방법은 `JPA가 제공하는 네이티브 SQL` 혹은 `Spring JDBC Template`을 사용해서 SQL을 직접 사용

## 컬렉션 조회 최적화

toOne(OneToOne, ManyToOne)관계에 이어서 컬렉션인 일대다 관계(OneToMany)를 최적화해보자.

toOne 관계와 동일한 부분들이 포함되어 있다.

.

**엔티티를 직접 노출**

- 엔티티가 변하면 API 스펙이 변함
- 트랜잭션 안에서 지연 로딩(LAZY) 강제 초기화 필요
- 양방향 연관관계 문제 (@JsonIgnore 설정으로 해결 가능하지만 지연로딩 객체를 읽을 수 없는 문제 발생할 수 있음)

```java
// OrderApiController.java

@GetMapping("/api/orders")
public List<Order> ordersV1() {
    List<Order> all = orderRepository.findAllByString(new OrderSearch());
    for (Order order : all) {
        order.getMember().getName(); // Lazy 강제 초기화
        order.getDelivery().getAddress(); // Lazy 강제 초기환
        List<OrderItem> orderItems = order.getOrderItems();
        orderItems.stream().forEach(o -> o.getItem().getName()); // Lazy 강제 초기화
    }

    return all;
}
```

**엔티티를 DTO로 변환**

- 트랜잭션 안에서 지연 로딩 필요 (지연 로딩으로 너무 많은 SQL 실행)
- 지연 로딩은 영속성 컨텍스트에 있는 엔티티 사용을 시도하고 없으면 SQL을 실행
- ex) Order 조회 시 Member - N번, Address - N 번, OrderItem - N 번, item M번
  - N : order 조회 수, M : orderItem 조회 수
  - 총 1 + N + N + N + M 개의 쿼리 발생

```java
@GetMapping("/api/orders")
public List<OrderDto> ordersV2() {
    List<Order> orders = orderRepository.findAllByString(new OrderSearch());
    List<OrderDto> result = orders.stream()
            .map(OrderDto::new)
            .collect(toList());
    return result;
}

@Data
static class OrderDto {
    private Long orderId;
    private String name;
    private LocalDateTime orderDate;
    private OrderStatus orderStatus;
    private Address address;
    private List<OrderItemDto> orderItems;

    public OrderDto(Order order) {
        this.orderId = order.getId();
        this.name = order.getMember().getName();
        this.orderDate = order.getOrderDate();
        this.orderStatus = order.getStatus();
        this.address = order.getDelivery().getAddress();
        this.orderItems = order.getOrderItems().stream() // 엔티티 필드 또한 DTO로 변환
                .map(OrderItemDto::new)
                .collect(toList());
    }
}

@Data
static class OrderItemDto {
    private String itemName;
    private int orderPrice;
    private int count;

    public OrderItemDto(OrderItem orderItem) {
        this.itemName = orderItem.getItem().getName();
        this.orderPrice = orderItem.getOrderPrice();
        this.count = orderItem.getCount();
    }
}
```

**페치 조인 최적화**

- 페치 조인으로 SQL 1번만 실행
- 단, 컬렉션 페치 조인 사용 시 `페이징이 불가능한 단점`이 존재
  - 하이버네이트는 경고 로그를 남기면서 모든 데이터를 DB에서 읽어오고, 메모리에서 페이징 작업 - OOM 발생 위험
- 컬렉션 페치 조인은 `1개만 사용 가능`
  - 둘 이상의 컬렉션에 페치 조인을 사용하면 데이터가 부정합하게 조회될 수 있음 (1 * N * N..)
- JPA `distinct`는 SQL에 distinct 추가 및 같은 엔티티(=id)가 조회되면 애플리케이션에서 `중복을 제거`
  - 1:N 조인이 있으면 데이터베이스 row가 뻥튀기되어 distinct 필요

```java
// OrderApiController.java

@GetMapping("/api/orders")
public List<OrderDto> ordersV3() {
    List<Order> orders = orderRepository.findAllWithItem();
    List<OrderDto> result = orders.stream()
            .map(OrderDto::new)
            .collect(toList());

    return result;
}

// OrderRepository.java

public List<Order> findAllWithItem() {
    return em.createQuery(
                    "select distinct o from Order o" +
                            " join fetch o.member m" +
                            " join fetch o.delivery d" +
                            " join fetch o.orderItems oi" +
                            " join fetch oi.item i", Order.class)
            .getResultList();
}
```

**페이징**

컬렉션 페치 조인에서 `페이징이 불가능한 단점 존재`

- 일대다(1:N) 조인이 발생하므로 데이터가 일(1) 기준이 아닌 다(N)를 기준으로 row가 예측할 수 없이 증가
- 일(1)인 Order 기준으로 페이징 하고 싶지만, 다(N)인 OrderItem을 조인하면 OrderItem이 기준이 되어버리는 문제
- 이 경우 하이버네이트는 경고 로그를 남기고 모든 DB 데이터를 읽은 후 메모리에서 페이징을 시도 (최악의 경우 OOM 장애 발생)

페이징 + 컬렉션 엔티티 조회 **문제 해결**

- ToOne(OneToOne, ManyToOne) 관계는 모두 `페치 조인`으로
- 컬렉션은 `지연 로딩`으로 조회
- 지연 로딩 성능 최적화를 위해 `hibernate.default_batch_fetch_size`(글로벌 설정) 또는 `@BatchSize`(개별 최적화) 적용
  - 컬렉션이나, 프록시 객체를 한꺼번에 설정한 size 만큼 IN 쿼리 조회

default_batch_fetch_size 사이즈 선택

  - 적당한 사이즈는 100~1000 사이 권장
  - IN 절 파라미터를 1000 으로 제한하는 데이터베이스가 있음(max size = 1,000)
  - 사이즈를 높게 설정할 경우 한꺼번에 DB에서 애플리케이션으로 불러오므로 DB에 순간 부하가 증가할 수 있음.
  - 하지만 애플리케이션은 사이즈가 어떻게 설정이 되어있든 결국 전체 데이터를 로딩해야 하므로 메모리 사용량이 같다.
  - 1000 으로 설정하는 것이 성능상 가장 좋지만, 결국 DB든 애플리케이션이든 순간 부하를 어디까지 견딜 수 있는지 테스트를 진행해보며 결정하는 것이 중요

장점

- `쿼리 호출 수`가 1+N 에서 1+1 로 `최적화`
- IN 쿼리 사용으로 일반 조인보다 `DB 데이터 전송량 최적화`
- 페치 조인 방식과 비교해서 쿼리 호출 수가 약간 증가하지만(IN 쿼리), `DB 데이터 전송량 감소`(중복 제거)
- 컬렉션 페치 조인에서 `페이징이 불가능한 단점을 해결`

```java
// OrderApiController.java

@GetMapping("/api/v3.1/orders")
public List<OrderDto> ordersV3_page(@RequestParam(value = "offset", defaultValue = "0") int offset,
                                    @RequestParam(value = "limit", defaultValue = "100") int limit) {
    List<Order> orders = orderRepository.findAllWithMemberDelivery(offset, limit);

    List<OrderDto> result = orders.stream()
            .map(o -> new OrderDto(o))
            .collect(toList());

    return result;
}

// OrderRepository.java

public List<Order> findAllWithMemberDelivery(int offset, int limit) {
    return em.createQuery(
                    "select o from Order o" +
                            " join fetch o.member m" +
                            " join fetch o.delivery d", Order.class)
            .setFirstResult(offset)
            .setMaxResults(limit)
            .getResultList();
}
```

```yml
// application.yml

spring:
  jpa:
    properties:
      hibernate:
        default_batch_fetch_size: 100
```

**DTO 직접 조회**

-

**컬렉션 조회 최적화**

-

**플랫 데이터 최적화**

-

## 실무 필수 최적화