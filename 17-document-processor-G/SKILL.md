---
name: 17-document-processor-G
description: Document processing system for multi-format document parsing and conversion. Supports multiple formats (PDF/DOCX/XLSX/CSV/TXT), OCR processing (Tesseract/Cloud Vision), table extraction and structuring, format conversion (PDF↔DOCX↔Markdown), data analysis (Excel/CSV data processing). Use for document automation, data extraction, format conversion.
---

# Document Processor

**Version**: 2.0.0
**Priority**: P1
**Category**: External Integration
**Status**: Production Ready

## Description

Intelligent document processing system that handles multiple file formats (PDF, DOCX, XLSX, CSV, Markdown) with advanced parsing, content extraction, and format conversion capabilities. Supports OCR for scanned documents, table extraction, data analysis, and automatic format detection.

**Core Capabilities**:
- **Multi-Format Document Parsing**: PDF, Word, Excel, CSV, Markdown with automatic format detection
- **Advanced Content Extraction**: Text, tables, images, metadata with structural preservation
- **OCR Processing**: Extract text from scanned documents and images with high accuracy
- **Intelligent Format Conversion**: Convert between formats while preserving structure and formatting
- **Data Analysis**: Automatic data type detection, statistics, and pattern recognition for structured data
- **Batch Processing**: Handle multiple documents efficiently with progress tracking

## Instructions

### Trigger Conditions

Activate this skill when user requests involve:

1. **Document Parsing**:
   - "Parse this PDF document"
   - "Extract text from this Word file"
   - "Read data from this Excel spreadsheet"
   - "Convert this document to Markdown"

2. **Content Extraction**:
   - "Extract all tables from this PDF"
   - "Get images from this document"
   - "Parse the metadata of this file"
   - "Extract specific sections from this document"

3. **OCR Processing**:
   - "Read text from this scanned PDF"
   - "Extract text from this image"
   - "Process this scanned document"

4. **Format Conversion**:
   - "Convert PDF to Markdown"
   - "Export Excel data to CSV"
   - "Transform Word document to plain text"

5. **Data Analysis**:
   - "Analyze data in this spreadsheet"
   - "Summarize statistics from this Excel file"
   - "Find patterns in this CSV data"

### Execution Flow

```mermaid
graph TD
    A[Document Input] --> B{Detect Format}
    B -->|PDF| C[PDF Parser]
    B -->|DOCX| D[Word Parser]
    B -->|XLSX| E[Excel Parser]
    B -->|CSV| F[CSV Parser]
    B -->|Markdown| G[Markdown Parser]

    C --> H{OCR Required?}
    H -->|Yes| I[OCR Processing]
    H -->|No| J[Text Extraction]
    I --> J

    J --> K[Structure Analysis]
    D --> K
    E --> L[Data Processing]
    F --> L
    G --> K

    K --> M{Extract Tables?}
    M -->|Yes| N[Table Extraction]
    M -->|No| O[Content Processing]
    N --> O

    L --> P{Analyze Data?}
    P -->|Yes| Q[Statistical Analysis]
    P -->|No| O
    Q --> O

    O --> R{Convert Format?}
    R -->|Yes| S[Format Conversion]
    R -->|No| T[Return Results]
    S --> T
```

## Input/Output

### Input Interface

