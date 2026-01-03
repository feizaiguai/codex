"""
03-code-generator 命令行接口
"""

import argparse
import json
import sys
from pathlib import Path
from engine import CodeGenerator, CodegenConfig, Language, ArchitectureStyle, Entity


def main():
    parser = argparse.ArgumentParser(
        description='03-code-generator: 代码生成引擎',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从 OpenAPI 生成 Python FastAPI 代码
  python handler.py --openapi openapi.json --lang python --framework fastapi --output ./generated

  # 生成 CRUD 接口
  python handler.py --entity User --lang python --framework fastapi --output ./generated

  # 生成项目脚手架
  python handler.py --scaffold my-project --lang python --framework fastapi --output ./projects
        """
    )

    parser.add_argument('--openapi', help='OpenAPI 规范文件路径')
    parser.add_argument('--entity', help='实体名称（生成 CRUD）')
    parser.add_argument('--scaffold', help='项目名称（生成脚手架）')

    parser.add_argument(
        '--lang',
        choices=['python', 'typescript', 'go', 'java', 'rust'],
        default='python',
        help='编程语言'
    )

    parser.add_argument(
        '--framework',
        default='fastapi',
        help='框架（fastapi, express, gin等）'
    )

    parser.add_argument(
        '--arch',
        choices=['clean', 'pragmatic', 'mvc', 'layered'],
        default='pragmatic',
        help='架构风格'
    )

    parser.add_argument('--database', default='postgresql', help='数据库')
    parser.add_argument('--output', '-o', default='./output', help='输出目录')
    parser.add_argument('--no-tests', action='store_true', help='不生成测试')
    parser.add_argument('--no-docker', action='store_true', help='不生成 Docker 文件')

    args = parser.parse_args()

    # 构建配置
    config = CodegenConfig(
        language=Language(args.lang),
        architecture=ArchitectureStyle(args.arch),
        framework=args.framework,
        database=args.database,
        use_orm=True,
        include_tests=not args.no_tests,
        include_docker=not args.no_docker
    )

    generator = CodeGenerator(config)

    try:
        if args.openapi:
            # 从 OpenAPI 生成
            print(f"[代码生成] 从 OpenAPI 规范生成代码...")
            with open(args.openapi, 'r', encoding='utf-8') as f:
                openapi_spec = json.load(f)

            files = generator.generate_from_openapi(openapi_spec)
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)

            for filename, content in files.items():
                filepath = output_dir / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ {filepath}")

            print(f"\n生成完成！共 {len(files)} 个文件")

        elif args.entity:
            # 生成 CRUD
            print(f"[代码生成] 为实体 '{args.entity}' 生成 CRUD 接口...")

            # 示例实体（实际应从配置文件读取）
            entity = Entity(
                name=args.entity,
                fields=[
                    {'name': 'id', 'type': 'integer'},
                    {'name': 'name', 'type': 'string'},
                    {'name': 'email', 'type': 'string'},
                ],
                relationships=[]
            )

            files = generator.generate_crud([entity])
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)

            for filename, content in files.items():
                filepath = output_dir / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ {filepath}")

            print(f"\n生成完成！共 {len(files)} 个文件")

        elif args.scaffold:
            # 生成项目脚手架
            print(f"[代码生成] 生成项目 '{args.scaffold}' 脚手架...")

            files = generator.generate_project(args.scaffold)
            output_dir = Path(args.output)

            for filepath, content in files.items():
                full_path = output_dir / filepath
                full_path.parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ {full_path}")

            print(f"\n生成完成！共 {len(files)} 个文件")
            print(f"\n项目位置: {output_dir / args.scaffold}")

        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
