"""
PDF 转换器
"""

import re
from pathlib import Path
from typing import Dict, Any, List

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

from .base import BaseConverter


class PDFConverter(BaseConverter):
    """
    PDF文件转换器
    
    将PDF文件转换为Markdown格式
    """
    
    CATEGORY = "文档"
    
    def convert(self, file_path: Path) -> str:
        """
        将PDF转换为Markdown
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            Markdown格式的文本内容
        """
        if PDFPLUMBER_AVAILABLE:
            return self._convert_with_pdfplumber(file_path)
        elif PYPDF2_AVAILABLE:
            return self._convert_with_pypdf2(file_path)
        else:
            raise ImportError("请安装 pdfplumber 或 PyPDF2: pip install pdfplumber")
    
    def _convert_with_pdfplumber(self, file_path: Path) -> str:
        """使用pdfplumber转换PDF"""
        content_parts = []
        
        with pdfplumber.open(file_path) as pdf:
            # 添加文档标题
            content_parts.append(self._create_header(f"文档: {file_path.stem}", 1))
            content_parts.append(f"**页数**: {len(pdf.pages)}\n\n")
            content_parts.append("---\n\n")
            
            for page_num, page in enumerate(pdf.pages, 1):
                # 提取页面文本
                text = page.extract_text()
                
                if text and len(text.strip()) >= self.config['min_text_length']:
                    content_parts.append(self._create_header(f"第 {page_num} 页", 2))
                    
                    # 清理文本
                    text = self._clean_text(text)
                    content_parts.append(text)
                    content_parts.append("\n\n")
                
                # 提取表格
                if self.config['extract_tables']:
                    tables = page.extract_tables()
                    for table in tables:
                        if table and len(table) > 1:
                            headers = table[0]
                            rows = table[1:]
                            content_parts.append(self._create_table(headers, rows))
        
        return "".join(content_parts)
    
    def _convert_with_pypdf2(self, file_path: Path) -> str:
        """使用PyPDF2转换PDF"""
        content_parts = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # 添加文档标题
            content_parts.append(self._create_header(f"文档: {file_path.stem}", 1))
            content_parts.append(f"**页数**: {len(pdf_reader.pages)}\n\n")
            content_parts.append("---\n\n")
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                
                if text and len(text.strip()) >= self.config['min_text_length']:
                    content_parts.append(self._create_header(f"第 {page_num} 页", 2))
                    
                    # 清理文本
                    text = self._clean_text(text)
                    content_parts.append(text)
                    content_parts.append("\n\n")
        
        return "".join(content_parts)
