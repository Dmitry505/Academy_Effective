# Academy_Effective

## Макет сайта для обучения backend разработке (Django)

Этот репозиторий содержит простой сайт с учётом книг
locallibrary, подключённой базой данных, созданной админ панели,
нескольких страниц с информацией из бд и счётчиком сессий.

Сделанный по обучаемому примеру с сайта:
https://developer.mozilla.org/ru/docs/Learn/Server-side/Django

## В ходе 2й лабораторной:

### Были пройдены разделы:
* 5: Создание домашней страницы
* 6: Отображение списков и детальной информации
* 7: Сессии
* 
### Было получено:
* Дополненный сайт из первой лабораторной работы
* URL и шаблоны страниц
* Главная (домашняя) страница
* Функционал базовой библиотеки
* Сессии для оптимизации работы с анонимными пользователями

## Необходимые инструменты 
* Python (3.12.6)
* Poetry (1.8.3)


# Установка и запуск

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Dmitry505/Academy_Effective
   cd Academy_Effective/lab_2

2. Установите зависимости:

    ```bash
    poetry install
   
3. Перемещений в нужный каталог

    ```bash
   cd .\locallibrary\

4. Создание .env

    ```bash
   echo SECRET_KEY= > .env
   echo DEBUG= >> .env

5. Откройте файл .env и введите значение ключа и дэбага.

    ```bash
   SECRET_KEY=<secret-key-value>
   DEBUG=<debug-value>

6. Создание миграций  в бд

    ```bash
   py manage.py makemigrations
   py manage.py migrate

7. Запуск сервера

    ```bash
    py manage.py runserver


    