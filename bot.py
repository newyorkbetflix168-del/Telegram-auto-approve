import os
import time
import requests

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"

offset = 0

print("Telegram Auto Approve Bot started")

while True:
    try:
        response = requests.get(
            f"{API}/getUpdates",
            params={
                "offset": offset,
                "timeout": 50,
                "allowed_updates": '["chat_join_request"]'
            },
            timeout=60
        )

        data = response.json()

        for update in data.get("result", []):
            offset = update["update_id"] + 1

            if "chat_join_request" in update:
                request = update["chat_join_request"]

                chat_id = request["chat"]["id"]
                user_id = request["from"]["id"]

                print("New join request:", user_id)

                # รอ 30 วินาทีก่อนอนุมัติ
                time.sleep(30)

                result = requests.post(
                    f"{API}/approveChatJoinRequest",
                    data={
                        "chat_id": chat_id,
                        "user_id": user_id
                    },
                    timeout=20
                )

                print("Approved:", user_id, result.text)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
