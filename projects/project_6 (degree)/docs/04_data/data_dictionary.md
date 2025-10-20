# Словарь данных (Data Dictionary)

## Контекст

Словарь данных содержит детальное описание всех атрибутов из ER-модели приложения Stets Home. Включает типы данных, ограничения, валидации и примеры значений для всех 50+ атрибутов системы.

## Структура словаря

| Элемент данных | Описание | Тип данных | Длина | Значение/Ограничения |
|----------------|----------|------------|-------|----------------------|

## Таблица USER (Пользователи)

| Элемент данных | Описание | Тип данных | Длина | Значение/Ограничения |
|----------------|----------|------------|-------|----------------------|
| user_id | Уникальный идентификатор пользователя | INT | 11 | PRIMARY KEY, AUTO_INCREMENT, NOT NULL |
| email | Email адрес для входа и уведомлений | VARCHAR | 255 | UNIQUE, NOT NULL, формат email, пример: "user@example.com" |
| password_hash | Хэш пароля пользователя | VARCHAR | 60 | NOT NULL, bcrypt hash, пример: "$2b$10$N9qo8uLOickgx2ZMRZoMye..." |
| name | Имя пользователя | VARCHAR | 100 | NOT NULL, минимум 2 символа, пример: "Михаил" |
| created_at | Дата и время регистрации | TIMESTAMP | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP, формат: "YYYY-MM-DD HH:MM:SS" |
| updated_at | Дата и время последнего обновления | TIMESTAMP | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE |

## Таблица HOME (Дома)

| Элемент данных | Описание | Тип данных | Длина | Значение/Ограничения |
|----------------|----------|------------|-------|----------------------|
| home_id | Уникальный идентификатор дома | INT | 11 | PRIMARY KEY, AUTO_INCREMENT, NOT NULL |
| name | Название дома | VARCHAR | 100 | NOT NULL, DEFAULT 'Мой дом', пример: "Квартира на Невском" |
| created_at | Дата и время создания дома | TIMESTAMP | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

## Таблица USER_HOME (Связь пользователей и домов)

| Элемент данных | Описание | Тип данных | Длина | Значение/Ограничения |
|----------------|----------|------------|-------|----------------------|
| user_home_id | Уникальный идентификатор связи | INT | 11 | PRIMARY KEY, AUTO_INCREMENT, NOT NULL |
| user_id | Ссылка на пользователя | INT | 11 | FOREIGN KEY → USER(user_id), NOT NULL |
| home_id | Ссылка на дом | INT | 11 | FOREIGN KEY → HOME(home_id), NOT NULL |
| role | Роль пользователя в доме | ENUM | - | NOT NULL, DEFAULT 'member', значения: 'owner', 'member' |
| added_at | Дата и время добавления к дому | TIMESTAMP | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

## Таблица ICON (Справочник иконок)

| Элемент данных | Описание | Тип данных | Длина | Значение/Ограничения |
|----------------|----------|------------|-------|----------------------|
| icon_id | Уникальный идентификатор иконки | INT | 11 | PRIMARY KEY, AUTO_INCREMENT, NOT NULL |
| icon_name | Название иконки | VARCHAR | 50 | NOT NULL, UNIQUE, пример: "bedroom", "kitchen", "bathroom" |
| icon_url | URL иконки | VARCHAR | 255 | NOT NULL, валидный URL, пример: "/icons/bedroom.svg" |
| category | Категория иконки | VARCHAR | 30 | NOT NULL, значения: "room_type", "device_type" |

## Таблица ROOM (Комнаты)

| Элемент данных | Описание | Тип данных | Длина | Значение/Ограничения |
|----------------|----------|------------|-------|----------------------|
| room_id | Уникальный идентификатор комнаты | INT | 11 | PRIMARY KEY, AUTO_INCREMENT, NOT NULL |
| home_id | Ссылка на дом | INT | 11 | FOREIGN KEY → HOME(home_id), NOT NULL |
| name | Название комнаты | VARCHAR | 100 | NOT NULL, минимум 1 символ, пример: "Главная спальня" |
| type | Тип комнаты | ENUM | - | NOT NULL, DEFAULT 'other', значения: 'living_room', 'bedroom', 'kitchen', 'bathroom', 'hallway', 'corridor', 'other' |
| icon_id | Ссылка на иконку | INT | 11 | FOREIGN KEY → ICON(icon_id), NOT NULL |
| created_at | Дата и время создания комнаты | TIMESTAMP | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

## Таблица DEVICE_MODEL (Справочник моделей устройств)

