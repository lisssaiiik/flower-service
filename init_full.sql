-- create tables
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    first_name VARCHAR UNIQUE NOT NULL,
    last_name VARCHAR NOT NULL,
    middle_name VARCHAR NOT NULL,
    phone_number VARCHAR UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL,
    address VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR DEFAULT 'user'
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE bouquets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0
);

CREATE TABLE bouquet_components (
    id SERIAL PRIMARY KEY,
    bouquet_id INT NOT NULL,
    flower_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (bouquet_id) REFERENCES bouquets(id),
    FOREIGN KEY (flower_id) REFERENCES categories(id)
);

-- insert initial data
INSERT INTO categories (name) VALUES ('Розы'), ('Тюльпаны');

INSERT INTO bouquets (name, description, price, stock_quantity)
VALUES ('Букет красных роз', 'Красивый суперский букет роз для твоей второй половинки', 1599, 25),
       ('Букет розовых тюльпанов', 'желтые тюльпаны вестники разлуки, поэтому покупай розовые', 1299, 30);

INSERT INTO bouquet_components (bouquet_id, flower_id, quantity)
VALUES (1, 1, 13),
       (2, 2, 9);