```typescript
/**
 * Document Processor input configuration
 */
interface DocumentProcessorInput {
  /**
   * Document source configuration
   */
  source: {
    /**
     * Source type
     * - file: Local file path
     * - url: Remote URL to download
     * - base64: Base64-encoded document data
     * - buffer: Binary buffer data
     */
    type: 'file' | 'url' | 'base64' | 'buffer';

    /**
     * Source data (path, URL, or encoded content)
     */
    data: string | Buffer;

    /**
     * Original filename (for format detection)
     */
    filename?: string;
  };

  /**
   * Document format
   * - auto: Automatic detection from filename/content
   */
  format?: 'pdf' | 'docx' | 'xlsx' | 'csv' | 'markdown' | 'txt' | 'auto';

  /**
   * Processing options
   */
  options?: {
    /**
     * PDF-specific options
     */
    pdf?: {
      /**
       * Extract text content
       * @default true
       */
      extractText?: boolean;

      /**
       * Extract tables from PDF
       * @default false
       */
      extractTables?: boolean;

      /**
       * Extract embedded images
       * @default false
       */
      extractImages?: boolean;

      /**
       * Enable OCR for scanned PDFs
       * @default false
       */
      ocrEnabled?: boolean;

      /**
       * OCR language (ISO 639-1 code)
       * @default 'eng'
       */
      ocrLanguage?: string;

      /**
       * Page range to process (e.g., "1-5", "1,3,5", "all")
       * @default 'all'
       */
      pageRange?: string;

      /**
       * Preserve text formatting and structure
       * @default true
       */
      preserveFormatting?: boolean;

      /**
       * Extract PDF metadata
       * @default true
       */
      extractMetadata?: boolean;
    };

    /**
     * Word document options
     */
    docx?: {
      /**
       * Extract text content
       * @default true
       */
      extractText?: boolean;

      /**
       * Extract tables
       * @default false
       */
      extractTables?: boolean;

      /**
       * Extract images with base64 encoding
       * @default false
       */
      extractImages?: boolean;

      /**
       * Preserve paragraph styles (headings, bold, italic)
       * @default true
       */
      preserveStyles?: boolean;

      /**
       * Convert to Markdown format
       * @default false
       */
      convertToMarkdown?: boolean;

      /**
       * Extract comments and track changes
       * @default false
       */
      includeComments?: boolean;
    };

    /**
     * Excel spreadsheet options
     */
    xlsx?: {
      /**
       * Specific sheets to process (empty = all sheets)
       * @default []
       */
      sheets?: string[];

      /**
       * Evaluate formulas to get calculated values
       * @default true
       */
      evaluateFormulas?: boolean;

      /**
       * Include empty cells in output
       * @default false
       */
      includeEmpty?: boolean;

      /**
       * Parse as JSON with column headers as keys
       * @default false
       */
      headerRow?: boolean;

      /**
       * Analyze data types automatically
       * @default false
       */
      analyzeDataTypes?: boolean;

      /**
       * Calculate statistics for numeric columns
       * @default false
       */
      calculateStats?: boolean;

      /**
       * Detect and parse dates
       * @default true
       */
      parseDates?: boolean;

      /**
       * Cell range to extract (e.g., "A1:D10")
       */
      range?: string;
    };

    /**
     * CSV processing options
     */
    csv?: {
      /**
       * Column delimiter
       * @default ','
       */
      delimiter?: ',' | ';' | '\t' | '|';

      /**
       * First row contains headers
       * @default true
       */
      hasHeaders?: boolean;

      /**
       * Quote character for escaped values
       * @default '"'
       */
      quoteChar?: string;

      /**
       * Encoding (utf8, latin1, etc.)
       * @default 'utf8'
       */
      encoding?: string;

      /**
       * Automatically detect data types
       * @default true
       */
      autoDetectTypes?: boolean;

      /**
       * Skip empty rows
       * @default true
       */
      skipEmptyRows?: boolean;

      /**
       * Maximum rows to process (0 = unlimited)
       * @default 0
       */
      maxRows?: number;
    };

    /**
     * Output format conversion
     */
    outputFormat?: {
      /**
       * Target format for conversion
       */
      target: 'markdown' | 'json' | 'html' | 'plain-text' | 'csv';

      /**
       * Markdown-specific options
       */
      markdown?: {
        /**
         * Include table of contents
         * @default false
         */
        includeToc?: boolean;

        /**
         * Heading level offset (add to all heading levels)
         * @default 0
         */
        headingOffset?: number;

        /**
         * Code fence style for code blocks
         * @default 'backticks'
         */
        codeFence?: 'backticks' | 'tilde';
      };

      /**
       * JSON-specific options
       */
      json?: {
        /**
         * Pretty print with indentation
         * @default true
         */
        pretty?: boolean;

        /**
         * Include metadata in output
         * @default false
         */
        includeMetadata?: boolean;
      };
    };

    /**
     * Processing preferences
     */
    processing?: {
      /**
       * Maximum file size in MB (0 = unlimited)
       * @default 50
       */
      maxSizeMB?: number;

      /**
       * Processing timeout in milliseconds
       * @default 60000
       */
      timeout?: number;

      /**
       * Use parallel processing for multi-page documents
       * @default true
       */
      parallel?: boolean;

      /**
       * Cache parsed results
       * @default false
       */
      enableCache?: boolean;

      /**
       * Cache TTL in seconds
       * @default 3600
       */
      cacheTTL?: number;
    };
  };
}

/**
 * Document Processor output
 */
interface DocumentProcessorOutput {
  /**
   * Processing success status
   */
  success: boolean;

  /**
   * Document metadata
   */
  metadata: {
    /**
     * Original filename
     */
    filename: string;

    /**
     * Detected or specified format
     */
    format: string;

    /**
     * File size in bytes
     */
    sizeBytes: number;

    /**
     * Number of pages (for paginated formats)
     */
    pageCount?: number;

    /**
     * Document creation date
     */
    createdDate?: string;

    /**
     * Document modification date
     */
    modifiedDate?: string;

    /**
     * Document author
     */
    author?: string;

    /**
     * Document title
     */
    title?: string;

    /**
     * Additional custom metadata
     */
    custom?: Record<string, any>;
  };

  /**
   * Extracted content
   */
  content: {
    /**
     * Plain text content
     */
    text?: string;

    /**
     * Structured content by page/section
     */
    pages?: Array<{
      pageNumber: number;
      text: string;
      tables?: any[];
      images?: any[];
    }>;

    /**
     * Extracted tables
     */
    tables?: Array<{
      /**
       * Table index
       */
      index: number;

      /**
       * Page number (if applicable)
       */
      page?: number;

      /**
       * Table headers
       */
      headers: string[];

      /**
       * Table rows
       */
      rows: any[][];

      /**
       * Table data as JSON (if headers available)
       */
      data?: Record<string, any>[];
    }>;

    /**
     * Extracted images
     */
    images?: Array<{
      /**
       * Image index
       */
      index: number;

      /**
       * Page number (if applicable)
       */
      page?: number;

      /**
       * Image format
       */
      format: string;

      /**
       * Base64-encoded image data
       */
      data: string;

      /**
       * Image width in pixels
       */
      width?: number;

      /**
       * Image height in pixels
       */
      height?: number;
    }>;

    /**
     * Structured data (for spreadsheets/CSV)
     */
    data?: Array<{
      /**
       * Sheet name (for Excel)
       */
      sheet?: string;

      /**
       * Column headers
       */
      headers: string[];

      /**
       * Row data
       */
      rows: any[][];

      /**
       * Data as JSON objects (if headers available)
       */
      records?: Record<string, any>[];

      /**
       * Data type analysis
       */
      types?: Record<string, 'string' | 'number' | 'date' | 'boolean'>;

      /**
       * Statistical summary (if calculated)
       */
      statistics?: Record<string, {
        min?: number;
        max?: number;
        mean?: number;
        median?: number;
        stdDev?: number;
        count: number;
        nullCount: number;
      }>;
    }>;
  };

  /**
   * Converted output (if format conversion requested)
   */
  converted?: {
    /**
     * Target format
     */
    format: string;

    /**
     * Converted content
     */
    content: string;
  };

  /**
   * OCR results (if OCR was performed)
   */
  ocr?: {
    /**
     * OCR engine used
     */
    engine: string;

    /**
     * Language detected/used
     */
    language: string;

    /**
     * Average confidence score (0-100)
     */
    confidence: number;

    /**
     * Per-page OCR details
     */
    pages?: Array<{
      pageNumber: number;
      text: string;
      confidence: number;
    }>;
  };

  /**
   * Processing performance metrics
   */
  performance: {
    /**
     * Total processing time in milliseconds
     */
    processingTime: number;

    /**
     * Parse time
     */
    parseTime?: number;

    /**
     * OCR time (if applicable)
     */
    ocrTime?: number;

    /**
     * Conversion time (if applicable)
     */
    conversionTime?: number;

    /**
     * Memory usage in MB
     */
    memoryUsage?: number;
  };

  /**
   * Warnings and non-critical issues
   */
  warnings?: Array<{
    code: string;
    message: string;
    page?: number;
  }>;

  /**
   * Error information (if success is false)
   */
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}
```


