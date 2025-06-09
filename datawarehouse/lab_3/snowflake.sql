-- Create schema for snowflake data warehouse
CREATE SCHEMA IF NOT EXISTS snowflake_dwh;

-- Dimension: Time
CREATE TABLE snowflake_dwh.dim_time (
    date_key SERIAL PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(10),
    day_of_month INTEGER NOT NULL,
    day_of_week VARCHAR(10)
);

-- Dimension: Country
CREATE TABLE snowflake_dwh.dim_country (
    country_key SERIAL PRIMARY KEY,
    country_id INTEGER NOT NULL,
    country VARCHAR(50) NOT NULL
);

-- Dimension: City
CREATE TABLE snowflake_dwh.dim_city (
    city_key SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL,
    city VARCHAR(50) NOT NULL,
    country_key INTEGER REFERENCES snowflake_dwh.dim_country(country_key)
);

-- Dimension: Address
CREATE TABLE snowflake_dwh.dim_address (
    address_key SERIAL PRIMARY KEY,
    address_id INTEGER NOT NULL,
    address VARCHAR(100) NOT NULL,
    city_key INTEGER REFERENCES snowflake_dwh.dim_city(city_key)
);

-- Dimension: Customer
CREATE TABLE snowflake_dwh.dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    address_key INTEGER REFERENCES snowflake_dwh.dim_address(address_key),
    active BOOLEAN
);

-- Dimension: Category
CREATE TABLE snowflake_dwh.dim_category (
    category_key SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL
);

-- Dimension: Film
CREATE TABLE snowflake_dwh.dim_film (
    film_key SERIAL PRIMARY KEY,
    film_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    rating VARCHAR(10),
    rental_rate NUMERIC(4,2)
);

-- Bridge Table: Film-Category
CREATE TABLE snowflake_dwh.film_category_bridge (
    film_key INTEGER REFERENCES snowflake_dwh.dim_film(film_key),
    category_key INTEGER REFERENCES snowflake_dwh.dim_category(category_key),
    PRIMARY KEY (film_key, category_key)
);

-- Dimension: Store
CREATE TABLE snowflake_dwh.dim_store (
    store_key SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL,
    address_key INTEGER REFERENCES snowflake_dwh.dim_address(address_key),
    manager_name VARCHAR(100)
);

-- Fact: Rentals and Payments
CREATE TABLE snowflake_dwh.fact_rentals (
    rental_id INTEGER NOT NULL,
    payment_id INTEGER,
    rental_date_key INTEGER REFERENCES snowflake_dwh.dim_time(date_key),
    customer_key INTEGER REFERENCES snowflake_dwh.dim_customer(customer_key),
    film_key INTEGER REFERENCES snowflake_dwh.dim_film(film_key),
    store_key INTEGER REFERENCES snowflake_dwh.dim_store(store_key),
    rental_count INTEGER NOT NULL DEFAULT 1,
    payment_amount NUMERIC(10,2),
    PRIMARY KEY (rental_id, payment_id)
);

-- Populate dim_time
INSERT INTO snowflake_dwh.dim_time (full_date, year, quarter, month, month_name, day_of_month, day_of_week)
SELECT DISTINCT
    rental_date::DATE,
    EXTRACT(YEAR FROM rental_date),
    EXTRACT(QUARTER FROM rental_date),
    EXTRACT(MONTH FROM rental_date),
    TO_CHAR(rental_date, 'Month'),
    EXTRACT(DAY FROM rental_date),
    TO_CHAR(rental_date, 'Day')
FROM dvdrental.public.rental
UNION
SELECT DISTINCT
    payment_date::DATE,
    EXTRACT(YEAR FROM payment_date),
    EXTRACT(QUARTER FROM payment_date),
    EXTRACT(MONTH FROM payment_date),
    TO_CHAR(payment_date, 'Month'),
    EXTRACT(DAY FROM payment_date),
    TO_CHAR(payment_date, 'Day')
FROM dvdrental.public.payment
ORDER BY full_date;

-- Populate dim_country
INSERT INTO snowflake_dwh.dim_country (country_id, country)
SELECT country_id, country
FROM dvdrental.public.country;

-- Populate dim_city
INSERT INTO snowflake_dwh.dim_city (city_id, city, country_key)
SELECT 
    ci.city_id,
    ci.city,
    co.country_key
FROM dvdrental.public.city ci
JOIN dvdrental.public.country c ON ci.country_id = c.country_id
JOIN snowflake_dwh.dim_country co ON c.country_id = co.country_id;

-- Populate dim_address
INSERT INTO snowflake_dwh.dim_address (address_id, address, city_key)
SELECT 
    a.address_id,
    a.address,
    ci.city_key
FROM dvdrental.public.address a
JOIN dvdrental.public.city c ON a.city_id = c.city_id
JOIN snowflake_dwh.dim_city ci ON c.city_id = ci.city_id;

-- Populate dim_customer
INSERT INTO snowflake_dwh.dim_customer (customer_id, first_name, last_name, email, address_key, active)
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    a.address_key,
    c.activebool
FROM dvdrental.public.customer c
JOIN dvdrental.public.address ad ON c.address_id = ad.address_id
JOIN snowflake_dwh.dim_address a ON ad.address_id = a.address_id;

-- Populate dim_category
INSERT INTO snowflake_dwh.dim_category (category_id, name)
SELECT category_id, name
FROM dvdrental.public.category;

-- Populate dim_film
INSERT INTO snowflake_dwh.dim_film (film_id, title, rating, rental_rate)
SELECT film_id, title, rating, rental_rate
FROM dvdrental.public.film;

-- Populate film_category_bridge
INSERT INTO snowflake_dwh.film_category_bridge (film_key, category_key)
SELECT 
    f.film_key,
    c.category_key
FROM dvdrental.public.film_category fc
JOIN snowflake_dwh.dim_film f ON fc.film_id = f.film_id
JOIN snowflake_dwh.dim_category c ON fc.category_id = c.category_id;

-- Populate dim_store
INSERT INTO snowflake_dwh.dim_store (store_id, address_key, manager_name)
SELECT 
    s.store_id,
    a.address_key,
    st.first_name || ' ' || st.last_name AS manager_name
FROM dvdrental.public.store s
JOIN dvdrental.public.address ad ON s.address_id = ad.address_id
JOIN snowflake_dwh.dim_address a ON ad.address_id = a.address_id
JOIN dvdrental.public.staff st ON s.manager_staff_id = st.staff_id;

-- Populate fact_rentals
INSERT INTO snowflake_dwh.fact_rentals (
    rental_id, payment_id, rental_date_key, customer_key, film_key, store_key, rental_count, payment_amount
)
SELECT 
    r.rental_id,
    p.payment_id,
    t.date_key AS rental_date_key,
    c.customer_key,
    f.film_key,
    s.store_key,
    1 AS rental_count,
    p.amount AS payment_amount
FROM dvdrental.public.rental r
LEFT JOIN dvdrental.public.payment p ON r.rental_id = p.rental_id
JOIN dvdrental.public.inventory i ON r.inventory_id = i.inventory_id
JOIN snowflake_dwh.dim_time t ON r.rental_date::DATE = t.full_date
JOIN snowflake_dwh.dim_customer c ON r.customer_id = c.customer_id
JOIN snowflake_dwh.dim_film f ON i.film_id = f.film_id
JOIN snowflake_dwh.dim_store s ON i.store_id = s.store_id;