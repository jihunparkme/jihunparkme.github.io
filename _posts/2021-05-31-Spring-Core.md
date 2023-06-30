---
layout: post
title: Spring Core
summary: Inflearn Spring Core Principles (스프링 핵심 원리 - 기본편)
categories: Spring-Conquest Spring Container Bean
featured-img: spring_core
# mathjax: true
---

# Inflearn_Spring2_Core_Principles

영한님의 [스프링 핵심 원리 - 기본편]((https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%ED%95%B5%EC%8B%AC-%EC%9B%90%EB%A6%AC-%EA%B8%B0%EB%B3%B8%ED%8E%B8/dashboard)) 강의노트

스프링 핵심 원리 - 기본편 강의 노트

## Spring

[Spring Documentaion](https://spring.io/projects)

- Required
  - Spring Framework
  - Spring Boot
- Optional
  - Spring Data
  - Spring Session
  - Spring Security
  - Spring Rest Docs
  - Spring Batch
  - Spring Cloud

---

## 좋은 객체지향의 5가지 원칙 (SOLID)

**SRP**: 단일 책임 원칙(single responsibility principle)
- `하나의 클래스는 하나의 책임만` 가져야 한다.
- 관심사를 분리시켜 변경이 있을 때 파급 효과를 줄일 수 있다.
- 클라이언트 객체는 실행하는 책임만 담당
  
**DIP**: 의존관계 역전 원칙 (Dependency inversion principle)
- 프로그래머는 `“추상화에 의존해야지, 구체화에 의존하면 안된다.”`
- 구현 클래스에 의존하지 말고, `인터페이스에 의존`하라.
- `역할(Interface)에 의존`해야 `구현의 변경에 유연`해질 수 있다.
- 의존성 주입(DI)은 DIP 원칙을 따름

**OCP**: 개방-폐쇄 원칙 (Open/closed principle)
- 소프트웨어 요소는 `확장에서는 열려 있으나 변경에는 닫혀 있어야 한다`
- 애플리케이션을 `사용 영역`과 `구성 영역`으로 나눔
- 인터페이스를 구현한 새로운 클래스에 새로운 기능을 구현하면 사용 역영의 변경을 닫을 수 있다.

**LSP**: 리스코프 치환 원칙 (Liskov substitution principle)
- 프로그램의 `객체는 프로그램의 정확성을 깨뜨리지 않으면서 하위 타입의 인스턴스로 바꿀 수 있어야 한다.`
- 다형성에서 하위 클래스는 인터페이스 규약을 다 지켜야 한다.

**ISP**: 인터페이스 분리 원칙 (Interface segregation principle)
- `특정 클라이언트를 위한 인터페이스 여러 개가 범용 인터페이스 하나보다 낫다.`
- 인터페이스의 분리로 인터페이스가 명확해지고, 대체 가능성이 높아진다.

## 스프링과 객체지향

**IoC(Inversion of Control, 제어의 역전)**
- `프로그램의 제어 흐름을` 직접 제어하는 것이 아니라 `외부에서 관리`하는 것

**DI(Dependency Injection, 의존관계 주입)**
- 의존관계는 정적인 클래스 의존 관계와, `실행 시점에 결정되는 동적인 객체(인스턴스)` 의존 관계 둘을 분리해서 생각
- 스프링이 다형성 + OCP(개방-폐쇄 원칙), DIP(의존관계 역전 원칙) 가능하도록 지원
- **정적인 클래스 의존관계**
  - 클래스가 사용하는 import 코드만 보고 의존관계를 쉽게 판단
- **동적인 객체 인스턴스 의존 관계**
  - 애플리케이션 실행 시점에 실제 생성된 객체 인스턴스의 참조가 연결된 의존 관계
- 클라이언트 코드를 변경하지 않고, 클라이언트가 호출하는 대상의 타입 인스턴스 의존관계 변경 가능

**DI Container(IoC Container)**
- 객체를 생성하고 관리하면서 의존관계를 연결해 주는 것을 의미
- 의존관계 주입에 초점을 맞추면 DI 컨테이너라고 불리는게 적합

> 스프링은 DI, DI Container로 `다형성 + OCP, DIP`을 적용시켜 클라이언트의 코드 변경 없이 기능 확장이 가능하도록 지원

---

**도메인 설계**

- 도메인 `협력, 역할, 책임` 관계 (기획자 시점)
  - `역할과 구현을 분리`하여 자유롭게 구현 객체를 조립할 수 있도로 설계
- 클래스 다이어그램 (개발자 시점)
- 객체 다이어그램 (인스턴스끼리의 참조)

## Spring Container

```java
/** 
 * AnnotationConfigApplicationContext : ApplicationContext 인터페이스의 구현체
 *  ConfigObject : 구성 정보
 */
ApplicationContext applicationContext = 
  new AnnotationConfigApplicationContext(ConfigObject.class);
```

- ApplicationContext = 스프링 컨테이너
- 스프링 컨테이너는 XML 기반 또는 애노테이션 기반의 자바 설정 클래스로 만들 수 있음

**스프링 컨테이너 생성 과정**
- **스프링 컨테이너 생성**
  - `@Configuration` 선언 객체를 `설정 정보`로 사용
  - 또는 `new AnnotationConfigApplicationContext(ConfigObject.class)`
- **스프링 빈 등록**
  - Config 객체에서 `@Bean` 선언된 메서드를 모두 호출해서 반환된 객체를 `스프링 컨테이너에 등록`
  - 스프링 빈(스프링 컨테이너에 등록된 객체)은 @Bean 선언된 메서드명을 스프링 빈의 이름으로 사용하거나 `@Bean(name="beanName")` 처럼 직접 부여도 가능
  - 빈 이름은 항상 다른 이름을 사용하자.
    - 같은 이름을 사용하면, 다른 빈이 무시되거나, 덮어쓰이거나 설정에 따라 오류가 발생
- **스프링 빈 의존관계 설정**
  - 설정 정보를 참고해서 의존관계 주입(DI)

### Bean 조회

```java
AnnotationConfigApplicationContext ac = 
  new AnnotationConfigApplicationContext(AppConfig.class);

@Test
void findAllBean() {
    // 스프링에 등록된 모든 빈 정보 조회
    String[] beanDefinitionNames = ac.getBeanDefinitionNames();
    for (String beanDefinitionName : beanDefinitionNames) {
        // 빈 이름으로 빈 객체(인스턴스) 조회
        Object bean = ac.getBean(beanDefinitionName);
        System.out.println("name=" + beanDefinitionName + " object=" +
        bean);
    }
}

@Test
void findApplicationBean() {
    String[] beanDefinitionNames = ac.getBeanDefinitionNames();
    for (String beanDefinitionName : beanDefinitionNames) {
        BeanDefinition beanDefinition = ac.getBeanDefinition(beanDefinitionName);
        // ROLE_APPLICATION: 직접 등록한 애플리케이션 빈
        // ROLE_INFRASTRUCTURE: 스프링이 내부에서 사용하는 빈
        if (beanDefinition.getRole() == BeanDefinition.ROLE_APPLICATION) {
        Object bean = ac.getBean(beanDefinitionName);
        System.out.println("name=" + beanDefinitionName + " object=" +
        bean);
        }
    }
}
```

**빈 조회 방법**
- 빈 이름과 타입으로 조회: `ac.getBean(빈이름, 타입)`
- 해당 타입의 모든 빈 조회: `ac.getBeansOfType()` 
- 조회 대상 스프링 빈이 없으면 예외 발생
  - NoSuchBeanDefinitionException: No bean named 'xxxxx' available

**BeanFactory**

- 스프링 컨테이너의 최상위 인터페이스
- 스프링 빈을 관리하고 조회하는 역할 담당(getBean() 제공)

> BeanFactory <- ApplicationContext <- AnnotationConfig, ApplicationContext

**ApplicationContext**

- BeanFactory 기능을 모두 상속받아서 제공
- 빈을 관리하고 검색하는 기능뿐만 아니라, 수 많은 편리 부가 기능 제공
  - MessageSource
    - 메시지소스를 활용한 국제화 기
    - 한국에서 들어오면 한국어, 영어권에서 들어오면 영어 출력
  - EnvironmentCapable
    - 환경변수
    - 로컬, 개발, 운영등을 구분해서 처리
  - ApplicationEventPublisher
    - 애플리케이션 이벤트
    - 이벤트를 발행하고 구독하는 모델을 편리하게 지원
  - ResourceLoader
    - 편리한 리소스 조회
    - 파일, 클래스패스, 외부 등에서 리소스를 편리하게 조회

**BeanDefinition**

- 스프링 빈 설정 메타 정보
  - `@Bean`, `<bean>` 각 하나씩 메타 정보 생성
- 추상화된 BeanDefinition 덕분에 스프링이 (자바 코드, XML, Groovy 등)다양한 설정 형식을 지원
- 스프링 컨테이너는 이 메타정보를 기반으로 스프링 빈 생성

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring/bean-definition.png?raw=true 'Result')

