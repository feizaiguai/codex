---
name: 48-skill-list-maintainer-G
description: Use when managing the skill registry/configuration file (skills.json), including add/update/delete/view, validation, backups, or batch operations.
---

# Skill List Maintainer

**鐗堟湰**: 2.0.0

## 鎻忚堪

鏅鸿兘鎶€鑳藉垪琛ㄧ淮鎶ゅ伐鍏凤紝鐢ㄤ簬绠＄悊Claude Code鎶€鑳借矾鐢辩郴缁熺殑閰嶇疆鏂囦欢锛坰kills.json锛夈€?

## 鏍稿績鑳藉姏

- 鉁?娣诲姞鏂版妧鑳藉埌閰嶇疆鏂囦欢
- 鉁?鏇存柊鐜版湁鎶€鑳界殑淇℃伅
- 鉁?鍒犻櫎鎶€鑳?
- 鉁?鏌ョ湅鎶€鑳藉垪琛?
- 鉁?鑷姩楠岃瘉閰嶇疆鏍煎紡
- 鉁?澶囦唤閰嶇疆鏂囦欢
- 鉁?鎵归噺鎿嶄綔鏀寔

## 瑙﹀彂鏉′欢

褰撶敤鎴疯姹備互涓嬫搷浣滄椂鑷姩瑙﹀彂锛?
- 娣诲姞鏂版妧鑳藉埌绯荤粺
- 鏇存柊鐜版湁鎶€鑳介厤缃?
- 鍒犻櫎鎶€鑳?
- 鏌ョ湅鎶€鑳藉垪琛?
- 鎵归噺瀵煎叆鎶€鑳介厤缃?

## 鍩烘湰宸ヤ綔娴佺▼

1. **瑙ｆ瀽鐢ㄦ埛鍛戒护** - 璇嗗埆鎿嶄綔绫诲瀷锛坅dd/update/delete/view锛?
2. **楠岃瘉杈撳叆** - 妫€鏌ユ妧鑳藉弬鏁版牸寮?
3. **澶囦唤閰嶇疆** - 鑷姩鍒涘缓閰嶇疆鏂囦欢澶囦唤
4. **鎵ц鎿嶄綔** - 鍘熷瓙鎬т慨鏀归厤缃枃浠?
5. **楠岃瘉缁撴灉** - 纭繚閰嶇疆鏂囦欢鏍煎紡姝ｇ‘
6. **杩斿洖纭** - 鎻愪緵鎿嶄綔缁撴灉鍙嶉

## 浣跨敤鍦烘櫙

### 1. 娣诲姞鏂版妧鑳?
```
娣诲姞鎶€鑳斤細
鍚嶇О: pdf-processor
绫诲瀷: utility
浼樺厛绾? medium
鎻忚堪: PDF鏂囦欢澶勭悊宸ュ叿
鍏抽敭璇? 澶勭悊PDF, 杞崲PDF, PDF鎿嶄綔
```

### 2. 鏇存柊鎶€鑳?
```
鏇存柊鎶€鑳?02-architecture:
娣诲姞鍏抽敭璇? 绯荤粺鏋舵瀯, 寰湇鍔?
淇敼鎻忚堪: 鏋舵瀯璁捐涓撳锛屾彁渚涘叏闈㈢殑鎶€鏈灦鏋勬柟妗?
```

### 3. 鍒犻櫎鎶€鑳?
```
鍒犻櫎鎶€鑳? old-skill-name
```

### 4. 鏌ョ湅鎶€鑳?
```
鏄剧ず鎵€鏈夋妧鑳?
鏌ョ湅鎶€鑳? 02-architecture
```

## 蹇€熺ず渚?

**鏈€绠€鍗曠殑浣跨敤绀轰緥**锛?
```
鐢ㄦ埛: "娣诲姞鎶€鑳斤細web-scraper锛屽叧閿瘝锛氱埇铏?鎶撳彇缃戦〉"
Assistant: [浣跨敤skill-list-maintainer鑷姩娣诲姞鍒皊kills.json]
```

## 鎶€鑳藉弬鏁?

- `name`: 鎶€鑳藉悕绉帮紙蹇呴渶锛?
- `type`: 绫诲瀷锛坉omain/utility/general锛?
- `priority`: 浼樺厛绾э紙high/medium/low锛?
- `description`: 鎻忚堪
- `keywords`: 瑙﹀彂鍏抽敭璇嶅垪琛?
- `patterns`: 姝ｅ垯琛ㄨ揪寮忔ā寮忥紙鍙€夛級

## 娉ㄦ剰浜嬮」

1. 鎵€鏈夋搷浣滈兘浼氳嚜鍔ㄥ浠藉師閰嶇疆鏂囦欢
2. 娣诲姞鎶€鑳芥椂浼氶獙璇佹牸寮忔纭€?
3. 鍏抽敭璇嶆敮鎸佷腑鑻辨枃
4. 淇敼浼氱珛鍗崇敓鏁堬紝鏃犻渶閲嶅惎Claude Code

## 鎶€鏈疄鐜?

- 浣跨敤Python瀹炵幇
- JSON鏍煎紡閰嶇疆鏂囦欢
- 鑷姩鏍煎紡楠岃瘉
- 鍘熷瓙鎬ф搷浣滀繚璇佹暟鎹畨鍏?

## 鍙傝€冩枃妗?

璇︾粏鍐呭璇峰弬鑰冿紙鎸夐渶闃呰锛夛細
- [api_reference.md](references/api_reference.md): 閰嶇疆鏂囦欢API璇︾粏鍙傝€?
- [best_practices.md](references/best_practices.md): 鎶€鑳介厤缃渶浣冲疄璺?
- [troubleshooting.md](references/troubleshooting.md): 甯歌闂鎺掓煡

