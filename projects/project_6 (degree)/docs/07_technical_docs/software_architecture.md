# Проект системы (программное обеспечение) Stets Home

## 1. Общие сведения

### 1.1 Наименование системы
**Полное наименование:** Проект программного обеспечения системы управления умным домом Stets Home  
**Краткое наименование:** Stets Home Software  
**Код проекта:** STETS-HOME-SOFTWARE-001

### 1.2 Назначение проекта
Проект определяет архитектуру, технологии и подходы к разработке программного обеспечения для системы управления умным домом, включая:
- Мобильное приложение для пользователей
- Backend сервисы для обработки данных
- IoT интеграцию для работы с устройствами
- Системы безопасности и мониторинга

### 1.3 Принципы разработки
- **Microservices Architecture:** Модульная архитектура сервисов
- **API-First Design:** Приоритет API в разработке
- **Cloud-Native:** Развертывание в облачной среде
- **DevOps Integration:** Интеграция разработки и эксплуатации
- **Security by Design:** Безопасность на всех уровнях

## 2. Архитектура программного обеспечения

### 2.1 Общая архитектура системы

```mermaid
graph TB
    %% Client Layer
    subgraph "Client Layer"
        MobileApp["📱 Mobile App<br/>(React Native)"]
        WebApp["🌐 Web App<br/>(React.js)"]
        AdminPanel["⚙️ Admin Panel<br/>(Vue.js)"]
    end
    
    %% API Gateway
    subgraph "API Gateway"
        Gateway["🚪 API Gateway<br/>(Kong/AWS)"]
        Auth["🔐 Authentication<br/>(JWT/OAuth)"]
        RateLimit["⏱️ Rate Limiting"]
        Monitoring["📊 Monitoring"]
    end
    
    %% Microservices Layer
    subgraph "Microservices"
        UserService["👤 User Service<br/>(Node.js)"]
        DeviceService["🔌 Device Service<br/>(Go)"]
        ScenarioService["🤖 Scenario Service<br/>(Python)"]
        NotificationService["📧 Notification Service<br/>(Node.js)"]
        AnalyticsService["📈 Analytics Service<br/>(Python)"]
    end
    
    %% Data Layer
    subgraph "Data Layer"
        PostgreSQL["🗄️ PostgreSQL<br/>(Primary DB)"]
        Redis["⚡ Redis<br/>(Cache/Sessions)"]
        InfluxDB["📊 InfluxDB<br/>(Time Series)"]
        S3["☁️ S3<br/>(File Storage)"]
    end
    
    %% IoT Integration
    subgraph "IoT Integration"
        MQTTBroker["📡 MQTT Broker<br/>(Eclipse Mosquitto)"]
        DeviceGateway["🔗 Device Gateway<br/>(Node.js)"]
        ProtocolAdapter["🔄 Protocol Adapter"]
    end
    
    %% External Services
    subgraph "External Services"
        EmailService["📧 Email Service<br/>(SendGrid)"]
        PushService["📱 Push Service<br/>(FCM)"]
        SMSService["📱 SMS Service<br/>(Twilio)"]
    end
    
    %% Connections
    MobileApp --> Gateway
    WebApp --> Gateway
    AdminPanel --> Gateway
    
    Gateway --> Auth
    Gateway --> RateLimit
    Gateway --> Monitoring
    
    Gateway --> UserService
    Gateway --> DeviceService
    Gateway --> ScenarioService
    Gateway --> NotificationService
    Gateway --> AnalyticsService
    
    UserService --> PostgreSQL
    UserService --> Redis
    DeviceService --> PostgreSQL
    DeviceService --> Redis
    ScenarioService --> PostgreSQL
    ScenarioService --> Redis
    NotificationService --> Redis
    AnalyticsService --> InfluxDB
    
    DeviceService --> MQTTBroker
    DeviceGateway --> MQTTBroker
    DeviceGateway --> ProtocolAdapter
    
    NotificationService --> EmailService
    NotificationService --> PushService
    NotificationService --> SMSService
    
    %% Styling
    classDef client fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef gateway fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef service fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef data fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef iot fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef external fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    
    class MobileApp,WebApp,AdminPanel client
    class Gateway,Auth,RateLimit,Monitoring gateway
    class UserService,DeviceService,ScenarioService,NotificationService,AnalyticsService service
    class PostgreSQL,Redis,InfluxDB,S3 data
    class MQTTBroker,DeviceGateway,ProtocolAdapter iot
    class EmailService,PushService,SMSService external
```

### 2.2 Технологический стек

#### 2.2.1 Frontend (Клиентские приложения)
**Mobile App (React Native)**
- **Framework:** React Native 0.72+
- **State Management:** Redux Toolkit + RTK Query
- **Navigation:** React Navigation 6
- **UI Components:** React Native Elements
- **Charts:** Victory Native
- **Push Notifications:** React Native Firebase
- **Biometric Auth:** React Native Touch ID / Face ID

**Web App (React.js)**
- **Framework:** React 18 + TypeScript
- **State Management:** Redux Toolkit + RTK Query
- **Routing:** React Router 6
- **UI Framework:** Material-UI (MUI)
- **Charts:** Chart.js / Recharts
- **PWA:** Workbox

**Admin Panel (Vue.js)**
- **Framework:** Vue 3 + TypeScript
- **State Management:** Pinia
- **UI Framework:** Vuetify 3
- **Charts:** Chart.js
- **Tables:** Vue Good Table

#### 2.2.2 Backend (Серверные сервисы)
**API Gateway**
- **Technology:** Kong / AWS API Gateway
- **Authentication:** JWT + OAuth 2.0
- **Rate Limiting:** Redis-based
- **Monitoring:** Prometheus + Grafana

**User Service (Node.js)**
- **Runtime:** Node.js 18+ LTS
- **Framework:** Express.js + TypeScript
- **ORM:** Prisma
- **Validation:** Joi / Zod
- **Testing:** Jest + Supertest

**Device Service (Go)**
- **Language:** Go 1.21+
- **Framework:** Gin / Fiber
- **ORM:** GORM
- **Validation:** go-playground/validator
- **Testing:** Testify

**Scenario Service (Python)**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Task Queue:** Celery + Redis
- **Scheduler:** APScheduler
- **Testing:** Pytest

**Notification Service (Node.js)**
- **Runtime:** Node.js 18+ LTS
- **Framework:** Express.js + TypeScript
- **Queue:** Bull Queue + Redis
- **Templates:** Handlebars
- **Testing:** Jest

**Analytics Service (Python)**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Data Processing:** Pandas + NumPy
- **ML Libraries:** Scikit-learn
- **Visualization:** Matplotlib + Seaborn

#### 2.2.3 Data Layer
**PostgreSQL**
- **Version:** PostgreSQL 15+
- **Extensions:** pgcrypto, pg_stat_statements
- **Connection Pooling:** PgBouncer
- **Backup:** pg_dump + WAL-E

