"""
半导体喷胶显影喷嘴检测系统 - 主程序入口
"""
import asyncio
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config.settings import settings
from api.routes import router
from video_capture.camera_manager import CameraManager
from communication.mqtt_client import MQTTClient
from storage.minio_client import MinIOClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="半导体喷嘴检测系统API",
    description="提供检测算法、视频管理、配置管理等API接口",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api/v1")

# 全局对象
camera_manager = None
mqtt_client = None
minio_client = None


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    global camera_manager, mqtt_client, minio_client
    
    logger.info("系统启动中...")
    
    # 初始化MinIO客户端
    try:
        minio_client = MinIOClient(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        logger.info("MinIO客户端初始化成功")
    except Exception as e:
        logger.error(f"MinIO客户端初始化失败: {e}")
    
    # 初始化MQTT客户端
    try:
        mqtt_client = MQTTClient(
            broker=settings.MQTT_BROKER,
            port=settings.MQTT_PORT,
            username=settings.MQTT_USERNAME,
            password=settings.MQTT_PASSWORD
        )
        await mqtt_client.connect()
        logger.info("MQTT客户端连接成功")
    except Exception as e:
        logger.error(f"MQTT客户端连接失败: {e}")
    
    # 初始化相机管理器
    try:
        camera_manager = CameraManager(
            camera_config=settings.CAMERA_CONFIG
        )
        logger.info("相机管理器初始化成功")
    except Exception as e:
        logger.error(f"相机管理器初始化失败: {e}")
    
    logger.info("系统启动完成")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理资源"""
    global camera_manager, mqtt_client
    
    logger.info("系统关闭中...")
    
    if camera_manager:
        await camera_manager.stop_all()
    
    if mqtt_client:
        await mqtt_client.disconnect()
    
    logger.info("系统关闭完成")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "半导体喷胶显影喷嘴检测系统API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "camera": camera_manager is not None,
        "mqtt": mqtt_client is not None if mqtt_client else False,
        "minio": minio_client is not None
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
