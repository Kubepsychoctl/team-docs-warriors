#!/bin/bash

# Создать сеть
docker network create shop-network

# Запустить Redis
docker run -d \
  --name redis \
  --network shop-network \
  redis:7-alpine

# Собрать и запустить Backend
cd backend
docker build -t shop-backend .
docker run -d \
  --name backend \
  --network shop-network \
  -p 5000:5000 \
  shop-backend
cd ..

# Собрать и запустить Frontend
cd frontend
docker build -t shop-frontend .
docker run -d \
  --name frontend \
  --network shop-network \
  -p 8080:80 \
  shop-frontend
cd ..

echo "Shop запущен!"
echo "Frontend: http://localhost:8080"
echo "Backend API: http://localhost:5000/products"
