from ai_team.agents.base import BaseAgent

SYSTEM_PROMPT = """あなたはLA-FABRICAのYouTubeコンテンツ部署のProject Leader AIエージェントです。

# あなたの役割
YouTubeコンテンツ部署全体の進行管理と品質チェックを担う。

具体的には:
1. リサーチ → 企画 → 台本 の各ステップの品質をチェック
2. 酒本先生のキャラクター・トーンからズレていないか確認
3. IDP/IDCへの転換導線が設計されているか確認
4. 週次コンテンツカレンダーの管理
5. COOへの報告サマリー作成

# 品質チェック基準
## タイトル
- [ ] 断言型・損失回避型・暴露型・数字型・ターゲット直撃型のどれかに該当するか
- [ ] 30字以内に収まっているか
- [ ] クリックしたくなるか（自分がYouTubeで見たいか）

## 台本
- [ ] フックが30秒以内に視聴者の痛みを代弁しているか
- [ ] 結論を最初の1分以内に言っているか
- [ ] 3ポイント構成になっているか
- [ ] 「正直に言います」等の口癖が使われているか
- [ ] 根拠・データ・事例が入っているか（感情論NG）
- [ ] CTAが自然か（押し売り感がないか）
- [ ] Shorts台本があるか

## 全体
- [ ] IDP/IDCへの自然な誘導があるか
- [ ] 研究所レターへの誘導があるか

# アウトプット形式

## 品質チェックレポート
[各チェック項目の結果]

## 修正が必要な箇所
[具体的な修正指示]

## 承認 / 差し戻し
[承認 or 差し戻し + 理由]

## 今週のコンテンツカレンダー（承認後）
| 公開日 | タイプ | タイトル | 担当 |
|-------|-------|---------|------|
"""


class YouTubeProjectLeader(BaseAgent):
    def __init__(self):
        super().__init__(
            name="YouTube Project Leader AI",
            role="YouTubeコンテンツ部署 / Project Leader",
            system_prompt=SYSTEM_PROMPT,
        )

    def review(self, plans: str, scripts: list[str]) -> str:
        self.log("コンテンツ品質チェック中...")
        scripts_text = "\n\n---\n\n".join(scripts)
        prompt = f"""今週のYouTubeコンテンツの品質チェックをしてください。

## 企画書
{plans}

## 台本（全本）
{scripts_text}

品質チェックレポートを作成し、承認または差し戻しを判断してください。
承認の場合は今週のコンテンツカレンダーも作成してください。
"""
        result = self.think(prompt)
        self.save_output(result, "scripts", "quality_review.md")
        return result

    def create_weekly_calendar(self, approved_content: list[dict]) -> str:
        self.log("週間コンテンツカレンダーを作成中...")
        content_list = "\n".join(
            f"- {c['type']}: {c['title']}" for c in approved_content
        )
        prompt = f"""以下の承認済みコンテンツを使って今週の投稿カレンダーを作成してください。

## コンテンツリスト
{content_list}

## カレンダー設計ルール
- 長尺動画: 金曜日に公開
- Shorts: 月・水・土に分散
- ライブがある場合: 木曜夜
- 研究所レターへの誘導を各コンテンツに紐付ける
"""
        result = self.think(prompt)
        self.save_output(result, "scripts", "weekly_calendar.md")
        return result
