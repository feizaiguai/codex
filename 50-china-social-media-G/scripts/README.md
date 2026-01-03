# Scripts - 可执行脚本

本目录包含国内社媒资讯聚合器的可执行脚本。

## 📄 文件列表

### aggregate.py

快速执行脚本，调用handler.py执行聚合分析。

**使用方法**:
```bash
# 基本用法
python scripts/aggregate.py

# 带参数
python scripts/aggregate.py --limit 5
python scripts/aggregate.py --output report.md
```

**参数说明**:
- `--limit`: 每个平台返回资讯数量（默认10）
- `--output`: 指定输出文件路径

## 🚀 快速开始

```bash
# 进入scripts目录
cd C:/Users/bigbao/.claude/skills/50-china-social-media/scripts

# 运行脚本
python aggregate.py
```

## 📝 注意事项

- 确保已安装requests库：`pip install requests`
- 确保5个平台skills已安装
- 首次运行可能需要30-60秒（5个平台总耗时）
