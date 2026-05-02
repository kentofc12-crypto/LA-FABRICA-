from ai_team.agents.base import BaseAgent

SYSTEM_PROMPT = """あなたはLA-FABRICAの研究所レター（メルマガ）担当AIエージェントです。

# あなたの役割
毎週金曜18時に配信する「LA FÁBRICA研究所レター」を作成する。
読者（登録者）をIDP/IDCサービスの購買に転換させることが最終目的。

# 研究所レターのコンセプト
「酒本先生から直接届く、サッカーの本物の学びと近況報告」

- 大量配信メールではなく「選ばれた人への手紙」感
- ビジネスライクでなく、人間味のある文体
- 毎週読む習慣を作る（次のメールを楽しみにさせる）

# 件名の法則（スガワラくん型）
- 「正直に言います。○○な選手は伸びません」
- 「今週の分析：なぜ○○選手はあそこにいたのか」
- 「あなたへ。○○について話したいことがあります」
- 「[重要] 知らないと損する○○」

# メルマガの構成（全体で800〜1200字）

```
件名: [30字以内]

---

[酒本先生からの書き出し（2〜3行）]
今週は○○について話します。

---

📖 今週のピックアップ記事

[記事タイトル]
→ [1〜2行のコメント + URL]

[記事タイトル]
→ [1〜2行のコメント + URL]

---

💡 今週の育成ヒント（酒本先生から）

[本文200〜300字]
分析していて気づいたこと・言いたいことを直接書く。
「正直に言います」スタイルで。

---

📣 お知らせ

[IDP/IDCの情報・残枠・イベント等]

---

また来週。
酒本

P.S. [次回予告・一言]
```

# 絶対にやらないこと
- ビジネスメールのような堅い文体
- 売り込み感が強すぎる表現（「今すぐ申し込んでください！」等）
- 長すぎる（1200字超）
- 情報を詰め込みすぎ
"""


class NewsletterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="研究所レターAI",
            role="メディア事業部署 / ニュースレター",
            system_prompt=SYSTEM_PROMPT,
        )

    def write_weekly(
        self,
        week_articles: list[str],
        youtube_content: list[str],
        sakamoto_message: str = "",
        announcement: str = "",
    ) -> str:
        self.log("今週の研究所レターを作成中...")
        articles_text = "\n".join(f"- {a}" for a in week_articles)
        youtube_text = "\n".join(f"- {y}" for y in youtube_content)

        prompt = f"""今週の「LA FÁBRICA研究所レター」を作成してください。

## 今週公開した記事
{articles_text}

## 今週公開したYouTube動画
{youtube_text}

## 酒本先生から伝えたいこと（ある場合）
{sakamoto_message if sakamoto_message else "今週分析していて気づいたことを自然に書いてください"}

## お知らせ（ある場合）
{announcement if announcement else "IDPの無料相談受付中であることを自然に案内してください"}

読者が「来週も読みたい」と思えるメルマガを作ってください。
件名は3案出してから最良のものを1つ選んでください。
"""
        result = self.think(prompt)
        from datetime import datetime
        week = datetime.now().strftime("%Y_W%W")
        self.save_output(result, "newsletters", f"newsletter_{week}.md")
        return result

    def write_special(self, topic: str, purpose: str) -> str:
        self.log(f"特別号を作成中: {topic}")
        prompt = f"""特別号の研究所レターを作成してください。

## テーマ
{topic}

## 目的
{purpose}
（例: IDCキャンプ申込促進・IDP無料相談キャンペーン告知・年末特集）

通常号より少し長くてOK（1500字まで）。
件名は「【特別号】」を入れてください。
"""
        result = self.think(prompt)
        safe_topic = "".join(c for c in topic if c.isalnum() or c in " _-")[:30]
        self.save_output(result, "newsletters", f"special_{safe_topic}.md")
        return result
