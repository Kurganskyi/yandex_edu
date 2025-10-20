# Проект системы (архитектура) Stets Home

## 1. Общие сведения

### 1.1 Наименование системы
**Полное наименование:** Система управления умным домом Stets Home  
**Краткое наименование:** Stets Home System  
**Код проекта:** STETS-HOME-ARCH-001

### 1.2 Назначение системы
Система предназначена для централизованного управления умными устройствами дома через мобильное приложение, обеспечивая:
- Удаленное управление устройствами (лампочки, розетки)
- Автоматизацию через сценарии с расписанием
- Совместный доступ для членов семьи
- Мониторинг состояния устройств и энергопотребления

### 1.3 Область применения
- Частные дома и квартиры
- Офисные помещения
- Образовательные учреждения
- Малый бизнес

## 2. Архитектура системы

### 2.1 Общая архитектура

Система построена по принципу **клиент-сервер** с микросервисной архитектурой:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App    │    │   Web Portal    │    │  Admin Panel   │
│  (iOS/Android)  │    │   (Optional)    │    │   (Future)     │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴─────────────┐
                    │      API Gateway          │
                    │   (Authentication,        │
                    │    Rate Limiting,          │
                    │    Load Balancing)        │
                    └─────────────┬─────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
┌───────┴────────┐    ┌───────────┴──────────┐    ┌────────┴────────┐
│  Auth Service  │    │   Device Service     │    │ Scenario Service│
│  (JWT, OAuth)  │    │  (Device Control,   │    │ (Automation,    │
│                │    │   Status Sync)      │    │  Scheduling)   │
└───────┬────────┘    └───────────┬──────────┘    └────────┬────────┘
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │     Database Layer         │
                    │  (PostgreSQL + Redis)      │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │     IoT Integration       │
                    │  (MQTT Broker, Device     │
                    │   Communication)          │
                    └───────────────────────────┘
```

### 2.2 Компоненты системы

#### 2.2.1 Клиентские приложения
**Mobile App (iOS/Android)**
- **Технология:** React Native или Flutter
- **Функции:** Основной интерфейс пользователя
- **Особенности:** Offline режим, push-уведомления, биометрия

**Web Portal (Optional)**
- **Технология:** React.js или Vue.js
- **Функции:** Дополнительный веб-интерфейс
- **Особенности:** Адаптивный дизайн, PWA

#### 2.2.2 Серверные компоненты
**API Gateway**
- **Технология:** Kong или AWS API Gateway
- **Функции:** Маршрутизация, аутентификация, rate limiting
- **Особенности:** SSL termination, мониторинг

**Auth Service**
- **Технология:** Node.js + Express или Python + FastAPI
- **Функции:** Аутентификация, авторизация, управление пользователями
- **Особенности:** JWT токены, OAuth 2.0, refresh tokens

**Device Service**
- **Технология:** Node.js + Express или Go
- **Функции:** Управление устройствами, синхронизация статуса
- **Особенности:** WebSocket соединения, real-time updates

**Scenario Service**
- **Технология:** Node.js + Express или Python + Celery
- **Функции:** Создание и выполнение сценариев, планировщик
- **Особенности:** Cron jobs, event-driven architecture

**Notification Service**
- **Технология:** Node.js + Express
- **Функции:** Email, push, SMS уведомления
- **Особенности:** Queue-based processing, templates

#### 2.2.3 Слой данных
**PostgreSQL**
- **Назначение:** Основная реляционная база данных
- **Содержит:** Пользователи, дома, устройства, сценарии
- **Особенности:** ACID транзакции, репликация

**Redis**
- **Назначение:** Кэширование и сессии
- **Содержит:** JWT токены, кэш данных, очереди
- **Особенности:** In-memory storage, pub/sub

**InfluxDB (Optional)**
- **Назначение:** Временные ряды данных
- **Содержит:** Метрики устройств, логи событий
- **Особенности:** Time-series optimization

#### 2.2.4 IoT Integration
**MQTT Broker**
- **Технология:** Eclipse Mosquitto или AWS IoT Core
- **Функции:** Коммуникация с устройствами
- **Особенности:** QoS levels, retained messages

**Device Gateway**
- **Технология:** Node.js или Python
- **Функции:** Протокол адаптация, device discovery
- **Особенности:** Protocol translation, device management

## 3. Детальная архитектура компонентов

### 3.1 Mobile App Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Mobile App Layer                     │
├─────────────────────────────────────────────────────────┤
│  Presentation Layer (UI Components)                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │   Screens   │ │ Components  │ │ Navigation  │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
├─────────────────────────────────────────────────────────┤
│  Business Logic Layer                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │   Stores    │ │  Services   │ │  Utils       │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
├─────────────────────────────────────────────────────────┤
│  Data Layer                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │   API       │ │ Local Cache │ │ Offline DB  │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘
```

**Ключевые компоненты:**
- **State Management:** Redux или MobX для управления состоянием
- **API Client:** Axios или Fetch для HTTP запросов
- **Local Storage:** SQLite или Realm для offline данных
- **Push Notifications:** Firebase Cloud Messaging
- **Biometric Auth:** Touch ID / Face ID интеграция