**Redis**
- **Version:** Redis 7+
- **Clustering:** Redis Cluster
- **Persistence:** RDB + AOF
- **Modules:** RedisJSON, RedisSearch

**InfluxDB**
- **Version:** InfluxDB 2.7+
- **Retention:** 90 days for metrics
- **Compression:** Snappy
- **Queries:** Flux language

#### 2.2.4 IoT Integration
**MQTT Broker**
- **Broker:** Eclipse Mosquitto 2.0+
- **Security:** TLS 1.3 + Client Certificates
- **Persistence:** File-based
- **Bridge:** MQTT Bridge for clustering

**Device Gateway**
- **Runtime:** Node.js 18+ LTS
- **MQTT Client:** mqtt.js
- **Protocol Support:** Stets Protocol, Zigbee, WiFi Direct
- **Device Discovery:** mDNS + SSDP

#### 2.2.5 Infrastructure
**Containerization**
- **Container Runtime:** Docker 24+
- **Orchestration:** Kubernetes 1.28+
- **Service Mesh:** Istio (optional)
- **Ingress:** NGINX Ingress Controller

**CI/CD**
- **Version Control:** Git (GitHub/GitLab)
- **CI/CD:** GitHub Actions / GitLab CI
- **Container Registry:** Docker Hub / AWS ECR
- **Deployment:** ArgoCD / Flux

**Monitoring & Observability**
- **Metrics:** Prometheus + Grafana
- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing:** Jaeger / Zipkin
- **APM:** New Relic / DataDog

## 3. Детальная архитектура сервисов

### 3.1 User Service

#### 3.1.1 Назначение
Управление пользователями, аутентификацией, авторизацией и профилями.

#### 3.1.2 API Endpoints
```typescript
// Authentication
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/refresh
POST   /api/auth/logout
POST   /api/auth/forgot-password
POST   /api/auth/reset-password
POST   /api/auth/verify-email

// User Management
GET    /api/users/profile
PUT    /api/users/profile
PUT    /api/users/email
PUT    /api/users/password
DELETE /api/users/account
GET    /api/users/homes
```

#### 3.1.3 Структура проекта
```
user-service/
├── src/
│   ├── controllers/
│   │   ├── auth.controller.ts
│   │   └── user.controller.ts
│   ├── services/
│   │   ├── auth.service.ts
│   │   ├── user.service.ts
│   │   └── email.service.ts
│   ├── models/
│   │   ├── user.model.ts
│   │   └── session.model.ts
│   ├── middleware/
│   │   ├── auth.middleware.ts
│   │   ├── validation.middleware.ts
│   │   └── rate-limit.middleware.ts
│   ├── routes/
│   │   ├── auth.routes.ts
│   │   └── user.routes.ts
│   ├── utils/
│   │   ├── jwt.util.ts
│   │   ├── bcrypt.util.ts
│   │   └── validation.util.ts
│   └── app.ts
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── prisma/
│   ├── schema.prisma
│   └── migrations/
├── package.json
└── Dockerfile
```

#### 3.1.4 Ключевые компоненты

**Auth Controller:**
```typescript
export class AuthController {
  async register(req: Request, res: Response) {
    const { email, password, name } = req.body;
    
    // Валидация данных
    const validation = await this.validateRegistration(email, password, name);
    if (!validation.isValid) {
      return res.status(400).json({ errors: validation.errors });
    }
    
    // Проверка существования пользователя
    const existingUser = await this.userService.findByEmail(email);
    if (existingUser) {
      return res.status(409).json({ error: 'User already exists' });
    }
    
    // Создание пользователя
    const user = await this.userService.create({
      email,
      password,
      name
    });
    
    // Создание первого дома
    const home = await this.homeService.createFirstHome(user.id);
    
    // Отправка email подтверждения
    await this.emailService.sendVerificationEmail(user.email, user.verificationToken);
    
    // Генерация JWT токенов
    const tokens = await this.authService.generateTokens(user);
    
    res.status(201).json({
      user: this.sanitizeUser(user),
      tokens,
      home
    });
  }
  
  async login(req: Request, res: Response) {
    const { email, password } = req.body;
    
    // Поиск пользователя
    const user = await this.userService.findByEmail(email);
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Проверка пароля
    const isValidPassword = await this.authService.verifyPassword(password, user.passwordHash);
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Обновление последнего входа
    await this.userService.updateLastLogin(user.id);
    
    // Генерация токенов
    const tokens = await this.authService.generateTokens(user);
    
    res.json({
      user: this.sanitizeUser(user),
      tokens
    });
  }
}
```

**User Service:**
```typescript
export class UserService {
  constructor(
    private prisma: PrismaClient,
    private bcrypt: BcryptService,
    private emailService: EmailService
  ) {}
  
  async create(userData: CreateUserDto): Promise<User> {
    const { email, password, name } = userData;
    
    // Хэширование пароля
    const passwordHash = await this.bcrypt.hash(password, 12);
    
    // Генерация токена подтверждения email
    const verificationToken = crypto.randomBytes(32).toString('hex');
    
    // Создание пользователя
    const user = await this.prisma.user.create({
      data: {
        email,
        passwordHash,
        name,
        emailVerificationToken: verificationToken,
        emailVerified: false
      }
    });
    
    return user;
  }
  
  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { email }
    });
  }
  
  async updateLastLogin(userId: number): Promise<void> {
    await this.prisma.user.update({
      where: { id: userId },
      data: { lastLogin: new Date() }
    });
  }
  
  async verifyEmail(token: string): Promise<boolean> {
    const user = await this.prisma.user.findFirst({
      where: { emailVerificationToken: token }
    });
    
    if (!user) {
      return false;
    }
    
    await this.prisma.user.update({
      where: { id: user.id },
      data: {
        emailVerified: true,
        emailVerificationToken: null
      }
    });
    
    return true;
  }
}
```

### 3.2 Device Service

#### 3.2.1 Назначение
Управление умными устройствами, их статусом, командами и синхронизацией.

#### 3.2.2 API Endpoints
```typescript
// Device Management
GET    /api/homes/{homeId}/devices
POST   /api/homes/{homeId}/devices
GET    /api/devices/{deviceId}
PUT    /api/devices/{deviceId}
DELETE /api/devices/{deviceId}

// Device Control
POST   /api/devices/{deviceId}/control
GET    /api/devices/{deviceId}/status
POST   /api/devices/{deviceId}/energy-saving
GET    /api/devices/{deviceId}/history

// Device Discovery
POST   /api/devices/discover
GET    /api/devices/available
POST   /api/devices/pair
```

