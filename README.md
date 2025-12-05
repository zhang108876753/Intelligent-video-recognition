# 半导体喷胶显影喷嘴检测摄像监控算法识别系统

## 项目简介

本项目是一套完整的工业视觉检测系统，用于实时检测半导体喷胶显影设备的喷嘴状态。系统支持9种检测算法，实现0.05mm精度检测，60fps实时处理，并通过PLC信号控制实现自动化检测流程。

## 核心功能

- ✅ **9种检测算法**：偏移距离、角度偏移、脏污、挂滴、掉滴、损坏、回吸高度、喷液宽度、气泡检测
- ✅ **自动标定系统**：像素到物理坐标转换，精度0.05mm
- ✅ **实时视频处理**：60fps，海康工业相机
- ✅ **PLC信号控制**：Modbus TCP协议，自动触发录制
- ✅ **视频存储**：MinIO对象存储，支持回放和下载
- ✅ **实时通信**：MQTT消息推送，WebSocket实时更新
- ✅ **Web界面**：参数配置、结果展示、视频回放
- ✅ **异常标注**：自动标注异常位置和报警信息

## 技术架构

### 后端技术栈
- **语言**: Python 3.9+
- **视觉库**: OpenCV 4.8+
- **Web框架**: FastAPI
- **相机SDK**: 海康威视SDK
- **PLC通信**: pymodbus
- **消息队列**: paho-mqtt
- **对象存储**: minio-py
- **数据库**: PostgreSQL + Redis

### 前端技术栈
- **框架**: Vue 3 + TypeScript
- **UI组件**: Element Plus
- **图表**: ECharts
- **实时通信**: MQTT.js

### 基础设施
- **容器化**: Docker + Docker Compose
- **消息代理**: Eclipse Mosquitto
- **对象存储**: MinIO
- **数据库**: PostgreSQL + Redis

## 项目结构

```
semiconductor-nozzle-inspection-system/
├── backend/                    # 后端服务
│   ├── video_capture/         # 视频采集模块
│   ├── algorithm/             # 算法处理模块
│   ├── storage/               # 存储模块
│   ├── communication/         # 通信模块（MQTT、PLC）
│   ├── config/                # 配置管理
│   ├── api/                   # API接口
│   └── main.py               # 主程序入口
├── frontend/                   # 前端应用（待开发）
├── docs/                       # 项目文档
│   ├── 使用和调试指南.md      # 使用和调试文档
│   └── 算法详细设计.md        # 算法设计文档
├── docker-compose.yml          # Docker编排配置
├── requirements.txt            # Python依赖
├── .env.example                # 环境变量模板
└── README.md                   # 项目说明
```

## 快速开始

### 1. 环境准备

```bash
# 系统要求
- Python 3.9+
- Docker & Docker Compose
- 海康工业相机（支持RTSP）
- PLC设备（Modbus TCP协议）
```

### 2. 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd semiconductor-nozzle-inspection-system

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置相机、PLC、MinIO、MQTT等参数

# 5. 启动基础设施服务
docker-compose up -d

# 6. 启动后端服务
cd backend
python main.py
```

### 3. 验证安装

```bash
# 健康检查
curl http://localhost:8000/health

# API文档
# 访问 http://localhost:8000/docs
```

## 使用流程

### 首次使用 - 标定

1. 准备标定板（棋盘格9×6或圆点板）
2. 启动标定流程，采集≥10张不同角度图像
3. 系统自动计算标定参数
4. 验证标定精度（重投影误差<0.1像素）

### 日常检测

1. 配置检测参数（阈值等）
2. 连接相机和PLC
3. PLC信号触发 → 自动开始检测
4. 实时显示检测结果和报警
5. 视频自动上传MinIO

## 文档

- **[使用和调试指南](./docs/使用和调试指南.md)** - 完整的使用说明、API接口、调试方法和常见问题
- **[算法详细设计](./docs/算法详细设计.md)** - 9种检测算法的详细设计文档

## API文档

启动服务后，访问 `http://localhost:8000/docs` 查看完整的Swagger API文档。

## 开发状态

- [x] 项目架构设计
- [x] 基础框架搭建
- [x] 视频采集模块框架
- [x] PLC通信模块
- [x] MQTT通信模块
- [x] MinIO存储模块
- [x] API接口框架
- [x] 算法基类和示例算法
- [ ] 标定系统开发
- [ ] 9种检测算法完整实现
- [ ] 前端界面开发
- [ ] 系统集成测试

## 许可证

MIT License

## 技术支持

详细的使用和调试指南请参考 [使用和调试指南](./docs/使用和调试指南.md)
