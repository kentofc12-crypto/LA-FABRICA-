"""メディア記事生産ワークフロー

リサーチ → 編集（記事執筆） → SEO最適化 → CTA最適化 の自動フロー
"""

import os
from ai_team.agents.research.domestic import DomesticResearchAgent
from ai_team.agents.research.international import InternationalResearchAgent
from ai_team.agents.media.editorial import EditorialAgent
from ai_team.agents.media.seo import SEOAgent
from ai_team.agents.media.funnel import FunnelAgent


def run_media_workflow(
    articles_per_week: int = 2,
    additional_context: str = "",
    existing_research: dict | None = None,
    post_to_wordpress: bool = True,
) -> dict:
    """
    メディア記事週次生産ワークフローを実行する。

    Args:
        articles_per_week: 今週制作する記事本数
        additional_context: 追加コンテキスト
        existing_research: YouTube WFで既にリサーチ済みの場合は使い回す

    Returns:
        dict: 各ステップの生産物
    """
    print("\n" + "="*60)
    print("📰 メディア記事生産ワークフロー 開始")
    print("="*60 + "\n")

    outputs = {}

    # Step 1: リサーチ（YouTube WFと共有できる場合はスキップ）
    if existing_research:
        print("📡 Step 1: リサーチ（共有データを使用）")
        domestic_topics = existing_research.get("domestic_research", "")
        international_topics = existing_research.get("international_research", "")
    else:
        print("📡 Step 1: マーケットリサーチ")
        domestic_agent = DomesticResearchAgent()
        international_agent = InternationalResearchAgent()
        domestic_topics = domestic_agent.generate_weekly_topics(additional_context)
        international_topics = international_agent.generate_weekly_topics(additional_context)

    outputs["domestic_research"] = domestic_topics
    outputs["international_research"] = international_topics

    # Step 2: 記事執筆
    print("\n✍️  Step 2: 記事執筆")
    editorial_agent = EditorialAgent()
    seo_agent = SEOAgent()
    funnel_agent = FunnelAgent()

    articles = []

    # 各記事の種類を交互に配置（戦術 + 育成）
    article_configs = [
        {
            "type": "戦術分析",
            "keywords": ["サッカー 戦術", "サッカー 分析"],
        },
        {
            "type": "育成・選手向け",
            "keywords": ["サッカー 上手くなる 方法", "サッカー 伸び悩む"],
        },
        {
            "type": "保護者向け",
            "keywords": ["サッカー 育成 親", "子供 サッカー 上達"],
        },
        {
            "type": "エビデンス",
            "keywords": ["サッカー 科学 トレーニング", "スポーツ科学 育成"],
        },
    ]

    for i in range(articles_per_week):
        config = article_configs[i % len(article_configs)]
        topic = f"記事{i+1}（{config['type']}）"

        print(f"\n  記事 {i+1}/{articles_per_week}: {config['type']}")

        # 記事執筆
        article = editorial_agent.write_article(
            topic=f"{domestic_topics[:500]}から選んだ{config['type']}テーマ",
            article_type=config["type"],
            keywords=config["keywords"],
        )

        # SEO最適化
        seo_result = seo_agent.optimize(article, config["keywords"])

        # CTA最適化
        cta_result = funnel_agent.optimize_cta(article, config["type"])

        # WordPress 下書き保存
        wp_result = None
        if post_to_wordpress and os.environ.get("WP_USER") and os.environ.get("WP_APP_PASSWORD"):
            from ai_team.utils.wordpress import post_as_draft
            print(f"  📤 WordPress下書き保存中...")
            wp_result = post_as_draft(article)

        articles.append({
            "type": config["type"],
            "article": article,
            "seo": seo_result,
            "cta": cta_result,
            "wordpress": wp_result,
        })

    outputs["articles"] = articles

    print("\n" + "="*60)
    print("✅ メディア記事ワークフロー完了")
    print("="*60 + "\n")

    return outputs
