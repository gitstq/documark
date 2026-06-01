"""
DocuMark 工具函数
"""

import os
import mimetypes
from pathlib import Path
from typing import Optional, Dict, List


def detect_file_type(file_path: Union[str, Path]) -> str:
    """
    检测文件类型
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件MIME类型
    """
    file_path = Path(file_path)
    
    # 首先尝试通过扩展名检测
    mime_type, _ = mimetypes.guess_type(str(file_path))
    
    if mime_type:
        return mime_type
    
    # 回退到扩展名映射
    ext = file_path.suffix.lower()
    mime_map = {
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.html': 'text/html',
        '.htm': 'text/html',
        '.txt': 'text/plain',
        '.md': 'text/markdown',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.yaml': 'application/x-yaml',
        '.yml': 'application/x-yaml',
        '.csv': 'text/csv',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.tiff': 'image/tiff',
        '.webp': 'image/webp',
    }
    
    return mime_map.get(ext, 'application/octet-stream')


def ensure_dir(dir_path: Path) -> Path:
    """
    确保目录存在
    
    Args:
        dir_path: 目录路径
        
    Returns:
        目录路径
    """
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_supported_formats() -> Dict[str, List[str]]:
    """
    获取支持的文件格式
    
    Returns:
        格式分类字典
    """
    return {
        '文档': ['.pdf', '.doc', '.docx', '.txt', '.md'],
        '表格': ['.xls', '.xlsx', '.csv'],
        '演示': ['.ppt', '.pptx'],
        '网页': ['.html', '.htm'],
        '图片': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'],
        '数据': ['.json', '.xml', '.yaml', '.yml'],
    }


def sanitize_filename(filename: str) -> str:
    """
    清理文件名中的非法字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        清理后的文件名
    """
    # Windows和Unix的非法字符
    illegal_chars = '<>:"/\\|?*'
    
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    
    # 移除控制字符
    filename = ''.join(char for char in filename if ord(char) >= 32)
    
    # 限制长度
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200 - len(ext)] + ext
    
    return filename.strip()


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        格式化后的文件大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断文本
    
    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 后缀
        
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


# 类型提示
from typing import Union
