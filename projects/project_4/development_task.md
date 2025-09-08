# Задача на разработку новой операции API

## Название
Сортировка списка фильмов и сериалов по рейтингу зрителей и кинокритиков.

## Цель
Дать пользователям возможность сортировать контент по рейтингу кинокритиков и пользовательскому рейтингу для облегчения выбора фильмов и сериалов для просмотра.

## Требование
Пользователь должен иметь возможность сортировать список фильмов и сериалов по рейтингу кинокритиков или пользовательскому рейтингу в порядке возрастания или убывания, при этом контент без рейтинга кинокритиков должен отображаться в конце списка.

## UseCase
В разделе «Библиотека» пользователь видит список фильмов и сериалов.
Пользователь в интерфейсе выбирает параметры, по которым он хочет отфильтровать список фильмов и сериалов, и/или режим сортировки.
Система возвращает список фильмов и сериалов, отфильтрованный и отсортированный согласно указанным данным.

## Описание изменений

### Необходимо доработать Films Server API.
1.1. В ответ {{FilmsServer}}/films/list добавить новое поле criticsRating.
1.2. В ответ {{FilmsServer}}/films добавить новое поле criticsRating.

### Необходимо доработать Series Server API.
2.1. В ответ {{SeriesServer}}/series/list добавить новое поле criticsRating.
2.2. В ответ {{SeriesServer}}/series добавить новое поле criticsRating.

### Необходимо доработать Web Server API.
3.1. В запрос {{WebServer}}/content/list добавить параметры сортировки sortBy и direction.
3.2. В ответ {{WebServer}}/content/list добавить новое поле criticsRating.

## Контекст
В ответе запроса {{FilmsServer}}/films/list и {{SeriesServer}}/series/list уже есть рейтинг зрителей rating, по которому так же нужно будет выполнять сортировку.

---

## Операции Films Server API

### 1.1. В ответ {{FilmsServer}}/films/list необходимо добавить новое опциональное поле criticsRating. Поле должно заполняться данными о рейтинге кинокритиков.

**Тип метода**
GET

**URL запроса**
/films/list

**Параметры запроса**
-

**Пример запроса**
https://2ee4902e-6893-4bf2-9b6f-88b9f5fcb78a.mock.pstmn.io/films/list

**Элементы тела запроса**
-

**Пример ответа**
```json
[   
   {
       "id": 101,
       "type": "film",
       "title": "Хосэ Каньон",
       "description": "Хосэ Каньон — добрый и открытый парень — устроился в офис электриком и рассказывает коллегам историю своей необыкновенной жизни.",
       "imageUrl": "https://otium.imagestorage.ru/JoseCanyon.img",
       "previewUrl": "https://otium.previewstorage.ru/JoseCanyon.mov",
       "recordUrl": "https://otium.recordstorage.ru/JoseCanyon.mov",
       "genre": [
           "comedy"
       ],
       "recommended": true,
       "details": {
           "yearOfIssue": "1995",
           "duration": 152,
           "country": [
               "США"
           ],
           "ageRate": "16+"
       },
       "rating": 9.4,
       "criticsRating": 7.4
   }
]
```

**Элементы ответа, которые нужно добавить**
- **criticsRating** (number, опциональное) - рейтинг кинокритиков от 0.0 до 10.0, может быть null для контента без рейтинга

**Ошибки**
Изменения не требуются

### 1.2. В ответ {{FilmsServer}}/films в объект с описанием фильма необходимо добавить новое опциональное поле criticsRating. Поле должно заполняться данными о рейтинге кинокритиков.

**Тип метода**
GET

**URL запроса**
/films

**Параметры запроса**
Изменения не требуются

**Пример запроса**
https://2ee4902e-6893-4bf2-9b6f-88b9f5fcb78a.mock.pstmn.io/films?id=101

**Элементы тела запроса**
-

