"""
PLC客户端 - 负责与PLC设备通信，监听录制信号
"""
import asyncio
import logging
from typing import Optional, Callable
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

logger = logging.getLogger(__name__)


class PLCClient:
    """PLC客户端"""
    
    def __init__(self, host: str, port: int = 502, slave_id: int = 1,
                 start_signal_address: int = 0, stop_signal_address: int = 1):
        """
        初始化PLC客户端
        
        Args:
            host: PLC IP地址
            port: Modbus端口
            slave_id: 从站ID
            start_signal_address: 开始信号地址
            stop_signal_address: 停止信号地址
        """
        self.host = host
        self.port = port
        self.slave_id = slave_id
        self.start_signal_address = start_signal_address
        self.stop_signal_address = stop_signal_address
        self.client: Optional[ModbusTcpClient] = None
        self.connected = False
        self.monitoring = False
        self.monitor_task: Optional[asyncio.Task] = None
        self.start_callback: Optional[Callable] = None
        self.stop_callback: Optional[Callable] = None
    
    async def connect(self) -> bool:
        """
        连接PLC
        
        Returns:
            是否连接成功
        """
        try:
            self.client = ModbusTcpClient(host=self.host, port=self.port)
            
            if self.client.connect():
                self.connected = True
                logger.info(f"PLC连接成功: {self.host}:{self.port}")
                return True
            else:
                logger.error(f"PLC连接失败: {self.host}:{self.port}")
                return False
                
        except Exception as e:
            logger.error(f"PLC连接异常: {e}")
            return False
    
    async def disconnect(self):
        """断开PLC连接"""
        if self.monitoring:
            await self.stop_monitoring()
        
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("PLC已断开连接")
    
    async def read_coil(self, address: int) -> Optional[bool]:
        """
        读取线圈状态
        
        Args:
            address: 地址
            
        Returns:
            线圈状态，失败返回None
        """
        if not self.connected or not self.client:
            return None
        
        try:
            result = self.client.read_coils(address, 1, slave=self.slave_id)
            if result.isError():
                logger.error(f"读取线圈失败: {result}")
                return None
            return result.bits[0]
        except ModbusException as e:
            logger.error(f"读取线圈异常: {e}")
            return None
    
    async def write_coil(self, address: int, value: bool) -> bool:
        """
        写入线圈状态
        
        Args:
            address: 地址
            value: 值
            
        Returns:
            是否成功
        """
        if not self.connected or not self.client:
            return False
        
        try:
            result = self.client.write_coil(address, value, slave=self.slave_id)
            if result.isError():
                logger.error(f"写入线圈失败: {result}")
                return False
            return True
        except ModbusException as e:
            logger.error(f"写入线圈异常: {e}")
            return False
    
    async def start_monitoring(self, start_callback: Callable, stop_callback: Callable,
                              interval: float = 0.1):
        """
        开始监听PLC信号
        
        Args:
            start_callback: 开始信号回调函数
            stop_callback: 停止信号回调函数
            interval: 检查间隔（秒）
        """
        if self.monitoring:
            logger.warning("已在监听中")
            return
        
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.monitoring = True
        
        async def monitor_loop():
            prev_start_signal = False
            prev_stop_signal = False
            
            while self.monitoring:
                try:
                    # 读取开始信号
                    start_signal = await self.read_coil(self.start_signal_address)
                    if start_signal is not None and start_signal and not prev_start_signal:
                        logger.info("检测到开始信号")
                        if self.start_callback:
                            await self.start_callback()
                    
                    # 读取停止信号
                    stop_signal = await self.read_coil(self.stop_signal_address)
                    if stop_signal is not None and stop_signal and not prev_stop_signal:
                        logger.info("检测到停止信号")
                        if self.stop_callback:
                            await self.stop_callback()
                    
                    prev_start_signal = start_signal if start_signal is not None else prev_start_signal
                    prev_stop_signal = stop_signal if stop_signal is not None else prev_stop_signal
                    
                    await asyncio.sleep(interval)
                    
                except Exception as e:
                    logger.error(f"监听PLC信号异常: {e}")
                    await asyncio.sleep(interval)
        
        self.monitor_task = asyncio.create_task(monitor_loop())
        logger.info("开始监听PLC信号")
    
    async def stop_monitoring(self):
        """停止监听PLC信号"""
        if not self.monitoring:
            return
        
        self.monitoring = False
        
        if self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
        
        logger.info("停止监听PLC信号")
