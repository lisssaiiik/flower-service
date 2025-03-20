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

-- таблица bouquets - они же букеты
CREATE TABLE bouquets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0
);

-- таблица с цветами, которые входят в состав букета
CREATE TABLE bouquet_components (
    id SERIAL PRIMARY KEY,
    bouquet_id INT NOT NULL,
    flower_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (bouquet_id) REFERENCES bouquets(id),
    FOREIGN KEY (flower_id) REFERENCES categories(id)
);

-- таблица избранное
CREATE TABLE stars (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    bouquet_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (bouquet_id) REFERENCES bouquets(id)
);


-- таблица Элементы корзины
CREATE TABLE basket_items (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    bouquet_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (bouquet_id) REFERENCES bouquets(id)
);


CREATE TABLE orders (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id INTEGER REFERENCES users(id),
    order_date DATE,
    total_cost FLOAT,
    order_status VARCHAR NOT NULL,
    payment_method VARCHAR,
    shipping_method VARCHAR,
    is_delivered BOOLEAN,
    address VARCHAR
);

