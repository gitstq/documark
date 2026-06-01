#!/usr/bin/env python3
"""
DocuMark CLI - 命令行接口
"""

import sys
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from .converter import DocuMarkConverter
from .utils import get_supported_formats, format_file_size
from . import __version__

app = typer.Typer(
    name="documark",
    help="DocuMark - 智能文档转换器",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """版本信息回调"""
    if value:
        console.print(f"[bold cyan]DocuMark[/bold cyan] 版本 [green]{__version__}[/green]")
        raise typer.Exit()


@app.command()
def convert(
    input_path: str = typer.Argument(..., help="输入文件或目录路径"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="输出文件或目录路径"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="递归处理子目录"),
    workers: int = typer.Option(4, "--workers", "-w", help="并行处理的线程数"),
    ocr: bool = typer.Option(False, "--ocr", help="启用图片OCR识别"),
    ocr_lang: str = typer.Option("chi_sim+eng", "--ocr-lang", help="OCR识别语言"),
    no_tables: bool = typer.Option(False, "--no-tables", help="不提取表格"),
    no_links: bool = typer.Option(False, "--no-links", help="不提取链接"),
):
    """
    转换文件为Markdown格式
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        console.print(f"[red]错误: 路径不存在 - {input_path}[/red]")
        raise typer.Exit(1)
    
    # 构建选项
    options = {
        'ocr_enabled': ocr,
        'ocr_language': ocr_lang,
        'extract_tables': not no_tables,
        'extract_links': not no_links,
    }
    
    # 创建转换器
    converter = DocuMarkConverter(
        output_dir=Path(output) if output else None,
        max_workers=workers
    )
    
    try:
        if input_path.is_file():
            # 单个文件转换
            result = converter.convert(input_path, output, options)
            console.print(f"[green]✓[/green] 转换成功: [cyan]{input_path.name}[/cyan]")
            
            if output:
                console.print(f"  输出: [blue]{output}[/blue]")
            
        elif input_path.is_dir():
            # 目录转换
            results = converter.convert_directory(
                input_path,
                output,
                recursive=recursive,
                options=options
            )
            
            converter.print_stats()
        
    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def batch(
    files: List[str] = typer.Argument(..., help="输入文件路径列表"),
    output_dir: Optional[str] = typer.Option(None, "--output-dir", "-o", help="输出目录"),
    workers: int = typer.Option(4, "--workers", "-w", help="并行处理的线程数"),
    ocr: bool = typer.Option(False, "--ocr", help="启用图片OCR识别"),
):
    """
    批量转换多个文件
    """
    input_paths = [Path(f) for f in files]
    
    # 验证文件
    for path in input_paths:
        if not path.exists():
            console.print(f"[red]错误: 文件不存在 - {path}[/red]")
            raise typer.Exit(1)
    
    # 构建选项
    options = {
        'ocr_enabled': ocr,
    }
    
    # 创建转换器
    converter = DocuMarkConverter(
        output_dir=Path(output_dir) if output_dir else None,
        max_workers=workers
    )
    
    try:
        results = converter.convert_batch(input_paths, output_dir, options)
        converter.print_stats()
        
    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def formats():
    """
    显示支持的文件格式
    """
    table = Table(
        title="[bold cyan]DocuMark 支持的文件格式[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("类别", style="cyan", no_wrap=True)
    table.add_column("扩展名", style="green")
    
    formats_dict = get_supported_formats()
    
    for category, extensions in formats_dict.items():
        ext_str = ", ".join([f"[bold]{ext}[/bold]" for ext in extensions])
        table.add_row(category, ext_str)
    
    console.print()
    console.print(table)
    console.print()
    console.print(Panel(
        "[dim]使用 [bold]documark convert <文件>[/bold] 开始转换[/dim]",
        border_style="blue"
    ))


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v",
        callback=version_callback,
        is_eager=True,
        help="显示版本信息"
    ),
):
    """
    DocuMark - 智能文档转换器
    
    将各种文件格式（PDF, Word, Excel, PowerPoint, HTML, 图片等）
    转换为结构化的Markdown格式。
    
    示例:
        documark convert document.pdf
        documark convert document.docx -o output.md
        documark convert ./documents -r -o ./output
        documark batch file1.pdf file2.docx -o ./output
        documark formats
    """
    pass


def main_entry():
    """入口函数"""
    app()


if __name__ == "__main__":
    main_entry()
