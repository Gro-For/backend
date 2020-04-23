CREATE TABLE public.version (version bigint DEFAULT 0);

CREATE TABLE public.users
(
    id SERIAL PRIMARY KEY,
    firstname TEXT,
    lastname TEXT,
    patronymic TEXT,
    email TEXT,
    password TEXT,
    number_phone TEXT,
    address_id INT,
    inn INT,
    certificate BOOLEAN,
    intresting TEXT,
    url_instagram TEXT,
    url_vk TEXT,
    equipment_id INT,
    fertilizer TEXT,
    saleform TEXT,
    role INT,
    last_login TIMESTAMP WITHOUT TIME ZONE,
    last_change TIMESTAMP WITHOUT TIME ZONE,
    UNIQUE(email)
);

INSERT INTO public.users(email, password, intresting, role) VALUES('Admin', 'sha256$9Q6NrDfi$b836d54af9e7a7066fbf0df78ae4f3a18db8cf3013994f557775971e0be718e4', 'Pas$word1', 0);

CREATE TABLE products(
    id SERIAL PRIMARY KEY,
    method TEXT,
    name TEXT,
    type TEXT
);

CREATE TABLE currencys(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    country TEXT
);

CREATE TABLE units(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE users_poduct(
    id SERIAL PRIMARY KEY,
    user_id bigint REFERENCES public.users(id) ON DELETE CASCADE,
    product_id bigint REFERENCES public.products(id) ON DELETE CASCADE,
    photo TEXT,
    price int,
    currency_id int REFERENCES public.currencys(id),
    weight float,
    unit_id int REFERENCES public.units(id),
    sale int -- Скидка
);

CREATE TABLE address(
    id SERIAL PRIMARY KEY,
    user_id  bigint REFERENCES public.users(id) ON DELETE CASCADE,
    country TEXT,
    city TEXT,
    address TEXT,
    lat FLOAT,
    lng FLOAT,
    UNIQUE(user_id, address)
);