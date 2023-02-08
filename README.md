# Проект Foodgram - «Продуктовый помощник»
Сервис, который позволяет пользователям публиковать свои рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Запуск проекта через Docker

Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

Клонируйте репозиторий с проектом на свой компьютер.
В терминале из рабочей директории выполните команду:
```
git clone https://github.com/haus2100/foodgram-project-react.git
```
Перейдите в папку foodgram-project-react/infra
```
cd foodgram-project-react/infra
```

Выполните команду:
```
docker-compose up -d --build
```

### Для работы с удаленным сервером (на ubuntu):
* Выполните вход на свой удаленный сервер.

* Установите docker на сервер:
```
sudo apt install docker.io 
```
* Установите docker-compose на сервер. [Установка и использование Docker Compose в Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-ru)
* Локально отредактируйте файл infra/nginx/default.conf.conf, в строке server_name впишите свой IP
* Скопируйте файлы docker-compose.yml и nginx.conf из папки infra на сервер:
```
scp infra/docker-compose.yml <username>@<ip host>:/home/<username>/docker-compose.yml
scp infra/nginx.conf <username>@<ip host>:/home/<username>/nginx.conf
```
* Скопируйте папку docs на сервер:
```
scp -r docs <username>@<ip host>@130.193.43.140:/home/<username>/
```

* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя на DockerHub>

    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    SSH_KEY=<ваш SSH ключ (для получения выполните команду: cat ~/.ssh/id_rsa)>
    PASSPHRASE=<если при создании ssh-ключа вы использовали фразу-пароль>

    ```
* Workflow состоит из четырех шагов:
     - Проверка кода на соответствие PEP8 и выполнение тестов, реализованных в проекте
     - Сборка и публикация образа приложения на DockerHub.
     - Автоматическое скачивание образа приложения и деплой на удаленном сервере.
     - Отправка уведомления в телеграм-чат.  
  

* После успешного развертывания проекта на удаленном сервере, можно выполнить:
    - Создать суперпользователя Django:
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
    - Импортровать в БД ингредиенты, чтобы пользователи могли ими пользоваться при создании рецептов:  
    ```
    sudo docker-compose exec backend python3 manage.py import_ingredients
