"""
マーケティング・市場リサーチ ワークフロー

市場分析 → マーケティング施策立案 → SNS・メール・広告コンテンツ生成
"""

from datetime import datetime
from ai_team.agents.market_research.market_research_agent import MarketResearchAgent
from ai_team.agents.marketing.marketing_agent import MarketingAgent


# 月次マーケティングプランのデフォルト申込目標
MONTHLY_IDP_TARGETS = {
    "5月": 10,
    "6月": 17,
    "7月": 25,
    "8月": 75,
    "9月": 100,
    "10月": 200,
    "11月": 200,
    "12月": 400,
}

SNS_THEMES = [
    "練習だけでは上手くならない理由",
    "プレーコンサルティングとは何か",
    "セレクションで落ちる選手の共通点",
    "IDP参加者の変化",
    "自分を知ることが成長の第一歩",
    "世界の育成と日本の育成の差",
    "保護者が知っておくべき育成の真実",
    "酒本先生の正直な話",
]

WEBINAR_THEMES = [
    "プレーコンサルティング入門：自分を知ることから始める育成革命",
    "セレクション前に必ずやるべき個人分析",
    "保護者向け：子どものサッカーに正しく投資する方法",
    "IDP体験会：あなたのプレーを今夜分析します",
]


def run_market_research(full: bool = False) -> dict:
    """市場リサーチを実行する"""
    print("\n" + "="*60)
    print("🔬 市場リサーチ フル稼働開始")
    print("="*60 + "\n")

    agent = MarketResearchAgent()
    outputs = {}

    if full:
        outputs = agent.run_full_research()
    else:
        print("📊 市場規模分析中...")
        outputs["market_size"] = agent.analyze_market_size()
        print("👥 顧客ペルソナ分析中...")
        outputs["personas"] = agent.analyze_customer_persona()
        print("📅 購買タイミング分析中...")
        outputs["timing"] = agent.analyze_timing_calendar()

    print("\n✅ 市場リサーチ完了")
    return outputs


def run_marketing_sprint(month: str | None = None) -> dict:
    """マーケティング施策を一括生成する"""
    month = month or f"{datetime.now().month}月"
    idp_target = MONTHLY_IDP_TARGETS.get(month, 50)

    print("\n" + "="*60)
    print(f"📣 マーケティングチーム フル稼働 [{month}]")
    print(f"   IDP目標: {idp_target}件")
    print("="*60 + "\n")

    agent = MarketingAgent()
    outputs = {}

    print("📅 月次マーケティングプラン作成中...")
    outputs["monthly_plan"] = agent.write_monthly_marketing_plan(month, idp_target)

    print("📱 SNS投稿コンテンツ作成中（全プラットフォーム）...")
    outputs["sns"] = agent.write_sns_posts(SNS_THEMES[0])

    print("📧 ステップメール設計中...")
    outputs["step_email"] = agent.write_step_email_sequence()

    print("🎯 Meta広告コピー作成中...")
    outputs["meta_ad"] = agent.write_ad_copy("Meta（Instagram/Facebook）", "IDP無料相談申込")

    print("🔍 Google広告コピー作成中...")
    outputs["google_ad"] = agent.write_ad_copy("Google検索広告", "研究所レター登録")

    print("🤝 紹介制度設計中...")
    outputs["referral"] = agent.write_referral_program()

    print("🎤 ウェビナー企画作成中...")
    outputs["webinar"] = agent.write_webinar_plan(WEBINAR_THEMES[0])

    print("\n" + "="*60)
    print("✅ マーケティングスプリント完了")
    print("="*60 + "\n")

    return outputs


def run_full_marketing_workflow() -> dict:
    """市場リサーチ → マーケティング施策まで全て実行"""
    print("\n" + "="*60)
    print("🚀 マーケティングチーム × 市場リサーチ フル稼働")
    print("="*60 + "\n")

    research = run_market_research(full=True)
    marketing = run_marketing_sprint()

    return {**research, **marketing}
