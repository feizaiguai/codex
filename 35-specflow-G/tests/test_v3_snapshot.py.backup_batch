"""
V3输出快照测试
捕获V3生成器的输出作为升级基线,确保V4不破坏现有功能
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any

# 添加路径
SPECFLOW_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SPECFLOW_DIR))

from core.models import DepthLevel
from loaders.json_loader import (
    load_json,
    extract_data_from_json,
    create_requirements_from_json,
    create_quality_report_from_json
)
from generator_v3 import SpecificationGenerator


class V3Snapshot:
    """V3输出快照管理器"""

    def __init__(self, snapshot_dir: str = "tests/snapshots"):
        self.snapshot_dir = Path(SPECFLOW_DIR) / snapshot_dir
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)

    def capture_v3_output(self, json_file: str) -> Dict[str, str]:
        """
        捕获V3生成器的完整输出

        参数:
            json_file: 输入JSON文件路径

        返回:
            Dict[str, str]: 文档类型 -> Markdown内容
        """
        print(f"\n{'='*70}")
        print(f"  捕获V3输出快照")
        print('='*70)
        print(f"输入文件: {json_file}")

        # 加载数据
        json_data = load_json(json_file)
        extracted_data = extract_data_from_json(json_data)
        requirements = create_requirements_from_json(extracted_data)
        quality_report = create_quality_report_from_json(extracted_data)

        # 准备用户故事
        user_stories = []
        for req in requirements:
            user_stories.extend(req.user_stories)

        # 创建V3生成器
        generator = SpecificationGenerator()

        # 捕获所有文档
        snapshots = {}

        # 01-需求规格
        print("\n捕获: 01-需求规格")
        doc = generator.generate_requirements(requirements, user_stories)
        snapshots['01-需求规格'] = doc.markdown
        print(f"  ✓ 长度: {len(doc.markdown)} 字符")

        # 02-领域模型
        print("捕获: 02-领域模型")
        doc = generator.generate_domain_model(quality_report.domain, requirements)
        snapshots['02-领域模型'] = doc.markdown
        print(f"  ✓ 长度: {len(doc.markdown)} 字符")

        # 03-架构设计
        print("捕获: 03-架构设计")
        doc = generator.generate_architecture(quality_report.complexity, quality_report.domain)
        snapshots['03-架构设计'] = doc.markdown
        print(f"  ✓ 长度: {len(doc.markdown)} 字符")

        # 04-实施计划
        print("捕获: 04-实施计划")
        doc = generator.generate_implementation_plan(user_stories, quality_report.estimated_hours)
        snapshots['04-实施计划'] = doc.markdown
        print(f"  ✓ 长度: {len(doc.markdown)} 字符")

        # 05-测试策略
        print("捕获: 05-测试策略")
        doc = generator.generate_test_strategy(user_stories, [])
        snapshots['05-测试策略'] = doc.markdown
        print(f"  ✓ 长度: {len(doc.markdown)} 字符")

        # 06-风险评估
        print("捕获: 06-风险评估")
        doc = generator.generate_risk_assessment(
            quality_report.complexity,
            quality_report.validation_issues
        )
        snapshots['06-风险评估'] = doc.markdown
        print(f"  ✓ 长度: {len(doc.markdown)} 字符")

        # 07-质量报告
        print("捕获: 07-质量报告")
        doc = generator.generate_quality_report(quality_report)
        snapshots['07-质量报告'] = doc.markdown
        print(f"  ✓ 长度: {len(doc.markdown)} 字符")

        print(f"\n{'='*70}")
        print(f"   已捕获 {len(snapshots)} 个文档快照")
        print('='*70)

        return snapshots

    def save_snapshots(self, snapshots: Dict[str, str], name: str = "baseline"):
        """
        保存快照到文件

        参数:
            snapshots: 文档快照字典
            name: 快照名称
        """
        snapshot_file = self.snapshot_dir / f"{name}.json"

        # 保存为JSON格式
        snapshot_data = {
            "name": name,
            "timestamp": "2025-12-20T10:00:00Z",
            "documents": snapshots,
            "metadata": {
                "total_docs": len(snapshots),
                "total_chars": sum(len(content) for content in snapshots.values())
            }
        }

        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(snapshot_data, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 快照已保存到: {snapshot_file}")
        print(f"  文档数: {snapshot_data['metadata']['total_docs']}")
        print(f"  总字符数: {snapshot_data['metadata']['total_chars']}")

    def load_snapshot(self, name: str = "baseline") -> Dict[str, str]:
        """
        加载快照

        参数:
            name: 快照名称

        返回:
            Dict[str, str]: 文档快照字典
        """
        snapshot_file = self.snapshot_dir / f"{name}.json"

        if not snapshot_file.exists():
            raise FileNotFoundError(f"快照文件不存在: {snapshot_file}")

        with open(snapshot_file, 'r', encoding='utf-8') as f:
            snapshot_data = json.load(f)

        return snapshot_data['documents']

    def compare_outputs(self, v3_output: Dict[str, str], v4_output: Dict[str, str]) -> Dict[str, Any]:
        """
        比较V3和V4的输出

        参数:
            v3_output: V3输出快照
            v4_output: V4输出快照

        返回:
            Dict[str, Any]: 比较结果
        """
        print(f"\n{'='*70}")
        print(f"  V3 vs V4 输出比较")
        print('='*70)

        results = {
            'identical': [],
            'similar': [],
            'different': [],
            'missing': [],
            'extra': []
        }

        # 检查缺失和额外的文档
        v3_keys = set(v3_output.keys())
        v4_keys = set(v4_output.keys())

        results['missing'] = list(v3_keys - v4_keys)
        results['extra'] = list(v4_keys - v3_keys)

        # 比较共同的文档
        for doc_type in v3_keys & v4_keys:
            v3_content = v3_output[doc_type]
            v4_content = v4_output[doc_type]

            if v3_content == v4_content:
                results['identical'].append(doc_type)
                print(f"✓ {doc_type}: 完全一致")
            else:
                # 计算相似度(简单字符级别)
                similarity = self._calculate_similarity(v3_content, v4_content)

                if similarity > 0.95:
                    results['similar'].append((doc_type, similarity))
                    print(f"≈ {doc_type}: 高度相似 ({similarity*100:.1f}%)")
                else:
                    results['different'].append((doc_type, similarity))
                    print(f"✗ {doc_type}: 差异较大 ({similarity*100:.1f}%)")

        # 报告缺失和额外的文档
        for doc_type in results['missing']:
            print(f"  {doc_type}: V4缺失")

        for doc_type in results['extra']:
            print(f"  {doc_type}: V4额外")

        print(f"\n{'='*70}")
        print(f"  比较结果汇总")
        print('='*70)
        print(f"完全一致: {len(results['identical'])}个")
        print(f"高度相似: {len(results['similar'])}个")
        print(f"差异较大: {len(results['different'])}个")
        print(f"V4缺失: {len(results['missing'])}个")
        print(f"V4额外: {len(results['extra'])}个")

        return results

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度(简单版)

        参数:
            text1: 文本1
            text2: 文本2

        返回:
            float: 相似度(0-1)
        """
        # 简单的字符级别相似度
        len1 = len(text1)
        len2 = len(text2)

        if len1 == 0 and len2 == 0:
            return 1.0

        if len1 == 0 or len2 == 0:
            return 0.0

        # 计算相同字符的比例
        max_len = max(len1, len2)
        common_prefix_len = 0

        for i in range(min(len1, len2)):
            if text1[i] == text2[i]:
                common_prefix_len += 1
            else:
                break

        # 更精细的比较:按行比较
        lines1 = text1.split('\n')
        lines2 = text2.split('\n')

        same_lines = sum(1 for l1, l2 in zip(lines1, lines2) if l1.strip() == l2.strip())
        max_lines = max(len(lines1), len(lines2))

        return same_lines / max_lines if max_lines > 0 else 0.0


def test_create_baseline_snapshot():
    """创建V3基线快照"""
    print("\n\n")
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "    V3输出快照测试 - 创建基线".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)

    # 查找测试JSON文件(使用02-architecture的测试JSON)
    test_json = SPECFLOW_DIR.parent / "02-architecture" / "TEST_ARCH.json"

    if not test_json.exists():
        print(f"\n  测试JSON文件不存在: {test_json}")
        print("尝试使用workflow_test的JSON")
        test_json = SPECFLOW_DIR.parent / "workflow_test" / "step2_arch.json"

    if not test_json.exists():
        print(f"\n 找不到测试JSON文件")
        print("跳过快照创建")
        return

    # 创建快照管理器
    snapshot_mgr = V3Snapshot()

    # 捕获V3输出
    snapshots = snapshot_mgr.capture_v3_output(str(test_json))

    # 保存快照
    snapshot_mgr.save_snapshots(snapshots, name="v3_baseline")

    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "     V3基线快照创建完成".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    print("\n")


if __name__ == "__main__":
    try:
        test_create_baseline_snapshot()
        sys.exit(0)
    except Exception as e:
        print(f"\n\n 错误: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
