#!/usr/bin/env python3
"""
LA-FABRICA AIチーム 大量コンテンツ生成バッチ

使い方:
  python ai_team/batch.py                        # デフォルト（全テーマ順次）
  python ai_team/batch.py --parallel 3           # 3並列
  python ai_team/batch.py --limit 10             # 10テーマだけ
  python ai_team/batch.py --type youtube         # YouTube台本のみ
  python ai_team/batch.py --type media           # メディア記事のみ
  python ai_team/batch.py --loop                 # テーマを使い切ったらループ（無限生成）
"""

import argparse
import subprocess
import sys
import time
import random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# テーマリスト（YouTube・メディア共用）
# ─────────────────────────────────────────────────────────────

YOUTUBE_THEMES = [
    # ── 認知ステップ1：「練習だけでは上手くならない」問題提起 ──
    "練習しても上手くならない選手に共通する1つの盲点。データで正直に話します",
    "日本のサッカー育成が世界に30年遅れている本当の理由",
    "頑張っているのに試合で活躍できない選手へ。原因は練習量じゃない",
    "週5回練習しても伸びない選手と、週3回でどんどん伸びる選手の違い",
    "コーチに言われたことをやるだけでは上手くなれない科学的な理由",
    "がんばりを量で測る文化の限界。日本のサッカー選手に今すぐ伝えたいこと",
    "Jリーグのスカウトが正直に言っていること。選手選考の本当の基準",
    "なぜ日本の選手は海外に出ると急に活躍できなくなるのか",

    # ── 認知ステップ2：「自分を知ることが最初の一歩」新常識 ──
    "上手くなる選手が練習前に必ずやっていること。97%の選手がやっていない習慣",
    "自分の本当の弱点は自分では気づけない理由。プレー分析の科学",
    "プレーコンサルティングとは何か。日本初のサッカー個人分析の全て",
    "バルセロナのアカデミーが全選手にやらせていること。日本との決定的な差",
    "セレクションで落ちる選手と受かる選手の違いは技術じゃない",
    "自分の強みを言語化できる選手だけが次のステージに行ける理由",
    "勘と感覚で練習している選手に正直に伝えたいこと",
    "世界のトップ選手が個人分析を受け続ける理由を初めて聞いたとき衝撃だった",
    "なぜ今サッカーで「プレーコンサルティング」が必要なのか。5分で全部話します",
    "IDP（個人分析プログラム）を受けると何が変わるのか。全プロセスを公開",

    # ── ポジション・技術特化 ──
    "GKの個人分析。ゴールキーパーに特化したプレーコンサルティングとは",
    "FWが得点を増やすために最初に分析すべきたった1つのこと",
    "MFの選手がポジショニングで損をしている理由と改善の3ステップ",
    "DFの選手が審判に嫌われない守備から、選ばれる守備へ変わる方法",
    "ドリブルが上手いのに試合で使えない選手に欠けていること",
    "パスが正確なのに評価されない選手の盲点",
    "フィジカルに頼りすぎている選手への正直なアドバイス",
    "判断が遅い選手に共通する脳内の癖と、3週間で変える方法",
    "トランジションが遅い選手の本当の原因。走力ではなく認知の問題",

    # ── 年代・シーン特化 ──
    "小学生のうちに絶対身につけておくべきサッカーIQの磨き方",
    "中学生で伸び悩んでいる選手へ。高校でブレイクする選手との差",
    "高校生でレギュラーになれない選手が今すぐやるべきこと",
    "大学サッカーで活躍するために高校時代にやっておくべき個人分析",
    "保護者が子どもの成長を最も邪魔してしまうパターンと解決策",
    "週末しか練習できない選手が平日にやるべき個人分析の方法",
    "スクールに月3万使っても伸びない選手への正直な診断",
    "女子サッカー選手の個人分析。男子と異なる3つの分析視点",
    "社会人サッカーでもっと上手くなりたい人への個人分析活用法",

    # ── 認知ステップ3：LA FABRICAへの行動定着 ──
    "IDP分析を受けた選手が半年でどう変わったか。Before/Afterを正直に話す",
    "セレクションに合格した選手が事前にやっていたたった1つのこと",
    "分析なしで練習し続けることがいかにリスクか。時間と費用の試算",
    "LA FABRICAのIDPとは何か。プレーコンサルティングの全プロセスを公開",
    "無料相談で何を話すのか。IDP初回セッションの全貌を見せます",
    "IDP参加者100人突破。分析してわかった日本の育成の共通課題",

    # ── 保護者向け ──
    "子どもがサッカーで伸び悩んでいる親へ。原因は練習量じゃない可能性",
    "スクールを増やす前にやること。保護者が最初に知るべきプレー分析",
    "子どもの強みを活かした育成法。個人分析で見えた才能の引き出し方",
    "Jアカデミーに入れたい保護者へ。セレクションで本当に見られること",

    # ── 比較・証拠系 ──
    "スペインと日本の育成を10年比べてわかった本質的な差",
    "強豪クラブ出身なのにプロになれない選手と、無名クラブからプロになる選手の違い",
    "身体能力が高いのに試合で活躍できない選手の個人分析をやってみた",
]

