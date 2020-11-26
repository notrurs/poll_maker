# API Создания опросов
API для платформы создания опросов и вопросов к ним. Платформа позволяет администратору создавать опросы и с точки
зрения архитектуры это будет выглядеть так:
```
Опрос <- Вопрос <- Вариант ответа
```
Таким образом, Вопросы связыватся с Опросами, а Варианты ответов с Вопросами.
Обычные пользователи могут получать список активных опросов и проходить их.
## Оглавление
* [Перед началом работы](#Перед-началом-работы)
    * [Установка](#Установка)
* [Документация к API](#Документация-к-API)
    * [Авторизация в системе](#Авторизация-в-системе)
    * [Функционал администратора](#Функционал-администратора)
        * [API Опросов](#API-Опросов)
            * [Получение списка всех опросов](#Получение-списка-всех-опросов)
            * [Создание опроса](#Создание-опроса)
            * [Обновление опроса](#Обновление-опроса)
            * [Удаление опроса](#Удаление-опроса)
        * [API Вопросов](#API-Вопросов)
            * [Создание вопроса](#Создание-вопроса)
            * [Обновление вопроса](#Обновление-вопроса)
            * [Удаление вопроса](#Удаление-вопроса)
        * [API Вариантов ответа](#API-Вариантов-ответа)
            * [Создание варианта ответа](#Создание-варианта-ответа)
            * [Обновление варианта ответа](#Обновление-варианта-ответа)
            * [Удаление варианта ответа](#Удаление-варианта-ответа)
    * [Функционал пользователя](#Функционал-пользователя)
        * [Получение всех активных опросов](#Получение-всех-активных-опросов)
        * [Прохождение опроса](#Прохождение-опроса)
        * [Просмотр всех ответов пользователей](#Просмотр-всех-ответов-пользователей)
## Перед началом работы

### Установка

Шаг 1. Клонируйте этот репозиторий

Шаг 2. Установите зависимости:
```
pip install -r requirements.txt
```

Шаг 3. Перейдите в папку `poll_maker`:
```
cd poll_maker
```

Шаг 4. Сделайте миграции:
```
python manage.py makemigrations
python manage.py migrate
```

Шаг 5. Запустите сервер:
```
python manage.py runserver
```
## Документация к API
### Авторизация в системе
Перед авторизацией убедитесь, что авторизируемый пользователь присутствует в базе Users

Метод: POST

URL: http://localhost:8000/api/v1/login/

Тело запроса:
* username: логин
* password: пароль

Пример: 
```
curl --location --request POST "http://localhost:8000/api/v1/create_poll/" \
--form "username=%логин%" \
--form "password=%пароль%"
```

На выходе метод возвращает токен пользователя, который необходим для дальнейшей работы с API
### Функционал администратора
Администратор может:
* Создавать, удалять и изменять опросы
* Получать список всех опросов (активных и неактивных)
* Создавать, удалять и изменять вопросы
* Создавать, удалять и изменять варианты ответов
* Возможности обычного пользователя
#### API Опросов
##### Получение списка всех опросов
Метод: GET

URL: http://localhost:8000/api/v1/list_polls/

Заголовок:
*  Authorization: Token %токен%

Пример: 
```
curl --location --request GET "http://localhost:8000/api/v1/list_polls/" \
--header "Authorization: Token %токен%"
```

##### Создание опроса
Метод: POST

URL: http://localhost:8000/api/v1/create_poll/

Заголовок:
*  Authorization: Token %токен%

Тело запроса:
* poll_name: название опроса
* poll_date_start: дата начала опроса, формат записи: YYYY-MM-DD HH:MM
* poll_date_end: дата конца опроса, формат записи: YYYY-MM-DD HH:MM
* Poll_description: описание опроса

Пример: 
```
curl --location --request POST "http://localhost:8000/api/v1/create_poll/" \
--header "Authorization: Token %токен%" \
--form "poll_name=%название опроса%" \
--form "poll_date_start=%дата начала опроса%" \
--form "poll_date_end=%дата конца опроса%" \
--form "poll_description=%описание опроса%"
```

##### Обновление опроса
Метод: PATCH

URL: http://localhost:8000/api/v1/update_poll/%question_id%/

Заголовок:
*  Authorization: Token %токен%

Тело запроса:
* poll_name: название опроса
* poll_date_end: дата конца опроса, формат записи: YYYY-MM-DD HH:MM
* Poll_description: описание опроса

Примечание: дату начала опроса поменять нельзя!

Пример: 
```
curl --location --request PATCH "http://localhost:8000/api/v1/update_poll/%id_вопроса%/" \
--header "Authorization: Token %токен%" \
--form "poll_name=%название опроса%" \
--form "poll_date_end=%дата конца опроса%" \
--form "poll_description=%описание опроса%"
```

##### Удаление опроса
Метод: DELETE

URL: http://localhost:8000/api/v1/delete_poll/%poll_id%/

Заголовок:
*  Authorization: Token %токен%

Пример: 
```
curl --location --request DELETE "http://localhost:8000/api/v1/delete_poll/%id_опроса%/" \
--header "Authorization: Token %токен%"
```

#### API Вопросов
##### Создание вопроса
Метод: POST

URL: http://localhost:8000/api/v1/create_question/

Заголовок:
*  Authorization: Token %токен%

Тело запроса:
* question_text: текст вопроса
* question_type: тип вопроса (`one` - один вариант ответа, `multiple` - несколько вариантов, `text` - ответ на вопрос даётся текстом)
* poll: id опроса, к которому нужно прикрепить создаваемый вопрос

Пример: 
```
curl --location --request POST "http://localhost:8000/api/v1/create_question/" \
--header "Authorization: Token %токен%" \
--form "question_text=%текст вопроса%" \
--form "question_type=%тип вопроса%" \
--form "poll=%id вопроса%"
```

##### Обновление вопроса
Метод: PATCH

URL: http://localhost:8000/api/v1/update_question/%question_id%/

Заголовок:
*  Authorization: Token %токен%

Тело запроса:
* question_text: текст вопроса
* question_type: тип вопроса (`one` - один вариант ответа, `multiple` - несколько вариантов, `text` - ответ на вопрос даётся текстом)
* poll: id опроса, к которому нужно прикрепить создаваемый вопрос

Пример: 
```
curl --location --request PATCH "http://localhost:8000/api/v1/update_poll/%id вопроса%/" \
--header "Authorization: Token %токен%" \
--form "question_text=%текст вопроса%" \
--form "question_type=%тип вопроса%" \
--form "poll=%id вопроса%"
```

##### Удаление вопроса
Метод: DELETE

URL: http://localhost:8000/api/v1/delete_question/%question_id%/

Заголовок:
*  Authorization: Token %токен%

Пример: 
```
curl --location --request DELETE "http://localhost:8000/api/v1/delete_question/%id_question%/" \
--header "Authorization: Token %токен%"
```

#### API Вариантов ответа
##### Создание варианта ответа
Метод: POST

URL: http://localhost:8000/api/v1/create_choice/

Заголовок:
*  Authorization: Token %токен%

Тело запроса:
* choice_text: текст варианта ответа
* question: id вопроса, к которому нужно прикрепить создаваемый вариант ответа

Пример: 
```
curl --location --request POST "http://localhost:8000/api/v1/create_choice/" \
--header "Authorization: Token %токен%" \
--form "choice_text=%текст варианта ответа%" \
--form "question=%id варианта ответа%"
```

##### Обновление варианта ответа
Метод: PATCH

URL: http://localhost:8000/api/v1/update_choice/%choice_id%/

Заголовок:
*  Authorization: Token %токен%

Тело запроса:
* choice_text: текст варианта ответа
* question: id вопроса, к которому нужно прикрепить создаваемый вариант ответа

Пример: 
```
curl --location --request PATCH "http://localhost:8000/api/v1/update_poll/%id вопроса%/" \
--header "Authorization: Token %токен%" \
--form "choice_text=%текст варианта ответа%" \
--form "question=%id варианта ответа%"
```

##### Удаление варианта ответа
Метод: DELETE

URL: http://localhost:8000/api/v1/delete_choice/%choice_id%/

Заголовок:
*  Authorization: Token %токен%

Пример: 
```
curl --location --request DELETE "http://localhost:8000/api/v1/delete_choice/%id_choice%/" \
--header "Authorization: Token %токен%"
```

### Функционал пользователя
Пользователь может:
* Получить список активных опросов
* Пройти опрос
* Посмотреть на ответы всех пользователей
#### Получение всех активных опросов
Метод: GET

URL: http://localhost:8000/api/v1/active_polls/

Заголовок:
*  Authorization: Token %токен%

Пример: 
```
curl --location --request GET "http://localhost:8000/api/v1/active_polls/" \
--header "Authorization: Token %токен%"
```

#### Прохождение опроса
Метод: POST

URL: http://localhost:8000/api/v1/create_answer/

Заголовок:
*  Authorization: Token %токен%

Тело запроса:
* user_id: id пользователя
* question: id вопроса
* choice: id ответа на вопрос
* choice_text: для текста на вопрос, если ответ должен быть текстовым

Пример: 
```
curl --location --request POST "http://localhost:8000/api/v1/create_answer/" \
--header "Authorization: Token %токен%" \
--form "user_id=%id пользователя%" \
--form "question=%id вопроса%" \
--form "choice=%id ответа на вопрос%" \
--form "choice_text=%ответ текстом%"
```

#### Просмотр всех ответов пользователей
Метод: GET

URL: http://localhost:8000/api/v1/answers/

Заголовок:
*  Authorization: Token %токен%

Пример: 
```
curl --location --request GET "http://localhost:8000/api/v1/answers/" \
--header "Authorization: Token %токен%"
```
