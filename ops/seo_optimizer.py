import os
import json
from langchain_core.prompts import PromptTemplate
from ops.llm_factory import get_local_llm

def optimize_seo(topic: str, script_content: str):
    print("[INFO] Bat dau toi ưu hoa SEO voi Local LLM...")
    try:
        llm = get_local_llm()
        prompt = PromptTemplate.from_template(
            "Dua vao chu de '{topic}' va noi dung: '{script_content}'.
"
            "Tra ve dung dinh dang JSON co cac truong: titles (array), description (string), tags (array), thumbnail_prompt (string).
"
            "Chi tra ve duy nhat JSON."
        )
        chain = prompt | llm
        result = chain.invoke({"topic": topic, "script_content": script_content})
        content = result.content
        if "```json" in content: content = content.split("```json")[1].split("```")[0]
        elif "```" in content: content = content.split("```")[1].split("```")[0]
        return json.loads(content.strip())
    except Exception as e:
        print(f"[ERROR] Loi SEO Local LLM: {e}")
        return {"titles": ["Title"], "description": "Desc", "tags": ["AI"], "thumbnail_prompt": "Prompt"}

if __name__ == '__main__':
    print(optimize_seo("Test", "Content"))
