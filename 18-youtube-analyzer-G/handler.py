#!/usr/bin/env python3
"""18-youtube-analyzer CLI"""
import argparse
import json
import os
import sys
from pathlib import Path
from youtube_analyzer import (
    YouTubeAPI,
    extract_video_id,
    extract_channel_id,
    analyze_video,
    analyze_channel,
    search_videos,
)


def _write_output(data, output: str | None, as_json: bool) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) if as_json else str(data)
    if output:
        Path(output).write_text(text, encoding="utf-8")
    print(text)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="18-youtube-analyzer: YouTube 分析器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    v = subparsers.add_parser("analyze-video", help="分析视频")
    v.add_argument("video", help="视频URL或ID")
    v.add_argument("--comments", action="store_true", help="包含评论情绪")
    v.add_argument("--json", action="store_true", help="JSON输出")
    v.add_argument("--output", help="输出文件")

    c = subparsers.add_parser("analyze-channel", help="分析频道")
    c.add_argument("channel", help="频道URL或ID")
    c.add_argument("--json", action="store_true", help="JSON输出")
    c.add_argument("--output", help="输出文件")

    s = subparsers.add_parser("search", help="搜索视频")
    s.add_argument("query", help="搜索关键词")
    s.add_argument("--max-results", type=int, default=5)
    s.add_argument("--json", action="store_true", help="JSON输出")
    s.add_argument("--output", help="输出文件")

    parser.add_argument("--api-key", help="YouTube API Key (或设置 YOUTUBE_API_KEY)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    api_key = args.api_key or os.environ.get("YOUTUBE_API_KEY")
    api = YouTubeAPI(api_key)

    if args.command == "analyze-video":
        vid = extract_video_id(args.video)
        data = analyze_video(api, vid, include_comments=args.comments)
        _write_output(data, args.output, args.json)
        return 0

    if args.command == "analyze-channel":
        cid = extract_channel_id(args.channel)
        data = analyze_channel(api, cid)
        _write_output(data, args.output, args.json)
        return 0

    if args.command == "search":
        results = search_videos(api, args.query, args.max_results)
        _write_output({"query": args.query, "results": results}, args.output, args.json)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())