# Scripts - 可执行脚本

本目录包含Hacker News趋势分析器的可执行脚本。

## 📄 文件列表

### fetch.py

快速执行脚本，调用handler.py获取HN热门故事。

**使用方法**:
```bash
# 基本用法（快速模式）
python scripts/fetch.py

# 完整模式（含背景搜索）
python scripts/fetch.py --full

# 自定义数量
python scripts/fetch.py --limit 20

# 指定输出文件
python scripts/fetch.py --output hn_report.md
```

**参数说明**:
- `--limit`: 返回故事数量（默认10）
- `--full`: 完整模式，包含背景搜索
- `--output`: 指定输出文件路径

## 🚀 快速开始

```bash
# 进入scripts目录
cd C:/Users/bigbao/.claude/skills/51-hackernews/scripts

# 运行脚本
python fetch.py
```

## 📝 注意事项

- 确保已安装requests库：`pip install requests`
- 快速模式耗时2-5秒
- 完整模式耗时30-60秒（含背景搜索）
