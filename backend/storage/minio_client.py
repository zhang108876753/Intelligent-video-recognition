"""
MinIO客户端 - 负责视频文件上传和管理
"""
import logging
from typing import Optional
from datetime import datetime
from minio import Minio
from minio.error import S3Error
import io

logger = logging.getLogger(__name__)


class MinIOClient:
    """MinIO客户端"""
    
    def __init__(self, endpoint: str, access_key: str, secret_key: str, 
                 secure: bool = False, bucket: str = "nozzle-videos"):
        """
        初始化MinIO客户端
        
        Args:
            endpoint: MinIO服务地址
            access_key: 访问密钥
            secret_key: 秘密密钥
            secure: 是否使用HTTPS
            bucket: 存储桶名称
        """
        self.endpoint = endpoint
        self.bucket = bucket
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        
        # 确保存储桶存在
        self._ensure_bucket()
    
    def _ensure_bucket(self):
        """确保存储桶存在"""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
                logger.info(f"创建存储桶: {self.bucket}")
        except S3Error as e:
            logger.error(f"创建存储桶失败: {e}")
    
    def upload_video(self, video_data: bytes, filename: str, 
                    metadata: Optional[dict] = None) -> Optional[str]:
        """
        上传视频文件
        
        Args:
            video_data: 视频数据（字节）
            filename: 文件名
            metadata: 元数据
            
        Returns:
            对象名称，失败返回None
        """
        try:
            # 生成对象名称（带时间戳）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            object_name = f"videos/{timestamp}_{filename}"
            
            # 上传
            data_stream = io.BytesIO(video_data)
            self.client.put_object(
                self.bucket,
                object_name,
                data_stream,
                length=len(video_data),
                content_type="video/mp4",
                metadata=metadata or {}
            )
            
            logger.info(f"视频上传成功: {object_name}")
            return object_name
            
        except S3Error as e:
            logger.error(f"视频上传失败: {e}")
            return None
    
    def get_video_url(self, object_name: str, expires_seconds: int = 3600) -> Optional[str]:
        """
        获取视频访问URL（预签名）
        
        Args:
            object_name: 对象名称
            expires_seconds: 过期时间（秒）
            
        Returns:
            URL，失败返回None
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket,
                object_name,
                expires=expires_seconds
            )
            return url
        except S3Error as e:
            logger.error(f"获取视频URL失败: {e}")
            return None
    
    def list_videos(self, prefix: str = "videos/", limit: int = 100) -> list:
        """
        列出视频文件
        
        Args:
            prefix: 前缀
            limit: 最大数量
            
        Returns:
            视频对象列表
        """
        try:
            objects = self.client.list_objects(
                self.bucket,
                prefix=prefix,
                recursive=True
            )
            
            videos = []
            count = 0
            for obj in objects:
                if count >= limit:
                    break
                videos.append({
                    "name": obj.object_name,
                    "size": obj.size,
                    "last_modified": obj.last_modified
                })
                count += 1
            
            return videos
            
        except S3Error as e:
            logger.error(f"列出视频失败: {e}")
            return []
    
    def delete_video(self, object_name: str) -> bool:
        """
        删除视频文件
        
        Args:
            object_name: 对象名称
            
        Returns:
            是否成功
        """
        try:
            self.client.remove_object(self.bucket, object_name)
            logger.info(f"删除视频: {object_name}")
            return True
        except S3Error as e:
            logger.error(f"删除视频失败: {e}")
            return False
