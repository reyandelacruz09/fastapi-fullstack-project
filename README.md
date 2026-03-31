"# Fastapi-The-Complete-Course"

Course and code created by: Eric Roby


Create table query scripts
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL,
  email varchar(200) DEFAULT NULL,
  username varchar(45) DEFAULT NULL,
  first_name varchar(45) DEFAULT NULL,
  last_name varchar(45) DEFAULT NULL,
  hashed_password varchar(200) DEFAULT NULL,
  phone_number varchar(45) DEFAULT NULL,
  is_active boolean DEFAULT NULL,
  role varchar(45) DEFAULT NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS todos;

CREATE TABLE todos (
  id SERIAL,
  title varchar(200) DEFAULT NULL,
  description varchar(200) DEFAULT NULL,
  priority integer  DEFAULT NULL,
  complete boolean  DEFAULT NULL,
  owner_id integer  DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (owner_id) REFERENCES users(id)
);


DROP TABLE IF EXISTS addresses;

CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,

  street VARCHAR(200),
  city VARCHAR(100),
  province VARCHAR(100),
  zip_code VARCHAR(20),

  user_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE cities (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  province_id INTEGER NOT NULL,

  CONSTRAINT fk_province
    FOREIGN KEY (province_id)
    REFERENCES provinces(id)
    ON DELETE CASCADE
);

CREATE TABLE provinces (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,

  street VARCHAR(200) NOT NULL,

  city_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,

  CONSTRAINT fk_city
    FOREIGN KEY (city_id)
    REFERENCES cities(id)
    ON DELETE CASCADE,

  CONSTRAINT fk_user
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);