# TPFinalIntro
 Tp Final Introducción al Desarrollo de Software FIUBA:
 Aplicación web desarrollada como trabajo final para la materia Introducción al Desarrollo de Software FIUBA.
 Permite al usuario registrarse e iniciar sesión, ver la carta de un restaurante, crear y cancelar reservas y publicar reseñas. Mientras que, el administrador puede crear y eliminar platos de la carta, reseñas, usuarios además de actualizar estos y reservas hechas en la página (estas no se eliminan de la base de datos pero se marcan como desactivadas en esta).
  Requisitos previos:

   .Python 3.10 o superior
Lenguaje principal utilizado para el desarrollo del backend y parte de la lógica del sistema. Es necesario para ejecutar la aplicación y sus dependencias.

   .MySQL
Sistema de gestión de bases de datos utilizado para almacenar la información de usuarios, reservas, reseñas y platos del restaurante.

   .Git
Necesario para clonar el repositorio y obtener el código fuente del proyecto desde GitHub.

   .Sistema operativo compatible con Bash (Linux, Linux Mint, Ubuntu o WSL en windows)

   .Entorno virtual
Requerido para ejecutar scripts de automatización incluidos en el proyecto, como init.sh, encargado de preparar el entorno de desarrollo e instalar dependencias.

   .Acceso a Terminal de comandos de proyecto(de linux, de Vscode, etc.)
Necesaria para ejecutar los comandos de instalación, configuración y puesta en marcha del sistema.

. Docker (opcional)
El proyecto incluye archivos de configuración Docker que permiten ejecutar la aplicación dentro de contenedores, facilitando la portabilidad y garantizando un entorno de ejecución consistente entre distintos equipos.

   Pasos previos a la instalación: 
   1.Clonar repositorio:
git clone https://github.com/FinKedinn1/TPFinalIntro.git.
Este paso descarga una copia local del proyecto desde GitHub, permitiendo acceder al código fuente, realizar modificaciones y ejecutar la aplicación en el equipo local.

   2.Ingresar a la carpeta del repositorio:
cd TPFinalIntro

Permite ubicarse dentro del directorio principal del proyecto para poder ejecutar correctamente los comandos de instalación, configuración y ejecución.

3.Ejecutar el script init.sh:

Este script automatiza la configuración inicial del proyecto. Se encarga de crear los entornos virtuales necesarios en los módulos frontend y backend, activarlos cuando corresponde e instalar automáticamente todas las dependencias definidas en sus respectivos archivos requirements.txt.

Gracias a este proceso, el entorno de desarrollo queda preparado para la ejecución de la aplicación sin necesidad de realizar manualmente cada paso de configuración.


Docker: Este proyecto cuenta con configuraciones Docker.
Las dependencias se encuentran en el requirements.txt y se instalan automáticamente al construir el contenedor. La aplicación requiere una base de datos MySQL. Asegúrese de haber creado previamente una base de datos llamada "restaurante_medieval".

   Configuración de la base de datos:

La API web utiliza MySQL como sistema gestor de base de datos. Para facilitar la configuración entre distintos entornos de desarrollo y evitar exponer información sensible en el código fuente, las credenciales de acceso se almacenan mediante variables de entorno.

Se recomienda crear un archivo .env propio para cada integrante del equipo y agregarlo al .gitignore, de forma que no sea compartido en el repositorio. Esto permite que cada desarrollador utilice sus propias credenciales sin comprometer la seguridad de la base de datos.

Variables requeridas:

DB_USUARIO="tu_usuario"
DB_CONTRASEÑA="tu_contraseña"
DB_NOMBRE="restaurante_medieval"


Estructura de la base de datos:

La aplicación se apoya en un conjunto de tablas relacionadas entre sí, que permiten gestionar usuarios, reservas, reseñas, la carta del restaurante y sus platos mas populares. Cada tabla cumple una función específica dentro del sistema y se encuentra vinculada mediante claves primarias y claves foráneas.

Tabla: Usuarios

Almacena la información necesaria para el registro e identificación de los usuarios dentro de la plataforma.

Campos principales:

ID de usuario (primary key).
Nombre.
Correo electrónico único.
Contraseña.
Fecha de Creación del usuario

Esta tabla es utilizada durante los procesos de registro, inicio de sesión y asociación de reservas realizadas por cada usuario.

Tabla: Carta

Contiene la información de todos los platos disponibles en el restaurante.

Campos principales:

ID de plato (primary key).
Nombre del plato.
Descripción.
Precio.
Categoría.
Stock disponible.

Permite mostrar la carta al cliente, aplicar filtros por categoría con la funcionalidad de los botones del menu y mostrar datos de las distintas comidas

Tabla: Reservas

Almacena todas las reservas realizadas desde la aplicación.

Campos principales:

ID de reserva (primary key).
ID de usuario (foreign key, proveniente de la tabla usuarios).
Fecha de reserva.
Turno seleccionado
Cantidad de personas.
Estado de la reserva.
Fecha de creación.

Esta tabla permite gestionar la creación, consulta y cancelación de reservas, además de mantener un historial de las mismas mediante el control de estados.

Tabla: Reseñas