## Singleton Container

**Singleton Pattern**

- 클래스의 인스턴스가 딱 한개만 생성되는 것을 보장하는 디자인 패턴
- 객체 인스턴스를 두 개 이상 생성하지 못하도록 private 생성자 사용
- 이미 만들어진 객체를 공유 해서 효율적으로 사용 가능하지만 수 많은 문제점 보유
  - 싱글톤 패턴을 구현하기 위해 코드가 길어질 수 있음.
  - 의존관계상 클라이언트가 구체 클래스에 의존(DIP를 위반).
  - 클라이언트가 구체 클래스에 의존해서 OCP 원칙을 위반할 가능성이 높음.
  - 테스트의 어려움.
  - 내부 속성을 변경하거나 초기화 하기 어려움.
  - private 생성자를 사용하다보니 자식 클래스를 만들기 어려움
  - 결론적으로 유연성이 떨어지고, 안티패턴으로 불리움.

**Singleton Container**

> 스프링 컨테이너: 싱글톤 컨테이너 역할
> 
> 싱글톤 레지스트: 싱글톤 객체를 생성하고 관리하는 기능

- 싱글톤 패턴의 문제점을 해결하면서, 객체 인스턴스를 싱글톤으로 관리
  - DIP, OCP, 테스트, private 생성자로 부터 자유로움
