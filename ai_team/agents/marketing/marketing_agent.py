"""
マーケティングAIエージェント

IDP会員1000人達成のための全マーケティング施策を立案・実行する。
SNS投稿・広告コピー・ステップメール・紹介制度・LP改善など。
"""

from ai_team.agents.base import BaseAgent, LA_FABRICA_CONTEXT, PRESENTER, MEDIA_URL

SYSTEM_PROMPT = f"""あなたはLA-FABRICAのマーケティングAIエージェントです。

{LA_FABRICA_CONTEXT}

# あなたの役割
IDP会員1000人達成のために必要なマーケティング施策を全て立案・実行する。
コンテンツマーケ・SNS・メール・広告・紹介制度・イベントを統括する。

# マーケティングの最優先ゴール
「プレーコンサルティング = LA FABRICA」という認知を作りながら、
YouTube → 研究所レター → 無料相談 → IDP というファネルを最大化する。

# マーケティングの鉄則
1. **認知より信頼**: 「知っている」より「信頼している」を作る
2. **量より導線**: 多く発信するより、申込への導線を正確に設計する
3. **データで判断**: 感覚でなく数字で改善する
4. **今すぐ行動させる**: 「後で」を「今すぐ」に変えるコピー設計

# 担当領域
- SNS投稿文（Instagram / X / TikTok / LINE）
- ステップメール設計（研究所レター登録後の自動配信）
- 広告コピー（Google / Meta）
- 紹介制度設計
- ウェビナー・イベント企画
- A/Bテスト案
- 月次マーケティングレポート
"""


class MarketingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="マーケティングAI",
            role="マーケティング部門",
            system_prompt=SYSTEM_PROMPT,
        )

    def write_sns_posts(self, theme: str, platforms: list[str] | None = None) -> str:
        self.log(f"SNS投稿作成: {theme}")
        platforms = platforms or ["Instagram", "X（Twitter）", "TikTok", "LINE"]
        prompt = f"""以下のテーマでSNS投稿文を作成してください。

## テーマ
{theme}

## 作成するプラットフォーム
{', '.join(platforms)}

## 各プラットフォームへの要件

### Instagram（フィード投稿）
- キャプション: 300字以内
- ハッシュタグ: 15〜20個（サッカー育成・個人分析関連）
- 1枚目画像のテキスト案（キャッチコピー）
- CTA: プロフィールリンクへ誘導

### X（Twitter）
- 140字以内×3パターン（A: 問題提起型 / B: 断言型 / C: データ型）
- リプライ誘導の仕掛け（「〇〇な人はRTして」等）

### TikTok / Shorts
- 冒頭3秒のフック（画面に出るテキスト）
- ナレーション案（30秒）
- ラストのCTA

### LINE公式
- 友達追加直後のウェルカムメッセージ
- 週1回の配信テンプレート

## 全プラットフォーム共通
- 「プレーコンサルティング」という言葉を必ず使う
- {PRESENTER}先生の「正直に言います」スタイルを貫く
- 最終的にIDP無料相談か研究所レター登録に誘導する
"""
        result = self.think(prompt)
        self.save_output(result, "marketing", f"sns_posts_{theme[:20]}.md")
        return result

    def write_step_email_sequence(self) -> str:
        self.log("ステップメール設計中...")
        prompt = f"""研究所レター登録後のステップメール（自動配信）を設計してください。

## 設計する配信スケジュール

### Day 0（登録直後）: ウェルカム
### Day 1: 「プレーコンサルティング」とは何か
### Day 3: 「練習だけでは上手くならない」科学的根拠
### Day 5: 自己診断コンテンツ（「あなたは何タイプ？」）
### Day 7: 酒本先生の個人的なストーリー
### Day 10: IDP参加者の変化（事例）
### Day 14: IDP無料相談の案内（初回CTA）
### Day 21: 「今だけ」の特別オファー
### Day 30: 最終CTA（期限設定）
### Day 45〜: 月1回の継続配信テンプレート

## 各メールに含める内容
1. 件名（開封率を最大化する3案）
2. 本文（500字以内・スマホ1スクロール）
3. CTA（1メール1アクション）
4. PS（読後感を高める一言）

## 設計の原則
- 最初の7日で「信頼」を作る
- Day14のCTAを最も力を入れて設計する
- 「売り込み」ではなく「価値提供の延長線上」にIDPを置く
- 解除されないための「読みたくなる」工夫
"""
        result = self.think(prompt)
        self.save_output(result, "marketing", "step_email_sequence.md")
        return result

    def write_ad_copy(self, platform: str, objective: str) -> str:
        self.log(f"広告コピー作成: {platform} / {objective}")
        prompt = f"""LA-FABRICAのIDP広告コピーを作成してください。

## 媒体
{platform}

## 広告目的
{objective}

## 作成内容

### メインコピー（3パターン）
- パターンA: 問題提起型
- パターンB: 社会的証明型
- パターンC: 限定・緊急型

### 各パターンに含める
- ヘッドライン（30字以内）
- ディスクリプション（90字以内）
- CTA文言（「今すぐ無料相談」「まず診断してみる」等）
- ターゲティング推奨設定（年齢・興味・地域）

### ランディングページへの誘導
- クリック後に表示するLPの推奨内容
- ファーストビューで見せるべきメッセージ

## 重要
- 「プレーコンサルティング」という言葉を入れる
- 日本初のポジションを明示する
- 費用対効果を感じさせる（「方向性の間違った練習に何年費やすか」）
"""
        result = self.think(prompt)
        safe = lambda s: "".join(c if c.isalnum() or c in "_ -" else "_" for c in s)
        self.save_output(result, "marketing", f"ad_copy_{safe(platform)[:15]}_{safe(objective)[:15]}.md")
        return result

    def write_referral_program(self) -> str:
        self.log("紹介制度設計中...")
        prompt = """LA-FABRICAのIDP紹介制度を設計してください。

## 目的
IDP参加者が自発的に友人・チームメイトを紹介する仕組みを作り、
口コミによる会員数拡大を実現する。

## 設計する内容

### 紹介者（既存IDP会員）への特典
- 経済的インセンティブ（割引・特典）
- 非金銭的インセンティブ（限定コンテンツ・優先予約等）
- 紹介しやすくなる仕組み（専用URL・紹介カード等）

### 被紹介者（新規申込者）への特典
- 初回割引・特典
- 申込のハードルを下げる仕掛け

### 運用フロー
- 紹介URLの発行方法
- 紹介の追跡方法
- 特典の付与タイミング

### 紹介を促進するコンテンツ
- 既存会員へのお願いメール文
- SNSでシェアしてもらうための投稿テンプレート
- 「友達も一緒に始めよう」キャンペーン案

## 目標
月10件の紹介申込（全体申込の20%を口コミで達成）
"""
        result = self.think(prompt)
        self.save_output(result, "marketing", "referral_program.md")
        return result

    def write_webinar_plan(self, theme: str) -> str:
        self.log(f"ウェビナー企画作成: {theme}")
        prompt = f"""LA-FABRICAのウェビナー（オンラインセミナー）を企画してください。

## テーマ
{theme}

## 企画内容

### 基本設定
- タイトル（参加したくなる）
- 開催時間・形式（Zoom / YouTube Live等）
- 対象参加者
- 定員

### プログラム（90分構成）
- オープニング（5分）
- コンテンツ1（30分）
- コンテンツ2（30分）
- Q&A（15分）
- クロージング＋IDP案内（10分）

### 集客施策
- 告知コンテンツ（YouTube / SNS / 研究所レター）
- 参加申込フォームの設計
- リマインダーメール（3通）

### 当日運営
- 進行台本
- 参加者エンゲージメント施策（質問・アンケート等）
- IDP誘導のタイミングと言葉

### フォローアップ
- 参加者へのサンクスメール
- 未参加者へのアーカイブ案内
- IDP申込への誘導メール（3日後・7日後）
"""
        result = self.think(prompt)
        self.save_output(result, "marketing", f"webinar_{theme[:20]}.md")
        return result

    def write_monthly_marketing_plan(self, month: str, idp_target: int) -> str:
        self.log(f"月次マーケティングプラン作成: {month}")
        prompt = f"""LA-FABRICAの{month}のマーケティング実行プランを作成してください。

## 今月のIDP申込目標
{idp_target}件

## 作成する内容

### 今月の最重要テーマ（1つ）
市場カレンダー・季節性・競合状況から最も効果的なテーマを選定

### コンテンツカレンダー（週別）
- Week1〜Week4の各週のYouTube・記事・SNSのテーマ
- 各コンテンツが目標申込数にどう貢献するか

### 施策優先順位（TOP3）
1位・2位・3位それぞれの施策内容・期待効果・担当（AI）

### KPI設定
| 指標 | 目標値 |
- YouTube再生数
- 研究所レター新規登録
- 無料相談申込
- IDP成約

### リスクと対策
今月想定されるリスクと対応策

### 今月やらないこと
集中するために捨てる施策
"""
        result = self.think(prompt)
        self.save_output(result, "marketing", f"monthly_plan_{month}.md")
        return result
