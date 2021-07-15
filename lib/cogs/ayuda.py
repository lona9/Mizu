from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed

class Ayuda(Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.remove_command("help")

  @command(aliases=["ayuda"])
  async def help(self, ctx):
      embed = Embed(title="Ayuda")

      fields =[("¡Hola!", "Soy Mizu, un bot diseñado para recordarte que tomes agua y hacer registros de tu consumo de agua durante el día para mejorar tus hábitos. Para usarme, debes usar los siguientes comandos:", False),
      ("\u200B", "**+start:** Comando para iniciar tus registros, donde vas a poder seleccionar las horas en que quieres recibir los recordatorios en formato 0-24 horas, y separadas por comas sin espacios (ejemplo: 9,12,16,19).\nTe enviaré recordatorios todos los días a las horas que elijas, y puedes reaccionar al mensaje de recordatorio cuando hayas tomado agua, y te preguntaré cuánto tomaste para poder registrarlo en tu total diario. Los recordatorios te llegarán en el mismo canal donde enviaste el comando.\n**+reset:** Comando para cambiar tus horas para recibir recordatorios, y el canal donde los recibas.\n**+agregar:** Comando para agregar agua en cualquier momento, debes escribir el monto como número (sin letras), en mL) después del comando (ejemplo: +agregar 200).\n**+total:** Comando para ver tu total diario de agua consumida.\nCada comando te avisará con una reacción o un mensaje si la información se procesó de forma correcta.", False)]

      for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
        embed.set_author(name='mizu', icon_url="https://cdn.discordapp.com/attachments/804445064029798431/864165622739894293/main-qimg-4ea724cecc975a5f50f9738c5c07c1f6-c.jpg")

      await ctx.channel.send(embed=embed)


  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("ayuda")

def setup(bot):
  bot.add_cog(Ayuda(bot))
