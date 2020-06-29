---
layout: post
title: Spring Framework
summary: Let's learn Spring Framework
categories: IT
featured-img: spring
# mathjax: true
---

# Table of Contents

* [개요 소개](#개요 소개)
  * [스프링 개요](#스프링 개요)
* [스프링 프레임워크](#스프링 프레임워크)
  * [개발 환경 구축](#개발 환경 구축)
* [프로젝트 생성](#프로젝트 생성)
  * [test](#test)
* [의존객체](#의존객체)
  * [DI(Dependency injection)](#DI(Dependency injection))
  * [다양한 의존 객체 주입](#다양한 의존 객체 주입)
  * [스프링 설정 파일 분리](#스프링-설정-파일-분리)



# 개요 소개

## 스프링 개요

#### 주요 기능
- DI
- AOP
- MVC
- JDBC

#### 스프링 프레임워크에서 제공하고 있는 모듈
- spring-core : 스프링의 핵심인 DI(Dependency Injection)와 IoC(Inversion of Control)를 제공 
- spring-aop : AOP구현 기능 제공 
- spring-jdbc : 데이터베이스를 쉽게(적은 양의 코드) 다룰 수 있는 기능 제공 
- spring-tx : 스프링에서 제공하는 트랜잭션 관련 기능 제공 
- spring-webmvc : 스프링에서 제공하는 컨트롤러(Controller)와 뷰(View)를 이용한 스프링MVC 구현 기능 제공

#### 스프링 컨테이너(IoC)
- 스프링에서 객체를 생성하고 조립하는 컨테이너(container)로, 
  컨테이너를 통해 생성된 객체를 빈(Bean)이라고 부름
  
# 스프링 프레임워크

## 개발 환경 구축

#### 폴더 및 pom.xml 파일 이해
- pjt project : 스프링 프로젝트
- pjt/src/main/java : .java 파일 관리
  - 앞으로 만들어지는 자바 파일들이 관리되는 폴더이
- pjt/src/main/resources : 자원파일 관리
  - 스프링 설정 파일(XML) 또는 프로퍼티 파일 등이 관리

pom.xml 파일은 메이븐 설정파일로 메이븐은 라이브러리를 연결해주고, 빌드를 위한 플랫폼

pom.xml에 의해서 필요한 라이브러리만 다운로드 해서 사용

# 프로젝트 생성

## test

스프링 방식의 ‘의존’을 이용하기 위해서는 Main에서 TransportationWalk 객체를 직접 생성하지 않고, 스프링 설정 파일(XML)을 이용

가장 큰 차이점은 Java 파일에서 이용한 new 연산자를 이용하지 않고 스프링 설정파일(XML)을 이용

1. 스프링 설정 파일(applicationContext.xml)에 Bean tag로 명시된 tag들이
2. GenericXmlApplicationContext  class에 의해
3.  Spring Containr 안에 객체로 생성
   - DI가 적용된 객체들도 존재
4. 이렇게 생성된 Bean 객체들은 getBean() method로 사용

```xml
<?xml version="1.0" encoding="UTF-8"?>

<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
 		http://www.springframework.org/schema/beans/spring-beans.xsd">

	<!-- 객체(Bean) 등록 -->
	<bean id="tWalk" class="lec03Pjt001.TransportationWalk" />
	
</beans>
```

```java
package lec03Pjt001;

import org.springframework.context.support.GenericXmlApplicationContext;

public class MainClass {

	public static void main(String[] args) {
		
///////////////////////
//일반 java framework
///////////////////////
		// TransportationWalk transportationWalk = new TransportationWalk();
		// transportationWalk.move();
		

///////////////////////
//spring framework
///////////////////////
		// xml 파일을 이용하여 객체를 생성

		/*
		1. 컨테이너 생성
		xml을 사용하므로 GenericXmlApplicationContext class 를 사용
		이 class를 생성할 때, 그 안쪽에 리소스(xml)의 내용을 작성.
		*/
		GenericXmlApplicationContext ctx = 
				new GenericXmlApplicationContext("classpath:applicationContext.xml");
		
		/* 
		컨테이너에서 어떠한 객체를 가져올지 ID와 dataType 을 작성
		*/
		TransportationWalk transportationWalk = ctx.getBean("tWalk", TransportationWalk.class);

		transportationWalk.move();
		
        // 외부 자원은 반환하여 리소스를 남기지 않도록 해준다.
		ctx.close();
	}
}
```

<br>

# 의존객체

## DI(Dependency injection)

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

## 다양한 의존 객체 주입

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

  