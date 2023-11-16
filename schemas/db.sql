-- Active: 1699638164224@@127.0.0.1@3306@colinaperla

DROP DATABASE IF EXISTS colinaperla;

CREATE DATABASE colinaperla DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE colinaperla;

CREATE TABLE permissions (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY name (name)
);

CREATE TABLE roles (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    PRIMARY KEY (id),
    UNIQUE KEY name (name)
);

CREATE TABLE rol_perms (
    id INT NOT NULL AUTO_INCREMENT,
    role_id INT NOT NULL,
    perm_id INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY rol_perm (role_id, perm_id),
    CONSTRAINT fk_rol_perm_rol FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE,
    CONSTRAINT fk_rol_perm_perm FOREIGN KEY (perm_id) REFERENCES permissions (id) ON DELETE CASCADE
);

CREATE TABLE users (
    id BINARY(16) NOT NULL DEFAULT (UUID_TO_BIN(UUID())),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    token BINARY(60) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
);

CREATE TABLE user_perms (
    id INT NOT NULL AUTO_INCREMENT,
    user_id BINARY(16) NOT NULL,
    perm_id INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY user_perm (user_id, perm_id),
    CONSTRAINT fk_user_perm_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_user_perm_perm FOREIGN KEY (perm_id) REFERENCES permissions (id) ON DELETE CASCADE
);

CREATE TABLE user_roles (
    id INT NOT NULL AUTO_INCREMENT,
    user_id BINARY(16) NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY user_rol (user_id, role_id),
    CONSTRAINT fk_user_rol_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_user_rol_rol FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sellers (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    enterprise VARCHAR(255) NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
);

CREATE TABLE dev_status (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY name (name)
);

INSERT INTO dev_status (name) VALUES
    ('En desarrollo'),
    ('En preventa'),
    ('En construcción'),
    ('Entregado'),
    ('Oculto'),
    ('Disponible');

CREATE TABLE developments (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    address VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    logo_url VARCHAR(255) NOT NULL,
    contact_number VARCHAR(25) NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    view_url TEXT,
    status INT NOT NULL DEFAULT 6,
    PRIMARY KEY (id),
    UNIQUE KEY name (name),
    CONSTRAINT fk_dev_status FOREIGN KEY (status) REFERENCES dev_status (id)
);

CREATE TABLE payment_plans (
    id INT NOT NULL AUTO_INCREMENT,
    months_to_pay INT NOT NULL,
    interest_rate DECIMAL(5,2) NOT NULL,
    annuity DECIMAL(10,2) NOT NULL,
    pay_per_month DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE batch_status(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY name (name)
);

INSERT INTO batch_status (name) VALUES
    ('Disponible'),
    ('Vendido'),
    ('Reservado');

CREATE TABLE batches (
    id INT NOT NULL AUTO_INCREMENT,
    area DECIMAL(10,2) NOT NULL,
    block INT NOT NULL,
    number_of_batch INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    perimeter DECIMAL(10,2) NOT NULL,
    longitude DECIMAL(10,2) NOT NULL,
    coords VARCHAR(255) NOT NULL,
    amenities VARCHAR(255) NOT NULL,
    development_id INT NOT NULL,
    currency VARCHAR(10) NOT NULL,
    location TEXT NOT NULL,
    sq_m DECIMAL(10,2) NOT NULL,
    sides INT NOT NULl,
    status INT NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    CONSTRAINT fk_batch_dev FOREIGN KEY (development_id) REFERENCES developments (id) ON DELETE CASCADE,
    CONSTRAINT fk_batch_status FOREIGN KEY (status) REFERENCES batch_status (id)
);

CREATE TABLE batch_assets (
    id INT NOT NULL AUTO_INCREMENT,
    batch_id INT NOT NULL,
    asset_url VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_batch_asset_batch FOREIGN KEY (batch_id) REFERENCES batches (id) ON DELETE CASCADE
);

CREATE TABLE batch_payment_plans (
    id INT NOT NULL AUTO_INCREMENT,
    batch_id INT NOT NULL,
    payment_plan_id INT NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_batch_payment_batch FOREIGN KEY (batch_id) REFERENCES batches (id) ON DELETE CASCADE,
    CONSTRAINT fk_batch_payment_payment FOREIGN KEY (payment_plan_id) REFERENCES payment_plans (id) ON DELETE CASCADE,
    UNIQUE KEY batch_payment (batch_id, payment_plan_id)
);