from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.ext.commands.cooldowns import C
from nextcord.utils import get
import nextcord
import json
import pprint


class Flight(commands.Cog):

    '''
    Flight data mock-up

    {'lff': 
        [
            {
                'user': <Member id=106828075274149888 name='Grimnir' discriminator='3890' bot=False nick='Xeraos' guild=<Guild id=358048911144779777 name='emoji' shard_id=0 chunked=True member_count=3>>, 
                'aircraft': 'FA-18C bingus', 
                'notes': None, 
                'flight': None
            }
        ], 
    'flights': [
            {
                'name' : "biguses"
                'lead' : ctx.author
                'members' : [{user, aircraft}]
                'size' : 1
                'flight-Notes' : 'Bingus'
            }
        ]
    }   
    '''

    # init vars and task loops
    def __init__(self, bot):
        self.bot = bot
        self.flight_data = {
            # holding array for pilots looking for flight
            "lff": [],
            # currently existing flights
            "flights": [

            ]
        }
        self.available_aircraft = []
        try:
            with open("available_aircraft.json") as available_aircraft_file:
                self.available_aircraft = json.load(available_aircraft_file)
            print("available_aircraft loaded")
            available_aircraft_file.close()
        except IOError as e:
            print("No available_aircraft.json detected!")
            raise e

    # if for some reason we crash and start up again
    # remove all gci roles from all guilds
    @commands.Cog.listener()
    async def on_ready(self):

        for guild in self.bot.guilds:
            for member in guild.members:
                role = get(member.guild.roles, name="Looking for Flight")
                if role in member.roles:
                    await member.remove_roles(role)

    @commands.group(pass_context=True, description="Flight Main Command")
    async def flight(self, ctx):
        pass

    @flight.command(pass_context=True, description="Find buddies to fly with")
    async def list(self, ctx):
        embed = nextcord.Embed(
            title=f"Users Looking for group",
            description="Note: Information may not be up to date.",
            color=0x03B300,
        )
        embed.set_author(
            name=ctx.author, icon_url=ctx.author.avatar.url)

        pilotsLFF = ''

        if len(self.flight_data['lff']) > 0:
            for pilot in self.flight_data['lff']:
                pilotsLFF = pilotsLFF + \
                    f"`{pilot['user']}` - `{pilot['aircraft']}` - `{pilot['notes']}`\n"
        else:
            pilotsLFF = 'None!'

        embed.add_field(name='Current Pilots LFF',
                        value=pilotsLFF, inline=False)

        for flight in self.flight_data['flights']:

            members_string = ''
            for count, member in enumerate(flight['members'], start=1):
                members_string = members_string + \
                    f'`{flight["name"].capitalize()} 1-{count}` | `{member["user"].name}` - `{member["aircraft"]}`\n'

            flight_string = f'''
            Flight Description: `{flight['notes']}`
            Flight Lead: `{flight['lead']}`
            ***Flight Slots***
            {members_string}
            '''
            embed.add_field(name=flight['name'],
                            value=flight_string, inline=True)

        await ctx.reply(ctx.author.mention, embed=embed)

    @flight.command(pass_context=True, description="Find buddies that are looking for a flight")
    async def lff(self, ctx, aircraft, *, notes=None):
        if not any(user["user"] == ctx.author for user in self.flight_data['lff']):

            if aircraft in self.available_aircraft:
                self.flight_data['lff'].append({
                    "user": ctx.author,
                    "aircraft": aircraft,
                    "notes": notes,
                    "flight": None
                })
                print(self.flight_data)
            else:
                available_aircraft_string = ''
                for available_aircraft in self.available_aircraft:
                    available_aircraft_string = available_aircraft_string + \
                        f'`{available_aircraft}`\n'

                await ctx.reply(
                    f'Please strictly specifify the airframe you wish to sign up with. \nHere is a list of the following available aircraft:\n{available_aircraft_string}\nType `!help lff` for assistance.')

    @flight.command(pass_context=True, description="Create a Flight for people to join.")
    async def create(self, ctx, flight_name: str, flight_size: int, *, flight_notes=None):
        # check to see if the user has an already open flight
        if not any(flight["lead"] == ctx.author for flight in self.flight_data['flights']):

            self.flight_data['flights'].append({
                'name': flight_name,
                'lead': ctx.author,
                'members': [],
                'size': flight_size,
                'notes': flight_notes
            })

            print(self.flight_data['flights'])
            await ctx.message.add_reaction("✅")

    @flight.command(pass_context=True, description="Create a Flight for people to join.")
    async def join(self, ctx, flight_name: str, aircraft: str):
        if any(flight["name"] == flight_name for flight in self.flight_data['flights']):
            for flight in self.flight_data['flights']:
                for member in flight['members']:
                    if ctx.author == member['user']:
                        await ctx.reply(
                            'You are in a Flight already. Please leave using `!leave` before joining another flight.')
                        return

        if aircraft not in self.available_aircraft:
            await ctx.reply(f"{aircraft} is not a invalid aircraft.")
            return

        for flight in self.flight_data['flights']:
            if flight['name'] == flight_name:
                if len(flight['members']) < flight['size']:
                    flight['members'].append(
                        {
                            'user': ctx.author,
                            'aircraft': aircraft
                        }
                    )
                    await ctx.message.add_reaction("✅")
                else:
                    await ctx.reply(
                        f'Flight `{flight_name}` is currently full')


def setup(bot):
    bot.add_cog(Flight(bot))
