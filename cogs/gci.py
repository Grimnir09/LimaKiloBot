from datetime import datetime, timedelta
from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.utils import get
import asyncio
import json


class GCI(commands.Cog):

    gci_data = []

    def __init__(self, bot):
        self.bot = bot
        self.check_gci_awake.start()

    @tasks.loop(seconds=5)
    async def check_gci_awake(self):
        for count, gci in enumerate(self.gci_data):
            print(gci["user"])

            d1 = datetime.now()
            d2 = gci["date_to_expire"]

            print(d1, d2)

            if d1 > d2:
                print("Gci is past 10 seconds!")
                self.gci_data.pop(count)
                role = get(gci["user"].guild.roles, name="GCI")
                await gci["user"].remove_roles(role)

    @commands.command(pass_context=True, description="Get server status")
    async def gci(self, ctx, state=None, *, notes=None):

        if not state and not notes:
            gci_status = ""
            for count, gci in enumerate(self.gci_data):
                gci_status = (
                    gci_status + f"{gci['user']}/{gci['user'].nick} - `{gci['notes']}`"
                )
            await ctx.send(gci_status)
            return

        if state.lower() == "sunrise" and ctx.author not in self.gci_data:
            print("gci roll given")
            self.gci_data.append(
                {
                    "user": ctx.author,
                    "date_to_expire": datetime.now() + timedelta(seconds=30),
                    "notes": notes,
                }
            )
            role = get(ctx.guild.roles, name="GCI")
            await ctx.author.add_roles(role)
            await ctx.send(f"{ctx.author.mention} GCI Sunrise, `{notes}`")

        elif state.lower() == "sunset":
            print("gci roll removed")


def setup(bot):
    bot.add_cog(GCI(bot))
