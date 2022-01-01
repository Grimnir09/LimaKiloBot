from config import discord_token
import nextcord
from nextcord.ext import commands
import logging

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    print("Lemon Ready")


try:
    bot.load_extension("cogs.server")
    bot.load_extension("cogs.information")
    bot.load_extension("cogs.gci")
    # not really nessesary extentions comment them out if needed.

except commands.errors.ExtensionNotFound as e:
    print(f"No Cog named: {e.name}")


bot.run(discord_token)
