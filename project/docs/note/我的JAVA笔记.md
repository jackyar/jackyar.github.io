# Mybatis

### @Param注解的作用

当SQL语句中有多个参数时, 且方法也有多个参数时. 可以通过param注解给参数命名, 否则只是按参数位置传入

原因：在SQL语句中#{}占位符中的参数只能用JavaBean中的属性，或者Map中的键的名称，否则按参数位置传

**错误实例：**

```java
@Select("select * from user where username = #{name} or id = #{id}")
List<User> queryUserByName(int id, String name);
```

![image-20210725164114140](C:\Users\28531\AppData\Roaming\Typora\typora-user-images\image-20210725164114140.png)

**正确示例：**

```java
// 按参数的位置arg0,arg1,arg2 ... 传入
@Select("select * from user where username = #{arg1} or id = #{arg0}")
List<User> queryUserByName(int id, String name);

// 使用@param注解命名后传入
@Select("select * from user where username = #{username} or id = #{id}")
List<User> queryUserByName(@Param("id") int id, @Param("username") String name);

// 如果参数是JavaBean对象时，同样可以使用JavaBean中的属性名

// 如果传入的是一个Map参数，同样可以使用Map的key值

// 如果参数只有一个基本类型时，可以不用@param参数注解（建议统一使用注解）
@Select("select * from user where username = #{name}")
List<User> queryUserByName(String name);
```

![image-20210725165520521](C:\Users\28531\AppData\Roaming\Typora\typora-user-images\image-20210725165520521.png)



### Log4j.properties的配置信息

- 使用maven导入log4j的依赖jar包

```xml
<dependency>
    <groupId>log4j</groupId>
    <artifactId>log4j</artifactId>
    <version>1.2.17</version>
</dependency>
```

- log4j.properties配置文件

```properties
log4j.rootLogger=DEBUG,console,file

#控制台输出的相关设置
log4j.appender.console = org.apache.log4j.ConsoleAppender
log4j.appender.console.Target = System.out
log4j.appender.console.Threshold=DEBUG
log4j.appender.console.layout = org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=[%c]-%m%n

#文件输出的相关设置
log4j.appender.file = org.apache.log4j.RollingFileAppender
log4j.appender.file.File=./log/mybatis.log
log4j.appender.file.MaxFileSize=10mb
log4j.appender.file.Threshold=DEBUG
log4j.appender.file.layout=org.apache.log4j.PatternLayout
log4j.appender.file.layout.ConversionPattern=[%p][%d{yy-MM-dd}][%c]%m%n

#日志输出级别
log4j.logger.org.mybatis=DEBUG
log4j.logger.java.sql=DEBUG
log4j.logger.java.sql.Statement=DEBUG
log4j.logger.java.sql.ResultSet=DEBUG
log4j.logger.java.sql.PreparedStatement=DEBUG
```

- 在mybatis的设置settings标签中配置

```xml
<setting name="logImpl" value="LOG4J"/>
```



### Lombok插件

**Lombok是一款Java开发的插件，使得Java开发者可以通过其定义的一些注解来消除业务工程中冗长和繁琐的代码，尤其是对于简单Java类模型（POJO）。在开发环境中使用Lombok插件后，Java开发人员可以节省出重复构建，诸如hashCode和equals这样的方法以及各种业务对象模型的accessor和ToString等方法的大量时间。**

- 使用步骤

1、 在idea安装lombok插件

2、 使用maven导入所需要的jar包

```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.18.12</version>
    <scope>provided</scope>
</dependency>
```



**lombok 的常用注解：**

可以放在类上面。	也可以放在字段上面（放在字段上只是对其下面的一个字段有效）

```java
@Getter and @Setter // 生成getter和setter方法
@FieldNameConstants 
@ToString // 生成toString方法
@EqualsAndHashCode // 生成Equals和HashCode方法
@AllArgsConstructor, @RequiredArgsConstructor and @NoArgsConstructor
@Log, @Log4j, @Log4j2, @Slf4j, @XSlf4j, @CommonsLog, @JBossLog, @Flogger, @CustomLog
@Data // 生成所有字段的getter,setter,toString,Equals和HashCode等方法
@Builder
@SuperBuilder
@Singular
@Delegate
@Value
@Accessors
@Wither
@With
@SneakyThrows
@val
@var
experimental @var
@UtilityClass
```



### 多表连接中ResultMap的使用

#### 一对多

- 通过**子查询**的方式

```java
<mapper namespace="com.jackyar.dao.StudentMapper">
    <!--Student表和Teacher表的关联查询-->
    <!--
        实现思路：
            1、先查询到所有的学生信息
            2、根据学生信息中的tid，和查找出的老师信息进行匹配
    -->
    <select id="queryStudent" resultMap="student">
        select * from student
    </select>
    
    <resultMap id="student" type="Student">
        <!--通过注册resultMap管理实体类属性和数据库字段-->
        <!--
            1、 association 对象映射
            2、 collection  集合映射
        -->
        <id property="id" column="id" />
        <result property="name" column="name" />
        <association property="teacher" column="tid" javaType="Teacher" select="queryTeacher" />
    </resultMap>

    <select id="queryTeacher" resultType="Teacher" >
        select * from teacher
        where id = #{id}
    </select>

</mapper>
```

- 根据结果嵌套处理(**联表查询**)

```java
<!--根据查询结果嵌套处理-->
<select id="queryStudentAndTeacher" resultMap="stuInfo">
    SELECT s.id sid, s.name sname, t.name tname
    from student s, teacher t
    WHERE s.tid = t.id;
</select>

<resultMap id="stuInfo" type="Student">
    <id property="id" column="sid" />
    <result property="name" column="sname" />
    <association property="teacher" javaType="Teacher">
        <result property="name" column="tname" />
    </association>
</resultMap>
```

