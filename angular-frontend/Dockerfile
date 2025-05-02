# Usa Node como base
FROM node:18

# Crea directorio de trabajo
WORKDIR /app

# Copia package.json y package-lock.json
COPY package*.json ./

# Instala Angular CLI y tslib globalmente
RUN npm install -g @angular/cli@16 tslib

# Instala Chart.js (no es necesario instalarlo globalmente)
RUN npm install chart.js

# Instala dependencias del proyecto
RUN npm install

# Copia el resto del código
COPY . .

# Expón el puerto
EXPOSE 4200

# Ejecuta Angular en modo desarrollo
CMD ["npm", "start"]