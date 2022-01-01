import json
from os import name
import nextcord
from nextcord import message
from nextcord.ext import commands
import aiohttp
import asyncio


class Information(commands.Cog):

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
    async def set_info(self, ctx):
        if ctx.author.guild_permissions.administrator:

            embed = nextcord.Embed(
                title=f"Information Setup",
                description="Below are the currently available subjects.",
                color=0x03B300,
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)

            available_subjects = ""

            for count, subject in enumerate(self.info_data):
                available_subjects = available_subjects + f"{count}. `{subject}`\n"

            embed.add_field(
                name="Subjects",
                value=available_subjects,
                inline=False,
            )

            original_msg = await ctx.send(ctx.author.mention, embed=embed)

            try:
                msg = await self.bot.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author
                    and message.content.lower() in self.info_data,
                )

            except asyncio.TimeoutError:
                embed.set_footer(
                    "Command Timed out after 1 minute, try again!",
                    icon_url=self.bot.user.avatar_url,
                )
                return

            embed.remove_field(0)
            embed.title = f"Information Setup for {msg.content.capitalize()}"
            embed.description = (
                f"Currently available items for `{msg.content.capitalize()}`"
            )

            available_items = ""

            for items in self.info_data[msg.content.lower()]:
                available_items = available_items + f"`{items['Name']}`\n"

            embed.add_field(name="Items", value=available_items, inline=False)

            await original_msg.edit(embed=embed)

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
