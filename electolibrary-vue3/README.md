# ElectoLibrary — Vue 3 + FastAPI

Ссылка на репозиторий: **https://github.com/USERNAME/electolibrary-vue3**  
Перед сдачей замените `USERNAME` на свой GitHub-аккаунт и вставьте реальную ссылку.

## Описание

ElectoLibrary — SPA-приложение «Электронная библиотека». Проект содержит:

- клиентскую часть на Vue 3 + Vue Router;
- серверную часть на Python FastAPI;
- хранение данных в SQLite-файле `data/tasks.db`;
- запуск через Docker Compose.

## Реализовано

- Главная страница `/`.
- Каталог книг `/books`.
- Создание книги `/books/new`.
- Редактирование книги `/books/:id/edit`.
- Избранные книги `/books/favorites`.
- Страница 404.
- CRUD API:
  - `GET /api/books`
  - `GET /api/books/{id}`
  - `GET /api/boooks/{id}` — добавлено также из-за опечатки в задании
  - `POST /api/books`
  - `PUT /api/books/{id}`
  - `DELETE /api/books/{id}`
- Фильтрация по статусу.
- Поиск по названию, автору, издательству и тематике.
- Сортировка по дате добавления и алфавиту.
- Добавление в избранное.
- Бронирование книги.
- Тематические подборки.
- Загрузка JPG-обложки.
- Компоненты, props, events, slots, computed, watch, refs, lifecycle hooks.

## Запуск через Docker

```bash
docker compose build
docker compose up
```

После запуска:

- Frontend: http://localhost:8080
- Backend API: http://localhost:8000/api/books
- Swagger: http://localhost:8000/docs

## Локальный запуск без Docker

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend будет доступен на http://localhost:5173.

## Структура

```text
/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── router/
│   │   ├── services/
│   │   └── views/
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf
│   └── Dockerfile
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
├── data/
├── docker-compose.yml
└── REPORT.md
```
