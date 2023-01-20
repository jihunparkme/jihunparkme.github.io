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

참고.

docker mysql
```shell
# download mysql image
docker pull --platform linux/amd64 mysql:8.0.28

# check images
docker images

# create conatiner
docker run --platform linux/amd64 --name mysql -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=1234 mysql:8.0.28

# execute mysql
docker exec -it mysql bash

# root login
mysql -uroot -p1234

# checker process
docker ps

# stop conatiner
docker stop mysql
```
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

**관련 테이블**

Job 관련 테이블

- `BATCH_JOB_INSTANCE`
  - Job 이 실행될 때 JobInstance 정보가 저장되며 job_name과 job_key를 키로 하여 하나의 데이터가 저장
  - 동일한 job_name 과 job_key 로 중복 저장될 수 없다
    ```sql
    CREATE TABLE BATCH_JOB_INSTANCE  (
      JOB_INSTANCE_ID BIGINT  NOT NULL PRIMARY KEY, -- 고유 식별 기본 키
      VERSION BIGINT, -- 업데이트 시 1씩 증가
      JOB_NAME VARCHAR(100) NOT NULL, -- Job 구성 시 부여하는 Job 이름
      JOB_KEY VARCHAR(32) NOT NULL, -- job_name + jobParameter 해싱 값
    );
    ```
- `BATCH_JOB_EXECUTION`
  - job 의 실행정보가 저장되며 Job 생성, 시작, 종료 시간, 실행상태, 메시지 등을 관리
    ```sql
    CREATE TABLE BATCH_JOB_EXECUTION  (
      JOB_EXECUTION_ID BIGINT  NOT NULL PRIMARY KEY, -- JobExecution 고유 식별 기본 키 (JOB_INSTANCE 와 일대 다 관계)
      VERSION BIGINT, -- 업데이트 시 1씩 증가
      JOB_INSTANCE_ID BIGINT NOT NULL, -- JOB_INSTANCE 키
      CREATE_TIME DATETIME(6) NOT NULL, -- Execution 생성된 시점을 TimeStamp 형식으로 기록
      START_TIME DATETIME(6) DEFAULT NULL, -- Execution 시작 시점을 TimeStamp 형식으로 기록
      END_TIME DATETIME(6) DEFAULT NULL, -- 실행이 종료된 시점을 TimeStamp으로 기록 (Job 실행 도중 오류 발생으로 Job 중단 시 값이 저장되지 않을 수 있음)
      STATUS VARCHAR(10), -- 실행 상태(BatchStatus) 저장 (COMPLETED, FAILED, STOPPED…)
      EXIT_CODE VARCHAR(2500), -- 실행 종료코드(ExitStatus) 저장 (COMPLETED, FAILED…)
      EXIT_MESSAGE VARCHAR(2500), -- Status 실패 시 실패 원인 등의 내용 저장
      LAST_UPDATED DATETIME(6), -- 마지막 실행(Execution) 시점을 TimeStamp 형식으로 기록
    );
    ```
- `BATCH_JOB_EXECUTION_PARAMS`
  - Job과 함께 실행되는 JobParameter 정보를 저장
    ```sql
    CREATE TABLE BATCH_JOB_EXECUTION_PARAMS  (
      JOB_EXECUTION_ID BIGINT NOT NULL , -- JobExecution 식별 키, (JOB_EXECUTION 와 일대다 관계)
      TYPE_CD VARCHAR(6) NOT NULL , -- STRING, LONG, DATE, DUBLE 타입정보
      KEY_NAME VARCHAR(100) NOT NULL , -- 파라미터 키 값
      STRING_VAL VARCHAR(250) , -- 파라미터 문자 값
      DATE_VAL DATETIME(6) DEFAULT NULL , -- 파라미터 날짜 값
      LONG_VAL BIGINT , -- 파라미터 LONG 값
      DOUBLE_VAL DOUBLE PRECISION , -- 파라미터 DOUBLE 값
      IDENTIFYING CHAR(1) NOT NULL , -- 식별여부 (TRUE, FALSE)
    );
    ``` 
