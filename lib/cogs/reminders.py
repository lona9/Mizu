from discord.ext.commands import Cog
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import command
import datetime
from datetime import datetime
from datetime import time
import random
import pandas as pd
from discord.ext import tasks
from datetime import timedelta
from discord.utils import get
from..db import db


class Reminders(Cog):
  def __init__(self, bot):
    self.bot = bot
    self.check_reminder.start()

  @command(aliases=["start"])
  async def start_reminders(self, ctx):

      author = ctx.message.author.mention
      channel = ctx.channel.id

      await ctx.send("Te recordaré que tomes agua diariamente de aquí en adelante.")

      self.set_reminders.start(author, channel)

  @tasks.loop(hours = 24)
  async def set_reminders(self, author, channel):

      now = datetime.now()

      hours = [now.replace(hour=16, minute=49, second=20, microsecond=0)]

      reminderoptions = ["Toma agua, maldita", "Toma awita por favor", "Es hora de que tomes agua zorra", "A tomar aguita", "Anda a tomar agua ahora mismo!!!!", "toma awa uwu", "por favor hidrátate", "no crees que es hora de tomar agua?", "mmm podrías tomar agua", "de las cosas que podrías hacer, tomar agua suena bien", "TOMA AGUA AHORA", "agua? uwu"]

      for hour in hours:
        reminder_time = hour
        remindertext = random.choice(reminderoptions)
        rm_id = random.randint(1, 10000)

        db.execute("INSERT OR IGNORE INTO reminders (ReminderID, ReminderTime, ReminderText, ReminderAuthor, ReminderChannel) VALUES (?, ?, ?, ?, ?)", rm_id, reminder_time, remindertext, author, channel)

      db.commit()

  @tasks.loop(seconds = 1)
  async def check_reminder(self):
    stored_reminders = db.column("SELECT ReminderID FROM reminders")

    if stored_reminders == ():
        self.check_reminder.stop()

    else:
        for reminder_id in stored_reminders:
            time_to_check = db.record("SELECT ReminderTime FROM reminders WHERE ReminderID = ?", reminder_id)

            time_to_check = pd.to_datetime(time_to_check)

            if time_to_check > datetime.now():
                continue

            else:
                remindertext = db.record("SELECT ReminderText FROM reminders WHERE ReminderID = ?", reminder_id)

                reminderauthor = db.record("SELECT ReminderAuthor FROM reminders WHERE ReminderID = ?", reminder_id)

                reminderchannel = db.record("SELECT ReminderChannel FROM reminders WHERE ReminderID = ?", reminder_id)

                remindertext = str(remindertext[0])

                reminderauthor = str(reminderauthor[0])

                channel = int(reminderchannel[0])

                channel = self.bot.get_channel(channel)

                reminder = await channel.send(f"{reminderauthor}: **{remindertext}**")

                await reminder.add_reaction("✅")

                db.execute("DELETE FROM reminders WHERE ReminderID = ?", reminder_id)

                db.commit()

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("reminders")

def setup(bot):
  bot.add_cog(Reminders(bot))
