import json
import nextcord
from nextcord.ext import commands
import aiohttp


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description="Get server status")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def status(self, ctx):
        """Gets the server's mission status"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://levant.limakilo.net/status/data"
            ) as response:
                await ctx.send(ctx.author.mention)
                with open("server_status.json", "wb") as outfile:
                    async for chunk in response.content.iter_chunked(4096):
                        outfile.write(chunk)
                outfile.close()
            await session.close()

        with open("server_status.json") as infile:
            server_data = json.load(infile)
            infile.close()

        friendly_airbases = ""
        enemyAssets = ""

        for airbase in server_data["airbases"]:
            friendly_airbases = friendly_airbases + f"🔵 `{airbase['name']}`\n"

        for assets in server_data["enemyAssets"]:
            if len(assets["assets"]) > 0:
                enemyAssets = enemyAssets + f"🔴 `{assets['name']}`\n"

        active_sams = ""

        for sam in server_data["enemySAMs"]:
            if len(sam["assets"]) > 0:
                for asset in sam["assets"]:
                    active_sams = (
                        active_sams
                        + f"📡 `{asset['codename']} {asset['sitetype']} {sam['name']}`\n"
                    )

        embed = nextcord.Embed(
            title="Server Campaign Status",
            description="Current Lima Kilo Campaign Status, Syria",
            color=0x03B300,
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        embed.add_field(name="Friendly Airbases", value=friendly_airbases, inline=True)
        embed.add_field(name="Hostile Active Regions", value=enemyAssets, inline=True)
        embed.add_field(name="Active SAMs", value=active_sams, inline=True)
        embed.add_field(
            name="Packages in progress",
            value="Package Region / Type / BDA",
            inline=True,
        )

        if len(server_data["missions"]) > 0:

            for mission in server_data["missions"]:

                mission_data = f"{mission['region']} {mission['type']} {mission['target']['status']}%\n"

                for assigned in mission["assigned"]:
                    mission_data = (
                        mission_data
                        + f"`{assigned['player']} - {assigned['aircraft']}`\n"
                    )

                embed.add_field(
                    name=f"📦 {mission['target']['codename']}",
                    value=mission_data,
                    inline=False,
                )

        else:
            embed.add_field(
                name=f"`No Packages are currently scheduled`",
                value="`Sad!`",
                inline=False,
            )
        embed.set_footer(text=f"Generated at: {server_data['date']}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Server(bot))
