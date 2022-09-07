![example workflow](https://github.com/haus2100/foodgram-project-react/actions/workflows/main.yml/badge.svg)

### Проект доступен по адресу: http://130.193.43.140



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

### Выполните миграции:
```
docker-compose exec backend python manage.py migrate
```

### Загрузите статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```

### Заполните базу тестовыми данными:
```
docker-compose exec backend python manage.py loaddata fixtures.json
```
Теперь приложение будет доступно в браузере по адресу localhost/admin/
Логин: admin@admin.ru
пароль: admin
