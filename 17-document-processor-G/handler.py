#!/usr/bin/env python3
"""
handler 模块
"""


"""
17-document-processor 命令行接口
"""

from typing import Dict, List, Optional, Any, Tuple, Union

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from engine import (
    DocumentProcessor,
    DocumentFormat,
    TableFormat
)

LOGGER = logging.getLogger(__name__)


def main() -> Any:
    try:
        """主函数"""
        if len(sys.argv) < 2:
            print("文档处理系统 - 多格式文档解析和转换")
            print("\n用法: python handler.py <命令> [参数]")
            print("\n可用命令:")
            print("  process <文件>        - 处理文档")
            print("  convert <输入> <输出格式> <输出文件> - 转换格式")
            print("  analyze <Excel文件>   - 分析Excel数据")
            return
    except Exception as e:
        LOGGER.error(f"执行出错: {e}")
        return 1

    command = sys.argv[1]
    processor = DocumentProcessor()

    if command == "process":
        if len(sys.argv) < 3:
            print("用法: python handler.py process <文件>")
            return

        file_path = Path(sys.argv[2])
        doc = processor.process(file_path)

        print(f"文档: {doc.metadata.title}")
        print(f"格式: {doc.metadata.format.value}")
        print(f"页数: {doc.metadata.page_count}")
        print(f"字数: {doc.metadata.word_count}")
        print(f"表格数: {len(doc.tables)}")
        print(f"图片数: {len(doc.images)}")

    elif command == "convert":
        if len(sys.argv) < 5:
            print("用法: python handler.py convert <输入> <输出格式> <输出文件>")
            return

        input_path = Path(sys.argv[2])
        output_format = DocumentFormat(sys.argv[3])
        output_path = Path(sys.argv[4])

        processor.convert(input_path, output_format, output_path)
        print(f"转换完成: {output_path}")

    elif command == "analyze":
        if len(sys.argv) < 3:
            print("用法: python handler.py analyze <Excel文件>")
            return

        file_path = Path(sys.argv[2])
        analysis = processor.excel_processor.analyze_data(file_path)

        for sheet_name, sheet_analysis in analysis.items():
            print(f"\n工作表: {sheet_name}")
            print(f"  行数: {sheet_analysis['row_count']}")
            print(f"  列数: {sheet_analysis['column_count']}")
            print("  列信息:")
            for col in sheet_analysis['columns']:
                print(f"    {col['name']}: {col['type']}")


if __name__ == "__main__":
    main()
