#!/bin/bash

echo "🚀 Deteniendo contenedores previos..."
docker-compose down

echo "🧹 Limpiando cachés de Docker (opcional)..."
docker system prune -f

echo "🔧 Construyendo y levantando el proyecto..."
docker-compose up --build
