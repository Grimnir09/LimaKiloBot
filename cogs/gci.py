import asyncio
from datetime import datetime, timedelta
from nextcord import SlashOption
from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.utils import get
import nextcord


class GCI(commands.Cog):

    # init vars and task loops
    def __init__(self, bot):
        self.bot = bot
        self.check_gci_awake.start()
        self.gci_data = []

    # if for some reason we crash and start up again
    # remove all gci roles from all guilds
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                role = get(member.guild.roles, name="GCI")
                if role in member.roles:
                    await member.remove_roles(role)

    # task loop that checks our list of dicts for any upcoming events
    # using datetime.
    @tasks.loop(seconds=5)
    async def check_gci_awake(self):
        for count, gci in enumerate(self.gci_data):

            current_date = datetime.now()
            expire_date = gci["date_to_expire"]
            refresh_warning_date = gci["date_refresh_warning"]

            # if expire_date is in the past remove role
            if current_date > expire_date:
                self.gci_data.pop(count)
                role = get(gci["user"].guild.roles, name="GCI")
                await gci["user"].remove_roles(role)

            # if refresh_date is in the past send a refresh warning
            if (
                current_date > refresh_warning_date
                and gci["refresh_warning_sent"] == False
            ):

                await gci["user"].send(
                    f"{gci['user'].mention} this is your 10 minute refresh warning. \n Your GCI session will end in `10 Minutes` \n To refresh your session use `/gci refresh`",
                )

                gci["refresh_warning_sent"] = True

    @nextcord.slash_command(name="gci", description='GCI Related Commands', guild_ids=[358048911144779777, 772617490827313162, 924753029402619924])
    async def gci(self, interaction: nextcord.Interaction,
                  state: str = SlashOption(
                      name='state',
                      choices=['Sunrise', 'Sunset', 'Refresh', 'List'],
                      description='Sunrise: Ready To Rock, Sunset: Heaven or Hell?'
                  ),
                  notes: str = SlashOption(
                      description='Give a short description about what your going to do as a GCI.',
                      default='Monitoring 134.000 AM',
                      required=False
                  )
                  ):

        if state == "Sunrise" and not (any(gci["user"] == interaction.user for gci in self.gci_data)):

            self.gci_data.append(
                {
                    "user": interaction.user,
                    "date_to_expire": datetime.now() + timedelta(hours=1),
                    "date_refresh_warning": datetime.now() + timedelta(minutes=40),
                    "notes": notes,
                    "ctx": interaction,
                    "refresh_warning_sent": False,
                }
            )
            role = get(interaction.user.guild.roles, name="GCI")
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f'GCI `{interaction.user.name}` - `Sunrise` - `{notes}`')
            return

        else:
            await interaction.response.send_message('You are already Sunrise. To update your status use `/gci` to set yourself as sunset', ephemeral=True)

        if state == "Sunset":
            for count, gci in enumerate(self.gci_data):
                if gci["user"] == interaction.user:
                    role = get(gci["user"].guild.roles, name="GCI")
                    await gci["user"].remove_roles(role)
                    self.gci_data.pop(count)
                    await interaction.response.send_message('Gotcha Chief!', ephemeral=True)

        if state == "Refresh" and any(gci["user"] == interaction.user for gci in self.gci_data) == True:
            for gci in self.gci_data:

                if gci["user"] == interaction.user and datetime.now() >= gci["date_refresh_warning"]:
                    gci["date_to_expire"] = datetime.now() + timedelta(hours=1)
                    gci["date_refresh_warning"] = datetime.now() + \
                        timedelta(minutes=30)
                    gci["refresh_warning_sent"] = False
                    await interaction.response.send_message(f'Got it! Your next refresh will be at `{gci["date_to_expire"]:%H:%M}` Zulu', ephemeral=True)
                    return

                else:
                    await interaction.response.send_message(f'Your not inside the refresh period. Your refresh period starts at: `{gci["date_refresh_warning"]:%H:%M}` Zulu', ephemeral=True)
                    return
        if state == "List":
            if len(self.gci_data) == 0:
                await interaction.response.send_message("No GCIs currently online.", ephemeral=True)
                return

            gci_status = ""
            for count, gci in enumerate(self.gci_data):
                gci_status = (
                    gci_status
                    + f"{gci['user']}/{gci['user'].nick} - `{gci['notes']}`\n"
                )
            await interaction.response.send_message(gci_status, ephemeral=True)


def setup(bot):
    bot.add_cog(GCI(bot))
