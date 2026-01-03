"""29-knowledge-manager 测试"""
from engine import KnowledgeManager, DocType

def test_knowledge_manager():
    manager = KnowledgeManager()
    doc = manager.add_document("测试文档", "这是测试内容", DocType.TUTORIAL, ["test"])
    print(f"创建文档: {doc.title}")
    print(manager.generate_summary())
    assert len(manager.knowledge_base.documents) == 1

if __name__ == '__main__':
    print("知识管理器测试")
    test_knowledge_manager()
    print("✓ 测试通过")