#### 3.2.3 Структура проекта
```
device-service/
├── src/
│   ├── controllers/
│   │   ├── device.controller.ts
│   │   └── discovery.controller.ts
│   ├── services/
│   │   ├── device.service.ts
│   │   ├── mqtt.service.ts
│   │   └── protocol.service.ts
│   ├── models/
│   │   ├── device.model.ts
│   │   └── command.model.ts
│   ├── middleware/
│   │   ├── auth.middleware.ts
│   │   └── validation.middleware.ts
│   ├── routes/
│   │   ├── device.routes.ts
│   │   └── discovery.routes.ts
│   ├── utils/
│   │   ├── mqtt.util.ts
│   │   └── protocol.util.ts
│   └── app.go
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── go.mod
├── go.sum
└── Dockerfile
```

#### 3.2.4 Ключевые компоненты

**Device Controller:**
```go
type DeviceController struct {
    deviceService *services.DeviceService
    mqttService   *services.MQTTService
    authService   *services.AuthService
}

func (dc *DeviceController) AddDevice(c *gin.Context) {
    homeID, err := strconv.Atoi(c.Param("homeId"))
    if err != nil {
        c.JSON(400, gin.H{"error": "Invalid home ID"})
        return
    }
    
    var req AddDeviceRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    
    // Валидация кода устройства
    if !dc.validateDeviceCode(req.DeviceCode) {
        c.JSON(400, gin.H{"error": "Invalid device code format"})
        return
    }
    
    // Проверка уникальности
    exists, err := dc.deviceService.DeviceExists(req.DeviceCode)
    if err != nil {
        c.JSON(500, gin.H{"error": "Internal server error"})
        return
    }
    if exists {
        c.JSON(409, gin.H{"error": "Device already exists"})
        return
    }
    
    // Создание устройства
    device, err := dc.deviceService.CreateDevice(homeID, req)
    if err != nil {
        c.JSON(500, gin.H{"error": "Failed to create device"})
        return
    }
    
    // Подключение к MQTT
    err = dc.mqttService.SubscribeToDevice(device.DeviceCode)
    if err != nil {
        // Логирование ошибки, но не прерывание процесса
        log.Printf("Failed to subscribe to device %s: %v", device.DeviceCode, err)
    }
    
    c.JSON(201, gin.H{"device": device})
}

func (dc *DeviceController) ControlDevice(c *gin.Context) {
    deviceID, err := strconv.Atoi(c.Param("deviceId"))
    if err != nil {
        c.JSON(400, gin.H{"error": "Invalid device ID"})
        return
    }
    
    var req ControlDeviceRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    
    // Получение устройства
    device, err := dc.deviceService.GetDevice(deviceID)
    if err != nil {
        c.JSON(404, gin.H{"error": "Device not found"})
        return
    }
    
    // Отправка команды через MQTT
    command := &models.DeviceCommand{
        DeviceCode: device.DeviceCode,
        Action:     req.Action,
        Params:     req.Params,
        Timestamp:  time.Now(),
    }
    
    err = dc.mqttService.PublishCommand(command)
    if err != nil {
        c.JSON(500, gin.H{"error": "Failed to send command"})
        return
    }
    
    // Обновление статуса в БД
    err = dc.deviceService.UpdateDeviceStatus(deviceID, req.Action, req.Params)
    if err != nil {
        log.Printf("Failed to update device status: %v", err)
    }
    
    c.JSON(200, gin.H{"message": "Command sent successfully"})
}
```

**MQTT Service:**
```go
type MQTTService struct {
    client mqtt.Client
    deviceService *services.DeviceService
}

func (ms *MQTTService) PublishCommand(command *models.DeviceCommand) error {
    topic := fmt.Sprintf("stets/home/device/%s/command", command.DeviceCode)
    
    payload, err := json.Marshal(command)
    if err != nil {
        return fmt.Errorf("failed to marshal command: %w", err)
    }
    
    token := ms.client.Publish(topic, 1, false, payload)
    if token.Wait() && token.Error() != nil {
        return fmt.Errorf("failed to publish command: %w", token.Error())
    }
    
    return nil
}

func (ms *MQTTService) SubscribeToDevice(deviceCode string) error {
    topic := fmt.Sprintf("stets/home/device/%s/status", deviceCode)
    
    token := ms.client.Subscribe(topic, 1, ms.handleDeviceStatus)
    if token.Wait() && token.Error() != nil {
        return fmt.Errorf("failed to subscribe to device: %w", token.Error())
    }
    
    return nil
}

func (ms *MQTTService) handleDeviceStatus(client mqtt.Client, msg mqtt.Message) {
    var status models.DeviceStatus
    if err := json.Unmarshal(msg.Payload(), &status); err != nil {
        log.Printf("Failed to unmarshal device status: %v", err)
        return
    }
    
    // Обновление статуса в БД
    err := ms.deviceService.UpdateDeviceStatusFromMQTT(status)
    if err != nil {
        log.Printf("Failed to update device status from MQTT: %v", err)
    }
    
    // Отправка WebSocket уведомления клиентам
    ms.broadcastDeviceStatus(status)
}
```

### 3.3 Scenario Service

#### 3.3.1 Назначение
Управление сценариями автоматизации, их расписанием и выполнением.

#### 3.3.2 API Endpoints
```typescript
// Scenario Management
GET    /api/homes/{homeId}/scenarios
POST   /api/homes/{homeId}/scenarios
GET    /api/scenarios/{scenarioId}
PUT    /api/scenarios/{scenarioId}
DELETE /api/scenarios/{scenarioId}

// Scenario Execution
POST   /api/scenarios/{scenarioId}/execute
POST   /api/scenarios/{scenarioId}/stop
GET    /api/scenarios/{scenarioId}/status

// Scenario Scheduling
PUT    /api/scenarios/{scenarioId}/schedule
GET    /api/scenarios/{scenarioId}/schedule
DELETE /api/scenarios/{scenarioId}/schedule
```

#### 3.3.3 Структура проекта
```
scenario-service/
├── src/
│   ├── controllers/
│   │   ├── scenario.controller.py
│   │   └── execution.controller.py
│   ├── services/
│   │   ├── scenario.service.py
│   │   ├── scheduler.service.py
│   │   └── execution.service.py
│   ├── models/
│   │   ├── scenario.model.py
│   │   ├── schedule.model.py
│   │   └── action.model.py
│   ├── tasks/
│   │   ├── execute_scenario.py
│   │   └── schedule_scenario.py
│   ├── middleware/
│   │   ├── auth.py
│   │   └── validation.py
│   ├── routes/
│   │   ├── scenario.routes.py
│   │   └── execution.routes.py
│   ├── utils/
│   │   ├── scheduler.py
│   │   └── validator.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── requirements.txt
└── Dockerfile
```

#### 3.3.4 Ключевые компоненты

