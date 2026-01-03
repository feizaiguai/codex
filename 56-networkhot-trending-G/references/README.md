# References Directory

This directory contains reference documentation for the networkhot-trending skill.

## Available References

- API documentation for TianAPI Network Hot Search
- Best practices for hot topic analysis
- Example reports and use cases

## API Documentation

### TianAPI Network Hot Search API

**Endpoint**: `https://apis.tianapi.com/networkhot/index`

**Parameters**:
- `key`: API密钥（必需）

**Response Format**:
```json
{
  "code": 200,
  "msg": "success",
  "result": {
    "list": [
      {
        "title": "热搜标题",
        "hotnum": "1234567",
        "digest": "摘要",
        "url": "链接",
        "mobilurl": "移动端链接",
        "tag": "标签"
      }
    ]
  }
}
```

## Related Documentation

- [15-web-search Skill Documentation](../../15-web-search/SKILL.md)
- [TianAPI Official Documentation](https://www.tianapi.com/apiview/223)