Registra las valoraciones y comentarios realizados por los usuarios sobre los distintos platos.

Campos principales:

ID de reseña (primary key).
ID de reserva (foreign key, viene de la tabla de reservas).
ID de plato (foreign key, viene de la tabla de la carta).
Fecha de creación.
Comentario.
Puntaje de estrellas (entre 1 y 5).

Su función es almacenar la opinión de los clientes y proporcionar la información necesaria para calcular valoraciones y promedio (en estrellas) de los platos.

Tabla: Platos Populares

Mantiene estadísticas derivadas de las reseñas recibidas por cada plato.

Campos principales:

ID de plato popular (primary key).
ID de plato (foreign key, viene de la tabla carta).
Promedio de estrellas.
Cantidad de reseñas.
Indicador de popularidad.
Fecha de actualización.

Esta tabla permite identificar automáticamente los platos mejor valorados por los usuarios, facilitando la implementación de comidas populares como recomendaciones del local a sus usuarios dentro de la aplicación.

Pasos de ejecución (sin utilizar docker):
1. Ejecutar backend: python back/app.py
2. Ejecutar frontend (en otra terminal distinta del backend) python front/app.py 3. Abrir en un navegador web el frontend de la aplicación: http://127.0.0.1:5001

Ejecución mediante Docker (opcional):

El proyecto incluye una configuración Docker Compose (archivo: 'compose.yml') que permite levantar automáticamente la base de datos, el backend y el frontend en contenedores independientes.

Primero, hay que verificar que Docker y Docker Compose se encuentren instalados en el sistema.
Luego, configurar las variables de entorno necesarias para la conexión con la base de datos.

Desde la raíz del proyecto, ejecutar:

docker compose up --build

Este comando construirá las imágenes necesarias e iniciará los servicios definidos en el archivo compose.yml.

Una vez finalizado el proceso de inicialización, acceder desde el navegador a:

http://127.0.0.1:5001

Para detener todos los servicios ejecutados mediante Docker:

docker compose down

Listado de herramientas:

.Python
Lenguaje principal utilizado para el desarrollo de la aplicación. Se empleó tanto en la lógica del backend como en distintas funcionalidades auxiliares del proyecto.

.Flask
Framework utilizado para desarrollar los servicios de la aplicación y gestionar las rutas, vistas y comunicación entre frontend, backend y base de datos.

.flask_cors
Librería utilizada para habilitar la comunicación entre aplicaciones ejecutadas en distintos puertos, permitiendo el intercambio seguro de información entre frontend y backend.

.MySQL
Sistema gestor de bases de datos empleado para almacenar y administrar usuarios, reservas, reseñas, platos y demás información persistente del sistema.

.HTML / CSS / JavaScript
Tecnologías utilizadas para el desarrollo de la interfaz web. HTML define la estructura de las páginas, CSS se encarga de la presentación visual y JavaScript aporta, funcionalidad, interactividad y dinamismo.

.qrcode
Librería utilizada para generar códigos QR asociados a las reservas realizadas por los usuarios.

.Pillow
Librería de procesamiento de imágenes utilizada como soporte para la generación, manipulación y almacenamiento de los códigos QR generados por el sistema.

.Kivy
Framework utilizado para el desarrollo de una versión móvil de la aplicación, permitiendo crear interfaces gráficas multiplataforma mediante Python.

 Funcionalidades del sistema:

.Registro e inicio de sesión de usuarios
Permite a los usuarios crear una cuenta, autenticarse dentro de la plataforma y acceder a las funcionalidades disponibles según su perfil.

.Gestión de reservas
Los usuarios pueden crear reservas indicando fecha, horario y cantidad de personas. El sistema almacena la información en la base de datos y permite su posterior consulta o cancelación.

.Generación de códigos QR
Cada reserva puede asociarse a un código QR generado automáticamente, facilitando la identificación y validación de la reserva.

.Envío automático de correos electrónicos
El sistema envía correos electrónicos asociados a las reservas, incluyendo información relevante, códigos QR y enlaces para su cancelación.

.Visualización de la carta del restaurante
Los clientes pueden consultar los platos disponibles, visualizar sus descripciones, categorías y precios, además de utilizar filtros para facilitar la navegación.

.Gestión de reseñas y valoraciones
Los usuarios pueden registrar opiniones y puntuaciones sobre los platos consumidos, contribuyendo a la generación de estadísticas y recomendaciones.

.Identificación de platos populares
A partir de las reseñas registradas, el sistema calcula promedios de valoración y determina cuáles son los platos más destacados por los usuarios.

.Administración de usuarios, reservas, reseñas y platos
Los administradores disponen de herramientas para crear, consultar, modificar y gestionar la información almacenada en el sistema, garantizando el correcto funcionamiento de la aplicación.
Creado por: grupo 5 "las Barbies y el Ken".
 Integrantes: 
 -Lara Ovejero-112774
 -Abril Martinelli-114515
 -Delfina Colamónico-114827
 -Milagros Pili Gomez-114397
 -Lourdes Rosa Larrieu-114035
 -Guillermo Miguel Gutierrez-115655
 -Joaquin Zavala-114676
 -Lautaro Castilla-114960
