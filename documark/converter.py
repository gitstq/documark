"""
DocuMark 核心转换器
"""

import os
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.text import Text

from .utils import detect_file_type, get_supported_formats, ensure_dir
from .converters import (
    PDFConverter,
    WordConverter,
    ExcelConverter,
    PowerPointConverter,
    HTMLConverter,
    ImageConverter,
    TextConverter,
)

console = Console()


class DocuMarkConverter:
    """
    DocuMark 智能文档转换器主类
    
    支持将多种文件格式转换为Markdown格式
    """
    
    # 文件扩展名到转换器的映射
    CONVERTERS = {
        # PDF
        '.pdf': PDFConverter,
        # Word
        '.doc': WordConverter,
        '.docx': WordConverter,
        # Excel
        '.xls': ExcelConverter,
        '.xlsx': ExcelConverter,
        '.csv': ExcelConverter,
        # PowerPoint
        '.ppt': PowerPointConverter,
        '.pptx': PowerPointConverter,
        # HTML
        '.html': HTMLConverter,
        '.htm': HTMLConverter,
        # Image (OCR)
        '.png': ImageConverter,
        '.jpg': ImageConverter,
        '.jpeg': ImageConverter,
        '.gif': ImageConverter,
        '.bmp': ImageConverter,
        '.tiff': ImageConverter,
        '.webp': ImageConverter,
        # Text
        '.txt': TextConverter,
        '.md': TextConverter,
        '.json': TextConverter,
        '.xml': TextConverter,
        '.yaml': TextConverter,
        '.yml': TextConverter,
    }
    
    def __init__(self, output_dir: Optional[str] = None, max_workers: int = 4):
        """
        初始化转换器
        
        Args:
            output_dir: 输出目录，默认为当前目录
            max_workers: 并行处理的最大线程数
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.max_workers = max_workers
        self.stats = {
            'success': 0,
            'failed': 0,
            'skipped': 0,
        }
    
    def convert(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        转换单个文件
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径（可选）
            options: 转换选项
            
        Returns:
            转换后的Markdown内容
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"文件不存在: {input_path}")
        
        # 检测文件类型
        file_ext = input_path.suffix.lower()
        
        if file_ext not in self.CONVERTERS:
            raise ValueError(f"不支持的文件格式: {file_ext}")
        
        # 获取转换器
        converter_class = self.CONVERTERS[file_ext]
        converter = converter_class(options or {})
        
        # 执行转换
        try:
            content = converter.convert(input_path)
            
            # 保存到文件
            if output_path:
                output_path = Path(output_path)
            else:
                output_path = self.output_dir / f"{input_path.stem}.md"
            
            ensure_dir(output_path.parent)
            output_path.write_text(content, encoding='utf-8')
            
            self.stats['success'] += 1
            return content
            
        except Exception as e:
            self.stats['failed'] += 1
            console.print(f"[red]转换失败: {input_path} - {str(e)}[/red]")
            raise
    
    def convert_batch(
        self,
        input_paths: List[Union[str, Path]],
        output_dir: Optional[Union[str, Path]] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        批量转换文件
        
        Args:
            input_paths: 输入文件路径列表
            output_dir: 输出目录
            options: 转换选项
            
        Returns:
            转换后的Markdown内容列表
        """
        output_dir = Path(output_dir) if output_dir else self.output_dir
        ensure_dir(output_dir)
        
        results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            
            task = progress.add_task("[cyan]批量转换中...", total=len(input_paths))
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {}
                
                for input_path in input_paths:
                    input_path = Path(input_path)
                    output_path = output_dir / f"{input_path.stem}.md"
                    
                    future = executor.submit(
                        self._convert_safe,
                        input_path,
                        output_path,
                        options
                    )
                    futures[future] = input_path
                
                for future in as_completed(futures):
                    input_path = futures[future]
                    try:
                        result = future.result()
                        results.append(result)
                        progress.update(task, advance=1)
                    except Exception as e:
                        console.print(f"[red]✗ {input_path.name}: {str(e)}[/red]")
                        progress.update(task, advance=1)
        
        return results
    
    def _convert_safe(
        self,
        input_path: Path,
        output_path: Path,
        options: Optional[Dict[str, Any]]
    ) -> str:
        """安全转换（用于线程池）"""
        try:
            content = self.convert(input_path, output_path, options)
            console.print(f"[green]✓ {input_path.name}[/green]")
            return content
        except Exception as e:
            raise e
    
    def convert_directory(
        self,
        input_dir: Union[str, Path],
        output_dir: Optional[Union[str, Path]] = None,
        recursive: bool = True,
        options: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        转换整个目录
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            recursive: 是否递归处理子目录
            options: 转换选项
            
        Returns:
            转换后的Markdown内容列表
        """
        input_dir = Path(input_dir)
        
        if not input_dir.is_dir():
            raise NotADirectoryError(f"不是有效的目录: {input_dir}")
        
        # 收集所有支持的文件
        files = []
        pattern = "**/*" if recursive else "*"
        
        for file_path in input_dir.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.CONVERTERS:
                files.append(file_path)
        
        if not files:
            console.print("[yellow]未找到可转换的文件[/yellow]")
            return []
        
        console.print(Panel(
            f"找到 [bold cyan]{len(files)}[/bold cyan] 个可转换文件",
            title="DocuMark",
            border_style="blue"
        ))
        
        return self.convert_batch(files, output_dir, options)
    
    def get_supported_formats(self) -> Dict[str, List[str]]:
        """获取支持的文件格式"""
        formats = {}
        for ext, converter_class in self.CONVERTERS.items():
            category = converter_class.CATEGORY
            if category not in formats:
                formats[category] = []
            formats[category].append(ext)
        return formats
    
    def print_stats(self):
        """打印转换统计信息"""
        console.print(Panel(
            f"[green]成功: {self.stats['success']}[/green] | "
            f"[red]失败: {self.stats['failed']}[/red] | "
            f"[yellow]跳过: {self.stats['skipped']}[/yellow]",
            title="转换统计",
            border_style="green"
        ))
