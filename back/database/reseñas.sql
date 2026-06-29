CREATE DATABASE IF NOT EXISTS restaurante_medieval;

USE restaurante_medieval;

CREATE TABLE IF NOT EXISTS reseñas (
    id_reseña INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    id_plato INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    comentario VARCHAR(255),
    puntaje_estrellas INT CHECK (puntaje_estrellas >= 1 AND puntaje_estrellas <= 5),
    FOREIGN KEY (id_reserva)
    REFERENCES reservas(id_reserva),
    FOREIGN KEY (id_plato)
    REFERENCES carta(id_plato)
);