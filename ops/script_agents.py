import os
from ops.llm_factory import get_local_llm

def generate_script(topic: str) -> str:
    print(f"[INFO] Dang tao kich ban cho chu de: {topic}...")
    try:
        llm = get_local_llm()
        prompt = (
            f"Viet mot kich ban video ngan (duoi 60 giay) ve chu de: {topic}.\n"
            f"Viet bang tieng Viet, giong dieu cuon thuat, ro rang, chia thanh cac doan ngan."
        )
        res = llm.invoke(prompt)
        script_content = res.content if hasattr(res, 'content') else str(res)
        print(f"[SUCCESS] Da tao xong kich ban.")
        return script_content
    except Exception as e:
        print(f"[WARNING] Loi khi tao kich ban ({e}), su dung kich ban mau.")
        return f"Chao mung cac ban den voi xu huong moi nhat ve {topic}. Hay cung kham pha ngay hom nay!"

if __name__ == '__main__':
    generate_script("Tri tue nhan tao")
