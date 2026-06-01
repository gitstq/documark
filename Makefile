# DocuMark Makefile

.PHONY: help install install-dev test lint format clean build publish

help:
	@echo "DocuMark 开发命令:"
	@echo "  make install      - 安装依赖"
	@echo "  make install-dev  - 安装开发依赖"
	@echo "  make test         - 运行测试"
	@echo "  make lint         - 代码检查"
	@echo "  make format       - 代码格式化"
	@echo "  make clean        - 清理构建文件"
	@echo "  make build        - 构建分发包"
	@echo "  make publish      - 发布到PyPI"

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=documark --cov-report=term-missing

lint:
	flake8 documark/ tests/
	mypy documark/

format:
	black documark/ tests/
	isort documark/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

publish: build
	twine check dist/*
	twine upload dist/*
