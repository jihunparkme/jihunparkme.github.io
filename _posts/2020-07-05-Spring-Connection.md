---

layout: post
title: Spring Connection
summary: Let's learn Spring Framework
categories: Spring
featured-img: spring
# mathjax: true
---

# Table of Contents

* [세션, 쿠키](#세션-쿠키)
* [Redirect, Interceptor](#Redirect,-Interceptor)
* [Database](#DataBase)
* [JDBC](#JDBC)
* [JdbcTemplate](#JdbcTemplate) : Spring DataSource, c3p0 DataSource
* [Connection pool](#Connection-pool)

<br/>

<br/>

# 연결

## 세션-쿠키

### **Connectionless Protocol**

- 웹 서비스는 HTTP 프로토콜을 기반으로 하는데, HTTP 프로토콜은 클라이언트와 서버의 관계를 유지 하지 않는 특징이 있음

  - 서버에 연결되는 클라이언트가 수많을 경우, 서버에 연결된 클라이언트가 많아질 것이고 부화가 걸릴 수 있기 때문

  - 서버의 효율적인 운영을 위해 요청 응답 후 바로 서버 연결 해제

- 서버의 부하를 줄일 수 있는 장점은 있나, 클라이언트의 요청 시마다 서버와 매번 새로운 연결이 생성되기 때문에 일반적인 로그인 상태 유지, 장바구니 등의 기능을 구현하기 어려움

- 이러한 Connectionless Protocol의 불편함을 해결하기 위해서 세션과 쿠키를 이용

- 세션과 쿠키는 클라이언트와 서버의 연결 상태를 유지해주는 방법으로, 

  - 세션은 서버에서 연결 정보를 관리하는 반면
  - 쿠키는 클라이언트에서 연결 정보를 관리하는데 차이



### 세션(Session)

- 서버와 클라이언트 사이의 연결을 유지
- 세션은 서버에 정보를 저장
- 스프링 MVC에서 HttpServletRequest를 이용해서 세션을 이용하려면 컨트롤러의 메소드에서 파라미터로 HttpServletRequest를 받으면 된다

####  세션 생성

- HttpServletRequest를 이용한 세션 생성

```java
// MemberController.java
// ...
@RequestMapping(value = "/login", method = RequestMethod.POST)
public String memLogin(Member member, HttpServletRequest request) {

    Member mem = service.memberSearch(member);

    HttpSession session = request.getSession();
    session.setAttribute("member", mem);

    return "/member/loginOk";
}
// ...
```

- HttpSession을 이용한 세션 생성
  - HttpServletRequest와 HttpSession의 차이점은 거의 없으며, 단지 세션객체를 얻는 방법에 차이
  - HttpServletRequest는 파라미터로 HttpServletRequest를 받은 후 getSession()으로 세션을 얻음.
  - HttpSession은 파라미터로 HttpSession을 받아 세션을 바로 사용

```java
// MemberController.java
//...
@RequestMapping(value = "/login", method = RequestMethod.POST)
public String memLogin(Member member, HttpSession session) {

    Member mem = service.memberSearch(member);

    session.setAttribute("member", mem);

    return "/member/loginOk";
}
//...
```

#### 세션(Session) 삭제

- 세션을 삭제하는 방법은 세션에 저장된 속성이 더 이상 필요 없을 때 이루어지는 과정으로 주로 로그아웃 또는 회원 탈퇴 등에 사용

- 로그아웃

```java
// MemberController.java
//...
@RequestMapping("/logout")
public String memLogout(Member member, HttpSession session) {

    session.invalidate();

    return "/member/logoutOk";
}
```

- 회원탈퇴

```java
// MemberController.java
//...
@RequestMapping(value = "/remove", method = RequestMethod.POST)
public String memRemove(Member member, HttpServletRequest request) {

    service.memberRemove(member);

    HttpSession session = request.getSession();
    session.invalidate();

    return "/member/removeOk";
}
```

#### 세션 주요 메소드

- getId() : 세션 ID 반환
- setAttribute() : 세션 객체에 속성을 저장
- getAttribute() : 세션 객체에 저장된 속성을 반환
- removeAttribute() : 세션 객체에 저장된 속성을 제거
- setMaxInactiveInterval() : 세션 객체의 유지시간을 설정
- getMaxInactiveInterval() : 세션 객체의 유지시간을 반환
- invalidate() : 세션 객체의 모든 정보를 삭제

#### 세션 플로어

<img src="..\post_img\session.JPG" alt="img" style="zoom: 70%;" />

### 쿠키(Cookie)

- 서버와 클라이언트 사이의 연결을 유지
- 쿠키는 클라이언트 에 정보를 저장

#### 쿠키 생성

- mallMain()에서 쿠키를 생성하고, 파라미터로 받은 HttpServletResponse에 쿠키를 담고 있다. 
- 쿠키를 생성할 때는 생성자에 두 개의 파라미터를 넣어주는 데 첫 번째는 쿠키이름을 넣어 주고 두 번째는 쿠키값을 넣어 준다.

- MallController.java

```java
//...
@RequestMapping("/main")
public String mallMain(Mall mall, HttpServletResponse response){

    Cookie genderCookie = new Cookie("gender", mall.getGender());

    if(mall.isCookieDel()) {  // 쿠키를 삭제하라는 옵션이 있을 경우
        genderCookie.setMaxAge(0);  // 서버와 연결을 끊는 과정
        mall.setGender(null);
    } else { // 쿠키를 삭제하라는 옵션이 없을 경우
        // 쿠키 생성(한 달 동안 쿠키를 유지)
        genderCookie.setMaxAge(60*60*24*30);
    }
    // response에 Cookie 삽입
    response.addCookie(genderCookie);

    return "/mall/main";
}
```

#### 쿠키 사용

- mallMain()에서 생성된 쿠키를 mallIndex()에서 사용
- 쿠키를 사용할 때는 @CookieValue 를 사용
  - @CookieValue value = 쿠키 이름, required = 해당 쿠키가 없어도 excaption이 발생하지 않도록 false 로 설정 (default는 true)

- MallController.java

```java
@RequestMapping("/index")
public String mallIndex(Mall mall, 
        @CookieValue(value="gender", required=false) Cookie genderCookie, 
        HttpServletRequest request) {
	
    // 쿠키가 존재한다면
    if(genderCookie != null) 
        mall.setGender(genderCookie.getValue());

    return "/mall/index";
}
```

<br/>

## Redirect,-Interceptor

### Redirect

- 컨트롤러에서 뷰를 분기하는 방법
- 현재 페이지에서 특정 페이지로 전환하는 기능
- MemberController.java
  - 세션이 존재하지 않으면 main 으로 redirect

```java
// 회원 정보 수정 ...
@RequestMapping(value = "/modifyForm")
public String modifyForm(Model model, HttpServletRequest request) {

    HttpSession session = request.getSession();
    Member member = (Member) session.getAttribute("member");

    if(member == null) {
        return "redirect:/";
    } else {
        model.addAttribute("member", service.memberSearch(member));
    }

    return "/member/modifyForm";
}
```

```java
// 회원 정보 삭제 ...
@RequestMapping("/removeForm")
public ModelAndView removeForm(HttpServletRequest request) {

    ModelAndView mav = new ModelAndView();

    HttpSession session =  request.getSession();
    Member member = (Member) session.getAttribute("member");

    if(member == null) {
        mav.setViewName("redirect:/");
    } else {
        mav.addObject("member", member);
        mav.setViewName("/member/removeForm");
    }
    
    return mav;
}
```

### Interceptor

- 컨트롤러 실행 전/후에 특정 작업을 가능하게 하는 방법

- 리다이렉트를 사용해야 하는 경우가 많은 경우 HandlerInterceptor를 이용

- HandlerInterceptor Interface

  - preHandle() : Controller가 작동하기 전 (가장 많이 사용)
  - postHandle() : Controller가 작동한 후
  - afterCompletion()  : Controller와 View가 모두 작업한 후

  <img src="..\post_img\Interceptor.JPG" alt="img" style="zoom: 70%;" />

- src\main\java\com\bs\lec21\member\MemberLoginInterceptor.java

```java
// ...
public class MemberLoginInterceptor extends HandlerInterceptorAdapter {

    @Override	// Controller가 작동하기 전
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response, 
                             Object handler) throws Exception {

        HttpSession session = request.getSession(false);
        
        // Session이 있을 경우
        if(session != null) {
            Object obj = session.getAttribute("member");
            if(obj != null) 
                return true;
        }
		
        // Session이 없을 경우 main page로 redirect
        response.sendRedirect(request.getContextPath() + "/");
        return false;
    }

    @Override
    public void postHandle(HttpServletRequest request,
                           HttpServletResponse response, Object handler,
                           ModelAndView modelAndView) throws Exception {

        super.postHandle(request, response, handler, modelAndView);
    }

    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response, 
                                Object handler, Exception ex)
        throws Exception {

        super.afterCompletion(request, response, handler, ex);
    }
}
```

- src\main\webapp\WEB-INF\spring\appServlet\servlet-context.xml

  - 해당 interceptor가 적용되는 범위 mapping

  - 메소드마다 반복해서 redirect 처리를 해주는 수고를 줄일 수 있음

    ```java
    <!-- ... -->
    	<interceptors>
    		<interceptor>
    			<mapping path="/member/modifyForm"/>
    			<mapping path="/member/removeForm"/>
    			<beans:bean class="com.bs.lec21.member.MemberLoginInterceptor"/>
    		</interceptor>
    	</interceptors>
    ```

  - 멤버 하위에 있는 모든 경로에 대한 interceptor 요청

    - exclude-mapping 에 해당되는 경로는 제외 처리

    ```java
    <!-- ... -->
    	<interceptors>
    		<interceptor>
    			<mapping path="/member/**"/>
    			<exclude-mapping path="/member/joinForm"/>
    			<exclude-mapping path="/member/join"/>
    			<exclude-mapping path="/member/loginForm"/>
    			<exclude-mapping path="/member/login"/>
    			<exclude-mapping path="/member/logout"/>
    			<exclude-mapping path="/member/modify"/>
    			<exclude-mapping path="/member/remove"/>
    		</interceptor>
    	</interceptors>
    ```

<br/>

## DataBase

### 오라클 설치

1. [다운로드](#https://www.oracle.com/database/technologies/xe-downloads.html)

2. 설치

   - setup.exe 실행

3. 계정 생성

   - 명령프롬프트 접속(cmd)

   - ```cmd
     # sqlplus 접속
     C:\> sqlplus
     
     # system 계정 로그인
     C:\> system
          oracle
       
     # 계정 생성, user ID : scott, user PW : tiger
     SQL>  create user scott identified by tiger;
     	    	  
     # 권한(connect, resource 접근 권한 부여)
     SQL> grant connect, resource to scott;
     
     # 계정 삭제
     SQL> drop user scott cascade;
     ```

### SQL developer 설치

1. [다운로드](#https://www.oracle.com/tools/downloads/sqldev-v192-downloads.html)
2. sqldeveloper.exe 실행
   - 초기 실행 시 JDK 경로 설정

<br/>

## JDBC

- 테이블 생성 및 삭제
  - CONSTRAINT : unique value
  - memId_pk PRIMARY KEY : 중복 방지를 위한 기본 키 
  - DEFAULT 0 : default로 0부터 시작
  - memPurNum_ck CHECK (memPurcNum < 3) : 세 번 미만으로 구매할 수 있도록 제한

```sql
CREATE TABLE member (
    memId VARCHAR2(10) CONSTRAINT memId_pk PRIMARY KEY,
    memPw VARCHAR2(10),
    memMail VARCHAR2(15),
    memPurcNum NUMBER(3) DEFAULT 0 CONSTRAINT memPurNum_ck CHECK (memPurcNum < 3)
);
```

- 데이터 삽입

```sql
INSERT INTO member (memId, memPw, memMail)
values ('b', 'bb', 'bbb@gmail.com');
```

- 데이터 조회

```sql
SELECT * FROM member;
```

- 회원 삭제

```sql
DELETE FROM member WHERE memId = 'b';
```

- 테이블 삭제

```sql
DROP TABLE member;
```

### JDBC를 사용한 Oracle 연동

- 의존 설정

  - pom.xml
  
  ```xml
    <!-- ... -->
        <dependency>
            <groupId>com.oracle</groupId>
            <artifactId>ojdbc6</artifactId>
            <version>12.1.0.2</version>
        </dependency>
    <!-- ... ->
    ```
  
- MemberDao.java

  - `드라이버 로딩` -> `DB 연결` -> `SQL 작성 및 전송` -> `자원 해제`
  - 드라이버 로딩, DB 연결, 자원 해제의 중복되는 코드를 보완하기 위해 JdbcTemplate 사용

  ```java
  // ...
  @Repository
  public class MemberDao implements IMemberDao {
  
  	private String driver = "oracle.jdbc.driver.OracleDriver";
  	private String url = "jdbc:oracle:thin:@localhost:1521:xe";
  	private String userid = "scott";
  	private String userpw = "tiger";
  	
  	private Connection conn = null;
  	private PreparedStatement pstmt = null;
  	private ResultSet rs = null;
  	
  	@Override
  	public int memberInsert(Member member) {
  		
  		int result = 0;
  		
  		try {
  			// 드라이버 로딩
  			Class.forName(driver);
  			// Connection 객체
  			conn = DriverManager.getConnection(url, userid, userpw);
  			// SQL 작성
  			String sql = "INSERT INTO member (memId, memPw, memMail) values (?,?,?)";	
  			pstmt = conn.prepareStatement(sql);
  			pstmt.setString(1, member.getMemId());
  			pstmt.setString(2, member.getMemPw());
  			pstmt.setString(3, member.getMemMail());
  			// SQL 전송
  			result = pstmt.executeUpdate();
  		} catch (ClassNotFoundException e) {
  			e.printStackTrace();
  		} catch (SQLException e) {
  			e.printStackTrace();
  		} finally {	 // 자원 해제
  			try {
  				if(pstmt != null) pstmt.close();
  				if(conn != null) conn.close();
  			} catch (SQLException e) {
  				e.printStackTrace();
  			}
  		}
  		
  		return result;
  	}
      
      // ...
  }
  ```

<br/>

## JdbcTemplate

- JDBC의 단점(반복되는 작업)을 보완한 JdbcTemplate	

  - JDBC
    - `드라이버 로딩` -> `DB 연결` -> `SQL 작성 및 전송` -> `자원 해제`
  - JdbcTemplate
    - `JdbcTemplate(드라이버 로딩, DB 연결, 자원 해제)` ->`SQL 작성 및 전송`
- DataSource 클래스
  - 데이터베이스 연결과 관련된 정보를 가지고 있는 DataSource는 스프링 또는 c3p0에 제공하는 클래스를 이용할 수 있음
  - Spring : `org.springframework.jdbc.datasource.DriverManagerDataSource`
  - c3p0 : `com.mchange.v2.c3p0. DriverManagerDataSource` 

### 의존 설정

- pom.xml

  ```xml
  <!-- Oracle JDBC repository 추가 -->
  	<repositories>
          <repository>
              <id>oracle</id>
              <name>ORACLE JDBC Repository</name>
              <url>http://maven.jahia.org/maven2</url>
          </repository>
      </repositories>
  <!-- ... -->
      <!-- DB -->
      <dependency>
          <groupId>com.oracle</groupId>
          <artifactId>ojdbc6</artifactId>
          <version>12.1.0.2</version>
      </dependency>
      <dependency>
          <groupId>com.mchange</groupId>
          <artifactId>c3p0</artifactId>
          <version>0.9.5</version>
      </dependency>
      <dependency>
          <groupId>org.springframework</groupId>
          <artifactId>spring-jdbc</artifactId>
          <version>4.1.6.RELEASE</version>
      </dependency>
  <!-- ... ->
  ```

### Spring DataSource

- Spring DataSource 기본 문법
- MemberDao.java

```java
@Repository
public class MemberDao implements IMemberDao {

	private String driver = "oracle.jdbc.driver.OracleDriver";
	private String url = "jdbc:oracle:thin:@localhost:1521:xe";
	private String userid = "scott";
	private String userpw = "tiger";
	
	private DriverManagerDataSource dataSource;
	private JdbcTemplate template;
	
	public MemberDao() {
		dataSource = new DriverManagerDataSource();
		dataSource.setDriverClassName(driver);
		dataSource.setUrl(url);
		dataSource.setUsername(userid);
		dataSource.setPassword(userpw);
	}
    // ...
}
```

### c3p0 DataSource

- c3p0 DataSource 기본 문법
- MemberDao.java

```java
@Repository
public class MemberDao implements IMemberDao {

	private String driver = "oracle.jdbc.driver.OracleDriver";
	private String url = "jdbc:oracle:thin:@localhost:1521:xe";
	private String userid = "scott";
	private String userpw = "tiger";
	
	private DriverManagerDataSource dataSource;
	private JdbcTemplate template;
	
	public MemberDao() {
		dataSource = new DriverManagerDataSource();
		dataSource.setDriverClass(driver);
		dataSource.setJdbcUrl(url);
		dataSource.setUser(userid);
		dataSource.setPassword(userpw);
	}
    // ...
}
```

### JdbcTemplate 적용(c3p0)

- MemberDao.java

```java
@Repository
public class MemberDao implements IMemberDao {

	private String driver = "oracle.jdbc.driver.OracleDriver";
	private String url = "jdbc:oracle:thin:@localhost:1521:xe";
	private String userid = "scott";
	private String userpw = "tiger";
	
	private DriverManagerDataSource dataSource;
	private JdbcTemplate template;
	
    ////////////////////////////////////////////////
    // 생성자
	public MemberDao() {
		dataSource = new DriverManagerDataSource();
		dataSource.setDriverClass(driver);
		dataSource.setJdbcUrl(url);
		dataSource.setUser(userid);
		dataSource.setPassword(userpw);
        
        template = new JdbcTemplate();
		template.setDataSource(dataSource);
	}
   ////////////////////////////////////////////////
    // memberInsert
    @Override
	public int memberInsert(final Member member) {
		int result = 0;
		
		final String sql = "INSERT INTO member (memId, memPw, memMail) values (?,?,?)";
        
        /* 
        1. template.update 첫 번째 방법
        */
		result = template.update(sql, member.getMemId(), member.getMemPw(), member.getMemMail());
        
        /* 
        2. template.update 두 번째 방법 : PreparedStatementCreator
        */
        result = template.update(new PreparedStatementCreator() {
			
			@Override
			public PreparedStatement createPreparedStatement(Connection conn)
					throws SQLException {
				PreparedStatement pstmt = conn.prepareStatement(sql);
				pstmt.setString(1, member.getMemId());
				pstmt.setString(2, member.getMemPw());
				pstmt.setString(3, member.getMemMail());
				
				return pstmt;
			}
		});
        
        /* 
        3. template.update 세 번째 방법 : PreparedStatementSetter
        */
        result = template.update(sql, new PreparedStatementSetter() {
			
			@Override
			public void setValues(PreparedStatement pstmt) throws SQLException {
				pstmt.setString(1, member.getMemId());
				pstmt.setString(2, member.getMemPw());
				pstmt.setString(3, member.getMemMail());
				
			}
		});
        
        //
        
		return result;
	}
    ////////////////////////////////////////////////
    // memberSelect
    @Override
	public Member memberSelect(final Member member) {
		List<Member> members = null;
		
		final String sql = "SELECT * FROM member WHERE memId = ? AND memPw = ?";
        
        /* 
        1. template.query 첫 번째 방법 : PreparedStatementSetter
        */
        members = template.query(sql, new PreparedStatementSetter() {

            @Override
            public void setValues(PreparedStatement pstmt) throws SQLException {
                pstmt.setString(1, member.getMemId());
                pstmt.setString(2, member.getMemPw());
            }
        }, new RowMapper<Member>() {

            @Override
            public Member mapRow(ResultSet rs, int rowNum) throws SQLException {
                Member mem = new Member();
                mem.setMemId(rs.getString("memId"));
                mem.setMemPw(rs.getString("memPw"));
                mem.setMemMail(rs.getString("memMail"));
                mem.setMemPurcNum(rs.getInt("memPurcNum"));
                return mem;
            }
        });
        
        /* 
        2. template.query 두 번째 방법 : PreparedStatementCreator
        */
        members = template.query(new PreparedStatementCreator() {
			
			@Override
			public PreparedStatement createPreparedStatement(Connection conn)
					throws SQLException {
				PreparedStatement pstmt = conn.prepareStatement(sql);
				pstmt.setString(1, member.getMemId());
				pstmt.setString(2, member.getMemPw());
				return pstmt;
			}
		}, new RowMapper<Member>() {

			@Override
			public Member mapRow(ResultSet rs, int rowNum) throws SQLException {
				Member mem = new Member();
				mem.setMemId(rs.getString("memId"));
				mem.setMemPw(rs.getString("memPw"));
				mem.setMemMail(rs.getString("memMail"));
				mem.setMemPurcNum(rs.getInt("memPurcNum"));
				return mem;
			}
		});
        
        /* 
        3. template.query 세 번째 방법 : RowMapper
        */
        members = template.query(sql, new RowMapper<Member>() {

			@Override
			public Member mapRow(ResultSet rs, int rowNum) throws SQLException {
				Member mem = new Member();
				mem.setMemId(rs.getString("memId"));
				mem.setMemPw(rs.getString("memPw"));
				mem.setMemMail(rs.getString("memMail"));
				mem.setMemPurcNum(rs.getInt("memPurcNum"));
				return mem;
			}
			
		}, member.getMemId(), member.getMemPw());
        
        /* 
        4. template.query 네 번째 방법 : Object[]
        */
        members = template.query(sql, new Object[]{member.getMemId(), member.getMemPw()}, new RowMapper<Member>() {

			@Override
			public Member mapRow(ResultSet rs, int rowNum) throws SQLException {
				Member mem = new Member();
				mem.setMemId(rs.getString("memId"));
				mem.setMemPw(rs.getString("memPw"));
				mem.setMemMail(rs.getString("memMail"));
				mem.setMemPurcNum(rs.getInt("memPurcNum"));
				return mem;
			}
			
		});
        
        //
        
        if(members.isEmpty()) 
			return null;
		
		return members.get(0);
    
    // ...
}
```

<br/>

## Connection-pool

 DataBase connection을 미리 만들어 놓는 방법 -> 서버 부하 최소화

1. c3p0 Module의 ComboPooledDataSource 을 사용하는 방법

   - com.mchange.v2.c3p0.ComboPooledDataSource
   - MemberDao.java

   ```java
   @Repository
   public class MemberDao implements IMemberDao {
       
   	// ...
       
   	private ComboPooledDataSource dataSource;
   	private JdbcTemplate template;
   
       public MemberDao() {
   		dataSource = new ComboPooledDataSource();
   		try {	// DataSource와 유사하지만 dataSource 객체 생성 과정에서 예외처리 필요
   			dataSource.setDriverClass(driver);
   			dataSource.setJdbcUrl(url);
   			dataSource.setUser(userid);
   			dataSource.setPassword(userpw);
   		} catch (PropertyVetoException e) {
   			e.printStackTrace();
   		}
   		
   		template = new JdbcTemplate();
   		template.setDataSource(dataSource);
   	}
   ```

2. Spring 설정파일을 이용한 DataSource 설정

   - servlet-context.xml
     - Spring Container가 만들어질 때 dataSource 객체 생성

   ```xml
   <!-- ... -->
   <beans:bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
       <beans:property name="driverClass" value="oracle.jdbc.driver.OracleDriver" />
       <beans:property name="jdbcUrl" value="jdbc:oracle:thin:@localhost:1521:xe" />
       <beans:property name="user" value="scott" />
       <beans:property name="password" value="tiger" />
       <beans:property name="maxPoolSize" value="200" />
       <beans:property name="checkoutTimeout" value="60000" />
       <beans:property name="maxIdleTime" value="1800" />
       <beans:property name="idleConnectionTestPeriod" value="600" />
   </beans:bean>
   ```

   - MemberDao.java

   ```java
   // ...
   
   @Repository
   public class MemberDao implements IMemberDao {
   
   	private JdbcTemplate template;
   	
   	@Autowired
   	public MemberDao(ComboPooledDataSource dataSource) {
   		this.template = new JdbcTemplate(dataSource);
   	}
       
       // ...
   }
   ```

3. Annotation을 이용하여 Java Config 파일을 이용한 DataSource 설정

   - DBConfig.java

   ```java
   // ...
   
   @Configuration
   public class DBConfig {
   
   	@Bean
   	public ComboPooledDataSource dataSource() throws PropertyVetoException {
   		ComboPooledDataSource dataSource = new ComboPooledDataSource();
   		
   		dataSource.setDriverClass("oracle.jdbc.driver.OracleDriver");
   		dataSource.setJdbcUrl("jdbc:oracle:thin:@localhost:1521:xe");
   		dataSource.setUser("scott");
   		dataSource.setPassword("tiger");
   		dataSource.setMaxPoolSize(200);
   		dataSource.setCheckoutTimeout(60000);
   		dataSource.setMaxIdleTime(1800);
   		dataSource.setIdleConnectionTestPeriod(600);
   		
   		return dataSource;
   
   	}
   	
   }
   ```

   - MemberDao.java 에서의 객체 사용은 Spring 설정파일을 이용한 방법과 동일