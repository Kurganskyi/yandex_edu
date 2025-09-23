# Диаграмма последовательности: Сортировка по рейтингу кинокритиков

## 🎯 Сценарий
Пользователь запрашивает список фильмов с сортировкой по рейтингу кинокритиков в убывающем порядке.

## 📊 Диаграмма последовательности

```mermaid
sequenceDiagram
    participant U as 👤 Пользователь
    participant W as 🌐 Web Server API
    participant F as 🎬 Films Server API
    participant S as 📺 Series Server API
    participant DB as 🗄️ База данных

    Note over U,DB: Запрос списка с сортировкой по criticsRating

    U->>+W: GET /content/list?type=film&sortBy=criticsRating&sortOrder=desc
    
    Note over W: Валидация параметров запроса
    
    W->>+F: GET /films/list?includeCriticsRating=true
    F->>+DB: SELECT * FROM films WHERE type='film'
    DB-->>-F: Список фильмов с criticsRating
    F-->>-W: Фильмы с рейтингом кинокритиков
    
    W->>+S: GET /series/list?includeCriticsRating=true
    S->>+DB: SELECT * FROM series WHERE type='series'
    DB-->>-S: Список сериалов с criticsRating
    S-->>-W: Сериалы с рейтингом кинокритиков
    
    Note over W: Объединение и сортировка данных
    
    W->>W: Объединить фильмы и сериалы
    W->>W: Разделить на группы:<br/>- С criticsRating<br/>- Без criticsRating
    W->>W: Сортировать группу с criticsRating по убыванию
    W->>W: Добавить группу без criticsRating в конец
    
    Note over W: Формирование ответа
    
    W-->>-U: Отсортированный список контента<br/>с criticsRating

    Note over U,DB: Успешное выполнение запроса
```

## 🔄 Детальная логика сортировки

```mermaid
sequenceDiagram
    participant W as 🌐 Web Server
    participant L as 🧠 Логика сортировки
    participant R as 📋 Результат

    Note over W,R: Внутренняя обработка данных

    W->>+L: Получить данные от Films и Series API
    
    L->>L: Объединить все элементы в один список
    
    L->>L: Разделить на две группы:
    Note right of L: Группа 1: элементы с criticsRating<br/>Группа 2: элементы без criticsRating
    
    L->>L: Сортировать Группу 1 по criticsRating DESC
    Note right of L: Используется алгоритм быстрой сортировки
    
    L->>L: Добавить Группу 2 в конец списка
    Note right of L: Сохраняется исходный порядок
    
    L->>L: Применить фильтр по типу (film/series)
    
    L-->>-W: Отсортированный список
    
    W->>+R: Формировать JSON ответ
    R-->>-W: Готовый ответ для пользователя
```

## 📋 Примеры запросов и ответов

### Запрос
```http
GET /content/list?type=film&sortBy=criticsRating&sortOrder=desc
```

### Ответ
```json
{
  "content": [
    {
      "id": 104,
      "type": "film",
      "title": "Ребус Атлантиды",
      "rating": 6.5,
      "criticsRating": 8.2,
      "description": "Описание фильма...",
      "year": 2023
    },
    {
      "id": 105,
      "type": "film", 
      "title": "Другой фильм",
      "rating": 7.1,
      "criticsRating": 7.8,
      "description": "Описание...",
      "year": 2023
    },
    {
      "id": 106,
      "type": "film",
      "title": "Фильм без рейтинга",
      "rating": 5.5,
      "criticsRating": null,
      "description": "Описание...",
      "year": 2022
    }
  ],
  "total": 3,
  "sortedBy": "criticsRating",
  "sortOrder": "desc"
}
```

## ⚡ Обработка ошибок

```mermaid
sequenceDiagram
    participant U as 👤 Пользователь
    participant W as 🌐 Web Server API
    participant F as 🎬 Films Server API
    participant S as 📺 Series Server API

    Note over U,S: Сценарий с ошибкой

    U->>+W: GET /content/list?type=film&sortBy=criticsRating&sortOrder=desc
    
    W->>+F: GET /films/list?includeCriticsRating=true
    F-->>-W: ❌ Ошибка 500: Сервис недоступен
    
    W->>+S: GET /series/list?includeCriticsRating=true
    S-->>-W: ✅ Сериалы получены успешно
    
    Note over W: Обработка частичной ошибки
    
    W->>W: Использовать только доступные данные
    W->>W: Применить сортировку к доступным данным
    W->>W: Добавить информацию об ошибке в ответ
    
    W-->>-U: Частичный результат + предупреждение об ошибке
```

## 🎯 Ключевые моменты

### 1. **Параллельные запросы**
- Films и Series API вызываются одновременно
- Улучшает производительность системы

### 2. **Обработка null значений**
- Элементы с `criticsRating` сортируются по убыванию
- Элементы без `criticsRating` добавляются в конец

### 3. **Обработка ошибок**
- Частичные ошибки не блокируют весь запрос
- Пользователь получает доступные данные

### 4. **Производительность**
- Сортировка происходит в памяти Web Server
- Минимальная нагрузка на базу данных

## 📊 Временные характеристики

| Этап | Время выполнения | Описание |
|------|------------------|----------|
| Валидация запроса | ~1ms | Проверка параметров |
| Запрос к Films API | ~50ms | Получение данных о фильмах |
| Запрос к Series API | ~50ms | Получение данных о сериалах |
| Сортировка данных | ~5ms | Алгоритм быстрой сортировки |
| Формирование ответа | ~2ms | Создание JSON |
| **Общее время** | **~108ms** | **Время ответа пользователю** |

---

**Статус**: Готово к реализации  
**Сложность**: Средняя  
**Приоритет**: Высокий