from signalbot import SignalBot
from dotenv import load_dotenv
import logging
import os
import asyncio

class MessageBot:
  logging.getLogger().setLevel(logging.INFO)
  logging.getLogger("apscheduler").setLevel(logging.WARNING)

  internal_id = ""
  
  def __init__(self):
    global internal_id
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
    self.bot = SignalBot(config)
    self.bot.listenGroup(group_id, internal_id)

  def sendMessage(self, string: str):  
    print('In Send MESSAGE!!!')
    asyncio.run(self.bot.send(internal_id, string))
