create table item(id int primary key not null auto_increment,product_name varchar(20) not null,product_price int(7) not null, product_qty int(4) not null,created_at datetime not null)  default charset=utf8;

create table member(id varchar(20) not null primary key,email varchar(50) not null, name varchar(20) not null,pwd varchar(20) not null,created_at datetime not null) default charset=utf8;

create table orders(id int primary key not null auto_increment,member_id varchar(20) not null,item_id int(6) not null, item_name varchar(20) not null,order_qty int(4) not null, order_price int(8) not null,created_at datetime not null) default charset=utf8;

insert into member(id,pwd,email,name,created_at) values('admin','admin1234','admin','admin',now());
