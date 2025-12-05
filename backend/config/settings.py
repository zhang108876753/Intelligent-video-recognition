"""
系统配置管理
"""
from pydantic_settings import BaseSettings
from typing import List, Dict, Any
from functools import lru_cache


class Settings(BaseSettings):
    """系统配置"""
    
    # 应用配置
    APP_NAME: str = "半导体喷嘴检测系统"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # 相机配置
    CAMERA_CONFIG: Dict[str, Any] = {
        "type": "hikvision",
        "ip": "192.168.1.64",
        "port": 8000,
        "username": "admin",
        "password": "admin123",
        "fps": 60,
        "resolution": {"width": 2048, "height": 2048}
    }
    
    # PLC配置
    PLC_CONFIG: Dict[str, Any] = {
        "type": "modbus_tcp",
        "host": "192.168.1.100",
        "port": 502,
        "slave_id": 1,
        "start_signal_address": 0,
        "stop_signal_address": 1
    }
    
    # MinIO配置
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = False
    MINIO_BUCKET: str = "nozzle-videos"
    
    # MQTT配置
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_USERNAME: str = ""
    MQTT_PASSWORD: str = ""
    MQTT_TOPIC_PREFIX: str = "nozzle/inspection"
    
    # 数据库配置
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/nozzle_db"
    
    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # 算法配置
    ALGORITHM_CONFIG: Dict[str, Any] = {
        "calibration": {
            "method": "chessboard",  # chessboard or circle
            "board_size": (9, 6),  # 棋盘格大小
            "square_size_mm": 10.0,  # 方格大小（mm）
            "min_images": 10  # 最少标定图像数
        },
        "detection": {
            "offset_threshold_mm": 0.1,  # 偏移阈值
            "angle_threshold_deg": 2.0,  # 角度阈值
            "contamination_threshold": 0.3,  # 脏污阈值
            "hanging_drop_threshold_mm2": 50.0,  # 挂滴面积阈值
            "suction_height_min_mm": 3.0,  # 回吸高度最小值
            "suction_height_max_mm": 5.0,  # 回吸高度最大值
            "liquid_width_threshold_mm": 2.0,  # 喷液宽度阈值
            "bubble_count_threshold": 5  # 气泡数量阈值
        },
        "precision": {
            "target_accuracy_mm": 0.05,  # 目标精度
            "pixel_size_x_mm": 0.005,  # X方向像素大小（需标定）
            "pixel_size_y_mm": 0.005  # Y方向像素大小（需标定）
        }
    }
    
    # 视频配置
    VIDEO_CONFIG: Dict[str, Any] = {
        "codec": "H264",
        "fps": 60,
        "quality": "high",
        "segment_duration_sec": 60,  # 视频分段时长
        "save_path": "./videos"
    }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置实例（单例）"""
    return Settings()


settings = get_settings()
