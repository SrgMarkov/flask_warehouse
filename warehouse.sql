
START TRANSACTION;
CREATE TABLE products (
	id INTEGER NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	description TEXT, 
	price FLOAT NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO products VALUES(1,'лыжи',replace(replace('детские, 80см\r\nпалки в комплекте','\r',char(13)),'\n',char(10)),1200.0);
INSERT INTO products VALUES(2,'телефон','кнопочный, зеленый',300.0);
INSERT INTO products VALUES(3,'коньки ','Детские коньки',3000.0);
INSERT INTO products VALUES(4,'ножницы','острые',50.0);
INSERT INTO products VALUES(5,'печенье','очень вкусное',120.0);
INSERT INTO products VALUES(6,'мазь лыжная','Мазь лыжная 6тюбиков в комплекте',1200.0);
INSERT INTO products VALUES(7,'очки','солнцезащитные',600.0);
INSERT INTO products VALUES(8,'шуруповерт','АКБ, удобная ручка',2500.0);
INSERT INTO products VALUES(9,'конь','педальный',500000.0);
INSERT INTO products VALUES(10,'коробка','картонная',10.0);
INSERT INTO products VALUES(11,'болт','железный',5.0);
INSERT INTO products VALUES(12,'болтушка','кухонная',1200.0);
CREATE TABLE locations (
	id INTEGER NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO locations VALUES(1,'Ижевск');
INSERT INTO locations VALUES(2,'Москва');
INSERT INTO locations VALUES(3,'Лондон');
INSERT INTO locations VALUES(4,'Берлин');
INSERT INTO locations VALUES(5,'Владивосток');
CREATE TABLE inventory (
	id INTEGER NOT NULL, 
	product_id INTEGER, 
	location_id INTEGER, 
	quantity INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_id) REFERENCES products (id), 
	FOREIGN KEY(location_id) REFERENCES locations (id)
);
INSERT INTO inventory VALUES(1,1,1,6);
INSERT INTO inventory VALUES(2,2,3,3);
INSERT INTO inventory VALUES(3,3,1,1);
INSERT INTO inventory VALUES(4,4,1,70);
INSERT INTO inventory VALUES(5,5,5,500);
INSERT INTO inventory VALUES(6,6,5,3);
INSERT INTO inventory VALUES(7,7,1,20);
INSERT INTO inventory VALUES(8,8,4,4);
INSERT INTO inventory VALUES(9,9,2,1);
INSERT INTO inventory VALUES(10,10,4,800);
INSERT INTO inventory VALUES(11,11,2,2876);
INSERT INTO inventory VALUES(12,12,4,32);
COMMIT;