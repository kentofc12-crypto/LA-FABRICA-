#!/usr/bin/env python3
"""
LA-FABRICA AIチーム メインランナー

使い方:
  python main.py                      # 今日の曜日に応じたワークフロー実行
  python main.py --workflow youtube   # YouTubeワークフローのみ実行
  python main.py --workflow media     # メディア記事ワークフローのみ実行
  python main.py --workflow newsletter # 研究所レターのみ実行
  python main.py --workflow all       # 全ワークフロー実行
  python main.py --workflow research  # リサーチのみ実行
"""

import argparse
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    parser = argparse.ArgumentParser(
        description="LA-FABRICA AIチーム コンテンツ生産システム"
    )
    parser.add_argument(
        "--workflow",
        choices=["youtube", "media", "newsletter", "all", "research", "daily", "pr", "ops", "marketing", "market-research"],
        default="daily",
        help="実行するワークフロー (default: daily)",
    )
    parser.add_argument(
        "--message",
        type=str,
        default="",
        help="酒本先生からのメッセージ（今週伝えたいこと）",
    )
    parser.add_argument(
        "--announcement",
        type=str,
        default="",
        help="お知らせ（IDC残枠・イベント等）",
    )
    parser.add_argument(
        "--articles",
        type=int,
        default=2,
        help="メディア記事の本数 (default: 2)",
    )
    parser.add_argument(
        "--videos",
        type=int,
        default=1,
        help="YouTube動画の本数 (default: 1)",
    )

    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════════════╗
║          LA-FABRICA AIチーム 稼働開始                ║
║   YouTube部署 / メディア部署 / リサーチ部署          ║
╚══════════════════════════════════════════════════════╝
    """)

    if args.workflow == "daily":
        from ai_team.workflows.daily import run_daily
        run_daily(
            sakamoto_message=args.message,
            announcement=args.announcement,
        )

    elif args.workflow == "all":
        from ai_team.workflows.daily import run_daily
        run_daily(
            sakamoto_message=args.message,
            announcement=args.announcement,
            force_workflow="all",
        )

    elif args.workflow == "youtube":
        from ai_team.workflows.youtube_workflow import run_youtube_workflow
        run_youtube_workflow(
            additional_context=args.message,
            videos_per_week=args.videos,
        )

    elif args.workflow == "media":
        from ai_team.workflows.media_workflow import run_media_workflow
        run_media_workflow(
            articles_per_week=args.articles,
            additional_context=args.message,
        )

    elif args.workflow == "newsletter":
        from ai_team.workflows.newsletter_workflow import run_newsletter_workflow
        run_newsletter_workflow(
            week_articles=["最新記事"],
            youtube_content=["最新動画"],
            sakamoto_message=args.message,
            announcement=args.announcement,
        )

    elif args.workflow == "research":
        from ai_team.agents.research.domestic import DomesticResearchAgent
        from ai_team.agents.research.international import InternationalResearchAgent
        DomesticResearchAgent().generate_weekly_topics(args.message)
        InternationalResearchAgent().generate_weekly_topics(args.message)

    elif args.workflow == "pr":
        from ai_team.workflows.pr_workflow import run_pr_workflow
        run_pr_workflow(additional_context=args.message)

    elif args.workflow == "ops":
        from ai_team.workflows.ops_workflow import run_ops_setup
        run_ops_setup()

    elif args.workflow == "marketing":
        from ai_team.workflows.marketing_workflow import run_marketing_sprint
        run_marketing_sprint()

    elif args.workflow == "market-research":
        from ai_team.workflows.marketing_workflow import run_market_research
        run_market_research(full=True)

    print("\n🏁 LA-FABRICA AIチーム 稼働終了")
    print("📁 生成物は ai_team/output/ に保存されました")


if __name__ == "__main__":
    main()
