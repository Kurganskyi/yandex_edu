# Словарь данных (логический уровень)

Документ описывает атрибуты сущностей логической ER-модели Stets Home. Для каждой сущности перечислены основные поля, типы данных, ограничения и примеры значений. Внешние ключи явно не приводятся — связи задокументированы в `er_model.md`.

## USER — Пользователи

| Поле | Описание | Тип | Длина/диапазон | Ограничения/пример |
|------|----------|-----|----------------|--------------------|
| user_id | Уникальный идентификатор | INT | 11 | PK, AUTO_INCREMENT |
| email | Email для входа и уведомлений | VARCHAR | 255 | NOT NULL, UNIQUE, формат email (`user@example.com`) |
| password_hash | Хэш пароля | VARCHAR | 60 | NOT NULL, bcrypt |
| name | Имя пользователя | VARCHAR | 100 | NOT NULL, мин. 2 символа, пример: «Михаил» |
| created_at | Дата регистрации | TIMESTAMP | - | NOT NULL, `DEFAULT CURRENT_TIMESTAMP` |
| updated_at | Дата обновления | TIMESTAMP | - | NOT NULL, `DEFAULT CURRENT_TIMESTAMP ON UPDATE` |

## HOME — Дома

| Поле | Описание | Тип | Длина | Ограничения/пример |
|------|----------|-----|-------|--------------------|
| home_id | Идентификатор дома | INT | 11 | PK, AUTO_INCREMENT |
| name | Название дома | VARCHAR | 100 | NOT NULL, по умолчанию «Мой дом» |
| created_at | Дата создания | TIMESTAMP | - | NOT NULL |

## USER_HOME — Участие пользователя

| Поле | Описание | Тип | Длина | Ограничения/пример |
|------|----------|-----|-------|--------------------|
| user_home_id | Идентификатор связи | INT | 11 | PK, AUTO_INCREMENT |
| role | Роль в доме | ENUM | - | NOT NULL, значения: `owner`, `member` |
| added_at | Дата добавления | TIMESTAMP | - | NOT NULL |

## ROOM — Комнаты

| Поле | Описание | Тип | Длина | Ограничения/пример |
|------|----------|-----|-------|--------------------|
| room_id | Идентификатор комнаты | INT | 11 | PK, AUTO_INCREMENT |
| name | Название комнаты | VARCHAR | 100 | NOT NULL, пример: «Главная спальня» |
| type | Тип помещения | ENUM | - | NOT NULL; значения: `living_room`, `bedroom`, `kitchen`, `bathroom`, `hallway`, `corridor`, `other` |
| icon_code | Код иконки | VARCHAR | 50 | NOT NULL, пример: `icon-bedroom` |
| created_at | Дата создания | TIMESTAMP | - | NOT NULL |

## DEVICE — Устройства

| Поле | Описание | Тип | Длина | Ограничения/пример |
|------|----------|-----|-------|--------------------|
| device_id | Идентификатор устройства | INT | 11 | PK, AUTO_INCREMENT |
| device_code | 12-значный код | CHAR | 12 | NOT NULL, UNIQUE, `^[0-9]{12}$`, пример: `123456789012` |
| model_name | Название модели | VARCHAR | 100 | NOT NULL, пример: «Stets Bulb Pro» |
| device_type | Тип устройства | ENUM | - | NOT NULL, значения: `bulb`, `socket` |
| capabilities | Поддерживаемые возможности | JSON | - | NOT NULL, пример: `{"energy_saving": true, "brightness": true}` |
| custom_name | Пользовательское название | VARCHAR | 100 | NULL, пример: «Лампочка в спальне» |
| status | Статус устройства | ENUM | - | NOT NULL, `on/off/unavailable`, по умолчанию `off` |
| energy_saving_mode | Режим энергосбережения | BOOLEAN | - | NOT NULL, DEFAULT FALSE |
| added_at | Дата добавления | TIMESTAMP | - | NOT NULL |
| last_seen | Последний контакт | TIMESTAMP | - | NULL |

## SCENARIO — Сценарии

| Поле | Описание | Тип | Длина | Ограничения/пример |
|------|----------|-----|-------|--------------------|
| scenario_id | Идентификатор сценария | INT | 11 | PK, AUTO_INCREMENT |
| name | Название сценария | VARCHAR | 30 | NOT NULL, UNIQUE в пределах дома, пример: «Утренний свет» |
| created_at | Дата создания | TIMESTAMP | - | NOT NULL |
| updated_at | Дата обновления | TIMESTAMP | - | NOT NULL |

## SCENARIO_SCHEDULE — Расписания

| Поле | Описание | Тип | Ограничения/пример |
|------|----------|-----|--------------------|
| schedule_id | Идентификатор расписания | INT | PK, AUTO_INCREMENT |
| weekdays | Флаги дней недели | BOOLEAN[7] | Пример: `[true,true,true,true,true,false,false]` |
| start_time | Время начала | TIME | NULL, формат `HH:MM:SS`, пример: `07:00:00` |
| end_time | Время окончания | TIME | NULL, формат `HH:MM:SS`, пример: `08:00:00` |

## SCENARIO_ACTION — Действия сценариев

| Поле | Описание | Тип | Длина | Ограничения/пример |
|------|----------|-----|-------|--------------------|
| action_id | Идентификатор действия | INT | 11 | PK, AUTO_INCREMENT |
| action_type | Тип действия | ENUM | - | NOT NULL, значения: `turn_on`, `turn_off` |
| execution_order | Порядок выполнения | INT | 11 | NOT NULL, минимум 1 |

## Валидации и бизнес-правила

- Максимум 10 домов на пользователя, 10 комнат и сценариев на дом, 100 устройств на дом.
- Код устройства: строго 12 цифр (`^[0-9]{12}$`).
- Название сценария: 1–30 символов, уникально в пределах дома.
- Пароль пользователя (до хэширования): 8–16 символов, минимум 1 строчная и 1 заглавная латинская буква.

## Примеры записей

```sql
INSERT INTO USER (email, password_hash, name)
VALUES ('mikhail@example.com', '$2b$10$N9qo8uLOickgx2ZMRZoMye...', 'Михаил');

INSERT INTO DEVICE (device_code, model_name, device_type, capabilities, status)
VALUES ('123456789012', 'Stets Bulb Pro', 'bulb', '{"energy_saving": true}', 'off');

INSERT INTO SCENARIO (name)
VALUES ('Утренний свет');
```

## Связанные материалы

- ER-модель: [`er_model.md`](er_model.md)
- Диаграммы DFD и описания интерфейса: разделы `../03_design` и `../05_interface`
 