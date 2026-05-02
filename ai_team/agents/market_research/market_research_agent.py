"""
市場リサーチAIエージェント

日本のサッカー育成市場を徹底分析し、
LA FABRICAが先行者利益を取り切るための情報を提供する。
"""

from ai_team.agents.base import BaseAgent, LA_FABRICA_CONTEXT

SYSTEM_PROMPT = f"""あなたはLA-FABRICAの市場リサーチAIエージェントです。

{LA_FABRICA_CONTEXT}

# あなたの役割
日本のサッカー育成市場・競合・顧客心理を深く分析し、
LA FABRICAがIDP会員1000人を達成するための戦略的情報を提供する。

# リサーチの4つの軸

## 1. 市場規模・成長性
- 日本のジュニアサッカー登録人口と市場規模
- サッカースクール・個人コーチ市場の推計
- 「プレーコンサルティング」カテゴリーの潜在市場規模

## 2. 競合分析
- 類似サービスの存在確認（個人指導・育成コンサル等）
- 価格帯・ターゲット・差別化ポイントの比較
- LA FABRICAが勝てるポジションの特定

## 3. 顧客心理分析
- 選手・保護者の購買決定プロセス
- 「IDP申込」の心理的ハードルとその解消方法
- セグメント別の訴求ポイント（U-12保護者 / U-15選手 / 高校生 等）

## 4. チャネル・タイミング分析
- 最も効果的なリーチチャネル（YouTube / SEO / SNS / 口コミ）
- 申込が増えるタイミング（セレクション前・大会後・新学期等）
- 競合が来る前に取るべきアクション

# アウトプット形式
- データ・数字を必ず含める
- 「だから何をすべきか」まで落とす
- LA FABRICAの意思決定に直結する情報のみ出力
"""


class MarketResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="市場リサーチAI",
            role="市場リサーチ部門",
            system_prompt=SYSTEM_PROMPT,
        )

    def analyze_market_size(self) -> str:
        self.log("日本サッカー育成市場の規模を分析中...")
        prompt = """日本のサッカー育成市場を分析してください。

## 分析項目
1. **登録人口データ**
   - 日本サッカー協会の登録選手数（年代別）
   - 推定の非登録・スクール生を含めた実態人口
   - 地域別分布

2. **市場規模の試算**
   - サッカースクール市場（売上規模・店舗数）
   - 個人コーチ・プライベートレッスン市場
   - 育成関連グッズ・DVD・オンライン教材市場
   - 「プレーコンサルティング」カテゴリーの潜在市場規模

3. **成長トレンド**
   - 過去5年のサッカー人口推移
   - 少子化の影響と個人課金化トレンド
   - 保護者の教育投資意欲の変化

4. **LA FABRICAへの示唆**
   - IDP 1000人のリアリティ（市場規模から見た実現可能性）
   - 最も取りやすいセグメントはどこか
   - 今すぐ動くべき理由

数字・データ・具体的な結論まで出してください。
"""
        result = self.think(prompt)
        self.save_output(result, "market_research", "market_size_analysis.md")
        return result

    def analyze_competitors(self) -> str:
        self.log("競合分析中...")
        prompt = """LA FABRICAの競合となりうるサービス・プレイヤーを分析してください。

## 分析対象
1. **直接競合**（個人分析・プレーコンサルティング類似サービス）
2. **間接競合**（個人コーチ・サッカースクール・オンライン指導）
3. **代替品**（YouTube・本・チームコーチに頼る）

## 各競合への分析項目
- サービス内容と価格帯
- ターゲット顧客層
- 強み・弱み
- 認知度・口コミ状況
- LA FABRICAとの差別化ポイント

## 結論として出してほしいこと
- LA FABRICAが「プレーコンサルティング = LA FABRICA」を確立するための
  最重要アクション（競合が強化してくる前にやること）
- 競合が来た時の対抗戦略

現時点で「プレーコンサルティング」という言葉を使っている競合は
ほぼ存在しないという前提で、先行者として何をすべきかを中心に分析してください。
"""
        result = self.think(prompt)
        self.save_output(result, "market_research", "competitor_analysis.md")
        return result

    def analyze_customer_persona(self) -> str:
        self.log("顧客ペルソナ分析中...")
        prompt = """IDP（個人分析プログラム）の購買顧客ペルソナを詳細に設計してください。

## 作成するペルソナ（4種類）

### ペルソナ1: 「セレクション前の焦り保護者」
### ペルソナ2: 「伸び悩みを自覚している中学生選手」
### ペルソナ3: 「我が子に最善を尽くしたい父親」
### ペルソナ4: 「プロを本気で目指す高校生」

## 各ペルソナに含める情報
- 年齢・性別・地域・家族構成
- サッカーとの関わり方
- 毎月のサッカーへの投資額
- 今抱えている最大の悩み（3つ）
- 情報収集の方法（どこで何を見ているか）
- IDPを知るきっかけになりそうな接点
- 申込を決める最後の一押し（何があれば決断するか）
- 申込を躊躇させる心理的ハードル
- ハードルを越えるための言葉・施策

## 結論
- 最初に集中すべきペルソナはどれか
- そのペルソナに最も刺さるコンテンツ・チャネル・メッセージ
"""
        result = self.think(prompt)
        self.save_output(result, "market_research", "customer_persona.md")
        return result

    def analyze_timing_calendar(self) -> str:
        self.log("購買タイミングカレンダー分析中...")
        prompt = """日本のサッカー育成カレンダーに基づいて、
IDP申込が増えるタイミングと施策を月別に設計してください。

## 月別分析（1月〜12月）
各月について:
- この月のサッカーイベント・大会・セレクション
- 選手・保護者の心理状態
- IDP申込の可能性（高/中/低）
- LA FABRICAが打つべき施策
- 配信すべきコンテンツのテーマ

## 特に重要な時期（詳細分析）
- 春セレクション期（3〜5月）
- 夏大会・移籍期（7〜8月）
- 冬セレクション期（10〜11月）
- 年度末・年始（12〜1月）

## 結論
- 今（5月）から12月までの月別申込目標と施策カレンダー
- 「仕込み」と「刈り取り」のタイミング設計
"""
        result = self.think(prompt)
        self.save_output(result, "market_research", "timing_calendar.md")
        return result

    def analyze_channel_strategy(self) -> str:
        self.log("チャネル戦略分析中...")
        prompt = """IDP会員1000人達成のための最適なマーケティングチャネル戦略を分析してください。

## 分析するチャネル
1. YouTube（動画コンテンツ）
2. SEO・メディア（media.lafabrica.jp）
3. Instagram / TikTok（短尺動画・画像）
4. X（Twitter）（情報発信・エンゲージメント）
5. LINE公式アカウント（育成・クロージング）
6. メールマーケティング（研究所レター）
7. PR・メディア露出
8. 口コミ・紹介制度
9. 法人営業（スクール・クラブ）

## 各チャネルの評価
- 到達できる顧客層
- IDP申込への転換率（推定）
- 必要な工数・コスト
- 効果が出るまでの期間
- LA FABRICAとの相性

## 結論
- 今すぐ注力すべき上位3チャネル（理由付き）
- 3ヶ月後に追加すべきチャネル
- 捨てるべきチャネル（コスパが悪いもの）
- チャネル別の月次KPI設定
"""
        result = self.think(prompt)
        self.save_output(result, "market_research", "channel_strategy.md")
        return result

    def run_full_research(self) -> dict:
        """市場リサーチ全項目を一括実行"""
        self.log("フル市場リサーチ開始...")
        return {
            "market_size": self.analyze_market_size(),
            "competitors": self.analyze_competitors(),
            "personas": self.analyze_customer_persona(),
            "timing": self.analyze_timing_calendar(),
            "channels": self.analyze_channel_strategy(),
        }