**Scenario Service:**
```python
class ScenarioService:
    def __init__(self, db: Session, scheduler: APScheduler, device_service: DeviceService):
        self.db = db
        self.scheduler = scheduler
        self.device_service = device_service
    
    async def create_scenario(self, home_id: int, scenario_data: CreateScenarioDto) -> Scenario:
        """Создание нового сценария"""
        # Создание сценария
        scenario = Scenario(
            home_id=home_id,
            name=scenario_data.name,
            description=scenario_data.description,
            created_by_user_id=scenario_data.user_id
        )
        
        self.db.add(scenario)
        self.db.flush()  # Получаем ID сценария
        
        # Создание действий
        for action_data in scenario_data.actions:
            action = ScenarioAction(
                scenario_id=scenario.id,
                device_id=action_data.device_id,
                action_type=action_data.action_type,
                action_params=action_data.params,
                execution_order=action_data.order
            )
            self.db.add(action)
        
        # Создание расписания (если указано)
        if scenario_data.schedule:
            schedule = ScenarioSchedule(
                scenario_id=scenario.id,
                monday=scenario_data.schedule.monday,
                tuesday=scenario_data.schedule.tuesday,
                wednesday=scenario_data.schedule.wednesday,
                thursday=scenario_data.schedule.thursday,
                friday=scenario_data.schedule.friday,
                saturday=scenario_data.schedule.saturday,
                sunday=scenario_data.schedule.sunday,
                start_time=scenario_data.schedule.start_time,
                end_time=scenario_data.schedule.end_time
            )
            self.db.add(schedule)
            
            # Добавление в планировщик
            self.schedule_scenario(scenario.id, schedule)
        
        self.db.commit()
        return scenario
    
    async def execute_scenario(self, scenario_id: int, user_id: int) -> ExecutionResult:
        """Выполнение сценария"""
        scenario = self.db.query(Scenario).filter(Scenario.id == scenario_id).first()
        if not scenario:
            raise ScenarioNotFoundError(f"Scenario {scenario_id} not found")
        
        # Получение действий сценария
        actions = self.db.query(ScenarioAction).filter(
            ScenarioAction.scenario_id == scenario_id
        ).order_by(ScenarioAction.execution_order).all()
        
        if not actions:
            raise ScenarioEmptyError(f"Scenario {scenario_id} has no actions")
        
        # Выполнение действий
        results = []
        for action in actions:
            try:
                result = await self.execute_action(action)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to execute action {action.id}: {e}")
                results.append(ActionResult(success=False, error=str(e)))
        
        # Обновление времени последнего выполнения
        scenario.last_executed = datetime.utcnow()
        self.db.commit()
        
        return ExecutionResult(
            scenario_id=scenario_id,
            executed_at=datetime.utcnow(),
            results=results,
            success=all(r.success for r in results)
        )
    
    async def execute_action(self, action: ScenarioAction) -> ActionResult:
        """Выполнение отдельного действия"""
        # Отправка команды устройству через Device Service
        command = DeviceCommand(
            device_id=action.device_id,
            action=action.action_type,
            params=action.action_params
        )
        
        try:
            result = await self.device_service.send_command(command)
            return ActionResult(success=True, result=result)
        except Exception as e:
            return ActionResult(success=False, error=str(e))
    
    def schedule_scenario(self, scenario_id: int, schedule: ScenarioSchedule):
        """Планирование сценария"""
        # Создание cron выражения для дней недели
        days = []
        if schedule.monday: days.append(1)
        if schedule.tuesday: days.append(2)
        if schedule.wednesday: days.append(3)
        if schedule.thursday: days.append(4)
        if schedule.friday: days.append(5)
        if schedule.saturday: days.append(6)
        if schedule.sunday: days.append(0)
        
        if not days:
            return
        
        # Создание cron выражения
        cron_expr = f"{schedule.start_time.minute} {schedule.start_time.hour} * * {','.join(map(str, days))}"
        
        # Добавление задачи в планировщик
        self.scheduler.add_job(
            func=self.execute_scenario,
            trigger='cron',
            args=[scenario_id],
            id=f"scenario_{scenario_id}",
            replace_existing=True,
            cron=cron_expr
        )
```

**Scheduler Service:**
```python
class SchedulerService:
    def __init__(self):
        self.scheduler = APScheduler()
        self.scheduler.start()
    
    def add_scenario_schedule(self, scenario_id: int, schedule: ScheduleDto):
        """Добавление расписания сценария"""
        job_id = f"scenario_{scenario_id}"
        
        # Удаление существующего расписания
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)
        
        # Создание cron выражения
        cron_expr = self.create_cron_expression(schedule)
        
        # Добавление задачи
        self.scheduler.add_job(
            func=self.execute_scenario_task,
            trigger='cron',
            args=[scenario_id],
            id=job_id,
            cron=cron_expr,
            replace_existing=True
        )
    
    def create_cron_expression(self, schedule: ScheduleDto) -> str:
        """Создание cron выражения из расписания"""
        days = []
        if schedule.monday: days.append(1)
        if schedule.tuesday: days.append(2)
        if schedule.wednesday: days.append(3)
        if schedule.thursday: days.append(4)
        if schedule.friday: days.append(5)
        if schedule.saturday: days.append(6)
        if schedule.sunday: days.append(0)
        
        if not days:
            raise ValueError("At least one day must be selected")
        
        # Формат: minute hour day month day_of_week
        cron_expr = f"{schedule.start_time.minute} {schedule.start_time.hour} * * {','.join(map(str, days))}"
        return cron_expr
    
    def execute_scenario_task(self, scenario_id: int):
        """Задача выполнения сценария"""
        # Асинхронное выполнение через Celery
        execute_scenario.delay(scenario_id)
```

### 3.4 Notification Service

#### 3.4.1 Назначение
Отправка уведомлений пользователям через различные каналы (email, push, SMS).

#### 3.4.2 API Endpoints
```typescript
// Notification Management
POST   /api/notifications/send
POST   /api/notifications/email
POST   /api/notifications/push
POST   /api/notifications/sms

// Notification Templates
GET    /api/notifications/templates
POST   /api/notifications/templates
PUT    /api/notifications/templates/{templateId}
DELETE /api/notifications/templates/{templateId}

// Notification Preferences
GET    /api/users/{userId}/notification-preferences
PUT    /api/users/{userId}/notification-preferences
```

#### 3.4.3 Структура проекта
```
notification-service/
├── src/
│   ├── controllers/
│   │   ├── notification.controller.ts
│   │   └── template.controller.ts
│   ├── services/
│   │   ├── notification.service.ts
│   │   ├── email.service.ts
│   │   ├── push.service.ts
│   │   └── sms.service.ts
│   ├── models/
│   │   ├── notification.model.ts
│   │   └── template.model.ts
│   ├── templates/
│   │   ├── email/
│   │   ├── push/
│   │   └── sms/
│   ├── queues/
│   │   ├── email.queue.ts
│   │   ├── push.queue.ts
│   │   └── sms.queue.ts
│   ├── middleware/
│   │   ├── auth.middleware.ts
│   │   └── validation.middleware.ts
│   ├── routes/
│   │   ├── notification.routes.ts
│   │   └── template.routes.ts
│   ├── utils/
│   │   ├── template.util.ts
│   │   └── queue.util.ts
│   └── app.ts
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── package.json
└── Dockerfile
```

