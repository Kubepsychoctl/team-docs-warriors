# ============ STAGE 1: Build React ============
FROM node:18 AS react-build

WORKDIR /app/client

# Установить зависимости
COPY client/package*.json ./
RUN npm ci

# Собрать React
COPY client/ .
RUN npm run build

# ============ STAGE 2: Build Server ============
FROM node:18-alpine

# Создать non-root пользователя (UID 1000 уже занят пользователем node)
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser

WORKDIR /app

# Установить только production зависимости
COPY server/package*.json ./
RUN npm ci --only=production

# Копировать сервер
COPY server/server.js .

# Копировать собранный React из stage 1
COPY --from=react-build /app/client/build ./build

# Переключиться на appuser
USER appuser

EXPOSE 3000

CMD ["node", "server.js"]
