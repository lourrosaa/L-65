CREATE DATABASE IF NOT EXISTS restaurante_medieval;

USE restaurante_medieval;

CREATE TABLE carta (
    id_plato INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_plato VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2),
    categoria VARCHAR(100),
    stock BOOLEAN DEFAULT TRUE
);

INSERT INTO carta
(nombre_plato, descripcion, precio, categoria)
VALUES
(
'L-65 Concentré',
'Crema de coco pura extraída en primera prensa mecánica. Concentración grasa al 65%, textura densa y sedosidad natural.',
18500,
'Extractos Botanicos'
),
(
'L-65 Extrait Liquide',
'Leche de coco raw obtenida por prensa simétrica y filtrada por ósmosis. Sin aditivos, gomas químicas ni conservantes.',
12000,
'Extractos Botanicos'
),
(
'L-65 Fibra Botánica',
'Harina de coco fina derivada del deshidratado técnico del endospermo. Libre de gluten y de bajo impacto glucémico.',
9500,
'Molienda'
),
(
'L-65 System Box',
'Asignación semanal cerrada que incluye un Concentré (200cc), dos Extrait Liquide (500cc) y una Fibra Botánica (250g).',
45000,
'Suscripción Privada'
)