---
name: 18-youtube-analyzer-G
description: YouTube video and channel analysis system. Supports video metadata extraction (title/description/tags/stats), comment analysis (top comments/sentiment), sentiment analysis (positive/negative/neutral), channel analysis (subscriber trends/video performance), engagement metrics (like rate/comment rate/share rate). Use for content marketing analysis, competitor analysis, public opinion monitoring.
---

# YouTube Analyzer

**Version**: 2.0.0
**Priority**: P1
**Category**: External Integration
**Status**: Production Ready

## Description

Comprehensive YouTube video and channel analysis system powered by YouTube Data API v3. Extract metadata, statistics, transcripts, comments, and perform sentiment analysis to gain insights from YouTube content.

**Core Capabilities**:
- **Video Analysis**: Extract metadata, statistics, transcripts, and chapter information
- **Comment Processing**: Fetch and analyze comments with sentiment analysis and topic extraction
- **Channel Analytics**: Analyze channel performance, video trends, and publishing patterns
- **Engagement Metrics**: Calculate engagement scores, like ratios, and audience interaction metrics
- **Content Intelligence**: Extract key points, detect chapters, and identify trending topics

## Instructions

### Trigger Conditions

Activate this skill when user requests involve:

1. **Video Analysis**:
   - "Analyze this YouTube video"
   - "Get statistics for this video"
   - "Extract transcript from this YouTube video"
   - "Summarize this YouTube tutorial"

2. **Comment Analysis**:
   - "Analyze comments on this video"
   - "What do people think about this video?"
   - "Find popular comments"
   - "Sentiment analysis for video comments"

3. **Channel Analysis**:
   - "Analyze this YouTube channel"
   - "Get channel statistics"
   - "Find top videos on this channel"
   - "Track channel growth"

4. **Comparative Analysis**:
   - "Compare these two YouTube videos"
   - "Which video performed better?"
   - "Analyze competitor videos"

5. **Content Research**:
   - "Find popular topics in tech tutorials"
   - "Analyze engagement on coding videos"
   - "Research best performing content"

### Execution Flow

```mermaid
graph TD
    A[YouTube URL/ID] --> B{Target Type}
    B -->|Video| C[Fetch Video Metadata]
    B -->|Channel| D[Fetch Channel Data]
    B -->|Playlist| E[Fetch Playlist Items]

    C --> F[Get Video Statistics]
    F --> G{Fetch Transcript?}
    G -->|Yes| H[Extract Captions]
    G -->|No| I[Skip Transcript]

    H --> J{Fetch Comments?}
    I --> J
    J -->|Yes| K[Fetch Comments]
    J -->|No| L[Skip Comments]

    K --> M{Sentiment Analysis?}
    M -->|Yes| N[Analyze Sentiment]
    M -->|No| O[Skip Sentiment]

    N --> P[Process Topics]
    O --> P
    L --> P

    D --> Q[Get Channel Videos]
    Q --> R[Calculate Statistics]

    E --> S[Process Each Video]
    S --> R

    P --> T[Generate Summary]
    R --> T
    T --> U[Return Results]
```

## Input/Output

### Input Interface