#### 3.4.4 Ключевые компоненты

**Notification Service:**
```typescript
export class NotificationService {
  constructor(
    private emailService: EmailService,
    private pushService: PushService,
    private smsService: SMSService,
    private templateService: TemplateService,
    private queueService: QueueService
  ) {}
  
  async sendNotification(notification: SendNotificationDto): Promise<void> {
    const { userId, type, templateId, data, channels } = notification;
    
    // Получение шаблона
    const template = await this.templateService.getTemplate(templateId);
    if (!template) {
      throw new Error(`Template ${templateId} not found`);
    }
    
    // Получение предпочтений пользователя
    const preferences = await this.getUserPreferences(userId);
    
    // Определение каналов для отправки
    const targetChannels = channels.filter(channel => 
      preferences[channel] === true
    );
    
    // Отправка через каждый канал
    for (const channel of targetChannels) {
      await this.sendToChannel(channel, userId, template, data);
    }
  }
  
  private async sendToChannel(
    channel: NotificationChannel,
    userId: number,
    template: NotificationTemplate,
    data: any
  ): Promise<void> {
    switch (channel) {
      case 'email':
        await this.queueEmailNotification(userId, template, data);
        break;
      case 'push':
        await this.queuePushNotification(userId, template, data);
        break;
      case 'sms':
        await this.queueSMSNotification(userId, template, data);
        break;
    }
  }
  
  private async queueEmailNotification(
    userId: number,
    template: NotificationTemplate,
    data: any
  ): Promise<void> {
    const job = await this.queueService.addEmailJob({
      userId,
      templateId: template.id,
      data,
      priority: 'normal'
    });
    
    // Логирование
    this.logger.info(`Email notification queued for user ${userId}`, {
      jobId: job.id,
      templateId: template.id
    });
  }
}
```

**Email Service:**
```typescript
export class EmailService {
  constructor(
    private sendGridClient: SendGrid,
    private templateEngine: Handlebars
  ) {}
  
  async sendEmail(emailData: EmailData): Promise<void> {
    const { to, templateId, data, subject } = emailData;
    
    // Получение шаблона
    const template = await this.getEmailTemplate(templateId);
    
    // Компиляция шаблона
    const htmlContent = this.templateEngine.compile(template.html)(data);
    const textContent = this.templateEngine.compile(template.text)(data);
    
    // Создание сообщения
    const msg = {
      to: to,
      from: {
        email: 'noreply@stets-home.com',
        name: 'Stets Home'
      },
      subject: subject || template.subject,
      html: htmlContent,
      text: textContent
    };
    
    try {
      await this.sendGridClient.send(msg);
      this.logger.info(`Email sent successfully to ${to}`);
    } catch (error) {
      this.logger.error(`Failed to send email to ${to}:`, error);
      throw new Error('Failed to send email');
    }
  }
  
  async sendVerificationEmail(email: string, token: string): Promise<void> {
    await this.sendEmail({
      to: email,
      templateId: 'email-verification',
      data: {
        verificationLink: `${process.env.APP_URL}/verify-email?token=${token}`,
        appName: 'Stets Home'
      },
      subject: 'Подтвердите ваш email'
    });
  }
  
  async sendPasswordResetEmail(email: string, token: string): Promise<void> {
    await this.sendEmail({
      to: email,
      templateId: 'password-reset',
      data: {
        resetLink: `${process.env.APP_URL}/reset-password?token=${token}`,
        appName: 'Stets Home'
      },
      subject: 'Восстановление пароля'
    });
  }
}
```

## 4. Интеграция и развертывание

### 4.1 Контейнеризация

#### 4.1.1 Docker конфигурация

**User Service Dockerfile:**
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM node:18-alpine AS runtime

WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
CMD ["npm", "start"]
```

**Device Service Dockerfile:**
```dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/

COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
```

**Scenario Service Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 4.1.2 Docker Compose для разработки
```yaml
version: '3.8'

services:
  # Databases
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: stets_home
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  influxdb:
    image: influxdb:2.7
    environment:
      DOCKER_INFLUXDB_INIT_MODE: setup
      DOCKER_INFLUXDB_INIT_USERNAME: admin
      DOCKER_INFLUXDB_INIT_PASSWORD: password
      DOCKER_INFLUXDB_INIT_ORG: stets
      DOCKER_INFLUXDB_INIT_BUCKET: metrics
    ports:
      - "8086:8086"
    volumes:
      - influxdb_data:/var/lib/influxdb2

  # MQTT Broker
  mosquitto:
    image: eclipse-mosquitto:2.0
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf
      - mosquitto_data:/mosquitto/data

  # Services
  user-service:
    build: ./user-service
    ports:
      - "3001:3000"
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/stets_home
      REDIS_URL: redis://redis:6379
      JWT_SECRET: your-secret-key
    depends_on:
      - postgres
      - redis

  device-service:
    build: ./device-service
    ports:
      - "3002:8080"
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/stets_home
      REDIS_URL: redis://redis:6379
      MQTT_BROKER: mosquitto:1883
    depends_on:
      - postgres
      - redis
      - mosquitto

  scenario-service:
    build: ./scenario-service
    ports:
      - "3003:8000"
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/stets_home
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

  notification-service:
    build: ./notification-service
    ports:
      - "3004:3000"
    environment:
      REDIS_URL: redis://redis:6379
      SENDGRID_API_KEY: your-sendgrid-key
      FCM_SERVER_KEY: your-fcm-key
    depends_on:
      - redis

volumes:
  postgres_data:
  redis_data:
  influxdb_data:
  mosquitto_data:
```

### 4.2 Kubernetes развертывание

#### 4.2.1 Namespace и ConfigMap
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: stets-home

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: stets-config
  namespace: stets-home
data:
  DATABASE_URL: "postgresql://postgres:password@postgres:5432/stets_home"
  REDIS_URL: "redis://redis:6379"
  MQTT_BROKER: "mosquitto:1883"
  JWT_SECRET: "your-secret-key"
```

#### 4.2.2 User Service Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: stets-home
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: stets/user-service:latest
        ports:
        - containerPort: 3000
        envFrom:
        - configMapRef:
            name: stets-config
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: stets-home
spec:
  selector:
    app: user-service
  ports:
  - port: 80
    targetPort: 3000
  type: ClusterIP
