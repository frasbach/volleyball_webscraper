from signalbot import SignalBot
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
signal_service = os.environ["SIGNAL_SERVICE"]
phone_number = os.environ["PHONE_NUMBER"]
group_id = os.environ["GROUP_ID"]
internal_id = os.environ["GROUP_INTERNAL_ID"]
config = {
  "signal_service": signal_service,
  "phone_number": phone_number,
  "storage": None,
  }
bot = SignalBot(config)
bot.listenGroup(group_id, internal_id)
asyncio.run(bot.send("kxsFKnE4PhUIoWMk4GMsBIkQfSaMYjc06lVSbEr9yf8=", "Hello Flo"))
