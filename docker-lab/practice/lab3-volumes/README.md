# Lab 3: PostgreSQL with persistent storage (Docker volumes)

A PostgreSQL container keeps its data in the named volume `postgres-lab-data`.
Deleting the container does **not** delete the data; a new container that mounts the same volume sees it.

## Files
- `init.sql` - creates the tables `students`, `courses` and inserts test data
- `commands.sh` - every command of the lab in order (run it with `bash commands.sh`)
- `backup.sql` - logical backup made with `pg_dump`
- `postgres-volume-backup.tar.gz` - archive of the whole volume (not committed, ~6 MB; recreate with `commands.sh`)

## Steps
1. `docker volume create postgres-lab-data`
2. Run `postgres:15-alpine` as `postgres-lab` with `--mount source=postgres-lab-data,target=/var/lib/postgresql/data`
3. `docker exec -i postgres-lab psql -U student -d university < init.sql`
4. `docker stop postgres-lab && docker rm postgres-lab` (container deleted, volume stays)
5. Start `postgres-lab-2` with the same volume and run `SELECT * FROM students;` - all 4 students are still there
6. Backups: `pg_dump` -> `backup.sql`, and a `tar czf` of the volume contents

## Cleanup
```bash
docker rm -f postgres-lab-2
docker volume rm postgres-lab-data
```
