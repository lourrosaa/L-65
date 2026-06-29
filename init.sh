#!/bin/bash

echo "Iniciando proyecto completo"

# BACKEND

echo "Configurando el BACKEND"

cd back

if [ ! -d "venv" ]; then
    echo "Creando el entorno virtual de BACK"
    python3 -m venv venv
fi

echo "Activando el entorno virtual de BACK"
source venv/bin/activate

echo "Instalando dependencias de BACK"
pip install -r requirements.txt

echo "Levantando el BACKEND"
python app.py &

cd ..

# FRONTEND

echo "Configurando el FRONTEND"

cd front

if [ ! -d "venv" ]; then
    echo "Creando el entorno virtual de FRONT"
    python3 -m venv venv
fi

echo "Activando el entorno virtual de FRONT"
source venv/bin/activate

echo "Instalando dependencias de FRONT"
pip install -r requirements.txt

echo "Levantando el FRONTEND"
python app.py &

cd ..


echo "Todo levantado!"
echo "Backend y Front corriendo en paralelo"

wait