- 싱글톤 객체(스프링 빈)는 상태를 `무상태(stateless)`로 설계해야 한다.
  - 특정 클라이언트에 `의존적인 필드`가 있으면 안된다.
  - 특정 클라이언트가 `값을 변경할 수 있는 필드`가 있으면 안된다.
  - 가급적으로 `읽기만 가능`해야 한다.
  - 필드 대신에 자바에서 `공유되지 않는` 지역변수, 파라미터, ThreadLocal 등을 사용해야 한다.
- 스프링 설정 정보는 항상 `@Configuration`을 사용하여 싱글톤을 보장하자.
  - @Configuration 선언 시 바이트코드를 조작하는 CGLIB 기술이 적용되어 싱글톤 보장
  - 설정 정보 클래스를 상속받은 xxx@CGLIB 클래스가 싱글톤을 보장

## Component Scan

- 설정 정보 클래스에 `@ComponentScan`을 명시해 주면, 자동으로 class path를 탐색해서 `@Component`가 명시된 class들을 스캔해서 스프링 빈으로 등록
  - 빈 이름 기본 전략: 앞글자만 소문자로 변경된 클래스명을 사용
  - 빈 이름 직접 지정: @Component("beanName")
- 의존관계 주입은 `@Autowired`가 해결
  - 기본 조회 전략: 타입이 같은 빈을 찾아서 주입

