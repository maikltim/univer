

-- Ensure dimension tables are empty before population
TRUNCATE TABLE star_dwh.dim_time, star_dwh.dim_customer, star_dwh.dim_film, star_dwh.dim_store, star_dwh.fact_rentals CASCADE;

-- Populate dim_time
INSERT INTO star_dwh.dim_time (full_date, year, quarter, month, month_name, day_of_month, day_of_week)
SELECT DISTINCT
    rental_date::DATE AS full_date,
    EXTRACT(YEAR FROM rental_date)::INTEGER,
    EXTRACT(QUARTER FROM rental_date)::INTEGER,
    EXTRACT(MONTH FROM rental_date)::INTEGER,
    TO_CHAR(rental_date, 'Mon') AS month_name,
    EXTRACT(DAY FROM rental_date)::INTEGER,
    TO_CHAR(rental_date, 'Dy') AS day_of_week
FROM public.rental
WHERE rental_date IS NOT NULL
UNION
SELECT DISTINCT
    payment_date::DATE AS full_date,
    EXTRACT(YEAR FROM payment_date)::INTEGER,
    EXTRACT(QUARTER FROM payment_date)::INTEGER,
    EXTRACT(MONTH FROM payment_date)::INTEGER,
    TO_CHAR(payment_date, 'Mon') AS month_name,
    EXTRACT(DAY FROM payment_date)::INTEGER,
    TO_CHAR(payment_date, 'Dy') AS day_of_week
FROM public.payment
WHERE payment_date IS NOT NULL
ORDER BY full_date;

-- Populate dim_customer
INSERT INTO star_dwh.dim_customer (customer_id, first_name, last_name, email, address, city, country, active)
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    a.address,
    ci.city,
    co.country,
    c.activebool
FROM public.customer c
JOIN public.address a ON c.address_id = a.address_id
JOIN public.city ci ON a.city_id = ci.city_id
JOIN public.country co ON ci.country_id = co.country_id;

-- Populate dim_film
INSERT INTO star_dwh.dim_film (film_id, title, rating, rental_rate, categories)
SELECT 
    f.film_id,
    f.title,
    f.rating,
    f.rental_rate,
    STRING_AGG(cat.name, ', ') AS categories
FROM public.film f
LEFT JOIN public.film_category fc ON f.film_id = fc.film_id
LEFT JOIN public.category cat ON fc.category_id = cat.category_id
GROUP BY f.film_id, f.title, f.rating, f.rental_rate;

-- Populate dim_store
INSERT INTO star_dwh.dim_store (store_id, address, city, country, manager_name)
SELECT 
    s.store_id,
    a.address,
    ci.city,
    co.country,
    st.first_name || ' ' || st.last_name AS manager_name
FROM public.store s
JOIN public.address a ON s.address_id = a.address_id
JOIN public.city ci ON a.city_id = ci.city_id
JOIN public.country co ON ci.country_id = co.country_id
JOIN public.staff st ON s.manager_staff_id = st.staff_id;

-- Populate fact_rentals
INSERT INTO star_dwh.fact_rentals (
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
FROM public.rental r
LEFT JOIN public.payment p ON r.rental_id = p.rental_id
JOIN public.inventory i ON r.inventory_id = i.inventory_id
JOIN star_dwh.dim_time t ON r.rental_date::DATE = t.full_date
JOIN star_dwh.dim_customer c ON r.customer_id = c.customer_id
JOIN star_dwh.dim_film f ON i.film_id = f.film_id
JOIN star_dwh.dim_store s ON i.store_id = s.store_id
WHERE r.rental_date IS NOT NULL;