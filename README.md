
## Настройка окружения

```bash
DB_USER= (default: postgres)
DB_PASSWORD= (default: postgres)
DB_HOST= (default: 127.0.0.1)
DB_PORT= (default: 5432)
DB_NAME= (default: recruit_maps)

JWT_SECRET= (default: super_secret)
STORAGE_PATH= (default: storage)
```

## Запуск для разработки

1. Настроить окружение
2. Установить необходимые зависимости

```bash
pip install -r ./requirements.txt
```

3. Выполнить миграции базы данных

```bash
alembic upgrade head
```

4. Запустить сервис

```bash
gunicorn src.main:app --worker-class uvicorn.workers.UvicornWorker

```

## Production

1. Настроить окружение
2. Собрать образы

```bash
docker-compose build
```

3. Запустить контейнеры

```bash
docker-compose up
```