---

## TypeScript接口

### 基础输出接口

所有Skill的输出都继承自`BaseOutput`统一接口：

```typescript
interface BaseOutput {
  success: boolean;
  error?: {
    code: string;
    message: string;
    suggestedFix?: string;
  };
  metadata?: {
    requestId: string;
    timestamp: string;
    version: string;
  };
  warnings?: Array<{
    code: string;
    message: string;
    severity: 'low' | 'medium' | 'high';
  }>;
}
```

### 输入接口

```typescript
interface DocumentProcessorInput {

  quotaMonitoring?: {
    enabled: boolean;
    dailyLimit?: number;
    warningThreshold?: number;
    resetTime?: string;
    fallbackStrategy?: 'cache' | 'queue' | 'fail';
    provider?: string;
  };
}
```

### 输出接口

```typescript
interface DocumentProcessorOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段

  quotaUsage?: {
    used: number;
    limit: number;
    remaining: number;
    percentUsed: number;
    resetAt: string;
    willExceed: boolean;
    costEstimate?: number;
  };
}
```

---

## Examples

### Example 1: PDF Technical Document Parsing with Table Extraction

**Scenario**: Parse a technical PDF document, extract all tables, and convert to Markdown.

**User Request**:
> "Parse this technical specification PDF and extract all tables. Convert the content to Markdown format."

**Implementation**:

```typescript
import { DocumentProcessor } from '@/skills/17-document-processor';
import * as fs from 'fs/promises';

async function parseTechnicalPDF() {
  const processor = new DocumentProcessor();

  // Configure PDF processing with table extraction
  const input: DocumentProcessorInput = {
    source: {
      type: 'file',
      data: './docs/api-specification-v2.pdf',
      filename: 'api-specification-v2.pdf'
    },
    format: 'pdf',
    options: {
      pdf: {
        extractText: true,
        extractTables: true,
        extractImages: false,
        ocrEnabled: false,  // Not needed for digital PDF
        pageRange: 'all',
        preserveFormatting: true,
        extractMetadata: true
      },
      outputFormat: {
        target: 'markdown',
        markdown: {
          includeToc: true,
          headingOffset: 0,
          codeFence: 'backticks'
        }
      },
      processing: {
        maxSizeMB: 50,
        timeout: 120000,  // 2 minutes
        parallel: true,
        enableCache: true,
        cacheTTL: 3600
      }
    }
  };

  console.log('📄 Processing PDF document...');
  const startTime = Date.now();

  const result = await processor.process(input);

  if (!result.success) {
    console.error('❌ Processing failed:', result.error);
    return;
  }

  // Display metadata
  console.log('\n📋 Document Metadata:');
  console.log(`  Title: ${result.metadata.title}`);
  console.log(`  Author: ${result.metadata.author}`);
  console.log(`  Pages: ${result.metadata.pageCount}`);
  console.log(`  Size: ${(result.metadata.sizeBytes / 1024).toFixed(2)} KB`);
  console.log(`  Created: ${result.metadata.createdDate}`);

  // Display extracted tables
  console.log(`\n📊 Extracted ${result.content.tables?.length || 0} tables:`);

  result.content.tables?.forEach((table, index) => {
    console.log(`\nTable ${index + 1} (Page ${table.page}):`);
    console.log(`  Headers: ${table.headers.join(', ')}`);
    console.log(`  Rows: ${table.rows.length}`);

    // Display table in formatted text
    console.log('\n  Preview:');
    const headerRow = '| ' + table.headers.join(' | ') + ' |';
    const separator = '| ' + table.headers.map(() => '---').join(' | ') + ' |';
    console.log('  ' + headerRow);
    console.log('  ' + separator);

    // Show first 3 rows
    table.rows.slice(0, 3).forEach(row => {
      const rowStr = '| ' + row.join(' | ') + ' |';
      console.log('  ' + rowStr);
    });

    if (table.rows.length > 3) {
      console.log(`  ... (${table.rows.length - 3} more rows)`);
    }
  });

  // Save Markdown output
  if (result.converted) {
    const outputPath = './output/api-specification.md';
    await fs.writeFile(outputPath, result.converted.content);
    console.log(`\n✅ Markdown output saved to: ${outputPath}`);

    // Display sample of converted content
    console.log('\n📝 Markdown Preview (first 500 chars):');
    console.log(result.converted.content.substring(0, 500));
    console.log('...\n');
  }

  // Performance metrics
  console.log('⚡ Performance:');
  console.log(`  Total time: ${result.performance.processingTime}ms`);
  console.log(`  Parse time: ${result.performance.parseTime}ms`);
  console.log(`  Conversion time: ${result.performance.conversionTime}ms`);
  console.log(`  Memory usage: ${result.performance.memoryUsage?.toFixed(2)} MB`);

  // Handle warnings
  if (result.warnings && result.warnings.length > 0) {
    console.log(`\n⚠️  ${result.warnings.length} warnings:`);
    result.warnings.forEach(warning => {
      console.log(`  - ${warning.message} (Page ${warning.page})`);
    });
  }

  return result;
}

// Run the parser
parseTechnicalPDF()
  .then(() => console.log('\n✨ PDF processing complete'))
  .catch(err => console.error('💥 Error:', err));
```

**Expected Output**:
```
📄 Processing PDF document...

📋 Document Metadata:
  Title: API Specification v2.0
  Author: Engineering Team
  Pages: 45
  Size: 2048.50 KB
  Created: 2024-01-15T10:30:00Z

📊 Extracted 8 tables:

Table 1 (Page 5):
  Headers: Endpoint, Method, Description, Auth Required
  Rows: 12

  Preview:
  | Endpoint | Method | Description | Auth Required |
  | --- | --- | --- | --- |
  | /api/users | GET | List all users | Yes |
  | /api/users/{id} | GET | Get user by ID | Yes |
  | /api/users | POST | Create new user | Yes |
  ... (9 more rows)

Table 2 (Page 8):
  Headers: Status Code, Message, Description
  Rows: 8

  Preview:
  | Status Code | Message | Description |
  | --- | --- | --- |
  | 200 | OK | Request successful |
  | 201 | Created | Resource created |
  | 400 | Bad Request | Invalid request |
  ... (5 more rows)

... (6 more tables)

✅ Markdown output saved to: ./output/api-specification.md

📝 Markdown Preview (first 500 chars):
# Table of Contents

1. [Introduction](#introduction)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Error Handling](#error-handling)

# Introduction

This document describes the API Specification v2.0 for our platform...

## Authentication

All API requests require authentication using Bearer tokens...

| Endpoint | Method | Description | Auth Required |
| --- | --- | --- | --- |
| /api/users | GET | List all users | Yes |
...

⚡ Performance:
  Total time: 4567ms
  Parse time: 3200ms
  Conversion time: 1367ms
  Memory usage: 145.23 MB

⚠️  2 warnings:
  - Complex table structure detected, formatting may vary (Page 23)
  - Image extraction skipped as not requested (Page 12)

✨ PDF processing complete
```

### Example 2: Excel Sales Data Analysis

**Scenario**: Process an Excel sales report, analyze data types, calculate statistics, and export to JSON.

**User Request**:
> "Analyze the sales data in this Excel file. Calculate statistics for numeric columns and export to JSON."

**Implementation**:

```typescript
import { DocumentProcessor } from '@/skills/17-document-processor';
import * as fs from 'fs/promises';

async function analyzeSalesData() {
  const processor = new DocumentProcessor();

  const input: DocumentProcessorInput = {
    source: {
      type: 'file',
      data: './data/sales-report-q4-2024.xlsx',
      filename: 'sales-report-q4-2024.xlsx'
    },
    format: 'xlsx',
    options: {
      xlsx: {
        sheets: ['Sales Data', 'Summary'],  // Process specific sheets
        evaluateFormulas: true,
        includeEmpty: false,
        headerRow: true,
        analyzeDataTypes: true,
        calculateStats: true,
        parseDates: true,
        range: undefined  // Process entire sheet
      },
      outputFormat: {
        target: 'json',
        json: {
          pretty: true,
          includeMetadata: true
        }
      },
      processing: {
        maxSizeMB: 25,
        timeout: 60000,
        parallel: true,
        enableCache: false
      }
    }
  };

  console.log('📊 Analyzing Excel sales data...');

  const result = await processor.process(input);

  if (!result.success) {
    console.error('❌ Analysis failed:', result.error);
    return;
  }

  // Process each sheet
  result.content.data?.forEach((sheet, sheetIndex) => {
    console.log(`\n📄 Sheet: ${sheet.sheet || `Sheet ${sheetIndex + 1}`}`);
    console.log(`  Rows: ${sheet.rows.length}`);
    console.log(`  Columns: ${sheet.headers.length}`);

    // Display data types
    console.log('\n  📋 Column Data Types:');
    Object.entries(sheet.types || {}).forEach(([column, type]) => {
      console.log(`    ${column}: ${type}`);
    });

    // Display statistics for numeric columns
    if (sheet.statistics) {
      console.log('\n  📈 Statistical Summary:');
      Object.entries(sheet.statistics).forEach(([column, stats]) => {
        console.log(`\n    ${column}:`);
        console.log(`      Count: ${stats.count}`);
        console.log(`      Null Count: ${stats.nullCount}`);

        if (stats.min !== undefined) {
          console.log(`      Min: ${stats.min.toFixed(2)}`);
          console.log(`      Max: ${stats.max!.toFixed(2)}`);
          console.log(`      Mean: ${stats.mean!.toFixed(2)}`);
          console.log(`      Median: ${stats.median!.toFixed(2)}`);
          console.log(`      Std Dev: ${stats.stdDev!.toFixed(2)}`);
        }
      });
    }

    // Display sample records
    console.log('\n  📝 Sample Records (first 3):');
    sheet.records?.slice(0, 3).forEach((record, index) => {
      console.log(`\n    Record ${index + 1}:`);
      Object.entries(record).forEach(([key, value]) => {
        console.log(`      ${key}: ${value}`);
      });
    });

    if ((sheet.records?.length || 0) > 3) {
      console.log(`\n    ... (${(sheet.records?.length || 0) - 3} more records)`);
    }
  });

  // Save JSON output
  if (result.converted) {
    const outputPath = './output/sales-report.json';
    await fs.writeFile(outputPath, result.converted.content);
    console.log(`\n✅ JSON output saved to: ${outputPath}`);
  }

  // Display performance
  console.log('\n⚡ Performance:');
  console.log(`  Processing time: ${result.performance.processingTime}ms`);
  console.log(`  Memory usage: ${result.performance.memoryUsage?.toFixed(2)} MB`);

  return result;
}

// Run the analyzer
analyzeSalesData()
  .then(() => console.log('\n✨ Analysis complete'))
  .catch(err => console.error('💥 Error:', err));
```

**Expected Output**:
```
📊 Analyzing Excel sales data...

📄 Sheet: Sales Data
  Rows: 1,247
  Columns: 8

  📋 Column Data Types:
    Date: date
    Region: string
    Product: string
    Quantity: number
    Unit Price: number
    Total: number
    Sales Rep: string
    Status: string

  📈 Statistical Summary:

    Quantity:
      Count: 1247
      Null Count: 0
      Min: 1.00
      Max: 500.00
      Mean: 87.34
      Median: 75.00
      Std Dev: 45.23

    Unit Price:
      Count: 1247
      Null Count: 0
      Min: 9.99
      Max: 999.99
      Mean: 245.67
      Median: 199.99
      Std Dev: 156.89

    Total:
      Count: 1247
      Null Count: 0
      Min: 19.98
      Max: 49999.50
      Mean: 21456.32
      Median: 14999.25
      Std Dev: 12345.67

  📝 Sample Records (first 3):

    Record 1:
      Date: 2024-10-01T00:00:00.000Z
      Region: North
      Product: Widget Pro
      Quantity: 125
      Unit Price: 199.99
      Total: 24998.75
      Sales Rep: John Smith
      Status: Completed

    Record 2:
      Date: 2024-10-01T00:00:00.000Z
      Region: South
      Product: Gadget Plus
      Quantity: 75
      Unit Price: 149.99
      Total: 11249.25
      Sales Rep: Jane Doe
      Status: Completed

    Record 3:
      Date: 2024-10-02T00:00:00.000Z
      Region: East
      Product: Widget Pro
      Quantity: 200
      Unit Price: 199.99
      Total: 39998.00
      Sales Rep: Bob Johnson
      Status: Pending

    ... (1244 more records)

📄 Sheet: Summary
  Rows: 4
  Columns: 3

  📋 Column Data Types:
    Region: string
    Total Sales: number
    Count: number

  📈 Statistical Summary:

    Total Sales:
      Count: 4
      Null Count: 0
      Min: 4567890.12
      Max: 8901234.56
      Mean: 6734562.34
      Median: 6500000.00
      Std Dev: 1234567.89

    Count:
      Count: 4
      Null Count: 0
      Min: 245.00
      Max: 412.00
      Mean: 311.75
      Median: 302.50
      Std Dev: 67.34

  📝 Sample Records (first 3):

    Record 1:
      Region: North
      Total Sales: 8901234.56
      Count: 412

    Record 2:
      Region: South
      Total Sales: 5678901.23
      Count: 302

    Record 3:
      Region: East
      Total Sales: 7345678.90
      Count: 321

    ... (1 more records)

✅ JSON output saved to: ./output/sales-report.json

⚡ Performance:
  Processing time: 2345ms
  Memory usage: 87.45 MB

✨ Analysis complete
```

### Example 3: OCR Processing for Scanned Document