**Пример ответа**
```json
{
       "id": 101,
       "type": "film",
       "title": "Хосэ Каньон",
       "description": "Хосэ Каньон — добрый и открытый парень — устроился в офис электриком и рассказывает коллегам историю своей необыкновенной жизни.",
       "imageUrl": "https://otium.imagestorage.ru/JoseCanyon.img",
       "previewUrl": "https://otium.previewstorage.ru/JoseCanyon.mov",
       "recordUrl": "https://otium.recordstorage.ru/JoseCanyon.mov",
       "genre": [
           "comedy"
       ],
       "recommended": true,
       "details": {
           "yearOfIssue": "1995",
           "duration": 152,
           "country": [
               "США"
           ],
           "ageRate": "16+"
       },
       "language": {
           "original": [
               "английский"
           ],
           "sound": [
               "русский",
               "английский"
           ],
           "subtitle": [
               "русский",
               "английский"
           ]
       },
       "team": {
           "cast": [
               "Джон Джэксон",
               "Джулия Блэйк"
           ],
           "dubbingTeam": [
               "Дэвид Браун"
           ]
       },
       "rating": 9.4,
       "criticsRating": 7.4
   }
```

**Элементы ответа, которые нужно добавить**
- **criticsRating** (number, опциональное) - рейтинг кинокритиков от 0.0 до 10.0, может быть null для контента без рейтинга

**Ошибки**
Изменения не требуются

---

## Операции Series Server API

### 2.1. В ответ {{SeriesServer}}/series/list необходимо добавить новое опциональное поле criticsRating. Поле должно заполняться данными о рейтинге кинокритиков.

**Тип метода**
GET

**URL запроса**
/series/list

**Параметры запроса**
-

**Пример запроса**
https://2ee4902e-6893-4bf2-9b6f-88b9f5fcb78a.mock.pstmn.io/series/list

**Элементы тела запроса**
-

**Пример ответа**
```json
[   
   {
       "id": 201,
       "type": "serie",
       "title": "Загадка города Эльдорадо",
       "description": "Географа подозревают в написании книги, которую он не писал. Герой знакомится с журналисткой мексиканской газеты Глорией, вместе они пытаются раскрыть тайну мифического города.",
       "imageUrl": "https://otium.imagestorage.ru/MysteryOfEldorado.img",
       "previewUrl": "https://otium.previewstorage.ru/MysteryOfEldorado.mov",
       "recordUrl": "https://otium.recordstorage.ru/MysteryOfEldorado.mov",
       "genre": [
           "action"
       ],
       "recommended": true,
       "details": {
           "yearOfIssue": "2007",
           "episodesCount": 12,
           "country": [
               "Великобритания",
               "Турция",
               "США"
           ],
           "ageRate": "12+"
       },
       "rating": 6.5,
       "criticsRating": 8.2
   }
]
```

**Элементы ответа, которые нужно добавить**
- **criticsRating** (number, опциональное) - рейтинг кинокритиков от 0.0 до 10.0, может быть null для контента без рейтинга

**Ошибки**
Изменения не требуются

### 2.2. В ответ {{SeriesServer}}/series в объект с описанием сериала необходимо добавить новое опциональное поле criticsRating. Поле должно заполняться данными о рейтинге кинокритиков.

**Тип метода**
GET

**URL запроса**
/series

**Параметры запроса**
Изменения не требуются

**Пример запроса**
https://2ee4902e-6893-4bf2-9b6f-88b9f5fcb78a.mock.pstmn.io/series?id=201

**Элементы тела запроса**
-