#### 多对一

- 按结果嵌套处理

```java
@Data
public class Student {
    private int id;
    private String name;
    private int tid;
}

@Data
public class Teacher {
    private int id;
    private String name;
    private List<Student> students;
}
```



```java
<mapper namespace="com.jackyar.dao.TeacherMapper">
    <select id="TeacherById" resultMap="teacher">
        SELECT t.id tid, t.name tname, s.name sname, s.id sid
        from student s, teacher t
        WHERE s.tid = #{id};
    </select>

    <resultMap id="teacher" type="Teacher">
        <id property="id" column="tid" />
        <result property="name" column="tname" />
        <collection property="students" ofType="Student" >
            <result property="id" column="sid" />
            <result property="name" column="tname" />
            <result property="tid" column="tid" />
        </collection>
    </resultMap>
</mapper>
        
/*
Teacher( id=1, name=秦老师, 
	students=[
	Student(id=1, name=秦老师, tid=1), 
	Student(id=2, name=秦老师, tid=1), 
	Student(id=3, name=秦老师, tid=1), 
	Student(id=4, name=秦老师, tid=1), 
	Student(id=5, name=秦老师, tid=1)]
)
*/
```

collection和association中**javaTpye**和**ofType**的区别： 

1、javaType 用来指定实体类中（即pojo）中的一些复杂属性的类型

2、ofTpye 用来指定映射到List中的pojo类型（即泛型<>中的约束类型）



### 动态 SQL

**${} 和 #{}两者的区别：**

​	1、${} 类似与statement的字符串拼接sql语句，可能会导致sql注入

​	2、#{} 可防止sql注入，类似与使用preparedStatement参数占位

- if
- choose (when, otherwise)  ==>类似与swithc case只选择一个条件
- trim (where, set)

```xml
<!--
    prefix:在trim标签内sql语句加上前缀。

    suffix:在trim标签内sql语句加上后缀。

    prefixOverrides:指定去除多余的前缀内容

    suffixOverrides:指定去除多余的后缀内容，
    
    如：suffixOverrides=","，去除trim标签内sql语句多余的后缀","。
  -->
```



- foreach

**SQL片段：**使用<sql id="name"></sql>可以在里面写一些重复的sql, 让后<include></include>复用



### Mybatis缓存

MyBatis 内置了一个强大的事务性查询缓存机制，它可以非常方便地配置和定制。MyBatis 3 中的缓存实现进行了许多改进。默认情况下，只启用了本地的会话缓存(值存在一个sqlSession中)，它仅仅对一个会话中的数据进行缓存。 要启用全局的二级缓存，只需要在 SQL 映射文件中添加一行

#### 一级缓存

一级缓存默认开启，只在一次sqlSession中有效，也就是拿到连接到关闭连接这个作用区间。 一级缓存只针对查询有效，当在作用域中出现了set, update, delete操作时，会清空缓存。

#### 二级缓存

- 二级缓存也叫全局缓存， 由于一级缓存的作用域太低所以诞生了二级缓存。
- 二级缓存是基于namespace级别的缓存，一个命名空间对应（即一个dao）,对应一个二级缓存
- 二级缓存的工作机制
  - 一个会话查询一条数据，这个数据就会被放在当前会话中的一级缓存中；
  - 如果当前会话关闭的话，这个会话对应的一级缓存就会清空，但是开启二级缓存后，一级缓存中的数据会被保存的二级缓存中去；
  - 新会话查询信息时，就可以从二级缓存中获取内容；
  - 不同mapper查询出的数据会被放在自己对应的缓存（map）中

1. 在mybatis核心配置文件的settings项中开启缓存。cacheEnabled = true
2. 在对应的mapper标签下方添加<cache />标签即可

```java
<cache
  eviction="FIFO" // 缓存策略
  flushInterval="60000" // 缓存刷新的时间间隔
  size="512" // 缓存中的引用数目
  readOnly="true"/> 
```

这个更高级的配置创建了一个 FIFO 缓存，每隔 60 秒刷新，最多可以存储结果对象或列表的 512 个引用，而且返回的对象被认为是只读的，因此对它们进行修改可能会在不同线程中的调用者产生冲突。

可用的清除策略有：

- `LRU` – 最近最少使用：移除最长时间不被使用的对象。
- `FIFO` – 先进先出：按对象进入缓存的顺序来移除它们。
- `SOFT` – 软引用：基于垃圾回收器状态和软引用规则移除对象。
- `WEAK` – 弱引用：更积极地基于垃圾收集器状态和弱引用规则移除对象。

#### 缓存查询顺序

- 先走二级缓存
- 如果二级缓存没有，则到一级缓存中查找
- 如果二级缓存中也没有的话，则到通过sqlSession连接到数据库中查询

### 字段名与实体类属性名不同

当数据库表中的字段名与java实体类的属性名不一致，导致mybatis不能自动映射:

https://blog.csdn.net/li627528647/article/details/77915661

- 查询语句中为查询字段取与实体类属性名相同的别名
- 使用ResultMap, 指定映射关系

```xml
<resultMap type="User" id="UserResultMap">
		<id column="id" property="id"/>
		<result column="user_name" property="userName"/>
		<result column="user_password" property="userPassword"/>
</resultMap>
```

- 在数据库字段下滑线命名，实体类属性驼峰命名的情况下，开启配置属性mapUnderscoreToCamelCase



# Spring

```xml
<!--Spring依赖jar
 Spring-webmvc会依赖于Spring-beans 和 Spring-core,Spring-aop,spring-web,
spring-expression, spring-context
 因此只需要导入这个webmvc依赖即可
-->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>5.3.8</version>
</dependency>
```

