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
    - 1,0,Job,0c5cf62846f98c894b8dce3de3433509
    
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
    - 1,2,1,2023-01-23 00:16:14.365000,2023-01-23 00:16:14.452000,2023-01-23 00:16:14.645000,COMPLETED,COMPLETED,"",2023-01-23 00:16:14.646000,

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
    - 2,STRING,name,user1,1970-01-01 09:00:00,0,0,Y
    - 2,LONG,seq,"",1970-01-01 09:00:00,1,0,Y
    - 2,DATE,date,"",2023-01-23 00:16:14.666000,0,0,Y
    - 2,DOUBLE,age,"",1970-01-01 09:00:00,0,29.5,Y

    
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
    - 1,"{""@class"":""java.util.HashMap""}",

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
    - 1,3,step1,1,2023-01-23 00:16:14.507000,2023-01-23 00:16:14.551000,COMPLETED,1,0,0,0,0,0,0,0,COMPLETED,"",2023-01-23 00:16:14.552000

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
    - 1,"{""@class"":""java.util.HashMap"",""batch.taskletType"":""io.springbatch.springbatchlecture.job.JobConfiguration$1"",""batch.stepType"":""org.springframework.batch.core.step.tasklet.TaskletStep""}",


## 스프링 배치 도메인

### Job

**`Job`**

- 배치 계층 구조에서 가장 상위에 있는 개념으로 하나의 배치작업 자체를 의미
- Job Configuration 을 통해 생성되는 객체 단위로, 배치작업을 어떻게 구성하고 실행할 것인지 전체적으로 설정하고 명세해 놓은 객체
- 배치 Job 구성을 위한 최상위 인터페이스, 스프링 배치가 기본 구현체 제공
- 여러 Step 을 포함하는 컨테이너, 반드시 한 개 이상의 Step으로 구성

**기본 구현체**

- **SimpleJob**
  - 순차적으로 **Step** 을 실행시키는 Job
  - 모든 Job에서 유용하게 사용할 수 있는 표준 기능을 갖음
- **FlowJob**
  - 특정한 조건과 흐름에 따라 Step 을 구성하여 실행시키는 Job
  - **Flow** 객체를 실행시켜서 작업을 진행

**`JobInstance`**

- Job 실행 시(SimpleJob) 생성되는 Job 의 논리적 실행 단위 객체 (고유하게 식별 가능한 작업 실행을 나타냄)
- Job 과 설정/구성은 동일하지만, Job 실행 시점에 처리하는 내용은 다르므로 Job 실행 구분이 필요
  - ex. 하루 한 번씩 배치 Job이 실행된다면, 매일 실행되는 각각의 Job 을 JobInstance 로 표현
- JobInstance 생성 및 실행
  - 처음 시작 : [Job + JobParameter] 의 새로운 JobInstance 생성
  - 이전과 동일한 [Job + JobParameter] 으로 실행 : 이미 존재하는 JobInstance 리턴 -> 예외 발생 및 배치 실패
    - JobName + jobKey(jobParametes 의 해시값) 가 동일한 데이터는 중복 저장 불가
- Job : 1 - JobInstance : N

![Result](https://github.com/jihunparkme/jihunparkme.github.io/blob/master/post_img/spring-batch/JobInstance.png?raw=true 'Result')


**`JobParameters`**

- job 실행 시 함께 포함되어 사용되는 파라미터를 가진 도메인 객체
- 하나의 Job에 존재할 수 있는 여러개의 JobInstance 구분
- JobParameters : 1 - JobInstance : 1
- 생성 및 바인딩
  - 어플리케이션 실행 시 주입
    - `Java -jar LogBatch.jar requestDate(date)=2021/01/01 name=user seq(long)=2L age(double)=29.5`
  - 코드로 생성
    - JobParameterBuilder, DefaultJobParametersConverter
  - SpEL 이용
    - @Value(“#{jobParameter[requestDate]}”), @JobScope, @StepScope 선언 필수
  - JOB_EXECUTION : 1 - BATCH_JOB_EXECUTION_PARAM : N

```java
// JobParameters.java
private final Map<String, JobParameter> parameters;

// JobParameter.java
private final Object parameter;
private final JobParameter.ParameterType parameterType;
private final boolean identifying;

// ParameterType enum
STRING,
DATE,
LONG,
DOUBLE;
```

실행 시 Arguments : job.name=JobParameter date(date)=2021/01/01 name=user seq(long)=2L age(double)=29.5

**`JobExecution`**

- JobIstance(동일한 JobParameter)에 대한 한번의 시도를 의미하는 객체
  - Job 실행 중 발생한 정보들을 저장 -> 시작시간, 종료시간, 상태(시작/완료/실패), 종료상태
- JobExecution 은 'FAILED' 또는 'COMPLETED‘ 등의 Job 실행 결과 상태를 가지고 있음
  - 실행 상태 결과가 'COMPLETED’ 일 경우, JobInstance 실행이 완료된 것으로 간주해서 재 실행 불가
  - 실행 상태 결과가 'FAILED’ 일 경우, JobInstance 실행이 완료되지 않은 것으로 간주해서 재실행 가능
  - 실행 상태 결과가 'COMPLETED’ 될 때까지 하나의 JobInstance 내에서 여러 번의 시도 발생 가능
- BATCH_JOB_INSTANCE : 1 - BATCH_JOB_EXECUTION : N관계로서 
  - JobInstance 에 대한 성공/실패의 내역을 보유

JobExecution.java

```java
final JobParameters jobParameters; // JobParameters 객체 저장
JobInstance jobInstance; // JobInstance 객체 저장
volatile ExecutionContext executionContext; // 실행하는 동안 유지해야 하는 데이터를 담고 있음
volatile BatchStatus status; // 실행 상태를 나타내는 Eum 클래스 (COMPLETED, STARTING, STARTED, STOPPING, STOPPED, FAILED, ABANDONED, UNKNOWN)
volatile ExitStatus exitStatus; // 실행 결과를 나타내는 클래스로서 종료코드를 포함(UNKNOWN, EXECUTING, COMPLETED, NOOP, FAILED, STOPPED)
transient volatile List<Throwable> failureExceptions; // Job 실행 중 발생한 예외 리스트
volatile Date startTime; // Job을 실행할 때의 시스템 시간
volatile Date createTime; // JobExecution이 처음 저장될 때의 시스템 시간
volatile Date endTime; // 성공 여부와 상관없이 실행이 종료되는 시간
volatile Date lastUpdated; // JobExecution이 마지막 저장될 때의 시스템 시간
```

### Step

### ExecutionContext

### JobRepository

### JobLauncher
