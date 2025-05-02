# start.ps1
Write-Host "Construyendo y levantando los servicios..."

# Navegar a la ruta del proyecto (ajusta si es necesario)
Set-Location -Path "$PSScriptRoot"

# Eliminar contenedores anteriores si existen
docker-compose down

#Ejecutar docker compose con build sin cache
docker-compose build --no-cache
docker-compose up
#Ejecutar Docker Compose con build
#docker-compose up --build
