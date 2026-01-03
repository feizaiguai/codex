"""
生成器抽象基类
定义所有生成器的通用接口
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, Template
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.models import Document


class BaseGenerator(ABC):
    """文档生成器抽象基类"""

    # 类级别的模板缓存(性能优化)
    _template_cache: Dict[str, Any] = {}

    def __init__(self, template_dir: str = "templates"):
        """
        初始化生成器

        参数:
            template_dir: 模板目录路径(相对于35-specflow根目录)
        """
        self.template_dir = template_dir

        # 初始化Jinja2环境(如果可用)
        if JINJA2_AVAILABLE:
            templates_path = Path(__file__).parent.parent / template_dir
            self.template_env = Environment(
                loader=FileSystemLoader(str(templates_path)),
                autoescape=False,  # Markdown不需要自动转义
                trim_blocks=True,
                lstrip_blocks=True
            )
        else:
            self.template_env = None

    @abstractmethod
    def generate(self, context: Dict[str, Any]) -> Document:
        """
        生成文档(抽象方法,子类必须实现)

        参数:
            context: 生成上下文(包含所有必要数据)

        返回:
            Document: 生成的文档对象
        """
        pass

    def render_template(self, template_name: str, data: Dict[str, Any]) -> str:
        """
        渲染Jinja2模板(如果可用),否则使用简单替换

        参数:
            template_name: 模板文件名(如 "overview.md.j2")
            data: 模板变量字典

        返回:
            str: 渲染后的Markdown文本
        """
        if not JINJA2_AVAILABLE or not self.template_env:
            # 降级:使用简单的字符串格式化
            return self._simple_template_render(template_name, data)

        # 使用缓存的模板(性能优化)
        cache_key = f"{self.template_dir}/{template_name}"
        if cache_key not in self._template_cache:
            try:
                self._template_cache[cache_key] = self.template_env.get_template(template_name)
            except Exception as e:
                print(f"  模板加载失败: {template_name}, 错误: {e}")
                return self._simple_template_render(template_name, data)

        template = self._template_cache[cache_key]
        return template.render(**data)

    def _simple_template_render(self, template_name: str, data: Dict[str, Any]) -> str:
        """
        简单模板渲染(Jinja2不可用时的后备方案)

        使用缓存优化性能(Gemini建议)

        参数:
            template_name: 模板名称
            data: 数据字典

        返回:
            str: 渲染结果
        """
        # 使用缓存的模板内容(性能优化)
        cache_key = f"simple:{self.template_dir}/{template_name}"

        if cache_key not in self._template_cache:
            # 首次加载:读取并缓存模板文件
            template_path = Path(__file__).parent.parent / self.template_dir / template_name

            if not template_path.exists():
                # 模板不存在,缓存空字符串
                print(f"  模板文件不存在: {template_path}")
                self._template_cache[cache_key] = ""
                return ""

            try:
                template_content = template_path.read_text(encoding='utf-8')
                self._template_cache[cache_key] = template_content
            except Exception as e:
                print(f"  简单模板读取失败: {e}")
                self._template_cache[cache_key] = ""
                return ""

        # 从缓存获取模板内容
        template_content = self._template_cache[cache_key]

        if not template_content:
            return ""

        # 执行简单的 {key} 替换
        try:
            result = template_content
            for key, value in data.items():
                placeholder = f"{{{key}}}"
                result = result.replace(placeholder, str(value))
            return result
        except Exception as e:
            print(f"  简单模板渲染失败: {e}")
            return ""

    def _dict_to_markdown(self, content: Dict[str, Any]) -> str:
        """
        将内容字典转换为Markdown(向后兼容方法)

        参数:
            content: 内容字典

        返回:
            str: Markdown文本
        """
        markdown = ""
        for key, value in content.items():
            if isinstance(value, str):
                markdown += value + "\n\n"
            elif isinstance(value, list):
                for item in value:
                    markdown += f"- {item}\n"
                markdown += "\n"
        return markdown.strip()
