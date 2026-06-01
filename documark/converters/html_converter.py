"""
HTML 转换器
"""

import re
from pathlib import Path
from typing import Dict, Any

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    from markdownify import markdownify as md
    MARKDOWNIFY_AVAILABLE = True
except ImportError:
    MARKDOWNIFY_AVAILABLE = False

from .base import BaseConverter


class HTMLConverter(BaseConverter):
    """
    HTML网页转换器
    
    将.html, .htm文件转换为Markdown格式
    """
    
    CATEGORY = "网页"
    
    def convert(self, file_path: Path) -> str:
        """
        将HTML转换为Markdown
        
        Args:
            file_path: HTML文件路径
            
        Returns:
            Markdown格式的文本内容
        """
        html_content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        if MARKDOWNIFY_AVAILABLE:
            return self._convert_with_markdownify(html_content, file_path)
        elif BS4_AVAILABLE:
            return self._convert_with_bs4(html_content, file_path)
        else:
            raise ImportError("请安装 beautifulsoup4 或 markdownify: pip install beautifulsoup4 markdownify")
    
    def _convert_with_markdownify(self, html_content: str, file_path: Path) -> str:
        """使用markdownify转换"""
        # 添加文档标题
        header = self._create_header(f"网页: {file_path.stem}", 1)
        header += "---\n\n"
        
        # 转换HTML到Markdown
        markdown_content = md(html_content, heading_style="ATX")
        
        return header + markdown_content
    
    def _convert_with_bs4(self, html_content: str, file_path: Path) -> str:
        """使用BeautifulSoup转换"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        content_parts = []
        
        # 添加文档标题
        content_parts.append(self._create_header(f"网页: {file_path.stem}", 1))
        content_parts.append("---\n\n")
        
        # 移除脚本和样式标签
        for script in soup(["script", "style"]):
            script.decompose()
        
        # 提取标题
        title = soup.find('title')
        if title:
            content_parts.append(self._create_header(title.get_text().strip(), 2))
        
        # 提取主要内容
        # 优先查找主要内容区域
        main_content = None
        for selector in ['main', 'article', '[role="main"]', '.content', '#content', '.main', '#main']:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.body
        
        if main_content:
            content_parts.append(self._process_element(main_content))
        
        return "".join(content_parts)
    
    def _process_element(self, element) -> str:
        """递归处理HTML元素"""
        content_parts = []
        
        for child in element.children:
            if child.name is None:  # 文本节点
                text = str(child).strip()
                if text:
                    content_parts.append(text)
            elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(child.name[1])
                text = child.get_text().strip()
                if text:
                    content_parts.append(self._create_header(text, level))
            elif child.name in ['p', 'div']:
                text = child.get_text().strip()
                if text:
                    content_parts.append(text + "\n\n")
            elif child.name == 'br':
                content_parts.append("\n")
            elif child.name in ['ul', 'ol']:
                content_parts.append(self._process_list(child))
            elif child.name == 'a':
                href = child.get('href', '')
                text = child.get_text().strip()
                if href and text:
                    content_parts.append(self._create_link(text, href))
                elif text:
                    content_parts.append(text)
            elif child.name == 'img':
                src = child.get('src', '')
                alt = child.get('alt', '')
                if src:
                    content_parts.append(self._create_image(alt, src))
            elif child.name == 'table':
                content_parts.append(self._process_table(child))
            elif child.name in ['strong', 'b']:
                text = child.get_text().strip()
                if text:
                    content_parts.append(f"**{text}**")
            elif child.name in ['em', 'i']:
                text = child.get_text().strip()
                if text:
                    content_parts.append(f"*{text}*")
            elif child.name == 'code':
                text = child.get_text().strip()
                if text:
                    content_parts.append(f"`{text}`")
            elif child.name == 'pre':
                text = child.get_text().strip()
                if text:
                    content_parts.append(self._create_code_block(text))
            else:
                # 递归处理其他元素
                content_parts.append(self._process_element(child))
        
        return "".join(content_parts)
    
    def _process_list(self, element) -> str:
        """处理列表"""
        items = []
        is_ordered = element.name == 'ol'
        
        for li in element.find_all('li', recursive=False):
            text = li.get_text().strip()
            if text:
                if is_ordered:
                    items.append(f"1. {text}")
                else:
                    items.append(f"- {text}")
        
        return "\n".join(items) + "\n\n"
    
    def _process_table(self, table) -> str:
        """处理表格"""
        rows = table.find_all('tr')
        if not rows:
            return ""
        
        rows_data = []
        for row in rows:
            cells = row.find_all(['td', 'th'])
            row_data = [cell.get_text().strip() for cell in cells]
            rows_data.append(row_data)
        
        if not rows_data:
            return ""
        
        # 检测是否有表头
        headers = rows_data[0]
        data_rows = rows_data[1:] if len(rows_data) > 1 else []
        
        return self._create_table(headers, data_rows)
