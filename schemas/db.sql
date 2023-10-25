-- Active: 1698255626383@@soportefoco.com@3306

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
