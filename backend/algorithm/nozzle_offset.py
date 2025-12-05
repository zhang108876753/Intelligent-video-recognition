"""
喷嘴偏移距离检测算法
"""
import numpy as np
import cv2
from typing import Dict, Any, Optional, Tuple
from .base import DetectionAlgorithm


class NozzleOffsetDetection(DetectionAlgorithm):
    """喷嘴偏移距离检测"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化算法
        
        Args:
            config: 配置字典，包含threshold_mm等参数
        """
        super().__init__(config)
        self.threshold_mm = config.get('threshold_mm', 0.1)
        self.template: Optional[np.ndarray] = None
        self.standard_position: Optional[Tuple[int, int]] = None
    
    def set_template(self, template: np.ndarray, standard_position: Tuple[int, int]):
        """
        设置标准模板和位置
        
        Args:
            template: 标准喷嘴模板图像
            standard_position: 标准位置 (x, y)
        """
        self.template = template
        self.standard_position = standard_position
    
    def detect(self, image: np.ndarray, roi: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        执行检测
        
        Args:
            image: 输入图像
            roi: 感兴趣区域（可选）
            
        Returns:
            检测结果字典
        """
        if roi is not None:
            search_image = roi
        else:
            search_image = image
        
        if self.template is None or self.standard_position is None:
            return {
                'algorithm_name': 'nozzle_offset',
                'status': 'error',
                'error': '模板或标准位置未设置',
                'result': {}
            }
        
        # 模板匹配
        result = cv2.matchTemplate(search_image, self.template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # 亚像素级定位
        if max_val > 0.7:  # 匹配度阈值
            # 使用亚像素级定位提高精度
            center_x = max_loc[0] + self.template.shape[1] / 2
            center_y = max_loc[1] + self.template.shape[0] / 2
            
            # 计算像素偏移
            offset_x_pixel = center_x - self.standard_position[0]
            offset_y_pixel = center_y - self.standard_position[1]
            
            # 转换为物理距离（mm）
            offset_x_mm = self.pixel_to_physical(offset_x_pixel, 'x')
            offset_y_mm = self.pixel_to_physical(offset_y_pixel, 'y')
            offset_distance_mm = np.sqrt(offset_x_mm**2 + offset_y_mm**2)
            
            # 判断状态
            thresholds = {
                'warning': self.threshold_mm * 0.7,
                'error': self.threshold_mm
            }
            status = self._get_status(offset_distance_mm, thresholds)
            
            return {
                'algorithm_name': 'nozzle_offset',
                'status': status,
                'result': {
                    'offset_x_mm': round(offset_x_mm, 3),
                    'offset_y_mm': round(offset_y_mm, 3),
                    'offset_distance_mm': round(offset_distance_mm, 3),
                    'match_score': round(max_val, 3),
                    'center_position': (int(center_x), int(center_y))
                },
                'annotations': [
                    {
                        'type': 'point',
                        'coordinates': [(int(center_x), int(center_y))],
                        'color': (0, 255, 0) if status == 'normal' else (0, 0, 255),
                        'label': f'偏移: {offset_distance_mm:.3f}mm'
                    },
                    {
                        'type': 'line',
                        'coordinates': [
                            self.standard_position,
                            (int(center_x), int(center_y))
                        ],
                        'color': (255, 0, 0),
                        'thickness': 2
                    }
                ]
            }
        else:
            return {
                'algorithm_name': 'nozzle_offset',
                'status': 'error',
                'error': '模板匹配失败',
                'result': {
                    'match_score': round(max_val, 3)
                }
            }
    
    def annotate_result(self, image: np.ndarray, result: Dict[str, Any]) -> np.ndarray:
        """
        在图像上标注检测结果
        
        Args:
            image: 输入图像
            result: 检测结果
            
        Returns:
            标注后的图像
        """
        annotated = image.copy()
        
        if 'annotations' in result:
            for ann in result['annotations']:
                if ann['type'] == 'point':
                    for coord in ann['coordinates']:
                        cv2.circle(annotated, coord, 5, ann['color'], -1)
                        if 'label' in ann:
                            cv2.putText(annotated, ann['label'], 
                                      (coord[0] + 10, coord[1] - 10),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, ann['color'], 1)
                
                elif ann['type'] == 'line':
                    if len(ann['coordinates']) >= 2:
                        pt1 = ann['coordinates'][0]
                        pt2 = ann['coordinates'][1]
                        thickness = ann.get('thickness', 1)
                        cv2.line(annotated, pt1, pt2, ann['color'], thickness)
        
        # 标注标准位置
        if self.standard_position:
            cv2.circle(annotated, self.standard_position, 5, (0, 255, 255), 2)
            cv2.putText(annotated, '标准位置', 
                       (self.standard_position[0] + 10, self.standard_position[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        return annotated
