import anthropic
import json
from datetime import datetime
from pathlib import Path

MODEL = "claude-sonnet-4-6"


class BaseAgent:
    """全AIエージェントの基底クラス"""

    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.client = anthropic.Anthropic()
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
