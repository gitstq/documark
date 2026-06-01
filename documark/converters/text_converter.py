"""
Text 转换器
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any

from .base import BaseConverter


class TextConverter(BaseConverter):
    """
    纯文本转换器
    
    将.txt, .md, .json, .xml, .yaml等文本文件转换为Markdown格式
    """
    
    CATEGORY = "文本"
    
    def convert(self, file_path: Path) -> str:
        """
        将文本文件转换为Markdown
        
        Args:
            file_path: 文本文件路径
            
        Returns:
            Markdown格式的文本内容
        """
        ext = file_path.suffix.lower()
        
        if ext == '.json':
            return self._convert_json(file_path)
        elif ext == '.xml':
            return self._convert_xml(file_path)
        elif ext in ['.yaml', '.yml']:
            return self._convert_yaml(file_path)
        elif ext in ['.txt', '.md']:
            return self._convert_text(file_path)
        else:
            return self._convert_text(file_path)
    
    def _convert_text(self, file_path: Path) -> str:
        """转换纯文本文件"""
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # 如果是markdown文件，直接返回
        if file_path.suffix.lower() == '.md':
            return content
        
        content_parts = []
        
        # 添加文档标题
        content_parts.append(self._create_header(f"文本: {file_path.stem}", 1))
        content_parts.append("---\n\n")
        
        # 将文本包装为代码块
        content_parts.append(self._create_code_block(content, "text"))
        
        return "".join(content_parts)
    
    def _convert_json(self, file_path: Path) -> str:
        """转换JSON文件"""
        content_parts = []
        
        # 添加文档标题
        content_parts.append(self._create_header(f"JSON: {file_path.stem}", 1))
        content_parts.append("---\n\n")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 格式化JSON
            formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
            content_parts.append(self._create_code_block(formatted_json, "json"))
            
        except json.JSONDecodeError as e:
            # 如果解析失败，作为普通文本处理
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            content_parts.append(f"*JSON解析错误: {str(e)}*\n\n")
            content_parts.append(self._create_code_block(content, "text"))
        
        return "".join(content_parts)
    
    def _convert_xml(self, file_path: Path) -> str:
        """转换XML文件"""
        content_parts = []
        
        # 添加文档标题
        content_parts.append(self._create_header(f"XML: {file_path.stem}", 1))
        content_parts.append("---\n\n")
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # 显示XML结构
            content_parts.append(self._create_header("XML结构", 2))
            content_parts.append(self._process_xml_element(root, 0))
            content_parts.append("\n")
            
        except ET.ParseError as e:
            # 如果解析失败，作为普通文本处理
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            content_parts.append(f"*XML解析错误: {str(e)}*\n\n")
            content_parts.append(self._create_code_block(content, "xml"))
        
        return "".join(content_parts)
    
    def _process_xml_element(self, element, depth: int) -> str:
        """递归处理XML元素"""
        indent = "  " * depth
        content_parts = []
        
        # 元素标签
        tag_name = element.tag.split('}')[-1] if '}' in element.tag else element.tag
        
        # 属性
        attrs = ""
        if element.attrib:
            attr_str = " ".join(f'{k}="{v}"' for k, v in element.attrib.items())
            attrs = f" {attr_str}"
        
        # 文本内容
        text = element.text.strip() if element.text else ""
        
        if text:
            content_parts.append(f"{indent}- **<{tag_name}{attrs}>**: {text}")
        else:
            content_parts.append(f"{indent}- **<{tag_name}{attrs}>**")
        
        # 子元素
        for child in element:
            content_parts.append(self._process_xml_element(child, depth + 1))
        
        return "\n".join(content_parts)
    
    def _convert_yaml(self, file_path: Path) -> str:
        """转换YAML文件"""
        content_parts = []
        
        # 添加文档标题
        content_parts.append(self._create_header(f"YAML: {file_path.stem}", 1))
        content_parts.append("---\n\n")
        
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        content_parts.append(self._create_code_block(content, "yaml"))
        
        return "".join(content_parts)
