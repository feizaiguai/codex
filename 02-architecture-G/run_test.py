"""
Run Test 模块

提供 Run Test 相关功能的实现。
"""


from typing import Dict, List, Optional, Any, Tuple, Union, Callable, Set

"""
02-architecture 测试启动脚本
解决相对导入问题
"""
import sys
import os
from pathlib import Path

# 将skills目录添加到Python路径
skills_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skills_dir))

# 现在可以导入02-architecture模块
if __name__ == '__main__':
    # 设置测试参数
    input_file = str(skills_dir / "01-spec-explorer" / "DESIGN_DRAFT.md")
    output_file = str(Path(__file__).parent / "TEST_ARCHITECTURE.md")

    print(f"[测试启动] 开始功能测试")
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print(f"Python路径已设置: {skills_dir}")
    print("-" * 80)

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 输入文件不存在: {input_file}")
        sys.exit(1)

    # 导入并运行
    from architecture_designer import main as run_main

    # 设置命令行参数
    sys.argv = ['architecture_designer.py', '-i', input_file, '-o', output_file]

    # 执行主程序
    try:
        run_main()
        print("\n" + "=" * 80)
        print("[测试完成] 功能测试成功")
    except Exception as e:
        print(f"\n[测试失败] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
