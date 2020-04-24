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

CREATE TABLE currencys(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    country TEXT
);

CREATE TABLE units(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE users_product(
    id SERIAL PRIMARY KEY,
    user_id bigint REFERENCES public.users(id) ON DELETE CASCADE,
    method TEXT,
    name TEXT,
    type TEXT,
    photo TEXT,
    price int,
    currency_id bigint REFERENCES public.currencys(id),
    weight float,
    address_id bigint REFERENCES public.address(id),
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

CREATE TABLE favorit_products(
    id SERIAL PRIMARY KEY,
    user_id bigint REFERENCES public.users(id) ON DELETE CASCADE,
    users_product_id bigint REFERENCES public.users_product(id) ON DELETE CASCADE,
    UNIQUE(user_id, users_product_id)
);

CREATE TABLE cart(
    id SERIAL PRIMARY KEY,
    user_id bigint REFERENCES public.users(id) ON DELETE CASCADE,
    users_product_id bigint REFERENCES public.users_product(id) ON DELETE CASCADE,
    weight float,
    add_time TIMESTAMP WITHOUT TIME ZONE,
    UNIQUE(user_id, users_product_id)
);