### 优点

- spring是一个开源免费的框架（容器）
- spring是一个轻量级的、非入侵式的框架
- 控制反转（IOC），面向切面（AOP）
- 支持事务的处理和对框架整合的支持



### Spring的配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd">
</beans>
```



### IOC创建对象的方式

不用到源程序中修改不同的操作，只需要对xml配置文件修改，所谓IoC 就是：对象由Spring创建、管理和装配

#### xml配置项

- import导入(可以再一个xml文件中引用其他xml中配置的beans)

  ```xml
  <beans>
      <import resource="services.xml"/>
      <import resource="resources/messageSource.xml"/>
      <import resource="/resources/themeSource.xml"/>
  </beans>
  ```

- 为实例对象其别名

  ```xml
  <!--起别名-->
  <alias name="hello" alias="helloNickname"/>
  <!--
      1、一个bean标签代表一个实例对象
      2、id：表示该对象名
      3、class：表示对象所属的实体类（需要使用全限定类名）
      4、name: 也可通过name属性起别名（使用, ; 空格的分开）
  -->
  <bean id="hello" class="com.jackyar.pojo.Hello" name="AnotherName,AnotherName2">
      <!--bean注入-->
      <property name="str" value="Hello Spring"/>
  </bean>
  
  <bean id="hello2" class="com.jackyar.pojo.Hello">
      <!-- 构造器注入 -->
      <constructor-arg name="str" value="有参str"/>
  </bean>
  ```



### 依赖注入

象仅通过构造函数参数、工厂方法的参数或对象实例在构造或构造后设置的属性来定义它们的依赖项

**依赖注入方式：**

- 基于构造函数的依赖注入
- 基于setter方法的依赖注入

**bean | ref | idref | list | set | map | props | value | null** 

```xml
<bean id="moreComplexObject" class="example.ComplexObject">
    <!-- results in a setAdminEmails(java.util.Properties) call -->
    <property name="adminEmails">
        <props>
            <prop key="administrator">administrator@example.org</prop>
            <prop key="support">support@example.org</prop>
            <prop key="development">development@example.org</prop>
        </props>
    </property>
    <!-- results in a setSomeList(java.util.List) call -->
    <property name="someList">
        <list>
            <value>a list element followed by a reference</value>
            <ref bean="myDataSource" />
        </list>
    </property>
    <!-- results in a setSomeMap(java.util.Map) call -->
    <property name="someMap">
        <map>
            <entry key="an entry" value="just some string"/>
            <entry key ="a ref" value-ref="myDataSource"/>
        </map>
    </property>
    <!-- results in a setSomeSet(java.util.Set) call -->
    <property name="someSet">
        <set>
            <value>just some string</value>
            <ref bean="myDataSource" />
        </set>
    </property>
</bean>
```

- 使用p命名空间和c命名空间注入依赖

```xml
<bean id="hello" class="com.jackyar.pojo.Hello"
          p:str="hello spring"/>
    <bean id="teacher" class="com.jackyar.pojo.Teacher"
          p:name="catalina" p:age="26"/>

    <!--p命名空间相当与setter注入，p可理解为对property的简写-->
    <bean id="user" class="com.jackyar.pojo.User"
          p:age="18" p:name="jackyar" p:hello-ref="hello" p:teacher-ref="teacher"/>

    <!--c命名空间相当与构造方法注入，c可理解为对constructor的简写-->
    <bean id="userC" class="com.jackyar.pojo.User"
          c:name="用户1" c:age="23" c:hello-ref="hello" c:teacher-ref="teacher"/>
```



### 自动装配

设置autowire的属性为：byName或者byTpye

**byName:  **会自动在容器上下文中查找，和自己对象set方法后值对应的 beanid

**byType:  **   会自动在容器上下文中查找，和自己对象属性类型相同的bean

 (byType可以不加id, 但是该类型实例对象在context中只能存在唯一的一个，否则报错！！！)

```xml
<bean id="userOutoName" class="com.jackyar.pojo.User" autowire="byName"
          p:name="yuhang-autoByName" p:age="21"/>

<bean id="userOutoType" class="com.jackyar.pojo.User" autowire="byType"
          p:name="yuhang-autoByType" p:age="22"/>
