import base64,json
from pathlib import Path
import google.generativeai as genai

MODEL="models/gemini-2.5-flash-image"
ASSET_ROOT=Path("venture_foundry/media/content/assets")

def generate_image(prompt,output_name,api_key):
    if not api_key:
        raise RuntimeError("Missing Gemini credential")
    genai.configure(api_key=api_key)
    response=genai.GenerativeModel(MODEL).generate_content(prompt)
    parts=[]
    for candidate in (getattr(response,"candidates",None) or []):
        content=getattr(candidate,"content",None)
        parts.extend(getattr(content,"parts",None) or [])
    inline_items=[getattr(part,"inline_data",None) for part in parts]
    inline_items=[item for item in inline_items if item is not None and getattr(item,"data",None)]
    if not inline_items:
        raise RuntimeError("No image returned")
    data=inline_items[0].data
    raw=data if isinstance(data,bytes) else base64.b64decode(data)
    out=ASSET_ROOT/output_name
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(raw)
    meta={
        "asset":out.as_posix(),
        "provider":"gemini",
        "model":MODEL,
        "prompt":prompt,
        "publishing_authorized":False
    }
    Path(str(out)+".provenance.json").write_text(
        json.dumps(meta,ensure_ascii=False,indent=2),
        encoding="utf-8"
    )
    return meta
