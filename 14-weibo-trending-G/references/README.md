# References - 参考文档

本目录包含14-weibo-trending skill的参考文档和资源。

## 📚 参考资料

### API文档
- [天行API - 微博热搜榜](https://www.tianapi.com/apiview/223)
- [微博热搜官方页面](https://s.weibo.com/top/summary)

### 技术文档
- `api_reference.md` - 天行API详细文档
- `data_format.md` - 数据格式说明
- `best_practices.md` - 最佳实践指南

### 示例数据
- `sample_response.json` - API响应示例
- `sample_report.md` - 报告输出示例

## 🔧 Progressive Disclosure

本skill遵循Progressive Disclosure设计原则：

**Layer 1 (Metadata)**: SKILL.md的YAML frontmatter (~100 tokens)
**Layer 2 (Core Instructions)**: SKILL.md的主要内容 (<5000 tokens)
**Layer 3 (References)**: 本目录的详细参考文档（按需加载）

Claude会根据任务需求自动加载相关参考文档，避免不必要的Token消耗。

## 🔄 备用API

### FreeAPIs.cn 微博热搜API

**URL**: `https://api.freeapis.cn/v1/weibo/hot`

**方法**: GET

**参数**:
- `KEY`: API密钥（需注册）

**注册地址**: https://www.freeapis.cn/user/key

**配额**: 10,000次/天，1次/秒限流

**状态**: ⚠️ 需要注册获取KEY（2025-12-29测试）

---

### ALAPI 微博热搜

**URL**: `https://v2.alapi.cn/api/weibo/hot`

**方法**: GET

**参数**:
- `token`: API token（需注册）

**注册地址**: https://www.alapi.cn

**配额**: 10 QPS

**状态**: ⚠️ 需要注册获取token

---

## 📖 文档列表

### 即将添加
- `api_reference.md` - API详细参数说明
- `data_format.md` - 数据结构和字段说明
- `best_practices.md` - 使用最佳实践
- `troubleshooting.md` - 常见问题排查
- `examples.md` - 更多使用示例
