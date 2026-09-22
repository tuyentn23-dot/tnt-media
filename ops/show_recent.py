import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
d = json.load(open("channels/Mialinhcute/published_ledger.json", encoding="utf-8"))
sigs = d.get("signatures", {})
recent = list(sigs.items())[-8:]
for k, v in recent:
 print(v.get("ts"), "| ", v.get("youtube_id"), "| ", k[:60])