"""
365日稼働スケジューラー

曜日別に適切なワークフローを自動実行する。
"""

from datetime import datetime
from ai_team.agents.coo import COOAgent
from ai_team.workflows.youtube_workflow import run_youtube_workflow
from ai_team.workflows.media_workflow import run_media_workflow
from ai_team.workflows.newsletter_workflow import run_newsletter_workflow


def run_daily(
    sakamoto_message: str = "",
    announcement: str = "",
    force_workflow: str | None = None,
) -> dict:
    """
    今日の曜日に応じたワークフローを実行する。

    Args:
        sakamoto_message: 酒本先生からの今週のメッセージ
        announcement: 今週のお知らせ（IDC残枠等）
        force_workflow: 曜日に関係なく特定のWFを実行（"youtube"/"media"/"newsletter"/"all"）
    """
    today = datetime.now()
    weekday = today.weekday()  # 0=月, 1=火, ..., 6=日
    weekday_names = ["月曜", "火曜", "水曜", "木曜", "金曜", "土曜", "日曜"]

    print(f"\n🗓️  LA-FABRICA AIチーム稼働 | {today.strftime('%Y年%m月%d日')} ({weekday_names[weekday]})")
    print("="*60)

    outputs = {}
    coo = COOAgent()

    if force_workflow == "all" or (force_workflow is None and weekday == 0):
        # 月曜: COOブリーフィング + リサーチ起動
        print("\n📌 月曜タスク: COOブリーフィング + リサーチ")
        from ai_team.agents.research.domestic import DomesticResearchAgent
        from ai_team.agents.research.international import InternationalResearchAgent

        domestic = DomesticResearchAgent().generate_weekly_topics()
        international = InternationalResearchAgent().generate_weekly_topics()

        brief = coo.create_weekly_brief(domestic, international)
        outputs["coo_brief"] = brief
        outputs["domestic_research"] = domestic
        outputs["international_research"] = international

    if force_workflow in ("youtube", "all") or (force_workflow is None and weekday == 0):
        # 月曜 or 強制: YouTube企画・台本
        print("\n🎬 YouTube ワークフロー実行")
        yt_outputs = run_youtube_workflow(
            additional_context=sakamoto_message,
            videos_per_week=1,
        )
        outputs.update({f"yt_{k}": v for k, v in yt_outputs.items()})

    if force_workflow in ("media", "all") or (force_workflow is None and weekday == 0):
        # 月曜 or 強制: メディア記事
        print("\n📰 メディア記事ワークフロー実行")
        existing_research = {
            "domestic_research": outputs.get("domestic_research", ""),
            "international_research": outputs.get("international_research", ""),
        }
        media_outputs = run_media_workflow(
            articles_per_week=2,
            existing_research=existing_research if existing_research["domestic_research"] else None,
        )
        outputs.update({f"media_{k}": v for k, v in media_outputs.items()})

    if force_workflow in ("newsletter", "all") or (force_workflow is None and weekday == 4):
        # 金曜 or 強制: 研究所レター
        print("\n📬 研究所レターワークフロー実行")
        nl_outputs = run_newsletter_workflow(
            week_articles=["今週公開した記事"],
            youtube_content=["今週公開したYouTube動画"],
            sakamoto_message=sakamoto_message,
            announcement=announcement,
        )
        outputs.update(nl_outputs)

    # COO週次レポート（金曜のみ）
    if force_workflow == "all" or (force_workflow is None and weekday == 4):
        print("\n📊 COO週次レポート作成")
        report = coo.review_weekly_output(
            {k: str(v)[:500] for k, v in outputs.items()}
        )
        outputs["coo_report"] = report

    print("\n✅ 本日の稼働完了")
    return outputs
