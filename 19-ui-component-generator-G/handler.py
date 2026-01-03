#!/usr/bin/env python3
"""19-ui-component-generator CLI"""
import argparse
from engine import ComponentSpec, ComponentGenerator, save_files


def main() -> int:
    parser = argparse.ArgumentParser(
        description="19-ui-component-generator: UI组件生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python handler.py --name ProductCard --framework react --props title,price --output ./components
  python handler.py --name UserBadge --framework vue --props name,role --output ./components
        """,
    )
    parser.add_argument("--name", required=True, help="组件名称")
    parser.add_argument("--framework", choices=["react", "vue"], default="react")
    parser.add_argument("--props", default="", help="逗号分隔的props列表")
    parser.add_argument("--output", default="./output", help="输出目录")
    parser.add_argument("--no-tests", action="store_true", help="不生成测试")

    args = parser.parse_args()
    props = [p.strip() for p in args.props.split(",") if p.strip()]

    spec = ComponentSpec(name=args.name, framework=args.framework, props=props)
    gen = ComponentGenerator()
    files = gen.generate(spec, with_tests=not args.no_tests)
    paths = save_files(args.output, files)

    print("\n".join(str(p) for p in paths))
    print(f"\n已生成 {len(paths)} 个文件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())