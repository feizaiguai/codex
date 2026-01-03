# 36-deep-research References

本目录包含36-deep-research的参考文档（按需加载）。

## 官方规范（Anthropic Agent Skills）

根据官方规范，references/目录用于：
- **Progressive Disclosure**: 按需加载的详细文档
- **Token优化**: 降低初始context消耗
- **深度内容**: 详细的技术参考、模式库、最佳实践

## 设计原则

### 三层加载策略
1. **Layer 1: Metadata** (~100 tokens) - SKILL.md的YAML frontmatter
2. **Layer 2: Core Instructions** (<5000 tokens) - SKILL.md的核心说明
3. **Layer 3: References** (按需) - 本目录的详细文档

### 何时加载References
- 用户明确请求详细信息时
- 任务复杂度需要深度参考时
- 核心instructions不足以解决问题时

## 参考文档列表

当前此Skill暂无参考文档。V2.1版本将陆续添加。

## 文档命名规范

- `patterns.md` - 设计模式和架构模式
- `workflows.md` - 详细工作流程
- `best_practices.md` - 最佳实践指南
- `api_reference.md` - API详细参考
- `examples.md` - 完整示例集合
- `troubleshooting.md` - 故障排查指南

## 开发指南

添加新参考文档时：
1. 文件名使用小写+下划线
2. 内容结构清晰（使用Markdown标题）
3. 包含具体示例
4. 保持文档原子性（单一主题）
5. 更新此README的文档列表
