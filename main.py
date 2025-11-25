from fastapi import FastAPI, Request, HTTPException
from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.config import Configuration

app = FastAPI()

# ======== 把你的 token / secret 放這裡 ========
CHANNEL_ACCESS_TOKEN = "+aOlJoyIzihL/lVxDMTpm//93vTXpYfp+l26IKLtiWPiqDGRgGSQJmlGSOVOsLlS1CUI65XsnomqJVhpHmus9d8ZbbjvitGvIgBTGw4DJ44vyvdBfVMnVjGLURhk4lxfsXIE9fvg3X8WVOlapbdKqQdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "748829ed9c6a6eef3af746ae599fc6a3"
# ==========================================

config = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
messaging_api = MessagingApi(configuration=config)
parser = WebhookParser(CHANNEL_SECRET)

@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Line-Signature")

    try:
        events = parser.parse(body.decode("utf-8"), signature)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        # 只處理文字訊息
        if event.type == "message" and event.message.type == "text":
            received_text = event.message.text

            reply_text = f"你說：{received_text}"

            messaging_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )

    return "OK"