**Scenario**: Process a scanned PDF document using OCR to extract text content.

**User Request**:
> "Extract text from this scanned contract PDF using OCR. It's in English."

**Implementation**:

```typescript
import { DocumentProcessor } from '@/skills/17-document-processor';
import * as fs from 'fs/promises';

async function processScannedDocument() {
  const processor = new DocumentProcessor();

  const input: DocumentProcessorInput = {
    source: {
      type: 'file',
      data: './contracts/vendor-agreement-signed.pdf',
      filename: 'vendor-agreement-signed.pdf'
    },
    format: 'pdf',
    options: {
      pdf: {
        extractText: true,
        extractTables: false,
        extractImages: false,
        ocrEnabled: true,  // Enable OCR for scanned content
        ocrLanguage: 'eng',
        pageRange: 'all',
        preserveFormatting: true,
        extractMetadata: true
      },
      outputFormat: {
        target: 'plain-text'
      },
      processing: {
        maxSizeMB: 100,
        timeout: 180000,  // 3 minutes for OCR
        parallel: true,
        enableCache: true,
        cacheTTL: 7200  // Cache for 2 hours
      }
    }
  };

  console.log('🔍 Processing scanned PDF with OCR...');
  console.log('⏳ This may take a few minutes...');

  const result = await processor.process(input);

  if (!result.success) {
    console.error('❌ OCR processing failed:', result.error);
    return;
  }

  // Display OCR results
  if (result.ocr) {
    console.log('\n🔤 OCR Results:');
    console.log(`  Engine: ${result.ocr.engine}`);
    console.log(`  Language: ${result.ocr.language}`);
    console.log(`  Average Confidence: ${result.ocr.confidence.toFixed(2)}%`);

    // Display per-page confidence
    console.log('\n  📄 Per-Page Confidence:');
    result.ocr.pages?.forEach(page => {
      const confidenceBar = '█'.repeat(Math.floor(page.confidence / 10));
      console.log(`    Page ${page.pageNumber}: ${page.confidence.toFixed(1)}% ${confidenceBar}`);
    });
  }

  // Display metadata
  console.log('\n📋 Document Metadata:');
  console.log(`  Pages: ${result.metadata.pageCount}`);
  console.log(`  Size: ${(result.metadata.sizeBytes / 1024 / 1024).toFixed(2)} MB`);

  // Display extracted text sample
  console.log('\n📝 Extracted Text (first 1000 characters):');
  const textSample = result.content.text?.substring(0, 1000) || '';
  console.log(textSample);
  console.log('...\n');

  // Save full text output
  if (result.converted) {
    const outputPath = './output/vendor-agreement-extracted.txt';
    await fs.writeFile(outputPath, result.converted.content);
    console.log(`✅ Full text saved to: ${outputPath}`);
    console.log(`   Total characters: ${result.converted.content.length}`);
    console.log(`   Total words: ${result.converted.content.split(/\s+/).length}`);
  }

  // Performance metrics
  console.log('\n⚡ Performance:');
  console.log(`  Total time: ${(result.performance.processingTime / 1000).toFixed(2)}s`);
  console.log(`  OCR time: ${(result.performance.ocrTime! / 1000).toFixed(2)}s`);
  console.log(`  Memory usage: ${result.performance.memoryUsage?.toFixed(2)} MB`);

  // Low confidence warnings
  const lowConfidencePages = result.ocr?.pages?.filter(p => p.confidence < 80) || [];
  if (lowConfidencePages.length > 0) {
    console.log(`\n⚠️  ${lowConfidencePages.length} pages with low OCR confidence (<80%):`);
    lowConfidencePages.forEach(page => {
      console.log(`  - Page ${page.pageNumber}: ${page.confidence.toFixed(1)}%`);
    });
    console.log('  Consider manual review for these pages.');
  }

  return result;
}

// Run OCR processing
processScannedDocument()
  .then(() => console.log('\n✨ OCR processing complete'))
  .catch(err => console.error('💥 Error:', err));
```

**Expected Output**:
```
🔍 Processing scanned PDF with OCR...
⏳ This may take a few minutes...

🔤 OCR Results:
  Engine: Tesseract 5.3.0
  Language: eng
  Average Confidence: 92.34%

  📄 Per-Page Confidence:
    Page 1: 95.2% █████████
    Page 2: 93.8% █████████
    Page 3: 89.1% ████████
    Page 4: 91.5% █████████
    Page 5: 94.7% █████████

📋 Document Metadata:
  Pages: 5
  Size: 8.45 MB

📝 Extracted Text (first 1000 characters):
VENDOR AGREEMENT

This Vendor Agreement ("Agreement") is entered into as of January 15, 2024
("Effective Date") by and between:

ACME Corporation, a Delaware corporation with its principal place of business
at 123 Main Street, San Francisco, CA 94105 ("Company"), and

Widget Suppliers Inc., a California corporation with its principal place of
business at 456 Oak Avenue, Los Angeles, CA 90001 ("Vendor").

RECITALS

WHEREAS, Company desires to engage Vendor to provide certain products and
services as described herein; and

WHEREAS, Vendor agrees to provide such products and services in accordance
with the terms and conditions set forth in this Agreement.

NOW, THEREFORE, in consideration of the mutual covenants and agreements
contained herein, and for other good and valuable consideration, the receipt
and sufficiency of which are hereby acknowledged, the parties agree as follows:

1. SERVICES AND DELIVERABLES

1.1 Services. Vendor shall provide the following services to Company:
    (a) Manufacturing and delivery of widgets as specified in Exhibit A
    (b) Quality assurance and testing
    (c) Technical support and...
...

✅ Full text saved to: ./output/vendor-agreement-extracted.txt
   Total characters: 45,678
   Total words: 7,234

⚡ Performance:
  Total time: 127.45s
  OCR time: 118.23s
  Memory usage: 512.34 MB

⚠️  1 pages with low OCR confidence (<80%):
  - Page 3: 78.9%
  Consider manual review for these pages.

✨ OCR processing complete
```