### 3.2 Backend Services Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Backend Services                        │
├─────────────────────────────────────────────────────────┤
│  API Gateway (Kong/AWS API Gateway)                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │   Auth      │ │ Rate Limit  │ │ Monitoring  │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
├─────────────────────────────────────────────────────────┤
│  Microservices Layer                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │Auth Service │ │Device Svc   │ │Scenario Svc │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │Notification │ │Analytics    │ │File Storage │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
├─────────────────────────────────────────────────────────┤
│  Data Access Layer                                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │PostgreSQL   │ │   Redis     │ │  InfluxDB   │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘
```

**Паттерны архитектуры:**
- **Microservices:** Независимые сервисы с собственными БД
- **Event-Driven:** Асинхронная коммуникация через события
- **CQRS:** Разделение команд и запросов
- **Circuit Breaker:** Обработка отказов сервисов

### 3.3 IoT Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│                IoT Integration Layer                     │
├─────────────────────────────────────────────────────────┤
│  Device Communication                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │MQTT Broker  │ │CoAP Gateway │ │HTTP Gateway │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
├─────────────────────────────────────────────────────────┤
│  Protocol Translation                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │Stets Protocol│ │Zigbee      │ │WiFi Direct  │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
├─────────────────────────────────────────────────────────┤
│  Device Management                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │Discovery    │ │Provisioning │ │Monitoring   │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘
```

## 4. Протоколы и интерфейсы

### 4.1 API Endpoints

#### 4.1.1 Authentication API
```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/refresh
POST /api/auth/logout
POST /api/auth/forgot-password
POST /api/auth/reset-password
```

#### 4.1.2 User Management API
```
GET    /api/users/profile
PUT    /api/users/profile
PUT    /api/users/email
PUT    /api/users/password
DELETE /api/users/account
```

#### 4.1.3 Home Management API
```
GET    /api/homes
POST   /api/homes
GET    /api/homes/{id}
PUT    /api/homes/{id}
DELETE /api/homes/{id}
POST   /api/homes/{id}/members
PUT    /api/homes/{id}/members/{userId}
DELETE /api/homes/{id}/members/{userId}
```

#### 4.1.4 Device Management API
```
GET    /api/homes/{homeId}/devices
POST   /api/homes/{homeId}/devices
GET    /api/devices/{id}
PUT    /api/devices/{id}
DELETE /api/devices/{id}
POST   /api/devices/{id}/control
GET    /api/devices/{id}/status
```

#### 4.1.5 Scenario Management API
```
GET    /api/homes/{homeId}/scenarios
POST   /api/homes/{homeId}/scenarios
GET    /api/scenarios/{id}
PUT    /api/scenarios/{id}
DELETE /api/scenarios/{id}
POST   /api/scenarios/{id}/execute
PUT    /api/scenarios/{id}/schedule
```

### 4.2 WebSocket Events

