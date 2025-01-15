from flask import Flask, request, jsonify
import requests

app = Flask(jacky_flask)

# 設定你的 LINE 和 Dify API Key
LINE_ACCESS_TOKEN = "YOUR_LINE_ACCESS_TOKEN"
DIFY_API_KEY = "YOUR_DIFY_API_KEY"

def send_line_reply(reply_token, text):
    """回覆 LINE 訊息"""
    headers = {"Authorization": f"Bearer {LINE_ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {"replyToken": reply_token, "messages": [{"type": "text", "text": text}]}
    requests.post("https://api.line.me/v2/bot/message/reply", json=payload, headers=headers)

@app.route("/webhook", methods=["POST"])
def webhook():
    """處理 LINE Webhook 事件"""
    body = request.get_json()
    for event in body["events"]:
        if event["type"] == "message":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]

            # 呼叫 Dify 取得 AI 回應
            dify_response = requests.post(
                "https://api.dify.ai/v1/chat/completions",
                json={"messages": [{"role": "user", "content": user_message}], "stream": False},
                headers={"Authorization": f"Bearer {DIFY_API_KEY}", "Content-Type": "application/json"}
            ).json()

            reply_text = dify_response["choices"][0]["message"]["content"]
            send_line_reply(reply_token, reply_text)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(port=5000)
