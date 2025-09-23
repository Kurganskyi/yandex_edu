# Детальная диаграмма обработки данных и применения фильтров

## 🎯 Сценарий
Пользователь запрашивает список контента с фильтрацией по типу и сортировкой по рейтингу кинокритиков.

## 📊 Основная диаграмма последовательности

```mermaid
sequenceDiagram
    participant U as 👤 Пользователь
    participant W as 🌐 Web Server API
    participant F as 🎬 Films Server API
    participant S as 📺 Series Server API
    participant DB as 🗄️ База данных

    Note over U,DB: Запрос с фильтрацией и сортировкой

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
    
    Note over W: 🔄 ОБРАБОТКА ДАННЫХ И ПРИМЕНЕНИЕ ФИЛЬТРОВ
    
    W->>W: Объединить данные от Films и Series API
    W->>W: Применить фильтр по типу контента
    W->>W: Разделить на группы по наличию criticsRating
    W->>W: Сортировать группу с criticsRating
    W->>W: Объединить отсортированные группы
    
    Note over W: Формирование ответа
    
    W-->>-U: Отсортированный список контента
```

## 🔄 Детальная диаграмма обработки данных

```mermaid
sequenceDiagram
    participant W as 🌐 Web Server
    participant DM as 📊 Data Merger
    participant FM as 🔍 Filter Manager
    participant SM as 📈 Sort Manager
    participant R as 📋 Result Builder

    Note over W,R: Детальная обработка данных

    W->>+DM: Получить данные от Films API
    DM-->>-W: Список фильмов: [film1, film2, film3...]
    
    W->>+DM: Получить данные от Series API
    DM-->>-W: Список сериалов: [series1, series2, series3...]
    
    W->>+DM: Объединить все данные
    Note right of DM: Создать единый массив:<br/>[film1, film2, series1, series2...]
    DM-->>-W: Объединенный список: [item1, item2, item3...]
    
    W->>+FM: Применить фильтр по типу
    Note right of FM: Фильтр: type='film'<br/>Оставить только фильмы
    FM->>FM: Проверить каждый элемент
    FM->>FM: if (item.type === 'film') keep
    FM-->>-W: Отфильтрованный список: [film1, film2...]
    
    W->>+SM: Разделить на группы по criticsRating
    Note right of SM: Группа 1: с criticsRating<br/>Группа 2: без criticsRating
    SM->>SM: Группа 1: [film1, film2] (есть criticsRating)
    SM->>SM: Группа 2: [film3] (нет criticsRating)
    SM-->>-W: Две группы данных
    
    W->>+SM: Сортировать группу с criticsRating
    Note right of SM: Сортировка по убыванию:<br/>criticsRating DESC
    SM->>SM: Сортировать Группу 1: [film2, film1]
    SM-->>-W: Отсортированная группа 1
    
    W->>+SM: Объединить группы
    Note right of SM: Группа 1 + Группа 2<br/>[film2, film1, film3]
    SM-->>-W: Финальный отсортированный список
    
    W->>+R: Формировать JSON ответ
    R->>R: Добавить метаданные (total, sortedBy, sortOrder)
    R-->>-W: Готовый ответ для пользователя
```

## 🧠 Логика фильтрации по типу

```mermaid
flowchart TD
    A[📥 Получить объединенный список] --> B[🔍 Проверить параметр type]
    
    B --> C{type === 'film'?}
    C -->|Да| D[🎬 Оставить только фильмы]
    C -->|Нет| E{type === 'series'?}
    
    E -->|Да| F[📺 Оставить только сериалы]
    E -->|Нет| G[📋 Оставить все типы]
    
    D --> H[📊 Применить сортировку]
    F --> H
    G --> H
    
    H --> I[📤 Вернуть результат]
    
    style A fill:#e3f2fd
    style D fill:#c8e6c9
    style F fill:#c8e6c9
    style G fill:#fff3e0
    style I fill:#f3e5f5
```

## 📈 Логика сортировки по criticsRating

```mermaid
flowchart TD
    A[📥 Получить отфильтрованный список] --> B[🔍 Проверить наличие criticsRating]
    
    B --> C[📊 Разделить на две группы]
    C --> D[✅ Группа 1: С criticsRating]
    C --> E[❌ Группа 2: Без criticsRating]
    
    D --> F[📈 Сортировать по criticsRating DESC]
    F --> G[🔢 Применить алгоритм быстрой сортировки]
    G --> H[📋 Отсортированная группа 1]
    
    E --> I[📝 Сохранить исходный порядок]
    I --> J[📋 Группа 2 без изменений]
    
    H --> K[🔗 Объединить группы]
    J --> K
    K --> L[📤 Финальный результат]
    
    style A fill:#e3f2fd
    style D fill:#c8e6c9
    style E fill:#ffecb3
    style F fill:#e1f5fe
    style L fill:#f3e5f5
```

