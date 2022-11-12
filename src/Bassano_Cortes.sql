create table cliente (
    id_user serial primary key,
	rut varchar(12),
    user_name varchar(100) not null unique,
    pswd varchar(60) not null,
    amount int,
    admin_flag boolean not null 
);
create table carrito (
   	id_carrito serial primary key,
    id_user int references cliente(id_user),
	total_price int
);

create table producto (
    id_product serial primary key,
    product_name varchar(30) not null unique,
    cost int not null,
    stock int
);

create table carrito_producto (
    id_carrito int references carrito(id_carrito),
    id_product int references producto(id_product)
);

create table venta (
    id_venta serial primary key,
    venta_date date not null,
    total_price int not null
);

create table carrito_venta (
    id_carrito int references carrito(id_carrito),
    id_venta int references venta(id_venta)
);


--------inserts test-------------------------
insert into cliente(rut,user_name,pswd,amount,admin_Flag)
	values
	('rutAdmin1','ADMIN1','NegocioJuanita',NULL,TRUE),
	('rut1','user1','contra1',0,FALSE),
	('rut3','user3','contra2',0,FALSE)

select * from cliente


