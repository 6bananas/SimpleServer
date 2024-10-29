create database `simpleserver`;

use `simpleserver`;

create table machine(
    id int comment '饮水机ID' primary key,
    location varchar(100) not null comment '位置',
    tds double not null comment '水质',
    state int not null comment '状态'
)engine=InnoDB default charset=utf8;

create table drink(
    id int auto_increment comment '编号' primary key,
    cardnumber int not null comment '校园卡号',
    machineid int not null comment '饮水机ID',
    time datetime not null comment '饮水时间',
    consumption int not null comment '饮水量',
    foreign key (machineid) references machine(id)
)engine=InnoDB default charset=utf8;

insert into machine
values
(2001, '图书馆', 99.8, 1),
(2002, '教学楼', 97.1, 1);

insert into drink
(cardnumber, machineid, time, consumption)
values
(2101, 2001, '2024-07-07 09:27:03', 500),
(2101, 2001, '2024-07-07 09:30:10', 200);

