# Task 5: Фильтрация списка фильмов и сериалов по эксклюзивности

## Описание задачи

**Название:** Фильтрация списка фильмов и сериалов по эксклюзивности

**Цель:** Повысить конверсию в просмотры эксклюзивного каталога Otium за счёт быстрого фильтра в «Библиотеке» (цель: +15% доли просмотров эксклюзивного контента).

**Требование (user story):** Как пользователь, я хочу включить фильтр «представлены эксклюзивно в Otium», чтобы видеть только эксклюзивные фильмы и сериалы.

## Контекст задания

Это комплексное задание по изучению архитектуры стримингового сервиса **Otium** и доработке API для фильтрации по эксклюзивности. Задание включает:

1. **[Анализ архитектуры](ARCHITECTURE_ANALYSIS.md)** - изучение микросервисной архитектуры Otium
2. **[Изучение API](API_ANALYSIS.md)** - анализ SOAP-сервисов и XML-форматов
3. **[Диаграммы последовательности](SEQUENCE_DIAGRAM.md)** - проектирование взаимодействий
4. **[Доработка API](IMPLEMENTATION_PLAN.md)** - реализация фильтрации по эксклюзивности

## UseCase

1. Пользователь открывает раздел «Библиотека»
2. Отмечает чек-бокс «представлены эксклюзивно в Otium»
3. (Опционально) выбирает тип контента: «Фильмы» / «Сериалы» / «Все»
4. (Опционально) выбирает жанр
5. Клиент вызывает GetContentList с exclusiveOnly=true (+ передаёт contentType, genreValue, пагинацию) - см. [примеры запросов](examples/)
6. Сервис возвращает список, где у каждого элемента есть признак exclusive - см. [примеры ответов](examples/)
7. Интерфейс показывает только позиции с exclusive=true

> **Подробнее:** см. [диаграмму последовательности](SEQUENCE_DIAGRAM.md) и [детальное описание](docs/task_description.md)

## Описание изменений

Необходимо доработать метод **POST {{WebServer}}/content/list** Web Server API:

- **Добавить** в запрос элемент exclusiveOnly (xs:boolean, по умолчанию false) - см. [GetContentListRequest.xsd](xsd/GetContentListRequest.xsd)
- **Добавить** в ответ элемент exclusive (xs:boolean) внутри каждого content - см. [GetContentListResponse.xsd](xsd/GetContentListResponse.xsd)
- **Добавить** обработку комбинаций: exclusiveOnly + contentType + genreValue - см. [примеры](examples/)
- **Добавить** обработку случая, если exclusiveOnly=true и результатов нет — вернуть пустой список без ошибок

> **Подробнее:** см. [план реализации](IMPLEMENTATION_PLAN.md) и [тикет для разработчика](DEVELOPER_TICKET.md)

### Условия работы:

- **если** exclusiveOnly=true, в ответ включаются только записи с exclusive=true
- **если** exclusiveOnly=false (или отсутствует) — поведение выдачи не меняется

## Контекст

В ответах {{FilmsServer}}/films/list и {{SeriesServer}}/series/list уже присутствует элемент exclusive. Требуется унифицировать контракт в XSD GetContentList*. 

> **Подробнее:** см. [анализ API](API_ANALYSIS.md) и [архитектурный анализ](ARCHITECTURE_ANALYSIS.md)

## Acceptance Criteria

- [x] Запрос с exclusiveOnly=true возвращает только exclusive=true - см. [примеры](examples/)
- [x] Комбинации фильтров (тип/жанр/эксклюзивность) отрабатывают корректно - см. [request_variants.xml](examples/request_variants.xml)
- [x] Схемы XSD валидны; автотесты на фильтр проходят - см. [XSD схемы](xsd/)
- [x] Приложены примеры Request/Response - см. [examples/](examples/)

> **Подробнее:** см. [тикет для разработчика](DEVELOPER_TICKET.md) с полным списком критериев приёмки

## Структура решения

```
task_5/
├── [README.md](README.md)                           # Основное описание задачи
├── [STRUCTURE.md](STRUCTURE.md)                     # Структура решения
├── [ARCHITECTURE_ANALYSIS.md](ARCHITECTURE_ANALYSIS.md)  # Анализ архитектуры Otium
├── [API_ANALYSIS.md](API_ANALYSIS.md)               # Анализ API сервисов
├── [SEQUENCE_DIAGRAM.md](SEQUENCE_DIAGRAM.md)       # Диаграммы последовательности
├── [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) # План реализации
├── [DEVELOPER_TICKET.md](DEVELOPER_TICKET.md)       # Тикет для разработчика
├── [ASSIGNMENT_SUMMARY.md](ASSIGNMENT_SUMMARY.md)   # Краткое описание задания
├── docs/
│   └── [task_description.md](docs/task_description.md)  # Детальное описание задачи
├── xsd/
│   ├── [GetContentListRequest.xsd](xsd/GetContentListRequest.xsd)    # Схема запроса (исправленная)
│   └── [GetContentListResponse.xsd](xsd/GetContentListResponse.xsd)  # Схема ответа (исправленная)
└── examples/
    ├── [request_example.xml](examples/request_example.xml)           # Пример запроса
    ├── [response_example.xml](examples/response_example.xml)         # Пример ответа
    └── [request_variants.xml](examples/request_variants.xml)         # Различные варианты запросов
```