```



### 注解自动装配

1. 配置xml条件约束

   ```xml
   <beans xmlns="http://www.springframework.org/schema/beans"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:p="http://www.springframework.org/schema/p"
          xmlns:c="http://www.springframework.org/schema/c"
          <!--1-->
          xmlns:context="http://www.springframework.org/schema/context"
          xsi:schemaLocation="http://www.springframework.org/schema/beans
          https://www.springframework.org/schema/beans/spring-beans.xsd
   	   <!--2-->
          http://www.springframework.org/schema/context
          https://www.springframework.org/schema/context/spring-context.xsd">
   </beans>
   ```

2. 添加注解上下文配置项

   ```xml
    <context:annotation-config/> 
   ```

3. 在bean实体类的属性上添加@AutoWired注解

   ```java
   public class User {
       private String name;
       private Integer age;
       @Autowired
       private Hello hello;
       @Autowired
       private Teacher teacher;
   }
   ```
   
   `@Autowired`: 按照类型注入,多个类型使用变量名来判定注入的bean.   
   
   ` @Qualifiler`: 配合@Autoeired注解完成注入,一起使用,使用该注解指定注入的名称.
   
   

**@resource注解和@AutoWired注解的区别：**

- @resource注解也可以实现自动装配，它是JDK原生的注解，在javax.annotation包下。默认通过byName的方式查找，如果找不到则通过byType方式。否则报错
- @AutoWired注解是spring的自动装配注解，通过byName方式查找；如果找不到就报错。



### 常用的注解

1. 在xml中导入context配置，添加一个组件引用的配置项

   ```xml
   <!--扫描注解组件-->
   <context:component-scan base-package="com.jackyar.pojo"/>
   ```

2. 使用注解注入bean

   **@Component**写在类上方，表示对象注入到SpringIoC容器中

   **@Value**写属性上方，表示为bean对象装配值

   ```java
   @Component
   public class Hello {
       @Value("Hello Annotation")
       private String str;
   }
   ```

3. 衍生注解

   与@Component功能相同，在web开发中会按照mvc三层架构分层. 表示将某个类注册到Spring, 装配bean

   - dao层 **@Repository**
   - service层 **@Service**
   - controller层 **@Controller**

4. 自动装配注解

   **@AutoWired**  

5. 作用域注解

   使用**@Scope**注解声明作用域（singleton单例，prototype原型）

   ```java
   @Component
   @Scope("singleton")
   public class Hello {
       @Value("Hello Annotation")
       private String str;
   }
   ```

   ![image-20210729084919916](C:\Users\28531\AppData\Roaming\Typora\typora-user-images\image-20210729084919916.png)

6. xml与注解的区别
   - xml是万能的，使用与任何场景，且方便后期维护
   - 注解不是自己的类使用不了
   - 可以两者结合使用，使用xml管理bean, 使用注解注入`属性`



### 可以直接使用Java类注册bean

- 效果与xml中配置的效果相同

```java
@Configuration
public class AppConfig {

    @Bean
    public TransferServiceImpl transferService() {
        return new TransferServiceImpl();
    }
}
```

- 引用配置

```java
public static void main(String[] args) {
    ApplicationContext ctx = new AnnotationConfigApplicationContext(SystemTestConfig.class);
    // everything wires up across configuration classes...
    TransferService transferService = ctx.getBean(TransferService.class);
    transferService.transfer(100.00, "A123", "C456");
}
```



### 动态代理

- 可以使用真实角色操作更加纯粹，不用再去关注公共的业务
- 公共也就是交由一个代理角色去处理业务，实现不同业务的分工
- 当公共业务发生扩展时方便集中管理
- 动态代理类代理的时一个接口，只负责对应的一类业务即可
- 动态代理类可以代理多个不同的业务类，前提时这些业务实现了统一接口

**编写动态代理类实现InvocationHandler**

```java
public class ProxyInvocationHandler implements InvocationHandler {
    private Object target;

    public ProxyInvocationHandler(Object target) {
        this.target = target;
    }

    public void setTarget(Object target){
        this.target = target;
    }

    public Object getProxy(){
        return Proxy.newProxyInstance(this.getClass().getClassLoader(), target.getClass().getInterfaces(), this);
    }

    // 代理对象要执行的具体方法
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        log(method.getName());
        Object invoke = method.invoke(target, args);
        return invoke;
    }

    public void log(String methodName){
        System.out.println("[debug] 成功调用" + methodName + "方法");
    }
}
```

**具体调用获取动态生成的代理对象，实现业务功能**

```java
public class Client {
    public static void main(String[] args) {
        UserServiceImpl userService = new UserServiceImpl();
        ProxyInvocationHandler handler = new ProxyInvocationHandler(userService);
        UserService proxy = (UserService) handler.getProxy();
        proxy.add();
    }
}
```



### spring实现Aop

- 使用Aop织入，需要导入依赖包

  ```xml
  <dependency>
      <groupId>org.aspectj</groupId>
      <artifactId>aspectjweaver</artifactId>
      <version>1.9.4</version>
  </dependency>
  ```

#### 使用原生Spring API 实现

- 在配置文件注入bean对象，并声明aop

  - xml格式声明

  ```xml
  <beans xmlns="http://www.springframework.org/schema/beans"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xmlns:p="http://www.springframework.org/schema/p"
         xmlns:c="http://www.springframework.org/schema/c"
         xmlns:context="http://www.springframework.org/schema/context"
         <!--1-->
         xmlns:aop="http://www.springframework.org/schema/aop"
         
         xsi:schemaLocation="http://www.springframework.org/schema/beans
         https://www.springframework.org/schema/beans/spring-beans.xsd
  	   <!--2-->
         http://www.springframework.org/schema/aop
         https://www.springframework.org/schema/aop/spring-aop.xsd
  
         http://www.springframework.org/schema/context
         https://www.springframework.org/schema/context/spring-context.xsd">
  ```

  - bean对象与aop的声明

  ```xml
  <!--注入bean对象-->
      <bean name="beforeLog" class="com.jackyar.log.BeforeLog"/>
      <bean name="userServiceImpl" class="com.jackyar.service.UserServiceImpl"/>
      <bean name="afterLog" class="com.jackyar.log.AfterLog"/>
      <!--aop配置-->
      <aop:config>
          <!--需要执行的切入点-->
          <!--
          For example : 'execution(* com.xyz.myapp.service.*.*(..))'
          * 可理解为表示包下的所有类 和 类中的所有方法
  
          .. 可理解为表示方法中所有参数
          -->
          <aop:pointcut id="userServiceCut" expression="execution(* com.jackyar.service.UserServiceImpl.*(..))"/>
          <aop:advisor advice-ref="beforeLog" pointcut-ref="userServiceCut"/>
          <aop:advisor advice-ref="afterLog" pointcut-ref="userServiceCut"/>
      </aop:config>
  ```

- 在切入点（方法）前面添加新功能  **实现MethodBeforeAdvice接口**

```java
public class BeforeLog implements MethodBeforeAdvice {
    /**
     * 动态代理，在被执行方法之前执行的功能
     * @param method 被执行的方法
     * @param args 被执行方法的参数
     * @param target 被执行方法所在的类具体实现类
     * @throws Throwable
     */
    public void before(Method method, Object[] args, Object target) throws Throwable {
        System.out.println(method.getClass().getClass() + "的" + method.getName() + "执行之前执行");
    }
}
```

- 在切入点（方法）后面添加新功能 **AfterReturningAdvice接口**

```java
public class AfterLog implements AfterReturningAdvice {
    /**
     * 动态代理，在被执行方法之后执行的功能
     * @param returnValue 被执行方法的返回值
     * @param method 正在被执行的方法
     * @param args 正在被执行的方法的参数
     * @param target 正在被执行的方法所属的类
     * @throws Throwable
     */
    public void afterReturning(Object returnValue, Method method, Object[] args, Object target) throws Throwable {
        System.out.println(method.getClass().getClass() + "的" + method.getName() + "执行之后执行");
    }
}
```

- 执行测试

```java
@Test
    public void testAop_01(){
        ApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml");
        // AOP面向切面是动态代理，需要代理接口
        UserService userService = context.getBean("userServiceImpl", UserService.class);
        userService.query();
    }
