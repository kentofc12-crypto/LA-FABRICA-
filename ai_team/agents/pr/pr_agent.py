from ai_team.agents.base import BaseAgent, LA_FABRICA_CONTEXT, PRESENTER, BRAND_JP, MEDIA_URL

SYSTEM_PROMPT = f"""あなたはLA-FABRICAのPR戦略AIエージェントです。

{LA_FABRICA_CONTEXT}

# あなたの役割
「プレーコンサルティング = LA FABRICA」という認知を日本に作るため、
プレスリリース・メディアアウトリーチ・パートナーシップ提案・キャンペーン企画など
あらゆるPR施策を立案・実行します。

# 最終目標
2026年12月31日までにIDP会員1000人達成

# PRの3原則
1. **カテゴリーを作る**: 「プレーコンサルティング」という言葉を世に広める
2. **権威を作る**: 酒本先生を「日本初のサッカープレーコンサルタント」として権威化
3. **事例を作る**: IDP参加者のBefore/Afterを積み上げて社会的証明を構築

# ターゲット別アプローチ
- **メディア**: サカイク / ジュニアサッカーNews / フットボールチャンネル / Yahoo!スポーツ
- **インフルエンサー**: サッカー系YouTube（5万〜50万登録）/ 育成コーチ / 元Jリーガー
- **法人**: 民間スクール / Jアカデミー / 高校強豪校 / 個人コーチ
- **保護者コミュニティ**: Facebookグループ / LINE / 地域のサッカーコミュニティ

# アウトプット品質基準
- プレスリリース: PR TIMESに即掲載できる品質
- アウトリーチメール: 返信率30%以上を狙う件名と本文
- 提案書: 相手の利益を最初に伝える構成
- キャンペーン: 申込ページのCVRを最大化するコピー
"""


class PRAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PR AI",
            role="PR戦略",
            system_prompt=SYSTEM_PROMPT,
        )

    def write_press_release(self, theme: str, milestone: str = "") -> str:
        self.log(f"プレスリリース作成中: {theme}")
        prompt = f"""以下のテーマでPR TIMESに掲載できるプレスリリースを作成してください。

## テーマ
{theme}

## マイルストーン・実績（あれば）
{milestone if milestone else "ローンチ・サービス開始の告知"}

## 必須要素
1. 見出し（キャッチーで検索されやすい）
2. サブ見出し
3. リード文（5W1H）
4. 本文（背景→課題→解決策→実績→展望）
5. {PRESENTER}先生のコメント（引用）
6. サービス概要表
7. 会社概要
8. 問い合わせ先（{MEDIA_URL}）

## トーン
- ニュース性を強調
- 「日本初」「日本唯一」のポジションを明示
- 数字・データを必ず入れる
"""
        result = self.think(prompt)
        self.save_output(result, "pr", f"press_release_{theme[:20]}.md")
        return result

    def write_outreach_email(self, target_type: str, target_name: str = "") -> str:
        self.log(f"アウトリーチメール作成: {target_type}")
        prompt = f"""LA-FABRICAのIDP（個人分析プログラム）を広めるための
アウトリーチメールを作成してください。

## 送り先の種類
{target_type}

## 送り先の名前（あれば）
{target_name if target_name else "（担当者様）"}

## 要件
1. 件名：開封率を最大化する件名3案
2. 本文：
   - 冒頭で相手の利益を伝える（LA FABRICAの紹介は後回し）
   - 「プレーコンサルティング」という新概念を簡潔に説明
   - 具体的な提案内容（コラボ・取材・導入など）
   - 返信しやすい一言CTA
3. 全文500字以内（読んでもらえる長さ）

## 返信率を上げるポイント
- 相手が「自分ごと」に感じる書き出し
- 「断りにくい」提案設計（無料・試し・期間限定）
- 社会的証明（「○○先生も協力してくれました」等）
"""
        result = self.think(prompt)
        self.save_output(result, "pr", f"outreach_{target_type[:20]}.md")
        return result

    def write_campaign(self, campaign_name: str, season: str, target: str) -> str:
        self.log(f"キャンペーン企画作成: {campaign_name}")
        prompt = f"""LA-FABRICAのIDPキャンペーンを企画してください。

## キャンペーン名
{campaign_name}

## 季節・タイミング
{season}

## ターゲット
{target}

## 作成するもの
1. キャンペーンコンセプト（一言で伝わるキャッチコピー）
2. 特典・割引内容の設計
3. LPに使うコピー（ヘッドライン・本文・CTA）
4. SNS告知文3パターン（Twitter/Instagram/LINE）
5. 研究所レター告知文
6. YouTube動画告知スクリプト（30秒）
7. 期間・実施スケジュール

## 目標
申込み件数を最大化する。緊急性・希少性・社会的証明を全て活用すること。
"""
        result = self.think(prompt)
        self.save_output(result, "pr", f"campaign_{campaign_name[:20]}.md")
        return result

    def write_b2b_proposal(self, organization_type: str) -> str:
        self.log(f"法人提案書作成: {organization_type}")
        prompt = f"""LA-FABRICAのIDP法人プランの提案書を作成してください。

## 提案先の種類
{organization_type}

## 提案書の構成
1. エグゼクティブサマリー（1ページ相当）
2. 現状の課題（相手の痛みを言語化）
3. LA FABRICAが提供できる価値
4. 具体的なサービス内容と料金プラン
5. 導入実績・事例（パイロット段階の成果を含む）
6. 導入ステップ（3ステップで簡単に）
7. FAQ
8. 特別オファー（期間限定）

## トーン
- 相手の利益を最優先に
- 「プレーコンサルティング」の市場価値を伝える
- 競合がいない今だからこその先行者メリットを強調
"""
        result = self.think(prompt)
        self.save_output(result, "pr", f"b2b_proposal_{organization_type[:20]}.md")
        return result

    def write_lp_copy(self, page_type: str) -> str:
        self.log(f"LPコピー作成: {page_type}")
        prompt = f"""LA-FABRICAの{page_type}のランディングページコピーを作成してください。

## 必須セクション
1. ヒーローセクション
   - キャッチコピー（一撃で刺さる）
   - サブコピー（キャッチを補強）
   - CTA（申込ボタン）
2. 問題提起セクション（読者の悩みを言語化）
3. 解決策セクション（IDPがなぜ答えなのか）
4. サービス内容セクション（何をしてもらえるか）
5. 実績・社会的証明セクション
6. 料金セクション（シンプルに）
7. FAQ
8. 最終CTA（緊急性・希少性を付ける）

## コピーの原則
- 「プレーコンサルティング」という言葉を3回以上使う
- 読者は「保護者」と「選手本人」の両方を意識
- ベネフィット訴求（特徴より、変化後の姿を語る）
- 具体的な数字を入れる（○%改善、○人が体験、等）
"""
        result = self.think(prompt)
        self.save_output(result, "pr", f"lp_{page_type[:20]}.md")
        return result
