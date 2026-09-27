# Gloria

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](compose.yaml)
[![Helm](https://img.shields.io/badge/helm-v3-0f1689.svg?logo=helm&logoColor=white)](.helm/)

Асинхронный сервис сбора, парсинга и агрегации статистики зрителей с каналов Twitch (по умолчанию на канале [jeensoff](https://twitch.tv/jeensoff)).

Сервис отслеживает сообщения от чат-бота `gloria_bot`, извлекает данные об опыте, времени на стримах и рангах зрителей, сохраняя актуальное состояние и историческую динамику в **PostgreSQL**.

---

## 📋 О проекте

Бот `gloria_bot` периодически выводит в чат Twitch статистику зрителей по запросу или событию. Формат сообщений:

```text
nikmosi, у вас 329234 очков опыта, провел(а) на стримах 2 594,75 часов. В топе 10, ты боб[12/20].
mama_y_pokakala, у вас 20166 очков опыта, провел(а) на стримах 358,92 часов. В топе 3037, ты викинг[8/20].
qzajl, у вас 24787 очков опыта, провел(а) на стримах 263,75 часов. В топе 2400, ты викинг[8/20].
```

**Gloria** перехватывает эти сообщения, парсит регулярным выражением и раскладывает по сущностям:
- **Никнейм (`nickname`)**: имя зрителя.
- **Очки опыта (`points`)**: количество накопленного XP.
- **Часы на стримах (`hours`)**: общее время просмотра стримов.
- **Место в топе (`position`)**: позиция в рейтинге канала.
- **Ранг (`rank`)**: название ранга (`rank_name`), текущий уровень (`rank_left`) и максимальный уровень (`rank_right`).

---

## 🏗 Архитектура и стек технологий

Проект построен по принципам чистой архитектуры с разделением ответственности и инверсией зависимостей (Dependency Injection):

- **Язык & среда**: Python 3.12+, менеджер пакетов [uv](https://github.com/astral-sh/uv), Nix-окружение [devenv](https://devenv.sh/).
- **DI & Конфигурация**: `dependency-injector` для связывания компонентов, `pydantic-settings` для типобезопасных настроек из переменных окружения.
- **Twitch Integration**: `twitchAPI` для подключения к Twitch Chat через EventSub/WebSockets и прохождения OAuth2.
- **Встроенный сервер авторизации**: `Litestar` + `uvicorn`. При первом старте поднимается локальный веб-сервер для прохождения Twitch User OAuth, после чего токен сохраняется в файл и используется в дальнейшем с автоматическим обновлением.
- **Хранилище данных**: `PostgreSQL` + `SQLAlchemy 2.0 (asyncio)` + `asyncpg`.
- **Миграции**: `Alembic`.
- **Логирование**: `loguru` с поддержкой структурированного вывода и JSON-формата.
- **Инфраструктура**: Docker Compose, Kubernetes / Helm Chart.

### Структура БД

- **`last_messages`**: актуальный срез статистики по каждому зрителю (первичный ключ — `nickname`, сохранение методом UPSERT `ON CONFLICT DO UPDATE`).
- **`messages`**: полная история сообщений с автоматическим инкрементом `id` и фиксацией времени `date` для анализа динамики.

---

## 🚀 Быстрый старт

### 1. Подготовка приложения в Twitch

1. Перейдите в [Twitch Developer Console](https://dev.twitch.tv/console/apps).
2. Зарегистрируйте новое приложение:
   - **OAuth Redirect URLs**: `http://localhost:8000/login/confirm` (или внешний URL вашего ингресса).
   - **Категория**: Chat Bot / Analytics Tool.
3. Скопируйте **Client ID** и сгенерируйте **Client Secret**.

### 2. Запуск через Docker Compose (рекомендуется)

Создайте файл `.env` в директории `collector/.env`:

```env
GLORIA_CLIENT_ID=your_twitch_client_id
GLORIA_CLIENT_SECRET=your_twitch_client_secret
GLORIA_TARGET_CHANNELS=jeensoff
```

Запустите стек (Collector + PostgreSQL + pgAdmin):

```bash
docker compose up -d
```

- **PgAdmin**: доступен по адресу `http://localhost:5050` (логин/пароль по умолчанию: `pgadmin4@pgadmin.org` / `admin`).
- **Авторизация Twitch**: при первом запуске перейдите в браузере по адресу `http://localhost:8000/login` для подтверждения прав чата. После авторизации токен сохранится в `./.var/collector/token.json`, и коллектор автоматически начнет сбор данных.

### 3. Локальный запуск для разработки

Убедитесь, что установлены `python 3.12+` и `uv` (или используйте `devenv shell`):

```bash
# Перейдите в директорию коллектора
cd collector

# Установите зависимости
uv sync

# Создайте файл .env и укажите валидные Client ID и Client Secret
# GLORIA_CLIENT_ID=...
# GLORIA_CLIENT_SECRET=...

# Примените миграции БД (убедитесь, что PostgreSQL запущен)
uv run alembic upgrade head

# Запустите коллектор
uv run src/main.py
```

---

## ⚙️ Конфигурация (Переменные окружения)

Все параметры настраиваются через переменные окружения с префиксом `GLORIA_`:

| Переменная | По умолчанию | Описание |
| :--- | :--- | :--- |
| `GLORIA_CLIENT_ID` | `...` | Twitch Application Client ID |
| `GLORIA_CLIENT_SECRET` | `...` | Twitch Application Client Secret |
| `GLORIA_TARGET_CHANNELS` | `jeensoff` | Целевой канал Twitch для сбора статистики |
| `GLORIA_FILTERED_NAME` | `["gloria_bot", "nikmosi"]` | Список авторов сообщений, которые будут обрабатываться |
| `GLORIA_DATABASE` | `postgresql+asyncpg://user:123@postgres:5432/collector` | Строка подключения к PostgreSQL (asyncpg) |
| `GLORIA_PORT` | `8000` | Порт встроенного веб-сервера OAuth-авторизации |
| `GLORIA_CALLBACK_URL` | `http://localhost/login/confirm` | Callback URL для подтверждения авторизации Twitch OAuth |
| `GLORIA_STORAGE_PATH` | `./var/collector/token.json` | Путь сохранения файла OAuth-токенов Twitch |
| `GLORIA_LOG__LEVEL` | `INFO` | Уровень логирования (`TRACE`, `DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `GLORIA_LOG__JSON_FORMAT` | `false` | Форматировать логи в JSON (`true` / `false`) |

---

## ☸️ Развертывание в Kubernetes (Helm)

В репозитории подготовлен production-ready Helm-чарт в директории `.helm/`:

```bash
# Установка или обновление релиза
helm upgrade --install gloria .helm/ \
  --set collector.twitch.clientId="<YOUR_CLIENT_ID>" \
  --set collector.twitch.clientSecret="<YOUR_CLIENT_SECRET>" \
  --set collector.targetChannels="jeensoff" \
  --set collector.database="postgresql+asyncpg://user:password@postgres-service:5432/collector"
```

Особенности чарта:
- **Migration Job**: автоматический запуск `alembic upgrade head` перед стартом сервиса (хук `pre-install,pre-upgrade`).
- **PersistentVolumeClaim**: выделенный том под сохранение `token.json` для сохранения сессии между перезапусками подов.
- **Non-root Security Context**: контейнер работает от непривилегированного пользователя (UID 1000).

---

## 🧪 Тестирование и проверка качества

```bash
# Запуск тестов
cd collector
uv run pytest

# Проверка линтером и форматирование (Ruff)
uv run ruff check .
uv run ruff format --check .

# Проверка статической типизации
uv run mypy src
uvx ty check
```

При использовании `devenv` доступны готовые скрипты:
- `test-collector` — запуск pytest
- `lint-collector` — проверка Ruff
- `check-all` — комплексная проверка (Ruff + Mypy)
- `bump-patch` / `bump-minor` / `bump-major` — инкремент версии через `bump-my-version`

---

## 🗺 Roadmap

- [x] Чтение и перехват сообщений чата Twitch
- [x] Фильтрация сообщений по авторам
- [x] Регулярный парсинг формата статистики `gloria_bot`
- [x] Сохранение и автоматическое обновление токенов Twitch OAuth в файл
- [x] Сохранение актуального состояния и истории в PostgreSQL
- [x] Helm-чарт и Docker Compose для легкого развертывания
- [ ] CLI-утилита для локального просмотра статистики
- [ ] REST API / Web UI для визуализации лидерборда и графиков активности

---

## 📄 Лицензия

Проект распространяется под лицензией [GNU General Public License v3.0](LICENSE).
