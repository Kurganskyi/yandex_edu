# Программа и методика испытаний (ПМИ)

## Объект испытаний

Мобильное приложение "Stets Home" версии 1.0 (прототип)

---

## Цель испытаний

Проверить соответствие прототипа мобильного приложения "Stets Home" требованиям MVP, определенным в первой части дипломного проекта. Убедиться, что все функции MVP реализованы в прототипе и соответствуют описанным пользовательским историям с критериями приемки и Gherkin-сценариями.

---

## Требования к программе

Прототип должен реализовывать следующие функции MVP:

### АКТИВНОСТЬ 1: Войти в приложение

**US-001:** Регистрация нового пользователя  
**US-003:** Вход в приложение  
**US-004:** Восстановление пароля  
**US-005:** Изменение email  
**US-006:** Выход из приложения

### АКТИВНОСТЬ 2: Организовать умный дом

**US-007:** Создание комнат  
**US-008:** Редактирование комнат  
**US-009:** Удаление комнат  
**US-010:** Добавление устройства через QR-код  
**US-011:** Добавление устройства вручную  
**US-012:** Предотвращение дубликатов устройств  
**US-013:** Привязка устройства к комнате  
**US-014:** Удаление устройства  
**US-044:** Удаление устройства из комнаты

### АКТИВНОСТЬ 3: Управлять умным домом

**US-016:** Управление режимом энергосбережения  
**US-017:** Управление всеми устройствами комнаты  
**US-018:** Создание сценария  
**US-019:** Ручной запуск сценария  
**US-020:** Настройка расписания сценария  
**US-021:** Удаление сценария

### Дополнительные функции (не в MVP)

**TR-7:** Выдача доступа к дому (совместный доступ)  
**TR-7.1:** Принятие приглашения

---

## Требования к программной документации

Для проведения испытаний необходимы следующие документы:

1. **Программа и методика испытаний (ПМИ)** - настоящий документ
2. **Карта пользовательских историй** - документ с описанием всех пользовательских историй, критериев приемки и Gherkin-сценариев
3. **Диаграммы потоков данных (DFD)** - контекстная и логическая диаграммы
4. **ER-диаграмма** - модель данных приложения
5. **Словарь данных** - описание всех элементов данных
6. **Диаграмма структуры интерфейса** - структура экранов приложения
7. **Список экранов прототипа** - детальное описание всех экранов с элементами интерфейса

---

## Средства и порядок испытаний

### Средства испытаний

1. **Прототип приложения:**
   - Интерактивный или статический прототип в Figma
   - Доступ к прототипу через веб-интерфейс Figma
   - Размер экранов: iPhone 13 mini (375 × 812)

2. **Оборудование:**
   - Компьютер или ноутбук с доступом в интернет
   - Мобильное устройство (iOS/Android) или эмулятор для тестирования навигации (опционально)
   - Браузер для просмотра прототипа в Figma

3. **Документация:**
   - Все документы из первой части дипломного проекта
   - Список экранов прототипа
   - Карта пользовательских историй

### Порядок испытаний

1. **Подготовка:**
   - Открыть прототип в Figma
   - Иметь под рукой карту пользовательских историй и список экранов
   - Подготовить чек-лист для отметки выполненных проверок

2. **Проведение испытаний:**
   - Последовательно проходить по всем функциям MVP согласно методике испытаний
   - Для каждой функции выполнять шаги проверки
   - Фиксировать результаты (успех/ошибка) и замечания

3. **Документирование результатов:**
   - Заполнить таблицу результатов испытаний
   - Отметить найденные несоответствия требованиям
   - Подготовить отчет о результатах испытаний

---

## Методика испытаний

### Таблица методики испытаний

