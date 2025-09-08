# Результаты тестирования API в Swagger

## Обзор тестирования

**Цель:** Проанализировать существующие API и определить необходимые изменения для добавления рейтинга кинокритиков и сортировки.

**Swagger URL:** https://app.swaggerhub.com/apis-docs/Otium/Otium_REST/1.0.0

## Анализ Web Server API

### Текущий эндпоинт: `GET /content/list`

**Параметры запроса:**
- `contentType` (string, optional) - тип контента (film/series/all)
- `genre` (string, optional) - фильтр по жанру
- `page` (integer, optional) - номер страницы
- `pageSize` (integer, optional) - размер страницы

**Тело ответа:**
```json
{
  "contentList": [
    {
      "contentId": "string",
      "contentType": "string",
      "title": "string",
      "description": "string",
      "imageUrl": "string",
      "previewUrl": "string",
      "recordUrl": "string",
      "genre": ["string"],
      "recommended": true,
      "exclusive": true,
      "details": {
        "yearOfIssue": 2024,
        "duration": "PT95M",
        "country": "string",
        "ageRate": "string"
      },
      "team": {
        "cast": ["string"],
        "dubbingTeam": "string"
      },
      "rating": 7.8
    }
  ],
  "total": 100,
  "page": 1,
  "pageSize": 20
}
```

### Анализ текущих возможностей

**✅ Что есть:**
- Фильтрация по типу контента (`contentType`)
- Фильтрация по жанру (`genre`)
- Пагинация (`page`, `pageSize`)
- Пользовательский рейтинг (`rating`)
- Признак эксклюзивности (`exclusive`)

**❌ Чего не хватает:**
- Параметры сортировки (`sortBy`, `sortOrder`)
- Рейтинг кинокритиков в ответе
- Сортировка по рейтингу кинокритиков
- Сортировка по пользовательскому рейтингу

## Анализ Films Server API

### Текущий эндпоинт: `GET /films/list`

**Параметры запроса:**
- `genre` (string, optional) - фильтр по жанру
- `page` (integer, optional) - номер страницы
- `pageSize` (integer, optional) - размер страницы

**Тело ответа:**
```json
{
  "films": [
    {
      "filmId": "string",
      "title": "string",
      "description": "string",
      "imageUrl": "string",
      "previewUrl": "string",
      "recordUrl": "string",
      "genre": ["string"],
      "recommended": true,
      "exclusive": true,
      "details": {
        "yearOfIssue": 2024,
        "duration": "PT95M",
        "country": "string",
        "ageRate": "string"
      },
      "team": {
        "cast": ["string"],
        "dubbingTeam": "string"
      },
      "rating": 7.8
    }
  ],
  "total": 50,
  "page": 1,
  "pageSize": 20
}
```

### Анализ текущих возможностей

**✅ Что есть:**
- Фильтрация по жанру
- Пагинация
- Пользовательский рейтинг (`rating`)
- Признак эксклюзивности (`exclusive`)

**❌ Чего не хватает:**
- Рейтинг кинокритиков (`criticsRating`)
- Параметры сортировки
- Сортировка по рейтингу кинокритиков

## Анализ Series Server API

### Текущий эндпоинт: `GET /series/list`

**Параметры запроса:**
- `genre` (string, optional) - фильтр по жанру
- `page` (integer, optional) - номер страницы
- `pageSize` (integer, optional) - размер страницы

**Тело ответа:**
```json
{
  "series": [
    {
      "seriesId": "string",
      "title": "string",
      "description": "string",
      "imageUrl": "string",
      "previewUrl": "string",
      "recordUrl": "string",
      "genre": ["string"],
      "recommended": true,
      "exclusive": true,
      "details": {
        "yearOfIssue": 2024,
        "episodesCount": 10,
        "country": "string",
        "ageRate": "string"
      },
      "team": {
        "cast": ["string"],
        "dubbingTeam": "string"
      },
      "rating": 8.2
    }
  ],
  "total": 30,
  "page": 1,
  "pageSize": 20
}
```

