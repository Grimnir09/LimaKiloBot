from datetime import datetime, timedelta
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
                    f"{gci['user'].mention} this is your 10 minute refresh warning. \n Your GCI session will end in `30 seconds` \n To refresh your session use `!gci refresh`",
                )

                gci["refresh_warning_sent"] = True

    @commands.command(pass_context=True, description="Assigns and Deligates GCI roles")
    async def gci(self, ctx, state=None, *, notes=None):

        # eq to !gci, get a list of gcis
        if not state and not notes:
            if len(self.gci_data) == 0:
                await ctx.reply("No GCIs currently online.")

            gci_status = ""
            for count, gci in enumerate(self.gci_data):
                gci_status = (
                    gci_status
                    + f"{gci['user']}/{gci['user'].nick} - `{gci['notes']}`\n"
                )
            await ctx.send(gci_status)
            return

        if state.lower() == "sunrise" and ctx.author not in self.gci_data:

            self.gci_data.append(
                {
                    "user": ctx.author,
                    "date_to_expire": datetime.now() + timedelta(hours=1),
                    "date_refresh_warning": datetime.now() + timedelta(minutes=40),
                    "notes": notes,
                    "ctx": ctx,
                    "refresh_warning_sent": False,
                }
            )
            role = get(ctx.guild.roles, name="GCI")
            await ctx.author.add_roles(role)
            await ctx.reply(f"{ctx.author.mention} GCI Sunrise, `{notes}`")

        elif state.lower() == "sunset":
            for count, gci in enumerate(self.gci_data):
                if gci["user"] == ctx.author:
                    role = get(gci["user"].guild.roles, name="GCI")
                    await gci["user"].remove_roles(role)
                    await ctx.message.add_reaction("✅")
                    self.gci_data.pop(count)

        elif (
            state.lower() == "refresh"
            and any(gci["user"] == ctx.author for gci in self.gci_data) == True
            ):
            for gci in self.gci_data:
                if gci["user"] == ctx.author and (
                    datetime.now() >= gci["date_refresh_warning"]
                ):
                    gci["date_to_expire"] = datetime.now() + timedelta(hours=1)
                    gci["date_refresh_warning"] = datetime.now() + timedelta(minutes=30)
                    gci["refresh_warning_sent"] = False
                    await ctx.message.add_reaction("✅")

        # Expose self.gci_data
        elif (
            state.lower() == "debug"
            and ctx.author.guild_permissions.administrator == True
        ):
            embed = nextcord.Embed(
                title=f"GCI Debug",
                description=f"Current Time: `{datetime.now()}`",
                color=0x03B300,
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)

            gci_debug = ""

            for gci in self.gci_data:
                gci_debug = (
                    gci_debug
                    + f"`{gci['user']}`\nExpire:{gci['date_to_expire']}\nRefresh:{gci['date_refresh_warning']}\n"
                )

            embed.add_field(name="GCIs", value=gci_debug)
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(GCI(bot))
