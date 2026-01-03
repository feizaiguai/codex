# Scripts - 可执行脚本

本目录包含Reddit趋势分析器的可执行脚本。

## 📄 fetch.py

快速执行脚本，调用handler.py获取Reddit热门帖子。

**使用方法**:
```bash
# 基本用法（快速模式）
python scripts/fetch.py --no-analysis

# 指定subreddit
python scripts/fetch.py --subreddit technology

# 完整模式
python scripts/fetch.py --limit 10
```
