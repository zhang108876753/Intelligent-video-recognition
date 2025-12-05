"""
相机管理器 - 负责海康相机的连接、控制和视频采集
"""
import asyncio
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import cv2
import numpy as np

logger = logging.getLogger(__name__)


class CameraManager:
    """相机管理器"""
    
    def __init__(self, camera_config: Dict[str, Any]):
        """
        初始化相机管理器
        
        Args:
            camera_config: 相机配置字典
        """
        self.config = camera_config
        self.cameras: Dict[str, Any] = {}
        self.capture_tasks: Dict[str, asyncio.Task] = {}
        self.is_recording: Dict[str, bool] = {}
        
    async def connect_camera(self, camera_id: str = "default") -> bool:
        """
        连接相机
        
        Args:
            camera_id: 相机ID
            
        Returns:
            是否连接成功
        """
        try:
            # TODO: 集成海康SDK
            # 这里先用OpenCV模拟
            if self.config["type"] == "hikvision":
                # 海康相机RTSP地址
                rtsp_url = f"rtsp://{self.config['username']}:{self.config['password']}@{self.config['ip']}:554/Streaming/Channels/101"
                cap = cv2.VideoCapture(rtsp_url)
                
                if not cap.isOpened():
                    logger.error(f"无法打开相机 {camera_id}")
                    return False
                
                # 设置相机参数
                cap.set(cv2.CAP_PROP_FPS, self.config["fps"])
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config["resolution"]["width"])
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config["resolution"]["height"])
                
                self.cameras[camera_id] = cap
                self.is_recording[camera_id] = False
                
                logger.info(f"相机 {camera_id} 连接成功")
                return True
            else:
                logger.error(f"不支持的相机类型: {self.config['type']}")
                return False
                
        except Exception as e:
            logger.error(f"连接相机 {camera_id} 失败: {e}")
            return False
    
    async def start_capture(self, camera_id: str = "default", callback=None):
        """
        开始视频采集
        
        Args:
            camera_id: 相机ID
            callback: 帧回调函数
        """
        if camera_id not in self.cameras:
            await self.connect_camera(camera_id)
        
        if camera_id in self.capture_tasks:
            logger.warning(f"相机 {camera_id} 已在采集")
            return
        
        async def capture_loop():
            cap = self.cameras[camera_id]
            frame_count = 0
            
            while self.is_recording.get(camera_id, False):
                ret, frame = cap.read()
                if not ret:
                    logger.warning(f"相机 {camera_id} 读取帧失败")
                    await asyncio.sleep(0.01)
                    continue
                
                frame_count += 1
                timestamp = datetime.now()
                
                # 调用回调函数
                if callback:
                    await callback(frame, timestamp, frame_count)
                
                # 控制帧率
                await asyncio.sleep(1.0 / self.config["fps"])
        
        self.is_recording[camera_id] = True
        task = asyncio.create_task(capture_loop())
        self.capture_tasks[camera_id] = task
        
        logger.info(f"相机 {camera_id} 开始采集")
    
    async def stop_capture(self, camera_id: str = "default"):
        """
        停止视频采集
        
        Args:
            camera_id: 相机ID
        """
        if camera_id in self.is_recording:
            self.is_recording[camera_id] = False
        
        if camera_id in self.capture_tasks:
            task = self.capture_tasks[camera_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.capture_tasks[camera_id]
        
        logger.info(f"相机 {camera_id} 停止采集")
    
    async def stop_all(self):
        """停止所有相机采集"""
        for camera_id in list(self.capture_tasks.keys()):
            await self.stop_capture(camera_id)
        
        # 释放所有相机资源
        for camera_id, cap in self.cameras.items():
            cap.release()
        
        self.cameras.clear()
        logger.info("所有相机已停止")
    
    def get_frame(self, camera_id: str = "default") -> Optional[np.ndarray]:
        """
        获取单帧图像
        
        Args:
            camera_id: 相机ID
            
        Returns:
            图像数组，失败返回None
        """
        if camera_id not in self.cameras:
            return None
        
        cap = self.cameras[camera_id]
        ret, frame = cap.read()
        
        if ret:
            return frame
        return None