```java
@ComponentScan(
  /**
   * basePackages
   * 탐색할 패키지의 시작 위치(하위 패키지 모두 탐색)
   * 지정하지 않으면 @ComponentScan 선언된 설정 정보 클래스의 패키지가 시작 위치
   * 설정 정보 클래스의 위치를 프로젝트 최상 단에 두는 것을 추천
   * 
   * 스프링 부트는 기본 방법으로 @SpringBootApplication 에 @ComponentScan 포함
   */
    basePackages = {"hello.core", "hello.service"}, 
}
```

- Component Scan 기본 대상
  - `@Component`:  컴포넌트 스캔 탐색 대상
  - `@Controller` : 스프링 MVC 컨트롤러
  - `@Service` : 비즈니스 로직 계층
  - `@Repository` : 스프링 데이터 접근 계층(데이터 계층의 예외를 스프링 예외로 변환)
  - `@Configuration` : 스프링 설정 정보(스프링 빈이 싱글톤을 유지하도록 처리)

**Filters**

- includeFilters : 컴포넌트 스캔 대상 추가 지정
- excludeFilters : 컴포넌트 스캔에서 제외할 대상 지정

```java
@ComponentScan(
    includeFilters = @Filter(type = FilterType.ANNOTATION, classes = MyIncludeComponent.class),
    excludeFilters = @Filter(type = FilterType.ANNOTATION, classes = MyExcludeComponent.class)
)
```

## 의존관계 자동 주입

- `생성자 주입` ⭐️

  - 생성자를 통해 의존 관계를 주입받는 방법
  - 딱 1번 호출 보장. **불변-필수** 의존관계
  - 불변하게 설계 가능하고, 의존관계 누락 방지(final)
  - 항상 생성자 주입을 선택하자.
  - lombok 사용 시 `@RequiredArgsConstructor`

  ```java
  @Component
  public class OrderServiceImpl implements OrderService {

    private final MemberRepository memberRepository;
    private final DiscountPolicy discountPolicy;

    @Autowired
    public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
        this.memberRepository = memberRepository;
        this.discountPolicy = discountPolicy;
    }
  }
  ```

- `수정자 주입(Setter)`

  - 수정자 메서드를 통해서 의존관계를 주입
  - **선택, 변경** 가능성이 있는 의존 관계
    - 선택적으로 사용할 경우(주입할 대상이 없어도 동작하도록 할 경우)
      - @Autowired(required = false)
    - 단, 중간에 의존관계를 변경할 일은 거의 없음

  ```java
  @Component
  public class OrderServiceImpl implements OrderService {

    private MemberRepository memberRepository;
    private DiscountPolicy discountPolicy;

    @Autowired
    public void setMemberRepository(MemberRepository memberRepository) {
      this.memberRepository = memberRepository;
    }

    @Autowired
    public void setDiscountPolicy(DiscountPolicy discountPolicy) {
      this.discountPolicy = discountPolicy;
    }
  }
  ```

- `필드 주입`

  - 외부에서 변경이 불가능하여 테스트하기 힘들다는 치명적
  - 가급적 테스트 코드에서만 사용

  ```java
  @Component
  public class OrderServiceImpl implements OrderService {

      @Autowired private MemberRepository memberRepository;

      @Autowired private DiscountPolicy discountPolicy;
  }
  ```

- `일반 메서드 주입`

  - 일반 메서드를 통해 주입
  - 한번에 여러 필드를 주입 받을 수 있는 특징이 있지만 잘 사용하지 않음

  ```java
  @Component
  public class OrderServiceImpl implements OrderService {

    private MemberRepository memberRepository;
    private DiscountPolicy discountPolicy;

    @Autowired
    public void init(MemberRepository memberRepository, DiscountPolicy discountPolicy) {

      this.memberRepository = memberRepository;
      this.discountPolicy = discountPolicy;
    }
  }
  ```

**옵션**

- @Autowired(required=false)
  - 자동 주입할 대상이 없으면 수정자 메서드 자체를 호출하지 않음
  ```java
  @Autowired(required = false)
  public void setNoBean1(Member member) {
      System.out.println("setNoBean1 = " + member);
  }
  ```
