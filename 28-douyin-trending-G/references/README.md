# References - 参考文档

此目录包含抖音热搜分析器的参考文档和资源。

## 数据源

- **抖音官网**: https://www.douyin.com
- **天行API**: https://www.tianapi.com

## API接口

### 天行API - 抖音热搜

**URL**: `https://apis.tianapi.com/douyinhot/index`

**方法**: GET

**参数**:
- `key`: API密钥

**响应示例**:
```json
{
  "code": 200,
  "msg": "success",
  "result": {
    "list": [{
      "hotindex": 11998468,
      "label": 3,
      "word": "话题标题"
    }]
  }
}
```

**标签说明**:
- 0: 无标签
- 1: 新
- 2: 热
- 3: 爆
- 8: 视频
- 9: 挑战
- 16: 话题
- 17: 音乐

## 相关链接

- **15-web-search skill**: C:/Users/bigbao/.claude/skills/15-web-search/
- **天行数据**: https://www.tianapi.com

## 备用API

### API盒子 - 抖音热搜

**URL**: `https://cn.apihz.cn/api/xinwen/douyin.php`

**方法**: GET

**参数**:
- `id`: API ID（需注册）

**注册地址**: https://www.apihz.cn

**配额**: 免费版有调用次数限制

**状态**: ⚠️ 需要注册获取ID（2025-12-29）

---

### AA1.cn - 抖音热搜

**文档URL**: https://api.aa1.cn/doc/douyin-hot.html

**方法**: GET

**参数**: 需查看官方文档

**配额**: 需查看官方文档

**状态**: ⚠️ 需要查看官方文档并注册

---

## 更新日志

### 2025-12-29
- 初始版本发布
- 集成天行API
- 添加15-web-search集成
- 添加备用API文档（API盒子、AA1.cn）
