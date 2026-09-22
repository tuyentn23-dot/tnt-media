import os
import json
from datetime import datetime
import hashlib

DB_FILE = 'memory/scripts_db.json'

def save_script(topic: str, script_content: str, status: str = 'ready_for_production'):
    print(f'[INFO] Dang luu kich ban vao database: {topic}')
    os.makedirs('memory', exist_ok=True)
    
    db = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try:
                db = json.load(f)
            except Exception:
                db = []
                
    script_id = hashlib.md5((topic + str(datetime.now())).encode('utf-8')).hexdigest()[:8]
    record = {
        'id': script_id,
        'topic': topic,
        'content': script_content,
        'status': status,
        'created_at': datetime.now().isoformat()
    }
    
    db.append(record)
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
        
    print(f'[SUCCESS] Da luu kich ban thanh cong. Script ID: {script_id}')
    return script_id

if __name__ == '__main__':
    print('=== TEST DB MANAGER ===')
    save_script('Test Topic AI', 'Kich ban test mau tu CrewAI...')
