import discord
from dotenv import load_dotenv
from os import getenv
import requests

load_dotenv()

DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = getenv("DISCORD_CHANNEL_ID")
DISCORD_IGNORED_AUTHORS = getenv("DISCORD_IGNORED_AUTHORS", "")

LINE_BOT_TOKEN = getenv("LINE_BOT_TOKEN")
LINE_CHANNEL_ID = getenv("LINE_CHANNEL_ID")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_message(message):

    if str(message.channel.id) != DISCORD_CHANNEL_ID:
        return

    if str(message.author.id) in DISCORD_IGNORED_AUTHORS.split(","):
        print(f"Author {message.author.id} is in the ignore list")
        return
    
    print(f"Realying message from user {message.author.name}: {message.content}")

    url = "https://api.line.me/v2/bot/message/push"
    headers = {"Authorization": f"Bearer {LINE_BOT_TOKEN}"}
    json = {
        "to": LINE_CHANNEL_ID,
        # "messages": [{"type": "text", "text": text}], # For simple text messages
        "messages": [
            {
                "type": "flex",
                "altText": "Message from Discord",
                "contents": {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Discord message",
                                "color": "#eeeeee",
                                "size": "sm",
                            }
                        ],
                        "paddingTop": "sm",
                        "paddingBottom": "sm",
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            # {
                            #     "type": "text",
                            #     "text": "Message from Discord",
                            #     "size": "xxs",
                            # },
                            {
                                "type": "text",
                                "text": message.author.name,
                                "weight": "bold",
                                "size": "sm",
                            },
                            {"type": "text", "text": message.content},
                        ],
                        "paddingTop": "md",
                        "paddingBottom": "md",
                    },
                    "styles": {"header": {"backgroundColor": "#5865F2"}},
                },
            }
        ],
    }

    res = requests.post(url=url, json=json, headers=headers)

    if not res.ok:
        print(res.text)
    else:
        


client.run(DISCORD_BOT_TOKEN)
