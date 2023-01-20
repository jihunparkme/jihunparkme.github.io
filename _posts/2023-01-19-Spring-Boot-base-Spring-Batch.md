---
layout: post
title: Spring Boot base Spring Batch
summary: Spring Boot 기반 Spring Batch
categories: spring-boot spring-batch
featured-img: spring-batch
# mathjax: true
---

# Spring Core Principles Advanced

정수원님의 [Spring Boot 기반으로 개발하는 Spring Batch](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EB%B0%B0%EC%B9%98/dashboard) 강의 노트

[Project](https://github.com/jihunparkme/Inflearn-Spring-Batch)

docker mysql 실행 : `docker run -p 5432:5432 --name pg -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=postgres -e POSTGRES_DB=springboot -d postgres`

## 개요

**핵심 패턴**

- Read: 데이터베이스, 파일, 큐에서 다량의 데이터 조회
- Process: 특정 방법으로 데이터 가공
- Write: 수정된 양식으로 데이터를 다시 저장

**아키텍처**

- Application
  - 모든 배치 Job, 커스텀 코드 포함
  - 업무로직 구현에만 집중하고 공통 기술은 프레임워크가 담당
- Batch Core
  - Job 실행, 모니터링, 관리 API로 구성
  - JobLauncher, Job, Step, Flow ..
- Batch Infrastructure
  - Application, Core 모두 공통 Infrastructure 위에서 빌드
  - Job 실행 흐름과 처리를 위한 틀 제공
  - Reader, Processor Writer, Skip, Retry ..

**스프링 배치 활성화**

- `@EnableBatchProcessing`
  - 총 4개의 설정 클래스를 실행시키며 스프링 배치의 모든 초기화 및 실행 구성
    - `BatchAutoConfiguration`
      - 스프링 배치가 초기화 될 때 자동으로 실행되는 설정 클래스
      - Job을 수행하는 **JobLauncherApplicationRunner** 빈 생성
    - `SimpleBatchConfiguration`
      - **JobBuilderFactory** 와 **StepBuilderFactory** 생성
      - 스프링 배치의 주요 구성 요소 생성 -> 프록시 객체로 생성
    - BatchConfigurerConfiguration
      - `BasicBatchConfigurer`
        - SimpleBatchConfiguration 에서 생성한 프록시 객체의 실제 대상 객체를 생성하는 설정 클래스
        - 빈으로 의존성 주입 받아서 주요 객체들을 참조해서 사용
      - `JpaBatchConfigurer`
        - JPA 관련 객체를 생성하는 설정 클래스  
  - 스프링 부트 배치의 자동 설정 클래스가 실행됨으로 빈으로 등록된 모든 Job을 검색해서 초기화와 동시에 Job을 수행하도록 구성

[img. enable-batch-processing](https://raw.githubusercontent.com/jihunparkme/jihunparkme.github.io/master/post_img/spring-batch/enable-batch-processing.png)

**기본 코드**

```java
@Configuration //=> 하나의 배치 잡을 정의하고 빈 설정
@RequiredArgsConstructor
public class HelloJobConfiguration {

    private final JobBuilderFactory jobBuilderFactory; //=> Job을 생성
    private final StepBuilderFactory stepBuilderFactory; //=> Step을 생성

    @Bean
    public Job helloJob() {
        return this.jobBuilderFactory.get("helloJob") //=> Job 생성 (일, 일감)
                .start(helloStep())
                .build();
    }

    public Step helloStep() {
        return stepBuilderFactory.get("helloStep2") //=> Step 생성 (일의 항목, 단계)
                .tasklet((contribution, chunkContext) -> { //=> Step 안에서 단일 Task로 수행되는 로직 구현 (작업 내용)
                    System.out.println(" ============================");
                    System.out.println(" >> Step2 has executed");
                    System.out.println(" ============================");
                    return RepeatStatus.FINISHED;
                })
                .build();
    }
}
```

### DB 스키마

- 스프링 배치의 실행/관리를 위한 목적으로 여러 도메인(Job, Step, JobParameters..)의 정보들을 저장/업데이트/조회할 수 있는 스키마 제공
- 과거, 현재의 실행에 대한 정보, 성공과 실패 여부 등을 관리하여 배치운용 리스크 발생 시 빠른 대처 가능
- DB 연동 시 메타 테이블 생성 필수
- DB 스키마는 유형별로 제공 (/org/springframework/batch/core/schema-*.sql)
  - 스키마는 수동 또는 자동으로 생성 가능(자동 생성 시 spring.batch.jdbc.initialize-schema 설정)
    - `ALWAYS` : 스크립트 항상 실행(RDBMS 설정이 되어 있을 경우 내장 DB 보다 먼저 실행)
    - `EMBEDDED` : 내장 DB일 때만 실행, 스키마 자동 생성(default)
    - `NEVER` : 스크립트 항상 실행 안함(내장 DB일경우 스크립트가 생성되지 않으므로 오류 발생)
      - 운영에서 수동으로 스크립트 생성 후 설정 권장

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-batch/batch-schema.png?raw=true 'Result')

[Meta-Data Schema](https://docs.spring.io/spring-batch/docs/3.0.x/reference/html/metaDataSchema.html)