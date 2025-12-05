# 半导体喷胶显影喷嘴检测摄像监控算法识别系统

## 项目简介

本项目是一套完整的工业视觉检测系统，用于实时检测半导体喷胶显影设备的喷嘴状态，包括偏移、角度、脏污、挂滴、掉滴、损坏、回吸高度、喷液宽度、液体气泡等9种检测项目。

## 核心功能

- ✅ 9种检测算法（偏移距离、角度偏移、脏污、挂滴、掉滴、损坏、回吸高度、喷液宽度、气泡）
- ✅ 自动标定系统（像素到物理坐标转换，精度0.05mm）
- ✅ 实时视频处理（60fps，海康工业相机）
- ✅ PLC信号控制（录制开始/结束）
- ✅ 视频存储（MinIO）
- ✅ 实时通信（MQTT）
- ✅ Web界面（参数配置、结果展示、视频回放）
- ✅ 异常标注和报警

## 技术栈

### 后端
- Python 3.9+
- OpenCV 4.8+
- FastAPI
- PyTorch/TensorFlow（深度学习）
- 海康威视SDK
- pymodbus（PLC通信）
- paho-mqtt
- minio-py

### 前端
- Vue 3 + TypeScript
- Element Plus
- ECharts
- MQTT.js

### 基础设施
- Docker + Docker Compose
- PostgreSQL
- Redis
- MinIO
- Eclipse Mosquitto

## 项目结构

```
semiconductor-nozzle-inspection-system/
├── backend/                    # 后端服务
│   ├── video_capture/         # 视频采集模块
│   ├── algorithm/             # 算法处理模块
│   ├── storage/               # 存储模块
│   ├── communication/         # 通信模块
│   ├── config/                # 配置管理
│   └── api/                   # API接口
├── frontend/                   # 前端应用
├── docs/                       # 文档
├── tests/                      # 测试
├── docker/                     # Docker配置
└── requirements.txt            # Python依赖
```

## 快速开始

### 环境要求

- Python 3.9+
- Docker & Docker Compose
- 海康工业相机
- PLC设备（Modbus协议）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd semiconductor-nozzle-inspection-system
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置相机、PLC、MinIO、MQTT等参数
```

4. **启动服务**
```bash
docker-compose up -d
```

5. **启动后端服务**
```bash
cd backend
python main.py
```

6. **启动前端服务**
```bash
cd frontend
npm install
npm run dev
```

## 使用说明

### 1. 标定流程

1. 放置标定板（棋盘格或圆点）
2. 在Web界面启动标定流程
3. 采集多角度图像（≥10张）
4. 系统自动计算标定参数
5. 验证标定精度

### 2. 检测流程

1. 配置检测参数（阈值等）
2. PLC信号触发录制
3. 系统自动开始检测
4. 实时显示检测结果
5. 异常自动报警
6. 视频自动上传MinIO

### 3. 参数配置

在Web界面可以配置：
- 各检测项的阈值参数
- 报警阈值
- 相机参数
- 标定参数

## 文档

- [可行性分析和技术方案](./docs/可行性分析和技术方案.md)
- [算法详细设计](./docs/算法详细设计.md)
- [API文档](./docs/API文档.md)
- [部署文档](./docs/部署文档.md)

## 开发计划

- [x] 可行性分析和技术方案设计
- [ ] 基础框架搭建
- [ ] 视频采集模块开发
- [ ] 标定系统开发
- [ ] 检测算法开发
- [ ] 系统集成
- [ ] 测试与优化

## 许可证

MIT License

## 联系方式

如有问题，请联系开发团队。