- `BATCH_JOB_EXECUTION_CONTEXT`
  - Job 의 실행동안 여러가지 상태정보, 공유 데이터를 직렬화 (Json 형식) 해서 저장
  - Step 간 서로 공유 가능함
    ```sql
    CREATE TABLE BATCH_JOB_EXECUTION_CONTEXT  (
      JOB_EXECUTION_ID BIGINT NOT NULL PRIMARY KEY, -- JobExecution 식별 키 (JOB_EXECUTION 마다 각 생성)
      SHORT_CONTEXT VARCHAR(2500) NOT NULL, -- JOB 실행 상태정보 (공유데이터 등 정보를 문자열로 저장)
      SERIALIZED_CONTEXT TEXT , -- 직렬화(serialized)된 전체 컨텍스트
    );
    ```

Step 관련 테이블

- `BATCH_STEP_EXECUTION`
  - Step 의 실행정보가 저장되며 생성, 시작, 종료 시간, 실행상태, 메시지 등을 관리
    ```sql
    CREATE TABLE BATCH_STEP_EXECUTION  (
      STEP_EXECUTION_ID BIGINT  NOT NULL PRIMARY KEY , -- Step 실행정보 고유 식별 기본 키
      VERSION BIGINT NOT NULL, -- 업데이트 시 1씩 증가
      STEP_NAME VARCHAR(100) NOT NULL, -- Step 구성 시 부여하는 Step 이름
      JOB_EXECUTION_ID BIGINT NOT NULL, -- JobExecution 기본키 (JobExecution 과 일대 다 관계)
      START_TIME DATETIME(6) NOT NULL , -- 실행(Execution) 시작 시점을 TimeStamp 형식으로 기록
      END_TIME DATETIME(6) DEFAULT NULL , -- 실행이 종료 시점을 TimeStamp 으로 기록 (Job 실행 도중 오류 발생으로 Job 중단 시 값이 저장되지 않을 수 있음)
      STATUS VARCHAR(10) , -- 실행 상태 (BatchStatus) 저장 (COMPLETED, FAILED, STOPPED…)
      COMMIT_COUNT BIGINT , -- 트랜잭션 당 커밋되는 수 기록
      READ_COUNT BIGINT , -- 실행시점에 Read한 Item 수 기록
      FILTER_COUNT BIGINT , -- 실행도중 필터링된 Item 수 기록
      WRITE_COUNT BIGINT , -- 실행도중 저장되고 커밋된 Item 수 기록
      READ_SKIP_COUNT BIGINT , -- 실행도중 Read가 Skip 된 Item 수 기록
      WRITE_SKIP_COUNT BIGINT , -- 실행도중 write가 Skip된 Item 수 기록
      PROCESS_SKIP_COUNT BIGINT , -- 실행도중 Process가 Skip 된 Item 수 기록
      ROLLBACK_COUNT BIGINT , -- 실행도중 rollback이 일어난 수 기록
      EXIT_CODE VARCHAR(2500) , -- 실행 종료코드(ExitStatus) 저장 (COMPLETED, FAILED…)
      EXIT_MESSAGE VARCHAR(2500) , -- Status 실패 시 실패 원인 등의 내용 저장
      LAST_UPDATED DATETIME(6), -- 마지막 실행(Execution) 시점을 TimeStamp 형식으로 기록
    );
    ```
- `BATCH_STEP_EXECUTION_CONTEXT`
  - Step 의 실행동안 여러가지 상태정보, 공유 데이터를 직렬화 (Json 형식) 해서 저장
  - Step 별로 저장되며 Step 간 서로 공유할 수 없음
    ```sql
    CREATE TABLE BATCH_STEP_EXECUTION_CONTEXT  (
      STEP_EXECUTION_ID BIGINT NOT NULL PRIMARY KEY, -- StepExecution 식별 키 (STEP_EXECUTION 마다 각 생성)
      SHORT_CONTEXT VARCHAR(2500) NOT NULL, -- STEP  실행 상태정보, 공유데이터 등의 정보를 문자열로 저장
      SERIALIZED_CONTEXT TEXT , -- 직렬화(serialized)된 전체 컨텍스트
    );
    ```