MEDIA_THEMES = [
    # ── SEO狙い（検索需要が高いキーワード）──
    "プレーコンサルティングとは何か。日本にまだない概念を徹底解説",
    "サッカーで個人分析が必要な5つの科学的根拠",
    "セレクション合格者の共通点をデータで分析した結果",
    "バルセロナ・アヤックス・ライプツィヒの育成システムと日本の差",
    "練習量より重要なこと。スペインのコーチが言っていた衝撃の一言",
    "ポジション別・個人分析チェックリスト完全版",
    "保護者が知っておくべき子どものプレー分析の見方",
    "U-12で身につけておくべきサッカーIQ向上法",
    "セレクション前にやるべき個人分析3ステップ",
    "日本の育成現場が変わらない本当の理由と解決策",
    "トップ選手が毎試合やっている振り返り方法を公開",
    "プレー映像の正しい見方。感情的分析と構造的分析の違い",
    "強みを伸ばすか弱みを直すか。科学が出した答え",
    "Jリーグアカデミーが求める選手像を元スカウトが解説",
    "個人分析で発見された意外な才能。実例5選",
    "サッカー留学の前にやるべき個人分析とは",
    "オフシーズンの過ごし方で差がつく個人分析活用法",
    "チーム練習だけでは身につかないこと。個人分析の役割",
    "ドリブラー・パサー・ランナー。タイプ別個人分析の違い",
    "試合後48時間の正しい過ごし方。世界標準の振り返り法",
    # ── IDP直接訴求 ──
    "IDP（個人分析プログラム）の全て。料金・内容・流れを完全公開",
    "無料相談で何をするのか。LA FABRICAの初回セッション完全ガイド",
    "IDP参加者の3ヶ月成長記録。数字で見る変化",
    "プレーコンサルティングを受ける前に知っておくべきこと",
    "IDPと普通のコーチングの違い。なぜ個人分析が必要なのか",
    # ── 保護者・法人向け ──
    "子どものサッカーにいくら使っているか。投資対効果を正直に計算する",
    "サッカースクールだけでは足りない理由。個人分析との組み合わせ方",
    "チームに個人分析を導入したコーチの報告。選手の変化を3つ紹介",
    "学校の部活とクラブチーム、どちらが個人分析に向いているか",
    # ── SEO強化キーワード ──
    "サッカー 個人分析 やり方【完全版】プレーコンサルティングの基礎",
    "セレクション 対策 個人分析で合格率を上げる具体的な方法",
    "サッカー 上達しない 原因 プレー分析で見えてくる本当の理由",
    "プレーコンサルティング サッカー 料金 効果 LA FABRICA完全ガイド",
]

# ─────────────────────────────────────────────────────────────

