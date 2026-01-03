# Document Processor Skill - 文档处理系统

**版本**: 2.0.0
**类型**: 外部集成
**质量等级**: A+

## 📋 功能概述

多格式文档解析和转换,支持PDF/Word/Excel/CSV等。

### 核心能力

1. **多格式支持** - PDF/DOCX/XLSX/CSV/Markdown/TXT自动识别
2. **OCR文字识别** - 扫描件PDF和图片文字提取
3. **表格提取** - 从PDF/Word自动提取表格并结构化
4. **格式转换** - PDF↔Word↔Markdown无损转换
5. **数据分析** - Excel/CSV自动统计分析和模式识别

## 🚀 使用方法

### Slash Command
```bash
/process-document [文件路径]
```

### 自然语言调用
```
解析这个PDF文件
从Excel表格中提取数据
将Word文档转换为Markdown
```

## 📖 使用示例

### 示例:解析PDF报告
**输入**:
```
/process-document report.pdf --extract-tables --ocr
```

**输出**:
- ✅ 文档类型: PDF
- ✅ 页数: 15页
- ✅ 文本提取: 完成 (12,345字)
- ✅ 表格提取: 发现3个表格
- ✅ OCR处理: 第3,7,12页 (扫描件)
- 📊 内容摘要:
  - 章节: 5个
  - 图片: 8张
  - 表格: 3个

## 📄 支持的文件格式

### 文档格式
- **PDF**: 文本PDF、扫描PDF、加密PDF
- **Word**: .docx、.doc (需转换)
- **Markdown**: .md、.markdown
- **纯文本**: .txt、.log

### 数据格式
- **Excel**: .xlsx、.xls
- **CSV**: .csv、.tsv
- **JSON**: .json
- **XML**: .xml

## 🔍 PDF处理能力

### 文本提取
```typescript
// 保留格式的文本提取
{
  extractText: true,
  preserveFormatting: true,
  pageRange: '1-10' // 或 'all'
}

// 输出:
{
  text: '完整文本内容...',
  pages: [
    { pageNumber: 1, text: '第1页内容...' },
    { pageNumber: 2, text: '第2页内容...' }
  ]
}
```

### 表格提取
```typescript
// 自动检测并提取表格
{
  extractTables: true
}

// 输出:
{
  tables: [
    {
      page: 3,
      rows: 10,
      columns: 5,
      data: [
        ['姓名', '年龄', '城市', '职位', '薪资'],
        ['张三', '28', '北京', '工程师', '15000']
      ]
    }
  ]
}
```

### OCR文字识别
```typescript
// 扫描件PDF文字识别
{
  ocrEnabled: true,
  ocrLanguage: 'chi_sim+eng' // 中英文混合
}

// 支持语言:
- eng: 英文
- chi_sim: 简体中文
- chi_tra: 繁体中文
- jpn: 日文
- kor: 韩文
```

## 📊 Excel数据分析

### 自动统计
```typescript
// Excel文件自动分析
{
  source: { type: 'file', data: 'sales.xlsx' },
  options: {
    xlsx: {
      analyzeData: true,
      sheets: ['2024年销售'] // 或 'all'
    }
  }
}

// 输出:
{
  statistics: {
    totalRows: 1234,
    totalColumns: 8,
    numericColumns: ['销售额', '数量', '利润'],
    summary: {
      '销售额': { sum: 1234567, avg: 1000, max: 5000, min: 100 },
      '数量': { sum: 5000, avg: 4, max: 50, min: 1 }
    }
  }
}
```

### 数据透视
```typescript
// 数据透视和分组
{
  pivot: {
    rows: ['地区', '产品'],
    columns: ['月份'],
    values: ['销售额'],
    aggregation: 'sum'
  }
}
```

## 🔄 格式转换

### PDF → Markdown
```typescript
{
  source: { type: 'file', data: 'doc.pdf' },
  convert: {
    targetFormat: 'markdown',
    options: {
      preserveHeadings: true, // 保留标题层级
      extractImages: true,    // 提取图片
      convertTables: true     // 表格转Markdown表格
    }
  }
}

// 输出:
# 第一章 引言

这是文档内容...

## 1.1 背景

| 项目 | 数量 | 金额 |
|------|------|------|
| A    | 10   | 100  |
```

### Word → PDF
```typescript
{
  source: { type: 'file', data: 'report.docx' },
  convert: {
    targetFormat: 'pdf',
    options: {
      preserveFormatting: true,
      pageSize: 'A4',
      orientation: 'portrait'
    }
  }
}
```

### Excel → JSON
```typescript
{
  source: { type: 'file', data: 'data.xlsx' },
  convert: {
    targetFormat: 'json',
    options: {
      headerRow: 1, // 第1行为表头
      skipEmptyRows: true
    }
  }
}

// 输出:
[
  { "姓名": "张三", "年龄": 28, "城市": "北京" },
  { "姓名": "李四", "年龄": 32, "城市": "上海" }
]
```

## 🖼️ 图片处理

### 从文档提取图片
```typescript
{
  extractImages: true,
  options: {
    imageFormat: 'png', // 或 'jpeg', 'original'
    minWidth: 100,      // 最小宽度(过滤小图标)
    minHeight: 100
  }
}

// 输出:
{
  images: [
    {
      page: 3,
      filename: 'image_001.png',
      width: 800,
      height: 600,
      base64: 'iVBORw0KGgoAAAANS...'
    }
  ]
}
```

## 📋 批量处理

### 批量文档转换
```typescript
{
  batchProcess: {
    files: [
      'report1.pdf',
      'report2.pdf',
      'report3.pdf'
    ],
    operation: 'convert',
    targetFormat: 'markdown',
    parallel: true, // 并行处理
    maxConcurrency: 3
  }
}

// 进度追踪:
Processing: 33% (1/3 files)
  ✅ report1.pdf → report1.md
  ⏳ report2.pdf (processing...)
  ⏳ report3.pdf (queued)
```

## 🛠️ 最佳实践

1. **启用OCR**: 对扫描件PDF必须启用OCR
2. **指定页面范围**: 大文件只处理需要的页面
3. **选择合适语言**: OCR语言设置影响识别准确率
4. **批量处理**: 多文件使用批量模式提升效率
5. **缓存结果**: 重复处理启用缓存节省时间

## 🔗 与其他 Skills 配合

- `log-analyzer`: 分析日志文件
- `data-analysis`: 深度数据分析
- `ai-summarizer`: 文档内容摘要

---

**状态**: ✅ 生产就绪 | **质量等级**: A+