```

![image-20210729173506804](C:\Users\28531\AppData\Roaming\Typora\typora-user-images\image-20210729173506804.png)



#### 使用自定义类实现acpect

```java
public class MyLogsAspect {
    public void before(){
        System.out.println("[debug] == 在方法执行前执行 ==");
    }

    public void after(){
        System.out.println("[debug] == 在方法执行后执行 ==");
    }
}
```

```xml
<!--自定义类实现AOP-->
    <bean id="myLogsAspect" class="com.jackyar.log.MyLogsAspect"/>

    <aop:config>
        <aop:aspect id="logs" ref="myLogsAspect">
            <aop:pointcut id="userServiceCut" expression="execution(* com.jackyar.service.UserServiceImpl.*(..))"/>
            <aop:before method="before" pointcut-ref="userServiceCut"/>
            <aop:after method="after" pointcut-ref="userServiceCut"/>
        </aop:aspect>
    </aop:config>
```



#### 使用注解实现

需要先声明注解自动配置

```xml
<!--
    proxy-target-class="false" 使用JDK原生代理（Proxy类 和 InvocationHandler）
    proxy-target-class="true"  使用cglib代理
    -->
    <aop:aspectj-autoproxy/>
    <bean name="annotationAspect" class="com.jackyar.log.AnnotationAspect"/>
```

@Around环绕注解、**@Before** 、**@After**

```java
@Aspect
public class AnnotationAspect {
    @Before("execution(* com.jackyar.service.UserServiceImpl.*(..))")
    public void before(){
        System.out.println("[debug] == 在方法执行前执行 ==");
    }

    @After("execution(* com.jackyar.service.UserServiceImpl.*(..))")
    public void after(){
        System.out.println("[debug] == 在方法执行后执行 ==");
    }
}
```



### spring整合mybatis的使用

- 需要导入spring-jdbc的依赖包 引入mybatis-spring的依赖jar包

``` xml
<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis-spring</artifactId>
    <version>2.0.6</version>
</dependen
```

- 将mybatis的配置文件注入到spring中

```xml
<bean name="datasource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
    <property name="driverClassName" value="com.mysql.cj.jdbc.Driver"/>
    <property name="url" value="jdbc:mysql://localhost:3306/mybatisdb?useSSL=false&amp;serverTimezone=UTC"/>
    <property name="username" value="root"/>
    <property name="password" value="123456"/>
</bean>

<bean name="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
    <property name="dataSource" ref="datasource"/>
    <property name="configLocation" value="classpath:mybatis-config.xml"/>
    <property name="mapperLocations" value="classpath:com/jackyar/dao/*.xml"/>
</bean>

<bean name="sqlSession" class="org.mybatis.spring.SqlSessionTemplate">
    <constructor-arg index="0" ref="sqlSessionFactory"/>
</bean>
```

- 由于spring中不需要new对象，所有需要写一个接口的实现类注册到spring容器中调用

```java
public class UserMapperImpl implements UserMapper {
    // 需要注入到sping
    private SqlSessionTemplate sqlSessionTemplate;

    public void setSqlSessionTemplate(SqlSessionTemplate sqlSessionTemplate) {
        this.sqlSessionTemplate = sqlSessionTemplate;
    }

    public List<User> queryUser() {
        return sqlSessionTemplate.getMapper(UserMapper.class).queryUser();
    }
}
```

- 或者继承更简洁的**SqlSessionDaoSupport**类

```java
public class UserMapperImpl_02 extends SqlSessionDaoSupport implements UserMapper {

    public List<User> queryUser() {
        return getSqlSession().getMapper(UserMapper.class).queryUser();
    }
}
```



### spring的事务管理

- 声明式事务
- 编程式事务

#### 声明式事务

```xml
<!--使用spring实现事务管理-->
<!--
    1、配置声明式事务
-->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <constructor-arg ref="datasource" />
</bean>

<!--配置事务通知  propagation:表示事务的传播方式-->
<tx:advice id="userQueryTx" transaction-manager="transactionManager">
    <tx:attributes>
        <tx:method name="queryUser" propagation="REQUIRED"/>
    </tx:attributes>
</tx:advice>

<!--使用Aop切入事务-->
<aop:config>
    <aop:pointcut id="queryUserPoint" expression="execution(* com.jackyar.dao.UserMapper.*(..))"/>
    <aop:advisor advice-ref="userQueryTx" pointcut-ref="queryUserPoint"/>
