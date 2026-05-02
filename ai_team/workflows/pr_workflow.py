"""PR コンテンツ生産ワークフロー

プレスリリース / アウトリーチメール / キャンペーン / LP / 法人提案書 の自動生成
"""

from ai_team.agents.pr.pr_agent import PRAgent


# ─────────────────────────────────────────────
# キャンペーンカレンダー（自動生成トリガー）
# ─────────────────────────────────────────────
CAMPAIGN_CALENDAR = [
    {
        "name": "パイロット完了記念・初回限定キャンペーン",
        "season": "5月下旬〜6月",
        "target": "U-15〜U-18の向上心のある選手・保護者",
    },
    {
        "name": "夏のセレクション前・緊急個人分析キャンペーン",
        "season": "7〜8月（夏のセレクションシーズン）",
        "target": "セレクション前の選手・保護者",
    },
    {
        "name": "IDP正式ローンチキャンペーン",
        "season": "9月",
        "target": "研究所レター登録者・YouTube視聴者全員",
    },
    {
        "name": "冬のセレクション駆け込みキャンペーン",
        "season": "10〜11月",
        "target": "高校・Jアカデミーセレクション前の選手",
    },
    {
        "name": "年末・1000人達成記念キャンペーン",
        "season": "12月",
        "target": "全ターゲット（年内最終受付）",
    },
]

PRESS_RELEASE_THEMES = [
    ("日本初のサッカープレーコンサルタント誕生：LA FABRICAがIDP正式ローンチ", ""),
    ("プレーコンサルティングでセレクション合格率向上：IDP参加者データ公開", "パイロット参加者5名の成果"),
    ("サッカー育成革命：「練習量より個人分析」という新常識を日本に", ""),
    ("LA FABRICA、IDP会員100人突破：「プレーコンサルティング」市場の先行者に", "累計100人分析完了"),
    ("LA FABRICA、IDP会員1000人突破：日本のサッカー育成を変えた1年", "年間1000人分析達成"),
]

OUTREACH_TARGETS = [
    ("サッカー系YouTubeチャンネル（登録者5万人以上）への対談依頼", ""),
    ("サカイク・ジュニアサッカーNewsへの取材依頼", ""),
    ("Jリーグアカデミーコーチへのプレーコンサルティング紹介", ""),
    ("民間サッカースクールへのIDP法人導入提案", ""),
    ("高校サッカー部顧問への個人分析研修提案", ""),
    ("育成系インフルエンサーへのコラボ提案", ""),
]

B2B_TARGETS = [
    "民間サッカースクール・アカデミー",
    "Jリーグ下部組織・アカデミー",
    "高校サッカー部強豪校",
    "個人コーチ・フリーランスコーチ",
    "保護者コミュニティ・育成団体",
]

LP_TYPES = [
    "IDP（個人分析プログラム）メインLP",
    "無料相談申込みLP",
    "セレクション特化LP",
    "保護者向けLP",
    "法人・スクール向けLP",
]


def run_pr_workflow(pr_type: str = "all", additional_context: str = "") -> dict:
    """
    PR コンテンツ生産ワークフローを実行する。

    pr_type: "press" / "outreach" / "campaign" / "lp" / "b2b" / "all"
    """
    print("\n" + "="*60)
    print("📣 PR コンテンツ生産ワークフロー 開始")
    print("="*60 + "\n")

    agent = PRAgent()
    outputs = {}

    if pr_type in ("press", "all"):
        print("📰 プレスリリース作成中...")
        theme, milestone = PRESS_RELEASE_THEMES[0]
        outputs["press_release"] = agent.write_press_release(theme, milestone)

    if pr_type in ("outreach", "all"):
        print("📧 アウトリーチメール作成中...")
        target_type, target_name = OUTREACH_TARGETS[0]
        outputs["outreach"] = agent.write_outreach_email(target_type, target_name)

    if pr_type in ("campaign", "all"):
        print("🎯 キャンペーン企画作成中...")
        c = CAMPAIGN_CALENDAR[0]
        outputs["campaign"] = agent.write_campaign(c["name"], c["season"], c["target"])

    if pr_type in ("lp", "all"):
        print("🖥️  LPコピー作成中...")
        outputs["lp"] = agent.write_lp_copy(LP_TYPES[0])

    if pr_type in ("b2b", "all"):
        print("🤝 法人提案書作成中...")
        outputs["b2b"] = agent.write_b2b_proposal(B2B_TARGETS[0])

    print("\n" + "="*60)
    print("✅ PR ワークフロー完了")
    print("="*60 + "\n")

    return outputs
