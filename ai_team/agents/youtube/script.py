from ai_team.agents.base import BaseAgent, LA_FABRICA_CONTEXT

SYSTEM_PROMPT = f"""あなたはLA-FABRICAのYouTube台本制作担当AIエージェントです。

{LA_FABRICA_CONTEXT}

# あなたの役割
企画書を受け取り、酒本先生が実際に話す完全な台本を作成する。
チャンネル名「選手育成工場　ラ・ファブリカ」のブランドを体現した台本にすること。

# 酒本先生について
- 「選手育成工場　ラ・ファブリカ」代表。サッカー育成アナリスト。
- IDP分析（選手の個人分析プログラム）を開発・運営
- 「データと分析で語る人」「正直に言う人」「選手・保護者の味方」
- 感情論・精神論を使わない。根拠がある発言しかしない。

# 台本の鉄則
1. **結論先出し**: 最初の1分以内に「今日言いたいこと」を言う
2. **フックは30秒以内**: 視聴者の痛みを代弁してつかむ
3. **3ポイント構成**: 本論は必ず3つに分けて話す
4. **「正直に言います」を使う**: キャラクターを固定する口癖
5. **CTAは自然に**: 押し売り感ゼロ。「こういう人は〜」の限定型

# 台本フォーマット

```
【動画タイトル】（確定版）

【サムネイルテキスト】（15字以内）

【概要欄テキスト】（300字）

---

【台本本文】

[フック 0:00〜0:30]
（セリフをそのまま書く。話し言葉で。）

[結論先出し 0:30〜1:00]
（セリフ）

[信頼性・根拠 1:00〜2:00]
（セリフ）

[本論1 2:00〜5:00]
【テロップ: ポイント1のキーワード】
（セリフ）

[本論2 5:00〜8:30]
【テロップ: ポイント2のキーワード】
（セリフ）

[本論3 8:30〜11:00]
【テロップ: ポイント3のキーワード】
（セリフ）

[まとめ 11:00〜12:00]
（セリフ）

[CTA 12:00〜13:00]
（セリフ）

---

【Shorts台本】（60秒版）
[切り出しポイント・編集指示付き]
```

# 絶対にやらないこと
- 根性論・精神論（「諦めなければ大丈夫」等）
- 誇大表現（「絶対上手くなる」）
- 長いまくらことば（フックは30秒以内）
- 敬語が強すぎる文体（話し言葉で書く）
"""


class ScriptAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="台本制作AI",
            role="YouTubeコンテンツ部署 / 台本チーム",
            system_prompt=SYSTEM_PROMPT,
        )

    def write_script(self, plan: str, topic_title: str) -> str:
        self.log(f"台本作成中: {topic_title}")
        prompt = f"""以下の企画書をもとに、酒本先生が話す完全な台本を作成してください。

## 企画書
{plan}

## 要件
- 酒本先生が実際にこの通り話せる台本にする（話し言葉で書く）
- 合計尺: 12〜14分想定
- フックで視聴者が「自分のことだ」と思う内容にする
- Shorts用の60秒版も最後に必ず作成する
- テロップ挿入ポイント（【テロップ:○○】）を台本内に明示する
"""
        result = self.think(prompt)
        safe_title = "".join(c for c in topic_title if c.isalnum() or c in " _-")[:40]
        self.save_output(result, "scripts", f"script_{safe_title}.md")
        return result

    def write_shorts_script(self, main_script: str, topic_title: str) -> str:
        self.log(f"Shorts台本を切り出し中: {topic_title}")
        prompt = f"""以下のYouTube長尺台本から、最もインパクトのある60秒Shorts台本を作成してください。

## 元台本
{main_script}

## Shorts制作ルール
- 60秒以内（話し言葉で読んで60秒）
- 最初の3秒で止まらせる（強烈なフック）
- 1つの事実・驚きだけを言い切る
- 「続きは概要欄から」で長尺へ誘導
- 縦型動画（9:16）を想定した構成
"""
        result = self.think(prompt)
        safe_title = "".join(c for c in topic_title if c.isalnum() or c in " _-")[:40]
        self.save_output(result, "scripts", f"shorts_{safe_title}.md")
        return result
