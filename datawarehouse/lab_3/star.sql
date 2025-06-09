-- Create schema for star data warehouse
DROP TABLE IF EXISTS star_dwh.fact_rentals CASCADE;
DROP TABLE IF EXISTS star_dwh.dim_time CASCADE;
DROP TABLE IF EXISTS star_dwh.dim_customer CASCADE;
DROP TABLE IF EXISTS star_dwh.dim_film CASCADE;
DROP TABLE IF EXISTS star_dwh.dim_store CASCADE;

create schema if not exists star_dwh;


-- Dimension: Time
create table star_dwh.dim_time (
	date_key SERIAL primary key,
	full_date date not null,
	year int not null,
	quarter int not null,
	month int not null,
	month_name varchar(10),
	day_of_month int not null,
	day_of_week varchar(10)
);

-- Dimension: Customer

create table star_dwh.dim_customer (
	costomer_key serial primary key,
	customer_id int not null,
	first_name varchar(50) not null,
	last_name varchar(50) not null,
	enail varchar(100),
	address varchar(100),
	city varchar(50),
	country varchar(50),
	active boolean
);

-- Dimension: Film (denormalized with category)
create table star_dwh.dim_film(
	film_key serial primary key,
	film_id int not null,
	title varchar(255),
	rating varchar(10),
	rental_rate numeric(4, 2),
	categories varchar(255)
);


-- Dimension: Store
create table star_dwh.dim_store (
	store_key serial primary key,
	store_id int not null,
	address varchar(100),
	city varchar(50),
	country varchar(50),
	manager_name varchar(100)
);


-- Fact: Rentals and Payments
CREATE table star_dwh.fact_rentals (
    rental_id INT NOT NULL,
    payment_id INT,
    rental_date_key INT REFERENCES star_dwh.dim_time(date_key),
    customer_key INT REFERENCES star_dwh.dim_customer(costomer_key),
    film_key INT REFERENCES star_dwh.dim_film(film_key),
    store_key INT REFERENCES star_dwh.dim_store(store_key),
    rental_count INT NOT NULL DEFAULT 1,
    payment_amount NUMERIC(10, 2),
    PRIMARY KEY (rental_id, payment_id)
);
