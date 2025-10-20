# Архитектура системы Stets Home

## Описание

Диаграмма архитектуры системы показывает компоненты Stets Home и их взаимодействие на высоком уровне. Использует UML Component Diagram для отображения архитектуры.

## Диаграмма

```mermaid
graph TB
    %% Пользователи и внешние системы
    User["👤 Пользователь<br/>(Mobile App)"]
    IoTDevices["🏠 Умные устройства Stets<br/>(IoT)"]
    EmailService["📧 Email Service<br/>(External)"]
    
    %% Мобильное приложение
    MobileApp["📱 Mobile App<br/>(React Native/Flutter)"]
    
    %% Backend компоненты
    APIGateway["🚪 API Gateway<br/>(Load Balancer, Auth)"]
    AuthService["🔐 Authentication Service<br/>(JWT, OAuth)"]
    UserService["👤 User Service<br/>(CRUD Users)"]
    HomeService["🏠 Home Service<br/>(CRUD Homes, Rooms)"]
    DeviceService["🔌 Device Service<br/>(CRUD Devices)"]
    ScenarioService["🤖 Scenario Service<br/>(Automation Logic)"]
    IoTGateway["🌐 IoT Gateway<br/>(Device Communication)"]
    NotificationService["📢 Notification Service<br/>(Email, Push)"]
    
    %% База данных
    Database["🗄️ PostgreSQL Database<br/>(Primary Data Store)"]
    
    %% Кэш и очереди
    Redis["⚡ Redis Cache<br/>(Sessions, Temp Data)"]
    MessageQueue["📬 Message Queue<br/>(RabbitMQ/Kafka)"]
    
    %% Мониторинг
    Monitoring["📊 Monitoring<br/>(Prometheus, Grafana)"]
    Logging["📝 Logging<br/>(ELK Stack)"]
    
    %% Связи пользователя
    User --> MobileApp
    
    %% Связи мобильного приложения
    MobileApp --> APIGateway
    
    %% Связи API Gateway
    APIGateway --> AuthService
    APIGateway --> UserService
    APIGateway --> HomeService
    APIGateway --> DeviceService
    APIGateway --> ScenarioService
    APIGateway --> NotificationService
    
    %% Связи сервисов с базой данных
    AuthService --> Database
    UserService --> Database
    HomeService --> Database
    DeviceService --> Database
    ScenarioService --> Database
    
    %% Связи сервисов с кэшем
    AuthService --> Redis
    UserService --> Redis
    HomeService --> Redis
    DeviceService --> Redis
    
    %% Связи IoT
    DeviceService --> IoTGateway
    IoTGateway --> IoTDevices
    IoTDevices --> IoTGateway
    
    %% Связи уведомлений
    NotificationService --> EmailService
    NotificationService --> MobileApp
    
    %% Связи с очередями
    ScenarioService --> MessageQueue
    IoTGateway --> MessageQueue
    NotificationService --> MessageQueue
    
    %% Связи мониторинга
    Monitoring --> AuthService
    Monitoring --> UserService
    Monitoring --> HomeService
    Monitoring --> DeviceService
    Monitoring --> ScenarioService
    Monitoring --> IoTGateway
    Monitoring --> NotificationService
    
    Logging --> AuthService
    Logging --> UserService
    Logging --> HomeService
    Logging --> DeviceService
    Logging --> ScenarioService
    Logging --> IoTGateway
    Logging --> NotificationService
    
    %% Стили
    classDef user fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef mobile fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    classDef api fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef service fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef database fill:#e0f2f1,stroke:#00695c,stroke-width:2px
    classDef external fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef monitoring fill:#f1f8e9,stroke:#558b2f,stroke-width:2px
    
    class User user
    class MobileApp mobile
    class APIGateway api
    class AuthService,UserService,HomeService,DeviceService,ScenarioService,IoTGateway,NotificationService service
    class Database,Redis,MessageQueue database
    class IoTDevices,EmailService external
    class Monitoring,Logging monitoring
```

## Компоненты системы

### Frontend Layer (Слой представления)

#### Mobile App (React Native/Flutter)
- **Назначение:** Мобильное приложение для iOS и Android
- **Технологии:** React Native или Flutter
- **Функции:**
  - UI/UX интерфейс
  - Управление состоянием
  - Локальное кэширование
  - Push-уведомления
  - QR-сканер

### API Layer (Слой API)

#### API Gateway
- **Назначение:** Единая точка входа для всех API запросов
- **Функции:**
  - Маршрутизация запросов
  - Аутентификация и авторизация
  - Rate limiting
  - Логирование запросов
  - Load balancing

### Business Logic Layer (Слой бизнес-логики)

#### Authentication Service
- **Назначение:** Управление аутентификацией и авторизацией
- **Функции:**
  - Регистрация пользователей
  - Вход в систему
  - Восстановление пароля
  - Управление JWT токенами
  - Проверка прав доступа

#### User Service
- **Назначение:** Управление пользователями
- **Функции:**
  - CRUD операции с пользователями
  - Управление профилями
  - Изменение email и пароля
  - Удаление аккаунтов

#### Home Service
- **Назначение:** Управление домами и комнатами
- **Функции:**
  - CRUD операции с домами
  - CRUD операции с комнатами
  - Управление участниками дома
  - Приглашения пользователей