</aop:config>
```





# SpringMVC

### 案例（原生非注解方式）

- 在xml中配置映射器、适配器 、视图解析器和 Handler

```xml
<!--处理器映射器-->
<bean class="org.springframework.web.servlet.handler.BeanNameUrlHandlerMapping"/>
<!--处理器适配器-->
<bean class="org.springframework.web.servlet.mvc.SimpleControllerHandlerAdapter"/>

<!--视图解析器-->
<bean id="internalResourceViewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver">
    <!--前缀-->
    <property name="prefix" value="static/"/>
    <!--后缀-->
    <property name="suffix" value=".jsp"/>
</bean>

<!--Handler-->
<bean id="/hello" class="com.jackyar.controller.HelloController"/>
```

- 编写**controller**处理业务和视图跳转

```java
public class HelloController implements Controller {
    public ModelAndView handleRequest(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse) throws Exception {
        ModelAndView view = new ModelAndView();
        view.addObject("message", "HelloSpringMVC");
        view.setViewName("login");
        return view;
    }
}
```

- 在web.xml中配置**DispatcherServlet**

```xml
<servlet>
    <servlet-name>springmvc</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <!--配置DispatcherServlet启动要绑定的spring配置文件
    即，要注入bean初始化DispatcherServlet的内置参数
    -->
    <init-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath:springmvc-servlet.xml</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
    <servlet-name>springmvc</servlet-name>
    <url-pattern>/</url-pattern>
</servlet-mapping>
```



### 使用注解开发

```xml
<!--自动扫描包，让指定包下的注解生效，交由IOC容器管理-->
<context:component-scan base-package="com.jackyar.controller"/>
<!--让Spring MVC不处理静态资源-->
<mvc:default-servlet-handler/>
<!--开启SpringMVC注解-->
<mvc:annotation-driven/>
<!--视图解析器-->
<bean id="internalResourceViewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver">
    <!--前缀-->
    <property name="prefix" value="/static/"/>
    <!--后缀-->
    <property name="suffix" value=".jsp"/>
</bean>
```

- 在类的上方使用**@Controller**注解，将controller类注册到bean中, 类中的所有方法统一走视图解析器。如果使用**@RestController**则不走视图，返回json字符串。（或者在方法中使用**@ResponseBody**）
- **@RequestMapping**在方法前声明，表示映射地址处理的业务程序（相当于一个servlet地址）。如果注解在类的上方页声明了，则两个地址嵌套（类上方的为上一级地址）
- Controller类中写对应地址需要处理的方法，方法统一返回String（相应页面的jsp文件名）

```java
@Controller
public class AnnoHelloController {
    @RequestMapping("anno")
    public String annotationHello(Model model){
        model.addAttribute("message", "Hello Annotation");
        return "login";
    }
```



### RESTFUL 风格

这种风格的地址参数不是以 参数名=参数值显示url， 而是以斜线分割不同参数，根据不同的请求方式请求服务。

方法中的地址参数使用**@PathVariable**注解声明

```java
@RequestMapping("restful/{a}/{b}")
public String mappingUrl(@PathVariable int a, @PathVariable int b, Model model){
    model.addAttribute("message", "RESTFUL=> " + a + " " + b);
    return "login";
}
```

- 不同的请求方式，对应不同的方法执行

```java
@RequestMapping(value = "restful/{a}/{b}", method = RequestMethod.GET)

GET, HEAD, POST, PUT, PATCH, DELETE, OPTIONS, TRACE;
```

```java
// 两者等价
@GetMapping("restful/{a}/{b}") 
@RequestMapping(value = "restful/{a}/{b}", method = RequestMethod.GET)
```



### 解决请求乱码问题

- 使用SpingMVC提供的**CharacterEncodingFilter**乱码过滤器  ( url要匹配所有刚需 /* )

```xml
<!--配置springmvc乱码过滤器-->
<filter>
    <filter-name>encoding</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <init-param>
        <param-name>encoding</param-name>
        <param-value>utf-8</param-value>
    </init-param>
</filter>
<filter-mapping>
    <filter-name>encoding</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```



### JSON的使用

- 使用Jackson解析

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-core</artifactId>
    <version>2.12.3</version>
</dependency>
```

- 配置JSON乱码

```xml
<!--开启SpringMVC注解-->
<mvc:annotation-driven >
    <!--配置JSON乱码问题-->
    <mvc:message-converters register-defaults="true">
        <bean class="org.springframework.http.converter.StringHttpMessageConverter">
            <constructor-arg value="UTF-8"/>
        </bean>
        <bean class="org.springframework.http.converter.json.MappingJackson2HttpMessageConverter">
            <property name="objectMapper">
                <bean class="org.springframework.http.converter.json.Jackson2ObjectMapperFactoryBean">
                    <property name="failOnEmptyBeans" value="false"/>
                </bean>
            </property>
        </bean>
    </mvc:message-converters>
</mvc:annotation-driven>
```

- 编写Controller、使用**@RestController**则不走视图，返回字符串。或者在方法中使用**@ResponseBody**

```java
@Controller
public class JsonController {
    @RequestMapping("json1")
    @ResponseBody
    public String json1() throws JsonProcessingException {
        ObjectMapper mapper = new ObjectMapper();
        HashMap<String, String> map = new HashMap<String, String>();
        map.put("hello1", "中国");
        map.put("hello2", "世界");
        map.put("hello3", "开源");
        return mapper.writeValueAsString(map);
    }
}
```

![image-20210801110010181](C:\Users\28531\AppData\Roaming\Typora\typora-user-images\image-20210801110010181.png)



- 也可使用阿里巴巴的FastJson, fastjson更简洁

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>1.2.58</version>
</dependency>
```

```java
@RequestMapping("json2")
public String json2() throws JsonProcessingException {
    HashMap<String, String> map = new HashMap<String, String>();
    map.put("hello1", "中国");
    map.put("hello2", "FastJson");
    map.put("hello3", "开源");

    return JSON.toJSONString(map);
}
```



### 拦截器

核心思想是aop，本质是在请求处理方法的前后切入新功能。实现**HandlerInterceptor**的类，就是拦截器

```java
public class MyInterceptor implements HandlerInterceptor {
    /*
        前置拦截器，在请求处理前执行
        return true;表示可以通过
        return false; 表示被拦截
     */
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        System.out.println("======请求处理前=====");
        return true;
    }

