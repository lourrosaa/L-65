const estrellas = document.getElementsByClassName('estrella');
const filtroPlato = document.getElementById('filtro-plato');
const reseñas = document.getElementsByClassName('reseña');


for (let i = 0; i < estrellas.length; i++) {
    estrellas[i].addEventListener('click', function() {

        for (let j = 0; j < estrellas.length; j++) {
            estrellas[j].classList.remove('activa');
        }

        for (let k = 0; k <= i; k++) {
            estrellas[k].classList.add('activa');
        }

        document.getElementById("puntaje_estrellas").value = i + 1;
    });
}
filtroPlato.addEventListener('change', function() {
const platoSeleccionado = filtroPlato.value;

for (let i = 0; i < reseñas.length; i++) {
const reseña = reseñas[i].getAttribute('info-plato');

if (platoSeleccionado === 'all' || reseña === platoSeleccionado) {
reseñas[i].classList.remove('comida-escondida');
} else {
reseñas[i].classList.add('comida-escondida');
}
}
});