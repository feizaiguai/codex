"""
JSON加载器 - 简化版本

从01-spec-explorer生成的spec_model.json加载数据
"""

import json
from pathlib import Path
from typing import Dict, Any, List

from core.models import DesignDraft


def load_json(json_file: str) -> DesignDraft:
    """
    从JSON文件加载设计草稿数据
    
    Args:
        json_file: spec_model.json文件路径
    
    Returns:
        DesignDraft对象
    """
    json_path = Path(json_file)
    if not json_path.exists():
        raise FileNotFoundError(f"JSON文件不存在: {json_file}")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    spec_model = data.get("spec_model", {})
    
    # 提取元数据
    meta = data.get("meta", {})
    project_name = meta.get("project_name", "未命名项目")
    
    # 提取上下文
    context = spec_model.get("context", {})
    
    # 提取用户故事
    flow_modeling = spec_model.get("flow_modeling", {})
    user_stories_data = flow_modeling.get("user_stories", [])
    
    # 转换为Dict格式
    user_stories = [
        {
            "id": story.get("id", ""),
            "title": story.get("title", ""),
            "description": story.get("i_want", "")
        }
        for story in user_stories_data
    ]
    
    # 提取实体
    domain_modeling = spec_model.get("domain_modeling", {})
    entities_data = domain_modeling.get("entities", [])
    
    entities = [
        {
            "name": entity.get("name", ""),
            "attributes": entity.get("attributes", []),
            "behaviors": entity.get("behaviors", [])
        }
        for entity in entities_data
    ]
    
    # 提取限界上下文
    bounded_contexts_data = domain_modeling.get("bounded_contexts", [])
    contexts = [
        {
            "name": bc.get("name", ""),
            "entities": bc.get("entities", []),
            "responsibilities": "\n".join(bc.get("responsibilities", []))
        }
        for bc in bounded_contexts_data
    ]
    
    # 从用户故事创建features
    features = [
        {
            "name": story.get("title", ""),
            "priority": "P1",
            "description": story.get("i_want", "")
        }
        for story in user_stories_data
    ]
    
    # 创建DesignDraft对象
    draft = DesignDraft(
        project_name=project_name,
        core_value=context.get("value_proposition", ""),
        target_users=", ".join(context.get("target_users", [])),
        user_scale="未知",
        features=features,
        entities=entities,
        value_objects=[],
        aggregates=[],
        contexts=contexts,
        user_stories=user_stories,
        workflows=[]
    )
    
    return draft


def main():
    """测试代码"""
    import sys
    if len(sys.argv) > 1:
        draft = load_json(sys.argv[1])
        print(f"✅ 成功加载: {draft.project_name}")
        print(f"  - {len(draft.entities)}个实体")
        print(f"  - {len(draft.features)}个功能")
        print(f"  - {len(draft.contexts)}个上下文")


if __name__ == "__main__":
    main()