    /*
        在请求处理后执行
     */
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println("======请求处理后=====");
    }

    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        System.out.println("======请求处理后，清理资源=====");
    }
}
```

配置拦截器。**表示拦截所有请求的方法

```xml
<!--配置拦截器-->
<mvc:interceptors>
    <mvc:interceptor>
        <mvc:mapping path="/**/"/>
        <bean class="com.jackyar.filter.MyInterceptor"/>
    </mvc:interceptor>
</mvc:interceptors>
```



### 文件上传和下载

```xml
<dependency>
    <groupId>commons-fileupload</groupId>
    <artifactId>commons-fileupload</artifactId>
    <version>1.3.3</version>
</dependency>
```





# SpringBoot2

https://www.yuque.com/atguigu/springboot



### 配置maven镜像和环境参数

- 配值本地的maven文件setting.xml, 使用阿里云镜像 和 配置JDK版本
- Spring Boot 2.5.3 的最低maven版本 3.5+

```xml
<mirrors>
  <mirror>
    <id>nexus-aliyun</id>
    <mirrorOf>central</mirrorOf>
    <name>Nexus aliyun</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public</url>
  </mirror>
</mirrors>

<profiles>
     <profile>
          <id>jdk-1.8</id>
          <activation>
            <activeByDefault>true</activeByDefault>
            <jdk>1.8</jdk>
          </activation>
          <properties>
            <maven.compiler.source>1.8</maven.compiler.source>
            <maven.compiler.target>1.8</maven.compiler.target>
            <maven.compiler.compilerVersion>1.8</maven.compiler.compilerVersion>
          </properties>
     </profile>
</profiles>
```



### 导入spingboot需要的依赖包

```xml
<!--引入springboot的父工程-->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.5.3</version>
</parent>

<!--导入web开发所需要的依赖包-->
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>

<!--这个插件会将整个项目打包成可执行的jar包-->
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
        </plugin>
    </plugins>
</build>
```



### 快速开始

- 项目的启动的主方法，不需要xml依赖，作为整个程序的主入口

```java
/**
 * 主程序类
 * @SpringBootApplication：这是一个SpringBoot应用
 *
 * 可以使用 @EnableAutoConfiguration @ComponentScan() 两个注解代替 SpringBootApplication
 */
@SpringBootApplication
public class MainApplication {

    public static void main(String[] args) {
        SpringApplication.run(MainApplication.class,args);
    }
}
```

- 简化配置，整个项目的配置写在**application.properties 或者 application.yml**中
- 简化部署，不需要安装和配置tomcat, 内部集成
- springboot有自动版本仲裁机制，引入依赖默认都可以不写版本。但是如果引入非仲裁版本的jar包需要说明版本号 （springboot的所有仲裁版本都在 <artifactId>spring-boot-dependencies</artifactId> ）
- 修改工程中某些组件的版本 (例如：)

```xml
<properties>
	<mysql.version>5.7.12</mysql.version>
</properties>
```



### starter场景启动器

starter是一组方便的依赖描述符，可以获得所需的所有 Spring 和相关技术的一站式服务。所有**官方**首发都遵循类似的命名模式；`spring-boot-starter-*`，其中`*`是特定类型的应用程序。

![image-20210814150122253](C:\Users\28531\AppData\Roaming\Typora\typora-user-images\image-20210814150122253.png)

### 添加容器组件

使用 @Configuration类注解定义配置类， 并在方法上使用@Bean注解表示一个容器组件。

```java
@Configuration
/**
 * proxyBeanMethods默认=true
 * 保证每个@Bean方法被调用多少次返回的组件都是单实例的
 *
 * @Configuration(proxyBeanMethods = false)
 * 每个@Bean方法被调用多少次返回的组件都是新创建的
 */
public class MyConfig {

    @Bean("tom")
    public Pet pet(){
        return new Pet("tomcat");
    }

    @ConditionalOnBean(name = "tom")
    @Bean
    public User user(){
        return new User("yuhang", 18, pet());
    }
}
```



### yml 配置文件

- key: value；kv之间有空格
- 大小写敏感
- 使用缩进表示层级关系
- 缩进不允许使用tab，只允许空格
- 缩进的空格数不重要，只要相同层级的元素左对齐即可
- '#'表示注释
- 字符串无需加引号，如果要加，''与""表示字符串内容 会被 转义/不转义
- yaml可以给实体类赋值 
  - 通过 @ConfigrationPropertis(prefix = "yaml中配置的父级名") 绑定配置，实现自动赋值
  - @PropertySource(value = "classpath: xxx.properties")

```xml
<!--配置文件配置自己的类时，弹出提示-->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-configuration-processor</artifactId>
    <optional>true</optional>
</dependency>
```

项目打包时，排除这个包，不是程序运行的依赖包

```xml
<!--这个插件会将整个项目打包成可执行的jar包-->
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <configuration>
                <!--项目打包时需要排除的包-->
                <excludes>
                    <exclude>
                        <groupId>org.springframework.boot</groupId>
                        <artifactId>spring-boot-configuration-processor</artifactId>
                    </exclude>
                </excludes>
            </configuration>
        </plugin>
    </plugins>