**Пример ответа**
```json
{
       "id": 201,
       "type": "serie",
       "title": "Загадка города Эльдорадо",
       "description": "Географа подозревают в написании книги, которую он не писал. Герой знакомится с журналисткой мексиканской газеты Глорией, вместе они пытаются раскрыть тайну мифического города.",
       "imageUrl": "https://otium.imagestorage.ru/MysteryOfEldorado.img",
       "previewUrl": "https://otium.previewstorage.ru/MysteryOfEldorado.mov",
       "recordUrl": "https://otium.recordstorage.ru/MysteryOfEldorado.mov",
       "genre": [
           "action"
       ],
       "recommended": true,
       "details": {
           "yearOfIssue": "2007",
           "episodesCount": 12,
           "country": [
               "Великобритания",
               "Турция",
               "США"
           ],
           "ageRate": "12+"
       },
       "language": {
           "original": [
               "английский",
               "турецкий"
           ],
           "sound": [
               "русский",
               "английский"
           ],
           "subtitle": [
               "русский",
               "английский",
               "турецкий"
           ]
       },
       "rating": 6.5,
       "criticsRating": 8.2
   }
```

**Элементы ответа, которые нужно добавить**
- **criticsRating** (number, опциональное) - рейтинг кинокритиков от 0.0 до 10.0, может быть null для контента без рейтинга

**Ошибки**
Изменения не требуются

---

## Операции Web Server API

### 3.1. В запрос {{WebServer}}/content/list добавить два query-параметра: sortBy и direction.

Поле sortBy может принимать два значения:
- Если "sortBy": "rating", внутри массива сортировка элементов должна выполняться по полю rating (пользовательский рейтинг);
- Если "sortBy": "criticsRating", внутри массива сортировка элементов должна выполняться по полю criticsRating (рейтинг кинокритиков).

Поле direction может принимать два значения:
- Если "direction": "desc", внутри массива элементы должны сортироваться по параметру sortBy по убыванию;
- Если "direction": "asc", внутри массива элементы должны сортироваться по параметру sortBy по возрастанию.

**Тип метода**
GET

**URL запроса**
/content/list

**Параметры запроса, которые нужно добавить**
- **sortBy** (string, опциональное) - поле для сортировки, возможные значения: "rating", "criticsRating"
- **direction** (string, опциональное) - направление сортировки, возможные значения: "asc", "desc", по умолчанию "desc"

**Пример запроса**
https://2ee4902e-6893-4bf2-9b6f-88b9f5fcb78a.mock.pstmn.io/content/list?sortBy=criticsRating&direction=desc

**Элементы тела запроса**
-

**Пример ответа**
```json
[   
   {
       "id": 201,
       "type": "serie",
       "title": "Индийский океан и я",
       "description": "Погрузитесь в веселые приключения на берегу Индийского океана, где дети вместе с местными животными учатся ценить природу и дружбу.",
       "imageUrl": "https://otium.imagestorage.ru/IndianOcean&I.img",
       "previewUrl": "https://otium.previewstorage.ru/IndianOcean&I.mov",
       "recordUrl": "https://otium.recordstorage.ru/IndianOcean&I.mov",
       "genre": [
           "kids"
       ],
       "recommended": false,
       "details": {
           "yearOfIssue": "2015",
           "episodesCount": 4,
           "country": [
               "Индонезия"
           ],
           "ageRate": "6+"
       },
       "rating": 9.5,
       "criticsRating": 8.4
   },
   {
       "id": 101,
       "type": "film",
       "title": "Хосэ Каньон",
       "description": "Хосэ Каньон — добрый и открытый парень — устроился в офис электриком и рассказывает коллегам историю своей необыкновенной жизни.",
       "imageUrl": "https://otium.imagestorage.ru/JoseCanyon.img",
       "previewUrl": "https://otium.previewstorage.ru/JoseCanyon.mov",
       "recordUrl": "https://otium.recordstorage.ru/JoseCanyon.mov",
       "genre": [
           "comedy"
       ],
       "recommended": true,
       "details": {
           "yearOfIssue": "1995",
           "duration": 152,
           "country": [
               "США"
           ],
           "ageRate": "16+"
       },
       "rating": 9.4,
       "criticsRating": 7.4
   }
]
```

