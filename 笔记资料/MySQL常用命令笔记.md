# CTF中 MySQL 常用命令笔记

## 登录命令

### 登录命令语法格式

```my
mysql -u用户名 [-h主机名] -p密码 [-P端口号] [-D数据库名] [-eMySQL命令] [-S socket文件名]
```

参数说明：

（1）【-u用户名】或者【–user=用户名】：指定用户登录的用户名；
（2）【-p密码（p小写）】或者【–password=密码】：输入登录密码；
（3）【-h主机名或ip地址】或者【–host=主机名ip地址】：指定登录的主机名；
（4）【-P端口号（P大写）】或者【–port=端口号】：指定登录的MySQL的端口号；
（5）【-D数据库名】或者【–database=数据库名】：指定登录的数据库名称；
（6）【-S socket文件名】或者【–socket=socket文件名】：指定登录时使用的socket文件名。
（7）【-e MySQL命令】或者【–execute= MySQL命令】：在不登录MySQL的情况下执行MySQL命令。

### 登录本地数据库

如果需要登录本地数据库，只需要指定用户名（-u）和密码（-p）即可，不需要指定主机名（-h），命令如下：

```mysql
#mysql -uroot -proot
```

### 登录远程数据库

如果希望登录远程数据库服务器，则必须在远程的MySQL服务器中创建登录账号并授予相应的访问权限。然后使用（-h）参数指定远程服务器的IP地址，使用（-P）参数指定远程服务器中MySQL的端口号。命令如下：

```mysql
mysql -uusername -h192.168.1.11 -ppassword -P3306
```

### 登录指定的数据库

可以使用 `show databases` 查看MySQL服务器中的数据库，然后使用 `use [数据库名]` 切换到指定数据库，也可以直接使用下面名登录到指定数据库：

```mysql
mysql -uroot -proot -D[数据库名]
```

### 使用（-e）参数在不登录MySQL的情况下执行MySQL命令

```mysql
mysql -uroot -p -e "use [数据库名]; select * from [数据库名].[表名];"
```

## 库操作

### 创建数据库

命令：`create database <数据库名>`

例如：建立一个名为 sqlroad 的数据库

`mysql> create database sqlroad;`

### 显示所有的数据库

命令：`show databases` （注意：最后有个s）

`mysql> show databases;`

### 删除数据库

命令：`drop database <数据库名>`

例如：删除名为 sqlroad的数据库

`mysql> drop database sqlroad;`

### 导出数据库

一般形式：

```mysql
mysqldump -h IP -u 用户名 -p -d 数据库名 > 导出的文件名

参数解析：
-h:表示host地址
-u:表示user用户
-p:表示password密码
-d:表示不导出数据
```

例如：

- 导出数据库结构和数据（此时不用加-d），如下导出库dbtest中所有表结构和数据

  ```mysql
  - mysqldump -h 192.168.182.134 -u root -p dbtest > C:\Users\Administrator\Desktop\users2.sql
  ```

  只导出数据库表结构（此时要加-d），如下导出库dbtest中的users表结构没有数据

  ```mysql
  mysqldump -h 192.168.182.134 -u root -p -d dbtest > C:\Users\Administrator\Desktop\users2.sql
  ```

- 导出某张表结构和数据（此时不用加-d），如下导出库dbtest中的users表结构和数据

  ```mysql
  - mysqldump -h 192.168.182.134 -u root -p dbtest users > C:\Users\Administrator\Desktop\users2.sql
  ```

- 导出某张表结构（此时要加-d），如下导出库dbtest中的users表结构

  ```mysql
  mysqldump -h 192.168.182.134 -u root -p -d dbtest users > C:\Users\Administrator\Desktop\users2.sql
  ```

  **注意：**

```mysql
（1）-p 后面不能加password，只能单独输入数据库名称
（2）mysqldump是在cmd下的命令，不能再mysql下面，即不能进入mysql的（如果进入了mysql，得exit退出mysql后才可以的。）
```

### 导入数据库

**1.已经建好数据库，导入数据库文件**

- 首先登录并进入数据库：


```mysql
本地访问：
mysql -h localhost -u root -p
远程访问：
mysql -h 192.168.182.120 -uroot -p
参数解析：
-h:表示host地址，本地直接使用localhost，远程需要使用ip地址
-u:表示user用户
-p:表示password密码
```

**2.登录成功后执行导入命令source+文件路径：**

```mysql
source C:\Users\Administrator\Desktop\users2.sql
```

### 连接数据库

命令：`use <数据库名>`

例如：如果sqlroad数据库存在，尝试存取它：

`mysql> use sqlroad;`

屏幕提示：Database changed

### 查看当前使用的数据库

`mysql> select database();`

### 当前数据库包含的表信息

`mysql> show tables;` （注意：最后有个s）

## 表操作

<!--操作之前应链接某个数据库-->

### 建表

命令：`create table <表名> ( <字段名> <类型> [,..<字段名n> <类型n>]);`

```mysql
mysql> create table MyClass(

> id int(4) not null primary key auto_increment,

> name char(20) not null,

> sex int(4) not null default ’′,

> degree double(16,2));
```