| Элемент данных | Описание | Тип данных | Длина | Значение/Ограничения |
|----------------|----------|------------|-------|----------------------|
| model_id | Уникальный идентификатор модели | INT | 11 | PRIMARY KEY, AUTO_INCREMENT, NOT NULL |
| model_name | Название модели устройства | VARCHAR | 100 | NOT NULL, UNIQUE, пример: "Stets Bulb Pro", "Stets Socket Basic" |
| device_type | Тип устройства | ENUM | - | NOT NULL, значения: 'bulb', 'socket' |
| capabilities | Возможности устройства в JSON | JSON | - | NOT NULL, пример: {"energy_saving": true, "brightness": true, "color": false} |
| description | Описание модели | TEXT | - | NULL, пример: "Умная лампочка с поддержкой энергосбережения" |

## Таблица DEVICE (Устройства)

| Элемент данных | Описание | Тип данных | Длина | Значение/Ограничения |
|----------------|----------|------------|-------|----------------------|
| device_id | Уникальный идентификатор устройства | INT | 11 | PRIMARY KEY, AUTO_INCREMENT, NOT NULL |
| device_code | 12-значный код устройства | CHAR | 12 | UNIQUE, NOT NULL, только цифры, пример: "123456789012" |
| model_id | Ссылка на модель устройства | INT | 11 | FOREIGN KEY → DEVICE_MODEL(model_id), NOT NULL |
| home_id | Ссылка на дом | INT | 11 | FOREIGN KEY → HOME(home_id), NOT NULL |
| room_id | Ссылка на комнату | INT | 11 | FOREIGN KEY → ROOM(room_id), NULL (опционально) |
| custom_name | Пользовательское название устройства | VARCHAR | 100 | NULL, пример: "Лампочка в спальне" |
| status | Статус устройства | ENUM | - | NOT NULL, DEFAULT 'off', значения: 'on', 'off', 'unavailable' |
| energy_saving_mode | Режим энергосбережения | BOOLEAN | - | NOT NULL, DEFAULT FALSE |
| added_at | Дата и время добавления устройства | TIMESTAMP | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| last_seen | Последний контакт с устройством | TIMESTAMP | - | NULL, обновляется при каждом контакте |

## Таблица SCENARIO (Сценарии)

| Элемент данных | Описание | Тип данных | Длина | Значение/Ограничения |
|----------------|----------|------------|-------|----------------------|
| scenario_id | Уникальный идентификатор сценария | INT | 11 | PRIMARY KEY, AUTO_INCREMENT, NOT NULL |
| home_id | Ссылка на дом | INT | 11 | FOREIGN KEY → HOME(home_id), NOT NULL |
| name | Название сценария | VARCHAR | 30 | NOT NULL, минимум 1 символ, максимум 30 символов, пример: "Утренний свет" |
| created_at | Дата и время создания сценария | TIMESTAMP | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | Дата и время последнего обновления | TIMESTAMP | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE |

## Таблица SCENARIO_SCHEDULE (Расписания сценариев)

| Элемент данных | Описание | Тип данных | Длина | Значение/Ограничения |
|----------------|----------|------------|-------|----------------------|
| schedule_id | Уникальный идентификатор расписания | INT | 11 | PRIMARY KEY, AUTO_INCREMENT, NOT NULL |
| scenario_id | Ссылка на сценарий | INT | 11 | FOREIGN KEY → SCENARIO(scenario_id), NOT NULL |
| monday | Выполнение в понедельник | BOOLEAN | - | NOT NULL, DEFAULT FALSE |
| tuesday | Выполнение во вторник | BOOLEAN | - | NOT NULL, DEFAULT FALSE |
| wednesday | Выполнение в среду | BOOLEAN | - | NOT NULL, DEFAULT FALSE |
| thursday | Выполнение в четверг | BOOLEAN | - | NOT NULL, DEFAULT FALSE |
| friday | Выполнение в пятницу | BOOLEAN | - | NOT NULL, DEFAULT FALSE |
| saturday | Выполнение в субботу | BOOLEAN | - | NOT NULL, DEFAULT FALSE |
| sunday | Выполнение в воскресенье | BOOLEAN | - | NOT NULL, DEFAULT FALSE |
| start_time | Время начала выполнения | TIME | - | NULL, формат: "HH:MM:SS", пример: "07:00:00" |
| end_time | Время окончания выполнения | TIME | - | NULL, формат: "HH:MM:SS", пример: "08:00:00" |

## Таблица SCENARIO_ACTION (Действия сценариев)

| Элемент данных | Описание | Тип данных | Длина | Значение/Ограничения |
|----------------|----------|------------|-------|----------------------|
| action_id | Уникальный идентификатор действия | INT | 11 | PRIMARY KEY, AUTO_INCREMENT, NOT NULL |
| scenario_id | Ссылка на сценарий | INT | 11 | FOREIGN KEY → SCENARIO(scenario_id), NOT NULL |
| device_id | Ссылка на устройство | INT | 11 | FOREIGN KEY → DEVICE(device_id), NOT NULL |
| action_type | Тип действия | ENUM | - | NOT NULL, значения: 'turn_on', 'turn_off' |
| execution_order | Порядок выполнения действия | INT | 11 | NOT NULL, DEFAULT 1, минимум 1 |

