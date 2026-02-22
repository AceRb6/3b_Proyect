-- Crear tablas normalizadas
CREATE TABLE IF NOT EXISTS stores (
    store_id VARCHAR(10) PRIMARY KEY,
    region VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100),
    category_id INT REFERENCES categories(category_id),
    base_price DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS weather_conditions (
    weather_id SERIAL PRIMARY KEY,
    weather_type VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS seasons (
    season_id SERIAL PRIMARY KEY,
    season_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory_facts (
    fact_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    store_id VARCHAR(10) REFERENCES stores(store_id),
    product_id VARCHAR(10) REFERENCES products(product_id),
    weather_id INT REFERENCES weather_conditions(weather_id),
    season_id INT REFERENCES seasons(season_id),
    inventory_level INT,
    units_sold INT,
    units_ordered INT,
    demand_forecast DECIMAL(10,2),
    price DECIMAL(10,2),
    discount DECIMAL(5,2),
    competitor_pricing DECIMAL(10,2),
    holiday_promotion BOOLEAN DEFAULT FALSE,
    CONSTRAINT unique_daily_record UNIQUE (date, store_id, product_id)
);

CREATE INDEX idx_facts_date ON inventory_facts(date);
CREATE INDEX idx_facts_store ON inventory_facts(store_id);
CREATE INDEX idx_facts_product ON inventory_facts(product_id);