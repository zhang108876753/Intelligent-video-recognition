"""
检测算法基类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import numpy as np
import cv2


class DetectionAlgorithm(ABC):
    """检测算法基类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化算法
        
        Args:
            config: 算法配置字典
        """
        self.config = config
        self.calibration_params: Optional[Dict[str, Any]] = None
    
    def set_calibration(self, calibration_params: Dict[str, Any]):
        """
        设置标定参数
        
        Args:
            calibration_params: 标定参数字典，包含pixel_size_x_mm, pixel_size_y_mm等
        """
        self.calibration_params = calibration_params
    
    def pixel_to_physical(self, pixel_value: float, axis: str = 'x') -> float:
        """
        像素值转换为物理值（mm）
        
        Args:
            pixel_value: 像素值
            axis: 坐标轴 ('x' 或 'y')
            
        Returns:
            物理值（mm）
        """
        if not self.calibration_params:
            raise ValueError("标定参数未设置")
        
        if axis == 'x':
            return pixel_value * self.calibration_params.get('pixel_size_x_mm', 0.005)
        else:
            return pixel_value * self.calibration_params.get('pixel_size_y_mm', 0.005)
    
    def physical_to_pixel(self, physical_value: float, axis: str = 'x') -> float:
        """
        物理值转换为像素值
        
        Args:
            physical_value: 物理值（mm）
            axis: 坐标轴 ('x' 或 'y')
            
        Returns:
            像素值
        """
        if not self.calibration_params:
            raise ValueError("标定参数未设置")
        
        if axis == 'x':
            return physical_value / self.calibration_params.get('pixel_size_x_mm', 0.005)
        else:
            return physical_value / self.calibration_params.get('pixel_size_y_mm', 0.005)
    
    @abstractmethod
    def detect(self, image: np.ndarray, roi: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        执行检测
        
        Args:
            image: 输入图像
            roi: 感兴趣区域（可选）
            
        Returns:
            检测结果字典
        """
        pass
    
    @abstractmethod
    def annotate_result(self, image: np.ndarray, result: Dict[str, Any]) -> np.ndarray:
        """
        在图像上标注检测结果
        
        Args:
            image: 输入图像
            result: 检测结果
            
        Returns:
            标注后的图像
        """
        pass
    
    def _extract_roi(self, image: np.ndarray, roi_box: Optional[tuple] = None) -> np.ndarray:
        """
        提取感兴趣区域
        
        Args:
            image: 输入图像
            roi_box: ROI框 (x, y, width, height)
            
        Returns:
            ROI图像
        """
        if roi_box is None:
            return image
        
        x, y, w, h = roi_box
        return image[y:y+h, x:x+w]
    
    def _get_status(self, value: float, thresholds: Dict[str, float]) -> str:
        """
        根据阈值判断状态
        
        Args:
            value: 检测值
            thresholds: 阈值字典 {'warning': 0.1, 'error': 0.2}
            
        Returns:
            状态: 'normal', 'warning', 'error'
        """
        if 'error' in thresholds and abs(value) > thresholds['error']:
            return 'error'
        elif 'warning' in thresholds and abs(value) > thresholds['warning']:
            return 'warning'
        else:
            return 'normal'
