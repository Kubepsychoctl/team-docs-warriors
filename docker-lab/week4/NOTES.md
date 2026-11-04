# Docker Advanced - Labs 1 and 2

## Lab 1 - react-blog (multi-stage, non-root, alpine)

| Image | Size |
|---|---|
| naive (`node:18`, `COPY . .`, no .dockerignore, single stage) | 2.64 GB |
| optimized (multi-stage, `node:18-alpine`, non-root, .dockerignore) | 191 MB (about 14x smaller) |

Run: `docker build -t react-blog . && docker run -d -p 3000:3000 --name blog react-blog`

Differences from the handout (all needed to make it work):
- `.dockerignore`: `node_modules` -> `**/node_modules` (the plain pattern only matches the root folder, so `client/node_modules` was still sent in the build context).
- Dockerfile: non-root user uses UID/GID **1001**. In `node:18-alpine` ID 1000 already belongs to the `node` user, so `addgroup -g 1000` fails.
- `server/package.json`: Express pinned to **4.x**. A plain `npm install express` now installs Express 5, which rejects `app.get("*", ...)` used in `server.js`.

## Lab 2 - shop-app (frontend nginx + backend Flask + Redis on `shop-network`)

Run: `cd shop-app && ./start.sh` then open http://localhost:8080 (API: http://localhost:5000/products).

Difference from the handout:
- `frontend/index.html`: added `<meta charset="UTF-8">`, otherwise the Cyrillic text is garbled in the browser.

## Note on this environment

The images were built in a sandbox whose proxy certificate is not trusted inside containers, so `pip install` / `npm ci` were run with the CA mounted as a build secret (not stored in the image). On a normal machine the Dockerfiles in this repo build as-is.