### 获取表结构

命令：`desc 表名，或者show columns from 表名`

```mysql
mysql>DESCRIBE MyClass

mysql> desc MyClass;

mysql> show columns from MyClass;
```



### 删除表

命令：`drop table <表名>`

例如：删除表名为 MyClass 的表

`mysql> drop table MyClass;`

### 插入数据

命令：`insert into <表名> [( <字段名>[,..<字段名n> ])] values ( 值 )[, ( 值n )]`

例如，往表 MyClass中插入二条记录, 这二条记录表示：编号为的名为Tom的成绩为.45, 编号为 的名为Joan 的成绩为.99，编号为 的名为Wang 的成绩为.5.

```mysql
mysql> insert into MyClass values(1,’Tom’,96.45),(2,’Joan’,82.99), (2,’Wang’, 96.59);
```

## 查询表中的数据

### 查询所有行

命令：`select <字段，字段，...> from < 表名 > where < 表达式 >`

例如：查看表 MyClass 中所有数据

`mysql> select * from MyClass;`

### 查询前几行数据

例如：查看表 MyClass 中前行数据

`mysql> select * from MyClass order by id limit 0,2;`

或者：

`mysql> select * from MyClass limit 0,2;`

### 删除表中数据

命令：`delete from 表名 where 表达式`

例如：删除表 MyClass中编号为 的记录

`mysql> delete from MyClass where id=1;`

### 修改表中数据

`update 表名 set 字段=新值,…where 条件`

`mysql> update MyClass set name=’Mary’where id=1;`

### 在表中增加字段

命令：`alter table 表名 add字段 类型 其他;`

例如：在表MyClass中添加了一个字段passtest，类型为int(4)，默认值为

`mysql> alter table MyClass add passtest int(4) default ’′`

### 更改表名

命令：`rename table 原表名 to 新表名;`

例如：在表MyClass名字更改为YouClass

`mysql> rename table MyClass to YouClass;`

### 更新字段内容

`update 表名 set 字段名 = 新内容`

`update 表名 set 字段名 = replace(字段名,’旧内容’, 新内容’)`

`update article set content=concat(‘　　’,content);`

## 字段类型

### 字段类型

**1．INT[(M)] 型：**正常大小整数类型

**2．DOUBLE[(M,D)] [ZEROFILL] 型：**正常大小(双精密)浮点数字类型

**3．DATE 日期类型：**支持的范围是-01-01到-12-31。MySQL以YYYY-MM-DD格式来显示DATE值，但是允许你使用字符串或数字把值赋给DATE列

**4．CHAR(M) 型：**定长字符串类型，当存储时，总是是用空格填满右边到指定的长度

**5．BLOB TEXT类型：**最大长度为(2^16-1)个字符。

**6．VARCHAR型：**变长字符串类型

## MySQL数据库的授权

```mysql
mysql>grant select,insert,delete,create,drop

on *.* (或test.*/user.*/..)

to 用户名@localhost

identified by ‘密码’；
```

如：新建一个用户帐号以便可以访问数据库，需要进行如下操作：

```mysql
mysql> grant usage

　　-> ON test.*

　　-> TO testuser@localhost;
```

此后就创建了一个新用户叫：testuser，这个用户只能从localhost连接到数据库并可以连接到test 数据库。下一步，我们必须指定testuser这个用户可以执行哪些操作：

```mysql
mysql> GRANT select, insert, delete,update

　　-> ON test.*

　　-> TO testuser@localhost;
```

此操作使testuser能够在每一个test数据库中的表执行SELECT，INSERT和DELETE以及UPDATE查询操作。

## DDL操作

### 查看现在的数据库中存在什么表

```mysql
mysql> SHOW TABLES;
```

### 显示表的结构

```mysql
mysql> DESCRIBE MYTABLE;
```

### 用文本方式将数据装入数据库表中（例如D:/mysql.txt）

```mysql
mysql> LOAD DATA LOCAL INFILE “D:/mysql.txt”INTO TABLE MYTABLE;
```

### 更新表中数据

```mysql
mysql>update MYTABLE set sex=”f”where name=’hyq’;
```

## MySQL读写文件

### 读取文件

- **load_file()**

  ```mysql
  select cast(load_file('/flag') as char);#输出格式转化为字符
  select convert(load_file("/flag"),char);#输出格式转化为字符
  ```

- **load data infile**

  ```mysql
  load data infile '/tmp/1.txt' into table user;
  ```

- **system cat**

  MySQL 版本为5.x时，支持此操作，此方法只能在本地读取，远程连接时无法使用，无法越权读取。

  ```mysql
  system cat /flag.txt
  ```

### 写入文件

- **SELECT…INTO OUTFILE**

  前提条件

  1. 目标目录要有可写权限
  2. 当前数据库用户要有FILE权限
  3. 目标文件不能已存在
  4. secure_file_priv的值为空
  5. 路径完整

  ```mysql
  select load_file("/etc/passwd") into outfile "/tmp/passwd";
  ```