```

#### 4.2.3 Ingress Configuration
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: stets-home-ingress
  namespace: stets-home
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - api.stets-home.com
    secretName: stets-home-tls
  rules:
  - host: api.stets-home.com
    http:
      paths:
      - path: /api/users
        pathType: Prefix
        backend:
          service:
            name: user-service
            port:
              number: 80
      - path: /api/devices
        pathType: Prefix
        backend:
          service:
            name: device-service
            port:
              number: 80
      - path: /api/scenarios
        pathType: Prefix
        backend:
          service:
            name: scenario-service
            port:
              number: 80
      - path: /api/notifications
        pathType: Prefix
        backend:
          service:
            name: notification-service
            port:
              number: 80
```

### 4.3 CI/CD Pipeline

#### 4.3.1 GitHub Actions Workflow
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [user-service, device-service, scenario-service, notification-service]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      if: matrix.service == 'user-service' || matrix.service == 'notification-service'
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: ${{ matrix.service }}/package-lock.json
    
    - name: Setup Go
      if: matrix.service == 'device-service'
      uses: actions/setup-go@v3
      with:
        go-version: '1.21'
        cache: true
        cache-dependency-path: ${{ matrix.service }}/go.sum
    
    - name: Setup Python
      if: matrix.service == 'scenario-service'
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
        cache-dependency-path: ${{ matrix.service }}/requirements.txt
    
    - name: Install dependencies
      run: |
        cd ${{ matrix.service }}
        if [ "${{ matrix.service }}" = "user-service" ] || [ "${{ matrix.service }}" = "notification-service" ]; then
          npm ci
        elif [ "${{ matrix.service }}" = "device-service" ]; then
          go mod download
        elif [ "${{ matrix.service }}" = "scenario-service" ]; then
          pip install -r requirements.txt
        fi
    
    - name: Run tests
      run: |
        cd ${{ matrix.service }}
        if [ "${{ matrix.service }}" = "user-service" ] || [ "${{ matrix.service }}" = "notification-service" ]; then
          npm test
        elif [ "${{ matrix.service }}" = "device-service" ]; then
          go test ./...
        elif [ "${{ matrix.service }}" = "scenario-service" ]; then
          pytest
        fi
    
    - name: Run linting
      run: |
        cd ${{ matrix.service }}
        if [ "${{ matrix.service }}" = "user-service" ] || [ "${{ matrix.service }}" = "notification-service" ]; then
          npm run lint
        elif [ "${{ matrix.service }}" = "device-service" ]; then
          golangci-lint run
        elif [ "${{ matrix.service }}" = "scenario-service" ]; then
          flake8 .
        fi

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push images
      run: |
        services=("user-service" "device-service" "scenario-service" "notification-service")
        for service in "${services[@]}"; do
          docker buildx build --platform linux/amd64,linux/arm64 \
            -t stets/$service:${{ github.sha }} \
            -t stets/$service:latest \
            --push \
            ./$service
        done

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'v1.28.0'
    
    - name: Configure kubectl
      run: |
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig
    
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/
        kubectl rollout restart deployment/user-service -n stets-home
        kubectl rollout restart deployment/device-service -n stets-home
        kubectl rollout restart deployment/scenario-service -n stets-home
        kubectl rollout restart deployment/notification-service -n stets-home
```

## 5. Мониторинг и наблюдаемость

### 5.1 Метрики и мониторинг

#### 5.1.1 Prometheus конфигурация
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

scrape_configs:
  - job_name: 'user-service'
    static_configs:
      - targets: ['user-service:3000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'device-service'
    static_configs:
      - targets: ['device-service:8080']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'scenario-service'
    static_configs:
      - targets: ['scenario-service:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'notification-service'
    static_configs:
      - targets: ['notification-service:3000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

#### 5.1.2 Grafana Dashboard
```json
{
  "dashboard": {
    "title": "Stets Home System Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Active Devices",
        "type": "stat",
        "targets": [
          {
            "expr": "stets_devices_active_total",
            "legendFormat": "Active Devices"
          }
        ]
      }
    ]
  }
}
```

### 5.2 Логирование

#### 5.2.1 ELK Stack конфигурация
```yaml
# Logstash configuration
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][service] {
    mutate {
      add_field => { "service" => "%{[fields][service]}" }
    }
  }
  
  if [fields][environment] {
    mutate {
      add_field => { "environment" => "%{[fields][environment]}" }
    }
  }
  
  # Parse JSON logs
  if [message] =~ /^\{.*\}$/ {
    json {
      source => "message"
    }
  }
  
  # Parse timestamp
  date {
    match => [ "timestamp", "ISO8601" ]
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "stets-home-%{+YYYY.MM.dd}"
  }
}
```

#### 5.2.2 Структурированное логирование
```typescript
// Winston logger configuration
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'user-service',
    environment: process.env.NODE_ENV
  },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

// Usage in service
export class UserService {
  async createUser(userData: CreateUserDto): Promise<User> {
    logger.info('Creating new user', {
      email: userData.email,
      userId: userData.id
    });
    
    try {
      const user = await this.prisma.user.create({
        data: userData
      });
      
      logger.info('User created successfully', {
        userId: user.id,
        email: user.email
      });
      
      return user;
    } catch (error) {
      logger.error('Failed to create user', {
        error: error.message,
        stack: error.stack,
        userData
      });
      throw error;
    }
  }
}
```

### 5.3 Трассировка

#### 5.3.1 Jaeger конфигурация
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jaeger
  template:
    metadata:
      labels:
        app: jaeger
    spec:
      containers:
      - name: jaeger
        image: jaegertracing/all-in-one:latest
        ports:
        - containerPort: 16686
        - containerPort: 14268
        env:
        - name: COLLECTOR_OTLP_ENABLED
          value: "true"
```

#### 5.3.2 Инструментация сервисов
```typescript
// OpenTelemetry instrumentation
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger';

const sdk = new NodeSDK({
  traceExporter: new JaegerExporter({
    endpoint: 'http://jaeger:14268/api/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();

// Custom tracing
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('user-service');

export class UserService {
  async createUser(userData: CreateUserDto): Promise<User> {
    const span = tracer.startSpan('user.create');
    
    try {
      span.setAttributes({
        'user.email': userData.email,
        'user.name': userData.name
      });
      
      const user = await this.prisma.user.create({
        data: userData
      });
      
      span.setAttributes({
        'user.id': user.id,
        'user.created_at': user.createdAt.toISOString()
      });
      
      span.setStatus({ code: SpanStatusCode.OK });
      return user;
    } catch (error) {
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: error.message
      });
      throw error;
    } finally {
      span.end();
    }
  }
}
```

## 6. Безопасность

### 6.1 Аутентификация и авторизация

