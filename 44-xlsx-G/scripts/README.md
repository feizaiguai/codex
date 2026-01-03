# 44-xlsx Scripts

本目录包含44-xlsx的可执行脚本。

## 官方规范（Anthropic Agent Skills）

根据官方规范，scripts/目录用于存放：
- 可执行的命令行工具
- CLI接口脚本
- 自动化任务脚本

## 使用方式

### 基本用法
```bash
python scripts/<script_name>.py [options]
```

### 示例脚本结构
```python
#!/usr/bin/env python3
"""
<脚本描述>
"""

import argparse

def main():
    parser = argparse.ArgumentParser(description='<描述>')
    parser.add_argument('input', help='输入参数')
    args = parser.parse_args()

    # 脚本逻辑
    print(f"处理: {args.input}")

if __name__ == '__main__':
    main()
```

## 脚本列表

当前此Skill暂无脚本。V2.1版本将陆续添加。

## 开发指南

添加新脚本时：
1. 脚本必须有清晰的docstring
2. 使用argparse处理命令行参数
3. 包含错误处理
4. 提供使用示例
5. 更新此README的脚本列表