```typescript
/**
 * YouTube Analyzer input configuration
 */
interface YouTubeAnalyzerInput {
  /**
   * Target to analyze
   */
  target: {
    /**
     * Target type
     */
    type: 'video' | 'channel' | 'playlist';

    /**
     * YouTube URL or ID
     * @example "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
     * @example "dQw4w9WgXcQ"
     * @example "https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxx"
     */
    url?: string;

    /**
     * Direct video/channel/playlist ID
     */
    id?: string;
  };

  /**
   * Analysis configuration
   */
  analysis: {
    /**
     * Fetch video/channel metadata
     * @default true
     */
    fetchMetadata?: boolean;

    /**
     * Fetch statistics (views, likes, comments count)
     * @default true
     */
    fetchStatistics?: boolean;

    /**
     * Fetch video transcript/captions
     * @default false
     */
    fetchTranscript?: boolean;

    /**
     * Preferred transcript language
     * @default 'en'
     */
    transcriptLanguage?: string;

    /**
     * Fetch comments
     * @default false
     */
    fetchComments?: boolean;

    /**
     * Maximum number of comments to fetch
     * @default 100
     */
    maxComments?: number;

    /**
     * Comment sort order
     * @default 'relevance'
     */
    commentOrder?: 'relevance' | 'time';

    /**
     * Perform sentiment analysis on comments
     * @default false
     */
    sentimentAnalysis?: boolean;

    /**
     * Extract topics from comments
     * @default false
     */
    topicExtraction?: boolean;

    /**
     * Generate AI summary of content
     * @default false
     */
    generateSummary?: boolean;

    /**
     * Detect video chapters (from description or transcript)
     * @default false
     */
    detectChapters?: boolean;
  };

  /**
   * Filtering options
   */
  filters?: {
    /**
     * Date range for channel/playlist analysis
     */
    dateRange?: {
      from: string;
      to: string;
    };

    /**
     * Minimum view count filter
     */
    minViews?: number;

    /**
     * Minimum duration in seconds
     */
    minDuration?: number;

    /**
     * Maximum duration in seconds
     */
    maxDuration?: number;

    /**
     * Video category IDs
     */
    categories?: string[];

    /**
     * Search query for filtering videos
     */
    searchQuery?: string;
  };

  /**
   * Output configuration
   */
  output?: {
    /**
     * Output format
     * @default 'json'
     */
    format?: 'json' | 'markdown' | 'csv';

    /**
     * Include raw API responses
     * @default false
     */
    includeRawData?: boolean;

    /**
     * Save output to file
     */
    saveToFile?: string;
  };

  /**
   * API configuration
   */
  api?: {
    /**
     * YouTube Data API key
     * If not provided, uses environment variable YOUTUBE_API_KEY
     */
    apiKey?: string;

    /**
     * Request timeout in milliseconds
     * @default 30000
     */
    timeout?: number;

    /**
     * Retry failed requests
     * @default true
     */
    retry?: boolean;

    /**
     * Maximum retry attempts
     * @default 3
     */
    maxRetries?: number;
  };
}

/**
 * YouTube Analyzer output
 */
interface YouTubeAnalyzerOutput {
  /**
   * Analysis success status
   */
  success: boolean;

  /**
   * Target type analyzed
   */
  targetType: 'video' | 'channel' | 'playlist';

  /**
   * Video metadata (for video analysis)
   */
  metadata?: {
    /**
     * Video ID
     */
    videoId: string;

    /**
     * Video title
     */
    title: string;

    /**
     * Video description
     */
    description: string;

    /**
     * Channel name
     */
    channelName: string;

    /**
     * Channel ID
     */
    channelId: string;

    /**
     * Publish date (ISO 8601)
     */
    publishedAt: string;

    /**
     * Video duration (ISO 8601 duration)
     */
    duration?: string;

    /**
     * Video duration in seconds
     */
    durationSeconds?: number;

    /**
     * Thumbnail URLs
     */
    thumbnails: {
      default: string;
      medium: string;
      high: string;
      standard?: string;
      maxres?: string;
    };

    /**
     * Video tags
     */
    tags?: string[];

    /**
     * Video category
     */
    category?: string;

    /**
     * Default language
     */
    defaultLanguage?: string;

    /**
     * Live broadcast content type
     */
    liveBroadcastContent?: 'none' | 'upcoming' | 'live' | 'completed';
  };

  /**
   * Video statistics
   */
  statistics?: {
    /**
     * View count
     */
    viewCount: number;

    /**
     * Like count
     */
    likeCount: number;

    /**
     * Comment count
     */
    commentCount: number;

    /**
     * Engagement metrics
     */
    engagement?: {
      /**
       * Like ratio (likes / views)
       */
      likeRatio: number;

      /**
       * Comment ratio (comments / views)
       */
      commentRatio: number;

      /**
       * Engagement rate ((likes + comments) / views)
       */
      engagementRate: number;

      /**
       * Engagement score (0-10)
       */
      engagementScore: number;
    };
  };

  /**
   * Video transcript
   */
  transcript?: {
    /**
     * Language of transcript
     */
    language: string;

    /**
     * Transcript type
     */
    type: 'manual' | 'auto-generated';

    /**
     * Full transcript text
     */
    text: string;

    /**
     * Timestamped captions
     */
    captions: Array<{
      start: number;
      duration: number;
      text: string;
    }>;

    /**
     * Word count
     */
    wordCount: number;
  };

  /**
   * Detected chapters
   */
  chapters?: Array<{
    /**
     * Chapter title
     */
    title: string;

    /**
     * Start time in seconds
     */
    startTime: number;

    /**
     * End time in seconds (optional)
     */
    endTime?: number;

    /**
     * Chapter summary
     */
    summary?: string;
  }>;

  /**
   * Comments data
   */
  comments?: {
    /**
     * Total comment count
     */
    total: number;

    /**
     * Fetched comments
     */
    items: Array<{
      /**
       * Comment ID
       */
      id: string;

      /**
       * Author display name
       */
      author: string;

      /**
       * Author channel ID
       */
      authorChannelId: string;

      /**
       * Comment text
       */
      text: string;

      /**
       * Like count
       */
      likeCount: number;

      /**
       * Reply count
       */
      replyCount: number;

      /**
       * Published date (ISO 8601)
       */
      publishedAt: string;

      /**
       * Updated date (ISO 8601)
       */
      updatedAt: string;

      /**
       * Is top-level comment (not a reply)
       */
      isTopLevel: boolean;

      /**
       * Sentiment classification
       */
      sentiment?: 'positive' | 'negative' | 'neutral';

      /**
       * Sentiment score (-1 to 1)
       */
      sentimentScore?: number;
    }>;

    /**
     * Sentiment analysis
     */
    sentiment?: {
      /**
       * Positive comment ratio
       */
      positive: number;

      /**
       * Negative comment ratio
       */
      negative: number;

      /**
       * Neutral comment ratio
       */
      neutral: number;

      /**
       * Overall sentiment score (-1 to 1)
       */
      overallScore: number;
    };

    /**
     * Topic distribution
     */
    topicDistribution?: Record<string, number>;

    /**
     * Most mentioned keywords
     */
    keywords?: Array<{
      word: string;
      count: number;
      sentiment?: number;
    }>;
  };

  /**
   * AI-generated summary
   */
  summary?: {
    /**
     * Key points extracted
     */
    keyPoints: string[];

    /**
     * Overall summary
     */
    overview: string;

    /**
     * Target audience
     */
    targetAudience?: string;

    /**
     * Content type
     */
    contentType?: 'tutorial' | 'review' | 'entertainment' | 'educational' | 'vlog' | 'other';

    /**
     * Difficulty level
     */
    difficulty?: 'beginner' | 'intermediate' | 'advanced';
  };

  /**
   * Channel data (for channel analysis)
   */
  channel?: {
    /**
     * Channel ID
     */
    id: string;

    /**
     * Channel name
     */
    name: string;

    /**
     * Channel description
     */
    description: string;

    /**
     * Subscriber count
     */
    subscriberCount: number;

    /**
     * Total video count
     */
    videoCount: number;

    /**
     * Total view count
     */
    viewCount: number;

    /**
     * Channel created date
     */
    createdAt: string;

    /**
     * Custom URL
     */
    customUrl?: string;

    /**
     * Channel thumbnails
     */
    thumbnails: {
      default: string;
      medium: string;
      high: string;
    };
  };

  /**
   * Videos (for channel/playlist analysis)
   */
  videos?: Array<{
    videoId: string;
    title: string;
    publishedAt: string;
    statistics: {
      viewCount: number;
      likeCount: number;
      commentCount: number;
    };
    metadata: {
      duration: string;
      thumbnails: any;
    };
  }>;

  /**
   * Performance metrics
   */
  performance: {
    /**
     * Total processing time in milliseconds
     */
    processingTime: number;

    /**
     * API requests made
     */
    apiRequests: number;

    /**
     * API quota used
     */
    quotaUsed: number;

    /**
     * Cache hits
     */
    cacheHits?: number;
  };

  /**
   * Warnings (non-critical issues)
   */
  warnings?: Array<{
    code: string;
    message: string;
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
interface YouTubeAnalyzerInput {

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
interface YouTubeAnalyzerOutput extends BaseOutput {
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

### Example 1: Comprehensive Video Analysis with Comments

**Scenario**: Analyze a technical tutorial video including transcript, comments, and sentiment analysis to generate a comprehensive report.

**User Request**:
> "Analyze this YouTube coding tutorial. Get the transcript, analyze comments, and generate a summary of what people think about it."

**Implementation**:

```typescript
import { YouTubeAnalyzer } from '@/skills/18-youtube-analyzer';
import * as fs from 'fs/promises';