## 💻 Псевдокод обработки данных

```javascript
function processContentData(filmsData, seriesData, filters) {
    // 1. Объединение данных
    let allContent = [...filmsData, ...seriesData];
    
    // 2. Применение фильтра по типу
    if (filters.type) {
        allContent = allContent.filter(item => item.type === filters.type);
    }
    
    // 3. Разделение на группы по наличию criticsRating
    let withCriticsRating = [];
    let withoutCriticsRating = [];
    
    allContent.forEach(item => {
        if (item.criticsRating !== null && item.criticsRating !== undefined) {
            withCriticsRating.push(item);
        } else {
            withoutCriticsRating.push(item);
        }
    });
    
    // 4. Сортировка группы с criticsRating
    if (filters.sortBy === 'criticsRating') {
        withCriticsRating.sort((a, b) => {
            if (filters.sortOrder === 'desc') {
                return b.criticsRating - a.criticsRating;
            } else {
                return a.criticsRating - b.criticsRating;
            }
        });
    }
    
    // 5. Объединение групп
    let result = [...withCriticsRating, ...withoutCriticsRating];
    
    // 6. Формирование ответа
    return {
        content: result,
        total: result.length,
        sortedBy: filters.sortBy,
        sortOrder: filters.sortOrder
    };
}
```

## 📊 Примеры обработки данных

### Входные данные
```json
// Films API
[
  {"id": 1, "type": "film", "title": "Фильм 1", "criticsRating": 8.5},
  {"id": 2, "type": "film", "title": "Фильм 2", "criticsRating": null},
  {"id": 3, "type": "film", "title": "Фильм 3", "criticsRating": 7.2}
]

// Series API
[
  {"id": 4, "type": "series", "title": "Сериал 1", "criticsRating": 9.1},
  {"id": 5, "type": "series", "title": "Сериал 2", "criticsRating": null}
]
```

### После объединения
```json
[
  {"id": 1, "type": "film", "title": "Фильм 1", "criticsRating": 8.5},
  {"id": 2, "type": "film", "title": "Фильм 2", "criticsRating": null},
  {"id": 3, "type": "film", "title": "Фильм 3", "criticsRating": 7.2},
  {"id": 4, "type": "series", "title": "Сериал 1", "criticsRating": 9.1},
  {"id": 5, "type": "series", "title": "Сериал 2", "criticsRating": null}
]
```

### После фильтрации по типу (type=film)
```json
[
  {"id": 1, "type": "film", "title": "Фильм 1", "criticsRating": 8.5},
  {"id": 2, "type": "film", "title": "Фильм 2", "criticsRating": null},
  {"id": 3, "type": "film", "title": "Фильм 3", "criticsRating": 7.2}
]
```

### После разделения на группы
```json
// Группа 1: С criticsRating
[
  {"id": 1, "type": "film", "title": "Фильм 1", "criticsRating": 8.5},
  {"id": 3, "type": "film", "title": "Фильм 3", "criticsRating": 7.2}
]

// Группа 2: Без criticsRating
[
  {"id": 2, "type": "film", "title": "Фильм 2", "criticsRating": null}
]
```

### После сортировки и объединения
```json
[
  {"id": 1, "type": "film", "title": "Фильм 1", "criticsRating": 8.5},
  {"id": 3, "type": "film", "title": "Фильм 3", "criticsRating": 7.2},
  {"id": 2, "type": "film", "title": "Фильм 2", "criticsRating": null}
]
```

## ⚡ Производительность обработки

| Этап | Время | Описание |
|------|-------|----------|
| Объединение данных | ~1ms | Конкатенация массивов |
| Фильтрация по типу | ~2ms | O(n) проход по массиву |
| Разделение на группы | ~3ms | O(n) проверка criticsRating |
| Сортировка | ~5ms | O(n log n) быстрая сортировка |
| Объединение групп | ~1ms | Конкатенация отсортированных групп |
| **Общее время** | **~12ms** | **Обработка 1000 элементов** |

---

**Статус**: Детализировано  
**Сложность**: Средняя  
**Производительность**: Высокая
