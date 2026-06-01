<div align="center">

# 📄 DocuMark

**智能文档转换器 - 将各种文件格式一键转换为Markdown**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](https://github.com/gitstq/documark/releases)

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

**DocuMark** 是一款强大的智能文档转换工具，能够将各种常见文件格式（PDF、Word、Excel、PowerPoint、HTML、图片等）快速转换为结构化的Markdown格式。

**灵感来源**: 受到Microsoft MarkItDown项目的启发，DocuMark在此基础上进行了全面升级，支持更多文件格式、更美观的CLI界面、批量转换功能以及图片OCR识别。

**核心价值**:
- 🚀 一站式解决文档格式转换需求
- 🎨 保留原文档结构和格式
- 🤖 支持图片文字识别（OCR）
- ⚡ 批量处理与并行转换

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📑 **多格式支持** | PDF、Word、Excel、PowerPoint、HTML、图片、文本等 |
| 🎨 **美观CLI** | 基于Rich库的彩色终端界面与进度显示 |
| ⚡ **批量转换** | 支持目录递归处理与多线程并行转换 |
| 🤖 **OCR识别** | 图片文字智能识别（支持中英文）|
| 📊 **表格提取** | 自动识别并转换文档中的表格 |
| 🔗 **链接保留** | 保留原文档中的超链接信息 |
| 🛠️ **易于扩展** | 模块化设计，轻松添加新格式支持 |

### 🚀 快速开始

#### 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows、macOS、Linux

#### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/gitstq/documark.git
cd documark

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

#### 快速使用

```bash
# 转换单个文件
documark convert document.pdf
documark convert document.docx -o output.md

# 批量转换目录（递归）
documark convert ./documents -r -o ./output

# 启用OCR识别图片
documark convert image.png --ocr

# 查看支持的格式
documark formats
```

### 📖 详细使用指南

#### 命令行参数

```bash
# 基础转换
documark convert <输入路径> [选项]

# 选项说明
-o, --output PATH       # 指定输出路径
-r, --recursive         # 递归处理子目录
-w, --workers INTEGER   # 并行线程数（默认：4）
--ocr                   # 启用OCR识别
--ocr-lang TEXT         # OCR语言（默认：chi_sim+eng）
--no-tables             # 不提取表格
--no-links              # 不提取链接
```

#### Python API 使用

```python
from documark import DocuMarkConverter

# 创建转换器
converter = DocuMarkConverter(output_dir="./output")

# 转换单个文件
content = converter.convert("document.pdf")

# 批量转换
converter.convert_batch(["file1.pdf", "file2.docx"])

# 转换整个目录
converter.convert_directory("./documents", recursive=True)
```

### 💡 设计思路与迭代规划

#### 技术选型

- **pdfplumber/PyPDF2**: PDF解析与文本提取
- **python-docx**: Word文档处理
- **openpyxl**: Excel表格处理
- **python-pptx**: PowerPoint处理
- **BeautifulSoup**: HTML解析
- **pytesseract**: OCR文字识别
- **Rich/Typer**: 现代化CLI界面

#### 后续迭代计划

- [ ] 支持更多格式（EPUB、RTF等）
- [ ] Web API服务模式
- [ ] 目录监控自动转换
- [ ] AI增强内容结构化
- [ ] 图形界面（GUI）版本

### 📦 打包与部署

```bash
# 构建分发包
make build

# 安装到本地
pip install dist/documark-1.0.0-py3-none-any.whl
```

### 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: 添加新特性'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

---

## 繁體中文

### 🎉 專案介紹

**DocuMark** 是一款強大的智慧文件轉換工具，能夠將各種常見文件格式（PDF、Word、Excel、PowerPoint、HTML、圖片等）快速轉換為結構化的Markdown格式。

**核心價值**:
- 🚀 一站式解決文件格式轉換需求
- 🎨 保留原始文件結構和格式
- 🤖 支援圖片文字識別（OCR）
- ⚡ 批次處理與平行轉換

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📑 **多格式支援** | PDF、Word、Excel、PowerPoint、HTML、圖片、文字等 |
| 🎨 **美觀CLI** | 基於Rich函式庫的彩色終端介面 |
| ⚡ **批次轉換** | 支援目錄遞迴處理與多執行緒 |
| 🤖 **OCR識別** | 圖片文字智慧識別（支援中英文）|
| 📊 **表格提取** | 自動識別並轉換文件中的表格 |

### 🚀 快速開始

```bash
# 安裝
pip install -r requirements.txt
pip install -e .

# 轉換檔案
documark convert document.pdf
documark convert ./documents -r -o ./output
```

### 📄 開源協議

[MIT](LICENSE) License

---

## English

### 🎉 Introduction

**DocuMark** is a powerful intelligent document converter that transforms various file formats (PDF, Word, Excel, PowerPoint, HTML, Images, etc.) into structured Markdown format.

**Core Values**:
- 🚀 One-stop solution for document format conversion
- 🎨 Preserves original document structure and formatting
- 🤖 Image text recognition (OCR) support
- ⚡ Batch processing with parallel conversion

### ✨ Features

| Feature | Description |
|---------|-------------|
| 📑 **Multi-format** | PDF, Word, Excel, PowerPoint, HTML, Images, Text |
| 🎨 **Beautiful CLI** | Colorful terminal UI based on Rich library |
| ⚡ **Batch Convert** | Directory recursion & multi-threading |
| 🤖 **OCR Support** | Intelligent image text recognition |
| 📊 **Table Extraction** | Auto-detect and convert tables |

### 🚀 Quick Start

```bash
# Install
pip install -r requirements.txt
pip install -e .

# Convert files
documark convert document.pdf
documark convert ./documents -r -o ./output
```

### 📄 License

[MIT](LICENSE) License

---

<div align="center">

**Made with ❤️ by gitstq**

[GitHub](https://github.com/gitstq) • [Issues](https://github.com/gitstq/documark/issues)

</div>
