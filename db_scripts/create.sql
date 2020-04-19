create table users
(
    id SERIAL PRIMARY KEY,
    firstname text,
    lastname text,
    patronymic text,
    email text,
    phone text,
    country text,
    city text,
    inn int,
    certificate bool,
    intresting text,
    url_instagram text,
    url_vk text,
    equipment_id int,
    fertilizer text,
    saleform text
);

