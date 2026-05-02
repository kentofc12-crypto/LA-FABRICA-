# LA-FABRICA AIチーム

酒本先生と代表以外、全員AIエージェントで構成されたコンテンツ生産チーム。

## AIチームの構成

```
COO AI（コンテンツ統括）
├── YouTube コンテンツ部署
│   ├── Project Leader AI    品質管理・カレンダー管理
│   ├── 企画AI               国内・国外ネタから企画書作成
│   ├── 台本AI               酒本先生スタイルの台本・Shorts制作
│   └── [編集は人間 or 外注]  動画編集・テロップ・サムネイル
│
├── メディア事業部署
│   ├── Marketing Leader AI  戦略・KPI管理
│   ├── 編集AI               記事執筆（戦術分析・育成・保護者向け）
│   ├── SEO・配信AI          SEO設定・SNS配信文・キーワード
│   └── 誘導・CTA AI         CTA最適化・ステップメール設計
│
├── リサーチ部署
│   ├── 国内リサーチAI       国内サッカーニュース・トレンド収集
│   └── 国外リサーチAI       海外育成メソッド・科学論文・戦術収集
│
└── ニュースレターAI         研究所レター週次・特別号作成
```

## 稼働状況の確認方法

### 1. ターミナル（リアルタイム）
実行中はターミナルにログが流れます。
```
[国内リサーチAI / マーケットリサーチ部署 / 国内担当] 今週の国内ネタリストを生成中...
[YouTube企画AI / YouTubeコンテンツ部署 / 企画チーム] 今週のYouTube企画書 1本を作成中...
[台本制作AI / YouTubeコンテンツ部署 / 台本チーム] 台本作成中: 動画1
...
✅ YouTube ワークフロー完了
```

### 2. output/ フォルダ（生成物の確認）
全AIエージェントの生成物が保存される。
```
ai_team/output/
├── research/
│   ├── 20260502_120000_domestic_topics.md    国内リサーチ結果
│   ├── 20260502_120100_international_topics.md  国外リサーチ結果
│   └── 20260502_120200_coo_weekly_brief.md   COO判断
├── scripts/
│   ├── 20260502_120300_weekly_plans.md       企画書
│   ├── 20260502_120400_script_動画1.md       台本（本番用）
│   ├── 20260502_120500_shorts_動画1.md       Shorts台本
│   └── 20260502_120600_quality_review.md     PLレビュー
├── articles/
│   ├── 20260502_120700_article_○○.md        記事本文
│   ├── 20260502_120800_seo_settings.md       SEO設定
│   └── 20260502_120900_cta_optimization.md   CTA設定
└── newsletters/
    └── 20260502_121000_newsletter_2026_W18.md 研究所レター
```

### 3. GitHub（非同期確認）
`docs/MAY_SPRINT.md` で5月の進捗を追跡。
Issues でタスク管理（手動更新）。

## セットアップ

```bash
cd ai_team
pip install -r requirements.txt

# APIキーを設定
export ANTHROPIC_API_KEY=sk-ant-xxxxx
```

## 使い方

```bash
# 今日の曜日に応じたワークフロー（推奨）
python main.py

# YouTube動画を今すぐ1本制作
python main.py --workflow youtube

# メディア記事を今すぐ2本制作
python main.py --workflow media

# 研究所レターを作成
python main.py --workflow newsletter

# 全ワークフローを一括実行
python main.py --workflow all

# 酒本先生からのメッセージを入れて実行
python main.py --workflow all --message "今週はセレクション前の選手に特化したい"

# お知らせを入れて実行
python main.py --workflow newsletter --announcement "IDCキャンプ残枠3名"
```

## 生産目標（5月）

| コンテンツ | 目標 |
|---------|------|
| YouTube長尺 | 4本 |
| YouTube Shorts | 16本 |
| メディア記事 | 20本 |
| 研究所レター | 4本 |
