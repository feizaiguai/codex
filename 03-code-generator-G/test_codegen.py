"""
03-code-generator 测试脚本
"""

from engine import (
    CodeGenerator, CodegenConfig, Language, ArchitectureStyle,
    Entity, CRUDGenerator
)


def test_crud_generation():
    """测试 CRUD 生成"""
    print("=== 测试 CRUD 生成 ===\n")

    config = CodegenConfig(
        language=Language.PYTHON,
        architecture=ArchitectureStyle.PRAGMATIC,
        framework='fastapi',
        database='postgresql',
        use_orm=True,
        include_tests=True,
        include_docker=True
    )

    entity = Entity(
        name='User',
        fields=[
            {'name': 'id', 'type': 'integer'},
            {'name': 'username', 'type': 'string'},
            {'name': 'email', 'type': 'string'},
            {'name': 'is_active', 'type': 'boolean'},
        ],
        relationships=[]
    )

    crud_gen = CRUDGenerator(config)

    print("Python FastAPI 创建操作:")
    print(crud_gen.generate_create(entity))

    print("\nPython FastAPI 读取操作:")
    print(crud_gen.generate_read(entity)[:300] + "...")

    print("\n✓ CRUD 生成测试通过")


def test_scaffold_generation():
    """测试脚手架生成"""
    print("\n=== 测试项目脚手架生成 ===\n")

    config = CodegenConfig(
        language=Language.PYTHON,
        architecture=ArchitectureStyle.PRAGMATIC,
        framework='fastapi',
        database='postgresql',
        use_orm=True,
        include_tests=True,
        include_docker=True
    )

    generator = CodeGenerator(config)
    files = generator.generate_project('test-project')

    print(f"生成 {len(files)} 个文件:")
    for filepath in files.keys():
        print(f"  - {filepath}")

    print("\n✓ 脚手架生成测试通过")


def test_typescript_generation():
    """测试 TypeScript 代码生成"""
    print("\n=== 测试 TypeScript 代码生成 ===\n")

    config = CodegenConfig(
        language=Language.TYPESCRIPT,
        architecture=ArchitectureStyle.PRAGMATIC,
        framework='express',
        database='postgresql',
        use_orm=True,
        include_tests=True,
        include_docker=False
    )

    entity = Entity(
        name='Product',
        fields=[
            {'name': 'id', 'type': 'integer'},
            {'name': 'name', 'type': 'string'},
            {'name': 'price', 'type': 'number'},
        ],
        relationships=[]
    )

    crud_gen = CRUDGenerator(config)
    print("TypeScript Express 创建操作:")
    print(crud_gen.generate_create(entity))

    print("\n✓ TypeScript 生成测试通过")


if __name__ == '__main__':
    test_crud_generation()
    test_scaffold_generation()
    test_typescript_generation()

    print("\n" + "=" * 50)
    print("所有测试通过！")
    print("=" * 50)
