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
import re
from..db import db


class Reminders(Cog):
  def __init__(self, bot):
    self.bot = bot
    self.set_reminders.start()
    self.check_reminder.start()

  @command(aliases=["start"])
  async def start_reminders(self, ctx):

      author = ctx.message.author.mention
      channel = ctx.channel.id

      ahora = datetime.now()

      await ctx.send(f'Escribe las horas en que quieres recibir los recordatorios en formato 0-24 horas, y separadas por comas sin espacios (ejemplo: 9,12,16,19). Considerar hora actual: {ahora.strftime("%H:%M")}')

      #TESTEO
      # horas = "50, 51, 52, 53, 54"

      ## BORRAR ESTE BLOQUE PARA TESTEAR
      message = await self.bot.wait_for('message', timeout=20, check=lambda message: message.author == ctx.author)

      if "mL" not in message.content or " " not in message.content:
          horas = message.content
          await ctx.send("Te recordaré que tomes agua de ahora en adelante.")

      else:
          await ctx.send("Debes ingresar los números de forma correcta, en formato 0-24, y separados por comas sin espacios (ejemplo: 8,12,15,20,22)")

      await self.set_users(horas, author, channel)

  @command()
  async def bugfix(ctx, self):
      author = "<@728054482533089360>"
      channel = 830443858507989023
      horas = "10,12,15,17,20"

      db.execute("INSERT OR IGNORE INTO users (ReminderAuthor, ReminderChannel, ReminderHours) VALUES (?, ?, ?)", author, channel, horas)
      db.commit()

  async def set_users(self, horas, author, channel):

      db.execute("INSERT OR IGNORE INTO users (ReminderAuthor, ReminderChannel, ReminderHours) VALUES (?, ?, ?)", author, channel, horas)
      db.commit()

  @tasks.loop(seconds=1)
  async def set_reminders(self):

      stored_users = db.column("SELECT ReminderAuthor FROM users")

      now = datetime.now()

      reminderoptions = ["Toma agua, maldita", "Toma awita por favor", "Es hora de que tomes agua zorra", "A tomar aguita", "Anda a tomar agua ahora mismo!!!!", "toma awa uwu", "por favor hidrátate", "no crees que es hora de tomar agua?", "mmm podrías tomar agua", "de las cosas que podrías hacer, tomar agua suena bien", "TOMA AGUA AHORA", "agua? uwu", "yapue y el aguita?", "agua.", "aaguaaaaaa", "my love is like (drinking) wateeeerrrr", "quieres la piel bonita? toma agua", "awa awa awa"]

      for user in stored_users:
          horas = db.record("SELECT ReminderHours FROM users WHERE ReminderAuthor = ?", user)

          horas = horas[0]
          horas = horas.split(",")

          author = db.record("SELECT ReminderAuthor FROM users WHERE ReminderAuthor = ?", user)
          author = str(author[0])

          channel = db.record("SELECT ReminderChannel FROM users WHERE ReminderAuthor = ?", user)

          channel = str(channel[0])

          hours = []

          for hora in horas:
            hora = int(hora)
            horario = now.replace(hour=hora, minute=0, second=0, microsecond=0)
            hours.append(horario)

          for hour in hours:
            reminder_time = hour
            remindertext = random.choice(reminderoptions)

            reminder_id = f'{author}-{reminder_time.strftime("%d/%m %H:%M")}'

            if reminder_time < datetime.now():
                pass

            else:
                db.execute("INSERT OR IGNORE INTO reminders (ReminderTime, ReminderID, ReminderText, ReminderAuthor, ReminderChannel) VALUES (?, ?, ?, ?, ?)", reminder_time, reminder_id, remindertext, author, channel)

                amountdb_date = datetime.now().strftime("%d/%m/%Y")

                db.execute("INSERT OR IGNORE INTO amounts (ReminderDate, ReminderAuthor) VALUES (?, ?)", amountdb_date, author)

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
                print(channel)
                print(type(channel))

                self.channel = self.bot.get_channel(channel)
                print(type(self.channel))

                reminder = await self.channel.send(f"{reminderauthor}: **{remindertext}**")

                await reminder.add_reaction("☑️")

                db.execute("DELETE FROM reminders WHERE ReminderID = ?", reminder_id)

                db.commit()

  @check_reminder.before_loop
  async def before_check(self):
      await self.bot.wait_until_ready()

  @Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.member.bot:
      pass

    else:
      if payload.emoji.name == "☑️":
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        msgcontent = message.content
        user = payload.member

        author = str(re.search("(\d+)", msgcontent)[0])

        if author == str(user.id):
            await self.water_amount(channel, user)

        else:
            pass

  async def water_amount(self, channel, user):

    await channel.send("Cuánta agua tomaste? (escribir solo número en mL)")

    try:
        message = await self.bot.wait_for('message', timeout=20, check=lambda message: message.author == user)

        amount = int(message.content)
        print(amount)

        user = user.mention

        today = datetime.now().strftime("%d/%m/%Y")

        db.execute("UPDATE amounts SET WaterAmount = WaterAmount + ? WHERE ReminderDate = ? AND ReminderAuthor = ?", amount, today, user)

        db.commit()

        await message.add_reaction("🚰")

    except:
        await channel.send("Debes ingresar una cantidad válida! Intenta reaccionando de nuevo.")

  @command(aliases=["total"])
  async def daily(self, ctx):
      today = datetime.now().strftime("%d/%m/%Y")
      author = ctx.message.author.mention
      daily_total = db.record("SELECT WaterAmount FROM amounts WHERE ReminderDate = ? and ReminderAuthor = ?", today, author)
      daily_total = daily_total[0]

      await ctx.send(f"Has tomado {daily_total} mL de agua hoy.")

  @command(aliases=["agregar", "agua"])
  async def add_water(self, ctx, *args):
      today = datetime.now().strftime("%d/%m/%Y")
      author = ctx.message.author.mention
      amount = int(str(''.join(args)))

      db.execute("UPDATE amounts SET WaterAmount = WaterAmount + ? WHERE ReminderDate = ? AND ReminderAuthor = ?", amount, today, author)
      db.commit()

      await ctx.message.add_reaction("🚰")

  @Cog.listener()
  async def on_ready(self):

    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("reminders")

def setup(bot):
  bot.add_cog(Reminders(bot))
