import sys, json
sys.path.insert(0, ".")
from ops.youtube_uploader import get_authenticated_service
service = get_authenticated_service()
ch = service.channels().list(part="contentDetails,snippet,statistics", mine=True).execute()
item = ch["items"][0]
uploads = item["contentDetails"]["relatedPlaylists"]["uploads"]
all = []
next = None
while True:
    pl = service.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=next).execute()
    for i in pl["items"]:
        all.append(i["contentDetails"]["videoId"])
    next = pl.get("pageToken")
    if not next:
        break
print("TOTAL:", len(all))
rows = []
for i in range(0, len(all), 50):
    chunk = all[i:i+50]
    stats = service.videos().list(part="snippet,statistics,contentDetails", id=",".join(chunk)).execute()
    for it in stats["items"]:
        rows.append({"tid": it["id"], "title": it["snippet"]["title"], "published": it["snippet"]["publishedAt"], "views": int(it["statistics"].get("viewCount", "0")), "likes": int(it["statistics"].get("likeCount", "0")), "comments": int(it["statistics"].get("commentCount", "0")), "duration": it["contentDetails"].get("duration", "?")})
rows.sort(key=lambda r: r["views"], reverse=True)
with open("analytics/channel_videos.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
print("SAVED:", len(rows))
low = sum(1 for r in rows if r["views"] <= 10)
print("VIDEOS_LESS_10_VIEWS:", low)
high = sum(1 for r in rows if r["views"] >= 1000)
print("VIDEOS_GQ_1K_VIEWS:", high)
for r in rows[:12]:
    print(r["views"], r["title"][:50].encode("ascii", "replace").decode())
