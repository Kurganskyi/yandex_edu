# ER-диаграмма Stets Home (основная)

## Описание

Основная ER-диаграмма показывает логическую модель данных приложения Stets Home с 10 сущностями и их связями в нотации Crow's Foot.

## Диаграмма

```mermaid
erDiagram
    USER {
        int user_id PK
        varchar email UK
        varchar password_hash
        varchar name
        timestamp created_at
        timestamp updated_at
    }
    
    HOME {
        int home_id PK
        varchar name
        timestamp created_at
    }
    
    USER_HOME {
        int user_home_id PK
        int user_id FK
        int home_id FK
        enum role
        timestamp added_at
    }
    
    ICON {
        int icon_id PK
        varchar icon_name UK
        varchar icon_url
        varchar category
    }
    
    ROOM {
        int room_id PK
        int home_id FK
        varchar name
        enum type
        int icon_id FK
        timestamp created_at
    }
    
    DEVICE_MODEL {
        int model_id PK
        varchar model_name UK
        enum device_type
        json capabilities
        text description
    }
    
    DEVICE {
        int device_id PK
        char(12) device_code UK
        int model_id FK
        int home_id FK
        int room_id FK
        varchar custom_name
        enum status
        boolean energy_saving_mode
        timestamp added_at
        timestamp last_seen
    }
    
    SCENARIO {
        int scenario_id PK
        int home_id FK
        varchar name
        timestamp created_at
        timestamp updated_at
    }
    
    SCENARIO_SCHEDULE {
        int schedule_id PK
        int scenario_id FK
        boolean monday
        boolean tuesday
        boolean wednesday
        boolean thursday
        boolean friday
        boolean saturday
        boolean sunday
        time start_time
        time end_time
    }
    
    SCENARIO_ACTION {
        int action_id PK
        int scenario_id FK
        int device_id FK
        enum action_type
        int execution_order
    }
    
    %% Связи
    USER ||--o{ USER_HOME : "имеет доступ к"
    HOME ||--o{ USER_HOME : "содержит пользователей"
    HOME ||--o{ ROOM : "содержит"
    ICON ||--o{ ROOM : "используется в"
    HOME ||--o{ DEVICE : "содержит"
    ROOM ||--o{ DEVICE : "содержит"
    DEVICE_MODEL ||--o{ DEVICE : "является моделью"
    HOME ||--o{ SCENARIO : "содержит"
    SCENARIO ||--o{ SCENARIO_SCHEDULE : "имеет расписание"
    SCENARIO ||--o{ SCENARIO_ACTION : "выполняет действия"
    DEVICE ||--o{ SCENARIO_ACTION : "участвует в действиях"
```

## Сущности и их назначение

### Основные сущности

#### USER (Пользователь)
- **Назначение:** Зарегистрированные пользователи системы
- **Ключевые атрибуты:** email (уникальный), password_hash, name
- **Особенности:** Автоматическое создание/обновление временных меток

#### HOME (Дом)
- **Назначение:** Умные дома пользователей
- **Ключевые атрибуты:** name (по умолчанию "Мой дом")
- **Особенности:** Автосоздание при регистрации пользователя

#### USER_HOME (Связь пользователей и домов)
- **Назначение:** Связующая таблица для связи многие-ко-многим
- **Ключевые атрибуты:** role (owner/member)
- **Особенности:** Один пользователь может быть в доме только один раз

### Справочные сущности

#### ICON (Справочник иконок)
- **Назначение:** Предустановленные иконки для комнат
- **Ключевые атрибуты:** icon_name (уникальный), icon_url, category
- **Особенности:** Только чтение, переиспользование

#### DEVICE_MODEL (Справочник моделей устройств)
- **Назначение:** Модели устройств Stets
- **Ключевые атрибуты:** model_name (уникальный), device_type, capabilities (JSON)
- **Особенности:** Масштабируемость при добавлении новых моделей

### Основные бизнес-сущности

#### ROOM (Комната)
- **Назначение:** Комнаты в домах
- **Ключевые атрибуты:** name, type (enum), icon_id
- **Особенности:** Опциональная привязка к дому

#### DEVICE (Устройство)
- **Назначение:** Умные устройства в домах
- **Ключевые атрибуты:** device_code (12 цифр, уникальный), status, energy_saving_mode
- **Особенности:** Может существовать без привязки к комнате

#### SCENARIO (Сценарий)
- **Назначение:** Сценарии автоматизации
- **Ключевые атрибуты:** name (до 30 символов)
- **Особенности:** Уникальное название в рамках дома

### Вспомогательные сущности

#### SCENARIO_SCHEDULE (Расписание сценария)
- **Назначение:** Расписания выполнения сценариев
- **Ключевые атрибуты:** Дни недели (boolean), start_time, end_time
- **Особенности:** Опциональное расписание

#### SCENARIO_ACTION (Действие сценария)
- **Назначение:** Действия, выполняемые сценарием
- **Ключевые атрибуты:** action_type, execution_order
- **Особенности:** Порядок выполнения действий

## Связи и кардинальность

### Связи один-ко-многим (1:M)
- **HOME → ROOM** - в доме может быть много комнат (максимум 10)
- **HOME → DEVICE** - в доме может быть много устройств (максимум 100)
- **HOME → SCENARIO** - в доме может быть много сценариев (максимум 10)
- **ICON → ROOM** - одну иконку могут использовать много комнат
- **DEVICE_MODEL → DEVICE** - одну модель могут иметь много устройств
- **SCENARIO → SCENARIO_SCHEDULE** - у сценария может быть одно расписание
- **SCENARIO → SCENARIO_ACTION** - сценарий может выполнять много действий

### Связи многие-ко-многим (M:N)
- **USER ↔ HOME** (через USER_HOME) - пользователь может управлять несколькими домами, дом может иметь несколько пользователей
- **SCENARIO ↔ DEVICE** (через SCENARIO_ACTION) - сценарий может управлять несколькими устройствами, устройство может участвовать в нескольких сценариях

### Опциональные связи
- **ROOM → DEVICE** - устройство может быть привязано к комнате или существовать без привязки (room_id может быть NULL)

## Ключевые особенности модели

### 1. Нормализация до 3НФ
- Выделены справочники (ICON, DEVICE_MODEL)
- Устранены транзитивные зависимости
- Связующие таблицы для M:N связей

### 2. Масштабируемость
- Справочники позволяют добавлять новые модели устройств и иконки
- Гибкая структура сценариев через SCENARIO_ACTION
- Поддержка множественных домов на пользователя

### 3. Бизнес-правила
- Ограничения количества (10 домов, 10 комнат, 100 устройств, 10 сценариев)
- Уникальность кодов устройств в системе
- Уникальность названий сценариев в доме

### 4. Гибкость
- Комнаты опциональны (снижение порога входа)
- Расписания сценариев опциональны (ручной запуск)
- Порядок выполнения действий в сценариях

## Связь с документацией

Эта диаграмма соответствует документу `04_data/er_model.md` и детализируется в `04_data/data_dictionary.md`.
