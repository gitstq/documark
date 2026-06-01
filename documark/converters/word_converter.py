"""
Word 转换器
"""

from pathlib import Path
from typing import Dict, Any, List

try:
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

from .base import BaseConverter


class WordConverter(BaseConverter):
    """
    Word文档转换器
    
    将.docx文件转换为Markdown格式
    """
    
    CATEGORY = "文档"
    
    def convert(self, file_path: Path) -> str:
        """
        将Word文档转换为Markdown
        
        Args:
            file_path: Word文件路径
            
        Returns:
            Markdown格式的文本内容
        """
        if not DOCX_AVAILABLE:
            raise ImportError("请安装 python-docx: pip install python-docx")
        
        doc = Document(file_path)
        content_parts = []
        
        # 添加文档标题
        content_parts.append(self._create_header(f"文档: {file_path.stem}", 1))
        content_parts.append("---\n\n")
        
        # 遍历文档元素
        for element in doc.element.body:
            if element.tag.endswith('p'):  # 段落
                paragraph = Paragraph(element, doc)
                content_parts.append(self._process_paragraph(paragraph))
            elif element.tag.endswith('tbl'):  # 表格
                table = Table(element, doc)
                content_parts.append(self._process_table(table))
        
        return "".join(content_parts)
    
    def _process_paragraph(self, paragraph: Paragraph) -> str:
        """处理段落"""
        if not paragraph.text.strip():
            return "\n"
        
        # 获取段落样式
        style_name = paragraph.style.name if paragraph.style else "Normal"
        
        # 根据样式确定标题级别
        text = paragraph.text
        
        if style_name.startswith('Heading'):
            try:
                level = int(style_name.replace('Heading ', ''))
                return self._create_header(text, level)
            except ValueError:
                pass
        
        # 处理文本格式
        formatted_text = ""
        for run in paragraph.runs:
            run_text = run.text
            
            # 应用格式
            if run.bold:
                run_text = f"**{run_text}**"
            if run.italic:
                run_text = f"*{run_text}*"
            if run.underline:
                run_text = f"<u>{run_text}</u>"
            
            formatted_text += run_text
        
        return formatted_text + "\n\n"
    
    def _process_table(self, table: Table) -> str:
        """处理表格"""
        if not table.rows:
            return ""
        
        rows_data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            rows_data.append(row_data)
        
        if not rows_data:
            return ""
        
        # 第一行作为表头
        headers = rows_data[0]
        data_rows = rows_data[1:] if len(rows_data) > 1 else []
        
        return self._create_table(headers, data_rows)
