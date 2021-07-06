---
layout: post
title: HTTP Web Network (2)
summary: (Method) 모든 개발자를 위한 HTTP 웹 기본 지식
categories: (Inflearn)HTTP-Web-Network
featured-img: http
# mathjax: true
---

# HTTP Web Network

영한님의 [모든 개발자를 위한 HTTP 웹 기본 지식](https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC#) 강의
HTTP Web Network 강의 노트

- HTTP Method

# Table Of Contents

1. [HTTP 메서드](#HTTP-메서드)

- HTTP API
- GET, POST
- PUT, PATCH, DELETE
- HTTP 메서드 속성

2. [HTTP 메서드 활용](#HTTP-메서드-활용)

- 클라이언트에서 서버로 데이터 전송
- HTTP API 설계 예시

3. [HTTP 상태코드](#HTTP-상태코드)

- 2xx (성공)
- 3xx (리다이렉션)
- 4xx (클라이언트 오류)
- 5xx (서버 오류)

---

# HTTP 메서드

- GET : 리소스 조회
- POST : 요청 데이터 처리(등록)
- PUT : 리소스 대체, 없으면 생성
- PATCH : 리소스 부분 변경
- DELETE : 리소스 삭제

## API URI 설계

- 좋은 URI 설계는 리소스 식별이 중요
  - 회원 = 리소스
  - **회원** 목록 조회 /members
  - **회원** 조회 /members/{id} `GET`
  - **회원** 등록 /members/{id} `POST`
  - **회원** 수정 /members/{id} `PUT`
  - **회원** 삭제 /members/{id} `DELETE`
- 리소스(회원)와 행위(조회, 등록, 삭제, 변경)를 분리
  - URI는 리소스만 식별

### `GET`

- 리소스 **조회**
- 전달 데이터는 query parameter OR query string 을 통해 전달

### `POST`

- 새 리소스 **생성**(등록)
- 요청 **데이터 처리**
  - 프로세스 처리
  - 컨트롤 URI
- massage body를 통해 서버로 요청 데이터 전달

### `PUT`

- 리소스가 있으면 대체, 없으면 생성 **(덮어쓰기)**
- 클라이언트가 리소스 위치를 알고 URI 지정 (POST와의 차이)
  - `PUT /members/100 HTTP/1.1`
  - `POST /members HTTP/1.1`

### `PATCH`

- 리소스 **부분 변경**
  - `PATCH /members/100 HTTP/1.1`

### `DELETE`

- 리소스 **제거**
  - `DELETE /members/100 HTTP/1.1`

## HTTP 메서드의 속성

[HTTP 속성](https://ko.wikipedia.org/wiki/HTTP#%EC%9A%94%EC%95%BD%ED%91%9C)

- 안전(Safe)
  - 리소스 변경이 일어나지 않는 것 (ex. GET, HEAD ..)
- 멱등(Idempotent)
  - 몇 번을 호출하든 결과는 같다 (GET, PUT, DELETE)
  - 자동 복구 메커니즘에서 활용
- 캐시가능(Cacheable)
  - 응답 결과 리소스를 캐시해서 사용 (GET, HEAD 정도만 캐시로 사용)

---

# HTTP 메서드 활용

## 클라이언트에서 서버로 데이터 전송

- Query Parameter를 통한 데이터 전송
  - GET
  - ex) 정렬 필터(검색)
- Message Body를 통한 데이터 전송
  - POST, PUT, PATCH
  - ex) 회원가입, 상품주문, 리소스 등록, 리소스 변경

**정적 데이터 조회**

- GET
- 이미지, 정적 텍스트 문서
- Query Parameter 없이 리소스 경로로 단순 조회

**동적 데이터 조회**

- GET
- 게시물 검색, 정렬, 필터
- Query Parameter 사용

**HTML FORM을 통한 데이터 전송**

- POST
- 등록, 변경
- Content-Type
  - application/x-www-form-urlencoded
    - form 내용을 Message Body를 통해 전송
    - 전송 데이터를 url encoding 처리
  - multipart/form-data
    - 파일 업로드 같은 바이너리 데이터 전송 시 사용
    - 다른 종류의 여러 파일과 폼 내용을 함께 전송 가능
- HTML Form 전송은 GET, POST만 지원

**HTTP API를 통한 데이터 전송**

- Server to Server 통신
- 모바일 앱 클라이언트
- Ajax 웹 클라이언트
- GET -> Query Parameter로 데이터 전달 후 조회
- POST, PUT, PATCH -> Message Body를 통해 데이터 전송
- Content-Type : application/json

## HTTP API 설계 예시

**POST 기반 등록**

서버가 관리하는 리소스 디렉토리 (Collection)

- 회원 목록 /members -> `GET`
- 회원 등록 /members -> `POST`
- 회원 조회 /members/{id} -> `GET`
- 회원 수정 /members/{id} -> `PATCH`, `PUT`, `POST`
- 회원 삭제 /members/{id} -> `DELETE`

**PUT 기반 등록**

클라이언트가 관리하는 리소스 저장소 (Store)

- 파일 목록 /files -> `GET`
- 파일 조회 /files/{filename} -> `GET`
- 파일 등록 /files/{filename} -> `PUT`
- 파일 삭제 /files/{filename} -> `DELETE`
- 파일 대량 등록 /files -> `POST`

**HTML FORM 사용**

HTML FORM은 GET, POST만 지원하므로 Control URI 사용

- 회원 목록 /members -> `GET`
- 회원 등록 폼 /members/new -> `GET`
- 회원 등록 /members/new -> `POST`
- 회원 조회 /members/{id} -> `GET`
- 회원 수정 폼 /members/{id}/edit -> `GET`
- 회원 수정 /members/{id}/edit -> `POST`
- 회원 삭제 /members/{id}/delete -> `POST`

[REST Resource Naming Guide](https://restfulapi.net/resource-naming/)

- 컬렉션과 문서로 최대한 해결하고 그 후에 컨트롤 URI 사용

---

# HTTP 상태코드

## `2xx` (Successful): 요청 정상 처리

**Code**

- 200 OK
- 201 Created (POST)
- 202 Accepted (batch)
- 204 No Content

## `3xx` (Redirection): 요청을 완료를 위해 추가 행동 필요

**Redirect**

- 웹 브라우저는 3xx 응답의 결과에 Location 헤더가 있으면, Location 위치로 자동 이동
- 영구 리다이렉션 : 특정 리소스의 URI가 영구적으로 이동 (301, 308)
- 일시 리다이렉션 : 일시적인 변경 (302, 303, 307)
  - PRG(Post/Redirect/Get)에 사용 / 새로고침 중복 주문 방지
- 특수 리다이렉션 : 결과 대신 캐시 사용

**Code**

- 300 Multiple Choices (X)
- 301 Moved Permanently
  - 리다이렉트 시 <u>Get</u>으로 변하고, 본문 손실
- 302 Found
  - 리다이렉트 시 <u>GET</u>으로 변하고, 본문 제거
- 303 See Other
  - 리다이렉트 시 <u>GET</u>으로 변경
- 304 Not Modified
  - 클라이언트에게 리소스가 수정되지 않았음을 알려줌 (캐시 재사용)
- 307 Temporary Redirect
  - 리다이렉트 시 메서드와 본문 유지
- 308 Permanent Redirect
  - 리다이렌트 시 <u>POST</u>, 본문 유지

## `4xx` (Client Error)

- 오류의 원인은 클라이언트

**Code**

- 400 Bad Request
  - 클라이언트가 잘못된 요청을 해서 서버가 요청을 처리할 수 없음
- 401 Unauthorized
  - 클라이언트가 해당 리소스에 대한 인증이 필요
  - 인증(Authentication): 로그인
  - 인가(Authorization): 권한
- 403 Forbidden
  - 서버가 요청을 이해했지만 승인을 거부 (접근 권한 제한)
- 404 Not Found
  - 요청 리소스를 찾을 수 없음

## `5xx` (Server Error)

- 서버 문제로 오류 발생

**Code**

- 500 Internal Server Error
  - 서버 내부 문제로 오류 발생 (애매하면 500)
- 503 Service Unavailable
  - 서비스 이용 불가