async function analyzeCodeTutorial() {
  const analyzer = new YouTubeAnalyzer();

  const input: YouTubeAnalyzerInput = {
    target: {
      type: 'video',
      url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    },
    analysis: {
      fetchMetadata: true,
      fetchStatistics: true,
      fetchTranscript: true,
      transcriptLanguage: 'en',
      fetchComments: true,
      maxComments: 200,
      commentOrder: 'relevance',
      sentimentAnalysis: true,
      topicExtraction: true,
      generateSummary: true,
      detectChapters: true
    },
    output: {
      format: 'markdown',
      saveToFile: './output/video-analysis.md'
    },
    api: {
      timeout: 60000,
      retry: true,
      maxRetries: 3
    }
  };

  console.log('🔍 Analyzing YouTube video...');
  const startTime = Date.now();

  const result = await analyzer.analyze(input);

  if (!result.success) {
    console.error('❌ Analysis failed:', result.error);
    return;
  }

  // Display metadata
  console.log('\n📹 Video Information:');
  console.log(`  Title: ${result.metadata?.title}`);
  console.log(`  Channel: ${result.metadata?.channelName}`);
  console.log(`  Published: ${new Date(result.metadata?.publishedAt!).toLocaleDateString()}`);
  console.log(`  Duration: ${formatDuration(result.metadata?.durationSeconds!)}`);

  // Display statistics
  console.log('\n📊 Statistics:');
  console.log(`  Views: ${result.statistics?.viewCount.toLocaleString()}`);
  console.log(`  Likes: ${result.statistics?.likeCount.toLocaleString()}`);
  console.log(`  Comments: ${result.statistics?.commentCount.toLocaleString()}`);

  // Display engagement metrics
  if (result.statistics?.engagement) {
    const eng = result.statistics.engagement;
    console.log('\n💡 Engagement Metrics:');
    console.log(`  Like Ratio: ${(eng.likeRatio * 100).toFixed(2)}%`);
    console.log(`  Comment Ratio: ${(eng.commentRatio * 100).toFixed(2)}%`);
    console.log(`  Engagement Rate: ${(eng.engagementRate * 100).toFixed(2)}%`);
    console.log(`  Engagement Score: ${eng.engagementScore}/10`);
  }

  // Display transcript info
  if (result.transcript) {
    console.log('\n📝 Transcript:');
    console.log(`  Language: ${result.transcript.language}`);
    console.log(`  Type: ${result.transcript.type}`);
    console.log(`  Word Count: ${result.transcript.wordCount.toLocaleString()}`);
    console.log(`  Captions: ${result.transcript.captions.length}`);

    // Display first few lines
    console.log('\n  First 3 captions:');
    result.transcript.captions.slice(0, 3).forEach(cap => {
      const time = formatTime(cap.start);
      console.log(`    [${time}] ${cap.text}`);
    });
  }

  // Display chapters
  if (result.chapters && result.chapters.length > 0) {
    console.log(`\n📑 Detected Chapters (${result.chapters.length}):`);
    result.chapters.forEach((chapter, i) => {
      const time = formatTime(chapter.startTime);
      console.log(`  ${i + 1}. ${chapter.title} (${time})`);
      if (chapter.summary) {
        console.log(`     ${chapter.summary.substring(0, 100)}...`);
      }
    });
  }

  // Display comment sentiment
  if (result.comments?.sentiment) {
    const sent = result.comments.sentiment;
    console.log('\n😊 Comment Sentiment Analysis:');
    console.log(`  Positive: ${(sent.positive * 100).toFixed(1)}% ${'█'.repeat(Math.floor(sent.positive * 20))}`);
    console.log(`  Neutral:  ${(sent.neutral * 100).toFixed(1)}% ${'█'.repeat(Math.floor(sent.neutral * 20))}`);
    console.log(`  Negative: ${(sent.negative * 100).toFixed(1)}% ${'█'.repeat(Math.floor(sent.negative * 20))}`);
    console.log(`  Overall Score: ${sent.overallScore.toFixed(2)}`);
  }

  // Display top topics
  if (result.comments?.topicDistribution) {
    console.log('\n🏷️  Top Discussion Topics:');
    const topics = Object.entries(result.comments.topicDistribution)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);

    topics.forEach(([topic, count], i) => {
      console.log(`  ${i + 1}. ${topic}: ${count} mentions`);
    });
  }

  // Display top keywords
  if (result.comments?.keywords) {
    console.log('\n🔑 Most Mentioned Keywords:');
    result.comments.keywords.slice(0, 10).forEach((kw, i) => {
      const sentimentEmoji = kw.sentiment
        ? kw.sentiment > 0.2 ? '😊' : kw.sentiment < -0.2 ? '😞' : '😐'
        : '';
      console.log(`  ${i + 1}. "${kw.word}" - ${kw.count} times ${sentimentEmoji}`);
    });
  }

  // Display popular comments
  if (result.comments?.items) {
    console.log('\n💬 Top 5 Most Liked Comments:');
    const topComments = result.comments.items
      .sort((a, b) => b.likeCount - a.likeCount)
      .slice(0, 5);

    topComments.forEach((comment, i) => {
      const sentimentIcon = comment.sentiment === 'positive' ? '😊'
        : comment.sentiment === 'negative' ? '😞' : '😐';
      console.log(`\n  ${i + 1}. ${comment.author} ${sentimentIcon} (👍 ${comment.likeCount})`);
      console.log(`     "${comment.text.substring(0, 150)}${comment.text.length > 150 ? '...' : ''}"`);
    });
  }

  // Display AI summary
  if (result.summary) {
    console.log('\n🤖 AI-Generated Summary:');
    console.log(`  Content Type: ${result.summary.contentType}`);
    console.log(`  Difficulty: ${result.summary.difficulty}`);
    console.log(`  Target Audience: ${result.summary.targetAudience}`);

    console.log('\n  Key Points:');
    result.summary.keyPoints.forEach((point, i) => {
      console.log(`    ${i + 1}. ${point}`);
    });

    console.log(`\n  Overview:`);
    console.log(`    ${result.summary.overview}`);
  }

  // Performance metrics
  console.log('\n⚡ Performance:');
  console.log(`  Processing Time: ${result.performance.processingTime}ms`);
  console.log(`  API Requests: ${result.performance.apiRequests}`);
  console.log(`  Quota Used: ${result.performance.quotaUsed} units`);
  if (result.performance.cacheHits) {
    console.log(`  Cache Hits: ${result.performance.cacheHits}`);
  }

  // Warnings
  if (result.warnings && result.warnings.length > 0) {
    console.log(`\n⚠️  Warnings (${result.warnings.length}):`);
    result.warnings.forEach(warning => {
      console.log(`  - ${warning.message}`);
    });
  }

  const totalTime = Date.now() - startTime;
  console.log(`\n✨ Analysis complete in ${totalTime}ms`);

  return result;
}

