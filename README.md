Запуск aiogram бота:
cd task2
создать .env с переменными:
  POSTGRES_HOST=db
  POSTGRES_PORT=5432
  POSTGRES_DB=postgres
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  TG_BOT_TOKEN={УКАЗАТЬ ТОКЕН ТЕЛЕГРАМ БОТА}
docker-compose up -d --build
подождать, пока поднимется БД, пройдут миграции и запустится бот.
Открыть чат с ботом, нажать команду /start
