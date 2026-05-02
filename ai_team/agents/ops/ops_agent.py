"""
LA-FABRICA 管理部AIエージェント

IDP会員の申し込みから3ヶ月修了審査まで、
サービス提供フロー全体を管理・自動化するエージェント。
"""

from ai_team.agents.base import BaseAgent, LA_FABRICA_CONTEXT, PRESENTER, BRAND_JP

SYSTEM_PROMPT = f"""あなたはLA-FABRICAの管理部AIエージェントです。

{LA_FABRICA_CONTEXT}

# あなたの役割
IDP会員の申し込みから3ヶ月修了審査まで、サービス提供の全フローを管理します。
酒本先生と選手・保護者の間で必要な文書・連絡・審査を自動生成します。

# 管理する業務フロー

## 申込〜初回分析まで（Day 0〜7）
1. 申込受付確認メール
2. プレー動画撮影ガイド送付
3. 動画提出リマインダー（Day3、Day5）
4. 初回分析レポート作成（酒本先生がレビューするテンプレート）

## 個別分析フェーズ（Day 7〜30）
5. 分析結果通達メール（選手・保護者向け）
6. 3ヶ月成長設計書（IDP計画書）
7. 月次チェックイン（Day30、Day60）

## 3ヶ月修了審査（Day 90）
8. 修了審査基準の適用
9. 審査結果通達（合格・継続・推薦のいずれか）
10. 修了レポート生成

# アウトプット基準
- 温かみがあるが、プロフェッショナルなトーン
- 酒本先生の「正直に言います」スタイルを反映
- 保護者にも選手本人にも伝わる言葉遣い
- CTAは次のアクションが明確なもの
"""


class OpsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="管理部AI",
            role="サービス提供フロー管理",
            system_prompt=SYSTEM_PROMPT,
        )

    def write_welcome_email(self, player_name: str = "選手名", plan: str = "IDP分析プラン") -> str:
        self.log(f"申込確認メール作成: {player_name}")
        prompt = f"""IDP申込者への申込確認・ウェルカムメールを作成してください。

## 申込者情報
- 選手名（またはお子さまの名前）: {player_name}
- 申込プラン: {plan}

## メールに含める内容
1. 申込への感謝と歓迎メッセージ
2. これから何が始まるかの全体像（ワクワク感を持たせる）
3. 次のステップ（プレー動画撮影ガイドを送る旨）
4. 酒本先生からの一言（手書き感のある温かいメッセージ）
5. 連絡先・よくある質問リンク

## トーン
- 選手本人と保護者の両方が読む想定
- 「プレーコンサルティングの第一歩」という期待感
- 不安を取り除く安心感
"""
        result = self.think(prompt)
        self.save_output(result, "ops", f"welcome_email_{player_name[:10]}.md")
        return result

    def write_video_guide(self) -> str:
        self.log("プレー動画撮影ガイド作成")
        prompt = f"""IDP参加者へのプレー動画撮影ガイドを作成してください。

## 目的
{PRESENTER}先生が正確な個人分析を行うために、
参加者が適切な角度・場面で動画を撮影・提出できるようにする。

## ガイドに含める内容
1. 撮影が必要な場面の種類（試合・練習・自主練）
2. 各場面での撮影角度・距離の指定（図解の説明文）
3. スマホでOKな最低画質・時間の目安
4. 提出方法（Google Drive / LINE / メール）
5. 撮影NGパターンと失敗例
6. よくある質問と回答

## トーン
- 初めての人でも迷わない、具体的なステップ形式
- 「撮れなかった」を防ぐ、ハードルを下げる設計
- ポジティブな表現（「これだけで十分です」等）
"""
        result = self.think(prompt)
        self.save_output(result, "ops", "video_shooting_guide.md")
        return result

    def write_analysis_report_template(self) -> str:
        self.log("分析レポートテンプレート作成")
        prompt = f"""IDP個人分析レポートのテンプレートを作成してください。

## 目的
{PRESENTER}先生が各選手のプレー動画を見て記入し、
選手・保護者に提供する公式分析レポート。

## レポートの構成
1. 選手プロフィール（ポジション・年代・目標）
2. 分析サマリー（3行で要約）
3. 強み分析（3点、具体的な場面付き）
4. 改善ポイント（優先度順に3点）
5. 今後3ヶ月の成長設計（月別マイルストーン）
6. {PRESENTER}先生からのメッセージ
7. 次回チェックインの日程

## 品質基準
- 「なんとなく頑張れ」は絶対NG
- 具体的な場面・数値・行動を伴う記述
- 選手が一人でも読んで理解できる表現
- 保護者が読んでも納得できる根拠
"""
        result = self.think(prompt)
        self.save_output(result, "ops", "analysis_report_template.md")
        return result

    def write_graduation_criteria(self) -> str:
        self.log("3ヶ月修了審査基準作成")
        prompt = f"""IDP（3ヶ月個人分析プログラム）の修了審査基準を作成してください。

## 審査の目的
3ヶ月間のIDP参加を経て、選手の成長を客観的に評価し、
次のステップ（継続・IDC参加・修了）を判定する。

## 審査基準（以下を詳細に設計してください）

### 技術・戦術評価（40点）
- 初回分析で設定した改善ポイントの達成度
- 強みの再現性の向上
- 新たな課題の自己認識度

### 行動・習慣評価（30点）
- 自主分析の習慣化（動画振り返り頻度等）
- 課題への取り組み姿勢
- チェックインの参加率・質

### 成長実感・言語化評価（30点）
- 自分のプレーを言語化できるか
- Before/Afterを自分で説明できるか
- 次の3ヶ月の目標を設定できるか

## 審査結果の3パターン
1. **修了（推薦状付き）**: 90点以上 → セレクション推薦状を発行
2. **修了（継続推薦）**: 70〜89点 → 継続プランを提案
3. **延長（要フォロー）**: 69点以下 → 1ヶ月延長フォロー

## 審査結果通達メールのテンプレートも3パターン作成してください。
"""
        result = self.think(prompt)
        self.save_output(result, "ops", "graduation_criteria.md")
        return result

    def write_monthly_checkin(self, month: int, player_name: str = "選手名") -> str:
        self.log(f"月次チェックイン（{month}ヶ月目）作成: {player_name}")
        prompt = f"""IDP参加{month}ヶ月目の月次チェックインメールを作成してください。

## 対象
- 選手名: {player_name}
- 時期: 参加{month}ヶ月目

## メールの目的
- 成長の確認と可視化
- 次の1ヶ月の方向性の確認
- モチベーションの維持・向上
- 酒本先生との接点を保つ

## 含める内容
1. {month}ヶ月目を迎えたことへの言葉
2. この1ヶ月で特に確認したいポイント（質問形式）
3. 動画提出のリマインダー（あれば）
4. 酒本先生からのミニアドバイス（季節・大会に合わせた内容）
5. 次回チェックインの案内

## トーン
- 「管理されている感」ではなく「寄り添っている感」
- 短く読める（スマホで1スクロール以内）
"""
        result = self.think(prompt)
        self.save_output(result, "ops", f"checkin_month{month}_{player_name[:10]}.md")
        return result

    def write_crm_template(self) -> str:
        self.log("顧客管理テンプレート作成")
        prompt = f"""IDP会員の顧客管理シート（CRM）のテンプレートを作成してください。

## 管理する情報
1. 基本情報（名前・年齢・ポジション・所属チーム・保護者連絡先）
2. 申込情報（プラン・申込日・決済状況）
3. 動画提出状況（提出日・本数・品質評価）
4. 分析進捗（初回分析・月次チェックイン状況）
5. 成長記録（月別の定性・定量評価）
6. 修了審査結果
7. アップセル・継続状況（IDC参加・継続IDP）
8. SNS・紹介元（流入経路）

## スプレッドシート形式で列設計してください
- 各列の名前
- データ型（テキスト・数値・日付・選択肢）
- 選択肢の場合はその選択肢リスト
- 備考欄の活用方法

## 管理フローも含めてください
- 申込時に記入する項目
- 毎月更新する項目
- 修了時に記入する項目
"""
        result = self.think(prompt)
        self.save_output(result, "ops", "crm_template.md")
        return result
