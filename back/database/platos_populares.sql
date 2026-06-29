CREATE DATABASE IF NOT EXISTS restaurante_medieval;

USE restaurante_medieval;

CREATE TABLE IF NOT EXISTS platos_populares (
    id_plato_popular INT AUTO_INCREMENT PRIMARY KEY,
    id_plato INT NOT NULL,
    promedio_estrellas DECIMAL(3,2) NOT NULL DEFAULT 0.00,
    cantidad_reseñas INT NOT NULL DEFAULT 0,
    es_popular BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (id_plato)
    REFERENCES carta(id_plato)
    ON DELETE CASCADE,

    UNIQUE (id_plato)
);