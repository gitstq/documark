"""
DocuMark - 智能文档转换器

将各种文件格式（PDF, Word, Excel, PowerPoint, HTML, 图片等）
转换为结构化的Markdown格式。

作者: gitstq
版本: 1.0.0
许可证: MIT
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from .converter import DocuMarkConverter
from .converters import *
from .utils import detect_file_type, get_supported_formats

__all__ = [
    "DocuMarkConverter",
    "detect_file_type",
    "get_supported_formats",
]
