CREATE DATABASE IF NOT EXISTS restaurante_medieval;

USE restaurante_medieval;

CREATE TABLE IF NOT EXISTS reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_reserva DATE NOT NULL,
    turno VARCHAR(10) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cant_personas INT NOT NULL,
    estado VARCHAR(20) DEFAULT 'activa',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);