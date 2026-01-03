# Scripts - 可执行脚本

本目录包含国外社媒资讯聚合器的可执行脚本。

## 📄 文件列表

### aggregate.py

快速执行脚本，调用handler.py执行聚合分析。

**使用方法**:
```bash
# 基本用法
python scripts/aggregate.py

# 带参数
python scripts/aggregate.py --limit 5
python scripts/aggregate.py --newsapi-key YOUR_KEY
python scripts/aggregate.py --output report.md
```

**参数说明**:
- `--limit`: 每个平台返回资讯数量（默认10）
- `--newsapi-key`: NewsAPI密钥（或设置NEWSAPI_KEY环境变量）
- `--output`: 指定输出文件路径

## 🚀 快速开始

```bash
# 进入scripts目录
cd C:/Users/bigbao/.claude/skills/55-international-media/scripts

# 运行脚本
python aggregate.py
```

## 📝 注意事项

- 确保已安装requests库：`pip install requests`
- 确保3个平台skills已安装
- NewsAPI需要API密钥（免费注册）
- 首次运行可能需要15-20秒（3个平台总耗时）