// Helper function to format duration
function formatDuration(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;

  if (h > 0) return `${h}h ${m}m ${s}s`;
  if (m > 0) return `${m}m ${s}s`;
  return `${s}s`;
}

// Helper function to format timestamp
function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

// Run the analysis
analyzeCodeTutorial()
  .then(() => console.log('\n✅ Done'))
  .catch(err => console.error('💥 Error:', err));
```

**Expected Output**:
```
🔍 Analyzing YouTube video...

📹 Video Information:
  Title: Full Stack TypeScript Tutorial - Build a SaaS Platform
  Channel: Tech With Tim
  Published: 1/15/2024
  Duration: 3h 45m 30s

📊 Statistics:
  Views: 1,234,567
  Likes: 98,765
  Comments: 4,321

💡 Engagement Metrics:
  Like Ratio: 8.00%
  Comment Ratio: 0.35%
  Engagement Rate: 8.35%
  Engagement Score: 9.2/10

📝 Transcript:
  Language: en
  Type: manual
  Word Count: 45,678
  Captions: 1,234

  First 3 captions:
    [0:00] Hey everyone, welcome back to the channel. Today we're building a complete SaaS platform using TypeScript
    [0:15] We'll be using React for the frontend, Node.js for the backend, and PostgreSQL for the database
    [0:30] This is going to be a comprehensive tutorial covering authentication, payments, and deployment

📑 Detected Chapters (6):
  1. Introduction & Project Setup (0:00)
     Covers the project overview, technology stack selection, and initial setup of the development environmen...
  2. Database Design with PostgreSQL (15:30)
     Designing the database schema, setting up migrations, and implementing TypeORM for type-safe database qu...
  3. Authentication System (45:20)
     Building JWT-based authentication with refresh tokens, password hashing, and session management...
  4. Stripe Payment Integration (1:30:15)
     Integrating Stripe for subscription payments, webhooks, and billing portal...
  5. Real-time Features with WebSockets (2:15:45)
     Implementing Socket.io for real-time notifications and collaborative features...
  6. Deployment & Scaling (3:10:00)
     Docker containerization, AWS deployment, and performance optimization techniques...

😊 Comment Sentiment Analysis:
  Positive: 87.3% ████████████████
  Neutral:  9.5% █
  Negative: 3.2%
  Overall Score: 0.84

🏷️  Top Discussion Topics:
  1. excellent tutorial: 342 mentions
  2. authentication issue: 156 mentions
  3. stripe integration: 134 mentions
  4. deployment help: 123 mentions
  5. typescript benefits: 98 mentions

🔑 Most Mentioned Keywords:
  1. "tutorial" - 567 times 😊
  2. "works" - 342 times 😊
  3. "great" - 298 times 😊
  4. "authentication" - 245 times 😐
  5. "issue" - 178 times 😞
  6. "error" - 156 times 😞
  7. "deployment" - 145 times 😐
  8. "typescript" - 134 times 😊
  9. "helpful" - 123 times 😊
  10. "thank" - 456 times 😊

💬 Top 5 Most Liked Comments:

  1. JohnDev123 😊 (👍 1,234)
     "This is hands down the best full-stack TypeScript tutorial I've ever watched. The authentication implementation is production-ready and the Stripe integration..."

  2. ReactQueen 😊 (👍 987)
     "At 1:32:15, the Stripe webhook implementation saved my project. Was struggling for weeks. Clear explanation, working code. You're a lifesaver! Already deployed..."

  3. BackendBob 😊 (👍 876)
     "Love the TypeScript patterns throughout. The type safety for the database models is brilliant. One question: how would you handle background jobs for email no..."

  4. NewbieCoder 😊 (👍 743)
     "I'm a complete beginner and managed to follow along. Took me 5 days but I finished! Now I have a working SaaS app for my portfolio. Thank you so much!"

  5. DevOpsGuru 😊 (👍 621)
     "The deployment section is gold. Docker multi-stage builds + AWS ECS is exactly what production looks like. Most tutorials skip this. Highly appreciated!"

🤖 AI-Generated Summary:
  Content Type: tutorial
  Difficulty: intermediate
  Target Audience: Full-stack developers with TypeScript experience

  Key Points:
    1. Build a complete SaaS platform using TypeScript, React, Node.js, and PostgreSQL
    2. Implement production-ready JWT authentication with refresh tokens
    3. Integrate Stripe for subscription payments and billing
    4. Add real-time features using Socket.io for notifications
    5. Deploy using Docker and AWS with performance optimization

  Overview:
    A comprehensive 3.5-hour tutorial demonstrating how to build a production-ready SaaS platform using modern TypeScript stack. Covers everything from database design to deployment, with emphasis on best practices, type safety, and scalability. Highly rated for clarity and real-world applicability.

⚡ Performance:
  Processing Time: 15,678ms
  API Requests: 8
  Quota Used: 47 units
  Cache Hits: 2

⚠️  Warnings (1):
  - Some comments may be hidden due to content filters

✨ Analysis complete in 16,234ms

✅ Done
```

### Example 2: Channel Performance Analysis

**Scenario**: Analyze a YouTube channel's performance over the past year, identifying top-performing videos and publishing patterns.

**User Request**:
> "Analyze the Tech With Tim channel for 2024. Show me the top videos, publishing frequency, and overall stats."

**Implementation**:

```typescript
import { YouTubeAnalyzer } from '@/skills/18-youtube-analyzer';

