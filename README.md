# django-xlsx-mailing-import

Django-проект для импорта рассылок из XLSX и отправки писем через management command.

## Запуск

```bash
git clone https://github.com/DaniilFedotov/django-xlsx-mailing-import.git
cd django-xlsx-mailing-import

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# опционально: пустая база с нуля (удобно перед первой проверкой)
rm -f db.sqlite3
python manage.py migrate
python manage.py import_mailings sample_mailings.xlsx
```

`requirements-dev.txt` включает runtime-зависимости из `requirements.txt` и пакеты для тестов.

`pytest` использует in-memory SQLite (`TEST.NAME` в settings) и **не пишет** в `db.sqlite3`.

## Конфигурация

Настройки — в `config/settings.py`. Значения читаются из переменных окружения через `os.environ.get()` при старте. Шаблон переменных — `.env.example`. Без env используются dev-дефолты (SQLite, задержка отправки 5–20 сек).

## Примеры XLSX для ручной проверки

В корне репозитория лежат готовые файлы:

| Файл | Назначение |
|------|------------|
| `sample_mailings.xlsx` | 3 валидные строки |
| `sample_mailings_invalid.xlsx` | 3 строки с ошибками валидации |

Путь передаётся аргументом команды (относительный — от текущей директории):

```bash
# из корня проекта
python manage.py import_mailings sample_mailings.xlsx
python manage.py import_mailings sample_mailings_invalid.xlsx

# абсолютный путь
python manage.py import_mailings /path/to/sample_mailings.xlsx
```

Пересоздать файлы заново:

```bash
python manage.py generate_sample_xlsx          # оба файла в корень
python manage.py generate_sample_xlsx valid    # только валидный
python manage.py generate_sample_xlsx invalid --output-dir /tmp
```

Повторный импорт `sample_mailings.xlsx`: все строки → **skipped** (уже в БД).  
`sample_mailings_invalid.xlsx`: processed=3, created=0, errors=3.

**Первый запуск** `sample_mailings.xlsx` на чистой базе: created=3, skipped=0.  
**Второй запуск** того же файла: created=0, skipped=3.

Если оба раза skipped=3 — в `db.sqlite3` уже были записи (например, после предыдущего импорта). Пересоздайте базу (см. блок «Запуск» выше).

## Логи отправки писем

При импорте `send_email` пишет в Python logging. Сообщения видны **в том же терминале**, где запущена команда:

```
Send EMAIL to user1@example.com | subject=Welcome | message=...
```

Между строками пауза 5–20 сек (по ТЗ). Для быстрой проверки:

```bash
MAILING_SEND_DELAY_MIN=0 MAILING_SEND_DELAY_MAX=0 python manage.py import_mailings sample_mailings.xlsx
```

## Формат XLSX

Первая строка — заголовки: `external_id`, `user_id`, `email`, `subject`, `message`.

## Тесты

```bash
pytest
```