- org.springframework.lang.@Nullable
  - 자동 주입할 대상이 없으면 null
  ```java
  @Autowired
  public void setNoBean2(@Nullable Member member) {
      System.out.println("setNoBean2 = " + member);
  }
  ```
- Optional<>
  - 자동 주입할 대상이 없으면 Optional.empty
  ```java
  @Autowired(required = false)
  public void setNoBean3(Optional<Member> member) {
      System.out.println("setNoBean3 = " + member);
  }
  ```

### 조회 대상 빈이 2개 이상일 경우

**`@Autowired`**

- 타입 매칭을 시도
- 여러 빈이 조회되면 필드 이름, 파라미터 이름으로 빈 이름을 추가 매칭
```java
@Autowired
private DiscountPolicy rateDiscountPolicy
```

**`@Qualifier`**

- 빈 등록 시 @Qualifier 로 추가 구분자 설정
- @Qualifier 매칭 -> 빈 이름 매칭 -> NoSuchBeanDefinitionException 예외

```java
@Component
@Qualifier("mainDiscountPolicy") // 빈 등록 시 이름 설정
public class RateDiscountPolicy implements DiscountPolicy {}

/** 1. 생성자 자동 주입의 경우 **/
@Autowired
public OrderServiceImpl(
        MemberRepository memberRepository,
        @Qualifier("mainDiscountPolicy") DiscountPolicy discountPolicy) {

  this.memberRepository = memberRepository;
  this.discountPolicy = discountPolicy;

}

/** 2. 수정자 자동 주입의 경우 **/
@Autowired
public DiscountPolicy setDiscountPolicy(@Qualifier("mainDiscountPolicy") DiscountPolicy discountPolicy) {
  return discountPolicy;
}
```

**`@Primary`**

- @Autowired 시에 여러 빈이 매칭되면 @Primary가 우선권
- Database Connection을 가져올 경우 등 은근 사용
```java
@Component
@Primary
public class RateDiscountPolicy implements DiscountPolicy {}
```

**참고. 빈 애노테이션 만들기**

```java
@Target({ElementType.FIELD, ElementType.METHOD, ElementType.PARAMETER,
ElementType.TYPE, ElementType.ANNOTATION_TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Qualifier("mainDiscountPolicy")
public @interface MainDiscountPolicy {
}

//

@Component
@MainDiscountPolicy
public class RateDiscountPolicy implements DiscountPolicy {}

//

@Autowired
public OrderServiceImpl(
          MemberRepository memberRepository,
          @MainDiscountPolicy DiscountPolicy discountPolicy) {
  this.memberRepository = memberRepository;
  this.discountPolicy = discountPolicy;
}
```

### 조회한 빈이 모두 필요할 경우

동적으로 Bean을 선택해야할 때, 다형성 코드를 유지하면서 Bean을 사용할 수 있음

```java
public class AllBeanTest {

    @Test
    void findAllBean() {
        ApplicationContext ac = new AnnotationConfigApplicationContext(AutoAppConfig.class, DiscountService.class);

        DiscountService discountService = ac.getBean(DiscountService.class);
        Member member = new Member(1L, "userA", Grade.VIP);
        int discountPrice = discountService.discount(member, 10000, "fixDiscountPolicy");

        assertThat(discountService).isInstanceOf(DiscountService.class);
        assertThat(discountPrice).isEqualTo(1000);

        int rateDiscountPrice = discountService.discount(member, 20000, "rateDiscountPolicy");
        assertThat(rateDiscountPrice).isEqualTo(2000);
    }


    static class DiscountService {
        // Map(Key=스프링 빈 이름, value=DiscountPolicy 타입으로 조회한 모든 스프링 빈)
        private final Map<String, DiscountPolicy> policyMap;
        // DiscountPolicy 타입으로 조회한 모든 스프링 빈을
        private final List<DiscountPolicy> policies;

        public DiscountService(Map<String, DiscountPolicy> policyMap,  List<DiscountPolicy> policies) {
            this.policyMap = policyMap;
            this.policies = policies;
        }

        // 원하는 할인 방법은 매개변수로 받은 후, Map에서 꺼내서 사용
        public int discount(Member member, int price, String discountCode) {
            DiscountPolicy discountPolicy = policyMap.get(discountCode);
            return discountPolicy.discount(member, price);
        }
    }
}
```

