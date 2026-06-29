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
'Hamburguesa del Rey',
'Hamburguesa saludable con pan integral',
8500,
'Plato Principal'
),
(
'Papas del Castillo',
'Papas rusticas con especias medievales',
4200,
'Entradas'
),
(
'Poción Frutal',
'Jugo natural de frutos rojos',
3000,
'Bebidas'
),
(
'Tarta del Guerrero',
'Tarta integral de manzana',
3900,
'Postres'
),
(
'Costillas del Palacio Real',
'Costillas glaseadas con salsa de miel y especias',
12500,
'Plato Principal'
),
(
'Sopa del Hechicero',
'Sopa cremosa de calabaza y hierbas',
4800,
'Entradas'
),
(
'Elixir de los Bosques',
'Limonada con menta y frutos cítricos',
3200,
'Bebidas'
),
(
'Banquete de la Reina',
'Cheesecake de frutos rojos',
4500,
'Postres'
),
(
'Pollo del Caballero',
'Pechuga grillada con hierbas y vegetales',
9800,
'Plato Principal'
),

(
'Anillos del Reino',
'Aros de cebolla crocantes con salsa especial',
4500,
'Entradas'
),

(
'Hidromiel Real',
'Bebida refrescante inspirada en la hidromiel medieval',
3500,
'Bebidas'
),

(
'Delicia de la Corona',
'Brownie tibio con salsa de chocolate',
4800,
'Postres'
);