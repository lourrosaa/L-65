// Configuración del Backend (puedes cambiar este puerto por el de tu API)
const BACKEND_URL = 'http://localhost:5000/api/menu';
const Platos = document.getElementsByClassName('carta-de-platos');
const Botones = document.getElementsByClassName("boton-filtrar");
    for (let i = 0; i < Botones.length; i++) {
        Botones[i].addEventListener("click", function() {
            for (let j = 0; j < Botones.length; j++) {
                Botones[j].classList.remove("activo");
            }
            Botones[i].classList.add("activo");
            const categoria_seleccionada = Botones[i].getAttribute("data-filter");

            for (let k = 0; k < Platos.length; k++) {
                const plato = Platos[k];
                const categoria_plato = plato.getAttribute("comida-categoria");

                if (categoria_seleccionada === "all") {
                    plato.classList.remove("comida-escondida");
                }
                else if (categoria_seleccionada === "Populares") {
                    const es_popular = plato.getAttribute("comida-popular");
                    if (es_popular === "True") {
                        plato.classList.remove("comida-escondida");
                    } else {
                        plato.classList.add("comida-escondida");
                    }
                }
                else {
                    if (categoria_plato === categoria_seleccionada) {
                        plato.classList.remove("comida-escondida");
                    } else {
                        plato.classList.add("comida-escondida");
                    }
                }
            }

        }); 
    }