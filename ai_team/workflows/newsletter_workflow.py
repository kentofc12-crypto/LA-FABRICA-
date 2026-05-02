"""研究所レター（週次メルマガ）生産ワークフロー"""

from ai_team.agents.newsletter.newsletter import NewsletterAgent
from ai_team.agents.media.funnel import FunnelAgent


def run_newsletter_workflow(
    week_articles: list[str],
    youtube_content: list[str],
    sakamoto_message: str = "",
    announcement: str = "",
    special_topic: str = "",
) -> dict:
    """
    週次研究所レター生産ワークフローを実行する。

    Args:
        week_articles: 今週公開したメディア記事タイトルリスト
        youtube_content: 今週公開したYouTube動画タイトルリスト
        sakamoto_message: 酒本先生から伝えたいこと
        announcement: お知らせ（IDC残枠等）
        special_topic: 特別号の場合はテーマを入力

    Returns:
        dict: 生産したニュースレター
    """
    print("\n" + "="*60)
    print("📬 研究所レター生産ワークフロー 開始")
    print("="*60 + "\n")

    outputs = {}
    newsletter_agent = NewsletterAgent()

    if special_topic:
        print(f"📣 特別号を作成中: {special_topic}")
        newsletter = newsletter_agent.write_special(
            topic=special_topic,
            purpose=announcement or "登録者への価値提供",
        )
        outputs["special_newsletter"] = newsletter
    else:
        print("📝 週次レターを作成中...")
        newsletter = newsletter_agent.write_weekly(
            week_articles=week_articles,
            youtube_content=youtube_content,
            sakamoto_message=sakamoto_message,
            announcement=announcement,
        )
        outputs["weekly_newsletter"] = newsletter

    print("\n" + "="*60)
    print("✅ 研究所レターワークフロー完了")
    print("="*60 + "\n")

    return outputs
