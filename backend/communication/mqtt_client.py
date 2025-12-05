"""
MQTT客户端 - 负责与Viewer端通信
"""
import asyncio
import json
import logging
from typing import Optional, Callable
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class MQTTClient:
    """MQTT客户端"""
    
    def __init__(self, broker: str, port: int = 1883, 
                 username: Optional[str] = None, 
                 password: Optional[str] = None,
                 topic_prefix: str = "nozzle/inspection"):
        """
        初始化MQTT客户端
        
        Args:
            broker: MQTT broker地址
            port: MQTT端口
            username: 用户名
            password: 密码
            topic_prefix: 主题前缀
        """
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.topic_prefix = topic_prefix
        self.client: Optional[mqtt.Client] = None
        self.connected = False
        self.callbacks: Dict[str, Callable] = {}
    
    async def connect(self):
        """连接MQTT broker"""
        try:
            self.client = mqtt.Client()
            
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            
            # 设置回调
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_message = self._on_message
            
            # 连接
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            
            # 等待连接
            await asyncio.sleep(1)
            
            if self.connected:
                logger.info(f"MQTT连接成功: {self.broker}:{self.port}")
            else:
                logger.error("MQTT连接失败")
                
        except Exception as e:
            logger.error(f"MQTT连接异常: {e}")
    
    def _on_connect(self, client, userdata, flags, rc):
        """连接回调"""
        if rc == 0:
            self.connected = True
            logger.info("MQTT连接成功")
            
            # 订阅配置更新主题
            config_topic = f"{self.topic_prefix}/config/update"
            client.subscribe(config_topic)
            logger.info(f"订阅主题: {config_topic}")
        else:
            logger.error(f"MQTT连接失败，错误码: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """断开连接回调"""
        self.connected = False
        logger.warning("MQTT断开连接")
    
    def _on_message(self, client, userdata, msg):
        """消息接收回调"""
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode('utf-8'))
            
            logger.debug(f"收到MQTT消息: {topic}")
            
            # 调用注册的回调函数
            if topic in self.callbacks:
                callback = self.callbacks[topic]
                asyncio.create_task(callback(payload))
                
        except Exception as e:
            logger.error(f"处理MQTT消息失败: {e}")
    
    async def publish_result(self, result: dict):
        """
        发布检测结果
        
        Args:
            result: 检测结果字典
        """
        if not self.connected or not self.client:
            logger.warning("MQTT未连接，无法发布消息")
            return
        
        topic = f"{self.topic_prefix}/result"
        payload = json.dumps(result, ensure_ascii=False)
        
        try:
            self.client.publish(topic, payload, qos=1)
            logger.debug(f"发布检测结果: {topic}")
        except Exception as e:
            logger.error(f"发布MQTT消息失败: {e}")
    
    async def publish_alarm(self, alarm: dict):
        """
        发布报警信息
        
        Args:
            alarm: 报警信息字典
        """
        if not self.connected or not self.client:
            return
        
        topic = f"{self.topic_prefix}/alarm"
        payload = json.dumps(alarm, ensure_ascii=False)
        
        try:
            self.client.publish(topic, payload, qos=1)
            logger.info(f"发布报警: {alarm}")
        except Exception as e:
            logger.error(f"发布报警失败: {e}")
    
    def subscribe_config(self, callback: Callable):
        """
        订阅配置更新
        
        Args:
            callback: 配置更新回调函数
        """
        topic = f"{self.topic_prefix}/config/update"
        self.callbacks[topic] = callback
    
    async def disconnect(self):
        """断开MQTT连接"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
            logger.info("MQTT已断开连接")
