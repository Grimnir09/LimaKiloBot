import json
import nextcord
from nextcord.ext import commands


class Information(commands.Cog):
    
    # TODO: Clean up, convert to Slash Commands.
    # Needs clarification on how to use class level vars
    # Inside of a slash option's Choice parameter.

    info_data = None
    lsogrades = None

    def __init__(self, bot):
        self.bot = bot
        try:
            with open("information.json") as infoFile:
                self.info_data = json.load(infoFile)
            print("information loaded")
            infoFile.close()
        except IOError as e:
            print("No information.json detected!")
            raise e

        try:
            with open("lsogrades.json", encoding="utf-8") as lsograde_file:
                self.lsogrades = json.load(lsograde_file)
            print("lsogrades loaded")
            lsograde_file.close()
        except IOError as e:
            print("No information.json detected!")
            raise e

    @commands.command(pass_context=True, description="List carrier information")
    async def info(self, ctx, *, subject: str):

        if subject == "reload" and ctx.author.guild_permissions.administrator:
            try:
                with open("information.json") as infoFile:
                    self.info_data = json.load(infoFile)

                print("information loaded")
                infoFile.close()
                return
            except IOError as e:
                print("No information.json detected!")
                raise e

        embed = nextcord.Embed(
            title=f"{subject.capitalize()} Information",
            description="Note: Information may not be up to date.",
            color=0x03B300,
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)

        subject = subject.lower()
        if subject in self.info_data and subject != "config":
            for item in self.info_data[subject]:
                info = ""
                for k, v in item.items():
                    if k == "Name":
                        continue
                    info = info + f"`{k}: {v}`\n"

                embed.add_field(
                    name=item["Name"],
                    value=info,
                    inline=True,
                )

            await ctx.send(ctx.author.mention, embed=embed)

        else:
            await ctx.send(
                f"{ctx.author.mention} No infomation on `{subject}`, check spelling and try again."
            )

    @commands.command(pass_context=True, description="List carrier information")
    async def lso(self, ctx, *, lsograde):
        lsograde = lsograde.split(" ")
        parsed_grades = {}

        for lsosubgrade in lsograde:
            readout = ""
            for grade, remarks in self.lsogrades.items():
                if grade in lsosubgrade:
                    # print(f"found {grade}")
                    readout = readout + f"{remarks} "
            parsed_grades[lsosubgrade] = readout
        msg = ""
        for lso_raw_grade, description in parsed_grades.items():
            msg = msg + f"`{lso_raw_grade}` - {description}\n"

        embed = nextcord.Embed(
            title=f"LSO Grade Decode",
            description=msg,
            color=0x03B300,
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
