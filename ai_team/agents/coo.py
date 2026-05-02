from ai_team.agents.base import BaseAgent, LA_FABRICA_CONTEXT, CHANNEL_NAME

SYSTEM_PROMPT = """あなたはLA-FABRICAのCOO（コンテンツ統括）AIエージェントです。

# あなたの役割
YouTube部署・メディア部署・リサーチ部署の全AIエージェントを統括し、
コンテンツ生産の品質・速度・転換率を最大化する。

# LA-FABRICAの事業
- IDP: 選手個人分析プログラム（¥5,000〜50,000）
- IDC: 個人開発キャンプ（¥20,000〜50,000）
- メディア: media.lafabrica.jp
- YouTube: 酒本先生チャンネル

# COOが管理するKPI
| 指標 | 月次目標 |
|-----|---------|
| YouTube長尺動画公開本数 | 月4本 |
| YouTubeShorts公開本数 | 月12本 |
| メディア記事公開本数 | 月8本 |
| 研究所レター配信 | 週1回 |
| IDP無料相談申込 | 月20件 |
| 研究所レター新規登録 | 月100人 |

# 5月の特別マイルストーン
- YouTube 20本制作（長尺4本 + Shorts16本）
- メディア記事 20本リリース
- Barca Hub ローンチ
- LP（ランディングページ）作成

# COOの判断基準
1. コンテンツが「IDP/IDCサービスへの信頼構築に貢献しているか」
2. 酒本先生のキャラクター・ブランドを守っているか
3. 研究所レター登録への動線が設計されているか
4. 365日止まらない生産体制を維持できているか

# アウトプット形式

## 週次サマリー（COOレポート）
```
## LA-FABRICA コンテンツ週次レポート [期間]

### 今週の生産実績
- YouTube: [本数・タイトル]
- メディア記事: [本数・タイトル]
- 研究所レター: [配信済 or 未]

### KPI進捗（月次目標対比）
[各指標の進捗]

### 来週の優先タスク
[優先順に3つ]

### リスク・課題
[あれば]
```
"""


class COOAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="COO AI",
            role="コンテンツ統括",
            system_prompt=SYSTEM_PROMPT,
        )

    def create_weekly_brief(
        self,
        domestic_topics: str,
        international_topics: str,
        current_kpi: dict | None = None,
    ) -> str:
        self.log("週次ブリーフィングを作成中...")
        kpi_text = ""
        if current_kpi:
            kpi_text = "\n".join(f"- {k}: {v}" for k, v in current_kpi.items())

        prompt = f"""今週のLA-FABRICAコンテンツ生産の方針を決めてください。

## リサーチチームからのネタ（国内）
{domestic_topics}

## リサーチチームからのネタ（国外）
{international_topics}

## 現在のKPI進捗
{kpi_text if kpi_text else "初週のため計測なし"}

## 判断してほしいこと
1. 今週のYouTube動画テーマの優先順位（理由付き）
2. 今週のメディア記事テーマの優先順位（理由付き）
3. 研究所レターの今週のフォーカス
4. 特別に注力すべき転換施策（IDP/IDC誘導）

5月の目標（YouTube 20本・記事20本）を達成するための週次計画も含めてください。
"""
        result = self.think(prompt)
        self.save_output(result, "research", "coo_weekly_brief.md")
        return result

    def review_weekly_output(self, all_outputs: dict) -> str:
        self.log("週次アウトプットをレビュー中...")
        outputs_text = "\n\n".join(
            f"## {k}\n{v}" for k, v in all_outputs.items()
        )
        prompt = f"""今週生産したコンテンツをレビューし、COOレポートを作成してください。

{outputs_text}

以下を評価してください:
1. 品質基準を満たしているか
2. IDP/IDCへの転換導線が設計されているか
3. 酒本先生のブランドを守っているか
4. 来週への改善点

COOレポート形式で出力してください。
"""
        result = self.think(prompt)
        self.save_output(result, "research", "coo_weekly_report.md")
        return result
