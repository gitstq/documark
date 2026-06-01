"""
DocuMark 转换器测试
"""

import pytest
from pathlib import Path
from documark.converter import DocuMarkConverter


class TestDocuMarkConverter:
    """测试DocuMarkConverter类"""
    
    def test_init(self):
        """测试初始化"""
        converter = DocuMarkConverter()
        assert converter.output_dir is not None
        assert converter.max_workers == 4
        
        converter = DocuMarkConverter(output_dir="/tmp", max_workers=8)
        assert str(converter.output_dir) == "/tmp"
        assert converter.max_workers == 8
    
    def test_get_supported_formats(self):
        """测试获取支持的格式"""
        converter = DocuMarkConverter()
        formats = converter.get_supported_formats()
        
        assert isinstance(formats, dict)
        assert len(formats) > 0
        
        # 检查是否包含主要类别
        categories = ['文档', '表格', '演示', '网页', '图片', '文本']
        for category in categories:
            assert category in formats or any(category in k for k in formats.keys())
    
    def test_convert_nonexistent_file(self):
        """测试转换不存在的文件"""
        converter = DocuMarkConverter()
        
        with pytest.raises(FileNotFoundError):
            converter.convert("/nonexistent/file.pdf")
    
    def test_convert_unsupported_format(self):
        """测试转换不支持的格式"""
        converter = DocuMarkConverter()
        
        # 创建一个临时文件
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
            f.write(b"test")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError):
                converter.convert(temp_path)
        finally:
            Path(temp_path).unlink()


class TestUtils:
    """测试工具函数"""
    
    def test_detect_file_type(self):
        """测试文件类型检测"""
        from documark.utils import detect_file_type
        
        # 测试PDF
        mime = detect_file_type("test.pdf")
        assert "pdf" in mime
        
        # 测试Word
        mime = detect_file_type("test.docx")
        assert "word" in mime or "document" in mime
    
    def test_ensure_dir(self):
        """测试目录创建"""
        from documark.utils import ensure_dir
        import tempfile
        import shutil
        
        temp_dir = tempfile.mkdtemp()
        test_dir = Path(temp_dir) / "test" / "nested"
        
        result = ensure_dir(test_dir)
        assert result.exists()
        assert result.is_dir()
        
        # 清理
        shutil.rmtree(temp_dir)
    
    def test_format_file_size(self):
        """测试文件大小格式化"""
        from documark.utils import format_file_size
        
        assert "B" in format_file_size(100)
        assert "KB" in format_file_size(1024)
        assert "MB" in format_file_size(1024 * 1024)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
