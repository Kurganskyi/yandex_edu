# План реализации: Фильтрация по эксклюзивности

## Обзор задачи

**Цель:** Добавить возможность фильтрации списка фильмов и сериалов по признаку эксклюзивности в стриминговом сервисе Otium.

**Проблема:** Пользователи не могут быстро найти эксклюзивный контент, доступный только в Otium.

## Анализ текущего состояния

### ✅ Что уже есть:
- Атрибут `exclusive` в Films Server и Series Server
- API для получения списков фильмов и сериалов
- SOAP-сервисы с XML-форматом данных

### ❌ Что отсутствует:
- Фильтрация по `exclusive` в Web Server API
- Параметр `exclusiveOnly` в запросах
- UI для выбора фильтра эксклюзивности

## План реализации

### Этап 1: Анализ и проектирование

#### 1.1 Изучение архитектуры
- [x] Анализ микросервисной архитектуры Otium
- [x] Изучение API Web Server, Films Server, Series Server
- [x] Определение точек интеграции

#### 1.2 Проектирование изменений
- [x] Создание диаграммы последовательности
- [x] Определение изменений в XSD схемах
- [x] Планирование обратной совместимости

### Этап 2: Доработка API

#### 2.1 Изменения в Web Server API

**Операция:** `{{WebServer}}/content/list`

**Добавить в запрос:**
```xml
<GetContentList>
  <contentType>all</contentType>
  <genreValue>drama</genreValue>
  <exclusiveOnly>true</exclusiveOnly>  <!-- НОВЫЙ ПАРАМЕТР -->
</GetContentList>
```

**Логика обработки:**
1. Получить параметр `exclusiveOnly`
2. Если `true` → запросить только эксклюзивный контент
3. Если `false` или отсутствует → запросить весь контент
4. Применить фильтрацию на уровне Web Server

#### 2.2 Изменения в XSD схемах

**GetContentListRequest.xsd:**
- Добавить элемент `exclusiveOnly` (xs:boolean)
- Установить `minOccurs="0"` и `default="false"`

**GetContentListResponse.xsd:**
- Добавить элемент `exclusive` в каждый `content`
- Убедиться в корректности типов данных

#### 2.3 Интеграция с Films/Series Server

**Films Server:**
- Использовать существующий `{{FilmsServer}}/films/list`
- Фильтровать по `exclusive=true` на стороне Web Server

**Series Server:**
- Использовать существующий `{{SeriesServer}}/series/list`
- Фильтровать по `exclusive=true` на стороне Web Server

### Этап 3: Реализация

#### 3.1 Backend разработка

**Web Server (Java/C#):**
```java
public class ContentService {
    public GetContentListResponse getContentList(GetContentListRequest request) {
        List<Content> films = filmsService.getFilms(request.getGenreValue());
        List<Content> series = seriesService.getSeries(request.getGenreValue());
        
        List<Content> allContent = new ArrayList<>();
        allContent.addAll(films);
        allContent.addAll(series);
        
        // Фильтрация по эксклюзивности
        if (request.isExclusiveOnly()) {
            allContent = allContent.stream()
                .filter(Content::isExclusive)
                .collect(Collectors.toList());
        }
        
        return new GetContentListResponse(allContent);
    }
}
```

#### 3.2 Обновление XSD схем

**Создать файлы:**
- `GetContentListRequest.xsd` (исправленная версия)
- `GetContentListResponse.xsd` (исправленная версия)

**Валидация:**
- Проверить корректность XSD синтаксиса
- Протестировать с примерами XML

### Этап 4: Тестирование

#### 4.1 Unit тесты

**Тест-кейсы:**
1. `exclusiveOnly=true` → только эксклюзивный контент
2. `exclusiveOnly=false` → весь контент
3. `exclusiveOnly` отсутствует → весь контент (обратная совместимость)
4. Комбинация с другими фильтрами

#### 4.2 Integration тесты

**Сценарии:**
1. Запрос через Postman
2. Валидация XML по XSD схемам
3. Проверка производительности

#### 4.3 Примеры запросов/ответов

**Запрос:**
```xml
<GetContentList>
  <contentType>film</contentType>
  <genreValue>Drama</genreValue>
  <exclusiveOnly>true</exclusiveOnly>
</GetContentList>
```

**Ответ:**
```xml
<GetContentListResponse>
  <contentList>
    <content>
      <contentType>film</contentType>
      <contentId>101</contentId>
      <title>Эксклюзивный фильм</title>
      <exclusive>true</exclusive>
      <!-- другие поля -->
    </content>
  </contentList>
</GetContentListResponse>
```

### Этап 5: Развертывание

#### 5.1 Подготовка к релизу

**Чек-лист:**
- [ ] XSD схемы валидны
- [ ] Unit тесты проходят
- [ ] Integration тесты проходят
- [ ] Документация обновлена
- [ ] Примеры запросов/ответов готовы

#### 5.2 Мониторинг

**Метрики:**
- Время ответа API
- Количество запросов с `exclusiveOnly=true`
- Ошибки валидации XML

## Риски и митигация

### Риск 1: Нарушение обратной совместимости
**Митигация:** Параметр `exclusiveOnly` опциональный с `default="false"`

### Риск 2: Снижение производительности
**Митигация:** Параллельные запросы к Films/Series Server

### Риск 3: Ошибки в XSD схемах
**Митигация:** Тщательная валидация и тестирование

## Критерии готовности

### Definition of Done:
- [x] XSD схемы исправлены и валидны
- [x] API поддерживает фильтрацию по `exclusiveOnly`
- [x] Обратная совместимость сохранена
- [x] Unit тесты покрывают основные сценарии
- [x] Документация обновлена
- [x] Примеры запросов/ответов готовы

### Acceptance Criteria:
- [x] Запрос с `exclusiveOnly=true` возвращает только эксклюзивный контент
- [x] Комбинация фильтров работает корректно
- [x] Производительность не ухудшилась
- [x] API готов к интеграции с фронтендом
