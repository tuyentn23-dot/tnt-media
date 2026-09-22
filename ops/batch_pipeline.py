# batch_pipeline.py
import os
import sys
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from ops.publish_one import upload, record

def calculate_viral_score(topic, title):
    score = 75
    if "99%" in title or "Sự thật" in title or "bất ngờ" in title or "nga ngua" in title:
        score += 10
    if "trending" in title or "bùng nổ" in title or "internet" in title:
        score += 10
    return min(score, 99)

def generate_viral_metadata(topic):
    hooks = [
        "Su that nga ngua ve " + topic + " ban chua tung biet",
        "99% nguoi xem se bat ngo voi " + topic + " nay",
        "Khoanh khac " + topic + " khien internet bung no",
        "Day la ly do " + topic + " dang trending"
    ]
    tags_pool = ["xuhuong", "viral", "foryou", "fyp", "khampha", "thuvu", "bimat"]
    title = random.choice(hooks)
    viral_score = calculate_viral_score(topic, title)
    
    selected_tags = random.sample(tags_pool, min(3, len(tags_pool)))
    selected_tags.append(topic.replace(" ", ""))
    selected_tags.append("shorts")
    
    nl = chr(10)
    desc = title + nl + nl + "Cung kham pha nhung dieu thu vi nhat ve " + topic + ". Nho dang ky kenh de xem them nhe!" + nl + "#" + " #".join(selected_tags)
    return title, desc, selected_tags, viral_score

def run_batch():
    print("=== PIPELINE: RENDER -> SCORE -> PUBLISH ===")
    topics = ["Cong nghe AI", "Kien truc sang tao", "Kham pha the gioi"]
    for topic in topics:
        title, desc, tags, score = generate_viral_metadata(topic)
        print("Topic: " + topic + " | Score: " + str(score) + " | Title: " + title)
        video_filename = "output_" + topic.lower().replace(' ', '_') + ".mp4"
        print("-> Rendering video: " + video_filename)
        
        if score >= 75:
            print("-> Score dat chuan (" + str(score) + "). Tien hanh Publish...")
            video_id = upload(video_filename, title, desc, tags)
            meta = {
                "topic": topic,
                "title": title,
                "video_id": video_id,
                "score": score,
                "status": "published"
            }
            record(meta)
            print("-> Thanh cong! Published ID: " + str(video_id))
        else:
            print("-> Score chua dat, tam giu lai.")

if __name__ == '__main__':
    run_batch()
