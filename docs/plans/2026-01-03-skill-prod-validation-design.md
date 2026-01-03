# Skills 生产验证设计

## 目标
在 `C:\Users\bigbao\.codex\skills` 中对 55 个技能进行真实数据生产级验证，确保每个技能可在生产环境运行并能生成真实输出；验证通过后统一提交并推送到 codex 远程仓库。

## 设计概要
采用“真实数据测试矩阵 + 统一测试执行器 + 统一报告”的架构。每个技能对应一条可执行的真实命令，命令优先调用各技能 `handler.py` 的 CLI 接口，必要时读取仓库内真实文件作为输入（如 `SKILL.md`、`README.md`、真实架构文档），并对外部 API 类技能使用真实密钥拉取真实数据。测试执行器 `tools/skill_prod_test.py` 负责逐项运行命令、采集 stdout/stderr、落盘日志、输出 `results.json` 与 `summary.md`。

## 功能正常判定标准
1) 命令退出码为 0。2) 输出行数与字符数达到最低阈值。3) 输出不包含 `fallback/degraded/mock/模拟/示例` 等虚拟数据标记。4) 若配置 `must_contain`，输出必须包含指定真实字段。5) 依赖外部 API 的技能必须使用真实 API 响应。

## 风险与对策
- 缺少 API Key：测试标记为 blocked，并汇总缺失项。收到密钥后重新执行相关技能。
- CLI 参量差异：通过矩阵逐项记录命令与输入，必要时补充适配。
- 输出不足：提高输入质量或指定更明确的输出目标文件。

## 交付物
- `tools/skill_prod_matrix.json`：55 个技能的真实测试命令矩阵
- `tools/skill_prod_test.py`：统一执行器
- `reports/skills-prod-real/`：结果与汇总报告