---
layout: post
title: Header
summary: HTTP Header
categories: Spring-Conquest
featured-img: http
# mathjax: true
---

# HTTP Web Network

영한님의 [모든 개발자를 위한 HTTP 웹 기본 지식](#https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC#) 강의
HTTP Web Network 강의 노트

- HTTP Header

---

# HTTP 해더 (일반 헤더)

```text
HTTP/1.1 200 OK         -- start line

-- HTTP Header
Content-Type: text/html;charset=UTF-8
Content-Length: 3423
---

-- Message Body
<html>
 <body>...</body>
</html>
---
```

## HTTP 헤더

- `header-field`
  - field-name: field-value
  - HTTP 전송에 필요한 모든 부가정보
    - ex) Mesasage body 내용/크기, 압축, 인증, 서버 정보 등..
  - [표준 헤더](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields)

## 표현

- **표현**은 요청이나 응답에서 전달할 실제 데이터
- **표현 헤더**는 **표현 데이터**를 해석할 수 있는 정보 제공
- 표현 헤더
  - `Content-Type` : 표현 데이터의 형식
    - text/html; charset=utf-8
    - application/json
    - image/png
  - `Content-Encoding` : 표현 데이터의 압축 방식
    - gzip
    - deflate
    - identity
  - `Content-Language` : 표현 데이터의 자연 언어
    - ko
    - en
    - en-US
  - `Content-Length` : 표현 데이터의 길이(Byte)

## Content negotiation

Client가 선호하는 표현 요청 (요청시에만 사용)

