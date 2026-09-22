# title_optimizer.py - generate viral titles + hashtags from proven patterns
import json,random
PATTERNS=[
    {"p":"Dieu gi xay ra neu {x}?","t":"whatif"},
    {"p":"Su that giat minh ve {x}","t":"fact"},
    {"p":"{x} - Ban co tin noi?","t":"shock"},
    {"p":"Toi da kham pha ra {x}","t":"story"},
]
def make(keyword,kind="whatif"):
    p=[x for x in PATTERNS if x["t"]==kind][0]["p"]
    return p.replace("{x}",keyword)+" #shorts"
def hashtags(topic):
    m={"space":["#space","#universe","#facts"],"animal":["#animals","#nature","#facts"],"psychology":["#psychology","#mind","#facts"],"ocean":["#ocean","#sea","#facts"],"body":["#health","#body","#facts"]}
    return " ".join(m.get(topic,["#facts"])+["#shorts"])
if __name__ == "__main__":
    print(make("ban roi vao ho den"))
    print(hashtags("space"))
