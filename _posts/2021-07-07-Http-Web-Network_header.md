---
layout: post
title: HTTP Web Network (3)
summary: (Header) 모든 개발자를 위한 HTTP 웹 기본 지식
categories: (Inflearn)HTTP-Web-Network
featured-img: http
# mathjax: true
---

# HTTP Web Network

영한님의 [모든 개발자를 위한 HTTP 웹 기본 지식](#https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC#) 강의
HTTP Web Network 강의 노트

- HTTP Header

# Table Of Contents

- [HTTP 해더 (일반 헤더)](<#HTTP-해더-(일반-헤더)>)
  - 표현
  - 콘텐츠 협상 (Content negotiation)
  - 전송 방식
  - 일반 정보
  - 특별한 정보
  - 인증
  - 쿠키
- [HTTP 해더 (캐시와 조건부 요청)](<#HTTP-해더-(캐시와-조건부-요청)>)

---

# HTTP 해더 (일반 헤더)

```header
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

`WWW-Authenticate`

- 리소스 접근시 필요한 인증 방법 정의

# HTTP 해더 (캐시와 조건부 요청)

---
