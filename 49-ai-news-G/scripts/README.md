# Scripts - 可执行脚本

本目录包含AI资讯分析器的可执行脚本。

## 📄 文件列表

### ai_news.py

快速执行脚本，调用handler.py执行分析。

**使用方法**:
```bash
# 基本用法
python scripts/ai_news.py

# 带参数
python scripts/ai_news.py --limit 5
python scripts/ai_news.py --keyword "OpenAI"
python scripts/ai_news.py --no-analysis
```

**参数说明**:
- `--limit`: 返回资讯数量（默认10）
- `--keyword`: 关键词筛选
- `--no-analysis`: 不包含详细分析
- `--output`: 指定输出文件路径

## 🚀 快速开始

```bash
# 进入scripts目录
cd C:/Users/bigbao/.claude/skills/49-ai-news/scripts

# 运行脚本
python ai_news.py
```

## 📝 注意事项

- 确保已安装requests库：`pip install requests`
- 确保15-web-search skill已安装
- 首次运行可能需要几秒钟初始化
