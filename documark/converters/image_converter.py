"""
Image 转换器 (OCR)
"""

from pathlib import Path
from typing import Dict, Any

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

from .base import BaseConverter


class ImageConverter(BaseConverter):
    """
    图片OCR转换器
    
    将图片中的文字提取为Markdown格式
    """
    
    CATEGORY = "图片"
    
    def convert(self, file_path: Path) -> str:
        """
        将图片OCR转换为Markdown
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            Markdown格式的文本内容
        """
        if not PIL_AVAILABLE:
            raise ImportError("请安装 Pillow: pip install Pillow")
        
        if not TESSERACT_AVAILABLE:
            raise ImportError("请安装 pytesseract: pip install pytesseract")
        
        content_parts = []
        
        # 添加文档标题
        content_parts.append(self._create_header(f"图片: {file_path.stem}", 1))
        content_parts.append(f"**文件**: {file_path.name}\n\n")
        content_parts.append("---\n\n")
        
        # 打开图片
        image = Image.open(file_path)
        
        # 获取图片信息
        content_parts.append(self._create_header("图片信息", 2))
        content_parts.append(f"- **格式**: {image.format}\n")
        content_parts.append(f"- **尺寸**: {image.size[0]} x {image.size[1]}\n")
        content_parts.append(f"- **模式**: {image.mode}\n\n")
        
        # OCR识别
        if self.config['ocr_enabled']:
            content_parts.append(self._create_header("OCR识别结果", 2))
            
            try:
                # 设置OCR语言
                lang = self.config['ocr_language']
                text = pytesseract.image_to_string(image, lang=lang)
                
                if text.strip():
                    content_parts.append(self._clean_text(text))
                    content_parts.append("\n\n")
                else:
                    content_parts.append("*未识别到文本内容*\n\n")
                    
            except Exception as e:
                content_parts.append(f"*OCR识别失败: {str(e)}*\n\n")
        else:
            content_parts.append("*OCR未启用，使用 `--ocr` 参数启用文字识别*\n\n")
        
        # 添加图片引用
        content_parts.append(self._create_header("原始图片", 2))
        content_parts.append(self._create_image(file_path.stem, str(file_path)))
        content_parts.append("\n")
        
        return "".join(content_parts)
