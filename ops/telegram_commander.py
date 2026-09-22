import os
import logging
import urllib.request
import urllib.parse
import json

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TelegramCommander:
    """
    Hệ thống điều khiển và cảnh báo thời gian thực hai chiều (Two-way Real-time Command & Alert Center)
    giúp AI tự động quản lý kênh 24/7, báo cáo tiến độ và tiếp nhận lệnh từ xa.
    """
    def __init__(self, token=None, chat_id=None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_alert(self, message):
        """
        Gửi thông báo trạng thái hoặc báo cáo lỗi trực tiếp về trung tâm điều hành.
        """
        if self.token == "YOUR_BOT_TOKEN":
            print(f"[Telegram Commander Mock Alert]: {message}")
            return False
            
        try:
            url = f"{self.base_url}/sendMessage"
            data = urllib.parse.urlencode({
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }).encode("utf-8")
            
            req = urllib.request.Request(url, data=data, method="POST")
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("ok", False)
        except Exception as e:
            logging.error(f"Lỗi gửi thông báo Telegram: {e}")
            print(f"[Telegram Error]: {e}")
            return False

    def poll_commands(self):
        """
        Lắng nghe lệnh điều khiển từ xa của người vận hành để tinh chỉnh chu kỳ PDCA realtime.
        """
        if self.token == "YOUR_BOT_TOKEN":
            return []
            
        try:
            url = f"{self.base_url}/getUpdates?offset=-1"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                if result.get("ok"):
                    updates = result.get("result", [])
                    commands = []
                    for update in updates:
                        msg = update.get("message", {}).get("text", "")
                        if msg.startswith("/"):
                            commands.append(msg)
                    return commands
        except Exception as e:
            logging.error(f"Lỗi quét lệnh Telegram: {e}")
        return []

commander = TelegramCommander()
