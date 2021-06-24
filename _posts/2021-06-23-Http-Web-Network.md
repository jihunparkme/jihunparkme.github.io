---
layout: post
title: HTTP Web Network
summary: Inflearn 모든 개발자를 위한 HTTP 웹 기본 지식
categories: (Inflearn)HTTP-Web-Network
featured-img: http
# mathjax: true
---

# HTTP Web Network

영한님의 [모든 개발자를 위한 HTTP 웹 기본 지식](#https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC#) 강의
HTTP Web Network 강의 노트

# Table Of Contents

1. [인터넷 네트워크](#인터넷-네트워크)

- IP(Internet Protocol)
- TCP, UDP
- PORT
- DNS

2. [URI와 웹 브라우저 요청 흐름](#URI과-웹-브라우저-요청-흐름)

- URI
- 웹 브라우저 요청 흐름

3. [HTTP 기본](#HTTP-기본)

- HTTP
- 클라이언트 서버 구조
- Stateful, Stateless
- 비 연결성(connectionless)
- HTTP 메시지

4. [HTTP 메서드](#HTTP-메서드)

- HTTP API
- GET, POST
- PUT, PATCH, DELETE
- HTTP 메서드 속성

5. [HTTP 메서드 활용](#HTTP-메서드-활용)

- 클라이언트에서 서버로 데이터 전송
- HTTP API 설계 예시

6. [HTTP 상태코드](#HTTP-상태코드)
7. [HTTP 해더 (일반 헤더)](<#HTTP-해더-(일반-헤더)>)
8. [HTTP 해더 (캐시와 조건부 요청)](<#HTTP-해더-(캐시와-조건부-요청)>)

---

# 인터넷 네트워크

message를 서버를 통해 어떻게 전달될까?

## `IP(Internet Protocol)`

- 지정한 IP Address에 데이터 전달
- Packet이라는 통신 단위로 데이터 전달
  - IP Packet 정보 : 출발지 IP, 목적지 IP, 기타.. 전송 데이터
  - 인터넷 노드들끼리 목적지 IP를 향해 Packet을 전달
- Internet Protocol의 한계
  - 비연결성 (대상이 없거나 서비스 불능 상태일 경우)
  - 비신뢰성 (패킷이 사라지거나, 순서가 지켜지지 않을 경우)
- 프로그램 구분

## `TCP, UDP`

- `참고 `> 프로토콜 계층 순서

  - 애플리케이션 계층 (브라우저, 채팅, 게임 등)
    - HTTP, FTP
  - OS
    - 전송 계층 : TCP, UDP
    - 인터넷 계층 : IP
  - 네트워크 인터페이스
    - LAN 드라이버/장비

- `TCP (Transmission Control Protocol)` 특징

  - 연결지향 (3 Way Handshake)
  - 데이터 전달 보증
  - 순서 보장 등..
  - IP의 한계를 해결. 대부분이 사용

- `UDP (User Datagram Protocol)`

  - 기능이 거의 없지만, 추가 설정 가능
  - 단순하고 빠름
  - IP와 동일하지만 PORT, 체크섬 정도 추가

## `PORT`

- TCP/IP 패킷
  - IP로 목적지 서버 찾기
  - PORT로 같은 서버 안에서 프로세스 구분
  - 클라이언트 IP : 100.100.1:1010
  - 서버 IP : 200.200.200:80
- 0 ~ 65535 까지 할당 가능
- 0 ~ 1023 은 잘 알려진 포트이므로, 사용하지 않는 것을 추천

  - FTP : 20, 21
  - TELNET : 23
  - HTTP : 80
  - HTTPS : 443

## `DNS`

- Domain Name System
- `도메인명`(이름)과 `IP`(전화번호)가 저장된 전화번호부

📑

```
복잡한 인터넷 망을 통해 메시지를 보내기 위해서 IP가 필요.
IP만으로는 신뢰가 부족하고 구분이 힘들기 때문에 TCP/UDP가 필요.
같은 IP 안에서 동작하는 애플리케이션을 구분하기 위해 PORT가 필요
IP는 변하기 쉽고 외우기 어렵기 때문에 DNS가 필요
```

---

# URI과 웹 브라우저 요청 흐름

## `URI` (**U**niform **R**esource **I**dentifier)

- 자원을 식별하는 방법
- **URI**는
  - **UR**esource**L**ocator : 리소스가 있는 위치를 지정
    - foo://example.com:8042/over/there?name=ferret#nose
  - **UR**esource**N**ame : 리소스에 이름을 부여
    - urn:example:animal:ferret:nose
  - 또는 둘 다 추가로 분류될 수 있음.
- [RFC Reference](https://www.ietf.org/rfc/rfc3986.txt)
- URL 문법
  - https://www.google.com:433/search?q=hello&hl=ko
    - `https` : 프로토콜 (http, https, ftp 등)
    - `www.google.com` : 호스트명
    - `433` : 포트 번호 (http는 80, https는 443)
    - `/search` : Path (리소스 경로)
    - `q=hello&hl=ko` : query parameter or query string 으로 불림

## 웹 브라우저 요청 흐름

- https://www.google.com:433/search?q=hello&hl=ko
  - www.google.com : DNS 조회 -> 200.200.200.2
    - 443 : HTTPS PORT 생략
  - 웹 브라우저가 HTTP 요청 메시지 생성
    - GET /search?q=hello&hl=ko HTTP/1.1
    - Host: www.google.com
  - socket 라이브러리를 통해 TCP/IP에 전달
  - TCP/IP 패킷 생성, HTTP 메시지 포함
  - ..
  - 응답 메시지

---

# HTTP 기본

## `HTTP`

- **H**yper**T**ext **T**ransfer **P**rotocol
- HTTP에 거의 모든 형태의 데이터를 전송할 수 있음
  - HTML, TEXT, IMAGE, 음성, 영상, 파일, JSON, XML ...
- 특징
  - 클라이언트 서버 구조
  - Stateless, connectionless
  - HTTP 메시지로 통신
  - 단순, 확장성

## 클라이언트 서버 구조

- Request-Response 구조
- 클라이언트는 서버에 request 후 response 대기
- 서버가 request에 대한 결과를 만들어서 응답

## `Stateful, Stateless`

### `Stateful`

- 서버가 클라이언트의 `이전 상태를 보존`
- ex) 점원이 바뀌면 고객의 상태를 알 수 없음 (로그인)
  - 항상 같은 서버와 연결
- 일반적으로 브라우저 쿠키와 서버 세션들을 사용해 상태 유지
- 상태 유지는 <i>최소한</i>만 사용

### `Stateless`

- 서버가 클라이언트의 `이전 상태를 보존 X`
- ex) 점원이 바뀌어도 고객의 상태를 알 수 있음 (소개 페이지)
  - 스케일 아웃(수평 확장)에 유리
- 장: 서버 확장성이 높음, 응답 서버를 쉽게 바꿀 수 있음
- 단: 클라이언트가 필요한 데이터를 지속적으로 전송

## 비 연결성(connectionless)

- Connectionless
  - 서버 연결을 유지하는 모델
    - 서버 자원 소모
  - 서버 연결을 유지하지 않는 모델
    - 최소한의 자원 유지
- HTTP는 기본이 연결을 유지하지 않는 모델
- 서버의 자원을 효율적으로 사용
- HTTP 지속 연결(Persistent Connections)로 TCP/IP의 3 way handshake 시간 소요 해결
- HTTP/2, HTTP/3 에서 최적화

## HTTP 메시지

- HTTP 메시지 구조
  - 시작 라인 (start-line)
  - 헤더 (header)
  - 공백 라인 (empty line, CRLF)
  - message body

### Start-Line

- request-line (`GET` `/search?q=hello&hl=ko` `HTTP/1.1`)
  - HTTP 메서드
    -GET, POST, PUT, DELETE
  - 요청 대상 (absolute-path[?query])
  - HTTP Version
  ```text
  // 요청 메시지
  GET /search?q=hello&hl=ko HTTP/1.1
  Host: www.google.com
  ```
- status-line

  - HTTP 버전
  - HTTP 상태 코드
    - 200, 400, 500
  - 이유 문구

  ```text
  // 응답 메시지
  HTTP/1.1 200 OK
  Content-Type: text/html;charset=UTF-8
  Content-Length: 3423

  <html>
      <body>...</body>
  </html>
  ```

### HTTP Header

- HTTP 전송에 필요한 모든 부가정보
  - message body를 제외하고 필요한 모든 메타 정보

### Message Body

- 실제 전송할 데이터
  - HTML 문서, 이미지, 영상, JSON 등등 (Byte 표현 가능한 모든 데이터)

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

---

# HTTP 상태코드

---

# HTTP 해더 (일반 헤더)

---

# HTTP 해더 (캐시와 조건부 요청)

---
