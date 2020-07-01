---
layout: post
title: Spring Framework(설정 및 구현)
summary: Let's learn Spring Framework
categories: Spring
featured-img: spring
# mathjax: true
---

# Table of Contents

* [설정 및 구현](#설정-및-구현)
  * [생명주기(Life Cycle)](#생명주기(Life-Cycle)) : afterPropertiesSet(), destroy(), init-method, destroy-method
  * [@Annotation을 이용한 스프링 설정 (.xml to .java)](#@Annotation을-이용한-스프링-설정-I) : @Configuration, @Bean
  * [@Annotation을 이용한 스프링 설정 (분리)](#@Annotation을-이용한-스프링-설정-II) : @import
  * [웹 프로그래밍 설계 모델](#웹-프로그래밍-설계-모델)

<br/>

<br/>

# 설정-및-구현

## 생명주기(Life-Cycle)

빈 객체의 생명주기는 스프링 컨테이너의 생명주기와 같음

1. GenericXmlApplicationContext를 이용한 스프링 컨테이너 초기화(생성)

   - 스프링 컨테이너와 Bean 객체의 생성 시점은 동일
     - 빈 객체 생성 및 주입

   ```java
   GenericXmlApplicationContext ctx = 
       new GenericXmlApplicationContext("classpath:appCtx.xml");
   ```

2. getBean()을 이용한 Bean객체 이용

   ```java
   BookRegisterService bookRegisterService = 
   				ctx.getBean("bookRegisterService", BookRegisterService.class);
   
   BookSearchService bookSearchService = 
   				ctx.getBean("bookSearchService", BookSearchService.class);
   
   MemberRegisterService memberRegisterService = 
   				ctx.getBean("memberRegisterService", MemberRegisterService.class);
   
   MemberSearchService memberSearchService = 
   				ctx.getBean("memberSearchService", MemberSearchService.class);
   ```

3. close()를 이용한 스프링 컨테이너 종료

   - 스프링 컨테이너 소멸(안에 있는 Bean 객체들도 자동 소멸)

   ```java
   ctx.close();
   ```

**Bean 객체 Interface를 이용한 동작**

- InitializingBean Interface : afterPropertiesSet()
  
  - Bean 객체 생성시점에 호출
- DisposableBean Interface : destroy()
  
- Bean 객체 소멸시점에 호출
  
- Ex)

  ```java
  public class BookRegisterService implements InitializingBean, DisposableBean{
  
  	@Autowired
  	private BookDao bookDao;
  	
  	public BookRegisterService() { }
  	
  	public void register(Book book) {
  		bookDao.insert(book);
  	}
  	
  	@Override
  	public void afterPropertiesSet() throws Exception {
          // bean 객체 생성 시점 동작
          // (DB connet, 특정 네트워크 자원 사용 등..)
  		System.out.println("빈(Bean)객체 생성 단계");
  	}
  
  	@Override
  	public void destroy() throws Exception {
          // bean 객체 소멸 시점 동작
  		System.out.println("빈(Bean)객체 소멸 단계");
  	}
  }
  ```

 **속성(init-method, destroy-method)을 이용한 동작**

-  init-method, destroy-method Method 설정

  ```xml
  <bean id="bookRegisterService" class="com.brms.book.service.BookRegisterService" 
        init-method="initMethod" destroy-method="destroyMethod"/>
  ```

- 속성 값과 똑같은 method 생성

  ```java
  public class BookRegisterService {
  
  	@Autowired
  	private BookDao bookDao;
  	
  	public BookRegisterService() { }
  	
  	public void register(Book book) {
  		bookDao.insert(book);
  	}
  
  	public void initMethod() {
  		System.out.println("빈(Bean)객체 생성 단계");
  	}
  	
  	public void destroyMethod() {
  		System.out.println("빈(Bean)객체 소멸 단계");
  	}
  }
  ```

<br/>

## @Annotation을-이용한-스프링-설정-I

.xml 파일을 .java 파일로 변경

- applicationContext.xml

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  
  <beans xmlns="http://www.springframework.org/schema/beans"
  	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  	xsi:schemaLocation="http://www.springframework.org/schema/beans 
   		http://www.springframework.org/schema/beans/spring-beans.xsd">
  
  	<bean id="studentDao" class="ems.member.dao.StudentDao" ></bean>
  	
  	
  	<bean id="registerService" class="ems.member.service.StudentRegisterService">
  		<constructor-arg ref="studentDao" ></constructor-arg>
  	</bean>
  	
  	<bean id="modifyService" class="ems.member.service.StudentModifyService">
  		<constructor-arg ref="studentDao" ></constructor-arg>
  	</bean>
  	
  	<bean id="deleteService" class="ems.member.service.StudentDeleteService">
  		<constructor-arg ref="studentDao" ></constructor-arg>
  	</bean>
  	
  	<bean id="selectService" class="ems.member.service.StudentSelectService">
  		<constructor-arg ref="studentDao" ></constructor-arg>
  	</bean>
  	
  	<bean id="allSelectService" class="ems.member.service.StudentAllSelectService">
  		<constructor-arg ref="studentDao" ></constructor-arg>
  	</bean>
  	
  	<bean id="dataBaseConnectionInfoDev" class="ems.member.DataBaseConnectionInfo">
  		<property name="jdbcUrl" value="jdbc:oracle:thin:@localhost:1521:xe" />
  		<property name="userId" value="scott" />
  		<property name="userPw" value="tiger" />
  	</bean>
  	
  	<bean id="dataBaseConnectionInfoReal" class="ems.member.DataBaseConnectionInfo">
  		<property name="jdbcUrl" value="jdbc:oracle:thin:@192.168.0.1:1521:xe" />
  		<property name="userId" value="masterid" />
  		<property name="userPw" value="masterpw" />
  	</bean>
  	
  	<bean id="informationService" class="ems.member.service.EMSInformationService">
  		<property name="info">
  			<value>Education Management System program was developed in 2015.</value>
  		</property>
  		<property name="copyRight">
  			<value>COPYRIGHT(C) 2015 EMS CO., LTD. ALL RIGHT RESERVED. CONTACT MASTER FOR MORE INFORMATION.</value>
  		</property>
  		<property name="ver">
  			<value>The version is 1.0</value>
  		</property>
  		<property name="sYear">
  			<value>2015</value>
  		</property>
  		<property name="sMonth">
  			<value>1</value>
  		</property>
  		<property name="sDay">
  			<value>1</value>
  		</property>
  		<property name="eYear" value="2015" />
  		<property name="eMonth" value="2" />
  		<property name="eDay" value="28" />
  		<property name="developers">
  			<list>
  				<value>Cheney.</value>
  				<value>Eloy.</value>
  				<value>Jasper.</value>
  				<value>Dillon.</value>
  				<value>Kian.</value>
  			</list>
  		</property>
  		<property name="administrators">
  			<map>
  				<entry>
  					<key>
  						<value>Cheney</value>
  					</key>
  					<value>cheney@springPjt.org</value>
  				</entry>
  				<entry>
  					<key>
  						<value>Jasper</value>
  					</key>
  					<value>jasper@springPjt.org</value>
  				</entry>
  			</map>
  		</property>
  		<property name="dbInfos">
  			<map>
  				<entry>
  					<key>
  						<value>dev</value>
  					</key>
  					<ref bean="dataBaseConnectionInfoDev"/>
  				</entry>
  				<entry>
  					<key>
  						<value>real</value>
  					</key>
  					<ref bean="dataBaseConnectionInfoReal"/>
  				</entry>
  			</map>
  		</property>
  	</bean>
  	
  </beans>
  ```

- MemberConfig.java

  - @Configuration : 이 .java 파일은 스프링 컨테이너를 만드는데 사용될 꺼에요
  - @Bean : 메소드를 이용하여 Bean 객체 생성

  ```java
  package ems.member.configration;
  
  // ...
  
  @Configuration
  public class MemberConfig {
  
  	@Bean
  	public StudentDao studentDao() {
  		return new StudentDao();
  	}
  	
  	@Bean
  	public StudentRegisterService registerService() {
  		return new StudentRegisterService(studentDao());
  	}
  	
  	@Bean
  	public StudentModifyService modifyService() {
  		return new StudentModifyService(studentDao());
  	}
  	
  	@Bean
  	public StudentSelectService selectService() {
  		return new StudentSelectService(studentDao());
  	}
  	
  	@Bean
  	public StudentDeleteService deleteService() {
  		return new StudentDeleteService(studentDao());
  	}
  	
  	@Bean
  	public StudentAllSelectService allSelectService() {
  		return new StudentAllSelectService(studentDao());
  	}
  	
  	@Bean
  	public DataBaseConnectionInfo dataBaseConnectionInfoDev() {
  		DataBaseConnectionInfo infoDev = new DataBaseConnectionInfo();
  		infoDev.setJdbcUrl("jdbc:oracle:thin:@localhost:1521:xe");
  		infoDev.setUserId("scott");
  		infoDev.setUserPw("tiger");
  		
  		return infoDev;
  	}
  	
  	@Bean
  	public DataBaseConnectionInfo dataBaseConnectionInfoReal() {
  		DataBaseConnectionInfo infoReal = new DataBaseConnectionInfo();
  		infoReal.setJdbcUrl("jdbc:oracle:thin:@192.168.0.1:1521:xe");
  		infoReal.setUserId("masterid");
  		infoReal.setUserPw("masterpw");
  		
  		return infoReal;
  	}
  	
  	@Bean
  	public EMSInformationService informationService() {
  		EMSInformationService info = new EMSInformationService();
  		info.setInfo("Education Management System program was developed in 2015.");
  		info.setCopyRight("COPYRIGHT(C) 2015 EMS CO., LTD. ALL RIGHT RESERVED. CONTACT MASTER FOR MORE INFORMATION.");
  		info.setVer("The version is 1.0");
  		info.setsYear(2015);
  		info.setsMonth(1);
  		info.setsDay(1);
  		info.seteYear(2015);
  		info.seteMonth(2);
  		info.seteDay(28);
  		
  		ArrayList<String> developers = new ArrayList<String>();
  		developers.add("Cheney.");
  		developers.add("Eloy.");
  		developers.add("Jasper.");
  		developers.add("Dillon.");
  		developers.add("Kian.");
  		info.setDevelopers(developers);
  		
  		Map<String, String> administrators = new HashMap<String, String>();
  		administrators.put("Cheney", "cheney@springPjt.org");
  		administrators.put("Jasper", "jasper@springPjt.org");
  		info.setAdministrators(administrators);
  		
  		Map<String, DataBaseConnectionInfo> dbInfos = new HashMap<String, DataBaseConnectionInfo>();
  		dbInfos.put("dev", dataBaseConnectionInfoDev());
  		dbInfos.put("real", dataBaseConnectionInfoReal());
  		info.setDbInfos(dbInfos);
  		
  		return info;
  	}
  }
  ```

- Main.java

  ```java
  // Using .xml
  GenericXmlApplicationContext ctx = 
  				new GenericXmlApplicationContext("classpath:applicationContext.xml");
  
  // Using .java
  AnnotationConfigApplicationContext ctx = 
  				new AnnotationConfigApplicationContext(MemberConfig.class);
  ```

<br/>

## @Annotation을-이용한-스프링-설정-II

코드가 길어지면 유지보수에 어려움이 생기므로 파일을 분리해주는 것이 편리

(참고 : Ctrl + Shift + o : 참조되지 않는 패키지 정리)

- 보통 기능별로 분리
  - Dao (Data Access Object)
  - Service
  - DataBase 관련 기능
  - Utility

- .java 파일 분리

    - MemberDaoConfig.java

      ```java
      // ...
      @Configuration
      public class MemberDaoConfig {

        @Bean
        public DataBaseConnectionInfo dataBaseConnectionInfoDev() {
            DataBaseConnectionInfo infoDev = new DataBaseConnectionInfo();
            infoDev.setJdbcUrl("jdbc:oracle:thin:@localhost:1521:xe");
            infoDev.setUserId("scott");
            infoDev.setUserPw("tiger");

            return infoDev;
        }

        @Bean
        public DataBaseConnectionInfo dataBaseConnectionInfoReal() {
            DataBaseConnectionInfo infoReal = new DataBaseConnectionInfo();
            infoReal.setJdbcUrl("jdbc:oracle:thin:@192.168.0.1:1521:xe");
            infoReal.setUserId("masterid");
            infoReal.setUserPw("masterpw");

            return infoReal;
        }
}
      ```
    
- MemberServiceConfig.java
  
  ```java
      // ...
      @Configuration
      public class MemberServiceConfig {
    
    @Bean
        public StudentDao studentDao() {
            return new StudentDao();
        }
    
    @Bean
        public StudentRegisterService registerService() {
            return new StudentRegisterService(studentDao());
        }
    
    @Bean
        public StudentModifyService modifyService() {
            return new StudentModifyService(studentDao());
        }
    
    @Bean
        public StudentSelectService selectService() {
            return new StudentSelectService(studentDao());
        }
    
    @Bean
        public StudentDeleteService deleteService() {
            return new StudentDeleteService(studentDao());
        }
    
    @Bean
        public StudentAllSelectService allSelectService() {
            return new StudentAllSelectService(studentDao());
        }
    }
  ```
  
    - MemberUtilConfig.java

      ```java
  @Configuration
      public class MemberUtilConfig {
      
        // dbInfos 객체에서 필요한 DataBaseConnectionInfo 객체를 @Autowired 로 생성
      @Autowired
        DataBaseConnectionInfo dataBaseConnectionInfoDev;
      
        @Autowired
      DataBaseConnectionInfo dataBaseConnectionInfoReal;
      
        @Bean
      public EMSInformationService informationService() {
            EMSInformationService info = new EMSInformationService();
            info.setInfo("Education Management System program was developed in 2015.");
            info.setCopyRight("COPYRIGHT(C) 2015 EMS CO., LTD. ALL RIGHT RESERVED. CONTACT MASTER FOR MORE INFORMATION.");
            info.setVer("The version is 1.0");
            info.setsYear(2015);
            info.setsMonth(1);
            info.setsDay(1);
            info.seteYear(2015);
            info.seteMonth(2);
            info.seteDay(28);
      
            ArrayList<String> developers = new ArrayList<String>();
        developers.add("Cheney.");
            developers.add("Eloy.");
            developers.add("Jasper.");
            developers.add("Dillon.");
            developers.add("Kian.");
            info.setDevelopers(developers);
      
            Map<String, String> administrators = new HashMap<String, String>();
        administrators.put("Cheney", "cheney@springPjt.org");
            administrators.put("Jasper", "jasper@springPjt.org");
            info.setAdministrators(administrators);
      
            Map<String, DataBaseConnectionInfo> dbInfos = new HashMap<String, DataBaseConnectionInfo>();
        dbInfos.put("dev", dataBaseConnectionInfoDev);
            dbInfos.put("real", dataBaseConnectionInfoReal);
            info.setDbInfos(dbInfos);
      
            return info;
      }
      }
      ```
  
    - Main.java
  
  ```java
      AnnotationConfigApplicationContext ctx = 	         // spring 설정 파일을 나열
                new AnnotationConfigApplicationContext(MemberServiceConfig.class, 
                                                             MemberDaoConfig.class,
                                                             MemberUtilConfig.class);
  ```

- @import Annotation

  - 하나의 파일에 분리된 설정 파일을 import하는 방법

  - MemberServiceConfig.java 에 다른 설정 파일들을 import

    ```java
    // ...
    
    @Configuration
    @Import({MemberDaoConfig.class, MemberUtilConfig.class})
    public class MemberServiceConfig {
    
    	@Bean
    	public StudentDao studentDao() {
    		return new StudentDao();
    	}
    	
    	@Bean
    	public StudentRegisterService registerService() {
    		return new StudentRegisterService(studentDao());
    	}
    	
    	// ...
    	
    }
    ```

  - Main.java

    ```java
    AnnotationConfigApplicationContext ctx =    // 다른 설정 파일들을 import한 파일만 명시
    				new AnnotationConfigApplicationContext(MemberServiceConfig.class);
    ```

<br/>

## 웹-프로그래밍-설계-모델

**스프링 MVC 프레임워크 기반의 웹 프로그래밍 구조**

- Model 1

  - JSP, Servicem DAO 를 한 파일로 관리
    - 개발 속도는 빠르지만 여러 언어를 하나의 문서에 다 작성하다보니 유지보수가 어려움

  <img src="..\post_img\M1.jpg" alt="img" style="zoom: 70%;" />

  - Request
    1. 사용자가 필요한 정보를 WAS에 request
    2. WAS는 필요한 데이터를 DB에 request
  - Response
    1. DB로부터 response한 데이터를 WAS에서 가공한 후
    2. 사용자는 WAS로부터 정보를 response

- Model 2

  - Model 1 의 단점을 보완하기 위해 나온 모델
    - 각 기능을 MVC를 기본으로 모듈화 (쉬운 유지보수)
      - Model : DB와 통신하기 위한 모듈
      - View : 사용자에게 보여주기 위한 모듈
      - Controller : Service(기능)와 View를 컨트롤하기 위한 모듈

  <img src="..\post_img\M2.jpg" alt="img" style="zoom: 70%;" />

  - Request
    1. 사용자가 필요한 정보를 WAS에 request 하면
    2. 먼저 Controller가 사용자에게 필요한 정보를 제공해줄 수 있는 Service(기능)를 컨트롤한 후
    3. Service를 제공해주기 위해 필요한 데이터를 데이터베이스에 request 하기 위해
    4. 데이터베이스 접근을 위한 DAO 모듈에 요청 후 Model 이라는 객체를 통해 DB와 통신
  - Response 
    1. Model 이라는 객체를 통해 DB와 통신하면서 필요한 데이터를 response
    2. Service는 DB로부터 데이터를 response한 후 
    3. Controller는 Service를 response하고
    4. 이 Service를 사용자에게 다시 response해주기 위해
    5. Controller는 View 객체(JSP)를 통해 사용자에게 response



**스프링 MVC framework 설계 구조**

<img src="..\post_img\MVC.jpg" alt="img" style="zoom: 70%;" />

- 사용자는 필요한 정보를 DispatcherServlet에게 요청
- DispatcherServlet은 
  1. 받은 요청을 <u>HandlerMapping</u>에 토스
     - HandlerMapping은 다양한 Controller 중 <u>적합한 Controller를 선택</u>
  2. 다시 <u>HandlerAdapter</u>에 토스
     - HandlerAdapter는 해당 Controller가 가지고 있는 다양한 method 중 <u>적합한 method를 선택</u>
     - Model을 반환
  3. 다음 <u>ViewResolver</u>에 토스
     - ViewResolver는 받은 model(Controller, Method)에 <u>적합한 JSP 문서를 선택</u>
  4. 다음 View에 토스
     - View는 받은 JSP 문서로 response 생성
  5. 사용자에게 response 
- 개발자가 실질적으로 개발해야할 부분은 Controller와 View
  - Controller는 Back-End
  - View는 Front-End



**DispatcherServlet 설정**

Web application 진입의 첫 번째 관문

- web.xml에 servlet 매핑

  ```xml
  <servlet> 
      <servlet-name>서블릿 별칭</servlet-name> 
      <servlet-class>서블릿명(패키지 이름을 포함한 전체서블릿명)</servlet-class> 
  </servlet> 
  
  <servlet-mapping> 
      <servlet-name>서블릿별칭</servlet-name> 
      <url-pattern>/맵핑명</url-pattern> 
  </servlet-mapping>
  ```

- 적용

  ```xml
  <servlet> 
      <servlet-name>appServlet</servlet-name> 
      <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class> 
      <init-param> 
          <param-name>contextConfigLocation</param-name> 
          <param-value>/WEB-INF/spring/appServlet/servlet-context.xml</param-value> 
      </init-param> 
      <load-on-startup>1</load-on-startup> 
  </servlet>
  
  <servlet-mapping> 
      <servlet-name>appServlet</servlet-name> 
      <url-pattern>/</url-pattern> 
  </servlet-mapping>
  ```

  1. DispatcherServlet을 appServlet로 이름을 지정

     - ```xml
       <servlet-name>appServlet</servlet-name> 
       ```

  2. Web 구조에서 사용자로부터 request가 오면 DispatcherServlet을 servlet으로 등록

     - ```xml
       <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
       ```

  3. DispatcherServlet이 등록될 때 init-param, 초기 파라미터에 스프링 설정 파일도 설정

     - spring container가 생성되면 HandlerMapping, HandlerAdapter, ViewResolver도 spring container 안에 자동으로 생성
     - 스프링 설정 파일을 명시하지 않을 경우, 자동으로 appServlet-context.xml 이라는 파일을 설정
       
   - 일반적으로 초기 파라미터로 스프링 설정 파일을 설정
     
     - ```xml
       <param-value>/WEB-INF/spring/appServlet/servlet-context.xml</param-value> 
       ```
  
3. appServlet은 루트(/)에 들어온 모든 기능을 처리
  
     - ```xml
       <servlet-name>appServlet</servlet-name> 
       <url-pattern>/</url-pattern> 
       ```



**Controller 객체**

DispatcherServlet <- HandlerAdapter -> Controller

Controller는 Server, Dao-DB와 연결되어있고 Model, View를 response

- @Controller

  - Controller는 직접 만들어줘야 함

  - servlet-context.xml 스프링 설정 파일에 annotation-driven TAG 추가

    - spring container를 사용하기 위한 여러 class들이 빈 객체로 설정 파일로 존재
    - @Controller annotation 사용을 위함

    ```xml
    <annotation-driven />
    ```

  - Controller로 사용할 객체는 class로 정의하고 class 위헤 @Controller annotation 추가

    - 이 class 파일은 Controller 기능을 수행

    ```java
    @Controller
    public class HomeController {
        // ...
    }
    ```

- @RequestMapping
  - @Controller 안에 있는 method들은 @RequestMapping을 이용하여

  - 사용자로부터 들어오는 요청에 적절한 method가 실행될 수 있도록 매핑

    ```java
    @RequestMapping("/success")
    public string success(Model model) {
        return "success";
    }
    ```

- Model 타입의 파라미터

    - Controller에서 모든 작업이 완료되고 Model과 View를 response하기 위해

        - method의 파라미터로 model 객체 명시

          ```java
          @RequestMapping("/success")
          public string success(Model model) {
              // ...
          }
          ```

        - Model 데이터를 View에서 사용하기 위해 setAttribute()

          ```java
          model.setAttribute("tmpData", "model has data!!")
          ```

    - 개발자는 Model 객체에 데이터를 담아서 DispatcherServlet에 전달할 수 있음
    - DispatcherServler에 전달된 Model데이터는 View에서 가공되어 클라이언트한테 응답



**View 객체**

DispatcherServlet <- ViewResolver-> View

- spring 설정 파일에 InternalResourceViewResolver라는 Bean 객체 생성

  - 해당하는 적합한 View를 선택

  ```xml
  <beans:bean class="org.springframework.web.servlet.view.InternalResourceViewResolver"> 	<beans:property name="prefix" value="/WEB-INF/views/" /> 
  <beans:property name="suffix" value=".jsp" /> 
  </beans:bean>
  ```

- 적합한 View를 선택하는 방법은

  - @Controller 안에 매핑되는 mothod의 return값과

    ```java
    @RequestMapping("/success")
    public string success(Model model) {
        return "success";
    }
    ```

  - InternalResourceViewResolver에서 만들어준 prefix, suffix값이 합쳐져서 
  - /WEB-INF/views/success.jsp 라면 JSP 파일을 찾아주게 된다.



**전체적인 웹프로그래밍 구조**

<img src="..\post_img\structure.jpg" alt="img" style="zoom: 70%;" />