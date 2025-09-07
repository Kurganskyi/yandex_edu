# Анализ API сервисов Otium

## Обзор API

### Стиль API
- **SOAP** - все три сервиса используют протокол SOAP
- **XML** - формат представления данных
- **WSDL** - описание веб-сервисов

### Формат данных
```xml
<content type="film" id="101">
  <title>Название фильма</title>
  <exclusive>true</exclusive>
  <!-- другие поля -->
</content>
```

## Web Server API

### Операции

#### 1. Получение списка контента
- **Endpoint:** `{{WebServer}}/content/list`
- **Описание:** Возвращает список всех фильмов и сериалов
- **Проблема:** Нет фильтрации по эксклюзивности

#### 2. Детальная информация
- **Endpoint:** `{{WebServer}}/content/details`
- **Описание:** Подробная информация о конкретном фильме/сериале

### Текущая структура запроса/ответа

**Запрос:**
```xml
<GetContentList>
  <contentType>all</contentType>
  <genreValue>drama</genreValue>
</GetContentList>
```

**Ответ:**
```xml
<GetContentListResponse>
  <contentList>
    <content>
      <contentType>film</contentType>
      <contentId>101</contentId>
      <title>Название</title>
      <exclusive>true</exclusive>
      <!-- другие поля -->
    </content>
  </contentList>
</GetContentListResponse>
```

## Films Server API

### Операции

#### Список фильмов
- **Endpoint:** `{{FilmsServer}}/films/list`
- **Описание:** Возвращает список всех фильмов
- **Атрибут exclusive:** ✅ Присутствует

### Структура ответа
```xml
<films>
  <film id="101" exclusive="true">
    <title>Название фильма</title>
    <genre>Drama</genre>
    <!-- другие поля -->
  </film>
</films>
```

## Series Server API

### Операции

#### Список сериалов
- **Endpoint:** `{{SeriesServer}}/series/list`
- **Описание:** Возвращает список всех сериалов
- **Атрибут exclusive:** ✅ Присутствует

### Структура ответа
```xml
<series>
  <serie id="201" exclusive="true">
    <title>Название сериала</title>
    <genre>Comedy</genre>
    <!-- другие поля -->
  </serie>
</series>
```

## Анализ требований

### Текущее состояние
- ✅ Атрибут `exclusive` есть в Films Server и Series Server
- ❌ Web Server API не поддерживает фильтрацию по `exclusive`
- ❌ Нет возможности получить только эксклюзивный контент

### Необходимые изменения

#### 1. Доработка Web Server API
**Операция:** `{{WebServer}}/content/list`

**Добавить в запрос:**
```xml
<GetContentList>
  <contentType>all</contentType>
  <genreValue>drama</genreValue>
  <exclusiveOnly>true</exclusiveOnly>  <!-- НОВОЕ ПОЛЕ -->
</GetContentList>
```

#### 2. Логика фильтрации
1. Web Server получает запрос с `exclusiveOnly=true`
2. Обращается к Films Server и Series Server
3. Фильтрует результаты по `exclusive=true`
4. Возвращает отфильтрованный список

#### 3. Обратная совместимость
- Если `exclusiveOnly` не указан или `false` → возвращать все записи
- Если `exclusiveOnly=true` → возвращать только эксклюзивные

## Сравнение с существующими API

| Сервис | Стиль | Формат | Exclusive | Фильтрация |
|--------|-------|--------|-----------|------------|
| Web Server | SOAP | XML | ❌ | ❌ |
| Films Server | SOAP | XML | ✅ | ❌ |
| Series Server | SOAP | XML | ✅ | ❌ |

## Рекомендации по реализации

### 1. Изменения в XSD схемах
- Добавить `exclusiveOnly` в `GetContentListRequest.xsd`
- Добавить `exclusive` в `GetContentListResponse.xsd`

### 2. Изменения в бизнес-логике
- Реализовать фильтрацию на уровне Web Server
- Сохранить обратную совместимость

### 3. Тестирование
- Тесты с `exclusiveOnly=true`
- Тесты с `exclusiveOnly=false`
- Тесты комбинации фильтров
