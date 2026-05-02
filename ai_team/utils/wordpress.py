"""
WordPress REST API 連携ユーティリティ

生成した記事をmedia.lafabrica.jpの下書きとして自動保存する。

必要な設定（.envに記載）:
  WP_URL=https://media.lafabrica.jp
  WP_USER=ユーザー名
  WP_APP_PASSWORD=アプリケーションパスワード（スペースなし）

WordPressのアプリケーションパスワード取得方法:
  WordPress管理画面 → ユーザー → プロフィール
  → 「アプリケーションパスワード」→ 名前を入力して「新しいアプリケーションパスワードを追加」
"""

import os
import re
import sys
from pathlib import Path

# .env 読み込み
_env_file = Path(__file__).parent.parent.parent / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def _get_wp_config() -> tuple[str, str, str]:
    url = os.environ.get("WP_URL", "https://media.lafabrica.jp")
    user = os.environ.get("WP_USER", "")
    password = os.environ.get("WP_APP_PASSWORD", "")
    if not user or not password:
        print("\n❌ WordPress認証情報が見つかりません。")
        print(".envファイルに以下を追加してください:")
        print("  WP_USER=ユーザー名")
        print("  WP_APP_PASSWORD=アプリケーションパスワード")
        sys.exit(1)
    return url, user, password


def _parse_article(content: str) -> dict:
    """マークダウン記事からタイトル・本文・カテゴリを抽出する"""
    lines = content.strip().splitlines()

    # タイトル（最初の # 行）
    title = "（タイトル未設定）"
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            break

    # カテゴリ推定
    category_map = {
        "戦術": "分析・戦術",
        "ポジション": "分析・戦術",
        "分析": "分析・戦術",
        "エビデンス": "エビデンス",
        "科学": "エビデンス",
        "データ": "エビデンス",
        "プレーコンサルティング": "サービス紹介",
        "IDP": "サービス紹介",
        "IDC": "サービス紹介",
    }
    category = "育成・選手向け"
    for keyword, cat in category_map.items():
        if keyword in title or keyword in content[:200]:
            category = cat
            break

    # 抜粋（リード文：最初の200字程度）
    body_lines = [l for l in lines if not l.startswith("# ") and l.strip()]
    excerpt = " ".join(body_lines[:3])[:200] if body_lines else ""

    # HTML変換（簡易版：## → h2, **text** → <strong>text</strong>）
    html = _markdown_to_html(content)

    return {
        "title": title,
        "category": category,
        "excerpt": excerpt,
        "html": html,
    }


def _markdown_to_html(md: str) -> str:
    """最低限のMarkdown→HTML変換"""
    lines = []
    in_code = False
    for line in md.splitlines():
        if line.startswith("```"):
            in_code = not in_code
            lines.append("<pre><code>" if in_code else "</code></pre>")
            continue
        if in_code:
            lines.append(line)
            continue
        if line.startswith("# "):
            lines.append(f"<h1>{line[2:].strip()}</h1>")
        elif line.startswith("## "):
            lines.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("### "):
            lines.append(f"<h3>{line[4:].strip()}</h3>")
        elif line.startswith("- ") or line.startswith("* "):
            lines.append(f"<li>{line[2:].strip()}</li>")
        elif line.startswith("| "):
            # テーブルは簡易スキップ
            lines.append(line)
        elif line.strip() == "---":
            lines.append("<hr>")
        elif line.strip() == "":
            lines.append("<br>")
        else:
            # **bold** と *italic*
            line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
            line = re.sub(r"\*(.+?)\*", r"<em>\1</em>", line)
            lines.append(f"<p>{line}</p>")
    return "\n".join(lines)


def post_as_draft(content: str, tags: list[str] | None = None) -> dict:
    """
    記事をWordPressの下書きとして投稿する。

    Returns:
        dict: {"success": bool, "post_id": int, "edit_url": str, "title": str}
    """
    try:
        import requests
    except ImportError:
        print("❌ requestsライブラリが必要です: pip install requests")
        return {"success": False, "error": "requests not installed"}

    wp_url, wp_user, wp_password = _get_wp_config()
    parsed = _parse_article(content)

    payload = {
        "title": parsed["title"],
        "content": parsed["html"],
        "status": "draft",          # ← 下書き保存
        "excerpt": parsed["excerpt"],
        "format": "standard",
    }

    if tags:
        payload["tags"] = tags

    try:
        resp = requests.post(
            f"{wp_url}/wp-json/wp/v2/posts",
            json=payload,
            auth=(wp_user, wp_password),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        post_id = data.get("id")
        edit_url = f"{wp_url}/wp-admin/post.php?post={post_id}&action=edit"

        print(f"  ✅ WordPress下書き保存完了")
        print(f"     タイトル: {parsed['title']}")
        print(f"     編集URL: {edit_url}")

        return {
            "success": True,
            "post_id": post_id,
            "edit_url": edit_url,
            "title": parsed["title"],
        }

    except Exception as e:
        print(f"  ❌ WordPress投稿エラー: {e}")
        return {"success": False, "error": str(e)}


def list_drafts() -> list[dict]:
    """WordPress上の下書き一覧を取得する"""
    try:
        import requests
    except ImportError:
        return []

    wp_url, wp_user, wp_password = _get_wp_config()

    try:
        resp = requests.get(
            f"{wp_url}/wp-json/wp/v2/posts",
            params={"status": "draft", "per_page": 50},
            auth=(wp_user, wp_password),
            timeout=30,
        )
        resp.raise_for_status()
        posts = resp.json()
        return [
            {
                "id": p["id"],
                "title": p["title"]["rendered"],
                "edit_url": f"{wp_url}/wp-admin/post.php?post={p['id']}&action=edit",
                "modified": p["modified"],
            }
            for p in posts
        ]
    except Exception as e:
        print(f"下書き取得エラー: {e}")
        return []
