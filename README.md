# Backend Django for MIND
- Необходимо настроить базу Postgres c параметрами

        'NAME': 'mind_db', <- название БД
        'USER': 'postgres', <- стандартный user
        `PASSWORD': '1234qwer', <- пароль (замена в настройка settings в mind)

- Создание виртуального окружения -  `python3 -m venv venv`
- Активация - `source venv/bin/activate`
- Установка зависимостей - `pip install -r requirements`
- Сделать миграции в базу

        `python manage.py makemigrations projects`
        `python manage.py makemigrations users`

- Сделать миграции

        `python manage.py migrate`

- Создать супер пользователя

        `python manage.py createsuperuser`

- Запустить сервис

        `python manage.py runserver` -> будет на localhost:8000
        
# Для моделей
- streamlit с входным фалйом app.py
- Файл с requirements