[rfc7231 Accept](https://datatracker.ietf.org/doc/html/rfc7231#section-5.3.2)

- Accept : Client가 선호하는 미디어 타입 전달
  - `Accept: text/*, text/plain, text/plain;format=flowed, */*`
- Accept-Charset : Client가 선호하는 문자 인코딩
- Accept-Encoding : Client가 선호하는 압축 인코딩
- Accept-Language : Client가 선호하는 자연 언어
  - `Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7`

## 전송 방식

**단순 전송**

- `Content-Length: 3423`

**압축 전송**

- `Content-Encoding: gzip`

**분할 전송**

- `Transfer-Encoding: chunked`

**범위 전송**

- `Content-Range: bytes 1001-2000 / 2000`

## 일반 정보

`Form`

- User agent email 정보 (요청)

`Referer`

- 이전 웹 페이지 주소 (요청)

`User-Agent`

- User-Agent Application 정보 (요청)
- Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36

`Server`

- 요청을 처리하는 ORIGIN 서버의 소프트웨어 정보 (응답)
- Apache/2.2.22

`Date`

- 메시지가 발생한 날짜와 시간 (응답)

## 특별한 정보

`Host`

- 요청한 호스트의 정보 (도메인)
- 요청에서 필수
- 하나의 IP에 여러 도메인이 적용되었을 경우

`Location`

- 페이지 리다이렉션
- 3xx 응답의 결과에 Location 헤더가 있으면, Location 위치로 자동 이동
- 201 (Created), 3xx (Redirection)

## 인증

`Authorization`

- 클라이언트 인증 정보를 서버에 전달
- Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW

`WWW-Authenticate`

- 리소스 접근시 필요한 인증 방법 정의

## 쿠키

`Set-Cookie`

- 서버에서 클라이언트로 쿠키 전달(응답)

`Cookie`

- 클라이언트가 서버에서 받은 쿠키를 저장하고, HTTP 요청시 서버로 전달

**동작**

1. 로그인
2. 서버는 Set-Cookie에 user 정보를 담아서 응답
3. 웹브라우저 내부 쿠키 저장소에 쿠키(user) 정보 저장
4. 로그인 이후 요청을 보낼 때마다 자동으로 쿠키 저장소를 조회 후 Cookie 헤더를 만들어서 서버에 전송

**사용**

- 사용자 로그인 세션 관리
- 광고 정보 트래킹

**쿠키 정보는 항상 서버에 전송**

- 네트워크 트래픽 추가 유발
- 최소한의 정보만 사용(session id, 인증 token)
- 웹 스토리지(localStorage, sessionStorage)를 사용하여 웹 브라우저 내부에 데이터 저장 가능

**생명주기**

- Set-Cookie
  - `expires`=Sat, 26-Dec-2020 04:39:21 GMT
  - `max-age`=3600 (sec)
  - `domain`=google.com
    - 명시 : 명시 도메인 + 서브 도메인
    - 생략 : 현재 문서 기준 도메인
  - `path`=/
    - 명시 경로 포함 하위 경로
  - `Secure`
    - https인 경우에만 쿠키 전송
  - `HttpOnly`
    - XSS 공격 방지 / JS에서 접근 불가
  - `SameSite`
    - XSRF 공격 방지
    - 요청 도메인과 쿠키 설정 도메인이 같은 경우에만 쿠키 전송
- 세션 쿠키: 만료 날짜를 생략하면 브라우저 종료시 까지만 유지
- 영속 쿠키: 만료 날짜를 입력하면 해당 날짜까지 유지

---

# HTTP 해더 (캐시와 조건부 요청)

## 캐시 기본 동작

**동작**

1. 캐시 유효 시간 설정 -> `cache-control`: max-age=60
2. 응답 결과를 브라우저 캐시에 저장
3. 두 번째 요청 시 캐시를 탐색 후 캐시에서 조회 (네트워크 사용량 감소)
4. 재요청 시 캐시 유효 시간이 초과되었다면 갱신

## 검증 헤더와 조건부 요청 (Last-Modified)

- 캐시 만료후에도 서버에서 데이터를 변경하지 않았다만 저장해 두었던 캐시를 재사용 할 수 있다.

- 초기 요청 시 데이터 최종 수정일을 캐시에 함께 저장 (검증 헤더)
  - `Last-Modified`: Wed, 21 July 2021 07:28:00 GMT
- 캐시 시간 초과 후 재요청 시 데이터 최종 수정일을 헤더에 함께 전달 (조건부 요청)
  - `if-modified-since`: Wed, 21 July 2021 07:28:00 GMT
- 서버에서 데이터가 수정되지 않은게 확인되면 **304 Not Modified** 로 응답
  - HTTP Body는 포함하지 않고 Header 메타 정보만 응답
- 클라이언트는 캐시에 저장되어 있는 데이터 재사용

## 검증 헤더와 조건부 요청 (ETag)

- Entity Tag : Last-Modified의 단점 보완
- 캐시 제어 로직을 서버에서 관리
  - 캐시 데이터는 임의의 고유 버전 혹은 Hash 이름 보유
- 초기 요청 시 ETag를 캐시에 함께 저장 (검증 헤더)
  - `ETag`: "a2jiodwjekjl3"
- 캐시 시간 초과 후 재요청 시 ETag를 헤더에 함께 전달 (조건부 요청)
  - `If-None-Match`: "aaaaaaaaaa"
- 서버에서 데이터가 수정되지 않은게 확인되면 **304 Not Modified** 로 응답
  - HTTP Body는 포함하지 않고 Header 메타 정보만 응답
- 클라이언트는 캐시에 저장되어 있는 데이터 재사용

## 캐시와 조건부 요청 헤더

`Cache-Control` : 캐시 제어

- `max-age` : 캐시 유효 시간 (초)
- `no-cache` : (이터는 캐시해도 되지만), 프록시 캐시가 아닌 항상 원서버에 변경사항 검증 후 사용
- `no-store` : 데이터에 민감한 정보가 있으므로 저장 X
- `must-revalidate` : 캐시 만료 후 최초 조회 시 원 서버에 검증

## 프록시 서버

- 해외 원서버에 있는 데이터를 브라우저에서(private cache)빠르게 이용하기 위해 중간(프록시 캐시 서버, public cache)에서 공용으로 사용하는 캐시 서버

캐시 지시어(directives)

- `Cache-Control: public`
  - 응답이 public 캐시에 저장 가능
- `Cache-Control: private`
  - 응답이 해당 사용자만을 위한 것, private 캐시에 저장(기본값)

## 캐시 무효화

`Cache-Control`: no-cache, no-store, must-revalidate

`Pragma`: no-cache # HTTP 1.0 하위 호환

> Reference
>
> [HTTP 스펙 : RFC 7230~7235](https://datatracker.ietf.org/doc/html/rfc7230)
>
> HTTP 완벽가이드 도서

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