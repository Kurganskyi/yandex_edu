# Отчет о тестировании API Otium

## Цель тестирования
Определить возможности существующего API для реализации новой функции сортировки контента по рейтингу кинокритиков и выявить необходимые изменения.

## Анализ требований пользователя

### Задача пользователя
Пользователи хотят сортировать фильмы и сериалы по рейтингу кинокритиков (по возрастанию и убыванию), чтобы легче выбирать контент для просмотра.

### Текущая проблема
- Пользователям сложно выбрать из множества фильмов/сериалов
- Существующий пользовательский рейтинг не всегда помогает (мало оценок для новых/непопулярных фильмов)
- Нет экспертной оценки от кинокритиков

### Требуемое решение
1. Добавить рейтинг кинокритиков для всех фильмов и сериалов
2. Реализовать сортировку по рейтингу кинокритиков (asc/desc)
3. Реализовать сортировку по пользовательскому рейтингу (asc/desc)
4. Контент без рейтинга кинокритиков показывать в конце списка
5. Сохранить существующую фильтрацию по жанру

## Анализ текущего API

### Web Server API (`/content/list`)

**Текущие возможности:**
- ✅ Фильтрация по типу контента (`type` параметр)
- ✅ Возвращает объединенный список фильмов и сериалов
- ✅ Содержит пользовательский рейтинг (`rating`)

**Недостающие возможности:**
- ❌ Параметры сортировки (`sortBy`, `sortOrder`)
- ❌ Рейтинг кинокритиков в ответе (`criticsRating`)
- ❌ Логика сортировки контента без рейтинга

**Необходимые изменения:**
1. Добавить параметры запроса:
   - `sortBy` (enum: "userRating", "criticsRating")
   - `sortOrder` (enum: "asc", "desc")
2. Добавить поле `criticsRating` в схему ответа
3. Реализовать логику сортировки с учетом контента без рейтинга

### Films Server API (`/films/list`)

**Текущие возможности:**
- ✅ Возвращает список всех фильмов
- ✅ Содержит пользовательский рейтинг (`rating`)

**Недостающие возможности:**
- ❌ Рейтинг кинокритиков в ответе (`criticsRating`)

**Необходимые изменения:**
1. Добавить поле `criticsRating` в схему ответа

### Series Server API (`/series/list`)

**Текущие возможности:**
- ✅ Возвращает список всех сериалов
- ✅ Содержит пользовательский рейтинг (`rating`)

**Недостающие возможности:**
- ❌ Рейтинг кинокритиков в ответе (`criticsRating`)

**Необходимые изменения:**
1. Добавить поле `criticsRating` в схему ответа

## Детальный анализ эндпоинтов

### 1. Web Server API - `/content/list`

**Текущая схема запроса:**
```yaml
parameters:
  - name: type
    in: query
    description: фильтр по типу контента (film, serie)
    required: false
    schema:
      type: string
```

**Текущая схема ответа:**
```yaml
properties:
  rating:
    type: integer
    description: рейтинг пользователей
    example: 6.5
```

**Требуемые изменения:**
```yaml
parameters:
  - name: type
    in: query
    description: фильтр по типу контента (film, serie)
    required: false
    schema:
      type: string
  - name: sortBy
    in: query
    description: поле для сортировки
    required: false
    schema:
      type: string
      enum: ["userRating", "criticsRating"]
  - name: sortOrder
    in: query
    description: порядок сортировки
    required: false
    schema:
      type: string
      enum: ["asc", "desc"]
      default: "desc"

properties:
  rating:
    type: integer
    description: рейтинг пользователей
    example: 6.5
  criticsRating:
    type: number
    description: рейтинг кинокритиков
    example: 8.2
    nullable: true
```

### 2. Films Server API - `/films/list`

**Текущая схема ответа:**
```yaml
properties:
  rating:
    type: integer
    description: рейтинг пользователей
    example: 6.5
```

**Требуемые изменения:**
```yaml
properties:
  rating:
    type: integer
    description: рейтинг пользователей
    example: 6.5
  criticsRating:
    type: number
    description: рейтинг кинокритиков
    example: 8.2
    nullable: true
```

### 3. Series Server API - `/series/list`

**Текущая схема ответа:**
```yaml
properties:
  rating:
    type: integer
    description: рейтинг пользователей
    example: 6.5
```

**Требуемые изменения:**
```yaml
properties:
  rating:
    type: integer
    description: рейтинг пользователей
    example: 6.5
  criticsRating:
    type: number
    description: рейтинг кинокритиков
    example: 8.2
    nullable: true
```

## Логика сортировки

### Алгоритм сортировки по рейтингу кинокритиков:
1. Получить все фильмы и сериалы
2. Применить фильтрацию по типу контента (если указана)
3. Разделить контент на две группы:
   - С рейтингом кинокритиков
   - Без рейтинга кинокритиков (criticsRating = null)
4. Отсортировать первую группу по рейтингу кинокритиков
5. Добавить вторую группу в конец списка
6. Вернуть объединенный список

### Примеры запросов:
- `GET /content/list?sortBy=criticsRating&sortOrder=desc` - по убыванию рейтинга кинокритиков
- `GET /content/list?sortBy=criticsRating&sortOrder=asc` - по возрастанию рейтинга кинокритиков
- `GET /content/list?sortBy=userRating&sortOrder=desc` - по убыванию пользовательского рейтинга
- `GET /content/list?type=film&sortBy=criticsRating&sortOrder=desc` - фильмы по убыванию рейтинга кинокритиков

## Выводы

### Что нужно изменить:

1. **Web Server API** - требует наибольших изменений:
   - Добавить параметры сортировки
   - Добавить поле criticsRating в ответ
   - Реализовать логику сортировки

2. **Films Server API** - минимальные изменения:
   - Добавить поле criticsRating в ответ

3. **Series Server API** - минимальные изменения:
   - Добавить поле criticsRating в ответ

### Приоритет изменений:
1. **Высокий**: Web Server API (основная логика)
2. **Средний**: Films Server API и Series Server API (данные)

### Обратная совместимость:
Все изменения обратно совместимы - существующие клиенты продолжат работать без изменений.