<table>
<thead>
<tr>
<th style="text-align: left; padding: 8px; border: 1px solid #ddd;">Требование</th>
<th style="text-align: left; padding: 8px; border: 1px solid #ddd;">Предусловия</th>
<th style="text-align: left; padding: 8px; border: 1px solid #ddd;">Шаг проверки</th>
<th style="text-align: left; padding: 8px; border: 1px solid #ddd;">Ожидаемый результат</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4" style="background-color: #f0f0f0; font-weight: bold; padding: 8px; border: 1px solid #ddd;"><strong>АКТИВНОСТЬ 1: Войти в приложение</strong></td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-001: Регистрация нового пользователя</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь регистрируется впервые</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. На экране входа нажать «Зарегистрироваться».<br>2. Указать валидные значения в полях «Имя» и «Электронная почта».<br>3. Ввести и повторить пароль (соответствует требованиям).<br>4. Нажать «Создать аккаунт».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Кнопка становится активной. Пользователь успешно зарегистрирован. На email приходит письмо о регистрации.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-001: Регистрация - невалидный email</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь регистрируется впервые</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Повторить шаги TR-1, указав невалидный email.<br>2. Нажать «Создать аккаунт».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Поле email подсвечивается красным. Отображается подсказка «Неверный формат электронной почты».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-001: Регистрация - пароли не совпадают</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь регистрируется впервые</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Повторить шаги TR-1, указав разные значения пароля.<br>2. Нажать «Создать аккаунт».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Поле «Повторите пароль» подсвечивается красным. Сообщение «Пароли не совпадают».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-001: Регистрация - невалидный пароль</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь регистрируется впервые</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Повторить шаги TR-1, указав пароль, не соответствующий требованиям.<br>2. Нажать «Создать аккаунт».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Поле «Пароль» подсвечивается красным. Сообщение «Пароль не соответствует требованиям».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-003: Вход в приложение - успешный</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Учетная запись зарегистрирована</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. На экране входа указать валидные email и пароль.<br>2. Нажать «Войти».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь авторизован и попадает на домашний экран.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-003: Вход - неверный пароль</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Учетная запись зарегистрирована</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Указать валидный email и неверный пароль.<br>2. Нажать «Войти».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Поле «Пароль» подсвечивается красным. Сообщение «Неверный пароль».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-003: Вход - несуществующий email</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Аккаунт с указанным email отсутствует</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Указать незарегистрированный email и валидный пароль.<br>2. Нажать «Войти».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Поле email подсвечивается красным. Сообщение «Пользователь с таким email не найден».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-004: Восстановление пароля</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь находится на экране восстановления</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Нажать «Восстановить пароль».<br>2. Указать email и отправить код.<br>3. Ввести корректный 4-значный код вместе с новым паролем.<br>4. Нажать «Сохранить».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Пароль обновлён. Сообщение «Пароль успешно изменён».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-004: Восстановление пароля - просроченный код</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Код подтверждения старше 5 минут</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Повторить TR-3, введя просроченный код.<br>2. Нажать «Сохранить».<br>3. Нажать «Выслать код ещё раз».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сообщение «Код подтверждения устарел». Поле подсвечено красным. Кнопка повторной отправки активна.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-004: Восстановление пароля - неверный код</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь получил код</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Повторить TR-3, указав неверный код.<br>2. Нажать «Сохранить».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сообщение «Введён неверный код». Поле подсвечивается красным. Кнопка повторной отправки активируется через 5 минут.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-005: Изменение email</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь авторизован</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Настройки → «Личные данные».<br>2. Нажать «Изменить email».<br>3. Ввести новый email.<br>4. Нажать «Отправить код».<br>5. Ввести код и подтвердить.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Email изменён. Сообщение «Электронная почта успешно изменена».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-006: Выход из приложения</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь авторизован</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Настройки → «Выход из учётной записи».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сессия завершена. Пользователь перенаправлен на экран входа.</td>
</tr>
<tr>
<td colspan="4" style="background-color: #f0f0f0; font-weight: bold; padding: 8px; border: 1px solid #ddd;"><strong>АКТИВНОСТЬ 2: Организовать умный дом</strong></td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-007: Создание комнат</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">—</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Открыть вкладку «Комнаты».<br>2. Нажать «Добавить комнату».<br>3. Выбрать тип и иконку.<br>4. Нажать «Сохранить».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Появляется карточка комнаты. Сообщение «Комната успешно добавлена».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-007: Создание комнат - превышение лимита</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">В доме 10 комнат</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Нажать «Добавить комнату».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сообщение «Достигнут лимит на количество комнат (10)».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-008: Редактирование комнат</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Есть минимум одна комната</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Открыть комнату из списка.<br>2. Нажать «Тип комнаты».<br>3. Выбрать новое значение.<br>4. Нажать «Сохранить».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Тип обновлён. Сообщение «Комната успешно изменена».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-009: Удаление комнат</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Есть минимум одна комната</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Открыть комнату.<br>2. Нажать «Удалить» → подтвердить.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Комната удалена. Сообщение «Комната успешно удалена».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-010: Добавление устройства через QR-код</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь сканирует устройство Stets</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Во вкладке «Устройства» нажать «Добавить по QR-коду».<br>2. Нажать «Сканировать QR-код».<br>3. Подтвердить данные устройства.<br>4. Нажать «Сохранить».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Данные устройства подставлены. Устройство появляется в списке.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-010: Добавление устройства - QR другого производителя</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь сканирует чужой QR</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Повторить TR-4, используя сторонний QR-код.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сообщение «Устройства других производителей не поддерживаются».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-010: Добавление устройства - превышение лимита</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">В доме уже 100 устройств</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Повторить TR-4 при заполненном лимите.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сообщение «Достигнут лимит на количество устройств (100)».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-011: Добавление устройства вручную</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">—</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Нажать «Добавить устройство вручную».<br>2. Ввести 12-значный ID устройства.<br>3. Выбрать тип устройства из справочника.<br>4. Указать пользовательское название (опционально).<br>5. Подтвердить сохранение.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Устройство появляется в списке с выбранным типом. Статус = `off`, энергосбережение = `false` по умолчанию.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-012: Предотвращение дубликатов устройств</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Устройство уже добавлено</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Повторить TR-4 для устройства, которое уже в системе.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сообщение «Устройство уже добавлено».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-013: Привязка устройства к комнате</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">В системе есть устройства</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Открыть комнату.<br>2. Нажать «Добавить устройство».<br>3. Выбрать устройство → «Сохранить».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Устройство привязано к комнате. Сообщение «Устройство добавлено в комнату».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-014: Удаление устройства</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">В доме есть устройства</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Смахнуть карточку устройства влево.<br>2. Выбрать «Удалить».<br>3. Подтвердить действие.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Устройство удалено. Сообщение «Устройство успешно удалено».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-044: Удаление устройства из комнаты</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Устройство привязано к комнате</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Открыть комнату.<br>2. Свайпнуть устройство влево → «Удалить».<br>3. Подтвердить.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Устройство отвязано. Сообщение «Устройство успешно удалено».</td>
</tr>
<tr>
<td colspan="4" style="background-color: #f0f0f0; font-weight: bold; padding: 8px; border: 1px solid #ddd;"><strong>АКТИВНОСТЬ 3: Управлять умным домом</strong></td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-016: Управление режимом энергосбережения</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">В комнате есть устройства</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Открыть комнату.<br>2. Выбрать устройство.<br>3. Нажать на переключатель энергосбережения.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Статус энергосбережения меняется.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-017: Массовое управление устройствами комнаты</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">В комнате ≥ 1 устройство</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Открыть комнату.<br>2. Переключить «Включить/выключить все устройства».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Статус всех устройств меняется.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-018: Создание сценария по расписанию</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">В доме есть устройства</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. На экране «Сценарии» нажать «Создать сценарий».<br>2. Указать название.<br>3. Добавить устройства и статусы.<br>4. Задать время и дни.<br>5. Нажать «Сохранить».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сценарий сохранён. Сообщение «Сценарий успешно создан».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-018: Создание сценария - превышение лимита</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Создано 10 сценариев</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Нажать «Создать сценарий».<br>2. Подтвердить предупреждение.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сообщение «Достигнут лимит на количество сценариев (10)».</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-019: Ручной запуск сценария</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Есть сценарий с расписанием</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. На экране «Сценарии» нажать «Запустить» у сценария по расписанию.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Статус сценария «Включено», затем «Завершён». Устройства меняют статус.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-019: Запуск сценария с ручным управлением</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Есть сценарий без расписания</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. На экране «Сценарии» нажать «Включить» у ручного сценария.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Устройства принимают заданные статусы. Сценарий завершается.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-020: Создание сценария с ручным запуском</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">В доме есть устройства</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Повторить TR-6, не указывая время и дни.<br>2. Нажать «Сохранить».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сценарий без расписания сохранён.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>US-021: Удаление сценария</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Сценарий существует</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Свайпнуть карточку сценария влево.<br>2. Выбрать «Удалить» и подтвердить.</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сценарий удалён. Сообщение «Сценарий успешно удалён».</td>
</tr>
<tr>
<td colspan="4" style="background-color: #f0f0f0; font-weight: bold; padding: 8px; border: 1px solid #ddd;"><strong>Дополнительные функции (не в MVP)</strong></td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>TR-7: Выдача доступа к дому</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Пользователь авторизован</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. Настройки → «Совместный доступ».<br>2. Указать имя, email, дом «Текущий».<br>3. Выбрать уровень доступа.<br>4. Нажать «Добавить доступ».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сообщение «Доступ успешно выдан». Приглашение появляется в списке. На email отправлено письмо.</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>TR-7.1: Принятие приглашения</strong></td>
<td style="padding: 8px; border: 1px solid #ddd;">Приглашённый пользователь авторизован</td>
<td style="padding: 8px; border: 1px solid #ddd;">1. На экране «Мой дом» нажать «Принять приглашение».</td>
<td style="padding: 8px; border: 1px solid #ddd;">Сообщение «Доступ успешно принят». Доступ к дому открыт.</td>
</tr>
</tbody>
</table>

---

## Примечания

- Для выполнения сценариев можно использовать как физическое устройство, так и эмулятор мобильной ОС.
- Все визуальные состояния (подсветки, уведомления) должны соответствовать дизайн-системе приложения.
- Рекомендуется фиксировать ключевые результаты скриншотами либо записями экрана.