**Элементы ответа, которые нужно добавить**
- **criticsRating** (number, опциональное) - рейтинг кинокритиков от 0.0 до 10.0, может быть null для контента без рейтинга

**Ошибки**
- **400** - неверные значения параметров sortBy или direction
- **422** - некорректные значения параметров сортировки

### 3.2. В ответ {{WebServer}}/content/list добавить новое поле criticsRating.

**Тип метода**
GET

**URL запроса**
/content/list

**Параметры запроса**
Изменения не требуются

**Пример запроса**
https://2ee4902e-6893-4bf2-9b6f-88b9f5fcb78a.mock.pstmn.io/content/list

**Элементы тела запроса**
-

**Пример ответа**
```json
[   
   {
       "id": 201,
       "type": "serie",
       "title": "Загадка города Эльдорадо",
       "description": "Географа подозревают в написании книги, которую он не писал. Герой знакомится с журналисткой мексиканской газеты Глорией, вместе они пытаются раскрыть тайну мифического города.",
       "imageUrl": "https://otium.imagestorage.ru/MysteryOfEldorado.img",
       "previewUrl": "https://otium.previewstorage.ru/MysteryOfEldorado.mov",
       "recordUrl": "https://otium.recordstorage.ru/MysteryOfEldorado.mov",
       "genre": [
           "action"
       ],
       "recommended": true,
       "details": {
           "yearOfIssue": "2007",
           "episodesCount": 12,
           "country": [
               "Великобритания",
               "Турция",
               "США"
           ],
           "ageRate": "12+"
       },
       "rating": 6.5,
       "criticsRating": 8.2
   },
   {
       "id": 101,
       "type": "film",
       "title": "Хосэ Каньон",
       "description": "Хосэ Каньон — добрый и открытый парень — устроился в офис электриком и рассказывает коллегам историю своей необыкновенной жизни.",
       "imageUrl": "https://otium.imagestorage.ru/JoseCanyon.img",
       "previewUrl": "https://otium.previewstorage.ru/JoseCanyon.mov",
       "recordUrl": "https://otium.recordstorage.ru/JoseCanyon.mov",
       "genre": [
           "comedy"
       ],
       "recommended": true,
       "details": {
           "yearOfIssue": "1995",
           "duration": 152,
           "country": [
               "США"
           ],
           "ageRate": "16+"
       },
       "rating": 9.4,
       "criticsRating": 7.4
   }
]
```

**Элементы ответа, которые нужно добавить**
- **criticsRating** (number, опциональное) - рейтинг кинокритиков от 0.0 до 10.0, может быть null для контента без рейтинга

**Ошибки**
Изменения не требуются

---

## Логика сортировки

### Алгоритм сортировки по рейтингу кинокритиков:
1. Получить все фильмы и сериалы из Films Server API и Series Server API
2. Применить существующую фильтрацию по типу контента (если указана)
3. Разделить контент на две группы:
   - С рейтингом кинокритиков (criticsRating != null)
   - Без рейтинга кинокритиков (criticsRating == null)
4. Отсортировать первую группу по полю criticsRating согласно параметру direction
5. Добавить вторую группу в конец списка (независимо от направления сортировки)
6. Вернуть объединенный отсортированный список

### Алгоритм сортировки по пользовательскому рейтингу:
1. Получить все фильмы и сериалы из Films Server API и Series Server API
2. Применить существующую фильтрацию по типу контента (если указана)
3. Отсортировать весь список по полю rating согласно параметру direction
4. Вернуть отсортированный список

### Примеры запросов:
- `GET /content/list?sortBy=criticsRating&direction=desc` - по убыванию рейтинга кинокритиков
- `GET /content/list?sortBy=criticsRating&direction=asc` - по возрастанию рейтинга кинокритиков
- `GET /content/list?sortBy=rating&direction=desc` - по убыванию пользовательского рейтинга
- `GET /content/list?type=film&sortBy=criticsRating&direction=desc` - фильмы по убыванию рейтинга кинокритиков
