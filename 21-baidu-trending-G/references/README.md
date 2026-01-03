# References - 参考文档

此目录包含百度热搜分析器的参考文档和资源。

## 数据源

- **百度热搜官网**: https://top.baidu.com
- **API文档**: 百度官方API (无公开文档，通过逆向工程获取)

## API接口

### 百度热搜API

**URL**: `https://top.baidu.com/api/board?platform=wise&tab=realtime`

**方法**: GET

**参数**:
- `platform`: wise (移动端)
- `tab`: realtime (实时热搜)

**响应示例**:
```json
{
  "success": true,
  "data": {
    "cards": [{
      "content": [{
        "content": [{
          "index": 1,
          "word": "话题标题",
          "url": "https://m.baidu.com/s?word=...",
          "hotTag": "3",
          "newHotName": "热",
          "isTop": false
        }]
      }]
    }]
  }
}
```

### 天行网络热搜API (备用)

**URL**: `https://apis.tianapi.com/nethot/index`

**方法**: GET

**参数**:
- `key`: 天行API密钥

**响应示例**:
```json
{
  "code": 200,
  "msg": "success",
  "result": {
    "list": [{
      "keyword": ""反腐败没有选择 必须知难而进"",
      "brief": "中共中央政治局12月25日召开会议...",
      "index": "7903980",
      "trend": "新"
    }]
  }
}
```

**字段说明**:
- `keyword`: 热搜话题标题
- `brief`: 话题简介/摘要
- `index`: 热度指数
- `trend`: 趋势标签（新/热）

**数据来源**: 聚合多平台网络热搜

**测试状态**: ✅ 已测试可用（2025-12-29）

## 相关链接

- **15-web-search skill**: C:/Users/bigbao/.claude/skills/15-web-search/
- **百度搜索指数**: https://index.baidu.com
- **百度风云榜**: https://top.baidu.com/board
- **天行数据**: https://www.tianapi.com

## 更新日志

### 2025-12-29
- 初始版本发布
- 集成百度官方API
- 添加15-web-search集成
- 添加天行网络热搜备用API