#### 4.2.1 Device Events
```json
{
  "type": "device.status.changed",
  "data": {
    "deviceId": "123456789012",
    "status": "on",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

#### 4.2.2 Scenario Events
```json
{
  "type": "scenario.executed",
  "data": {
    "scenarioId": 456,
    "status": "success",
    "executedAt": "2024-01-15T10:30:00Z"
  }
}
```

### 4.3 MQTT Topics

#### 4.3.1 Device Control Topics
```
stets/home/{homeId}/device/{deviceId}/command
stets/home/{homeId}/device/{deviceId}/status
stets/home/{homeId}/device/{deviceId}/energy
```

#### 4.3.2 System Topics
```
stets/home/{homeId}/system/heartbeat
stets/home/{homeId}/system/error
stets/home/{homeId}/system/discovery
```

## 5. Безопасность системы

### 5.1 Аутентификация и авторизация

#### 5.1.1 JWT Token Strategy
```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user123",
    "iat": 1642248000,
    "exp": 1642251600,
    "homeId": "home456",
    "role": "owner"
  }
}
```

#### 5.1.2 Role-Based Access Control (RBAC)
- **Owner:** Полный доступ к дому и всем функциям
- **Member:** Ограниченный доступ к управлению устройствами
- **Guest:** Только просмотр статуса устройств

### 5.2 Сетевая безопасность

#### 5.2.1 Transport Security
- **HTTPS:** Все API запросы через TLS 1.3
- **WSS:** WebSocket соединения через TLS
- **MQTTS:** MQTT соединения через TLS

#### 5.2.2 API Security
- **Rate Limiting:** 1000 запросов в час на пользователя
- **CORS:** Настроенные домены для веб-клиентов
- **Input Validation:** Валидация всех входящих данных
- **SQL Injection Protection:** Prepared statements

### 5.3 IoT Security

#### 5.3.1 Device Authentication
- **Device Certificates:** X.509 сертификаты для устройств
- **Unique Device Codes:** 12-значные коды для идентификации
- **Secure Pairing:** QR-коды для безопасного добавления

#### 5.3.2 Network Security
- **VPN:** Защищенный туннель для IoT коммуникации
- **Firewall:** Правила для блокировки нежелательного трафика
- **Intrusion Detection:** Мониторинг подозрительной активности

## 6. Масштабируемость и производительность

### 6.1 Горизонтальное масштабирование

#### 6.1.1 Load Balancing
- **Application Load Balancer:** Распределение нагрузки между сервисами
- **Database Sharding:** Горизонтальное разделение данных по домам
- **CDN:** Кэширование статических ресурсов

#### 6.1.2 Auto Scaling
- **Kubernetes HPA:** Автоматическое масштабирование подов
- **Database Scaling:** Read replicas для запросов
- **Cache Scaling:** Redis Cluster для кэширования

### 6.2 Оптимизация производительности

#### 6.2.1 Caching Strategy
- **Application Cache:** Redis для часто используемых данных
- **Database Cache:** Query result caching
- **CDN Cache:** Статические ресурсы и API ответы

#### 6.2.2 Database Optimization
- **Indexing:** Оптимизированные индексы для запросов
- **Connection Pooling:** Пул соединений к БД
- **Query Optimization:** Оптимизированные SQL запросы

## 7. Мониторинг и логирование

### 7.1 Application Monitoring

#### 7.1.1 Metrics Collection
- **Prometheus:** Сбор метрик производительности
- **Grafana:** Визуализация метрик и дашборды
- **Custom Metrics:** Бизнес-метрики (активные пользователи, устройства)

#### 7.1.2 Health Checks
- **Service Health:** Проверка состояния всех сервисов
- **Database Health:** Мониторинг подключений к БД
- **External Dependencies:** Проверка внешних сервисов

### 7.2 Logging Strategy

#### 7.2.1 Centralized Logging
- **ELK Stack:** Elasticsearch, Logstash, Kibana
- **Structured Logging:** JSON формат логов
- **Log Levels:** DEBUG, INFO, WARN, ERROR, FATAL

#### 7.2.2 Security Logging
- **Authentication Events:** Логи входов и выходов
- **Authorization Events:** Логи доступа к ресурсам
- **Security Incidents:** Логи подозрительной активности

## 8. Развертывание и DevOps

### 8.1 Containerization

#### 8.1.1 Docker Containers
```dockerfile
# Example Dockerfile for API service
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

#### 8.1.2 Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stets-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: stets-api
  template:
    metadata:
      labels:
        app: stets-api
    spec:
      containers:
      - name: api
        image: stets/api:latest
        ports:
        - containerPort: 3000
```

### 8.2 CI/CD Pipeline

#### 8.2.1 Continuous Integration
- **Code Quality:** ESLint, Prettier, SonarQube
- **Testing:** Unit tests, Integration tests, E2E tests
- **Security Scanning:** OWASP dependency check, SAST

#### 8.2.2 Continuous Deployment
- **Blue-Green Deployment:** Безопасное развертывание
- **Feature Flags:** Управление функциональностью
- **Rollback Strategy:** Быстрый откат при проблемах

## 9. Резервное копирование и восстановление

### 9.1 Backup Strategy

#### 9.1.1 Database Backups
- **Daily Full Backups:** Полное резервное копирование
- **Hourly Incremental:** Инкрементальные копии
- **Point-in-Time Recovery:** Восстановление на момент времени

#### 9.1.2 Application Backups
- **Configuration Backups:** Резервное копирование конфигураций
- **Code Repository:** Git с удаленными репозиториями
- **Infrastructure as Code:** Terraform для инфраструктуры

### 9.2 Disaster Recovery

#### 9.2.1 RTO/RPO Targets
- **RTO (Recovery Time Objective):** 4 часа
- **RPO (Recovery Point Objective):** 1 час
- **Multi-Region:** Развертывание в нескольких регионах

#### 9.2.2 Recovery Procedures
- **Automated Recovery:** Автоматическое восстановление сервисов
- **Manual Procedures:** Ручные процедуры для критических ситуаций
- **Testing:** Регулярное тестирование процедур восстановления

## 10. Заключение

Предложенная архитектура обеспечивает:

### 10.1 Преимущества
- **Масштабируемость:** Горизонтальное масштабирование компонентов
- **Надежность:** Высокая доступность и отказоустойчивость
- **Безопасность:** Многоуровневая система защиты
- **Производительность:** Оптимизированные запросы и кэширование
- **Гибкость:** Микросервисная архитектура для независимого развития

### 10.2 Технологический стек
- **Frontend:** React Native / Flutter
- **Backend:** Node.js / Python / Go
- **Database:** PostgreSQL + Redis
- **IoT:** MQTT + WebSocket
- **Infrastructure:** Kubernetes + Docker
- **Monitoring:** Prometheus + Grafana

### 10.3 Следующие шаги
1. **Детальное проектирование** каждого сервиса
2. **Создание прототипов** ключевых компонентов
3. **Настройка инфраструктуры** разработки
4. **Начало разработки** MVP версии

---

**Дата создания:** [Текущая дата]  
**Версия:** 1.0  
**Статус:** Утвержден