## Валидации и бизнес-правила

### Валидация email
- Формат: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Длина: 5-255 символов
- Уникальность в системе

### Валидация пароля (описание для пользователя)
- Длина: 8-16 символов
- Минимум 1 строчная буква латиницы (a-z)
- Минимум 1 прописная буква латиницы (A-Z)
- Может содержать цифры и специальные символы
- Примеры валидных паролей: "Password123", "MySecure1", "TestPass9"

### Валидация кода устройства
- Формат: `^[0-9]{12}$`
- Ровно 12 цифр
- Уникальность в системе
- Примеры: "123456789012", "987654321098"

### Валидация названия сценария
- Длина: 1-30 символов
- Может содержать буквы, цифры, пробелы, дефисы
- Уникальность в рамках дома
- Примеры: "Утренний свет", "Вечерний режим", "Выход из дома"

### Валидация времени
- Формат: HH:MM:SS (24-часовой формат)
- Диапазон: 00:00:00 - 23:59:59
- Примеры: "07:00:00", "22:30:00", "00:15:30"

### Валидация JSON (capabilities)
- Валидный JSON формат
- Обязательные поля зависят от типа устройства
- Пример для лампочки: `{"energy_saving": true, "brightness": true, "color": false}`
- Пример для розетки: `{"energy_saving": true, "brightness": false, "color": false}`

## Ограничения целостности

### Каскадные операции
- При удалении пользователя: удаляются все его связи с домами (USER_HOME)
- При удалении дома: удаляются все комнаты, устройства и сценарии дома
- При удалении комнаты: устройства остаются без привязки (room_id = NULL)
- При удалении сценария: удаляются все его расписания и действия

### Проверки ограничений
- Максимум 10 домов на пользователя (проверка в приложении)
- Максимум 10 комнат на дом (проверка в приложении)
- Максимум 100 устройств на дом (проверка в приложении)
- Максимум 10 сценариев на дом (проверка в приложении)

### Уникальные ограничения
- Один пользователь может быть в доме только один раз (UNIQUE(user_id, home_id))
- Уникальное название комнаты в доме (UNIQUE(home_id, name))
- Уникальное название сценария в доме (UNIQUE(home_id, name))
- Уникальный код устройства в системе (UNIQUE(device_code))

## Индексы для производительности

### Первичные индексы
- Все таблицы имеют первичный ключ с AUTO_INCREMENT

### Уникальные индексы
- USER.email
- USER_HOME(user_id, home_id)
- ROOM(home_id, name)
- SCENARIO(home_id, name)
- DEVICE.device_code
- ICON.icon_name
- DEVICE_MODEL.model_name

### Обычные индексы
- USER_HOME.home_id
- ROOM.home_id
- DEVICE.home_id
- DEVICE.room_id
- DEVICE.status
- SCENARIO.home_id
- SCENARIO_SCHEDULE.scenario_id
- SCENARIO_ACTION(scenario_id, execution_order)

## Примеры данных

### Пример записи USER
```sql
INSERT INTO USER (email, password_hash, name) VALUES 
('mikhail@example.com', '$2b$10$N9qo8uLOickgx2ZMRZoMye...', 'Михаил');
```

### Пример записи DEVICE
```sql
INSERT INTO DEVICE (device_code, model_id, home_id, room_id, custom_name, status) VALUES 
('123456789012', 1, 1, 1, 'Лампочка в спальне', 'off');
```

### Пример записи SCENARIO_SCHEDULE
```sql
INSERT INTO SCENARIO_SCHEDULE (scenario_id, monday, tuesday, wednesday, thursday, friday, start_time, end_time) VALUES 
(1, TRUE, TRUE, TRUE, TRUE, TRUE, '07:00:00', '08:00:00');
```

### Пример JSON capabilities
```json
{
  "energy_saving": true,
  "brightness": true,
  "color": false,
  "max_brightness": 100,
  "min_brightness": 1
}
```

## Рекомендации по реализации

### Типы данных в разных СУБД
- **MySQL**: Использовать указанные типы
- **PostgreSQL**: TIMESTAMP → TIMESTAMPTZ для учета часовых поясов
- **SQLite**: VARCHAR → TEXT, BOOLEAN → INTEGER

### Безопасность
- Все пароли хранить только в виде bcrypt хэшей
- Использовать prepared statements
- Валидировать все входные данные на уровне приложения
- Реализовать rate limiting для API

### Производительность
- Использовать connection pooling
- Реализовать кэширование для справочников (ICON, DEVICE_MODEL)
- Рассмотреть партиционирование больших таблиц
- Мониторить производительность запросов
