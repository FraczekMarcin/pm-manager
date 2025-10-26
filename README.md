# PM Manager — FastAPI + SQLite + JWT + React + Vite

Kompletna aplikacja przygotowana do uruchomienia lokalnie lub na serwerze (VM). Zawiera:
- backend (FastAPI) z JWT, admin, backup, export Excel
- frontend (React + Vite) z ładnym UI (Tailwind)
- docker-compose dla prostego uruchomienia

## Szybkie uruchomienie (z GitHub)
1. Na serwerze (Ubuntu):
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose-plugin unzip
sudo usermod -aG docker $USER
newgrp docker
```
2. Sklonuj repo (przykład):
```bash
git clone https://github.com/fraczek.marcin/pm-manager.git
cd pm-manager
```
3. Uruchom kontenery:
```bash
docker compose up -d --build
```
4. Frontend: http://<VM_IP>:3000
   Backend: http://<VM_IP>:8000

## Admin
Pierwszy admin: zarejestruj konto przez `/auth/register` z is_admin=true lub zrób to ręcznie w DB.

## Backup
Endpoint `GET /admin/backup` zwraca ścieżkę do pliku sqlite (można też skopiować wolumen `dbdata`).

## Export
Endpoint `GET /admin/export_excel` generuje i zwraca plik Excel z projektami.