## Best Practices

### Document Parsing

1. **Format Detection**:
   ```typescript
   // Let the processor auto-detect format when possible
   const input: DocumentProcessorInput = {
     source: { type: 'file', data: filePath },
     format: 'auto'  // Automatic detection
   };

   // Specify format explicitly for better performance
   const inputExplicit: DocumentProcessorInput = {
     source: { type: 'file', data: 'report.pdf' },
     format: 'pdf'  // Skip detection
   };
   ```

2. **Page Range Optimization**:
   ```typescript
   // Only process needed pages to save time
   options: {
     pdf: {
       pageRange: '1-5',  // First 5 pages only
       // or: '1,3,5,7'   // Specific pages
       // or: '10-end'    // From page 10 to end
     }
   }
   ```

3. **Memory Management**:
   ```typescript
   // Set appropriate limits for large documents
   options: {
     processing: {
       maxSizeMB: 100,         // Reject files > 100MB
       timeout: 300000,        // 5-minute timeout
       parallel: true,         // Use parallel processing
     }
   }
   ```

### Content Extraction

1. **Selective Extraction**:
   ```typescript
   // Only extract what you need
   options: {
     pdf: {
       extractText: true,
       extractTables: false,    // Skip if not needed
       extractImages: false,    // Skip to save time
     }
   }
   ```

2. **Table Processing**:
   ```typescript
   // Process tables efficiently
   const tables = result.content.tables || [];

   tables.forEach(table => {
     // Use structured data format
     const records = table.data || [];

     // Or process raw rows
     table.rows.forEach(row => {
       const obj = table.headers.reduce((acc, header, i) => {
         acc[header] = row[i];
         return acc;
       }, {} as Record<string, any>);
     });
   });
   ```

3. **Image Handling**:
   ```typescript
   // Extract and save images
   const images = result.content.images || [];

   for (const img of images) {
     const buffer = Buffer.from(img.data, 'base64');
     await fs.writeFile(
       `./images/page-${img.page}-img-${img.index}.${img.format}`,
       buffer
     );
   }
   ```

### OCR Best Practices

1. **Language Configuration**:
   ```typescript
   options: {
     pdf: {
       ocrEnabled: true,
       ocrLanguage: 'eng',     // English
       // or: 'chi_sim'        // Simplified Chinese
       // or: 'spa'            // Spanish
       // or: 'fra'            // French
     }
   }
   ```

2. **Confidence Threshold**:
   ```typescript
   // Check OCR confidence before using results
   if (result.ocr && result.ocr.confidence < 85) {
     console.warn('Low OCR confidence, results may be inaccurate');
     // Consider manual review or re-processing
   }

   // Per-page confidence check
   const lowConfPages = result.ocr?.pages?.filter(p => p.confidence < 80);
   if (lowConfPages && lowConfPages.length > 0) {
     console.warn(`Low confidence on pages: ${lowConfPages.map(p => p.pageNumber)}`);
   }
   ```

3. **Pre-processing for Better OCR**:
   ```typescript
   // For scanned documents, consider:
   // - Higher resolution scans (300+ DPI)
   // - Black and white conversion
   // - Noise reduction
   // - Deskewing

   // The processor handles basic pre-processing automatically
   options: {
     pdf: {
       ocrEnabled: true,
       // Automatic pre-processing includes:
       // - Noise removal
       // - Contrast enhancement
       // - Deskewing
     }
   }
   ```

### Format Conversion

1. **Markdown Conversion**:
   ```typescript
   // Generate clean Markdown output
   options: {
     outputFormat: {
       target: 'markdown',
       markdown: {
         includeToc: true,        // Add table of contents
         headingOffset: 0,        // Heading level adjustment
         codeFence: 'backticks'   // Code block style
       }
     }
   }
   ```

2. **JSON Export**:
   ```typescript
   // Structure data as JSON
   options: {
     xlsx: {
       headerRow: true,           // Use first row as headers
       analyzeDataTypes: true,    // Detect types
     },
     outputFormat: {
       target: 'json',
       json: {
         pretty: true,            // Format with indentation
         includeMetadata: true    // Include document info
       }
     }
   }
   ```

3. **Batch Conversion**:
   ```typescript
   // Convert multiple documents
   async function batchConvert(files: string[]) {
     const processor = new DocumentProcessor();
     const results = [];

     for (const file of files) {
       const result = await processor.process({
         source: { type: 'file', data: file },
         format: 'auto',
         options: {
           outputFormat: { target: 'markdown' }
         }
       });

       if (result.success) {
         results.push(result);
       }
     }

     return results;
   }
   ```

