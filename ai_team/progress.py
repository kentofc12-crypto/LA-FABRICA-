#!/usr/bin/env python3
"""
LA-FABRICA AIチーム 進捗ダッシュボード

使い方: python ai_team/progress.py
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

OUTPUT_DIR = Path(__file__).parent / "output"


def count_files(subdir: str, pattern: str = "*.md") -> list[Path]:
    d = OUTPUT_DIR / subdir
    if not d.exists():
        return []
    return sorted(d.glob(pattern))


def show_dashboard():
    print("""
╔══════════════════════════════════════════════════════════════╗
║      LA-FABRICA AIチーム 進捗ダッシュボード                  ║
║      サッカー選手育成工場「ラ・ファブリカ」                   ║
╚══════════════════════════════════════════════════════════════╝
""")
    print(f"  確認日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n")

    # ── 生成コンテンツ ──────────────────────────────────
    scripts = count_files("scripts")
    articles = count_files("articles")
    research = count_files("research")
    newsletters = count_files("newsletters")

    script_files = [f for f in scripts if f.name.startswith("2") and "script_" in f.name]
    shorts_files = [f for f in scripts if "shorts_" in f.name]
    plan_files   = [f for f in scripts if "weekly_plans" in f.name]
    review_files = [f for f in scripts if "quality_review" in f.name]
    article_files = [f for f in articles if "article_" in f.name]
    nl_files     = [f for f in newsletters if "newsletter_" in f.name]

    print("  ┌─────────────────────────────────────────────┐")
    print("  │  生成コンテンツ（累計）                       │")
    print("  ├─────────────────────────────────────────────┤")
    print(f"  │  🎬 YouTube台本（長尺）  : {len(script_files):>3} 本              │")
    print(f"  │  📱 Shorts台本          : {len(shorts_files):>3} 本              │")
    print(f"  │  📋 企画書              : {len(plan_files):>3} 本              │")
    print(f"  │  ✅ Project Leaderレビュー: {len(review_files):>3} 件            │")
    print(f"  │  📰 メディア記事         : {len(article_files):>3} 本            │")
    print(f"  │  📬 研究所レター         : {len(nl_files):>3} 通              │")
    print(f"  │  🔍 リサーチレポート      : {len(research):>3} 件              │")
    print("  └─────────────────────────────────────────────┘")

    # ── 5月スプリント進捗 ────────────────────────────────
    MAY_YT_LONG_TARGET  = 4
    MAY_YT_SHORT_TARGET = 16
    MAY_ARTICLE_TARGET  = 20
    MAY_NL_TARGET       = 4

    def bar(done: int, total: int, width: int = 20) -> str:
        filled = int(width * done / total) if total else 0
        pct = int(100 * done / total) if total else 0
        return f"[{'█' * filled}{'░' * (width - filled)}] {done}/{total} ({pct}%)"

    print("\n  ┌─────────────────────────────────────────────┐")
    print("  │  5月スプリント進捗                            │")
    print("  ├─────────────────────────────────────────────┤")
    print(f"  │  YouTube長尺   {bar(len(script_files), MAY_YT_LONG_TARGET)}  │")
    print(f"  │  Shorts        {bar(len(shorts_files), MAY_YT_SHORT_TARGET)}  │")
    print(f"  │  メディア記事  {bar(len(article_files), MAY_ARTICLE_TARGET)}  │")
    print(f"  │  研究所レター  {bar(len(nl_files), MAY_NL_TARGET)}  │")
    print("  └─────────────────────────────────────────────┘")

    # ── 最新生成ファイル ─────────────────────────────────
    all_files = list(OUTPUT_DIR.rglob("*.md"))
    if all_files:
        recent = sorted(all_files, key=lambda f: f.stat().st_mtime, reverse=True)[:5]
        print("\n  ┌─────────────────────────────────────────────┐")
        print("  │  最新の生成ファイル（直近5件）                │")
        print("  ├─────────────────────────────────────────────┤")
        for f in recent:
            mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%m/%d %H:%M")
            name  = f.name[:38]
            print(f"  │  {mtime}  {name:<38}  │")
        print("  └─────────────────────────────────────────────┘")

    # ── 次のアクション ───────────────────────────────────
    print("""
  ┌─────────────────────────────────────────────┐
  │  AIチームを動かすコマンド                     │
  ├─────────────────────────────────────────────┤
  │  YouTube台本1本作る:                         │
  │    python ai_team/main.py --workflow youtube  │
  │                                             │
  │  メディア記事2本作る:                         │
  │    python ai_team/main.py --workflow media    │
  │                                             │
  │  研究所レター作る:                            │
  │    python ai_team/main.py --workflow newsletter│
  │                                             │
  │  全部まとめて:                               │
  │    python ai_team/main.py --workflow all      │
  └─────────────────────────────────────────────┘
""")


if __name__ == "__main__":
    show_dashboard()
