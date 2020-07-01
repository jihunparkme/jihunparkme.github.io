---
layout: post
title: Spring Framework(의존객체)
summary: Let's learn Spring Framework
categories: IT
featured-img: spring
# mathjax: true
---

# Table of Contents

* [의존객체](#의존객체)
  * [DI(Dependency injection)](#DI(Dependency-injection))
  * [다양한 의존 객체 주입](#다양한-의존-객체-주입) : constructor-arg(생성자), setter, List Type, Map Type
  * [스프링 설정 파일 분리](#스프링-설정-파일-분리) : Singleton, Prototype
  * [의존객체 자동 주입](#의존객체-자동-주입) : @Autowired, @Resource
  * [의존객체 선택](#의존객체-선택) : qualifier Tag, @Qualifier, @Inject

<br/>

<br/>

# 의존객체

## DI(Dependency-Injection)

의존성 주입

**Example)**

- 장난감 배터리 주입 (in Java)

```java
// 배터리 일체형 장난감
public class ElectronicCarToy {
    private Battery battery;

    public ElectronicCarToy() {
        // 생성자에서 주입
        battery = new NormalBattery(); 
    }
}

// 배터리 분리형 장난감
public class ElectronicRobotToy {
    private Battery battery;
    
    public ElectronicRobotToy() {
        // 배터리가 들어있지 않은 빈 장난감
    }
    
    public void setBattery(Battery battery) {
        // 필요 시 setBattery() method를 사용하여 배터리 주입
    	this.battery = battery;	
    }
}

// 배터리 분리형 장난감(구매 시 건전지 포함)
public class ElectronicRadioToy {
    private Battery battery;
    
    public ElectronicRadioToy(Battery battery) {
        // 배터리가 들어있는 장난감
    	this.battery = battery; 
    }
    
    public void setBattery(Battery battery) {
        // 필요 시 setBattery() method를 사용하여 배터리 주입
    	this.battery = battery; 
    }
}
```

**DI ?**

- 한 객체를 다른 객체가 생성될 때 주입

**Java VS Spring (생성자에서 주입)**

- Java

```java
/*
ems.member.assembler.StudentAssembler.java
*/
public class StudentAssembler {

	//..
	
	public StudentAssembler() {
		studentDao = new StudentDao();
        // registerService, modifyService 는 studentDao 객체의 의존(의존 주입)
		registerService = new StudentRegisterService(studentDao);
		modifyService = new StudentModifyService(studentDao);
		deleteService = new StudentDeleteService(studentDao);
		selectService = new StudentSelectService(studentDao);
		allSelectService = new StudentAllSelectService(studentDao);
	}

	// ...
}

// ems.member.service.StudentRegisterService.java
	private StudentDao studentDao;

	public StudentRegisterService(StudentDao studentDao) {
		this.studentDao = studentDao;
	}
// ems.member.service.StudentModifyService.java
	private StudentDao studentDao;
	
	public StudentModifyService(StudentDao studentDao) {
		this.studentDao = studentDao;
	}
// ems.member.service.StudentDeleteService.java
	private StudentDao studentDao;
	
	public StudentDeleteService(StudentDao studentDao) {
		this.studentDao = studentDao;
	}
// ems.member.service.StudentSelectService.java
	private StudentDao studentDao;
	
	public StudentSelectService(StudentDao studentDao) {
		this.studentDao = studentDao;
	}
// ems.member.service.StudentAllSelectService.java
	private StudentDao studentDao;
	
	public StudentAllSelectService(StudentDao studentDao) {
		this.studentDao = studentDao;
	}

    
/*
ems.member.main.MainClass.java
*/

StudentAssembler assembler = new StudentAssembler();

StudentRegisterService registerService = assembler.getRegisterService();
		
StudentModifyService modifyService = assembler.getModifyService();

StudentSelectService selectService = assembler.getSelectService();
				
StudentAllSelectService allSelectService = assembler.getAllSelectService();
```

- Spring

```xml
<!-- 
src/main/resources/applicationContext.xml
 -->

<?xml version="1.0" encoding="UTF-8"?>

<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
 		http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!-- Dao 객체 생성 -->
	<bean id="studentDao" class="ems.member.dao.StudentDao" ></bean>
	
    <!-- constructor-arg tag를 이용한 StdentDao 객체 주입 -->
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
    
	<!-- ... -->
    
</beans>
```

```java
/* 
ems.member.main.MainClassUseXML.java
*/

GenericXmlApplicationContext ctx = 
				new GenericXmlApplicationContext("classpath:applicationContext.xml");

StudentRegisterService registerService = 
    ctx.getBean("registerService", StudentRegisterService.class);

StudentModifyService modifyService  = ctx.getBean("modifyService", StudentModifyService.class);

StudentSelectService selectService = ctx.getBean("selectService", StudentSelectService.class);

StudentAllSelectService allSelectService = 
    ctx.getBean("allSelectService", StudentAllSelectService.class);
```

<br/>

## 다양한-의존-객체-주입

1. 생성자를 이용한 의존 객체 주입 (constructor-arg TAG)

   - Java

   ```java
   public StudentRegisterService(StudentDao studentDao) {
       this.studentDao = studentDao;
   }
   
   public StudentModifyService(StudentDao studentDao) {
       this.studentDao = studentDao;
   }
   
   public StudentDeleteService(StudentDao studentDao) {
       this.studentDao = studentDao;
   }
   
   public StudentSelectService(StudentDao studentDao) {
       this.studentDao = studentDao;
   }
   
   public StudentAllSelectService(StudentDao studentDao) {
       this.studentDao = studentDao;
   }
   ```

   - Spring

   ```xml
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
   ```

2. setter를 이용한 의존 객체 주입

   - Java 

   ```java
   public void setJdbcUrl(String jdbcUrl) {
   	this.jdbcUrl = jdbcUrl;
   }
   public void setUserId(String userId) {
   	this.userId = userId;
   }
   public void setUserPw(String userPw) {
   	this.userPw = userPw;
   }
   
   ```

   - Spring

   ```xml
   <bean id="dataBaseConnectionInfoDev" class="ems.member.DataBaseConnectionInfo">
   	<property name="jdbcUrl" value="jdbc:oracle:thin:@localhost:1521:xe" />
   	<property name="userId" value="scott" />
   	<property name="userPw" value="tiger" />
   </bean>
   ```

3. List타입 의존 객체 주입

   - Java

   ```java
   public void setDevelopers(List<String> developers) {
   	this.developers = developers;
   }
   ```

   - Spring

   ```xml
   <property name="developers">
       <list>
           <value>Cheney.</value>
           <value>Eloy.</value>
           <value>Jasper.</value>
           <value>Dillon.</value>
           <value>Kian.</value>
       </list>
   </property>
   
   ```

4. Map 타입 객체 주입

   - Java

   ```java
   public void setAdministrators(Map<String, String> administrators) {
   	this.administrators = administrators;
   }
   ```

   - Spring

   ```xml
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
   ```

<br/>

## 스프링-설정-파일-분리

기능이 추가되면서 xml 파일이 길어지는 것을 방지하기 위해 기능별로 xml 파일을 분리

1.여러 xml 파일을 배열 형태로 불러서 사용

- applicationContext.xml (Original)

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

- appService.xml

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
  	
  </beans>
  ```

- appDatabase.xml

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  
  <beans xmlns="http://www.springframework.org/schema/beans"
  	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  	xsi:schemaLocation="http://www.springframework.org/schema/beans 
   		http://www.springframework.org/schema/beans/spring-beans.xsd">
  
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
  	
  </beans>
  ```

- appInfo.xml

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  
  <beans xmlns="http://www.springframework.org/schema/beans"
  	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  	xsi:schemaLocation="http://www.springframework.org/schema/beans 
   		http://www.springframework.org/schema/beans/spring-beans.xsd">
  
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

- Main.java

  ```java
  String[] appCtxs =
  	{"classpath:appCtx1.xml", "classpath:appCtx2.xml", "classpath:appCtx3.xml"};
  GenericXmlApplicationContext ctx = new GenericXmlApplicationContext(appCtxs);
  ```

2.여러 xml 파일을 import 하여 사용

- appCtximport.xml

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  
  <beans xmlns="http://www.springframework.org/schema/beans"
  	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  	xsi:schemaLocation="http://www.springframework.org/schema/beans 
   		http://www.springframework.org/schema/beans/spring-beans.xsd">
  
  	<import resource="classpath:appDatabase.xml"/>
  	<import resource="classpath:appInfo.xml"/>
  
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
  	
  </beans>
  ```

- Main.java

  ```java
  enericXmlApplicationContext ctx =  
      new GenericXmlApplicationContext("classpath:appCtxImport.xml");
  ```

**빈(Bean)의 범위**

- 싱글톤(Singleton) : 
  - 스프링 컨테이너에서 생성된 빈(Bean)객체의 경우 동일한 타입에 대해서는 기본적으 로 한 개만 생성이 되며, getBean() 메소드로 호출될 때 동일한 객체가 반환
  - 객체를 여러 번 생성하더라고 동일한 객체를 공유

- 프로토타입(Prototype) :

  - 싱글톤 범위와 반대의 개념도 있는데 이를 프로토타입(Prototype) 범위라고 한다. 프로토타입의 경우 개발자는 별도로 설정을 해줘야 하는데, 스프링 설정 파일에서 빈 (Bean)객체을 정의할 때 scope속성을 명시해 주면 된다.
  - 객체를 호출할 때마다 다른 객체로 생성하고 싶은 경우

  ```xml
  <bean id="injectionBean" class="scope.ex.InjectionBean" />
  	
  <bean id="dependencyBean" class="scope.ex.DependencyBean" scope="prototype">
      <constructor-arg ref="injectionBean" />
      <property name="injectionBean" ref="injectionBean" />
  </bean>
  ```

<br/>

## 의존객체-자동-주입

- 의존객체 자동 주입 : 
  - 스프링 설정 파일에서 의존 객체를 주입할 때  또는  태그로 의존 대상 객체를 명시하지 않아도 스프링 컨테이너 가 자동으로 필요한 의존 대상 객체를 찾아서 의존 대상 객체가 필요한 객체에 주입해 주는 기능
  - 구현 방법은 @Autowired와 @Resource 어노테이션을 이용해서 쉽게 구현
  - 실무에서도 많이 사용(주로 @Autowired)

- @Autowired

  - 주입하려고 하는 **객체의 타입**이 일치하는 객체를 자동으로 주입

  - @Autowired가 적용되어 있는 구문에 필요한 객체의 데이터 타입을 가지고 있는 Bean 객체를 Ctx.xml 에서 찾고, 알맞는 데이터 타입을 넣어 주는 방식

    - appCtx.xml

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    
    <beans xmlns="http://www.springframework.org/schema/beans"
    	xmlns:context="http://www.springframework.org/schema/context" <!-- +추가 -->
    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    	xsi:schemaLocation="http://www.springframework.org/schema/beans 
     		http://www.springframework.org/schema/beans/spring-beans.xsd  <!-- +추가 -->
     		http://www.springframework.org/schema/context  <!-- +추가 -->
     		http://www.springframework.org/schema/context/spring-context.xsd" <!-- +추가 -->>
    
    	<context:annotation-config /> <!-- +추가 --> 
    
    	<bean id="wordDao" class="com.word.dao.WordDao" />
    	<bean id="registerService" class="com.word.service.WordRegisterServiceUseAutowired" />
    	<!-- constructor-arg ref="wordDao" /> -제거 -->
    	<bean id="searchService" class="com.word.service.WordSearchServiceUseAutowired" />
    	<!-- constructor-arg ref="wordDao" /> -제거 -->
    	
    </beans>
    ```

    - java

    ```java
    // WordRegisterService.java
    
    	@Autowired
    	public WordRegisterService(WordDao wordDao) {
    		this.wordDao = wordDao;
    	}
    
    // WordSearchService.java
    
        @Autowired
        public WordSearchService(WordDao wordDao) {
    		this.wordDao = wordDao;
    	}
    ```

  - property나 method에 @Autowired 사용 시 default 생성자 필요

    ```java
    	@Autowired
    	private WordDao wordDao;
    	
    	public WordRegisterService() {
    	}
    
    	@Autowired
    	public void setWordDao(WordDao wordDao) {
    		this.wordDao = wordDao;
    	}
    ```

- @Resource 

  - 주입하려고 하는 **객체의 이름**이 일치하는 객체를 자동으로 주입

  - 생성자에서는 사용할 수 없고, property나 method에 사용 가능

  - property나 method에 적용하기 위해서는 default 생성자 필요

  - 객체가 일단 생성되어야 property나 method에 자동주입이 가능하므로

    - appCtx.xml 은 @Autowired 과 동일
    - Java

    ```java
    	@Resource
    	private WordDao wordDao;
    	
    	public WordRegisterService() {
    	}
    
    	@Resource
    	public void setWordDao(WordDao wordDao) {
    		this.wordDao = wordDao;
    	}
    ```

<br/>

## 의존객체-선택

다수의 빈(Bean)객체 중 의존 객체의 대상이 되는 객체를 선택하는 방법

- 동일한 객체가 2개 이상인 경우 스프링 컨테이너는 자동 주입 대상 객체를 판단하지 못해서 Exception을 발생

- Problem

  - WordDao라는 class로부터 여러 객체가 만들어 질 경우 (.xml)

    ```xml
    <bean id="wordDao1" class="com.word.dao.WordDao" />
    <bean id="wordDao2" class="com.word.dao.WordDao" />
    <bean id="wordDao3" class="com.word.dao.WordDao" />
    ```

  - property WordDao DataType의 wordDao를 @Autowired를 이용하여 자동주입 할 경우 (.java)

    ```java
    @Autowired
    private WordDao wordDao;
    ```

  - 어떤 Bean 객체를 주입해야할지 모르기 때문에 Exception 발생

    ```console
    No qualifying bean of type [com.word.dao.WordDao] is defined: expected single matching bean but found 3: wordDao1,wordDao2,wordDao3     
    
    expected single matching bean but found 3: wordDao1,wordDao2,wordDao3
    ```

- Solution

  - qualifier Tag 사용 (.xml)

    ```xml
    <bean id="wordDao1" class="com.word.dao.WordDao" >
        <qualifier value="usedDao"/>
    </bean>
    <bean id="wordDao2" class="com.word.dao.WordDao" />
    <bean id="wordDao3" class="com.word.dao.WordDao" />
    ```

  - Qualifier annotation 사용 (.java)

    ```java
    @Autowired
    @Qualifier("usedDao")
    private WordDao wordDao;
    ```

**@Inject**

- @Autowired와 거의 비슷하게 @Inject 어노테이션을 이용해서 의존 객체를 자동으로 주입

- @Autowired와 차이점 이라면 @Autowired의 경우 required 속성을 이용해서 의존 대상 객체가 없어도 익셉션을 피할 수 있지만, @Inject의 경우 required 속성을 지원하지 않음

- @Autowired은 qualifier Tag를 사용했지만 @Inject는 Bean객체 ID만 명시

  ```xml
  <bean id="wordDao1" class="com.word.dao.WordDao" />
  <bean id="wordDao2" class="com.word.dao.WordDao" />
  <bean id="wordDao3" class="com.word.dao.WordDao" />
  ```

  ```java
  @Inject
  @Named(value = "wordDao1")
  private WordDao wordDao;
  ```

<br/>
