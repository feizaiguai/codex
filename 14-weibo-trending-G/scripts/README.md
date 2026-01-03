# Scripts - 可执行脚本

本目录包含14-weibo-trending skill的可执行脚本。

## 可用脚本

### 1. weibo_trending.py
快速获取微博热搜的命令行工具。

**使用方法**:
```bash
# 获取默认前10名热搜
python scripts/weibo_trending.py

# 获取前5名
python scripts/weibo_trending.py --limit 5

# 搜索关键词
python scripts/weibo_trending.py --keyword "AI"

# 不包含详细分析（仅基本信息）
python scripts/weibo_trending.py --no-analysis
```

**参数说明**:
- `--limit`: 返回热搜数量（默认10）
- `--keyword`: 关键词筛选
- `--no-analysis`: 不包含WebSearch详细分析

### 2. monitor_trending.py（计划中）
实时监控微博热搜变化。

### 3. export_trending.py（计划中）
导出热搜数据为CSV/JSON格式。

## 依赖安装

```bash
pip install requests
```

## 注意事项

- 所有脚本需要在项目根目录运行
- 确保API密钥有效
- WebSearch功能需要在Claude环境中运行