> 편리한 자동 빈 등록 기능을 기본으로 사용하자.
> 
> 수동 빈 등록은 기술 지원 객체, 다형성을 활용하는(Bean Map, List) 비즈니스 로직에 적용해보자.
> 
> 직접 등록하는 빈은 설정 정보에 바로 나타나게 하는 것이 유지보수하기 좋다.

## 빈 생성주기 콜백

**스프링 빈의 이벤트 라이프사이클**

- `스프링 컨테이너 생성` -> `스프링 빈 생성` -> `의존관계 주입` -> `초기화 콜백` -> `사용` -> `소멸전 콜백` -> `스프링 종료`

.

**객체의 생성과 초기화를 분리하자.**

- **생성자**는 `객체 생성에 책임`을, **초기화**는 생성된 값들을 활용해서 커넥션 열결과 같은 `무거운 동작을 수행`
- 객체를 생성하는 부분과 초기화 하는 부분을 명확하게 나누는 것이 유지보수 관점에서 좋음

.

**스프링의 빈 생명주기 콜백 지원 방법**

`@PostConstruct`, `@PreDestory` 지원

- 스프링에서 권장하는 방법
- 메서드에 애너테이션만 선언하면 되는 편리한 방법
- 스프링에 종속족이지 않은 기술
- 외부 라이브러리에 적용 불가(@Bean 설정정보 기능 활용)

`설정 정보`에 초기화/종료 메서드 지정

- @Bean(initMethod = "init", destroyMethod = "close")
- destroyMethod 기본값이 inferred(추론)으로 등록
  - close, shutdown(대부분의 라이브러리가 가지는 종료 메서드 이름) 메서드를 자동으로 호출
- 메서드 이름의 자유로움
- 스프링 빈이 스프링 코드에 의존하지 않음
- 외부 라이브러리에도 적용 가능(코드가 아닌 설정 정보를 사용)

`InitializingBean`, `DisposableBean` 인터페이스

- InitializingBean.afterPropertiesSet()
- DisposableBean.destroy()
- 지금은 거의 사용하지 않는 방법
  - 스프링 전용 인터페이스에 의존
  - 초기화, 소멸 메서드 이름 변경 불가
  - 외부 라이브러리에 적용 불가

## 빈 스코프

**빈이 존재할 수 있는 범위**

스프링은 싱글톤, 프로토타입, 웹 관련 스코프(request, session, application)를 지원

빈 스코프 지정 방법

```java
// 컴포넌트 스캔 자동 등록
@Scope("prototype")
@Component
public class HelloBean {}

...

// 수동 등록
@Scope("prototype")
@Bean
PrototypeBean HelloBean() {
    return new HelloBean();
}
```

.

**`싱글톤`**

- 기본 스코프
- 스프링 컨테이너의 시작~종료까지 유지되는 가장 넓은 범위의 스코프
- 스프링 컨테이너는 항상 같은 인스턴스의 스프링 빈을 반환

.

**`프로토타입`**

- 스프링 컨테이너는 프로토타입 빈의 생성과 의존관계 주입, 초기화까지만 관여하는 매우 짧은 범위의 스코프(종료 메서드 호출 X)
- 스프링 컨테이너에 조회할 때마다 새로운 인스턴스를 생성해서 반환
  - 의존성 주입을 받는 시점에 각각 새로운 프로토타입 빈이 생성
- 프로토타입 빈을 조회한 클라이언트가 관리. 종료 메서드 호출도 클라이언트가 수행
- 직접적으로 사용하는 일은 매우 드묾

참고. 싱글톤 빈과 함께 사용시 문제점