async function analyzeChannelPerformance() {
  const analyzer = new YouTubeAnalyzer();

  const input: YouTubeAnalyzerInput = {
    target: {
      type: 'channel',
      id: 'UCxxxxxxxxxxxxxxxx'  // Channel ID
    },
    analysis: {
      fetchMetadata: true,
      fetchStatistics: true,
      fetchComments: false,
      sentimentAnalysis: false
    },
    filters: {
      dateRange: {
        from: '2024-01-01',
        to: '2024-12-31'
      },
      minViews: 1000  // Only videos with 1000+ views
    },
    output: {
      format: 'markdown',
      saveToFile: './output/channel-analysis-2024.md'
    }
  };

  console.log('📺 Analyzing YouTube channel...');

  const result = await analyzer.analyze(input);

  if (!result.success) {
    console.error('❌ Analysis failed:', result.error);
    return;
  }

  // Display channel info
  console.log('\n🎬 Channel Information:');
  console.log(`  Name: ${result.channel?.name}`);
  console.log(`  Subscribers: ${result.channel?.subscriberCount.toLocaleString()}`);
  console.log(`  Total Videos: ${result.channel?.videoCount}`);
  console.log(`  Total Views: ${result.channel?.viewCount.toLocaleString()}`);
  console.log(`  Created: ${new Date(result.channel?.createdAt!).toLocaleDateString()}`);

  const videos = result.videos || [];
  console.log(`\n📊 Analysis Period: 2024 (${videos.length} videos)`);

  // Calculate overall statistics
  const totalViews = videos.reduce((sum, v) => sum + v.statistics.viewCount, 0);
  const totalLikes = videos.reduce((sum, v) => sum + v.statistics.likeCount, 0);
  const totalComments = videos.reduce((sum, v) => sum + v.statistics.commentCount, 0);
  const avgViews = totalViews / videos.length;
  const avgLikes = totalLikes / videos.length;

  console.log('\n📈 Overall Statistics:');
  console.log(`  Total Views: ${totalViews.toLocaleString()}`);
  console.log(`  Total Likes: ${totalLikes.toLocaleString()}`);
  console.log(`  Total Comments: ${totalComments.toLocaleString()}`);
  console.log(`  Average Views per Video: ${Math.round(avgViews).toLocaleString()}`);
  console.log(`  Average Likes per Video: ${Math.round(avgLikes).toLocaleString()}`);
  console.log(`  Average Like Rate: ${((totalLikes / totalViews) * 100).toFixed(2)}%`);

  // Top 10 videos by views
  console.log('\n🏆 Top 10 Videos (by views):');
  const top10 = videos
    .sort((a, b) => b.statistics.viewCount - a.statistics.viewCount)
    .slice(0, 10);

  top10.forEach((video, i) => {
    const likeRate = (video.statistics.likeCount / video.statistics.viewCount) * 100;
    console.log(`\n  ${i + 1}. ${video.title}`);
    console.log(`     Views: ${video.statistics.viewCount.toLocaleString()}`);
    console.log(`     Likes: ${video.statistics.likeCount.toLocaleString()} (${likeRate.toFixed(2)}%)`);
    console.log(`     Comments: ${video.statistics.commentCount.toLocaleString()}`);
    console.log(`     Published: ${new Date(video.publishedAt).toLocaleDateString()}`);
  });

  // Publishing frequency analysis
  const monthlyVideos = videos.reduce((acc, video) => {
    const month = video.publishedAt.substring(0, 7);  // YYYY-MM
    acc[month] = (acc[month] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  console.log('\n📅 Publishing Frequency:');
  Object.entries(monthlyVideos)
    .sort((a, b) => a[0].localeCompare(b[0]))
    .forEach(([month, count]) => {
      const bar = '█'.repeat(count);
      console.log(`  ${month}: ${count.toString().padStart(2)} videos ${bar}`);
    });

  // Monthly views trend
  const monthlyViews = videos.reduce((acc, video) => {
    const month = video.publishedAt.substring(0, 7);
    acc[month] = (acc[month] || 0) + video.statistics.viewCount;
    return acc;
  }, {} as Record<string, number>);

  console.log('\n👁️  Views by Month:');
  Object.entries(monthlyViews)
    .sort((a, b) => a[0].localeCompare(b[0]))
    .forEach(([month, views]) => {
      console.log(`  ${month}: ${views.toLocaleString()} views`);
    });

  // Performance insights
  console.log('\n💡 Performance Insights:');

  const bestMonth = Object.entries(monthlyViews)
    .sort((a, b) => b[1] - a[1])[0];
  console.log(`  📌 Best performing month: ${bestMonth[0]} (${bestMonth[1].toLocaleString()} views)`);

  const mostActiveMonth = Object.entries(monthlyVideos)
    .sort((a, b) => b[1] - a[1])[0];
  console.log(`  📌 Most active month: ${mostActiveMonth[0]} (${mostActiveMonth[1]} videos)`);

  const avgVideoPerMonth = videos.length / 12;
  console.log(`  📌 Average videos per month: ${avgVideoPerMonth.toFixed(1)}`);

  const viewsPerSub = totalViews / (result.channel?.subscriberCount || 1);
  console.log(`  📌 Views per subscriber ratio: ${viewsPerSub.toFixed(2)}`);

  // Growth recommendations
  console.log('\n🚀 Recommendations:');

  if (avgVideoPerMonth < 4) {
    console.log('  ⚠️  Publishing frequency is low. Consider increasing to 4-5 videos per month for better growth.');
  } else {
    console.log('  ✅ Publishing frequency is healthy.');
  }

  const likeRate = (totalLikes / totalViews) * 100;
  if (likeRate < 5) {
    console.log('  ⚠️  Like rate is below 5%. Consider adding stronger CTAs for engagement.');
  } else {
    console.log('  ✅ Like rate is good, audience is engaged.');
  }

  console.log('\n⚡ Performance:');
  console.log(`  Processing Time: ${result.performance.processingTime}ms`);
  console.log(`  API Requests: ${result.performance.apiRequests}`);
  console.log(`  Quota Used: ${result.performance.quotaUsed} units`);

  return result;
}

// Run the analysis
analyzeChannelPerformance()
  .then(() => console.log('\n✨ Channel analysis complete'))
  .catch(err => console.error('💥 Error:', err));
```

**Expected Output**:
```
📺 Analyzing YouTube channel...

🎬 Channel Information:
  Name: Tech With Tim
  Subscribers: 1,250,000
  Total Videos: 487
  Total Views: 95,432,890
  Created: 3/15/2016

📊 Analysis Period: 2024 (48 videos)

📈 Overall Statistics:
  Total Views: 15,432,890
  Total Likes: 1,234,567
  Total Comments: 98,765
  Average Views per Video: 321,518
  Average Likes per Video: 25,720
  Average Like Rate: 8.00%

🏆 Top 10 Videos (by views):

  1. Full Stack TypeScript Tutorial - Build a SaaS Platform
     Views: 1,234,567
     Likes: 98,765 (8.00%)
     Comments: 4,321
     Published: 1/15/2024

  2. Master React Hooks in 2024 - Complete Guide
     Views: 987,654
     Likes: 87,432 (8.85%)
     Comments: 3,456
     Published: 3/22/2024

  3. Next.js 14 Tutorial - Build a Modern Web App
     Views: 876,543
     Likes: 76,543 (8.73%)
     Comments: 2,987
     Published: 5/10/2024

  4. Docker for Beginners - Full Course 2024
     Views: 765,432
     Likes: 65,234 (8.52%)
     Comments: 2,543
     Published: 2/18/2024

  5. GraphQL vs REST API - Which Should You Use?
     Views: 654,321
     Likes: 54,321 (8.30%)
     Comments: 2,123
     Published: 4/5/2024

  6. TypeScript Advanced Patterns - Pro Tips
     Views: 543,210
     Likes: 45,678 (8.41%)
     Comments: 1,876
     Published: 6/12/2024

  7. AWS Lambda Tutorial - Serverless Architecture
     Views: 432,109
     Likes: 38,901 (9.00%)
     Comments: 1,654
     Published: 7/20/2024

  8. MongoDB Performance Optimization Guide
     Views: 345,678
     Likes: 31,234 (9.04%)
     Comments: 1,432
     Published: 8/15/2024

  9. CI/CD Pipeline with GitHub Actions
     Views: 298,765
     Likes: 28,765 (9.63%)
     Comments: 1,234
     Published: 9/10/2024

  10. Microservices Design Patterns Explained
      Views: 267,543
      Likes: 25,432 (9.51%)
      Comments: 1,098
      Published: 10/5/2024

📅 Publishing Frequency:
  2024-01:  4 videos ████
  2024-02:  5 videos █████
  2024-03:  6 videos ██████
  2024-04:  4 videos ████
  2024-05:  3 videos ███
  2024-06:  4 videos ████
  2024-07:  5 videos █████
  2024-08:  4 videos ████
  2024-09:  5 videos █████
  2024-10:  4 videos ████
  2024-11:  3 videos ███
  2024-12:  1 videos █

👁️  Views by Month:
  2024-01: 2,345,678 views
  2024-02: 1,876,543 views
  2024-03: 1,654,321 views
  2024-04: 1,432,109 views
  2024-05: 1,234,567 views
  2024-06: 1,098,765 views
  2024-07: 987,654 views
  2024-08: 876,543 views
  2024-09: 765,432 views
  2024-10: 654,321 views
  2024-11: 543,210 views
  2024-12: 432,109 views

💡 Performance Insights:
  📌 Best performing month: 2024-01 (2,345,678 views)
  📌 Most active month: 2024-03 (6 videos)
  📌 Average videos per month: 4.0
  📌 Views per subscriber ratio: 12.35

🚀 Recommendations:
  ✅ Publishing frequency is healthy.
  ✅ Like rate is good, audience is engaged.

⚡ Performance:
  Processing Time: 8,765ms
  API Requests: 12
  Quota Used: 125 units

✨ Channel analysis complete
```

### Example 3: Video Comparison Analysis

**Scenario**: Compare two competing tutorial videos to understand which performed better and why.

**User Request**:
> "Compare these two React tutorial videos. Which one is more popular and why?"

**Implementation**:

```typescript
import { YouTubeAnalyzer } from '@/skills/18-youtube-analyzer';

async function compareVideos() {
  const analyzer = new YouTubeAnalyzer();

  console.log('🔄 Comparing two YouTube videos...');

  // Analyze first video
  const video1Result = await analyzer.analyze({
    target: {
      url: 'https://www.youtube.com/watch?v=video1'
    },
    analysis: {
      fetchMetadata: true,
      fetchStatistics: true,
      fetchComments: true,
      maxComments: 100,
      sentimentAnalysis: true
    }
  });

  // Analyze second video
  const video2Result = await analyzer.analyze({
    target: {
      url: 'https://www.youtube.com/watch?v=video2'
    },
    analysis: {
      fetchMetadata: true,
      fetchStatistics: true,
      fetchComments: true,
      maxComments: 100,
      sentimentAnalysis: true
    }
  });

  if (!video1Result.success || !video2Result.success) {
    console.error('❌ Failed to analyze one or both videos');
    return;
  }

  const v1 = video1Result;
  const v2 = video2Result;

  // Comparison report
  console.log('\n📊 Video Comparison Report\n');

  // Basic info table
  console.log('## Basic Information\n');
  console.log('| Metric | Video A | Video B |');
  console.log('|--------|---------|---------|');
  console.log(`| Title | ${v1.metadata?.title.substring(0, 40)}... | ${v2.metadata?.title.substring(0, 40)}... |`);
  console.log(`| Channel | ${v1.metadata?.channelName} | ${v2.metadata?.channelName} |`);
  console.log(`| Duration | ${formatDuration(v1.metadata?.durationSeconds!)} | ${formatDuration(v2.metadata?.durationSeconds!)} |`);
  console.log(`| Published | ${new Date(v1.metadata?.publishedAt!).toLocaleDateString()} | ${new Date(v2.metadata?.publishedAt!).toLocaleDateString()} |\n`);

  // Performance comparison
  console.log('## Performance Metrics\n');
  console.log('| Metric | Video A | Video B | Winner |');
  console.log('|--------|---------|---------|--------|');

  const viewWinner = v1.statistics!.viewCount > v2.statistics!.viewCount ? 'A 🏆' : 'B 🏆';
  console.log(`| Views | ${v1.statistics?.viewCount.toLocaleString()} | ${v2.statistics?.viewCount.toLocaleString()} | ${viewWinner} |`);

  const likeWinner = v1.statistics!.likeCount > v2.statistics!.likeCount ? 'A 🏆' : 'B 🏆';
  console.log(`| Likes | ${v1.statistics?.likeCount.toLocaleString()} | ${v2.statistics?.likeCount.toLocaleString()} | ${likeWinner} |`);

  const commentWinner = v1.statistics!.commentCount > v2.statistics!.commentCount ? 'A 🏆' : 'B 🏆';
  console.log(`| Comments | ${v1.statistics?.commentCount.toLocaleString()} | ${v2.statistics?.commentCount.toLocaleString()} | ${commentWinner} |`);

  const likeRate1 = (v1.statistics!.engagement!.likeRatio * 100).toFixed(2);
  const likeRate2 = (v2.statistics!.engagement!.likeRatio * 100).toFixed(2);
  const likeRateWinner = v1.statistics!.engagement!.likeRatio > v2.statistics!.engagement!.likeRatio ? 'A 🏆' : 'B 🏆';
  console.log(`| Like Rate | ${likeRate1}% | ${likeRate2}% | ${likeRateWinner} |`);

  const engScore1 = v1.statistics!.engagement!.engagementScore;
  const engScore2 = v2.statistics!.engagement!.engagementScore;
  const engWinner = engScore1 > engScore2 ? 'A 🏆' : 'B 🏆';
  console.log(`| Engagement Score | ${engScore1}/10 | ${engScore2}/10 | ${engWinner} |\n`);

  // Sentiment comparison
  if (v1.comments?.sentiment && v2.comments?.sentiment) {
    console.log('## Sentiment Analysis\n');
    console.log('| Sentiment | Video A | Video B |');
    console.log('|-----------|---------|---------|');
    console.log(`| Positive | ${(v1.comments.sentiment.positive * 100).toFixed(1)}% | ${(v2.comments.sentiment.positive * 100).toFixed(1)}% |`);
    console.log(`| Neutral | ${(v1.comments.sentiment.neutral * 100).toFixed(1)}% | ${(v2.comments.sentiment.neutral * 100).toFixed(1)}% |`);
    console.log(`| Negative | ${(v1.comments.sentiment.negative * 100).toFixed(1)}% | ${(v2.comments.sentiment.negative * 100).toFixed(1)}% |`);
    console.log(`| Overall Score | ${v1.comments.sentiment.overallScore.toFixed(2)} | ${v2.comments.sentiment.overallScore.toFixed(2)} |\n`);
  }

  // Conclusion
  console.log('## Conclusion\n');

  const overallWinner = engScore1 > engScore2 ? 'Video A' : 'Video B';
  const winnerResult = engScore1 > engScore2 ? v1 : v2;
  const loserResult = engScore1 > engScore2 ? v2 : v1;

  console.log(`### Overall Winner: ${overallWinner} 🎉\n`);

  console.log('**Reasons:**');

  if (winnerResult.statistics!.viewCount > loserResult.statistics!.viewCount) {
    const viewDiff = ((winnerResult.statistics!.viewCount / loserResult.statistics!.viewCount - 1) * 100).toFixed(1);
    console.log(`- ${viewDiff}% more views`);
  }

  if (winnerResult.statistics!.engagement!.likeRatio > loserResult.statistics!.engagement!.likeRatio) {
    console.log(`- Higher like rate (${(winnerResult.statistics!.engagement!.likeRatio * 100).toFixed(2)}% vs ${(loserResult.statistics!.engagement!.likeRatio * 100).toFixed(2)}%)`);
  }

  if (winnerResult.comments?.sentiment && loserResult.comments?.sentiment) {
    if (winnerResult.comments.sentiment.positive > loserResult.comments.sentiment.positive) {
      console.log(`- More positive sentiment (${(winnerResult.comments.sentiment.positive * 100).toFixed(1)}% vs ${(loserResult.comments.sentiment.positive * 100).toFixed(1)}%)`);
    }
  }

  console.log(`- Superior engagement score (${winnerResult.statistics!.engagement!.engagementScore}/10 vs ${loserResult.statistics!.engagement!.engagementScore}/10)`);

  console.log('\n✨ Comparison complete');

  return { video1: v1, video2: v2 };
}

function formatDuration(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;

  if (h > 0) return `${h}h ${m}m`;
  return `${m}m ${s}s`;
}

// Run comparison
compareVideos()
  .then(() => console.log('\n✅ Done'))
  .catch(err => console.error('💥 Error:', err));
```

**Expected Output**:
```
🔄 Comparing two YouTube videos...

📊 Video Comparison Report

## Basic Information

| Metric | Video A | Video B |
|--------|---------|---------|
| Title | React Hooks Complete Guide - 2024 Edition... | Learn React Hooks in 30 Minutes - Quick... |
| Channel | Web Dev Simplified | Traversy Media |
| Duration | 1h 45m | 32m 15s |
| Published | 2/15/2024 | 3/10/2024 |

## Performance Metrics

| Metric | Video A | Video B | Winner |
|--------|---------|---------|--------|
| Views | 1,234,567 | 876,543 | A 🏆 |
| Likes | 98,765 | 65,432 | A 🏆 |
| Comments | 4,321 | 2,876 | A 🏆 |
| Like Rate | 8.00% | 7.46% | A 🏆 |
| Engagement Score | 9.2/10 | 8.5/10 | A 🏆 |

## Sentiment Analysis

| Sentiment | Video A | Video B |
|-----------|---------|---------|
| Positive | 87.3% | 82.1% |
| Neutral | 9.5% | 13.2% |
| Negative | 3.2% | 4.7% |
| Overall Score | 0.84 | 0.77 |

## Conclusion

### Overall Winner: Video A 🎉

**Reasons:**
- 40.9% more views
- Higher like rate (8.00% vs 7.46%)
- More positive sentiment (87.3% vs 82.1%)
- Superior engagement score (9.2/10 vs 8.5/10)

✨ Comparison complete

✅ Done
```

## Best Practices

### API Quota Management

1. **Monitor Quota Usage**:
   ```typescript
   // YouTube Data API has daily quota limit (10,000 units by default)
   const quotaUsage = {
     video_list: 1,        // Cost: 1 unit
     commentThreads: 1,    // Cost: 1 unit per request
     captions: 50,         // Cost: 50 units
     search: 100           // Cost: 100 units
   };

   // Track quota in your application
   class QuotaTracker {
     private dailyUsed = 0;
     private readonly dailyLimit = 10000;

     canMakeRequest(cost: number): boolean {
       return (this.dailyUsed + cost) <= this.dailyLimit;
     }

     recordUsage(cost: number) {
       this.dailyUsed += cost;
       if (this.dailyUsed > this.dailyLimit * 0.8) {
         console.warn('⚠️  YouTube API quota at 80%');
       }
     }
   }
   ```

2. **Implement Caching**:
   ```typescript
   // Cache frequently accessed data
   const cache = new Map<string, { data: any; expiresAt: number }>();

   function getCachedOrFetch(videoId: string, ttl = 3600000): Promise<any> {
     const cached = cache.get(videoId);
     if (cached && Date.now() < cached.expiresAt) {
       return Promise.resolve(cached.data);
     }

     return fetchVideoData(videoId).then(data => {
       cache.set(videoId, {
         data,
         expiresAt: Date.now() + ttl
       });
       return data;
     });
   }
   ```

3. **Batch Requests**:
   ```typescript
   // Fetch multiple videos in one API call
   const videoIds = ['id1', 'id2', 'id3', 'id4', 'id5'];
   const batchedIds = videoIds.join(',');  // Max 50 IDs

   const response = await youtube.videos.list({
     part: ['snippet', 'statistics'],
     id: batchedIds
   });
   // This uses only 1 quota unit instead of 5
   ```

### Data Accuracy and Validation

1. **Handle Data Delays**:
   ```typescript
   // YouTube statistics have delays (usually a few hours)
   function addFreshnessIndicator(publishedAt: string): string {
     const age = Date.now() - new Date(publishedAt).getTime();
     const hours = age / (1000 * 60 * 60);

     if (hours < 24) {
       return '⚠️  Stats may not be final (video < 24h old)';
     }
     return '';
   }
   ```

2. **Validate Data Completeness**:
   ```typescript
   // Some fields may be missing or disabled
   function validateVideoData(video: any): string[] {
     const issues: string[] = [];

     if (!video.statistics) {
       issues.push('Statistics unavailable');
     }

     if (video.statistics?.likeCount === undefined) {
       issues.push('Likes hidden by creator');
     }

     if (!video.snippet?.tags || video.snippet.tags.length === 0) {
       issues.push('No tags available');
     }

     return issues;
   }
   ```

3. **Handle Missing Transcripts**:
   ```typescript
   async function fetchTranscriptSafely(videoId: string): Promise<Transcript | null> {
     try {
       const transcript = await getTranscript(videoId);
       return transcript;
     } catch (error) {
       if (error.code === 'CAPTIONS_NOT_AVAILABLE') {
         console.warn(`⚠️  No transcript available for ${videoId}`);
         return null;
       }
       throw error;
     }
   }
   ```

### Performance Optimization

1. **Parallel Processing**:
   ```typescript
   // Process multiple videos in parallel
   async function analyzeMultipleVideos(videoIds: string[]): Promise<any[]> {
     const CONCURRENCY_LIMIT = 5;  // Don't overwhelm the API

     const results = [];
     for (let i = 0; i < videoIds.length; i += CONCURRENCY_LIMIT) {
       const batch = videoIds.slice(i, i + CONCURRENCY_LIMIT);
       const batchResults = await Promise.all(
         batch.map(id => analyzeVideo(id))
       );
       results.push(...batchResults);
     }

     return results;
   }
   ```

2. **Incremental Updates**:
   ```typescript
   // Only fetch new videos since last check
   interface ChannelState {
     lastCheckedAt: string;
     lastVideoId: string;
   }

   async function getNewVideos(channelId: string, state: ChannelState): Promise<any[]> {
     const response = await youtube.search.list({
       channelId,
       part: ['id'],
       order: 'date',
       publishedAfter: state.lastCheckedAt,
       type: ['video']
     });

     return response.data.items || [];
   }
   ```

3. **Lazy Loading**:
   ```typescript
   // Only fetch details when needed
   class LazyVideo {
     constructor(private videoId: string) {}

     private _statistics?: any;
     async getStatistics() {
       if (!this._statistics) {
         this._statistics = await fetchStatistics(this.videoId);
       }
       return this._statistics;
     }

     private _comments?: any;
     async getComments() {
       if (!this._comments) {
         this._comments = await fetchComments(this.videoId);
       }
       return this._comments;
     }
   }
   ```

### Error Handling

1. **API Error Handling**:
   ```typescript
   async function handleYouTubeAPICall<T>(
     apiCall: () => Promise<T>
   ): Promise<T> {
     try {
       return await apiCall();
     } catch (error: any) {
       switch (error.code) {
         case 403:
           if (error.message.includes('quotaExceeded')) {
             throw new Error('YouTube API quota exceeded for today');
           }
           throw new Error('YouTube API access forbidden');

         case 404:
           throw new Error('Video or channel not found');

         case 400:
           throw new Error('Invalid request parameters');

         default:
           throw error;
       }
     }
   }
   ```

2. **Retry Logic**:
   ```typescript
   async function fetchWithRetry<T>(
     fn: () => Promise<T>,
     maxRetries = 3,
     delay = 1000
   ): Promise<T> {
     for (let attempt = 1; attempt <= maxRetries; attempt++) {
       try {
         return await fn();
       } catch (error: any) {
         // Don't retry on client errors (4xx)
         if (error.code >= 400 && error.code < 500) {
           throw error;
         }

         if (attempt === maxRetries) {
           throw error;
         }

         // Exponential backoff
         await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, attempt - 1)));
       }
     }

     throw new Error('Max retries exceeded');
   }
   ```

### Privacy and Compliance

1. **Respect Privacy Settings**:
   ```typescript
   // Check video privacy status
   function canAnalyzeVideo(video: any): boolean {
     if (video.status.privacyStatus !== 'public') {
       console.warn(`Video is ${video.status.privacyStatus}, skipping analysis`);
       return false;
     }
     return true;
   }
   ```

2. **Data Retention Policy**:
   ```typescript
   // Don't store personal information
   function sanitizeComment(comment: any) {
     return {
       text: comment.snippet.textDisplay,
       likeCount: comment.snippet.likeCount,
       publishedAt: comment.snippet.publishedAt,
       // Don't store: authorChannelUrl, authorProfileImageUrl
     };
   }
   ```

3. **Terms of Service Compliance**:
   ```typescript
   // Always include proper attribution
   function generateReport(video: any): string {
     return `
   # ${video.snippet.title}

   **Source**: [YouTube](${video.url})
   **Channel**: ${video.snippet.channelName}

   *Data retrieved via YouTube Data API v3*
   *Analysis generated on ${new Date().toISOString()}*
     `;
   }
   ```

## Related Skills

- **15-web-search**: Search for YouTube videos on specific topics
- **16-api-integrator**: Generic API integration patterns applicable to YouTube API
- **17-document-processor**: Process video transcripts similar to document parsing
- **19-social-media-agent**: Cross-platform social media analysis
- **26-ai-code-optimizer**: Optimize video content analysis algorithms
- **32-knowledge-manager**: Index and search video content

## Changelog

### v2.0.0 (2025-12-12)
- Initial release with comprehensive YouTube analysis capabilities
- Integrated YouTube Data API v3 for metadata and statistics
- Added transcript extraction and processing
- Implemented comment fetching with pagination support
- Added sentiment analysis for comments
- Included topic extraction and keyword analysis
- Implemented chapter detection from descriptions and transcripts
- Added channel and playlist analysis
- Comprehensive engagement metrics calculation
- API quota tracking and management
- Caching support for frequently accessed data
- Detailed error handling and validation
