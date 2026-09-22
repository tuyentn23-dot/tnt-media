import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ops import channel_loader as ch
from ops import content_freshness as cf
from ops import channel_style as cs
from ops import os_publish
CID = "Mialinhcute"
def main():
    cfg = ch.load(CID)
    style = cfg.get("style", {})
    kinds = cfg.get("content", {}).get("kinds", ["anime","roblox","cute_animals","meme"])
    cf.set_channel(CID)
    os_publish.set_channel(CID)
    picks = []
    for kind in kinds:
        items = ch.load_content(CID, kind)
        fresh = [it for it in items if not cf.is_published(cf.signature(it, kind))]
        picks.extend([(kind, it) for it in fresh[:1]])
    done = 0
    for kind, item in picks[:4]:
        out = os.path.abspath("output/ch" + CID + "_" + item["id"] + "_" + time.strftime("%Y%m%d_%H%M%S") + ".mp4")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        cs.build_styled(item, out, style=style)
        c = cfg.get("content", {})
        title = (item.get("hook") or item["id"])[:100]
        desc = ((item.get("body","") + " " + item.get("payoff",""))[:450])
        tags = list(c.get("tags_base", [])) + [item.get("topic",""), CID]
        topic = "ch" + CID + "_" + kind + "_" + item["id"]
        res = os_publish.publish(out, title, description=desc, tags=tags, privacy="public", topic=topic, category_id=str(c.get("category_id","24")), force=True)
        cf.mark_published(cf.signature(item, kind), {"youtube_id": res.get("youtube_id") if isinstance(res, dict) else None, "topic": topic, "kind": kind, "file": out})
        print("PUBLISHED", kind, item["id"], res.get("youtube_id") if isinstance(res, dict) else res)
        done += 1
    print("DONE", done)
if __name__ == "__main__":
    main()