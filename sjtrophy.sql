drop database if exists sjtrophy;
create database sjtrophy;
use sjtrophy;

CREATE TABLE branch (
	b_id		integer AUTO_INCREMENT,
    mgr_id		integer not null,
    primary key (b_id)
);

CREATE TABLE coupon (
	coup_id		integer AUTO_INCREMENT,
    exp_date	date,
    discount	decimal(4,2) not null,
    branch		integer,
    primary key (coup_id)
);

ALTER TABLE coupon AUTO_INCREMENT=1000;
ALTER TABLE coupon add foreign key (branch) references branch(b_id);

CREATE TABLE employee (
	e_id		integer AUTO_INCREMENT,
    e_name		varchar(50) not null,
    e_addr		varchar(100),
    e_phone		varchar(10),
    e_pw        varchar(100),
    branch		integer,
    sup_id		integer,
    primary key	(e_id),
    foreign key (branch) references branch(b_id),
    foreign key (sup_id) references employee(e_id)
);

ALTER TABLE branch add foreign key (mgr_id) references employee(e_id);
ALTER TABLE employee AUTO_INCREMENT=100;

CREATE TABLE design (
	d_id		integer AUTO_INCREMENT,
    d_size		varchar(5),
    d_font		varchar(20),
    d_text		varchar(100),
    d_price		decimal(5,2),
    primary key (d_id)
);

CREATE TABLE item (
	i_id		integer AUTO_INCREMENT,
    i_type		varchar(20),
	count		integer,
    i_price		decimal(6,2),
    branch      integer,
    primary key	(i_id),
    foreign key (branch) references branch(b_id)
);

CREATE TABLE customer (
	c_id		integer AUTO_INCREMENT,
    c_name		varchar(50) not null,
    c_addr		varchar(100),
    c_phone		varchar(10),
    primary key (c_id)
);

ALTER TABLE customer AUTO_INCREMENT=1000;

CREATE TABLE customer_order (
	ord_num		integer AUTO_INCREMENT,
	branch      integer,
	date_created TIMESTAMP default NOW(),
    count		integer,
    o_status	varchar(10),
    item_id		integer,
    design_id	integer,
    customer	integer,
    last_ud_by	integer,
    total_cost	decimal(7,2),
    primary key	(ord_num),
    foreign key (branch) references branch(b_id),
    foreign key (item_id) references item(i_id),
    foreign key	(design_id) references design(d_id),
    foreign key	(customer) references customer(c_id),
    foreign key	(last_ud_by) references employee(e_id)
);

ALTER TABLE customer_order AUTO_INCREMENT=10000;

CREATE TABLE review (
	c_id		integer, 
    r_id		integer not null,
    r_type		varchar(5),
    primary key (c_id, r_id),
    foreign key (c_id) references customer (c_id)
);


CREATE TABLE item_request (
	i_id		integer,
    c_id		integer,
    amount		integer,
    primary key (i_id, c_id),
    foreign key (i_id) references item(i_id),
    foreign key (c_id) references customer(c_id)
);

CREATE TABLE coupon_offer (
	coup_id		integer,
    e_id		integer,
    c_id		integer,
    primary key (coup_id, e_id, c_id),
    foreign key (coup_id) references coupon(coup_id),
    foreign key (e_id) references employee(e_id),
    foreign key (c_id) references customer(c_id)
);