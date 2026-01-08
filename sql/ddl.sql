CREATE DATABASE 'migrator_db';


-- USER TABLE
CREATE TABLE users (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	mongo_id VARCHAR(100) NOT NULL, 
	username VARCHAR(100) NOT NULL, 
	password VARCHAR(255) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	first_name VARCHAR(100) NOT NULL, 
	last_name VARCHAR(100) NOT NULL, 
	migrado BOOL, 
	PRIMARY KEY (id)
)

-- ROLES TABLE
 CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_roles_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

INSERT INTO roles(role) VALUES ('ROLE_USER');
INSERT INTO roles(role) VALUES ('ROLE_ADMIN');