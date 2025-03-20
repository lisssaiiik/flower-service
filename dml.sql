-- Добавление категорий
INSERT INTO categories (name) VALUES ('Розы'), ('Тюльпаны');

-- Добавление цветов
INSERT INTO bouquets (name, description, price, stock_quantity)
VALUES ('Букет красных роз', 'Красивый суперский букет роз для твоей второй половинки', 1599, 25),
       ('Букет розовых тюльпанов', 'желтые тюльпаны вестники разлуки, поэтому покупай розовые', 1299, 30);


-- Состав букета
INSERT INTO bouquet_components (bouquet_id, flower_id, quantity)
VALUES (1, 1, 13),
       (2, 2, 9)