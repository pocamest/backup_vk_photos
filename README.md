# Резервное копирование ВК фотографий

## Описание

Программа предназначена для резервного копирования фотографий пользователей ВК

## Начало работы

Проект написан на Python 3.10.12

### Установка необходмых зависимостей:

```bash
pip install -r requirements.txt
```

### Токен VK

Токен VK ID должен храниться в файле `.env`, который находится в корневой директории проекта. Формат записи следующий:

`VK_TOKEN=<ваш_токен_VK>`

## Использование

Чтобы запустить программу, перейдите в корень проекта и выполните команду:

```bash
python main.py
```

После запуска вам потребуется ввести идентификатор пользователя ВКонтакте и OAuth-токен от Яндекса.Диск.

Программа создаст папку на Яндекс.Диске и загрузит туда до пяти фотографий профиля указанного пользователя.

## Параметры

Вы можете изменить конечный путь сохранения файлов, отредактировав первый аргумент метода `upload_photo()` в файле `main.py`.

Если указанный каталог уже существует, программа сохранит файлы в него. Если же такой каталог отсутствует, он будет создан автоматически.

Кроме того, вы можете сохранить все альбомы пользователя, установив значение параметра `save_all_albums` в методе `get_photos()` равным `True`.

Количество загружаемых фотографий можно изменить, задав нужное значение переменной `count_photos` в классе VK.