#### 6.1.1 JWT Implementation
```typescript
export class JWTService {
  private readonly secretKey: string;
  private readonly expiresIn: string;
  
  constructor() {
    this.secretKey = process.env.JWT_SECRET || 'default-secret';
    this.expiresIn = process.env.JWT_EXPIRES_IN || '1h';
  }
  
  generateTokens(user: User): { accessToken: string; refreshToken: string } {
    const payload = {
      sub: user.id,
      email: user.email,
      name: user.name,
      iat: Math.floor(Date.now() / 1000)
    };
    
    const accessToken = jwt.sign(payload, this.secretKey, {
      expiresIn: this.expiresIn,
      algorithm: 'HS256'
    });
    
    const refreshToken = jwt.sign(
      { sub: user.id, type: 'refresh' },
      this.secretKey,
      { expiresIn: '7d', algorithm: 'HS256' }
    );
    
    return { accessToken, refreshToken };
  }
  
  verifyToken(token: string): JWTPayload {
    try {
      return jwt.verify(token, this.secretKey) as JWTPayload;
    } catch (error) {
      throw new UnauthorizedError('Invalid token');
    }
  }
  
  refreshAccessToken(refreshToken: string): string {
    const payload = this.verifyToken(refreshToken);
    
    if (payload.type !== 'refresh') {
      throw new UnauthorizedError('Invalid refresh token');
    }
    
    const newPayload = {
      sub: payload.sub,
      email: payload.email,
      name: payload.name,
      iat: Math.floor(Date.now() / 1000)
    };
    
    return jwt.sign(newPayload, this.secretKey, {
      expiresIn: this.expiresIn,
      algorithm: 'HS256'
    });
  }
}
```

#### 6.1.2 Middleware для авторизации
```typescript
export class AuthMiddleware {
  constructor(private jwtService: JWTService) {}
  
  authenticate = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const authHeader = req.headers.authorization;
      
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        throw new UnauthorizedError('Missing or invalid authorization header');
      }
      
      const token = authHeader.substring(7);
      const payload = this.jwtService.verifyToken(token);
      
      // Проверка существования пользователя
      const user = await this.userService.findById(payload.sub);
      if (!user) {
        throw new UnauthorizedError('User not found');
      }
      
      // Добавление пользователя в контекст запроса
      req.user = user;
      next();
    } catch (error) {
      next(error);
    }
  };
  
  authorize = (roles: string[]) => {
    return (req: Request, res: Response, next: NextFunction) => {
      if (!req.user) {
        return next(new UnauthorizedError('User not authenticated'));
      }
      
      const userRole = req.user.role;
      if (!roles.includes(userRole)) {
        return next(new ForbiddenError('Insufficient permissions'));
      }
      
      next();
    };
  };
}
```

### 6.2 Шифрование данных

#### 6.2.1 Шифрование паролей
```typescript
export class PasswordService {
  private readonly saltRounds: number = 12;
  
  async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, this.saltRounds);
  }
  
  async verifyPassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }
  
  validatePassword(password: string): ValidationResult {
    const errors: string[] = [];
    
    if (password.length < 8 || password.length > 16) {
      errors.push('Password must be between 8 and 16 characters');
    }
    
    if (!/[a-z]/.test(password)) {
      errors.push('Password must contain at least one lowercase letter');
    }
    
    if (!/[A-Z]/.test(password)) {
      errors.push('Password must contain at least one uppercase letter');
    }
    
    return {
      isValid: errors.length === 0,
      errors
    };
  }
}
```

#### 6.2.2 Шифрование чувствительных данных
```typescript
export class EncryptionService {
  private readonly algorithm: string = 'aes-256-gcm';
  private readonly key: Buffer;
  
  constructor() {
    this.key = crypto.scryptSync(
      process.env.ENCRYPTION_KEY || 'default-key',
      'salt',
      32
    );
  }
  
  encrypt(text: string): EncryptedData {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipher(this.algorithm, this.key);
    cipher.setAAD(Buffer.from('stets-home', 'utf8'));
    
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const authTag = cipher.getAuthTag();
    
    return {
      encrypted,
      iv: iv.toString('hex'),
      authTag: authTag.toString('hex')
    };
  }
  
  decrypt(encryptedData: EncryptedData): string {
    const decipher = crypto.createDecipher(
      this.algorithm,
      this.key
    );
    
    decipher.setAAD(Buffer.from('stets-home', 'utf8'));
    decipher.setAuthTag(Buffer.from(encryptedData.authTag, 'hex'));
    
    let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  }
}
```

### 6.3 Безопасность API

#### 6.3.1 Rate Limiting
```typescript
export class RateLimitMiddleware {
  private redis: Redis;
  
  constructor() {
    this.redis = new Redis(process.env.REDIS_URL);
  }
  
  rateLimit = (windowMs: number, maxRequests: number) => {
    return async (req: Request, res: Response, next: NextFunction) => {
      const key = `rate_limit:${req.ip}:${req.path}`;
      const current = await this.redis.incr(key);
      
      if (current === 1) {
        await this.redis.expire(key, Math.ceil(windowMs / 1000));
      }
      
      if (current > maxRequests) {
        return res.status(429).json({
          error: 'Too many requests',
          retryAfter: Math.ceil(windowMs / 1000)
        });
      }
      
      res.setHeader('X-RateLimit-Limit', maxRequests);
      res.setHeader('X-RateLimit-Remaining', Math.max(0, maxRequests - current));
      
      next();
    };
  };
}
```

#### 6.3.2 Input Validation
```typescript
export class ValidationMiddleware {
  validateRegister = (req: Request, res: Response, next: NextFunction) => {
    const schema = Joi.object({
      email: Joi.string().email().required(),
      password: Joi.string().min(8).max(16).pattern(/^(?=.*[a-z])(?=.*[A-Z])/).required(),
      name: Joi.string().min(2).max(50).required()
    });
    
    const { error } = schema.validate(req.body);
    if (error) {
      return res.status(400).json({
        error: 'Validation failed',
        details: error.details.map(d => d.message)
      });
    }
    
    next();
  };
  
  validateDeviceCode = (req: Request, res: Response, next: NextFunction) => {
    const schema = Joi.object({
      deviceCode: Joi.string().length(12).pattern(/^[0-9]+$/).required()
    });
    
    const { error } = schema.validate(req.body);
    if (error) {
      return res.status(400).json({
        error: 'Invalid device code format',
        details: error.details.map(d => d.message)
      });
    }
    
    next();
  };
}
```

## 7. Тестирование

### 7.1 Unit Testing

