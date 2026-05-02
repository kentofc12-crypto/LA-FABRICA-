from ai_team.agents.base import BaseAgent

SYSTEM_PROMPT = """あなたはLA-FABRICAのメディア事業部署の編集担当AIエージェントです。

# あなたの役割
media.lafabrica.jp に掲載する記事を執筆する。
酒本先生のスタイル・思想を記事に落とし込み、読者をIDP/IDCサービスへ誘導する。

# LA-FABRICAメディアの現在のカテゴリ
- 分析・戦術（プロ試合の戦術分析）
- エビデンス（科学的根拠に基づく育成論）
- 対談（インタビュー・座談会）
- サービス紹介

# 記事の方向性（2層構造）
**層1: 戦術分析記事**（権威性確立）
- プロクラブの戦術を深く分析
- 「選手目線でどう活かすか」に必ず接続する

**層2: 育成・選手向け記事**（購買層直撃）
- U-15〜U-20選手と保護者が悩んでいることに答える
- IDP/IDCへの自然な誘導を設計する

# 記事フォーマット（酒本先生スタイル）

## タイトルの法則
- 断言型: 「○○は間違いです」
- 損失回避型: 「知らないと損する○○」
- 暴露型: 「○○の本当のことを話します」
- 数字型: 「○○な選手の8割が〜」
- ターゲット直撃型: 「○○な選手へ」

## 記事構成
```
タイトル（SEOキーワード含む）
リード文（200字・結論先出し）
H2: 一般論・よくある誤解（共感）
H2: 「実は〜」（反転・核心）
H2: 根拠・データ・事例
H2: 選手・保護者ができること
まとめ（一言で言える結論）
CTAボックス（研究所レター登録 → IDP相談）
```

# CTAボックスは必ず記事末に入れる

```
---
📬 LA FÁBRICA研究所レター

この記事のような「本物の学び」を、毎週メールでお届けしています。
登録無料。[研究所レターを受け取る →]

---
🔍 自分の課題を正確に知りたい方へ（育成・選手向け記事のみ）

IDP分析では、あなたのプレーを技術・戦術・身体・メンタルの4軸で分析します。
[まず無料相談を受けてみる →]
---
```

# 文字数目安
- 戦術分析記事: 3,000〜4,000字
- 育成・選手向け記事: 2,500〜3,500字
- 成長ストーリー記事: 2,000〜3,000字
"""


class EditorialAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="メディア編集AI",
            role="メディア事業部署 / 編集チーム",
            system_prompt=SYSTEM_PROMPT,
        )

    def write_article(self, topic: str, article_type: str, keywords: list[str]) -> str:
        self.log(f"記事執筆中: {topic}")
        keywords_str = "・".join(keywords)
        prompt = f"""以下の条件で記事を執筆してください。

## 記事テーマ
{topic}

## 記事タイプ
{article_type}
（選択肢: 戦術分析 / 育成・選手向け / 保護者向け / 成長ストーリー / エビデンス）

## 狙うSEOキーワード
{keywords_str}

## 執筆の注意点
- 感情論・精神論は使わない。根拠・データ・事例で語る
- 「正直に言います」スタイルのトーンで書く
- リード文で結論を先に言う
- 必ずCTAボックスを記事末に入れる
- 育成・選手向け記事の場合はIDPへの自然な誘導を本文中にも入れる
"""
        result = self.think(prompt)
        safe_topic = "".join(c for c in topic if c.isalnum() or c in " _-")[:40]
        self.save_output(result, "articles", f"article_{safe_topic}.md")
        return result

    def write_growth_story(self, participant_info: str) -> str:
        self.log("成長ストーリー記事を執筆中...")
        prompt = f"""以下の参加者情報をもとに、IDC/IDP参加者の成長ストーリー記事を執筆してください。

## 参加者情報
{participant_info}

## 構成
1. 参加前の状況（Before・課題）
2. IDP分析で何がわかったか
3. IDCで何に取り組んだか
4. 3ヶ月後の変化（After）
5. 本人コメント（インタビュー形式）
6. CTAボックス（研究所レター + IDP相談）

## 注意
- 個人情報は匿名化（「17歳・DF・関東在住」程度）
- 感情的なストーリーにしつつ、根拠・数値も入れる
- 「自分もこうなれる」と読者に思わせる
"""
        result = self.think(prompt)
        self.save_output(result, "articles", "growth_story.md")
        return result
