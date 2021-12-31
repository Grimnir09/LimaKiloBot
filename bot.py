from config import discord_token
import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


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