def run_single(workflow: str, message: str, idx: int) -> dict:
    """1本のワークフローを実行して結果を返す"""
    start = time.time()
    label = f"[{idx:03d}] {message[:40]}..."
    print(f"\n🚀 開始: {label}")

    result = subprocess.run(
        [sys.executable, "ai_team/main.py", "--workflow", workflow, "--message", message],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )

    elapsed = time.time() - start
    status = "✅" if result.returncode == 0 else "❌"
    print(f"{status} 完了: {label} ({elapsed:.0f}秒)")

    if result.returncode != 0:
        print(f"   エラー: {result.stderr[-200:]}")

    return {
        "idx": idx,
        "theme": message,
        "workflow": workflow,
        "success": result.returncode == 0,
        "elapsed": elapsed,
    }


def count_outputs() -> dict:
    output_dir = Path(__file__).parent / "output"
    return {
        "台本": len(list((output_dir / "scripts").glob("*script_*.md"))),
        "Shorts": len(list((output_dir / "scripts").glob("*shorts_*.md"))),
        "記事": len(list((output_dir / "articles").glob("*article_*.md"))),
        "レター": len(list((output_dir / "newsletters").glob("*newsletter_*.md"))),
    }


def show_stats(results: list):
    ok = sum(1 for r in results if r["success"])
    ng = len(results) - ok
    avg = sum(r["elapsed"] for r in results) / len(results) if results else 0
    counts = count_outputs()

    print(f"""
╔══════════════════════════════════════════════════╗
║  バッチ完了サマリー  {datetime.now().strftime('%H:%M')}                   ║
╠══════════════════════════════════════════════════╣
║  成功: {ok:>3}  失敗: {ng:>3}  平均: {avg:>4.0f}秒/本            ║
╠══════════════════════════════════════════════════╣
║  累計生成コンテンツ                              ║
║  🎬 YouTube台本: {counts['台本']:>4} 本                          ║
║  📱 Shorts:      {counts['Shorts']:>4} 本                          ║
║  📰 メディア記事: {counts['記事']:>4} 本                          ║
║  📬 研究所レター: {counts['レター']:>4} 通                          ║
╚══════════════════════════════════════════════════╝
""")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parallel", type=int, default=1, help="並列実行数（デフォルト1）")
    parser.add_argument("--limit", type=int, default=None, help="生成本数の上限")
    parser.add_argument("--type", choices=["youtube", "media", "both"], default="both")
    parser.add_argument("--loop", action="store_true", help="テーマを使い切ったらループ（無限生成）")
    parser.add_argument("--shuffle", action="store_true", help="テーマをランダム順で実行")
    args = parser.parse_args()

    # テーマリストを構築
    tasks = []
    if args.type in ("youtube", "both"):
        tasks += [("youtube", t) for t in YOUTUBE_THEMES]
    if args.type in ("media", "both"):
        tasks += [("media", t) for t in MEDIA_THEMES]

    if args.shuffle:
        random.shuffle(tasks)

    if args.loop:
        # 無限ループ：テーマを使い切ったら最初に戻る
        def theme_gen():
            while True:
                pool = tasks.copy()
                if args.shuffle:
                    random.shuffle(pool)
                yield from pool
        theme_iter = theme_gen()
    else:
        theme_iter = iter(tasks)

    limit = args.limit or (None if args.loop else len(tasks))

    print(f"""
╔══════════════════════════════════════════════════╗
║  LA-FABRICA 大量コンテンツ生成バッチ              ║
╠══════════════════════════════════════════════════╣
║  タイプ: {args.type:<8}  並列: {args.parallel}             ║
║  上限: {str(limit) + '本' if limit else '無制限（--loop）':<10}  シャッフル: {'ON' if args.shuffle else 'OFF'}          ║
╚══════════════════════════════════════════════════╝
""")

    results = []
    idx = 1

    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = {}
        batch = []

        for workflow, message in theme_iter:
            if limit and idx > limit:
                break

            future = executor.submit(run_single, workflow, message, idx)
            futures[future] = idx
            idx += 1

            # 並列数を超えたら完了を待つ
            if len(futures) >= args.parallel:
                done = next(as_completed(futures))
                result = done.result()
                results.append(result)
                del futures[done]

                # 中間サマリー（10本ごと）
                if len(results) % 10 == 0:
                    show_stats(results)

        # 残りを完了
        for future in as_completed(futures):
            results.append(future.result())

    show_stats(results)


if __name__ == "__main__":
    main()