</build>
```



### restful风格的使用与原理

-  *GET-*获取用户  *DELETE-删除用户*     *PUT-修改用户*      *POST-保存用户*

- 核心Filter；HiddenHttpMethodFilter

  - 用法： 表单method=post，隐藏域 _method=put
  - SpringBoot中手动开启

  ``` yaml
  spring:
    mvc:
      hiddenmethod:
        filter:
          enabled: true   #开启页面表单的Rest功能
  ```

  

Rest原理（表单提交要使用REST的时候）

- 表单提交会带上**_method=PUT**
- **请求过来被**HiddenHttpMethodFilter拦截

- 请求是否正常，并且是POST

- 获取到**_method**的值。
- 兼容以下请求；**PUT **.**DELETE** .**PATCH**

- **原生request（post），包装模式requesWrapper重写了getMethod方法，返回的是传入的值。**
- **过滤器链放行的时候用wrapper。以后的方法调用getMethod是调用 ** **requesWrapper的。**



### JSR303数据校验

```java
@ConfigurationProperties(prefix = "user") // 表示类可以通过yaml配置文件赋值
@Validated // 开启数据校验功能
public class User { 
    @NotNull // 表示属性的值非空
    private String name;
    private Integer age;
    private Pet pet;
}
```

- 常见的校验注解

```java
// 空检查
@Null		// 验证对象是否为空
@NotNull	// 验证对象是否为null, 无法检查长度为0的字符串
@NotBlank	// 检查约束字符串是不是Null 还有被Trim的长度是否大于0， 只对字符串起作用，且会去掉前后空格
@NotEmpty	// 检查约束元素是否为Null 或者是Empty.

// Boolean检查
@AssertTrue		// 验证Boolean 对象是否为true
@AssertFalse 	// 验证Boolean 对象是否为false

// 长度检查
@Size(min=, max=) 	// 验证对象（Array, Collection, Map, String）长度是否在给定的范围内
@Length(min=, max)	// 验证String的长度是否在给定长度

// 日期检查
@Past		// 验证 Date 和 Calendar 对象是否在当前时间之前
@Future		// 验证 Date 和 Calendar 对象是否在当前时间之后
@Pattern 	// 验证 String 对象是否符合正则表达式的规则
```

- 需要导入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```



### 静态资源访问路径

![image-20210817172821007](C:\Users\28531\AppData\Roaming\Typora\typora-user-images\image-20210817172821007.png)

默认路径下的优先级：**resource > static > public**



### Thymeleaf 模板引擎

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

简单的表达：

- 变量表达式： `${...}`
- 选择变量表达式： `*{...}`
- 消息表达： `#{...}`
- 链接 URL 表达式： `@{...}`   **url表达式中的 / 表示当前项目的根目录**
- 片段表达式： `~{...}`



头部声明

```html
<html lang="en" xmlns:th="http://www.thymeleaf.org">
```



### 页面国际化

1. 配置i18n文件
2. 如果需要通过按钮自动切换中英文状态，需要自定义一个组件
3. 最后将自己组件配置放到 spring 容器中 @Bean



### @Bean 容器注入对象

在使用java配置类时，通过@Bean注解为 Spring  容器注入对象

bean对象的名字默认 **方法名** ，也可以通过@Bean的name属性自定义名称

```java
@Configuration
public class MyConfig implements WebMvcConfigurer {

    @Bean
    public LocaleResolver localeResolver(){
        return new MyLocaleResolve();
    }
}
```



### 定制化功能

编写自定义配置类，可在容器中增加组件，扩展和增加功能。

- web应用中，实现 WebMvcConfigurer 即可定制化web功能

```java
@Configuration
public class MyConfig implements WebMvcConfigurer {
    // 视图控制别名
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/main.html").setViewName("dashboard");
        registry.addViewController("/index.html").setViewName("index");
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LoginHandlerInterceptor()).addPathPatterns("/**")
                .excludePathPatterns("/index.html", "/", "/user/login", "/css/**", "/js/**", "/img/**", "/user/query");
    }

    @Bean
    public LocaleResolver localeResolver(){
        return new MyLocaleResolve();
    }
}
```



### 注入web原生组件

1、 注解方式（使用原生 Servlet, Filter, Listener）

- @ServletComponentScan(basePackages = **"com.atguigu.admin"**) :指定原生Servlet组件位置（标记在主程序上面）
- @WebServlet(urlPatterns = **"/my"**)：效果：直接响应，**不会经过Spring的拦截器？**
- @WebFilter(urlPatterns={**"/css/\*"**,**"/images/\*"**})    /* 是原生写法， /**是spring的写法
- @WebListener

2、 通过**xxxxRegistrationBean**

- ServletRegistrationBean (HttpServlet)
- FilterRegistrationBean (Filter)
- ServletListenerRegistrationBean (ServletContextListener)



### Swagger 

```xml
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger2</artifactId>
    <version>2.10.5</version>
</dependency>

<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>
    <version>2.10.5</version>
</dependency>

```

- 配置swagger





![image-20210809152526014](C:\Users\28531\AppData\Roaming\Typora\typora-user-images\image-20210809152526014.png)



/** 拦截所有请求，包括静态资源

![image-20210808165211761](C:\Users\28531\AppData\Roaming\Typora\typora-user-images\image-20210808165211761.png)





# SpringCloud

![image-20211007233425645](C:\Users\28531\AppData\Roaming\Typora\typora-user-images\image-20211007233425645.png)