#### 7.1.1 User Service Tests
```typescript
describe('UserService', () => {
  let userService: UserService;
  let mockPrisma: jest.Mocked<PrismaClient>;
  
  beforeEach(() => {
    mockPrisma = {
      user: {
        create: jest.fn(),
        findUnique: jest.fn(),
        update: jest.fn()
      }
    } as any;
    
    userService = new UserService(mockPrisma, mockPasswordService, mockEmailService);
  });
  
  describe('createUser', () => {
    it('should create a user successfully', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'Password123',
        name: 'Test User'
      };
      
      const expectedUser = {
        id: 1,
        email: userData.email,
        name: userData.name,
        createdAt: new Date()
      };
      
      mockPrisma.user.create.mockResolvedValue(expectedUser);
      
      const result = await userService.createUser(userData);
      
      expect(result).toEqual(expectedUser);
      expect(mockPrisma.user.create).toHaveBeenCalledWith({
        data: expect.objectContaining({
          email: userData.email,
          name: userData.name,
          passwordHash: expect.any(String)
        })
      });
    });
    
    it('should throw error if user already exists', async () => {
      const userData = {
        email: 'existing@example.com',
        password: 'Password123',
        name: 'Test User'
      };
      
      mockPrisma.user.findUnique.mockResolvedValue({
        id: 1,
        email: userData.email
      });
      
      await expect(userService.createUser(userData)).rejects.toThrow('User already exists');
    });
  });
});
```

#### 7.1.2 Device Service Tests
```go
func TestDeviceService_AddDevice(t *testing.T) {
    tests := []struct {
        name        string
        deviceCode  string
        homeID      int
        expectError bool
        errorMsg    string
    }{
        {
            name:        "valid device code",
            deviceCode:  "123456789012",
            homeID:      1,
            expectError: false,
        },
        {
            name:        "invalid device code length",
            deviceCode:  "12345678901",
            homeID:      1,
            expectError: true,
            errorMsg:    "invalid device code format",
        },
        {
            name:        "invalid device code characters",
            deviceCode:  "12345678901a",
            homeID:      1,
            expectError: true,
            errorMsg:    "invalid device code format",
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Setup
            mockDB := &MockDatabase{}
            mockMQTT := &MockMQTTService{}
            deviceService := NewDeviceService(mockDB, mockMQTT)
            
            // Execute
            device, err := deviceService.AddDevice(tt.homeID, tt.deviceCode)
            
            // Assert
            if tt.expectError {
                assert.Error(t, err)
                assert.Contains(t, err.Error(), tt.errorMsg)
            } else {
                assert.NoError(t, err)
                assert.NotNil(t, device)
                assert.Equal(t, tt.deviceCode, device.DeviceCode)
            }
        })
    }
}
```

### 7.2 Integration Testing

#### 7.2.1 API Integration Tests
```typescript
describe('User API Integration', () => {
  let app: Express;
  let server: Server;
  
  beforeAll(async () => {
    app = createApp();
    server = app.listen(0);
  });
  
  afterAll(async () => {
    server.close();
  });
  
  describe('POST /api/auth/register', () => {
    it('should register a new user', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'Password123',
        name: 'Test User'
      };
      
      const response = await request(app)
        .post('/api/auth/register')
        .send(userData)
        .expect(201);
      
      expect(response.body).toHaveProperty('user');
      expect(response.body).toHaveProperty('tokens');
      expect(response.body.user.email).toBe(userData.email);
    });
    
    it('should return error for invalid email', async () => {
      const userData = {
        email: 'invalid-email',
        password: 'Password123',
        name: 'Test User'
      };
      
      const response = await request(app)
        .post('/api/auth/register')
        .send(userData)
        .expect(400);
      
      expect(response.body).toHaveProperty('error');
    });
  });
});
```

### 7.3 E2E Testing

#### 7.3.1 Playwright E2E Tests
```typescript
import { test, expect } from '@playwright/test';

test.describe('Stets Home App', () => {
  test('user can register and login', async ({ page }) => {
    // Navigate to registration page
    await page.goto('/register');
    
    // Fill registration form
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'Password123');
    await page.fill('[data-testid="name-input"]', 'Test User');
    
    // Submit form
    await page.click('[data-testid="register-button"]');
    
    // Wait for redirect to dashboard
    await page.waitForURL('/dashboard');
    
    // Verify user is logged in
    await expect(page.locator('[data-testid="user-name"]')).toContainText('Test User');
  });
  
  test('user can add device', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'Password123');
    await page.click('[data-testid="login-button"]');
    
    // Navigate to add device
    await page.click('[data-testid="add-device-button"]');
    
    // Select manual input
    await page.click('[data-testid="manual-input-button"]');
    
    // Enter device code
    await page.fill('[data-testid="device-code-input"]', '123456789012');
    
    // Select room
    await page.selectOption('[data-testid="room-select"]', 'bedroom');
    
    // Submit
    await page.click('[data-testid="add-device-submit"]');
    
    // Verify device was added
    await expect(page.locator('[data-testid="device-list"]')).toContainText('123456789012');
  });
});
```

## 8. Заключение

### 8.1 Ключевые особенности архитектуры

#### 8.1.1 Микросервисная архитектура
- **Независимость сервисов:** Каждый сервис может развиваться независимо
- **Масштабируемость:** Возможность масштабирования отдельных сервисов
- **Технологическое разнообразие:** Использование подходящих технологий для каждой задачи
- **Отказоустойчивость:** Изоляция сбоев между сервисами

#### 8.1.2 Современные технологии
- **Cloud-Native:** Развертывание в облачной среде
- **Containerization:** Docker и Kubernetes для оркестрации
- **API-First:** Приоритет API в разработке
- **DevOps Integration:** Автоматизация CI/CD процессов

#### 8.1.3 Безопасность и надежность
- **Многоуровневая безопасность:** От аутентификации до шифрования данных
- **Мониторинг и наблюдаемость:** Полная видимость работы системы
- **Тестирование:** Комплексное тестирование на всех уровнях
- **Резервное копирование:** Надежное хранение и восстановление данных

### 8.2 Преимущества решения

#### 8.2.1 Для разработки
- **Быстрая разработка:** Готовые компоненты и шаблоны
- **Качество кода:** Стандарты и лучшие практики
- **Тестируемость:** Легкое тестирование компонентов
- **Документированность:** Подробная документация API

#### 8.2.2 Для эксплуатации
- **Простота развертывания:** Автоматизированные процессы
- **Мониторинг:** Полная видимость работы системы
- **Масштабирование:** Горизонтальное и вертикальное масштабирование
- **Обслуживание:** Минимальное время простоя

#### 8.2.3 Для пользователей
- **Производительность:** Быстрая работа приложения
- **Надежность:** Стабильная работа системы
- **Безопасность:** Защита данных пользователей
- **Удобство:** Интуитивный интерфейс

### 8.3 Следующие шаги

1. **Реализация MVP:** Разработка базовой функциональности
2. **Тестирование:** Комплексное тестирование системы
3. **Развертывание:** Настройка production окружения
4. **Мониторинг:** Настройка системы мониторинга
5. **Оптимизация:** Улучшение производительности на основе метрик

---

**Дата создания:** [Текущая дата]  
**Версия:** 1.0  
**Статус:** Утвержден