- 스프링은 일반적으로 싱글톤 빈을 사용하여 싱글톤 빈이 프로토타입 빈을 사용
- 싱글톤 빈은 생성 시점에만 의존성 주입을 받으므로, 프로토타입 빈을 사용할 때마다 새로 생성해서 사용하고자하는 의도와 다르게 프로토타입 빈 스코프가 싱글톤 빈과 함께 계속 유지
- ObjectProvider 을 활용한 문제 해결
  - 지정한 빈을 컨테이너에서 대신 찾아주는 DL(Dependency Lookup) 서비스 제공
  ```java
  @Autowired
  private ObjectProvider<PrototypeBean> prototypeBeanProvider;

  public int logic() {
      PrototypeBean prototypeBean = prototypeBeanProvider.getObject();
      prototypeBean.addCount();
      int count = prototypeBean.getCount();
      return count;
  }
  ```

.

**`웹 스코프`**

- 웹 환경에서만 동작
- 프로토타입 빈과 다르게 스프링이 해당 스코프의 종료시점까지 관리
- 유지보수를 위해 필요한 곳에만 최소화해서 사용 권장

request: 
- HTTP 요청 하나가 들어오고 나갈 때까지 유지되는 스코프
- 각각의 HTTP 요청마다 별도의 빈 인스턴스 생성/관리

```java
/**
 * @Scope
 * - 실제 고객 요청이 들어와야 request 스코프 객체의 빈이 생성되므로 빈 생성 지연이 필요.
 * - 적용 대상에 따라 ScopedProxyMode.TARGET_CLASS, ScopedProxyMode.INTERFACES 선택
 * 
 * - HTTP request와 관계 없이 싱글톤처럼 동작하는 프록시 객체를 다른 빈에 미리 의존성 주입
 * - 요청이 오면 프록시 객체 내부에서 원본 객체을 요청하는 위임 로직
 */
@Component
@Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class MyLogger {...}
```

session: 
- HTTP Session과 동일한 생명주기(생성~종료)를 가지는 스코프

application: 
- 서블릿 컨텍스트(ServletContext)와 동일한 생명주기를 가지는 스코프

websocket: 
- 웹 소켓과 동일한 생명주기를 가지는 스코프

---

**스프링 완전 정복 로드맵**

- 스프링 입문 > 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술
- [스프링 핵심 원리 > 기본편](https://jihunparkme.github.io/Spring-Core/)
- 모든 개발자를 위한 HTTP 웹 기본 지식
  - [Basic](https://jihunparkme.github.io/Http-Web-Network_basic/)
  - [Method](https://jihunparkme.github.io/Http-Web-Network_method/)
  - [Header](https://jihunparkme.github.io/Http-Web-Network_header/)
- 스프링 웹 MVC 1편
  - [Servlet](https://jihunparkme.github.io/Spring-MVC-Part1-Servlet/)
  - [MVC](https://jihunparkme.github.io/Spring-MVC-Part1-MVC/)
- 스프링 웹 MVC 2편
  - [Thymeleaf](https://jihunparkme.github.io/Spring-MVC-Part2-Thymeleaf/)
  - [etc](https://jihunparkme.github.io/Spring-MVC-Part2-Etc/)
  - [Validation](https://jihunparkme.github.io/Spring-MVC-Part2-Validation/)
  - [Login](https://jihunparkme.github.io/Spring-MVC-Part2-Login/)
  - [Exception](https://jihunparkme.github.io/Spring-MVC-Part2-Exception/)
- [스프링 DB 1편 > 데이터 접근 핵심 원리](https://jihunparkme.github.io/Spring-DB-Part1/)
- [스프링 DB 2편 > 데이터 접근 활용 기술](https://jihunparkme.github.io/Spring-DB-Part2/)
- [스프링 핵심 원리 > 고급편](https://jihunparkme.github.io/Spring-Core-Principles-Advanced/)
- [실전! 스프링 부트](https://jihunparkme.github.io/spring-boot/)