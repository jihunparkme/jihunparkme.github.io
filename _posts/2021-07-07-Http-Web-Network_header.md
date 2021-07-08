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
  - 콘텐츠 협상
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

---

# HTTP 해더 (캐시와 조건부 요청)

---
