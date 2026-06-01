"""
DocuMark 基础转换器类
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional


class BaseConverter(ABC):
    """
    文档转换器基类
    
    所有具体转换器都应继承此类
    """
    
    # 转换器类别
    CATEGORY = "未知"
    
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        初始化转换器
        
        Args:
            options: 转换选项字典
        """
        self.options = options or {}
        self.config = {
            'preserve_images': self.options.get('preserve_images', True),
            'extract_tables': self.options.get('extract_tables', True),
            'extract_links': self.options.get('extract_links', True),
            'ocr_enabled': self.options.get('ocr_enabled', False),
            'ocr_language': self.options.get('ocr_language', 'chi_sim+eng'),
            'min_text_length': self.options.get('min_text_length', 10),
        }
    
    @abstractmethod
    def convert(self, file_path: Path) -> str:
        """
        将文件转换为Markdown
        
        Args:
            file_path: 输入文件路径
            
        Returns:
            Markdown格式的文本内容
        """
        pass
    
    def _clean_text(self, text: str) -> str:
        """
        清理文本内容
        
        Args:
            text: 原始文本
            
        Returns:
            清理后的文本
        """
        if not text:
            return ""
        
        # 移除多余的空白字符
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # 移除行尾空白
            line = line.rstrip()
            # 将制表符替换为空格
            line = line.replace('\t', '    ')
            cleaned_lines.append(line)
        
        # 合并连续的空白行
        result = []
        prev_empty = False
        
        for line in cleaned_lines:
            is_empty = not line.strip()
            if is_empty and prev_empty:
                continue
            result.append(line)
            prev_empty = is_empty
        
        return '\n'.join(result)
    
    def _escape_markdown(self, text: str) -> str:
        """
        转义Markdown特殊字符
        
        Args:
            text: 原始文本
            
        Returns:
            转义后的文本
        """
        # 需要转义的Markdown字符
        chars_to_escape = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!', '|']
        
        for char in chars_to_escape:
            text = text.replace(char, '\\' + char)
        
        return text
    
    def _create_header(self, title: str, level: int = 1) -> str:
        """
        创建Markdown标题
        
        Args:
            title: 标题文本
            level: 标题级别 (1-6)
            
        Returns:
            Markdown标题
        """
        level = max(1, min(6, level))
        return f"{'#' * level} {title}\n\n"
    
    def _create_table(self, headers: list, rows: list) -> str:
        """
        创建Markdown表格
        
        Args:
            headers: 表头列表
            rows: 数据行列表（每行是一个列表）
            
        Returns:
            Markdown表格
        """
        if not headers or not rows:
            return ""
        
        # 转义单元格内容
        def escape_cell(cell):
            if cell is None:
                return ""
            cell = str(cell).replace('|', '\\|').replace('\n', ' ')
            return cell
        
        # 表头
        header_line = "| " + " | ".join(escape_cell(h) for h in headers) + " |"
        separator = "| " + " | ".join("---" for _ in headers) + " |"
        
        # 数据行
        row_lines = []
        for row in rows:
            row_line = "| " + " | ".join(escape_cell(cell) for cell in row) + " |"
            row_lines.append(row_line)
        
        return "\n".join([header_line, separator] + row_lines) + "\n\n"
    
    def _create_code_block(self, code: str, language: str = "") -> str:
        """
        创建Markdown代码块
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            Markdown代码块
        """
        return f"```{language}\n{code}\n```\n\n"
    
    def _create_link(self, text: str, url: str) -> str:
        """
        创建Markdown链接
        
        Args:
            text: 链接文本
            url: 链接地址
            
        Returns:
            Markdown链接
        """
        return f"[{text}]({url})"
    
    def _create_image(self, alt_text: str, url: str) -> str:
        """
        创建Markdown图片
        
        Args:
            alt_text: 替代文本
            url: 图片地址
            
        Returns:
            Markdown图片
        """
        return f"![{alt_text}]({url})"
