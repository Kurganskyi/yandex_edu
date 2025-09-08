# Диаграмма текущего состояния API

## Текущее состояние API

```mermaid
graph TD
    A[Пользователь] --> B[Web Server API<br/>/content/list]
    B --> C[Films Server API<br/>/films/list]
    B --> D[Series Server API<br/>/series/list]
    
    C --> E[Фильмы<br/>✅ userRating<br/>❌ criticsRating]
    D --> F[Сериалы<br/>✅ userRating<br/>❌ criticsRating]
    
    E --> G[Объединенный список<br/>❌ Сортировка<br/>❌ criticsRating]
    F --> G
    
    G --> H[Ответ пользователю<br/>❌ Нет сортировки по рейтингу]
    
    style E fill:#ffcccc
    style F fill:#ffcccc
    style G fill:#ffcccc
    style H fill:#ffcccc
```

## Необходимые изменения

```mermaid
graph TD
    A[Пользователь] --> B[Web Server API<br/>/content/list<br/>+ sortBy, sortOrder]
    B --> C[Films Server API<br/>/films/list<br/>+ criticsRating]
    B --> D[Series Server API<br/>/series/list<br/>+ criticsRating]
    
    C --> E[Фильмы<br/>✅ userRating<br/>✅ criticsRating]
    D --> F[Сериалы<br/>✅ userRating<br/>✅ criticsRating]
    
    E --> G[Объединенный список<br/>✅ Сортировка<br/>✅ criticsRating<br/>✅ Логика для null]
    F --> G
    
    G --> H[Ответ пользователю<br/>✅ Отсортированный список]
    
    style E fill:#ccffcc
    style F fill:#ccffcc
    style G fill:#ccffcc
    style H fill:#ccffcc
```

## Сравнение параметров запроса

### Текущий запрос
```
GET /content/list?type=film
```

### Новый запрос
```
GET /content/list?type=film&sortBy=criticsRating&sortOrder=desc
```

## Сравнение схемы ответа

### Текущая схема
```json
{
  "id": 104,
  "type": "film",
  "title": "Ребус Атлантиды",
  "rating": 6.5,
  // ... другие поля
}
```

### Новая схема
```json
{
  "id": 104,
  "type": "film", 
  "title": "Ребус Атлантиды",
  "rating": 6.5,
  "criticsRating": 8.2,
  // ... другие поля
}
```

## Логика сортировки

```mermaid
flowchart TD
    A[Получить все фильмы и сериалы] --> B[Применить фильтр по типу]
    B --> C[Разделить на группы]
    C --> D[С рейтингом кинокритиков]
    C --> E[Без рейтинга кинокритиков]
    D --> F[Сортировать по criticsRating]
    E --> G[Добавить в конец списка]
    F --> H[Объединить списки]
    G --> H
    H --> I[Вернуть результат]
```

## Приоритет изменений

1. **Web Server API** - Критично
   - Добавить параметры сортировки
   - Реализовать логику сортировки
   - Добавить criticsRating в ответ

2. **Films Server API** - Важно
   - Добавить criticsRating в ответ

3. **Series Server API** - Важно
   - Добавить criticsRating в ответ
