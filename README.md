# Foodgram - Продуктовый помощник.

![workflow](https://github.com/artemis1359/foodgram-project-react/actions/workflows/main.yml/badge.svg)


## Описание проекта
Проект «Фудграм» — сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Технологии

- [Python 3.9.10](https://www.python.org/downloads/)
- [Django 3.2](https://www.djangoproject.com/)
- [Django Rest Framewok 3.12.4](https://www.django-rest-framework.org/)
- [PostgreSQL](https://postgrespro.ru/docs/postgresql)
 
## Установка проекта на локальный компьютер из репозитория 
 - Клонировать репозиторий `git clone git@github.com:Artemis1359/foodgram-project-react.git`
 - перейти в директорию с клонированным репозиторием
 - в корневой директории создайте файл .env
 - в файле .env прописать ваши данные
 - установить виртуальное окружение `python3 -m venv venv`
 - активировать виртуальное окружение `source venv/bin/activate` (Linux/masOS), `source venv/Scripts/activate` (Windows)
 - установить зависимости `pip install -r requirements.txt`
 - выполнить миграции `python3 manage.py migrate`
 - запустить сервер `python3 manage.py runserver`

### Создание Docker-образов

1.  Создаём образы для установки на сервер. Замените username на ваш логин на DockerHub:

    ```bash
    cd ..
    docker build -t username/backend:latest backend/
    docker build -t username/frontend:latest frontend/
    docker build -t username/nginx:latest nginx/
    ```

2. Загрузите образы на DockerHub:

    ```bash
    docker push username/frontend
    docker push username/backend
    docker push username/nginx
    ```

### Деплой на сервере

1. Подключитесь к удаленному серверу

    ```bash
    ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом имя_пользователя@ip_адрес_сервера 
    ```

2. Создайте на сервере директорию foodgram через терминал

    ```bash
    mkdir foodgram
    ```

3. Установка docker compose на сервер:

    ```bash
    sudo apt update
    sudo apt install curl
    curl -fSL https://get.docker.com -o get-docker.sh
    sudo sh ./get-docker.sh
    sudo apt-get install docker-compose-plugin
    ```

4. В директорию foodgram/ скопируйте файлы docker-compose.production.yml и .env:

    ```bash
    scp -i path_to_SSH/SSH_name docker-compose.production.yml username@server_ip:/home/username/foodgram/docker-compose.production.yml
    * path_to_SSH — путь к файлу с SSH-ключом;
    * SSH_name — имя файла с SSH-ключом;
    * username — ваше имя пользователя на сервере;
    * server_ip — IP вашего сервера.
    ```

5. Запустите docker compose в режиме демона:

    ```bash
    sudo docker compose -f docker-compose.production.yml up -d
    ```

6. Выполните миграции, соберите статические файлы бэкенда и скопируйте их в /static/:

    ```bash
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
    sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /backend_static/static/
    ```
    Создайте администратора:

    ```bash
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
    ```
    Заполните базу данных:
    ```bash
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py loaddata
    ```

7. На сервере в редакторе nano откройте конфиг Nginx:

    ```bash
    sudo nano /etc/nginx/sites-enabled/default
    ```

8. Измените настройки location в секции server:

    ```bash
    location / {
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:8000;
    }
    ```

9. Проверьте работоспособность конфига Nginx:

    ```bash
    sudo nginx -t
    ```
    Если ответ в терминале такой, значит, ошибок нет:
    ```bash
    nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    nginx: configuration file /etc/nginx/nginx.conf test is successful
    ```

10. Перезапускаем Nginx
    ```bash
    sudo service nginx reload
    ```

### Настройка CI/CD

1. Файл workflow уже написан. Он находится в директории

    ```bash
    foodgram/.github/workflows/main.yml
    ```

2. Для адаптации его на своем сервере добавьте секреты в GitHub Actions:

    ```bash
    DOCKER_USERNAME                # имя пользователя в DockerHub
    DOCKER_PASSWORD                # пароль пользователя в DockerHub
    HOST                           # ip_address сервера
    USER                           # имя пользователя
    SSH_KEY                        # приватный ssh-ключ (cat ~/.ssh/id_rsa)
    SSH_PASSPHRASE                 # кодовая фраза (пароль) для ssh-ключа

    TELEGRAM_TO                    # id телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
    TELEGRAM_TOKEN                 # токен бота (получить токен можно у @BotFather, /token, имя бота)
    ```


## Автор
Потапов Артем - [GitHub](https://github.com/artemis1359)
