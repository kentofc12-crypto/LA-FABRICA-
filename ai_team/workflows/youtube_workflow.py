"""YouTube コンテンツ生産ワークフロー

リサーチ → 企画 → 台本 → Project Leaderレビュー の自動フロー
"""

from ai_team.agents.research.domestic import DomesticResearchAgent
from ai_team.agents.research.international import InternationalResearchAgent
from ai_team.agents.youtube.planning import PlanningAgent
from ai_team.agents.youtube.script import ScriptAgent
from ai_team.agents.youtube.project_leader import YouTubeProjectLeader


def run_youtube_workflow(
    additional_context: str = "",
    videos_per_week: int = 1,
) -> dict:
    """
    YouTube週次コンテンツ生産ワークフローを実行する。

    Returns:
        dict: 各ステップの生産物
    """
    print("\n" + "="*60)
    print("🎬 YouTube コンテンツ生産ワークフロー 開始")
    print("="*60 + "\n")

    outputs = {}

    # Step 1: リサーチ
    print("📡 Step 1: マーケットリサーチ")
    domestic_agent = DomesticResearchAgent()
    international_agent = InternationalResearchAgent()

    domestic_topics = domestic_agent.generate_weekly_topics(additional_context)
    international_topics = international_agent.generate_weekly_topics(additional_context)

    outputs["domestic_research"] = domestic_topics
    outputs["international_research"] = international_topics

    # Step 2: 企画
    print("\n📋 Step 2: 企画書作成")
    planning_agent = PlanningAgent()
    plans = planning_agent.create_plan(
        domestic_topics,
        international_topics,
        count=videos_per_week,
    )
    outputs["plans"] = plans

    # Step 3: 台本作成
    print("\n✍️  Step 3: 台本作成")
    script_agent = ScriptAgent()
    scripts = []

    # 企画書から各動画の台本を作成
    for i in range(videos_per_week):
        topic_title = f"動画{i+1}"
        script = script_agent.write_script(plans, topic_title)
        scripts.append(script)

        # Shortsも作成
        script_agent.write_shorts_script(script, topic_title)

    outputs["scripts"] = scripts

    # Step 4: Project Leaderレビュー
    print("\n🔍 Step 4: Project Leaderレビュー")
    pl = YouTubeProjectLeader()
    review = pl.review(plans, scripts)
    outputs["review"] = review

    print("\n" + "="*60)
    print("✅ YouTube ワークフロー完了")
    print("="*60 + "\n")

    return outputs