### Performance Optimization

1. **Caching Strategy**:
   ```typescript
   // Enable caching for repeated processing
   options: {
     processing: {
       enableCache: true,
       cacheTTL: 3600  // Cache for 1 hour
     }
   }

   // Cache key is based on:
   // - File content hash (for files)
   // - URL (for remote documents)
   // - Processing options
   ```

2. **Parallel Processing**:
   ```typescript
   // Process multiple documents in parallel
   const processor = new DocumentProcessor();

   const promises = files.map(file =>
     processor.process({
       source: { type: 'file', data: file },
       format: 'auto',
       options: {
         processing: { parallel: true }
       }
     })
   );

   const results = await Promise.all(promises);
   ```

3. **Stream Processing**:
   ```typescript
   // For very large files, use streaming
   import { createReadStream } from 'fs';

   const stream = createReadStream(largePdfPath);
   const result = await processor.processStream(stream, {
     format: 'pdf',
     options: { /* ... */ }
   });
   ```

### Error Handling

1. **Comprehensive Error Handling**:
   ```typescript
   try {
     const result = await processor.process(input);

     if (!result.success) {
       // Handle processing errors
       switch (result.error?.code) {
         case 'FILE_TOO_LARGE':
           console.error('File exceeds size limit');
           break;
         case 'UNSUPPORTED_FORMAT':
           console.error('Unsupported file format');
           break;
         case 'OCR_FAILED':
           console.error('OCR processing failed');
           break;
         case 'TIMEOUT':
           console.error('Processing timeout');
           break;
         default:
           console.error('Unknown error:', result.error?.message);
       }
       return;
     }

     // Check for warnings
     if (result.warnings && result.warnings.length > 0) {
       result.warnings.forEach(warning => {
         console.warn(`Warning: ${warning.message}`);
       });
     }

   } catch (error) {
     console.error('Unexpected error:', error);
   }
   ```

2. **Validation**:
   ```typescript
   // Validate input before processing
   function validateInput(input: DocumentProcessorInput): string[] {
     const errors: string[] = [];

     if (!input.source.data) {
       errors.push('Source data is required');
     }

     if (input.options?.processing?.maxSizeMB) {
       const maxBytes = input.options.processing.maxSizeMB * 1024 * 1024;
       // Validate file size
     }

     if (input.options?.processing?.timeout) {
       if (input.options.processing.timeout > 600000) {
         errors.push('Timeout cannot exceed 10 minutes');
       }
     }

     return errors;
   }
   ```

### Security Considerations

1. **File Upload Validation**:
   ```typescript
   // Validate uploaded files
   const ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.xlsx', '.csv', '.md', '.txt'];
   const MAX_SIZE_MB = 50;

   function validateUpload(file: Express.Multer.File): boolean {
     // Check file extension
     const ext = path.extname(file.originalname).toLowerCase();
     if (!ALLOWED_EXTENSIONS.includes(ext)) {
       throw new Error('Unsupported file type');
     }

     // Check file size
     if (file.size > MAX_SIZE_MB * 1024 * 1024) {
       throw new Error('File too large');
     }

     // Check MIME type
     const ALLOWED_MIMES = [
       'application/pdf',
       'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
       'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
       'text/csv',
       'text/markdown',
       'text/plain'
     ];

     if (!ALLOWED_MIMES.includes(file.mimetype)) {
       throw new Error('Invalid MIME type');
     }

     return true;
   }
   ```

2. **Content Sanitization**:
   ```typescript
   // Sanitize extracted content
   import DOMPurify from 'isomorphic-dompurify';

   function sanitizeContent(result: DocumentProcessorOutput): string {
     // Remove potentially malicious content
     const text = result.content.text || '';

     // Remove script tags and dangerous HTML
     const clean = DOMPurify.sanitize(text, {
       ALLOWED_TAGS: [],  // Strip all HTML
       ALLOWED_ATTR: []
     });

     return clean;
   }
   ```

3. **Path Traversal Prevention**:
   ```typescript
   // Prevent directory traversal attacks
   import path from 'path';

   function safeFilePath(userInput: string, baseDir: string): string {
     const normalized = path.normalize(userInput);
     const fullPath = path.join(baseDir, normalized);

     // Ensure the resolved path is within baseDir
     if (!fullPath.startsWith(path.resolve(baseDir))) {
       throw new Error('Invalid file path');
     }

     return fullPath;
   }
   ```

## Related Skills

- **15-web-search**: Search for document processing libraries and best practices
- **16-api-integrator**: Integrate with cloud document processing services (Google Document AI, AWS Textract)
- **18-youtube-analyzer**: Extract transcripts and metadata (similar content extraction pattern)
- **32-knowledge-manager**: Index and search processed documents
- **26-ai-code-optimizer**: Optimize document processing performance
- **29-project-planner**: Generate project documentation from templates

## Changelog

### v2.0.0 (2025-12-12)
- Initial release with comprehensive multi-format document processing
- Added OCR support for scanned documents (Tesseract integration)
- Implemented table extraction with data analysis
- Added format conversion (Markdown, JSON, HTML, plain text)
- Included statistical analysis for Excel/CSV data
- Implemented caching and parallel processing
- Added detailed metadata extraction
- Comprehensive error handling and validation
