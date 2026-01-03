#!/usr/bin/env python3
"""23-infrastructure-coder CLI"""
import argparse
import json
from pathlib import Path
from engine import InfrastructureCoder, IaCTool, CloudProvider, Resource, Module


def main() -> int:
    parser = argparse.ArgumentParser(
        description="23-infrastructure-coder: IaC 生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python handler.py --tool terraform --provider aws --name web --instance-type t2.micro --ami ami-123456 --output main.tf
        """,
    )
    parser.add_argument("--tool", choices=["terraform", "cloudformation"], default="terraform")
    parser.add_argument("--provider", choices=["aws", "azure", "gcp"], default="aws")
    parser.add_argument("--name", required=True, help="模块名称")
    parser.add_argument("--resource-type", default="aws_instance")
    parser.add_argument("--resource-name", default="web_server")
    parser.add_argument("--instance-type", default="t2.micro")
    parser.add_argument("--ami", default="ami-123456")
    parser.add_argument("--output", help="输出文件")

    args = parser.parse_args()
    tool = IaCTool(args.tool)
    provider = CloudProvider(args.provider)

    resource = Resource(
        type=args.resource_type,
        name=args.resource_name,
        properties={"instance_type": args.instance_type, "ami": args.ami},
        tags={"Environment": "Production"},
    )
    module = Module(name=args.name, resources=[resource])
    coder = InfrastructureCoder(tool, provider)
    code = coder.generate(module)

    if args.output:
        Path(args.output).write_text(code, encoding="utf-8")
    print(code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())