#!/bin/bash
# Lab: PostgreSQL with persistent storage (Docker volumes)
set -e

# Part 1: volume + PostgreSQL
docker volume create postgres-lab-data
docker run -d \
  --name postgres-lab \
  --mount source=postgres-lab-data,target=/var/lib/postgresql/data \
  -e POSTGRES_USER=student \
  -e POSTGRES_PASSWORD=student123 \
  -e POSTGRES_DB=university \
  -p 5432:5432 \
  postgres:15-alpine
docker ps
docker logs postgres-lab

# Part 2: create tables + data (wait for the server to accept connections first)
until docker exec postgres-lab pg_isready -U student -d university >/dev/null 2>&1; do sleep 1; done
docker exec -i postgres-lab psql -U student -d university < init.sql
docker exec postgres-lab psql -U student -d university -c "SELECT * FROM students;"
docker exec postgres-lab psql -U student -d university -c "SELECT * FROM courses;"
docker exec postgres-lab psql -U student -d university -c "\dt"

# Part 3: persistence test - delete the container, keep the volume
docker stop postgres-lab
docker rm postgres-lab
docker volume ls | grep postgres-lab-data
docker volume inspect postgres-lab-data
docker run -d \
  --name postgres-lab-2 \
  --mount source=postgres-lab-data,target=/var/lib/postgresql/data \
  -e POSTGRES_USER=student \
  -e POSTGRES_PASSWORD=student123 \
  -p 5432:5432 \
  postgres:15-alpine
until docker exec postgres-lab-2 pg_isready -U student -d university >/dev/null 2>&1; do sleep 1; done
docker exec postgres-lab-2 psql -U student -d university -c "SELECT * FROM students;"

# Part 4: backups
docker exec postgres-lab-2 pg_dump -U student university > backup.sql
docker run --rm \
  --mount source=postgres-lab-data,target=/data \
  -v "$(pwd)":/backup \
  ubuntu \
  tar czf /backup/postgres-volume-backup.tar.gz /data
ls -lh backup.sql postgres-volume-backup.tar.gz