> **Быстрый доступ:** [XSD схемы](xsd/) | [Примеры](examples/) | [Документация](docs/) | [План реализации](IMPLEMENTATION_PLAN.md)

## Найденные ошибки в исходных XSD

### [GetContentListRequest.xsd](xsd/GetContentListRequest.xsd)
- Лишний символ `]` после имени элемента
- Отсутствует `xs:complexType` у корневого элемента
- `genreValue` без указания `type`
- Отсутствуют закрывающие теги `xs:complexType/xs:sequence/xs:schema`

### [GetContentListResponse.xsd](xsd/GetContentListResponse.xsd)
- Лишние/неуместные namespace/атрибуты (`soap:encodingStyle`) на `xs:schema`
- У многих элементов нет `type` (contentId, ageRate и др.)
- Синтаксические ошибки: перепутан порядок name/type, битые кавычки, незакрытые теги
- Пустые имена элементов (`name="" type=""`)
- Неправильные кратности (нет `maxOccurs` там, где нужен список)
- Отсутствует поле `exclusive`, необходимое по требованиям
- Неправильный тип `contentId` (должен быть `xs:integer`)
- Неправильная структура `country` (должен быть простой элемент)
- Неправильный элемент `directors` (должен быть `dubbingTeam`)

> **Подробнее:** см. [структуру решения](STRUCTURE.md) с описанием всех исправлений

## Решение

### Анализ архитектуры
- ✅ Изучена микросервисная архитектура Otium (5 сервисов) - см. [ARCHITECTURE_ANALYSIS.md](ARCHITECTURE_ANALYSIS.md)
- ✅ Определены точки интеграции для фильтрации - см. [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
- ✅ Создана диаграмма последовательности с параллельными запросами - см. [SEQUENCE_DIAGRAM.md](SEQUENCE_DIAGRAM.md)

### Анализ API
- ✅ Изучены SOAP-сервисы с XML-форматом данных - см. [API_ANALYSIS.md](API_ANALYSIS.md)
- ✅ Определен Web Server API как точка доработки - см. [DEVELOPER_TICKET.md](DEVELOPER_TICKET.md)
- ✅ Проанализированы существующие атрибуты `exclusive` - см. [примеры ответов](examples/)

### Техническое решение
Созданы исправленные и дополненные XSD-схемы с:
- Добавленным фильтром `exclusiveOnly` в запросе - см. [GetContentListRequest.xsd](xsd/GetContentListRequest.xsd)
- Добавленным полем `exclusive` в ответе - см. [GetContentListResponse.xsd](xsd/GetContentListResponse.xsd)
- Исправленными синтаксическими ошибками - см. [STRUCTURE.md](STRUCTURE.md)
- Правильными типами данных и кратностями
- Единым перечислением `ContentType` (film|series|all)
- **Исправленным типом `contentId`** на `xs:integer`
- **Упрощенным элементом `country`** (без вложенности)
- **Замененным `directors` на `dubbingTeam`** (простой элемент)

> **Подробнее:** см. [структуру решения](STRUCTURE.md) и [план реализации](IMPLEMENTATION_PLAN.md)

### Готовые материалы
- [x] [Исправленные XSD-схемы](xsd/) - [GetContentListRequest.xsd](xsd/GetContentListRequest.xsd), [GetContentListResponse.xsd](xsd/GetContentListResponse.xsd)
- [x] [Диаграммы последовательности](SEQUENCE_DIAGRAM.md)
- [x] [План реализации](IMPLEMENTATION_PLAN.md)
- [x] [Тикет для разработчика](DEVELOPER_TICKET.md)
- [x] [Примеры запросов/ответов](examples/) - [request_example.xml](examples/request_example.xml), [response_example.xml](examples/response_example.xml), [request_variants.xml](examples/request_variants.xml)
- [x] [Полная документация](docs/) - [task_description.md](docs/task_description.md), [API_ANALYSIS.md](API_ANALYSIS.md), [ARCHITECTURE_ANALYSIS.md](ARCHITECTURE_ANALYSIS.md)
- [x] [Краткое описание задания](ASSIGNMENT_SUMMARY.md)

> **Быстрый старт:** [XSD схемы](xsd/) | [Примеры](examples/) | [План реализации](IMPLEMENTATION_PLAN.md) | [Тикет для разработчика](DEVELOPER_TICKET.md)
