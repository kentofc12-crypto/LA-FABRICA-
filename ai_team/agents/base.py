import anthropic
import os
import sys
from datetime import datetime
from pathlib import Path

MODEL = "claude-sonnet-4-6"

# .env ファイルがあれば読み込む
_env_file = Path(__file__).parent.parent.parent / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

def _make_client() -> anthropic.Anthropic:
    # 1. 明示的なAPIキー（.env or 環境変数）
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if api_key:
        return anthropic.Anthropic(api_key=api_key)

    # 2. Claude Code環境のセッショントークン
    token_file = os.environ.get(
        "CLAUDE_SESSION_INGRESS_TOKEN_FILE",
        "/home/claude/.claude/remote/.session_ingress_token",
    )
    if Path(token_file).exists():
        token = Path(token_file).read_text().strip()
        return anthropic.Anthropic(auth_token=token)

    # 3. どちらもなければガイドを出して終了
    print("\n❌ APIキーが見つかりません。")
    print("プロジェクトルートに .env ファイルを作成してください:")
    print("  ANTHROPIC_API_KEY=sk-ant-xxxxxxxxx")
    sys.exit(1)


class BaseAgent:
    """全AIエージェントの基底クラス"""

    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.client = _make_client()
        self.output_dir = Path(__file__).parent.parent / "output"

    def think(self, user_message: str, context: dict | None = None) -> str:
        """エージェントにメッセージを送り、回答を得る"""
        messages = []

        if context:
            context_text = "\n\n".join(
                f"## {k}\n{v}" for k, v in context.items()
            )
            messages.append({
                "role": "user",
                "content": f"【コンテキスト情報】\n{context_text}\n\n【タスク】\n{user_message}"
            })
        else:
            messages.append({"role": "user", "content": user_message})

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=8096,
            system=[
                {
                    "type": "text",
                    "text": self.system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=messages,
        )

        return response.content[0].text

    def save_output(self, content: str, subdir: str, filename: str) -> Path:
        """生成したコンテンツをファイルに保存"""
        output_path = self.output_dir / subdir
        output_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_path / f"{timestamp}_{filename}"
        filepath.write_text(content, encoding="utf-8")
        print(f"[{self.name}] 保存完了: {filepath}")
        return filepath

    def log(self, message: str):
        print(f"[{self.name} / {self.role}] {message}")