### Анализ текущих возможностей

**✅ Что есть:**
- Фильтрация по жанру
- Пагинация
- Пользовательский рейтинг (`rating`)
- Признак эксклюзивности (`exclusive`)

**❌ Чего не хватает:**
- Рейтинг кинокритиков (`criticsRating`)
- Параметры сортировки
- Сортировка по рейтингу кинокритиков

## Ответы на ключевые вопросы

### 1. Какую задачу или проблему пользователя необходимо решить?

**Проблема:** Пользователям сложно выбрать, что смотреть из большого количества фильмов и сериалов. Просмотр трейлеров к каждому фильму утомителен, и пользователи иногда уходят с платформы из-за сложности выбора.

**Решение:** Добавить рейтинг кинокритиков и возможность сортировки по этому рейтингу, чтобы пользователи могли быстро найти качественный контент.

### 2. Каким образом можно решить эту задачу или проблему?

**Способ решения:**
1. Добавить рейтинг кинокритиков к каждому фильму и сериалу
2. Предоставить возможность сортировки по рейтингу кинокритиков
3. Предоставить возможность сортировки по пользовательскому рейтингу
4. Контент без рейтинга кинокритиков показывать в конце списка

### 3. Чего сейчас в ПО и его интерфейсе не хватает, чтобы решить задачу или проблему?

**Не хватает:**
- Рейтинга кинокритиков в данных
- Параметров сортировки в API
- Логики сортировки в Web Server
- Отображения рейтинга кинокритиков в UI
- Элементов управления сортировкой в UI

### 4. Текущее Web Server API позволяет решить задачу или проблему пользователя?

**❌ НЕТ** - текущее API не поддерживает:
- Параметры сортировки (`sortBy`, `sortOrder`)
- Рейтинг кинокритиков в ответе
- Сортировку по рейтингу кинокритиков
- Сортировку по пользовательскому рейтингу

**Что должно измениться в Web Server API:**
- Добавить параметры `sortBy` (criticsRating, userRating) и `sortOrder` (asc, desc)
- Добавить поле `criticsRating` в ответ
- Реализовать логику сортировки с учетом контента без рейтинга

### 5. Films Server API и Series Server API удовлетворяют запросам Web Server API?

**❌ НЕТ** - текущие API не поддерживают:
- Рейтинг кинокритиков в ответе
- Параметры сортировки

**Что должно измениться в Films Server API:**
- Добавить поле `criticsRating` в ответ
- Добавить параметры сортировки (опционально)

**Что должно измениться в Series Server API:**
- Добавить поле `criticsRating` в ответ
- Добавить параметры сортировки (опционально)

## Рекомендации по доработке

### 1. Web Server API
**Добавить параметры:**
```json
{
  "sortBy": "criticsRating" | "userRating",
  "sortOrder": "asc" | "desc"
}
```

**Добавить в ответ:**
```json
{
  "criticsRating": 8.5,
  "hasCriticsRating": true
}
```

### 2. Films Server API
**Добавить в ответ:**
```json
{
  "criticsRating": 8.5,
  "hasCriticsRating": true
}
```

### 3. Series Server API
**Добавить в ответ:**
```json
{
  "criticsRating": 8.5,
  "hasCriticsRating": true
}
```

### 4. Логика сортировки
- При `sortBy: "criticsRating"` и `sortOrder: "asc"` - контент без рейтинга в конце
- При `sortBy: "criticsRating"` и `sortOrder: "desc"` - контент без рейтинга в конце
- Аналогично для `sortBy: "userRating"`

## Заключение

Текущие API не поддерживают требуемую функциональность. Необходимо доработать все три API для добавления рейтинга кинокритиков и сортировки. Основные изменения должны быть в Web Server API, где будет реализована логика сортировки.

---

**Дата тестирования:** [Текущая дата]
**Статус:** API проанализированы, требования к доработке определены
