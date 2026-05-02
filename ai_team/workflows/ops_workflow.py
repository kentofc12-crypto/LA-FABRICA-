"""管理部ワークフロー

IDP会員管理に必要な全テンプレートを一括生成する
"""

from ai_team.agents.ops.ops_agent import OpsAgent


def run_ops_setup() -> dict:
    """IDP管理体制のセットアップ（初回1回実行）"""
    print("\n" + "="*60)
    print("🏢 管理部 セットアップ開始")
    print("="*60 + "\n")

    agent = OpsAgent()
    outputs = {}

    print("📹 動画撮影ガイド作成中...")
    outputs["video_guide"] = agent.write_video_guide()

    print("📋 分析レポートテンプレート作成中...")
    outputs["report_template"] = agent.write_analysis_report_template()

    print("🎓 修了審査基準作成中...")
    outputs["graduation_criteria"] = agent.write_graduation_criteria()

    print("📊 顧客管理テンプレート作成中...")
    outputs["crm"] = agent.write_crm_template()

    print("📧 ウェルカムメール作成中...")
    outputs["welcome"] = agent.write_welcome_email()

    print("📅 月次チェックイン作成中（1・2・3ヶ月目）...")
    outputs["checkin_m1"] = agent.write_monthly_checkin(1)
    outputs["checkin_m2"] = agent.write_monthly_checkin(2)
    outputs["checkin_m3"] = agent.write_monthly_checkin(3)

    print("\n" + "="*60)
    print("✅ 管理部セットアップ完了")
    print("   ai_team/output/ops/ に全テンプレートを保存しました")
    print("="*60 + "\n")

    return outputs
