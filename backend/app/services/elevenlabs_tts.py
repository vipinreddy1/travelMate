from __future__ import annotations

from pathlib import Path
import re
from typing import Final

import httpx

from app.core.config import get_settings


DEFAULT_OUTPUT_DIR: Final[Path] = Path("generated_audio")


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "audio"


async def elevenlabsTTS(text: str, output_path: str | Path | None = None) -> Path:
    settings = get_settings()
    api_key = settings.elevenlabs_api_key_value
    if not api_key:
        raise ValueError(
            "ELEVENLABS_API_KEY is not configured. Add it to your .env file before calling elevenlabsTTS()."
        )

    target_path = Path(output_path) if output_path is not None else DEFAULT_OUTPUT_DIR / f"{_slugify(text)}.mp3"
    target_path.parent.mkdir(parents=True, exist_ok=True)

    url = f"{settings.elevenlabs_base_url}/text-to-speech/{settings.elevenlabs_voice_id}"
    payload = {
        "text": text,
        "model_id": settings.elevenlabs_model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }
    headers = {
        "xi-api-key": api_key,
        "accept": "audio/mpeg",
        "content-type": "application/json",
    }

    timeout = httpx.Timeout(settings.elevenlabs_request_timeout_seconds)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.is_error:
        raise RuntimeError(
            f"ElevenLabs request failed with {response.status_code}: {response.text}"
        )

    target_path.write_bytes(response.content)
    return target_path




# Example usage:
# async def main() -> None:
#     input_path = Path("temp_tts_input.txt")
#     text = input_path.read_text(encoding="utf-8").strip()
#     output_path = Path("temp_output") / "temp_tts_test.mp3"

#     generated_path = await elevenlabsTTS(text, output_path=output_path)
#     print(f"Generated audio: {generated_path.resolve()}")