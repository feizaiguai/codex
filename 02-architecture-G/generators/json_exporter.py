"""
JSON导出器

将架构设计结果导出为符合project_schema.json的JSON格式
"""

import json
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

from core.models import ArchitectureDesign, DesignDraft


def generate_json(
    design_draft: DesignDraft,
    architecture: ArchitectureDesign
) -> Dict[str, Any]:
    """
    生成符合project_schema.json的架构模型JSON数据
    
    Args:
        design_draft: 设计草稿对象
        architecture: 架构设计对象
    
    Returns:
        Dict[str, Any]: 符合schema的JSON字典
    """
    
    # 元数据
    meta = {
        "project_name": design_draft.project_name,
        "version": "1.0.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "generated_by": "02-architecture"
    }
    
    # arch_model - scale_assessment
    scale_assessment = {
        "scale": architecture.scale_assessment.scale.value,
        "score": architecture.scale_assessment.score,
        "complexity_level": architecture.scale_assessment.complexity_level,
        "details": architecture.scale_assessment.details,
        "reasoning": architecture.scale_assessment.reasoning
    }
    
    # arch_model - tech_stack
    tech_stack = {
        "backend_language": {
            "recommendation": architecture.tech_stack.backend_language.recommendation,
            "alternatives": architecture.tech_stack.backend_language.alternatives,
            "rationale": architecture.tech_stack.backend_language.reasoning
        },
        "database": {
            "recommendation": architecture.tech_stack.database.recommendation,
            "alternatives": architecture.tech_stack.database.alternatives,
            "rationale": architecture.tech_stack.database.reasoning
        },
        "cache": {
            "recommendation": architecture.tech_stack.cache.recommendation,
            "rationale": architecture.tech_stack.cache.reasoning
        },
        "api_style": {
            "recommendation": architecture.tech_stack.api_style.recommendation,
            "rationale": architecture.tech_stack.api_style.reasoning
        }
    }
    
    # arch_model - pattern_selection
    pattern_selection = {
        "primary_pattern": architecture.pattern_selection.primary_pattern.value,
        "supporting_patterns": [
            p.value for p in architecture.pattern_selection.supporting_patterns
        ],
        "rationale": architecture.pattern_selection.reasoning
    }
    
    # arch_model - adrs
    adrs = [
        {
            "id": adr.adr_id,
            "title": adr.title,
            "status": adr.status,
            "context": adr.context,
            "decision": adr.decision,
            "consequences": adr.consequences
        }
        for adr in architecture.adrs
    ]
    
    # 组装完整JSON
    return {
        "meta": meta,
        "arch_model": {
            "scale_assessment": scale_assessment,
            "tech_stack": tech_stack,
            "pattern_selection": pattern_selection,
            "adrs": adrs
        }
    }


def save_json(data: Dict[str, Any], output_path: str) -> None:
    """
    保存JSON到文件
    
    Args:
        data: JSON数据字典
        output_path: 输出文件路径
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON数据已保存: {output_path}")


def merge_json_models(
    spec_model_file: str,
    arch_model: Dict[str, Any]
) -> Dict[str, Any]:
    """
    合并01的spec_model和02的arch_model到一个完整JSON
    
    Args:
        spec_model_file: spec_model.json文件路径
        arch_model: 架构模型字典
    
    Returns:
        完整的merged JSON
    """
    # 读取spec_model
    spec_path = Path(spec_model_file)
    if not spec_path.exists():
        # 如果spec_model不存在，只返回arch_model
        return arch_model
    
    with open(spec_path, "r", encoding="utf-8") as f:
        spec_data = json.load(f)
    
    # 合并两个JSON
    merged = {
        "meta": arch_model["meta"],  # 使用02的meta（更新的时间戳）
        "spec_model": spec_data.get("spec_model", {}),  # 来自01
        "arch_model": arch_model["arch_model"]  # 来自02
    }
    
    return merged


def main():
    """测试代码"""
    pass


if __name__ == "__main__":
    main()
