#!/usr/bin/env python3
"""YouTube 分析器（精简可用版）"""
from __future__ import annotations

import os
import re
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, Any, List

BASE_URLS = [
    "https://www.googleapis.com/youtube/v3",
    "https://youtube.googleapis.com/youtube/v3",
]
HTML_ONLY = os.getenv("YOUTUBE_HTML_ONLY", "").lower() in ("1", "true", "yes")


def extract_video_id(url_or_id: str) -> str:
    m = re.search(r"v=([A-Za-z0-9_-]{6,})", url_or_id)
    if m:
        return m.group(1)
    m = re.search(r"youtu\.be/([A-Za-z0-9_-]{6,})", url_or_id)
    if m:
        return m.group(1)
    return url_or_id.strip()


def extract_channel_id(url_or_id: str) -> str:
    m = re.search(r"/channel/([A-Za-z0-9_-]{6,})", url_or_id)
    if m:
        return m.group(1)
    return url_or_id.strip()


class YouTubeAPI:
    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("缺少 YOUTUBE_API_KEY")
        self.api_key = api_key
        self.session = requests.Session()
        retries = Retry(
            total=1,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })

    def get(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params = dict(params)
        params["key"] = self.api_key
        last_error: Exception | None = None
        for base in BASE_URLS:
            try:
                resp = self.session.get(f"{base}/{endpoint}", params=params, timeout=(5, 15))
                resp.raise_for_status()
                return resp.json()
            except Exception as exc:
                last_error = exc
                continue
        raise last_error if last_error else RuntimeError("请求失败")


def _simple_sentiment(comments: List[str]) -> Dict[str, int]:
    positive = ["好", "赞", "喜欢", "优秀", "amazing", "great", "love"]
    negative = ["差", "糟", "失望", "bad", "hate"]
    pos = 0
    neg = 0
    for c in comments:
        lc = c.lower()
        if any(p in lc for p in positive):
            pos += 1
        if any(n in lc for n in negative):
            neg += 1
    return {"positive": pos, "negative": neg, "neutral": max(0, len(comments) - pos - neg)}


def get_video_details(api: YouTubeAPI, video_id: str) -> Dict[str, Any]:
    if HTML_ONLY:
        return get_video_html_meta(video_id)
    try:
        data = api.get("videos", {"part": "snippet,statistics,contentDetails", "id": video_id})
        items = data.get("items", [])
        if not items:
            raise ValueError("未找到视频")
        return items[0]
    except Exception:
        try:
            return get_video_oembed(video_id)
        except Exception:
            return get_video_html_meta(video_id)


def get_video_oembed(video_id: str) -> Dict[str, Any]:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    resp = requests.get(url, timeout=(10, 30))
    resp.raise_for_status()
    data = resp.json()
    return {
        "snippet": {
            "title": data.get("title"),
            "channelTitle": data.get("author_name"),
            "channelId": "",
            "publishedAt": "",
        },
        "statistics": {},
        "contentDetails": {},
    }


def get_video_html_meta(video_id: str) -> Dict[str, Any]:
    sources = [
        f"https://www.youtube.com/watch?v={video_id}",
        f"https://r.jina.ai/http://www.youtube.com/watch?v={video_id}",
    ]
    text = ""
    last_error: Exception | None = None
    for url in sources:
        try:
            resp = requests.get(url, timeout=(5, 15))
            resp.raise_for_status()
            text = resp.text
            if text:
                break
        except Exception as exc:
            last_error = exc
            continue
    if not text:
        raise last_error if last_error else RuntimeError("无法获取视频页面")
    title_match = re.search(r'<meta name="title" content="([^"]+)"', text)
    author_match = re.search(r'<meta name="author" content="([^"]+)"', text)
    channel_match = re.search(r'"channelId":"([^"]+)"', text)
    return {
        "snippet": {
            "title": title_match.group(1) if title_match else "",
            "channelTitle": author_match.group(1) if author_match else "",
            "channelId": channel_match.group(1) if channel_match else "",
            "publishedAt": "",
        },
        "statistics": {},
        "contentDetails": {},
    }


def get_channel_details(api: YouTubeAPI, channel_id: str) -> Dict[str, Any]:
    data = api.get("channels", {"part": "snippet,statistics", "id": channel_id})
    items = data.get("items", [])
    if not items:
        raise ValueError("未找到频道")
    return items[0]


def get_video_comments(api: YouTubeAPI, video_id: str, max_results: int = 20) -> List[str]:
    data = api.get("commentThreads", {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results,
        "textFormat": "plainText",
    })
    comments = []
    for item in data.get("items", []):
        snippet = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
        text = snippet.get("textDisplay") or ""
        if text:
            comments.append(text)
    return comments


def analyze_video(api: YouTubeAPI, video_id: str, include_comments: bool = False) -> Dict[str, Any]:
    detail = get_video_details(api, video_id)
    stats = detail.get("statistics", {})
    snippet = detail.get("snippet", {})
    views = int(stats.get("viewCount", 0)) if stats.get("viewCount") else 0
    likes = int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0
    comments_count = int(stats.get("commentCount", 0)) if stats.get("commentCount") else 0
    engagement = (likes + comments_count) / views if views else 0

    result = {
        "video_id": video_id,
        "title": snippet.get("title"),
        "channel_id": snippet.get("channelId"),
        "channel_title": snippet.get("channelTitle"),
        "published_at": snippet.get("publishedAt"),
        "views": views,
        "likes": likes,
        "comments": comments_count,
        "engagement_rate": round(engagement, 4),
    }

    if include_comments:
        comments = get_video_comments(api, video_id)
        result["sample_comments"] = comments[:10]
        result["sentiment"] = _simple_sentiment(comments)

    return result


def analyze_channel(api: YouTubeAPI, channel_id: str) -> Dict[str, Any]:
    detail = get_channel_details(api, channel_id)
    stats = detail.get("statistics", {})
    snippet = detail.get("snippet", {})
    return {
        "channel_id": channel_id,
        "title": snippet.get("title"),
        "description": snippet.get("description", "")[:200],
        "subscribers": int(stats.get("subscriberCount", 0)) if stats.get("subscriberCount") else 0,
        "views": int(stats.get("viewCount", 0)) if stats.get("viewCount") else 0,
        "videos": int(stats.get("videoCount", 0)) if stats.get("videoCount") else 0,
    }


def search_videos(api: YouTubeAPI, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    data = api.get("search", {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
    })
    results = []
    for item in data.get("items", []):
        vid = item.get("id", {}).get("videoId")
        snippet = item.get("snippet", {})
        results.append({
            "video_id": vid,
            "title": snippet.get("title"),
            "channel_title": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
        })
    return results


def get_api_key() -> str:
    return os.environ.get("YOUTUBE_API_KEY", "")


def to_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print("youtube_analyzer ready")
