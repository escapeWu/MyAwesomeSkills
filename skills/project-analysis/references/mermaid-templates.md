# Mermaid 图表模板参考

本文档提供各种架构模式和数据流场景的 Mermaid 图表模板。

## 目录

1. [架构图模板](#架构图模板)
2. [时序图模板](#时序图模板)
3. [数据流图模板](#数据流图模板)
4. [类图模板](#类图模板)

---

## 架构图模板

### 分层架构（经典三层/多层）

```mermaid
graph TB
    subgraph 客户端["客户端层"]
        Web[Web 浏览器]
        Mobile[移动应用]
    end

    subgraph 表示层["表示层"]
        Controller[控制器]
        View[视图模板]
    end

    subgraph 业务层["业务逻辑层"]
        Service[服务层]
        Domain[领域模型]
        Validator[验证器]
    end

    subgraph 数据层["数据访问层"]
        Repository[仓储层]
        ORM[ORM映射]
    end

    subgraph 基础设施["基础设施"]
        DB[(主数据库)]
        Cache[(Redis缓存)]
        MQ[消息队列]
    end

    Web --> Controller
    Mobile --> Controller
    Controller --> Service
    Controller --> View
    Service --> Domain
    Service --> Validator
    Service --> Repository
    Repository --> ORM
    ORM --> DB
    Service --> Cache
    Service --> MQ
```

### 微服务架构

```mermaid
graph TB
    subgraph 网关["API 网关"]
        Gateway[网关服务]
        Auth[认证服务]
    end

    subgraph 核心服务["核心业务服务"]
        UserService[用户服务]
        OrderService[订单服务]
        ProductService[商品服务]
        PaymentService[支付服务]
    end

    subgraph 基础服务["基础服务"]
        ConfigService[配置中心]
        Registry[服务注册]
        MQ[消息总线]
    end

    subgraph 数据存储["数据存储"]
        UserDB[(用户库)]
        OrderDB[(订单库)]
        ProductDB[(商品库)]
    end

    Gateway --> Auth
    Gateway --> UserService
    Gateway --> OrderService
    Gateway --> ProductService

    UserService --> UserDB
    OrderService --> OrderDB
    ProductService --> ProductDB

    OrderService --> PaymentService
    OrderService -.-> MQ
    MQ -.-> ProductService

    UserService --> Registry
    OrderService --> Registry
    ProductService --> Registry
```

### 前后端分离架构

```mermaid
graph TB
    subgraph 前端["前端应用"]
        SPA[单页应用]
        State[状态管理]
        Router[路由]
    end

    subgraph 后端["后端 API"]
        REST[REST API]
        GraphQL[GraphQL]
        WebSocket[WebSocket]
    end

    subgraph 服务层["业务服务"]
        BizService[业务服务]
        AuthService[认证服务]
    end

    subgraph 存储["数据存储"]
        DB[(数据库)]
        OSS[对象存储]
        Redis[(缓存)]
    end

    SPA --> REST
    SPA --> GraphQL
    SPA --> WebSocket
    REST --> BizService
    GraphQL --> BizService
    BizService --> AuthService
    BizService --> DB
    BizService --> OSS
    BizService --> Redis
```

### 事件驱动架构

```mermaid
graph LR
    subgraph 生产者["事件生产者"]
        P1[服务A]
        P2[服务B]
        P3[外部系统]
    end

    subgraph 事件总线["事件总线"]
        Kafka[消息队列]
        EventStore[(事件存储)]
    end

    subgraph 消费者["事件消费者"]
        C1[处理器1]
        C2[处理器2]
        C3[通知服务]
    end

    P1 --> Kafka
    P2 --> Kafka
    P3 --> Kafka
    Kafka --> EventStore
    Kafka --> C1
    Kafka --> C2
    Kafka --> C3
```

---

## 时序图模板

### 用户认证流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant C as 客户端
    participant G as 网关
    participant A as 认证服务
    participant D as 用户数据库

    U->>C: 输入用户名密码
    C->>G: POST /login
    G->>A: 验证请求
    A->>D: 查询用户
    D-->>A: 用户信息
    A->>A: 验证密码
    alt 验证成功
        A->>A: 生成JWT
        A-->>G: 返回Token
        G-->>C: 登录成功
        C-->>U: 跳转首页
    else 验证失败
        A-->>G: 认证失败
        G-->>C: 401错误
        C-->>U: 提示错误
    end
```

### CRUD 操作流程

```mermaid
sequenceDiagram
    participant C as 客户端
    participant API as API层
    participant S as 服务层
    participant R as 仓储层
    participant DB as 数据库
    participant Cache as 缓存

    C->>API: 请求数据
    API->>S: 调用服务
    S->>Cache: 查询缓存
    alt 缓存命中
        Cache-->>S: 返回数据
    else 缓存未命中
        S->>R: 查询仓储
        R->>DB: SQL查询
        DB-->>R: 查询结果
        R-->>S: 实体对象
        S->>Cache: 更新缓存
    end
    S-->>API: 业务数据
    API-->>C: JSON响应
```

### 异步处理流程

```mermaid
sequenceDiagram
    participant C as 客户端
    participant API as API服务
    participant MQ as 消息队列
    participant W as 工作进程
    participant DB as 数据库
    participant N as 通知服务

    C->>API: 提交任务
    API->>DB: 创建任务记录
    API->>MQ: 发送消息
    API-->>C: 返回任务ID

    Note over MQ,W: 异步处理
    MQ->>W: 消费消息
    W->>W: 执行任务
    W->>DB: 更新任务状态
    W->>N: 发送完成通知
    N-->>C: 推送结果
```

---

## 数据流图模板

### 请求处理数据流

```mermaid
flowchart LR
    subgraph 输入
        REQ[HTTP请求]
        HEADER[请求头]
        BODY[请求体]
    end

    subgraph 中间件
        AUTH[认证中间件]
        VALID[参数验证]
        RATE[限流器]
    end

    subgraph 处理
        CTRL[控制器]
        SVC[服务层]
        REPO[数据访问]
    end

    subgraph 输出
        RESP[HTTP响应]
        LOG[日志记录]
    end

    REQ --> AUTH
    HEADER --> AUTH
    AUTH --> RATE
    BODY --> VALID
    VALID --> CTRL
    RATE --> CTRL
    CTRL --> SVC
    SVC --> REPO
    REPO --> SVC
    SVC --> CTRL
    CTRL --> RESP
    CTRL --> LOG
```

### ETL 数据流

```mermaid
flowchart TB
    subgraph 数据源["数据源"]
        S1[(MySQL)]
        S2[(MongoDB)]
        S3[API接口]
        S4[文件系统]
    end

    subgraph 抽取["抽取 Extract"]
        E1[数据读取器]
        E2[增量检测]
    end

    subgraph 转换["转换 Transform"]
        T1[数据清洗]
        T2[格式转换]
        T3[聚合计算]
        T4[数据校验]
    end

    subgraph 加载["加载 Load"]
        L1[批量写入]
        L2[索引更新]
    end

    subgraph 目标["目标存储"]
        D1[(数据仓库)]
        D2[搜索引擎]
    end

    S1 --> E1
    S2 --> E1
    S3 --> E1
    S4 --> E1
    E1 --> E2
    E2 --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> L1
    L1 --> L2
    L2 --> D1
    L2 --> D2
```

### 状态机数据流

```mermaid
stateDiagram-v2
    [*] --> 待提交: 创建订单
    待提交 --> 待支付: 提交订单
    待支付 --> 已支付: 完成支付
    待支付 --> 已取消: 超时取消
    已支付 --> 待发货: 商家确认
    待发货 --> 已发货: 发货
    已发货 --> 已完成: 确认收货
    已完成 --> [*]
    已取消 --> [*]

    note right of 待支付
        支付超时30分钟
        自动取消订单
    end note
```

---

## 类图模板

### 领域模型类图

```mermaid
classDiagram
    class 用户 {
        +String 用户ID
        +String 用户名
        +String 邮箱
        +登录()
        +注销()
    }

    class 订单 {
        +String 订单ID
        +Date 创建时间
        +Decimal 总金额
        +String 状态
        +提交()
        +取消()
        +支付()
    }

    class 订单项 {
        +String 商品ID
        +Integer 数量
        +Decimal 单价
        +计算小计()
    }

    class 商品 {
        +String 商品ID
        +String 名称
        +Decimal 价格
        +Integer 库存
        +扣减库存()
    }

    用户 "1" --> "*" 订单 : 创建
    订单 "1" --> "*" 订单项 : 包含
    订单项 "*" --> "1" 商品 : 引用
```

### 设计模式类图

```mermaid
classDiagram
    class Controller {
        <<interface>>
        +handleRequest()
    }

    class Service {
        <<interface>>
        +execute()
    }

    class Repository {
        <<interface>>
        +find()
        +save()
        +delete()
    }

    class UserController {
        -UserService service
        +handleRequest()
    }

    class UserService {
        -UserRepository repo
        +execute()
    }

    class UserRepository {
        -Database db
        +find()
        +save()
        +delete()
    }

    Controller <|.. UserController
    Service <|.. UserService
    Repository <|.. UserRepository
    UserController --> UserService
    UserService --> UserRepository
```
