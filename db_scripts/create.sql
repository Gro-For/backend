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
    country TEXT,
    city TEXT,
    inn INT,
    certificate BOOLEAN,
    intresting TEXT,
    url_instagram TEXT,
    url_vk TEXT,
    equipment_id INT,
    fertilizer TEXT,
    saleform TEXT,
    role INT,
    UNIQUE(email)
);

CREATE INDEX users_email_index ON public.users USING btree(email);
CREATE INDEX users_number_phone_index ON public.users USING btree(number_phone);
CREATE INDEX users_country_index ON public.users USING btree(country);
CREATE INDEX users_city_index ON public.users USING btree(city);


INSERT INTO public.users(firstname,lastname,email,number_phone,country,city) VALUES('Петров', 'Володя', 'my_email@mail.ru','7(777)-777-7777','Canada','Vancouver');