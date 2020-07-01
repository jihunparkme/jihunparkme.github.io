---
layout: post
title: Spring Framework(설정 및 구현)
summary: Let's learn Spring Framework
categories: IT
featured-img: spring
# mathjax: true
---

# Table of Contents

* [설정 및 구현](#설정-및-구현)
  * [생명주기(Life Cycle)](#생명주기(Life-Cycle)) : afterPropertiesSet(), destroy(), init-method, destroy-method
  * [@Annotation을 이용한 스프링 설정](#@Annotation을-이용한-스프링-설정) : @Configuration, @Bean

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

## @Annotation을-이용한-스프링-설정

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

  