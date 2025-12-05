# API参考文档

## 目录
- [基础信息](#基础信息)
- [检测相关API](#检测相关api)
- [标定相关API](#标定相关api)
- [配置相关API](#配置相关api)
- [视频相关API](#视频相关api)

---

## 基础信息

### API地址
- **基础URL**: `http://localhost:8000`
- **API版本**: `/api/v1`
- **文档地址**: `http://localhost:8000/docs` (Swagger UI)

### 认证方式
当前版本无需认证（生产环境建议添加）

### 响应格式
所有API响应均为JSON格式

---

## 检测相关API

### 启动检测

**接口**: `POST /api/v1/detection/start`

**请求体**:
```json
{
  "camera_id": "default",
  "algorithms": ["nozzle_offset", "suction_height"]
}
```

**响应**:
```json
{
  "message": "检测已启动",
  "request_id": "12345"
}
```

### 停止检测

**接口**: `POST /api/v1/detection/stop`

**查询参数**:
- `camera_id` (string): 相机ID，默认"default"

**响应**:
```json
{
  "message": "检测已停止"
}
```

### 获取检测结果

**接口**: `GET /api/v1/detection/results`

**查询参数**:
- `camera_id` (string): 相机ID
- `limit` (int): 返回数量，默认100
- `offset` (int): 偏移量，默认0

**响应**:
```json
{
  "results": [
    {
      "algorithm_name": "nozzle_offset",
      "timestamp": "2024-01-01 12:00:00",
      "frame_id": 12345,
      "result": {
        "offset_x_mm": 0.12,
        "offset_y_mm": 0.08,
        "offset_distance_mm": 0.15
      },
      "status": "normal",
      "annotations": []
    }
  ],
  "total": 100,
  "limit": 100,
  "offset": 0
}
```

---

## 标定相关API

### 启动标定

**接口**: `POST /api/v1/calibration/start`

**请求体**:
```json
{
  "method": "chessboard",
  "board_size": [9, 6],
  "square_size_mm": 10.0
}
```

**响应**:
```json
{
  "message": "标定已启动",
  "calibration_id": "cal_12345"
}
```

### 上传标定图像

**接口**: `POST /api/v1/calibration/upload-image`

**请求类型**: `multipart/form-data`

**表单字段**:
- `file`: 图像文件
- `calibration_id`: 标定ID

**响应**:
```json
{
  "message": "图像上传成功",
  "image_id": "img_12345"
}
```

### 计算标定参数

**接口**: `POST /api/v1/calibration/calculate`

**请求体**:
```json
{
  "calibration_id": "cal_12345"
}
```

**响应**:
```json
{
  "calibration_id": "cal_12345",
  "status": "success",
  "parameters": {
    "pixel_size_x_mm": 0.005,
    "pixel_size_y_mm": 0.005,
    "accuracy_mm": 0.03,
    "reprojection_error": 0.08
  }
}
```

### 获取标定参数

**接口**: `GET /api/v1/calibration/parameters`

**响应**:
```json
{
  "pixel_size_x_mm": 0.005,
  "pixel_size_y_mm": 0.005,
  "last_updated": "2024-01-01 12:00:00"
}
```

---

## 配置相关API

### 获取算法配置

**接口**: `GET /api/v1/config/algorithms`

**响应**:
```json
{
  "algorithms": [
    {
      "name": "nozzle_offset",
      "parameters": {
        "threshold_mm": 0.1
      }
    },
    {
      "name": "suction_height",
      "parameters": {
        "min_mm": 3.0,
        "max_mm": 5.0
      }
    }
  ]
}
```

### 更新配置

**接口**: `POST /api/v1/config/update`

**请求体**:
```json
{
  "algorithm": "suction_height",
  "parameters": {
    "min_mm": 3.0,
    "max_mm": 5.0
  }
}
```

**响应**:
```json
{
  "message": "配置已更新"
}
```

---

## 视频相关API

### 列出视频

**接口**: `GET /api/v1/videos`

**查询参数**:
- `limit` (int): 返回数量，默认100
- `offset` (int): 偏移量，默认0

**响应**:
```json
{
  "videos": [
    {
      "id": "video_12345",
      "filename": "video_20240101_120000.mp4",
      "camera_id": "default",
      "start_time": "2024-01-01 12:00:00",
      "end_time": "2024-01-01 12:01:00",
      "duration_seconds": 60,
      "file_size": 10485760
    }
  ],
  "total": 100,
  "limit": 100,
  "offset": 0
}
```

### 获取视频URL

**接口**: `GET /api/v1/videos/{video_id}/url`

**查询参数**:
- `expires` (int): URL过期时间（秒），默认3600

**响应**:
```json
{
  "url": "https://minio.example.com/videos/video_12345?X-Amz-Algorithm=..."
}
```

---

## 健康检查

### 健康检查

**接口**: `GET /health`

**响应**:
```json
{
  "status": "healthy",
  "camera": true,
  "mqtt": true,
  "minio": true,
  "timestamp": "2024-01-01T12:00:00"
}
```

---

## 错误响应

所有API错误响应格式：

```json
{
  "error": "错误描述",
  "detail": "详细错误信息",
  "status_code": 400
}
```

**常见错误码**:
- `400`: 请求参数错误
- `404`: 资源不存在
- `500`: 服务器内部错误

---

## 完整API文档

访问 `http://localhost:8000/docs` 查看完整的Swagger API文档，包括：
- 所有接口的详细说明
- 请求/响应示例
- 在线测试功能