#### Device Service
- **Назначение:** Управление устройствами
- **Функции:**
  - Добавление устройств (QR + ручной ввод)
  - CRUD операции с устройствами
  - Управление статусом устройств
  - Предотвращение дубликатов

#### Scenario Service
- **Назначение:** Управление сценариями автоматизации
- **Функции:**
  - Создание и редактирование сценариев
  - Выполнение сценариев
  - Управление расписанием
  - Планировщик задач

#### IoT Gateway
- **Назначение:** Коммуникация с IoT устройствами
- **Функции:**
  - Протоколы связи с устройствами
  - Синхронизация статусов
  - Обработка ошибок связи
  - Режим энергосбережения

#### Notification Service
- **Назначение:** Отправка уведомлений
- **Функции:**
  - Email уведомления
  - Push уведомления
  - Восстановление пароля
  - Приглашения пользователей

### Data Layer (Слой данных)

#### PostgreSQL Database
- **Назначение:** Основное хранилище данных
- **Содержимое:**
  - Все бизнес-данные
  - Пользователи, дома, комнаты
  - Устройства и сценарии
  - Аудит и логи

#### Redis Cache
- **Назначение:** Кэширование и сессии
- **Использование:**
  - Сессии пользователей
  - Кэш часто запрашиваемых данных
  - Временные данные
  - Rate limiting

#### Message Queue (RabbitMQ/Kafka)
- **Назначение:** Асинхронная обработка
- **Использование:**
  - Выполнение сценариев
  - Отправка уведомлений
  - Синхронизация с IoT
  - Обработка событий

### External Services (Внешние сервисы)

#### Email Service
- **Назначение:** Отправка email
- **Функции:**
  - Восстановление пароля
  - Приглашения пользователей
  - Уведомления о событиях

#### IoT Devices (Умные устройства Stets)
- **Назначение:** Физические устройства
- **Функции:**
  - Выполнение команд
  - Передача статуса
  - Режим энергосбережения

### Monitoring Layer (Слой мониторинга)

#### Monitoring (Prometheus + Grafana)
- **Назначение:** Мониторинг системы
- **Метрики:**
  - Производительность API
  - Использование ресурсов
  - Доступность сервисов
  - Бизнес-метрики

#### Logging (ELK Stack)
- **Назначение:** Централизованное логирование
- **Компоненты:**
  - Elasticsearch (хранение)
  - Logstash (обработка)
  - Kibana (визуализация)

## Потоки данных

### Поток управления устройством
1. **Mobile App** → API Gateway → Device Service
2. **Device Service** → IoT Gateway → IoT Devices
3. **IoT Devices** → IoT Gateway → Device Service
4. **Device Service** → Database (обновление статуса)
5. **Device Service** → Mobile App (подтверждение)

### Поток создания сценария
1. **Mobile App** → API Gateway → Scenario Service
2. **Scenario Service** → Database (сохранение сценария)
3. **Scenario Service** → Message Queue (планирование)
4. **Message Queue** → Scenario Service (выполнение)
5. **Scenario Service** → Device Service (команды)

### Поток аутентификации
1. **Mobile App** → API Gateway → Auth Service
2. **Auth Service** → Database (проверка учетных данных)
3. **Auth Service** → Redis (сохранение сессии)
4. **Auth Service** → Mobile App (JWT токен)

## Технологический стек

### Frontend
- **Mobile:** React Native или Flutter
- **State Management:** Redux/MobX или Provider/Bloc
- **Navigation:** React Navigation или Flutter Navigation

### Backend
- **API Gateway:** Kong, AWS API Gateway, или NGINX
- **Services:** Node.js, Python (FastAPI), или Go
- **Database:** PostgreSQL
- **Cache:** Redis
- **Message Queue:** RabbitMQ или Apache Kafka

### Infrastructure
- **Containerization:** Docker + Kubernetes
- **Cloud:** AWS, Google Cloud, или Azure
- **CI/CD:** GitHub Actions, GitLab CI, или Jenkins
- **Monitoring:** Prometheus + Grafana
- **Logging:** ELK Stack

## Масштабируемость

### Горизонтальное масштабирование
- **API Gateway:** Load balancer с множественными инстансами
- **Services:** Микросервисная архитектура
- **Database:** Read replicas для чтения
- **Cache:** Redis Cluster

### Вертикальное масштабирование
- **Database:** Увеличение ресурсов сервера
- **Services:** Увеличение CPU/RAM для сервисов
- **IoT Gateway:** Оптимизация протоколов связи

## Безопасность

### Аутентификация и авторизация
- **JWT токены** с коротким временем жизни
- **Refresh токены** для обновления сессий
- **Role-based access control** (RBAC)
- **API ключи** для IoT устройств

### Защита данных
- **HTTPS** для всех соединений
- **Шифрование** паролей (bcrypt)
- **Валидация** всех входных данных
- **Rate limiting** для предотвращения атак

### Мониторинг безопасности
- **Логирование** всех операций
- **Алерты** на подозрительную активность
- **Аудит** доступа к данным

## Связь с документацией

Эта диаграмма дополняет техническую документацию и соответствует архитектурным решениям из документа `06_summary/project_summary.md`.
