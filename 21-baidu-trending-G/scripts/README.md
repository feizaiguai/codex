# Scripts - 可执行脚本

此目录包含百度热搜分析器的可执行脚本。

## baidu_trending.py

快速查询百度热搜的脚本。

### 使用方法

```bash
# 获取默认前10名热搜
python scripts/baidu_trending.py

# 获取前5名
python scripts/baidu_trending.py --limit 5

# 搜索关键词
python scripts/baidu_trending.py --keyword "AI"

# 只要基本信息（不含详细分析）
python scripts/baidu_trending.py --no-analysis
```

### 参数说明

- `--limit`: 返回热搜数量（默认10）
- `--keyword`: 关键词筛选
- `--no-analysis`: 不包含详细分析
