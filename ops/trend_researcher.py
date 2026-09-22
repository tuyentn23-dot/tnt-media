import os
from ops.llm_factory import get_local_llm
from ddgs import DDGS

def research_trend(niche: str):
    print(f"[INFO] Bat dau quet trend cho ngach: {niche}...")
    raw_data = []
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"{niche} xu hướng mới nhất 2026", max_results=3))
            for r in results:
                raw_data.append(r.get('body', ''))
        print("[INFO] Da lay du lieu tho tu Internet.")
    except Exception as e:
        print(f"[WARNING] Khong quet duoc internet ({e}), su dung du lieu du phong.")
        raw_data = [f"Xu huong cong nghe AI va tu dong hoa trong ngach {niche} dang phat trien manh me."]

    combined_text = " ".join(raw_data)
    
    print("[INFO] Dang dua du lieu vao Local LLM phan tich...")
    try:
        llm = get_local_llm()
        prompt_text = (
            f"Dua tren thong tin sau: {combined_text[:800]}\n"
            f"Hay tom tat 1 chu de xu huong noi bat nhat trong ngach '{niche}' de lam video YouTube ngan.\n"
            f"Chi tra ve ten chu de hoac tieu de ngan gon, khong dien giai dai dong."
        )
        res = llm.invoke(prompt_text)
        topic = res.content if hasattr(res, 'content') else str(res)
        topic = topic.strip().split('\n')[-1]
        print(f"[SUCCESS] Xac dinh duoc chu de trend: {topic}")
        return topic
    except Exception as e:
        print(f"[ERROR] Loi khi AI phan tich: {e}")
        return f"Tu dong hoa quy trinh voi AI trong {niche}"

if __name__ == "__main__":
    research_trend("Cong nghe AI")
