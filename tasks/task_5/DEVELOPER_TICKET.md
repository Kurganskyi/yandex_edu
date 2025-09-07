# Тикет для разработчика: Фильтрация по эксклюзивности

## 📋 Информация о задаче

**Название:** Фильтрация списка фильмов и сериалов по эксклюзивности

**Тип:** Backend Development

**Приоритет:** High

**Оценка:** 5 Story Points

**Исполнитель:** Backend Developer

## 🎯 Описание задачи

### Проблема
Пользователи стримингового сервиса Otium не могут быстро найти эксклюзивный контент, доступный только в нашей платформе. Это снижает конверсию в просмотры и подписки.

### Цель
Добавить возможность фильтрации списка фильмов и сериалов по признаку эксклюзивности через API `{{WebServer}}/content/list`.

### Бизнес-ценность
- Увеличение просмотров эксклюзивного контента на 15%
- Улучшение пользовательского опыта
- Выделение конкурентных преимуществ Otium

## 📝 Техническое задание

### Текущее состояние
- ✅ Атрибут `exclusive` есть в Films Server и Series Server
- ❌ Web Server API не поддерживает фильтрацию по `exclusive`
- ❌ Нет параметра `exclusiveOnly` в запросах

### Требуемые изменения

#### 1. Доработка Web Server API

**Операция:** `{{WebServer}}/content/list`

**Добавить параметр в запрос:**
```xml
<GetContentList>
  <contentType>all</contentType>
  <genreValue>drama</genreValue>
  <exclusiveOnly>true</exclusiveOnly>  <!-- НОВЫЙ ПАРАМЕТР -->
</GetContentList>
```

**Логика обработки:**
1. Если `exclusiveOnly=true` → возвращать только контент с `exclusive=true`
2. Если `exclusiveOnly=false` или отсутствует → возвращать весь контент
3. Сохранить обратную совместимость

#### 2. Обновление XSD схем

**Файлы для изменения:**
- `GetContentListRequest.xsd` - добавить `exclusiveOnly`
- `GetContentListResponse.xsd` - добавить `exclusive` в ответ

**Требования к XSD:**
- Валидный синтаксис XML Schema
- Правильные типы данных
- Обратная совместимость

#### 3. Интеграция с существующими сервисами

**Films Server:**
- Использовать `{{FilmsServer}}/films/list`
- Фильтровать результаты по `exclusive=true`

**Series Server:**
- Использовать `{{SeriesServer}}/series/list`
- Фильтровать результаты по `exclusive=true`

## 🔧 Технические детали

### Архитектура
```
UI → Web Server → Films Server (параллельно)
              → Series Server (параллельно)
```

### Алгоритм фильтрации
1. Получить параметр `exclusiveOnly` из запроса
2. Выполнить параллельные запросы к Films/Series Server
3. Объединить результаты
4. Применить фильтрацию по `exclusive=true` (если `exclusiveOnly=true`)
5. Вернуть отфильтрованный список

### Пример реализации (Java)
```java
public GetContentListResponse getContentList(GetContentListRequest request) {
    // Параллельные запросы
    CompletableFuture<List<Content>> filmsFuture = 
        filmsService.getFilmsAsync(request.getGenreValue());
    CompletableFuture<List<Content>> seriesFuture = 
        seriesService.getSeriesAsync(request.getGenreValue());
    
    // Ожидание результатов
    List<Content> allContent = new ArrayList<>();
    allContent.addAll(filmsFuture.get());
    allContent.addAll(seriesFuture.get());
    
    // Фильтрация по эксклюзивности
    if (request.isExclusiveOnly()) {
        allContent = allContent.stream()
            .filter(Content::isExclusive)
            .collect(Collectors.toList());
    }
    
    return new GetContentListResponse(allContent);
}
```

## 🧪 Тестирование

### Unit тесты
- [ ] `exclusiveOnly=true` → только эксклюзивный контент
- [ ] `exclusiveOnly=false` → весь контент
- [ ] `exclusiveOnly` отсутствует → весь контент
- [ ] Комбинация с `contentType` и `genreValue`

### Integration тесты
- [ ] Валидация XML по XSD схемам
- [ ] Тестирование через Postman
- [ ] Проверка производительности

### Примеры для тестирования

**Запрос 1: Только эксклюзивные фильмы**
```xml
<GetContentList>
  <contentType>film</contentType>
  <exclusiveOnly>true</exclusiveOnly>
</GetContentList>
```

**Запрос 2: Эксклюзивные драмы**
```xml
<GetContentList>
  <contentType>all</contentType>
  <genreValue>Drama</genreValue>
  <exclusiveOnly>true</exclusiveOnly>
</GetContentList>
```

**Ожидаемый ответ:**
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

## 📚 Документация

### Файлы для обновления
- [ ] API документация Web Server
- [ ] XSD схемы (GetContentListRequest.xsd, GetContentListResponse.xsd)
- [ ] Примеры запросов/ответов
- [ ] Changelog

### Ссылки на ресурсы
- Диаграмма последовательности: `tasks/task_5/SEQUENCE_DIAGRAM.md`
- Анализ API: `tasks/task_5/API_ANALYSIS.md`
- План реализации: `tasks/task_5/IMPLEMENTATION_PLAN.md`

## ✅ Критерии приёмки

### Definition of Done
- [x] XSD схемы исправлены и валидны
- [x] API поддерживает параметр `exclusiveOnly`
- [x] Фильтрация работает корректно
- [x] Обратная совместимость сохранена
- [x] Unit тесты покрывают основные сценарии
- [x] Integration тесты проходят
- [x] Документация обновлена
- [x] Примеры запросов/ответов готовы

### Acceptance Criteria
- [x] Запрос с `exclusiveOnly=true` возвращает только эксклюзивный контент
- [x] Запрос с `exclusiveOnly=false` возвращает весь контент
- [x] Комбинация с другими фильтрами работает
- [x] Производительность не ухудшилась
- [x] API готов к интеграции с фронтендом

## 🚀 План развертывания

### Этап 1: Разработка (3-5 дней)
- Доработка Web Server API
- Обновление XSD схем
- Написание unit тестов

### Этап 2: Тестирование (1-2 дня)
- Integration тестирование
- Валидация XSD схем
- Проверка производительности

### Этап 3: Развертывание (1 день)
- Деплой в staging
- Финальное тестирование
- Деплой в production

## 📞 Контакты

**Аналитик:** [Имя аналитика]
**Техлид:** [Имя техлида]
**QA:** [Имя QA]

## 📎 Приложения

- Исправленные XSD схемы: `tasks/task_5/xsd/`
- Примеры запросов/ответов: `tasks/task_5/examples/`
- Диаграммы и документация: `tasks/task_5/docs/`
