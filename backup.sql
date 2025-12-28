PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE building (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description TEXT, 
	PRIMARY KEY (id)
);
INSERT INTO building VALUES(2,'CST Building','A building for guys in CST');
CREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE buildings (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description TEXT, 
	image_url VARCHAR(255), 
	PRIMARY KEY (id)
);
INSERT INTO buildings VALUES(2,'Main Gate','Campus entrance',NULL);
INSERT INTO buildings VALUES(3,'Library','Central library',NULL);
INSERT INTO buildings VALUES(4,'Science Block','Science faculty',NULL);
INSERT INTO buildings VALUES(5,'GDG Building','The Building for all GDG members',NULL);
INSERT INTO buildings VALUES(6,'GDG Building','Building for Memebers of GDG','https://res.cloudinary.com/dhulu97nv/image/upload/v1766892578/campus-navigation/buildings/jchaebxvik03bf1g5orr.png');
CREATE TABLE routes (
	id INTEGER NOT NULL, 
	start_building_id INTEGER NOT NULL, 
	end_building_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(start_building_id) REFERENCES buildings (id), 
	FOREIGN KEY(end_building_id) REFERENCES buildings (id)
);
INSERT INTO routes VALUES(1,2,3);
INSERT INTO routes VALUES(2,2,6);
CREATE TABLE route_cards (
	id INTEGER NOT NULL, 
	step_number INTEGER NOT NULL, 
	instruction TEXT NOT NULL, 
	image_url VARCHAR(255), 
	route_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(route_id) REFERENCES routes (id)
);
INSERT INTO route_cards VALUES(1,1,'Exit through main gate',NULL,1);
INSERT INTO route_cards VALUES(2,2,'Walk straight for 100m',NULL,1);
INSERT INTO route_cards VALUES(3,3,'Library is on your right',NULL,1);
INSERT INTO route_cards VALUES(4,1,'Go to Chapel',NULL,2);
INSERT INTO route_cards VALUES(5,2,'Turn Left to CMSS',NULL,2);
INSERT INTO route_cards VALUES(6,3,'Turn Right to CEDS',NULL,2);
INSERT INTO route_cards VALUES(7,4,'Go to CEDS Hall',NULL,2);
CREATE TABLE users (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id)
);
COMMIT;
