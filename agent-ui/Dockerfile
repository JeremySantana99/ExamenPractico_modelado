### Etapa 1: Build del frontend con pnpm
FROM node:18 as frontend-builder

# Habilitar pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Carpeta de trabajo
WORKDIR /usr/src/app

# Copiar archivos de dependencias
COPY package.json pnpm-lock.yaml ./

# Instalar dependencias
RUN pnpm install

# Copiar el resto del proyecto
COPY . .

# Compilar el proyecto (Next.js u otro framework)
RUN pnpm run build


### Etapa 2: Contenedor de producción liviano
FROM node:18-alpine as production

# Activar pnpm en entorno reducido
RUN corepack enable && corepack prepare pnpm@latest --activate

# Directorio de ejecución
WORKDIR /app

# Copiar únicamente lo necesario para producción
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --prod

# Copiar archivos generados desde la etapa de construcción
COPY --from=frontend-builder /usr/src/app/.next ./.next
COPY --from=frontend-builder /usr/src/app/next.config.ts ./next.config.ts

# Puerto por defecto de Next.js (ajústalo si usas otro)
EXPOSE 8080

# Iniciar la aplicación
CMD ["pnpm", "start"]
