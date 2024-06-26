## веб приложение учета товаров на складе

Применены технологии Flask, SQLAlchemy, MySQL, jquerry, ajax
Приложение может быть использовано локально без подключения к интернет, вся статика и js скачаны в `static`, без адаптации к мобильным устройствам

### Как установить

- код адаптирован под Python3.10, это минимальное требование для установки
- Установить зависимости командой
```
pip install -r requirements.txt
```

### Как запустить

Необходимо подготовить базу данных Mysql, прописать данные в файле `.env` в виде
```text
DATABASE=mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}
```
для запуска в `dev` режиме выполнить команду
```
python3 app.py
```
для запуска в режиме `prod`:
```
gunicorn -b :8080 app:app
```

### Frontend дополнения

Основа jquery кода для клавиш "+" и "-" взят с сайта [atuin.ru](https://atuin.ru/blog/plyus-i-minus-dlya-polya-input/) с добавлением ajax, кнопка удаления товара написана на подобии

### Docker
Подготовлен Dockerfile для быстрого опубликования в `prod`

### Пример работы приложения
Посмотреть пример работы приложения можно по [ссылке](http://95.163.242.132)

### Цель проекта
Приложение подготовлено как тестовое задание по данному [notion](https://alkrivda.notion.site/6a52ccac004f49e39dcc4e2f9f01756f?pvs=74)


