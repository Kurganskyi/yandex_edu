# Улучшенная диаграмма API для сортировки по рейтингу кинокритиков

## 🎯 Проблема
Текущий API не поддерживает сортировку по рейтингу кинокритиков (`criticsRating`), что ограничивает возможности пользователей в поиске качественного контента.

## 📊 Текущее состояние API

```mermaid
graph TD
    A[👤 Пользователь] --> B[🌐 Web Server API<br/>/content/list]
    B --> C[🎬 Films Server API<br/>/films/list]
    B --> D[📺 Series Server API<br/>/series/list]
    
    C --> E[🎬 Фильмы<br/>✅ userRating: 6.5<br/>❌ criticsRating: отсутствует]
    D --> F[📺 Сериалы<br/>✅ userRating: 7.2<br/>❌ criticsRating: отсутствует]
    
    E --> G[📋 Объединенный список<br/>❌ Сортировка по рейтингу<br/>❌ criticsRating в ответе]
    F --> G
    
    G --> H[📤 Ответ пользователю<br/>❌ Нет сортировки по рейтингу]
    
    style E fill:#ffcccc,stroke:#ff0000,stroke-width:2px
    style F fill:#ffcccc,stroke:#ff0000,stroke-width:2px
    style G fill:#ffcccc,stroke:#ff0000,stroke-width:2px
    style H fill:#ffcccc,stroke:#ff0000,stroke-width:2px
```

## 🚀 Целевое состояние API

```mermaid
graph TD
    A[👤 Пользователь] --> B[🌐 Web Server API<br/>/content/list<br/>+ sortBy, sortOrder]
    B --> C[🎬 Films Server API<br/>/films/list<br/>+ criticsRating]
    B --> D[📺 Series Server API<br/>/series/list<br/>+ criticsRating]
    
    C --> E[🎬 Фильмы<br/>✅ userRating: 6.5<br/>✅ criticsRating: 8.2]
    D --> F[📺 Сериалы<br/>✅ userRating: 7.2<br/>✅ criticsRating: 9.1]
    
    E --> G[📋 Объединенный список<br/>✅ Сортировка по criticsRating<br/>✅ Логика для null значений<br/>✅ Приоритет: с рейтингом → без рейтинга]
    F --> G
    
    G --> H[📤 Ответ пользователю<br/>✅ Отсортированный список<br/>✅ criticsRating в ответе]
    
    style E fill:#ccffcc,stroke:#00aa00,stroke-width:2px
    style F fill:#ccffcc,stroke:#00aa00,stroke-width:2px
    style G fill:#ccffcc,stroke:#00aa00,stroke-width:2px
    style H fill:#ccffcc,stroke:#00aa00,stroke-width:2px
```

## 🔄 Логика сортировки

```mermaid
flowchart TD
    A[📥 Получить все фильмы и сериалы] --> B[🔍 Применить фильтр по типу]
    B --> C[📊 Разделить на группы]
    C --> D[✅ С рейтингом кинокритиков]
    C --> E[❌ Без рейтинга кинокритиков]
    D --> F[📈 Сортировать по criticsRating DESC]
    E --> G[📝 Добавить в конец списка]
    F --> H[🔗 Объединить списки]
    G --> H
    H --> I[📤 Вернуть отсортированный результат]
    
    style A fill:#e1f5fe
    style F fill:#c8e6c9
    style G fill:#fff3e0
    style I fill:#f3e5f5
```

## 📋 Сравнение API

### Текущий запрос
```http
GET /content/list?type=film
```

### Новый запрос
```http
GET /content/list?type=film&sortBy=criticsRating&sortOrder=desc
```

## 📊 Сравнение схемы ответа

### Текущая схема
```json
{
  "id": 104,
  "type": "film",
  "title": "Ребус Атлантиды",
  "rating": 6.5,
  "description": "Описание фильма...",
  "year": 2023
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
  "description": "Описание фильма...",
  "year": 2023
}
```

## 🎯 Приоритет изменений

```mermaid
gantt
    title План реализации изменений API
    dateFormat  YYYY-MM-DD
    section Критично
    Web Server API изменения    :crit, web, 2024-01-01, 5d
    section Важно
    Films Server API изменения  :films, after web, 3d
    Series Server API изменения :series, after web, 3d
    section Тестирование
    Интеграционные тесты        :test, after series, 2d
    Пользовательские тесты      :uat, after test, 2d
```

## 📈 Ожидаемые результаты

- **Улучшение UX**: Пользователи смогут сортировать контент по рейтингу кинокритиков
- **Повышение качества**: Более качественный контент будет показываться первым
- **Гибкость**: Поддержка сортировки по разным критериям
- **Обратная совместимость**: Существующие запросы продолжат работать

## 🔧 Технические детали

### Параметры сортировки
- `sortBy`: `criticsRating`, `userRating`, `title`, `year`
- `sortOrder`: `asc`, `desc`

### Логика обработки null значений
1. Элементы с `criticsRating` сортируются по убыванию
2. Элементы без `criticsRating` добавляются в конец списка
3. Внутри группы без рейтинга сохраняется исходный порядок

---

**Статус**: Готово к реализации  
**Приоритет**: Высокий  
**Сложность**: Средняя
