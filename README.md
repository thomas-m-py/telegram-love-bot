## Telegram Love Bot

Telegram‑бот знакомств (клон Дайвинчика).
В Боте можно создавать и редактировать профиль, просмотривать и лайкать анкеты.

### Как работает бот
- Пользователь запускает бота, выбирает язык, заполняет профиль (имя, возраст, город, пол, интерес, медиа, био).
- В режиме поиска видит анкету → лайк/дизлайк/лайк с сообщением. При взаимном лайке — оба получают уведомление и ссылки друг на друга.

## Запуск

### Вручную
1) Установить зависимости:
```bash
poetry install
```
2) Создать `.env` и настроить БД/Redis/токен бота. (Шаблон .env.template)
3) Применить миграции:
```bash
alembic upgrade head
```
4) Установить вебхук:
```bash
python -m src.bot.cli set --url https://your.domain/webhook/
python -m src.bot.cli set  # возьмет URL из env
```
Проверить/удалить:
```bash
python -m src.bot.cli info
python -m src.bot.cli delete
```
5) Запустить:
```bash
python start_dev.py
```

### Через Docker

1) Создать `.env` и настроить. (Шаблон .env.template)
2) Собрать образы:
```bash
docker compose build
```
3) Применить миграции БД
```bash
docker compose exec app alembic upgrade head
```
4) Установить вебхук:
```bash
docker compose exec app python -m src.bot.cli set

# проверить текущее значение
docker compose exec app python -m src.bot.cli info
```
5) Запустить приложение:
```bash
docker compose up -d app

# С локальным Bot API
docker compose up -d telegram-bot-api app
```

## Структура проекта
- `locales/`: тексты интерфейса на разных языках.
- `src/bot/`: обработчики, middlewares, FSM
- `src/db/`: работа с БД
- `src/modules/match/`: Модуль симпатий, который фиксирует лайки, определяет взаимные симпатии.
- `src/modules/profile/`: Модуль анкет, который отвечает за создание, редактирование и поиск анкет.
- `src/modules/user/`: Модуль пользователей, который хранит базовую информацию об аккаунте.
- `src/settings/`: настройки и конфигурации.
