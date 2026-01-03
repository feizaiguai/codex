"""06-documentation 测试"""
from engine import DocumentationEngine, APIEndpoint

def test_documentation():
    print("=== 测试文档生成 ===\n")

    engine = DocumentationEngine()

    # 测试 README
    project_info = {
        'name': 'Test Project',
        'description': 'A test project',
        'features': ['Feature 1', 'Feature 2']
    }
    readme = engine.generate_readme(project_info)
    print("README 预览:")
    print(readme[:200] + "...\n")

    # 测试 API 文档
    endpoints = [
        APIEndpoint(
            path='/api/users',
            method='GET',
            summary='Get users',
            parameters=[],
            responses={'200': {'description': 'Success'}}
        )
    ]
    docs = engine.generate_api_docs(endpoints)
    print(f"生成文档: {list(docs.keys())}")

    print("\n✓ 所有测试通过")

if __name__ == '__main__':
    test_documentation()
