import base64
import datetime
import os
import re
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from openai import OpenAI

if not os.environ.get("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY is not set", file=sys.stderr)
    sys.exit(1)

MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2")
OUT_DIR = Path(os.environ.get("MCP_GPT_IMAGE_OUTPUT_DIR", "./generated")).resolve()

client = OpenAI()
mcp = FastMCP("gpt-image")


@mcp.tool()
def generate_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "auto",
    background: str = "auto",
    filename: str | None = None,
) -> str:
    """Generate an image using gpt-image-2 and save it to disk.

    Args:
        prompt: Text description of the image to generate.
        size: Image dimensions. One of 1024x1024, 1024x1536, 1536x1024, auto.
        quality: Render quality. One of low, medium, high, auto.
        background: Background style. One of transparent, opaque, auto.
        filename: Output filename without extension. Auto-generated if omitted.

    Returns:
        Absolute path to the saved PNG file.
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    resp = client.images.generate(
        model=MODEL,
        prompt=prompt,
        size=size,
        quality=quality,
        background=background,
        n=1,
    )

    image_data = resp.data[0]
    b64 = image_data.b64_json

    if filename:
        stem = filename
    else:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", prompt)[:40].strip("_")
        stem = f"{ts}_{slug}"

    path = OUT_DIR / f"{stem}.png"
    path.write_bytes(base64.b64decode(b64))

    result = str(path)
    if getattr(image_data, "revised_prompt", None):
        result += f"\n\nRevised prompt: {image_data.revised_prompt}"
    return result


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
